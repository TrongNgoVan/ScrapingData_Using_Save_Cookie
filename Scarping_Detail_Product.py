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

browser.get("https://www.kalodata.com/product/detail?id=1729577314986658654&language=vi-VN&currency=VND&region=VN")

# 2.Load cookie from file

cookies = pickle.load(open("my_cookie.pkl","rb"))
for cookie in cookies:
    browser.add_cookie(cookie)

# 3. Refresh the browser
browser.get("https://www.kalodata.com/product/detail?id=1729577314986658654&language=vi-VN&currency=VND&region=VN")

try:
    close_button = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ant-modal-close"))
    )
    close_button.click()
    print("Đã nhấn vào nút đóng!")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")



try:
    # Chờ đến khi phần tử '30 ngày trước' hiển thị và nhấp
    button_30_days = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'30 ngày trước')]"))
    )
    button_30_days.click()
    print("Đã nhấp vào nút '30 ngày trước'.")
    sleep(2)
except Exception as e:
    print(f"Không thể nhấp vào nút '30 ngày trước': {e}")



# Định nghĩa hàm click_next_page
def click_next_page():
    try:
        # Đợi cho đến khi nút "Trang Kế" không bị disabled và có thể click
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[not(@disabled)]//span[@aria-label="right"]'))
        )
        next_button.click()
        print("Đã chuyển sang trang tiếp theo.")
        return True
    except TimeoutException:
        print("Không tìm thấy nút 'Trang Kế' hoặc nút bị vô hiệu hóa.")
        return False

# Biến để theo dõi lần đầu tiên
first_page = True

# Vòng lặp để lấy dữ liệu từ nhiều trang
while True:
    try:
        # Đợi các hàng trong bảng xuất hiện trước khi lấy dữ liệu
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="ant-table-row ant-table-row-level-0"]'))
        )
        
        # Lấy tất cả các hàng
        rows = browser.find_elements(By.XPATH, '//tr[@class="ant-table-row ant-table-row-level-0"]')

        # Duyệt qua từng hàng và lấy dữ liệu
        for row in rows:
            try:
                # Lấy số thứ tự từ thẻ <td> đầu tiên (thẻ cố định bên trái)
                number = row.find_element(By.XPATH, './/td[@class="ant-table-cell ant-table-cell-fix-left"]').text
                print(f"Số thứ tự: {number}")

                # Lấy tên người dùng từ <div> class "line-clamp-1 group-hover:text-primary"
                username = row.find_element(By.XPATH, './/div[contains(@class, "line-clamp-1 group-hover:text-primary")]').text
                print(f"Nhà sáng tạo: {username}")

                # Lấy số lượng người theo dõi từ <div> class "text-base-999"
                followers = row.find_element(By.XPATH, './/div[contains(@class, "text-base-999")]').text
                print(f"Số người theo dõi: {followers}")

                # Lấy dữ liệu từ các thẻ <td> khác chứa giá trị tiền tệ và số liệu
                gia_tri1 = row.find_element(By.XPATH, './/td[@class="ant-table-cell ant-table-column-sort"]').text
                print(f"Doanh thu: {gia_tri1}")
                
                gia_tri2 = row.find_element(By.XPATH, './/td[@class="ant-table-cell"][1]').text  # Thẻ <td> đầu tiên sau thẻ sort
                print(f"Lượt bán: {gia_tri2}")
                
                gia_tri3 = row.find_element(By.XPATH, './/td[@class="ant-table-cell"][2]').text  # Thẻ <td> thứ hai
                print(f"Doanh thu từ video: {gia_tri3}")
                
                gia_tri4 = row.find_element(By.XPATH, './/td[@class="ant-table-cell"][3]').text  # Thẻ <td> thứ ba
                print(f"Doanh thu Live : {gia_tri4}")
                
            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")
                continue

        # Sau khi lấy dữ liệu trang hiện tại xong, nhấn nút "Trang Kế"
        if not first_page :
            if not click_next_page():
                break  # Nếu không còn trang tiếp theo, thoát vòng lặp
        else:
            first_page = False  # Sau lần đầu tiên thì cập nhật biến này

    except TimeoutException:
        print("Đã hết thời gian chờ, không thể lấy dữ liệu từ trang này.")
        break





browser.quit()





