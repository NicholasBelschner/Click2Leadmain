#!/bin/bash

echo "🚀 Click2Lead Deployment Script"
echo "================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin https://github.com/yourusername/Click2Lead.git"
    exit 1
fi

# Check if we're on main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "main" ]; then
    echo "⚠️  You're not on the main branch. Current branch: $current_branch"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Preparing deployment files..."

# Create deployment directory if it doesn't exist
mkdir -p deployment

# Copy necessary files
cp requirements.txt deployment/ 2>/dev/null || echo "⚠️  requirements.txt not found"
cp frontend/server.py deployment/app.py 2>/dev/null || echo "⚠️  frontend/server.py not found"

echo "✅ Deployment files prepared"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 You have uncommitted changes:"
    git status --short
    read -p "Commit these changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
    fi
fi

# Push to remote
echo "📤 Pushing to remote repository..."
git push origin main

echo ""
echo "🎉 Deployment files pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://render.com and sign up"
echo "2. Connect your GitHub repository"
echo "3. Create a new Web Service"
echo "4. Set build command: pip install -r requirements.txt"
echo "5. Set start command: gunicorn app:app"
echo "6. Add environment variables from deployment/env.example"
echo ""
echo "🌐 For frontend deployment:"
echo "1. Go to your GitHub repository settings"
echo "2. Enable GitHub Pages"
echo "3. Set source to main branch"
echo "4. Your site will be available at: https://yourusername.github.io/Click2Lead"
echo ""
echo "📊 For database setup:"
echo "1. Go to https://supabase.com"
echo "2. Create a new project"
echo "3. Get your database URL"
echo "4. Add DATABASE_URL to your environment variables"
echo ""
echo "🔗 Useful Links:"
echo "- Render.com: https://render.com"
echo "- Supabase: https://supabase.com"
echo "- GitHub Pages: https://pages.github.com"
echo ""
echo "📖 Full deployment guide: deployment/README.md" 