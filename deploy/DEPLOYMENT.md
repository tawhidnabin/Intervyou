# IntervYou Deployment Guide
## Frontend: Vercel (free) | Backend: AWS EC2 t3.large ($27/month)

---

## Part 1: Create EC2 Instance (10 minutes)

### Step 1: Launch Instance
1. Go to AWS Console → EC2 → Launch Instance
2. Configure:
   - **Name**: `intervyou-backend`
   - **AMI**: Ubuntu Server 22.04 LTS (64-bit ARM or x86)
   - **Instance type**: `t3.large` (2 vCPU, 8GB RAM)
   - **Key pair**: Create new or select existing (download the .pem file)
   - **Network**: Allow SSH (port 22), HTTP (port 80), HTTPS (port 443)
     - Check "Allow SSH traffic"
     - Check "Allow HTTP traffic from the internet"
     - Check "Allow HTTPS traffic from the internet"
   - **Storage**: 30 GB gp3
3. Click "Launch Instance"

### Step 2: SSH into Your Instance
```bash
# Make key readable
chmod 400 your-key.pem

# Connect (replace with your instance's public IP)
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3: Run Setup Script
```bash
curl -fsSL https://raw.githubusercontent.com/tawhidnabin/Intervyou/main/deploy/aws-setup.sh | bash
```

This automatically:
- Installs Python 3.11, ffmpeg, Nginx
- Installs Ollama + pulls qwen3:8b model
- Clones your repo
- Creates Python venv + installs all dependencies
- Sets up systemd service (auto-start on reboot)
- Configures Nginx reverse proxy
- Initializes the database with 21 questions

### Step 4: Verify
```bash
curl http://localhost/api/health
# Should return: {"status":"ok"}
```

From your browser, visit: `http://YOUR_EC2_PUBLIC_IP/api/health`

---

## Part 2: Deploy Frontend to Vercel (5 minutes)

### Step 1: Go to vercel.com, sign in with GitHub

### Step 2: Import `tawhidnabin/Intervyou`

### Step 3: Configure:
- **Root Directory**: `intervyou-frontend`
- **Install Command**: `npm install`
- **Build Command**: `npm run build`
- **Output Directory**: `dist/intervyou-frontend/browser`

### Step 4: Deploy

Your frontend URL: `https://intervyou-xxx.vercel.app`

---

## Part 3: Connect Frontend to Backend

### On your local machine:
1. Edit `intervyou-frontend/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'http://YOUR_EC2_PUBLIC_IP/api'
};
```
2. Commit and push:
```bash
git add -A && git commit -m "Set production API URL" && git push
```
3. Vercel auto-redeploys

### On your EC2 instance:
```bash
# Update the allowed frontend URL
sudo nano /home/ubuntu/Intervyou/backend/.env
# Change FRONTEND_URL to your Vercel URL

# Restart
sudo systemctl restart intervyou
```

---

## Useful Commands (on EC2)

```bash
# Check backend status
sudo systemctl status intervyou

# View backend logs
sudo journalctl -u intervyou -f

# Restart backend
sudo systemctl restart intervyou

# Check Ollama status
sudo systemctl status ollama

# Update code from GitHub
cd /home/ubuntu/Intervyou
git pull origin main
source venv/bin/activate
pip install -r backend/requirements.txt
sudo systemctl restart intervyou

# Check disk space
df -h

# Check memory usage
free -h
```

---

## Cost Breakdown (1 month)

| Resource | Cost |
|----------|------|
| EC2 t3.large (730 hours) | ~$27 |
| EBS 30GB gp3 storage | ~$3 |
| Data transfer (first 100GB free) | ~$0 |
| Vercel frontend | $0 |
| **Total** | **~$30** |
| **Your $100 credit remaining** | **~$70** |

---

## Security Checklist
- [ ] SSH key pair saved securely
- [ ] Security group only allows ports 22, 80, 443
- [ ] JWT_SECRET_KEY is randomly generated (done by setup script)
- [ ] Set a billing alarm in AWS at $50 to avoid surprises
