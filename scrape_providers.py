'''
Script Name: scrape_providers.py

Description:
This script is designed to scrape provider data (specifically cancer doctors) from hospital websites such as MD Anderson, Mayo Clinic, Stanford, and others. 
The goal is to gather key information about cancer specialists to build a database that can be integrated into the DrBot.Health platform for use in the AI-powered doctor recommendation system.

Functionality:
- Connects to hospital websites, navigates to the relevant sections (e.g., oncology departments, doctor directories).
- Extracts data such as doctor names, specialties, contact information, and other relevant details.
- Cleans and formats the data for storage in a database.
- Integrates the scraped data into the existing project database for use in the recommendation system.

Usage:
- Run this script independently to update or refresh the cancer doctor database.
- The data will be stored in the project’s main database, which is connected to the web app and dashboard.

Dependencies:
- BeautifulSoup (for parsing HTML)
- Requests (for sending HTTP requests)
- pandas (for data manipulation)
- SQLAlchemy (for database interaction)
'''

import requests
from bs4 import BeautifulSoup
import csv
import time
import os

# Base URL for scraping
base_url = "https://faculty.mdanderson.org/search-results.html?searchType=faculty&page={}"
profile_base_url = "https://faculty.mdanderson.org"

# CSV file to save data
output_file = "md_anderson_doctors.csv"

# Function to scrape a single page
def scrape_page(page_number):
    url = base_url.format(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    doctors = soup.find_all('div', class_='faculty-result')
    doctor_list = []
    
    for doctor in doctors:
        try:
            # Extract the name and profile link
            name = doctor.find('div', class_='search-result-subtitle').get_text(strip=True)
            profile_link = profile_base_url + doctor.find('a')['href']  # Prepend base URL
            
            # Extract the title (e.g., Professor, Department of XYZ, Division)
            title_info = doctor.find('p').get_text(strip=True)
            title_split = title_info.split(",")
            
            title = title_split[0].strip() if len(title_split) > 0 else "N/A"
            department = title_split[1].strip() if len(title_split) > 1 else "N/A"
            division = title_split[2].strip() if len(title_split) > 2 else "N/A"
        
        except Exception as e:
            print(f"Error processing doctor data on page {page_number}: {e}")
            continue
        
        doctor_list.append([name, title, department, division, profile_link])
    
    return doctor_list

def save_to_csv(data, file_name, mode='w'):
    with open(file_name, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':  # Write header only for the first time
            writer.writerow(['Name', 'Title', 'Department', 'Division', 'Profile Link'])
        writer.writerows(data)
    print(f"Data saved to {os.path.abspath(file_name)}")


# Main scraping function
def scrape_all_pages():
    all_doctors = []
    total_pages = 5  # Update this based on the number of pages on the website
    
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        doctors_on_page = scrape_page(page)
        if doctors_on_page:
            save_to_csv(doctors_on_page, output_file, mode='a')  # Append to CSV
        time.sleep(2)  # Add a delay to avoid overloading the server
    
    print(f"Scraping complete. Data saved to {output_file}")

# Run the scraping
scrape_all_pages()
