# coding: utf-8

# ce programme prend en entrée data_dump.tsv généré par 1_dump_data.py et a pour vocation de mettre en relation les joueurs
# qui cherche un jeu (wishlist, want, want to play, want to buy) avec les joueurs qui ont (own, preordered) le jeu


DATA_PATH = "../data/"
HTML_PATH = "../visual/"
IN_FILE = "data_dump.tsv"
OUT_FILE = "game_want_own.tsv"
OUT_FILE_JS = "game_want_own.html"

games_want_own = {}  # key = bgg game oid ; value = {name : game name,want:[users], own:[users]}

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
		if not split_line[headers.index("objectid")] in games_want_own:
			games_want_own[game_id] = {'name': split_line[headers.index("name")], 'own': [], 'want': []}

		if split_line[headers.index("own")] == "1" or \
						split_line[headers.index("preordered")] == "1":
			games_want_own[game_id]['own'].append(user)
		elif split_line[headers.index("want")] == "1" or \
						split_line[headers.index("wishlist")] == "1" or \
						split_line[headers.index("wanttoplay")] == "1" or \
						split_line[headers.index("wanttobuy")] == "1":
			games_want_own[game_id]['want'].append(user)
	if i % 100 == 0:
		print " .." + str(i) + " games processed"
	i += 1
filei.close()

fileo = open(DATA_PATH + OUT_FILE, "w")
fileo.write("id\tname\tplayersown\tplayerswant\n")
for game_id in games_want_own:
	game = games_want_own[game_id]
	owners = ','.join(str(x) for x in game['own']) if game['own'] else 'PERSONNE'
	wanters = ','.join(str(x) for x in game['want']) if game['want'] else 'PERSONNE'

	fileo.write(game_id + "\t"
	            + game['name'] + "\t"
	            + owners + "\t"
	            + wanters + "\n")
fileo.close()


filejs = open(HTML_PATH + OUT_FILE_JS, "w")
filejs.write("<html>\n")
filejs.write("<head>\n")
filejs.write("<meta charset=\"UTF-8\">\n")
filejs.write("<title>PC marketplace</title>\n")
filejs.write("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\n")
filejs.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"http://cdn.datatables.net/1.10.16/css/jquery.dataTables.css\">\n")
filejs.write("<script type=\"text/javascript\" charset=\"utf8\" src=\"http://cdn.datatables.net/1.10.16/js/jquery.dataTables.js\"></script>\n")
filejs.write("<style>\n")
filejs.write("\ta {\n")
filejs.write("\t\tcolor: black;\n")
filejs.write("\t\ttext-decoration: none;\n")
filejs.write("\t}\n")
filejs.write("\ta:hover {\n")
filejs.write("\t\ttext-decoration: underline;\n")
filejs.write("\t}\n")
filejs.write("</style>\n")
filejs.write("</head>\n")
filejs.write("<body bgcolor=\"white\">\n")
filejs.write("\t<table id=\"commons\" class=\"display\" width=\"100%\" cellspacing=\"0\">\n")
filejs.write("\t\t<thead>\n")
filejs.write("\t\t\t<tr>\n")
filejs.write("\t\t\t\t<th>ID</th>\n")
filejs.write("\t\t\t\t<th>Name</th>\n")
filejs.write("\t\t\t\t<th>Veulent le jeu</th>\n")
filejs.write("\t\t\t\t<th>Ont le jeu</th>\n")
filejs.write("\t\t\t</tr>\n")
filejs.write("\t\t</thead>\n")
filejs.write("\t\t<tfoot>\n")
filejs.write("\t\t\t<tr>\n")
filejs.write("\t\t\t\t<th>ID</th>\n")
filejs.write("\t\t\t\t<th>Name</th>\n")
filejs.write("\t\t\t\t<th>Veulent le jeu</th>\n")
filejs.write("\t\t\t\t<th>Ont le jeu</th>\n")
filejs.write("\t\t\t</tr>\n")
filejs.write("\t\t</tfoot>\n")
filejs.write("\t\t<tbody>\n")
for game_id in games_want_own:
	game = games_want_own[game_id]

	if not game['want']:
		continue # if someone has, but no one want, it's useless...

	owners = str(len(game['own']))+' joueurs ('+','.join(str(x) for x in game['own'])+')' if game['own'] else 'PERSONNE'
	wanters = str(len(game['want']))+' joueurs ('+','.join(str(x) for x in game['want'])+')' if game['want'] else 'PERSONNE'

	filejs.write('<tr><td>'+game_id + "</td><td>"
	            + game['name'] + "</td><td>"
	            + wanters + "</td><td>"
	            + owners + "</tr>\n")
filejs.write("\t\t</tbody>\n")
filejs.write("\t</table>\n")
filejs.write("<script>\n")
filejs.write("$(document).ready( function () {\n")
filejs.write("\t$('#commons').DataTable();});\n")
filejs.write("</script>\n")
filejs.write("</body>\n")
filejs.write("</html>\n")
filejs.close()