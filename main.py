from crawl_products import CrawlSearch
import argparse
from config import PROJECT_CONFIG

if __name__ == "__main__":
    #################################
    parser = argparse.ArgumentParser(description="Extracting data from amazon")

    parser.add_argument("search_text", type=str, help="the text you want to search in amazon")

    parser.add_argument("page_number", type=str, help="the page number you want to get")

    parser.add_argument("-S", "--storing", type=str, choices=["mongodb", "file", "csv", "redis"],
                        help=" if you want to store data choose a storage type, "
                             " for getting more information visit https://github.com/babakft")

    parser.add_argument("-I", "--download-image", help="downloading product images (-S is needed)", action="store_true")
    args = parser.parse_args()

    PROJECT_CONFIG["STORAGE_TYPE"] = getattr(args, "storing", None)
    PROJECT_CONFIG["DOWNLOAD_IMAGE"] = getattr(args, "download_image", False)

    if args.storing:
        PROJECT_CONFIG["STORING"] = True
    ###################################

    search = CrawlSearch(args.search_text, args.page_number)
    search.start()
