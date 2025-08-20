import React from 'react';
import { Share2, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const ResultsPanel = ({ results, onShare }) => {
  // If no results yet, show placeholder data
  const hasResults = results && results.avgFPS;
  
  const minFPS = hasResults ? results.minFPS : '—';
  const avgFPS = hasResults ? results.avgFPS : '—';
  const maxFPS = hasResults ? results.maxFPS : '—';
  const bottleneck = hasResults ? results.bottleneck : 'pending';
  const gpuScore = hasResults ? results.gpuScore : 0;
  const cpuScore = hasResults ? results.cpuScore : 0;
  const components = hasResults ? results.components : null;

  // Chart data for FPS visualization
  const chartData = {
    labels: ['Min FPS', 'Average FPS', 'Max FPS'],
    datasets: [
      {
        label: 'FPS',
        data: hasResults ? [minFPS, avgFPS, maxFPS] : [0, 0, 0],
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',   // Red for min
          'rgba(59, 130, 246, 0.8)',  // Blue for avg
          'rgba(34, 197, 94, 0.8)',   // Green for max
        ],
        borderColor: [
          'rgba(239, 68, 68, 1)',
          'rgba(59, 130, 246, 1)',
          'rgba(34, 197, 94, 1)',
        ],
        borderWidth: 2,
        borderRadius: 8,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(255, 255, 255, 0.2)',
        borderWidth: 1,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
        },
      },
      x: {
        grid: {
          display: false,
        },
        ticks: {
          color: 'rgba(255, 255, 255, 0.7)',
        },
      },
    },
  };

  const getBottleneckIcon = () => {
    switch (bottleneck) {
      case 'gpu':
        return <AlertTriangle className="w-6 h-6 text-yellow-400" />;
      case 'cpu':
        return <AlertTriangle className="w-6 h-6 text-orange-400" />;
      case 'pending':
        return <div className="w-6 h-6 bg-gray-400 rounded-full animate-pulse" />;
      default:
        return <CheckCircle className="w-6 h-6 text-green-400" />;
    }
  };

  const getBottleneckText = () => {
    switch (bottleneck) {
      case 'gpu':
        return 'GPU Limited';
      case 'cpu':
        return 'CPU Limited';
      case 'pending':
        return 'Pending Analysis';
      default:
        return 'Well Balanced';
    }
  };

  const getBottleneckColor = () => {
    switch (bottleneck) {
      case 'gpu':
        return 'bg-yellow-500/20 border-yellow-500/30 text-yellow-300';
      case 'cpu':
        return 'bg-orange-500/20 border-orange-500/30 text-orange-300';
      case 'pending':
        return 'bg-gray-500/20 border-gray-500/30 text-gray-400';
      default:
        return 'bg-green-500/20 border-green-500/30 text-green-300';
    }
  };

  const getPerformanceRating = () => {
    if (!hasResults) return { text: 'Pending', color: 'text-gray-400', bg: 'bg-gray-500/20' };
    if (avgFPS >= 120) return { text: 'Excellent', color: 'text-green-400', bg: 'bg-green-500/20' };
    if (avgFPS >= 80) return { text: 'Great', color: 'text-blue-400', bg: 'bg-blue-500/20' };
    if (avgFPS >= 60) return { text: 'Good', color: 'text-yellow-400', bg: 'bg-yellow-500/20' };
    if (avgFPS >= 30) return { text: 'Playable', color: 'text-orange-400', bg: 'bg-orange-500/20' };
    return { text: 'Poor', color: 'text-red-400', bg: 'bg-red-500/20' };
  };

  const performanceRating = getPerformanceRating();

  return (
    <div className="bg-white/5 backdrop-blur-sm rounded-lg p-8 border border-white/10">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-white">Performance Results</h2>
        <button
          onClick={onShare}
          disabled={!hasResults}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
            hasResults 
              ? 'bg-white/10 hover:bg-white/20 text-white' 
              : 'bg-gray-600/20 text-gray-500 cursor-not-allowed'
          }`}
        >
          <Share2 className="w-4 h-4" />
          <span>{hasResults ? 'Share' : 'Share (No Results)'}</span>
        </button>
      </div>

      {/* Main FPS Display */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="text-center">
          <div className="text-4xl font-bold text-red-400 mb-2">{minFPS}</div>
          <div className="text-gray-400">Min FPS</div>
        </div>
        <div className="text-center">
          <div className="text-6xl font-bold text-blue-400 mb-2">{avgFPS}</div>
          <div className="text-gray-400">Average FPS</div>
        </div>
        <div className="text-center">
          <div className="text-4xl font-bold text-green-400 mb-2">{maxFPS}</div>
          <div className="text-gray-400">Max FPS</div>
        </div>
      </div>

      {/* Performance Rating */}
      <div className="text-center mb-8">
        <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${performanceRating.bg} ${performanceRating.color}`}>
          {performanceRating.text} Performance
        </span>
      </div>

      {/* FPS Chart */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-white mb-4">FPS Breakdown</h3>
        <div className="h-64">
          <Bar data={chartData} options={chartOptions} />
        </div>
      </div>

      {/* System Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Bottleneck Analysis */}
        <div className="bg-white/5 rounded-lg p-6 border border-white/10">
          <div className="flex items-center space-x-3 mb-4">
            {getBottleneckIcon()}
            <h4 className="text-lg font-semibold text-white">System Bottleneck</h4>
          </div>
          <div className={`inline-block px-3 py-2 rounded-full text-sm font-medium border ${getBottleneckColor()}`}>
            {getBottleneckText()}
          </div>
                            <p className="text-gray-400 text-sm mt-3">
                    {bottleneck === 'gpu' && 'Your graphics card is limiting performance. Consider upgrading to a more powerful GPU.'}
                    {bottleneck === 'cpu' && 'Your processor is limiting performance. A faster CPU would improve your gaming experience.'}
                    {bottleneck === 'balanced' && 'Your system is well-balanced for this game. Both CPU and GPU are working efficiently.'}
                    {bottleneck === 'pending' && 'Run the FPS calculation to analyze your system performance and identify potential bottlenecks.'}
                  </p>
        </div>

        {/* Component Scores */}
        <div className="bg-white/5 rounded-lg p-6 border border-white/10">
          <h4 className="text-lg font-semibold text-white mb-4">Component Performance</h4>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">GPU Score</span>
                <span className="text-white">{gpuScore}/100</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${gpuScore}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">CPU Score</span>
                <span className="text-white">{cpuScore}/100</span>
              </div>
              <div className="w-full bg-white/10 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${cpuScore}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

              {/* Configuration Summary */}
        <div className="bg-white/5 rounded-lg p-6 border border-white/10">
          <h4 className="text-lg font-semibold text-white mb-4">Configuration Summary</h4>
          {hasResults ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-gray-400">GPU:</span>
                <span className="text-white ml-2">{components.gpu.name}</span>
              </div>
              <div>
                <span className="text-gray-400">CPU:</span>
                <span className="text-white ml-2">{components.cpu.name}</span>
              </div>
              <div>
                <span className="text-gray-400">Game:</span>
                <span className="text-white ml-2">{components.game.name}</span>
              </div>
              <div>
                <span className="text-gray-400">Resolution:</span>
                <span className="text-white ml-2">{components.resolution.name}</span>
              </div>
              <div>
                <span className="text-gray-400">Settings:</span>
                <span className="text-white ml-2">{components.settings.name}</span>
              </div>
              <div>
                <span className="text-gray-400">Game Type:</span>
                <span className="text-white ml-2 capitalize">{components.game.genre}</span>
              </div>
            </div>
          ) : (
            <div className="text-center py-8">
              <div className="text-gray-400 text-lg mb-2">No Configuration Selected</div>
              <div className="text-gray-500 text-sm">Select your hardware and game above to see configuration details</div>
            </div>
          )}
        </div>
    </div>
  );
};

export default ResultsPanel;
