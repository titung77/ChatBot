from data_loader import load_sitemap
from custom_spider import run_spider


if __name__ == '__main__':
    # Load sitemap URLs and save them to a JSON file
    load_sitemap()

    # Run the custom spider
    run_spider()
    print("Done!")
