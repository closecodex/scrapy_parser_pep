from urllib.parse import urlparse

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    start_urls = ['https://peps.python.org/']
    allowed_domains = [urlparse(url).netloc for url in start_urls]

    def parse(self, response):
        pep_links = response.xpath(
            ('//a[contains(@class, "pep reference internal")]/@href').extract()
        )
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title_parts = response.css('.page-title::text').get().split()
        pep_number = title_parts[1]
        pep_name = ' '.join(title_parts[3:])
        status = response.xpath(
            '//dt[contains(text(), "Status")]'
            '/following-sibling::dd[1]/abbr/text()'
        ).get()
        yield PepParseItem(
            number=int(pep_number),
            name=pep_name,
            status=status,
        )
