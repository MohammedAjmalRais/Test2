import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './index.css'

interface Flight {
  airline: string;
  price: number;
  duration: string;
  departure_time?: string;
  arrival_time?: string;
}

interface Hotel {
  name: string;
  price_per_night: number;
  rating?: number;
}

interface WeatherForecast {
  location: string;
  summary: string;
  daily: any[];
}

interface TravelPlanResponse {
  status: string;
  message: string;
  clarification_question?: string;
  flights?: Flight[];
  hotels?: Hotel[];
  weather?: WeatherForecast;
  itinerary?: string;
}

type ViewState = 'home' | 'loading' | 'results';
type TabState = 'itinerary' | 'flights' | 'hotels' | 'weather';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

function App() {
  const [view, setView] = useState<ViewState>('home');
  const [activeTab, setActiveTab] = useState<TabState>('itinerary');
  const [showAbout, setShowAbout] = useState(false);
  
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState<TravelPlanResponse | null>(null);

  const [chatSessionId, setChatSessionId] = useState<string>('');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setView('loading');
    setResponse(null);

    try {
      const res = await fetch('http://localhost:8000/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: prompt })
      });
      
      const data = await res.json();
      setResponse(data);
      setView('results');
      setActiveTab('itinerary');

      if (data.status === 'complete' && data.itinerary) {
        const sessionId = crypto.randomUUID();
        setChatSessionId(sessionId);
        try {
          await fetch('http://localhost:8000/chat/init', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, itinerary_text: data.itinerary })
          });
          setChatMessages([{ role: 'assistant', content: 'Hi! I am your AI Travel Assistant. Ask me any questions about your itinerary!' }]);
        } catch (err) {
          console.error("Failed to init chat", err);
        }
      }
    } catch (error) {
      console.error(error);
      setResponse({ status: 'error', message: 'Failed to connect to the server.' });
      setView('results');
    }
  };

  const handleNewSearch = () => {
    setPrompt('');
    setView('home');
    setChatSessionId('');
    setIsChatOpen(false);
    setChatMessages([]);
  };

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || !chatSessionId) return;

    const query = chatInput.trim();
    setChatInput('');
    setChatMessages(prev => [...prev, { role: 'user', content: query }, { role: 'assistant', content: '' }]);
    setIsChatLoading(true);

    try {
      const res = await fetch('http://localhost:8000/chat/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: chatSessionId, query })
      });

      if (!res.body) throw new Error("No body");
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          setChatMessages(prev => {
            const newMessages = [...prev];
            const lastIndex = newMessages.length - 1;
            newMessages[lastIndex] = {
              ...newMessages[lastIndex],
              content: newMessages[lastIndex].content + chunk
            };
            return newMessages;
          });
        }
      }
    } catch (err) {
      console.error(err);
      setChatMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1].content = "Sorry, I couldn't process your request right now.";
        return newMessages;
      });
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <>
      {/* Navbar is persistent across views or hidden in loading */}
      {view !== 'loading' && (
        <nav className="navbar">
          <div className="logo" onClick={handleNewSearch} style={{cursor: 'pointer'}}>
            Wanderlust AI
          </div>
          <div className="nav-links">
            <span onClick={handleNewSearch}>Home</span>
            <span>Destinations</span>
            <span>Eco-Travel</span>
            <span onClick={() => setShowAbout(true)}>About</span>
          </div>
          {view === 'results' ? (
            <button className="btn-primary" onClick={handleNewSearch}>New Search</button>
          ) : (
            <button className="btn-primary">Get Started</button>
          )}
        </nav>
      )}

      {/* HOME VIEW */}
      {view === 'home' && (
        <div className="view-enter" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
          <div className="hero-section">
            <img src="/hero_bg.jpg" alt="Beautiful landscape" className="hero-bg" />
            <div className="hero-overlay"></div>
            <h1 className="hero-title">Plan Your Perfect Trip Easily</h1>
            <p className="hero-subtitle">Discover sustainable, eco-friendly travel plans orchestrated by advanced AI.</p>
          </div>

          <form onSubmit={handleSubmit} className="search-container" style={{ margin: '-40px auto 0 auto' }}>
            <input 
              type="text" 
              className="search-input"
              placeholder="e.g. Plan a 5-day trip to Tokyo next month. I love nature and quiet places."
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
            />
            <button type="submit" className="btn-search" disabled={!prompt.trim()}>
              Generate Plan
            </button>
          </form>

          <div className="featured-section" style={{ width: '100%', maxWidth: '1200px', margin: '4rem auto', padding: '0 2rem' }}>
            <h2 className="section-title">Trending Global Destinations</h2>
            <div className="grid-3">
              {/* Card 1 */}
              <div className="eco-card">
                <div className="card-img-placeholder">
                  <img src="/dest_tokyo.jpg" alt="Tokyo" />
                </div>
                <h3 className="text-primary text-xl font-bold" style={{marginBottom: '0.5rem'}}>Neon Tokyo, Japan</h3>
                <p className="text-light">Experience the ultimate blend of ancient tradition and futuristic metropolis.</p>
              </div>
              {/* Card 2 */}
              <div className="eco-card">
                <div className="card-img-placeholder">
                  <img src="/dest_nyc.jpg" alt="New York City" />
                </div>
                <h3 className="text-primary text-xl font-bold" style={{marginBottom: '0.5rem'}}>New York City, USA</h3>
                <p className="text-light">Discover the city that never sleeps from Broadway to Central Park.</p>
              </div>
              {/* Card 3 */}
              <div className="eco-card">
                <div className="card-img-placeholder">
                  <img src="https://images.unsplash.com/photo-1512453979798-5ea266f8880c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Dubai" />
                </div>
                <h3 className="text-primary text-xl font-bold" style={{marginBottom: '0.5rem'}}>Luxurious Dubai, UAE</h3>
                <p className="text-light">Explore towering skyscrapers and modern oasis retreats in the desert.</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* LOADING VIEW */}
      {view === 'loading' && (
        <div className="fullscreen-loader view-enter">
          <div className="leaf-spinner"></div>
          <p className="text-xl text-primary font-bold" style={{marginTop: '2rem'}}>Designing your perfect getaway...</p>
          <p className="text-light">Analyzing eco-friendly flights, hotels, and researching local nature spots.</p>
        </div>
      )}

      {/* RESULTS VIEW */}
      {view === 'results' && response && (
        <div className="dashboard-container view-enter">
          
          {/* Sidebar */}
          <aside className="sidebar">
            <p className="sidebar-title">Trip Services</p>
            <button 
              className={`sidebar-tab ${activeTab === 'itinerary' ? 'active' : ''}`}
              onClick={() => setActiveTab('itinerary')}
            >
              Itinerary
            </button>
            
            {response.flights && (
              <button 
                className={`sidebar-tab ${activeTab === 'flights' ? 'active' : ''}`}
                onClick={() => setActiveTab('flights')}
              >
                Flights
              </button>
            )}

            {response.hotels && response.hotels.length > 0 && (
              <button 
                className={`sidebar-tab ${activeTab === 'hotels' ? 'active' : ''}`}
                onClick={() => setActiveTab('hotels')}
              >
                Hotels
              </button>
            )}

            {response.weather && (
              <button 
                className={`sidebar-tab ${activeTab === 'weather' ? 'active' : ''}`}
                onClick={() => setActiveTab('weather')}
              >
                Weather
              </button>
            )}
          </aside>

          {/* Main Panel Content */}
          <main className="dashboard-main">
            <div className="dashboard-header">
              <h2 className="dashboard-title">
                {activeTab === 'itinerary' && 'Personal Itinerary'}
                {activeTab === 'flights' && 'Eco-Friendly Flights'}
                {activeTab === 'hotels' && 'Sustainable Stays'}
                {activeTab === 'weather' && 'Local Weather'}
              </h2>
              <div className="flex-row">
                <span className={`badge ${response.status === 'complete' ? 'badge-success' : response.status === 'needs_clarification' ? 'badge-warning' : 'badge-error'}`}>
                  {response.status.toUpperCase()}
                </span>
                {response.status === 'complete' && (
                  <button onClick={() => window.print()} className="btn-primary" style={{padding: '0.5rem 1rem'}}>
                    <span>📥</span> Download PDF
                  </button>
                )}
              </div>
            </div>

            {response.clarification_question && (
              <div className="eco-card" style={{ background: '#fefce8', borderColor: '#fef08a', marginBottom: '2rem' }}>
                <h3 className="text-primary">Clarification Needed</h3>
                <p>{response.clarification_question}</p>
              </div>
            )}

            <div className="tab-content">
              {/* ITINERARY TAB */}
              {activeTab === 'itinerary' && response.status === 'error' && (
                <div className="eco-card" style={{ padding: '2.5rem 3rem', background: '#fef2f2', borderColor: '#fca5a5' }}>
                  <h3 className="text-xl" style={{ color: '#dc2626', marginBottom: '1rem' }}>{response.message}</h3>
                  {response.errors && response.errors.length > 0 && (
                    <ul style={{ color: '#991b1b', listStyleType: 'disc', paddingLeft: '1.5rem', marginTop: '1rem' }}>
                      {response.errors.map((err, idx) => (
                        <li key={idx}>{err}</li>
                      ))}
                    </ul>
                  )}
                  {response.message === 'Failed to connect to the server.' && (
                    <p style={{ color: '#991b1b', marginTop: '1rem' }}>
                      Please ensure the backend FastAPI server is running on port 8000.
                    </p>
                  )}
                </div>
              )}

              {activeTab === 'itinerary' && response.itinerary && (
                <div className="eco-card" style={{ padding: '2.5rem 3rem' }}>
                  <p className="text-xl" style={{ marginBottom: '2rem', color: 'var(--primary)', fontWeight: '600', borderBottom: '2px solid rgba(58, 106, 69, 0.1)', paddingBottom: '1rem' }}>{response.message}</p>
                  <div className="markdown-body" style={{ fontFamily: "'Lora', serif", lineHeight: '2', fontSize: '1.15rem', color: '#2c3e35' }}>
                    <ReactMarkdown>{response.itinerary}</ReactMarkdown>
                  </div>
                </div>
              )}

              {/* FLIGHTS TAB */}
              {activeTab === 'flights' && response.flights && (
                <div className="grid-2">
                  {response.flights.length === 0 ? (
                    <div className="eco-card" style={{ gridColumn: '1 / -1', textAlign: 'center' }}>
                      <h4 className="text-primary text-xl">No Flights Found</h4>
                      <p>We couldn't find any flights for your trip. Please check your dates or origin/destination.</p>
                    </div>
                  ) : (
                    response.flights.map((flight, idx) => (
                      <div key={idx} className="eco-card">
                        <div className="card-img-placeholder">
                          <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Flight" />
                        </div>
                        <h4 className="text-primary text-xl" style={{ marginBottom: '0.5rem' }}>{flight.airline}</h4>
                        <p><strong>Price:</strong> ${flight.price}</p>
                        <p><strong>Duration:</strong> {flight.duration}</p>
                        {flight.departure_time && <p><strong>Departure:</strong> {flight.departure_time}</p>}
                      </div>
                    ))
                  )}
                </div>
              )}

              {/* HOTELS TAB */}
              {activeTab === 'hotels' && response.hotels && (
                <div className="grid-2">
                  {response.hotels.map((hotel, idx) => (
                    <div key={idx} className="eco-card">
                      <div className="card-img-placeholder">
                        <img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Hotel" />
                      </div>
                      <h4 className="text-primary text-xl" style={{ marginBottom: '0.5rem' }}>{hotel.name}</h4>
                      <p><strong>Price:</strong> ${hotel.price_per_night} / night</p>
                      {hotel.rating && <p><strong>Rating:</strong> {hotel.rating} / 5</p>}
                    </div>
                  ))}
                </div>
              )}

              {/* WEATHER TAB */}
              {activeTab === 'weather' && response.weather && (
                <div className="eco-card" style={{ textAlign: 'center', background: 'var(--accent)', borderColor: 'var(--secondary)' }}>
                  <p className="text-xl font-bold text-primary" style={{ margin: 0 }}>
                    Forecast for {response.weather.location}: {response.weather.summary}
                  </p>
                </div>
              )}
            </div>

          </main>
        </div>
      )}
      {/* ABOUT MODAL */}
      {showAbout && (
        <div className="modal-overlay" onClick={() => setShowAbout(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setShowAbout(false)}>×</button>
            <h2 className="text-primary" style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>About Wanderlust AI</h2>
            
            <div className="flex-col" style={{ gap: '1.5rem' }}>
              <div>
                <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-color)' }}>Our Mission</h3>
                <p className="text-light" style={{ lineHeight: '1.6' }}>
                  Wanderlust AI exists to bridge the gap between exploring the world and protecting it. 
                  We use advanced AI to make sustainable travel effortless, curating experiences that respect the environment.
                </p>
              </div>

              <div>
                <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-color)' }}>How It Works</h3>
                <p className="text-light" style={{ lineHeight: '1.6' }}>
                  Behind the scenes, our platform is powered by a multi-agent AI system (LangGraph & Gemini). 
                  It autonomously cross-references real-time flights, weather, and eco-friendly hotels to build the perfect, personalized itinerary.
                </p>
              </div>

              <div style={{ marginTop: '1rem', padding: '1rem', background: 'var(--accent)', borderRadius: '12px' }}>
                <p className="font-bold text-primary" style={{ textAlign: 'center', margin: 0 }}>
                  Built for the Future of Travel. 🌱
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* CHATBOT WIDGET */}
      {view === 'results' && chatSessionId && (
        <div className={`chat-widget ${isChatOpen ? 'open' : ''}`}>
          {isChatOpen ? (
            <div className="chat-window shadow-xl">
              <div className="chat-header">
                <h3>Travel Assistant</h3>
                <button className="chat-close" onClick={() => setIsChatOpen(false)}>×</button>
              </div>
              <div className="chat-messages">
                {chatMessages.map((msg, idx) => (
                  <div key={idx} className={`chat-message ${msg.role}`}>
                    {msg.content}
                  </div>
                ))}
                {isChatLoading && <div className="chat-message assistant typing">...</div>}
              </div>
              <form className="chat-input-area" onSubmit={handleChatSubmit}>
                <input 
                  type="text" 
                  placeholder="Ask about your trip..." 
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  disabled={isChatLoading}
                />
                <button type="submit" disabled={!chatInput.trim() || isChatLoading}>Send</button>
              </form>
            </div>
          ) : (
            <button className="chat-toggle shadow-xl" onClick={() => setIsChatOpen(true)}>
              💬 Ask AI
            </button>
          )}
        </div>
      )}
    </>
  )
}

export default App
