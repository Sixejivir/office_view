# Temel imaj
FROM ubuntu:24.04

# Ortam değişkenleri
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Sistem paketleri ve LibreOffice kurulumu
RUN apt-get update && apt-get install -y \
    python3 python3-venv python3-pip \
    libreoffice-core libreoffice-writer libreoffice-impress \
    libxrender1 libxext6 libx11-6 fonts-dejavu \
    curl git unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıkları
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Upload klasörü
RUN mkdir -p uploads

# Port
EXPOSE 5000

# Başlatma komutu
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
