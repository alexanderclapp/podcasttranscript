import { useState } from 'react'

function Results({ transcript, summary, summaryType2, metadata, onReset }) {
  const [activeTab, setActiveTab] = useState('summary1')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Results</h2>
          {metadata?.title && (
            <p className="text-gray-600 mt-1">{metadata.title}</p>
          )}
        </div>
        <button
          onClick={onReset}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
        >
          Process Another Podcast
        </button>
      </div>

      {metadata && (
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm">
            {metadata.duration && (
              <div>
                <span className="font-semibold text-gray-700">Duration: </span>
                <span className="text-gray-600">
                  {Math.floor(metadata.duration / 60)}:
                  {String(metadata.duration % 60).padStart(2, '0')}
                </span>
              </div>
            )}
            {metadata.uploader && (
              <div>
                <span className="font-semibold text-gray-700">Author: </span>
                <span className="text-gray-600">{metadata.uploader}</span>
              </div>
            )}
            <div className="col-span-2 md:col-span-1">
              <span className="font-semibold text-gray-700">Transcript Length: </span>
              <span className="text-gray-600">{transcript.length.toLocaleString()} characters</span>
            </div>
          </div>
        </div>
      )}

      <div className="border-b border-gray-200">
        <nav className="flex space-x-4 overflow-x-auto">
          <button
            onClick={() => setActiveTab('summary1')}
            className={`py-3 px-4 border-b-2 font-medium transition-colors whitespace-nowrap ${
              activeTab === 'summary1'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Expert Summary
          </button>
          {summaryType2 && (
            <button
              onClick={() => setActiveTab('summary2')}
              className={`py-3 px-4 border-b-2 font-medium transition-colors whitespace-nowrap ${
                activeTab === 'summary2'
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Structured Summary
            </button>
          )}
          <button
            onClick={() => setActiveTab('transcript')}
            className={`py-3 px-4 border-b-2 font-medium transition-colors whitespace-nowrap ${
              activeTab === 'transcript'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Full Transcript
          </button>
        </nav>
      </div>

      <div className="mt-4">
        {activeTab === 'summary1' && (
          <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-indigo-900 mb-4">Expert Summary (10-min read)</h3>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap">
              {summary}
            </div>
          </div>
        )}

        {activeTab === 'summary2' && summaryType2 && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-green-900 mb-4">Structured Summary</h3>
            <div className="prose max-w-none text-gray-700 whitespace-pre-wrap markdown-content">
              {summaryType2.split('\n').map((line, i) => {
                if (line.startsWith('###')) {
                  return <h3 key={i} className="text-lg font-bold mt-6 mb-3 text-gray-900">{line.replace('###', '').trim()}</h3>
                } else if (line.startsWith('##')) {
                  return <h2 key={i} className="text-xl font-bold mt-8 mb-4 text-gray-900">{line.replace('##', '').trim()}</h2>
                } else if (line.startsWith('-') || line.startsWith('*')) {
                  return <li key={i} className="ml-4 mb-2">{line.replace(/^[-*]\s*/, '')}</li>
                } else if (line.trim() === '') {
                  return <br key={i} />
                } else {
                  return <p key={i} className="mb-3">{line}</p>
                }
              })}
            </div>
          </div>
        )}

        {activeTab === 'transcript' && (
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 max-h-96 overflow-y-auto">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Full Transcript</h3>
            <div className="text-gray-700 whitespace-pre-wrap leading-relaxed">
              {transcript}
            </div>
          </div>
        )}
      </div>

      <div className="flex space-x-4 pt-4 border-t border-gray-200">
        <button
          onClick={() => {
            const blob = new Blob([transcript], { type: 'text/plain' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `transcript-${Date.now()}.txt`
            a.click()
            URL.revokeObjectURL(url)
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          Download Transcript
        </button>
        <button
          onClick={() => {
            const blob = new Blob([summary], { type: 'text/plain' })
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `summary-expert-${Date.now()}.txt`
            a.click()
            URL.revokeObjectURL(url)
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
        >
          Download Expert Summary
        </button>
        {summaryType2 && (
          <button
            onClick={() => {
              const blob = new Blob([summaryType2], { type: 'text/plain' })
              const url = URL.createObjectURL(blob)
              const a = document.createElement('a')
              a.href = url
              a.download = `summary-structured-${Date.now()}.txt`
              a.click()
              URL.revokeObjectURL(url)
            }}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Download Structured Summary
          </button>
        )}
      </div>
    </div>
  )
}

export default Results

