import asyncio
import os
import re
import hashlib
from lxml import html
import aiohttp
import aiofiles
import shutil
from urllib.parse import unquote, quote

# Constants for easy configuration and maintenance
BASE_URL = "https://commons.wikimedia.org"
category_name = input("Enter the Wikimedia Commons category name: ")
CATEGORY_URL = f"{BASE_URL}/wiki/Category:{quote(category_name)}"
STORE_DIRECTORY = "C:\\Users\\David\\Projects\\smart-drone-vision\\downloaded_test"
CHECK_FOR_CATEGORIES = True


# Decode URL-encoded strings
def decode_url(url):
    return unquote(url)


# Fetch and parse a page
async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                return html.fromstring(text)
    except Exception as e:
        print(f"Failed to fetch {url} with error: {e}")
    return None


# Fetch images and subcategories from a given URL
async def fetch_images(session, url):
    dom = await fetch_page(session, url)
    if not dom:
        return

    # Extract image and subcategory links
    images = dom.xpath('//div[@class="thumb"]//a/@href')
    subcategories = (
        dom.xpath('//div[@class="CategoryTreeItem"]//a/@href')
        if CHECK_FOR_CATEGORIES
        else []
    )

    tasks = [download_image(session, BASE_URL + href) for href in images]
    tasks += [fetch_images(session, BASE_URL + href) for href in subcategories]

    await asyncio.gather(*tasks)


# Sanitize and format the filename
def sanitize_filename(filename):
    filename = decode_url(filename)
    filename = re.sub(r"\d+px-", "", filename)
    filename = re.sub(r"_\d+", "", filename)
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
    filename = re.sub(r"\.jpg[\w]*", ".jpg", filename, flags=re.IGNORECASE)
    filename = re.sub(r"\.png[\w]*", ".png", filename, flags=re.IGNORECASE)
    if not filename.lower().endswith((".jpg", ".png")):
        filename += ".jpg"
    if len(filename) > 150:
        filename = f"{hashlib.sha256(filename.encode()).hexdigest()[:10]}.jpg"
    return filename


# Download an image to the specified directory
async def download_image(session, image_url):
    category = image_url.split("/Category:")[1] if "/Category:" in image_url else "misc"
    dom = await fetch_page(session, image_url)
    if not dom:
        return

    img_url = decode_url(dom.xpath('//div[@class="fullImageLink"]//img/@src')[0])
    filename = sanitize_filename(img_url.split("/")[-1])

    save_path = os.path.join(STORE_DIRECTORY, category, filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    async with session.get(img_url) as resp:
        if resp.status == 200:
            async with aiofiles.open(save_path, mode="wb") as file:
                await file.write(await resp.read())


# Main coroutine to start the process
async def main():
    async with aiohttp.ClientSession() as session:
        await fetch_images(session, CATEGORY_URL)
    shutil.make_archive(
        os.path.join(STORE_DIRECTORY, "downloaded_images_archive"),
        "zip",
        STORE_DIRECTORY,
    )


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
