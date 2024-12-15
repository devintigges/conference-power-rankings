from DatabaseManager import DatabaseManager
import requests
from bs4 import BeautifulSoup

class Scraper:
    
    def get_game_data():
        # URL of the page to scrape
        url = 'https://www.ncaa.com/scoreboard/basketball-men/d1/2024/12/14/all-conf'

        # Send an HTTP request to fetch the page content
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all games with class "gamePod status-final" which indicates the game is final
            games = soup.find_all('div', class_='gamePod gamePod-type-game status-final')

            for game in games:
                # Find the team names and scores
                teams = game.find_all('span', class_='gamePod-game-team-name')
                scores = game.find_all('span', class_='gamePod-game-team-score')

                # Ensure there are two teams and two scores
                if len(teams) == 2 and len(scores) == 2:
                    # Identify the winner and loser by checking for class 'winner'
                    winner_team = None
                    loser_team = None
                    winner_score = None
                    loser_score = None

                    for i, team in enumerate(teams):
                        if 'winner' in team.find_parent('li')['class']:
                            winner_team = team.text.strip()
                            winner_score = scores[i].text.strip()
                        else:
                            loser_team = team.text.strip()
                            loser_score = scores[i].text.strip()

                    # Print the result if we identified both winner and loser
                    if winner_team and loser_team:
                        db_manager = DatabaseManager('teams.db')
                        db_manager.connect()
                        db_manager.add_game(winner_team, loser_team)
        else:
            print(f"Failed to retrieve the page, status code: {response.status_code}")
