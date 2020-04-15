import input, scraper, html_extraction, requests

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

with requests.Session() as s:
    
    scraper.login(s)
    scraper.download(s.get(GOLD_SEARCH_URL), DEFAULT_GOLD_FILE_PATH, "search")
    
    #crit = input.request_quarter()
    crit = input.criteria("2020spring")


    #crit = input.request_input()
    crit.department = "asdasd - CHEM"
    crit.days = [1,1,1,1,1,1,1]
    scraper.post_search(crit, s, "chem")

    html_extraction.parse_to_file("chem", pretty=True)
