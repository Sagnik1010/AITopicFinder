from flask import Flask, render_template_string, request
import subprocess
import os
import sys

app = Flask(__name__)

# Paths
BASE_DIR = os.path.join(os.path.dirname(__file__), "rag-based-ai-2a690d3f7a3c6d1ee227678f684f6af045457418")
PROCESS_SCRIPT = os.path.join(BASE_DIR, "process_incoming.py")
RESPONSE_FILE = os.path.join(BASE_DIR, "response.txt")

# HTML Template for the UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RAG-Based AI Web Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #f8f9fa; }
        h1 { color: #333; }
        textarea { width: 100%; height: 120px; margin-top: 10px; }
        pre { background: #fff; padding: 15px; border-radius: 5px; white-space: pre-wrap; }
        button { background-color: #007BFF; color: white; padding: 10px 20px;
                 border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <h1>RAG-Based AI Web Interface</h1>
    <form method="POST">
        <label>Ask your question:</label>
        <textarea name="query" placeholder="Type your question here..."></textarea>
        <br><br>
        <button type="submit">Submit</button>
    </form>
    {% if output %}
        <h2>Response:</h2>
        <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output_text = ""

    if request.method == "POST":
        user_input = request.form.get("query", "").strip()

        if user_input:
            try:
                # Run process_incoming.py with the user query
                subprocess.run(
                    [sys.executable, PROCESS_SCRIPT, user_input],
                    check=True
                )

                # After script runs, read response.txt
                if os.path.exists(RESPONSE_FILE):
                    with open(RESPONSE_FILE, "r", encoding="utf-8") as f:
                        output_text = f.read().strip()
                else:
                    output_text = "⚠️ No response.txt file found after execution."

            except subprocess.CalledProcessError as e:
                output_text = f"❌ Error running process_incoming.py: {e}"

        else:
            output_text = "Please enter a question before submitting."

    return render_template_string(HTML_TEMPLATE, output=output_text)

if __name__ == "__main__":
    app.run(debug=True)
