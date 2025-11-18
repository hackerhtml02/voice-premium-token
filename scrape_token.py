import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Import ChromeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

# --- Configuration ---
SPEECHIFY_URL = 'https://speechify.com/ai-voice-generator/?srsltid=AfmBOorvkHeSrsqo_GxU6dTF_sQwml06_WS9j5RqOCKlKPGa9yNO-J6T'
API_URL = 'https://api.sws.speechify.com/v1/audio/stream'

# --- Element Selectors ---
TEXTAREA_SELECTOR = (By.CSS_SELECTOR, 'textarea[aria-label="Text to convert to speech"]')
PLAY_BUTTON_SELECTOR = (By.CSS_SELECTOR, 'button[data-testid="voice-demo-button"]')

# --- WebDriver Setup for Headless Mode ---
# Create an instance of ChromeOptions
chrome_options = ChromeOptions()
# Add the headless argument
chrome_options.add_argument("--headless")
# These arguments are recommended for running in a headless environment
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--log-level=3") # Suppress console logs for a cleaner output

# Initialize the Chrome WebDriver with selenium-wire and the specified options
# The 'options' keyword argument is used for selenium-wire
driver = webdriver.Chrome(options=chrome_options)

try:
    # --- Navigation and Interaction ---
    print(f"Navigating to {SPEECHIFY_URL} (in headless mode)")
    driver.get(SPEECHIFY_URL)

    wait = WebDriverWait(driver, 20)

    # 1. Wait for the text area
    print("Waiting for the text area to load...")
    wait.until(
        EC.presence_of_element_located(TEXTAREA_SELECTOR)
    )
    print("Text area found.")

    # 2. Wait for the play button
    print("Waiting for the play button to become clickable...")
    play_button = wait.until(
        EC.element_to_be_clickable(PLAY_BUTTON_SELECTOR)
    )

    print("Play button found. Clicking now...")
    play_button.click()

    # --- Network Request Interception ---
    print(f"Waiting for request to '{API_URL}'...")
    request = driver.wait_for_request(API_URL, timeout=20)

    # --- Token Extraction ---
    if request:
        print("API request captured successfully!")
        auth_header = request.headers.get('Authorization')

        if auth_header:
            bearer_token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            print("Token extracted:", bearer_token)

            # NEW: Save token into token.txt
            with open("token.txt", "w") as f:
                f.write(bearer_token)

        else:
            print("Authorization header not found.")
    else:
        print("Could not find the specified API request.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # --- Cleanup ---
    print("Script finished. Closing the driver.")
    driver.quit()
