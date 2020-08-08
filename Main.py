import json

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
            return row['ID']
    
    return -1


def read_file(file_path):
    with open(file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    return data


def save_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



create_database()

