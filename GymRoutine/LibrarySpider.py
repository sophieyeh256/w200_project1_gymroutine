"""
Crawls website to extract data and write to a json file
References:
https://exrx.net/Lists/Directory
https://docs.scrapy.org/en/latest/
https://xpather.com/
https://www.w3schools.com/xml/xpath_syntax.asp
"""
import re
import scrapy
from scrapy.crawler import CrawlerProcess
import html

class LibrarySpider(scrapy.Spider):
    name = "libraryspider"
    start_urls = ['https://exrx.net/Lists/Directory']

    def parse(self, response):
        for quote in response.xpath('//article//li[count(ancestor::li)=0]/a'):
            text = quote.xpath('text()').get()
            link = quote.xpath('@href').get()
            link = response.urljoin(link)
            yield scrapy.Request(link,callback=self.parse_page2,
            cb_kwargs = dict(muscle = text))

    def parse_page2(self, response, muscle):
        library = {}
        for quote in response.xpath('//article//li[count(descendant::a) = 1]/a'):
            text = quote.xpath('text()').get()
            link = quote.xpath('@href').get()
            if link is not None and ('WeightExercises' in link or 'Stretch' in link):
                if text is None:
                    text = quote.xpath('*').get() # get text formatted differently
                    p = re.compile(r'<.*?>') # remove html tags
                    text = p.sub('', text)
                if muscle in library.keys():
                    library[muscle].append((text, link))
                else:
                    library[muscle] = [(text,link)]
        return library
