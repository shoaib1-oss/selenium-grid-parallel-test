# Selenium Grid Parallel Test

This project demonstrates how to set up a Selenium Grid using Docker and run Selenium tests in parallel across multiple nodes.

---

## 🔧 Project Overview

* **Objective**: Set up a Selenium Grid with Docker containers and run parallel browser tests.
* **Environment**: Ubuntu Linux VM (e.g., AWS EC2), Docker, Selenium, Python
* **Test Case**: Open Google in parallel on two Chrome nodes

---

## 📁 Folder Structure

```
project-root/
├── Docker setup
├── parallel_test.py
├── README.md
├── .gitignore
└── (optional virtual environment folders)
```

---

## 🐳 Selenium Grid Setup (Using Docker)

1. **Install Docker**:

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

2. **Set up the Hub**:

```bash
docker run -d -p 4444:4444 --name selenium-hub selenium/hub
```

3. **Add Two Chrome Nodes**:

```bash
docker run -d --name chrome1 --link selenium-hub:hub selenium/node-chrome

docker run -d --name chrome2 --link selenium-hub:hub selenium/node-chrome
```

4. **Verify Grid is Running**:
   Open your browser and go to: `http://<your-public-ip>:4444`

---

## 🧪 Parallel Test Script (Python)

**parallel\_test.py**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Process
import time

def run_test(grid_url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )
    driver.get("https://www.google.com")
    print("Title from", grid_url, ":", driver.title)
    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    grid_url = "http://<your-public-ip>:4444/wd/hub"
    processes = []
    for _ in range(2):
        p = Process(target=run_test, args=(grid_url,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
```

---

## 📄 .gitignore

```
venv/
__pycache__/
*.pyc
.env
selenium-env/
```

---

## 💡 Notes

* Ensure ports are open on your VM (port 4444 for Selenium Grid UI).
* Use SSH key-based authentication for GitHub (not password).
* Update `<your-public-ip>` in the script with your actual EC2 IP address.

---

## 📘 License

MIT License (add `LICENSE` file if needed)

---

## 👨‍💻 Author

**Shoaib Ahmad**
GitHub: [shoaib1-oss](https://github.com/shoaib1-oss)
