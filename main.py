import os
import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
from tqdm import tqdm


# --- Initial Setup ---
url = input("Enter the URL to download: ").strip()
save_folder = os.path.join(os.getcwd(), "downloaded_template")
os.makedirs(save_folder, exist_ok=True)


# --- File download function with folder structure preservation ---
def download_file(file_url):
    try:
        if not file_url:
            return file_url

        # Convert relative URL to absolute URL
        full_url = urljoin(url, file_url)

        # Skip local files and localhost URLs
        if full_url.startswith("file:///"):
            return file_url
        if "localhost" in full_url.lower():
            print(f"Skipping localhost URL: {full_url}")
            return file_url

        parsed_url = urlparse(full_url)
        file_path_in_site = parsed_url.path  # File path on the site

        # Remove leading slash to build local path
        if file_path_in_site.startswith("/"):
            file_path_in_site = file_path_in_site[1:]

        local_file_path = os.path.join(save_folder, file_path_in_site)

        # Create necessary directories
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Avoid re-downloading existing files
        if not os.path.exists(local_file_path):
            print(f"Downloading: {full_url}")
            response = requests.get(full_url, timeout=20)
            if response.status_code == 200:
                with open(local_file_path, "wb") as f:
                    f.write(response.content)
                print(f"Saved to: {local_file_path}")
            else:
                print(
                    f"Failed to download {full_url} - Status code: {response.status_code}"
                )
                return file_url  # Return original link if download fails

        # Return relative path for link replacement in HTML and CSS
        relative_path = os.path.relpath(local_file_path, save_folder).replace("\\", "/")
        return relative_path

    except Exception as e:
        print(f"Error downloading {file_url}: {e}")
        return file_url


# --- Selenium setup ---
options = Options()
# options.add_argument("--headless")  # Uncomment this line to run without opening the browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

# Wait for page body and at least one stylesheet link to load
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "link[rel='stylesheet']"))
    )
except Exception as e:
    print("Warning: Timeout waiting for page to load completely.", e)

sleep(15)  # Adjust this delay as needed for JavaScript-heavy pages

html = driver.page_source
driver.quit()

# --- Parse HTML with BeautifulSoup ---
html_path = os.path.join(save_folder, "index.html")
soup = BeautifulSoup(html, "html.parser")

# Download and update CSS links
css_links = [
    link for link in soup.find_all("link", rel="stylesheet") if link.get("href")
]
print(f"Downloading {len(css_links)} CSS files...")
for link in tqdm(css_links):
    href = link.get("href")
    new_path = download_file(href)
    link["href"] = new_path

# Download and update JavaScript sources
js_scripts = [script for script in soup.find_all("script", src=True)]
print(f"Downloading {len(js_scripts)} JavaScript files...")
for script in tqdm(js_scripts):
    src = script.get("src")
    new_path = download_file(src)
    script["src"] = new_path

# Download and update image sources
images = [img for img in soup.find_all("img", src=True)]
print(f"Downloading {len(images)} images...")
for img in tqdm(images):
    src = img.get("src")
    new_path = download_file(src)
    img["src"] = new_path

# Download and update video sources
videos = [video for video in soup.find_all("video")]
print("Downloading video files and their sources...")
for video in tqdm(videos):
    src = video.get("src")
    if src:
        new_path = download_file(src)
        video["src"] = new_path
    for source in video.find_all("source"):
        src = source.get("src")
        if src:
            new_path = download_file(src)
            source["src"] = new_path

# Process CSS files to download fonts and other assets, and update links
css_files = []
for link in css_links:
    href = link.get("href")
    if href:
        css_files.append(os.path.join(save_folder, href))

print(f"Processing {len(css_files)} CSS files for fonts and other assets...")
for css_path in tqdm(css_files):
    if not os.path.exists(css_path):
        continue
    with open(css_path, "r", encoding="utf-8", errors="ignore") as f:
        css_content = f.read()

    urls = re.findall(r"url\(([^)]+)\)", css_content)
    for u in urls:
        u_clean = u.strip().strip("'\"")
        if u_clean.startswith("data:"):
            continue

        ext = os.path.splitext(urlparse(u_clean).path)[1].lower()
        if ext in [".woff", ".woff2", ".ttf", ".otf", ".eot"]:
            new_path = download_file(u_clean)
        elif ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]:
            new_path = download_file(u_clean)
        elif ext in [".mp4", ".webm"]:
            new_path = download_file(u_clean)
        else:
            continue

        css_content = css_content.replace(u, f"'{new_path}'")

    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)

# Save the final modified HTML file
with open(html_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Full offline clone created successfully.")
