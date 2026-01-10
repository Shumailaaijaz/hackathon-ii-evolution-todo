# Deployment Guide - Todo Application

## Prerequisites
- GitHub account (connected to Vercel)
- Vercel account
- Railway account
- Neon PostgreSQL account (for database)

---

## 🚀 Quick Deploy Steps

### Step 1: Push Code to GitHub ✅

```bash
cd /mnt/d/hackathon-ii-evolution-todo
git push origin main
```

---

### Step 2: Deploy Backend to Railway 🚂

1. **Go to Railway Dashboard**: https://railway.app/dashboard

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `hackathon-ii-evolution-todo`
   - Click "Deploy Now"

3. **Configure Service Settings**:
   - Click on your service
   - Go to "Settings" tab
   - Set **Root Directory**: `apps/backend`
   - Railway will auto-detect the railway.toml, Procfile, and nixpacks.toml

4. **Add Environment Variables**:
   Go to "Variables" tab and add:

   ```env
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   API_SECRET_KEY=your-32-character-secret-key-here
   CORS_ORIGINS=["https://your-app.vercel.app"]
   ENVIRONMENT=production
   ```

   **To generate API_SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Get Database URL from Neon**:
   - Go to https://neon.tech
   - Create new project or use existing
   - Copy connection string from dashboard
   - Format: `postgresql://user:password@host/dbname?sslmode=require`

6. **Deploy**:
   - Railway will automatically deploy
   - Wait for deployment to complete
   - Copy your Railway URL: `https://your-app.railway.app`

---

### Step 3: Deploy Frontend to Vercel 🔺

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Select your GitHub repository: `hackathon-ii-evolution-todo`
   - Click "Import"

3. **Configure Project Settings**:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `apps/frontend` ⚠️ IMPORTANT
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`
   - **Node Version**: 20.x

4. **Add Environment Variables**:

   ```env
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```

   ⚠️ Replace `https://your-app.railway.app` with your actual Railway backend URL from Step 2

5. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes for build to complete
   - Vercel will give you a URL like: `https://your-app.vercel.app`

6. **Update Backend CORS**:
   - Go back to Railway dashboard
   - Update the `CORS_ORIGINS` environment variable with your Vercel URL:
     ```env
     CORS_ORIGINS=["https://your-app-name.vercel.app"]
     ```
   - Railway will automatically redeploy

---

## 🗄️ Database Setup (Neon)

1. **Create Neon Project**:
   - Go to https://console.neon.tech
   - Click "Create Project"
   - Choose a region close to your Railway deployment
   - Copy the connection string

2. **Run Migrations** (from Railway):
   - Go to Railway dashboard
   - Click on your service
   - Open terminal (three dots → "Terminal")
   - Run:
     ```bash
     cd apps/backend
     poetry run alembic upgrade head
     ```

   Or run locally with production DATABASE_URL:
   ```bash
   cd apps/backend
   export DATABASE_URL="your-neon-connection-string"
   poetry run alembic upgrade head
   ```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Backend health endpoint works: `https://your-app.railway.app/health`
- [ ] Backend API docs accessible: `https://your-app.railway.app/docs`
- [ ] Frontend loads: `https://your-app.vercel.app`
- [ ] Sign up flow works (creates user in database)
- [ ] Sign in flow works (returns JWT token)
- [ ] Create task works (shows in task list)
- [ ] Toggle task status works
- [ ] Edit task works
- [ ] Delete task works
- [ ] Dark/light theme toggle works

---

## 🔧 Environment Variables Reference

### Backend (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `API_SECRET_KEY` | JWT secret key (32 chars) | `generated-secret-key` |
| `CORS_ORIGINS` | Allowed frontend origins | `["https://app.vercel.app"]` |
| `ENVIRONMENT` | Deployment environment | `production` |

### Frontend (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-app.railway.app` |

---

## 🐛 Troubleshooting

### Frontend Build Errors

**Error**: `Module not found` or `Cannot find module`
- **Solution**: Ensure `apps/frontend` is set as Root Directory in Vercel settings

**Error**: `Type error` during build
- **Solution**: Run `npm run type-check` locally first to catch TypeScript errors

### Backend Deployment Errors

**Error**: `No module named 'app'`
- **Solution**: Verify Root Directory is set to `apps/backend` in Railway settings

**Error**: Database connection failed
- **Solution**: Check DATABASE_URL format includes `?sslmode=require` for Neon

### CORS Errors

**Error**: `Access-Control-Allow-Origin` error in browser console
- **Solution**: Add your Vercel URL to `CORS_ORIGINS` in Railway environment variables
- Format must be JSON array: `["https://your-app.vercel.app"]`

### Authentication Errors

**Error**: `Invalid token` or `Token expired`
- **Solution**: Ensure `API_SECRET_KEY` is the same across all backend instances
- Don't change it after users have logged in, or they'll need to log in again

---

## 🔄 Redeployment

### Frontend (Vercel)
Vercel automatically redeploys on every push to `main` branch.

To manually redeploy:
1. Go to Vercel dashboard
2. Select your project
3. Go to "Deployments" tab
4. Click "..." on latest deployment → "Redeploy"

### Backend (Railway)
Railway automatically redeploys on every push to `main` branch.

To manually redeploy:
1. Go to Railway dashboard
2. Select your service
3. Click "Deploy" button

---

## 📊 Monitoring

### Vercel
- View logs: Project → Deployments → [Latest] → "Logs"
- View analytics: Project → Analytics

### Railway
- View logs: Service → "Logs" tab
- View metrics: Service → "Metrics" tab

### Neon
- View database metrics: Project → "Monitoring"
- View query performance: Project → "Queries"

---

## 🎉 Your Deployment URLs

After completing all steps, save your URLs here:

- **Frontend (Vercel)**: `https://_____________________.vercel.app`
- **Backend (Railway)**: `https://_____________________.railway.app`
- **Database (Neon)**: `https://console.neon.tech/app/projects/_______`

---

## 📝 Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy backend to Railway
3. ✅ Deploy frontend to Vercel
4. ✅ Run database migrations
5. ✅ Test all features
6. 🎉 Share your deployed app!

---

**Built with ❤️ using Next.js + FastAPI + PostgreSQL**
