import json
import re

# Funcție pentru curățarea textului
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Înlocuiește spațiile multiple cu un singur spațiu
    text = text.strip()  # Elimină spațiile goale de la început și sfârșit
    return text

# Încarcă datele din fișierul JSON
with open('C:\pythonProject\pythonProject\phishing_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Preprocesează datele
for entry in data:
    entry['title'] = clean_text(entry['title'])
    entry['meta_description'] = clean_text(entry['meta_description'])
    entry['meta_keywords'] = clean_text(entry['meta_keywords'])
    entry['text_content'] = clean_text(entry['text_content'])

# Salvează datele preprocesate într-un nou fișier JSON
with open('phishing_data_clean.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Data cleaning complete. Preprocessed data saved to phishing_data_clean.json.")
