import csv
import datetime
from collections import defaultdict
from pathlib import Path
from scrapy import signals
from itemadapter import ItemAdapter
import logging
import uuid
import re


class PepParsePipeline:
    def __init__(self, results_dir='results'):
        self.status_count = defaultdict(int)
        self.results_dir = Path(results_dir)
        self.logger = logging.getLogger(__name__)
        self.pep_items = []
        self._close_called = False

    @classmethod
    def from_crawler(cls, crawler):
        feed_uri = list(crawler.settings.get('FEEDS').keys())[0]
        if isinstance(feed_uri, Path):
            feed_uri = feed_uri.as_posix()
        else:
            feed_uri = feed_uri.replace('\\', '/')
        feed_uri_clean = re.sub(r'%\([^\)]+\)[sdf]', '', feed_uri)
        feed_path = Path(feed_uri_clean)
        results_dir = feed_path.parent.resolve()
        pipeline = cls(results_dir=results_dir)
        crawler.signals.connect(pipeline.open_spider, signals.spider_opened)
        crawler.signals.connect(pipeline.close_spider, signals.spider_closed)
        return pipeline

    def open_spider(self, spider):
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f'Results directory: {self.results_dir}')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        status = adapter.get('status')
        if status:
            self.status_count[status] += 1
        self.pep_items.append(adapter)
        return item

    def close_spider(self, spider):
        if self._close_called:
            self.logger.info("close_spider already called, skipping.")
            return
        self._close_called = True
        unique_id = uuid.uuid4().hex
        now_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        summary_file = (
            self.results_dir / f'status_summary_{now_str}_{unique_id}.csv'
        )
        self.logger.info(f'Saving summary file to: {summary_file}')
        with open(summary_file, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Статус', 'Количество'])
            total_count = sum(self.status_count.values())
            for status, count in self.status_count.items():
                writer.writerow([status, count])
            writer.writerow(['Total', total_count])
