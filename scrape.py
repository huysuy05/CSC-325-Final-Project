import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager



# Variable names for each data values
TARGET_URL = "http://data.cityofchicago.org/stories/s/Crimes-2001-to-present-Dashboard/5cd6-ry5g"
GRID_ROOT_SELECTOR = (By.CSS_SELECTOR, "div.ag-root-wrapper.ag-layout-normal")
SCROLL_CONTAINER_SELECTOR = "div.ag-body-viewport"
ROW_SELECTOR = "div.ag-center-cols-container div[role='row'].ag-row"
CELL_SELECTOR = "div[role='gridcell'].ag-cell"
HEADER_CONTAINER_SELECTOR = "div.ag-header-container"
HEADER_CELL_SELECTOR = "div.ag-header-cell"
HEADER_TEXT_SELECTOR = "span.ag-header-cell-text"
NEXT_BUTTON = "//div[@class='ag-button ag-paging-button' and contains(@aria-label, 'Next Page')]"
GRID_DATA_SELECTOR = (By.CSS_SELECTOR, ROW_SELECTOR)

# We are only selecting a few data from here to reduce the size of the dataset
NUM_TIMES_TO_EXECUTE = 100
OUPUT_DIR = "datasets/crawled_crime_rate_chicago.csv"
COL_NAMES = ["id", 
             "CaseNumber", 
             "Date", 
             "Block", 
             "ICUR", 
             "PrimaryType", 
             "Description", 
             "LocationDescription",
             "Arrest",
             "Domestic",
             "Beat",
             "District",
             "Ward",
             "CommunityArea",
             "FBICode",
             "XCoordinate",
             "YCoordinate",
             "Year",
             "UpdatedOn",
             "Latitude",
             "Longitude",
             "Location"]

print("--- STARTING CRAWLING PROCESS ---")


# --- WEBDRIVER SETUP ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
print(f"Navigating to {TARGET_URL}...")
driver.get(TARGET_URL)

# --- SCRAPING LOOP ---
all_data = [] #Array to be saved later
try:
    print(f"--- CRAWLING, LOCKING INNNN ---")
    for _ in range(NUM_TIMES_TO_EXECUTE):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(GRID_ROOT_SELECTOR)
            )
            # Locate to the page source after scrolling and waiting
            page_src = driver.page_source
            soup = BeautifulSoup(page_src, "html.parser")
            
            # Find values by selecting all the grid cells inside the row
            rows_data = driver.execute_script("""
                return Array.from(document.querySelectorAll('div[role="row"]')).map(row => {
                    return Array.from(row.querySelectorAll('div[role="gridcell"]')).map(cell => cell.innerText);
                });
            """)

            # Process the rows_data
            for row_data in rows_data:
                # Ensure row_data matches the length of COL_NAMES
                while len(row_data) < len(COL_NAMES):
                    row_data.append("")  # Add empty strings for missing columns
                print(f"Row Data: {row_data}")
                all_data.append(row_data)

            try:
                # Locate the next button
                next_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, NEXT_BUTTON))
                )
                if not next_btn:
                    print("Could not locate the next button. Quitting the program...")
                    break

                # Simulate clicking the next button
                next_btn.click()
                # Wait for the JS to load all necessary file
                time.sleep(3)
            except TimeoutException:
                print(f"Browser taking too long to load. Exiting...")
            except NoSuchElementException:
                print("Next button not found in the page. Exiting...")
            except Exception as e:
                print(f"An error occured during crawling process: {e}")



        except TimeoutException:
            print(f"Browser taking too long to load. Exiting...")
            break
        except NoSuchElementException:
            print("Next button not found in the page. Exiting...")
            break
        except Exception as e:
            print(f"An error occured during crawling process: {e}")
            break
        
    
    # --- EXPORT TO A CSV FILE ---
    if not all_data:
        print("No data was saved during the crawling process.")
    else:
        try:
            # Create a pandas df
            df = pd.DataFrame(all_data, columns=COL_NAMES)
            df.to_csv(OUPUT_DIR, index=False)
            print(f"Data saved successfully to {OUPUT_DIR}")
        except Exception as e:
            print(f"An error occured while writing the file: {e}")

except Exception as e:
    print(f"--- Error while crawling: {e}")

finally:
    print("Closing browser...")
    print("--- CRAWLING COMPLETE ---")
    driver.quit()

