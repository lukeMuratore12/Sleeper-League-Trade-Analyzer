# Sleeper League Trade Analyzer
After years of using the ESPN app to play fantasy football, my friends and I decided to use [Sleeper](https://sleeper.com). This year after our draft, I realized I made some huge mistakes.  Amari Cooper wasn't looking to have a great year, so I needed to get rid of him. After playing around with some general trade analyzer websites, I got tired of constantly switching tabs and searching through each of my friends' rosters, guessing and checking to see what might be a fair trade. Thus, I decided to make a command line trade analyzer that's personalized to any Sleeper league. All you have to do is enter your Sleeper username, and your league's teams will show up. Enter a team you want to trade with, and you'll receive the trade value of each of their players in comparison to yours. When you're ready, you can submit a hypothetical trade and see who gets the better end. 

## Trade Values
Each player's trade values are updated week-by-week, with data scraped from FantasyPros.com. [Here](https://www.fantasypros.com/2022/09/fantasy-football-trade-value-chart-week-3-2022/) is an example of what Fantasy Pros' trade values look like in week 3 of the 2022 NFL season.

## Sleeper API
I used a [python wrapper](https://github.com/SwapnikKatkoori/sleeper-api-wrapper) for the [Sleeper API](https://docs.sleeper.app/#introduction) in order to get league information, including team names and what players each team owns. Additionally, it was used to gain NFL season information, including the week and year that my fantasy league's team is currently playing in.
