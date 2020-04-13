from bs4 import BeautifulSoup
import sys

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
GOLD_SEARCH_FORM = "../../html/GOLDForms/search/search.html"

HTML_DEFAULT_NAME = "/Find Course Results.html"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

def read_html(path):
    html = None
    with open(path, "r") as f:
        doc = f.read()
        html = BeautifulSoup(doc, "html.parser")
    return html


def extract_table_from_html(html):
    data_table = html.find("div", "cd-schedule").find("div", "datatableNew")
    preprocess = data_table.find_all("div")    
    postprocess = []
    
    for tag in preprocess:
        if tag["class"][0] == "courseSearchHeader" or tag["class"][0] == "courseSearchItem":
            postprocess.append(tag)
    return postprocess


def extract_label_text(data, tag, attr):
    return " ".join(data.find(tag, attr).get_text().split())


LDAYS_KEY = "col-lg-search-days col-sm-push-1 col-md-days col-sm-days col-xs-2"
LTIME_KEY = "col-lg-search-time col-sm-push-1 col-md-time col-sm-time col-xs-5"
LSPACE_KEY = "col-lg-search-space col-md-space col-sm-push-1 col-sm-space col-xs-2"
LMAX_KEY = "col-lg-days col-md-space col-sm-push-1 col-sm-space col-xs-2"
SID_KEY = "col-sm-1 col-sm-pull-11 col-xs-2"
SDAYS_KEY = "col-lg-search-days col-md-days col-sm-days col-sm-push-1 col-xs-2"
STIME_KEY = "col-lg-search-time col-md-time col-sm-time col-sm-push-1 col-xs-5"
SSPACE_KEY = "col-lg-search-space col-md-space col-sm-push-1 col-sm-space col-xs-2"
SMAX_KEY = "col-lg-days col-md-space col-sm-push-1 col-sm-space col-xs-2"


def parse_to_file(html_name, file_name):
    
    postprocess = extract_table_from_html(read_html(HTML_DEFAULT_FOLDER + html_name + HTML_DEFAULT_NAME))
    f = open(OUTPUT_DEFAULT_FOLDER + file_name, "w")
    
    for data in postprocess:
        
        if data["class"][0] == "courseSearchHeader":
            
            title = data.find("span", "courseTitle").get_text()
            units_and_grading = data.find_all("span", "pr5")
            title += " " + units_and_grading[0].get_text() + " " + units_and_grading[1].get_text()
            f.write(title + "\n")
            
        if data["class"][0] == "courseSearchItem":
            
            indent = "  "
            lecture_id = data.find("div", "row info")["data-target"].strip().split(',')[0][6:]
            lecture_days = extract_label_text(data, "div", LDAYS_KEY)
            lecture_time = extract_label_text(data, "div", LTIME_KEY)
            lecture_space = extract_label_text(data, "div", LSPACE_KEY)
            lecture_max = extract_label_text(data, "div", LMAX_KEY)         
            f.write(indent + "Lec " + lecture_id + " " + lecture_days + " " + lecture_time + " " + lecture_space + " " + lecture_max + "\n")
            
            sessions = data.find_all("div", "row susbSessionItem")
            for ses in sessions:
                
                session_id = extract_label_text(ses, "div", SID_KEY)[7:]
                session_days = extract_label_text(ses, "div", SDAYS_KEY)
                session_time = extract_label_text(ses, "div", STIME_KEY)
                session_space = extract_label_text(ses, "div", SSPACE_KEY)
                session_max = extract_label_text(ses, "div", SMAX_KEY)
                f.write(indent*2 + "Sec " + session_id + " " + session_days + " " + session_time + " " + session_space + " " + session_max + "\n")
                
    f.close()


def auto_parse_to_file(html_name):
    parse_to_file(html_name, html_name + ".txt")


def extract_search_form_data_field(html_name):
    html = read_html(html_name)
    data_field = {}
    
    def values_of_field_helper(name):
        result = html.find("select", attrs={"name" : name}).find_all("option")
        l = []
        for s in result:
            l.append(s.get_text())
        return l
    
    quarter = values_of_field_helper("ctl00$pageContent$quarterDropDown")
    data_field["quarter"] = quarter;
    
    department = values_of_field_helper("ctl00$pageContent$departmentDropDown")
    data_field["department"] = department;
    
    subject = values_of_field_helper("ctl00$pageContent$subjectAreaDropDown")
    data_field["subject"] = subject;
    
    data_field["course_num"] = "Course Number";
    
    course_level = values_of_field_helper("ctl00$pageContent$courseLevelDropDown")
    data_field["course_level"] = course_level;

    course_level = values_of_field_helper("ctl00$pageContent$courseLevelDropDown")
    data_field["course_level"] = course_level;
    
    GE = values_of_field_helper("ctl00$pageContent$GECollegeDropDown")
    data_field["GE"] = GE;
    
    area = values_of_field_helper("ctl00$pageContent$GECodeDropDown")
    data_field["area"] = area;

    return data_field


def extract_search_form_data_field():
    return extract_search_form_data_field(DEFAULT_GOLD_FILE_PATH)

"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expected use: html_extraction.py <filename>")
        sys.exit(1)
    auto_parse_to_file(sys.argv[1])
"""

