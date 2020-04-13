import os, requests, time, getpass
from bs4 import BeautifulSoup

class_name = "MATH"
DEFAULT_GOLF_FILE_PATH = "../../html/GOLDForms/"
DEFAULT_DOWNLOAD_PATH = "../../html/raw/"
GOLD_LOGIN_URL = "https://my.sa.ucsb.edu/gold/"
GOLD_LOGIN_FORM = "../../html/GOLDForms/login/"
GOLD_SEARCH_URL = "https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx"
GOLD_SEARCH_FORM = "../../html/GOLDForms/search/"


def save(path,soup_file):
    with open(path, "w") as outf:
        outf.write(str(soup_file))


def login():
    
    with open(GOLD_LOGIN_FORM + "login.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        
    #IO user and pass
    user = soup.find(id="pageContent_userNameText")
    user['value'] = input("Username: ")

    password = soup.find(id="pageContent_passwordText")
    password['value'] = getpass.getpass(prompt="Password: ")

    #saves the file and replaces the user and password values
    save(GOLD_LOGIN_FORM + "login.html",soup)
    
    cmd = "echo open " + GOLD_LOGIN_FORM + "login.html"
    os.system(cmd)

    time.sleep(2)
    #reset
    user['value'] = ""
    password['value'] = ""
    save(GOLD_LOGIN_FORM + "login.html",soup)


def download(url, dir, file_name):
    
    r = requests.get(url)    
    # Write data to file
    path = dir + file_name
    if not os.path.exists(path):
        os.mkdir(path)
    path += "\\" + file_name + ".html";
    file_ = open(path, 'w')
    file_.write(r.text)
    file_.close()


def login_and_fetch_search():
    if not os.path.exists(GOLD_LOGIN_FORM + "login.html"):
        download(GOLD_LOGIN_URL, DEFAULT_GOLF_FILE_PATH, "login")
    login()
    if not os.path.exists(GOLD_SEARCH_FORM + "search.html"):
        download(GOLD_SEARCH_URL, DEFAULT_GOLF_FILE_PATH, "search")


def main():
    login_and_fetch_search()
    

if __name__ == "__main__":
    main()
