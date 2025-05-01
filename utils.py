import requests
from bs4 import BeautifulSoup
from summarizer import summarize_and_classify, get_embedding

def get_page_content(url, use_selenium=False):
    if use_selenium:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from webdriver_manager.chrome import ChromeDriverManager

        options = Options()
        options.headless = True
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            page_source = driver.page_source
        except Exception as e:
            print(f"Error loading page with Selenium: {e}")
            page_source = None
        driver.quit()
        return page_source
    else:
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to retrieve: {url}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None


def summarize_content_from_html(content):
    try:
        if not content:
            return "Summary failed", "Unknown", []
        summary, page_type = summarize_and_classify(content)
        embedding = get_embedding(summary)
        return summary, page_type, embedding
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Summary failed", "Unknown", []


def capture_screenshot(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import tempfile
    import time

    options = Options()
    options.headless = True
    options.add_argument('--window-size=1280,1024')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)  

    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        screenshot_path = tmp_file.name
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path
