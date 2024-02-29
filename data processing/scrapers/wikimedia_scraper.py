import shutil
from lxml import html
import aiohttp
import asyncio
import aiofiles
import os
import re
import hashlib

from urllib.parse import unquote

def decode_url(url):
    return unquote(url)
category_name = input("Enter the Wikimedia Commons category name: ")
url = f'https://commons.wikimedia.org/wiki/Category:{category_name}'
storeDirectory = f"C:\\Users\\David\\Projects\\smart-drone-vision\\downloaded_{category_name}"  # Make sure this directory exists or is correctly set for your environment
checkForCategories = True

async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                dom = html.fromstring(text)
                return url, dom  # Ensure two values are returned
    except Exception as e:
        print(f"Failed to fetch {url} with error: {e}")
    return url, None  # Ensure two values are returned when catching exceptions

async def fetch_images(session, url):
    url, dom = await fetch_page(session, url)  # Unpack the returned tuple
    if dom is None:
        return

    images = dom.xpath('*//div[@class="thumb"]//a')
    subcategories = dom.xpath('*//div[@class="CategoryTreeItem"]//a')

    tasks = []
    if subcategories and checkForCategories:
        for category in subcategories:
            if 'href' in category.attrib:
                cat_url = 'https://commons.wikimedia.org' + category.attrib['href']
                tasks.append(fetch_images(session, cat_url))

    for image in images:
        if 'href' in image.attrib:
            image_url = 'https://commons.wikimedia.org' + image.attrib['href']
            tasks.append(download_image(session, image_url, url.split('Category:')[1]))

    await asyncio.gather(*tasks)

def sanitize_filename(filename):
    # Decode URL-encoded characters
    filename = decode_url(filename)
    
    # Remove pixel dimensions e.g., 800px-
    filename = re.sub(r'\d+px-', '', filename)
    
    # Remove timestamps and other noise e.g., _20190101095526
    filename = re.sub(r'_\d+', '', filename)
    
    # Replace invalid characters with an underscore
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Normalize extension
    # Here, simply ensure the extension is .jpg for demonstration; adjust as needed
    filename = re.sub(r'\.jpg[\w]*', '.jpg', filename, flags=re.IGNORECASE)
    filename = re.sub(r'\.png[\w]*', '.png', filename, flags=re.IGNORECASE)
    
    # Ensure the filename ends with a proper extension; default to .jpg if unsure
    if not (filename.lower().endswith('.jpg') or filename.lower().endswith('.png')):
        filename += '.jpg'
    
    # Optionally truncate or hash long filenames
    if len(filename) > 150:
        filename_hash = hashlib.sha256(filename.encode()).hexdigest()[:10]
        extension = '.jpg'  # Default to jpg if extension is ambiguous; adjust logic as needed
        filename = f"{filename_hash}{extension}"
    
    return filename



async def download_image(session, url, cat):
    _, dom = await fetch_page(session, url)
    if not dom:
        return

    imgURL = decode_url(dom.xpath('*//div[@class="fullImageLink"]//img')[0].attrib['src'])
    filename = imgURL.split('/')[-1]
    filename = sanitize_filename(filename)  # Sanitize the filename after decoding

    # Debug: Print the path before attempting to save
    print(f"Saving to: {os.path.join(storeDirectory, cat, filename)}")

    cat_path = os.path.join(storeDirectory, cat)
    os.makedirs(cat_path, exist_ok=True)

    async with session.get(imgURL) as resp:
        if resp.status == 200:
            async with aiofiles.open(os.path.join(cat_path, filename), mode='wb') as f:
                await f.write(await resp.read())



async def main():
    async with aiohttp.ClientSession() as session:
        await fetch_images(session, url)
    shutil.make_archive(os.path.join(storeDirectory, 'download'), 'zip', storeDirectory)

if __name__ == '__main__':
    asyncio.run(main())
