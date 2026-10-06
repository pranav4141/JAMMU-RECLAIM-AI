// Mirrors backend/app/scoring.py so the UI works even if the API is offline.
export interface Site{id:string;name:string;locality?:string;latitude:number;longitude:number;area_sqm:number;current_use:string;population_nearby:number;distance_to_road_m:number;distance_to_nearest_park_m:number;green_cover_percent:number;heat_risk:'High'|'Medium'|'Low';flood_risk:'High'|'Medium'|'Low';accessibility:number;confidence:number;status:string;verification?:string;analysis_status?:string;score?:number;priority?:string;recommendation?:string;rec_confidence?:number;reasons?:string[]}
export interface Change{id:string;locality?:string;approx_area_sqm?:number;latitude:number;longitude:number;historical_year:number;current_year:number;change_level:string;change_type:string;confidence:number;status:string;data_status:string}
export const WEIGHTS={population:.2,green:.2,access:.15,heat:.15,flood:.1,area:.1,facility:.05,underuse:.05}
export const HIGH_PRIORITY_THRESHOLD=61 // score >= 61 is "High" or "Critical"
const L={High:100,Medium:60,Low:25}, c=(v:number)=>Math.max(0,Math.min(100,v))
export const components=(s:Site)=>({population:c(s.population_nearby/100),green:c(100-s.green_cover_percent/30*100),access:c(s.accessibility),heat:L[s.heat_risk],flood:L[s.flood_risk],area:c(s.area_sqm/30),facility:c(100-s.distance_to_road_m/2),underuse:s.current_use==='Unused Road Margin'?70:100})
export const score=(s:Site)=>Math.round(Object.entries(components(s)).reduce((a,[k,v])=>a+v*WEIGHTS[k as keyof typeof WEIGHTS],0))
export const priority=(x:number)=>x>80?'Critical':x>60?'High':x>40?'Moderate':'Low'
export const COLORS:Record<string,string>={Critical:'#ef4444',High:'#f59e0b',Moderate:'#38bdf8',Low:'#94a3b8'}
const TXT:Record<string,[string,string,string]>={population:['Limited nearby population','Moderate nearby population','High nearby population'],green:['Adequate existing green coverage','Moderate green deficiency','Low existing green coverage'],access:['Limited accessibility','Moderate accessibility','Good accessibility'],heat:['Low heat exposure','Medium heat exposure','High heat exposure'],flood:['Low stormwater risk','Medium stormwater opportunity','High stormwater opportunity'],area:['Small open area','Moderate open area','Significant open area'],facility:['Far from road network','Moderate road proximity','Close to road network'],underuse:['Partly in use','Underutilised','Underutilised']}
/** Why a site scored what it did: weighted points per factor, largest first. */
export const contributors=(s:Site)=>Object.entries(components(s)).map(([k,v])=>({key:k,pts:v*WEIGHTS[k as keyof typeof WEIGHTS],max:WEIGHTS[k as keyof typeof WEIGHTS]*100,text:TXT[k][v>=70?2:v>=40?1:0]})).sort((a,b)=>b.pts-a.pts)
export const evidence=(s:Site):[boolean,string][]=>[[s.green_cover_percent<15,`Low existing green coverage (${s.green_cover_percent}%)`],[s.population_nearby>6000,`High nearby population (${s.population_nearby.toLocaleString()})`],[s.accessibility>65,`Good accessibility (${s.accessibility}/100)`],[s.area_sqm>3000,`Large open area (${s.area_sqm.toLocaleString()} m²)`],[s.heat_risk==='High','High heat exposure'],[s.flood_risk!=='Low',`${s.flood_risk} stormwater/flood opportunity`],[s.distance_to_nearest_park_m>800,`${(s.distance_to_nearest_park_m/1000).toFixed(1)} km from nearest park`]]
export const GREEN=['Pocket Park','Rain Garden','Urban Forest','Green Buffer','Green Corridor']
export const isGreen=(s:Site)=>GREEN.some(g=>s.recommendation?.includes(g))
export function recommend(s:Site){const r:[string,number,string[]][]=[]
 if(s.flood_risk==='High'&&s.area_sqm>=800)r.push(['Rain Garden',70+(s.heat_risk!=='Low'?10:0),['High flood/waterlogging risk','Open area suitable for stormwater capture']])
 if(s.area_sqm>4000&&s.green_cover_percent<20)r.push(['Urban Forest',85,['Large open area','Low existing green cover']])
 if(s.population_nearby>5000&&s.green_cover_percent<22&&s.accessibility>60)r.push(['Pocket Park',90,['High nearby population','Low green coverage','Good accessibility']])
 if(s.distance_to_road_m<100&&s.heat_risk!=='Low')r.push(['Green Buffer',78,['Close to road','High heat exposure']])
 if(s.accessibility>80&&s.population_nearby>7000)r.push(['Public Plaza',74,['High pedestrian accessibility','Dense catchment']])
 if(s.population_nearby>3500&&s.accessibility>55&&s.area_sqm>=1000&&s.area_sqm<=5000)r.push(['Community Space',72,['High nearby population','Good accessibility','Moderate area']])
 if(!r.length)r.push(['Green Corridor',55,['No stronger rule matched; general greening suggested']])
 let [n,cf,rs]=r.reduce((a,b)=>b[1]>a[1]?b:a)
 if(!['Rain Garden','Green Corridor'].includes(n)&&s.flood_risk!=='Low'&&s.area_sqm>=800){n+=' + Rain Garden';rs=[...rs,'Medium/high stormwater opportunity']}
 return{recommendation:n,rec_confidence:Math.min(99,Math.round(cf*s.confidence+8)),reasons:rs}}
export const enrich=(s:Site):Site=>{const sc=score(s);return{...s,score:sc,priority:priority(sc),...recommend(s)}}
// Ray-casting point-in-polygon against the district boundary ring ([lon,lat] pairs).
export function isWithinJammuDistrict(lat:number,lon:number,ring:number[][]){let i=false;for(let k=0;k<ring.length-1;k++){const[x1,y1]=ring[k],[x2,y2]=ring[k+1];if((y1>lat)!==(y2>lat)&&lon<(x2-x1)*(lat-y1)/(y2-y1)+x1)i=!i}return i}
export function validate<T extends{latitude:number;longitude:number}>(rows:T[],ring:number[][]){const ok=rows.filter(r=>isWithinJammuDistrict(r.latitude,r.longitude,ring));return{ok,report:{total:rows.length,inside:ok.length,rejected:rows.length-ok.length}}}
