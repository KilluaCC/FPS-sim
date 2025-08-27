import React, { useState, useEffect } from 'react';
import { Cpu, Monitor, Gamepad2, Settings, MonitorSmartphone } from 'lucide-react';

const FPSForm = ({ appData, onSubmit, loading, initialData }) => {
  const [formData, setFormData] = useState(initialData);

  useEffect(() => {
    setFormData(initialData);
  }, [initialData]);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.gpuId && formData.cpuId && formData.gameId) {
      onSubmit(formData);
    }
  };

  const isFormValid = formData.gpuId && formData.cpuId && formData.gameId;

  if (!appData) {
    return (
      <div className="bg-black/40 backdrop-blur-sm rounded-lg p-8 border border-gray-800">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-700 rounded w-1/4"></div>
          <div className="h-10 bg-gray-700 rounded"></div>
          <div className="h-10 bg-gray-700 rounded"></div>
          <div className="h-10 bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }



  return (
    <div className="bg-black/40 backdrop-blur-sm rounded-lg p-8 border border-gray-800">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Estimate Your FPS</h2>
        <p className="text-gray-300">Select your hardware and game to get performance estimates</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Hardware Selection - Side by Side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* GPU Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Monitor className="inline w-4 h-4 mr-2" />
              Graphics Card (GPU)
            </label>
            <div className="relative">
              <select
                value={formData.gpuId}
                onChange={(e) => handleInputChange('gpuId', e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="" className="bg-gray-800 text-gray-400">Select a GPU...</option>
                {appData.gpus.map(gpu => (
                  <option key={gpu.id} value={gpu.id} className="bg-gray-800 text-white">
                    {gpu.name} ({gpu.tier})
                  </option>
                ))}
              </select>
            </div>
            {formData.gpuId && (
              <div className="mt-2 space-y-1">
                <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                  appData.gpus.find(g => g.id === formData.gpuId)?.tier === 'flagship' ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' :
                  appData.gpus.find(g => g.id === formData.gpuId)?.tier === 'high-end' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' :
                  appData.gpus.find(g => g.id === formData.gpuId)?.tier === 'mid-high' ? 'bg-green-500/20 text-green-300 border border-green-500/30' :
                  'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30'
                }`}>
                  {appData.gpus.find(g => g.id === formData.gpuId)?.tier} Tier
                </span>
                {appData.gpus.find(g => g.id === formData.gpuId)?.price && (
                  <div className="text-xs text-gray-400">
                    💰 ${appData.gpus.find(g => g.id === formData.gpuId)?.price}
                  </div>
                )}
                {appData.gpus.find(g => g.id === formData.gpuId)?.brand && (
                  <div className="text-xs text-gray-400">
                    🏷️ {appData.gpus.find(g => g.id === formData.gpuId)?.brand}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* CPU Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Cpu className="inline w-4 h-4 mr-2" />
              Processor (CPU)
            </label>
            <div className="relative">
              <select
                value={formData.cpuId}
                onChange={(e) => handleInputChange('cpuId', e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="" className="bg-gray-800 text-gray-400">Select a CPU...</option>
                {appData.cpus.map(cpu => (
                  <option key={cpu.id} value={cpu.id} className="bg-gray-800 text-white">
                    {cpu.name} ({cpu.tier})
                  </option>
                ))}
              </select>
            </div>
            {formData.cpuId && (
              <div className="mt-2 space-y-1">
                <span className={`inline-block px-2 py-1 text-xs rounded-full ${
                  appData.cpus.find(c => c.id === formData.cpuId)?.tier === 'flagship' ? 'bg-purple-500/20 text-purple-300 border border-purple-500/30' :
                  appData.cpus.find(c => c.id === formData.cpuId)?.tier === 'high-end' ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' :
                  appData.cpus.find(c => c.id === formData.cpuId)?.tier === 'mid-high' ? 'bg-green-500/20 text-green-300 border border-green-500/30' :
                  'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30'
                }`}>
                  {appData.cpus.find(c => c.id === formData.cpuId)?.tier} Tier
                </span>
                {appData.cpus.find(c => c.id === formData.cpuId)?.price && (
                  <div className="text-xs text-gray-400">
                    💰 ${appData.cpus.find(c => c.id === formData.cpuId)?.price}
                  </div>
                )}
                {appData.cpus.find(c => c.id === formData.cpuId)?.brand && (
                  <div className="text-xs text-gray-400">
                    🏷️ {appData.cpus.find(c => c.id === formData.cpuId)?.brand}
                  </div>
                )}
                {appData.cpus.find(c => c.id === formData.cpuId)?.cores && (
                  <div className="text-xs text-gray-400">
                    🔧 {appData.cpus.find(c => c.id === formData.cpuId)?.cores} cores / {appData.cpus.find(c => c.id === formData.cpuId)?.threads} threads
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Game Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            <Gamepad2 className="inline w-4 h-4 mr-2" />
            Game
          </label>
          <div className="relative">
            <select
              value={formData.gameId}
              onChange={(e) => handleInputChange('gameId', e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="" className="bg-gray-800 text-gray-400">Select a game...</option>
              {appData.games.map(game => (
                <option key={game.id} value={game.id} className="bg-gray-800 text-white">
                  {game.name} ({game.genre})
                </option>
              ))}
            </select>
          </div>
          {formData.gameId && (
            <div className="mt-2 space-y-1">
              <span className="inline-block px-2 py-1 text-xs rounded-full bg-gray-500/20 text-gray-300 border border-gray-500/30">
                {appData.games.find(g => g.id === formData.gameId)?.genre}
              </span>
              {appData.games.find(g => g.id === formData.gameId)?.gpuIntensive && (
                <div className="text-xs text-red-400">
                  🔥 GPU Intensive
                </div>
              )}
              {appData.games.find(g => g.id === formData.gameId)?.cpuIntensive && (
                <div className="text-xs text-blue-400">
                  ⚡ CPU Intensive
                </div>
              )}
              {appData.games.find(g => g.id === formData.gameId)?.rayTracingSupport && (
                <div className="text-xs text-purple-400">
                  ✨ Ray Tracing Support
                </div>
              )}
            </div>
          )}
        </div>

        {/* Resolution and Settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <MonitorSmartphone className="inline w-4 h-4 mr-2" />
              Resolution
            </label>
            <select
              value={formData.resolution}
              onChange={(e) => handleInputChange('resolution', e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {appData.resolutions.map(res => (
                <option key={res.id} value={res.id} className="bg-gray-800 text-white">
                  {res.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <Settings className="inline w-4 h-4 mr-2" />
              Graphics Settings
            </label>
            <select
              value={formData.settings}
              onChange={(e) => handleInputChange('settings', e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {appData.settings.map(setting => (
                <option key={setting.id} value={setting.id} className="bg-gray-800 text-white">
                  {setting.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={!isFormValid || loading}
          className={`w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-200 transform ${
            isFormValid && !loading
              ? 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white hover:scale-105'
              : 'bg-gray-600 text-gray-400 cursor-not-allowed'
          }`}
        >
          {loading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              <span>Calculating...</span>
            </div>
          ) : (
            'Calculate FPS Estimate'
          )}
        </button>
      </form>
    </div>
  );
};

export default FPSForm;
