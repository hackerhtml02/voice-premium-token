import time
import base64
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

SPEECHIFY_URL = 'https://speechify.com/ai-voice-generator/?srsltid=AfmBOorvkHeSrsqo_GxU6dTF_sQwml06_WS9j5RqOCKlKPGa9yNO-J6T'
API_URL = 'https://api.sws.speechify.com/v1/audio/stream'

TEXTAREA_SELECTOR = (By.CSS_SELECTOR, 'textarea[aria-label="Text to convert to speech"]')
PLAY_BUTTON_SELECTOR = (By.CSS_SELECTOR, 'button[data-testid="voice-demo-button"]')

# Chrome headless setup
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    print("Opening page...")
    driver.get(SPEECHIFY_URL)
    wait = WebDriverWait(driver, 20)

    wait.until(EC.presence_of_element_located(TEXTAREA_SELECTOR))
    print("Textarea found")

    play_btn = wait.until(EC.element_to_be_clickable(PLAY_BUTTON_SELECTOR))
    print("Clicking play...")
    play_btn.click()

    print("Waiting for API call...")
    request = driver.wait_for_request(API_URL, timeout=20)

    if request:
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split(" ")[1]
            print("Token extracted:", token)

            # ----------------------------
            # Encode to Base64
            encoded_token = base64.b64encode(token.encode()).decode()
            print("Encoded Token:", encoded_token)
            # ----------------------------

            # Save token to file
            with open("token.txt", "w") as f:
                f.write(encoded_token)
        else:
            print("Authorization missing!")
    else:
        print("API call not found!")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
