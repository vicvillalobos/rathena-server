# Script in python to transform some items in the Renewal database
# to the pre-renewal database as costume items.
# Note that the items will use the renewal texts for the description, slot, etc.

# The script will not change the item ID, so beware of that.

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="ragnarok",
  password="ragnarok"
)

print(mydb)

# Select the database
mycursor = mydb.cursor()
mycursor.execute("USE ragnarok")
# Select the table
mycursor.execute("SELECT * FROM item_db2")

# Fetch all rows
myresult = mycursor.fetchall()

# Print the first 10 rows
for row in myresult[:10]:
    print(row)
    
# Close the cursor and connection
mycursor.close()
mydb.close()
#



