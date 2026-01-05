from flask import Flask, render_template, request, send_file
from crypto_utils import encrypt_file, decrypt_file
from io import BytesIO
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        file = request.files["file"]
        if file:
            encrypted = encrypt_file(file.read())
            filename = file.filename + ".enc"
            with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
                f.write(encrypted)
            message = "✅ File uploaded, encrypted, and saved successfully"

    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", message=message, files=files)

@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, "rb") as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(encrypted_data)
    original_name = filename.replace(".enc", "")

    return send_file(
        BytesIO(decrypted_data),
        as_attachment=True,
        download_name=original_name
    )

if __name__ == "__main__":
    app.run(debug=True)


