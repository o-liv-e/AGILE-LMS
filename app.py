
import os
from pathlib import Path
from flask import Flask, request, redirect, url_for, send_from_directory, abort, render_template_string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
VERSION = os.getenv("APP_VERSION", "v1")
ALLOWED = {".pdf", ".txt", ".doc", ".docx", ".ppt", ".pptx"}

PAGE = """
<!doctype html>
<html>
<head>
<title>LMS - {{ version }}</title>
<style>
body{font-family:Arial;max-width:720px;margin:50px auto;padding:20px;background:#f4f7fb}
main{background:white;padding:30px;border-radius:12px}
h1{color:#244a80}button{padding:10px 16px;background:#244a80;color:white;border:0;border-radius:5px}
</style>
</head>
<body><main>
<h1>Learning Management System</h1>
<h3>{{ heading }}</h3>
<p>Current version: {{ version }}</p>
{% if version == "v1" %}
<form method="post" enctype="multipart/form-data">
<input type="file" name="note" required>
<button type="submit">Upload Notes</button>
</form>
<p>{{ message }}</p>
{% elif version == "v2" %}
<ul>{% for file in files %}<li>{{ file }}</li>{% else %}<li>No notes uploaded yet.</li>{% endfor %}</ul>
{% elif version == "v3" %}
<ul>{% for file in files %}
<li>{{ file }} — <a href="{{ url_for('download', filename=file) }}">Download</a></li>
{% else %}<li>No notes available.</li>{% endfor %}</ul>
{% endif %}
</main></body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if VERSION == "v1" and request.method == "POST":
        uploaded = request.files.get("note")
        if not uploaded or not uploaded.filename:
            abort(400)
        filename = secure_filename(uploaded.filename)
        if not filename or Path(filename).suffix.lower() not in ALLOWED:
            return render_template_string(PAGE, version=VERSION, heading="Upload Notes",
                                          files=[], message="Unsupported file type."), 400
        uploaded.save(DATA_DIR / filename)
        message = f"Uploaded successfully: {filename}"
    files = sorted(p.name for p in DATA_DIR.iterdir() if p.is_file())
    headings = {"v1": "Upload Notes", "v2": "View Notes", "v3": "Download Notes"}
    return render_template_string(PAGE, version=VERSION,
                                  heading=headings.get(VERSION, "LMS"),
                                  files=files, message=message)

@app.route("/download/<path:filename>")
def download(filename):
    if VERSION != "v3":
        abort(404)
    safe_name = secure_filename(filename)
    if not safe_name or not (DATA_DIR / safe_name).is_file():
        abort(404)
    return send_from_directory(DATA_DIR, safe_name, as_attachment=True)

@app.route("/health")
def health():
    return {"status": "healthy", "version": VERSION}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
