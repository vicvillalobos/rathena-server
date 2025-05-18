# Script in python to transform some items in the Renewal database
# to the pre-renewal database as costume items.
# Note that the items will use the renewal texts for the description, slot, etc.

# The script will not change the item ID, so beware of that.

import mysql.connector

class ItemRenewal:
    def __init__(self, id, name_aegis, name_english, type, subtype, price_buy, price_sell, weight, location_costume_head_top, location_costume_head_mid, location_costume_head_low, location_costume_garment, view):
        self.id = id
        self.name_aegis = name_aegis
        self.name_english = name_english
        self.type = type
        self.subtype = subtype
        self.price_buy = price_buy
        self.price_sell = price_sell
        self.weight = weight
        self.location_costume_head_top = location_costume_head_top
        self.location_costume_head_mid = location_costume_head_mid
        self.location_costume_head_low = location_costume_head_low
        self.location_costume_garment = location_costume_garment
        self.view = view
        
    def __str__(self):
        return f"ItemRenewal (id={self.id}, name_aegis={self.name_aegis})"

    def generate_prerenewal_insert(self):
        # Generate the insert statement for the pre-renewal database
        return f"INSERT INTO item_db2 (id, name_aegis, name_english, type, subtype, price_buy, price_sell, weight, location_costume_head_top, location_costume_head_mid, location_costume_head_low, location_costume_garment, view, armor_level) VALUES ({self.id}, '{self.name_aegis}', '{self.name_english}', {self.type}, {self.subtype}, {self.price_buy}, {self.price_sell}, {self.weight}, {self.location_costume_head_top}, {self.location_costume_head_mid}, {self.location_costume_head_low}, {self.location_costume_garment}, {self.view}, 1);"
    
    

mydb = mysql.connector.connect(
  host="localhost",
  user="ragnarok",
  password="ragnarok"
)

print(mydb)

# Select the database
mycursor = mydb.cursor()
mycursor.execute("USE ragnarok")

# Select all costume items from renewal database
mycursor.execute("SELECT id, name_aegis, name_english, type, subtype, price_buy, price_sell, weight, location_costume_head_top, location_costume_head_mid, location_costume_head_low, location_costume_garment, view, armor_level FROM `item_db_re` WHERE location_costume_head_top IS NOT NULL OR location_costume_head_mid IS NOT NULL OR location_costume_head_low IS NOT NULL OR location_costume_garment IS NOT NULL")

# Fetch all rows
myresult = mycursor.fetchall()

# Print the first 10 rows
for row in myresult:
    item = ItemRenewal(*row)
    print(item)
    # Generate the insert statement for the pre-renewal database
    insert_statement = item.generate_prerenewal_insert()
    print(insert_statement)
    # Execute the insert statement
    mycursor.execute(insert_statement)
    # Commit the changes to the database
mydb.commit()
# Print the number of rows inserted
print(mycursor.rowcount, "rows inserted into item_db2")
    
# Close the cursor and connection
mycursor.close()
mydb.close()
#



