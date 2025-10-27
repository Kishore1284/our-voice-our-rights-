/**
 * Mock Service Worker handlers for API mocking
 */

export const handlers = [
  // Mock GET /api/v1/districts/states
  {
    method: 'GET',
    url: '/api/v1/districts/states',
    response: {
      states: [
        { name: 'Uttar Pradesh', district_count: 15 },
        { name: 'Bihar', district_count: 10 }
      ]
    }
  },

  // Mock GET /api/v1/districts
  {
    method: 'GET',
    url: '/api/v1/districts',
    response: {
      districts: [
        {
          id: 1,
          state: 'Uttar Pradesh',
          district_name: 'Lucknow',
          district_code: 'UP-LUC'
        },
        {
          id: 2,
          state: 'Uttar Pradesh',
          district_name: 'Kanpur Nagar',
          district_code: 'UP-KAN'
        }
      ],
      total: 2
    }
  },

  // Mock GET /api/v1/districts/{code}/snapshot
  {
    method: 'GET',
    url: '/api/v1/districts/UP-LUC/snapshot',
    response: {
      current: {
        year: 2025,
        month: 1,
        people_benefited: 45000,
        workdays_created: 900000,
        wages_paid: 158400000.00,
        payments_on_time_percent: 92.5,
        works_completed: 350
      },
      previous: {
        year: 2024,
        month: 12,
        people_benefited: 44000,
        workdays_created: 880000,
        wages_paid: 154880000.00,
        payments_on_time_percent: 91.0,
        works_completed: 340
      },
      district: {
        id: 1,
        state: 'Uttar Pradesh',
        district_name: 'Lucknow',
        district_code: 'UP-LUC'
      },
      comparison: {
        people_benefited: 2.27,
        workdays_created: 2.27,
        wages_paid: 2.27,
        payments_on_time_percent: 1.65,
        works_completed: 2.94
      }
    }
  },

  // Mock GET /api/v1/geolocate/test
  {
    method: 'GET',
    url: '/api/v1/geolocate/test',
    response: {
      district: {
        id: 1,
        state: 'Uttar Pradesh',
        district_name: 'Lucknow',
        district_code: 'UP-LUC'
      },
      distance_km: 0.5
    }
  }
]

