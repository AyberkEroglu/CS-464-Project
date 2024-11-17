import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import requests

def get_all_images():
    chrome_options = Options()

    # Disable pop-ups, notifications, and background tasks that are commonly used by ads
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-background-tasks")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://www.sporcle.com/games/NarwhalNukeYT/badly-drawn-flags-earth")
        print("Page loaded successfully.")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "imgbox")))

        main_image = driver.find_element(By.ID, "currimage")
        temp_image = driver.find_element(By.ID, "tempimage")

        print(f"Main image source: {main_image.get_attribute('src')}")
        print(f"Temporary image source: {temp_image.get_attribute('src')}")

        play_button = driver.find_element(By.XPATH, '//*[@id="button-play"]')
        driver.execute_script("arguments[0].click();", play_button)
        time.sleep(30)

        for i in range(197):
            try:

                # Wait for the outer element to be clickable
                outer_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, f"outer{i}"))
                )
                actions = ActionChains(driver)
                actions.move_to_element_with_offset(outer_element, 10, 10).click().perform()

                # Wait until the label is visible and has content
                label = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="resultText"]'))
                ).text.lower()
                print(label)
                folder_path = os.path.join("quiz_flags", label)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    print(f"Directory created: {folder_path}")
                # Wait for the main image to update
                main_image2 = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "currimage"))
                ).get_attribute('src')

                if main_image2:
                    image_response = requests.get(main_image2)
                    if image_response.status_code == 200:
                        image_path = os.path.join(folder_path, f"{label}_1.png")
                        with open(image_path, 'wb') as image_file:
                            image_file.write(image_response.content)
                        print(f"Image saved at: {image_path}")
                    else:
                        print(f"Failed to download image: Status code {image_response.status_code}")
                print(f"{i} Main image source: {main_image2}")

            except Exception as e:
                print(f"An error occurred in iteration {i}: {e}")
                continue

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


get_all_images()
