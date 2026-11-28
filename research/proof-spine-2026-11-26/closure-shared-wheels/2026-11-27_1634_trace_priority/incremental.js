function experiment(n,orig,mode,width,cap=2000000){
 let start=Date.now(),work=0,flips=0,changed=0,pairs=0,learned=[],nodes=0,trace=[],minima=[],initial=[],hits=0,checks=0,status="UNKNOWN",tree=null,stage="early",peak=0,peakLits=0;
 const canon=c=>[...new Set(c)].sort((a,b)=>a-b),key=c=>c.join(","),tick=(k=1)=>{work+=k;if(work>cap)throw Error("cap")};
 let root=[...new Map(orig.map(c=>{let a=canon(c);return[key(a),a]})).values()].filter(c=>!c.some(l=>c.includes(-l))),F=root.slice(),seen=new Set(F.map(key)),init=Array(n+1).fill(-1);
 function prop(a){a=a.slice();let more=true;while(more){more=false;for(let c of F){let k=0,last=0,sat=false;for(let l of c){tick();let x=a[Math.abs(l)];if(x<0){k++;last=l}else if(x===Number(l>0)){sat=true;break}}if(sat)continue;if(!k)return null;if(k===1){a[Math.abs(last)]=Number(last>0);more=true}}}return a}
 function walk(res,phase){
 const adj=Array.from({length:n+1},()=>[]);F.forEach((c,j)=>c.forEach(l=>{tick();adj[Math.abs(l)].push([j,l])}));
 for(let seed of [0,1]){
  let a=init.map(x=>x<0?seed:x),k=[],ss=[],sole=[],bad=0,zero=0;
  function scan(j){let count=0,sum=0,last=0;for(let l of F[j]){tick();if(a[Math.abs(l)]===Number(l>0)){count++;sum+=Math.sign(l);last=l}}return[count,sum,count===1?last:0]}
  const mod=x=>(x%3+3)%3, z=(k,s)=>Number(k>0&&mod(s)===0);
  for(let j=0;j<F.length;j++){let [v,w,l]=scan(j);k.push(v);ss.push(w);sole.push(l);bad+=Number(!v);zero+=z(v,w);tick(2)}
  function snapshot(){return k.map((v,j)=>{tick(2);return[v,v%3,mod(ss[j]),sole[j]]})}
  initial.push({phase,seed,rows:snapshot()});if(!phase)trace.push(snapshot());
  while(bad){
    let best=bad,v=0,plain=0,bz=Infinity;
    for(let i=1;i<=n;i++)if(init[i]<0){let cb=bad,cz=zero;for(const [j,l] of adj[i]){let d=a[i]===Number(l>0)?-1:1,nk=k[j]+d,ns=ss[j]+Math.sign(l)*d;tick(4);cb+=Number(!nk)-Number(!k[j]);if(res){tick(2);cz+=z(nk,ns)-z(k[j],ss[j])}}if(cb<best){best=cb;v=plain=i;bz=cz}else if(cb===best&&v&&res&&cz<bz){v=i;bz=cz}}
    if(!v)break;if(v!==plain)changed++;a[v]^=1;flips++;
    for(const [j,l] of adj[v]){let [nk,ns,sl]=scan(j);bad+=Number(!nk)-Number(!k[j]);zero+=z(nk,ns)-z(k[j],ss[j]);k[j]=nk;ss[j]=ns;sole[j]=sl;tick(4)}
    if(bad!==best||(res&&zero!==bz))throw Error("delta mismatch");
    // Full replay after every accepted flip, deliberately charged.
    let rb=0,rz=0;for(let j=0;j<F.length;j++){let [nk,ns,sl]=scan(j);tick(2);if(k[j]!==nk||ss[j]!==ns||sole[j]!==sl)throw Error("field mismatch");rb+=Number(!nk);rz+=z(nk,ns)}if(rb!==bad||rz!==zero)throw Error("total mismatch");
    if(!phase)trace.push(snapshot());
  }
  minima.push([phase,seed,bad]);if(!bad)throw Error("SAT trajectory; not classified");
 }
}
function deduce(){let pos=new Map(),neg=new Map();for(let i=0;i<root.length;i++)for(let l of root[i]){tick();let m=l>0?pos:neg,v=Math.abs(l),a=m.get(v)||[];a.push(i);m.set(v,a)}let C=[];for(let v=1;v<=n;v++)for(let i of pos.get(v)||[])for(let j of neg.get(v)||[]){pairs++;tick();let r=canon(root[i].filter(x=>x!==v).concat(root[j].filter(x=>x!==-v)));tick(root[i].length+root[j].length+r.length);if(r.length>width||r.some(l=>r.includes(-l))||seen.has(key(r)))continue;let h=0;for(let st of trace){tick();let A=st[i],B=st[j];h+=Number((A[0]===0&&B[0]===1&&B[3]===-v)||(B[0]===0&&A[0]===1&&A[3]===v))}C.push({i,j,v,r,h})}
 if(mode==="table"||mode==="residue")C.sort((a,b)=>{tick();return b.h-a.h||a.r.length-b.r.length||a.v-b.v||a.i-b.i||a.j-b.j});for(let {i,j,v,r,h} of C){tick();if(seen.has(key(r)))continue;seen.add(key(r));F.push(r);learned.push([i,j,v,r]);hits+=Number(h>0);if(learned.length===64)break}}
 function dpll(a){nodes++;let b=prop(a);if(b===null)return 0;let freq=new Int32Array(n+1);for(let c of F){tick(c.length);if(c.some(l=>b[Math.abs(l)]===Number(l>0)))continue;for(let l of c)if(b[Math.abs(l)]<0)freq[Math.abs(l)]++}let v=0;for(let i=1;i<=n;i++){tick();if(freq[i]>freq[v])v=i}if(!v)throw Error("SAT leaf");let x=b.slice(),y=b.slice();x[v]=0;y[v]=1;return[v,dpll(x),dpll(y)]}
 let forced=0;try{let z=prop(init);if(z!==null){init=z;forced=init.slice(1).filter(x=>x>=0).length;stage="first UP stall";if(["flips","table","residue"].includes(mode))walk(mode==="residue",0);if(["deductions","table","residue"].includes(mode)){deduce();let b=prop(init);if(b!==null){init=b;if(mode!=="deductions")walk(mode==="residue",1)}}}tree=dpll(init);let V=root.slice();for(let [i,j,v,r] of learned){checks++;tick(V[i].length+V[j].length+r.length);if(!V[i].includes(v)||!V[j].includes(-v)||key(canon(V[i].filter(l=>l!==v).concat(V[j].filter(l=>l!==-v))))!==key(r))throw Error("resolvent");V.push(r)}
 function verify(t,a){a=new Map(a);while(true){let unit=0;for(let c of V){let free=[],sat=false;for(let l of c){tick();if(!a.has(Math.abs(l)))free.push(l);else if(a.get(Math.abs(l))===(l>0)){sat=true;break}}if(sat)continue;if(!free.length)return t===0;if(free.length===1){unit=free[0];break}}if(!unit)break;a.set(Math.abs(unit),unit>0)}if(!Array.isArray(t)||a.has(t[0]))return false;return verify(t[1],[...a,[t[0],false]])&&verify(t[2],[...a,[t[0],true]])}
 if(!verify(tree,[]))throw Error("replay");status="UNSAT"}catch(e){stage+="; "+e.message}
 peak=F.length;peakLits=F.flat().length;return{mode,width,status,stage,work,ms:Date.now()-start,flips,changed,pairs,learned:learned.length,nodes,hits,checks,forced,peak,peakLits,minima,initial,proof:status==="UNSAT"?{root,learned,tree}:null}
}

