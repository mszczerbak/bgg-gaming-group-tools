#init
import time
import requests
import xmltodict
import pandas

DATA_PATH = "../data/"
IN_FILE = "data_dump.tsv"
OUT_FILE = "common_ludo.tsv"

games = {}

#aggregate data
print "aggregating data"
file = open(DATA_PATH + IN_FILE,"r")
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
ratingDB = pandas.read_csv(DATA_PATH + IN_FILE, sep="\t")
ratings = ratingDB[["objectid","rating"]].groupby("objectid").mean()["rating"]
print "enriching and storing data"
try:
	existingDB = pandas.read_csv(DATA_PATH + OUT_FILE, sep="\t", encoding="utf-8")
except:
	existingDB = None
i = 1
file = open(DATA_PATH + OUT_FILE,"w")
file.write("id\tname\tphoto\tlink\tusers\tpc_rating\tbgg_ranking\tyearpublished\tminplayers\tmaxplayers\tplayingtime\tminplaytime\tmaxplaytime\tminage\tcategories\tmechanics\tbasegame\tnew\n")
file.close()
for id in games.keys():
	if existingDB is None or existingDB[existingDB["id"]==int(id)].shape[0] == 0:
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
		thumbnail = dico["items"]["item"]["thumbnail"]
		yearpublished = dico["items"]["item"]["yearpublished"]["@value"]
		minplayers = dico["items"]["item"]["minplayers"]["@value"]
		maxplayers = dico["items"]["item"]["maxplayers"]["@value"]
		playingtime = dico["items"]["item"]["playingtime"]["@value"]
		minplaytime = dico["items"]["item"]["minplaytime"]["@value"]
		maxplaytime = dico["items"]["item"]["maxplaytime"]["@value"]
		minage = dico["items"]["item"]["minage"]["@value"]
		new = "1"
	else:
		existingEL = existingDB[existingDB["id"]==int(id)].iloc[0]
		name = existingEL["name"]
		categories = ("" if pandas.isnull(existingEL["categories"]) else existingEL["categories"])
		mechanics = ("" if pandas.isnull(existingEL["mechanics"]) else existingEL["mechanics"])
		ranking = "%.0f" % existingEL["bgg_ranking"]
		basegame = "%.0f" % existingEL["basegame"]
		thumbnail = existingEL["photo"]
		yearpublished = "%.0f" % existingEL["yearpublished"]
		minplayers = "%.0f" % existingEL["minplayers"]
		maxplayers = "%.0f" % existingEL["maxplayers"]
		playingtime = "%.0f" % existingEL["playingtime"]
		minplaytime = "%.0f" % existingEL["minplaytime"]
		maxplaytime = "%.0f" % existingEL["maxplaytime"]
		minage = "%.0f" % existingEL["minage"]
		new = "0"
	users = ""
	for user in games[id]:
		users += user["user"] + ","
	if len(users) > 0:
		users = users[:-1]
	rating = ""
	if ~pandas.isnull(ratings[int(id)]):
		rating = "%.1f" % ratings[int(id)]
	file = open(DATA_PATH + OUT_FILE,"a+")
	file.write(id.encode("utf-8") + "\t")
	file.write(name.encode("utf-8") + "\t")
	file.write(thumbnail.encode("utf-8") + "\t")
	file.write("https://boardgamegeek.com/boardgame/" + id + "\t")
	file.write(users.encode("utf-8") + "\t")
	file.write(rating.encode("utf-8") + "\t")
	file.write(ranking.encode("utf-8") + "\t")
	file.write(yearpublished.encode("utf-8") + "\t")
	file.write(minplayers.encode("utf-8") + "\t")
	file.write(maxplayers.encode("utf-8") + "\t")
	file.write(playingtime.encode("utf-8") + "\t")
	file.write(minplaytime.encode("utf-8") + "\t")
	file.write(maxplaytime.encode("utf-8") + "\t")
	file.write(minage.encode("utf-8") + "\t")
	file.write(categories.encode("utf-8") + "\t")
	file.write(mechanics.encode("utf-8") + "\t")
	file.write(basegame.encode("utf-8") + "\t")
	file.write(new.encode("utf-8") + "\n")
	file.close()
	if i%100 == 0 and i>0:
		print " .." + str(i) + " games done"
	i += 1
print " .." + str(i-1) + " games done"