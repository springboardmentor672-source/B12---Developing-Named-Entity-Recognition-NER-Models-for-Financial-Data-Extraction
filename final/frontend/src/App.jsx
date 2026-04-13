import { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')
  const [statusType, setStatusType] = useState('') 
  
  const [markdown, setMarkdown] = useState('')
  const [memo, setMemo] = useState('')
  const [entities, setEntities] = useState([])
  const [sentiment, setSentiment] = useState([]) // <-- NEW: Sentiment State

  const API_BASE_URL = "http://127.0.0.1:8000"

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const processDocument = async () => {
    if (!file) {
      alert("Please select a PDF first!")
      return
    }

    setLoading(true)
    setStatusType('processing')
    setMarkdown('')
    setMemo('')
    setEntities([])
    setSentiment([]) // <-- NEW: Reset Sentiment

    try {
      setStatus('Converting PDF to text...')
      const formData = new FormData()
      formData.append('file', file)

      const convertRes = await axios.post(`${API_BASE_URL}/convert/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      const extractedText = convertRes.data.markdown_content
      setMarkdown(extractedText)

      const textPayload = { text: extractedText, filename: file.name }

      setStatus('Generating AI Investment Memo...')
      const memoRes = await axios.post(`${API_BASE_URL}/analyze/memo/`, textPayload)
      setMemo(memoRes.data.memo)

      setStatus('Extracting Financial Entities...')
      const nerRes = await axios.post(`${API_BASE_URL}/analyze/ner/`, textPayload)
      setEntities(nerRes.data.entities)

      // --- NEW: Sentiment API Call ---
      setStatus('Analyzing Market Sentiment...')
      const sentimentRes = await axios.post(`${API_BASE_URL}/analyze/sentiment/`, textPayload)
      setSentiment(sentimentRes.data.results)
      // -------------------------------

      setStatus('Analysis Complete! ✅')
      setStatusType('success')

    } catch (error) {
      console.error("API Error:", error)
      setStatus(`❌ Error: ${error.response?.data?.detail || error.message}`)
      setStatusType('error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>Financial AI Analyst</h1>
        <p>Enterprise-Grade Document Intelligence</p>
      </header>

      <div className="upload-section">
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <br />
        <button className="analyze-btn" onClick={processDocument} disabled={loading}>
          {loading ? 'Processing Document...' : 'Initialize Analysis'}
        </button>
        {status && (
          <p className={`status-text status-${statusType}`}>{status}</p>
        )}
      </div>

      <div className="results-grid">
        
        {/* Left Column: Memo, Sentiment & NER */}
        <div className="main-content">
          {memo && (
            <div className="card">
              <h2>🧠 Executive Memo</h2>
              <div className="markdown-body">
                <ReactMarkdown>{memo}</ReactMarkdown>
              </div>
            </div>
          )}

          {/* --- NEW: Sentiment Analysis Card --- */}
          {sentiment.length > 0 && (
            <div className="card">
              <h2>⚖️ Market Sentiment</h2>
              <div className="sentiment-list">
                {sentiment.map((item, idx) => (
                  <div key={idx} className={`sentiment-item ${item.label.toLowerCase()}`}>
                    <span className={`sentiment-label ${item.label.toLowerCase()}`}>
                      {item.label} ({(item.score * 100).toFixed(1)}%)
                    </span>
                    <div>{item.sentence}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {/* ------------------------------------ */}

          {entities.length > 0 && (
            <div className="card">
              <h2>📌 Extracted Entities</h2>
              <div className="entity-list">
                {entities.map((ent, idx) => (
                  <div key={idx} className="entity-tag">
                    <span className="entity-class">{ent.class}</span>
                    <span className="entity-text">{ent.text}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Raw Markdown Text */}
        <div className="side-content">
          {markdown && (
            <div className="card" style={{ height: '100%' }}>
              <h3>📄 Source Text</h3>
              <div className="raw-text-container">
                <pre>{markdown}</pre>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default App