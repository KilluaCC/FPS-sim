import React, { useState, useEffect } from 'react';
import { Search, Cpu, Monitor, Gamepad2, Settings, MonitorSmartphone } from 'lucide-react';

const FPSForm = ({ appData, onSubmit, loading, initialData }) => {
  const [formData, setFormData] = useState(initialData);
  const [gpuSearch, setGpuSearch] = useState('');
  const [cpuSearch, setCpuSearch] = useState('');
  const [gameSearch, setGameSearch] = useState('');

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
      <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-white/10 rounded w-1/4"></div>
          <div className="h-10 bg-white/10 rounded"></div>
          <div className="h-10 bg-white/10 rounded"></div>
          <div className="h-10 bg-white/10 rounded"></div>
        </div>
      </div>
    );
  }

  const filteredGPUs = appData.gpus.filter(gpu => 
    gpu.name.toLowerCase().includes(gpuSearch.toLowerCase())
  );
  const filteredCPUs = appData.cpus.filter(cpu => 
    cpu.name.toLowerCase().includes(cpuSearch.toLowerCase())
  );
  const filteredGames = appData.games.filter(game => 
    game.name.toLowerCase().includes(gameSearch.toLowerCase())
  );

  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Estimate Your FPS</h2>
        <p className="text-gray-300">Select your hardware and game to get performance estimates</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* GPU Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            <Monitor className="inline w-4 h-4 mr-2" />
            Graphics Card (GPU)
          </label>
          <div className="relative">
            <input
              type="text"
              placeholder="Search GPUs..."
              value={gpuSearch}
              onChange={(e) => setGpuSearch(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
          </div>
          <div className="mt-2 max-h-48 overflow-y-auto space-y-1">
            {filteredGPUs.map(gpu => (
              <button
                key={gpu.id}
                type="button"
                onClick={() => handleInputChange('gpuId', gpu.id)}
                className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                  formData.gpuId === gpu.id
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    : 'text-gray-300 hover:bg-white/10'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>{gpu.name}</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    gpu.tier === 'flagship' ? 'bg-purple-500/20 text-purple-300' :
                    gpu.tier === 'high-end' ? 'bg-blue-500/20 text-blue-300' :
                    gpu.tier === 'mid-high' ? 'bg-green-500/20 text-green-300' :
                    'bg-yellow-500/20 text-yellow-300'
                  }`}>
                    {gpu.tier}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* CPU Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            <Cpu className="inline w-4 h-4 mr-2" />
            Processor (CPU)
          </label>
          <div className="relative">
            <input
              type="text"
              placeholder="Search CPUs..."
              value={cpuSearch}
              onChange={(e) => setCpuSearch(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
          </div>
          <div className="mt-2 max-h-48 overflow-y-auto space-y-1">
            {filteredCPUs.map(cpu => (
              <button
                key={cpu.id}
                type="button"
                onClick={() => handleInputChange('cpuId', cpu.id)}
                className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                  formData.cpuId === cpu.id
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    : 'text-gray-300 hover:bg-white/10'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>{cpu.name}</span>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    cpu.tier === 'flagship' ? 'bg-purple-500/20 text-purple-300' :
                    cpu.tier === 'high-end' ? 'bg-blue-500/20 text-blue-300' :
                    cpu.tier === 'mid-high' ? 'bg-green-500/20 text-green-300' :
                    'bg-yellow-500/20 text-yellow-300'
                  }`}>
                    {cpu.tier}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Game Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            <Gamepad2 className="inline w-4 h-4 mr-2" />
            Game
          </label>
          <div className="relative">
            <input
              type="text"
              placeholder="Search games..."
              value={gameSearch}
              onChange={(e) => setGameSearch(e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <Search className="absolute right-3 top-3 w-5 h-5 text-gray-400" />
          </div>
          <div className="mt-2 max-h-48 overflow-y-auto space-y-1">
            {filteredGames.map(game => (
              <button
                key={game.id}
                type="button"
                onClick={() => handleInputChange('gameId', game.id)}
                className={`w-full text-left px-3 py-2 rounded-md transition-colors ${
                  formData.gameId === game.id
                    ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    : 'text-gray-300 hover:bg-white/10'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span>{game.name}</span>
                  <span className="px-2 py-1 text-xs rounded-full bg-gray-500/20 text-gray-300">
                    {game.genre}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Resolution and Settings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <MonitorSmartphone className="inline w-4 h-4 mr-2" />
              Resolution
            </label>
            <select
              value={formData.resolutionId}
              onChange={(e) => handleInputChange('resolutionId', e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
              value={formData.settingsId}
              onChange={(e) => handleInputChange('settingsId', e.target.value)}
              className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
