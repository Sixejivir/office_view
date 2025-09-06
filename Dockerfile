# Resmi Python imajı kullan
FROM python:3.11-slim

# Sistem paketleri ve LibreOffice
RUN apt-get update && apt-get install -y \
    libreoffice-core libreoffice-writer libreoffice-impress \
    libxrender1 libxext6 libx11-6 fonts-dejavu \
    curl git unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Upload klasörü
RUN mkdir -p uploads

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
