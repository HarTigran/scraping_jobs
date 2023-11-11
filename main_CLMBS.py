import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


# Define the base URL without the page parameter
base_url = 'https://climatebase.org/jobs?l=USA&q=&experience_levels=Current+student+%28or+less+than+1+year%29&p=0&remote=false'

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
        job_listings = soup.find_all(class_=lambda c: c and "ListCard__ContainerLink-sc" in c)
        
        for job in job_listings:
            title = job.find(class_=lambda c: c and "ListCard__Title-sc" in c)
            title = title.text.strip() if title else ''
            
            company = job.find(class_=lambda c: c and "ListCard__Subtitle-sc" in c)
            company = company.text.strip() if company else ''
            
            location = job.find(class_=lambda c: c and "MetadataInfo__MetadataInfoStyle-hif7kv-1" in str(c))
            location = location.text.strip() if location else ''
            
            tag = job.find(class_=lambda c: c and "Tag__StyledTag-sc" in c)
            tag = tag.text.strip() if tag else ''
            
            if "Volunteer" in title:
                type = "Volunteer"
            elif "Intern" in title:
                type = "Intern"
            elif "Fellow" in title:
                type = "Fellow"
            else:
                type = "Full Time"
            
            link = 'https://climatebase.org' + job['href'] if job.has_attr('href') else ''
            
            # Extract the "X days ago" part and calculate the job posting date
            date_text = job.get_text(strip=True)
            match = re.search(r'(\d+) days? ago', date_text)
            if match:
                days_ago = int(match.group(1))
                posting_date = datetime.now() - timedelta(days=days_ago+1)
                posting_date_str = posting_date.strftime('%Y-%m-%d')
            else:
                match = re.search(r'(\d+) hours ago', date_text)
                if match:
                    hours_ago = int(match.group(1))
                    posting_date = datetime.now() - timedelta(hours=hours_ago)
                    posting_date_str = posting_date.strftime('%Y-%m-%d')
                else:
                    posting_date_str = ''
            
            # Extract the job description and compensation information from the job details page
            job_response = requests.get(link, headers=headers)
            if job_response.status_code == 200:
                # job_soup = BeautifulSoup(job_response.content, 'html.parser')
                # compensation_info = job_soup.find('div', class_='JobListing__DescriptionContainer-sc-15uyy2k-0')
                # compensation_text = compensation_info.get_text() if compensation_info else ''
                
                # pattern = r'(Base Pay:|Pay Range:|salary range for this position is)\s*(\$?[\d,]+(?:\.\d{2})?)\s*(?:-|to)\s*(\$?[\d,]+(?:\.\d{2})?)'

                # # Search for the pay range pattern in the text
                # pay_range_match = re.search(pattern, compensation_text)

                # if pay_range_match:
                #     header = pay_range_match.group(1).strip()
                #     start_range = pay_range_match.group(2).strip()
                #     end_range = pay_range_match.group(3).strip()
                #     pay_range = (header, start_range, end_range)
                # else:
                #     pay_range = ('', '', '')

                # # Extract job summary using a more specific pattern
                # job_summary_text = compensation_text


                all_job_listings.append({
                    'Title': title,
                    'Company': company,
                    'Location': location,
                    'Tag': tag,
                    'Type': type,
                    'Link': link,
                    'Posting Date': posting_date_str,
                    # 'Job Summary': job_summary_text,
                    # 'Compensation': pay_range
                })
            else:
                print(f'Failed to retrieve details for job: {title}. Status code:', job_response.status_code)
        
    else:
        print(f'Failed to retrieve job listings for page {page_num}. Status code:', response.status_code)

# Define the CSV file path
csv_file = 'CLMBS_student_listings.csv'

# Write all job listings data to a single CSV file
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['Title', 'Company', 'Location', 'Tag', 'Type', 'Link', 'Posting Date']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_job_listings)

print(f'All job listings saved to {csv_file} successfully.')