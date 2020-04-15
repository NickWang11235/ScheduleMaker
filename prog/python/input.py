import html_extraction

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
GOLD_SEARCH_FORM = "../../html/GOLDForms/search/search.html"

HTML_DEFAULT_NAME = "/Find Course Results.html"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

#class to store all the scheduling advanced variables
class mySchedule:
    def __init__(self, quarter):
        self.quarter = quarter
        self.department = ""
        self.subject = ""
        self.course_num = 0
        self.course_level = ""
        self.meet_begin = 8
        self.meet_end = 23
        self.days = [1, 1, 1, 1, 1]
        self.unit_min = 0
        self.unit_max = 12
        self.enrollment = 0
        self.instructor = ""
        self.title = ""
        self.GE = ""
        self.area = ""
        self.open_sections = False
        self.matching_sections = False
        self.noRestricts_only = False
        self.no_pre_req = False

dic = html_extraction.extract_search_form_data_field(GOLD_SEARCH_FORM)

def validationQuarter(inputed_commands):
    if(len(inputed_commands.split()) != 1):
        print("Invalid number of commands")

    temp = inputed_commands.split('=')
    key = temp[0][1:]
    season = temp[1][0:-4]
    year = temp[1][-4:]

    combine = season + " " + year

    if(not combine in dic[key]):
        print("Invalid Input")
        exit(2)
    

def validation(inputed_commands):
    for a in range(len(inputed_commands)):
        temp = inputed_commands[a].split('=')
        key = temp[0][1:]
        specification = temp[1]

        #help1()
        #help2()

        if(not specification in str(dic[key])):
            print("Invalid Input")
            exit(2)


def help1():
    print("Available Flags: ")
    for key in dic:
        print(key)

def help2():
    for key in dic:
        for str in dic[key]:
            print(str)
        print("\n")


value = input("First, please enter the quarter(ex. -quarter=Spring2020 ): ")
validationQuarter(value)
storage = mySchedule(value.split('=')[1])


#Replacement for switch statement
def switch(inputed_commands):
    for a in range(len(inputed_commands)):
        temp = inputed_commands[a].split('=')
        if (temp[0] == "-department"):
            storage.department = temp[1]


        elif (temp[0] == "-subject"):
            storage.subject = temp[1]


        elif (temp[0] == "-courseNum"):
            storage.courseNum = int(temp[1])


        elif (temp[0] == "-courseLevel"):
            storage.courseLevel = temp[1]


        elif (temp[0] == "-meetBegin"):
            storage.meetBegin = int(temp[1])


        elif (temp[0] == "-meetEnd"):
            storage.meetEnd = int(temp[1])


        elif (temp[0] == "-daysOfWeek"):
            storage.days = [int(x) for x in str(temp[1])]


        elif (temp[0] == "-unitMin"):
            storage.unitMin = int(temp[1])


        elif (temp[0] == "-unitMax"):
            storage.unitMax = int(temp[1])


        elif (temp[0] == "-enrollmentCode"):
            storage.Enrollment = int(temp[1])


        elif (temp[0] == "-instructor"):
            storage.Instructor = temp[1]


        elif (temp[0] == "-title"):
            storage.Title = temp[1]


        elif (temp[0] == "-geCollege"):
            storage.GE = temp[1]


        elif (temp[0] == "-geArea"):
            storage.geArea = temp[1]


        elif (temp[0] == "-openSections"):
            if(temp[1] == "True"):
                storage.openSections = True
            else:
                storage.openSections = False


        elif (temp[0] == "-matchingSections"):
            if(temp[1] == "True"):
                storage.matchingSections = True
            else:
                storage.matchingSections = False


        elif (temp[0] == "-noRestrictsOnly"):
            if(temp[1] == "True"):
                storage.noRestrictsOnly = True
            else:
                storage.noRestrictsOnly = False


        elif (temp[0] == "-noPreReq"):
            if(temp[1] == "True"):
                storage.noPreReq = True
            else:
                storage.noPreReq = False

#while loop to get all the conditions
while True:
    inputed = input("Please enter a flag followed by the desired specification. \
    \n -help1 for available flags \
    \n -help2 for available specifications \
    \n exit to stop \
    \nExample Input: -department=CHEM \
    \nInput: ")

    splitInput = inputed.split()


    if(splitInput[0] == "-help1"):
        help1()
        continue

    elif(splitInput[0] == "-help2"):
        help2()
        continue

    elif (splitInput[0] == "exit"):
        break
    
    else:
        validation(splitInput)

    switch(splitInput)
