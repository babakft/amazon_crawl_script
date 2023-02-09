from crawl_products import CrawlSearch
import argparse
from config import project_config

if __name__ == "__main__":
    #################################
    parser = argparse.ArgumentParser(description="Extracting data from amazon")

    parser.add_argument("search_text", type=str, help="the text you want to search in amazon")

    parser.add_argument("page_number", type=str, help="the page number you want to get")

    parser.add_argument("-S", "--storing", type=str, choices=["mongodb", "file", "csv"],
                        help="choose a storage type if you want to store data "
                             "for saving data")

    parser.add_argument("-I", "--download-image", help="downloading product images", action="store_true")
    args = parser.parse_args()

    project_config["STORAGE_TYPE"] = getattr(args, "storing", None)
    project_config["DOWNLOAD_IMAGE"] = getattr(args, "download_image", False)

    if args.storing:
        project_config["STORING"] = True
    ###################################

    search = CrawlSearch(args.search_text, args.page_number)
    search.start()
