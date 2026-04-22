from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

INDEX_HTML = "<h1>Hello World</h1>"
RESULT_HTML = "<h1>Result Page</h1>"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return render_template_string(RESULT_HTML)
    return render_template_string(INDEX_HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))