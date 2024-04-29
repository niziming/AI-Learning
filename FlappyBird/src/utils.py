# 工具函数
from selenium import webdriver



def get_webdriver(url):
    # 检查浏览器类型
    # browser_type = input("Enter browser type (chrome/edge): ")
    browser_type = "edge"
    if browser_type.lower() == 'chrome':
        # ChromeDriver 可执行文件路径
        chrome_driver_path = 'path/to/chromedriver.exe'
        # 启动 Chrome 浏览器并访问网页
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
    elif browser_type.lower() == 'edge':
        # EdgeDriver 可执行文件路径
        edge_driver_path = 'D:\Program Files\edgedriver_win64\msedgedriver.exe'
        # 启动 Edge 浏览器并访问网页
        driver = webdriver.Edge(executable_path=edge_driver_path)
    else:
        raise ValueError("Unsupported browser: {}".format(browser_type))

    # 创建 EdgeOptions 对象
    edge_options = webdriver.EdgeOptions()

    # 禁用弹出框
    edge_options.add_argument("--disable-popup-blocking")

    # 启动 Edge 浏览器并传入选项
    driver = webdriver.Edge(options=edge_options)

    # 访问网页
    driver.get(url)

    return driver