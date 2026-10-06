import json, pathlib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .scoring import score, priority, recommend, components, W
D=pathlib.Path(__file__).resolve().parents[2]/"data"
app=FastAPI(title="Jammu Reclaim API"); app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"])
BOUNDARY=json.load(open(D/"jammu_district_boundary.geojson")); RING=BOUNDARY["features"][0]["geometry"]["coordinates"][0]
def is_within_jammu_district(lat,lon):
    c=False
    for (x1,y1),(x2,y2) in zip(RING,RING[1:]):
        if (y1>lat)!=(y2>lat) and lon<(x2-x1)*(lat-y1)/(y2-y1)+x1: c=not c
    return c
def load():  # every record is clipped to the district here; nothing outside survives
    raw=json.load(open(D/"sites.json")); ok=[s for s in raw if is_within_jammu_district(s["latitude"],s["longitude"])]
    return [{**s,"score":score(s),"priority":priority(score(s)),**recommend(s),"components":components(s)} for s in ok],len(raw)
@app.get("/api/sites")
def sites(): return load()[0]
@app.get("/api/sites/{id}")
def site(id:str):
    for s in load()[0]:
        if s["id"]==id: return s
    raise HTTPException(404,"Site not found")
@app.get("/api/recommendations/{id}")
def rec(id:str): s=site(id); return {k:s[k] for k in("recommendation","rec_confidence","reasons","engine")}
@app.get("/api/rankings")
def rank(): return sorted(load()[0],key=lambda s:-s["score"])
@app.get("/api/statistics")
def stats():
    s,_=load(); return dict(sites=len(s),high_priority=sum(x["score"]>60 for x in s),area_ha=sum(x["area_sqm"] for x in s)/1e4,beneficiaries=sum(x["population_nearby"] for x in s),weights=W,high_priority_threshold="score >= 61",label="Prototype estimate")
@app.get("/api/validation")
def validation():
    s,total=load(); return dict(total=total,inside=len(s),rejected=total-len(s))
@app.get("/api/encroachments")
def enc(): return [c for c in json.load(open(D/"changes.json")) if is_within_jammu_district(c["latitude"],c["longitude"])]
@app.get("/api/regions")
def regions(): return BOUNDARY
