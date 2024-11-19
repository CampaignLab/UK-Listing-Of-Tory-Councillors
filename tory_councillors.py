#!/usr/bin/python3

# CHALLENGE: Create a list of all Conservative Party Councillors in the UK, per constituency and store a created list in a JSON file.
# CODE REVISION: Ejimofor Nwoye, Campaign Lab, Newspeak House, London, England, 17th November 2024

import requests
from bs4 import BeautifulSoup
import PyPDF2
import json
import os

os.system("clear")

# Define a dictionary to store the results
councillor_data = {}

# Function to scrape the London Councils Directory
def scrape_london_councils():
    url = "https://directory.londoncouncils.gov.uk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Modify this based on website structure (Example structure assumed)
    for council in soup.select('li > a'):  # Replace with actual tags and class
        council_name = council.text.strip()
        link = council['href']
        councillor_data[council_name] = {
            "councillors": [],  # Placeholder for future councillors
            "link": link
        }

# Function to scrape A-Z of Councils Online
def scrape_az_councils():
    url = "https://www.local.gov.uk/our-support/guidance-and-resources/communications-support/digital-councils/social-media/go-further/a-z-councils-online"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Modify this based on website structure
    for council in soup.select('li > a'):  # Replace with actual tags and class
        council_name = council.text.strip()
        link = council['href']
        if council_name not in councillor_data:
            councillor_data[council_name] = {"councillors": [], "link": link}
        else:
            councillor_data[council_name]["link"] = link

# Function to parse the Parliament Register PDF
def parse_parliament_register():
    url = "https://publications.parliament.uk/pa/cm/cmsecret/240830/register.pdf"
    response = requests.get(url)
    pdf_path = "register.pdf"
    with open(pdf_path, 'wb') as file:
        file.write(response.content)

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if "Conservative" in text:  # Simple keyword search
                print(text)  # Modify to parse relevant information

    os.remove(pdf_path)  # Clean up the temporary file

# Function to scrape candidates from Democracy Club
def scrape_democracy_club():
    url = "https://candidates.democracyclub.org.uk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Modify this based on website structure
    for candidate in soup.select('tr'):  # Replace with actual tags and class
        details = [td.text.strip() for td in candidate.find_all('td')]
        if "Conservative" in details:  # Check party affiliation
            councillor_data.setdefault(details[-1], {"councillors": [], "link": None})
            councillor_data[details[-1]]["councillors"].append(details)

# Main execution
scrape_london_councils()
scrape_az_councils()
parse_parliament_register()
scrape_democracy_club()

# Save the data to a JSON file
with open("conservative_councillors.json", "w") as file:
    json.dump(councillor_data, file, indent=4)
