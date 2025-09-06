FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Sistem paketleri ve LibreOffice kurulumu
RUN apt-get update && apt-get install -y \
    python3 python3-venv python3-pip \
    libreoffice-core libreoffice-writer libreoffice-impress \
    libxrender1 libxext6 libx11-6 fonts-dejavu \
    curl git unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Virtual environment oluştur
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Python bağımlılıklarını venv içine kur
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Upload klasörü
RUN mkdir -p uploads

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
