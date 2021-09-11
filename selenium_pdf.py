import selenium.webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import json

class TimetableFetch:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("-headless")        
        self.driver = Firefox(firefox_options=self.options)
        self.unknown = []
        self.ignored = ['športni', 'dan', '-', 'Posočje', 'športni', 'dan', '-', 'Posočje', 'ekskurzija', 'na', 'Koroško', 'športni', 'dan', '–', 'Bohinj', 'sistematski', 'pregled', 'študijsko', 'potovanje', 'v', 'Španijo', 'študijsko', 'potovanje', 'v', 'Španijo', 'URE', '7.20', '-', '8.05', '8.10', '-', '8.55', '9.00', '-', '9.45', '10.05', '-', '10.50', '10.55', '-', '11.40', '11.45', '-', '12.30', '12.35', '-', '13.20', '13.50', '-', '14.35', '13.00', '-', '13.45', 'f']
        self.matura = ['mO1/nOV/', 'n4/š1/š3a', 'geo1/nOV/š2', 'mV2/mO3\r\n/n3/š3b', 'mO1/nOV/\nn4/š1/š3a', 'geo1/nOV\n/š2', 'mV2/mO3\n/n3/š3b', 'n1/psi1', 'n26/š3c6/geo26/bio1/']
   
    def get_timetable(self):
        timetable =  self.extract_json(self.get_text())
        [print("unknown subject: "+subject) for subject in self.unknown if not subject in self.ignored]
        return timetable

    def get_text(self):
        self.driver.get("https://gz.zelimlje.si/wp-content/uploads/sites/2/2021/09/Urnik_teden.pdf")
        time.sleep(2)
        self.driver.find_element_by_xpath("/html").send_keys(Keys.CONTROL, "a")
        self.driver.find_element_by_xpath("/html").send_keys(Keys.CONTROL, "c")
        return pyperclip.paste()

    def extract_json(self, text):
        timetable = {}
        classes = ["1.a", "1.b", "2.a", "2.b", "2.c", "3.a", "3.b", "4.a", "4.b", "4.c"]
        for i,school_class in enumerate(classes):
            next_class = ""
            if len(classes) < i + 2:
                next_class = " 1 2 3 4 5 6 7 8 "
            else:
                next_class = classes[i+1]
            timetable[school_class] = self.extract_timetable(school_class, next_class, text)
        return timetable
            
    def extract_timetable(self,school_class, next_class, text):

        subjects = json.load(open("subjects.json", "r", encoding="utf-8"))
        timetable = []
        for day in text.split(school_class)[1:]:
            day = day.split(next_class)[0].replace("ru (ŠP)", "ru(ŠP)").strip()
            day_timetable = []
            for subject in day.split(" "):
                subject = subject.strip()
                if subject:
                    if subject in subjects or any([sub in subjects for sub in subject.split("/")]):
                        day_timetable.append(subject)
                    elif subject not in self.ignored and subject not in self.matura:
                        self.unknown.append(subject)
            timetable.append(day_timetable)
        return timetable

if __name__ == "__main__":
    t =TimetableFetch()

    with open("extracted.json", "w") as f:
        json.dump(t.get_timetable(), f, indent=3)