import sqlite3

connection = sqlite3.connect('teams.db')
cursor = connection.cursor()

# query = '''
#     CREATE TRIGGER IF NOT EXISTS update_timestamp
#     AFTER UPDATE ON games
#     FOR EACH ROW
#     UPDATE my_table 
#     SET last_updated = CURRENT_TIMESTAMP 
#     WHERE id = OLD.id;
#     '''

# # Execute the query
# cursor.execute(query)

q2 = '''
INSERT INTO db_info (version, creation_date, last_modified)
VALUES ('0.0.1', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
'''

cursor.execute(q2)

connection.commit()

connection.close()