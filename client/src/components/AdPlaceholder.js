import React from 'react';
import { Megaphone, Star } from 'lucide-react';

const AdPlaceholder = () => {
  return (
    <div className="bg-gradient-to-br from-yellow-500/10 to-orange-500/10 backdrop-blur-sm rounded-lg p-6 border border-yellow-500/20">
      <div className="text-center">
        <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl mx-auto mb-4">
          <Megaphone className="w-6 h-6 text-white" />
        </div>
        
        <h3 className="text-lg font-semibold text-white mb-2">Premium Features</h3>
        <p className="text-sm text-gray-300 mb-4">
          Unlock advanced analytics and remove ads
        </p>
        
        <div className="space-y-2 mb-4 text-sm text-gray-300">
          <div className="flex items-center space-x-2">
            <Star className="w-4 h-4 text-yellow-400" />
            <span>Detailed performance breakdowns</span>
          </div>
          <div className="flex items-center space-x-2">
            <Star className="w-4 h-4 text-yellow-400" />
            <span>Historical FPS tracking</span>
          </div>
          <div className="flex items-center space-x-2">
            <Star className="w-4 h-4 text-yellow-400" />
            <span>Upgrade recommendations</span>
          </div>
          <div className="flex items-center space-x-2">
            <Star className="w-4 h-4 text-yellow-400" />
            <span>Ad-free experience</span>
          </div>
        </div>
        
        <button className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-4 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
          Upgrade to Pro
        </button>
        
        <p className="text-xs text-gray-400 mt-3">
          Starting at $4.99/month
        </p>
      </div>
    </div>
  );
};

export default AdPlaceholder;
