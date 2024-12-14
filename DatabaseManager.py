import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        """Initialize the DatabaseManager with the path to the SQLite database."""
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print("Database connected successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    
    def execute_query(self, query, params=None):
        """
        Execute a single query that doesn't return data.
        Example: INSERT, UPDATE, DELETE.
        """
        if self.cursor:
            try:
                self.cursor.execute(query, params or ())
                self.connection.commit()
                print("Query executed successfully.")
            except sqlite3.Error as e:
                print(f"Error executing query: {e}")
                
    def get_head_to_head_results(self):
        query = '''
        SELECT c1.name AS winner_conference, 
           c2.name AS loser_conference, 
           COUNT(*) AS games_played,
           SUM(CASE WHEN g.winner = t1.name THEN 1 ELSE 0 END) AS wins,
           SUM(CASE WHEN g.loser = t2.name THEN 1 ELSE 0 END) AS losses
        FROM games g
        JOIN team t1 ON g.winner = t1.name
        JOIN team t2 ON g.loser = t2.name
        JOIN conference c1 ON t1.conference_id = c1.id
        JOIN conference c2 ON t2.conference_id = c2.id
        WHERE (c1.name IN ('Big Ten', 'SEC', 'ACC', 'Big East', 'Big 12'))
        AND (c2.name IN ('Big Ten', 'SEC', 'ACC', 'Big East', 'Big 12'))
        GROUP BY c1.name, c2.name;
        '''

        # Execute the query
        self.cursor.execute(query)

        # Fetch all results
        power_conference_games = self.cursor.fetchall()
        
        return power_conference_games

        