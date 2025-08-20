import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import FPSForm from './components/FPSForm';
import ResultsPanel from './components/ResultsPanel';
import AdPlaceholder from './components/AdPlaceholder';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    gpuId: '',
    cpuId: '',
    gameId: '',
    resolutionId: '1080p',
    settingsId: 'high'
  });
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [appData, setAppData] = useState(null);

  useEffect(() => {
    // Fetch available data on component mount
    fetchAppData();
  }, []);

  const fetchAppData = async () => {
    try {
      const response = await fetch('/api/data');
      const data = await response.json();
      if (data.success) {
        setAppData(data.data);
      }
    } catch (err) {
      console.error('Failed to fetch app data:', err);
    }
  };

  const handleFormSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/estimate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setResults(data.data);
        setFormData(formData);
      } else {
        setError(data.error || 'Failed to get FPS estimate');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleShare = () => {
    if (!results) return;
    
    const shareData = {
      title: 'FPS Estimate Results',
      text: `Check out my FPS estimate: ${results.avgFPS} FPS average on ${results.components.game.name}!`,
      url: window.location.href
    };
    
    if (navigator.share) {
      navigator.share(shareData);
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            <FPSForm 
              appData={appData}
              onSubmit={handleFormSubmit}
              loading={loading}
              initialData={formData}
            />
            
            <ResultsPanel 
              results={results}
              onShare={handleShare}
            />
            
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                <p className="text-red-400 text-center">{error}</p>
              </div>
            )}
          </div>
          
          {/* Sidebar */}
          <div className="space-y-6">
            <AdPlaceholder />
            
            {results && (
              <div className="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-white/10">
                <h3 className="text-lg font-semibold text-white mb-4">Performance Tips</h3>
                <div className="space-y-3 text-sm text-gray-300">
                  {results.bottleneck === 'gpu' && (
                    <p>🎯 Your GPU is the limiting factor. Consider upgrading for better performance.</p>
                  )}
                  {results.bottleneck === 'cpu' && (
                    <p>🎯 Your CPU is the limiting factor. A faster processor would help.</p>
                  )}
                  {results.bottleneck === 'balanced' && (
                    <p>⚖️ Your system is well-balanced for this game.</p>
                  )}
                  <p>💡 Lowering settings can significantly improve FPS.</p>
                  <p>💡 Resolution has the biggest impact on performance.</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
