import scrapy

class JobPostSpiderSpider(scrapy.Spider):
    name = "job_post_spider"

    # Add a list of allowed domains
    allowed_domains = ["climatebase.org", "climatechangejobs.com", "sustainablebusiness.com", "environmentalcareer.com", "conservationjobboard.com", "idealist.org", "netimpact.org"]

    # Specify start URLs for each domain
    start_urls = [
        ("climatebase.org", ["https://climatebase.org/jobs?l=&q=&p={}&remote=false".format(i) for i in range(9)]),
        ("climatechangejobs.com", ["https://climatechangejobs.com/jobs?page={}".format(i) for i in range(1,65)]),
        ("sustainablebusiness.com", ["https://www.sustainablebusiness.com/greendreamjobs/page/{}/".format(i) for i in range(1, 18)]),
        ("environmentalcareer.com", ["https://environmentalcareer.com/jobs/?&p={}".format(i) for i in range(1, 18)]),
        ("conservationjobboard.com", ["https://www.conservationjobboard.com/{}".format(i) for i in range(1, 8)]),
        # ("idealist.org", ["https://www.idealist.org/en/jobs?page={}&q=".format(i) for i in range(1, 14)]),
        # "netimpact.org": ["https://netimpact.org/jobs?page={}".format(i) for i in range(0, 4)],
    ]

    def start_requests(self):
        for domain, urls in self.start_urls:
            for url in urls:
                yield scrapy.Request(url, callback=self.parse, meta={'domain': domain})

    def parse(self, response):
        # Determine the domain of the current response
        current_domain = response.meta['domain']

        # Call the corresponding parsing method based on the domain
        if current_domain == "climatebase.org":
            yield from self.parse_climatebase(response)
        elif current_domain == "climatechangejobs.com":
            yield from self.parse_climatechangejobs(response)
        elif current_domain == "sustainablebusiness.com":
            yield from self.parse_sustainablebusiness(response)
        elif current_domain == "environmentalcareer.com":
            yield from self.parse_environmentalcareer(response)
        elif current_domain == "conservationjobboard.com":
            yield from self.parse_conservationjobboard(response)
        # elif current_domain == "idealist.org":
        #     yield from self.parse_idealist(response)
        # elif current_domain == "netimpact.org":
        #     yield from self.parse_netimpact(response)

    def parse_climatebase(self, response):
        # Add parsing logic for climatebase.org
        job_elements = response.css(".comp")
        for job_element in job_elements:
            company_name = job_element.css('.list_card__subtitle::text').extract_first().strip()
            location_list = [text.strip() for text in job_element.css('.list_card__metadata-item[type="location"]::text').extract() if text.strip()]
            href = job_element.css('a::attr(href)').extract_first().strip()
            # Extract job title using the provided selector
            job_title = job_element.css('.ListCard__TitleWrapper-sc-1dtq0w8-2 > div:nth-child(2) > div::text').extract_first().strip()
            # Extract posting date
            posting_date = job_element.css('.list_card__metadata-item[type="calendar"]').xpath('string()').extract_first().strip()
            yield {
                'domain': "climatebase.org",
                'company_name': company_name,
                'location': location_list[0],
                'job_title': job_title,
                'posting_date': posting_date,
                'href': response.urljoin(href),
            }

    def parse_climatechangejobs(self, response):
        # Initialize a set to keep track of processed job titles
        processed_job_postings = set()
        # Extract job elements
        job_elements = response.css('.job-listings-item')

        for job_element in job_elements:
            # Extract information from the job element using provided selectors
            link = job_element.css('div.job-main-info > div > div.job-details-group > div.job-details > span > a::attr(href)').extract_first()
            company_name = job_element.css('div.job-main-info > div > div.job-details-group > div.job-details > span > div > span > span:nth-child(1) > a::text').extract_first().strip()
            location = job_element.css('div.job-main-info > div > div.job-details-group > div.job-details > span > div > span > span:nth-child(3) > a::text').get()

            if location is None:
                location = job_element.css('div.job-main-info > div > div.job-details-group > div.job-details > span > div > span > span:nth-child(2) > a::text').get()
                if location is None:
                    location = job_element.css('div.job-listings-item:nth-child(13) span.job-details-content div.job-details-info-item::text').get()
            
            if location:
                if location in ["Full-time","Part-time", "Temporary","Contract" "Internship"]:
                    location = 'Remote'
                location = location.strip()
            else:
                location = "Multiple Locations"
            job_title = job_element.css('div.job-main-info > div > div.job-details-group > div.job-details > span > a > h3::text').extract_first().strip()
            #  Extract posting date
            posting_date_elements = job_element.css('div.job-posted-date::text').extract()
            posting_date = ' '.join(element.strip() for element in posting_date_elements)
            # Check if the job details have been processed before
            if link not in processed_job_postings:
                processed_job_postings.add(link)

            yield {
                'domain': "climatechangejobs.com",
                'company_name': company_name,
                'location': location,
                'job_title': job_title,
                'posting_date': posting_date,
                'href': response.urljoin(link) if link else None,
            }

    def parse_sustainablebusiness(self, response):
        # Add parsing logic for sustainablebusiness.com
        main_page_selector = '#post-25 > div > div.wpjb.wpjb-page-index'
        job_elements = response.css(f'{main_page_selector} div.wpjb-grid-row.wpjb-click-area')

        for job_element in job_elements:
            # Extract job title
            job_title = job_element.css('div.wpjb-col-title span.wpjb-line-major a::text').extract_first().strip()

            # Extract company name
            company_name = job_element.css('div.wpjb-col-title span.wpjb-sub.wpjb-sub-small::text').extract_first().strip()

            # Extract location
            location = job_element.css('div.wpjb-col-location span.wpjb-line-major span::text').extract_first().strip()

            # Extract link
            href = job_element.css('div.wpjb-col-title span.wpjb-line-major a::attr(href)').extract_first().strip()

            # Extract posting date
            posting_date = job_element.css('div.wpjb-grid-col-right span.wpjb-line-major::text').extract_first().strip()

            yield {
                'domain': "sustainablebusiness.com",
                'company_name': company_name,
                'location': location,
                'job_title': job_title,
                'posting_date': posting_date,
                'href': response.urljoin(href),
            }


    def parse_environmentalcareer(self, response):
        # Add parsing logic for environmentalcareer.com
        main_page_selector = '.search-results > div:nth-child(2)'
        job_elements = response.css(f'{main_page_selector} article.media')

        for job_element in job_elements:
            # Extract job title
            job_title = job_element.css('div:nth-child(2) > div:nth-child(2) > a:nth-child(1)::text').extract_first().strip()

            # Extract company name
            company_name = job_element.css('div:nth-child(2) > div:nth-child(3) > span:nth-child(1)::text').extract_first().strip()

            # Extract location
            location = job_element.css('div:nth-child(2) > div:nth-child(3) > span:nth-child(2)::text').extract_first()
            location = location.strip() if location else "None"

            # Extract link
            href = job_element.css('div:nth-child(2) > div:nth-child(2) > a:nth-child(1)::attr(href)').extract_first().strip()

            # Extract posting date
            posting_date = job_element.css('div:nth-child(2) > div:nth-child(1) > div:nth-child(2)::text').extract_first().strip()

            yield {
                'domain': "environmentalcareer.com",
                'company_name': company_name,
                'location': location,
                'job_title': job_title,
                'posting_date': posting_date,
                'href': response.urljoin(href),
            }


    def parse_conservationjobboard(self, response):
        # Add parsing logic for conservationjobboard.com
        job_elements = response.css('.listing__jobs div:nth-child(1) article')

        for job_element in job_elements:
            # Extract job title
            job_title = job_element.css('header h2 a::text').extract_first().strip()

            # Extract company name
            company_name = job_element.css('h3::text').extract_first().strip()

            # Extract location
            location = job_element.css('h4::text').extract_first().strip()

            # Extract link
            href = job_element.css('header h2 a::attr(href)').extract_first().strip()

            # Extract posting date more robustly
            posting_date = job_element.css('footer.listing__job__footer div::text').extract()[-1]
            # posting_date = posting_date.strip() if posting_date else None

            yield {
                'domain': "conservationjobboard.com",
                'company_name': company_name,
                'location': location,
                'job_title': job_title,
                'posting_date': posting_date,
                'href': response.urljoin(href),
            }


    def parse_idealist(self, response):
        # Add parsing logic for idealist.org
        job_elements = response.css('.sc-10hay43-1')

        for job_element in job_elements:
            # Extract job title
            job_title = job_element.css('div:nth-child(2) h3 a::text').extract_first().strip()

            # Extract company name
            company_name = job_element.css('div:nth-child(2) h4::text').extract_first().strip()

            # Extract location
            location = job_element.css('div:nth-child(2) div:nth-child(3) div:nth-child(1) div:nth-child(1)::text').extract_first().strip()

            # Extract link
            href = job_element.css('div:nth-child(2) h3 a::attr(href)').extract_first().strip()

            # Extract posting date
            posting_date = job_element.css('div:nth-child(2) div:nth-child(4)::text').extract_first().strip()

            yield {
                'domain': "idealist.org",
                'company_name': company_name,
                'location': location,
                'job_title': job_title,
                'posting_date': posting_date,
                'href': response.urljoin(href),
            }
    
    def parse_netimpact(self, response):
        # Add parsing logic for netimpact.org
        pass  # Modify this method as needed
    
    def closed(self, reason):
        self.save_to_csv()

    def save_to_csv(self):
        import csv

        items = self.crawler.stats.get_value('items')
        if items:
            filename = f'climatechangejobs_data_{len(items)}.csv'
            fields = ['domain', 'company_name', 'location', 'job_title', 'posting_date', 'href']

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()

                for item in items:
                    writer.writerow(item)