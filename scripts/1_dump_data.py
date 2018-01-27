import time
import xmltodict
import requests

DATA_PATH = "../data/"
IN_FILE = "pc_users.csv"
OUT_FILE = "data_dump.tsv"

#init in/out
file = open(DATA_PATH + IN_FILE,"r")
userline = file.read()
file.close()
users = userline.split(",")
file = open(DATA_PATH + OUT_FILE,"w")
file.write("user\tobjecttype\tobjectid\tsubtype\tcollid\tname\trating\town\tprevowned\tfortrade\twant\twanttoplay\twanttobuy\twishlist\tpreordered\n")
file.close()

#get the data
for user in users:
	print "processing " + user
	while True:
		r = requests.get("https://www.boardgamegeek.com/xmlapi2/collection?username=" + user + "&stats=1&version=1")
		if r.status_code == 200:
			break
		time.sleep(17)
	print " ..got response"
	body = r.content
	dico = xmltodict.parse(body)
	items_nb = int(dico["items"]["@totalitems"])
	already = []
	for i in range(items_nb):
		if i%100 == 0 and i > 0:
			print " ..processed " + str(i) + " items"
		if "version" in dico["items"]["item"][i] and int(dico["items"]["item"][i]["@objectid"]) in already:
			continue #skip the verion declaration, which are duplicates of the games themselves
		already += [int(dico["items"]["item"][i]["@objectid"])]
		rating = dico["items"]["item"][i]["stats"]["rating"]["@value"].encode('utf-8')
		if rating == "N/A":
			rating = ""
		file = open(DATA_PATH + OUT_FILE,"a+")
		file.write(user + "\t")
		file.write(dico["items"]["item"][i]["@objecttype"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["@objectid"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["@subtype"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["@collid"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["name"]["#text"].encode('utf-8') + "\t")
		file.write(rating + "\t")
		file.write(dico["items"]["item"][i]["status"]["@own"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@prevowned"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@fortrade"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@want"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@wanttoplay"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@wanttobuy"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@wishlist"].encode('utf-8') + "\t")
		file.write(dico["items"]["item"][i]["status"]["@preordered"].encode('utf-8') + "\n")
		file.close()
	print " ..processed " + str(items_nb) + " items"
print "DONE :)"