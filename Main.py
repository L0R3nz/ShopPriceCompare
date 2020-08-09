import json
import random
import csv

from time import sleep
from CeneoGrabber import getCeneoPrice
from os import path, remove
from io import TextIOWrapper

def create_database():
    
    item_list = []
    
    with open('WHR_Shop/Categories.json','r', encoding='utf-8') as json_file:
        for category in json.load(json_file):
            with open('WHR_Shop/{0}.json'.format(category['Id']),'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                for p in data['data']:
                    
                    row = {}
                    row['product_id']   = p['productId'];
                    row['ceneo_id']     = find_ceneo_id(p['productId'])
                    row['category']     = category['Name'];
                    row['available']    = p['available'];
                    row['brand']        = p['brand'];
                    row['model']        = p['title'];
                    row['price_whr']    = p['price'];
                    
                    item_list.append(row)
         

    save_file("DataBase.json",item_list)
    

def find_ceneo_id(product_id):
    
    for row in read_file("CeneoConnection.json"):
        if(row['ID'] == int(product_id)):
            return row['Ceneo_ID']
    
    return -1


def read_file(file_path):
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    return data


def save_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def create_report():
    
    report_list = []
     
    for item in read_file('DataBase.json'):
         
        if((item['available'] == True) and (item['ceneo_id'] != -1)):
             
            item['ceneo_price']  = getCeneoPrice(item['ceneo_id']);
            report_list.append(item)

            wait_time = random.randint(60, 5*60) # wait from 1 minute to 5 minutes to avoid captcha on ceneo.pl
            
            print("Wait {0:<3} sec | {1}".format(wait_time, item))
            save_file("Report.json", report_list)
            sleep(wait_time)
    

def analize_data(data):
    
    for item in data:
        item['whr_discount'] = round(item['ceneo_price'] - item['price_whr'],2)
        item['whr_discount_percent'] = round((item['whr_discount']/item['ceneo_price'])*100,2)
    return data           


def generate_csv(path, data):
    
    with open(path, 'wb') as csv_file, TextIOWrapper(csv_file, encoding='utf-8', newline='') as wrapper:
        
        writer = csv.writer(wrapper, quoting=csv.QUOTE_ALL)
        writer.writerow(data[0].keys())
        
        for data_row in data:
            writer.writerow(data_row.values())

            

def BuildReport(clean_build = False):
    
    if(clean_build == True):
        remove("DataBase.json")
        remove("Report.json")
    
    # Generate DataBase.json file which have product details and ceneo_id
    if(path.exists("DataBase.json") == False):
        print("Create DataBase.json")
        create_database()
    else:
        print("Skipped because DataBase.json exist")
        
    # Generate Report.json file which have product details and data grabbed from ceneo.pl
    if(path.exists("Report.json") == False):
        print("Create Report.json")
        create_report()
    else:
        print("Skipped because Report.json exist")

    
    # Analize data and calculate statistics
    save_file("Report.json", analize_data(read_file("Report.json")))
    
    # Create CSV file
    generate_csv("Report.csv", read_file("Report.json"))


BuildReport()
