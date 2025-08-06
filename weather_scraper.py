# weather_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date

def get_weather_data():
    td = date.today()
    wait_imp = 10

    # Setup Chrome Options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')  # run in background
    chrome_options.add_argument('--disable-gpu')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    weather_site = "https://www.timeanddate.com/weather/?sort=6&low=4"
    driver.get(weather_site)
    driver.implicitly_wait(wait_imp)

    temp_raw = driver.find_elements(By.CLASS_NAME, 'rbi')
    temp_list = []

    for val in temp_raw:
        text = val.text.strip()
        if text and text != "N/A":
            try:
                temp = int(text.split()[0])
                temp_list.append(temp)
            except ValueError:
                continue

    temp_list.sort(reverse=True)
    max_temp = max(temp_list)
    min_temp = min(temp_list)

    table_data = driver.find_element(By.CLASS_NAME, 'zebra.fw.tb-theme')
    table_rows = table_data.find_elements(By.TAG_NAME, "tr")

    city_names = []
    temp_vals = []

    column_indices = [0, 4, 8]
    for row in table_rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        for j in column_indices:
            if len(cells) > j + 3:
                city = cells[j].text.strip()
                temp_text = cells[j + 3].text.strip()
                temp_parts = temp_text.split()
                if city and temp_parts:
                    city_names.append(city)
                    temp_vals.append(temp_parts)

    c_name_H = c_name_C = "Unknown"
    for idx, val in enumerate(temp_vals):
        if val[0] == str(max_temp):
            c_name_H = city_names[idx]
            break
    for idx, val in enumerate(temp_vals):
        if val[0] == str(min_temp):
            c_name_C = city_names[idx]
            break

    driver.quit()

    return {
        "date": td.strftime("%b-%d-%Y"),
        "max_temp": max_temp,
        "max_city": c_name_H,
        "min_temp": min_temp,
        "min_city": c_name_C
    }
