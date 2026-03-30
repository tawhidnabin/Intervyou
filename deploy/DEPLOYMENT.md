# IntervYou Deployment Guide
## Vercel (Frontend) + Oracle Cloud (Backend)

---

## Part 1: Deploy Frontend to Vercel (5 minutes)

### Step 1: Create Vercel Account
1. Go to https://vercel.com and sign up with your GitHub account

### Step 2: Import Project
1. Click "Add New Project"
2. Select your GitHub repo: `tawhidnabin/Intervyou`
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `intervyou-frontend`
   - **Build Command**: `npx ng build --configuration production`
   - **Output Directory**: `dist/intervyou-frontend/browser`
4. Click "Deploy"

### Step 3: Update API URL
After deploying the backend (Part 2), come back and:
1. Go to your Vercel project → Settings → Environment Variables
2. Add: `API_URL` = `http://YOUR_ORACLE_VM_IP`
3. Or edit `intervyou-frontend/src/environments/environment.prod.ts` with your VM IP
4. Push to GitHub → Vercel auto-redeploys

Your frontend will be live at: `https://intervyou-xxx.vercel.app`

---

## Part 2: Deploy Backend to Oracle Cloud (30 minutes)

### Step 1: Create Oracle Cloud Account
1. Go to https://cloud.oracle.com and create a free account
2. You get the Always Free tier (never expires)

### Step 2: Create ARM VM Instance
1. Go to Compute → Instances → Create Instance
2. Configure:
   - **Name**: intervyou-backend
   - **Image**: Ubuntu 22.04 (Canonical)
   - **Shape**: Click "Change Shape" → Ampere (ARM) → VM.Standard.A1.Flex
   - **OCPUs**: 4 (free tier allows up to 4)
   - **Memory**: 24 GB (free tier allows up to 24)
   - **Boot volume**: 100 GB
3. **Networking**: Create new VCN or use default
4. **SSH Key**: Upload your public key or generate one
   - If you don't have one: `ssh-keygen -t rsa -b 4096` in your terminal
5. Click "Create"

### Step 3: Open Firewall Ports
1. Go to your instance → Virtual Cloud Network → Security Lists
2. Add Ingress Rules:
   - Port 80 (HTTP): Source 0.0.0.0/0, TCP, Port 80
   - Port 443 (HTTPS): Source 0.0.0.0/0, TCP, Port 443
3. Also open the OS firewall on the VM (after SSH):
   ```bash
   sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT
   sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT
   sudo netfilter-persistent save
   ```

### Step 4: SSH into Your VM
```bash
ssh -i your-key.pem ubuntu@YOUR_VM_PUBLIC_IP
```

### Step 5: Run Setup Script
```bash
# Download and run the setup script
curl -fsSL https://raw.githubusercontent.com/tawhidnabin/Intervyou/main/deploy/oracle-setup.sh | bash
```

Or manually:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip python3.11-dev ffmpeg nginx certbot python3-certbot-nginx

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3:8b

# Clone project
cd /home/ubuntu
git clone https://github.com/tawhidnabin/Intervyou.git
cd Intervyou

# Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install gunicorn imageio-ffmpeg
```

### Step 6: Configure Environment
```bash
# Create .env file
cat > /home/ubuntu/Intervyou/backend/.env << EOF
JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
FRONTEND_URL=https://your-vercel-app.vercel.app
EOF
```

### Step 7: Build Frontend (serve from same VM)
If you want to serve the frontend from the same VM instead of Vercel:
```bash
cd /home/ubuntu/Intervyou/intervyou-frontend

# Edit environment.prod.ts to point to same server
# apiUrl should be '/api' (relative, since Nginx proxies it)

npm install
npx ng build --configuration production
cp -r dist/intervyou-frontend/browser /home/ubuntu/Intervyou/frontend-dist
```

### Step 8: Configure Nginx
```bash
sudo cp /home/ubuntu/Intervyou/deploy/nginx.conf /etc/nginx/sites-available/intervyou

# Edit the config — replace YOUR_DOMAIN_OR_IP with your VM's public IP
sudo nano /etc/nginx/sites-available/intervyou

sudo ln -s /etc/nginx/sites-available/intervyou /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: Setup Systemd Service
```bash
sudo cp /home/ubuntu/Intervyou/deploy/intervyou.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start intervyou
sudo systemctl enable intervyou

# Check it's running
sudo systemctl status intervyou
```

### Step 10: Start Ollama on Boot
```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

### Step 11: Verify
```bash
# Test backend
curl http://localhost:5000/api/health

# Test from outside
curl http://YOUR_VM_PUBLIC_IP/api/health
```

---

## Part 3: Connect Frontend to Backend

### Option A: Frontend on Vercel + Backend on Oracle
1. Edit `intervyou-frontend/src/environments/environment.prod.ts`:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'http://YOUR_ORACLE_VM_IP/api'
   };
   ```
2. Push to GitHub → Vercel auto-redeploys
3. Update backend `.env`: `FRONTEND_URL=https://your-app.vercel.app`
4. Restart backend: `sudo systemctl restart intervyou`

### Option B: Both on Oracle VM (simpler)
1. Edit `intervyou-frontend/src/environments/environment.prod.ts`:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: '/api'  // relative URL, Nginx proxies to Flask
   };
   ```
2. Build frontend on the VM and serve via Nginx (Step 7 above)
3. Everything runs on one server, one IP

---

## Optional: Add SSL (HTTPS)
If you have a domain name pointing to your VM:
```bash
sudo certbot --nginx -d yourdomain.com
```
This auto-configures HTTPS with a free Let's Encrypt certificate.

---

## Updating the App
```bash
ssh ubuntu@YOUR_VM_IP
cd /home/ubuntu/Intervyou
git pull origin main
source venv/bin/activate
pip install -r backend/requirements.txt
sudo systemctl restart intervyou

# If frontend changed:
cd intervyou-frontend
npm install
npx ng build --configuration production
cp -r dist/intervyou-frontend/browser /home/ubuntu/Intervyou/frontend-dist
sudo systemctl restart nginx
```

---

## Cost Summary
| Resource | Cost |
|----------|------|
| Oracle Cloud ARM VM (4 OCPU, 24GB RAM) | Free forever |
| Vercel frontend hosting | Free |
| Domain name (optional) | ~$10/year |
| SSL certificate (Let's Encrypt) | Free |
| **Total for 2 months** | **$0** |
