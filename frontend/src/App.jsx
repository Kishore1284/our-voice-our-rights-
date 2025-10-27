import React, { useState, useEffect } from 'react';
import LocationSelector from './components/LocationSelector';
import Dashboard from './components/Dashboard';
import { loadVoices } from './utils/speech';

export default function App() {
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadVoices();
  }, []);

  const handleDistrictSelect = (district) => {
    setSelectedDistrict(district);
  };

  const handleBack = () => {
    setSelectedDistrict(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-r from-orange-500 to-green-600 text-white text-2xl px-3 py-2 rounded-lg font-bold">
              🇮🇳
            </div>
            <div>
              <h1 className="text-xl md:text-2xl font-bold text-gray-800">
                Our Voice, Our Rights
              </h1>
              <p className="text-sm text-gray-600">MGNREGA Performance Tracker</p>
            </div>
            <div className="ml-auto">
              <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-3 py-1 rounded-full">
                Digital India Initiative
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {selectedDistrict ? (
          <Dashboard district={selectedDistrict} onBack={handleBack} />
        ) : (
          <LocationSelector
            onDistrictSelect={handleDistrictSelect}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12 py-6">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-sm opacity-75">
            Data sourced from{' '}
            <a
              href="https://data.gov.in"
              target="_blank"
              rel="noopener noreferrer"
              className="underline hover:text-blue-300"
            >
              data.gov.in
            </a>
          </p>
          <p className="text-xs opacity-50 mt-2">
            © 2025 Digital India Initiative. Built with transparency and accessibility in mind.
          </p>
        </div>
      </footer>
    </div>
  );
}

