#!/usr/bin/env node
import fs from "node:fs";import crypto from "node:crypto";
const start=process.hrtime.bigint(),p=process.argv[2];if(!p)throw Error("usage: verifier record.json");
const r=JSON.parse(fs.readFileSync(p,"utf8"));let checks=0;const ok=(x,m)=>{if(!x)throw Error(m);checks++};
const canon=x=>Array.isArray(x)?x.map(canon):(x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canon(x[k])])):x);
const N=15,A=1<<N,B=A/8,truth=(l,a)=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0),sat=(c,a)=>c.some(l=>truth(l,a));
const mask=pred=>{const b=Buffer.alloc(B);for(let a=0;a<A;a++)if(pred(a))b[a>>3]|=1<<(a&7);return b};
const cmask=c=>mask(a=>sat(c,a)),amask=(vs,q)=>mask(a=>vs.reduce((z,v)=>z^((a>>(v-1))&1),0)===q);
const and=(x,y)=>{const b=Buffer.alloc(B);for(let i=0;i<B;i++)b[i]=x[i]&y[i];return b};
const subset=(x,y)=>x.every((v,i)=>(v&~y[i])===0),hash=x=>crypto.createHash("sha256").update(x).digest("hex");
function source(){const e=[];for(const o of [0,5])for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)
 (u===0&&v===1)?e.push([o,o+4],[o+4,o+1]):e.push([o+u,o+v]);e.push([4,9]);
 const inc=Array.from({length:10},()=>[]);e.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});const chi=[1,0,0,0,0,0,0,0,0,0],F=[],by=[];
 for(let v=0;v<10;v++){const ids=[];for(let t=0;t<8;t++){const b=[t>>2&1,t>>1&1,t&1];if((b[0]^b[1]^b[2])===chi[v])continue;ids.push(F.length);F.push(inc[v].map((x,j)=>b[j]?-x:x))}by.push(ids)}
 const d=`p cnf 15 40\n${F.map(c=>`${c.join(" ")} 0\n`).join("")}`;return{e,inc,chi,F,by,sha:crypto.createHash("sha256").update(d).digest("hex")}}
const s=source();ok(s.sha===r.source.dimacs_sha256,"source hash");ok(JSON.stringify(s.F)===JSON.stringify(r.source.clauses),"source bytes");
let models=0;const one=new Map();for(let a=0;a<A;a++){const bad=s.F.map((c,i)=>sat(c,a)?-1:i).filter(i=>i>=0);if(!bad.length)models++;if(bad.length===1&&!one.has(bad[0]))one.set(bad[0],a)}
ok(models===0&&one.size===36,"UNSAT and essential count");ok(JSON.stringify([...one.keys()].sort((a,b)=>a-b))===JSON.stringify(r.core),"core ids");
const got=[];for(const [side,endpoint] of [[[0,1,2,3,4],4],[[5,6,7,8,9],9]]){let vs=[],rhs=0,schi=0;for(const v of side){schi^=s.chi[v];if(v!==endpoint){vs=[...new Set([...vs,...s.inc[v]].filter(x=>!(vs.includes(x)&&s.inc[v].includes(x))))].sort((a,b)=>a-b);rhs^=s.chi[v]}}
 const boundary=amask(vs,rhs),non=s.inc[endpoint].filter(x=>x!==15),sel=[];for(const sid of s.by[endpoint]){const w=Object.fromEntries(s.F[sid].map(l=>[Math.abs(l),l<0?1:0]));if(w[15]===(1^schi)&&(w[non[0]]^w[non[1]])===rhs)sel.push(sid)}
 const joined=and(and(cmask(s.F[sel[0]]),cmask(s.F[sel[1]])),boundary),unit=amask([15],schi),support=[...new Set([...vs,15])].sort((a,b)=>a-b);let affine=false;
 for(let z=0;z<1<<support.length;z++)for(const q of [0,1]){const row=support.filter((_,i)=>z>>i&1);if(amask(row,q).equals(joined))affine=true}
 let witness=-1;for(let a=0;a<A;a++)if((unit[a>>3]>>(a&7)&1)&&!(joined[a>>3]>>(a&7)&1)){witness=a;break}
 got.push({vertices:side,endpoint,boundary:{vars:vs,rhs},selected_source_ids:sel,joined_support:support,side_charge:schi,
  joined_models:[...joined].reduce((z,x)=>z+x.toString(2).replaceAll("0","").length,0),unit_models:[...unit].reduce((z,x)=>z+x.toString(2).replaceAll("0","").length,0),
  joined_implies_unit:subset(joined,unit),joined_equals_unit:joined.equals(unit),any_exact_affine_annotation:affine,
  joined_mask_sha256:hash(joined),unit_mask_sha256:hash(unit),unit_not_joined_witness:witness,
  witness_bits:Object.fromEntries(support.map(v=>[String(v),witness>>(v-1)&1]))})}
ok(JSON.stringify(canon(got))===JSON.stringify(canon(r.sides)),"independent side replay");for(const x of got){ok(x.joined_implies_unit&&!x.joined_equals_unit,"strict implication");ok(!x.any_exact_affine_annotation,"no exact affine row");ok(x.joined_models===8192&&x.unit_models===16384,"cardinality firewall")}
const accepts=x=>x.source?.dimacs_sha256===s.sha&&JSON.stringify(x.source?.clauses)===JSON.stringify(s.F)&&JSON.stringify(x.core)===JSON.stringify([...one.keys()].sort((a,b)=>a-b))&&JSON.stringify(canon(x.sides))===JSON.stringify(canon(got));
ok(accepts(r),"complete record acceptance");
const mutants=[];let m=structuredClone(r);m.sides[0].joined_equals_unit=true;mutants.push(m);m=structuredClone(r);m.sides[1].unit_not_joined_witness=0;mutants.push(m);m=structuredClone(r);m.source.clauses[0][0]*=-1;mutants.push(m);
for(const x of mutants)ok(!accepts(x),"corrupt record rejected");
const result={pass:true,checks,mutations_rejected:mutants.length,source_models:models,essential:one.size,elapsed_seconds:Number(process.hrtime.bigint()-start)/1e9,max_rss_kib:process.resourceUsage().maxRSS,scope:"independent finite declared-semantic replay; no historical byte checker"};
if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2)+"\n");console.log(JSON.stringify(result));
