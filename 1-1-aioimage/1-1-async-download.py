import io
import time
import asyncio
import aiohttp, aiofiles
from PIL import Image

unsplash_search_url = "https://source.unsplash.com/random/300x300"

async def download_image_async(session: aiohttp.ClientSession, num: int = 1):
    print(f"{time.ctime} - Start download image {num}")
    async with session.get(unsplash_search_url) as response:
        if response.status == 200:
            image_buffer = await response.read()
            img = Image.open(io.BytesIO(image_buffer))
            print(f"{time.ctime} - Image {num} shape: {img.size}")
    
    async with aiofiles.open(f'./filename{num}.jpg', "wb") as new_file:
        print(f"{time.ctime()} - Writing to 'filename{num}.jpg'...")
        await new_file.write(image_buffer)
    
async def download_images_async(n: int = 10):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, i+ 1) for i in range(n)]
        _ = await asyncio.gather(*tasks)
    return

if __name__ == "__main__":
    tick = time.perf_counter()
    asyncio.run(download_images_async())
    tock = time.perf_counter()
    print(f"{time.ctime()} - elapsed: {tock-tick:.2f} seconds")