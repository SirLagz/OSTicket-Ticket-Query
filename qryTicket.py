#!/usr/bin/python
import mysql.connector

dbUser = 'ostuser'
dbPass = 'Chisholm1'
dbServer = '127.0.0.1'
dbName = 'ost'

db = mysql.connector.connect(user=dbUser,password=dbPass,host=dbServer,database=dbName)

cursor = db.cursor()
# Customise the below line to retrieve the tickets you require.
cursor.execute('select ticket_id from ost_ticket WHERE (topic_id=20 OR topic_id=30);')

# Run a loop on the tickets from the query above
tickets = cursor.fetchall()
type(tickets)
for tuple in tickets:
    ticket = tuple[0]
    # Customise the below line to get certain fields. The 'serial' and 'equip' fields that I've specified below are custom fields that I've put in, so yours will differ.
    cursor.execute("select label,value from ost_form_entry as t1 INNER JOIN ost_form_entry_values as t2 ON t1.id=t2.entry_id INNER JOIN ost_form_field as t3 ON t2.field_id = t3.id INNER JOIN ost_ticket as t4 ON t1.object_id=t4.ticket_id WHERE ticket_id="+str(ticket)+" AND (label = 'Serial Number' OR label = 'Equipment Type') ORDER BY label DESC;")

    info = cursor.fetchall()
    serial = info[0][1]
    equip = info[1][1]
    # Customise below line if you want more than just the first note on the ticket
    cursor.execute("select body from ost_ticket INNER JOIN ost_thread ON ost_ticket.ticket_id = ost_thread.object_id INNER JOIN ost_thread_entry on ost_thread.id = ost_thread_entry.thread_id WHERE ticket_id="+str(ticket)+" ORDER BY ost_thread_entry.id ASC LIMIT 1")

    lThread = cursor.fetchall()
    desc = lThread[0][0]

    body = """Do stuff with below information...

Equipment Type:
"""+equip+"""

Serial Number:
"""+serial+"""

Issue:
"""+desc+"""
"""
    print body


db.close()
