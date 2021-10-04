import os
import re
from lxml import *
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

# dir_path = os.path.dirname(os.path.realpath(__file__))
root = tk.Tk()
root.withdraw
file_path = filedialog.askopenfilename()

with open(file_path, 'rb') as html:
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

#section that parses subreq info
subrequirements = soup.find_all('div', class_="subrequirement")
for subreq in subrequirements:
    subreq_id = subreq['id'] #id of the sub_req
    if subreq['pseudo']: 
        subreq_course_title = subreq['pseudo']  #title of the subreq
        print(subreq_course_title)
    print(subreq_id)

    #finds credits for completed subreq
    subreq_body = subreq.find('div', class_="subreqBody")
    subreq_completed_courses = subreq_body.find('table', class_="completedCourses")
    if subreq_completed_courses:
        comp_courses_info = subreq_completed_courses.find('tbody')
        course_credits_total = comp_courses_info.find("td", class_="credit")
        course_credits_total = course_credits_total.contents
        if course_credits_total:
            print(f"Completed Credit Total: {course_credits_total}")


    #suggested courses for incomplete subreq
    subreq_selected_courses = subreq_body.find('table', class_="selectcourses")
    if subreq_selected_courses:
        selected_courses_info = subreq_selected_courses.find('tbody')
        course_list = selected_courses_info("span", class_="number")
        for course in course_list:
            course = course.contents
            print(f"Suggsted course: {course}")




    #finds the status of the subreq --refactor later
    subreq_pretext = subreq.find('div', class_="subreqPretext")
    subreq_status = subreq_pretext.find('span', class_=f"status Status_IP")
    if subreq_status:
        statlist = subreq_status["class"]
        if "Status_IP" in statlist:
            print("In progress\n")

    subreq_status = subreq_pretext.find('span', class_=f"status Status_OK")
    if subreq_status:
        statlist = subreq_status["class"]
        if "Status_OK" in statlist:
            print("Completed\n")

    subreq_status = subreq_pretext.find('span', class_=f"status Status_NO")
    if subreq_status:
        statlist = subreq_status["class"]
        if "Status_NO" in statlist:
            print("Incomplete\n")
    
# print("\n---Completed--")
# for course in soup.find_all('span', class_="subreqTitle srTitle_substatusOK"):
#     print(course.text)
# print("\n---In-Progress--")
# for course in soup.find_all('span', class_="subreqTitle srTitle_substatusIP"):
#     print(course.text)
# print("\n--Incomplete--")
# for course in soup.find_all('span', class_="subreqTitle srTitle_substatusIP"):
#     print(course.text)
 
# #section that parses requirments info
# requirements  = soup.find('div', id="auditRequirements") #class bs4 tag
# for req in requirements:
#     req_id = req['id']
#     print(req_id)
