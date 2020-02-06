import requests
import re
from lxml import html
from time import sleep

totalCasesPrevious = 0
totalDeathsPrevious = 0
UScasesPrevious = 0
USopenTestsPrevious = 0

totalCaseChange = 0
totalDeathChange = 0
UScasesChange = 0 
USopenChange = 0

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
    
    treereturn = tree[0].text_content()
    tree2return = tree2[0].text_content()
    tree3return = tree3[0].text_content()
    tree4return = tree4[0].text_content()
    
    totalCaseChange = int(re.findall("\d+",treereturn)[0]) - totalCasesPrevious
    totalDeathChange = int(re.findall("\d+",tree2return)[0]) - totalDeathsPrevious
    UScasesChange = int(re.findall("\d+",tree3return)[0]) - UScasesPrevious
    USopenChange = int(re.findall("\d+",tree4return)[0]) - USopenTestsPrevious
    

    print("Global Cases: " + treereturn) 
    print("Global Deaths: " + tree2return) 
    print("United States Cases: " + tree3return) 
    print("US Pending Cases: " + tree4return) 
    
    print("GC Change: " + str(totalCaseChange))
    print("Death Change: " + str(totalDeathChange))
    print("US Cases Change: " + str(totalCaseChange))
    print("US Open Test Change: " + str(totalCaseChange))
    
    totalCasesPrevious = int(re.findall("\d+",treereturn)[0])
    totalDeathsPrevious = int(re.findall("\d+",tree2return)[0])
    UScasesPrevious = int(re.findall("\d+",tree3return)[0])
    USopenTestsPrevious = int(re.findall("\d+",tree4return)[0])

    sleep(5)
