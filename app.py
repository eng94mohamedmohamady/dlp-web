from flask import Flask, request, render_template_string
import re, os, datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔹 Patterns
PATTERNS = {
    "EMAIL": r"[\w\.-]+@[\w\.-]+\.\w+",
    "PHONE": r"\b\d{10,15}\b",
    "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
    "MRN": r"\bMRN\d{5,10}\b"
}

def scan_text(text):
    findings = []
    for name, pattern in PATTERNS.items():
        matches = re.findall(pattern, text)
        if matches:
            findings.append({name: matches})
    return findings

def log_to_file(findings):
    with open("alerts.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {findings}\n")

# 🔹 HTML Templates inline
INDEX_HTML = """
<h2>Upload File for DLP Scan</h2>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Scan</button>
</form>
"""

RESULT_HTML = """
<h2>DLP Scan Results</h2>
{% if findings %}
    <h3 style="color:red;">Sensitive Data Found!</h3>
    <ul>
    {% for item in findings %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
{% else %}
    <h3 style="color:green;">No sensitive data detected.</h3>
{% endif %}
<a href="/">Scan another file</a>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            with open(filepath, "r") as f:
                content = f.read()

            findings = scan_text(content)

            if findings:
                log_to_file(findings)

            return render_template_string(RESULT_HTML, findings=findings)

    return render_template_string(INDEX_HTML)


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)