"""Generate evaluation dashboard HTML."""

import json
from pathlib import Path
from datetime import datetime


def generate_dashboard():
    """Generate HTML dashboard from evaluation results."""

    # Load results
    eval_dir = Path("experiments/evaluation")

    ragas_summary = {}
    llm_judge_summary = {}

    if (eval_dir / "llm_judge_summary.json").exists():
        with open(eval_dir / "llm_judge_summary.json", 'r') as f:
            llm_judge_summary = json.load(f)

    # Generate HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Agent System - Evaluation Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
        }}
        .metric-label {{
            color: #666;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .score-bar {{
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
        }}
        .timestamp {{
            color: #999;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Multi-Agent System Evaluation Dashboard</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-value">{llm_judge_summary.get('avg_overall', 0):.1f}</div>
            <div class="metric-label">Overall Quality Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{llm_judge_summary.get('avg_accuracy', 0):.1f}</div>
            <div class="metric-label">Accuracy Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{llm_judge_summary.get('avg_relevance', 0):.1f}</div>
            <div class="metric-label">Relevance Score</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{llm_judge_summary.get('score_distribution', {}).get('excellent (8-10)', 0)}</div>
            <div class="metric-label">Excellent Responses</div>
        </div>
    </div>

    <div class="section">
        <h2>Quality Metrics</h2>
        <div>
            <strong>Accuracy</strong>
            <div class="score-bar">
                <div class="score-fill" style="width: {llm_judge_summary.get('avg_accuracy', 0)*10}%"></div>
            </div>
        </div>
        <div>
            <strong>Relevance</strong>
            <div class="score-bar">
                <div class="score-fill" style="width: {llm_judge_summary.get('avg_relevance', 0)*10}%"></div>
            </div>
        </div>
        <div>
            <strong>Completeness</strong>
            <div class="score-bar">
                <div class="score-fill" style="width: {llm_judge_summary.get('avg_completeness', 0)*10}%"></div>
            </div>
        </div>
        <div>
            <strong>Clarity</strong>
            <div class="score-bar">
                <div class="score-fill" style="width: {llm_judge_summary.get('avg_clarity', 0)*10}%"></div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>Score Distribution</h2>
        <ul>
            <li>Excellent (8-10): {llm_judge_summary.get('score_distribution', {}).get('excellent (8-10)', 0)}</li>
            <li>Good (6-8): {llm_judge_summary.get('score_distribution', {}).get('good (6-8)', 0)}</li>
            <li>Fair (4-6): {llm_judge_summary.get('score_distribution', {}).get('fair (4-6)', 0)}</li>
            <li>Poor (0-4): {llm_judge_summary.get('score_distribution', {}).get('poor (0-4)', 0)}</li>
        </ul>
    </div>

    <div class="section">
        <h2>System Information</h2>
        <p><strong>Evaluation Framework:</strong> Ragas + LLM-as-Judge</p>
        <p><strong>Safety:</strong> Guardrails Enabled (PII, Prompt Injection, Hallucination Detection)</p>
        <p><strong>Observability:</strong> Phoenix Tracing</p>
    </div>
</body>
</html>
"""

    # Save dashboard
    output_path = Path("experiments/dashboard.html")
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"✓ Dashboard generated: {output_path}")
    print(f"Open in browser: file://{output_path.absolute()}")


if __name__ == "__main__":
    generate_dashboard()