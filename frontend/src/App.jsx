import { useState } from 'react'
import PodcastForm from './components/PodcastForm'
import Loading from './components/Loading'
import Results from './components/Results'
import axios from 'axios'

// Get API URL from environment or use default
const API_URL = import.meta.env.VITE_API_URL || '/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (url) => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await apiClient.post('/process-podcast', {
        url: url
      })

      setResults(response.data)
      setLoading(false)
    } catch (err) {
      let errorMessage = 'An error occurred while processing the podcast'
      
      if (err.response) {
        // Server responded with error
        errorMessage = err.response.data?.detail || err.response.data?.message || `Server error: ${err.response.status}`
      } else if (err.request) {
        // Request made but no response received
        errorMessage = `Network error: Unable to connect to the server. Please check if the backend is running.`
      } else {
        // Error setting up request
        errorMessage = err.message || errorMessage
      }
      
      setError(errorMessage)
      setLoading(false)
    }
  }

  const handleReset = () => {
    setResults(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Podcast Transcription & Summarization
          </h1>
          <p className="text-gray-600">
            Extract audio, transcribe, and get AI-generated summaries from Apple Podcasts
          </p>
        </header>

        <div className="bg-white rounded-lg shadow-xl p-6">
          {!results && !loading && (
            <PodcastForm onSubmit={handleSubmit} error={error} />
          )}

          {loading && <Loading />}

          {results && (
            <Results 
              transcript={results.transcript} 
              summary={results.summary}
              metadata={results.metadata}
              onReset={handleReset}
            />
          )}

          {error && !loading && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800 font-semibold mb-2">Error:</p>
              <p className="text-red-600">{error}</p>
              <button
                onClick={handleReset}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

