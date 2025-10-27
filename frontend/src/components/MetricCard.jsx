import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Minus, Volume2, VolumeX } from 'lucide-react';
import { speak, stopSpeaking, generateExplanation } from '../utils/speech';

export default function MetricCard({
  title,
  value,
  unit = '',
  icon: Icon,
  color = 'blue',
  change,
  metricKey,
  comparison = {},
}) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const formatNumber = (num) => {
    if (num >= 10000000) {
      return (num / 10000000).toFixed(2) + 'Cr';
    } else if (num >= 100000) {
      return (num / 100000).toFixed(2) + 'L';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const handleSpeak = () => {
    if (isSpeaking) {
      stopSpeaking();
      setIsSpeaking(false);
    } else {
      const text = generateExplanation(metricKey, { [metricKey]: value }, comparison);
      speak(text, { lang: 'hi-IN' });
      setIsSpeaking(true);
      setTimeout(() => setIsSpeaking(false), 1000);
    }
  };

  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    orange: 'from-orange-500 to-orange-600',
    purple: 'from-purple-500 to-purple-600',
    pink: 'from-pink-500 to-pink-600',
  };

  const gradientClass = colorClasses[color] || colorClasses.blue;

  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden">
      {/* Header */}
      <div className={`bg-gradient-to-r ${gradientClass} p-4 flex items-center justify-between`}>
        <div className="flex items-center space-x-2">
          {Icon && <Icon className="w-6 h-6 text-white" />}
          <h3 className="text-white font-semibold text-sm">{title}</h3>
        </div>
        <button
          onClick={handleSpeak}
          className="p-1 rounded-full hover:bg-white/20 transition-colors"
          aria-label="Speak"
        >
          {isSpeaking ? (
            <VolumeX className="w-5 h-5 text-white" />
          ) : (
            <Volume2 className="w-5 h-5 text-white" />
          )}
        </button>
      </div>

      {/* Value */}
      <div className="p-6">
        <div className="text-3xl sm:text-4xl font-bold text-gray-800 mb-2">
          {formatNumber(value)}
          {unit && <span className="text-xl text-gray-600"> {unit}</span>}
        </div>

        {/* Change indicator */}
        {change !== undefined && change !== null && (
          <div className="flex items-center space-x-1 text-sm">
            {change > 0 && (
              <>
                <TrendingUp className="w-4 h-4 text-green-600" />
                <span className="text-green-600 font-semibold">+{change.toFixed(1)}%</span>
              </>
            )}
            {change < 0 && (
              <>
                <TrendingDown className="w-4 h-4 text-red-600" />
                <span className="text-red-600 font-semibold">{change.toFixed(1)}%</span>
              </>
            )}
            {change === 0 && (
              <>
                <Minus className="w-4 h-4 text-gray-600" />
                <span className="text-gray-600">No change</span>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

