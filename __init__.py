import os
import shutil
import string

# Функція для транслітерації кирилиці на латиницю
def normalize(text):
    translit_table = str.maketrans(
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
        "abvgdeezijklmnoprstufhzcs'eiua"
    )
    text = text.lower()
    text = text.translate(translit_table)
    text = ''.join([c if c in string.ascii_lowercase or c.isdigit() else '_' for c in text])
    return text

# Функція для сортування файлів за розширенням
def organize_files(folder_path):
    image_extensions = ('jpeg', 'png', 'jpg', 'svg')
    video_extensions = ('avi', 'mp4', 'mov', 'mkv')
    document_extensions = ('doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx')
    music_extensions = ('mp3', 'ogg', 'wav', 'amr')
    archive_extensions = ('zip', 'gz', 'tar')

    known_extensions = set(
        image_extensions + video_extensions + document_extensions + music_extensions + archive_extensions
    )

    unknown_extensions = set()

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = file.split('.')[-1].lower()
            new_file_name = normalize(file.split('.')[0]) + '.' + file_extension
            new_file_path = os.path.join(root, new_file_name)

            if file_extension in known_extensions:
                if file_extension in image_extensions:
                    destination = 'images'
                elif file_extension in video_extensions:
                    destination = 'video'
                elif file_extension in document_extensions:
                    destination = 'documents'
                elif file_extension in music_extensions:
                    destination = 'audio'
                elif file_extension in archive_extensions:
                    destination = 'archives'
                if destination == 'archives':
                    # Розпаковка архіву і переміщення вмісту до відповідної підпапки
                    os.makedirs(os.path.join(root, destination), exist_ok=True)
                    shutil.unpack_archive(file_path, os.path.join(root, destination, normalize(file.split('.')[0])))
                else:
                    os.makedirs(os.path.join(root, destination), exist_ok=True)
                    shutil.move(file_path, os.path.join(root, destination, new_file_name))
            else:
                unknown_extensions.add(file_extension)

            os.remove(file_path)

    # Видалення порожніх папок
    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            if not os.listdir(directory_path):
                os.rmdir(directory_path)

    return known_extensions, unknown_extensions

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Потрібно вказати шлях до папки як аргумент командного рядка.")
    else:
        folder_path = sys.argv[1]
        known_extensions, unknown_extensions = organize_files(folder_path)
        print("Відомі розширення:", known_extensions)
        print("Невідомі розширення:", unknown_extensions)
        print("Сортування та перейменування завершено.")
