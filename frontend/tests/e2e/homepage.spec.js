import { test, expect } from '@playwright/test'

test.describe('Homepage', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('has correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/Our Voice, Our Rights/)
  })

  test('renders welcome header', async ({ page }) => {
    await expect(page.getByText(/Our Voice, Our Rights/i)).toBeVisible()
    await expect(page.getByText(/MGNREGA Transparency Dashboard/i)).toBeVisible()
  })

  test('displays district selector', async ({ page }) => {
    await expect(page.getByText(/Select Your District/i)).toBeVisible()
    await expect(page.getByText(/Use My Location/i)).toBeVisible()
    await expect(page.getByText(/Or select manually/i)).toBeVisible()
  })

  test('shows info cards', async ({ page }) => {
    await expect(page.getByText(/Live Data/i)).toBeVisible()
    await expect(page.getByText(/Audio Guide/i)).toBeVisible()
    await expect(page.getByText(/Mobile Friendly/i)).toBeVisible()
  })
})

test.describe('Location Selection', () => {
  test('clicking "Use My Location" triggers geolocation', async ({ page, context }) => {
    await page.goto('/')
    
    // Grant geolocation permission
    await context.grantPermissions(['geolocation'])
    
    // Mock geolocation
    await context.addInitScript(() => {
      navigator.geolocation.getCurrentPosition = async (success) => {
        success({
          coords: {
            latitude: 26.8467,
            longitude: 80.9462
          }
        })
      }
    })
    
    const locationButton = page.getByText(/Use My Location/i)
    await expect(locationButton).toBeVisible()
    
    // Click should not throw
    await locationButton.click()
  })
})

