// Define jobCards at the global level
let jobCards = [];
let bucketFilter;
let typeFilter;

// Function to populate job cards
function populateJobCards(jobListings) {
    const jobCardsContainer = document.querySelector('.job-cards-container');
    jobCardsContainer.innerHTML = ''; // Clear existing job cards
    jobCards = []; // Clear existing jobCards array

    jobListings.forEach((job) => {
        const jobCard = document.createElement('div');
        jobCard.classList.add('job-card');

        jobCard.innerHTML = `
        <div class="job-content">
            <div class="logo-section">
                <img src="/static/Logo.png" alt="Company Logo" class="company-logo">
            </div>
            <div class="text-section">
                <h2>${job.Title}</h2>
                <div class="job-card-description">
                    <p>Company: ${job.Company}</p>
                    <p>Location: ${job.Location}</p>
                    <p>Tag: ${job.Tag}</p>
                    <p>Type: ${job.Type}</p>
                </div>
                    <div class="job-card-actions">
                    <a href="${job.Link}" target="_blank">Apply</a>
                    <a href="#" class="save-job-button">Add to My Job List</a> <!-- Add the "Save" button -->
                </div>
            </div>
        </div>
        `;
        jobCards.push(jobCard); // Add the job card to the jobCards array
        jobCardsContainer.appendChild(jobCard);
    });
}
// Function to extract unique values from job cards
function getUniqueValues(cards, bucketSelector, typeSelector) {
    const bucketValues = new Set();
    const typeValues = new Set();

    cards.forEach(card => {
        const bucketElement = card.querySelector(bucketSelector);
        const typeElement = card.querySelector(typeSelector);

        if (bucketElement) {
            bucketValues.add(bucketElement.textContent.trim());
        }
        if (typeElement) {
            typeValues.add(typeElement.textContent.trim());
        }
    });

    return {
        bucket: Array.from(bucketValues),
        type: Array.from(typeValues),
    };
}

// Function to populate select element options
function populateSelectOptions(selectElement, options) {
    selectElement.innerHTML = ''; // Clear existing options
    const defaultOption = document.createElement('option');
    defaultOption.text = '_________';
    defaultOption.value = 'all';
    selectElement.appendChild(defaultOption);

    options.forEach(option => {
        const optionElement = document.createElement('option');
        optionElement.text = option.split(': ')[1]; // Extract the "Value" part
        optionElement.value = option.split(': ')[1]; // Set the value attribute to "Value"
        selectElement.appendChild(optionElement);
    });
}
// Function to filter job cards based on user selections
function filterJobCards() {
    const selectedBucket = bucketFilter.value;
    const selectedType = typeFilter.value;

    jobCards.forEach(jobCard => {
        const jobDescription = jobCard.querySelector('.job-card-description');
        const cardBucket = jobDescription.querySelector('p:nth-child(3)').textContent.split(': ')[1];
        const cardType = jobDescription.querySelector('p:nth-child(4)').textContent.split(': ')[1];

        if (
            (selectedBucket === 'all' || selectedBucket === cardBucket) &&
            (selectedType === 'all' || selectedType === cardType)
        ) {
            jobCard.style.display = 'block';
        } else {
            jobCard.style.display = 'none';
        }
    });
}
document.addEventListener('DOMContentLoaded', () => {
    populateJobCards(jobListings);
    const saveButtons = document.querySelectorAll('.save-job-button');

    saveButtons.forEach(button => {
        button.addEventListener('click', async event => {
            event.preventDefault();
            const jobCard = event.target.closest('.job-card');
            const jobTitleElement = jobCard.querySelector('h2');
            const jobTitle = jobTitleElement.textContent;
            const jobDescription = jobCard.querySelector('.job-card-description');    
            const jobDetails = {
                title: jobTitle,
                company: jobDescription.querySelector('p:nth-child(1)').textContent.split(': ')[1],
                location: jobDescription.querySelector('p:nth-child(2)').textContent.split(': ')[1],
                tag: jobDescription.querySelector('p:nth-child(3)').textContent.split(': ')[1],
                job_type: jobDescription.querySelector('p:nth-child(4)').textContent.split(': ')[1],
                link: jobCard.querySelector('.job-card-actions a[target="_blank"]').href,
            };
            
            try {
                const response = await fetch('/job_list', {
                    method: 'POST',
                    body: new URLSearchParams(jobDetails),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                });

                const data = await response.json();

                if (data.success) {
                    console.log('Job saved successfully!');
                    console.log('Saved Job Details:', data);
                } else {
                    alert('Failed to save job.');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });
    bucketFilter = document.getElementById('bucket-filter');
    typeFilter = document.getElementById('type-filter');

    // Adjust the selectors to match your HTML structure
    const { bucket, type } = getUniqueValues(jobCards, '.job-card-description p:nth-child(3)', '.job-card-description p:nth-child(4)');

    populateSelectOptions(bucketFilter, bucket);
    populateSelectOptions(typeFilter, type);

    // Attach event listeners to the filter select elements
    bucketFilter.addEventListener('change', filterJobCards);
    typeFilter.addEventListener('change', filterJobCards);
});