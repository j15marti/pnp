"use strict";
function experiment(){
  const R={seed:314159265,random:{cases:0,queries:0,sat:0,unsat:0,lifts:0,prunes:0,dpTransitions:0},forest:{cases:0,queries:0,forced:0,deleted:0,empty:0},cube:{cases:0,sat:0,unsat:0},barrier:[],assertions:0};
  let seed=R.seed; function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
  function check(x){R.assertions++;if(!x)throw Error("assert "+R.assertions)}
  function par(x){let p=0;while(x){p^=1;x&=x-1}return p}
  const vals=[0,1,2,3], perms=[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]];
  const val=(f,z,d)=>par(f[0]&(z|(1<<d)))+2*par(f[1]&(z|(1<<d)));
  const con=(v,d)=>[(v&1)<<d,(v>>1)<<d];
  const mask=(b,z,d)=>vals.filter(v=>!b.some(f=>val(f,z,d)===v));
  const xor=(a,b)=>[a[0]^b[0],a[1]^b[1]];
  function events(b,d){let out=[];if(b.length<4)return out;for(let i=1;i<b.length;i++)for(let j=i+1;j<b.length;j++)for(let k=j+1;k<b.length;k++)for(const p of perms){let e=[];for(const [t,v] of [[i,p[0]],[j,p[1]],[k,p[2]]])e.push(...xor(xor(b[t],b[0]),con(v,d)));out.push(e)}return out}
  function reduce(row,base,d){for(let i=d-1;i>=0;i--)if((row&(1<<i))&&base[i])row^=base[i];return row}
  function insert(row,base,d){row=reduce(row,base,d);if(!row)return 0;if(row===(1<<d))return -1;let i=31-Math.clz32(row&((1<<d)-1));base[i]=row;return 1}
  function closure(G,E,d){let B=Array(d).fill(0),C=1<<d;for(const r of G)if(insert(r,B,d)<0)return null;let es=E.slice();while(true){let changed=false;for(let i=0;i<es.length;i++){let b=B.slice(),added=[];let impossible=false;for(const r of es[i]){let t=reduce(r,b,d),s=insert(t,b,d);if(s<0){impossible=true;break}if(s>0)added.push(t)}if(impossible){es.splice(i,1);R.forest.deleted++;changed=true;break}if(!added.length){R.forest.empty++;return null}if(added.length===1){check(insert(added[0]^C,B,d)===1);R.forest.forced++;changed=true;break}}if(!changed)return {B,E:es}}}
  function holds(e,z,d){return e.every(r=>!par(r&(z|(1<<d))))}
  function dp(ms,countStats=true){let a=[1n,0n,0n,0n], hist=[a];for(const s of ms){let b=[0n,0n,0n,0n];for(const x of vals)for(const y of s){b[x^y]+=a[x];if(countStats)R.random.dpTransitions++}a=b;hist.push(a)}return hist}
  // graph manifests: edge objects {u,v,b}; blocks list edge index lists, length1 bridge.
  function solve(n,edges,blocks,z,d){
    let ms=edges.map(e=>mask(e.b,z,d));
    if(ms.some(x=>!x.length))return {count:0n};
    // Exact pointwise cycle support closure, one deletion then restart, before any traceback.
    while(true){let changed=false;for(const block of blocks){if(block.length===1)continue;let ss=block.map(i=>ms[i]);if(!dp(ss).at(-1)[0])return {count:0n};for(let j=0;j<block.length&&!changed;j++){for(const y of ms[block[j]]){let tt=ss.map((a,k)=>k===j?[y]:a);if(!dp(tt).at(-1)[0]){ms[block[j]]=ms[block[j]].filter(t=>t!==y);R.random.prunes++;changed=true;break}}}if(changed)break}if(!changed)break}
    let delta=Array(edges.length),ct=1n;
    for(const block of blocks){if(block.length===1){let i=block[0];ct*=BigInt(ms[i].length);delta[i]=ms[i][0];continue}let h=dp(block.map(i=>ms[i]));ct*=h.at(-1)[0];let t=0;for(let j=block.length-1;j>=0;j--){let i=block[j],y=ms[i].find(y=>h[j][t^y]>0n);check(y!==undefined);delta[i]=y;t^=y}check(t===0)}
    let color=Array(n).fill(-1),adj=Array.from({length:n},()=>[]);edges.forEach((e,i)=>{adj[e.u].push([e.v,delta[i]]);adj[e.v].push([e.u,delta[i]])});
    for(let s=0;s<n;s++)if(color[s]<0){ct*=4n;color[s]=0;let q=[s];for(let k=0;k<q.length;k++){let u=q[k];for(const [v,t] of adj[u]){if(color[v]<0){color[v]=color[u]^t;q.push(v)}else check(color[v]===(color[u]^t))}}}
    check(edges.every(e=>!e.b.some(f=>val(f,z,d)===(color[e.u]^color[e.v]))));return {count:ct,color};
  }
  function brute(n,edges,z,d){let c=0n;for(let x=0;x<4**n;x++){let y=x,colors=[];for(let j=0;j<n;j++){colors.push(y%4);y=Math.floor(y/4)}if(edges.every(e=>!e.b.some(f=>val(f,z,d)===(colors[e.u]^colors[e.v]))))c++}return c}
  function randB(d){return Array.from({length:1+rnd(6)},()=>[rnd(1<<(d+1)),rnd(1<<(d+1))])}
  for(let t=0;t<120;t++){let d=3,edges=[],blocks=[],n=1;function add(u,v){edges.push({u,v,b:randB(d)});return edges.length-1}let typ=t%3;if(typ===0){blocks.push([add(0,n++)],[add(1,n++)],[add(1,n++)])}else{let a=n++,b=n++;blocks.push([add(0,a),add(a,b),add(b,0)]);if(typ===1)blocks.push([add(b,n++)]);else{let c=n++,e=n++;blocks.push([add(b,c),add(c,e),add(e,b)])}}
    R.random.cases++;for(let z=0;z<1<<d;z++){let a=solve(n,edges,blocks,z,d),b=brute(n,edges,z,d);check(a.count===b);R.random.queries++;if(b){R.random.sat++;R.random.lifts++}else R.random.unsat++}}
  for(let t=0;t<120;t++){let d=5,bs=Array.from({length:1+rnd(3)},()=>randB(d));let G=Array.from({length:rnd(3)},()=>rnd(1<<(d+1)));let E=bs.flatMap(b=>events(b,d)),C=closure(G,E,d);R.forest.cases++;for(let z=0;z<1<<d;z++){let a=holds(G,z,d)&&bs.every(b=>mask(b,z,d).length),b=!!C&&holds(C.B.filter(Boolean),z,d)&&!C.E.some(e=>holds(e,z,d));check(!!a===b);R.forest.queries++}}
  // All subformulas of full 3-variable clause cube, a separate star edge for each clause.
  for(let F=0;F<256;F++){let d=3,C=1<<d,bs=[];for(let a=0;a<8;a++)if(F>>a&1){let b=[con(0,d)];for(let j=0;j<3;j++){let falseForm=(1<<j)^((1^((a>>j)&1))*C),v=j+1;b.push([v&1?falseForm:0,v&2?falseForm:0])}bs.push(b)}let E=bs.flatMap(b=>events(b,d)),cl=closure([],E,d);let cnt=0;for(let z=0;z<8;z++){let ref=!(F>>z&1);let pred=!!cl&&holds(cl.B.filter(Boolean),z,d)&&!cl.E.some(e=>holds(e,z,d));check(ref===pred);check(ref===bs.every(b=>mask(b,z,d).length>0));if(pred)cnt++}check(cnt===8-vals.reduce((s,_,i)=>s+((F>>i)&1)+((F>>(i+4))&1),0));R.cube.cases++;if(cnt)R.cube.sat++;else R.cube.unsat++}
  // Barrier cycle. For large tests evaluate fixed chart first and use constant forms.
  for(const n of [2,3,4,5,8,16,32,64,128]){function graph(pairs){let d=0,edges=pairs.map(([a,b],i)=>({u:i,v:i+1,b:[2,3,2^(3*a),2^(3*b)].map(x=>con(x,d))}));edges.push({u:n,v:0,b:[0,2,3].map(x=>con(x,d))});return edges}let tested=0,rejected=0;
    function run(pairs){let zc=pairs.filter(p=>!p[0]&&!p[1]).length,es=graph(pairs),a=solve(n+1,es,[es.map((_,i)=>i)],0,0);let expected=zc?4n*(1n<<BigInt(zc-1)):0n;check(a.count===expected);if(n<=5)check(a.count===brute(n+1,es,0,0));tested++;if(!a.count)rejected++}
    if(n<=5){for(let z=0;z<4**n;z++){let y=z,p=[];for(let i=0;i<n;i++){let c=y%4;y=Math.floor(y/4);p.push([c&1,c>>1])}run(p)}check(BigInt(rejected)===3n**BigInt(n))}else{run(Array.from({length:n},()=>[1,0]));run(Array.from({length:n},(_,i)=>i?[1,0]:[0,0]));run(Array.from({length:n},()=>[0,0]))}
    R.barrier.push({n,tested,rejected,affineCoverLower:((3n**BigInt(n)+(1n<<BigInt(n))-1n)/(1n<<BigInt(n))).toString()});
  }
  return R;
}
console.log(JSON.stringify(experiment(),null,2));
