#!/usr/bin/env python

import json
import requests
import sys
import codecs
import time

directions = [ "north",
		"north-east",
		"east",
		"south-east",
		"south",
		"south-west",
		"west",
		"north-west"]

def main():
  fin = codecs.open("forecast.json", "r", "utf-8") 
  s=''
  all_weather = json.loads(s.join(fin.readlines()))
  fin.close()
  if(all_weather['cod'] != "200"):
    print "Something goes wrong. Response code is {}. Exiting".format(all_weather['cod'])
    sys.exit(0)
  if(all_weather['cnt'] == "0"):
    print "Something goes wrong. Response is empty. Exiting"
    sys.exit(0)
  currenttime=int(time.time())
  for i in all_weather['list']:
    if(currenttime <= i['dt']):
      weather={}
      temp = int(i['main']['temp'] - 273)
      weather['temp'] = ('+' + str(temp) if temp>0 else str(temp))
      weather['wind']={}
      weather['wind']['speed'] = i['wind']['speed']
      weather['wind']['direction'] = directions[int(float(i['wind']['deg']) + 22.5 / 45) % 8]
      print json.dumps(weather)
      break
  
  
if __name__ == "__main__":
  sys.exit(main())
