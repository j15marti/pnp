/* LSPV-2/387. Strict Resolution local certificates and the odd binary triangle. */
"use strict";
const fs = require("fs");
function sorted(c){return [...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function sig(c){return sorted(c).join(",");}
function parity(vars,b){
  const ans=[];
  for(let mask=0;mask<2**vars.length;mask++){
    let v=0;for(let i=0;i<vars.length;i++)v^=(mask>>i)&1;
    if(v!==b)ans.push(vars.map((x,i)=>(mask>>i)&1?-x:x));
  }
  return ans;
}
function resolvent(a,b,p){
  if(!a.includes(p)||!b.includes(-p))return null;
  const s=new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  if([...s].some(x=>s.has(-x)))return null;
  return sorted([...s]);
}
function derivation(sources,keepVar){
  const records=sources.map((c,i)=>({c:sorted(c),source:i}));
  let active=records.map((_,i)=>i), seen=new Map(records.map((r,i)=>[sig(r.c),i]));
  function add(c,i,j,p){
    const k=sig(c);if(seen.has(k))return seen.get(k);
    const id=records.length;records.push({c:sorted(c),parents:[i,j],pivot:p});
    seen.set(k,id);return id;
  }
  if(keepVar!==undefined){
    for(let p=1;p<keepVar;p++){
      const yes=active.filter(i=>records[i].c.includes(p));
      const no=active.filter(i=>records[i].c.includes(-p));
      const next=new Set(active.filter(i=>!records[i].c.includes(p)&&!records[i].c.includes(-p)));
      for(const i of yes)for(const j of no){
        const c=resolvent(records[i].c,records[j].c,p);
        if(c!==null)next.add(add(c,i,j,p));
      }
      active=[...next];
    }
  }else{
    outer:for(let round=0;round<10;round++){
      const old=records.length;
      for(let i=0;i<old;i++)for(let j=0;j<old;j++){
        if(i===j)continue;
        for(const p of records[i].c){
          const c=resolvent(records[i].c,records[j].c,p);
          if(c!==null){add(c,i,j,p);if(c.length===0)break outer;}
        }
      }
      if(records.length===old)break;
    }
    active=records.map((_,i)=>i);
  }
  return {records,active};
}
function rowCase(d,b){
  const vars=Array.from({length:d},(_,i)=>i+1),clauses=parity(vars,b);
  let next=d+1,acc=1;
  const gates=[];
  function gate(a,c){const z=next++;gates.push({z,a,b:c});return z;}
  function xor(a,c){
    const u=gate(a,-c),v=gate(-a,c),w=gate(-u,-v);
    return -w;
  }
  for(let x=2;x<=d;x++)acc=xor(acc,x);
  const defs=gates.flatMap(({z,a,b})=>[[-z,a],[-z,b],[z,-a,-b]]);
  const proof=derivation([...clauses,...defs],Math.abs(acc));
  const unit=b===1?acc:-acc;
  if(!proof.active.some(i=>sig(proof.records[i].c)===sig([unit])))throw Error("missing derived parity unit");
  return {d,b,clauses,gates,defs,output:acc,derivedUnit:unit,proof:proof.records};
}
function models(cnf,n){
  const out=[];for(let mask=0;mask<2**n;mask++){
    if(cnf.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===(l>0?1:0)))))out.push(mask);
  }
  return out;
}
function produce(){
  const rows=[];for(let d=2;d<=4;d++)for(const b of [0,1])rows.push(rowCase(d,b));
  const source=[...parity([1,2],1),...parity([2,3],1),...parity([1,3],1)];
  const rr=derivation(source);
  const empty=rr.records.findIndex(r=>r.c.length===0);
  if(empty<0)throw Error("missing triangle contradiction");
  const needed=new Set();
  function visit(i){if(needed.has(i))return;needed.add(i);(rr.records[i].parents||[]).forEach(visit);}
  visit(empty);
  const proof=[...needed].sort((a,b)=>a-b).map(i=>({id:i,...rr.records[i]}));
  const paid=proof.filter(r=>r.parents).length;
  if(paid!==5||models(source,3).length!==0)throw Error("triangle checks");
  for(let i=0;i<source.length;i++)if(models(source.filter((_,j)=>i!==j),3).length===0)throw Error("source dispensable");
  const even=[...parity([1,2],1),...parity([2,3],1),...parity([1,3],0)];
  if(models(even,3).length!==2)throw Error("even control");
  const identities=[];
  for(let a=0;a<2;a++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){
    if(((a^x)^y)!==((a^y)^x)||((a^x)^x)!==a)throw Error("rewrite falsified");
    identities.push({a,x,y,swap:(a^x)^y,cancel:(a^x)^x});
  }
  return {version:387,model:"strict binary Resolution plus paid conservative signed-AND2",rows,
    triangle:{source,proof,paid,evenModels:models(even,3)},identities};
}
const result=produce();
const rendered=JSON.stringify(result,null,2)+"\n";
if(process.argv[2])fs.writeFileSync(process.argv[2],rendered);
else process.stdout.write(rendered);
