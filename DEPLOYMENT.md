# Deploying to Streamlit Community Cloud

This guide will walk you through deploying your Streamlit app to Streamlit Community Cloud for free.

## Prerequisites

1. A GitHub account
2. Your app code pushed to a GitHub repository
3. A Streamlit Community Cloud account (free)

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure your GitHub repository contains:
- `app.py` (main application file)
- `requirements.txt` (Python dependencies)
- All supporting files (`core/`, `components/`, `config/`, etc.)

### 2. Sign Up for Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit to access your GitHub account

### 3. Deploy Your App

1. Click "New app" button
2. Select your repository from the dropdown
3. Choose the branch (usually `main` or `master`)
4. Set the main file path: `app.py`
5. Click "Deploy!"

### 4. Initialize the Database

On first deployment, you need to initialize the database:

**Option A: Use the Streamlit Cloud Terminal (Recommended)**

1. After deployment, click the hamburger menu (≡) in your app
2. Select "Manage app"
3. Go to the "Logs" tab
4. You'll see the app running - the database will auto-initialize on first run

**Option B: Pre-initialize Locally and Commit**

```bash
# Run locally first
python scripts/init_db.py

# Add the database to git temporarily
git add -f data/app.db

# Commit and push
git commit -m "Initialize database for deployment"
git push

# After deployment, remove from git
git rm --cached data/app.db
git commit -m "Remove database from git"
git push
```

### 5. Access Your App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

## Important Considerations

### Database Persistence

⚠️ **Important**: Streamlit Community Cloud apps can restart at any time, which may reset your database!

**Solutions**:

1. **For Production**: Use an external database (SQLite is not ideal for production on Streamlit Cloud)
   - PostgreSQL (via Supabase, free tier)
   - MongoDB (via MongoDB Atlas, free tier)

2. **For Development/Testing**: Accept that data may be lost on restarts

### Managing Secrets

For sensitive configuration (like API keys):

1. Go to your app's settings in Streamlit Cloud
2. Click "Secrets"
3. Add your secrets in TOML format:

```toml
[database]
connection_string = "postgresql://..."

[auth]
secret_key = "your-secret-key"
```

Access in your app:
```python
import streamlit as st
db_connection = st.secrets["database"]["connection_string"]
```

### Resource Limits

Streamlit Community Cloud (free tier) has limits:

- **Memory**: 1 GB RAM
- **CPU**: Shared resources
- **Storage**: Not persistent (files can be deleted on restart)

If you need more resources, consider:
- Streamlit Cloud paid tiers
- Self-hosting on AWS/GCP/Azure
- Using Streamlit with Docker

## Updating Your App

To update your deployed app:

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```
3. Streamlit Cloud will automatically redeploy!

## Custom Domain (Optional)

Streamlit Community Cloud doesn't support custom domains on the free tier.

For custom domains, you'll need to:
- Upgrade to a paid plan, or
- Self-host your app

## Monitoring and Logs

View your app's logs:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click "Manage app"
4. View the "Logs" tab

## Troubleshooting

### App Won't Start

- Check the logs for errors
- Ensure all dependencies are in `requirements.txt`
- Verify your Python version is compatible

### Database Errors

- Make sure `data/` directory exists
- Check that `init_database()` is called
- Verify file permissions

### Session Issues

- Streamlit Cloud may reset sessions on inactivity
- Store critical data in the database, not session state

## Alternative Deployment Options

If Streamlit Cloud doesn't meet your needs:

1. **Heroku**: Good for production apps (has free tier)
2. **AWS EC2**: Full control, requires more setup
3. **Google Cloud Run**: Pay per use
4. **Azure App Service**: Enterprise option
5. **Docker + VPS**: Maximum control, cheapest for high traffic

## Need Help?

- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Cloud Status](https://status.streamlit.io/)
