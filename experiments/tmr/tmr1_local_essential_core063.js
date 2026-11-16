"use strict";
// TMR-1/063 source-authenticated locally essential input/gate compression.
// Native JS/V8 and Node 22, revision tmr1-local-essential-core063-js-v1, seed 20261115.
function run063() {
  let state=20261115>>>0, assertions=0;
  const fail=m=>{throw Error(m)};
  function ok(b,m){assertions++;if(!b)fail(m)}
  function rnd(n){state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n}
  const low=(v,w)=>Array.from({length:w},(_,j)=>String((v>>>j)&1)).join("");
  function encode(q,gates,root){
    const V=q+gates.length,w=Math.floor(Math.log2(Math.max(2,V)))+1;
    return "1".repeat(q)+"0"+"1".repeat(gates.length)+"0"+
      gates.map(([a,b,f])=>low(a,w)+low(b,w)+f.join("")).join("")+low(root,w);
  }
  function decode(s){
    if(/[^01]/.test(s))throw Error("nonbinary");
    let i=0;
    function unary(){let n=0;while(i<s.length&&s[i]==="1"){n++;i++}if(i>=s.length)throw Error("unary");i++;return n}
    const q=unary(),G=unary(),V=q+G,w=Math.floor(Math.log2(Math.max(2,V)))+1;
    if(!q||s.length!==i+G*(2*w+4)+w)throw Error("length");
    function pull(w){let n=0;for(let j=0;j<w;j++)n|=(+s[i++])<<j;return n}
    const gates=[];
    for(let j=0;j<G;j++){
      const a=pull(w),b=pull(w),f=Array.from({length:4},()=>+s[i++]);
      if(a>=q+j||b>=q+j)throw Error("forward");gates.push([a,b,f]);
    }
    const root=pull(w);if(root>=V||i!==s.length)throw Error("root");
    return {q,gates,root};
  }
  function full(q,gates,root,mask){
    const vals=Array.from({length:q},(_,i)=>(mask>>>i)&1);
    for(const [a,b,f] of gates)vals.push(f[2*vals[a]+vals[b]]);
    return vals[root];
  }
  function form(a,b,f){
    if(a===b){
      const v=[f[0],f[3]];
      return v[0]===v[1]?["C",[],[v[0]]]:["U",[a],v];
    }
    const eA=f[0]!==f[2]||f[1]!==f[3];
    const eB=f[0]!==f[1]||f[2]!==f[3];
    if(eA&&eB)return ["B",[a,b],f];
    if(eA)return ["U",[a],[f[0],f[2]]];
    if(eB)return ["U",[b],[f[0],f[1]]];
    return ["C",[],[f[0]]];
  }
  function quotient(q,gates,root){
    const meta=gates.map(([a,b,f])=>form(a,b,f)), live=new Set(), inputs=new Set();
    function visit(id){
      if(id<q){inputs.add(id);return}
      if(live.has(id))return;
      live.add(id);
      for(const child of meta[id-q][1])visit(child);
    }
    visit(root);
    const ix=[...inputs].sort((a,b)=>a-b), gx=[...live].sort((a,b)=>a-b);
    const ids=ix.concat(gx),mapping=new Map(ids.map((old,j)=>[old,j]));
    return {q,r:ix.length,L:gx.length,R:ids.length,ix,
      root:mapping.get(root),ops:gx.map(id=>{
        const [kind,kids,f]=meta[id-q];
        return [kind,kids.map(child=>mapping.get(child)),f];
      })};
  }
  function reduced(C,mask){
    const vals=Array.from({length:C.r},(_,i)=>(mask>>>i)&1);
    for(const [kind,ids,f] of C.ops)
      vals.push(kind==="C"?f[0]:kind==="U"?f[vals[ids[0]]]:f[2*vals[ids[0]]+vals[ids[1]]]);
    return [vals[C.root],vals];
  }
  function clauses(C){
    const out=[],lit=(v,b)=>[v,!!b];
    for(let j=0;j<C.ops.length;j++){
      const [kind,ids,f]=C.ops[j],z=C.r+j;
      if(kind==="C")out.push([lit(z,f[0])]);
      else if(kind==="U"){
        for(let u=0;u<2;u++)out.push([lit(ids[0],!u),lit(z,f[u])]);
      }else for(let u=0;u<2;u++)for(let v=0;v<2;v++)
        out.push([lit(ids[0],!u),lit(ids[1],!v),lit(z,f[2*u+v])]);
    }
    out.push([lit(C.root,true)]);
    return out;
  }
  const key=c=>JSON.stringify(c);
  function totalize(C,original){
    const unique=[...new Map(original.map(c=>[key(c),c])).values()];
    const used=new Set(unique.flatMap(c=>c.map(x=>x[0]))),u=C.R-used.size;
    const d=Math.max(1,4-C.R,Math.ceil((unique.length+u+1-4*C.R)/3));
    for(let j=0;j<C.R;j++)if(!used.has(j))unique.push([[j,true],[j,false]]);
    for(let j=0;j<d;j++)unique.push([[C.R+j,false]]);
    unique.push([[C.R,true],[C.R,false]]);
    const n=C.R+d,m=unique.length;
    ok(n>=4&&m>=2&&m<=4*n,"promise density");
    ok(new Set(unique.map(key)).size===m,"outer NoDup");
    ok(new Set(unique.flatMap(c=>c.map(x=>x[0]))).size===n,"AllOccur");
    ok(unique.every(c=>c.length<=3),"IsKCNF 3");
    return {n,cs:unique,d,u};
  }
  function sat(cs,mask){
    return cs.every(c=>c.some(([i,p])=>((mask>>>i)&1)==Number(p)));
  }
  function formal(F){
    const w=Math.floor(Math.log2(2*F.n))+1;
    let bits="1110"+"1".repeat(F.n)+"0";
    for(const clause of F.cs){
      const slots=clause.map(([i,p])=>2*i+1+Number(p));
      while(slots.length<3)slots.push(0);
      bits+=slots.map(v=>low(v,w)).join("");
    }
    ok(bits.length===F.n+5+3*F.cs.length*w,"encoded length");
    let off=4,n=0;
    while(bits[off]==="1"){off++;n++}off++;
    const decoded=[];
    while(off<bits.length){
      const c=[];
      for(let j=0;j<3;j++){
        let v=0;for(let t=0;t<w;t++)v+=(+bits[off++])*(2**t);
        if(v){const id=Math.floor((v-1)/2);ok(id<n,"slot id");c.push([id,v%2===0])}
      }
      decoded.push(c);
    }
    ok(n===F.n&&key(decoded)===key(F.cs),"formal low-first roundtrip");
    return bits.length;
  }
  function verify(q,gates,root,brute){
    const src=encode(q,gates,root),d=decode(src);
    ok(key(d)===key({q,gates,root}),"authenticate binary source");
    const C=quotient(q,gates,root),F=totalize(C,clauses(C));
    const formbits=formal(F);
    let rawCount=0,coreCount=0;
    for(let x=0;x<2**q;x++){
      const old=full(q,gates,root,x);
      const z=C.ix.reduce((v,id,i)=>v|(((x>>>id)&1)<<i),0);
      const [out,vals]=reduced(C,z);
      ok(out===old,"pointwise quotient");
      rawCount+=old;
      let canonical=0;
      for(let j=0;j<vals.length;j++)canonical|=vals[j]<<j;
      ok(sat(F.cs,canonical)===Boolean(out),"canonical unique extension");
      if(out)for(let j=0;j<F.d;j++)
        ok(!sat(F.cs,canonical|(1<<(C.R+j))),"forced auxiliary");
    }
    for(let x=0;x<2**C.r;x++)coreCount+=reduced(C,x)[0];
    ok(rawCount===coreCount*2**(q-C.r),"full count lift");
    if(brute&&F.n<=12){
      let counted=0;for(let x=0;x<2**F.n;x++)counted+=Number(sat(F.cs,x));
      ok(counted===coreCount,"complete CNF truth cube");
    }
    return {q,G:gates.length,r:C.r,L:C.L,rawCount,coreCount,srcbits:src.length,formbits};
  }
  const summary={cases:0,raw_assignments:0,formal_bits:0,pruned_inputs:0,pruned_gates:0,malformed:0,stress:0};
  let hash=0;
  function record(q,g,root,brute){
    const a=verify(q,g,root,brute);summary.cases++;
    summary.raw_assignments+=2**q;summary.formal_bits+=a.formbits;
    if(a.r<q)summary.pruned_inputs++;
    if(a.L<g.length)summary.pruned_gates++;
    for(const n of [a.q,a.G,a.r,a.L,a.rawCount,a.coreCount])
      hash=Math.imul(hash^n,16777619)>>>0;
  }
  record(5,[],3,true);
  record(7,[[0,0,[0,1,1,0]]],7,true);
  record(7,[[0,0,[0,0,0,1]]],7,true);
  record(7,[[1,2,[1,0,0,1]]],7,true);
  record(5,[[0,1,[1,1,0,1]]],5,true);
  record(5,[[0,1,[0,1,1,0]],[5,2,[0,1,1,0]]],6,true);
  record(5,[[0,1,[0,0,0,1]],[2,3,[1,1,1,0]],[5,6,[0,0,0,1]]],7,true);
  let g=[],parts=[],q=8;
  for(let i=0;i<4;i++){g.push([i,i+4,[1,1,1,0]]);parts.push(q+g.length-1)}
  let last=parts[0];for(const id of parts.slice(1)){g.push([last,id,[0,0,0,1]]);last=q+g.length-1}
  record(q,g,last,true);
  for(let k=0;k<300;k++){
    const q=1+rnd(7),G=rnd(11),g=[];
    for(let j=0;j<G;j++)
      g.push([rnd(q+j),rnd(q+j),Array.from({length:4},()=>rnd(2))]);
    record(q,g,rnd(q+G),k<70);
  }
  const good=encode(3,[[0,1,[0,0,0,1]]],3);
  const bad=[good+"0",good.slice(0,-1),good+"2",good.replace("0","2"),"1","0"+good.slice(1),"1".repeat(good.length),"","0000"];
  for(const s of bad){
    try{decode(s);fail("accepted malformed source")}
    catch(e){if(e.message==="accepted malformed source")throw e;summary.malformed++}
  }
  for(const n of [16,32,64]){
    const gates=[[0,0,[0,1,1,0]]];
    for(let i=0;i<n*n-1;i++)gates.push([i%n,(i+1)%n,[0,0,0,1]]);
    const C=quotient(n,gates,n);
    ok(C.r===0&&C.L===1,"prune real dead gate overload");summary.stress++;
  }
  return {revision:"tmr1-local-essential-core063-js-v1",seed:20261115,
    assertions,failures:0,summary,trace_hash:hash.toString(16).padStart(8,"0"),
    evidence:"finite exhaustive original and partial full CNF valuations; not a Lean kernel or an asymptotic proof"};
}
if(typeof module!=="undefined"&&require.main===module)
  console.log(JSON.stringify(run063(),null,2));
