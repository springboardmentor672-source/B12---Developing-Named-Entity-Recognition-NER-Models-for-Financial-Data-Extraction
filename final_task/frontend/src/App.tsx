import { useState, useCallback, useRef, useEffect } from 'react'
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import './App.css'

// Types
interface Entity {
  entity_group?: string
  word?: string
  text?: string
  type?: string
  score?: number
  start?: number
  end?: number
  description?: string
}

interface Sentiment {
  label: string
  score: number
  sentence?: string
  text?: string
  chunked?: boolean
}

interface Aggregate {
  label: string
  avg_score: number
}

interface NEResult {
  total_entities: number
  entities: Entity[]
}

interface LangExtractResult {
  total_entities: number
  entities: Entity[]
  error?: string
}

interface SentimentResult {
  total_sentences: number
  sentiments: Sentiment[]
  aggregate: Aggregate
}

interface AnalysisResults {
  status: string
  filename?: string
  markdown_text?: string
  total_entities?: number
  entities?: Entity[]
  aggregate?: Aggregate
  total_sentences?: number
  sentiments?: Sentiment[]
  ner?: NEResult
  langextract?: LangExtractResult
  sentiment?: SentimentResult
}

interface EndpointConfig {
  label: string
  color: string
}

type EndpointKey = 'convert-pdf' | 'ner' | 'langextract' | 'sentiment' | 'analyze-all'

type TabId = 'overview' | 'markdown' | 'ner' | 'financial' | 'sentiment'

// Constants
const ENDPOINTS: Record<EndpointKey, EndpointConfig> = {
  'convert-pdf': { label: 'Convert PDF', color: '#5b8def' },
  'ner': { label: 'Named Entities', color: '#0d7377' },
  'langextract': { label: 'Financial Data', color: '#2eab59' },
  'sentiment': { label: 'Sentiment', color: '#e67e22' },
  'analyze-all': { label: 'Analyze All', color: '#0d7377' }
}

const ENTITY_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  'ORG': { bg: 'rgba(13, 115, 119, 0.1)', border: '#0d7377', text: '#0d7377' },
  'PER': { bg: 'rgba(46, 171, 89, 0.1)', border: '#2eab59', text: '#2eab59' },
  'LOC': { bg: 'rgba(91, 141, 239, 0.1)', border: '#5b8def', text: '#5b8def' },
  'MISC': { bg: 'rgba(230, 126, 34, 0.1)', border: '#e67e22', text: '#e67e22' },
  'MONEY': { bg: 'rgba(13, 115, 119, 0.15)', border: '#0d7377', text: '#0d7377' },
  'PERCENT': { bg: 'rgba(46, 171, 89, 0.15)', border: '#2eab59', text: '#2eab59' },
  'DATE': { bg: 'rgba(91, 141, 239, 0.15)', border: '#5b8def', text: '#5b8def' },
  'GPE': { bg: 'rgba(230, 126, 34, 0.15)', border: '#e67e22', text: '#e67e22' },
}

const SENTIMENT_COLORS: Record<string, { bg: string; border: string; text: string; icon: string }> = {
  'positive': { bg: 'rgba(46, 171, 89, 0.1)', border: '#2eab59', text: '#2eab59', icon: '+' },
  'negative': { bg: 'rgba(231, 76, 60, 0.1)', border: '#e74c3c', text: '#e74c3c', icon: '−' },
  'neutral': { bg: 'rgba(91, 141, 239, 0.1)', border: '#5b8def', text: '#5b8def', icon: '·' }
}

// Components
function Header({ showBack = false, onBack }: { showBack?: boolean; onBack?: () => void }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect x="2" y="2" width="28" height="28" rx="6" stroke="currentColor" strokeWidth="2"/>
            <path d="M8 12h16M8 16h12M8 20h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <circle cx="24" cy="20" r="3" fill="var(--accent-primary)"/>
          </svg>
          <span className="logo-text">DocuMind</span>
        </div>
        <nav className="nav">
          {showBack ? (
            <button className="nav-back" onClick={onBack}>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M10 4L6 8l4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Back to Upload
            </button>
          ) : (
            <span className="nav-badge">Neural Document Analysis</span>
          )}
        </nav>
      </div>
    </header>
  )
}

