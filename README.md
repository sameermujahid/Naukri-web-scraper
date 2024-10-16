
# Job Scraper

## What is this?

This Job Scraper is a Python-based web scraping tool that extracts job listings from various job categories on the Naukri.com website. The scraper gathers detailed job information, including job title, company, location, salary, key skills, and more, and saves the collected data in a CSV format for further analysis or use.

## Features

- **Customizable Job Categories**: Scrapes job details from various categories, allowing you to add or modify categories as needed (e.g., Data Scientist, Data Analyst, DevOps, Full Stack, Python Developer).

- **Flexible Data Fields**: Customize the specific data fields you want to scrape, ensuring you only collect information relevant to your needs.

- **CSV Export**: Saves the scraped data into a CSV file, making it easy to access, analyze, and integrate with other tools.


## Installation

To set up this project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sameermujahid/Naukari-web-scraper.git
   cd Naukari-web-scraper
   ```

2. **Install required packages**:
   Make sure you have Python installed on your machine. Then, install the necessary packages using pip:
   ```bash
   pip install selenium beautifulsoup4
   ```

3. **Download ChromeDriver**:
   - Ensure you have the Chrome browser installed.
   - Download the ChromeDriver that matches your browser version from [ChromeDriver Download](https://googlechromelabs.github.io/chrome-for-testing/).
   - Place the downloaded `chromedriver.exe` file in a suitable directory, e.g., `C:\Downloads\chromedriver-win64\`.

4. **Update the script**:
   - Open the scraper code in your preferred text editor.
   - Update the `chrome_driver_path` variable in the script to point to the location of your `chromedriver.exe` file.

## How to Run the Scraper

To run the job scraper, execute the following command in your terminal:

```bash
python scraper.py
```
## Modifying Job Categories and Data Columns

You can easily customize the job categories and the specific data fields you want to scrape by modifying the code.

### To change job categories:
1. Locate the `job_categories` dictionary in the script.
2. Add or modify categories and their corresponding URLs as needed:
   ```python
   job_categories = {
       "New Category": "https://www.naukri.com/new-category-jobs",
       ...
   }
   ```

### To change the columns in the dataset:
1. Locate the `fieldnames` list in the script where the CSV header is defined.
2. Add or remove fields from this list to match the data you want to collect:
   ```python
   fieldnames = [
       "Job ID", "Job Title", "Company", "Reviews", ...
       # Add or remove fields as needed
   ]
   ```
### To customize the number of jobs:
Adjust the number of jobs you want to scrape by modifying the function call in the script:
 ```python
scrape_jobs_from_category(url, 150)  # Replace 150 with your desired number of jobs
```
## Acknowledgements

- Thanks to the developers of [Selenium](https://www.selenium.dev/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for their excellent libraries that make web scraping easier.
```
