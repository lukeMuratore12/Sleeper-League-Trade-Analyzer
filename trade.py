from sleeper_wrapper import *
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

# general details
username = input('Enter your sleeper username\n')
sport = 'nfl'
border_line = '********************************\n'

# fantasy user initalized
user = User(username)

# initializes players
players = Players()

# gets all players 
players = players.get_all_players()

# retrieve league id
league_id = user.get_all_leagues(sport, 2022)[0]['league_id']

# fantasy league initialized
league = League(league_id)

# week of current season
week = league.get_league()['settings']['leg']

# gets html from FantasyPros rankings for this week and year
r = requests.get('https://www.fantasypros.com/2022/09/fantasy-football-trade-value-chart-week-' + str(week) + '-2022/')
root = BeautifulSoup(r.content)

# key: player name 
# value: player trade value
trade_value = {}

# assigns trade value to players
tables = root.find('div', {'id' : 'entry-content'}).findAll('table')
for table in tables:
    rows = table.findAll('tr')
    df = pd.read_html(table.prettify())[0]
    df.columns = df.transpose()[0]
    df = df[1:]
    for row in df.iterrows():
        trade_value[row[1]['Name']] = row[1]['Value']

teams_data = league.get_users()

# maps team names to user id
teams_id = {}
for team in teams_data[:-1]:
    try:
        teams_id[team['metadata']['team_name']] = team['user_id']
    except:
        teams_id['Team ' + team['display_name']] = team['user_id']

rosters = league.get_rosters()

# maps owner id to player
teams = {}
for roster in rosters:
    teams[roster['owner_id']] = roster['players']
 
    
# now that we have our players mapped to values, let's start our command line menu
menu_input = 'Enter your team name: \n' + border_line
for team_name in teams_id.keys():
    menu_input += team_name + '\n'

menu_input += border_line

response = input(menu_input)
while response not in teams_id:
    if response == 'quit':
        quit()
    else:
        response = input('Enter a valid team name')
    
# user's team name
team1 = response

print(border_line)

menu_input = 'Enter a team to trade with: \n' + border_line
for team_name in teams_id.keys():
    if team_name != team1:
        menu_input += team_name + '\n'

menu_input += border_line

response = input(menu_input)
while response not in teams_id:
    if response == 'quit':
        quit()
    else:
        response = input('Enter a valid team name\n')

# team that user wants to trade with
team2 = response

print(border_line)
print(team1 + '\'s players\nPlayer Name\t\tValue\n')
print(border_line)
player_menu = ''
team1_names = set()
for player in teams[teams_id[team1]]:
    player_name = players[player]['first_name'] + ' ' + players[player]['last_name']
    team1_names.add(player_name)
    if len(player_name) > 15:
        tabs = '\t'
    else:
        tabs = '\t\t'
    
    if player_name in trade_value:
        player_menu += player_name + tabs + trade_value[player_name] + '\n'
    else:
        player_menu += player_name + tabs + 'N/A\n'

print(player_menu)
print(border_line)
print(team2 + '\'s players\nPlayer Name\tValue\n')
player_menu = ''
team2_names = set()
for player in teams[teams_id[team2]]:
    player_name = players[player]['first_name'] + ' ' + players[player]['last_name']
    team2_names.add(player_name)
    if len(player_name) > 15:
        tabs = '\t'
    else:
        tabs = '\t\t'
    
    if player_name in trade_value:
        player_menu += player_name + tabs + trade_value[player_name] + '\n'
    else:
        player_menu += player_name + tabs + 'N/A\n'
print(player_menu)
print(border_line)
num_send = input('How many players do you want to trade?\n')
while (not num_send.isdigit()) and (int(num_send) > 0 and int(num_send) < len(teams[teams_id[team1]])):
    num_send = input('Enter a valid number\n')

# list of players the user will send
players_send = []
for i in range(int(num_send)):
    p_name = input('Enter the name of a player you want to trade away\n')
    while p_name not in team1_names and p_name in players_send:
        p_name = input('Enter a valid player name\n')
    players_send.append(p_name)

num_receive = input('How many players do you want to receive?\n')
while (not num_receive.isdigit()) and (int(num_receive) > 0 and int(num_receive) < len(teams[teams_id[team2]])):
    num_receive = input('Enter a valid number\n')


# list of players the user will receive
players_receive = []
for i in range(int(num_receive)):
    p_name = input('Enter the name of a player you want to receive\n')
    while p_name not in team2_names and p_name in players_receive:
        p_name = input('Enter a valid player name\n')
    players_receive.append(p_name)

print(border_line + 'TRADE SUMMARY\n' + border_line)
print(team1 + ' SENDS TO ' + team2)
send_sum = 0
for player_name in players_send:
    if len(player_name) > 15:
        tabs = '\t'
    else:
        tabs = '\t\t'
    
    if player_name in trade_value:
        print(player_name + tabs + trade_value[player_name] + '\n')
        send_sum += float(trade_value[player_name])
    else:
        print(player_name + tabs + 'N/A\n')
        # assume a player's trade value is 2.0 if not found
        send_sum += 2.0

print('AT A VALUE OF ' + str(send_sum))
print(border_line)
print(team1 + ' RECEIVES FROM ' + team2)
receive_sum = 0
for player_name in players_receive:
    if len(player_name) > 15:
        tabs = '\t'
    else:
        tabs = '\t\t'
    
    if player_name in trade_value:
        print(player_name + tabs + trade_value[player_name] + '\n')
        receive_sum += float(trade_value[player_name])
    else:
        print(player_name + tabs + 'N/A\n')
        # assume a player's trade value is 2.0 if not found
        receive_sum += 2.0

print('AT A VALUE OF ' + str(receive_sum) + "\n" + border_line)