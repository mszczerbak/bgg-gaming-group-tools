import time
import xmltodict
import requests

#init in/out
file = open("pc_users.csv","r")
userline = file.read()
file.close()
users = userline.split(",")
#collections = {}
file = open("data_dump.csv","w")
file.write("user,objecttype,objectid,subtype,collid,name,rating,own,prevowned,fortrade,want,wanttoplay,wanttobuy,wishlist,preordered\n")
file.close()

#get the data
for user in users:
	print "processing " + user
	while True:
		r = requests.get("https://www.boardgamegeek.com/xmlapi2/collection?username=" + user)
		if r.status_code == 200:
			break
		time.sleep(17)
	print " ..got response"
	body = r.content
	dico = xmltodict.parse(body)
	#collections[user] = dico["items"]["item"]
	items_nb = int(dico["items"]["@totalitems"])
	for i in range(items_nb):
		if i%100 == 0 and i > 0:
			print " ..processed " + str(i) + " items"
		rating = ""
		try:
			rating = dico["items"]["item"][i]["stats"]["rating"]["@value"].encode('utf-8')
		except:
			pass
		file = open("data_dump.csv","a+")
		file.write(user + "," + dico["items"]["item"][i]["@objecttype"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["@objectid"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["@subtype"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["@collid"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["name"]["#text"].encode('utf-8') + ",")
		file.write(rating + ",")
		file.write(dico["items"]["item"][i]["status"]["@own"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@prevowned"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@fortrade"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@want"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@wanttoplay"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@wanttobuy"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@wishlist"].encode('utf-8') + ",")
		file.write(dico["items"]["item"][i]["status"]["@preordered"].encode('utf-8') + "\n")
		file.close()
	print " ..processed " + str(items_nb) + " items"
print "DONE :)"