function replayPeer(F,p){let canon=a=>[...new Set(a)].sort((a,b)=>a-b).join(","),checks=0,units=[];const get=id=>{checks++;if(!F[id-1])throw Error("ID");return F[id-1]};for(let u of p.units){let coeff=new Map(),rhs=0;for(let [r,k] of u.terms){let rows=r.ids.map(get).map(canon);if(!rows.includes(canon(r.v)))throw Error("ALO");for(let i=0;i<r.v.length;i++)for(let j=i+1;j<r.v.length;j++){checks++;if(!rows.includes(canon([-r.v[i],-r.v[j]])))throw Error("AMO")}for(let v of r.v)coeff.set(v,(coeff.get(v)||0)+k);rhs+=k}let P=[...coeff].filter(([v,k])=>k>0).map(([v])=>v);if(rhs!==u.rhs||rhs<=0||canon(P)!==canon(u.P)||u.guard[1]!==1||u.unit!==-u.guard[0])throw Error("row sum");for(let v of P){let r=u.zeroReasons.find(x=>x[0]===v);if(!r||canon(get(r[1]))!==canon([-v,-u.guard[0]]))throw Error("reason")}units.push(u.unit)}let a=new Map(units.map(l=>[Math.abs(l),l>0])),conflict=0,trace=[];while(!conflict){let more=false;for(let i=0;i<F.length;i++){let free=[],sat=false;for(let l of F[i]){checks++;if(!a.has(Math.abs(l)))free.push(l);else if(a.get(Math.abs(l))===(l>0)){sat=true;break}}if(sat)continue;if(!free.length){conflict=i+1;break}if(free.length===1){a.set(Math.abs(free[0]),free[0]>0);trace.push([free[0],i+1]);more=true}}if(!more)break}return{verified:!!conflict,units,conflict,trace,checks}}
