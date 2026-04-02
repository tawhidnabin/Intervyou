#!/bin/bash
# ============================================================
# IntervYou — AWS EC2 Setup Script (t3.large, Ubuntu 22.04)
# SSH into your EC2 instance and run:
#   curl -fsSL https://raw.githubusercontent.com/tawhidnabin/Intervyou/main/deploy/aws-setup.sh | bash
# ============================================================

set -e

echo "========================================="
echo "  IntervYou Backend — AWS EC2 Setup"
echo "========================================="

echo ""
echo "=== 1. Updating system ==="
sudo apt update && sudo apt upgrade -y

echo ""
echo "=== 2. Installing Python 3.11 ==="
sudo apt install -y python3.11 python3.11-venv python3-pip python3.11-dev build-essential

echo ""
echo "=== 3. Installing ffmpeg (for Whisper) ==="
sudo apt install -y ffmpeg

echo ""
echo "=== 4. Installing Nginx ==="
sudo apt install -y nginx

echo ""
echo "=== 5. Installing Ollama ==="
curl -fsSL https://ollama.com/install.sh | sh

echo ""
echo "=== 6. Pulling qwen3:8b model (this takes a few minutes) ==="
ollama pull qwen3:8b

echo ""
echo "=== 7. Cloning project ==="
cd /home/ubuntu
git clone https://github.com/tawhidnabin/Intervyou.git
cd Intervyou

echo ""
echo "=== 8. Setting up Python virtual environment ==="
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
pip install gunicorn

echo ""
echo "=== 9. Creating environment file ==="
JWT_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
cat > backend/.env << EOF
JWT_SECRET_KEY=${JWT_KEY}
FRONTEND_URL=https://intervyou.vercel.app
FLASK_ENV=production
EOF
echo "Created backend/.env"

echo ""
echo "=== 10. Initializing database ==="
cd backend
source ../venv/bin/activate
python3 -c "from app import create_app; create_app()"
cd ..

echo ""
echo "=== 11. Setting up systemd services ==="
sudo cp deploy/intervyou-aws.service /etc/systemd/system/intervyou.service
sudo systemctl daemon-reload
sudo systemctl enable intervyou
sudo systemctl start intervyou

echo ""
echo "=== 12. Configuring Nginx ==="
sudo cp deploy/nginx-aws.conf /etc/nginx/sites-available/intervyou
sudo ln -sf /etc/nginx/sites-available/intervyou /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo ""
echo "=== 13. Enabling Ollama on boot ==="
sudo systemctl enable ollama

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Backend running at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/api/health"
echo ""
echo "Next steps:"
echo "1. Update your Vercel frontend environment.prod.ts with this IP"
echo "2. Update backend/.env FRONTEND_URL with your Vercel URL"
echo "3. Restart: sudo systemctl restart intervyou"
echo ""
