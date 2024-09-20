import requests
from bs4 import BeautifulSoup
import os

# Base URL for the pages
base_url = "https://openmw.readthedocs.io/en/latest/reference/lua-scripting/"

# The index page URL
index_url = base_url + "index.html"

# Create the directory to store the files if it doesn't exist
output_dir = 'data/lua-scripting/'
os.makedirs(output_dir, exist_ok=True)

# Send a request to get the index page content
response = requests.get(index_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links within the main content
main_content = soup.find('div', class_='rst-content')

if main_content:
    # Extract all the links that point to the Lua scripting subpages
    links = main_content.find_all('a', href=True)

    for link in links:
        # Get the href attribute of the link
        href = link['href']
        
        # Skip if it is a fragment link or an external link
        if href.startswith('#') or not href.endswith('.html'):
            continue
        
        # Build the full URL to visit the page
        page_url = base_url + href
        
        # Send a request to the page
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        
        # Find the main content of the page
        page_content = page_soup.find('div', class_='rst-content')
        
        if page_content:
            # Save the HTML content of the page without the sidebar
            filename = os.path.join(output_dir, href)
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(page_content.prettify())
            print(f"Saved: {filename}")
else:
    print("Main content not found on the index page.")
