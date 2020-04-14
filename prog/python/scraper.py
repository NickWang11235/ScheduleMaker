import os, requests, time, getpass, shutil
from bs4 import BeautifulSoup

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

LOGIN_DATA = {
            "__VIEWSTATE" : "" ,
            "__VIEWSTATEGENERATOR" : "" ,
            "__EVENTVALIDATION" : ""
            , "ctl00$pageContent$userNameText" : "" ,
            "ctl00$pageContent$passwordText" : "" ,
            "ctl00$pageContent$loginButton" : "Login"
        }

SEARCH_DATA = {
        "__EVENTTARGET" : "" ,
        "__EVENTARGUMENT" : "" ,
        "__LASTFOCUS" : "" ,
        "__VIEWSTATE" : "" ,
        "__VIEWSTATEGENERATOR" : "" ,
        "ctl00$pageContent$quarterDropDown" : "" ,
        "ctl00$pageContent$sessionDropdown" : "" ,
        "ctl00$pageContent$departmentDropDown" : "" ,
        "ctl00$pageContent$subjectAreaDropDown" : "" ,
        "ctl00$pageContent$courseNumberTextBox" : "" ,
        "ctl00$pageContent$courseLevelDropDown" : "" ,
        "ctl00$pageContent$startTimeFromDropDown" : "" ,
        "ctl00$pageContent$startTimeToDropDown" : "" ,
        "ctl00$pageContent$daysCheckBoxList$0" : "" ,
        "ctl00$pageContent$daysCheckBoxList$1" : "" ,
        "ctl00$pageContent$daysCheckBoxList$2" : "" ,
        "ctl00$pageContent$daysCheckBoxList$3" : "" ,
        "ctl00$pageContent$daysCheckBoxList$4" : "" ,
        "ctl00$pageContent$daysCheckBoxList$5" : "" ,
        "ctl00$pageContent$daysCheckBoxList$6" : "" ,
        "ctl00$pageContent$unitsFromDropDown": "" ,
        "ctl00$pageContent$unitsToDropDown" : "" ,
        "ctl00$pageContent$enrollcodeTextBox" : "" ,
        "ctl00$pageContent$instructorTextBox" : "" ,
        "ctl00$pageContent$keywordTextBox" : "" ,
        "ctl00$pageContent$GECollegeDropDown" : "" ,
        "ctl00$pageContent$GECodeDropDown" : "" ,
        "ctl00$pageContent$openSectionsOnlyCheckBox" : "" ,
        "ctl00$pageContent$matchingSectionsOnlyCheckBox" : "" ,
        "ctl00$pageContent$noRestrictionsCheckBox" : "" ,
        "ctl00$pageContent$noPrerequisitesCheckBox" : "" ,
        "ctl00$pageContent$searchButton" : ""
    }


def save(path,soup_file):
    with open(path, "w") as outf:
        outf.write(str(soup_file))


def login(ses):
    data = LOGIN_DATA
    home = ses.get(GOLD_LOGIN_URL)
    soup = BeautifulSoup(home.text, "html.parser")
    
    data["__VIEWSTATE"] = soup.find("input", attrs={"type" : "hidden"
                                                  , "name" : "__VIEWSTATE"})["value"]
    data["__VIEWSTATEGENERATOR"] = soup.find("input", attrs={"type" : "hidden"
                                                  , "name" : "__VIEWSTATEGENERATOR"})["value"]
    data["__EVENTVALIDATION"] = soup.find("input", attrs={"type" : "hidden"
                                                  , "name" : "__EVENTVALIDATION"})["value"]
    
    username = input("Username: ")
    password = getpass.getpass(prompt="Password: ")
    data["ctl00$pageContent$userNameText"] = username
    data["ctl00$pageContent$passwordText"] = password
    ses.post(GOLD_LOGIN_URL, data=data)
    return ses


