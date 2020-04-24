import input, scraper, html_extraction, sys, requests, gui.test

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"


def main():
    args = sys.argv[1:]
    crit = input.criteria()
    input.run(args, crit)
    
    storage = input.criteria()
    storage.data["department"] = "asd-CHEM"

    with requests.Session() as s:
    
        scraper.login(s)
        scraper.download(s.get(GOLD_SEARCH_URL), DEFAULT_GOLD_FILE_PATH, "search")
        scraper.post_search(crit, s, "chem3")
        html_extraction.parse_to_file("chem3", pretty=True)


if __name__ == "__main__":
    main()
