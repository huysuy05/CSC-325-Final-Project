import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


# --- FUNCTION TO WAIT FOR EXPORTING FILE --- 
def wait_for_download(path, timeout=120):
    secs = 0
    while secs < timeout:
        files = os.listdir(path)
        downloading = [f for f in files if f.endswith(".crdownload")]
        if not downloading and len(files) > 0:
            return True
        time.sleep(1)
        secs += 1
    return False


# Variable names for each data values
TARGET_URL = "http://data.cityofchicago.org/stories/s/Crimes-2001-to-present-Dashboard/5cd6-ry5g"

# Table element
GRID_ROOT_SELECTOR = (By.CSS_SELECTOR, '[data-block-id="clientSideId_10"]')

# Data locator button to export data
DATA_LOCATOR_BUTTON = '[data-testid="vertical-kabob"]'

# Export data button
EXPORT_DATA_BTN = '[data-testid="export-data-link"]'

# Download data button
DOWNLOAD_DATA_BTN = '[data-testid="export-download-button"]'

# Set the path to export the file to
OUTPUT_DIR = os.path.abspath("../datasets")
chrome_options = Options()
prefs = {
    "download.default_directory": OUTPUT_DIR,  # ← Your download folder
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)


print("--- STARTING CRAWLING PROCESS ---")


# --- WEBDRIVER SETUP ---
service = Service(ChromeDriverManager().install()) #Chrome Drive manager to be able to run chrome
driver = webdriver.Chrome(service=service, options=chrome_options)
print("   --> Navigating to the website...")
driver.get(TARGET_URL)


# --- SCRAPING LOOP ---
try:
    while True:
        print(f"--- CRAWLING, LOCKING INNNN ---")
        # Locate to the table element
        table = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(GRID_ROOT_SELECTOR)
        )
        data_btn = table.find_element(By.CSS_SELECTOR, DATA_LOCATOR_BUTTON)
        
        # Scroll to view the button
        driver.execute_script("arguments[0].scrollIntoView(true)", data_btn)
        time.sleep(3)
        print(f"    - Checking if the button is found: {data_btn.is_displayed()}")
        print(f"    - Checking if the button is enable: {data_btn.is_enabled()}")
        actions = ActionChains(driver)
        actions.move_to_element(data_btn).click().perform()
        time.sleep(10)
        
        WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'forge-popup[role="menu"]'))
        )

        # Locate to the export data button
        export_btn = driver.find_element(By.CSS_SELECTOR, EXPORT_DATA_BTN)
        print("Export button found..." if export_btn.is_displayed() else "Export button not found")
        actions.move_to_element(export_btn).click().perform()
        time.sleep(30)

        # Download the data
        if export_btn.is_displayed():
            try:
                download_btn = driver.find_element(By.CSS_SELECTOR, DOWNLOAD_DATA_BTN)
                time.sleep(3)
                actions.move_to_element(download_btn).click().perform()
                if wait_for_download(OUTPUT_DIR):
                    break
            except TimeoutError:
                print("Download button not found...")
                break
        


except TimeoutException:
    print(f"Browser taking too long to load. Exiting...")
    
except NoSuchElementException:
    print("Data locating button not found in the page. Exiting...")
    
except Exception as e:
    print(f"An error occured during crawling process: {e}")
    
finally:
    print("    Closing browser...")
    print("--- CRAWLING COMPLETE ---")
    driver.quit()

