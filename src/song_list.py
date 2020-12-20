from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
import json
import time
import random


class Netease_spider:
    def __init__(self, comment="base"):
        self.comment = comment
        self.file2save = f'{self.comment}-list.json'

        self.originURL = 'https://music.163.com/#/discover/playlist/?cat=%E6%91%87%E6%BB%9A'
        self.data = list()
        self.browser = self._init_drive()

    def _init_drive(self):
        opt = webdriver.chrome.options.Options()
        opt.headless = True
        return webdriver.Chrome(
            ChromeDriverManager().install(),
            options=opt)

    def get_page(self, url):
        self.browser.get(url)
        self.browser.switch_to.frame('g_iframe')
        html = self.browser.page_source
        return html

    def parse4data(self, html):
        """parse html into organized dict
        """
        html_elem = etree.HTML(html)
        play_num = html_elem.xpath(
            '//ul[@id="m-pl-container"]/li/div/div/span[@class="nb"]/text()')
        song_title = html_elem.xpath(
            '//ul[@id="m-pl-container"]/li/p[1]/a/@title')
        song_href = html_elem.xpath(
            '//ul[@id="m-pl-container"]/li/p[1]/a/@href')
        song_link = ['https://music.163.com/#' + item for item in song_href]
        user_title = html_elem.xpath(
            '//ul[@id="m-pl-container"]/li/p[2]/a/@title')
        user_href = html_elem.xpath(
            '//ul[@id="m-pl-container"]/li/p[2]/a/@href')
        user_link = ['https://music.163.com/#' + item for item in user_href]
        data = list(
            map(
                lambda a, b, c, d, e: {
                    'play_count': a.replace('万', '0000'),
                    'list_name': b,
                    'list_url': c,
                    'user_name': d,
                    'user_url': e
                }, play_num, song_title, song_link, user_title, user_link))
        return data

    def parse4link(self, html):
        """Get next page of the current html
        """
        html_elem = etree.HTML(html)
        href = html_elem.xpath(
            '//div[@id="m-pl-pager"]/div[@class="u-page"]/a[@class="zbtn znxt"]/@href'
        )
        if not href:
            return None
        else:
            return 'https://music.163.com/#' + href[0]

    def crawl(self):
        """main function
        """
        print('Running')
        html = self.get_page(self.originURL)
        data = self.parse4data(html)
        self.data.extend(data)
        link = self.parse4link(html)
        while (link):
            html = self.get_page(link)
            data = self.parse4data(html)
            self.data.extend(data)
            link = self.parse4link(html)
            time.sleep(random.random())

        print('Processing')
        data_after_sort = sorted(
            self.data,
            key=lambda item: int(item['play_count']),
            reverse=True)

        print('Write into', self.file2save)
        with open(self.file2save, 'w', encoding='utf-8') as f:
            json.dump(data_after_sort,
                      f,
                      ensure_ascii=False,
                      indent=4)


if __name__ == '__main__':
    spider = Netease_spider(comment="rock")
    spider.crawl()
    print('Finished')