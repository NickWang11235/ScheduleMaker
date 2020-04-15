from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import sys

#default file and path
DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

def read_html(path):
    """reads and return a BeautifulSoup html object.

    path - the path to the html file
    """

    html = None
    with open(path, "r") as f:
        doc = f.read()
        html = BeautifulSoup(doc, "html.parser")
    return html


def extract_table_from_html(html):
    """extract and return portions of the html that contain the listings of a specific search

    html - an html object
    """
    
    data_table = html.find("div", "cd-schedule").find("div", "datatableNew")
    preprocess = data_table.find_all("div")    
    postprocess = []
    
    for tag in preprocess:
        if tag["class"][0] == "courseSearchHeader" or tag["class"][0] == "courseSearchItem":
            postprocess.append(tag)
    return postprocess

#html element names for tags of interest
LDAYS_KEY = "col-lg-search-days col-sm-push-1 col-md-days col-sm-days col-xs-2"
LTIME_KEY = "col-lg-search-time col-sm-push-1 col-md-time col-sm-time col-xs-5"
LSPACE_KEY = "col-lg-search-space col-md-space col-sm-push-1 col-sm-space col-xs-2"
LMAX_KEY = "col-lg-days col-md-space col-sm-push-1 col-sm-space col-xs-2"
SID_KEY = "col-sm-1 col-sm-pull-11 col-xs-2"
SDAYS_KEY = "col-lg-search-days col-md-days col-sm-days col-sm-push-1 col-xs-2"
STIME_KEY = "col-lg-search-time col-md-time col-sm-time col-sm-push-1 col-xs-5"
SSPACE_KEY = "col-lg-search-space col-md-space col-sm-push-1 col-sm-space col-xs-2"
SMAX_KEY = "col-lg-days col-md-space col-sm-push-1 col-sm-space col-xs-2"

def parse_to_file(html_name, pretty=False):
    """extract and write course listings from an html file to an xml file, and optionally a txt file

    html_name - the name of the folder containing the course search html file
    pretty - optional for writing to txt file
    """
    
    postprocess = extract_table_from_html(read_html(DEFAULT_DOWNLOAD_PATH + html_name + ".html"))
    #create xml and txt file
    root = ET.Element("root")
    f = None
    if pretty:
        f = open(OUTPUT_DEFAULT_FOLDER + html_name + ".txt", "w")

    #parse html data
    course = None
    for data in postprocess:

        #course title and general info
        if data["class"][0] == "courseSearchHeader":
            
            title = data.find("span", "courseTitle").get_text()
            units_and_grading = data.find_all("span", "pr5")

            #write to xml
            course = ET.SubElement(root, "course", name=title.strip())
            ET.SubElement(course, "course_info", name="units").text=units_and_grading[0].get_text()[6:].strip()
            ET.SubElement(course, "course_info", name="grading").text=units_and_grading[1].get_text().strip()
            #write to txt
            if pretty:
                title += " " + units_and_grading[0].get_text() + " " + units_and_grading[1].get_text()
                f.write(title + ":\n")
            
        if data["class"][0] == "courseSearchItem":

            def extract_label_text(data, tag, attr):
                """helper to extract text form html element"""
                return " ".join(data.find(tag, attr).get_text().split())
            
            indent = "  "
            lecture_id = data.find("div", "row info")["data-target"].strip().split(',')[0][6:]
            lecture_days = extract_label_text(data, "div", LDAYS_KEY)
            lecture_time = extract_label_text(data, "div", LTIME_KEY)
            lecture_space = extract_label_text(data, "div", LSPACE_KEY)
            lecture_max = extract_label_text(data, "div", LMAX_KEY)

            #write to xml
            lecture = ET.SubElement(course, "lecture")
            ET.SubElement(lecture, "lecture_info", name="id").text=lecture_id.strip()
            ET.SubElement(lecture, "lecture_info", name="days").text=lecture_days[5:].strip()
            ET.SubElement(lecture, "lecture_info", name="time").text=lecture_time[5:].strip()
            ET.SubElement(lecture, "lecture_info", name="space").text=lecture_space[6:].strip()
            ET.SubElement(lecture, "lecture_info", name="max").text=lecture_max[4:].strip()

            #write to txt
            if pretty:
                f.write(indent + "Lec " + lecture_id + " " + lecture_days + " " + lecture_time + " " + lecture_space + " " + lecture_max + "\n")
            
            sessions = data.find_all("div", "row susbSessionItem")
            for ses in sessions:
                
                session_id = extract_label_text(ses, "div", SID_KEY)[7:]
                session_days = extract_label_text(ses, "div", SDAYS_KEY)
                session_time = extract_label_text(ses, "div", STIME_KEY)
                session_space = extract_label_text(ses, "div", SSPACE_KEY)
                session_max = extract_label_text(ses, "div", SMAX_KEY)

                #write to xml
                session = ET.SubElement(lecture, "session")
                ET.SubElement(session, "session_info", name="id").text=session_id.strip()
                ET.SubElement(session, "session_info", name="days").text=session_days[5:].strip()
                ET.SubElement(session, "session_info", name="time").text=session_time[5:].strip()
                ET.SubElement(session, "session_info", name="space").text=session_space[6:].strip()
                ET.SubElement(session, "session_info", name="max").text=session_max[4:].strip()

                #write to txt
                if pretty:
                    f.write(indent*2 + "Sec " + session_id + " " + session_days + " " + session_time + " " + session_space + " " + session_max + "\n")


    tree = ET.ElementTree(root)
    tree.write(OUTPUT_DEFAULT_FOLDER + html_name + ".xml")
    if pretty:
        f.close()


def enumerate_data_field(html_name):
    """extract the data fields from the course search html form

    html_name - the path to the html file
    """
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
    
    course_level = values_of_field_helper("ctl00$pageContent$courseLevelDropDown")
    data_field["course_level"] = course_level;

    meet_begin = values_of_field_helper("ctl00$pageContent$startTimeFromDropDown")
    data_field["meet_begin"] = meet_begin;

    meet_end = values_of_field_helper("ctl00$pageContent$startTimeToDropDown")
    data_field["meet_end"] = meet_end;

    days = ["M","T","W","R","F"]
    data_field["days"] = days;

    unit_min = values_of_field_helper("ctl00$pageContent$unitsFromDropDown")
    data_field["unit_min"] = unit_min;

    unit_max = values_of_field_helper("ctl00$pageContent$unitsToDropDown")
    data_field["unit_max"] = unit_max;

    GE = values_of_field_helper("ctl00$pageContent$GECollegeDropDown")
    data_field["GE"] = GE;
    
    area = values_of_field_helper("ctl00$pageContent$GECodeDropDown")
    data_field["area"] = area;

    return data_field
