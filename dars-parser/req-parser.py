import sys
import json
import re
from lxml import *
from bs4 import BeautifulSoup
from bs4 import *
from jsonmerge import merge

# defines the schema of the json
# this is where we create json dicts


def createJson(req_id, course_name, course_type, status, weight, isCourse, semester):
    data = {}
    data["ID"] = str(req_id).strip()
    data["CourseID"] = str(req_id)
    data["isCourse"] = isCourse
    data["Name"] = str(course_name)
    data["Type"] = str(course_type)
    data["ExternalLink"] = "N/A"
    data["Description"] = "N/A"
    data["Weight"] = int(float(weight))
    data["Prereqs"] = "Unknown"
    data["Status"] = str(status)
    data["Semester"] = str(semester)
    return data


def parse_file(filePath):  # returns a list of json dicts
    with open(filePath, 'rb') as html:
        soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    parsed_data = []

    # rather than parsing indivual courses in the dars, we parse the requirements
    requirements = soup.find('div', id="auditRequirements")
    for requirement in requirements:
        # navigable strings were empty
        if str(type(requirement)) != "<class 'bs4.element.NavigableString'>":
            attr_list = requirement.get_attribute_list('class')
            if "category_Major" in attr_list:  # checks if this requirement is part of major

                if requirement["rname"]:  # checks if req. is an elective or a program core
                    req_type = requirement["rname"]
                    if "ELEC" in req_type:
                        req_type = "Elective"
                    else:
                        req_type = "ProgramCore"

                # looks into subrequirements. of a req
                # for example SE MATH req. has subreqs: Discrete Math, Calc 1, etc.
                # subreq parsings
                subrequirements = requirement.find_all(
                    "div", class_="subrequirement")
                for subrequirement in subrequirements:
                    temp_json = {}
                    if subrequirement["pseudo"]:  # courseID
                        subreq_id = subrequirement["pseudo"]
                        subreq_id = subreq_id.strip()
                        subreq_id = subreq_id.replace(" ", "")

                    # find course status
                    incomplete = ""
                    complete = ""
                    inprogress = ""

                    subreq_body = subrequirement.find(
                        'div', class_="subreqBody")  # parse body of subreq

                    if subreq_body:  # finds status of subreq i.e complete or inprogress
                        incomplete = subreq_body.find(
                            'span', class_="subreqTitle srTitle_substatusNO")
                        complete = subreq_body.find(
                            'span', class_="subreqTitle srTitle_substatusOK")
                        inprogress = subreq_body.find(
                            'span', class_="subreqTitle srTitle_substatusIP")

                    if incomplete:
                        subreq_status = "Incomplete"
                        course_weight = 0
                        # incomplete_course_list = subreq_body.find_all("span", class_="number")
                        course_name = subreq_body.find(
                            "span", class_="subreqTitle srTitle_substatusNO")
                        course_name = course_name.contents
                        course_name = course_name[0].strip()

                        pattern = "[A-Z]{2,4}" + "\d" + str({3})
                        result = re.match(pattern, subreq_id)
                        if result:
                            isCourse = True
                        else:
                            isCourse = False

                        semester = "N/A"

                        # index = 0
                        # course_list = []

                        # for course in incomplete_course_list:
                        #     courses = course.contents
                        #     courses = courses[index]
                        #     index += index
                        #     course_list.append(courses)
                        # course_names = course_list

                        temp_json = createJson(
                            subreq_id, course_name, req_type, subreq_status, course_weight, isCourse, semester)

                    if complete or inprogress:
                        course_table = subreq_body.find(
                            'table', class_="completedCourses")

                        # find subreq status
                        for item in course_table:
                            status_tag = course_table.find(
                                'td', class_="ccode")
                            subreq_status = status_tag.contents
                            course_weight = course_table.find(
                                'td', class_="credit")
                            course_weight = course_weight.contents[0]
                            if subreq_status:
                                subreq_status = subreq_status[0]
                                if 'IP' in subreq_status:
                                    subreq_status = "In-progress"
                            else:
                                subreq_status = "Completed"

                            # find subreq course-name
                            course_name = course_table.find(
                                'td', class_="descLine")
                            if course_name:
                                course_name = course_name.contents
                                if course_name:
                                    course_name = course_name[0]
                                else:
                                    course_name = 'N/A'

                            # finds semester course was taken
                            semester = course_table.find('td', class_="term")
                            if semester:
                                semester = semester.contents
                                if semester:
                                    semester = semester[0]
                                    semester = semester.strip()
                                    semester = semester.replace(" ", "")
                                else:
                                    semester = 'N/A'

                            pattern = "[A-Z]{2,4}" + "\d" + str({3})
                            result = re.match(pattern, subreq_id)
                            if result:
                                isCourse = True
                            else:
                                isCourse = False

                        temp_json = createJson(
                            subreq_id, course_name, req_type, subreq_status, course_weight, isCourse, semester)
                    if temp_json:
                        parsed_data.append(temp_json)
                    else:
                        continue
    return parsed_data  # list of json dicts


# reads json file from webscraper and returns the result of merging them based on courseID
def scrape_course_description(data):
    with open('course_metadata.json') as json_file:
        course_metadata = json.load(json_file)

    for req in data:
        if req["isCourse"]:
            courseid = req["CourseID"]
            for course in course_metadata:
                cid = course["CourseID"]
                if courseid == cid:
                    req.update(course)

    with open('dars_data.json', 'w') as f:  # writes merged data to json file
        json.dump(data, f, indent=4)

    print(json.dumps(data, indent=4))


filePath = sys.argv[1]
# filePath = "/Users/williamdoyle/Documents/Development/demo1/demo1/audit.html"
data = parse_file(filePath)
scrape_course_description(data)
