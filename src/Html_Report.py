import datetime


def export_html_report(final_report, output_path):
    project = final_report["project_profile"]
    billing = final_report["billing"]
    analysis = final_report["analysis"]
    recommendations = final_report["recommendations"]

    # ------------------ Pre-computed values (IMPORTANT) ------------------
    total_cost = analysis["total_cost"]
    budget = analysis["budget"]
    variance = total_cost - budget
    is_over = analysis["is_over_budget"]

    status_text = "Over Budget" if is_over else "Within Budget"
    status_class = "bad" if is_over else "good"

    summary = recommendations["summary"]
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # ------------------ HTML ------------------
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Cloud Cost Optimization Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 20px;
}}
h1, h2, h3 {{
    color: #1f2937;
}}
.section {{
    background: #ffffff;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}}
table {{
    width: 100%;
    border-collapse: collapse;
}}
th, td {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}
th {{
    background: #eef2f7;
}}
.good {{
    color: #047857;
    font-weight: bold;
}}
.bad {{
    color: #b91c1c;
    font-weight: bold;
}}
.card {{
    background: #f9fafb;
    padding: 15px;
    margin-bottom: 15px;
    border-left: 5px solid #2563eb;
    border-radius: 5px;
}}
.footer {{
    text-align: center;
    font-size: 12px;
    color: #6b7280;
    margin-top: 30px;
}}
</style>
</head>

<body>

<h1>Cloud Cost Optimization Report</h1>
<p><strong>Generated on:</strong> {now}</p>

<div class="section">
<h2>Project Overview</h2>
<p><strong>Project Name:</strong> {project["name"]}</p>
<p><strong>Description:</strong> {project["description"]}</p>
<p><strong>Monthly Budget:</strong> ₹{project["budget_inr_per_month"]}</p>
</div>

<div class="section">
<h2>Tech Stack</h2>
<ul>
"""
    for k, v in project["tech_stack"].items():
        html += f"<li><strong>{k}</strong>: {v}</li>"

    html += """
</ul>
</div>

<div class="section">
<h2>Synthetic Billing Details</h2>
<table>
<tr>
<th>Service</th>
<th>Purpose</th>
<th>Usage</th>
<th>Region</th>
<th>Cost (₹)</th>
</tr>
"""

    for b in billing:
        html += f"""
<tr>
<td>{b['service']}</td>
<td>{b['serves']}</td>
<td>{b['usage_quantity']} {b['unit']}</td>
<td>{b['region']}</td>
<td>{b['cost_inr']}</td>
</tr>
"""

    html += f"""
</table>
</div>

<div class="section">
<h2>Cost Summary</h2>
<p><strong>Total Monthly Cost:</strong> ₹{total_cost}</p>
<p><strong>Budget:</strong> ₹{budget}</p>
<p><strong>Variance:</strong> ₹{variance}</p>
<p>
<strong>Status:</strong>
<span class="{status_class}">
{status_text}
</span>
</p>
</div>

<div class="section">
<h2>Cost Optimization Recommendations</h2>
"""

    for r in recommendations["recommendations"]:
        html += f"""
<div class="card">
<h3>{r["title"]}</h3>
<p><strong>Service:</strong> {r["service"]}</p>
<p><strong>Current Cost:</strong> ₹{r["current_cost"]}</p>
<p><strong>Potential Savings:</strong> ₹{r["potential_savings"]}</p>
<p><strong>Type:</strong> {r["recommendation_type"]}</p>
<p><strong>Implementation Effort:</strong> {r["implementation_effort"]}</p>
<p><strong>Risk Level:</strong> {r["risk_level"]}</p>
<p>{r["description"]}</p>
</div>
"""

    html += f"""
</div>

<div class="section">
<h2>Final Summary</h2>
<ul>
<li><strong>Total Services Analyzed:</strong> {len(billing)}</li>
<li><strong>Total Recommendations:</strong> {summary["recommendations_count"]}</li>
<li><strong>Total Potential Savings:</strong> ₹{summary["total_potential_savings"]}</li>
<li><strong>Savings Percentage:</strong> {round(summary["savings_percentage"], 2)}%</li>
</ul>

<p>
<strong>Overall Outcome:</strong>
<span class="{ 'good' if not is_over else 'bad' }">
{"Cost Optimized" if not is_over else "Cost Optimization Required"}
</span>
</p>
</div>

<div class="footer">
<p>© 2025 OpenText — AI-Powered Cloud Cost Optimizer</p>
</div>

</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
