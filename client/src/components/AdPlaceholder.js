import React from 'react';
import { Megaphone, Star, Zap, TrendingUp, Shield, Crown, Gift, ArrowRight } from 'lucide-react';

const AdPlaceholder = () => {
  return (
    <div className="space-y-6">
      {/* Premium Upgrade Section */}
      <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 backdrop-blur-sm rounded-lg p-6 border border-purple-500/30">
        <div className="text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl mx-auto mb-4">
            <Crown className="w-6 h-6 text-white" />
          </div>
          
          <h3 className="text-lg font-semibold text-white mb-2">Unlock Premium Features</h3>
          <p className="text-sm text-gray-300 mb-4">
            Get advanced analytics and remove ads
          </p>
          
          <div className="space-y-2 mb-4 text-sm text-gray-300">
            <div className="flex items-center space-x-2">
              <Star className="w-4 h-4 text-yellow-400" />
              <span>Detailed performance breakdowns</span>
            </div>
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span>Historical FPS tracking</span>
            </div>
            <div className="flex items-center space-x-2">
              <Zap className="w-4 h-4 text-blue-400" />
              <span>Upgrade recommendations</span>
            </div>
            <div className="flex items-center space-x-2">
              <Shield className="w-4 h-4 text-purple-400" />
              <span>Ad-free experience</span>
            </div>
          </div>
          
          <button className="w-full bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white px-4 py-3 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
            Upgrade to Pro
          </button>
          
          <p className="text-xs text-gray-400 mt-3">
            Starting at $4.99/month
          </p>
        </div>
      </div>

      {/* Sponsored Hardware Section */}
      <div className="bg-gradient-to-br from-green-900/40 to-emerald-900/40 backdrop-blur-sm rounded-lg p-6 border border-green-500/30">
        <div className="text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl mx-auto mb-4">
            <Zap className="w-6 h-6 text-white" />
          </div>
          
          <h3 className="text-lg font-semibold text-white mb-2">Sponsored: RTX 4070 Ti</h3>
          <p className="text-sm text-gray-300 mb-4">
            Boost your gaming performance
          </p>
          
          <div className="bg-black/30 rounded-lg p-4 mb-4">
            <div className="text-2xl font-bold text-green-400 mb-2">$799</div>
            <div className="text-sm text-gray-300 mb-3">MSRP $799</div>
            <div className="text-xs text-gray-400 space-y-1">
              <div>• 12GB GDDR6X Memory</div>
              <div>• Ray Tracing Ready</div>
              <div>• DLSS 3.0 Support</div>
            </div>
          </div>
          
          <button className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
            <span className="flex items-center justify-center space-x-2">
              <span>Shop Now</span>
              <ArrowRight className="w-4 h-4" />
            </span>
          </button>
          
          <p className="text-xs text-gray-400 mt-3">
            Sponsored by NVIDIA
          </p>
        </div>
      </div>

      {/* Newsletter Signup */}
      <div className="bg-gradient-to-br from-orange-900/40 to-red-900/40 backdrop-blur-sm rounded-lg p-6 border border-orange-500/30">
        <div className="text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl mx-auto mb-4">
            <Gift className="w-6 h-6 text-white" />
          </div>
          
          <h3 className="text-lg font-semibold text-white mb-2">Stay Updated</h3>
          <p className="text-sm text-gray-300 mb-4">
            Get the latest gaming hardware news and FPS tips
          </p>
          
          <div className="space-y-3 mb-4">
            <input 
              type="email" 
              placeholder="Enter your email"
              className="w-full px-3 py-2 bg-black/30 border border-orange-500/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
            <button className="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 text-white px-4 py-2 rounded-lg font-semibold transition-all duration-200 transform hover:scale-105">
              Subscribe Free
            </button>
          </div>
          
          <p className="text-xs text-gray-400">
            Weekly updates • No spam • Unsubscribe anytime
          </p>
        </div>
      </div>

      {/* Banner Ad Placeholder */}
      <div className="bg-gradient-to-br from-gray-900/40 to-slate-900/40 backdrop-blur-sm rounded-lg p-6 border border-gray-700">
        <div className="text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-gray-500 to-slate-500 rounded-xl mx-auto mb-4">
            <Megaphone className="w-6 h-6 text-white" />
          </div>
          
          <h3 className="text-lg font-semibold text-white mb-2">Advertisement</h3>
          <div className="bg-black/30 rounded-lg p-8 mb-4 border-2 border-dashed border-gray-600">
            <div className="text-gray-400 text-sm">
              <div className="text-lg mb-2">📱 300x250</div>
              <div>Banner Ad Space</div>
              <div className="text-xs mt-2">Perfect for hardware retailers</div>
            </div>
          </div>
          
          <p className="text-xs text-gray-400">
            Contact us for advertising opportunities
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdPlaceholder;
