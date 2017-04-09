# -*- coding:utf-8 -*-

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from cnki.items import CnkiItem
from selenium import webdriver
import MySQLdb
import MySQLdb.cursors
import time


class CnkiSpider(Spider):

    name = "cnkispider"
    allowed_domains = ["cnki.net"]
    start_urls = ["http://www.cnki.net/"]
    #Ajax iframe page.


    #Set the browser to no-pic mode.
    chrome_option = webdriver.ChromeOptions()
    pref = {"profile.managed_default_content_settings.images":2}
    chrome_options.add_experimental_option("prefs",pref)
    driver = webdriver.Chrome(chrome_options = chrome_option)

    def parse(self, response):

        # Connect to the MySQLDB.
        db_conn = MySQLdb.connect(user='root', passwd='131072', db='source',
                                    host='127.0.0.1', charset='utf8',
                                    use_unicode=True)
        db_cursor = db_conn.cursor()
        db_num = db_cursor.execute("select count(*) from source")

        #Traverse the database.
        for n in range(1, db_num + 1):
            db_cursor.execute(
                "select name from source where id=" + str(n) + "")
            info = db_cursor.fetchall()
            for i_info in info:
                keyword = i_info[0]

            # Get the content of the first page.
            browser = self.driver
            browser.get(self.start_urls[0])
            browser.maximize_window()

            #Here input the key word to search.
            browser.find_element_by_class_name("rekeyword").send_keys(keyword)
            browser.find_element_by_id("btnSearch").click()
            time.sleep(2)
            browser.switch_to.frame('iframeResult')
            time.sleep(1)
            result_page = browser.current_window_handle
            #Display 50 items in one page.
            browser.find_element_by_xpath(
                "//*[@id='id_grid_display_num']/a[3]").click()

            #Grab the content and turn to next page.
            for j in range(1,121):
                try:
                    for i in range(2,52):
                        browser.find_element_by_xpath(
                            "//*[@id='ctl00']/table/tbody/tr[2]/td/table/tbody/tr[" + str(
                                i) + "]/td[2]/a").click()
                        time.sleep(0.88)
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
                    browser.find_element_by_xpath(
                        "//a[contains(text(),'下一页')]").click()

                except:
                    log.msg('Something is wrong!.', spider = spider)
                    browser.quit()
                    break


    def parse_item(self, response):

        sel = Selector(response)
        item = CnkiItem()
        page_title = sel.xpath('//div[@class="wxTitle"]/h2/text()').extract()
        page_abstract = sel.xpath('//span[@id="ChDivSummary"]/text()').extract()
        page_keyword = sel.xpath(
            '//label[@id="catalog_KEYWORD"]/../a/text()').extract()

        item['title'] = page_title
        item['abstract'] = page_abstract
        str0 = ' '.join(page_keyword).replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "").strip()
        item['keyword'] = str0
        yield item

