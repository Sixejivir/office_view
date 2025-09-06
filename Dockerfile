# Temel imaj
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Sistem paketleri ve LibreOffice kurulumu
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libreoffice-core libreoffice-writer libreoffice-impress \
    libxrender1 libxext6 libx11-6 fonts-dejavu \
    curl git unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python bağımlılıkları (pip upgrade yok)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Upload klasörü
RUN mkdir -p uploads

# Port
EXPOSE 5000

# Başlatma komutu
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
