import requests
from bs4 import BeautifulSoup
import json


def collect_legitimate_data(urls):
    legitimate_data = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string if soup.title else ""
            meta_description = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_description['content'] if meta_description else ""
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            meta_keywords = meta_keywords['content'] if meta_keywords else ""
            text_content = ' '.join([p.get_text() for p in soup.find_all('p')])

            legitimate_data.append({
                'url': url,
                'title': title,
                'meta_description': meta_description,
                'meta_keywords': meta_keywords,
                'text_content': text_content,
                'content_length': len(text_content),
                'num_forms': len(soup.find_all('form')),
                'num_external_links': len(soup.find_all('a', href=True))
            })
            print(f"Collected data from {url}")
        except requests.RequestException as e:
            print(f"Failed to collect data from {url}: {e}")
        except KeyError as e:
            print(f"KeyError collecting data from {url}: {e}")
    return legitimate_data


# Citim URL-urile din fișierul legitimate_urls.txt
with open('legitimate_urls.txt', 'r') as f:
    urls = [line.strip() for line in f]

# Colectăm datele legitime
legitimate_data = collect_legitimate_data(urls)

# Salvăm datele într-un fișier JSON
with open('legitimate_data.json', 'w', encoding='utf-8') as f:
    json.dump(legitimate_data, f, ensure_ascii=False, indent=4)

print("Legitimate data collected and saved to legitimate_data.json.")
