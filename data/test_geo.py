"""Geographic validation test: every site/change alert must be inside the real Jammu District polygon; known outside points must not be."""
import json, pathlib
from shapely.geometry import shape, Point
D=pathlib.Path(__file__).parent; poly=shape(json.load(open(D/"jammu_district_boundary.geojson"))["features"][0]["geometry"])
inside=lambda lat,lon:poly.contains(Point(lon,lat))
sites=json.load(open(D/"sites.json")); ch=json.load(open(D/"changes.json"))
assert all(inside(s["latitude"],s["longitude"]) for s in sites+ch), "site outside Jammu District"
for n,(la,lo) in {"Srinagar":(34.08,74.80),"Samba town":(32.56,75.12),"Kathua":(32.37,75.52),"Lahore (Pakistan)":(31.55,74.34),"Udhampur":(32.92,75.14)}.items():
    assert not inside(la,lo), n
assert inside(32.73,74.86), "Jammu city centre"
print(f"PASS: {len(sites)} sites + {len(ch)} change alerts inside Jammu District; 5 outside points correctly rejected")
