/* BS20: load the immutable BW17 and BS19 JSON objects, then call run(raw,bs). Node usage: node thisfile.js raw.json bs19.json */
function run(raw,bs){
 let assertions=0;const check=(q,s)=>{assertions++;if(!q)throw Error(s)};
 const v=l=>Math.abs(l),sg=l=>+(l<0),bit=(w,i)=>(w>>>i)&1,par=w=>{w^=w>>>16;w^=w>>>8;w^=w>>>4;return (0x6996>>>(w&15))&1};
 const ok=(C,A)=>C.every(c=>c.some(l=>(A[v(l)]^sg(l))!==(A[v(c[0])]^sg(c[0]))));
 function direct(C){let nodes=0,scans=0;
  function rec(A){nodes++;while(true){let changed=false;for(let c of C){scans++;let vals=new Set(c.filter(l=>A[v(l)]!==undefined).map(l=>A[v(l)]^sg(l)));if(vals.size===2)continue;let u=c.filter(l=>A[v(l)]===undefined);if(!u.length)return null;if(u.length===1&&vals.size===1){A[v(u[0])]=1^[...vals][0]^sg(u[0]);changed=true}}if(!changed)break}
   let cnt={};for(let c of C){if(new Set(c.filter(l=>A[v(l)]!==undefined).map(l=>A[v(l)]^sg(l))).size===2)continue;for(let l of c)if(A[v(l)]===undefined)cnt[v(l)]=(cnt[v(l)]||0)+1}
   let k=Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]||a-b)[0];if(k===undefined)return A;for(let b of [0,1]){let B=rec({...A,[k]:b});if(B)return B}return null}
  let A=rec({});if(A)check(ok(C,A),"direct lift");return {sat:!!A,nodes,scans}
 }
 function solve(C,full=false){
  let V=[...new Set(C.flat().map(v))].sort((a,b)=>a-b),P=new Set(),cnt=Object.fromEntries(V.map(x=>[x,C.filter(c=>c.some(l=>v(l)===x)).length]));
  // deterministic maximal private coordinate set, no all-private owner and at most two private incidences
  for(let x of V.slice().sort((a,b)=>cnt[b]-cnt[a]||a-b)){P.add(x);if(C.some(c=>c.filter(l=>P.has(v(l))).length>Math.min(2,c.length-1)))P.delete(x)}
  let X=[...P],Y=V.filter(x=>!P.has(x)),idx=new Map(X.map((x,i)=>[x,i]));
  let comp=new Map(V.map(x=>[x,x]));function root(x){while(comp.get(x)!==x)x=comp.get(x);return x}for(let c of C)for(let l of c)comp.set(root(v(l)),root(v(c[0])));
  let reps=new Map();for(let y of Y)if(!reps.has(root(y)))reps.set(root(y),y);
  let E=Y.filter(y=>reps.get(root(y))!==y),em=new Map(E.map((x,i)=>[x,1<<i])),mask=x=>em.get(x)||0;
  let rows=C.map(c=>{let ex=c.filter(l=>!P.has(v(l))),pr=c.filter(l=>P.has(v(l))),a=ex[0];return {a,act:ex.slice(1).map(l=>[mask(v(a))^mask(v(l)),sg(a)^sg(l)]),pr}});
  let ref=new Map();for(let o of rows)for(let l of o.pr)if(!ref.has(v(l)))ref.set(v(l),v(o.a));
  for(let o of rows)o.sign=o.pr.map(l=>[mask(v(o.a))^mask(ref.get(v(l))),sg(o.a)^sg(l)]);
  let B=[];function add(a){while(a){let h=31-Math.clz32(a);if(B[h])a^=B[h];else{B[h]=a;break}}}
  for(let o of rows)for(let [a] of [...o.act,...o.sign])add(a);
  check(B.filter(Boolean).length===E.length,"gauge rank");
  let stats={private:X,exterior:Y,rank:E.length,components:reps.size,jobs:0,skipped:0,learned:0,rankOne:0,graphEdges:0,pathVisits:0,ownerScans:0,packetTests:0,firstWitness:null,firstJobs:null,fullAccepted:0};
  function chart(w,needLift=true){stats.jobs++;let G=Array.from({length:2*X.length},()=>[]),edge=(a,b,i)=>{G[a].push([b,i]);stats.graphEdges++};
    for(let i=0;i<rows.length;i++){stats.ownerScans++;let o=rows[i];if(o.act.some(([a,b])=>par(a&w)!==b))continue;let f=o.pr.map((l,j)=>2*idx.get(v(l))+(par(o.sign[j][0]&w)^o.sign[j][1]));if(!f.length)return {bad:[i]};if(f.length===1)edge(f[0],f[0]^1,i);else{edge(f[0],f[1]^1,i);edge(f[1],f[0]^1,i)}}
    function path(a,b){let Q=[a],prev=new Map([[a,null]]);for(let j=0;j<Q.length;j++){let z=Q[j];stats.pathVisits++;if(z===b){let t=[];while(z!==a){let [p,i]=prev.get(z);if(i>=0)t.push(i);z=p}return t}for(let [u,i] of G[z])if(!prev.has(u)){prev.set(u,[z,i]);Q.push(u)}}return null}
    function conflict(){for(let i=0;i<X.length;i++){let a=path(2*i,2*i+1);if(a!==null){let b=path(2*i+1,2*i);if(b!==null)return [...new Set([...a,...b])]}}return null}
    let bad=conflict();if(bad!==null)return {bad};if(!needLift)return {};
    let A={};for(let y of Y)A[y]=par(mask(y)&w);
    for(let i=0;i<X.length;i++){edge(2*i+1,2*i,-1);let b=0;if(conflict()!==null){G[2*i+1].pop();edge(2*i,2*i+1,-1);b=1}A[X[i]]=b^A[ref.get(X[i])]}
    check(ok(C,A),"gauge lift");return {A}
  }
  let packets=[];
  for(let w=0;w<2**E.length;w++){
    let covered=packets.some(p=>{stats.packetTests++;return p.every(([a,b])=>par(a&w)===b)});
    if(covered){stats.skipped++;if(full){let q=chart(w,false);check(!!q.bad,"learned packet sound");stats.jobs--}continue}
    let q=chart(w);
    if(q.A){stats.fullAccepted++;if(!stats.firstWitness){stats.firstWitness=q.A;stats.firstJobs=stats.jobs}if(!full)break;continue}
    let p=q.bad.flatMap(i=>[...rows[i].act,...rows[i].sign.map(([a])=>[a,par(a&w)])]);let T=[];for(let [a,b] of p){while(a){let h=31-Math.clz32(a);if(T[h]){a^=T[h][0];b^=T[h][1]}else{T[h]=[a,b];break}}if(!a)check(!b,"consistent conflict guard")}
    p=T.filter(Boolean);check(p.every(([a,b])=>par(a&w)===b),"seed covered");packets.push(p);stats.learned++;if(p.length===1)stats.rankOne++;
    // Certified closure here: rank-one forbidden packets are necessary opposite parity; all later jobs are filtered by these and all higher-rank learned packets.
  }
  return {...stats,packets,rankHistogram:packets.reduce((a,p)=>(a[p.length]=(a[p.length]||0)+1,a),{})}
 }
 const C=raw.O.map(o=>o.t.map(x=>x+1)),K=bs.common.find(x=>x.K===16).residual;
 check(JSON.stringify(raw.O)===JSON.stringify(bs.source.O),"source identity");
 function lift(A){A={...A};for(let {v:x,bucket} of K.log.slice().reverse()){let needs=new Set();for(let c of bucket){let z=c.map(l=>A[v(l)]^sg(l));if(z.every(b=>b===z[0]))needs.add(z[0]^1)}check(needs.size<=1,"reverse compatible");A[x]=needs.size?[...needs][0]:0}check(ok(C,A),"source reverse");return Object.entries(A).reduce((s,[x,b])=>s+(b?2**(+x-1):0),0)}
 let rawA=solve(C),wideA=solve(K.C);check(rawA.firstWitness&&wideA.firstWitness,"both SAT");let sourceLift=lift(wideA.firstWitness);
 let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],controls=[];
 for(let i=-1;i<21;i++){let F=fano.map(c=>c.slice());if(i>=0)F[i/3|0][i%3]*=-1;let a=solve(F,true),d=direct(F);check(!!a.firstWitness===d.sat&&d.sat===(i>=0),"Fano label");let count=0;for(let w=0;w<128;w++)if(ok(F,Object.fromEntries(Array.from({length:7},(_,j)=>[j+1,bit(w,j)]))))count++;check(count===(i<0?0:10),"Fano count");controls.push({i,rank:a.rank,jobs:a.jobs,skipped:a.skipped,learned:a.learned,sat:d.sat})}
 // randomized signed NAE, include both labels and full learned-packet replay
 let seed=2601125,rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n},random={sat:0,unsat:0,jobs:0,skipped:0,learned:0};
 for(let i=0;i<80;i++){let n=5+i%4,F=[];for(let j=0;j<6+i%12;j++){let a=new Set();while(a.size<3)a.add(1+rand(n));F.push([...a].map(x=>rand(2)?x:-x))}let a=solve(F,true),d=direct(F);check(!!a.firstWitness===d.sat,"random decision");let exact=false;for(let w=0;w<2**n;w++)if(ok(F,Object.fromEntries(Array.from({length:n},(_,j)=>[j+1,bit(w,j)])))){exact=true;break}check(exact===d.sat,"random exhaustive");random[d.sat?"sat":"unsat"]++;for(let k of ["jobs","skipped","learned"])random[k]+=a[k]}
 return {assertions,raw:{direct:direct(C),gauge:rawA},wide:{direct:direct(K.C),gauge:wideA,sourceLift},fano:controls,random}
}
if(typeof require!=='undefined' && require.main===module){const fs=require('fs');console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2));}
