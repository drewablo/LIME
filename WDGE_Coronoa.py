import requests
import re
from lxml import html
import time
from os import system
previousSymbol = 0
totalCasesPrevious = 0
totalDeathsPrevious = 0
UScasesPrevious = 0
USopenTestsPrevious = 0

totalCaseChange = 0
totalDeathChange = 0
UScasesChange = 0 
USopenChange = 0

def symbolUpdate(caseChange):
    global previousSymbol
    if caseChange != 0:
        if caseChange > 0:
            previousSymbol = "\u25b2"
        elif caseChange < 0:
            previousSymbol = "\u25BE"
    else:
        previousSymbol = previousSymbol
    return previousSymbol
    
while True:
    response = requests.get("https://www.worldometers.info/coronavirus/")
    byte_data = response.content 
    source_code = html.fromstring(byte_data) 
    tree = source_code.xpath('//*[@id="maincounter-wrap"]/div/span')
    tree2 = source_code.xpath('//*[@id="maincounter-wrap"][2]/div/span')
    
    response2 = requests.get("https://www.cdc.gov/coronavirus/2019-ncov/cases-in-us.html")
    byte_data2 = response2.content 
    source_code2 = html.fromstring(byte_data2) 
    tree3 = source_code2.xpath('/html/body/div[6]/main/div[3]/div/div[3]/div[1]/div/div/div/div[2]/table/tbody/tr[1]/td')
    tree4 = source_code2.xpath('/html/body/div[6]/main/div[3]/div/div[3]/div[1]/div/div/div/div[2]/table/tbody/tr[3]/td')
    
    totalCasesReturn = tree[0].text_content()
    totalDeathsReturn = tree2[0].text_content()
    UScasesReturn = tree3[0].text_content()
    USopenTestsReturn = tree4[0].text_content()
    
    totalCaseChange = int(re.findall("\d+",totalCasesReturn)[0]) - totalCasesPrevious
    totalDeathChange = int(re.findall("\d+",totalDeathsReturn)[0]) - totalDeathsPrevious
    UScasesChange = int(re.findall("\d+",UScasesReturn)[0]) - UScasesPrevious
    USopenChange = int(re.findall("\d+",USopenTestsReturn)[0]) - USopenTestsPrevious
    
    update_time = time.localtime()
    t = time.asctime(update_time)
        
    if totalCaseChange != 0 or totalDeathChange != 0 or UScasesChange !=0 or USopenChange !=0:
        system('cls')
        print("Total Cases: " + totalCasesReturn + " " + symbolUpdate(totalCaseChange)) 
        print("Total Deaths: " + totalDeathsReturn + " " + symbolUpdate(totalDeathChange)) 
        print("US Cases: " + UScasesReturn + " " + symbolUpdate(UScasesChange)) 
        print("US Open Tests: " + USopenTestsReturn + " " + symbolUpdate(USopenChange)) 
        print("LAST CHANGE: " + t[:-4])
    totalCasesPrevious = int(re.findall("\d+",totalCasesReturn)[0])
    totalDeathsPrevious = int(re.findall("\d+",totalDeathsReturn)[0])
    UScasesPrevious = int(re.findall("\d+",UScasesReturn)[0])
    USopenTestsPrevious = int(re.findall("\d+",USopenTestsReturn)[0])

    time.sleep(10)
