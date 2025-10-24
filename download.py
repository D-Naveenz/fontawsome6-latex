# import asyncio
from playwright.async_api import async_playwright
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


async def get_download_url_async(url):
    async with async_playwright() as p:
        # Launch a browser (headless by default)
        browser = await p.chromium.launch() # Set headless=False to see the browser in action
        page = await browser.new_page()

        # Navigate to the target URL
        await page.goto(url)

        # Wait for the "Free for desktop" button to load
        button_selector = 'a.button:has-text("Free for desktop")'
        await page.wait_for_selector(button_selector)

        # Extract the href attribute of the button
        download_link = await page.get_attribute(button_selector, 'href')

        # Close the browser
        await browser.close()

        return download_link if download_link else None

def download_chunk(url, start, end, save_path, progress_bar):
    """Downloads a specific chunk of the file."""
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)

    with open(save_path, "r+b") as f:
        f.seek(start)
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            progress_bar.update(len(chunk))

def download_file(url, save_path, num_threads=4):
    """Downloads a file in parallel using multiple threads."""
    response = requests.head(url)
    file_size = int(response.headers.get("content-length", 0))

    # Create an empty file with the required size
    with open(save_path, "wb") as f:
        f.write(b"\0" * file_size)

    # Calculate chunk sizes
    chunk_size = file_size // num_threads
    chunks = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads)]
    chunks[-1] = (chunks[-1][0], file_size - 1)  # Adjust the last chunk

    # Download chunks in parallel
    with tqdm(total=file_size, unit="B", unit_scale=True, desc=save_path) as progress_bar:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(download_chunk, url, start, end, save_path, progress_bar)
                for start, end in chunks
            ]
            for future in futures:
                future.result()  # Ensure all threads finish
            
            executor.shutdown(wait=True)  # 🔥 Explicitly shut down executor
            progress_bar.refresh()  # 🔥 Ensure tqdm cleans up properly

    print(f"Download complete: {save_path}")
