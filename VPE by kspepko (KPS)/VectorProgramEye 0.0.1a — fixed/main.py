import flet as ft
import psutil
import threading
import time
import subprocess
import requests
import random
import string
import whois
import sounddevice as sd
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import win32gui
import win32api
import wmi

def main(page: ft.Page):
    page.title = "VectorP-Eye | by KPS (kspepko)"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Добавление иконки выше кнопки "Главная страница"
    icon_image = ft.Image(src="icon.png", width=200, height=200, fit=ft.ImageFit.COVER)
    clipped_icon = ft.Container(content=icon_image, clip_behavior=ft.ClipBehavior.ANTI_ALIAS, border_radius=50)

    # Создание кнопок для навигации с иконками
    buttons = [
        clipped_icon,
        ft.ElevatedButton("Главная страница", on_click=lambda e: switch_page(e, "home"), color=ft.colors.RED, height=60, width=200, icon=ft.icons.HOME),
        ft.ElevatedButton("Инструменты", on_click=lambda e: switch_page(e, "tools"), icon=ft.icons.BUILD),
        ft.ElevatedButton("Браузер инструментарий", on_click=lambda e: switch_page(e, "browser_killer"), icon=ft.icons.DELETE),
        ft.ElevatedButton("Данные ПК", on_click=lambda e: switch_page(e, "pc_data"), icon=ft.icons.COMPUTER),
        ft.ElevatedButton("Протоколы и IP", on_click=lambda e: switch_page(e, "protocols_ip"), icon=ft.icons.NETWORK_WIFI),
        ft.ElevatedButton("WEB-Взаимодействия", on_click=lambda e: switch_page(e, "web_interactions"), icon=ft.icons.PUBLIC),
        ft.ElevatedButton("VPE Guard", on_click=lambda e: switch_page(e, "anti_spy"), icon=ft.icons.SECURITY),
        ft.ElevatedButton("Процесс-чекер", on_click=lambda e: open_processes_window(), icon=ft.icons.LIST, color=ft.colors.GREEN)
    ]

    # Создание контейнера для кнопок
    button_column = ft.Container(
        content=ft.Column(controls=buttons, alignment=ft.MainAxisAlignment.START, spacing=10),
        bgcolor=ft.colors.BLACK12,
        padding=10,
        border_radius=10,
        height=page.height,
    )

    # Создание контейнера для отображения данных
    data_column = ft.Column(controls=[], alignment=ft.MainAxisAlignment.START, expand=True, scroll=ft.ScrollMode.AUTO)

    current_page = None
    notifications = {
        "Anti_Spy_Global": False,
        "micro": False,
        "camera (admin)": False,
        "external_ip": False,
        "device_connect": False
    }

    def switch_page(event, page_name):
        nonlocal current_page
        current_page = page_name
        data_column.controls.clear()
        if page_name == "home":
            data_column.controls.append(ft.Text("VectorP-Eye: Программa kspepko, многофункциоальный-меню проект для решания разных задач\n -VectorP-Eye (VectorProgramEye) это проект многофункционального приложения для защиты компьютера и быстрого доступа к скрытым возможностям\n -также данный проект в будущем планирует поддержку улучшенной поисковой системы для обнаружения информации по базам данных что должно ускорить многие задачи, к примеру вы сможете быстро определить данные о сайты и его метки"))
            data_column.controls.append(ft.Text("ВНИМАНИЕ: Процессы - работаю в консоли см. консоль", size=20, weight=ft.FontWeight.BOLD))
        elif page_name == "tools":
            create_tools_controls()
        elif page_name == "browser_killer":
            data_column.controls.append(ft.ElevatedButton("Убить процессы браузера", on_click=kill_browsers, color=ft.colors.RED))
            data_column.controls.append(ft.Text("Все браузеры будут закрыты", size=25))
        elif page_name == "pc_data":
            display_pc_data()
        elif page_name == "protocols_ip":
            display_protocols_ip_data()
        elif page_name == "web_interactions":
            display_web_interactions()
        elif page_name == "anti_spy":
            display_anti_spy()
        page.update()

    def create_tools_controls():
        process_name_input = ft.TextField(label="Введите имя процесса", width=200)
        kill_process_button = ft.ElevatedButton("Остановить процесс", on_click=lambda e: kill_process_by_name(process_name_input.value), icon=ft.icons.CHECK, color=ft.colors.RED)
        
        key_length_input = ft.TextField(label="Количество символов", width=200)
        generate_key_button = ft.ElevatedButton("Генерировать", on_click=lambda e: generate_key(int(key_length_input.value)), icon=ft.icons.CHECK, color=ft.colors.GREEN)
        key_output = ft.Text("", selectable=True)
        
        data_column.controls.append(ft.Container(
            content=ft.Column([
                ft.Text("Инструменты", size=20, weight=ft.FontWeight.BOLD),
                process_name_input,
                kill_process_button,
                ft.Text("Удаление процесса", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                key_length_input,
                generate_key_button,
                key_output
            ]),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLACK12
        ))
        
        def generate_key(length):
            characters = string.ascii_letters + string.digits
            key = ''.join(random.choice(characters) for _ in range(length))
            key_output.value = f"Сгенерированный ключ: {key}"
            page.update()

    def open_processes_window():
        subprocess.Popen(["python", "processes_info.py"])

    def kill_browsers(event):
        browsers = ["brave.exe", "chrome.exe", "duckduckgo.exe", "msedge.exe", "firefox.exe", "tor.exe", "amigo.exe", "yandex.exe"]
        for process in psutil.process_iter(attrs=["name"]):
            if process.info["name"].lower() in browsers:
                try:
                    process.kill()
                except Exception as e:
                    print(f"Ошибка при завершении процесса {process.info['name']}: {e}")
        data_column.controls.append(ft.Text("Все браузеры закрыты"))
        page.update()

    def kill_process_by_name(process_name):
        for process in psutil.process_iter(attrs=["name"]):
            if process.info["name"].lower() == process_name.lower():
                try:
                    process.kill()
                    data_column.controls.append(ft.Text(f"Процесс {process_name} завершен", color=ft.colors.GREEN, selectable=True))
                except Exception as e:
                    data_column.controls.append(ft.Text(f"Ошибка при завершении процесса {process_name}: {e}", color=ft.colors.RED, selectable=True))
                page.update()
                return
        data_column.controls.append(ft.Text(f"Процесс {process_name} не найден", color=ft.colors.RED, selectable=True))
        page.update()

    def get_ip_info(ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def display_protocols_ip_data():
        ip_info = get_ip_info("")
        data_column.controls.append(ft.Text(f"IPv4: {ip_info.get('ip', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"IPv6: {ip_info.get('hostname', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Город: {ip_info.get('city', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Регион: {ip_info.get('region', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Страна: {ip_info.get('country', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Организация: {ip_info.get('org', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Локация: {ip_info.get('loc', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Почтовый индекс: {ip_info.get('postal', 'N/A')}", selectable=True))

        data_column.controls.append(ft.Text("Подключенные IP-адреса:", selectable=True))
        for conn in psutil.net_connections():
            try:
                ip_address = conn.laddr.ip
                data_column.controls.append(ft.Text(ip_address, selectable=True))
            except Exception as e:
                pass
    
        data_column.controls.append(ft.Text("Список онлайн устройств:", selectable=True))
        for device in psutil.net_if_addrs():
            data_column.controls.append(ft.Text(device, selectable=True))

        page.update()

    def search_ip_data(ip):
        ip_info = get_ip_info(ip)
        data_column.controls.append(ft.Text(f"DNS: {ip_info.get('hostname', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Город: {ip_info.get('city', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Регион: {ip_info.get('region', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Страна: {ip_info.get('country', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Организация: {ip_info.get('org', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Локация: {ip_info.get('loc', 'N/A')}", selectable=True))
        data_column.controls.append(ft.Text(f"Почтовый индекс: {ip_info.get('postal', 'N/A')}", selectable=True))
        page.update()

    def get_whois_info(domain):
        try:
            domain_info = whois.whois(domain)
            return domain_info
        except Exception as e:
            return {"error": str(e)}

    def search_whois_data(domain):
        whois_info = get_whois_info(domain)
        if "error" in whois_info:
            data_column.controls.append(ft.Text(f"Ошибка: {whois_info['error']}", color=ft.colors.RED, selectable=True))
        else:
            data_column.controls.append(ft.Text(f"Domain: {whois_info.get('domain_name', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"Registrar: {whois_info.get('registrar', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"WHOIS Server: {whois_info.get('whois_server', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"Creation Date: {whois_info.get('creation_date', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"Expiration Date: {whois_info.get('expiration_date', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"Updated Date: {whois_info.get('updated_date', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"Status: {whois_info.get('status', 'N/A')}", selectable=True))
            data_column.controls.append(ft.Text(f"Name Servers: {whois_info.get('name_servers', 'N/A')}", selectable=True))
        page.update()

    def display_web_interactions():
        ip_input = ft.TextField(label="Введите IP адрес", width=200)
        search_button = ft.ElevatedButton("Узнать данные", on_click=lambda e: search_ip_data(ip_input.value), icon=ft.icons.CHECK, color=ft.colors.GREEN)
        
        whois_input = ft.TextField(label="Введите домен (WHOIS)", width=200)
        whois_button = ft.ElevatedButton("Узнать информацию", on_click=lambda e: search_whois_data(whois_input.value), icon=ft.icons.CHECK, color=ft.colors.GREEN)
        
        data_column.controls.append(ft.Container(
            content=ft.Column([
                ip_input,
                search_button,
                ft.Divider(),
                ft.Text("Результаты поиска по IP:", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                whois_input,
                whois_button,
                ft.Divider(),
                ft.Text("Результаты поиска WHOIS:", size=20, weight=ft.FontWeight.BOLD)
            ]),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLACK12
        ))
        page.update()

    def display_anti_spy():
        def toggle_notification(name):
            notifications[name] = not notifications[name]
            update_notifications()

        def update_notifications():
            notification_controls.clear()
            for name, value in notifications.items():
                checkbox = ft.Checkbox(
                    label=name.replace("_", " ").capitalize(),
                    value=value,
                    on_change=lambda e, name=name: toggle_notification(name),
                )
                notification_controls.append(checkbox)
            page.update()

        notification_controls = []
        update_notifications()

        data_column.controls.append(ft.Container(
            content=ft.Column([
                ft.Divider(),
                ft.Text("AntiSpy уведомления листа, см. консоль", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Column(notification_controls, spacing=10)
            ]),
            padding=10,
            border_radius=10,
            bgcolor=ft.colors.BLACK12
        ))
        page.update()

    def update_pc_data():
        while current_page == "pc_data":
            data_column.controls.clear()
            data_column.controls.append(ft.Text("Информация о ПК:", size=20, weight=ft.FontWeight.BOLD))
            data_column.controls.append(ft.Text(f"Процессор: {psutil.cpu_percent()}%", size=16))
            data_column.controls.append(ft.Text(f"Оперативная память: {psutil.virtual_memory().percent}%", size=16))
            data_column.controls.append(ft.Text(f"Диск C: {psutil.disk_usage('/').percent}%", size=16))
            data_column.controls.append(ft.Text(f"Пользователи: {psutil.cpu_times()}", size=10))
            data_column.controls.append(ft.Text(f"win_service_iter: {psutil.win_service_iter()}", size=10))
            page.update()
            time.sleep(0.2)

    def display_pc_data():
        threading.Thread(target=update_pc_data, daemon=True).start()

    # Функции для мониторинга

    def monitor_events():
        while True:
            if notifications["Anti_Spy_Global"]:
                capture_processes = detect_screen_capture()
                if capture_processes:
                    print("Обнаружены процессы, возможно связанные с захватом экрана, камерой или опасное деят.:")
                    for proc in capture_processes:
                        print(f"{proc['name']} (PID: {proc['pid']})")
                    subprocess.Popen(["python", "NullNotifyfixed.py"])
                else:
                    print("Неприятные процессы не обнаружены.")
            if notifications["micro"] and check_mic_usage():
                subprocess.Popen(["python", "NullNotifyfixed.py"])
            if notifications["camera (admin)"] and check_camera_status():
                subprocess.Popen(["python", "NullNotifyfixed.py"])
            if notifications["external_ip"] and check_external_ip_usage():
                subprocess.Popen(["python", "NullNotifyfixed.py"])
            if notifications["device_connect"] and check_new_device_connected():
                subprocess.Popen(["python", "NullNotifyfixed.py"])
            time.sleep(5)


    def check_mic_usage():
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and volume.GetMute() == 0:
                print(f"Процесс: {session.Process.name()} использует|не глушит|получает доступ (к) микрофон.")
                return True
        return False



    def check_camera_status():
        c = wmi.WMI()
        camera_in_use = False

        # Получаем все активные процессы
        for process in c.Win32_Process():
            try:
                if "camera" in process.Name.lower() or "webcam" in process.Name.lower():
                    print(f"Процесс: {process.Name} использует камеру.")
                    camera_in_use = True
            except Exception as e:
                print(f"Ошибка при проверке процесса: {e}")

        return camera_in_use

    def detect_screen_capture():
        suspicious_keywords = ["capture", "record", "screen", "zoom", "trojan", "virus"]
        capture_processes = []

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()
                if any(keyword in process_name for keyword in suspicious_keywords):
                    print(f"Обнаружен подозрительный процесс: {proc.info['name']} (PID: {proc.info['pid']})")
                    capture_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return capture_processes


    def check_external_ip_usage():
        connections = psutil.net_connections()
        for conn in connections:
            if conn.status == psutil.CONN_ESTABLISHED:
                print(f"Активное подключение: {conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}")
                return True
        return False

    def check_new_device_connected():
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        for drive in drives:
            print(f"Обнаружено устройство: {drive}")
        return True

    # Запуск мониторинга событий
    threading.Thread(target=monitor_events, daemon=True).start()

    # Расположение элементов на странице
    page.add(
        ft.Row([
            button_column,
            ft.VerticalDivider(width=1),
            ft.Container(
                content=data_column,
                padding=10,
                expand=True,
                height=page.height,
            )
        ],
        expand=True)
    )

ft.app(target=main)
