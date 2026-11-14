'use strict';
function runAudit(){
  function ok(v,why){if(!v)throw Error(why);}
  function parity(n){let p=0;while(n){p^=n%2;n=Math.floor(n/2);}return p;}
  const code=i=>2*i+parity(i);
  function prism(r){
    const edges=[];for(let i=0;i<r;i++)edges.push([i,(i+1)%r],[r+i,r+(i+1)%r],[i,r+i]);
    const adj=Array.from({length:2*r},()=>[]);
    edges.forEach(([a,b],j)=>{adj[a].push(j);adj[b].push(j)});
    ok(adj.every(x=>x.length===3),"not cubic");
    return {edges,adj};
  }
  function solve(eq,n){
    const basis=new Map();
    for(const e of eq){
      let m=0n,b=e.b;
      for(const id of e.ids)m^=1n<<BigInt(id);
      while(m){
        let k=0;while(((m>>BigInt(k))&1n)===0n)k++;
        if(!basis.has(k)){basis.set(k,{m,b});break;}
        const row=basis.get(k);m^=row.m;b^=row.b;
      }
      if(m===0n&&b)return null;
    }
    const ans=Array(n).fill(0);
    for(const k of [...basis.keys()].sort((a,b)=>b-a)){
      const row=basis.get(k);let b=row.b;
      for(let j=k+1;j<n;j++)if((row.m>>BigInt(j))&1n)b^=ans[j];
      ans[k]=b;
    }
    for(const e of eq)ok(e.ids.reduce((v,j)=>v^ans[j],0)===e.b,"GF2 incorrect");
    return ans;
  }
  function make(r,charged){
    const {edges,adj}=prism(r),vcount=2*r,t=edges.length,charge=Array(vcount).fill(0);
    charge[charged]=1;const core=[];
    for(let v=0;v<vcount;v++)for(let z=0;z<8;z++){
      const tuple=[z&1,(z>>1)&1,(z>>2)&1];
      if((tuple[0]^tuple[1]^tuple[2])!==charge[v])
        core.push({v,tuple,lits:adj[v].map((id,i)=>({id:code(id+1),neg:tuple[i]})),ids:adj[v]});
    }
    const w=Math.max(2,Math.ceil(Math.log2(2*t+2))),N=2**w-1;
    const used=new Set(Array.from({length:t},(_,i)=>code(i+1)));
    const spare=Array.from({length:N},(_,i)=>i+1).filter(x=>!used.has(x));
    ok(spare.length>=3,"spare count too small");
    const filler=[];
    for(let j=0;j+2<spare.length;j+=3)
      filler.push({lits:spare.slice(j,j+3).map(id=>({id,neg:0})),filler:true});
    const rem=spare.length%3;
    if(rem){
      const tail=spare.slice(spare.length-rem);
      const anchors=spare.filter(x=>!tail.includes(x)).slice(0,3-rem);
      filler.push({lits:[...tail,...anchors].map(id=>({id,neg:0})),filler:true});
    }
    const clauses=[...core,...filler],M=clauses.length;
    let source="1".repeat(N)+"0"+"1".repeat(M)+"0";
    const corePositions=[];
    for(let c=0;c<M;c++)for(let j=0;j<3;j++){
      const lit=clauses[c].lits[j];
      if(c<core.length)corePositions.push({at:source.length,ci:c,li:j,kind:"sign"});
      source+=String(lit.neg);
      const bits=lit.id.toString(2).padStart(w,"0");ok(bits.length===w,"id width");
      for(let b=0;b<w;b++)if(c<core.length)corePositions.push({at:source.length+b,ci:c,li:j,kind:"id"});
      source+=bits;
    }
    ok(source.length===N+M+2+3*M*(w+1),"source len");
    return {r,charged,adj,t,w,N,M,core,clauses,spare,corePositions,source};
  }
  function parse(s,N,M,w,requireAll=true){
    const h="1".repeat(N)+"0"+"1".repeat(M)+"0";
    if(s.length!==h.length+3*M*(w+1)||!s.startsWith(h))return null;
    let p=h.length,all=new Set(),out=[];
    for(let j=0;j<M;j++){
      const seen=new Set(),row=[];
      for(let k=0;k<3;k++){
        const neg=Number(s[p++]),id=parseInt(s.slice(p,p+w),2);p+=w;
        if(id<1||id>N||seen.has(id))return null;
        seen.add(id);all.add(id);row.push({id,neg});
      }
      out.push(row);
    }
    if(requireAll&&all.size!==N)return null;
    return out;
  }
  function satisfied(rows,a){return rows.every(cl=>cl.some(l=>((a.get(l.id)||0)^l.neg)===1));}
  const counts={schema:"TMR1-NO-UNUSED-009",status:"COMPUTATIONAL",cases:0,coreClauses:0,coreSignFlips:0,coreIdentifierBitFlips:0,allValidSATNeighbors:0,allUsedInputChecks:0,fillerClauses:0,bruteOriginalUNSAT:0,negativeFillerCases:0,failures:0,maxL:0,minDensity:1,maxDensity:0,perCase:[]};
  for(const r of [3,4,6,8,12]){
    const {adj}=prism(r),t=3*r;
    for(const charged of [0,r]){
      const d=make(r,charged),orig=parse(d.source,d.N,d.M,d.w,true);
      ok(orig!==null,"source no-unused invalid");
      const q=d.corePositions.length,ratio=q/d.source.length;
      const occ=new Map();for(const row of orig)for(const l of row)occ.set(l.id,(occ.get(l.id)||0)+1);
      ok(occ.size===d.N,"some declared variable unused");
      ok(d.core.every(c=>c.lits.every(l=>occ.get(l.id)>=2)),"core ID single use");
      const eq=adj.map((ids,v)=>({ids,b:v===charged?1:0}));
      ok(solve(eq,t)===null,"odd Tseitin unexpectedly SAT");
      counts.allUsedInputChecks++;
      if(r===3&&charged===0){
        for(let mask=0;mask<(1<<t);mask++){
          const a=new Map();for(let i=0;i<t;i++)a.set(code(i+1),(mask>>i)&1);
          for(const x of d.spare)a.set(x,1);
          ok(!satisfied(orig,a),"original should be UNSAT");
          counts.bruteOriginalUNSAT++;
        }
      }
      for(let ci=0;ci<d.core.length;ci++){
        const c=d.core[ci],rhs=adj.map((ids,v)=>({ids,b:(v===charged?1:0)^(v===c.v?1:0)}));
        for(let j=0;j<3;j++)rhs.push({ids:[c.ids[j]],b:c.tuple[j]});
        const wit=solve(rhs,t);ok(!!wit,"missing clause-deletion witness");
        const base=new Map();for(let i=0;i<t;i++)base.set(code(i+1),wit[i]);
        for(const u of d.spare)base.set(u,1);
        const failures=orig.map((cl,j)=>satisfied([cl],base)?-1:j).filter(j=>j>=0);
        ok(failures.length===1&&failures[0]===ci,"not minimally UNSAT core witness");
        counts.coreClauses++;
      }
      for(const p of d.corePositions){
        const mut=d.source.slice(0,p.at)+(d.source[p.at]==="0"?"1":"0")+d.source.slice(p.at+1);
        const neigh=parse(mut,d.N,d.M,d.w,true);
        ok(neigh!==null,"mutant invalid under no-unused grammar");
        const c=d.core[p.ci],rhs=adj.map((ids,v)=>({ids,b:(v===charged?1:0)^(v===c.v?1:0)}));
        for(let j=0;j<3;j++)rhs.push({ids:[c.ids[j]],b:c.tuple[j]});
        const wit=solve(rhs,t);ok(!!wit,"witness missing");
        const a=new Map();for(let i=0;i<t;i++)a.set(code(i+1),wit[i]);
        for(const u of d.spare)a.set(u,1);
        if(p.kind==="id"){
          const fresh=neigh[p.ci][p.li].id;
          ok(d.spare.includes(fresh),"flipped target should be spare");
          a.set(fresh,1^neigh[p.ci][p.li].neg);
          counts.coreIdentifierBitFlips++;
        }else counts.coreSignFlips++;
        ok(satisfied(neigh,a),"mutant SAT witness fails");
        counts.allValidSATNeighbors++;
      }
      const fillerBitStart=d.N+d.M+2+3*d.core.length*(d.w+1);
      const fillerFlip=d.source.slice(0,fillerBitStart)+(d.source[fillerBitStart]==="0"?"1":"0")+d.source.slice(fillerBitStart+1);
      ok(parse(fillerFlip,d.N,d.M,d.w,true)!==null,"filler mutation invalid");
      ok(solve(eq,t)===null,"filler-only mutation cannot remove UNSAT core");
      counts.negativeFillerCases++;
      counts.cases++;counts.fillerClauses+=d.M-d.core.length;
      counts.maxL=Math.max(counts.maxL,d.source.length);
      counts.minDensity=Math.min(counts.minDensity,ratio);
      counts.maxDensity=Math.max(counts.maxDensity,ratio);
      counts.perCase.push({r,charge:charged,t,N:d.N,w:d.w,coreM:d.core.length,fillerM:d.M-d.core.length,L:d.source.length,Q:q,density:Number(ratio.toFixed(6))});
    }
  }
  ok(counts.allValidSATNeighbors===counts.coreSignFlips+counts.coreIdentifierBitFlips,"counters");
  return counts;
}
console.log(JSON.stringify(runAudit(),null,2));
