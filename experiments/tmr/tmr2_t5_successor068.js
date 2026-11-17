"use strict";
// Standalone Node v22+ audit of source-encoded T5 exact counter, not a general P/NP lower bound.
const audit=function audit(){
  "use strict";
  const revision="tmr2-t5-succ068.v1", seed=202611171336;
  let checks=0, state=seed>>>0;
  const rng=()=>((state=Math.imul(state,1664525)+1013904223>>>0)/4294967296);
  const beat=(a,b)=>((b-a+5)%5===1||(b-a+5)%5===3);
  function parse(src){
    if(!/^[\x00-\x7f]*$/.test(src)||!src.endsWith("\n"))throw Error("nonascii/unterminated");
    const lines=src.slice(0,-1).split("\n"),m=/^p t5 (0|[1-9][0-9]*) (0|[1-9][0-9]*)$/.exec(lines[0]);
    if(!m)throw Error("header");
    const n=Number(m[1]),a=Number(m[2]);
    if(!Number.isSafeInteger(n)||!Number.isSafeInteger(a)||n>src.length||a>src.length||lines.length!==1+n+a)throw Error("unexpanded declarations");
    for(let i=0;i<n;i++)if(lines[1+i]!==`v ${i}`)throw Error("vertex declaration");
    const arcs=[];let old=[-1,-1];
    for(const s of lines.slice(1+n)){
      let v=/^a (0|[1-9][0-9]*) (0|[1-9][0-9]*)$/.exec(s);
      if(!v)throw Error("arc syntax");
      const u=Number(v[1]),w=Number(v[2]);
      if(u>=n||w>=n||u<old[0]||(u===old[0]&&w<=old[1]))throw Error("arc bounds/order");
      arcs.push([u,w]);old=[u,w];
    }
    return {n,arcs};
  }
  const key=(u,v)=>`${u},${v}`;
  function recognize(n,arcs){
    if(!arcs.length||arcs.some(([u,v])=>u===v))return null;
    const degI=Array(n).fill(0),degO=Array(n).fill(0),p=Array(n).fill(null),q=Array(n).fill(null),edge=new Set(arcs.map(e=>key(...e)));
    for(const [u,v] of arcs){degO[u]++;degI[v]++;p[v]=u;q[u]=v;}
    const B=new Set(),W=new Set(),X=new Set();
    for(let i=0;i<n;i++){
      if(degI[i]===0&&degO[i]>=2)B.add(i);
      else if(degO[i]===0&&degI[i]>=2)W.add(i);
      else if(degI[i]===1&&degO[i]===1)X.add(i);
      else return null;
    }
    const direct=new Set(arcs.filter(([u,v])=>B.has(u)&&W.has(v)).map(e=>key(...e)));
    if(direct.size!==X.size||arcs.length!==3*direct.size||!direct.size)return null;
    const seen=new Set();
    for(const x of X){
      const u=p[x],v=q[x],id=key(u,v);
      if(!B.has(u)||!W.has(v)||!direct.has(id)||seen.has(id))return null;
      seen.add(id);
      if(!edge.has(key(u,x))||!edge.has(key(x,v)))return null;
    }
    const parent=Array.from({length:n},(_,i)=>i);
    const find=i=>{while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i]}return i};
    for(const id of direct){let [u,v]=id.split(",").map(Number);parent[find(u)]=find(v);}
    let components=new Set([...B,...W].map(find)).size;
    return {components,baseEdges:direct.size,witnesses:X.size,black:B.size,white:W.size};
  }
  function brute(n,arcs){
    if(arcs.some(([u,v])=>u===v))return 0n;
    const prior=Array.from({length:n},()=>[]);
    for(const [u,v] of arcs)prior[Math.max(u,v)].push([Math.min(u,v),u<v]);
    const assigned=Array(n).fill(0);
    function dfs(i){
      if(i===n)return 1n;
      let z=0n;
      for(let a=0;a<5;a++){
        if(prior[i].every(([k,forward])=>forward?beat(assigned[k],a):beat(a,assigned[k]))){assigned[i]=a;z+=dfs(i+1);}
      }
      return z;
    }
    return dfs(0);
  }
  function solve(src){
    const {n,arcs}=parse(src),edges=new Set(arcs.map(e=>key(...e)));
    if(arcs.some(([u,v])=>u===v||edges.has(key(v,u))))return {mode:"local-contradiction",count:"0"};
    if(!arcs.length)return {mode:"empty",count:(5n**BigInt(n)).toString()};
    const cert=recognize(n,arcs);
    if(cert)return {mode:"successor",count:(5n**BigInt(cert.components)).toString(),...cert};
    return {mode:"complete-search",count:brute(n,arcs).toString()};
  }
  const encode=(n,arcs)=>`p t5 ${n} ${arcs.length}\n`+Array.from({length:n},(_,i)=>`v ${i}\n`).join("")+arcs.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]).map(([u,v])=>`a ${u} ${v}\n`).join("");
  function grid(k){
    const n=k*k,E=[];
    for(let i=0;i<k;i++)for(let j=0;j<k;j++)for(const [ii,jj] of [[i+1,j],[i,j+1]]){
      if(ii>=k||jj>=k)continue;
      let a=i*k+j,b=ii*k+jj;E.push((i+j)%2?[b,a]:[a,b]);
    }
    const arcs=[];
    E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]).forEach(([u,v],z)=>{const x=n+z;arcs.push([u,v],[u,x],[x,v]);});
    return {n:n+E.length,arcs:arcs.sort((a,b)=>a[0]-b[0]||a[1]-b[1])};
  }
  for(let x=0;x<5;x++)for(let z=0;z<5;z++){
    let W=Array.from({length:5},(_,w)=>w).filter(w=>beat(x,z)&&beat(x,w)&&beat(w,z));
    if(JSON.stringify(W)!==JSON.stringify(z===(x+1)%5?[(x+3)%5]:[]))throw Error("gadget truth table");
    checks++;
  }
  const grids=[];
  for(let k=2;k<=9;k++){
    const {n,arcs}=grid(k),r=solve(encode(n,arcs));
    if(r.count!=="5"||r.mode!=="successor")throw Error("grid count");
    checks++;
    if(k===2){if(brute(n,arcs)!==5n)throw Error("grid independent brute");checks++;}
    grids.push({side:k,n,arcs:arcs.length,twLowerBound:k,count:r.count});
  }
  const modes={};
  for(let h=0;h<180;h++){
    const n=1+Math.floor(rng()*7),E=[];
    for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(u!==v&&rng()<.24)E.push([u,v]);
    const src=encode(n,E),x=solve(src),y=brute(n,E);
    if(x.count!==y.toString()||y%5n!==0n)throw Error("random exact count or rotation");
    modes[x.mode]=(modes[x.mode]||0)+1;checks+=2;
  }
  const bad=["p t5 1000000000000 0\n","p t5 2 1\nv 0\nv 1\na 1 0","p t5 2 2\nv 0\nv 1\na 0 1\na 0 1\n","p t5 2 1\nv 0\nv 1\na 2 0\n","p t5 2 1\nv 0\nv 0\na 0 1\n","p t5 02 0\nv 0\nv 1\n"];
  for(const src of bad){let rejected=false;try{solve(src)}catch(e){rejected=true}if(!rejected)throw Error("bad input accepted");checks++;}
  return {revision,seed,checks,failures:0,grids,randomValid:180,randomModes:modes,negativeCases:6,gadget:"x->z AND x->w AND w->z iff z=x+1 and w=x+3 mod5",status:"COMPUTATIONAL; full Python-TM microtrace and independent review not run"};
};
console.log(JSON.stringify(audit(),null,2));
