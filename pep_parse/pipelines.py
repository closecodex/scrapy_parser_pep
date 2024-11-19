import csv
import datetime
from collections import defaultdict
import logging
from pathlib import Path
from scrapy import signals
from itemadapter import ItemAdapter


class PepParsePipeline:
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)
        if not self.results_dir.exists():
            self.results_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._close_called = False

    @classmethod
    def from_crawler(cls, crawler):
        feed_uri = list(crawler.settings.get('FEEDS').keys())[0]
        if isinstance(feed_uri, Path):
            feed_uri = feed_uri.as_posix()
        else:
            feed_uri = str(feed_uri).replace('\\', '/')
        feed_uri_clean = feed_uri.split('%')[0]
        feed_path = Path(feed_uri_clean).resolve()
        results_dir = feed_path.parent
        pipeline = cls(results_dir=results_dir)
        crawler.signals.connect(pipeline.open_spider, signals.spider_opened)
        crawler.signals.connect(pipeline.close_spider, signals.spider_closed)
        return pipeline

    def open_spider(self, spider):
        self.status_count = defaultdict(int)
        self.pep_items = []
        spider.logger.info(f"Results directory set to: {self.results_dir}")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.status_count[adapter['status']] += 1
        self.pep_items.append(adapter)
        return item

    def close_spider(self, spider):
        if self._close_called:
            self.logger.info("close_spider already called, skipping.")
            return
        self._close_called = True
        now_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        summary_file = self.results_dir / (
            f"status_summary_{now_str}.csv"
        )
        self.logger.info(f"Saving summary file to: {summary_file}")
        total_count = sum(self.status_count.values())
        rows = [
            ['Статус', 'Количество']
        ] + list(self.status_count.items()) + [['Total', total_count]]
        with open(
            summary_file, mode='w', encoding='utf-8', newline=''
        ) as file:
            writer = csv.writer(file)
            writer.writerows(rows)
