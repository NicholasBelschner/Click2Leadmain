# Click2Lead Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Render.com (Recommended - Free)

1. **Sign up for Render.com**
   - Go to https://render.com
   - Create free account

2. **Set up Database (Supabase - Free)**
   - Go to https://supabase.com
   - Create new project
   - Get your database URL

3. **Deploy Backend**
   - Connect your GitHub repository to Render
   - Create new Web Service
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
   - Add environment variables from `env.example`

4. **Deploy Frontend (GitHub Pages)**
   - Enable GitHub Pages in your repository settings
   - Set source to main branch
   - Your site will be available at: `https://yourusername.github.io/Click2Lead`

### Option 2: Railway.app (Alternative - Free)

1. **Sign up for Railway**
   - Go to https://railway.app
   - Connect GitHub account

2. **Deploy**
   - Create new project from GitHub
   - Railway will auto-detect Python
   - Add environment variables

### Option 3: Vercel (Frontend + Backend)

1. **Sign up for Vercel**
   - Go to https://vercel.com
   - Connect GitHub account

2. **Deploy**
   - Import your repository
   - Vercel will auto-deploy
   - Add environment variables

## 📊 Free Tier Limits

### Render.com
- **Web Services**: 750 hours/month free
- **PostgreSQL**: 1GB storage, 90 days free
- **Custom Domains**: Free

### Supabase
- **Database**: 500MB storage
- **File Storage**: 1GB
- **Bandwidth**: 2GB/month
- **Users**: Unlimited

### GitHub Pages
- **Storage**: 1GB
- **Bandwidth**: 100GB/month
- **Custom Domains**: Free

### Vercel
- **Bandwidth**: 100GB/month
- **Serverless Functions**: 100GB-hours/month
- **Custom Domains**: Free

## 🔧 Environment Variables

Set these in your deployment platform:

```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-secret-key-here
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1
REDIS_URL=redis://localhost:6379
FLASK_ENV=production
DEBUG=False
```

## 📁 Project Structure for Deployment

```
Click2Lead/
├── deployment/           # Deployment files
│   ├── app.py           # Production Flask app
│   ├── requirements.txt # Python dependencies
│   ├── render.yaml      # Render configuration
│   ├── Procfile         # Heroku configuration
│   └── env.example      # Environment variables template
├── frontend/            # Frontend files
├── agents/              # Agent system
└── README.md
```

## 🚀 Deployment Steps

### Step 1: Prepare Repository
```bash
# Add deployment files
git add deployment/
git commit -m "Add deployment configuration"
git push origin main
```

### Step 2: Set up Database
1. Create Supabase account
2. Create new project
3. Get database URL
4. Add to environment variables

### Step 3: Deploy Backend
1. Connect GitHub to Render/Railway
2. Create new service
3. Configure environment variables
4. Deploy

### Step 4: Deploy Frontend
1. Enable GitHub Pages
2. Configure custom domain (optional)
3. Update API endpoints to point to backend

### Step 5: Test
1. Test all features
2. Monitor logs
3. Set up monitoring

## 🔍 Monitoring & Maintenance

### Free Monitoring Tools
- **Uptime Robot**: Free uptime monitoring
- **Google Analytics**: Free analytics
- **Sentry**: Free error tracking

### Performance Optimization
- Enable caching
- Optimize images
- Use CDN for static files
- Monitor database queries

## 💰 Cost Estimation (Free Tier)

### Monthly Costs (Free Tier)
- **Backend Hosting**: $0 (Render/Railway)
- **Database**: $0 (Supabase)
- **File Storage**: $0 (Supabase)
- **Frontend Hosting**: $0 (GitHub Pages)
- **Domain**: $0 (GitHub Pages subdomain)

### When to Upgrade
- **100+ active users**: Consider paid plans
- **1GB+ storage**: Upgrade database plan
- **High traffic**: Consider Vercel Pro or AWS

## 🛠️ Troubleshooting

### Common Issues
1. **Import Errors**: Check Python path in app.py
2. **Database Connection**: Verify DATABASE_URL
3. **CORS Issues**: Check CORS configuration
4. **File Uploads**: Verify storage configuration

### Debug Commands
```bash
# Check logs
railway logs
render logs

# Test locally
python deployment/app.py

# Check dependencies
pip list
```

## 📈 Scaling Plan

### Phase 1: Free Tier (0-100 users)
- Render + Supabase + GitHub Pages

### Phase 2: Growth (100-1000 users)
- Upgrade to paid plans
- Add Redis for caching
- Implement CDN

### Phase 3: Scale (1000+ users)
- Consider AWS/GCP
- Implement load balancing
- Add monitoring and alerting 