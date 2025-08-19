import React from 'react';
import { Monitor, Zap } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-black/20 backdrop-blur-sm border-b border-white/10">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
              <Monitor className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">FPS Estimator</h1>
              <p className="text-sm text-gray-400">Game Performance Calculator</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <a href="#about" className="text-gray-300 hover:text-white transition-colors">
              About
            </a>
            <a href="#contact" className="text-gray-300 hover:text-white transition-colors">
              Contact
            </a>
            <button className="flex items-center space-x-2 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-4 py-2 rounded-lg transition-all duration-200 transform hover:scale-105">
              <Zap className="w-4 h-4" />
              <span>Pro Version</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
