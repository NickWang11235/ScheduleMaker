#class to store all the scheduling advanced variables
class mySchedule:

    def __init__(quarter):
        quarter = quarter
        department == "None"
        subject == "None"
        courseNum = 0
        courseLevel == "None"
        meetBegin = 8
        meetEnd = 23
        days = [1, 1, 1, 1, 1]
        unitMin = 0
        unitMax = 12
        Enrollment = 0
        Instructor == "None"
        Title == "None"
        GE == "None"
        Area == "None"
        openSections = False
        matchingSections = False
        noRestrictsOnly = False
        noPreReq = False

value = input("First, please enter the quarter: ")
storage = mySchedule(value);

#while loop to get all the conditions
while true
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
    if (splitInput[0] == "-department")
        storage.department = splitInput[1]

    elif (splitInput[0] == "-subject"):
        storage.subject = splitInput[1]

    elif (splitInput[0] == "-courseNum"):
        storage.courseNum = int(splitInput[1])

    elif (splitInput[0] == "-courseLevel"):
        storage.courseLevel = splitInput[1]

    elif (splitInput[0] == "-meetBegin"):
        storage.meetBegin = int(splitInput[1])

    elif (splitInput[0] == "-meetEnd"):
        storage.meetEnd = int(splitInput[1])

    elif (splitInput[0] == "-daysOfWeek"):
        storage.days = [int(x) for x in str(num)]

    elif (splitInput[0] == "-unitMin"):
        storage.unitMin = int(splitInput[1])

    elif (splitInput[0] == "-unitMax"):
        storage.unitMax = int(splitInput[1])

    elif (splitInput[0] == "-enrollmentCode"):
        storage.Enrollment = int(splitInput[1])

    elif (splitInput[0] == "-instructor"):
        storage.Instructor = splitInput[1]

    elif (splitInput[0] == "-title"):
        storage.Title = splitInput[1]

    elif (splitInput[0] == "-geCollege"):
        storage.GE = splitInput[1]

    elif (splitInput[0] == "-geArea"):
        storage.geArea = splitInput[1]

    elif (splitInput[0] == "-openSections"):
        if(splitInput[1] == "True"):
            storage.openSections = True
        else
            storage.openSections = False

    elif (splitInput[0] == "-matchingSections"):
        if(splitInput[1] == "True"):
            storage.matchingSections = True
        else
            storage.matchingSections = False

    elif (splitInput[0] == "-noRestrictsOnly"):
        if(splitInput[1] == "True"):
            storage.noRestrictsOnly = True

        else
            storage.noRestrictsOnly = False

    elif (splitInput[0] == "-noPreReq"):
        if(splitInput[1] == "True"):
            storage.noPreReq = True
        else
            storage.noPreReq = False

    elif (splitInput[0] == "exit"):
        break

    else:
        print("Invalid Input")