def post_search(criteria, ses, file_name):
    
    data = SEARCH_DATA
    search = ses.get(GOLD_SEARCH_URL)
    soup = BeautifulSoup(search.text, "html.parser")

    data["__VIEWSTATE"] = soup.find("input", attrs={"type" : "hidden"
                                                  , "name" : "__VIEWSTATE"})["value"]
    data["__VIEWSTATEGENERATOR"] = soup.find("input", attrs={"type" : "hidden"
                                                           , "name" : "__VIEWSTATEGENERATOR"})["value"]
    
    data["ctl00$pageContent$quarterDropDown"] = match_quarter(criteria.quarter)    
    data["ctl00$pageContent$sessionDropdown"] = match_session(criteria.session)
    data["ctl00$pageContent$departmentDropDown"] = match_department(criteria.department)
    data["ctl00$pageContent$subjectAreaDropDown"] = match_subject(criteria.subject)
    data["ctl00$pageContent$courseNumberTextBox"] = criteria.course_num
    data["ctl00$pageContent$courseLevelDropDown"] = match_course_level(criteria.course_level)
    data["ctl00$pageContent$startTimeFromDropDown"] = match_hours(criteria.meet_begin)
    data["ctl00$pageContent$startTimeToDropDown"] = match_hours(criteria.meet_end)

    week = ["M","T","W","R","F","S","U"]
    for i in range(len(criteria.days)):
        if criteria.days[i]:
            data["ctl00$pageContent$daysCheckBoxList$" + str(i)] = week[i]
                   
    data["ctl00$pageContent$unitsFromDropDown"] = criteria.unit_min
    data["ctl00$pageContent$unitsToDropDown"] = criteria.unit_max
    data["ctl00$pageContent$enrollcodeTextBox"] = criteria.enrollment
    data["ctl00$pageContent$instructorTextBox"] = criteria.instructor
    data["ctl00$pageContent$keywordTextBox"] = criteria.title
    data["ctl00$pageContent$GECollegeDropDown"] = match_GE(criteria.GE)
    data["ctl00$pageContent$GECodeDropDown"] = match_area(criteria.area)
    if criteria.open_sections:
        data["ctl00$pageContent$openSectionsOnlyCheckBox"] = "on"
    if criteria.matching_sections:
        data["ctl00$pageContent$matchingSectionsOnlyCheckBox"] = "on"
    if criteria.noRestricts_only:
        data["ctl00$pageContent$noRestrictionsCheckBox"] = "on"
    if criteria.no_pre_req:
        data["ctl00$pageContent$noPrerequisitesCheckBox"] = "on"
    data["ctl00$pageContent$searchButton"] = "Begin Search"
                   
    result = ses.post(GOLD_SEARCH_URL, data=data)
    download(result, DEFAULT_DOWNLOAD_PATH, file_name)    
    

def match_quarter(quarter):
    if not quarter:
        return ""
    str = "".join(quarter.split(" "))
    if "winter" in str:
        return str.replace("winter","").strip() + "1"
    if "spring" in str:
        return str.replace("spring","").strip() + "2"
    if "summer" in str:
        return str.replace("summer","").strip() + "3"
    if "fall" in str:
        return str.replace("fall","").strip() + "4"

def match_session(session):
    if not session:
        return ""    
    return "ALL"


def match_department(department):
    if not department:
        return ""
    if department == "any":
        return ""
    return department.split("-")[1].strip().ljust(5)


def match_subject(subject):
    return match_department(subject)


def match_course_level(course_level):
    if not course_level:
        return ""
    if course_level == "any":
        return ""
    return course_level.replace("undergraduate", "U")\
                       .replace(" lower division", "L")\
                       .replace(" upper division", "U")\
                       .replace("graduate", "G")


def match_hours(meet_hours):
    if not meet_hours:
        return ""
    if meet_hours == "any":
        return ""
    hr = int(meet_hours.split(":")[0])%12
    if meet_hours[-2] == "p":
        return str(hr+12) + "00"
    return str(hr) + "00"


COLLEGE_OF_CREATIVE_STUDIES = "ccs"
COLLEGE_OF_ENGINEERING = "coe"
COLLEGE_OF_ENVIRON_SCI_MGMT = "esm"
GRADUATE_DIVISION = "grad"
GRADUATE_SCHOOL_OF_EDUCATION = "gse"
COLLEGE_OF_LETTERS_AND_SCIENCE = "l&s"
NO_COLLEGE = "no"
def match_GE(GE):
    if not GE:
        return ""
    if GE == COLLEGE_OF_CREATIVE_STUDIES:
        return "CRST"
    if GE == COLLEGE_OF_ENGINEERING:
        return "ENGR"
    if GE == COLLEGE_OF_ENVIRON_SCI_MGMT:
        return "ESM "
    if GE == GRADUATE_DIVISION:
        return "GRAD"
    if GE == GRADUATE_SCHOOL_OF_EDUCATION:
        return "GSE "
    if GE == COLLEGE_OF_LETTERS_AND_SCIENCE:
        return "L&S "
    if GE == NO_COLLEGE:
        return "NO  "


def match_area(area):
    return area.upper().strip().ljust(3)


def download(response, dir, file_name):

    # Write data to file
    path = dir + file_name + ".html"
    file_ = open(path, 'w')
    file_.write(response.text)
    file_.close()
    
    
def login_and_fetch_search():
    s = login()
    r = s.get(GOLD_SEARCH_URL)
    download(r, DEFAULT_GOLD_FILE_PATH, "search")
