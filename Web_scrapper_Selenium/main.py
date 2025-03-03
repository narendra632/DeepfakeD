from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import yt_dlp

# Specify paths
chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"
user_data_dir = "C:\\Users\\Narendra\\AppData\\Local\\Google\\Chrome\\User Data"

# Set up Chrome driver
chrome_service = ChromeService(chrome_driver_path)
chrome_options = ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--start-maximized")

# Initialize driver
chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # Open Twitter and search for the hashtag
    chrome_driver.get("https://x.com/")
    WebDriverWait(chrome_driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search query"]')))

    search_box = chrome_driver.find_element(By.XPATH, '//input[@aria-label="Search query"]')
    search_box.clear()
    search_box.send_keys("#deepfakedornot")
    search_box.send_keys(Keys.RETURN)

    time.sleep(10)  # Wait for search results

    # Locate the tweet containing a video (assuming the first tweet)
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetText"]')))
    tweet_element = chrome_driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]')
    print(tweet_element.text)
    tweet_element.click()

    time.sleep(5)

    # Get the tweet URL
    current_url = chrome_driver.current_url
    print("Current Tweet URL:", current_url)


    # Define the video file path
    video_file_path = os.path.join(os.getcwd(), "test_videos", "video.mp4")
    
    # Delete the old video file if it exists
    if os.path.exists(video_file_path):
        os.remove(video_file_path)
        print("Old video file deleted.")

    # Download the video using yt_dlp
    ydl_opts = {'outtmpl': video_file_path}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([current_url])

    print(f"Video downloaded to: {video_file_path}")

    # Upload video to Django app
    chrome_driver.get("http://127.0.0.1:8000/")
    WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, 'id_upload_video_file')))

    file_input = chrome_driver.find_element(By.ID, 'id_upload_video_file')
    file_input.send_keys(video_file_path)

    upload_button = chrome_driver.find_element(By.ID, 'videoUpload')
    upload_button.click()

    print("Video uploaded. Waiting for results...")

    # Poll for processing completion
    result = None
    predict_url = "http://127.0.0.1:8000/predict/"
    while result is None:
        chrome_driver.get(predict_url)
        time.sleep(5)  # Poll every 5 seconds

        try:
            result_element = WebDriverWait(chrome_driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//h4[contains(text(), "Result:")]'))
            )
            result_text = result_element.text
            if "REAL" in result_text:
                result = "REAL"
            elif "FAKE" in result_text:
                result = "FAKE"
        except Exception:
            print("Result not available yet. Retrying...")

    print(f"Final result: {result}")

    # Reply to the original tweet
    chrome_driver.get(current_url)

    time.sleep(5)

    try:
        # Scroll to the reply box to make sure it's visible
        reply_box = chrome_driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
        chrome_driver.execute_script("arguments[0].scrollIntoView();", reply_box)
        time.sleep(2)  # Wait for the element to be visible

        # Click to activate using JavaScript to bypass interception issues
        chrome_driver.execute_script("arguments[0].click();", reply_box)
        time.sleep(2)

        # Enter the reply message
        result_text = f"The video you uploaded has been classified as {result}"

        # Use ActionChains to avoid interference
        actions = ActionChains(chrome_driver)
        actions.move_to_element(reply_box).click().send_keys(result_text).perform()

        # Wait for the reply button to become clickable
        reply_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="tweetButtonInline"]'))
        )

        # Optional: Remove disabled attribute if it is still set
        if reply_button.get_attribute("disabled"):
            chrome_driver.execute_script("arguments[0].removeAttribute('disabled');", reply_button)
            time.sleep(1)  # slight delay after attribute removal

        # Click the reply button using JavaScript to bypass any overlay issues
        chrome_driver.execute_script("arguments[0].click();", reply_button)

        print("Reply posted successfully!")

    except Exception as e:
        print("Error while posting reply:", e)

except Exception as e:
    print("Error:", e)

finally:
    input("Press Enter to exit and close the browser...")
    chrome_driver.quit()
    print("Browser closed.")
