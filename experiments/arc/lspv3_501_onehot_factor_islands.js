'use strict';
// Independent graph/source and exact factor-closure audit for one-hot Tseitin.
// DISTINCT SOURCE/AND3/XOR *abstraction*, NOT a full historical R_mix341 checker.
function ok(q,msg){if(!q)throw Error(msg||'failed')}
function graph(name){let n,edges=[];
 if(name==='K4'){n=4;for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)edges.push([a,b])}
 else if(name==='K33'){n=6;for(let a=0;a<3;a++)for(let b=3;b<6;b++)edges.push([a,b])}
 else if(name==='CUBE'){n=8;for(let a=0;a<n;a++)for(let b=0;b<3;b++){let c=a^(1<<b);if(a<c)edges.push([a,c])}}
 else if(name==='PRISM16'){const k=16;n=2*k;for(let a=0;a<k;a++){edges.push([a,(a+1)%k],[a+k,(a+1)%k+k],[a,a+k])}}
 else throw Error('unknown graph');return{n,edges}}
function source(name,charge){const{n,edges}=graph(name),inc=Array.from({length:n},()=>[]),cls=[];
 edges.forEach(([a,b],e)=>{inc[a].push(e);inc[b].push(e);cls.push([2*e+1,2*e+2],[-(2*e+1),-(2*e+2)])});
 for(let v=0;v<n;v++)for(let x=0;x<8;x++){
  let p=((x&1)+((x>>1)&1)+((x>>2)&1))&1;
  if(p===charge[v])continue;
  cls.push(inc[v].map((e,j)=>-(2*e+1+((x>>j)&1))))
 }
 ok(cls.length===7*n,'source size');return{n,edges,inc,cls}}
function support(cl){return cl.map(l=>Math.abs(l)-1).sort((a,b)=>a-b)}
function tab(cl,s){let out=0;for(let i=0;i<1<<s.length;i++)if(cl.some(l=>((i>>s.indexOf(Math.abs(l)-1))&1)===(l>0?1:0)))out|=1<<i;return out}
function lift(s,t,u){let out=0;for(let x=0;x<(1<<u.length);x++){
  let y=0;for(let j=0;j<s.length;j++)y|=((x>>u.indexOf(s[j]))&1)<<j;
  if((t>>y)&1)out|=1<<x;
 }return out}
function key(s,t){return s.join(',')+':'+t}
function affine(s,t){let rows=[];for(let m=1;m<(1<<s.length);m++)for(let rhs=0;rhs<2;rhs++){
  let w=0;for(let x=0;x<(1<<s.length);x++){
   let p=0;for(let j=0;j<s.length;j++)if(m&(1<<j))p^=(x>>j)&1;
   if(p===rhs)w|=1<<x;
  }
  if(w===t){let bm=0n;for(let j=0;j<s.length;j++)if(m&(1<<j))bm|=1n<<BigInt(s[j]);rows.push(bm.toString()+':'+rhs)}
 }return rows}
function closure(cls){let fac=new Map();for(let cl of cls){let s=support(cl),t=tab(cl,s);fac.set(key(s,t),[s,t])}let turns=0;
 while(true){let extra=new Map(),a=[...fac.values()];for(let i=0;i<a.length;i++)for(let j=i;j<a.length;j++){
  let [s,t]=a[i],[r,q]=a[j],u=[...new Set([...s,...r])].sort((x,y)=>x-y);if(u.length>3)continue;
  let d=lift(s,t,u)&lift(r,q,u),k=key(u,d);if(!fac.has(k))extra.set(k,[u,d]);
 }
 if(!extra.size)break;turns++;ok(turns<=4,'unbounded closure');for(let [k,v]of extra)fac.set(k,v);
 }
 let rows=new Set();for(let[s,t]of fac.values())for(let r of affine(s,t))rows.add(r);
 return{fac,rows,turns}}
function check(name,bits){let n=graph(name).n,charge=Array.from({length:n},(_,i)=>(bits.includes(i)?1:0)),s=source(name,charge),v=closure(s.cls);
 ok(v.turns===1,'extra closure iterations');ok(v.fac.size===s.cls.length+s.edges.length,'factor count');
 let expected=new Set(s.edges.map((_,e)=>((3n<<(BigInt(e)*2n)).toString()+':1')));
 ok(expected.size===v.rows.size,'affine count');for(let r of v.rows)ok(expected.has(r),'unexpected affine seed '+r);
 let modelCount=null;if(name==='K4'){modelCount=0;for(let a=0;a<1<<(2*s.edges.length);a++){
  if(s.cls.every(cl=>cl.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0))))modelCount++;
 }ok(modelCount===(bits.length%2?0:8),'source model count')}
 return{name,h:s.n,edges:s.edges.length,source_clauses:s.cls.length,exact_factors:v.fac.size,affine_rows:v.rows.size,source_models:modelCount,charge:bits}}
function main(){let cases=[];for(let i=0;i<16;i++)cases.push(check('K4',[0,1,2,3].filter(j=>(i>>j)&1)));
 for(let name of ['K33','CUBE','PRISM16'])for(let bits of [[0],[0,1,2],[],[0,1]])cases.push(check(name,bits));
 const s=source('K4',[1,0,0,0]);let e=s.cls[0],ep=s.cls[1],vc=s.cls[2*s.edges.length];
 ok(new Set([...support(e),...support(vc)]).size===4,'illegal source support union not caught');
 ok(affine(support(e),tab(e,support(e))).length===0,'single edge clause falsely affine');
 let t=tab(e,support(e))&tab(ep,support(ep));ok(affine(support(e),t).length===1,'missing edge parity');
 let vmask=s.inc[0].reduce((m,e)=>m|(1n<<BigInt(2*e)),0n).toString();
 ok(!closure(s.cls).rows.has(vmask+':1'),'forged vertex parity accepted');
 let sum=0n;for(let e=0;e<s.edges.length;e++)sum^=3n<<(BigInt(e)*2n);ok(sum!==0n,'incorrect XOR contradiction');
 let corrupt=s.cls.slice();corrupt[1]=[s.cls[1][0],-s.cls[1][1]];ok(JSON.stringify(corrupt)!==JSON.stringify(s.cls),'source corruption undetected');
 const negative=['illegal vertex-edge AND3','edge clause false affine','absent vertex-row','false XOR contradiction','mismatched source clause'];
 return{status:'PASS',cases:cases.length,negatives:negative.length,negative_controls:negative,trace:cases,model:'generic sticky-support SOURCE/AND3/exact alias/XOR only; historical grammar not authenticated'}}
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(main(),null,2));
