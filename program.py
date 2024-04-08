import os
import subprocess
import wmi
import json

# Функция для сканирования директории с драйверами на флешке
def scan_drivers(directory):
    # Возвращает список всех .exe файлов в указанной директории и её поддиректориях
    return [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if file.endswith('.exe')]

# Функция для определения модели компьютера
def get_computer_model():
    try:
        # Использует WMI для получения модели компьютера
        return wmi.WMI().Win32_ComputerSystem()[0].Model
    except Exception as e:
        print(f"Failed to retrieve computer model: {e}")
        return None

# Функция для получения списка установленных драйверов
def get_installed_drivers():
    try:
        # Использует WMI для получения списка установленных драйверов
        return [driver.Description for driver in wmi.WMI().Win32_PnPSignedDriver()]
    except Exception as e:
        print(f"Failed to retrieve installed drivers: {e}")
        return []

# Функция для установки драйвера
def install_driver(driver_file):
    print(f"Installing {driver_file}...")
    # Выполняет установку драйвера
    subprocess.call(driver_file)

# Функция для загрузки базы данных драйверов из JSON файла
def load_driver_database(file_path):
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Failed to load driver database: {e}")
        return {}

# Основная функция
def main():
    # Путь к директории с драйверами на флешке
    drivers_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Drivers")
    # Получаем модель компьютера
    computer_model = get_computer_model()
    print(f"Computer model: {computer_model}")
    if computer_model:
        # Получаем список драйверов для данной модели из базы данных
        database = load_driver_database("driver_database.json")
        required_drivers = database.get(computer_model, [])
        # Получаем список драйверов для данной модели на флешке
        driver_files = scan_drivers(os.path.join(drivers_directory, computer_model))
        # Получаем список установленных драйверов
        installed_drivers = get_installed_drivers()
        # Устанавливаем недостающие драйверы
        for driver_file in driver_files:
            if os.path.basename(driver_file) in required_drivers and os.path.basename(driver_file) not in installed_drivers:
                install_driver(driver_file)

if __name__ == "__main__":
    main()
