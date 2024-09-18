import pickle
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Đường dẫn đến msedgedriver
edge_driver_path = "B:\\Documents\\DataScience Research(09 2024)\\edgedriver_win64\\msedgedriver.exe"

# Khởi tạo trình duyệt Edge
service = Service(executable_path=edge_driver_path)
browser = webdriver.Edge(service=service)

# 1. Mở trang đăng nhập
# Bước này tôi đăng nhập gián tiếp qua link này để lúc đăng nhập xong nó vào thẳng luôn đỡ qua trang chủ lại mất công tìm thẻ button để nhấn vào 
browser.get("https://www.kalodata.com/video/detail?id=7396229557373766919&language=vi-VN&currency=VND&region=VN&dateRange=%5B%222024-08-30%22%2C%222024-09-05%22%5D")

# Đợi để trang tải xong
sleep(2)

# 3. Nhập số điện thoại
try:
    phone_field = browser.find_element(By.ID, "register_phone")
    phone_field.clear()
    phone_field.send_keys("0876587765")  # Thay đổi số điện thoại nếu cần
except Exception as e:
    print(f"Không tìm thấy trường số điện thoại: {e}")

# 4. Nhập mật khẩu
try:
    password_field = browser.find_element(By.ID, "register_password")
    password_field.clear()
    password_field.send_keys("trongtiktok3")  # Thay đổi mật khẩu nếu cần
except Exception as e:
    print(f"Không tìm thấy trường mật khẩu: {e}")

# 5. Nhấn vào nút đăng nhập
try:
    submit_button = browser.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Log in')]")
    submit_button.click()
    sleep(5)  # Đợi trang tải xong
except Exception as e:
    print(f"Không tìm thấy nút đăng nhập (submit): {e}")

pickle.dump(browser.get_cookies(), open("my_cookie.pkl", "wb"))

# Đóng trình duyệt
browser.quit()
