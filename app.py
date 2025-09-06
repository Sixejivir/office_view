import os
import subprocess
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert-to-pdf', methods=['POST'])
def convert_to_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya adı boş'}), 400

    pptx_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pptx_path)

    pdf_output_path = os.path.splitext(pptx_path)[0] + '.pdf'

    try:
        subprocess.run(
            [
                'libreoffice',
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

        return send_file(pdf_output_path, as_attachment=True)

    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e.stdout} {e.stderr}")
        return jsonify({'error': 'Dönüşümde bir aksilik oldu'}), 500

    finally:
        os.remove(pptx_path)
        if os.path.exists(pdf_output_path):
            os.remove(pdf_output_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
