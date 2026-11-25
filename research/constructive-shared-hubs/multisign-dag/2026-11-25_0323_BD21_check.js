function run(rt,da){
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};const hi=x=>31-Math.clz32(x);
 let checks=0, solves=0;function assert(b){checks++;if(!b)throw Error("assertion "+checks)}
 function system(rows){solves++;let B=new Map();for(let [m,b] of rows){while(m){let p=hi(m);if(!B.has(p)){B.set(p,[m,b]);break}let [a,c]=B.get(p);m^=a;b^=c}if(!m&&b)return null}let x=0;for(let p of [...B.keys()].sort((a,b)=>a-b)){let [m,b]=B.get(p);if(parity(m&x)!==b)x^=1<<p}return x}
 function evalE(M,x){let v=0;for(let [m,a] of M)v+=parity(m&x)?-a:a;return v}
 function add(M,m,a){let b=(M.get(m)||0)+a;if(!Number.isSafeInteger(b))throw Error("precision");if(b)M.set(m,b);else M.delete(m)}
 function elim(M,q){let p=1<<hi(q),U=[],V=[];for(let [m,a] of M)(parity(m&q)?V:U).push([m,a]);if(!V.length)return null;
  let D=new Map(),k=V.length,den=1,terms=[];
  let j=V.reduce((j,v,i)=>Math.abs(v[1])>Math.abs(V[j][1])?i:j,0);let dom=Math.abs(V[j][1])>=V.reduce((s,v,i)=>s+(i===j?0:Math.abs(v[1])),0);
  if(dom){let [m,a]=V[j];terms.push([0,-Math.abs(a)]);V.forEach(([u,b],i)=>{if(i!==j)terms.push([m^u,-Math.sign(a)*b])})}
  else{if(k>3)return null;den=1<<(k-1);let [m,a]=V[0],rest=V.slice(1);for(let s=0;s<den;s++){let z=0,w=0;for(let t=0;t<den;t++){let v=a;rest.forEach(([,b],i)=>v+=(t>>i&1)?-b:b);z+=(parity(s&t)?1:-1)*Math.abs(v)}rest.forEach(([u],i)=>{if(s>>i&1)w^=m^u});terms.push([w,z])}}
  U.forEach(([m,a])=>add(D,m&~p,a*den));terms.forEach(([m,a])=>add(D,m&~p,a));return {D,q,p,den,V,dom}
 }
 function solveEnergy(M,n){let root=new Map(M),log=[],scale=1,attempts=0,mode=null,word=null;for(;;){let terms=[...M].filter(([m])=>m),masks=terms.map(([m])=>m);if(!terms.length){mode="constant";word=0;break}let B=(M.get(0)||0)-terms.reduce((s,[,a])=>s+Math.abs(a),0);if(B>0){mode="positive-bound";break}if(B===0){word=system(terms.map(([m,a])=>[m,+(a>0)]));mode=word===null?"offset-conflict":"offset-witness";break}
  let q=null;
  // Test actual coordinate directions for dominant high-fanout moves first.
  for(let i=0;i<n;i++){let z=1<<i,V=terms.filter(([m])=>parity(m&z));if(V.length&&Math.max(...V.map(([,a])=>Math.abs(a)))*2>=V.reduce((s,[,a])=>s+Math.abs(a),0)){q=z;break}}
  if(q===null){function visit(start,left,S){if(q!==null)return;if(!left){attempts++;let z=system(masks.map((m,j)=>[m,+S.includes(j)]));if(z!==null)q=z;return}for(let j=start;j<=masks.length-left;j++){visit(j+1,left-1,[...S,j]);if(q!==null)return}}for(let k=1;k<=3&&q===null;k++)visit(0,k,[])}
  if(q===null){mode="OPEN";break}
  let prev=M,e=elim(M,q);assert(e!==null);M=e.D;scale*=e.den;assert([...M].filter(([m])=>m).length<=terms.length);
  // Every local identity independently checked on the complete small cube.
  for(let x=0;x<1<<n;x++)if(!(x&e.p))assert(evalE(M,x)===e.den*Math.min(evalE(prev,x),evalE(prev,x^q)));
  log.push(e)
 }
 let min=null;if(mode==="constant")min=(M.get(0)||0)/scale;
 if(word!==null){for(let i=log.length-1;i>=0;i--){let e=log[i];assert(!(word&e.p));let f=evalE(e.V,word);if(f>0)word^=e.q}if(mode==="offset-witness")min=0;assert(evalE(root,word)===min)}
 return {mode,min,word,steps:log.length,dominant:log.filter(e=>e.dom).length,maxFanout:Math.max(0,...log.map(e=>e.V.length)),initialTerms:[...root].filter(([m])=>m).length,remainingTerms:[...M].filter(([m])=>m).length,attempts,scale}
 }
 function test(n,reg,cuts){
 let basis=new Map(),passes=0,inferred=0,contradiction=false;
 function put(m,b){while(m){let p=hi(m);if(!basis.has(p)){basis.set(p,[m,b]);return 1}let [u,v]=basis.get(p);m^=u;b^=v}return b?-1:0}
 function reduce(m,b=0){for(let p of [...basis.keys()].sort((a,b)=>b-a))if(m>>p&1){let [u,v]=basis.get(p);m^=u;b^=v}return [m,b]}
 function form(o){let [a,b,c]=o.t,v=o.bad[0];return [[(1<<a)^(1<<b),(v^(v>>1))&1],[(1<<a)^(1<<c),(v^(v>>2))&1]].map(([m,b])=>reduce(m,b))}
 function close(){let change;do{change=false;passes++;for(let o of reg){let [[a,b],[c,d]]=form(o);if((!a&&b)||(!c&&d)||(a===c&&b!==d))continue;if(!a&&!c){contradiction=true;return}if(!a||!c||a===c){let s=put(a||c,(a?b:d)^1);if(s<0){contradiction=true;return}if(s){inferred++;change=true;break}}}}while(change)}
 close();for(let [m,b] of cuts){if(contradiction)break;let s=put(parseInt(m,16),b);if(s<0){contradiction=true;break}close()}if(!contradiction)close();
 let count=0,reference=Infinity;let M=new Map();for(let o of reg){let [[a,b],[c,d]]=form(o);add(M,0,1);add(M,a,b?-1:1);add(M,c,d?-1:1);add(M,a^c,b^d?-1:1)}
 for(let x=0;x<1<<n;x++){let e=reg.reduce((s,o)=>s+ +o.bad.includes(o.t.reduce((v,t,i)=>v|((x>>t&1)<<i),0)),0);if(!e){count++;assert(cuts.every(([m,b])=>parity(x&parseInt(m,16))===b));assert(!contradiction&&[...basis.values()].every(([m,b])=>parity(x&m)===b))}if(!contradiction&&[...basis.values()].every(([m,b])=>parity(x&m)===b)){assert(evalE(M,x)===4*e);reference=Math.min(reference,4*e)}}
 if(contradiction){assert(count===0);return {count,passes,inferred,mode:"local-contradiction"}}
 let z=solveEnergy(M,n);if(z.mode!=="OPEN"){if(z.min!==null)assert(z.min===reference);else assert(reference>0);if(z.word!==null){let x=z.word;for(let p of [...basis.keys()].sort((a,b)=>a-b)){let [m,b]=basis.get(p);if(parity(x&m)!==b)x^=1<<p}assert(evalE(M,x)===reference);z.sourceWord=x}}
 return {count,passes,inferred,reference,...z}
 }
 let out=[];for(let i=0;i<rt.controls.length;i++){let {n,registry:r}=rt.controls[i],d=da.rt[i],neighbor=r.map((o,j)=>j?o:{...o,bad:o.bad.map(x=>x^1)});out.push({n,root:test(n,r,[]),combined:test(n,r,d.alternating.accepted),neighbor:test(n,neighbor,[]),neighborCombined:test(n,neighbor,d.neighborAlternating.accepted)})}
 let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,bad:[0,7]}));let f=[test(7,fano,[])];for(let i=0;i<7;i++)for(let j=0;j<3;j++)f.push(test(7,fano.map((o,k)=>k===i?{...o,bad:o.bad.map(v=>v^(1<<j))}:o),[]));
 // Signed dense parity example, direct min, use three toggled terms in a non-coordinate direction.
 let synthetic=[];let seed=711;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
 for(let i=0;i<80;i++){let n=5,M=new Map();for(let j=0;j<8;j++)add(M,1+rnd(31),rnd(9)-4);let min=Math.min(...Array.from({length:1<<n},(_,x)=>evalE(M,x)));add(M,0,-min+(i%2));let a=solveEnergy(M,n);if(a.mode!=="OPEN"){if(a.min!==null)assert(a.min===i%2);else assert(i%2===1)}synthetic.push(a)}
 return {checks,solves,out,fano:f,synthetic:{cases:synthetic.length,closed:synthetic.filter(a=>a.mode!=="OPEN").length,steps:synthetic.reduce((s,a)=>s+a.steps,0),dominant:synthetic.reduce((s,a)=>s+a.dominant,0),maxFanout:Math.max(...synthetic.map(a=>a.maxFanout))}}
}
if(require.main===module){const fs=require("fs");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2))}
