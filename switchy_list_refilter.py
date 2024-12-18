import requests
from datetime import datetime
import re

# URLs для скачивания списков
url_main = "https://community.antifilter.download/list/domains.txt"  # URL основного списка
url_community = "https://raw.githubusercontent.com/MastiZz/Refilter-Switchy-Omega/main/community.txt"  # URL community списка

# Имя итогового файла
output_file = "Refilter+antifilter community.txt"

def download_list(url):
    """Скачивает список доменов по URL."""
    try:
        print(f"Скачивание списка: {url}")
        response = requests.get(url)
        response.raise_for_status()
        print("Список успешно скачан.")
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании списка: {e}")
        return []

def parse_switchy_lines(lines):
    """Парсит строки Switchy Omega, извлекает и проверяет домены."""
    domains = set()
    domain_pattern = re.compile(r"^\*://\*\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}/\*$")  # Проверяем формат доменов
    for line in lines:
        line = line.strip()
        if domain_pattern.match(line):  # Если строка соответствует формату
            domain = line[7:-2]  # Извлекаем домен без *://*. и /*
            domains.add(domain)
        else:
            print(f"Пропущена некорректная строка: {line}")
    return domains

def save_to_file(filename, domains):
    """Сохраняет список доменов в файл с заголовком и временем создания."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущее время
    with open(filename, "w", encoding="utf-8") as file:
        file.write("#BEGIN\n\n[Wildcard]\n")  # Заголовок
        for domain in sorted(domains):  # Сортируем для порядка
            file.write(f"*://*.{domain}/*\n")
        file.write("#END\n")  # Завершающая строка
        file.write(f"# List created on {now}\n")  # Дата и время создания
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(url1, url2, output_file):
    """Обрабатывает два списка, убирает дубликаты и сохраняет результат."""
    # Скачиваем списки
    main_list = download_list(url1)
    community_list = download_list(url2)

    # Парсим домены
    main_domains = parse_switchy_lines(main_list)
    community_domains = parse_switchy_lines(community_list)

    # Убираем дубликаты между списками
    unique_domains = main_domains.union(community_domains)  # Объединяем списки
    print(f"Объединено {len(unique_domains)} уникальных доменов.")

    # Сохраняем итоговый список
    save_to_file(output_file, unique_domains)

if __name__ == "__main__":
    process_and_refilter(url_main, url_community, output_file)
