import sys
import requests
from bs4 import BeautifulSoup
import re
import json


# Page for the major course links are grabbed from
url = "https://catalog.stcloudstate.edu/programs/YD9I0SxsSAzcG6Z0yCiV"
page = requests.get(url)
# Use the html parser when searching through the tags
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="s12RL")  # Resrict the search to the given div element
# Further resrict the search for course links
course = results.find("article", class_="main-content")
linklist = []
courseID = []
results_list = []
#courseName = sys.argv[1]

# Grabs every course link in the resricted area
for links in course.find_all('a'):
    link = links.get('data-course-id')  # Get the unique id for every course
    name = links.text
    name = name.replace(" ", "")  # Remove whitespace in course name
    # print("https://catalog.stcloudstate.edu/courses/" + link) # Since the link in each 'a' tag is a proper link, had to hard code in most of the link, then add the courses's unique id to direct the user to the correct page
    linklist.append("https://catalog.stcloudstate.edu/courses/" + link)
    courseID.append(name)


def findCourse(courseName):
    if courseName in courseID:
        linkpr = courseID.index(courseName)
        return linklist[linkpr]


def buildJson():
    all_results = []
    for i in range(len(linklist)):
        current_dict = {}

        current_course = courseID[i]
        current_link = linklist[i]
        current_dict["CourseID"] = current_course
        current_dict["ExternalLink"] = current_link

        all_results.append(current_dict)
    getAllDescriptions(all_results)
    return all_results


def getDescriptionFromUrl(url):
    page = requests.get(url)
    # Use the html parser when searching through the tags
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.get_text()
    # Find the "Description" heading, then get next elements
    description_heading = soup.find('dt', text=re.compile("Description"))
    description = description_heading.next_element.next_element.next_element.get_text()
    return description


def getAllDescriptions(results_list):
    for course in results_list:
        desc = getDescriptionFromUrl(course["ExternalLink"])
        course["Description"] = desc


# For running the script as a standalone program:
if __name__ == "__main__":
    results_list = buildJson()
    with open('course_metadata.json', 'w') as f:
        json.dump(results_list, f, indent=4)
