// TMR-2/073 exact T5 pp-disequality verifier. Node 22, no dependencies.
// Full mathematical proofs are in the TMR-2/073 report. Finite tests COMPUTATIONAL.
'use strict';
const seed=2026111718; let checks=0;
const ck=(p,msg)=>{checks++; if(!p) throw Error('check '+checks+': '+msg)};
const R=(a,b)=>[1,3].includes((b-a+5)%5);
const W=Array.from({length:5},(_,x)=>Array.from({length:5},(_,y)=>{
 let count=0;
 for(let s=0;s<5;s++)for(let t=0;t<5;t++)for(let u=0;u<5;u++)for(let v=0;v<5;v++)
 if(R(x,s)&&R(t,s)&&R(t,u)&&R(u,y)&&R(y,v)&&R(v,t))count++;
 return count;
}));
for(let x=0;x<5;x++)for(let y=0;y<5;y++) {
 const d=(y-x+5)%5;ck(W[x][y]===(d===0?0:[1,4].includes(d)?6:2),'gadget');
}
const subsets=[...Array(32).keys()];
const domainMasks=subsets.map(m=>[m,
  [...Array(5).keys()].reduce((acc,y)=>acc|(subsets.some(x=>x<5&&(m>>x&1)&&R(x,y))?1<<y:0),0),
  [...Array(5).keys()].reduce((acc,y)=>acc|([...Array(5).keys()].some(x=>(m>>x&1)&&R(y,x))?1<<y:0),0)]);
ck(domainMasks.length===32,'all masks');
const S=[1,3],diffSet=(s)=>[...new Set(s)].sort((a,b)=>a-b);
const A=diffSet(S.flatMap(i=>S.map(j=>(i-j+5)%5)));
const F=diffSet(S.flatMap(i=>S.map(j=>(i+j)%5)));
const G=diffSet(S.flatMap(i=>S.map(j=>(-i-j+10)%5)));
const B=F.filter(d=>G.includes(d)),D=diffSet(A.flatMap(a=>B.map(b=>(a+b)%5)));
ck(JSON.stringify([A,B,D])===JSON.stringify([[0,2,3],[1,4],[1,2,3,4]]),'pp closure');
// Endomorphisms, exhaustive over 5^5 functions.
let endos=0;
for(let z=0;z<3125;z++) {
 let v=z,f=Array(5);for(let i=0;i<5;i++){f[i]=v%5;v=Math.floor(v/5)}
 if(f.every((a,i)=>f.every((b,j)=>!R(i,j)||R(a,b)))) {
   endos++;ck(f.every((x,i)=>x===(i+f[0])%5),'endomorphism rotation');
 }
}
ck(endos===5,'five endomorphisms');
// Explicit original-graph source with declared vertices, sorted unique arcs.
const enc=(n,E)=>'p t5 '+n+' '+E.length+'\n'+Array.from({length:n},(_,i)=>'v '+i+'\n').join('')+E.map(([u,v])=>'a '+u+' '+v+'\n').join('');
const parse=s=>{let lines=s.split('\n');if(lines.pop()!==''||lines.some(l=>l.includes('\r')))throw Error('newline');
 let h=/^p t5 (0|[1-9][0-9]*) (0|[1-9][0-9]*)$/.exec(lines[0]||'');if(!h)throw Error('header');
 let n=+h[1],m=+h[2];if(n>s.length||m>s.length||lines.length!==1+n+m)throw Error('length');
 for(let i=0;i<n;i++)if(lines[1+i]!=='v '+i)throw Error('vertex');let E=[];
 for(let i=0;i<m;i++){let z=/^a (0|[1-9][0-9]*) (0|[1-9][0-9]*)$/.exec(lines[1+n+i]||'');
 if(!z)throw Error('arc');let a=+z[1],b=+z[2];if(a>=n||b>=n)throw Error('index');E.push([a,b])}
 for(let i=1;i<E.length;i++)if(E[i][0]<E[i-1][0]||(E[i][0]===E[i-1][0]&&E[i][1]<=E[i-1][1]))throw Error('sort/duplicate');
 if(enc(n,E)!==s)throw Error('canonical');return [n,E];};
const lift=(n,E)=>{let arcs=[];E.forEach(([x,y],j)=>{let s=n+4*j,t=s+1,u=s+2,v=s+3;
 arcs.push([x,s],[t,s],[t,u],[u,y],[y,v],[v,t]);});
 arcs.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);return [n+4*E.length,arcs];};
const weighted=(n,E)=>{let total=0,proper=0,N=5**n;
 for(let z=0;z<N;z++){let v=z,c=Array(n);for(let i=0;i<n;i++){c[i]=v%5;v=Math.floor(v/5)}
 let w=1;for(const [a,b] of E)w*=W[c[a]][c[b]];
 total+=w;proper+=w>0?1:0;}return [total,proper]};
let graphs=0;
for(let n=1;n<=4;n++){let pairs=[];for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)pairs.push([a,b]);
 for(let m=0;m<2**pairs.length;m++){let E=pairs.filter((p,i)=>m>>i&1);
 let [N,arcs]=lift(n,E);ck(JSON.stringify(parse(enc(N,arcs)))===JSON.stringify([N,arcs]),'canonical');
 let [sum,proper]=weighted(n,E);ck(proper===Array.from({length:5**n},(_,z)=>{
 let c=Array(n),v=z;for(let i=0;i<n;i++){c[i]=v%5;v=Math.floor(v/5)}
 return E.every(([a,b])=>c[a]!==c[b])?1:0}).reduce((a,b)=>a+b,0),'coloring');
 graphs++;}}
const K6=[];for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)K6.push([a,b]);
ck(weighted(6,K6)[1]===0,'K6 UNSAT');
// Independently brute the entire 6-vertex one-edge T5 graph.
const [N1,E1]=lift(2,[[0,1]]);let brute=0;
for(let z=0;z<5**N1;z++){let t=z,c=Array(N1);for(let i=0;i<N1;i++){c[i]=t%5;t=Math.floor(t/5)}
 if(E1.every(([a,b])=>R(c[a],c[b])))brute++}
ck(brute===weighted(2,[[0,1]])[0]&&brute===80,'full gadget count');
// Arithmetic of K5 categorical powers and sharp Hoffman ratio bound.
for(let k=1;k<=8;k++){let n=5**k,d=4**k,t=-(4**(k-1));ck(n*(-t)/(d-t)===5**(k-1),'Hoffman');}
let bad=0;for(const s of [enc(N1,E1).slice(0,-1),enc(N1,E1)+'a 0 1\n',enc(N1,E1).replace('v 1\n','v 01\n')]){
 try{parse(s)}catch(e){bad++}}
ck(bad===3,'reject malformed');
console.log(JSON.stringify({revision:'tmr2-t5-ppneq073-js.v1',seed,checks,failures:0,
  witnessMatrix:W,ppDifferenceSets:{A,B,D},domainMasks,endomorphisms:endos,
  graphsUpToFourVertices:graphs,K6Satisfiable:false,fullSourceBruteOneEdge:brute,
  note:'Executed finite controls only; mathematical all-arity clone and reductions require independent review.'},null,2));
