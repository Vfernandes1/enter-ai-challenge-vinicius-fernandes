import json
from pathlib import Path
from app.report_workflow import PortfolioEngine

BASE = Path(__file__).resolve().parent

class Node:
    def __init__(self, name, func, prompt_template=None):
        self.name = name
        self.func = func
        self.prompt_template = prompt_template
        self.output = None

    def run(self, context):
        prompt = self.prompt_template.format(**context) if self.prompt_template else None
        # Simulate LLM latency / reasoning by passing context to the deterministic func
        self.output = self.func(context, prompt)
        return self.output

class SimulatedLLM:
    """A deterministic simulator for LLM-based nodes. It runs provided callables
    which accept the shared context and optional prompt and return structured outputs.
    """
    def __init__(self, engine):
        self.engine = engine
        project_root = BASE.parent
        self.context = {
            'client_data_path': str(project_root / 'app' / 'inputs' / 'client_data.json'),
            'macro_data_path': str(project_root / 'app' / 'inputs' / 'macro_data.json')
        }
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

    def run(self):
        logs = []
        for node in self.nodes:
            out = node.run(self.context)
            logs.append({'node': node.name, 'output': out})
            # merge useful outputs into context for next nodes
            if isinstance(out, dict):
                self.context.update(out)
        return logs

# Node implementation functions - deterministic wrappers over PortfolioEngine

def ingest_node(context, prompt):
    engine = PortfolioEngine(Path(context['client_data_path']), Path(context['macro_data_path']))
    client = engine.client_data
    return {'client_data': client}


def quant_node(context, prompt):
    engine = PortfolioEngine(Path(context['client_data_path']), Path(context['macro_data_path']))
    data = engine.calculate_monthly_profitability()
    return {'portfolio_metrics': {'monthly_return': data['monthly_return'], 'portfolio_value': data['portfolio_value'], 'class_returns': data['class_returns']}}


def research_node(context, prompt):
    engine = PortfolioEngine(Path(context['client_data_path']), Path(context['macro_data_path']))
    macro = engine.evaluate_macro_impact()
    return {'macro_impact': macro}


def advisor_node(context, prompt):
    engine = PortfolioEngine(Path(context['client_data_path']), Path(context['macro_data_path']))
    # Ensure quant and macro have run (they are deterministic so re-running is safe)
    engine.calculate_monthly_profitability()
    engine.evaluate_macro_impact()
    recs = engine.generate_recommendations()
    return {'recommendations': recs}


def formatter_node(context, prompt):
    engine = PortfolioEngine(Path(context['client_data_path']), Path(context['macro_data_path']))
    engine.calculate_monthly_profitability()
    engine.evaluate_macro_impact()
    engine.generate_recommendations()
    # Ensure risk alignment is assessed so the formatter can include the score/note
    try:
        engine.assess_risk_alignment()
    except Exception:
        # fall back silently if the method is missing in older engine versions
        pass
    letter = engine.build_letter()
    # Also write a markdown file for downstream systems
    out_path = BASE / 'simulated_rivet_output.md'
    out_path.write_text(letter, encoding='utf-8')
    return {'final_letter_path': str(out_path), 'final_letter': letter}


def make_workflow():
    # Input files live under the main app/inputs directory
    project_root = BASE.parent
    engine = PortfolioEngine(project_root / 'app' / 'inputs' / 'client_data.json', project_root / 'app' / 'inputs' / 'macro_data.json')
    sim = SimulatedLLM(engine)

    sim.add_node(Node('IngestPortfolio', ingest_node, prompt_template='Ingest client data from {client_data_path}'))
    sim.add_node(Node('QuantMetrics', quant_node, prompt_template='Compute monthly returns and benchmarks'))
    sim.add_node(Node('ResearchMacro', research_node, prompt_template='Analyze macro impact using XP projections'))
    sim.add_node(Node('AdvisorRecommendations', advisor_node, prompt_template='Generate buy/sell/hold recommendations for profile: Moderado'))
    sim.add_node(Node('FormatLetter', formatter_node, prompt_template='Draft final letter in Portuguese, 2 pages max'))

    return sim

if __name__ == '__main__':
    wf = make_workflow()
    logs = wf.run()
    out_file = BASE / 'simulated_rivet_logs.json'
    out_file.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Simulated Rivet workflow finished. Logs written to:', out_file)
    print('Final letter written to:', logs[-1]['output'].get('final_letter_path'))
    # Produce a structured Rivet-like spec capturing prompts and end-state artifacts
    spec = {
        'name': 'XP_Monthly_Report_Rivet_Simulation',
        'description': 'Structured record of nodes, prompt templates and produced artifacts for reproducibility.',
        'nodes': [],
        'artifacts': {
            'logs': str(out_file),
            'final_letter_md': logs[-1]['output'].get('final_letter_path'),
        }
    }

    # Collect node-level metadata from the workflow definition
    for node in wf.nodes:
        spec['nodes'].append({
            'name': node.name,
            'prompt_template': node.prompt_template,
            'produced_output_keys': list((node.output or {}).keys())
        })

    spec_path = BASE / 'rivet_workflow_spec.json'
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding='utf-8')
    yaml_path = BASE / 'rivet_workflow_spec.yaml'
    yaml_lines = [
        f"name: {spec['name']}",
        f"description: {spec['description']}",
        "nodes:",
    ]
    for node in spec['nodes']:
        yaml_lines.extend([
            "  - name: {}".format(node['name']),
            "    prompt_template: '{}'".format(node['prompt_template'].replace("'", "\'")) if node['prompt_template'] else "    prompt_template: null",
            "    produced_output_keys:",
        ])
        for key in node['produced_output_keys']:
            yaml_lines.append(f"      - {key}")
    yaml_lines.extend([
        "artifacts:",
        f"  logs: {spec['artifacts']['logs']}",
        f"  final_letter_md: {spec['artifacts']['final_letter_md']}",
    ])
    yaml_path.write_text("\n".join(yaml_lines), encoding='utf-8')
    print('Rivet simulation spec written to:', spec_path)
    print('Rivet simulation YAML written to:', yaml_path)
