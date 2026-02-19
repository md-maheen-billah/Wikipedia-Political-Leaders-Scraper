import requests
import time
from bs4 import BeautifulSoup
import re
import json
class WikipediaScraper:
    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"
        self.check_endpoint = "/check"
        self.leaders_data = {}
        self.cookie = {}
        self.wikipedia_session = requests.Session()
        self.wikipedia_session.headers.update({
            "User-Agent": "Wikipedia-scraper/1.0 (md.maheen.billah.97@gmail.com)"
        })
    

    def get_cookie(self):
        cookie_url = f"{self.base_url}{self.cookies_endpoint}"
        req = requests.get(cookie_url)
        self.cookie = req.cookies.get_dict()
        return self.cookie
    
    def check_cookie(self):
        check_url = f"{self.base_url}{self.check_endpoint}"
        req = requests.get(check_url, cookies=self.cookie)
        return req.status_code == 200
    
    def ensure_valid_cookie(self):
        if not self.check_cookie():
            print("Cookie invalid or expired. Getting new cookie...")
            self.get_cookie()
        return self.cookie
    
    def get_countries(self):
        self.ensure_valid_cookie()
        country_url = f"{self.base_url}{self.country_endpoint}"
        req = requests.get(country_url, cookies=self.cookie)
        return req.json()
     
    def get_leaders(self, country: str):
        self.ensure_valid_cookie()
        url = f"{self.base_url}{self.leaders_endpoint}"
        req = requests.get(url, params={"country": country}, cookies=self.cookie)
        
        self.leaders_data[country] = req.json()
        
        for leader in self.leaders_data[country]:
            wikipedia_url = leader["wikipedia_url"]
            paragraph = self.get_first_paragraph(wikipedia_url)
            leader['bio'] = paragraph
            time.sleep(0.5)  


    def get_first_paragraph(self, wikipedia_url: str) -> str:
        headers = {
                "User-Agent": "Wikipedia-scraper/1.0 (md.maheen.billah.97@gmail.com)"
            }
        req = self.wikipedia_session.get(wikipedia_url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        paragraphs = soup.find_all('p')
            
        for paragraph in paragraphs:
            text = paragraph.get_text().strip()
            if not text:
                continue
            if paragraph.find_parent('div', class_='hatnote') or \
                paragraph.find_parent('div', class_='dablink') or \
                paragraph.find_parent('div', class_='homonymie') or \
                paragraph.find_parent('div', class_='bandeau') or \
                paragraph.find_parent('div', class_='mw-flagged') or \
                paragraph.find_parent('div', class_='mw-checked') or \
                paragraph.find_parent('div', class_='verified') or \
                paragraph.find_parent('div', class_='mw-verified') or \
                paragraph.find_parent('div', class_='metadata'): 
                continue
            if len(text) < 20:
                continue
            if "متحقق منها" in text or "مفحوصة" in text:  
                continue
            else:
                 text = re.sub(r'\[[^\]]*\]', '', text)
                 text = re.sub(r'\(\s*[^)]*[ɑɛœɔʁɡʒʃɥɑ̃ɛ̃ɔ̃][^)]*\)', '', text)
                 text = re.sub(r'Écouterⓘ', '', text)
                 text = re.sub(r'\[\d+\]', '', text)
                 text = re.sub(r'\[[a-z]\]', '', text) 
                 text = re.sub(r'\([^)]*ⓘ[^)]*\)', '', text)
                 text = re.sub(r'\([^)]*[ɑɛœɔʁɡʒʃ][^)]*\)', '', text)
                 text = re.sub(r'\(\s*\)', '', text)
                 text = re.sub(r'\s+', ' ', text).strip()
                 return text
            
    def to_json_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.leaders_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filepath}")
            
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        if self.leaders_data == loaded_data:
            print("Data successfully matched perfectly!")
        else:
            print("Data mismatch!")
           

