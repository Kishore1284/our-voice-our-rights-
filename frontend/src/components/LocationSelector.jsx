import React, { useState, useEffect } from 'react';
import { Navigation, MapPin, AlertCircle, BarChart3, Volume2, Smartphone } from 'lucide-react';
import { apiService } from '../services/api';

export default function LocationSelector({ onDistrictSelect, isLoading, setIsLoading }) {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const [selectedDistrictCode, setSelectedDistrictCode] = useState('');
  const [error, setError] = useState(null);
  const [geolocating, setGeolocating] = useState(false);

  useEffect(() => {
    loadStates();
  }, []);

  useEffect(() => {
    if (selectedState) {
      loadDistricts(selectedState);
    }
  }, [selectedState]);

  const loadStates = async () => {
    try {
      const response = await apiService.getStates();
      setStates(response.states || []);
    } catch (err) {
      console.error('Failed to load states:', err);
    }
  };

  const loadDistricts = async (state) => {
    try {
      const response = await apiService.getDistricts(state);
      setDistricts(response.districts || []);
    } catch (err) {
      console.error('Failed to load districts:', err);
    }
  };

  const handleGeolocate = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.');
      return;
    }

    setGeolocating(true);
    setError(null);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords;
          const response = await apiService.geolocateDistrict(latitude, longitude);
          onDistrictSelect(response.district);
        } catch (err) {
          setError('Failed to find nearest district. Please try manual selection.');
          console.error('Geolocation error:', err);
        } finally {
          setGeolocating(false);
        }
      },
      (err) => {
        setError('Please allow location access to use this feature.');
        setGeolocating(false);
        console.error('Geolocation error:', err);
      }
    );
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    if (selectedDistrictCode) {
      onDistrictSelect({ district_code: selectedDistrictCode });
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Welcome Card */}
      <div className="bg-gradient-to-r from-blue-600 to-green-600 rounded-2xl shadow-xl p-8 text-white">
        <h1 className="text-3xl md:text-4xl font-bold mb-3">
          Our Voice, Our Rights
        </h1>
        <p className="text-lg md:text-xl opacity-90 mb-2">
          MGNREGA Transparency Dashboard
        </p>
        <p className="text-sm opacity-75">
          Track employment and wage payments in your district
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Location Selection */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Select Your District</h2>

        {/* Geolocation Button */}
        <button
          onClick={handleGeolocate}
          disabled={geolocating || isLoading}
          className="w-full mb-6 bg-gradient-to-r from-orange-500 to-red-500 text-white font-semibold py-3 px-6 rounded-lg hover:shadow-lg transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {geolocating ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Finding your location...</span>
            </>
          ) : (
            <>
              <Navigation className="w-5 h-5" />
              <span>Use My Location</span>
            </>
          )}
        </button>

        <div className="border-t border-gray-200 pt-6">
          <p className="text-gray-600 mb-4 text-center">Or select manually</p>

          <form onSubmit={handleManualSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                State
              </label>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select a state</option>
                {states.map((state) => (
                  <option key={state.name} value={state.name}>
                    {state.name} ({state.district_count} districts)
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                District
              </label>
              <select
                value={selectedDistrictCode}
                onChange={(e) => setSelectedDistrictCode(e.target.value)}
                disabled={!selectedState}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100"
              >
                <option value="">Select a district</option>
                {districts.map((district) => (
                  <option key={district.district_code} value={district.district_code}>
                    {district.district_name}
                  </option>
                ))}
              </select>
            </div>

            <button
              type="submit"
              disabled={!selectedDistrictCode || isLoading}
              className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold py-3 px-6 rounded-lg hover:shadow-lg transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <MapPin className="w-5 h-5" />
              <span>View Dashboard</span>
            </button>
          </form>
        </div>
      </div>

      {/* Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-md p-6 text-center">
          <BarChart3 className="w-10 h-10 text-blue-600 mx-auto mb-3" />
          <h3 className="font-semibold text-gray-800 mb-1">Live Data</h3>
          <p className="text-sm text-gray-600">Real-time MGNREGA statistics from data.gov.in</p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-6 text-center">
          <Volume2 className="w-10 h-10 text-green-600 mx-auto mb-3" />
          <h3 className="font-semibold text-gray-800 mb-1">Audio Guide</h3>
          <p className="text-sm text-gray-600">Text-to-speech support in Hindi & English</p>
        </div>
        <div className="bg-white rounded-xl shadow-md p-6 text-center">
          <Smartphone className="w-10 h-10 text-purple-600 mx-auto mb-3" />
          <h3 className="font-semibold text-gray-800 mb-1">Mobile Friendly</h3>
          <p className="text-sm text-gray-600">Optimized for all devices and networks</p>
        </div>
      </div>
    </div>
  );
}

