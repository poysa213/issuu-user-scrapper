import time
import multiprocessing
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


def download_pdf(url, folder, link):
    response = requests.get(url)
    if response.status_code == 200:
        filename = link.split('/')[-1] + ".pdf"
        filepath = os.path.join(folder, filename)

        # Create the folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(filepath, 'wb') as file:
            file.write(response.content)
        # print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download PDF from: {url}")


def download_link_pdf(link, save_folder):
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--headless')

    # Initialize ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get('https://issuudownload.com/')

    input_field = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#DocumentUrl'))
    )

    input_field.clear()
    input_field.send_keys(link)

    submit_button = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn.btn-primary'))
    )
    submit_button.click()
    time.sleep(5)

    save_all_button = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.ID, 'btPdfDownload'))
    )
    save_all_button.click()
    time.sleep(5)

    download_button = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.btn.btn-outline-success'))
    )

    download_link = download_button.get_attribute('href')

    download_pdf(download_link, save_folder, link)

    driver.quit()


def download_issuu_pdfs(links, save_folder):
    print()
    print()
    print()
    print()
    print("Start downloading pdfs")

    pool = multiprocessing.Pool(processes=20)

    with tqdm(total=len(links), desc="Downloading PDFs") as pbar:
        results = []

        for link in links:
            result = pool.apply_async(download_link_pdf, args=(link, save_folder))
            results.append(result)

        for result in results:
            result.get()
            pbar.update(1)

    # Close the pool
    pool.close()
    pool.join()
    print("Finish downloading all the documents required")


def scrap_document_links(profile_url, save_folder):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(profile_url)

    time.sleep(5)

    allow_all_cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))
    )
    if allow_all_cookies_button:
        allow_all_cookies_button.click()
        time.sleep(2)

    publication_links = []

    print("Begin scraping...")
    start_time = time.time()  # Record start time
    page_number = 1
    while True:
        print("=========================================================================")
        print("Scraping page number: " + str(page_number))

        publication_cards = driver.find_elements(By.CSS_SELECTOR, 'a[class*="PublicationCard__publication-card__card-link"]')

        for card in publication_cards:
            href = card.get_attribute('href')
            publication_links.append(href)
        print("Current number of files to download is: " + str(len(publication_links)))

        next_button = driver.find_elements(By.XPATH, f'//a[contains(@aria-label, "Page {page_number + 1}")]')

        if next_button:
            # move to next page
            next_button[0].click()
            page_number += 1
            time.sleep(5)
        else:
            print("Next link is disabled. End of pages.")
            break
      

    end_time = time.time()  # Record end time
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time} seconds.")

    driver.quit()
    print("The Total number of links is: " + str(len(publication_links)))
    print("============================================================================")
    download_issuu_pdfs(publication_links, save_folder)


if __name__ == '__main__':
    profile_url = input("Please enter the profile URL: ")
    save_folder = input("Please enter the path to the save folder: ")
    scrap_document_links(profile_url, save_folder)
