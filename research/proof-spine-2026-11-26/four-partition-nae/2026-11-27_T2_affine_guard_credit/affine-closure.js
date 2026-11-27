function normalize(net, select=null){
 const n=4*net.types.length, adj=Array.from({length:n},()=>[]), seenP=new Set(),seenE=new Set();
 let counts={edgeReads:0,bfsArcs:0,tableRows:0};
 function edge(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
 if(net.format!=="STRICT-EB4-v1")throw Error("format");
 for(let [a,b,s] of net.edges){counts.edgeReads++;const u=Math.floor(a/4),v=Math.floor(b/4),k=[Math.min(u,v),Math.max(u,v)].join(":");if(!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=n||b>=n||u===v||seenP.has(a)||seenP.has(b)||seenE.has(k)||![0,1].includes(s))throw Error("invalid edge");seenP.add(a);seenP.add(b);seenE.add(k);edge(a,b,s)}
 if(seenP.size!==n)throw Error("degree");
 for(let i=0;i<net.types.length;i++){let t=net.types[i];if(t==="E"){for(let j=1;j<4;j++)edge(4*i,4*i+j,0)}else if(t!=="B")throw Error("type")}
 let root=new Int32Array(n).fill(-1),par=new Uint8Array(n);
 for(let i=0;i<n;i++)if(root[i]<0){let q=[i];root[i]=i;for(let j=0;j<q.length;j++)for(let [v,s] of adj[q[j]]){counts.bfsArcs++;let b=par[q[j]]^s;if(root[v]<0){root[v]=i;par[v]=b;q.push(v)}else if(par[v]!==b)throw Error("unexpected equality conflict")}}
 let F=[];
 for(let i=0;i<net.types.length;i++)if(net.types[i]==="B"&&(!select||select.has(i))){const ports=[0,1,2,3].map(j=>4*i+j),v=[...new Set(ports.map(p=>root[p]+1))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**v.length;w++){counts.tableRows++;if(ports.reduce((s,p)=>s+(((w>>v.indexOf(root[p]+1))&1)^par[p]),0)===2)ok.push(w)}if(!ok.every(w=>ok.includes(w^((1<<v.length)-1))))throw Error("complement");F.push({v,ok,ids:[i]})}
 return {F,root,par,counts};
}

function project(F,cap=1000000,gaugeOverride=null){
 let ct={scopeScans:0,rows:0,replayRows:0},freq=new Map();
 for(let a of F)for(let v of a.v)freq.set(v,(freq.get(v)||0)+1);
 let gauge=gaugeOverride??[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0]?.[0];
 const shrink=(a)=>{let i=a.v.indexOf(gauge);if(i<0)return {...a,ok:a.ok.slice()};return {v:a.v.filter(x=>x!==gauge),ok:a.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i)),ids:a.ids.slice()}};
 function merge(fs){let m=new Map();for(let a of fs){let k=a.v.join(",");if(!m.has(k))m.set(k,{...a,ok:a.ok.slice(),ids:a.ids.slice()});else{let b=m.get(k);b.ok=b.ok.filter(w=>a.ok.includes(w));b.ids.push(...a.ids)}}return [...m.values()]}
 let initial=merge(F.map(shrink)),fs=initial.slice(),steps=[];
 const localWord=(a,vs,w)=>a.v.reduce((z,x,i)=>z|((w>>vs.indexOf(x)&1)<<i),0);
 let status="COMPLETE";
 for(;;){
  let occ=new Map();for(let i=0;i<fs.length;i++)for(let v of fs[i].v){if(++ct.scopeScans>cap){status="CAP";break}if(!occ.has(v))occ.set(v,[]);occ.get(v).push(i)}if(status==="CAP")break;
  let cs=[];for(let [v,ix] of occ){let vs=[...new Set(ix.flatMap(i=>fs[i].v))].filter(x=>x!==v).sort((a,b)=>a-b);if(vs.length<=4)cs.push({v,ix,vs})}
  if(!cs.length||fs.some(a=>!a.ok.length))break;
  cs.sort((a,b)=>a.vs.length-b.vs.length||a.ix.length-b.ix.length||a.v-b.v);
  let {v,ix,vs}=cs[0],old=ix.map(i=>fs[i]),all=[v,...vs],ok=[],arg=[];
  for(let w=0;w<2**vs.length;w++){let yes=[];for(let b=0;b<2;b++){ct.rows++;if(old.every(a=>a.ok.includes(localWord(a,all,2*w+b))))yes.push(b)}if(yes.length){ok.push(w);arg.push(yes[0])}}
  let out={v:vs,ok,ids:old.flatMap(a=>a.ids).sort((a,b)=>a-b)};
  steps.push({pivot:v,out,arg});let g=new Set(ix);fs=merge([...fs.filter((_,i)=>!g.has(i)),out]);
 }
 // Independently replay union assignment enumeration and check witness map.
 let live=initial.slice();for(let s of steps){let old=live.filter(a=>a.v.includes(s.pivot)),all=[...s.out.v,s.pivot],hit=new Set();for(let w=0;w<2**all.length;w++){ct.replayRows++;if(old.every(a=>a.ok.some(r=>a.v.every((v,i)=>(r>>i&1)===(w>>all.indexOf(v)&1)))))hit.add(w&((1<<s.out.v.length)-1))}if(JSON.stringify([...hit].sort((a,b)=>a-b))!==JSON.stringify(s.out.ok))throw Error("projection");for(let i=0;i<s.out.ok.length;i++)if(!old.every(a=>a.ok.includes(localWord(a,all,s.out.ok[i]|(s.arg[i]<<s.out.v.length)))))throw Error("witness");live=merge([...live.filter(a=>!a.v.includes(s.pivot)),s.out])}
 if(JSON.stringify(live)!==JSON.stringify(fs))throw Error("residual");
 return {gauge,initial,final:fs,steps,counts:ct,status};
}

