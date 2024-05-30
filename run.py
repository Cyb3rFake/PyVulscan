#!/usr/bin/python3
import asyncio
import sys
import logging
import os
import re
import shutil
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor

import asyncclick as click
import httpx
from nmap import nmap

client = httpx.AsyncClient()  # Клиент асинхронных запросов

# Настройка логов
logger = logging.getLogger('PyVulscan')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = logging.StreamHandler()  # Вывод логов в консоль
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

executor = ThreadPoolExecutor(max_workers=10)

path_list = []

async def collect_subdomains(domain: str):

    """
    Сбор поддоменов через запрос к crt.sh
    :param domain: домен для поиска поддоменов
    :return: возвращает список поддоменов
    """
    local_subdomains = set()
    try:
        response = await client.get(
            "https://crt.sh",
            params={
                "q": domain,
                "output": "json"
            },
            timeout=10)
    except httpx.ReadTimeout:
        logger.error(f"Request to crt.sh timed out")
        sys.exit(1)
    data = response.json()
    if not data:
        logger.error(f"No data found for {domain}: {response.status_code}")
        sys.exit(1)
    for item in data:
        subdomain_list = item['name_value'].split('\n')
        _ = [local_subdomains.add(re.sub(r"^\*\.|www\.", "", subdomain)) for subdomain in subdomain_list]
    logger.info(f"Subdomains: {local_subdomains}")
    return list(local_subdomains)


# async def collect_subdomains(domain: str):
#     """
#       Поиск поддоменов через nmap dns-brute
#     """
#     nm = nmap.PortScanner()
#     r = nm.scan(domain,arguments='-p 80 --script "dns-brute"',sudo=True)
#     d_ip_list =list(r.get('scan').keys())

#     res = set()
#     for record in d_ip_list:
#         _=[]
#         for i in r['scan'][record]['hostscript'][0]['output'].split('\n')[2:]:
#             if '*' not in i.strip():
#                 _.append(i.strip())
#             for j in _:
#                 res.add(j.split(' ')[0].replace('www.',''))
#     logger.info(res)
#     return(list(res))




async def async_scan_port(subdomain: str):
    """
    Запускает асинхронно синхронную функцию scan_ports()
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, scan_ports, subdomain)

def scan_ports(subdomain: str):
    """
    Сканирует поддомены с выводом полученных ответов в консоль    
    """
    nm = nmap.PortScanner()
    _ = nm.scan(subdomain, arguments="-sV --script vulners")
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                port_info = nm[host][proto][port]
                logger.info(
                    f"""
                    =======
                    Host: {host}
                    Port: {port}
                    State: {port_info['state']}
                    Connection: {port_info['name']}
                    Product: {port_info['product']}
                    Version: {port_info['version']}
                    Potential Vulnerabilities: {port_info.get("script", {}).get("vulners")}
                    =======
                    """.strip()
                )

def check_empty_folders(path: str):
    try:
        if not os.listdir(path):
            shutil.rmtree(path)
            return True
    except Exception as e:
        logger.error(f"Не удалось удалить {path}: {e}")


async def run_sqlmap(subdomain: str):
    """
    Запускает sqlmap, он должен быть уже установлен в системе
    --crawl=1 - дополнитьельно сканирует ссылки(вложенность 1) на сайте
    --batch   - отключает интерактивный режим
    --random-agent - использует разные агенты для подключения
    --output-dir - сохраняет результаты в директории
    """
    path = os.path.join(os.getcwd(), "sqlmap_results", subdomain)
    os.makedirs(path, exist_ok=True)
    command = [
        "sqlmap",
        "-u", f"{subdomain if 'https' in subdomain else f'https://{subdomain}'}",
        "--crawl=1",
        "--random-agent",
        "--batch",
        f"--output-dir", f"{path}"
    ]
    # Добавляем задачу в асинхронный пулл задач
    await asyncio.create_subprocess_exec( 
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE # удаляет именованные аргументы если вывод логов в консоль
    )
    check_empty_folders(path)

@click.command()
@click.option("--domain", "-d", help="Domain to scan", required=True)
async def main(domain):
    subdomains = await collect_subdomains(domain)
    scan_port_tasks = [asyncio.create_task(async_scan_port(subdomain)) for subdomain in subdomains]
    sqlmap_tasks = [asyncio.create_task(run_sqlmap(subdomain)) for subdomain in subdomains]
    tasks = sqlmap_tasks + scan_port_tasks
    for task in asyncio.as_completed(tasks):
        await task

def check_sqlmap_installed():
    """
    Проверка устновки sqlmap
    """
    if os.path.exists("/usr/bin/sqlmap")!=True:
        return False
    else:
        return True


def check_nmap_installed():
    """
    Проверка устновки nmap
    """
    if os.path.exists("/usr/bin/nmap")!=True:
        return False
    else:
        return True

if __name__ == '__main__':
    if check_sqlmap_installed()!=True:
        print("SQLMap не установлен в системе")
        exit()

    elif check_nmap_installed()!=True:
        print("nmap не установлен в системе")
        exit()
    else:
        os.system('clear')
        print(Fore.LIGHTMAGENTA_EX+"Scanning in process..."+Style.RESET_ALL)
        asyncio.run(main())

