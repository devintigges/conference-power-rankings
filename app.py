from flask import Flask, render_template
from DatabaseManager import DatabaseManager

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    db_manager = DatabaseManager('teams.db')
    db_manager.connect()
    
    head_to_head_data = db_manager.get_head_to_head_results()
    conferences = ['Big Ten', 'SEC', 'ACC', 'Big East', 'Big 12']
    
    table = {conference: {other_conference: {'wins': 0, 'losses': 0} for other_conference in conferences} for conference in conferences}

    # Populate the table with the win/loss data
    for row in head_to_head_data:
        winner, loser, games_played, wins, losses = row
        if winner in conferences and loser in conferences:
            table[winner][loser]['wins'] = wins
            table[loser][winner]['losses'] = losses

    return render_template('index.html', table=table, conferences=conferences)
# Run the app
if __name__ == "__main__":
    app.run(debug=True)