function solver(F,mode,cap=700000,depthCap=22){
 const vars=[...new Set(F.flatMap(a=>a.v))].sort((a,b)=>a-b),ix=new Map(vars.map((v,i)=>[v,i+1])),bit=v=>1n<<BigInt(ix.get(v)),high=x=>x.toString(2).length-1;
 let C={rows:0,localParity:0,elimination:0,contexts:0,nodes:0,depth:0,deleted:0,rankMax:0,scoring:0},events=0;
 function tick(k){C[k]++;if(++events>cap)throw Error("cap")}
 function parity(x){let s=0;while(x){s^=1;x&=x-1}return s}
 function close(guard){
   tick("contexts");let T=F.map(a=>a.ok.slice()),pins=new Map(guard),changed=true,rank=0;
   while(changed){changed=false;
    for(let i=0;i<F.length;i++){let a=F[i],old=T[i];T[i]=old.filter(w=>{tick("rows");return a.v.every((v,j)=>!pins.has(v)||pins.get(v)===(w>>j&1))});C.deleted+=old.length-T[i].length;if(!T[i].length)return {no:true,rank};if(T[i].length<old.length)changed=true}
    if(mode==="affine"){
     let B=new Map();function insert(z){while(z>1n){tick("elimination");let p=high(z);if(!B.has(p)){B.set(p,z);return true}z^=B.get(p)}return z===0n}
     function constant(z){while(z>1n){tick("elimination");let p=high(z);if(!B.has(p))return null;z^=B.get(p)}return Number(z)}
     for(let [v,b] of pins)if(!insert(bit(v)^BigInt(b)))return {no:true,rank:B.size};
     for(let i=0;i<F.length;i++){let a=F[i],rr=T[i];for(let mask=1;mask<2**a.v.length;mask++){let b=parity(rr[0]&mask),all=true;for(let w of rr){tick("localParity");if(parity(w&mask)!==b){all=false;break}}if(all){let z=BigInt(b);for(let j=0;j<a.v.length;j++)if(mask>>j&1)z^=bit(a.v[j]);if(!insert(z))return {no:true,rank:B.size}}}}
     rank=B.size;C.rankMax=Math.max(C.rankMax,rank);
     for(let i=0;i<F.length;i++){let a=F[i],old=T[i],constraints=[];for(let mask=1;mask<2**a.v.length;mask++){let z=0n;for(let j=0;j<a.v.length;j++)if(mask>>j&1)z^=bit(a.v[j]);let k=constant(z);if(k!==null)constraints.push([mask,k])}T[i]=old.filter(w=>{tick("rows");return constraints.every(([m,b])=>parity(w&m)===b)});C.deleted+=old.length-T[i].length;if(!T[i].length)return {no:true,rank};if(T[i].length<old.length)changed=true}
    }
    for(let i=0;i<F.length;i++){let a=F[i],rr=T[i];for(let j=0;j<a.v.length;j++){let b=rr[0]>>j&1,all=true;for(let w of rr){tick("rows");if((w>>j&1)!==b){all=false;break}}if(all){let v=a.v[j];if(pins.has(v)&&pins.get(v)!==b)return {no:true,rank};if(!pins.has(v)){pins.set(v,b);changed=true}}}}
   }
   return {no:false,T,pins,rank};
 }
 let root=null;
 function search(guard,d){tick("nodes");C.depth=Math.max(C.depth,d);let a=close(guard);if(d===0)root={no:a.no,rank:a.rank,rows:a.T?.reduce((s,x)=>s+x.length,0),pins:a.pins?.size};
  if(a.no)return 0;
  let scores=new Map();for(let i=0;i<F.length;i++)for(let v of F[i].v){tick("scoring");if(!a.pins.has(v))scores.set(v,(scores.get(v)||0)+2**(4-Math.min(4,F[i].v.filter(v=>!a.pins.has(v)).length)))}
  if(!scores.size){if(F.every((f,i)=>a.T[i].length))return "SAT";throw Error("bad closure")}
  if(d>=depthCap)return null;
  let v=[...scores].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];
  let l=search([...guard,[v,0]],d+1);if(l===null||l==="SAT")return l;let r=search([...guard,[v,1]],d+1);return r===null||r==="SAT"?r:[v,l,r];
 }
 let tree=null,reason="depth cap";try{tree=search([],0);reason=tree===null?"depth cap":tree==="SAT"?"SAT witness":"verified candidate tree"}catch(e){if(e.message!=="cap")throw e;reason="event cap"}
 return {mode,status:tree===null?"UNKNOWN":tree==="SAT"?"SAT":"UNSAT",root,counts:C,events,cap,reason,tree};
}

