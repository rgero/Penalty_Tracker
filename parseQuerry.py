import json,httplib,urllib
connection = httplib.HTTPSConnection('api.parse.com', 443)


#Gets the penalties on a given day.
'''params = urllib.urlencode({"where":json.dumps({
       "date": "10/17/2015",
     })})
'''     
     
#Gets the penalties that exist.
params = urllib.urlencode({"where":json.dumps({
       "player": {
         "$exists": True
       }
     })})
connection.connect()
connection.request('GET', '/1/classes/Penalties?%s' % params, '', {
       "X-Parse-Application-Id": "oSY8MqxqilpXcaDSz3M45SZP0FnF1Hr7lJQ7gGMy",
       "X-Parse-REST-API-Key": "RTYdmM7W7Kno8JvTKJTn12gbAr8qdhGWvSx8BDCe"
     })
result = json.loads(connection.getresponse().read())
print len(result["results"])