function DropZone({
  onFileSelect,
  isLoading,
  selectedFile
}: {
  onFileSelect: (file: File) => void
  isLoading: boolean
  selectedFile: File | null
}) {
  const [isDragging, setIsDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }, [])

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    const files = e.dataTransfer?.files
    if (files && files.length > 0) {
      onFileSelect(files[0])
    }
  }, [onFileSelect])

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      onFileSelect(files[0])
    }
  }, [onFileSelect])

  return (
    <div
      className={`dropzone ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''} ${isLoading ? 'loading' : ''}`}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf"
        onChange={handleChange}
        className="dropzone-input"
      />
      <div className="dropzone-content">
        {isLoading ? (
          <>
            <div className="dropzone-spinner">
              <svg width="48" height="48" viewBox="0 0 48 48" className="spinner">
                <circle cx="24" cy="24" r="20" stroke="var(--border-medium)" strokeWidth="4" fill="none"/>
                <circle cx="24" cy="24" r="20" stroke="var(--accent-primary)" strokeWidth="4" fill="none" strokeDasharray="80 40"/>
              </svg>
            </div>
            <p className="dropzone-text">Processing document...</p>
          </>
        ) : selectedFile ? (
          <>
            <div className="dropzone-icon file-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect x="8" y="4" width="24" height="32" rx="3" stroke="currentColor" strokeWidth="2"/>
                <path d="M32 8h8a2 2 0 012 2v28a2 2 0 01-2 2H14a2 2 0 01-2-2V14l10-10z" stroke="currentColor" strokeWidth="2"/>
                <path d="M26 4v10h10" stroke="currentColor" strokeWidth="2"/>
                <path d="M16 20h16M16 26h12M16 32h8" stroke="var(--accent-primary)" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </div>
            <p className="dropzone-filename">{selectedFile.name}</p>
            <p className="dropzone-hint">Click or drag to replace</p>
          </>
        ) : (
          <>
            <div className="dropzone-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect x="8" y="14" width="32" height="24" rx="3" stroke="currentColor" strokeWidth="2"/>
                <path d="M24 8v20M16 18l8-8 8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <p className="dropzone-text">Drop PDF here or click to browse</p>
            <p className="dropzone-hint">Maximum file size: 10MB</p>
          </>
        )}
      </div>
    </div>
  )
}

