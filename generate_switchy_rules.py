import requests

# URL файла со списком доменов
GITHUB_URL = "https://github.com/1andrevich/Re-filter-lists/blob/main/ooni_domains.lst"  # Замени на реальный URL

# Имя выходного файла
OUTPUT_FILE = "switchy_omega_rules.txt"

def download_domains(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return [line.strip() for line in response.text.splitlines() if line.strip()]
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")
        return []

def generate_switchy_omega_rules(domains):
    rules = "BEGIN\n\n[Wildcard]\n"
    for domain in domains:
        rules += f"*://{domain}/*\n"
    return rules

def save_to_file(data, filename):
    with open(filename, "w") as file:
        file.write(data)

def main():
    print("Скачивание списка доменов...")
    domains = download_domains(GITHUB_URL)
    if not domains:
        print("Список пуст или не скачан.")
        return
    print("Генерация правил...")
    rules = generate_switchy_omega_rules(domains)
    save_to_file(rules, OUTPUT_FILE)
    print("Файл сохранен:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
