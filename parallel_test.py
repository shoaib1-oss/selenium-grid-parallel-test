from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Process

def run_test(node_url):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # optional: remove if you want to see the browser
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=node_url,
        options=chrome_options
    )

    driver.get("https://www.google.com")
    print(f"Title from {node_url}: {driver.title}")
    driver.quit()

if __name__ == "__main__":
    hub_url = "http://<public ip address>/wd/hub"  # Replace this
    p1 = Process(target=run_test, args=(hub_url,))
    p2 = Process(target=run_test, args=(hub_url,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

