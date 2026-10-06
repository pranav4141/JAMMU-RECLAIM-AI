"""Generates prototype sites strictly inside the (approximate, configurable) Jammu District polygon."""
import json, random
B=[[74.40,32.70],[74.65,32.58],[74.95,32.62],[75.20,32.80],[75.10,33.00],[74.75,33.05],[74.45,32.92],[74.40,32.70]]
def inside(lon,lat,poly=B):
    c=False
    for (x1,y1),(x2,y2) in zip(poly,poly[1:]):
        if (y1>lat)!=(y2>lat) and lon<(x2-x1)*(lat-y1)/(y2-y1)+x1: c=not c
    return c
json.dump({"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"Jammu District (approximate prototype boundary - replace with official survey boundary)"},"geometry":{"type":"Polygon","coordinates":[B]}}]},open("data/jammu_district_boundary.geojson","w"))
random.seed(7); S=[]
cl=[(74.86,32.73,.10),(74.80,32.70,.08),(74.65,32.68,.10),(74.95,32.75,.12),(74.75,32.90,.12)]
while len(S)<42:
    cx,cy,r=random.choice(cl); lon,lat=random.gauss(cx,r),random.gauss(cy,r*.8)
    if not inside(lon,lat): continue
    i=len(S)+1; urban=abs(lon-74.86)<.12 and abs(lat-32.73)<.1
    S.append({"id":f"JMU-{i:03d}","name":f"Candidate Urban Site {i:02d}","latitude":round(lat,5),"longitude":round(lon,5),
     "area_sqm":random.randint(600,9000),"current_use":random.choice(["Underutilised Open Space","Vacant Plot","Fallow Land","Unused Road Margin"]),
     "population_nearby":random.randint(5000,14000) if urban else random.randint(800,6000),
     "distance_to_road_m":random.randint(10,400),"distance_to_nearest_park_m":random.randint(200,3000),
     "green_cover_percent":random.randint(2,35),"heat_risk":random.choice(["High","High","Medium","Low"]),
     "flood_risk":random.choice(["High","Medium","Medium","Low"]),"accessibility":random.randint(40,95),
     "vegetation_index":round(random.uniform(.05,.45),2),"built_up_index":round(random.uniform(.1,.8),2),
     "candidate_type":"Underutilised Space","confidence":round(random.uniform(.7,.95),2),"status":"Prototype / Demonstration Data"})
assert all(inside(s["longitude"],s["latitude"]) for s in S)
json.dump(S,open("data/sites.json","w"),indent=1); print(len(S),"sites, all inside boundary")
