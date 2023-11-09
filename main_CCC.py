from requests_html import HTMLSession

url = "https://www.terra.do/climate-jobs/job-board/"

# Create an HTML session
session = HTMLSession()
r = session.get(url)

# Ensure JavaScript is rendered
r.html.render(sleep=2)  # Adjust the sleep time as needed

# Extract job links
job_links = r.html.find('.job-link')

for link in job_links:
    job_url = link.attrs['href']
    print("Job Link:", job_url)

# Close the session
session.close()