"use strict";
// LSPV-3/385 independent proof-data checker. node checker.js path/to/raw.json
function verify(raw){
 const need=(b,m)=>{if(!b)throw Error(m)};
 const ckey=a=>[...new Set(a)].sort((a,b)=>a-b).join(",");
 const norm=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 const eql=(a,b)=>ckey(a)===ckey(b);
 const cv=(c,s)=>c.some(l=>(!!s[Math.abs(l)])===(l>0));
 let n=0,checked=0;
 need(raw.records&&raw.records.length===4,"bad record count");
 for(const r of raw.records){
   const {p,q}=r;need(Math.abs(p)===1&&Math.abs(q)===2,"bad signed source");
   need(eql(r.sources[0],[p,q])&&eql(r.sources[1],[-p])&&eql(r.sources[2],[-q]),"source forged");
   need(eql(r.paid_definition_clauses[0],[-p,3])&&
        eql(r.paid_definition_clauses[1],[-q,3])&&
        eql(r.paid_definition_clauses[2],[p,q,-3]),"gate forged");
   for(const guarded of [false,true]){
     const steps=guarded?r.guarded_G:r.plain_P, db={};
     r.sources.forEach((c,i)=>db["S"+i]=guarded?norm([-4,...c]):c);
     r.paid_definition_clauses.forEach((c,i)=>db["D"+i]=c);
     need(steps.length===5,"wrong number of inferences");
     steps.forEach((op,i)=>{
       need(op.id==="R"+i,"out-of-order step");
       const a=db[op.parent1],b=db[op.parent2],p=op.pivot;
       need(a&&b&&a.includes(p)&&b.includes(-p),"pivot/parent violation");
       const expected=norm([...a.filter(l=>l!==p),...b.filter(l=>l!==-p)]);
       need(!expected.some(l=>expected.includes(-l)),"tautological proof line");
       need(eql(expected,op.clause),"incorrect proof line");
       db[op.id]=op.clause;n++;checked++;
     });
     need(eql(steps[4].clause,guarded?[-4]:[]),"invalid final clause");
   }
   for(let flags=0;flags<16;flags++){
     const s={1:!!(flags&1),2:!!(flags&2),3:!!(flags&4),4:!!(flags&8)};
     const d=r.paid_definition_clauses.every(c=>cv(c,s));
     const should=(s[3]===((p>0?s[1]:!s[1])||(q>0?s[2]:!s[2])));
     need(d===should,"not conservative definition");
     const original=r.sources.every(c=>cv(c,s));
     const guarded=r.sources.every(c=>cv([-4,...c],s));
     need(!original&&guarded===(!s[4]||original),"incorrect source labels");
     checked+=2;
   }
   need(r.charged_definition_nodes===1 && r.charged_resolution_nodes===5,"wrong charged weights");
 }
 const tamper=JSON.parse(JSON.stringify(raw));
 tamper.records[0].guarded_G[1].clause=[-4,1,3];
 let rejected=false;try{verifyNoTamper(tamper.records[0]);}catch(e){rejected=true;}
 need(rejected,"corruption not detected");
 return {status:"PASS",verified_inferences:n,checks:checked,
         deliberate_corruptions_rejected:1,source_label_controls:"all four UNSAT center polarity variants"};
 function verifyNoTamper(r){
   const db={};r.sources.forEach((c,i)=>db["S"+i]=[-4,...c]);
   r.paid_definition_clauses.forEach((c,i)=>db["D"+i]=c);
   for(let i=0;i<r.guarded_G.length;i++){
     const o=r.guarded_G[i], a=db[o.parent1],b=db[o.parent2],p=o.pivot;
     need(a&&b&&a.includes(p)&&b.includes(-p),"bad corrupted parent");
     const expected=norm([...a.filter(l=>l!==p),...b.filter(l=>l!==-p)]);
     need(eql(expected,o.clause),"corrupt inference");
     db[o.id]=o.clause;
   }
 }
}
if(typeof module!=="undefined"&&require.main===module){
 const fs=require("fs");
 const record=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 console.log(JSON.stringify(verify(record),null,2));
}