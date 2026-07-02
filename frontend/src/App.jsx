import { useState, useRef, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const SUGGESTIONS = [
  "We need assessments for senior leadership",
  "Hiring a senior Java backend engineer",
  "Screen entry-level contact centre agents",
  "Graduate management trainee battery",
]

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationEnded, setConversationEnded] = useState(false)
  const messagesEndRef = useRef(null)
  const textareaRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  const autoResize = (el) => {
    el.style.height = 'auto'
    el.style.height = Math.min(el.scrollHeight, 120) + 'px'
  }

  const sendMessage = async (text) => {
    const userMessage = text || input.trim()
    if (!userMessage || loading || conversationEnded) return

    const newMessages = [...messages, { role: 'user', content: userMessage }]
    setMessages(newMessages)
    setInput('')
    setLoading(true)

    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages.map(m => ({
            role: m.role,
            content: m.content
          }))
        })
      })

      if (!res.ok) throw new Error(`HTTP error: ${res.status}`)

      const data = await res.json()

      const agentMessage = {
        role: 'assistant',
        content: data.reply || '',
        recommendations: data.recommendations || [],
        end_of_conversation: data.end_of_conversation || false
      }

      setMessages([...newMessages, agentMessage])

      if (data.end_of_conversation) {
        setConversationEnded(true)
      }
    } catch (err) {
      console.error('Chat error:', err)
      setMessages([...newMessages, {
        role: 'assistant',
        content: 'Sorry, I encountered a network error. Please try again.',
        recommendations: [],
        end_of_conversation: false
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const resetChat = () => {
    setMessages([])
    setConversationEnded(false)
    setInput('')
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-logo">S</div>
        <div className="header-info">
          <h1>SHL Assessment Advisor</h1>
          <p>Powered by SHL Product Catalog</p>
        </div>
        <div className="header-status">
          <span className="status-dot"></span>
          Online
        </div>
      </header>

      {/* Messages */}
      {messages.length === 0 ? (
        <div className="welcome-screen">
          <div className="welcome-icon">🎯</div>
          <h2>SHL Assessment Recommendation Agent</h2>
          <p>
            I help you find the right SHL assessments for your hiring needs.
            Tell me about the role, seniority level, and skills you're looking for,
            and I'll recommend the best assessment battery from SHL's catalog.
          </p>
          <div className="suggestion-chips">
            {SUGGESTIONS.map((s, i) => (
              <button
                key={i}
                className="suggestion-chip"
                onClick={() => sendMessage(s)}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="messages-container">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role === 'user' ? 'user' : 'agent'}`}>
              <span className="message-label">
                {msg.role === 'user' ? 'You' : 'SHL Advisor'}
              </span>
              <div className="message-bubble">
                {msg.content}

                {/* Recommendations */}
                {msg.recommendations && msg.recommendations.length > 0 && (
                  <div className="recommendations">
                    <div className="recommendations-title">
                      📋 Recommended Assessments ({msg.recommendations.length})
                    </div>
                    {msg.recommendations.map((rec, j) => (
                      <div key={j} className="rec-card">
                        <div className="rec-card-header">
                          <span className="rec-card-name">{rec.name}</span>
                          <span className="rec-card-type">{rec.test_type}</span>
                        </div>
                        <a
                          className="rec-card-url"
                          href={rec.url}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          {rec.url}
                        </a>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {/* Typing indicator */}
          {loading && (
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          )}

          {/* End of conversation banner */}
          {conversationEnded && (
            <div className="eoc-banner">
              ✅ Conversation complete — your assessment shortlist is confirmed.
              <br />
              <button
                onClick={resetChat}
                style={{
                  marginTop: '8px',
                  padding: '6px 16px',
                  borderRadius: '8px',
                  border: '1px solid rgba(16, 185, 129, 0.3)',
                  background: 'rgba(16, 185, 129, 0.1)',
                  color: '#10b981',
                  cursor: 'pointer',
                  fontSize: '13px',
                  fontWeight: '500'
                }}
              >
                Start New Conversation
              </button>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Input Area */}
      <div className="input-area">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => {
              setInput(e.target.value)
              autoResize(e.target)
            }}
            onKeyDown={handleKeyDown}
            placeholder={
              conversationEnded
                ? 'Conversation ended. Click "Start New Conversation" above.'
                : 'Describe your hiring needs...'
            }
            disabled={loading || conversationEnded}
            rows={1}
          />
          <button
            className="send-btn"
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading || conversationEnded}
            title="Send message"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
