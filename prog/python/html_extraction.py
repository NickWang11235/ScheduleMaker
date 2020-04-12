from bs4 import BeautifulSoup

html = None

with open("../../html/example_search/Find Course Results.html", "r") as f:

    doc = f.read()
    html = BeautifulSoup(doc, "html.parser")

data_table = html.find("div", "cd-schedule").find("div", "datatableNew")

preprocess = data_table.find_all("div")
postprocess = []
for tag in preprocess:
    if tag["class"][0] == "courseSearchHeader" or tag["class"][0] == "courseSearchItem":
        postprocess.append(tag)

for data in postprocess:
    if data["class"][0] == "courseSearchHeader":
        print("\n")
        title = data.find("span", "courseTitle").get_text()
        units_and_grading = data.find_all("span", "pr5")
        title += " " + units_and_grading[0].get_text() + " " + units_and_grading[1].get_text()
        print(title)
    if data["class"][0] == "courseSearchItem":
        indent = "  "
        lecture_id = data.find("div", "row info")["data-target"].strip().split(',')[0][6:]
        days = " ".join(data.find("div", "col-lg-search-days col-sm-push-1 col-md-days col-sm-days col-xs-2").get_text().split())
        time = " ".join(data.find("div", "col-lg-search-time col-sm-push-1 col-md-time col-sm-time col-xs-5").get_text().split())
        print(indent + lecture_id + " " + days + " " + time)
