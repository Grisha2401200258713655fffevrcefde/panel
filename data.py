import json

data = {
    "Модель_ПК_1": ["драйвер1.exe", "драйвер2.exe"],
    "Модель_ПК_2": ["драйвер3.exe", "драйвер4.exe"],
    "Модель_ПК_3": ["драйвер5.exe"]
}

with open('driver_database.json', 'w') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
