import asyncio
import logging
import os,re,shutil,sys
from concurrent.futures import ThreadPoolExecutor


import httpx
import asyncclick as click
from nmap import nmap



client = httpx.AsyncClient() # Клиент асинхронных запросов 

# Настройка логов
logger = logging.getLogger('scanner_logger')
logger.setLevel(logging.INFO)
form = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_hangler = logging.StreamHandler()
log_hangler.setFormatter(form)
logger.addHandler(log_hangler)

executor = ThreadPoolExecutor(max_workers=10) # очередь асинхронных задач

path_list = []


async def collect_subdomains(domain: str):
    """
    Функция собирает собирает поддомены через запросы к https://crt.sh
    """
    local_subdomains = set()
    try:
        response = await client.get(
            "https://crt.sh",
            params={
                "q":domain,
                "output":"json"
            },
            timeout=10
        )
    except Exception as ex:
        logger.error(f"Не удалось получить данные с https://crt.sh: {ex}")
        sys.exit(1)
    
    data = response.json() # получаем ответ в виде json
    
    if not data:
        logger.error(f"Поддомен для {domain} не найдены")
        return []
    
    for el in data:
        names = el["name_value"].split('\n') # получаем список поддоменов разделенные \n
        _ = [local_subdomains.add(re.sub(r"^\*\.|www\.", "", name))for name in names] # вычищаем www и *. из поддоменов
    logger.info(f"Поддомены: {list(local_subdomains)}")
    return list(local_subdomains)


async def async_port_scan(domain: str):
    """
    Запускает асинхронно синхронную функцию scan_ports()
    
    """
    loop = nmap.PortScanner()
    await loop.run_in_exexutor(executor, scan_ports, domain)

def scan_ports(domain: str):
    """
    Сканирует домен и поддомены с выводом полученных ответов в коноль    
    """
    nm = nmap.PortScanner()
    _ = nm.scan(domain, arguments='-sV --script vulners', sudo=True)
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            port_list = nm[host][proto].keys()
            for port in port_list:
                port_info = nm[host][proto][port]


                logger.info(
                    f"""
                        ==========
                        URL: {domain}
                        Хост: {host}
                        Порт: {port}
                        Статус: {port_info.get('state')}
                        Имя: {port_info.get('name')}
                        Продукт: {port_info.get('product')}
                        Версия: {port_info.get('version')}
                        Возможные уязвимости: {port_info.get("script",{}).get("vulners")}
                    """.strip()
                )


def check_folder(path:str):
    """
    Проверка и очистка папки бд
    """
    try:
        if not os.listdir(path):
            shutil.rmtree(path)
            return True
    except Exception as ex:
        logger.error(f"Не удалось удалить папку '{path}': {ex}")


async def start_sqlmap(target_url, str):
    """
    Запускает sqlmap, он должен быть уже установлен на локальном хосте
    Сканирует на sql-injecion, xss список доменов

    --crawl=1 - дополнитьельно сканирует ссылки на сайте
    --batch   - отключает интерактивный режим
    --random-agent - использует разные агенты для подключения
    --output-dir - сохраняет результаты в директории
    """
    path = os.path.join(os.getcwd(), "sqlmap_result", target_url) # Прописываем путь для сохранения результатов
    os.makedirs(path, exist_ok=True) # Создаем директорию если ее не существует

    cmd = [
        'sqlmap', '-u',f"{target_url if 'https://' in target_url else f'https://{target_url}'}",
        '--crawl=1', '--batch', '--random-agent', 'output_dir', path
    ]
    # Добавляем задачу в асинхронный пулл задач
    await asyncio.create_subprocess_exec(path_list.append(path),*cmd,stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)



