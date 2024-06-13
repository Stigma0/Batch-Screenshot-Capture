# Batch Screenshot Capture

A Python script to capture full-page screenshots of multiple URLs using Selenium and Firefox. This script supports using a custom Firefox profile and can run in headless mode.

## Features

- Capture full-page screenshots of multiple URLs
- Supports custom Firefox profiles to retain extensions and cookies
- Runs in headless mode for automated environments
- Saves screenshots to a specified output directory

## Requirements

- Python 3.6+
- `selenium`
- `webdriver-manager`
- `Pillow`

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Stigma0/Batch-Screenshot-Capture.git
    cd Batch-Screenshot-Capture
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command Line Arguments

- `input_file`: Path to the text file containing URLs, one URL per line.
- `output_dir`: Directory to save the screenshots.
- `num_webpages`: Number of webpages to capture.
- `--profile`: (Optional) Path to the Firefox profile.
- `--headless`: (Optional) Run in headless mode.

### Example

1. **Create a text file (`urls.txt`) with the URLs you want to capture:**

    ```
    https://github.com/Stigma0/Batch-Screenshot-Capture/
    https://www.gnu.org
    ```

2. **Run the script with an explicit temporary directory to retain your firefox profile capturing:**

    ```bash
    TMPDIR=/path/to/tempdir python batch_screenshot.py urls.txt screenshots 10 --profile /path/to/firefox/profile --headless
    ```

### Explanation

- The script will read URLs from `urls.txt`.
- It will capture full-page screenshots of the first 10 URLs.
- Screenshots will be saved in the `screenshots` directory.
- The Firefox profile located at `/path/to/firefox/profile` will be used.
- The script will run in headless mode.
- Explicit temporary directory is set with `TMPDIR=/path/to/tempdir`.

## Tested Conditions

- Developed and tested on **Linux Fedora 39**.
- Works well for basic website setups.
- If cookies are accepted for a website beforehand in the firefox profile, the screenshot will work without accept cookies prompts.
- Does not take into account complex websites.
