/**
 * Web Speech API Utilities for Text-to-Speech Support
 */

let currentUtterance = null;
let voices = [];

/**
 * Load available voices from browser
 */
export function loadVoices() {
  return new Promise((resolve) => {
    const synth = window.speechSynthesis;
    
    const loadAvailableVoices = () => {
      voices = synth.getVoices();
      resolve(voices);
    };
    
    if (synth.getVoices().length > 0) {
      loadAvailableVoices();
    } else {
      synth.addEventListener('voiceschanged', loadAvailableVoices);
    }
  });
}

/**
 * Speak text using Web Speech API
 * @param {string} text - Text to speak
 * @param {object} options - Speech options (rate, pitch, volume, lang)
 */
export function speak(text, options = {}) {
  stopSpeaking();
  
  if (!window.speechSynthesis) {
    console.error('Speech synthesis not supported');
    return false;
  }
  
  const {
    rate = 0.9,
    pitch = 1.0,
    volume = 1.0,
    lang = 'hi-IN',
  } = options;
  
  currentUtterance = new SpeechSynthesisUtterance(text);
  currentUtterance.rate = rate;
  currentUtterance.pitch = pitch;
  currentUtterance.volume = volume;
  currentUtterance.lang = lang;
  
  // Try to find a Hindi voice, fallback to English
  if (voices.length > 0) {
    const hindiVoice = voices.find(v => v.lang.toLowerCase().includes('hi'));
    if (hindiVoice) {
      currentUtterance.voice = hindiVoice;
    }
  }
  
  try {
    window.speechSynthesis.speak(currentUtterance);
    return true;
  } catch (error) {
    console.error('Speech synthesis error:', error);
    return false;
  }
}

/**
 * Stop current speech
 */
export function stopSpeaking() {
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }
  currentUtterance = null;
}

/**
 * Check if currently speaking
 */
export function isSpeaking() {
  return window.speechSynthesis && window.speechSynthesis.speaking;
}

/**
 * Format number to Indian number format (lakh, crore)
 * @param {number} num - Number to format
 * @returns {string} Formatted string
 */
export function formatIndianNumber(num) {
  if (num >= 10000000) {
    // Crore
    const crore = Math.floor(num / 10000000);
    const remainder = Math.floor((num % 10000000) / 100000);
    if (remainder > 0) {
      return `${crore} crore ${remainder} lakh`;
    }
    return `${crore} crore`;
  } else if (num >= 100000) {
    // Lakh
    const lakh = Math.floor(num / 100000);
    return `${lakh} lakh`;
  } else if (num >= 1000) {
    // Thousand
    const thou = Math.floor(num / 1000);
    return `${thou} thousand`;
  }
  return num.toString();
}

/**
 * Generate text explanation for a metric
 * @param {string} metricKey - Metric key (e.g., "people_benefited")
 * @param {object} value - Current value
 * @param {object} comparison - Comparison object with percentage changes
 * @returns {string} Text explanation ready for TTS
 */
export function generateExplanation(metricKey, value, comparison = {}) {
  const explanations = {
    people_benefited: {
      label: 'People Benefited',
      description: `${formatIndianNumber(value.people_benefited)} people benefited from MGNREGA work.`,
    },
    workdays_created: {
      label: 'Workdays Created',
      description: `${formatIndianNumber(value.workdays_created)} workdays were created.`,
    },
    wages_paid: {
      label: 'Wages Paid',
      description: `Wages of ${formatIndianNumber(value.wages_paid)} rupees were paid.`,
    },
    payments_on_time_percent: {
      label: 'On-Time Payments',
      description: `${value.payments_on_time_percent.toFixed(1)} percent of payments were made on time.`,
    },
    works_completed: {
      label: 'Works Completed',
      description: `${formatIndianNumber(value.works_completed)} works were completed.`,
    },
  };
  
  const metric = explanations[metricKey];
  if (!metric) return 'Metric not found.';
  
  let text = metric.description;
  
  // Add comparison if available
  const change = comparison[metricKey];
  if (change !== undefined && change !== null) {
    const absChange = Math.abs(change);
    if (change > 0) {
      text += ` This is ${absChange.toFixed(1)} percent more than the previous month.`;
    } else if (change < 0) {
      text += ` This is ${absChange.toFixed(1)} percent less than the previous month.`;
    } else {
      text += ' This is similar to the previous month.';
    }
  }
  
  return text;
}

