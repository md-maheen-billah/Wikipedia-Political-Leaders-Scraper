# Wikipedia Political Leaders Scraper
[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


## 🏢 Description

As part of my training at BeCode, I developed this project to practice working with APIs, web scraping, and object-oriented programming concepts in Python.

The scenario involves building a scraper that retrieves information about political leaders from different countries. The application fetches data from a custom API, then enriches it by scraping the first paragraph from each leader's Wikipedia page.

Each time the script runs, it collects fresh data about leaders from multiple countries, their biographical information, and stores everything in a structured JSON format, demonstrating API integration, web scraping techniques, and OOP principles.

![wiki_scraper_img](https://i.ibb.co/m5GmYfFG/Chat-GPT-Image-Feb-20-2026-10-06-03-AM.png)


## 💡 OOP Concepts Used

This project demonstrates several key OOP principles:

Classes and Objects – WikipediaScraper class was created to encapsulate all scraping functionality.

Abstraction – Methods such as get_countries(), get_leaders(), and get_first_paragraph() hide complex implementation details behind simple interfaces.

State Management – The class maintains state through attributes like leaders_data and cookie, persisting data across method calls.

Modularity – Each method has a single responsibility, making the code maintainable and testable.


## 📦 Libraries Used

The project uses the following Python libraries:

 - BeautifulSoup (bs4) – To parse HTML content and extract relevant paragraphs.
 - re – For text cleaning and pattern matching (standard library).
 - json – To handle JSON data serialization (standard library).
 - time – To implement respectful delays between requests (standard library).


## 📦 Repo structure

```
.
├── src/
│   ├── leaders_scraper.py
│   └── scraper.py
├── leaders.json
├── main.py
├── README.md
├── requirements.txt
└── wikipedia_scraper.ipynb
```

## 🛎️ Usage

1. Clone the repository to your local machine.

```bash
git clone https://github.com/md-maheen-billah/Wikipedia-scraper.git
cd wikipedia-leaders-scraper
python main.py
```
2. Install the required dependencies.

```bash
pip install -r requirements.txt
```

3. In order to run the script, execute the `main.py` file from your terminal:

```bash
python main.py
```  

4. The script will:

 - Fetch a valid cookie from the API
 - Retrieve the list of supported countries
 - Collect leader data for each country
 - Scrape the first paragraph from each leader's Wikipedia page
 - Save everything to a JSON file

```python
input_filepath = "new_colleagues.csv"
output_filename = "output.csv"

# Create scraper instance
scraper = WikipediaScraper()

# Fetch all countries
print("Fetching countries data...")
countries = scraper.get_countries()
print(countries)
    
# Fetch all leaders data of a specific country
print("Fetching leaders data...")
leaders = scraper.get_leaders("be")

# Save to JSON
scraper.to_json_file("leaders.json")
print("Done! Data saved to leaders.json")

```
## 🔍 Methods Overview
| Method | Description | Returns |
|--------|-------------|---------|
| `refresh_cookie()` | Gets a new valid cookie from the API | Cookie object |
| `get_countries()` | Retrieves list of supported countries | List of country names |
| `get_leaders()` | Fetches leaders for all countries and adds Wikipedia bios | None (populates `leaders_data`) |
| `get_first_paragraph(url)` | Scrapes first paragraph from Wikipedia | String or None |
| `to_json_file(filepath)` | Saves data structure to JSON file | None |
## ⏱️ Timeline

This project took 2 days for completion.

## 📌 Personal Situation
This project was done as part of the AI Boocamp at BeCode.org. 

Connect with me on [LinkedIn](https://www.linkedin.com/in/md-maheen-billah/).

