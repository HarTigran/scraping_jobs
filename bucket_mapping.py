import pandas as pd
from fuzzywuzzy import process


# Environmental Policy and Advocacy (1a)
environmental_policy_advocacy_keywords = [
    "Climate Policy Analysis",
    "Climate Law & Policy",
    "Green Policy & Governance",
    "Environmental Policy Analyst",
    "Environmental Organizer",
    "Climate Lawyer",
    "Sustainable Policy Advisors/Managers"
]

# Environmental Justice & Equity (1b)
environmental_justice_equity_keywords = [
    "Climate Justice Advocacy",
    "Environmental Justice & Equity",
    "Climate Justice & Indigenous Knowledge",
    "Diversity, Equity, and Inclusion Managers",
    "Community Activists"
]

# Climate Communication & Public Engagement (1c)
climate_communication_public_engagement_keywords = [
    "Climate Science Communication",
    "Green Marketing & Communication",
    "Climate Art & Communication",
    "Environmental Journalist",
    "Sustainability Marketing Manager",
    "Climate Artist"
]

# International Cooperation & Sustainable Development (1d)
international_cooperation_sustainable_dev_keywords = [
    "International Development",
    "Environmental Consulting",
    "Climate Science & Research",
    "Sustainable Development Officer",
    "Environmental Consultant",
    "Climate Scientist"
]

# Combine all keywords into a single list
bucket_1_keywords = (
    environmental_policy_advocacy_keywords +
    environmental_justice_equity_keywords +
    climate_communication_public_engagement_keywords +
    international_cooperation_sustainable_dev_keywords
)

# Climate Data Analysis Pathway (2a)
climate_data_analysis_keywords = [
    "Climate Data Analysis & Modeling",
    "Environmental Data Science",
    "Climate Data Governance & Ethics",
    "Environmental Impact Assessment",
    "Climate/Environmental Data Analyst",
    "Data Governance Specialist",
    "Environmental Compliance Specialist"
]

# Corporate Sustainability, Green Business, & Supply Chain Management Pathway (2b)
corporate_sustainability_keywords = [
    "Corporate Sustainability Management",
    "Sustainable Consumer Goods & Packaging",
    "Supply Chain Management",
    "Climate Finance",
    "Greenhouse Gas Inventory Analysis",
    "Sustainability Manager/Consultant",
    "Procurement Specialist"
]

# Climate Entrepreneurship Pathway (2c)
climate_entrepreneurship_keywords = [
    "Green Technology & Innovation",
    "Climate Entrepreneurship & Investing",
    "Green Entrepreneur",
    "Impact Investor"
]

# Combine all keywords into a single list
bucket_2_keywords = (
    climate_data_analysis_keywords +
    corporate_sustainability_keywords +
    climate_entrepreneurship_keywords
)

climate_risk_adaptation_keywords = [
    "Climate Change Adaptation Planning",
    "Environmental Finance & Risk Management",
    "Climate Resettlement & Migration",
    "Climate Adaptation Planner/Manager",
    "Climate Risk Analyst",
    "Climate Policy Advisor"
]

# Combine all keywords into a single list
bucket_3_keywords = climate_risk_adaptation_keywords

# Climate Psychology & Behavioral Change Pathway (4a)
climate_psychology_keywords = [
    "Climate Psychology & Behavioral Change",
    "Climate Psychologist",
    "Climate-Aware Therapist"
]

# Environmental Health & Safety Pathway (4b)
environmental_health_safety_keywords = [
    "Environmental Health & Safety",
    "Environmental Compliance Specialist"
]

# Combine all keywords into a single list
bucket_4_keywords = (
    climate_psychology_keywords +
    environmental_health_safety_keywords
)


# Green Infrastructure, Urban Resilience, & Green Transportation Pathway (5a)
green_infrastructure_keywords = [
    "Sustainable & Biophilic Urban Planning",
    "Green Infrastructure & Climate Resilience",
    "Green Building & Sustainable Architecture",
    "Sustainable Transportation & Mobility",
    "Urban Planner",
    "Landscape Architect",
    "LEED/Green Building Sustainability Specialist",
    "Transportation Engineer"
]

