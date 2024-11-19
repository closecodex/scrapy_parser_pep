from pathlib import Path

BOT_NAME = 'pep_parse'
SPIDER_MODULES = [f'{BOT_NAME}.spiders']
NEWSPIDER_MODULE = f'{BOT_NAME}.spiders'
RESULTS_DIR = 'results'
BASE_DIR = Path(__file__).parent.parent

ITEM_PIPELINES = {
    f'{BOT_NAME}.pipelines.PepParsePipeline': 300,
}

FEEDS = {
    f'{RESULTS_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
    },
}
