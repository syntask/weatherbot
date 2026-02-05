import requests
import json
from datetime import datetime

def get_live_nfl_games():
    """Fetch live NFL games and their scores from ESPN API"""
    try:
        response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
        response.raise_for_status()
        data = response.json()
        
        live_games = []
        
        # Check each event for live games
        for event in data.get('events', []):
            status = event.get('status', {})
            status_type = status.get('type', {})
            
            # Check if game is in progress (state = "in")
            if status_type.get('state') == 'in':
                game_info = extract_game_info(event)
                live_games.append(game_info)
        
        return live_games, data.get('week', {}).get('number', 'Unknown')
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return [], 'Unknown'

def extract_game_info(event):
    """Extract relevant information from a game event"""
    competition = event.get('competitions', [{}])[0]
    competitors = competition.get('competitors', [])
    
    # Get team information and scores
    away_team = competitors[0] if len(competitors) > 0 else {}
    home_team = competitors[1] if len(competitors) > 1 else {}
    
    game_info = {
        'id': event.get('id'),
        'name': event.get('name'),
        'short_name': event.get('shortName'),
        'status': event.get('status', {}),
        'away_team': {
            'name': away_team.get('team', {}).get('displayName', 'Unknown'),
            'abbreviation': away_team.get('team', {}).get('abbreviation', 'UNK'),
            'score': away_team.get('score', '0'),
            'logo': away_team.get('team', {}).get('logo', '')
        },
        'home_team': {
            'name': home_team.get('team', {}).get('displayName', 'Unknown'),
            'abbreviation': home_team.get('team', {}).get('abbreviation', 'UNK'),
            'score': home_team.get('score', '0'),
            'logo': home_team.get('team', {}).get('logo', '')
        },
        'clock': competition.get('status', {}).get('displayClock', '0:00'),
        'period': competition.get('status', {}).get('period', 0),
        'venue': competition.get('venue', {}).get('fullName', 'Unknown Venue'),
        'broadcast': competition.get('broadcast', 'Unknown')
    }
    
    return game_info

def display_live_games(live_games, week_number):
    """Display live games in a formatted way"""
    print(f"\n🏈 NFL WEEK {week_number} - LIVE GAMES")
    print("=" * 60)
    
    if not live_games:
        print("No games currently live.")
        return
    
    for i, game in enumerate(live_games, 1):
        status = game['status']
        status_detail = status.get('type', {}).get('detail', 'In Progress')
        
        print(f"\nGame {i}: {game['short_name']}")
        print(f"📍 Venue: {game['venue']}")
        print(f"📺 Broadcast: {game['broadcast']}")
        print(f"⏰ Status: {status_detail}")
        print(f"🕐 Clock: {game['clock']} - Period {game['period']}")
        print(f"")
        print(f"  {game['away_team']['abbreviation']:<4} {game['away_team']['score']:>3}  |  {game['away_team']['name']}")
        print(f"  {game['home_team']['abbreviation']:<4} {game['home_team']['score']:>3}  |  {game['home_team']['name']}")
        print("-" * 40)

def get_all_games_summary(data):
    """Show summary of all games for the week"""
    print(f"\n📊 ALL GAMES SUMMARY - WEEK {data.get('week', {}).get('number', 'Unknown')}")
    print("=" * 60)
    
    status_counts = {'scheduled': 0, 'live': 0, 'completed': 0}
    
    for event in data.get('events', []):
        status_state = event.get('status', {}).get('type', {}).get('state', 'unknown')
        
        if status_state == 'pre':
            status_counts['scheduled'] += 1
        elif status_state == 'in':
            status_counts['live'] += 1
        elif status_state == 'post':
            status_counts['completed'] += 1
    
    print(f"Scheduled: {status_counts['scheduled']}")
    print(f"Live: {status_counts['live']}")
    print(f"Completed: {status_counts['completed']}")
    print(f"Total: {sum(status_counts.values())}")

def show_upcoming_games(data, limit=5):
    """Show next few upcoming games"""
    print(f"\n📅 NEXT UPCOMING GAMES")
    print("=" * 60)
    
    upcoming_games = []
    
    for event in data.get('events', []):
        status_state = event.get('status', {}).get('type', {}).get('state', 'unknown')
        
        if status_state == 'pre':  # Scheduled games
            game_time = event.get('date')
            status_detail = event.get('status', {}).get('type', {}).get('detail', '')
            short_detail = event.get('status', {}).get('type', {}).get('shortDetail', '')
            
            upcoming_games.append({
                'name': event.get('shortName', ''),
                'time': status_detail,
                'short_time': short_detail,
                'date_sort': game_time
            })
    
    # Sort by date
    upcoming_games.sort(key=lambda x: x['date_sort'] if x['date_sort'] else '9999')
    
    for i, game in enumerate(upcoming_games[:limit]):
        print(f"{i+1}. {game['name']:<15} - {game['time']}")
        
    if len(upcoming_games) > limit:
        print(f"... and {len(upcoming_games) - limit} more games")

if __name__ == "__main__":
    print("Fetching NFL live games...")
    
    # Get live games
    live_games, week_number = get_live_nfl_games()
    
    # Display live games
    display_live_games(live_games, week_number)
    
    # Also fetch all data for summary and upcoming games
    try:
        response = requests.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard")
        if response.status_code == 200:
            all_data = response.json()
            get_all_games_summary(all_data)
            show_upcoming_games(all_data)
    except:
        pass