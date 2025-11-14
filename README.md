# Podcast Transcription & Summarization App

A web application that extracts audio from Apple Podcasts, transcribes it using OpenAI Whisper, and generates AI-powered summaries using ChatGPT via OpenRouter.

## Features

- 🎙️ Extract audio from Apple Podcasts URLs
- 📝 High-quality transcription using OpenAI Whisper API
- 🤖 AI-generated summaries using ChatGPT (via OpenRouter)
- 💻 Modern web interface with React and Tailwind CSS
- ⚡ Fast API backend with FastAPI

## Prerequisites

- Python 3.8+
- Node.js 16+
- FFmpeg (required for audio processing)
- OpenAI API key
- OpenRouter API key

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` directory:
```bash
cp .env.example .env
```

5. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

6. Install FFmpeg:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate your virtual environment (if not already active)

3. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

### Start the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Paste an Apple Podcasts episode URL in the input field
3. Click "Process Podcast"
4. Wait for the processing to complete (this may take a few minutes)
5. View the transcript and summary in the results
6. Download the transcript or summary as text files if needed

## API Endpoints

### `POST /api/process-podcast`

Processes a podcast URL and returns transcript and summary.

**Request Body:**
```json
{
  "url": "https://podcasts.apple.com/gb/podcast/..."
}
```

**Response:**
```json
{
  "transcript": "Full transcript text...",
  "summary": "AI-generated summary...",
  "metadata": {
    "title": "Episode Title",
    "duration": 3600,
    "uploader": "Podcast Name"
  }
}
```

## Project Structure

```
audio transcription/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── services/
│   │   │   ├── audio_extractor.py  # Audio extraction
│   │   │   ├── transcriber.py      # Whisper transcription
│   │   │   └── summarizer.py       # ChatGPT summarization
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic models
│   │   └── main.py                 # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PodcastForm.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── Results.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
└── README.md
```

## Notes

- Processing time depends on the podcast length. A 1-hour podcast typically takes 2-5 minutes to process.
- Make sure FFmpeg is installed and accessible in your PATH.
- The app uses temporary files for audio processing, which are automatically cleaned up after processing.
- For very long transcripts (>8000 characters), the transcript will be truncated when generating summaries to stay within API token limits.

## Deployment to Fly.io

### Prerequisites

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login to Fly.io: `fly auth login`
3. Create accounts on [fly.io](https://fly.io) if needed

### Deploy Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create Fly.io app:
```bash
fly launch --no-deploy
```

3. Set secrets (API keys):
```bash
fly secrets set OPENAI_API_KEY=your_openai_key_here
fly secrets set OPENROUTER_API_KEY=your_openrouter_key_here
```

4. Deploy:
```bash
fly deploy
```

5. Get your backend URL:
```bash
fly status
# Note the app URL, e.g., https://podcast-transcription-api.fly.dev
```

### Deploy Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Create Fly.io app:
```bash
fly launch --no-deploy
```

3. Set the backend API URL:
```bash
fly secrets set VITE_API_URL=https://your-backend-app.fly.dev/api
```

4. Deploy:
```bash
fly deploy
```

**Note:** Since Vite environment variables are baked in at build time, you'll need to rebuild after setting VITE_API_URL. Alternatively, you can hardcode the backend URL in `vite.config.js` for production builds.

### Update Frontend to Use Backend URL

After deploying both, update the frontend's `vite.config.js` or use a `.env.production` file:

```bash
echo "VITE_API_URL=https://your-backend-app.fly.dev/api" > .env.production
npm run build
fly deploy
```

## GitHub Setup

1. Create a new repository on GitHub

2. Add remote and push:
```bash
git add .
git commit -m "Initial commit: Podcast transcription app"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

## License

MIT