function EndpointSelector({
  selectedEndpoint,
  onSelect,
  disabled
}: {
  selectedEndpoint: EndpointKey
  onSelect: (endpoint: EndpointKey) => void
  disabled: boolean
}) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className={`endpoint-selector ${disabled ? 'disabled' : ''}`}>
      <button
        className="endpoint-trigger"
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
      >
        <span className="trigger-label">{ENDPOINTS[selectedEndpoint]?.label || 'Select Analysis'}</span>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className={`trigger-arrow ${isOpen ? 'open' : ''}`}>
          <path d="M4 6l4 4 4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
      {isOpen && (
        <div className="endpoint-dropdown">
          {(Object.entries(ENDPOINTS) as [EndpointKey, EndpointConfig][]).map(([key, { label, color }]) => (
            <button
              key={key}
              className={`endpoint-option ${selectedEndpoint === key ? 'active' : ''}`}
              onClick={() => {
                onSelect(key)
                setIsOpen(false)
              }}
            >
              <span className="option-dot" style={{ background: color }} />
              {label}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function AnalyzeButton({
  onClick,
  isLoading,
  disabled
}: {
  onClick: () => void
  isLoading: boolean
  disabled: boolean
}) {
  return (
    <button
      className={`analyze-button ${isLoading ? 'loading' : ''}`}
      onClick={onClick}
      disabled={disabled || isLoading}
    >
      {isLoading ? (
        <>
          <svg width="20" height="20" viewBox="0 0 20 20" className="btn-spinner">
            <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2" fill="none" strokeDasharray="30 20"/>
          </svg>
          Analyzing...
        </>
      ) : (
        <>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 2v4M10 14v4M2 10h4M14 10h4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <circle cx="10" cy="10" r="3" fill="currentColor"/>
          </svg>
          Analyze Document
        </>
      )}
    </button>
  )
}

function StatusMessage({ status, error }: { status?: string | null; error?: string | null }) {
  if (!status && !error) return null

  return (
    <div className={`status-message ${error ? 'error' : 'success'}`}>
      {error ? (
        <>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2"/>
            <path d="M10 6v5M10 13v1" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          <span>{error}</span>
        </>
      ) : (
        <>
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="2"/>
            <path d="M6 10l3 3 5-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>{status}</span>
        </>
      )}
    </div>
  )
}

function UploadPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [selectedEndpoint, setSelectedEndpoint] = useState<EndpointKey>('analyze-all')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleFileSelect = useCallback((file: File) => {
    if (!file.name.endsWith('.pdf')) {
      setError('Please select a PDF file')
      return
    }
    setSelectedFile(file)
    setError(null)
  }, [])

  const handleAnalyze = useCallback(async () => {
    if (!selectedFile) return

    setIsLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)

      const response = await fetch(`/${selectedEndpoint}`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}`)
      }

      const data: AnalysisResults = await response.json()
      navigate('/results', { state: { results: data, filename: selectedFile.name, endpoint: selectedEndpoint } })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }, [selectedFile, selectedEndpoint, navigate])

  return (
    <div className="upload-page">
      <div className="upload-section">
        <DropZone
          onFileSelect={handleFileSelect}
          isLoading={isLoading}
          selectedFile={selectedFile}
        />

        <div className="controls">
          <EndpointSelector
            selectedEndpoint={selectedEndpoint}
            onSelect={setSelectedEndpoint}
            disabled={isLoading}
          />
          <AnalyzeButton
            onClick={handleAnalyze}
            isLoading={isLoading}
            disabled={!selectedFile}
          />
        </div>

        <StatusMessage status={null} error={error} />
      </div>
    </div>
  )
}

function AnalysisTabs({
  results,
  activeTab,
  onTabChange,
  analysisType
}: {
  results: AnalysisResults
  activeTab: TabId
  onTabChange: (tab: TabId) => void
  analysisType: EndpointKey
}) {
  const tabs: { id: TabId; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'markdown', label: 'Markdown' },
  ]

  if (analysisType === 'analyze-all' || analysisType === 'ner') {
    tabs.push({ id: 'ner', label: 'NER Entities' })
  }
  if (analysisType === 'analyze-all' || analysisType === 'langextract') {
    tabs.push({ id: 'financial', label: 'Financial Data' })
  }
  if (analysisType === 'analyze-all' || analysisType === 'sentiment') {
    tabs.push({ id: 'sentiment', label: 'Sentiment' })
  }

  return (
    <div className="analysis-tabs">
      <div className="tabs-header">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
            {activeTab === tab.id && <span className="tab-indicator" />}
          </button>
        ))}
      </div>
      <div className="tabs-content">
        {activeTab === 'overview' && <OverviewPanel results={results} analysisType={analysisType} />}
        {activeTab === 'markdown' && <MarkdownPanel markdown={results.markdown_text} />}
        {activeTab === 'ner' && <NERPanel results={results} />}
        {activeTab === 'financial' && <FinancialPanel results={results} />}
        {activeTab === 'sentiment' && <SentimentPanel results={results} />}
      </div>
    </div>
  )
}

function OverviewPanel({ results, analysisType }: { results: AnalysisResults; analysisType: EndpointKey }) {
  const stats: { label: string; value: string | number; subvalue?: string; icon: string }[] = []

  if (results.total_entities !== undefined) {
    stats.push({ label: 'Total Entities', value: results.total_entities, icon: '◆' })
  }
  if (results.total_sentences !== undefined) {
    stats.push({ label: 'Sentences', value: results.total_sentences, icon: '▢' })
  }
  if (results.aggregate) {
    stats.push({
      label: 'Dominant Sentiment',
      value: results.aggregate.label,
      subvalue: `Score: ${results.aggregate.avg_score}`,
      icon: '◐'
    })
  }
  if (results.filename) {
    stats.push({ label: 'Filename', value: results.filename, icon: '◎' })
  }

  if (results.ner?.total_entities !== undefined) {
    stats.push({ label: 'NER Entities', value: results.ner.total_entities, icon: '◆' })
  }
  if (results.langextract?.total_entities !== undefined) {
    stats.push({ label: 'Financial Items', value: results.langextract.total_entities, icon: '$' })
  }
  if (results.sentiment?.total_sentences !== undefined) {
    stats.push({ label: 'Sentences Analyzed', value: results.sentiment.total_sentences, icon: '▢' })
  }

  return (
    <div className="panel overview-panel">
      <div className="stats-grid">
        {stats.map((stat, i) => (
          <div key={i} className="stat-card" style={{ animationDelay: `${i * 100}ms` }}>
            <span className="stat-icon">{stat.icon}</span>
            <div className="stat-content">
              <span className="stat-value">{stat.value}</span>
              {stat.subvalue && <span className="stat-subvalue">{stat.subvalue}</span>}
              <span className="stat-label">{stat.label}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function MarkdownPanel({ markdown }: { markdown?: string }) {
  if (!markdown) return <div className="panel empty-state">No markdown content available</div>

  return (
    <div className="panel markdown-panel">
      <div className="markdown-toolbar">
        <span className="toolbar-label">Extracted Text</span>
        <span className="toolbar-badge">{markdown.length} chars</span>
      </div>
      <pre className="markdown-content">{markdown}</pre>
    </div>
  )
}

function NERPanel({ results }: { results: AnalysisResults }) {
  const entities = results.entities || results.ner?.entities || []

  const uniqueByWord = (items: Entity[]) => {
    const seen = new Set<string>()
    return items.filter(e => {
      const word = e.word || e.text || ''
      if (seen.has(word)) return false
      seen.add(word)
      return true
    })
  }

  const grouped = entities.reduce((acc, entity) => {
    const type = entity.entity_group || entity.type || 'MISC'
    if (!acc[type]) acc[type] = []
    acc[type].push(entity)
    return acc
  }, {} as Record<string, Entity[]>)

  return (
    <div className="panel ner-panel">
      <div className="entity-groups">
        {Object.entries(grouped).map(([type, items]) => {
          const colors = ENTITY_COLORS[type] || ENTITY_COLORS['MISC']
          const uniqueItems = uniqueByWord(items)
          return (
            <div key={type} className="entity-group" style={{ '--group-color': colors.border } as React.CSSProperties}>
              <div className="entity-group-header" style={{ borderColor: colors.border, background: colors.bg }}>
                <span className="entity-type" style={{ color: colors.text }}>{type}</span>
                <span className="entity-count">{uniqueItems.length}</span>
              </div>
              <div className="entity-list">
                {uniqueItems.map((entity, i) => (
                  <span
                    key={i}
                    className="entity-tag"
                    style={{ background: colors.bg, borderColor: colors.border, color: colors.text }}
                  >
                    {entity.word || entity.text}
                  </span>
                ))}
              </div>
            </div>
          )
        })}
      </div>
      {entities.length === 0 && (
        <div className="empty-state">No entities found</div>
      )}
    </div>
  )
}

function FinancialPanel({ results }: { results: AnalysisResults }) {
  const entities = results.entities || results.langextract?.entities || []

  const grouped = entities.reduce((acc, entity) => {
    const type = entity.type || 'INFO'
    if (!acc[type]) acc[type] = []
    acc[type].push(entity)
    return acc
  }, {} as Record<string, Entity[]>)

  return (
    <div className="panel financial-panel">
      <div className="entity-groups">
        {Object.entries(grouped).map(([type, items]) => {
          const colors = ENTITY_COLORS[type] || ENTITY_COLORS['MISC']
          return (
            <div key={type} className="entity-group" style={{ '--group-color': colors.border } as React.CSSProperties}>
              <div className="entity-group-header" style={{ borderColor: colors.border, background: colors.bg }}>
                <span className="entity-type" style={{ color: colors.text }}>{type}</span>
                <span className="entity-count">{items.length}</span>
              </div>
              <div className="entity-list">
                {items.map((entity, i) => (
                  <div key={i} className="financial-item" style={{ borderColor: colors.border }}>
                    <span className="financial-text" style={{ color: colors.text }}>{entity.text || entity.word}</span>
                    {entity.description && (
                      <span className="financial-desc">{entity.description}</span>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
      {entities.length === 0 && (
        <div className="empty-state">No financial data extracted</div>
      )}
    </div>
  )
}

function SentimentPanel({ results }: { results: AnalysisResults }) {
  const sentiments = results.sentiments || results.sentiment?.sentiments || []
  const aggregate = results.aggregate || results.sentiment?.aggregate || { label: 'neutral', avg_score: 0 }
  const colors = SENTIMENT_COLORS[aggregate.label] || SENTIMENT_COLORS['neutral']

  const grouped = sentiments.reduce((acc, s) => {
    const label = s.label || 'neutral'
    if (!acc[label]) acc[label] = []
    acc[label].push(s)
    return acc
  }, {} as Record<string, Sentiment[]>)

  return (
    <div className="panel sentiment-panel">
      <div className="sentiment-summary" style={{ background: colors.bg, borderColor: colors.border }}>
        <div className="sentiment-badge" style={{ color: colors.text, borderColor: colors.border }}>
          <span className="sentiment-icon">{colors.icon}</span>
          {aggregate.label.toUpperCase()}
        </div>
        <div className="sentiment-score">
          <span className="score-value">{aggregate.avg_score}</span>
          <span className="score-label">Average Score</span>
        </div>
      </div>

      <div className="sentiment-breakdown">
        <h4 className="breakdown-title">Sentiment Breakdown</h4>
        <div className="breakdown-bars">
          {Object.entries(grouped).map(([label, items]) => {
            const pct = (items.length / sentiments.length * 100).toFixed(1)
            const c = SENTIMENT_COLORS[label] || SENTIMENT_COLORS['neutral']
            return (
              <div key={label} className="breakdown-row">
                <span className="breakdown-label" style={{ color: c.text }}>{label}</span>
                <div className="breakdown-bar-container">
                  <div
                    className="breakdown-bar"
                    style={{ width: `${pct}%`, background: c.border }}
                  />
                </div>
                <span className="breakdown-pct">{pct}%</span>
              </div>
            )
          })}
        </div>
      </div>

      <div className="sentiment-sentences">
        <h4 className="sentences-title">Sentence Analysis</h4>
        <div className="sentences-list">
          {sentiments.slice(0, 20).map((s, i) => {
            const c = SENTIMENT_COLORS[s.label] || SENTIMENT_COLORS['neutral']
            return (
              <div key={i} className="sentence-item" style={{ borderColor: c.border }}>
                <span className="sentence-label" style={{ color: c.text, background: c.bg }}>
                  {s.label} {s.score?.toFixed(2)}
                </span>
                <span className="sentence-text">{s.text || s.sentence || ''}</span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

function ResultsPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const results = location.state?.results as AnalysisResults | undefined
  const filename = location.state?.filename as string | undefined
  const endpoint = location.state?.endpoint as EndpointKey | undefined

  const [activeTab, setActiveTab] = useState<TabId>('overview')

  useEffect(() => {
    if (!results) {
      navigate('/', { replace: true })
    }
  }, [results, navigate])

  const handleBack = () => {
    navigate('/')
  }

  if (!results || !filename || !endpoint) return null

  return (
    <div className="results-page">
      <div className="results-header">
        <div className="results-title-section">
          <h1 className="results-title">Analysis Results</h1>
          <p className="results-filename">{filename}</p>
        </div>
        <div className="results-meta">
          <span className="endpoint-badge">{ENDPOINTS[endpoint]?.label || endpoint}</span>
        </div>
      </div>

      <div className="results-content">
        <AnalysisTabs
          results={results}
          activeTab={activeTab}
          onTabChange={setActiveTab}
          analysisType={endpoint}
        />
      </div>
    </div>
  )
}

function HomePage() {
  return (
    <>
      <main className="main-content">
        <div className="hero-section">
          <h1 className="hero-title">
            <span className="title-line">Document</span>
            <span className="title-line accent">Intelligence</span>
          </h1>
          <p className="hero-subtitle">
            Extract named entities, financial data, and sentiment from your documents
            using advanced neural language models.
          </p>
        </div>

        <UploadPage />
      </main>

      <footer className="footer">
        <p>Powered by BERT NER • LangChain • FinBERT</p>
      </footer>
    </>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/results" element={
        <>
          <Header showBack onBack={() => window.history.back()} />
          <ResultsPage />
        </>
      } />
    </Routes>
  )
}

export default App
