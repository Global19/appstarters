import datetime
import json

from bs4 import BeautifulSoup
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import RedditCommentItem


class RedditSpider(CrawlSpider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = (
        'https://www.reddit.com/r/IAmA/',
        #'https://www.reddit.com/r/IAmA/comments/470yep/videogameattorney_here_to_answer_questions_about/',
    )
    index = 'reddit_comments'

    rules = (
        #Rule(LinkExtractor(allow=('https://www.reddit.com/r/IAmA/comments/470yep/videogameattorney_here_to_answer_questions_about/')), callback='parse_comments'),
        #Rule(LinkExtractor(allow=('https://www.reddit.com/r/[A-Za-z0-9_]+/comments/[A-Za-z0-9_]+/we_are_rocksdb_developers_ask_us_anything/$')), callback='parse_comments', follow=True), #[A-Za-z0-9\._+]+

        Rule(LinkExtractor(allow=('tommy_chong')), callback='parse_comments', follow=False),
        #Rule(LinkExtractor(allow=('comments')), callback='parse_comments', follow=False),
        #Rule(LinkExtractor(allow=('?count=25&')))
    )

    def parse_comments(self, response):
        for comment in response.xpath('//div[@data-type="comment"]'):
            l = ItemLoader(RedditCommentItem(), selector=comment)
            comment_root_xpath = './div[contains(@class, "entry")]'
            tagline = comment_root_xpath + '/p'
            content = comment_root_xpath + '/form'
            buttons = comment_root_xpath + '/ul'
            l.add_xpath('poster', tagline + '/a[contains(@class, "author")]/text()')
            l.add_xpath('score', tagline + '/span[contains(@class, "unvoted")]/text()')
            l.add_xpath('post_timestamp', tagline + '/time/@datetime')
            l.add_value('scrape_timestamp',datetime.datetime.now())
            l.add_xpath('text', content + '/div[contains(@class, "usertext-body")]/div/p/text()')
            l.add_xpath('permalink', buttons + '/li[@class="first"]/a[@class="bylink"]/@href')
            # l.add_xpath('parent', '//div[@class="product_title"]')
            # l.add_xpath('children', '//div[@class="product_title"]')
            yield l.load_item()

    def parse_page(self, response):
        bsObj = BeautifulSoup(response.body)
        # page_dict = json.loads(str(bsObj))
        #with open('page_dict.json', 'w') as outfile:
        #    json.dump(page_dict, outfile)
        print(bf.data(fromstring('<p id="main">Hello<b>bold</b></p>')))
        print('='*50)
        print(response.body[:1000])
        print('='*50)

        for linenum, line in enumerate(str(bsObj.body).split('\n')):
            if linenum > 115 and linenum < 125:
                print(linenum)
                print(line)
                if linenum == 120:
                    print('+'*50)
                    print(line[820:830])
                    print(line[800:8500])
                    print('+'*50)
        page_dict = bf.data(fromstring(str(bsObj.body)))#.encode(formatter='xml')))
        print(page_dict)


    # def parse(self, response):
    #     return self.parse_comments(response)
