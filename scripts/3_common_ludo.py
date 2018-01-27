#init
import time
import requests
import xmltodict
games = {}

#aggregate data
print "aggregating data"
file = open("data_dump.tsv","r")
i = 0
for line in file:
	if i == 0:
		headers = line[:-1].split("\t")
		i += 1
		continue
	split_line = line[:-1].split("\t")
	if split_line[headers.index("subtype")] == "boardgame":
		if split_line[headers.index("own")] == "1":
			if split_line[headers.index("objectid")] not in games.keys():
				games[split_line[headers.index("objectid")]] = [{"user":split_line[headers.index("user")],"rating":split_line[headers.index("rating")]}]
			else:
				games[split_line[headers.index("objectid")]] += [{"user":split_line[headers.index("user")],"rating":split_line[headers.index("rating")]}]
	if i%100 == 0:
		print " .." + str(i) + " games aggregated"
	i += 1
file.close()
print " .." + str(i) + " games aggregated"

#enrich and store
print "enriching and storing data"
i = 1
file = open("common_ludo.tsv","w")
file.write("id\tname\tphoto\tlink\tusers\tpc_rating\tbgg_ranking\tyearpublished\tminplayers\tmaxplayers\tplayingtime\tminplaytime\tmaxplaytime\tminage\tcategories\tmechanics\tbasegame\n")
file.close()
for id in games.keys():
	while True:
		r = requests.get("https://www.boardgamegeek.com/xmlapi2/thing?id=" + id + "&stats=1")
		if r.status_code == 200:
			break
		time.sleep(17)
	body = r.content
	dico = xmltodict.parse(body)
	name = ""
	try:
		name = dico["items"]["item"]["name"]["@value"]
	except:
		for name in dico["items"]["item"]["name"]:
			if name["@type"] == "primary":
				name = name["@value"]
				break
	users = ""
	rate_sum = 0
	rate_num = 0
	for user in games[id]:
		users += user["user"] + ","
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
			categories += link["@value"] + ","
		if link["@type"] == "boardgamemechanic":
			mechanics += link["@value"] + ","
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
	if ranking == "Not Ranked":
		ranking = ""
	basegame = "0"
	if dico["items"]["item"]["@type"] == "boardgame":
		basegame = "1"
	file = open("common_ludo.tsv","a+")
	file.write(id.encode("utf-8") + "\t")
	file.write(name.encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["thumbnail"].encode("utf-8") + "\t")
	file.write("https://boardgamegeek.com/boardgame/" + id + "\t")
	file.write(users.encode("utf-8") + "\t")
	file.write(rating.encode("utf-8") + "\t")
	file.write(ranking.encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["yearpublished"]["@value"].encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["minplayers"]["@value"].encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["maxplayers"]["@value"].encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["playingtime"]["@value"].encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["minplaytime"]["@value"].encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["maxplaytime"]["@value"].encode("utf-8") + "\t")
	file.write(dico["items"]["item"]["minage"]["@value"].encode("utf-8") + "\t")
	file.write(categories.encode("utf-8") + "\t")
	file.write(mechanics.encode("utf-8") + "\t")
	file.write(basegame.encode("utf-8") + "\n")
	file.close()
	if i%100 == 0 and i>0:
		print " .." + str(i) + " games done"
	i += 1
print " .." + str(i-1) + " games done"