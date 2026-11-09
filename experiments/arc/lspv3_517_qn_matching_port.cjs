"use strict";
/* LSPV-3/517: exact Q_n matching-CNF/XLRUP subset and Resolution certificate checks.
 * Source is only from the original CNF. Not the official CakeML or historical checker.
 * Usage: node lspv3_517_qn_matching_port.cjs
 */
function assert(x,message){if(!x)throw Error(message);}
function match(n,seed){
  const N=1<<n, mate=Array.from({length:N},(_,i)=>i^1);
  let r=((n*1048576+seed)>>>0),rnd=()=>{r=(Math.imul(1664525,r)+1013904223)>>>0;return r;};
  if(seed)for(let z=0;z<80*n;z++){
    const a=rnd()%N,b=mate[a],d=Math.log2(a^b)|0;
    let k=rnd()%(n-1);if(k>=d)k++;
    const a2=a^(1<<k),b2=b^(1<<k);
    if(mate[a2]===b2 && (new Set([a,b,a2,b2])).size===4){
      mate[a]=a2;mate[a2]=a;mate[b]=b2;mate[b2]=b;
    }
  }
  for(let i=0;i<N;i++)assert(mate[mate[i]]===i && Number.isInteger(Math.log2(i^mate[i])),"invalid matching");
  return mate;
}
function make(n,mate){
  const E=[];
  for(let a=0;a<mate.length;a++)if(a<mate[a]){
    const b=mate[a],d=Math.log2(a^b)|0;
    const lits=[];
    for(let j=0;j<n;j++)if(j!==d)lits.push((a&(1<<j))?-(j+1):(j+1));
    E.push({id:E.length+1,a,b,d,lits});
  }
  assert(E.length===1<<(n-1),"edge count");return E;
}
function falsifies(c,x){return c.every(l=>((x>>(Math.abs(l)-1))&1)===(l<0?1:0));}
function cover(n,edges,rhs,missing){
  for(let x=0;x<(1<<n);x++){
    let parity=0;for(let j=0;j<n;j++)parity^=(x>>j)&1;
    if(parity===rhs)continue;
    const desired=new Set(Array.from({length:n},(_,j)=>(x&(1<<j))?-(j+1):j+1));
    let ok=false;
    for(const e of edges)if(e.id!==missing && e.lits.every(l=>desired.has(l))){ok=true;break;}
    if(!ok)return false;
  }return true;
}
function res(n,edges){
  const m=edges.length, byKey=new Map();
  for(const e of edges){
    assert((e.a^e.b)===1,"upper tree only for coordinate zero matching");
    let key=0;for(let j=1;j<n;j++)key|=((e.a>>j)&1)<<(j-1);
    byKey.set(key,{id:e.id,clause:e.lits});
  }
  assert(byKey.size===m,"missing complete pattern");
  let current=Array.from({length:m},(_,i)=>byKey.get(i));
  let count=0,nextid=m+1;
  for(let j=1;j<n;j++){
    const pivot=j+1,step=[];
    for(let k=0;k<current.length;k+=2){
      const a=current[k],b=current[k+1];
      assert(a&&b,"parent");
      const ap=a.clause.find(l=>Math.abs(l)===pivot);
      const bp=b.clause.find(l=>Math.abs(l)===pivot);
      assert(ap===-bp && ap!==undefined,"bad pivot");
      const out=a.clause.filter(l=>Math.abs(l)!==pivot);
      assert(JSON.stringify(out)===JSON.stringify(b.clause.filter(l=>Math.abs(l)!==pivot)),"bad resolvent");
      step.push({id:nextid++,clause:out});count++;
    }current=step;
  }
  assert(count===m-1 && current.length===1 && current[0].clause.length===0,"resolution not empty");
  return count;
}
function encode(n,edges){
  const m=edges.length;
  const src="p cnf "+n+" "+m+"\n"+edges.map(e=>e.lits.join(" ")+" 0\n").join("");
  const ids=edges.map(e=>e.id).join(" ");
  const r1=Array.from({length:n},(_,j)=>j+1).join(" ");
  const r2=Array.from({length:n},(_,j)=>j?-1*(j+1)*0+(j+1):-1).join(" ");
  const pkt="i x 1 "+r1+" 0 "+ids+" 0\n"+
    "i x 2 "+r2+" 0 "+ids+" 0\n"+
    "x 3 0 1 2 0\n"+
    "i cx "+(m+1)+" 0 3 0\n";
  assert(pkt.trim().split("\n").length===4,"four-record packet");return{src,pkt};
}
function audit(n,seed){
  const edges=make(n,match(n,seed)),m=edges.length,N=1<<n,counts=Array(N).fill(0);
  for(const e of edges){
    let hit=0;for(let x=0;x<N;x++)if(falsifies(e.lits,x)){counts[x]++;hit++;}
    assert(hit===2 && falsifies(e.lits,e.a) && falsifies(e.lits,e.b),"source falsifying endpoints");
  }
  assert(counts.every(c=>c===1),"original source not minimal UNSAT");
  assert(cover(n,edges,0,null)&&cover(n,edges,1,null),"invalid exact XOR hint coverage");
  const tests=[1,Math.ceil(m/2),m];
  for(const id of tests){
    assert(!cover(n,edges,0,id) && !cover(n,edges,1,id),"deleted hint was still accepted");
  }
  const {src,pkt}=encode(n,edges);
  const nodeCount=seed===0?res(n,edges):null;
  return {n,seed,m,source_bytes:src.length,external_records:4,external_hint_references:2*m,
    external_bytes:pkt.length,native_lower:m-1,native_upper_parallel:nodeCount,
    coordinates:edges.reduce((a,e)=>(a[e.d]=(a[e.d]||0)+1,a),{}),
    ...(n===4&&seed===0?{sample_cnf:src,sample_xlrup:pkt}:{})};
}
function run(){
  const results=[];
  for(let n=2;n<=9;n++)for(let seed=0;seed<4;seed++)results.push(audit(n,seed));
  return {label:"LSPV-3/517 COMPUTATIONAL ONLY",checker:"Independent JS subset implementation, not cake_xlrup/R_mix341",
    checks:results.length,all_passed:true,configs:results,
    theorem:"Analytic Q_n any-matching source minimality; four XLRUP record upper; m-1 binary-source work lower",
    caveat:"Only n=4 yields strict 3-CNF; record count does not bound source bits"};
}
module.exports=run;
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
