import requests
from lxml import html

def scrape_climatebase_jobs(url):
    print(response)
    tree = html.fromstring(response.content)
    print(tree)

    # Extract job information from the parsed HTML
    job_elements = tree.xpath('//div[@class="list_card__info"]')
    print(job_elements)

    jobs = []
    for job_element in job_elements:
        job_title = job_element.xpath('.//a[@class="list_card__title"]/text()')[0].strip()
        company = job_element.xpath('.//div[@class="list_card__subtitle"]/text()')[0].strip()
        location = job_element.xpath('.//div[@class="list_card__location"]/text()')[0].strip()

        job_data = {'job_title': job_title, 'company': company, 'location': location}
        jobs.append(job_data)

    return jobs

# Example usage
job_url = 'https://climatebase.org/jobs?l=&q=&p=0&remote=false'
climatebase_jobs = scrape_climatebase_jobs(job_url)

for job in climatebase_jobs:
    print(job)