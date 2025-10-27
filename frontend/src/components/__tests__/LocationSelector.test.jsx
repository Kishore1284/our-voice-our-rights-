import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import LocationSelector from '../LocationSelector'
import { apiService } from '../../services/api'

// Mock the API service
vi.mock('../../services/api', () => ({
  apiService: {
    getStates: vi.fn().mockResolvedValue({
      states: [
        { name: 'Uttar Pradesh', district_count: 15 }
      ]
    }),
    getDistricts: vi.fn().mockResolvedValue({
      districts: [
        { id: 1, state: 'Uttar Pradesh', district_name: 'Lucknow', district_code: 'UP-LUC' }
      ],
      total: 1
    }),
    geolocateDistrict: vi.fn().mockResolvedValue({
      district: { id: 1, district_code: 'UP-LUC' }
    })
  }
}))

describe('LocationSelector', () => {
  it('renders location selector with states dropdown', () => {
    const onDistrictSelect = vi.fn()
    
    render(<LocationSelector onDistrictSelect={onDistrictSelect} />)
    
    expect(screen.getByText(/Select Your District/i)).toBeInTheDocument()
    expect(screen.getByText(/Use My Location/i)).toBeInTheDocument()
  })

  it('triggers onDistrictSelect when "Use My Location" clicked', async () => {
    const onDistrictSelect = vi.fn()
    
    render(<LocationSelector onDistrictSelect={onDistrictSelect} />)
    
    const button = screen.getByText(/Use My Location/i)
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(apiService.geolocateDistrict).toHaveBeenCalled()
    })
  })

  it('displays error when geolocation fails', async () => {
    const onDistrictSelect = vi.fn()
    
    // Mock geolocation error
    global.navigator.geolocation.getCurrentPosition = vi.fn((success, error) => {
      error({ code: 1, message: 'Permission denied' })
    })
    
    render(<LocationSelector onDistrictSelect={onDistrictSelect} />)
    
    const button = screen.getByText(/Use My Location/i)
    fireEvent.click(button)
    
    await waitFor(() => {
      expect(screen.getByText(/Please allow location access/i)).toBeInTheDocument()
    })
  })
})

