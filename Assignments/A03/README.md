- Place all files in the same directory
- Run scrape_game_ids.py then scrape_game_data.py then separateStats.py then calculatestats.py
- Years can be chaged in the scrape_game_ids.py file

- My program was written in python2 so some of the functions might not work with python3

- scrape_game_ids.py fetches all of the game ids from the last 10 seasons
- scrape_game_data.py fetches all of the stats from the given game ids, and stores them as JSON files
- separateStats.py gets all stats needed to answer questions, and stores them in a simpler format
- calculatestats.py answers all of the questions
