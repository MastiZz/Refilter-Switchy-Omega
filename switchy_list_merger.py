import requests
from datetime import datetime

# URLs списков
url_main = "https://community.antifilter.download/list/domains.txt"  # URL основного списка
url_community = "https://raw.githubusercontent.com/MastiZz/Refilter-Switchy-Omega/main/community.txt"  # URL community списка

# Выходной файл
output_file = "combined_switchy_list.txt"

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
    """Парсит строки Switchy Omega и извлекает домены."""
    domains = set()
    for line in lines:
        line = line.strip()
        if line.startswith("*://*.") and line.endswith("/*"):  # Проверяем формат
            domain = line[7:-2]  # Извлекаем домен без *://*. и /*
            domains.add(domain)
    return domains

def save_to_file(filename, domains):
    """Сохраняет объединённый список в файл с заголовком и временем создания."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущее время
    with open(filename, "w", encoding="utf-8") as file:
        file.write("#BEGIN\n\n[Wildcard]\n")  # Заголовок
        for domain in sorted(domains):  # Сортируем для порядка
            file.write(f"*://*.{domain}/*\n")
        file.write("#END\n")  # Завершающая строка
        file.write(f"# List created on {now}\n")  # Дата и время создания
    print(f"Объединённый список сохранён в {filename}")

def process_lists(url1, url2, output_file):
    """Скачивает два списка, объединяет их и сохраняет результат."""
    # Скачиваем списки
    list1 = download_list(url1)
    list2 = download_list(url2)

    # Парсим домены из обоих списков
    domains1 = parse_switchy_lines(list1)
    domains2 = parse_switchy_lines(list2)

    # Объединяем и удаляем дубликаты
    combined_domains = domains1.union(domains2)
    print(f"Объединено {len(combined_domains)} уникальных доменов.")

    # Сохраняем результат
    save_to_file(output_file, combined_domains)

if __name__ == "__main__":
    process_lists(url_main, url_community, output_file)
