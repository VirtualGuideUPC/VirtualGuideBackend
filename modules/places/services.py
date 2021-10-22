import math

class PlaceService:
    def __init__(self, _lat, _lon):
        self.lat = _lat
        self.lon = _lon

    def distance(self, lat1, lon1, lat2, lon2):
        R = 6373.0
        
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distancia = R * c #esta distancia te la da en Kms

        return distancia

    def tpnearbylist(self, tplist):
        list = []
        finalList=[]
        for tp in tplist:

            d = self.distance(self.lat, self.lon, float(tp.latitude), float(tp.longitude))
 
            if d < 3:
                temp=[d,tp]
                list.append(temp)

        list.sort()
        for i in list:
            finalList.append(i[1])

        return finalList


