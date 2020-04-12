import requests
import os
from bs4 import BeautifulSoup

def download(class_name):
    
    r = requests.get('https://my.sa.ucsb.edu/gold/CriteriaFindCourses.aspx')

    # Write data to file
    filename = os.path.join("html_downloads", class_name + ".html")
    file_ = open(filename, 'w')
    file_.write(r.text)
    file_.close()




