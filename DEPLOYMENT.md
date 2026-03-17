# 🚀 Deployment Guide

Complete guide to deploying the Object Detection System to various platforms.

## 📋 Table of Contents

1. [Local Docker Deployment](#local-docker-deployment)
2. [Streamlit Cloud (Free)](#streamlit-cloud-free)
3. [AWS EC2](#aws-ec2)
4. [Google Cloud Run](#google-cloud-run)
5. [Azure Container Instances](#azure-container-instances)
6. [Heroku](#heroku)

---

## 🐳 Local Docker Deployment

**Easiest way to run in any environment**

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

1. **Build and run:**
```bash
docker-compose up -d
```

2. **Access dashboard:**
```
http://localhost:8501
```

3. **View logs:**
```bash
docker-compose logs -f
```

4. **Stop:**
```bash
docker-compose down
```

### Troubleshooting

**Webcam not working?**
```bash
# List available cameras
ls /dev/video*

# Update docker-compose.yml with correct device
devices:
  - /dev/video1:/dev/video0  # Use video1 instead
```

---

## ☁️ Streamlit Cloud (Free)

**Best for demos and portfolios - NO WEBCAM SUPPORT**

### Prerequisites
- GitHub account
- GitHub repository with your code

### Steps

1. **Push code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/object-detection-system.git
git push -u origin main
```

2. **Deploy to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect GitHub repository
   - Select `dashboard.py` as main file
   - Click "Deploy"

3. **Configure settings:**
   - Python version: 3.9
   - Advanced settings: Add secrets if needed

4. **Access your app:**
```
https://yourusername-object-detection-system.streamlit.app
```

### Limitations
- ❌ No webcam access (cloud environment)
- ✅ Can demo with uploaded images/videos
- ✅ Perfect for showcasing analytics features

### Workaround for Demo
Modify `dashboard.py` to accept video file uploads:
```python
uploaded_file = st.file_uploader("Upload a video", type=['mp4', 'avi'])
if uploaded_file:
    # Process uploaded video instead of webcam
```

---

## 🔶 AWS EC2

**Full control, supports webcam (with attached USB camera)**

### Prerequisites
- AWS account
- AWS CLI configured

### Steps

1. **Launch EC2 instance:**
```bash
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \  # Amazon Linux 2
    --instance-type t3.medium \
    --key-name your-key-pair \
    --security-groups object-detection-sg
```

2. **Configure security group:**
```bash
# Allow HTTP/HTTPS and Streamlit port
aws ec2 authorize-security-group-ingress \
    --group-name object-detection-sg \
    --protocol tcp \
    --port 8501 \
    --cidr 0.0.0.0/0
```

3. **SSH into instance:**
```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

4. **Install dependencies:**
```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -a -G docker ec2-user
```

5. **Clone and run:**
```bash
git clone https://github.com/yourusername/object-detection-system.git
cd object-detection-system
docker-compose up -d
```

6. **Access:**
```
http://your-instance-ip:8501
```

### Cost Estimate
- **t3.medium:** ~$30/month (24/7)
- **t3.small:** ~$15/month (adequate for demos)

---

## 🌐 Google Cloud Run

**Serverless, auto-scaling, cost-effective**

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Steps

1. **Build container:**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/object-detection
```

2. **Deploy:**
```bash
gcloud run deploy object-detection \
    --image gcr.io/YOUR_PROJECT_ID/object-detection \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8501
```

3. **Access:**
```
https://object-detection-xxxxx-uc.a.run.app
```

### Cost Estimate
- **Pay per use:** $0.40 per million requests
- **Free tier:** 2 million requests/month
- **Typical cost:** $5-20/month depending on usage

### Limitations
- ❌ No webcam support (serverless environment)
- ✅ Great for video file processing
- ✅ Auto-scales with traffic

---

## 🔷 Azure Container Instances

**Simple container deployment**

### Prerequisites
- Azure account
- Azure CLI installed

### Steps

1. **Create resource group:**
```bash
az group create --name object-detection-rg --location eastus
```

2. **Create container registry:**
```bash
az acr create --resource-group object-detection-rg \
    --name objectdetectionacr --sku Basic
```

3. **Build and push image:**
```bash
az acr build --registry objectdetectionacr \
    --image object-detection:latest .
```

4. **Deploy container:**
```bash
az container create \
    --resource-group object-detection-rg \
    --name object-detection-app \
    --image objectdetectionacr.azurecr.io/object-detection:latest \
    --dns-name-label object-detection-unique \
    --ports 8501
```

5. **Access:**
```
http://object-detection-unique.eastus.azurecontainer.io:8501
```

### Cost Estimate
- **Basic:** ~$40/month (24/7)
- **Pay per second** when running

---

## 🟣 Heroku

**Simple deployment, good for demos**

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create app:**
```bash
heroku create object-detection-app
```

2. **Add buildpack:**
```bash
heroku buildpacks:add heroku/python
```

3. **Create Procfile:**
```bash
echo "web: streamlit run dashboard.py --server.port=\$PORT" > Procfile
```

4. **Deploy:**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

5. **Access:**
```
https://object-detection-app.herokuapp.com
```

### Cost
- **Free tier:** Limited hours/month
- **Hobby:** $7/month
- **Professional:** $25/month

### Limitations
- ❌ No webcam support
- ❌ Sleeps after 30 min inactivity (free tier)
- ✅ Easy deployment

---

## 📊 Deployment Comparison

| Platform | Cost | Webcam | Difficulty | Best For |
|----------|------|--------|------------|----------|
| **Local Docker** | Free | ✅ Yes | Easy | Development |
| **Streamlit Cloud** | Free | ❌ No | Easiest | Demos/Portfolio |
| **AWS EC2** | $15-30/mo | ✅ Yes | Medium | Production |
| **Google Cloud Run** | $5-20/mo | ❌ No | Medium | Serverless |
| **Azure ACI** | $40/mo | ❌ No | Medium | Enterprise |
| **Heroku** | $7-25/mo | ❌ No | Easy | Quick demos |

---

## 🎯 Recommended Deployment Strategy

### For Portfolio/Resume
1. **Streamlit Cloud** - Free demo (no webcam)
2. Add note: "Local version supports live webcam detection"
3. Include demo video showing webcam functionality

### For Production Use
1. **AWS EC2** with USB camera attached
2. Set up monitoring and alerts
3. Configure automatic backups

### For Cost-Effective Demo
1. **Google Cloud Run** with video file upload
2. Pay only when used
3. Auto-scales with traffic

---

## 🔒 Security Considerations

### For Public Deployments

1. **Add authentication:**
```python
# In dashboard.py
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'object_detection',
    'auth_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show dashboard
    main()
```

2. **Environment variables:**
```bash
# Never commit sensitive data
export EMAIL_PASSWORD="your_app_password"
export API_KEY="your_api_key"
```

3. **HTTPS:**
- Streamlit Cloud: Automatic
- AWS/GCP/Azure: Configure SSL certificate

---

## 📈 Monitoring

### Add health check endpoint:
```python
# health.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Monitor with:
- **AWS CloudWatch**
- **Google Cloud Monitoring**
- **Datadog**
- **New Relic**

---

## 🎬 Next Steps After Deployment

1. **Add domain name:**
   - Buy domain from Namecheap/GoDaddy
   - Point to deployment URL
   - Example: `detection.yourdomain.com`

2. **Set up CI/CD:**
   - GitHub Actions for auto-deployment
   - Every push to `main` → auto-deploy

3. **Add analytics:**
   - Google Analytics
   - Track usage metrics

4. **Share your deployment:**
   - Add link to README
   - Share on LinkedIn
   - Include in portfolio

---

**Questions? Issues?**
- Open a GitHub issue
- Check documentation
- Join community discussions
