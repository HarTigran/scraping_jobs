import csv
import requests
from bs4 import BeautifulSoup

url = 'https://climatebase.org/jobs?l=&q=&p=2&remote=false'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the job listings with class containing "ListCard__ContainerLink-sc"
    job_listings = soup.find_all(class_=lambda c: c and "ListCard__ContainerLink-sc" in c)

    # Define the CSV file path
    csv_file = 'job_listings.csv'

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Title', 'Company', 'Location', 'Tag', 'Link'])

        # Process each job listing
        for job in job_listings:
            # Extract the job title
            title = job.find(class_=lambda c: c and "ListCard__Title-sc" in c)
            title = title.text.strip() if title else ''

            # Extract the company name
            company = job.find(class_=lambda c: c and "ListCard__Subtitle-sc" in c)
            company = company.text.strip() if company else ''

            # Extract the location
            location = job.find(class_=lambda c: c and "MetadataInfo__MetadataInfoStyle-hif7kv-1" in str(c))
            location = location.text.strip() if location else ''

            # Extract the tag
            tag = job.find(class_=lambda c: c and "Tag__StyledTag-sc" in c)
            tag = tag.text.strip() if tag else ''

            # Extract the link
            link = 'https://climatebase.org' + job['href'] if job.has_attr('href') else ''

            # Write the data to the CSV file
            writer.writerow([title, company, location, tag, link])

    print(f'Job listings saved to {csv_file} successfully.')

else:
    print('Failed to retrieve job listings. Status code:', response.status_code)