# Sustainable Tourism Pathway (5b)
sustainable_tourism_keywords = [
    "Sustainable Tourism Development & Management",
    "Sustainable Tourism Developer",
    "Sustainable Tourism Consultant",
    "Sustainable Tourism Manager"
]

# Green Chemistry & Sustainable Materials Pathway (5c)
green_chemistry_keywords = [
    "Sustainable Materials Science",
    "Sustainable Fashion & Textiles",
    "Sustainable Materials Researcher",
    "Carbon Capture and Sequestration Engineer",
    "Life Cycle Analyst/Manager",
    "Textile Recycler"
]

# Combine all keywords into a single list
bucket_5_keywords = (
    green_infrastructure_keywords +
    sustainable_tourism_keywords +
    green_chemistry_keywords
)

# Energy Pathway (6a)
energy_pathway_keywords = [
    "Renewable Energy",
    "Energy Efficiency",
    "Sustainable Waste-to-Energy Solutions",
    "Renewable Energy Engineer",
    "Renewable Energy Technician",
    "Energy Efficiency Specialist",
    "Sustainable Energy Project Manager",
    "Renewable Energy Analyst",
    "Waste-to-Energy Engineer",
    "Sustainable Energy Policy Analyst",
    "Renewable Energy Consultant"
]

# Carbon Markets; Carbon Footprint Analysis Pathway (6b)
carbon_markets_keywords = [
    "Carbon Markets & Finance",
    "Carbon Markets & Voluntary Offset Programs",
    "Carbon Footprint Analysis & Management",
    "Carbon Market Analyst",
    "Sustainability Consultant"
]

# Combine all keywords into a single list
bucket_6_keywords = (
    energy_pathway_keywords +
    carbon_markets_keywords
)

# Circular Economy, Resource Management, & Biodiversity Conservation Pathway (7a)
resource_management_keywords = [
    "Resilient Food Systems",
    "Sustainable Agriculture & Food Systems",
    "Sustainable Waste Management",
    "Water Resource Management & Sanitation",
    "Sustainable Forest Management",
    "Ecosystem Conservation",
    "Agronomist",
    "Urban Farm Manager",
    "Waste Management Specialist",
    "Water Resource Engineer",
    "Forest Manager",
    "Ecosystem Restoration Specialist"
]

# Combine all keywords into a single list
bucket_7_keywords = resource_management_keywords

environmental_education_keywords = [
    "Environmental Education & Outreach",
    "Green Jobs & Workforce Development",
    "Climate Education & Curriculum Development",
    "Environmental Outreach Coordinator",
    "Sustainability Trainer",
    "Climate Educator"
]

# Combine all keywords into a single list
bucket_8_keywords = environmental_education_keywords

buckets = {
    "Bucket #1": bucket_1_keywords,
    "Bucket #2": bucket_2_keywords,
    "Bucket #3": bucket_3_keywords,
    "Bucket #4": bucket_4_keywords,
    "Bucket #5": bucket_5_keywords,
    "Bucket #6": bucket_6_keywords,
    "Bucket #7": bucket_7_keywords,
    "Bucket #8": bucket_8_keywords,
    "Bucket #9": ["Sustainable Consumer Goods","Consumer Goods","Product Developer","Sustainability Manager","Environmental Compliance Officer", "Recycled Materials","Energy-Efficient"]
}

# Read CSV file into a pandas DataFrame
df = pd.read_csv("CLMBS_student_listings.csv")

def match_title_to_bucket(title, buckets):
    choices = [keyword for keywords in buckets.values() for keyword in keywords]
    result, score = process.extractOne(title, choices)
    for bucket, keywords in buckets.items():
        if result in keywords:
            return bucket, result, score

# Add new columns for the best-matched bucket and result
df[['Best Matched Bucket', 'Matching Result', 'Matching Score']] = df['Title'].apply(lambda x: pd.Series(match_title_to_bucket(x, buckets)))

# Save the DataFrame to a new CSV file
df.to_csv("CLMBS_student_listings_with_buckets.csv", index=False)

print("DataFrame with best-matched buckets has been saved to CLMBS_student_listings_with_buckets.csv.")