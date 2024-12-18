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

def extract_domains(lines):
    """Извлекает домены из формата Switchy Omega."""
    domains = set()
    domain_pattern = re.compile(r"^\*://\*\.(.+)/\*$")  # Регулярка для извлечения доменов
    for line in lines:
        line = line.strip()
        match = domain_pattern.match(line)
        if match:
            domains.add(match.group(1))  # Добавляем только домен
        else:
            print(f"Пропущена некорректная строка: {line}")
    return domains

def convert_to_switchy(domains):
    """Преобразует домены в формат Switchy Omega."""
    switchy_lines = ["#BEGIN\n\n[Wildcard]\n"]
    for domain in sorted(domains):  # Сортируем для порядка
        switchy_lines.append(f"*://*.{domain}/*\n")
    switchy_lines.append("#END\n")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Текущее время
    switchy_lines.append(f"# List created on {now}\n")
    return switchy_lines

def save_to_file(filename, lines):
    """Сохраняет строки в файл."""
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(lines)
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(url1, url2, output_file):
    """Скачивает, обрабатывает списки и сохраняет результат."""
    # Скачиваем списки
    main_list = download_list(url1)
    community_list = download_list(url2)

    # Извлекаем домены
    main_domains = extract_domains(main_list)
    community_domains = extract_domains(community_list)

    # Убираем дубликаты
    unique_domains = main_domains.union(community_domains)
    print(f"Объединено {len(unique_domains)} уникальных доменов.")

    # Преобразуем в формат Switchy Omega
    switchy_lines = convert_to_switchy(unique_domains)

    # Сохраняем итоговый список
    save_to_file(output_file, switchy_lines)

if __name__ == "__main__":
    process_and_refilter(url_main, url_community, output_file)
