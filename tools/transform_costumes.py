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

