#!/bin/bash
# ============================================================
# IntervYou — Oracle Cloud VM Setup Script
# Run this on your Oracle Cloud ARM instance (Ubuntu 22.04)
# ============================================================

set -e

echo "=== Updating system ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing Python 3.11 + pip ==="
sudo apt install -y python3.11 python3.11-venv python3-pip python3.11-dev

echo "=== Installing ffmpeg (for Whisper) ==="
sudo apt install -y ffmpeg

echo "=== Installing Node.js 20 (for building frontend if needed) ==="
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

echo "=== Installing Nginx (reverse proxy) ==="
sudo apt install -y nginx

echo "=== Installing Certbot (SSL) ==="
sudo apt install -y certbot python3-certbot-nginx

echo "=== Installing Ollama ==="
curl -fsSL https://ollama.com/install.sh | sh

echo "=== Pulling qwen3:8b model ==="
ollama pull qwen3:8b

echo "=== Cloning project ==="
cd /home/ubuntu
git clone https://github.com/tawhidnabin/Intervyou.git
cd Intervyou

echo "=== Setting up Python virtual environment ==="
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install gunicorn imageio-ffmpeg

echo "=== Creating .env file ==="
cat > backend/.env << 'EOF'
FLASK_ENV=production
JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
SQLALCHEMY_DATABASE_URI=sqlite:///intervyou.db
EOF

echo "=== Setup complete! ==="
echo "Next steps:"
echo "1. Configure Nginx: sudo cp deploy/nginx.conf /etc/nginx/sites-available/intervyou"
echo "2. Enable site: sudo ln -s /etc/nginx/sites-available/intervyou /etc/nginx/sites-enabled/"
echo "3. Remove default: sudo rm /etc/nginx/sites-enabled/default"
echo "4. Start services: sudo systemctl start intervyou ollama"
echo "5. Enable on boot: sudo systemctl enable intervyou ollama nginx"
