import requests
from requests import Session
import json
import time
from bs4 import BeautifulSoup
import re
def get_first_paragraph(wikipedia_url, session: Session):
    # print(wikipedia_url) # keep this for the rest of the notebook
    headers = {
    "User-Agent": "Wikipedia-scraper/1.0 (md.maheen.billah.97@gmail.com)"
    }
    req = session.get(wikipedia_url,headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    paragraphs = soup.find_all('p')
    first_paragraph = None
    for paragraph in paragraphs:
        text = paragraph.get_text().strip() #stripping white space   
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
        if len(text) < 20:  # Adjust this threshold as needed
            continue
        if "متحقق منها" in text or "مفحوصة" in text:  
            continue
        else:  # we are hoping the length to be atleast more than 20
            text = re.sub(r'\[[^\]]*\]', '', text)
            text = re.sub(r'\(\s*[^)]*[ɑɛœɔʁɡʒʃɥɑ̃ɛ̃ɔ̃][^)]*\)', '', text)
            text = re.sub(r'Écouterⓘ', '', text)
            text = re.sub(r'\[\d+\]', '', text)
            text = re.sub(r'\[[a-z]\]', '', text) 
            text = re.sub(r'\([^)]*ⓘ[^)]*\)', '', text)
            text = re.sub(r'\([^)]*[ɑɛœɔʁɡʒʃ][^)]*\)', '', text)
            text = re.sub(r'\(\s*\)', '', text)
            text = re.sub(r'\s+', ' ', text).strip()
            first_paragraph = text
            break
    return first_paragraph

def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    # Set the cookies variable
    cookie_url = f"{root_url}/cookie"
    req = requests.get(cookie_url)
    cookies = req.cookies.get_dict()
    # Set the endpoint /countries and keep in a variable countries
    req = requests.get(f"{root_url}/countries",cookies=cookies)
    countries = req.json()
    #wikipedia sessions
    wikipedia_session = requests.Session()
    wikipedia_session.headers.update({
        "User-Agent": "Wikipedia-scraper/1.0 (md.maheen.billah.97@gmail.com)"
    })
    # Make a dictionary named leaders_per_country and loop through the countries variable and insert them inside the disctionary
    leaders_url = f"{root_url}/leaders"
    leaders_per_country = {}
    leaders_per_country = {country:requests.get(leaders_url,params={"country":country},cookies=cookies).json() for country in countries}
    for country in leaders_per_country:
        # print(f"Country: {country.upper()}\n")
        for leader in leaders_per_country[country]:
            wikipedia_url = leader["wikipedia_url"]
            # fname = leader["first_name"]
            # lname = leader["last_name"]
            # if  not lname or lname == "None":
            #     print(f"  Leader: {fname}")
            # else:
            #     print(f"  Leader: {fname} {lname}")
            # print(f"  URL: {wikipedia_url}")
            paragraph = get_first_paragraph(wikipedia_url,wikipedia_session)
            leader['bio'] = paragraph
            # print(f"  Bio: {paragraph}\n")
            time.sleep(0.5)
    # display the leaders variable (1 line)
    return leaders_per_country

leaders_per_country = get_leaders()

def save(leaders_per_country):
    with open('leaders.json', 'w', encoding='utf-8') as f:
        json.dump(leaders_per_country, f, indent=2, ensure_ascii=False)
        print("Data saved to leaders_per_country.json")
    with open('leaders.json', 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
    if leaders_per_country == loaded_data:
        print("Data successfully matched perfectly!")
    else:
        print("Data mismatch!")

save(leaders_per_country)


