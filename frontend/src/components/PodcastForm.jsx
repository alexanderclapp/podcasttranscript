import { useState } from 'react'

function PodcastForm({ onSubmit, error }) {
  const [url, setUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (url.trim()) {
      onSubmit(url.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label 
          htmlFor="podcast-url" 
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Apple Podcasts URL
        </label>
        <input
          type="url"
          id="podcast-url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://podcasts.apple.com/gb/podcast/..."
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
          required
        />
        <p className="mt-2 text-sm text-gray-500">
          Enter the URL of an Apple Podcasts episode
        </p>
      </div>

      <button
        type="submit"
        className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors"
      >
        Process Podcast
      </button>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 font-semibold mb-2">Error:</p>
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}
    </form>
  )
}

export default PodcastForm

