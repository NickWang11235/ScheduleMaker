import html_extraction

DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
OUTPUT_DEFAULT_FOLDER = "../../html/parsed/"

#class to store all the scheduling advanced variables
class criteria:
    def __init__(self):
        self.data = {
            "quarter" : "spring2020",
            "session" : "",
            "department" : "",
            "subject" : "",
            "course_num" : "",
            "course_level" : "",
            "meet_begin" : "",
            "meet_end" : "",
            "days" : [1, 1, 1, 1, 1, 1, 1],
            "unit_min" : "0",
            "unit_max" : "12",
            "enrollment" : "",
            "instructor" : "",
            "title" : "",
            "GE" : "",
            "area" : "",
            "open_sections" : "",
            "matching_sections" : "",
            "no_restricts_only" : "",
            "no_pre_req" : "",
            "pretty" : False
        }


def run(args, crit):
    if len(args) == 0:
        print(generate_err_msg())
    handle_commands(map_commands(args),crit)

CRITERIA_VALUES = html_extraction.enumerate_data_field(DEFAULT_GOLD_FILE_PATH + "search.html")

def map_commands(args):
    dict = {}
    i = 0
    while i < len(args):
        if(is_command(args[i])):
            argl = args[i][1:].split("=")

            if argl[0] in CRITERIA_VALUES:
                dict[argl[0]] = argl[1]
                i += 1
                continue

            if argl[0] == "help" and ((i+1 < len(args) and args[i+1][0] == "-") or (i+1 == len(args))):
                dict.update({argl[0] : ""})
                i += 1
                continue

            if argl[0] in CMD_ARGS:
                if CMD_ARGS[argl[0]]["r_data"]:
                    if CMD_ARGS[argl[0]]["equals"]:
                        dict[argl[0]] = argl[1]
                    else:
                        dict[argl[0]] = args[i+1]
                        i += 1
                else:
                    dict[argl[0]] = ""
                i += 1
            else:
                error_illegal_command(argl[0])
        else:
            error_illegal_option(args[i])
    return dict


def is_command(cmd):
    return cmd[0] == "-"


def validate_command_format(cmd):
    return cmd in CMD_ARGS


def handle_commands(cmds, criteria):
    for cmd in cmds:
        if cmd in CRITERIA_VALUES:
            validate_criteria_commands(cmd, cmds[cmd], criteria)
            update_criteria(cmd, cmds[cmd], criteria)
            continue
        if cmd == "pretty":
            pretty(cmds[cmd], criteria)
            continue
        if cmd == "help":
            help(cmds[cmd])
        if cmd == "list":
            list()
            continue


def pretty(arg, criteria):
    if arg.lower() == "true":
        criteria.data["pretty"] = True
    elif arg.lower() == "false":
        criteria.data["pretty"] = False
    else:
        error_illegal_argument("-pretty", arg)


def help(arg):
    if not arg:
        st = "This is a schedule maker for UCSB. It will take your criteria and fetch a list of classes that fits your descriptions,\nand make a schedule for you. You will enter your commands following the module name to specify the criteria of the class\nyour wish to search for and some specifications. You will be asked to enter your UCSB GOLD account username and password,\nand a list of all sutiable schedule will be generated."
        print(st + "\n" + generate_err_msg())
    else:
        if arg in CMD_ARGS:
            st = "usage: main.py " + generate_command_usage(arg) + "\n"
            st += "  Require arguments: " + str(CMD_ARGS[arg]["require_args"]) + "\n"
            st += "  Left hand side is data field: " + CMD_ARGS[arg]["l_data"] + "\n"
            st += "  Right hand side is data field: " + CMD_ARGS[arg]["r_data"] + "\n"
            st += "  Description: " + CMD_ARGS[arg]["info"] + "\n"
            print(st)
        else:
            error_illegal_argument("-help", arg)


def list():
    print("Listing all values for criteria fields: ")
    for key in CRITERIA_VALUES:
        print("option for -" + key)
        for val in CRITERIA_VALUES[key]:
            print("  " + val)


