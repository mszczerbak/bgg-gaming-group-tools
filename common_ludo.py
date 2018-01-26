#init
import requests
import xmltodict
games = {}

#aggregate data
file = open("data_dump.csv","r")
i = 0
for line in file:
	if i == 0:
		headers = line[:-1].split(",")
		i += 1
		continue
	split_line = line[:-1].split(",")
	if split_line[headers.index("subtype")] == "boardgame":
		if split_line[headers.index("own")] == "1":
			if split_line[headers.index("objectid")] not in games.keys():
				games[split_line[headers.index("objectid")]] = [{"user":split_line[headers.index("user")],"rating":split_line[headers.index("rating")]}]
			else:
				games[split_line[headers.index("objectid")]] += [{"user":split_line[headers.index("user")],"rating":split_line[headers.index("rating")]}]
	i += 1
file.close()

#enrich and store
file = open("common_ludo.csv","w")
file.write("id,name,photo,link,users,pc_rating,bgg_ranking,yearpublished,minplayers,maxplayers,playingtime,minplaytime,maxplaytime,minage,categories,mechanics,basegame\n")
file.close()
for id in games.keys():
	r = requests.get("https://www.boardgamegeek.com/xmlapi2/thing?id=" + id + "&stats=1")
	body = r.content
	dico = xmltodict.parse(body)
	name = ""
	try:
		name = dico["items"]["item"]["name"]["@value"]
	except:
		for name in dico["items"]["item"]["name"]:
			if name["@type"] == "primary":
				name = name["@value"].encode("utf-8")
				break
	users = ""
	rate_sum = 0
	rate_num = 0
	for user in games[id]:
		users += user["user"] + "+"
		if user["rating"] != "":
			rate_sum += float(user["rating"])
			rate_num += 1
	if len(users) > 0:
		users = users[:-1]
	rating = ""
	if rate_num > 0:
		rate = rate_sum / rate_num
		rating = "%.1f" % rate
	categories = ""
	mechanics = ""
	for link in dico["items"]["item"]["link"]:
		if link["@type"] == "boardgamecategory":
			categories += link["@value"] + "+"
		if link["@type"] == "boardgamemechanic":
			mechanics += link["@value"] + "+"
	if len(categories) > 0:
		categories = categories[:-1]
	if len(mechanics) > 0:
		mechanics = mechanics[:-1]
	for rank in dico["items"]["item"]["statistics"]["ratings"]["ranks"]["rank"]:
		try:
			ranking = dico["items"]["item"]["statistics"]["ratings"]["ranks"]["rank"]["@value"]
		except:
			if rank["@name"] == "boardgame":
				ranking = rank["@value"]
	basegame = "0"
	if dico["items"]["item"]["@type"] == "boardgame":
		basegame = "1"
	file = open("common_ludo.csv","a+")
	file.write(id + ",")
	file.write(name + ",")
	file.write(dico["items"]["item"]["thumbnail"].encode("utf-8") + ",")
	file.write("https://boardgamegeek.com/boardgame/" + id + ",")
	file.write(users + ",")
	file.write(rating + ",")
	file.write(ranking + ",")
	file.write(dico["items"]["item"]["yearpublished"]["@value"].encode("utf-8") + ",")
	file.write(dico["items"]["item"]["minplayers"]["@value"].encode("utf-8") + ",")
	file.write(dico["items"]["item"]["maxplayers"]["@value"].encode("utf-8") + ",")
	file.write(dico["items"]["item"]["playingtime"]["@value"].encode("utf-8") + ",")
	file.write(dico["items"]["item"]["minplaytime"]["@value"].encode("utf-8") + ",")
	file.write(dico["items"]["item"]["maxplaytime"]["@value"].encode("utf-8") + ",")
	file.write(dico["items"]["item"]["minage"]["@value"].encode("utf-8") + ",")
	file.write(categories + ",")
	file.write(mechanics + ",")
	file.write(basegame + "\n")
	file.close()