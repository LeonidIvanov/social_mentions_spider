import scrapy
from scrapy import signals
from scrapy.http import Request

from social_mentions_scraper.settings import DEFAULT_OUTPUT_NAME, DELETE_RESULTS_FILE_AFTER
from social_mentions_scraper.utils.keywords import get_keywords_list
from social_mentions_scraper.utils.file_processing import send_file_to_aws, delete_file
from social_mentions_scraper.utils.semantic_processing import get_name_from_domain


class SocialMentionSpider(scrapy.Spider):
    name = 'social-links-lookup-spider'

    def start_requests(self):
        keywords_file = getattr(self, 'file', None)
        if keywords_file:
            keywords = get_keywords_list(keywords_file)
            for keyword in keywords:
                url = 'https://www.google.com/search?hl=en&q="{}"'.format(keyword)
                yield scrapy.Request(url, self.parse_google_page)
        else:
            print('Please, provide absolute path to keywords csv file using "-a file=/path/to/file.csv"')

    def parse_google_page(self, response):
        srg = response.css("div.srg")
        g = srg.css("div.g")[0]
        link = g.css("a::attr(href)")[0].get()
        yield Request(link, callback=self.parse_query_result)

    def parse_query_result(self, response):
        link = response.url
        domain_name = get_name_from_domain(link)
        body = response.css("body").get()
        twitter, facebook, instagram = self.check_social_mentions(body)
        with open(DEFAULT_OUTPUT_NAME, 'a') as f:
            f.write('{domain_name}, {link}, {twitter}, {facebook}, {instagram}\n'.format(domain_name=domain_name,
                                                                                         link=link,
                                                                                         twitter=twitter,
                                                                                         facebook=facebook,
                                                                                         instagram=instagram))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SocialMentionSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    @staticmethod
    def spider_closed(spider):
        spider.logger.info('Spider closed: {}'.format(spider.name))
        send_file_to_aws(DEFAULT_OUTPUT_NAME)
        if DELETE_RESULTS_FILE_AFTER:
            delete_file(DEFAULT_OUTPUT_NAME)


    @staticmethod
    def check_social_mentions(html):
        twitter = "No"
        facebook = "No"
        instagram = "No"
        if "Twitter" in html:
            twitter = "Yes"
        if "Facebook" in html:
            facebook = "Yes"
        if "Instagram" in html:
            instagram = "Yes"
        return twitter, facebook, instagram
