# Deployment Guide

## Quick Deploy to Fly.io

This guide will help you deploy both the backend and frontend to Fly.io.

### 1. Install Fly CLI

```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login to Fly.io

```bash
fly auth login
```

### 3. Deploy Backend

```bash
cd backend

# Create and configure the app (don't deploy yet)
fly launch --no-deploy --name podcast-transcription-api --region iad

# Set your API keys as secrets
fly secrets set OPENAI_API_KEY=sk-proj-...
fly secrets set OPENROUTER_API_KEY=sk-or-v1-...

# Deploy!
fly deploy
```

Your backend will be available at `https://podcast-transcription-api.fly.dev`

### 4. Deploy Frontend

```bash
cd frontend

# Create and configure the app (don't deploy yet)
fly launch --no-deploy --name podcast-transcription-web --region iad

# Create .env.production with your backend URL
echo "VITE_API_URL=https://podcast-transcription-api.fly.dev/api" > .env.production

# Deploy!
fly deploy
```

Your frontend will be available at `https://podcast-transcription-web.fly.dev`

### 5. Update CORS on Backend

After deploying, you need to update the backend's CORS settings to allow requests from your frontend domain.

Edit `backend/app/main.py` and update the `allow_origins` list:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://podcast-transcription-web.fly.dev"  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy:
```bash
cd backend
fly deploy
```

## Environment Variables

### Backend Secrets (Fly.io)
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENROUTER_API_KEY` - Your OpenRouter API key

### Frontend Build-time Variables
- `VITE_API_URL` - URL of your backend API (e.g., `https://podcast-transcription-api.fly.dev/api`)

## Troubleshooting

### Backend Issues
- Check logs: `fly logs -a podcast-transcription-api`
- Check secrets: `fly secrets list -a podcast-transcription-api`
- SSH into machine: `fly ssh console -a podcast-transcription-api`

### Frontend Issues
- Check logs: `fly logs -a podcast-transcription-web`
- Verify API URL is correct in `.env.production`
- Check browser console for CORS errors

### CORS Errors
If you see CORS errors, make sure:
1. Backend CORS includes your frontend URL
2. Backend is deployed and accessible
3. API URL in frontend matches backend URL

## Scaling

To scale your backend:

```bash
fly scale count 2 -a podcast-transcription-api
```

To check resource usage:

```bash
fly status -a podcast-transcription-api
```