function independentCheck(F,tree,mode,cap=2500000){
 // Independent affine projection test: pin each candidate row into a cloned Gaussian basis.
 const vars=[...new Set(F.flatMap(a=>a.v))].sort((a,b)=>b-a),ix=new Map(vars.map((v,i)=>[v,BigInt(i+1)])),bit=v=>1n<<ix.get(v),counts={contexts:0,rows:0,parity:0,xors:0,treeNodes:0};
 let ev=0;function tick(k){counts[k]++;if(++ev>cap)throw Error("checker cap")}
 function add(B,z){for(let k=vars.length;k>=1;k--)if(z&(1n<<BigInt(k))){tick("xors");if(B[k]===undefined){B[k]=z;return true}z^=B[k]}return z===0n}
 function closure(guard){tick("contexts");let T=F.map(a=>a.ok.slice()),prev;
  do{prev=T.reduce((s,a)=>s+a.length,0);let B=[];for(let [v,b] of guard)if(!add(B,bit(v)^BigInt(b)))return true;
   for(let i=0;i<F.length;i++){let a=F[i],r=T[i];if(!r.length)return true;for(let m=1;m<2**a.v.length;m++){if(mode!=="affine"&&(m&(m-1)))continue;let values=new Set();for(let w of r){tick("parity");let z=0;for(let j=0;j<a.v.length;j++)if(m>>j&1)z^=w>>j&1;values.add(z)}if(values.size===1){let z=BigInt([...values][0]);for(let j=0;j<a.v.length;j++)if(m>>j&1)z^=bit(a.v[j]);if(!add(B,z))return true}}}
   T=T.map((r,i)=>r.filter(w=>{tick("rows");let X=B.slice();return F[i].v.every((v,j)=>add(X,bit(v)^BigInt(w>>j&1)))}));if(T.some(r=>!r.length))return true;
  }while(T.reduce((s,a)=>s+a.length,0)<prev);return false
 }
 function check(t,g){tick("treeNodes");if(t===0){if(!closure(g))throw Error("unverified conflict");return true}if(!Array.isArray(t)||t.length!==3||!ix.has(t[0])||g.some(([v])=>v===t[0]))throw Error("invalid branch");return check(t[1],[...g,[t[0],0]])&&check(t[2],[...g,[t[0],1]])}
 try{return {verified:check(tree,[]),counts,events:ev}}catch(e){if(e.message!=="checker cap")throw e;return {verified:false,reason:e.message,counts,events:ev}}
}

function cnfFactors(dimacs){return dimacs.trimEnd().split("\n").slice(1).map((l,i)=>{let c=l.trim().split(/\s+/).map(Number).slice(0,-1),v=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);if(v.length>12)return null;return {v,ok:Array.from({length:2**v.length},(_,w)=>w).filter(w=>c.some(l=>(w>>v.indexOf(Math.abs(l))&1)===+(l>0))),ids:[i+1]}})}
module.exports={normalize,project,solver,independentCheck,cnfFactors};
