# Задание №9
# � Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# � Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# � Программа должна использовать многопоточный, многопроцессорный и
# асинхронный подходы.
# � Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# � Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.

import os
import threading
import multiprocessing
import aiohttp
import asyncio
from pathlib import Path
import requests
import time


BASE_DIR = Path(__file__).resolve().parent
dir_for_images = os.path.join(BASE_DIR, 'dir_for_images')

if not os.path.exists(dir_for_images):
    os.mkdir(dir_for_images)

start_time = time.time()


def download_content(url: str):
    response = requests.get(url)
    filename = 'threads_processes_'+url.split('/')[-1]
    with open(os.path.join(dir_for_images, filename), 'wb') as file:
        file.write(response.content)    
    print(f"Downloaded {filename} in {time.time()-start_time:.2f} seconds")


def threads_choice(urls):
    threads: list[threading.Thread] = []

    for url in urls:
        thread = threading.Thread(target=download_content, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f'\nCompleted download using threads in {time.time() - start_time} seconds.\n')


def processes_choice(urls):
    processes = []

    start_time = time.time()

    for url in urls:
        process = multiprocessing.Process(target=download_content, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f'\nCompleted download using processes in {time.time() - start_time} seconds.\n')


async def async_choice(urls):
    async def download_content(url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                filename = 'async_'+url.split('/')[-1]
                with open(
                    os.path.join(dir_for_images, filename), 'wb', encoding='utf-8') as f:
                    f.write(await response.content())

    async def start():
        tasks = []

        for url in urls:
            task = asyncio.ensure_future(download_content(url))
            tasks.append(task)

        await asyncio.gather(*tasks)

    start_time = time.time()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start())
    print(f'Completed download using async in {time.time() - start_time} seconds.')


if __name__ == '__main__':
    
    urls = [
    'https://gas-kvas.com/grafic/uploads/posts/2023-09/1695965269_gas-kvas-com-p-kartinki-slonenok-31.jpg',
    'https://uprostim.com/wp-content/uploads/2021/02/image004-49.jpg',
    'https://pibig.info/uploads/posts/2021-06/1624323250_1-pibig_info-p-ozero-ritsa-letom-priroda-krasivo-foto-1.jpg',
    'https://w.forfun.com/fetch/6d/6d69d0353a5787842bfcb472da46bd23.jpeg',
    'https://byatrip.com/wp-content/uploads/argentina-perito-moreno.jpg',
    ]

    choice = int(input('Do you want to enter an additional URL? 1 - yes, 2 - no:\n'))
    if choice == 1:
        additional_url = input('Enter an URL: ')
        urls.append(additional_url)
    threads_choice(urls)
    processes_choice(urls)
    async_choice(urls)
