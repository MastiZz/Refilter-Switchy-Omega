import requests
from datetime import datetime

# URLs списков
url_domain = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/domains_all.lst"  # URL первого списка
url_community = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst"  # URL второго списка

# Выходные файлы
output_domain = "domain_all.txt"
output_community = "community.txt"

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

def convert_to_switchy_format(lines):
    """Преобразует список доменов в формат Switchy Omega."""
    unique_domains = set()
    for line in lines:
        domain = line.strip()
        if domain:  # Пропускаем пустые строки
            unique_domains.add(f"*://*.{domain}/*")
    return sorted(unique_domains)  # Сортируем для порядка

def save_to_file(filename, domains):
    """Сохраняет список в файл с заголовком, подвалом и временем создания."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущее время
    with open(filename, "w", encoding="utf-8") as file:
        file.write("#BEGIN\n\n[Wildcard]\n")  # Заголовок
        file.write("\n".join(domains))  # Домены
        file.write("\n#END\n")  # Завершающая строка
        file.write(f"# List created on {now}\n")  # Дата и время создания
    print(f"Список сохранён в {filename}")

def process_list(url, output_file):
    """Обрабатывает список: скачивает, преобразует и сохраняет."""
    lines = download_list(url)
    domains = convert_to_switchy_format(lines)
    save_to_file(output_file, domains)

if __name__ == "__main__":
    # Обработка первого списка
    process_list(url_domain, output_domain)

    # Обработка второго списка
    process_list(url_community, output_community)
