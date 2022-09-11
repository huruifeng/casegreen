## Function library

import requests
from bs4 import BeautifulSoup
import re

months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

# LIN – Lincoln Service Center (Nebraska Service Center)
# EAC – Eastern Adjudication Center (Vermont Service Center)
# IOE – USCIS Electronic Immigration System (ELIS)
# WAC – Western Adjudication Center (California Service Center)
# MSC – Missouri Service Center (National Benefits Center)
# NBC – National Benefits Center
# SRC – Southern Regional Center (Texas Service Center)
# YSC - Potomac Service Center
center_names = ["MSC",	"LIN","SRC", "WAC", "EAC", "IOE", "YSC"]

form_types = [
	"I-129CW",
    "I-129F",
	"I-600A",
	"I-601A",
	"I-765V",
	"I-485J",
	"I-800A",
	"I-821D",
	"I-90",
	"I-102",
	"I-129",
	"I-130",
	"I-131",
	"I-140",
	"I-212",
	"I-360",
	"I-485",
	"I-526",
	"I-539",
	"I-600",
	"I-601",
	"I-612",
	"I-730",
	"I-751",
	"I-765",
	"I-800",
	"I-817",
	"I-821",
	"I-824",
	"I-829",
	"I-914",
	"I-918",
	"I-924",
	"I-929"
    ]

def get_status(recepit_number):
    ## Test
    # recepit_number="LIN2290104917"

    url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
    case_data = {"appReceiptNum": recepit_number}

    try_n = 0
    while True:
        ## Try N times at most
        resp = requests.post(url, data=case_data)
        try_n += 1
        if resp.status_code in [200]:
            break
        else:
            if try_n >=10:
                return ["try_failed"]

    soup = BeautifulSoup(resp.text, 'html.parser')
    status_div=soup.find("div",class_="rows text-center")
    if status_div:
        ## case exists
        status_h_text = status_div.h1.get_text(strip=True)
        if status_h_text.strip() == "":
            return ["error", "invlid_num"]

        status_p_text = status_div.p.get_text()
        status_p_text_ls = re.split(" |,", status_p_text)
        status_p_text_ls = [i for i in status_p_text_ls if i]

        date=""
        form=""
        n_words = len(status_p_text_ls)
        for i in range(n_words):
            if status_p_text_ls[i] in months:
                date = status_p_text_ls[i] + " " + status_p_text_ls[i+1]+", " + status_p_text_ls[i+2]
            elif status_p_text_ls[i] == "Form":
                form = status_p_text_ls[i+1]
                break
        if form == "":
            for form_x in form_types:
                if form_x in status_p_text:
                    form = form_x
                    break
        if date!="":
            status_p_text = status_p_text.replace(date, "<u>"+date+"</u>")
        if form!="":
            status_p_text = status_p_text.replace(form, "<u>"+form+"</u>")

        status_p_text = status_p_text.replace(recepit_number, "<u>"+recepit_number+"</u>")
        return [form, date,status_h_text,status_p_text]
    else:
        ## the case number is invlid
        return ["error","invlid_num"]