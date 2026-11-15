function audit(){
"use strict";let checks=0,pairs=0,exhaustive=0,valid=0,invalid=0;
const ok=(x,m)=>{checks++;if(!x)throw Error("ASSERT "+m)};
const parity=a=>a.reduce((s,v)=>s^v,0);
const cmp=(a,b)=>a.length-b.length||(a<b?-1:a>b?1:0);
function block(ids,b){const o=[];for(let q=0;q<8;q++){const bits=[q>>2&1,q>>1&1,q&1];if(parity(bits)!==b)o.push(ids.map((s,i)=>s+(bits[i]?"-":"+")).join(","))}return o}
const source=gs=>gs.flatMap(g=>block(g.ids,g.b)).join(";");
function clause(s){const z=s.split(",");if(z.length!==3)return null;const r=[];for(const x of z){const m=/^([1-9][0-9]*)([+-])$/.exec(x);if(!m)return null;r.push({id:m[1],bit:m[2]==="-"?1:0})}return new Set(r.map(x=>x.id)).size===3?r:null}
function verify(s,token="1"){
 if(token!=="1"||typeof s!=="string"||!s.length)return false;
 const cs=s.split(";");if(cs.length%4!==0)return false;
 let charge=0;const ct=new Map();
 for(let k=0;k<cs.length;k+=4){let ids=null,p=null;const seen=new Set();
  for(let j=0;j<4;j++){const row=clause(cs[k+j]);if(!row)return false;row.sort((a,b)=>cmp(a.id,b.id));const x=row.map(v=>v.id);if(!ids)ids=x;if(x.some((v,i)=>v!==ids[i]))return false;const bs=row.map(v=>v.bit),z=parity(bs),key=bs.join("");if(p===null)p=z;if(z!==p||seen.has(key))return false;seen.add(key)}
  if(seen.size!==4)return false;charge^=1-p;for(const id of ids)ct.set(id,(ct.get(id)||0)+1)
 }
 if(charge!==1)return false;for(const v of ct.values())if(v%2!==0)return false;return true;
}
function prism(m,odd=true,prefix=""){const edges=[],vs=Array.from({length:2*m},()=>[]);function edge(u,v){const id=prefix+(edges.length+1);edges.push([u,v,id]);vs[u].push(id);vs[v].push(id)}for(let i=0;i<m;i++){edge(i,(i+1)%m);edge(m+i,m+(i+1)%m);edge(i,m+i)}const groups=vs.map((ids,i)=>({ids:ids.slice().sort(cmp),b:odd&&i===0?1:0}));return {groups,edges:edges.length,H:2*m,text:source(groups)}}
function sat(s){const rows=s.split(";").map(clause);if(rows.some(x=>!x))return null;const ids=[...new Set(rows.flatMap(x=>x.map(v=>v.id)))].sort(cmp);if(ids.length>12)return null;const di=new Map(ids.map((v,i)=>[v,i]));for(let a=0;a<1<<ids.length;a++)if(rows.every(r=>r.some(x=>((a>>di.get(x.id)&1)!==x.bit))))return true;return false}
function B(H){return H*(2+Math.ceil(Math.log2(H+1)))+(H-1)*(2+2*Math.ceil(Math.log2(2*H+1)))+(2+Math.ceil(Math.log2(2*H+1)))}
const records=[];
for(let m=3;m<=35;m++){const a=prism(m),e=prism(m,false),h=2*m;ok(a.groups.length===h,"groups");ok(a.edges===3*m,"edges");ok(verify(a.text),"odd valid");ok(!verify(e.text),"even reject");ok(!verify(a.text,"0"),"bad token");valid++;invalid+=2;const last=a.text.at(-1);ok(last==="+"||last==="-","last sign");const flipped=a.text.slice(0,-1)+(last==="+"?"-":"+");ok(!verify(flipped),"last-sign pair");ok(a.text.length===flipped.length&&a.text.slice(0,-1)===flipped.slice(0,-1),"prefix equality");ok(!verify(a.text.slice(0,-1)),"missing sign");ok(B(h)>h,"named stream nontrivial");pairs++;if(m<=4){ok(sat(a.text)===false,"odd UNSAT exhaustive");ok(sat(e.text)===true,"even SAT exhaustive");exhaustive+=2}if([3,4,5,12,35].includes(m))records.push({H:h,inputBytes:a.text.length,inputBits:8*a.text.length,edges:a.edges,namedRecordBits:B(h),macroCertificateBits:8,recordToMacroBitRatio:B(h)/8})}
const a=prism(3),e=prism(4);
ok(verify(source([...a.groups,...e.groups.map(g=>({ids:g.ids.map(s=>"8"+s),b:0}))])),"disconnected source accepted");
const cs=a.text.split(";");
ok(!verify(a.text.replace(";","")),"separator deletion");
let zz=cs.slice();zz[3]=zz[2];ok(!verify(zz.join(";")),"duplicate pattern");
zz=cs.slice();zz[3]=zz[3].replace(/^([0-9]+)/,x=>String(+x+19));ok(!verify(zz.join(";")),"mixed triple");
zz=cs.slice();zz[0]=zz[0].replace(/^([0-9]+)[+-],([0-9]+)[+-]/,(_,x)=>x+"+,"+x+"-");ok(!verify(zz.join(";")),"repeated variable");
ok(verify(source(a.groups.map(g=>({ids:g.ids.map(s=>"1"+"0".repeat(100)+s),b:g.b})))),"sparse huge IDs");
const pair=source([{ids:["1","2","3"],b:0},{ids:["1","2","3"],b:1}]);ok(verify(pair)&&sat(pair)===false,"two contradictory parity rows");
for(const s of ["1+,2+,3+","1+,2+,3+;1-,2+,3+","1+,1-,2+","1+,2+","garbage","","01+,2+,3+"]){ok(!verify(s),"non-source rejection");invalid++}
return {id:"MACROINGRESS067",checks,failures:0,distinguishingPairs:pairs,smallExhaustiveSATChecks:exhaustive,authenticatedOddSources:valid,rejectedControlClasses:invalid,samples:records,disconnectedAccepted:true,hugeIdentifierAccepted:true,proofScope:"authenticated contiguous four-clause parity-block unsat certificate, not all-CNF resolution, all SAT deciders or actual physical TM replay",execution:"self-contained V8 exact function, no random seeds"};
}
const output=audit();
console.log(JSON.stringify(output,null,2));
