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
ALLOWED_EXTENSIONS = ('.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.txt')

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya adı boş'}), 400

    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return jsonify({'error': f'Desteklenmeyen dosya türü: {file_ext}'}), 400

    unique_id = str(uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}{file_ext}")
    file.save(input_path)

    pdf_output_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}.pdf")

    try:
        # Dönüştürme komutu
        convert_cmd = [
            SOFFICE_PATH,
            '--headless',
            '--norestore',
            '--convert-to',
            'pdf',
            input_path,
            '--outdir',
            UPLOAD_FOLDER
        ]

        # Excel için özel filtre
        if file_ext in ('.xls', '.xlsx'):
            convert_cmd[4] = 'pdf:calc_pdf_Export'

        result = subprocess.run(
            convert_cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            app.logger.error(f"LibreOffice hatası:\nstdout: {result.stdout}\nstderr: {result.stderr}")
            return jsonify({'error': 'PDF oluşturulamadı (LibreOffice hatası)'}), 500

        if not os.path.exists(pdf_output_path):
            app.logger.error(f"PDF bulunamadı.\nstdout: {result.stdout}\nstderr: {result.stderr}")
            return jsonify({'error': 'PDF oluşturulamadı'}), 500

        return send_file(pdf_output_path, as_attachment=True)

    except Exception as e:
        app.logger.error(f"Hata: {str(e)}")
        return jsonify({'error': 'Dönüşümde bir hata oluştu'}), 500

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(pdf_output_path):
            os.remove(pdf_output_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
