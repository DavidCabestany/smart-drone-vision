import aiohttp
import asyncio
import aiofiles
import os
from bs4 import BeautifulSoup


async def ensure_directory_exists(directory):
    """Asynchronously ensure the specified directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

async def get_country_category_urls(session, main_category_url):
    try:
        async with session.get(main_category_url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                country_categories = soup.find_all('a', href=True, title=True)
                country_urls = ['https://commons.wikimedia.org' + a['href'] for a in country_categories if 'Category:Trees_of' in a['href']]
                return country_urls
            else:
                print("Failed to retrieve main category page")
                return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

async def get_tree_image_pages(session, country_category_url):
    try:
        async with session.get(country_category_url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                image_pages = soup.find_all('a', href=True, title=True)
                image_page_urls = ['https://commons.wikimedia.org' + a['href'] for a in image_pages if 'File:' in a['href'] and not any(x in a['href'] for x in ['edit', 'history', 'WhatLinksHere'])]
                return image_page_urls
            else:
                print(f"Failed to retrieve {country_category_url}")
                return []
    except Exception as e:
        print(f"An error occurred while processing {country_category_url}: {e}")
        return []

async def extract_image_url(session, image_page_url):
    try:
        async with session.get(image_page_url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                image_url_element = soup.find('a', href=True, title='File:View full resolution')
                if image_url_element:
                    return image_url_element['href']
                else:
                    print(f"No full resolution image found for {image_page_url}")
                    return None
            else:
                print(f"Failed to retrieve {image_page_url}")
                return None
    except Exception as e:
        print(f"An error occurred while processing {image_page_url}: {e}")
        return None

async def download_image(session, image_url, filename):
    try:
        async with session.get(image_url) as response:
            if response.status == 200:
                async with aiofiles.open(filename, 'wb') as file:
                    await file.write(await response.read())
            else:
                print("Failed to download image")
    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    images_dir = 'downloaded_images'
    await ensure_directory_exists(images_dir)

    main_category_url = 'https://commons.wikimedia.org/wiki/Category:Trees_of_Europe_by_country'
    
    async with aiohttp.ClientSession() as session:
        country_category_urls = await get_country_category_urls(session, main_category_url)

        for country_url in country_category_urls:
            print(f"Processing {country_url}...")
            tree_image_pages = await get_tree_image_pages(session, country_url)
            for image_page_url in tree_image_pages:
                image_url = await extract_image_url(session, image_page_url)
                if image_url:
                    filename = os.path.join(images_dir, image_url.split('/')[-1])
                    await download_image(session, image_url, filename)

# Run the main function
asyncio.run(main())
