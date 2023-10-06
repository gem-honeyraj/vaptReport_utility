from flask import Flask, request, render_template, make_response
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 


@app.route('/render', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        data = request.get_json()
        print("---")
        print(data)
        projectName = data.get("projectName", 'Default Project')
        projectUrl = data.get("projectUrl",'https://www.google.com')
        date = data.get("date")
        performedBy = data.get("performedBy")
        itration = data.get("itration")
        azureLink = data.get('azureLink')
        vulnerabilities = data.get('vulnerabilities', [])
        severity_counts = {'low': 0, 'medium': 0, 'high': 0}
        vulnerability_details = {'low': [], 'medium': [], 'high': []}
        vulnerability_names = {'low': [], 'medium': [], 'high': []}

        for vulnerability in vulnerabilities:
            severity = vulnerability['severity']
            severity_counts[severity] += 1
            details = {k: v for k, v in vulnerability.items() if k != 'severity'}
            vulnerability_details[severity].append(details)
            vulnerability_names[severity].append(vulnerability['vulnerability'])

        # default_severity_counts = {'low': 1, 'medium': 1, 'high': 1}
        # severity_counts = {k: severity_counts.get(k, default_severity_counts[k]) for k in default_severity_counts}



        rendered_html = render_template('vapt_report.html', projectName=projectName, projectUrl=projectUrl, severity_counts=severity_counts, vulnerability_details=vulnerability_details, vulnerability_names=vulnerability_names,date=date,performedBy=performedBy,itration=itration,azureLink=azureLink)

        return rendered_html
        
    return 'Hey, send a POST request with valid JSON to generate the report.'



if __name__ == '__main__':
    app.run(debug=True)
