import argparse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image
from io import BytesIO
import os
import time

def setup_selenium(profile_path=None, headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    if profile_path:
        options.profile = profile_path
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver

def capture_full_page_screenshot(driver, url, output_path):
    driver.get(url)
    time.sleep(5)  # Allow some time for the page to load

    # Calculate the number of scrolls needed to capture the entire page
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")
    viewport_width = driver.execute_script("return window.innerWidth")
    num_scrolls = (scroll_height + viewport_height - 1) // viewport_height

    # Capture screenshots and stitch them together
    stitched_image = Image.new('RGB', (viewport_width, scroll_height))
    for i in range(num_scrolls):
        driver.execute_script(f"window.scrollTo(0, {i * viewport_height});")
        time.sleep(1)  # Allow some time for the scrolling and rendering
        screenshot = Image.open(BytesIO(driver.get_screenshot_as_png()))

        # Calculate the part of the screenshot that fits within the remaining space
        if (i + 1) * viewport_height > scroll_height:
            crop_height = scroll_height % viewport_height
            screenshot = screenshot.crop((0, viewport_height - crop_height, viewport_width, viewport_height))

        stitched_image.paste(screenshot, (0, i * viewport_height))

    stitched_image.save(output_path)

def batch_screenshot(input_file, output_dir, n=10, profile_path=None, headless=True):
    # Read URLs from the input file
    with open(input_file, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    # Limit the number of screenshots to n
    urls = urls[:n]

    # Setup Selenium
    driver = setup_selenium(profile_path, headless)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Capture screenshots for each URL
    for i, url in enumerate(urls):
        output_path = os.path.join(output_dir, f"screenshot_{i + 1}.png")
        print(f"Capturing screenshot for: {url}")
        capture_full_page_screenshot(driver, url, output_path)

    # Quit the driver
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Screenshot Capture")
    parser.add_argument('input_file', type=str, help="Path to the text file containing URLs")
    parser.add_argument('output_dir', type=str, help="Directory to save the screenshots")
    parser.add_argument('num_webpages', type=int, help="Number of webpages to capture")
    parser.add_argument('--profile', type=str, help="Path to the Firefox profile", required=False)
    parser.add_argument('--headless', action='store_true', help="Run in headless mode")

    args = parser.parse_args()

    batch_screenshot(args.input_file, args.output_dir, args.num_webpages, args.profile, args.headless)
