import json
import pdfplumber
import requests
from datetime import datetime as dt


class TimetableFetch:
    def __init__(self):
        self.unknown = []
        self.ignored = ['športni', 'dan', '-', 'Posočje', 'športni', 'dan', '-', 'Posočje', 'ekskurzija', 'na', 'Koroško', 'športni', 'dan', '–', 'Bohinj', 'sistematski', 'pregled', 'študijsko', 'potovanje', 'v', 'Španijo', 'študijsko', 'potovanje', 'v', 'Španijo', 'URE', '7.20', '-', '8.05', '8.10', '-', '8.55', '9.00', '-', '9.45', '10.05', '-', '10.50', '10.55', '-', '11.40', '11.45', '-', '12.30', '12.35', '-', '13.20', '13.50', '-', '14.35', '13.00', '-', '13.45', 'f']
        self.matura = ['mO1/nOV/', 'n4/š1/š3a', 'geo1/nOV/š2', 'mV2/mO3\r\n/n3/š3b', 'mO1/nOV/\nn4/š1/š3a', 'geo1/nOV\n/š2', 'mV2/mO3\n/n3/š3b', 'n1/psi1', 'n26/š3c6/geo26/bio1/']
   
    def get_timetable(self):
        timetable =  self.extract_json(self.get_text())
        [print("unknown subject: "+subject) for subject in self.unknown if not subject in self.ignored]
        return timetable

    def get_text(self):
        d = dt.now()
        content = requests.get("https://gz.zelimlje.si/wp-content/uploads/sites/2/2021/" + d.strftime("%m") + "/Urnik_teden.pdf").content

        with open("tmp.pdf", "wb") as f:
            f.write(content)
            f.close()

        pdf = pdfplumber.open("tmp.pdf")

        page = pdf.pages[0]
        text =page.extract_text()
        return text

    def extract_json(self, text):
        timetable = {}
        classes = ["1.a", "1.b", "2.a", "2.b", "2.c", "3.a", "3.b", "4.a", "4.b", "4.c"]
        for i,school_class in enumerate(classes):
            next_class = ""
            if len(classes) < i + 2:
                next_class = "1  2  3  4  5  6  7  8"
            else:
                next_class = classes[i+1]
            timetable[school_class] = self.extract_timetable(school_class, next_class, text)
        return timetable
            
    def extract_timetable(self,school_class, next_class, text):
        subjects = json.load(open("./assets/subjects.json", "r"))
        timetable = []
        for day in text.split(school_class)[1:]:
            day = day.split(next_class)[0].replace("ru (ŠP)", "ru(ŠP)").strip()
            day_timetable = []
            for subject in day.split(" "):
                subject = subject.strip()
                if subject:
                    if subject in subjects or any([sub in subjects for sub in subject.split("/")]) and len(subject.split("/")) < 2:
                        day_timetable.append(subject)
                    elif subject not in self.ignored and subject not in self.matura:
                        self.unknown.append(subject)
            timetable.append(day_timetable)
        return timetable

class PersonalizedTimetable:
    def __init__(self):
        self.t=TimetableFetch()
        self.classes = json.load(open("./assets/classes.json", "r"))
        self.matura_timetable = json.load(open("./assets/matura_timetable.json", "r"))
        self.subjects = json.load(open("./assets/subjects.json", "r"))
        self.timetable_a = json.load(open("./assets/timetable_a.json", "r"))

    def easy_compare(self, str):
        return str.strip().lower().replace("č", "c").replace("š", "s").replace("ž", "z")

    def formate_timetable(self, first_name, second_name, timetable, class_name=False):
        if not class_name:
            class_name = self.get_class(first_name, second_name)[0]
            
        class_timetable = timetable[class_name]

        if class_name.split(".")[0] == "4":
            person_matura_timetable = self.matura_timetable[self.easy_compare(first_name) + " " + self.easy_compare(second_name)]
            return self.formate_matura_timetable(class_timetable, person_matura_timetable)
        
        return class_timetable

    def get_class(self,first_name, second_name):
        first_name = self.easy_compare(first_name)
        second_name = self.easy_compare(second_name)
        middle_name = ""
        if len(first_name.split(" "))==2:
            middle_name = first_name.split(" ")[1][0] + ". "
        name_in_classes = first_name.split(" ")[0] + " " + middle_name + second_name
        found_classes = []
        for class_name, name_list in self.classes.items():
            for name in name_list:
                if name_in_classes in self.easy_compare(name) and class_name not in found_classes:
                    found_classes.append(class_name)
        return found_classes

    def get_gender(self, first_name, second_name):
        return self.matura_timetable[self.easy_compare(first_name) + " " + self.easy_compare(second_name)]["gender"]
    
    def formate_matura_timetable(self, timetable, matura_timetable):
        person_timetable = []
        for i, day in enumerate(timetable):
            if day:
                if i == 0:
                    print([matura_timetable["subjects"][0]], day)
                    day = [matura_timetable["subjects"][0]] + day
                if i == 1:
                    day = day + matura_timetable["subjects"][1:4]
                if i == 2:
                    day = matura_timetable["subjects"][4:6] + day + [matura_timetable["subjects"][-1]]
                if i == 3:
                    day = [matura_timetable["subjects"][9]] + matura_timetable["subjects"][6:8] + day + [matura_timetable["subjects"][8]]
                if i == 4:
                    day = day + matura_timetable["subjects"][10:12]
            person_timetable.append(day)
        return person_timetable

    def get_personalized_timetable(self, first_name, second_name, class_name = False, online=True):
        timetable = json.load(open("./assets/timetable_a.json", "r"))
        if online:
            timetable = self.t.get_timetable()
        return self.formate_timetable(first_name, second_name, timetable, class_name)

if __name__ == "__main__":
    t =TimetableFetch()

    p = PersonalizedTimetable()
    print(p.get_class("aja", "knež"))
    print(p.formate_timetable("aja", "knez", t.get_timetable()))


    # with open("extracted.json", "w") as f:
    #     json.dump(t.get_timetable(), f, indent=3)