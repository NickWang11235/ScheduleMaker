import os
import time
from bs4 import BeautifulSoup

def save(path,soup_file):
    with open(path, "w") as outf:
        outf.write(str(soup_file))

def login():
    html_path = "/Users/bindingoath/Desktop/Projects/ScheduleMaker420/scraper/GOLD.html"

    with open(html_path) as fp:
        soup = BeautifulSoup(fp)
    #IO user and pass
    user = soup.find(id="pageContent_userNameText")
    user['value'] = input("Username: ")

    password = soup.find(id="pageContent_passwordText")
    password['value'] = input("Password: ")

    #saves the file and replaces the user and password values
    save(html_path,soup)
    
    cmd = "open " + html_path
    os.system(cmd)

    time.sleep(2)
    #reset
    user['value'] = ""
    password['value'] = ""
    save(html_path,soup)