// Run: npm test  — every site/alert must be inside the real boundary; known outside points must not be.
import {readFileSync} from 'fs'; import {isWithinJammuDistrict as w} from './scoring'
const rd=(f:string)=>JSON.parse(readFileSync(new URL('../../public/'+f,import.meta.url),'utf8'))
const ring=rd('boundary.json').features[0].geometry.coordinates[0]; const rows=[...rd('sites.json'),...rd('changes.json')]
const bad=rows.filter((r:any)=>!w(r.latitude,r.longitude,ring)); if(bad.length)throw new Error('outside: '+bad.map((b:any)=>b.id))
for(const [n,la,lo] of [['Srinagar',34.08,74.8],['Samba town',32.56,75.12],['Kathua',32.37,75.52],['Lahore',31.55,74.34]] as const)if(w(la,lo,ring))throw new Error(n+' wrongly inside')
if(!w(32.73,74.86,ring))throw new Error('Jammu city should be inside')
console.log(`PASS: ${rows.length} records inside Jammu District; 4 outside points rejected`)
