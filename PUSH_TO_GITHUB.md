# 🚀 Push to GitHub - Step by Step

## ✅ Current Status
- ✅ Git repository initialized
- ✅ All files committed
- ✅ Branch: `main`

## 📝 Next Steps

### Step 1: Create GitHub Repository

1. Go to **https://github.com** and sign in
2. Click the **"+"** icon → **"New repository"**
3. Repository name: `BookmyShow` (or any name)
4. Description: "Movie Ticket Booking System - Django Project"
5. Choose **Public** or **Private**
6. **IMPORTANT**: Do NOT check "Initialize with README"
7. Click **"Create repository"**

### Step 2: Add Remote and Push

After creating the repository, GitHub will show you commands. Use these:

**Replace `YOUR_USERNAME` with your actual GitHub username:**

```bash
# Navigate to your project
cd d:\BookmyShow

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/BookmyShow.git

# Push to GitHub
git push -u origin main
```

### Step 3: Authentication

When you run `git push`, you'll be asked for credentials:

**Option A: Use Personal Access Token (Recommended)**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name it: "BookmyShow Deployment"
4. Select scopes: ✅ `repo` (all repo permissions)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. When pushing:
   - Username: your GitHub username
   - Password: paste the token (not your GitHub password)

**Option B: Use GitHub CLI**
```bash
gh auth login
git push -u origin main
```

## 🔧 Complete Commands

Copy and paste these commands one by one:

```bash
# 1. Navigate to project
cd d:\BookmyShow

# 2. Check status
git status

# 3. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/BookmyShow.git

# 4. Verify remote added
git remote -v

# 5. Push to GitHub
git push -u origin main
```

## 🚨 Common Errors & Solutions

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/BookmyShow.git
git push -u origin main
```

### Error: "Authentication failed"
- Use Personal Access Token instead of password
- Make sure token has `repo` scope

### Error: "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Error: "repository not found"
- Check repository name matches
- Check you have access to the repository
- Verify GitHub username is correct

## ✅ After Successful Push

Once pushed, you'll see:
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To https://github.com/YOUR_USERNAME/BookmyShow.git
 * [new branch]      main -> main
```

Then you can deploy on Railway or Render!

## 🎯 Quick Reference

**Your repository URL will be:**
```
https://github.com/YOUR_USERNAME/BookmyShow
```

**To push future changes:**
```bash
git add .
git commit -m "Your message"
git push origin main
```

---

**Need help?** Check `GIT_SETUP.md` for more details!
