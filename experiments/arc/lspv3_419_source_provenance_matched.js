"use strict";
function produce419() {
  const val=(l,a)=> ((a>>(Math.abs(l)-1))&1)===(l>0?1:0);
  const sat=(c,a)=>c.some(l=>val(l,a));
  const scan=(f,n)=>{
    let models=0,solofail=Array(f.length).fill(null);
    for(let a=0;a<2**n;a++){
      let failures=0,j=-1;
      for(let k=0;k<f.length;k++)if(!sat(f[k],a)){failures++;j=k;if(failures>1)break}
      if(failures===0)models++;
      if(failures===1 && solofail[j]===null)solofail[j]=a;
    }
    return {models,solofail,essential:solofail.filter(x=>x!==null).length};
  };
  const resolve=(a,b,p)=>{
    if(!a.includes(p)||!b.includes(-p))throw Error("bad pivot");
    const x=[...new Set(a.filter(v=>v!==p).concat(b.filter(v=>v!==-p)))].sort((x,y)=>x-y);
    if(x.some(l=>x.includes(-l)))throw Error("tautology");
    return x;
  };
  let cases=[];
  for(let r=3;r<=5;r++){
    const h=2*r,n=3*r,m=8*r;
    const core=[];
    for(let k=0;k<8;k++)core.push([k&1?-1:1,k&2?-2:2,k&4?-3:3]);
    let pad=[];
    for(let i=4;i<=n;i++)pad.push([1,2,i]);
    for(let i=4;i<=n;i++)pad.push([1,-2,i],[-1,2,i]);
    if(pad.length<m-8)throw Error("padding fails");
    const easy=core.concat(pad.slice(0,m-8));
    let edges=[];
    for(let i=0;i<r;i++)edges.push([i,(i+1)%r]);
    for(let i=0;i<r;i++)edges.push([r+i,r+(i+1)%r]);
    for(let i=0;i<r;i++)edges.push([i,r+i]);
    const inc=Array.from({length:h},()=>[]);
    edges.forEach(([u,v],i)=>{inc[u].push(i+1);inc[v].push(i+1)});
    const tseitin=(odd)=>{
      let F=[];
      for(let v=0;v<h;v++)for(let k=0;k<8;k++){
        let parity=(k&1)^((k>>1)&1)^((k>>2)&1);
        if(parity!==(odd&&v===0?1:0))
          F.push(inc[v].map((id,j)=>((k>>j)&1)?-id:id));
      }
      return F;
    };
    const hard=tseitin(true),even=tseitin(false);
    if([easy,hard,even].some(f=>f.length!==m))throw Error("wrong clause count");
    let derived={},proof=[];
    const get=s=>s[0]==="S"?easy[Number(s.slice(1))]:derived[s];
    const add=(a,b,p)=>{
      let c=resolve(get(a),get(b),p),id="D"+proof.length;
      derived[id]=c;proof.push({id,left:a,right:b,pivot:p,clause:c});
    };
    for(let a=0;a<2;a++)for(let b=0;b<2;b++){
      const j=a+2*b;add("S"+j,"S"+(j+4),3);
    }
    add("D0","D1",2);add("D2","D3",2);add("D4","D5",1);
    if(proof.length!==7||proof[6].clause.length!==0)throw Error("proof fails");
    const data={easy,hard,even};
    const stats={easy:scan(easy,n),hard:scan(hard,n),even:scan(even,n)};
    if(stats.easy.models!==0 || stats.hard.models!==0 || stats.even.models!==2**(r+1)||stats.hard.essential!==m||stats.easy.essential!==8)
      throw Error("bad semantic counts");
    const dimacs=f=>"p cnf "+n+" "+f.length+"\n"+f.map(c=>c.join(" ")+" 0").join("\n")+"\n";
    cases.push({r,n,h,m,edges,source_chars:{easy:dimacs(easy).length,hard:dimacs(hard).length,even:dimacs(even).length},data,stats,proof});
  }
  return {schema:"native-rmix341-source-provenance419-v1",unit_weight:1,cases};
}
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
const raw=produce419();
console.log(JSON.stringify({result:verify419(raw),raw},null,2));
