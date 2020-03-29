from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from fake_useragent import UserAgent

import bs4, os, re, time, zipfile
from base64 import b64encode

import sys
from posix import unlink

## 自动打zip包，包含 background.js 和 manifest.json 两个文件
class Smartchrome():
    def __init__(self,proxy_enable=True,headers=None):
        proxy = {
            "host":"forward.apeyun.com", 
            "port":"9082",
            "user":"1910280004560115928",
            "passwd":"OwuEZGXHXPA0PsW1",
            "number":5
             }
        self.driver = None
        self.proxy_meta = proxy
        self.proxy_enable = proxy_enable
        self.timeout = 5
        self.html = None
        self.headers = headers
        self.display = None
    
    def get_chrome_proxy_extension(self):
        """获取一个Chrome代理扩展,里面配置有指定的代理(带用户名密码认证)
            proxy - 指定的代理,格式: username:password@ip:port
        """
        
        # Chrome代理插件的参考模板 https://github.com/RobinDev/Selenium-Chrome-HTTP-Private-Proxy
        CHROME_PROXY_HELPER_DIR = 'Chrome-proxy-helper'     # 自定义目录名，放在代理项目的当前同一级目录
        
        # 存储自定义Chrome代理扩展文件的目录，一般为当前同一级目录
        # 生成的zip路径为：chrome-proxy-extensions/mimvp-user_mimvp-pass@140.143.62.84_19480.zip
        CUSTOM_CHROME_PROXY_EXTENSIONS_DIR = 'chrome-proxy-extensions'  

        proxy = self.proxy_meta
        if proxy:
            # 提取代理的各项参数
            username = proxy.get("user")
            password = proxy.get("passwd")
            ip = proxy.get("host")
            port = proxy.get("port")
            # 创建一个定制Chrome代理扩展(zip文件)
            if not os.path.exists(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR):
                os.mkdir(CUSTOM_CHROME_PROXY_EXTENSIONS_DIR)
            extension_file_path = CUSTOM_CHROME_PROXY_EXTENSIONS_DIR + '/'  + proxy.get('user') + '.zip'
            
            # 扩展文件不存在，则创建配置文件，并写入zip文件
            if not os.path.exists(extension_file_path):
                zf = zipfile.ZipFile(extension_file_path, mode='w')
                zf.write(os.path.join(CHROME_PROXY_HELPER_DIR, 'manifest.json'), 'manifest.json')
                # 替换模板中的代理参数
                background_content = open(os.path.join(CHROME_PROXY_HELPER_DIR, 'background.js')).read()
                background_content = background_content.replace('mimvp_proxy_host', ip)
                background_content = background_content.replace('mimvp_proxy_port', port)
                background_content = background_content.replace('mimvp_username', username)
                background_content = background_content.replace('mimvp_password', password)
                zf.writestr('background.js', background_content)
                zf.close()
            return extension_file_path
        else:
            raise Exception('Invalid proxy format. Should be username:password@ip:port')

    def open_driver(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        try:
            proxy = self.proxy_meta 
            proxy_zip = self.get_chrome_proxy_extension()# 打包代理zip文件
            chrome_options = webdriver.ChromeOptions()      # ok
            chrome_options.add_extension(proxy_zip)
            # 隐藏"Chrome正在受到自动软件的控制"
            chrome_options.add_argument('disable-infobars')
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage") 
            # 设置selenium不加载图片，提高爬取效率
            #prefs = {"profile.managed_default_content_settings.images": 2}
            #options.add_experimental_option("prefs", prefs)
            # 修改请求头，伪装浏览器型号
            chrome_options.add_argument('user-agent='+UserAgent().random)
            
            chromedriver = '/usr/local/bin/chromedriver'
            driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
            # 将浏览器窗口最大化
            #driver.maximize_window()
            # 指定浏览器窗口大小
            #driver.set_window_size(560, 400)
            self.driver = driver
        except Exception as e:
            print("e:%s"% e)
            if self.driver: self.driver.quit()
            if self.display: self.display.stop()

    def close_driver(self):
        if self.driver: self.driver.quit()
        if self.display: self.display.stop()

if __name__ == '__main__':
    sc = Smartchrome()
    sc.open_driver()
    url2 = "http://cip.cc"
    sc.driver.get(url2)
    page = sc.driver.page_source
    print(page)
    sc.close_driver()
