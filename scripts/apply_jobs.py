import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_driver import init_driver

def load_credentials():
    with open('data/credentials.json', 'r') as file:
        return json.load(file)

def load_job_criteria():
    with open('data/job_criteria.json', 'r') as file:
        return json.load(file)

def login(driver, username, password):
    driver.get('https://www.linkedin.com/login')
    email_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')

    email_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

def search_jobs(driver, criteria):
    driver.get('https://www.linkedin.com/jobs/')
    search_bar = driver.find_element(By.CSS_SELECTOR, 'input.jobs-search-box__text-input')
    
    for keyword in criteria['keywords']:
        search_bar.clear()
        search_bar.send_keys(keyword)
        search_bar.send_keys(Keys.RETURN)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search-results'))
        )

def apply_to_jobs(driver):
    job_cards = driver.find_elements(By.CLASS_NAME, 'job-card-container')
    for job_card in job_cards[:5]:  # Applying to top 5 jobs for demo purposes
        job_card.click()
        apply_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'jobs-apply-button'))
        )
        apply_button.click()

def main():
    credentials = load_credentials()
    job_criteria = load_job_criteria()
    driver = init_driver()

    try:
        login(driver, credentials['username'], credentials['password'])
        search_jobs(driver, job_criteria)
        apply_to_jobs(driver)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
