const fs=require('fs');
function run(data){
 let assertions=0;function ck(x){assertions++;if(!x)throw Error("assert "+assertions)}
 const nae=(a,b,c)=>!(a===b&&b===c),legal=(O,w)=>O.every(o=>nae(...o.t.map(i=>w[i]))),bits=(s,n)=>Array.from({length:n},(_,i)=>Number((BigInt(s)>>BigInt(i))&1n));
 function solve(n,O,pins,eqs,prefer){
  const stats={nodes:0,scans:0,patterns:0,forces:0,cap:4*n*n};const C=O.map(o=>({t:o.t,p:[1,2,3,4,5,6]})).concat(eqs.map(([a,b])=>({t:[a,b],p:[1,2]})));
  let z=Array(n).fill(-1);for(let [i,v] of pins){if(z[i]>=0&&z[i]!==v)return {status:"UNSAT",stats};z[i]=v}
  let exhausted=false;
  function rec(w){
   if(stats.nodes>=stats.cap){exhausted=true;return null}stats.nodes++;
   outer:while(true){for(let {t,p} of C){stats.scans++;let keep=[];for(let a of p){stats.patterns++;if(t.every((i,j)=>w[i]<0||w[i]===((a>>j)&1)))keep.push(a)}if(!keep.length)return null;for(let j=0;j<t.length;j++){let i=t[j],v=(keep[0]>>j)&1;if(w[i]<0&&keep.every(a=>((a>>j)&1)===v)){w[i]=v;stats.forces++;continue outer}}}break}
   let i=w.indexOf(-1);if(i<0)return w;
   for(let v of [prefer[i],1-prefer[i]]){let t=w.slice();t[i]=v;let q=rec(t);if(q)return q;if(exhausted)return null}return null
  }
  let w=rec(z);if(w)ck(legal(O,w)&&pins.every(([i,v])=>w[i]===v)&&eqs.every(([a,b])=>w[a]!==w[b]));
  return {status:w?"SAT":exhausted?"UNKNOWN":"UNSAT",stats,w}
 }
 function job(name,O,x,y,A,d,pins){
  const B=[0,1,2,3].filter(p=>!A.includes(p));ck(x.filter((v,i)=>v!==y[i]).length===1&&x[d]!==y[d]);ck(legal(O.filter(o=>A.includes(o.p)),x)&&legal(O.filter(o=>B.includes(o.p)),y));ck(pins.every(([i,v])=>x[i]===v&&y[i]===v));
  let direct=solve(x.length,O,pins,[],x), targets=[];
  for(let [side,final] of [[A,y],[B,x]]){let eqs=O.filter(o=>side.includes(o.p)&&o.t.includes(d)).map(o=>o.t.filter(i=>i!==d));let res=solve(x.length,O,[...pins,[d,final[d]]],eqs,x);if(res.w){let before=res.w.slice();before[d]^=1;ck(legal(O.filter(o=>side.includes(o.p)),before));ck(legal(O,res.w))}targets.push({side,eqs,...res})}
  return {name,d,A,pins,direct,targets}
 }
 let [dr,m,bw]=data,peer=[job("DR17",dr.registry,dr.x,dr.y,[0,1],0,[])];
 for(let j of m.jobs)peer.push(job(`M23-k${j.k}-pin${j.pin}`,m.owners,bits(j.x,m.n),bits(j.y,m.n),[0,j.k],j.d,j.pin<0?[]:[[0,j.pin]]));
 peer.push(job("BW17",bw.O,bits(bw.x,bw.n),bits(bw.y,bw.n),[0,1],bw.d,[]));
 const plane=[];for(let p=0;p<3;p++)for(let b=0;b<3;b++)plane.push([0,1,2].map(i=>3*i+(p*i+b)%3));for(let i=0;i<3;i++)plane.push([3*i,3*i+1,3*i+2]);
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function sourceRef(T,n){let count=0,w=null;for(let k=0;k<2**n;k++){let z=bits(k,n);if(T.every(t=>nae(...t.map(i=>z[i])))){count++;w??=z}}return {count,w}}
 function build(T,n){
  const R=[];const s=2*n,t=s+1;for(let i=0;i<n;i++)R.push([s,2*i,2*i+1],[t,2*i,2*i+1]);for(let [a,b,c] of T)R.push([2*a+1,2*b,2*c]);
  let O=[],maps=[],wire=[],aux=[],N=0;const v=()=>N++;const add=(p,t)=>O.push({p,t});
  function opp(a,b,p){const u=Array.from({length:9},v);for(let i=0;i<plane.length;i++)if(i!==0&&i!==1)add((Math.floor(i/3)+p)%4,plane[i].map(j=>u[j]));add(p,[a,u[0],u[3]]);add(p,[b,u[1],u[4]]);wire.push({a,b,u})}
  const d=v(),copies=[];
  for(let c=0;c<2;c++){let occ=Array.from({length:2*n+2},()=>[]);function term(i,sign){let a=v();occ[i].push({a,sign});maps.push({a,c,i,sign});return a}
   let u=term(s,0),w=term(t,0);add(c===0?0:2,[d,u,w]);copies.push([u,w]);
   for(let [a,b,c] of R)add(0,[term(a,1),term(b,0),term(c,0)]);
   for(let list of occ)for(let j=1;j<list.length;j++){let l=list[j-1],q=list[j],mid=v();opp(l.a,mid,1);if(l.sign===q.sign)opp(mid,q.a,2);else{let e=v();opp(mid,e,3);opp(e,q.a,2)}}
  }
  while(N%3)v();
  let baseN=N;for(let p=0;p<4;p++){let used=new Set(O.filter(o=>o.p===p).flatMap(o=>o.t));let miss=Array.from({length:baseN},(_,i)=>i).filter(i=>!used.has(i));ck(miss.length%3===0);for(let j=0;j<miss.length;j+=3){let uu=[Array.from({length:21},v),Array.from({length:21},v)];for(let c=0;c<2;c++){for(let i=0;i<21;i++)aux.push([uu[c][i],Number(i>=7&&i<14)^c]);for(let q=0;q<4;q++)for(let k=0;k<7;k++)if(!(q===p&&k===0))add(q,[uu[c][k],uu[c][7+(k+q)%7],uu[c][14+(k+2*q)%7]])}for(let k=0;k<3;k++){let l=[0,7+p,14+2*p][k];add(p,[miss[j+k],uu[0][l],uu[1][l]])}}}
  let pairs=new Set(),slots=new Set();for(let o of O){for(let i of o.t){let key=4*i+o.p;ck(!slots.has(key));slots.add(key)}for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let key=[o.t[j],o.t[k]].sort((a,b)=>a-b).join(",");ck(!pairs.has(key));pairs.add(key)}}ck(slots.size===4*N);
  function lift(zz,dv){let w=Array(N).fill(0);w[d]=dv;for(let {a,c,i,sign} of maps)w[a]=zz[c][i]^sign;
   // path order: each edge sets next intermediate unless its endpoint is a terminal
   const terminals=new Set(maps.map(m=>m.a));for(let {a,b,u} of wire){if(terminals.has(b))ck(w[b]===1-w[a]);else w[b]=1-w[a];let pattern=[0,1,0,0,1,0,0,1,1];let flip=1^w[a];for(let i=0;i<9;i++)w[u[i]]=pattern[i]^flip}
   for(let [i,b] of aux)w[i]=b;return w
  }
  let zero=Array(2*n+2).fill(0),one=zero.map(()=>1),x=lift([zero,one],1),y=lift([zero,one],0),known=lift([one,one],0);
  ck(legal(O.filter(o=>[0,1].includes(o.p)),x)&&legal(O.filter(o=>[2,3].includes(o.p)),y));ck(legal(O,known));ck(x.filter((b,i)=>b!==y[i]).length===1);
  let blockers=[0,1].map(side=>O.filter(o=>o.t.includes(d)&&Math.floor(o.p/2)===side).filter(o=>{let w=side===0?x:y;return o.t.filter(i=>i!==d).every(i=>w[i]!==w[d])}).length);ck(blockers.every(b=>b===1));
  const ref=sourceRef(T,n);let target=[];
  if(ref.w){let seed=Array(2*n+2).fill(0);for(let i=0;i<n;i++){seed[2*i]=ref.w[i];seed[2*i+1]=1-ref.w[i]}seed[s]=0;seed[t]=1;ck(R.every(([a,b,c])=>seed[a]===seed[b]||seed[a]===seed[c]));
    for(let side of [0,1]){let w=side===0?lift([seed,one],0):lift([zero,seed],1);let before=w.slice();before[d]^=1;ck(legal(O,w)&&legal(O.filter(o=>Math.floor(o.p/2)===side),before));ck(aux.every(([i,b])=>w[i]===b));target.push({side,maskWeight:w.filter((b,i)=>i!==d&&b!==y[i]).length})}
  }
  return {n,clauses:T.length,originalModels:ref.count,compiledN:N,compiledOwners:O.length,blockers,knownSat:true,targetPositiveLifts:target,negativeScope:"negative from exact source projection theorem and exhaustive original reference, not full physical search"}
 }
 let controls=[build(fano,7),build(fano.slice(1),7),build(plane,9),build(plane.slice(2),9)];
 return {peer,controls,assertions}
}
const data=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));console.log(JSON.stringify(run(data),null,2));
