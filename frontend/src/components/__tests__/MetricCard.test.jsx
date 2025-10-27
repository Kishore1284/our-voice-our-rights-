import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import MetricCard from '../MetricCard'
import { Users } from 'lucide-react'

// Mock speech synthesis
const mockSpeak = vi.fn()
vi.mock('../../utils/speech', () => ({
  speak: () => mockSpeak(),
  generateExplanation: (metricKey, value, comparison) => 
    `Test explanation for ${metricKey} with value ${value}`
}))

describe('MetricCard', () => {
  const props = {
    title: 'People Benefited',
    value: 45000,
    unit: '',
    icon: Users,
    color: 'blue',
    change: 2.27,
    metricKey: 'people_benefited',
    comparison: { people_benefited: 2.27 }
  }

  beforeEach(() => {
    mockSpeak.mockClear()
  })

  it('renders metric card with title and value', () => {
    render(<MetricCard {...props} />)
    
    expect(screen.getByText('People Benefited')).toBeInTheDocument()
    expect(screen.getByText('45.0K')).toBeInTheDocument()
  })

  it('displays positive change with TrendingUp icon', () => {
    render(<MetricCard {...props} />)
    
    expect(screen.getByText('+2.3%')).toBeInTheDocument()
  })

  it('displays negative change with TrendingDown icon', () => {
    render(<MetricCard {...props} change={-5.5} />)
    
    expect(screen.getByText('-5.5%')).toBeInTheDocument()
  })

  it('calls TTS when speaker button clicked', () => {
    render(<MetricCard {...props} />)
    
    const speakButton = screen.getByLabelText('Speak')
    fireEvent.click(speakButton)
    
    expect(mockSpeak).toHaveBeenCalled()
  })

  it('formats large numbers correctly', () => {
    const croreProps = { ...props, value: 50000000 }
    const { rerender } = render(<MetricCard {...croreProps} />)
    expect(screen.getByText(/Cr/)).toBeInTheDocument()
    
    const lakhProps = { ...props, value: 500000 }
    rerender(<MetricCard {...lakhProps} />)
    expect(screen.getByText(/L/)).toBeInTheDocument()
  })
})

