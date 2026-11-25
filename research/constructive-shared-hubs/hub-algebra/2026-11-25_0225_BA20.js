function run(data,source){
 const results={}; let checks=0; function assert(b,m){checks++;if(!b)throw Error(m);}
 function solve(n,packets,guard=[],cap=4096,merge=true){
  const R=1<<n, MASK=R-1, st={add:0,split:0,merges:0,peak:1,rawPeak:1,hullScans:0,closureScans:0,deductions:0,steps:0};
  const pivot=x=>(x&MASK)&-(x&MASK);
  function add(A,e){st.add++;for(const a of A)if(e&pivot(a))e^=a;if(!(e&MASK))return e&R?null:A;let p=pivot(e);return [...A.map(a=>a&p?a^e:a),e].sort((a,b)=>pivot(a)-pivot(b));}
  function combine(A,B){for(let e of B){A=add(A,e);if(!A)return null;}return A;}
  function subtract(A,B){let C=A,parts=[];for(const e of B){let D=add(C,e);if(D===null)return [A];if(D===C)continue;parts.push(add(C,e^R));C=D;}st.split+=parts.length;return parts;}
  function mergeAll(L){if(!merge)return L;for(;;){let groups=new Map(),next=[],changed=false;for(let A of L){let key=A.map(x=>x&MASK).join(',');let B=groups.get(key);if(!B){groups.set(key,A);continue;}groups.delete(key);let i=A.findIndex((v,j)=>v!==B[j]);if(i<0)throw Error('overlap');let C=[];for(let j=0;j<A.length;j++)if(j!==i)C=add(C,A[j]===B[j]?A[j]:A[j]^A[i]);next.push(C);st.merges++;changed=true;}next.push(...groups.values());L=next;if(!changed)return L;}}
  function point(A){return A.reduce((x,e)=>x|(e&R?pivot(e):0),0);}
  function nullbasis(A){let piv=A.reduce((x,e)=>x|pivot(e),0),out=[];for(let j=0;j<n;j++){let p=1<<j;if(piv&p)continue;let v=p;for(let e of A)if(e&p)v|=pivot(e);out.push(v);}return out;}
  function parity(x){x^=x>>>16;x^=x>>>8;x^=x>>>4;return (0x6996>>>(x&15))&1;}
  function hull(L){let span=[],a=point(L[0]);for(let A of L){st.hullScans++;span=add(span,point(A)^a);for(let v of nullbasis(A)){span=add(span,v);if(span.length===n)return [];}if(span.length===n)return [];}let H=[];for(let v of nullbasis(span))H=add(H,v|(parity(v&a)?R:0));return H;}
  function close(H){for(;;){let old=H.length;for(let P of packets){st.closureScans++;let C=H,last=null;for(let e of P){let D=add(C,e);if(D===null){C=null;break;}if(D!==C)last=e;C=D;}if(C===null)continue;if(C.length===H.length)return null;if(C.length===H.length+1){H=add(H,last^R);if(!H)return null;st.deductions++;}}if(old===H.length)return H;}}
  let H=combine([],guard);if(H)H=close(H);if(!H)return {status:'UNSAT',count:0,st,cover:[]};
  let L=[H];
  for(let P of packets){let next=[];for(let A of L)next.push(...subtract(A,P));st.rawPeak=Math.max(st.rawPeak,next.length);L=mergeAll(next);st.steps++;st.peak=Math.max(st.peak,L.length);
   if(!L.length)return {status:'UNSAT',count:0,st,cover:[]};
   if(L.length>cap){let HH=close(H);return {status:HH?'OPEN':'UNSAT',count:HH?null:0,st,cover:[]};}
   let G=hull(L);if(G.length>H.length){let old=H.length;H=close(G);if(!H)return {status:'UNSAT',count:0,st,cover:[]};st.deductions+=G.length-old;L=L.map(A=>combine(A,H)).filter(Boolean);if(!L.length)return {status:'UNSAT',count:0,st,cover:[]};L=mergeAll(L);}
  }
  return {status:'SAT',count:L.reduce((s,A)=>s+2**(n-A.length),0),st,cover:L,witness:point(L[0]),hull:hull(L)};
 }
 function compile(C,ids){let n=ids.length,R=1<<n,index=new Map(ids.map((x,i)=>[x,i]));return C.map(c=>c.slice(1).map(l=>(1<<index.get(Math.abs(l)))^(1<<index.get(Math.abs(c[0])))^((l<0)!==(c[0]<0)?R:0)));}
 function accepted(n,P,x,G=[]){let R=1<<n;function sat(e){let z=e&x,p=0;while(z){p^=1;z&=z-1;}return p===+(!!(e&R));}return G.every(sat)&&P.every(p=>!p.every(sat));}
 function control(C,ids,G=[],cap=4096){let n=ids.length,P=compile(C,ids),a=solve(n,P,G,cap,true),b=solve(n,P,G,cap,false);let ref=0;for(let x=0;x<2**n;x++){let yes=accepted(n,P,x,G);ref+=+yes;for(let z of [a,b])if(z.status!=='OPEN'){let c=z.cover.reduce((s,A)=>s+ +(accepted(n,[],x,A)),0);assert(c===+yes,'support mismatch');}}for(let z of [a,b])if(z.status!=='OPEN')assert(z.count===ref,'count');return {ref,a:{status:a.status,count:a.count,st:a.st,pieces:a.cover.length},b:{status:b.status,count:b.count,st:b.st,pieces:b.cover.length}};}
 const F=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]], ids=[1,2,3,4,5,6,7];
 results.fano=[control(F,ids)];for(let i=0;i<7;i++)for(let j=0;j<3;j++){let C=F.map(a=>a.slice());C[i][j]*=-1;results.fano.push(control(C,ids));}
 let seed=98123;function rng(m){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%m;}
 results.random=[];for(let t=0;t<40;t++){let n=4+rng(4),C=[];for(let j=0;j<4+rng(8);j++){let s=new Set;while(s.size<3)s.add(1+rng(n));C.push([...s].map(x=>rng(2)?x:-x));}let G=t%2?[3|((t%4===1)?1<<n:0)]:[];results.random.push(control(C,Array.from({length:n},(_,i)=>i+1),G));}
 results.guarded=[]; for(let i=0;i<7;i++){let C=F.map(a=>a.slice());C[i][0]*=-1;for(let b=0;b<2;b++)results.guarded.push(control(C,ids,[1|(b?128:0),6|128]));}
 results.guarded.push(control(F,ids,[1,129]));
 results.stars=[];for(let k=1;k<=5;k++){let C=Array.from({length:k},(_,i)=>[1,2*i+2,2*i+3]),v=control(C,Array.from({length:2*k+1},(_,i)=>i+1));assert(v.ref===2*3**k,'star count');assert(v.a.pieces>=Math.ceil((3/2)**k),'cover bound');results.stars.push(v);}
 const orig=source.O.map(o=>o.t.map(x=>x+1)),r=data.common.find(x=>x.K===16).residual;
 const idsK=[...new Set(r.C.flat().map(Math.abs))].sort((a,b)=>a-b);
 results.k16=control(r.C,idsK,[],4096);
 const pK=compile(r.C,idsK),w=solve(idsK.length,pK,[],4096,true);let word=0;
 for(let i=0;i<idsK.length;i++)if(w.witness&(1<<i))word|=1<<(idsK[i]-1);
 function value(l,x){return ((x>>>(Math.abs(l)-1))&1)^+(l<0);}
 function ok(c,x){return c.some(l=>value(l,x)!==value(c[0],x));}
 for(let l of r.log.slice().reverse()){let a=word&~(1<<(l.v-1)),b=a|(1<<(l.v-1));let can=x=>l.bucket.every(t=>ok([l.v,...t],x));assert(can(a)||can(b),'lift');word=can(a)?a:b;}
 assert(orig.every(c=>ok(c,word)),'source witness');results.k16.lifted=word;results.k16.ids=idsK;results.k16.hullRank=w.hull?.length;
 let p=compile(orig,Array.from({length:24},(_,i)=>i+1));for(let merge of [false,true]){let z=solve(24,p,[],1024,merge);results[merge?'rawMerged':'rawPlain']={status:z.status,count:z.count,st:z.st,pieces:z.cover.length,witness:z.witness};if(z.status==='SAT')assert(accepted(24,p,z.witness),'raw witness');}
 results.checks=checks;return results;
}
const fs=require('fs'); console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
