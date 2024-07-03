import asyncio
import aiohttp
import csv
import re
import os
from tqdm.asyncio import tqdm

from exceptions import InvalidProxy

format='login:password@ip:port' # указать порядок элементов айпи в вашем софте через двоеточие названия элементов : ip:port:login:password
async def check_format(proxy: str):
    if format!= 'login:password@ip:port':
        format_parts = format.split(':')
        proxy_parts = re.split('[:@]', proxy)
        proxy_dict = {key: value for key, value in zip(format_parts, proxy_parts)}
        proxy = f"{proxy_dict['login']}:{proxy_dict['password']}@{proxy_dict['ip']}:{proxy_dict['port']}"
    if 'http' not in proxy:
        proxy = f'http://{proxy}'
    return proxy


async def check_ip(proxy: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://eth0.me/', proxy=proxy) as r:
                your_ip = (await r.text()).strip()
                if your_ip not in proxy:
                    raise InvalidProxy(f"Proxy {proxy} doesn't work! Your IP is {your_ip}.")
                else:
                    return f'Proxy {proxy} is good'
        except Exception as e:
            raise InvalidProxy(f"Proxy {proxy} doesn't work! Error: {e}")

def get_unique_filename(directory: str, base_filename: str) -> str:
    if not os.path.exists(directory):
        os.makedirs(directory)
    base_path = os.path.join(directory, base_filename)
    filename, extension = os.path.splitext(base_path)
    counter = 1
    new_filename = f"{filename}{extension}"
    while os.path.exists(new_filename):
        new_filename = f"{filename}_{counter}{extension}"
        counter += 1
    return new_filename

async def main():
    proxies = []
    # Read proxies from file
    try:
        with open('proxies.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Proxies file not found!")
        return

    results = []
    tasks = []
    for i, proxy in enumerate(proxies, start=1):
        formatted_proxy = await check_format(proxy)
        tasks.append((i, proxy, check_ip(formatted_proxy)))

    # Execute tasks concurrently with a progress bar
    for i, (idx, proxy, task) in tqdm(enumerate(tasks, start=1), total=len(tasks)):
        try:
            await task
            results.append([idx, proxy, 'Works'])
        except Exception as e:
            results.append([idx, proxy, 'Does not work'])

    results_dir = 'results'
    output_file = get_unique_filename(results_dir, 'proxy_results.csv')

    # Write results to CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['No', 'Proxy', 'Status']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(results)

if __name__ == '__main__':
    asyncio.run(main())
