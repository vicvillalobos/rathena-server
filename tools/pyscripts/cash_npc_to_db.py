# Reads shops from a rathena script file and
# writes them to a item_cash.yml file
from yaml import load, dump
import mysql.connector
from alive_progress import alive_bar

def get_item_name(item_id, cursor):
    # Select the item name from the database
    cursor.execute("SELECT name_aegis FROM item_db WHERE id = %s UNION SELECT name_aegis FROM item_db2 WHERE id = %s", (item_id, item_id))
    result = cursor.fetchall()
    
    if result and len(result) > 0:
        return result[0][0]
    else:
        return None

with open("./cashshop.txt", "r") as f:
    lines = f.readlines()

shop_items = []    

for line in lines:
    npcdata = line.split("\t")
    
    npc_shop = npcdata[-1].split(",")
    npc_items = npc_shop[1:]
    
    for item in npc_items:
        item = item.split(":")
        item_id = item[0]
        item_amount = item[1]
        
        if int(item_id) == 0:
            continue
        
        shop_items.append({
            "id": int(item_id),
            "amount": int(item_amount)
        })

cash_object = {
    "Header": {
        "Type": "ITEM_CASH_DB",
        "Version": 1,
    },
    "Body": [
        {
            "Tab": "New",
            "Items": []
        }  
    ],
    "Footer": {
        "Imports": [
            {
                "Path": "db/import/item_cash.yml",
            }
        ]
    }
}

mydb = mysql.connector.connect(
        host="ec2-54-196-161-223.compute-1.amazonaws.com",
        user="ragnarok",
        password="ragnarok"
    )

mycursor = mydb.cursor()
mycursor.execute("USE ragnarok")

with alive_bar(len(shop_items), title="Processing items") as bar:
    for item in shop_items:
        print("Getting name for item ID:", item["id"])
        item_name = get_item_name(item["id"], mycursor)
        if item_name is None:
            print("Item ID not found in database:", item["id"])
            bar()
            continue
        print("Item name:", item_name)
        # Append the item to the cash object
        cash_object["Body"][0]["Items"].append({
            "Item": item_name,
            "Price": item["amount"]
        })
        bar()
    
mycursor.close()
mydb.close()

with open("./item_cash.yml", "w") as f:
    f.write(dump(cash_object, sort_keys=False, default_flow_style=False, allow_unicode=True))