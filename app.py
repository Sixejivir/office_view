import os
import subprocess
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

SOFFICE_PATH = '/usr/bin/soffice'  # Ubuntu container içindeki path

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya adı boş'}), 400

    unique_id = str(uuid4())
    file_ext = os.path.splitext(file.filename)[1]
    pptx_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}{file_ext}")
    file.save(pptx_path)

    pdf_output_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.pdf")

    try:
        subprocess.run(
            [
                SOFFICE_PATH,
                '--headless',
                '--convert-to',
                'pdf',
                pptx_path,
                '--outdir',
                UPLOAD_FOLDER
            ],
            check=True,
            capture_output=True,
            text=True
        )

        if not os.path.exists(pdf_output_path):
            app.logger.error(f"PDF oluşturulamadı. stdout: {pptx_path}")
            return jsonify({'error': 'PDF oluşturulamadı'}), 500

        return send_file(pdf_output_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        app.logger.error(f"LibreOffice hatası: {e.stdout} {e.stderr}")
        return jsonify({'error': 'Dönüşümde bir aksilik oldu'}), 500

    finally:
        if os.path.exists(pptx_path):
            os.remove(pptx_path)
