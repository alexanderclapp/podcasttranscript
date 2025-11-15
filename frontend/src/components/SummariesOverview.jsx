import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || '/api'
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

function SummariesOverview({ onSelectSummary }) {
  const [summaries, setSummaries] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchSummaries()
  }, [])

  const fetchSummaries = async () => {
    try {
      setLoading(true)
      const response = await apiClient.get('/summaries')
      setSummaries(response.data.summaries || [])
      setError(null)
    } catch (err) {
      setError('Failed to load summaries')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-4 border-b-4 border-indigo-600"></div>
        <p className="mt-2 text-gray-600">Loading summaries...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
        <button
          onClick={fetchSummaries}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      </div>
    )
  }

  if (summaries.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <p className="text-gray-600 text-lg">No summaries yet</p>
        <p className="text-gray-500 mt-2">Process a podcast to see summaries here</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Summary History</h2>
        <button
          onClick={fetchSummaries}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm"
        >
          Refresh
        </button>
      </div>
      
      <div className="space-y-3">
        {summaries.map((summary) => (
          <div
            key={summary.id}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => onSelectSummary(summary.id)}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-semibold text-gray-900 mb-1">
                  {summary.podcast_title || 'Untitled Podcast'}
                </h3>
                <p className="text-sm text-gray-600 mb-2 line-clamp-2">
                  {summary.summary_type_1?.substring(0, 150)}...
                </p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>{formatDate(summary.created_at)}</span>
                  {summary.metadata?.duration && (
                    <span>
                      {Math.floor(summary.metadata.duration / 60)}:
                      {String(summary.metadata.duration % 60).padStart(2, '0')}
                    </span>
                  )}
                  {summary.summary_type_2 && (
                    <span className="text-green-600 font-medium">✓ Structured Summary</span>
                  )}
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  onSelectSummary(summary.id)
                }}
                className="ml-4 px-3 py-1 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition-colors text-sm"
              >
                View
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SummariesOverview

