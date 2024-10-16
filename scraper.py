from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv
import re

# Path to ChromeDriver executable
chrome_driver_path = r"C:\Users\samee\Downloads\chromedriver-win64\chromedriver.exe"

# Create a Service object using the specified path
service = Service(chrome_driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

# List to store job data
job_data_list = []

# Global job ID counter
global_job_id = 1

# Function to extract text for an element
def get_text(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        text = element.text.strip()
        return text
    except:
        return "NA"

# Function to get HTML content for an element
def get_html(xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        html = element.get_attribute('innerHTML')  # Get raw HTML
        return html
    except:
        return "NA"

# Function to clean and extract reviews from company name
def extract_company_and_reviews(company_text):
    reviews = "NA"
    match = re.search(r'(\d+\.\d+)\s*Reviews', company_text)
    if match:
        reviews = match.group(1)
        company_text = company_text.replace(match.group(0), "").strip()
    return company_text, reviews

# Function to clean key skills using BeautifulSoup
def clean_key_skills(key_skills_html):
    try:
        soup = BeautifulSoup(key_skills_html, 'html.parser')
        spans = soup.find_all('span')
        skills_list = [span.get_text(strip=True) for span in spans]
        formatted_skills = ', '.join(skills_list)
        return formatted_skills
    except Exception as e:
        print(f"Error cleaning key skills: {e}")
        return "NA"

# Function to clean education text
def clean_education(education_text):
    cleaned_education = education_text.replace("Education", "").strip()
    return cleaned_education

# Function to extract job details and store in job_data_list
def extract_job_details(job_element):
    global global_job_id
    try:
        job_url = job_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.execute_script("window.open(arguments[0], '_blank');", job_url)
        driver.switch_to.window(driver.window_handles[-1])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'styles_job-header-container___0wLZ')))

        job_title_text = get_text("//h1[contains(@class, 'styles_jd-header-title__rZwM1')]")
        company_text_raw = get_text("//div[contains(@class, 'styles_jd-header-comp-name__MvqAI')]")
        company_text, reviews_text = extract_company_and_reviews(company_text_raw)
        location_text = get_text("//div[contains(@class, 'styles_jhc__loc___Du2H')]")
        experience_text = get_text("//div[contains(@class, 'styles_jhc__exp__k_giM')]")
        salary_text = get_text("//div[contains(@class, 'styles_jhc__salary__jdfEC')]")

        job_details_parent_xpath = "//div[contains(@class, 'styles_jhc__jd-stats__KrId0')]"
        posted_on_text = get_text(f"{job_details_parent_xpath}//span[normalize-space(label)='Posted:']/span")
        openings_text = get_text(f"{job_details_parent_xpath}//span[normalize-space(label)='Openings:']/span")
        applications_text = get_text(f"{job_details_parent_xpath}//span[normalize-space(label)='Applicants:']/span")

        other_details_parent_xpath = "//div[contains(@class, 'styles_other-details__oEN4O')]"
        role_text = get_text(f"{other_details_parent_xpath}//div[contains(label, 'Role:')]/span")
        industry_type_text = get_text(f"{other_details_parent_xpath}//div[contains(label, 'Industry Type:')]/span")
        department_text = get_text(f"{other_details_parent_xpath}//div[contains(label, 'Department:')]/span")
        employment_type_text = get_text(f"{other_details_parent_xpath}//div[contains(label, 'Employment Type:')]/span")
        role_category_text = get_text(f"{other_details_parent_xpath}//div[contains(label, 'Role Category:')]/span")

        education_text_raw = get_text("//div[contains(@class, 'styles_education__KXFkO')]")
        education_text = clean_education(education_text_raw)

        key_skills_html = get_html("//div[contains(@class, 'styles_key-skill__GIPn_')]")
        key_skills_text = clean_key_skills(key_skills_html)

        job_desc_text = get_text("//div[contains(@class, 'styles_JDC__dang-inner-html__h0K4t')]")

        job_data_list.append({
            "Job ID": global_job_id,
            "Job Title": job_title_text,
            "Company": company_text,
            "Reviews": reviews_text,
            "Location": location_text,
            "Experience": experience_text,
            "Salary": salary_text,
            "Posted On": posted_on_text,
            "Openings": openings_text,
            "Applications": applications_text,
            "Job Description": job_desc_text,
            "Role": role_text,
            "Industry Type": industry_type_text,
            "Department": department_text,
            "Employment Type": employment_type_text,
            "Role Category": role_category_text,
            "Education": education_text,
            "Key Skills": key_skills_text
        })

        global_job_id += 1
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as e:
        print(f"Error processing job {global_job_id}: {e}")
        if len(driver.window_handles) > 1:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

# Function to scrape jobs from a given URL and collect jobs until the required count is reached
def scrape_jobs_from_category(url, job_count):
    page_number = 1
    total_jobs_collected = 0

    while total_jobs_collected < job_count:
        print(f"Scraping page {page_number}...")

        # Format URL to include page number
        if page_number == 1:
            current_url = url
        else:
            current_url = f"{url.rstrip('-')}-{page_number}"

        driver.get(current_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "srp-jobtuple-wrapper")))

        job_list = driver.find_elements(By.CLASS_NAME, "srp-jobtuple-wrapper")
        if not job_list:
            print("No more jobs found or page not loaded correctly.")
            break

        for i in range(len(job_list)):
            if total_jobs_collected >= job_count:
                break
            try:
                job_element = job_list[i]
                extract_job_details(job_element)
                total_jobs_collected += 1
                time.sleep(2)
            except Exception as e:
                print(f"Error processing job element {total_jobs_collected + 1}: {e}")

        if total_jobs_collected < job_count:
            # Increment page number
            page_number += 1
            time.sleep(3)  # Wait for the next page to load


# Define job categories and URLs
job_categories = {
    "Data Scientist": "https://www.naukri.com/data-scientist-jobs",
    "Data Analyst": "https://www.naukri.com/data-analyst-jobs",
    "DevOps": "https://www.naukri.com/devops-jobs",
    "Full Stack": "https://www.naukri.com/full-stack-developer-jobs",
    "Python Developer": "https://www.naukri.com/python-developer-jobs"
}

# Scrape jobs from each category
for category, url in job_categories.items():
    print(f"Scraping {category} jobs...")
    scrape_jobs_from_category(url, 150)
    print(f"Finished scraping {category} jobs.")

# Save the job data to a CSV file
with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        "Job ID", "Job Title", "Company", "Reviews", "Location", "Experience", "Salary",
        "Posted On", "Openings", "Applications", "Job Description", "Role",
        "Industry Type", "Department", "Employment Type", "Role Category",
        "Education", "Key Skills"
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for job_data in job_data_list:
        writer.writerow(job_data)

# Close the driver
driver.quit()
