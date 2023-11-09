import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import base64

# Define the base URL without the page parameter
base_url = 'https://climatebase.org/jobs?l=USA&q=&job_types=Internship&p={}&remote=false&utm_source=company_page'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Initialize an empty list to store job listings from all pages
all_job_listings = []

# Define the number of pages to scrape (you can set it to a large number to scrape all pages)
num_pages_to_scrape = 5

# Loop through the pages and scrape job listings
for page_num in range(1, num_pages_to_scrape + 1):
    page_url = base_url.format(page_num)
    response = requests.get(page_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Use the specific CSS selector to target job listings
        job_listings = soup.select('#jobList > a > div.ListCard__MainContent-sc-1dtq0w8-9.Huvcg.list_card__main > div.ListCard__Metadata-sc-1dtq0w8-7.kKDVMA.list_card__metadata > div:nth-child(2)')
        
        for job in job_listings:
            title = job.find_previous(class_=lambda c: c and "ListCard__Title-sc" in c)
            title = title.text.strip() if title else ''
            
            company = job.find_previous(class_=lambda c: c and "ListCard__Subtitle-sc" in c)
            company = company.text.strip() if company else ''
            
            location = job.find_previous(class_=lambda c: c and "MetadataInfo__MetadataInfoStyle-hif7kv-1" in str(c))
            location = location.text.strip() if location else ''
            
            tag = job.find_previous(class_=lambda c: c and "Tag__StyledTag-sc" in c)
            tag = tag.text.strip() if tag else ''
            
            if "Volunteer" in title:
                type = "Volunteer"
            elif "Intern" in title:
                type = "Intern"
            elif "Fellow" in title:
                type = "Fellow"
            else:
                type = "Full Time"
            
            # Extract the "X days ago" part and calculate the job posting date
            date_text = job.get_text(strip=True)
            match = re.search(r'(\d+) days? ago', date_text)
            if match:
                days_ago = int(match.group(1))
                posting_date = datetime.now() - timedelta(days=days_ago)
                posting_date_str = posting_date.strftime('%Y-%m-%d')
            else:
                posting_date_str = ''

            # Extract the picture
            picture = soup.select_one('.PageLayout__Avatar-sc-1ri9r3s-3.hIYqvL.list_card__img')

            if picture and picture.has_attr('style'):
                picture_url = re.search(r'url\((.*?)\)', picture['style']).group(1)

                # Download the image and encode it as Base64
                response_image = requests.get(picture_url)
                if response_image.status_code == 200:
                    image_data = base64.b64encode(response_image.content).decode()
                else:
                    image_data = ''
            else:
                picture_url = ''
                image_data = ''

            all_job_listings.append({
                'Title': title,
                'Company': company,
                'Location': location,
                'Tag': tag,
                'Type': type,
                'Link': '',  # You can add the link here if needed
                'Posting Date': posting_date_str,
                'Picture Base64': image_data  # Add the Base64-encoded image data to the dictionary
            })
        
    else:
        print(f'Failed to retrieve job listings for page {page_num}. Status code:', response.status_code)

# Define the CSV file path
csv_file = 'all_job_listings.csv'

# Write all job listings data to a single CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Company', 'Location', 'Tag', 'Type', 'Link', 'Posting Date', 'Picture Base64']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_job_listings)

print(f'All job listings saved to {csv_file} successfully.')