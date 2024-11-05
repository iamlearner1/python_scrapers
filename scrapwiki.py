import requests
from bs4 import BeautifulSoup
import json

def get_wikipedia_place_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract place name
        place_name_element = soup.find('h1', id='firstHeading')
        place_name = place_name_element.text.strip() if place_name_element else "N/A"

        # Hardcode place type as 'Neighborhood'
        place_type = "Neighborhood"

        # Extract coordinates with checks
        lat_element = soup.find('span', class_='latitude')
        lon_element = soup.find('span', class_='longitude')
        lat = lat_element.text if lat_element else "N/A"
        lon = lon_element.text if lon_element else "N/A"

        # Extract details from the infobox
        infobox = soup.find('table', class_='infobox ib-settlement vcard')
        details = {}
        if infobox:
            for row in infobox.find_all('tr'):
                if row.th and row.td:
                    key = row.th.text.strip()
                    value = row.td.text.strip()
                    if key in ['Country', 'State', 'Region', 'District', 'PIN', 'Parliament constituencies', 'Sasana Sabha constituencies']:
                        details[key] = value

        # Extract images
        images = []
        for img in soup.find_all('img'):
            img_src = img.get('src')
            if img_src:
                images.append('https:' + img_src)

        place_data = {
            'Place Name': place_name,
            'Place Type': place_type,  # Hardcoded
            'Coordinates': {'Latitude': lat, 'Longitude': lon},
            'Country': details.get('Country', 'N/A'),
            'State': details.get('State', 'N/A'),
            'Region': details.get('Region', 'N/A'),
            'District': details.get('District', 'N/A'),
            'Pincode': details.get('PIN', 'N/A'),
            'Lok Sabha Constituency': details.get('Parliament constituencies', 'N/A'),
            'Vidhan Sabha Constituency': details.get('Sasana Sabha constituencies', 'N/A'),
            'Image URLs': images
        }

        return place_data

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

def scrape_neighborhoods_and_save(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all <ul> elements
        uls = soup.find_all('ul')
        base_url = 'https://en.wikipedia.org'

        # Extract regions and neighborhoods
        all_place_data = []
        current_region = 'N/A'

        for ul in uls:
            for li in ul.find_all('li'):
                link = li.find('a', href=True)
                if link:
                    name = link.text.strip()
                    if name:
                        # Construct URL for each neighborhood
                        neighborhood_url = base_url + link['href']
                        print(f"Processing {name} in region {current_region}...")
                        place_data = get_wikipedia_place_details(neighborhood_url)
                        if place_data:
                            # Update region in place_data
                            place_data['Region'] = current_region
                            # Append data to the list
                            all_place_data.append(place_data)
        
        # Extract regions
        headings = soup.find_all('div', class_='mw-heading mw-heading3')
        for heading in headings:
            region_name = heading.find('h3')
            if region_name:
                current_region = region_name.text.strip()
        
        # Save all data to a single JSON file
        with open('neighborhoods_data.json', 'w') as json_file:
            json.dump(all_place_data, json_file, indent=4)

        print("All data saved to 'neighborhoods_data.json'.")

    except Exception as e:
        print(f"Error scraping neighborhoods: {e}")

# URL for the list of neighborhoods
url = 'https://en.wikipedia.org/wiki/List_of_neighbourhoods_in_Hyderabad'
scrape_neighborhoods_and_save(url)
