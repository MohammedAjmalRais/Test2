import { useState } from 'react'
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

interface TravelPlanResponse {
  status: string;
  message: string;
  clarification_question?: string;
  flights?: Flight[];
  hotels?: Hotel[];
  itinerary?: string;
}

function App() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<TravelPlanResponse | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch('http://localhost:8000/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: prompt })
      });
      
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error(error);
      setResponse({ status: 'error', message: 'Failed to connect to the server.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1>Wanderlust AI</h1>
        <p style={{ color: '#94a3b8', fontSize: '1.2rem' }}>Your personal intelligent travel orchestrator.</p>
      </header>

      <main className="flex-col">
        <div className="glass glass-card">
          <form onSubmit={handleSubmit} className="flex-col">
            <label htmlFor="prompt" style={{ fontWeight: 600 }}>Where would you like to go?</label>
            <textarea 
              id="prompt"
              rows={4}
              placeholder="e.g. Plan a 5-day trip to Tokyo next month. I love sushi and electronics."
              value={prompt}
              onChange={e => setPrompt(e.target.value)}
            />
            <button type="submit" disabled={loading || !prompt.trim()}>
              {loading ? 'Planning...' : 'Generate Travel Plan'}
            </button>
          </form>
        </div>

        {loading && (
          <div className="glass glass-card loader-container">
            <div className="spinner"></div>
            <p>Our AI agents are analyzing flights, hotels, and researching your destination...</p>
          </div>
        )}

        {response && (
          <div className="glass glass-card flex-col" style={{ marginTop: '2rem' }}>
            <div className="flex-row" style={{ justifyContent: 'space-between' }}>
              <h2>Plan Status</h2>
              <span className={`badge ${response.status === 'complete' ? 'badge-success' : response.status === 'needs_clarification' ? 'badge-warning' : 'badge-error'}`}>
                {response.status.toUpperCase()}
              </span>
            </div>
            
            <p style={{ fontSize: '1.1rem', color: '#e2e8f0', margin: '1rem 0' }}>{response.message}</p>

            {response.clarification_question && (
              <div className="glass glass-card" style={{ background: 'rgba(245, 158, 11, 0.1)', borderColor: 'rgba(245, 158, 11, 0.3)' }}>
                <h3>Clarification Needed</h3>
                <p>{response.clarification_question}</p>
              </div>
            )}

            {(response.flights && response.flights.length > 0) && (
              <div style={{ marginTop: '2rem' }}>
                <h3>Top Flights</h3>
                <div className="grid-2">
                  {response.flights.map((flight, idx) => (
                    <div key={idx} className="glass glass-card" style={{ background: 'rgba(59, 130, 246, 0.1)' }}>
                      <h4 style={{ color: '#60a5fa', marginBottom: '0.5rem' }}>{flight.airline}</h4>
                      <p><strong>Price:</strong> ${flight.price}</p>
                      <p><strong>Duration:</strong> {flight.duration}</p>
                      {flight.departure_time && <p><strong>Departure:</strong> {flight.departure_time}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {(response.hotels && response.hotels.length > 0) && (
              <div style={{ marginTop: '2rem' }}>
                <h3>Recommended Hotels</h3>
                <div className="grid-2">
                  {response.hotels.map((hotel, idx) => (
                    <div key={idx} className="glass glass-card" style={{ background: 'rgba(139, 92, 246, 0.1)' }}>
                      <h4 style={{ color: '#c084fc', marginBottom: '0.5rem' }}>{hotel.name}</h4>
                      <p><strong>Price:</strong> ${hotel.price_per_night} / night</p>
                      {hotel.rating && <p><strong>Rating:</strong> {hotel.rating} / 5</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {response.itinerary && (
              <div style={{ marginTop: '2rem' }}>
                <h3>Your Itinerary</h3>
                <div className="glass glass-card" style={{ background: 'rgba(255, 255, 255, 0.05)' }}>
                  <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', lineHeight: '1.6' }}>
                    {response.itinerary}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </>
  )
}

export default App
