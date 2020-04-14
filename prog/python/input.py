import html_extraction

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

#class to store all the scheduling advanced variables
class criteria:
    
    def __init__(self, quarter):
        self.quarter = quarter
        self.session = ""
        self.department = ""
        self.subject = ""
        self.course_num = ""
        self.course_level = ""
        self.meet_begin = ""
        self.meet_end = ""
        self.days = [1, 1, 1, 1, 1, 1, 1]
        self.unit_min = "0"
        self.unit_max = "12"
        self.enrollment = ""
        self.instructor = ""
        self.title = ""
        self.GE = ""
        self.area = ""
        self.open_sections = ""
        self.matching_sections = ""
        self.noRestricts_only = ""
        self.no_pre_req = ""


def request_quarter():
    value = input("First, please enter the quarter: ")
    data = criteria(value)
    return data

def request_input(data):
    dic = html_extraction.enumerate_data_field(DEFAULT_GOLD_FILE_PATH + "search/search.html")
    #while loop to get all the conditions
    while True:
        inputed = input("Please enter a flag followed by the desired specification. \
        \nAvailable Flags: \
        \n  -department \
        \n  -subject \
        \n  -courseNum \
        \n  -courseLevel \
        \n  -meetBegin \
        \n  -meetEnd \
        \n  -daysOfWeek (Ex. 00101 for Wednesday and Friday. 1s for days available and 0s for not)\
        \n  -unitMin \
        \n  -unitMax \
        \n  -enrollmentCode \
        \n  -instructor \
        \n  -title \
        \n  -geCollege \
        \n  -geArea \
        \n  -openSections (True or False)\
        \n  -matchingSections (True or False)\
        \n  -noRestrictsOnly (True or False)\
        \n  -noPreReq (True or False)\
        \n  exit when done \
        \nExample Input: -department CHEM \
        \nInput: ")

        splitInput = inputed.split()

        #Replacement for switch statement
        if (splitInput[0] == "-department"):
            data.department = splitInput[1]

        elif (splitInput[0] == "-subject"):
            data.subject = splitInput[1]

        elif (splitInput[0] == "-courseNum"):
            data.courseNum = int(splitInput[1])

        elif (splitInput[0] == "-courseLevel"):
            data.courseLevel = splitInput[1]

        elif (splitInput[0] == "-meetBegin"):
            data.meetBegin = int(splitInput[1])

        elif (splitInput[0] == "-meetEnd"):
            data.meetEnd = int(splitInput[1])

        elif (splitInput[0] == "-daysOfWeek"):
            data.days = [int(x) for x in str(num)]

        elif (splitInput[0] == "-unitMin"):
            data.unitMin = int(splitInput[1])

        elif (splitInput[0] == "-unitMax"):
            data.unitMax = int(splitInput[1])

        elif (splitInput[0] == "-enrollmentCode"):
            data.Enrollment = int(splitInput[1])

        elif (splitInput[0] == "-instructor"):
            data.Instructor = splitInput[1]

        elif (splitInput[0] == "-title"):
            data.Title = splitInput[1]

        elif (splitInput[0] == "-geCollege"):
            data.GE = splitInput[1]

        elif (splitInput[0] == "-geArea"):
            data.geArea = splitInput[1]

        elif (splitInput[0] == "-openSections"):
            if(splitInput[1] == "True"):
                data.openSections = True
            else:
                data.openSections = False

        elif (splitInput[0] == "-matchingSections"):
            if(splitInput[1] == "True"):
                data.matchingSections = True
            else:
                data.matchingSections = False

        elif (splitInput[0] == "-noRestrictsOnly"):
            if(splitInput[1] == "True"):
                data.noRestrictsOnly = True
            else:
                data.noRestrictsOnly = False

        elif (splitInput[0] == "-noPreReq"):
            if(splitInput[1] == "True"):
                data.noPreReq = True
            else:
                data.noPreReq = False

        elif (splitInput[0] == "exit"):
            break

        else:
            print("Invalid Input")

    return data
