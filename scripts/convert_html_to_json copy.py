import os
from bs4 import BeautifulSoup
import json

# Directories
html_dir = 'data/lua-scripting/'
json_dir = 'data/json/lua-scripting/'
os.makedirs(json_dir, exist_ok=True)

# Loop through all HTML files in the lua-scripting directory
for html_file in os.listdir(html_dir):
    if html_file.endswith('.html'):
        html_path = os.path.join(html_dir, html_file)
        
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main content and ignore the page navigation
        page_content = soup.find('div', class_='rst-content')

        if page_content:
            # Prepare the structure for JSON
            page_data = {
                "title": soup.find('h1').get_text(strip=True) if soup.find('h1') else "No Title",
                "sections": []
            }

            # Loop through each element in the content
            for element in page_content.find_all(['h2', 'h3', 'p', 'pre', 'code']):
                if element.name in ['h2', 'h3']:
                    section = {
                        "header": element.get_text(strip=True),
                        "content": []
                    }
                    page_data["sections"].append(section)
                elif element.name == 'p':
                    if page_data["sections"]:
                        page_data["sections"][-1]["content"].append({"paragraph": element.get_text(strip=True)})
                elif element.name in ['pre', 'code']:
                    if page_data["sections"]:
                        page_data["sections"][-1]["content"].append({"code": element.get_text(strip=True)})

            # Convert the page data to JSON format
            json_filename = os.path.join(json_dir, html_file.replace('.html', '.json'))
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(page_data, json_file, indent=2)
            print(f"Saved JSON: {json_filename}")
