from src.scraper import WikipediaScraper

def main():
    # Create scraper instance
    scraper = WikipediaScraper()

    # Fetch all countries
    print("Fetching countries data...")
    countries = scraper.get_countries()
    print(countries)
    
    # Fetch all leaders data of a specific country
    print("Fetching leaders data...")
    leaders = scraper.get_leaders("be")

    # Fetch all leaders data of a specific country
    print("Fetching leaders data...")
    leaders = scraper.get_leaders("be")

    # # Fetch all leaders data of a all countries
    # print("Fetching leaders data...")
    # for country in countries:
    #     leaders = scraper.get_leaders(country)
    
    # Save to JSON
    scraper.to_json_file("leaders.json")
    print("Done! Data saved to leaders.json")

if __name__ == "__main__":
    main()