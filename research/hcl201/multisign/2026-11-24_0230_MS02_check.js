"use strict";
// Node.js: node 2026-11-24_0230_MS02_check.js
function runMS02(){
  const bit=i=>1n<<BigInt(i), get=(v,i)=>Number((v>>BigInt(i))&1n);
  function par(x){let p=0;while(x){p^=1;x&=x-1n;}return p;}
  function xor(xs){return xs.reduce((a,b)=>a^b,0n);}
  // Row representation [coefficient bit mask, rhs 0/1].
  function solve(rows,n){const p=new Map();for(let [v,b] of rows){while(v){let i=v.toString(2).length-1;if(!p.has(i)){p.set(i,[v,b]);break;}let [w,c]=p.get(i);v^=w;b^=c;}if(!v&&b)return null;}
    let x=0n;for(const i of [...p.keys()].sort((a,b)=>a-b)){let [v,b]=p.get(i);if(par(v&x)!==b)x|=bit(i);}
    return {x,rank:p.size,count:bit(n-p.size)};
  }
  function eqs(cols,c,d){let rows=[];for(let j=0;j<d;j++){let a=0n;for(let i=0;i<cols.length;i++)if(get(cols[i],j))a|=bit(i);rows.push([a,get(c,j)]);}return rows;}
  function span(vs){let s=new Set([0n]);for(let v of vs)for(let u of [...s])s.add(u^v);return [...s];}
  function mass(F,r,d,c,extra=[],stats={}) {
    const n=F.length, mask=bit(r)-1n, base=xor(F.map(f=>f[0].a)), delta=F.map(f=>f[0].a^f[1].a), target=c^base;
    const rows=extra.concat(eqs(delta.map(x=>x>>BigInt(r)),target>>BigInt(r),d-r));
    stats.calls=(stats.calls||0)+1; stats.affine_checks=(stats.affine_checks||0)+1;
    if(!solve(rows,n))return 0n;
    let z=0n;for(let h=0n;h<bit(r);h++){
      stats.characters=(stats.characters||0)+1;
      let guard=[],ok=true,sg=0n;
      for(let i=0;i<n;i++){
        const allowed=F[i].map(f=>f.w.every(v=>!par(v&h)));
        if(!allowed[0]&&!allowed[1]){ok=false;break;}
        if(!allowed[0]||!allowed[1])guard.push([bit(i),allowed[1]?1:0]);
        if(par(delta[i]&h))sg|=bit(i);
      }
      if(!ok)continue;
      let rr=rows.concat(guard);
      let sign=par(target&h);
      let plus=solve(rr.concat([[sg,sign]]),n),minus=solve(rr.concat([[sg,1-sign]]),n);
      stats.character_linear_solves=(stats.character_linear_solves||0)+2;
      z+=(plus?.count??0n)-(minus?.count??0n);
    }
    if(z<0n)throw Error("negative normalized mass");
    return z;
  }
  function witness(F,r,d,c,extra=[],stats={}) {
    if(!mass(F,r,d,c,extra,stats))return null;
    const n=F.length;let rows=[...extra],t=0n;
    for(let i=0;i<n;i++){
      let a=mass(F,r,d,c,rows.concat([[bit(i),0]]),stats)?0:1;
      rows.push([bit(i),a]);if(a)t|=bit(i);
      // Exact closure is rerun with the accepted literal, not assumed to hold.
      if(!mass(F,r,d,c,rows,stats))throw Error("lost witness");
    }
    const selected=F.map((f,i)=>f[get(t,i)]), cols=selected.flatMap(f=>f.w), offset=xor(selected.map(f=>f.a));
    let q=solve(eqs(cols,c^offset,d),cols.length);if(!q)throw Error("fiber solve");
    let p=0;const ys=selected.map(f=>{let y=f.a;for(let v of f.w){if(get(q.x,p))y^=v;p++;}return y;});
    return {t,ys};
  }
  function check(F,c,extra,w){
    if(!w||xor(w.ys)!==c||extra.some(([a,b])=>par(a&w.t)!==b))return false;
    return F.every((f,i)=>{let s=f[get(w.t,i)];return span(s.w).includes(w.ys[i]^s.a);});
  }
  // Independent reference: enumerate each selector and explicit coset elements,
  // combine local supports by set convolution, then normalize by support size.
  function brute(F,r,c,extra){
    let z=0n;for(let t=0n;t<bit(F.length);t++){
      if(extra.some(([a,b])=>par(a&t)!==b))continue;
      let s=new Set([0n]);for(let i=0;i<F.length;i++){let f=F[i][get(t,i)];let u=span(f.w).map(x=>x^f.a);s=new Set([...s].flatMap(a=>u.map(b=>a^b)));}
      if(s.has(c))z+=bit(r)/BigInt(s.size);
    }return z;
  }
  let seed=0x2012026;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;}
  const stats={}, out={seed:"0x2012026",networks:0,queries:0,sat:0,unsat:0,witness_checks:0,conditional_checks:0,conditional_forcing:0,disagreements:0,scaling:[]};
  for(let k=0;k<240;k++){
    let r=rnd(5),d=r+rnd(5),n=1+rnd(7);
    let F=Array.from({length:n},()=>[0,1].map(()=>({a:BigInt(rnd(2**d)),w:Array.from({length:rnd(4)},()=>BigInt(rnd(2**r)))})));
    let extra=Array.from({length:rnd(4)},()=>[BigInt(rnd(2**n)),rnd(2)]);
    out.networks++;
    for(let j=0;j<6;j++){
      let c=BigInt(rnd(2**d));
      if(j===0){ // planted candidate, still subject to extra rows
        c=xor(F.map(f=>{let q=f[rnd(2)];let s=span(q.w);return q.a^s[rnd(s.length)];}));
      }
      let z=mass(F,r,d,c,extra,stats), ref=brute(F,r,c,extra);
      if(z!==ref)throw Error("mass mismatch");
      out.queries++;if(z){out.sat++;let w=witness(F,r,d,c,extra,stats);if(!check(F,c,extra,w))throw Error("invalid witness");out.witness_checks++;
        let i=rnd(n);const e0=extra.concat([[bit(i),0]]),e1=extra.concat([[bit(i),1]]);
        let m0=mass(F,r,d,c,e0,stats),m1=mass(F,r,d,c,e1,stats);
        if(m0!==brute(F,r,c,e0)||m1!==brute(F,r,c,e1)||m0+m1!==z)throw Error("conditional mismatch");
        out.conditional_checks+=2;if(!m0||!m1)out.conditional_forcing++;
      } else out.unsat++;
    }
  }
  // Analytic family: S_i={0,e_i,e_i+d0}; every local hull rank2 and
  // no first rank<=1 peel; global span rank n+1, guarded direction rank1.
  for(let n of [8,16,32,64,128,256]){
    let F=Array.from({length:n},(_,i)=>[{a:0n,w:[]},{a:bit(i+1),w:[1n]}]);
    let stat={}, sat=mass(F,1,n+1,bit(n)|1n,[],stat),unsat=mass(F,1,n+1,1n,[],stat);
    if(sat!==1n||unsat!==0n)throw Error("scaling");
    const row={factors:n,global_rank:n+1,guarded_rank:1,first_peel_possible:false,sat_mass:String(sat),unsat_mass:String(unsat),decision_stats:stat};
    if(n<=64){let st={},w=witness(F,1,n+1,bit(n)|1n,[],st);if(!check(F,bit(n)|1n,[],w))throw Error("scale witness");row.witness_stats=st;}
    out.scaling.push(row);
  }
  out.total_random_stats=stats;return out;
}
console.log(JSON.stringify(runMS02(),null,2));
