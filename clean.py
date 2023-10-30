import re
import shutil
import sys
from pathlib import Path


def handle_media(file_name: Path, target_folder: Path):
    # Обробка медіа-файлів: створюємо папку та перейменовуємо файл
    target_folder.mkdir(exist_ok=True, parents=True)
    new_name = target_folder / normalize(file_name.name)
    file_name.replace(new_name)

def handle_archive(file_name: Path, target_folder: Path):
    # Обробка архівів: розпаковуємо та організовуємо файли
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.stem)
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

# Функція для обробки папки та файлів в ній
def process_folder(folder: Path) -> object:
    for item in folder.iterdir():
        if item.is_dir() and item.name not in ('archives', 'video', 'audio', 'documents', 'images'):
            process_folder(item)
        elif item.is_file():
            extension = item.suffix[1:].upper()
            new_name = normalize(item.stem)
            target_folder = determine_target_folder(extension, folder)
            move_and_rename_file(item, target_folder, new_name)

# Визначення папки, в яку треба перенести файл
def determine_target_folder(extension, folder):
    if extension in ('JPEG', 'JPG', 'PNG', 'SVG'):
        return folder / 'images'
    elif extension in ('AVI', 'MP4', 'MOV', 'MKV'):
        return folder / 'video'
    elif extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'):
        return folder / 'documents'
    elif extension in ('MP3', 'OGG', 'WAV', 'AMR'):
        return folder / 'audio'
    elif extension in ('ZIP', 'GZ', 'TAR'):
        return folder / 'archives'
    else:
        return folder / 'unknown'

# Перейменовання та переміщення файлу
def move_and_rename_file(source, target_folder, new_name):
    target_folder.mkdir(parents=True, exist_ok=True)
    new_name_with_extension = new_name + source.suffix
    source.rename(target_folder / new_name_with_extension)

# Словник для транслітерації кирилічних символів в латиницю
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
             "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

# Створюємо словник для транслітерації
TRANS = dict()

# Наповнюємо словник транслітерації
for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()

def normalize(name: str) -> str:
    # Транслітеруємо і нормалізуємо назву файла
    translate_name = re.sub(r'\W', '_', name.translate(TRANS))
    return translate_name


def start(folder_to_process):
    process_folder(folder_to_process)


def main():
    # Запитуємо у користувача шлях до директорії для сортування
    folder_path = input("Введіть шлях до директорії для сортування: ")
    folder_path = Path(folder_path)

    # Перевіряємо, чи існує директорія
    if folder_path.exists() and folder_path.is_dir():
        # Запускаємо функцію сортування та передаємо шлях до директорії
        start(folder_path)
        print("Сортування завершено.")
    else:
        print("Директорія не існує. Перевірте введений шлях.")


if __name__ == "__main__":
    main()
