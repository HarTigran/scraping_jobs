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
    csv_file = 'job_listings_agg.csv'

    # Open the CSV file in write mode
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(['Title', 'Company', 'Location', 'Tag', 'Type', 'Link'])

        # Process each job listing
        for job in job_listings:
            # Extract the job title
            title = job.find(class_='ListCard__Title-sc').text.strip()

            # Extract the company name
            company = job.find(class_='ListCard__Subtitle-sc').text.strip()

            # Extract the location
            location = job.find(class_='MetadataInfo__MetadataInfoStyle-hif7kv-1').text.strip()

            # Extract the tag
            tag = job.find(class_='Tag__StyledTag-sc').text.strip()

            # Extract the type (full time, part time, intern)
            job_type = job.find(class_='ListCard__Time-sc').text.strip()

            # Extract the link
            link = 'https://climatebase.org' + job.find('a')['href'] if job.find('a') else ''

            # Write the data to the CSV file
            writer.writerow([title, company, location, tag, job_type, link])

    print(f'Job listings from Climatebase saved to {csv_file} successfully.')

else:
    print('Failed to retrieve job listings from Climatebase. Status code:', response.status_code)