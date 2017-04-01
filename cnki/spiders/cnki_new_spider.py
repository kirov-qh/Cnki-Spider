# -*- coding:utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from cnki.items import CnkiItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class CnkiSpider(Spider):

    name = "cnkispider"
    #Slow down the speed.
    download_delay = 1
    allowed_domains = ["cnki.net"]
    start_urls = ["http://www.cnki.net/"]
    
    #Set the browser to no-pic mode.
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options = chrome_options)

    def parse(self, response):

        #Get the content of the first page.
        browser = self.driver
        browser.get(self.start_urls[0])
        browser.maximize_window()
        #Here input the key word to search.
        elem = browser.find_element_by_class_name("rekeyword")
        elem.send_keys(u"蜜蜂")
        browser.find_element_by_xpath("//*[@id='btnSearch']").click()
        time.sleep(2)
        browser.switch_to.frame('iframeResult')
        time.sleep(1)
        result_page = browser.current_window_handle
        #Display 50 items in one page.
        browser.find_element_by_xpath("//*[@id='id_grid_display_num']/a[3]").click()
        
        #Grab the content and turn to next page.
        for j in range(1,121):
            for i in range(2,52):
                browser.find_element_by_xpath("//*[@id='ctl00']/table/tbody/tr[2]/td/table/tbody/tr["+str(i)+"]/td[2]/a").click()
                all_windows = browser.window_handles
                for window in all_windows:
                    if window != result_page:
                        item_page = window
                browser.switch_to.window(item_page)
                url = browser.current_url
                yield Request(url, callback=self.parse_item)
                browser.close()
                time.sleep(0.1)
                browser.switch_to.window(result_page)
                time.sleep(0.1)
                browser.switch_to.frame('iframeResult')
                time.sleep(0.1)
                
            if j >= 10:
                time.sleep(60)
            browser.find_element_by_xpath("//a[contains(text(),'下一页')]").click()
            

    def parse_item(self, response):

        sel = Selector(response)
        item = CnkiItem()
        page_title = sel.xpath('//div[@class="wxTitle"]/h2/text()').extract()
        page_abstract = sel.xpath('//span[@id="ChDivSummary"]/text()').extract()
        page_keyword = sel.xpath('//label[@id="catalog_KEYWORD"]/../a/text()').extract()

        item['title'] = page_title
        item['abstract'] = page_abstract
        str = ' '.join(page_keyword).replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").strip()
        item['keyword'] = str
        yield item
        
