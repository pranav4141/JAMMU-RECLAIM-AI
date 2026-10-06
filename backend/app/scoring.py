LVL={"High":100,"Medium":60,"Low":25}
W=dict(population=.20,green=.20,access=.15,heat=.15,flood=.10,area=.10,facility=.05,underuse=.05)
def components(s):
    c=lambda v:max(0,min(100,v))
    return dict(population=c(s["population_nearby"]/100),green=c(100-s["green_cover_percent"]/30*100),access=c(s["accessibility"]),
      heat=LVL[s["heat_risk"]],flood=LVL[s["flood_risk"]],area=c(s["area_sqm"]/30),facility=c(100-s["distance_to_road_m"]/2),
      underuse=100 if s["current_use"]!="Unused Road Margin" else 70)
def score(s): return round(sum(v*W[k] for k,v in components(s).items()))
def priority(x): return "Critical" if x>80 else "High" if x>60 else "Moderate" if x>40 else "Low"
def recommend(s):
    r=[]
    if s["flood_risk"]=="High" and s["area_sqm"]>=800: r.append(("Rain Garden",70+10*(s["heat_risk"]!="Low"),["High flood/waterlogging risk","Open area suitable for stormwater capture"]))
    if s["area_sqm"]>4000 and s["green_cover_percent"]<20: r.append(("Urban Forest",85,["Large open area","Low existing green cover"]))
    if s["population_nearby"]>5000 and s["green_cover_percent"]<22 and s["accessibility"]>60: r.append(("Pocket Park",90,["High nearby population","Low green coverage","Good accessibility"]))
    if s["distance_to_road_m"]<100 and s["heat_risk"]!="Low": r.append(("Green Buffer",78,["Close to road","High heat exposure"]))
    if s["accessibility"]>80 and s["population_nearby"]>7000: r.append(("Public Plaza",74,["High pedestrian accessibility","Dense catchment"]))
    if s["population_nearby"]>3500 and s["accessibility"]>55 and 1000<=s["area_sqm"]<=5000: r.append(("Community Space",72,["High nearby population","Good accessibility","Moderate area"]))
    if not r: r.append(("Green Corridor",55,["No stronger rule matched; general greening suggested"]))
    n,cf,rs=max(r,key=lambda x:x[1])
    if n not in("Rain Garden","Green Corridor") and s["flood_risk"] in("High","Medium") and s["area_sqm"]>=800: n+=" + Rain Garden"; rs=rs+["Medium/high stormwater opportunity"]
    return dict(recommendation=n,rec_confidence=min(99,round(cf*s["confidence"]+8)),reasons=rs,engine="AI-assisted rule-based recommendation engine")
