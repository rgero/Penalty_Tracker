import urllib
file = urllib.urlopen("https://www.nhl.com/gamecenter/2015020740/recap/box-score")

websiteData = file.read()

print websiteData.find("Polak")