from crawl_products import CrawlSearch
import argparse
from config import STORAGE_TYPE, DOWNLOAD_IMAGE

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extracting data from amazon")
    parser.add_argument("search_text", type=str, help="the text you want to search in amazon")
    parser.add_argument("page_number", type=str, help="the page number you want to get")
    parser.add_argument("storage_type", type=str, choices=["mongodb", "file", "csv"], help="choose a storage type "
                                                                                           "for saving data")
    parser.add_argument("-I", "--download-image", help="downloading product images", action="store_true")
    args = parser.parse_args()

    STORAGE_TYPE = args.storage_type
    DOWNLOAD_IMAGE = args.download_image

    search = CrawlSearch("ps4", "19")
    search.start()

