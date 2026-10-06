"""Builds the Jammu District boundary and validated prototype datasets.
Boundary: Census of India 2011 district polygon 'Jammu' (DT_CEN_CD 21), via DataMeet (github.com/datameet/maps, Districts/Census_2011).
Usage: python3 data/build_data.py <path/to/2011_Dist (shapefile prefix)> [old_sites.json]"""
import sys, json, math, random, shapefile
from shapely.geometry import shape, Point, mapping
SHP=sys.argv[1]; OLD=sys.argv[2] if len(sys.argv)>2 else None
g=[shape(s.shape.__geo_interface__) for s in shapefile.Reader(SHP).shapeRecords() if s.record['DISTRICT']=='Jammu' and s.record['ST_NM']=='Jammu & Kashmir']
assert len(g)==1; poly=g[0].simplify(0.0004); assert poly.geom_type=="Polygon"
json.dump({"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"Jammu District, Jammu & Kashmir, India","source":"Census of India 2011 district boundary (DataMeet)","dt_cen_cd":21},"geometry":mapping(poly)}]},open("data/jammu_district_boundary.geojson","w"))
inside=lambda lat,lon:poly.contains(Point(lon,lat))
rep={}
if OLD:  # audit of the previous dataset (built against an approximate polygon)
    old=json.load(open(OLD)); bad=[s["id"] for s in old if not inside(s["latitude"],s["longitude"])]
    rep["previous_dataset"]={"total":len(old),"inside":len(old)-len(bad),"rejected_outside":len(bad),"rejected_ids":bad}

import math as m
LOC={"Jammu city centre":(32.7266,74.8570,1),"Gandhi Nagar":(32.7030,74.8800,.95),"Satwari":(32.6800,74.8400,.8),"Bari Brahmana":(32.6000,74.9300,.55),"Bishnah":(32.6150,74.8550,.5),"RS Pura":(32.5800,74.7200,.45),"Akhnoor":(32.8950,74.7400,.45),"Nagrota":(32.7950,74.9100,.5),"Marh":(32.7600,74.7100,.35),"Jourian":(32.9300,74.8300,.3),"Miran Sahib":(32.6900,74.7600,.5),"Pargwal":(32.8200,74.7000,.25),"Arnia":(32.5500,74.8100,.3)}
LOC={k:v for k,v in LOC.items() if inside(v[0],v[1])}
TAWI=[(74.95,32.82),(74.89,32.75),(74.86,32.72),(74.80,32.66),(74.70,32.58)]  # approximate river corridors (prototype)
CHENAB=[(74.75,32.98),(74.74,32.89),(74.70,32.80),(74.63,32.68)]
kmx=lambda lon,lat:((lon-74.8)*93.9,(lat-32.7)*111.2)
def dseg(p,a,b):
    (px,py),(ax,ay),(bx,by)=kmx(*p),kmx(*a),kmx(*b); dx,dy=bx-ax,by-ay; t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy))); return m.hypot(px-ax-t*dx,py-ay-t*dy)
river=lambda p:min(dseg(p,l[i],l[i+1]) for l in(TAWI,CHENAB) for i in range(len(l)-1))
def near(lon,lat):
    k=min(LOC,key=lambda n:m.hypot(*[a-b for a,b in zip(kmx(lon,lat),kmx(LOC[n][1],LOC[n][0]))])); return k,m.hypot(*[a-b for a,b in zip(kmx(lon,lat),kmx(LOC[k][1],LOC[k][0]))])
def urban(lon,lat):
    return min(1,max(.03,max(w*m.exp(-m.hypot(*[a-b for a,b in zip(kmx(lon,lat),kmx(lo,la))])/(6 if w>.7 else 3.5)) for la,lo,w in LOC.values())))
cl=lambda v,a,b:max(a,min(b,v))
random.seed(21); core=poly.buffer(-0.012); S=[]; tries=0
while len(S)<46:
    tries+=1
    if random.random()<.9: k=random.choices(list(LOC.values()),[v[2]**2 for v in LOC.values()])[0]; lon,lat=random.gauss(k[1],.04),random.gauss(k[0],.035)
    else: b=poly.bounds; lon,lat=random.uniform(b[0],b[2]),random.uniform(b[1],b[3])
    if not core.contains(Point(lon,lat)): continue
    u=cl(urban(lon,lat)+random.uniform(-.06,.06),.03,1); loc,dl=near(lon,lat); rd=river((lon,lat)); i=len(S)+1
    built=round(cl(.08+.72*u+random.uniform(-.05,.05),.05,.9),2); green=int(cl(4+(1-built)*30+random.uniform(-3,3),2,35))
    road=int(cl(15+(1-u)*320*random.uniform(.3,1),10,400)); heat_i=built*70+(35-green)*.9
    use=random.choices(["Underutilised Open Space","Vacant Plot","Fallow Land","Unused Road Margin","Under-flyover Space","Drain/Canal Edge"],[3,3,2,2 if road<80 else 0,2 if u>.6 else 0,3 if rd<2.5 else 0])[0]
    S.append({"id":f"JMU-{i:03d}","name":f"Candidate site near {loc}","locality":loc,"latitude":round(lat,5),"longitude":round(lon,5),
     "area_sqm":int(cl(random.lognormvariate(7.5,.55),600,9000)),"current_use":use,
     "population_nearby":int(cl((250+5500*u**1.5)*3.14*random.uniform(.8,1.2),600,18000)),"distance_to_road_m":road,
     "distance_to_nearest_park_m":int(cl(250+(1-u)*3200*random.uniform(.5,1.2),200,3500)),"green_cover_percent":green,
     "heat_risk":"High" if heat_i>=45 else "Medium" if heat_i>=28 else "Low","flood_risk":"High" if rd<1.5 else "Medium" if rd<4 else "Low",
     "accessibility":int(cl(95-road/5-(1-u)*25+random.uniform(-5,5),30,97)),"vegetation_index":round(cl(.06+green/100+random.uniform(-.03,.03),.05,.5),2),"built_up_index":built,
     "candidate_type":"Underutilised Space","confidence":round(random.uniform(.72,.94),2),
     "status":"Prototype / Demonstration Data","verification":"Pending field verification","analysis_status":"AI/GIS Prototype"})
CH=[]
while len(CH)<8:
    lon,lat=random.gauss(74.85,.12),random.gauss(32.72,.1)
    if not core.contains(Point(lon,lat)): continue
    u=urban(lon,lat)
    if not .12<u<.6: continue
    loc,_=near(lon,lat); lv=random.choice(["High","High","Medium"])
    CH.append({"id":f"CHG-{len(CH)+1:03d}","locality":loc,"latitude":round(lat,5),"longitude":round(lon,5),"historical_year":2022,"current_year":2026,"change_level":lv,
     "change_type":random.choice(["Potential new built-up area","Potential new built-up area","Potential land-use change","Potential vegetation loss"]),"approx_area_sqm":random.randint(400,3500) if lv=="High" else random.randint(150,900),
     "confidence":round(random.uniform(.7,.92),2),"status":"FIELD VERIFICATION REQUIRED","data_status":"Prototype Change-Detection Demonstration (simulated)"})
rep["new_dataset"]={"points_sampled":tries,"accepted_inside_boundary":len(S),"rejected_outside_or_edge":tries-len(S),"change_alerts":len(CH)}
json.dump(S,open("data/sites.json","w"),indent=1); json.dump(CH,open("data/changes.json","w"),indent=1); json.dump(rep,open("data/validation_report.json","w"),indent=1)
print(json.dumps(rep["new_dataset"]),"localities used:",len(LOC),"boundary km2",round(poly.area*111*111*.84))
