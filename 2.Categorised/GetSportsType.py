f1 = open('ArticlesRefinedTestOddChar.csv','r')
f2 = open('ArticlesWithType.csv', 'w')

lines = f1.read().split('\n')

types = ["cricket", "football", "tennis", "badminton", "baseball", "basketball", "soccer", "hockey", "boxing", "wrestling", "swimming", "golf", "volleyball", "archery", "softball", "fencing", "cycling", "gymnastics", "handball", "netball", "rugby", "sailing", "squash", "table tennis", "polo", "athletics","weightlifting", "chess", "bullfighting", "taekwondo", "kabaddi", "contortion", "bodybuilding", "snooker", "olympics", "paralympics"]

typedic = {"goal":"football", "midfielder":"football", "free-kick":"football", "penalty":"football", "fifa":"football", "european championship":"football", "champions league":"football", "ballon d":"football", "premier league":"football", "basket":"basketball", "grand slam":"tennis", "wimbledon":"tennis", "french open":"tennis", "miami open":"tennis", "qatar open":"tennis", "us open":"tennis", "icc":"cricket", "t20":"cricket", "twenty20":"cricket", "wicket":"cricket", "bowler":"cricket", "bowling":"cricket", "inning":"cricket", "test match":"cricket", "test series":"cricket", "formula":"racing", "grand prix":"racing", "ferrari":"racing", "boxer":"boxing", "middleweight":"boxing", "breaststroke":"swimming", "tour de france":"cycling", "milansanremo":"cycling", "pga":"golf", "bullfight":"bullfighting", "contortionist":"contortion", "bodybuild":"bodybuilding", "olympic":"olympics", "paralympic":"paralympics", "transfer":"football", "manchester":"football", "chelsea":"football", "madrid":"football", "minute":"football", "arsenal":"football", "pacer":"cricket", "spinner":"cricket", "bat":"cricket", "bowl":"cricket", "climb":"climbing"}

for line in lines:
	arc = line[1:]
	stype = ""
	
	for type in types:
		if type in arc.lower():
			stype = type
			break
	
	if stype == "soccer":
		stype = "football"
	
	if stype == "":
		for key in typedic:
			if key in arc.lower():
				stype = typedic[key]
				break
	
	if stype == "":
		stype = "misc"
	
	line += "," + stype
	f2.write(line)
	f2.write("\n")

f1.close()
f2.close()
