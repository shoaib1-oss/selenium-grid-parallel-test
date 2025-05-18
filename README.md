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
 Step 1: Install Docker
Make sure Docker is installed on your system.

Check with:

bash
Copy
Edit
docker --version
If not installed, install it first from: https://docs.docker.com/get-docker/

🔹 Step 2: Create a Docker Network
Create a Docker network to allow containers to communicate easily.

bash
Copy
Edit
docker network create selenium-grid
🔹 Step 3: Start the Selenium Hub
Hub is the brain of the grid. It accepts test requests and sends them to nodes.

bash
Copy
Edit
docker run -d --net selenium-grid --name selenium-hub \
  -p 4442:4442 -p 4443:4443 -p 4444:4444 \
  selenium/hub:4.21.0
✅ Visit this URL in your browser to confirm it's running:
http://localhost:4444

🔹 Step 4: Start Chrome Node
This node will run Chrome browser instances.

bash
Copy
Edit
docker run -d --net selenium-grid --name chrome-node \
  -e SE_EVENT_BUS_HOST=selenium-hub \
  -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
  -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
  -p 5900:5900 \
  selenium/node-chrome:4.21.0
🔹 Step 5: (Optional) Start Firefox Node
You can also run Firefox if needed:

bash
Copy
Edit
docker run -d --net selenium-grid --name firefox-node \
  -e SE_EVENT_BUS_HOST=selenium-hub \
  -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
  -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
  -p 5901:5900 \
  selenium/node-firefox:4.21.0
🔹 Step 6: Verify Grid Status
Go to:
http://localhost:4444/grid/status
You should see both Chrome and Firefox nodes registered.

🔹 Step 7: Run a Selenium Test (Sample Python)
Install Selenium in Python (if needed):

bash
Copy
Edit
pip install selenium
Run this test:

python
Copy
Edit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    desired_capabilities=DesiredCapabilities.CHROME
)

driver.get("https://www.google.com")
print(driver.title)
driver.quit()
✅ This will open Chrome inside the Docker container.

🔹 Step 8: Watch the Browser via VNC (Optional)
Use a VNC viewer like RealVNC:

Host: localhost

Port: 5900 (Chrome) or 5901 (Firefox)

Password: secret (default for Selenium images)



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
