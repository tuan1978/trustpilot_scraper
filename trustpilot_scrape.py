
import csv
import requests
import lxml.html as html
from bs4 import BeautifulSoup
import trustpilot_review as tr

## Configurations

# Trustpilot review page
base_page = 'http://www.trustpilot.com/review/'
query_parameters = "languages=all"

# Data file to save to
datafile = 'dataMiele.csv'

combined_file = True

sites = [
    {
        "name": "NL",
        "url": "miele.nl",
        "pages": 7
    },
    {
        "name": "ES",
        "url": "miele.es",
        "pages": 3
    },
    {
        "name": "IT",
        "url": "miele.it",
        "pages": 3
    },
    {
        "name": "DK",
        "url": "www.miele.dk",
        "pages": 104
    },
    {
        "name": "NO",
        "url": "miele.no",
        "pages": 1
    },
    {
        "name": "SE",
        "url": "miele.se",
        "pages": 2
    },
    {
        "name": "UK",
        "url": "www.miele.co.uk",
        "pages": 118
    },
    {
        "name": "BE",
        "url": "miele.be",
        "pages": 3
    },
    {
        "name": "FR",
        "url": "miele.fr",
        "pages": 14
    },
    {
        "name": "DE",
        "url": "www.miele.de",
        "pages": 47
    },
    {
        "name": "US",
        "url": "mieleusa.com",
        "pages": 6
    }
]
review_results = [['Country', 'Name', 'Rating', 'PostedDate', 'Header', 'Content']]

for site in sites:
    review_site = site["url"]
    site_name = site["name"]

    review_page = f"{base_page}{review_site}?{query_parameters}"
    
    if not combined_file:
        review_results = [['Country', 'Name', 'Rating', 'PostedDate', 'Header', 'Content']]

    result = requests.get(review_page)
    initial_soup = BeautifulSoup(result.content, 'html.parser')
    last_page_link = initial_soup.find_all("a", {"data-pagination-button-last-link": "true"})
    if last_page_link:        
        number_of_pages = int(initial_soup.find_all("a", {"data-pagination-button-last-link": "true"})[0].find_all("span")[0].text)
    else:
        number_of_pages = 1
    for page in range(1, number_of_pages + 1):
        if page == 1:
            url = review_page
        else:
            url = f"{review_page}&page={page}"
    
        result = requests.get(url)
        soup = BeautifulSoup(result.content)
        review_results += tr.TrustpilotReview.reviews_from_html(soup, site_name)
    
    review_results = [list(review) for review in review_results]

    if not combined_file:
        parts = datafile.split(".")
        file_name = f"{parts[0]}_{site['name']}.{parts[1]}" 
        with open(file_name, 'w', newline='', encoding="utf-8") as f:      
            # using csv.writer method from CSV package
            write = csv.writer(f, delimiter=';')
            
            write.writerow(review_results[0])
            write.writerows(review_results[1:])
    
if combined_file:
    with open(datafile, 'w', newline='', encoding="utf-8") as f:      
        # using csv.writer method from CSV package
        write = csv.writer(f, delimiter=';')
        
        write.writerow(review_results[0])
        write.writerows(review_results[1:])
