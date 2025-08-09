# Offline Webpage Downloader

A Python script to download a complete webpage along with all its dependent files (CSS, JavaScript, images, videos, fonts) and save it locally while preserving the folder structure. This tool creates a full offline copy of a webpage for viewing without internet access.

---

## Features

- Downloads the HTML page using Selenium (to fully load pages with JavaScript)
- Extracts and downloads CSS, JavaScript, images, videos, and fonts
- Updates all links in HTML and CSS to local paths for proper offline display
- Preserves folder structure similar to the original website
- Supports both relative and absolute URLs

---

## Requirements

- Python 3.7 or higher
- [Google Chrome](https://www.google.com/chrome/) installed on your system
- [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version

---

## Installation

1. Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/offline-webpage-downloader.git
cd offline-webpage-downloader
```

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

**Contents of requirements.txt**:

```
selenium
requests
beautifulsoup4
tqdm
```

3. Make sure the `chromedriver` executable is available in your project folder or in your system PATH.

---

## Usage

1. Run the script:

```bash
python main.py
```

2. Enter the URL of the webpage you want to download, for example: `https://example.com`

3. The script will create a folder named `downloaded_template` and save all files there.

4. To properly view and run the downloaded files (especially for JavaScript-heavy pages and relative links), navigate into the `downloaded_template` folder and start a simple local server by running:

```bash
cd downloaded_template
python -m http.server 8000
```

5. Open your browser and go to:

```
http://localhost:8000
```

This will serve the page locally and ensure all resources load correctly.

---

## Notes

- This script uses Selenium and Chrome, so make sure your Chrome and ChromeDriver versions are compatible.
- Some complex or highly dynamic pages might require adjusting the sleep delay or additional tweaks.
- URLs starting with `file:///` or containing `localhost` are skipped.
- This tool is best suited for static or semi-dynamic sites; highly dynamic or protected sites may need custom handling.

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## Contact

If you have any questions or suggestions, please open an issue on GitHub.

---

### Example Output

```
Enter the URL to download: https://example.com
Downloading 3 CSS files...
Downloading 4 JavaScript files...
Downloading 10 images...
Downloading video files and their sources...
Processing 3 CSS files for fonts and other assets...
Full offline clone created successfully.
```

---

Use this script to archive your favorite pages or test templates offline.  
If you need any help, feel free to ask!
