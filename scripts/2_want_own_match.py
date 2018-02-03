# coding: utf-8

# ce programme prend en entrée data_dump.tsv généré par 1_dump_data.py et a pour vocation de mettre en relation les joueurs
# qui cherche un jeu (wishlist, want, want to play, want to buy) avec les joueurs qui ont (own, preordered) le jeu

DATA_PATH = "../data/"
HTML_PATH = "../visual/"
IN_FILE = "data_dump.tsv"
OUT_FILE_PLAY = "play_together.tsv"
OUT_FILE_TRADE = "trade_games.tsv"

games_to_play = {}  # key = bgg game oid ; value = {name : game name,want:[users], has:[users]}
games_to_trade = {}  # key = bgg game oid ; value = {name : game name,want:[users], has:[users]}

# aggregate data
print "aggregating data"
filei = open(DATA_PATH + IN_FILE, "r")
i = 0
for line in filei:
	if i == 0:
		headers = line[:-1].split("\t")
		i += 1
		continue
	split_line = line[:-1].split("\t")
	if split_line[headers.index("subtype")] == "boardgame":
		game_id = split_line[headers.index("objectid")]
		user = split_line[headers.index("user")]
		if not split_line[headers.index("objectid")] in games_to_play:
			games_to_play[game_id] = {'name': split_line[headers.index("name")], 'has': [], 'want': []}
			games_to_trade[game_id] = {'name': split_line[headers.index("name")], 'has': [], 'want': []}
		if split_line[headers.index("own")] == "1" or \
						split_line[headers.index("preordered")] == "1":
			games_to_play[game_id]["has"].append(user)
		if split_line[headers.index("fortrade")] == "1":
			games_to_trade[game_id]["has"].append(user)
		if split_line[headers.index("wantintrade")] == "1" or \
						split_line[headers.index("wishlist")] == "1" or \
						split_line[headers.index("wanttobuy")] == "1":
			games_to_trade[game_id]["want"].append(user)
		if split_line[headers.index("wanttoplay")] == "1":
			games_to_play[game_id]["want"].append(user)
	if i % 100 == 0:
		print " .." + str(i) + " games processed"
	i += 1
filei.close()

fileo = open(DATA_PATH + OUT_FILE_PLAY, "w")
fileo.write("id\tname\tplayershave\tplayerswant\n")
for game_id in games_to_play:
	game = games_to_play[game_id]
	owners = ','.join(str(x) for x in game['has']) if game['has'] else ''
	wanters = ','.join(str(x) for x in game['want']) if game['want'] else ''

	fileo.write(game_id + "\t"
	            + game['name'] + "\t"
	            + owners + "\t"
	            + wanters + "\n")
fileo.close()

fileo = open(DATA_PATH + OUT_FILE_TRADE, "w")
fileo.write("id\tname\tplayershave\tplayerswant\n")
for game_id in games_to_trade:
	game = games_to_trade[game_id]
	owners = ','.join(str(x) for x in game['has']) if game['has'] else ''
	wanters = ','.join(str(x) for x in game['want']) if game['want'] else ''

	fileo.write(game_id + "\t"
	            + game['name'] + "\t"
	            + owners + "\t"
	            + wanters + "\n")
fileo.close()