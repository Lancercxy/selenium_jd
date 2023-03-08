from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import json
import csv
import time
 
class JdSpider():
    
    #二、打开或创建保存数据的文件
    def open_file(self):
        self.fm = input('请输入文件保存格式(txt、json、csv):')
        while self.fm!='txt' and self.fm!='json' and self.fm!='csv':
            self.fm = input('输入错误，请重新输入文件保存格式(txt、json、csv):')
        if self.fm=='txt' :
            self.fd = open('Jd.txt','w',encoding='utf-8')
        elif self.fm=='json' :
            self.fd = open('Jd.json','w',encoding='utf-8')
        elif self.fm=='csv' :
            self.fd = open('Jd.csv','w',encoding='utf-8',newline='')
            
    #三、打开浏览器并等待
    def open_browser(self):
        #打开Chrome浏览器
        self.browser = webdriver.Chrome()
        #隐式等待10秒
        self.browser.implicitly_wait(10)
        #显式等待10秒
        self.wait = WebDriverWait(self.browser,10)
        
    #四、初始化变量
    def init_variable(self):
        #初始化变量
        self.data = zip()
        self.isLast = False
        
    #六、解析网页并获取关键数据
    def parse_page(self):
        try:
            skus = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//li[@class="gl-item"]')))
            skus = [item.get_attribute('data-sku') for item in skus]
            links = ['https://item.jd.com/{sku}.html'.format(sku=item) for item in skus]
            prices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[2]/strong/i')))
            prices = [item.text for item in prices]
            names = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[3]/a/em')))
            names = [item.text for item in names]
            comments = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[4]/strong')))
            comments = [item.text for item in comments]
            self.data = zip(links,prices,names,comments)
        except selenium.common.exceptions.TimeoutException:
            print('parse_page: TimeoutException')
            self.parse_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('parse_page: StaleElementReferenceException')
            self.browser.refresh()
            
    #七、保存数据
    def write_to_file(self):
        if self.fm == 'txt':
            for item in self.data:
                self.fd.write('----------------------------------------\n')
                self.fd.write('link:' + str(item[0]) + '\n')
                self.fd.write('price:' + str(item[1]) + '\n')
                self.fd.write('name:' + str(item[2]) + '\n')
                self.fd.write('comment:' + str(item[3]) + '\n')
        if self.fm == 'json':
            temp = ('link','price','name','comment')
            for item in self.data:
                json.dump(dict(zip(temp,item)),self.fd,ensure_ascii=False)
        if self.fm == 'csv':
            writer = csv.writer(self.fd)
            for item in self.data:
                writer.writerow(item)
                
    #八、实现换页
    def turn_page(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="pn-next"]'))).click()
            time.sleep(1)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            self.isLast = True
        except selenium.common.exceptions.TimeoutException:
            print('turn_page: TimeoutException')
            self.turn_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('turn_page: StaleElementReferenceException')
            self.browser.refresh()
            
    #九、关闭文件
    def close_file(self):
        self.fd.close()
 
    #十、关闭驱动
    def close_browser(self):
        self.browser.quit()
        
        
    #一、执行爬虫程序
    def crawl(self):
        
        #二、打开或创建保存数据的文件
        self.open_file()
        
        #三、打开浏览器并等待
        self.open_browser()
        
        #四、初始化变量
        self.init_variable()
        
        #五、开始爬取数据
        print('开始爬取')
        self.browser.get('https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC&enc=utf-8')
        time.sleep(1)
        
        #滚动到页面底部
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        count = 0
        while not self.isLast:
            count += 1
            print('正在爬取第 ' + str(count) + ' 页......')
            #六、解析网页并获取关键数据
            self.parse_page()
            
            #七、保存数据
            self.write_to_file()
            
            #八、实现换页
            self.turn_page()
            
        #九、关闭文件
        self.close_file()
        
        #十、关闭驱动
        self.close_browser()
        print('结束爬取')
 
if __name__ == '__main__':
    spider = JdSpider()
    spider.crawl()