/**
 * Vitest setup file for frontend tests
 */

import { expect, afterEach, vi } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

// Extend Vitest's expect with Jest-DOM matchers
expect.extend(matchers)

// Cleanup after each test
afterEach(() => {
  cleanup()
})

// Mock window.speechSynthesis
global.speechSynthesis = {
  speak: vi.fn(),
  cancel: vi.fn(),
  getVoices: () => [
    { lang: 'hi-IN', name: 'Hindi', voiceURI: 'hindi' },
    { lang: 'en-US', name: 'English', voiceURI: 'english' }
  ]
}

// Mock geolocation API
global.navigator.geolocation = {
  getCurrentPosition: vi.fn((success, error) => {
    success({
      coords: {
        latitude: 26.8467,
        longitude: 80.9462
      }
    })
  })
}

