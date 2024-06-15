import openai
import json
import os
from openai import OpenAI

# Setează cheia API OpenAI
api_key = 'sk-proj-vInvndpGgW3Is1u2uhwPT3BlbkFJQTezkqbve0dxTUk9nhxo'

client = OpenAI(
    api_key=api_key,
)

# Prompturi pentru diferite tipuri de phishing
prompts = [
    """
    Generate a realistic web page content similar to the following JSON examples, including URL, title, and other metadata in the same format:
    {
        "url": "https://secure-login.bankxyz.com/",
        "title": "BankXYZ Secure Login",
        "meta_description": "Secure login portal for BankXYZ customers. Access your account safely and manage your finances with ease.",
        "meta_keywords": "BankXYZ, secure login, online banking, account management",
        "text_content": "BankXYZ Secure Login Log in to your account. Forgot your password? Don't have an account? Sign up Contact Us Privacy Policy Terms of Service BankXYZ © 2024",
        "content_length": 206,
        "num_forms": 1,
        "num_external_links": 3
    },
    {
        "url": "https://socialmedia-app.com/login",
        "title": "SocialMedia App - Login",
        "meta_description": "Login to SocialMedia App to connect with friends and family. Share updates, photos, and videos.",
        "meta_keywords": "SocialMedia, login, connect, friends, family",
        "text_content": "SocialMedia App Login Log in to your account. Forgot your password? Don't have an account? Sign up Contact Us Privacy Policy Terms of Service SocialMedia © 2024",
        "content_length": 189,
        "num_forms": 1,
        "num_external_links": 2
    },
     {
        "url": "https://elenmistoprak.com/940293450/Instagram.com.html",
        "title": "Instagram",
        "meta_description": "Instagram",
        "meta_keywords": "Instagram",
        "text_content": "Instagram Please click Allow to access the website",
        "content_length": 114,
        "num_forms": 0,
        "num_external_links": 0
    },
    {
        "url": "https://ipfs.io/ipfs/bafybeigvhe4mkl2k5o3zpkqomu2s5zk76ht44z5wz567p572zitwi7jzdq/index%20(2).html",
        "title": "DHL | Tracking System",
        "meta_description": "",
        "meta_keywords": "",
        "text_content": "DHL | Tracking System Online Tracking System Track Package Login your E-mail to view package tracking information",
        "content_length": 170,
        "num_forms": 1,
        "num_external_links": 0
    },
    {
        "url": "https://cloudflare-ipfs.com/ipfs/bafybeigvhe4mkl2k5o3zpkqomu2s5zk76ht44z5wz567p572zitwi7jzdq/index%20(2).html",
        "title": "DHL | Tracking System",
        "meta_description": "",
        "meta_keywords": "",
        "text_content": "DHL | Tracking System Online Tracking System Track Package Login your E-mail to view package tracking information",
        "content_length": 170,
        "num_forms": 1,
        "num_external_links": 0
    },
    {
        "url": "http://pblishedaccs1st.ftp.sh/",
        "title": "Facebook",
        "meta_description": "",
        "meta_keywords": "",
        "text_content": "Facebook Teks asli Beri rating terjemahan ini Masukan Anda akan digunakan untuk membantu meningkatkan kualitas Google Terjemahan Your Account Has Been Locked Your account will soon be deactivated because someone has reported your account as violating copyright. Account Locked May 31, 2024 For the security and safety of other users we will immediately disable your account if you ignore this warning. We will walk you through several steps to cancel a deactivated account. Get Started",
        "content_length": 719,
        "num_forms": 1,
        "num_external_links": 5
    }
    
    Here are a few key points to ensure the data is suitable for training a phishing detection model:

    Realism: The generated data includes realistic URLs, titles, meta descriptions, and other metadata that are typical of legitimate websites. This realism is crucial for training a model to distinguish between phishing and legitimate sites.

    Diversity: The dataset covers various types of websites, from online shopping to social media, which is important for a robust phishing detection model.

    Common Elements: Each entry includes common elements like login forms, sign-up prompts, and contact links, which are typical features of both phishing and legitimate sites.
    
    Please provide just the raw json without any other inputs like "These JSON objects represent the metadata and content of various web pages, structured similarly to the examples you provided.}"
    """
]

# Funcție pentru generarea de date sintetice
def generate_phishing_content(prompts, num_samples_per_prompt=10, temperature=0.7):
    synthetic_data = []
    for prompt in prompts:
        for _ in range(num_samples_per_prompt):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1500
            )
            response_message = response.choices[0].message.content.strip()
            print("Raw API response:")
            print(response_message)  # Afișăm răspunsul brut de la API

            # Curățăm delimitatorii și descompunem răspunsul în multiple obiecte JSON
            response_message = response_message.replace('```json', '').replace('```', '').strip()
            try:
                json_objects = json.loads(f"[{response_message}]")
                synthetic_data.extend(json_objects)
            except json.JSONDecodeError:
                print("Failed to parse generated JSON")

    return synthetic_data

# Generează date sintetice
synthetic_data = generate_phishing_content(prompts, num_samples_per_prompt=10, temperature=0.7)

# Salvează datele sintetice într-un fișier JSON separat
with open('synthetic_phishing_data.json', 'w', encoding='utf-8') as f:
    json.dump(synthetic_data, f, ensure_ascii=False, indent=4)

print("Synthetic data generated and saved to synthetic_phishing_data.json.")
