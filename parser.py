from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw
file_path = filedialog.askopenfilename()

with open(file_path, 'rb') as html:
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

print("\n---Completed--")
for course in soup.find_all('span', class_="subreqTitle srTitle_substatusOK"):
    print(course.text)
print("\n---In-Progress--")
for course in soup.find_all('span', class_="subreqTitle srTitle_substatusIP"):
    print(course.text)
print("\n--Incomplete--")
for course in soup.find_all('span', class_="subreqTitle srTitle_substatusIP"):
    print(course.text)
 

