import os, requests, time, getpass, shutil
from bs4 import BeautifulSoup

class_name = "MATH"
DEFAULT_GOLD_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"


def save(path,soup_file):
    with open(path, "w") as outf:
        outf.write(str(soup_file))


def login():

    with requests.Session() as s:
        #DO NOT TOUCH
        datas = {
            "__VIEWSTATE" : "/wEPDwUKMTM5OTE1ODA1Ng9kFgJmD2QWAgIDD2QWCmYPDxYCHgdWaXNpYmxlaGQWAgIBD2QWAgIBDw8WAh8AaGRkAgEPFgIfAGhkAgIPFgIfAGhkAgMPZBYMAgIPDxYCHwBoZGQCAw8PZBYCHgxhdXRvY29tcGxldGUFA29mZmQCBA8PZBYCHwEFA29mZmQCBg9kFgJmD2QWBAIBDw8WAh8AaGRkAgcPFgIfAGhkAgcPDxYCHgtOYXZpZ2F0ZVVybAUtLy9teS5zYS51Y3NiLmVkdS9QZXJtUGluUmVzZXQvRm9yZ290UGVybS5hc3B4ZGQCCA8PFgIfAgUvLy9teS5zYS51Y3NiLmVkdS9QZXJtUGluUmVzZXQvUGVybVBpblJlc2V0LmFzcHhkZAIEDw8WAh8AaGQWAgIBD2QWAgIBDw8WAh8AaGRkZFWCuJoPk7ARvPD4xG4fSJedZVYd" ,
            "__VIEWSTATEGENERATOR" : "00732C32" ,
            "__EVENTVALIDATION" : "/wEdAAdbKm4OU/lsarSPEWzw3woTFPojxflIGl2QR/+/4M+LrK6wLDfR+5jffPpLqn7oL3ttZruIm/YRHYjEOQyILgzL2Nu6XIik3f0iXq7Wqnb39/ZNiE/A9ySfq7gBhQx160NmmrEFpfb3YUvL+k7EbVnKgIKH2XlDUw30P837MyfVDMpYxIk=" ,
            "ctl00$pageContent$userNameText" : "wang271" ,
            "ctl00$pageContent$passwordText" : "fzm5Ekjq4VRPdQF" ,
            "ctl00$pageContent$loginButton" : "Login"
        }
        
        username = input("Username: ")
        password = getpass.getpass(prompt="Password: ")
        datas["ctl00$pageContent$userNameText"] = username
        datas["ctl00$pageContent$passwordText"] = password
        s.post(GOLD_LOGIN_URL, data=datas)
        return s



def download(response, dir, file_name):
       
    # Write data to file
    path = dir + file_name
    if not os.path.exists(path):
        os.mkdir(path)
    path += "\\" + file_name + ".html";
    file_ = open(path, 'w')
    file_.write(response.text)
    file_.close()


def login_and_fetch_search():
    s = login()
    r = s.get(GOLD_SEARCH_URL)
    download(r, DEFAULT_GOLD_FILE_PATH, "search")


def main():
    login_and_fetch_search()
    #shutil.rmtree(DEFAULT_GOLD_FILE_PATH, ignore_errors=True)
    

if __name__ == "__main__":
    main()
