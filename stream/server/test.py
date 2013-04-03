from XMLServerDAO import XMLServerDAO

x = XMLServerDAO("../data")
for s in x.getServers():
    print(s)

