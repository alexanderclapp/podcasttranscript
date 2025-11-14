function Loading() {
  return (
    <div className="text-center py-12">
      <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-indigo-600 mb-4"></div>
      <h2 className="text-2xl font-semibold text-gray-800 mb-2">
        Processing Podcast...
      </h2>
      <p className="text-gray-600 mb-4">
        This may take a few minutes depending on the podcast length.
      </p>
      <div className="space-y-2 text-left max-w-md mx-auto mt-6">
        <div className="flex items-center text-gray-700">
          <div className="w-2 h-2 bg-indigo-600 rounded-full mr-3 animate-pulse"></div>
          <span>Extracting audio from podcast URL</span>
        </div>
        <div className="flex items-center text-gray-700">
          <div className="w-2 h-2 bg-indigo-600 rounded-full mr-3 animate-pulse"></div>
          <span>Transcribing audio content</span>
        </div>
        <div className="flex items-center text-gray-700">
          <div className="w-2 h-2 bg-indigo-600 rounded-full mr-3 animate-pulse"></div>
          <span>Generating AI summary</span>
        </div>
      </div>
    </div>
  )
}

export default Loading

