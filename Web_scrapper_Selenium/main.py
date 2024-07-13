from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import yt_dlp

# Specify the path to the ChromeDriver executable
chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"

# Specify the path to your Chrome user data directory and profile
user_data_dir = "C:\\Users\\Narendra\\AppData\\Local\\Google\\Chrome\\User Data"
profile_directory = "Profile 2"  # Change this to the name of your profile directory

# Create a Service object for Chrome
chrome_service = ChromeService(chrome_driver_path)

# Initialize Chrome options and set the user data directory
chrome_options = ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument(f"--profile-directory={profile_directory}")

# Initialize the Chrome driver with the Service object and options
chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # Open Twitter (X.com)
    chrome_driver.get("https://x.com/")

    # Wait for the page to load
    WebDriverWait(chrome_driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search query"]')))

    # Locate the search input field
    search_box = chrome_driver.find_element(By.XPATH, '//input[@aria-label="Search query"]')

    # Clear any pre-existing text, input the hashtag, and perform the search
    search_box.clear()
    search_box.send_keys("#deepfakedornot")
    search_box.send_keys(Keys.RETURN)

    # Wait for the search results to load
    time.sleep(10)  # Adjust sleep if necessary

    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))

    video_id = chrome_driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]')

    print(video_id.text)
    video_id.click()

    time.sleep(10)

    # Retrieve the current URL
    current_url = chrome_driver.current_url
    print("Current URL:", current_url)

    # Use yt_dlp to download the video
    ydl_opts = {
        'outtmpl': 'test_videos/video.mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([current_url])

    video_file_path = os.path.join(os.getcwd(), "test_videos", "video.mp4")
    print(f"Video downloaded to: {video_file_path}")

    # Open localhost to upload the video
    chrome_driver.get("http://127.0.0.1:8000/")

    # Wait for the page to load
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, 'id_upload_video_file')))

    # Locate the file input field and upload the video file
    file_input = chrome_driver.find_element(By.ID, 'id_upload_video_file')
    file_input.send_keys(video_file_path)

    # Click the upload button
    upload_button = chrome_driver.find_element(By.ID, 'videoUpload')
    upload_button.click()

    # Wait for the upload process to complete
    time.sleep(10)  # Adjust sleep if necessary

    print("Video uploaded successfully.")

except Exception as e:
    print(e)

finally:
    try:
        input("Press Enter to exit and close the browser...")
    except Exception as e:
        print(e)
    finally:
        chrome_driver.quit()
        print("Browser closed.")
