# Git Setup Guide

## ✅ Git Repository Initialized

Your repository has been initialized and initial commit created.

## 📝 Next Steps to Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click "New" or "+" → "New repository"
3. Name it: `BookmyShow` (or any name you prefer)
4. **DO NOT** initialize with README, .gitignore, or license
5. Click "Create repository"

### Step 2: Add Remote and Push

After creating the GitHub repository, run these commands:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/BookmyShow.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Alternative: Using SSH (if you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/BookmyShow.git
git branch -M main
git push -u origin main
```

## 🔐 Authentication

If you get authentication errors:

### Option 1: Use GitHub CLI
```bash
gh auth login
git push -u origin main
```

### Option 2: Use Personal Access Token
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`
4. Copy the token
5. When pushing, use token as password:
   ```bash
   git push -u origin main
   # Username: your-github-username
   # Password: your-personal-access-token
   ```

### Option 3: Use GitHub Desktop
- Download GitHub Desktop
- Add repository
- Push from GUI

## 📋 Commands Summary

```bash
# Check status
git status

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

## 🚨 Common Errors and Solutions

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/BookmyShow.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### Error: "branch 'main' does not exist"
```bash
git branch -M main
git push -u origin main
```

### Error: Authentication failed
- Use Personal Access Token instead of password
- Or set up SSH keys

## ✅ After Pushing to GitHub

Once your code is on GitHub, you can:

1. **Deploy on Railway**:
   - Go to railway.app
   - New Project → Deploy from GitHub
   - Select your repository
   - Deploy!

2. **Deploy on Render**:
   - Go to render.com
   - New Web Service → Connect GitHub
   - Select your repository
   - Deploy!

## 📝 Current Status

- ✅ Git repository initialized
- ✅ .gitignore file created
- ✅ Initial commit created
- ⏳ Ready to add remote and push

**Next**: Create GitHub repository and add remote!