CMD_ARGS = {
        "criteria" : { "require_args" : True, "equals" : True, "l_data" : "criteria", "r_data" : "value", "info" : "Enter a criteria field with a value. ex '-department=math'"} ,
        "pretty" : { "require_args" : True, "equals" : True, "l_data" : "", "r_data" : "value", "info" : "Accepts either True/Fals to toggle output to txt"} ,
        "help" : { "require_args" : True, "equals" : False, "l_data" : "", "r_data" : "command", "info" : "Provides general information for the package and usage for commands"} ,
        "list" : { "require_args" : False, "equals" : False, "l_data" : "", "r_data" : "", "info" : "List out all possible fields and values for criteria option"} ,
    }

def generate_command_usage(cmd):
    str = "[-"
    if CMD_ARGS[cmd]["l_data"]:
        str += "<" + CMD_ARGS[cmd]["l_data"] + ">"
    else:
        str += cmd

    if CMD_ARGS[cmd]["equals"]:
        str += "="
    elif CMD_ARGS[cmd]["r_data"]:
        str += " "

    if CMD_ARGS[cmd]["r_data"]:
        str += "<" + CMD_ARGS[cmd]["r_data"] + ">"
    str += "] "
    return str


def generate_err_msg():
    str = "usage: main.py "
    for e in CMD_ARGS:
        str += generate_command_usage(e)
    return str + "\n   for help, pass in command -help \n   for help on a command, run -help <command>"



def error_illegal_option(error):
    str = "error: " + error + " is not an option\n" + generate_err_msg()
    print(str)
    exit(1)


def error_illegal_command(error):
    str = "error: " + error + " is not a recognized command\n" + generate_err_msg()
    print(str)
    exit(1)


def error_illegal_argument(command, error):
    str = "error: " + error + " is not a recongized argument for " + command + "\n" + generate_err_msg()
    print(str)
    exit(1)


def validate_criteria_commands(cmd, arg, criteria):
    if(cmd == "quarter"):
        if(not validate_quarter(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "session"):
        if(not validate_session(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "department"):
        if(not validate_department(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "subject"):
        if(not validate_subject(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "course_num"):
        if(not validate_course_num(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "course_level"):
        if(not validate_course_level(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "meet_begin"):
        if(not validate_meet_begin(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "meet_end"):
        if(not validate_meet_end(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "days"):
        if(not validate_days(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "unit_min"):
        if(not validate_unit_min(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "unit_max"):
        if(not validate_unit_max(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "enrollment"):
        if(not validate_enrollment(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "instructor"):
        if(not validate_instructor(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "title"):
        if(not validate_title(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "GE"):
        if(not validate_GE(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "area"):
        if(not validate_area(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "open_sections"):
        if(not validate_open_sections(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "matching_sections"):
        if(not validate_matching_sections(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "no_restricts_only"):
        if(not validate_no_restricts_only(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "no_pre_req"):
        if(not validate_no_pre_req(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)

    elif(cmd == "pretty"):
        if(not validate_pretty(cmd, arg, criteria)):
            error_illegal_argument("-"+cmd, arg)
            

def validate_quarter(key, arg, criteria):
    season = arg[0:-4]
    year = arg[-4:]
    combine = season + " " + year

    if(combine.lower() in (str(CRITERIA_VALUES[key]).lower())):
        update_criteria(key, arg, criteria)
        return True
    else:
        return False
        

def validate_session(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_department(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_subject(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_course_num(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_course_level(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_meet_begin(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_meet_end(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_days(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_unit_min(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_unit_max(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_enrollment(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_instructor(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_title(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_GE(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_area(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_open_sections(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_matching_sections(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_no_restricts_only(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_no_pre_req(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def validate_pretty(key, arg, criteria):
    if arg.lower() in str(CRITERIA_VALUES[key]).lower():
        update_criteria(key, arg, criteria)
        return True
    else:
        return False


def update_criteria(cmd, arg, criteria):
    criteria.data[cmd] = arg


def request_input(data):
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
