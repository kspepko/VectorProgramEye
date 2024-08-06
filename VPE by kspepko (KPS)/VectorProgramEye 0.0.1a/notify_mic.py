import ctypes
import time

def show_message(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

show_message("AntiSpy Уведомление", "Микрофон был включен!")
