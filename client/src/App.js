import React, { useState, useEffect } from 'react';
import { Zap, TrendingUp, Crown } from 'lucide-react';
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
    resolution: '1080p',
    settings: 'High'
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
      // Convert string IDs to numbers for the API
      const apiData = {
        ...formData,
        gpuId: parseInt(formData.gpuId),
        cpuId: parseInt(formData.cpuId),
        gameId: parseInt(formData.gameId)
      };
      
      const response = await fetch('/api/estimate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(apiData),
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
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Top Banner Ad */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-900/40 to-purple-900/40 backdrop-blur-sm rounded-lg p-6 border border-blue-500/30">
            <div className="text-center">
              <div className="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl mx-auto mb-4">
                <Zap className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Sponsored: Gaming Gear Sale</h3>
              <p className="text-gray-300 mb-4">Up to 40% off on gaming mice, keyboards, and headsets</p>
              <button className="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white px-6 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
                Shop Now - Limited Time!
              </button>
              <p className="text-xs text-gray-400 mt-3">Sponsored by GamingCorp</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            <FPSForm 
              appData={appData}
              onSubmit={handleFormSubmit}
              loading={loading}
              initialData={formData}
            />
            
            {/* Inline Ad */}
            <div className="bg-gradient-to-r from-green-900/40 to-blue-900/40 backdrop-blur-sm rounded-lg p-6 border border-green-500/30">
              <div className="text-center">
                <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl mx-auto mb-3">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Boost Your FPS</h3>
                <p className="text-gray-300 mb-4">Get the latest drivers and optimization tips</p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div className="bg-black/30 rounded-lg p-3">
                    <div className="text-green-400 font-semibold">NVIDIA</div>
                    <div className="text-xs text-gray-400">Latest Drivers</div>
                  </div>
                  <div className="bg-black/30 rounded-lg p-3">
                    <div className="text-blue-400 font-semibold">AMD</div>
                    <div className="text-xs text-gray-400">Adrenalin Software</div>
                  </div>
                  <div className="bg-black/30 rounded-lg p-3">
                    <div className="text-purple-400 font-semibold">Intel</div>
                    <div className="text-xs text-gray-400">Graphics Drivers</div>
                  </div>
                </div>
                <button className="bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-600 hover:to-blue-600 text-white px-6 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
                  Download Now
                </button>
              </div>
            </div>
            
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
              <div className="bg-black/40 backdrop-blur-sm rounded-lg p-6 border border-gray-800">
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
        
        {/* Footer Ad Section */}
        <div className="mt-12">
          <div className="bg-gradient-to-r from-purple-900/40 to-pink-900/40 backdrop-blur-sm rounded-lg p-8 border border-purple-500/30">
            <div className="text-center">
              <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl mx-auto mb-6">
                <Crown className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Join the Elite Gamers</h3>
              <p className="text-gray-300 mb-6 text-lg">Get exclusive access to premium gaming content, early hardware reviews, and member-only discounts</p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-black/30 rounded-lg p-4">
                  <div className="text-purple-400 font-bold text-lg mb-2">🎮</div>
                  <div className="text-white font-semibold">Exclusive Content</div>
                  <div className="text-xs text-gray-400">Early access to reviews</div>
                </div>
                <div className="bg-black/30 rounded-lg p-4">
                  <div className="text-pink-400 font-bold text-lg mb-2">💰</div>
                  <div className="text-white font-semibold">Member Discounts</div>
                  <div className="text-xs text-gray-400">Up to 25% off hardware</div>
                </div>
                <div className="bg-black/30 rounded-lg p-4">
                  <div className="text-blue-400 font-bold text-lg mb-2">🚀</div>
                  <div className="text-white font-semibold">Priority Support</div>
                  <div className="text-xs text-gray-400">24/7 expert help</div>
                </div>
              </div>
              <button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white px-8 py-4 rounded-lg font-bold text-lg transition-all duration-200 transform hover:scale-105">
                Become a Member - $9.99/month
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
