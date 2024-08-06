import psutil
import time
from colorama import Fore, Style, init

init()

bravser = ["brave.exe", "chrome.exe", "duckduckgo.exe", "msedge.exe", "firefox.exe", "tor.exe", "yandex.exe"]
virus = ["virus", "trojan", ""]
whyvirus = ["svchost.exe", "explorer.exe", "msconfig.exe", "taskhost.exe", "services.exe"]
running_processes = []

while True:
    for process in psutil.process_iter(['pid', 'name']):
        pid = process.info['pid']
        name = process.info['name']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        if name in bravser:
            color = Fore.YELLOW  # оранжевый цвет
            message = 'Это браузерный процесс'
        elif name in virus:
            color = Fore.RED  # красный цвет
            message = 'Внимание, данный процесс является красным или опасным, уточните информацию!'
        elif name in whyvirus:
            color = Fore.CYAN
            message = 'Процесс который при повторе может указывать на вирус!'
        else:
            color = Fore.GREEN  # зелёный цвет
            message = ''

        if name not in running_processes:
            running_processes.append(name)
            print(f'{timestamp} - PID: {pid} - {color}{name} {message}{Style.RESET_ALL}')

    time.sleep(5)  # проверять каждые 5 секунд






