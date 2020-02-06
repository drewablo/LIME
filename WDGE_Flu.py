import requests
import re
import locale
from lxml import html
import time
from os import system

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

totalCasesPrevious = 0
totalDeathsPrevious = 0
totalHospitalizationsPrev = 0


totalCaseChange = 0
totalDeathChange = 0
totalHospitalizationsChange = 0 
    


def averageNumbers(xPathContent):
    numbersList = re.findall("(?:^|\s)(\d*\.?\d+|\d{1,3}(?:,\d{3})*(?:\.\d+)?)(?!\S)",xPathContent)
    # Credit where credit is due :https://stackoverflow.com/questions/5917082/regular-expression-to-match-numbers-with-or-without-commas-and-decimals-in-text
    lowNumb = numbersList[0]
    highNumb = numbersList[1]
    avg = int((int(highNumb.replace(',', '')) + int(lowNumb.replace(',', '')))/2)
    return avg
    

while True:
    response = requests.get("https://www.cdc.gov/flu/about/burden/preliminary-in-season-estimates.htm")
    byte_data = response.content 
    source_code = html.fromstring(byte_data) 

    rawSick = source_code.xpath("/html/body/div[6]/main/div[3]/div/div[4]/div[2]/div[1]/div/div/h4/strong[1]")
    rawHospital = source_code.xpath("/html/body/div[6]/main/div[3]/div/div[4]/div[3]/div[1]/div/div/h4/strong[1]")
    rawDeaths = source_code.xpath("/html/body/div[6]/main/div[3]/div/div[4]/div[3]/div[2]/div/div/h4/strong[1]")
    
    rawSickReturn = rawSick[0].text_content()
    rawHospitalReturn = rawHospital[0].text_content()
    rawDeathsReturn = rawDeaths[0].text_content()
    
    update_time = time.localtime()
    t = time.asctime(update_time)
    
    totalCaseChange = averageNumbers(rawSickReturn)- totalCasesPrevious
    totalDeathChange = averageNumbers(rawHospitalReturn) - totalDeathsPrevious
    totalHospitalizationsChange = averageNumbers(rawDeathsReturn)- totalHospitalizationsPrev
    
    if totalCaseChange != 0 or totalDeathChange != 0 or totalHospitalizationsChange !=0:
        print("INFLUENZA")
        print("IN THE USA")
        print("Infections: " + str(f'{averageNumbers(rawSickReturn):n}'))
        print("Hospitalizations: " + str(f'{averageNumbers(rawHospitalReturn):n}'))
        print("Deaths: " + str(f'{averageNumbers(rawDeathsReturn):n}'))
        print("LAST CHANGE: " + t[:-4])
        
    totalCasesPrevious = int(re.findall("\d+",rawSickReturn)[0])
    totalDeathsPrevious = int(re.findall("\d+",rawHospitalReturn)[0])
    totalHospitalizationsPrev = int(re.findall("\d+",rawDeathsReturn)[0])

    time.sleep(300)
