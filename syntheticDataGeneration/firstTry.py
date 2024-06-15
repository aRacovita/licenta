import openai
import json
import os
from openai import OpenAI
# Setează cheia API OpenAI
openai.api_key = 'sk-proj-vInvndpGgW3Is1u2uhwPT3BlbkFJQTezkqbve0dxTUk9nhxo'
client = OpenAI(
    # This is the default and can be omitted
    api_key='sk-proj-vInvndpGgW3Is1u2uhwPT3BlbkFJQTezkqbve0dxTUk9nhxo',
)
# Funcție pentru generarea de date sintetice
def generate_phishing_content(prompts, num_samples_per_prompt=5, temperature=0.7):
    synthetic_data = []
    for prompt in prompts:
        for _ in range(num_samples_per_prompt):
            response = client.chat.completions.create(
                model="gpt-4o",  # Poți folosi modelul 'gpt-3.5-turbo' sau alt model disponibil
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=200
            )
            response_message = response.choices[0].message.content.strip()
            synthetic_data.append({
                'url': 'synthetic_phishing_site',
                'title': 'Synthetic Phishing Page',
                'meta_description': '',
                'meta_keywords': '',
                'text_content': response_message,
                'content_length': len(response_message),
                'num_forms': response_message.count('<form'),
                'num_external_links': response_message.count('<a href="http')
            })
    return synthetic_data

# Prompturi pentru diferite tipuri de phishing
prompts = [
    """
    Generate a realistic web page content targeting users to enter their banking credentials. 
    Include common elements such as login forms, fake security alerts, and links.
    """,
    """
    Generate a realistic web page content targeting users to enter their social media credentials (e.g., Instagram, Telegram). 
    Include common elements such as login forms, fake notifications, and links.
    """,
    """
    Generate a realistic web page content targeting users to enter their online service credentials (e.g., Amazon, MetaMask). 
    Include common elements such as login forms, fake alerts, and links.
    """,
    """
    Generate a realistic web page content targeting users to enter their cryptocurrency wallet credentials (e.g., MetaMask, Trust Wallet). 
    Include common elements such as recovery phrase forms, fake alerts, and links.
    """,
    """
    Generate a realistic web page content pretending to be a technical support center (e.g., Business Help Center). 
    Include common elements such as support forms, fake notifications, and links.
    """
]

# Generează date sintetice
synthetic_data = generate_phishing_content(prompts, num_samples_per_prompt=5, temperature=0.7)

# Salvează datele sintetice într-un fișier JSON separat
with open('synthetic_phishing_data.json', 'w', encoding='utf-8') as f:
    json.dump(synthetic_data, f, ensure_ascii=False, indent=4)

print("Synthetic data generated and saved to synthetic_phishing_data.json.")