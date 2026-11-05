"use strict";
const fs=require('fs');
function verify419(raw) {
  let checks=0;const ok=(x,m)=>{checks++;if(!x)throw Error(m)};
  const clauseSat=(cl,a)=>cl.some(l=>{
    let bit=(a>>(Math.abs(l)-1))&1;
    return l>0?bit===1:bit===0;
  });
  let rows=[];
  for(const e of raw.cases){
    ok(e.n===3*e.r&&e.h===2*e.r&&e.m===8*e.r,"parameters");
    for(const [name,F] of Object.entries(e.data)){
      ok(F.length===e.m,"mismatch m");
      const seen=new Set();
      for(const c of F){
        ok(c.length===3,"not width 3");
        ok(new Set(c.map(Math.abs)).size===3,"repeated literal id");
        for(const l of c){ok(Math.abs(l)<=e.n&&l!==0,"invalid literal");seen.add(Math.abs(l))}
      }
      ok(seen.size===e.n,"variable coverage");
      const unique=new Array(e.m).fill(null);
      let count=0;
      for(let a=0;a<(1<<e.n);a++){
        let bad=0,last=-1;
        for(let k=0;k<F.length;k++)if(!clauseSat(F[k],a)){bad++;last=k;}
        if(bad===0)count++;
        if(bad===1&&unique[last]===null)unique[last]=a;
      }
      ok(count===e.stats[name].models,"SAT model count "+name);
      ok(unique.filter(v=>v!==null).length===e.stats[name].essential,"essential count "+name);
      for(let j=0;j<e.m;j++) {
        const a=e.stats[name].solofail[j];
        if(a!==null){
          ok(a>=0&&a<(1<<e.n),"bad deletion witness");
          ok(!clauseSat(F[j],a),"deletion witness falsification");
          for(let k=0;k<e.m;k++)if(k!==j)ok(clauseSat(F[k],a),"deletion witness other clauses");
        }
        ok((a===null)===(unique[j]===null),"missing essential index");
      }
      const sz=("p cnf "+e.n+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0").join("\n")+"\n").length;
      ok(sz===e.source_chars[name],"source size");
    }
    ok(e.stats.easy.models===0 && e.stats.hard.models===0,"UNSAT control");
    ok(e.stats.even.models===2**(e.r+1),"even control");
    ok(e.stats.easy.essential===8&&e.stats.hard.essential===e.m,"minimum source controls");
    for(let k=0;k<8;k++){
      const c=e.data.easy[k];
      ok(c[0]===(k&1?-1:1)&&c[1]===(k&2?-2:2)&&c[2]===(k&4?-3:3),"cube core mismatch");
    }
    const inc=Array.from({length:e.h},()=>[]);
    ok(e.edges.length===e.n,"edge total");
    e.edges.forEach(([u,v],i)=>{ok(u>=0&&v>=0&&u<e.h&&v<e.h&&u!==v,"invalid edge");inc[u].push(i+1);inc[v].push(i+1)});
    inc.forEach(xs=>ok(xs.length===3,"non cubic"));
    for(let [name,odd] of [["hard",true],["even",false]]){
      let ix=0;
      for(let v=0;v<e.h;v++)for(let b=0;b<8;b++){
        const parity=(b&1)^((b>>1)&1)^((b>>2)&1);
        if(parity!==(odd&&v===0?1:0)){
          const expected=inc[v].map((id,j)=>((b>>j)&1)?-id:id);
          ok(e.data[name][ix++].join(",")===expected.join(","),"Tseitin invalid parity clause");
        }
      }
      ok(ix===e.m,"parity clause total");
    }
    let proofTable={};
    const fetch=s=>s[0]==="S"?e.data.easy[Number(s.slice(1))]:proofTable[s];
    for(const p of e.proof){
      const l=fetch(p.left),r=fetch(p.right);
      ok(Array.isArray(l)&&Array.isArray(r),"invalid parent");
      ok(l.includes(p.pivot)&&r.includes(-p.pivot),"invalid pivot");
      const out=[...new Set(l.filter(x=>x!==p.pivot).concat(r.filter(x=>x!==-p.pivot)))].sort((a,b)=>a-b);
      ok(out.every(x=>!out.includes(-x)),"tautological resolvent");
      ok(out.join(",")===[...p.clause].sort((a,b)=>a-b).join(","),"wrong resolvent");
      ok(proofTable[p.id]===undefined,"duplicate derived id");
      proofTable[p.id]=p.clause;
    }
    ok(e.proof.length===7&&proofTable.D6.length===0,"seven-step RES refutation");
    const mutated=JSON.parse(JSON.stringify(e.proof[0]));
    mutated.pivot=1;
    const left=fetch(mutated.left),right=fetch(mutated.right);
    ok(!(left.includes(mutated.pivot)&&right.includes(-mutated.pivot)),"forged proof pivot accepted");
    rows.push({r:e.r,n:e.n,m:e.m,easy_exact:7,hard_exact:e.m-1,easy_essential:8,hard_essential:e.m,even_models:e.stats.even.models,source_chars:e.source_chars});
  }
  return {checks,rows,verdict:"PASS"};
}
const raw=JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
console.log(JSON.stringify(verify419(raw),null,2));
