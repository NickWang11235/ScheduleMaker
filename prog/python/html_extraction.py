from bs4 import BeautifulSoup
import sys

HTML_DEFAULT_FOLDER = "../../html/raw/"
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expected use: html_extraction.py <filename>")
        sys.exit(1)
    auto_parse_to_file(sys.argv[1])

