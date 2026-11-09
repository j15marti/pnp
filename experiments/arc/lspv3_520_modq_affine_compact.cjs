'use strict';
// LSPV-3/520, standard Node.js. No external packages.
const yes=(b,m)=>{if(!b)throw Error(m||'assertion failure'); checks++};
let checks=0, packets=0, negatives=0, cases=0;
const canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);
const key=a=>canon(a).join(',');
const rank=a=>{const B=new Map();for(let i=1;i<a.length;i++){let x=a[i]^a[0];while(x){const k=31-Math.clz32(x);if(B.has(k))x^=B.get(k);else{B.set(k,x);break}}}return B.size};
function source(s,t){const f=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)if(((s[0]*a+s[1]*b+s[2]*c-t)%3+3)%3)f.push([-(a+1),-(b+4),-(c+7)]);for(let g=0;g<3;g++)f.push([g*3+1,g*3+2,g*3+3]);return f}
function sat(f,mask){return f.every(c=>c.some(l=>!!(mask&(1<<(Math.abs(l)-1)))===(l>0)))}
function res(P,N,p){yes(P.includes(p)&&N.includes(-p),'oriented pivot');const z=canon([...P.filter(x=>x!==p),...N.filter(x=>x!==-p)]);yes(z.every(x=>!z.includes(-x)),'tautology');return z}
function packet(s,t,g,pair,F){const other=[0,1,2].filter(x=>x!==g),[bGroup,cGroup]=other;
const ids=new Map(F.map((c,i)=>[key(c),i])),tab=F.map(canon),lines=[];
function add(pos,neg,p){const z=res(tab[pos],tab[neg],p),id=tab.length;tab.push(z);lines.push({id,pos,neg,p,clause:z});return id}
let cur=0;
for(let b=0;b<3;b++){
 let sub=18+cGroup;
 for(let c=0;c<3;c++){
  const ok=a=>{const v=[0,0,0];v[g]=a;v[bGroup]=b;v[cGroup]=c;return ((s.reduce((z,t,j)=>z+t*v[j],0)-t)%3+3)%3===0};
  const a=ok(pair[0])?pair[1]:pair[0];yes(!ok(a),'wrong source triple');const v=[0,0,0];v[g]=a;v[bGroup]=b;v[cGroup]=c;
  sub=add(sub,ids.get(key(v.map((x,j)=>-(3*j+x+1)))),3*cGroup+c+1)
 }
 if(b===0)cur=18+bGroup;
 cur=add(cur,sub,3*bGroup+b+1)
}
const target=key(pair.map(a=>-(3*g+a+1)));yes(key(tab[cur])===target,'exact AMO');yes(lines.length===12,'node count');
function replay(P){const A=P.F.map(canon);for(const t of P.lines){yes(t.id===A.length,'acyclic ids');yes(t.pos<t.id&&t.neg<t.id&&t.pos>=0&&t.neg>=0,'parent provenance');const z=res(A[t.pos],A[t.neg],t.p);yes(key(z)===key(t.clause),'conclusion');A.push(z)}yes(key(A[P.sink])===P.target,'sink');return true}
const P={F,lines,sink:cur,target};replay(P);packets++;
for(let m=0;m<3;m++){const Q=JSON.parse(JSON.stringify(P)),L=Q.lines.at(-1);if(m===0)L.p=-L.p;if(m===1)L.clause.push(9999);if(m===2)L.pos=L.id;try{replay(Q);throw Error('corrupt accepted')}catch(e){if(e.message==='corrupt accepted')throw e;negatives++}}
return P}
for(let mask=0;mask<8;mask++){const signs=[0,1,2].map(i=>mask&(1<<i)?-1:1);
for(let t=0;t<3;t++){const F=source(signs,t),models=[];yes(F.length===21,'proper3 count');
for(let v=0;v<512;v++)if(sat(F,v))models.push(v);
yes(models.length===9&&rank(models)===6,'affine rank q3');
for(let j=0;j<F.length;j++){let m=0;for(let v=0;v<512;v++)if(sat(F.filter((_,i)=>i!==j),v))m++;yes(m===(j<18?13:58),'deletion witnesses')}
for(let g=0;g<3;g++)for(let a=0;a<3;a++)for(let b=a+1;b<3;b++)packet(signs,t,g,[a,b],F);
cases++}}
let modCases=0;
for(let q=2;q<=9;q++){for(const s of [[1,1,1],[-1,1,1],[1,-1,-1]])for(const t of [0,1]){
const A=[];for(let a=0;a<q;a++)for(let b=0;b<q;b++){const c=((s[2]*(t-s[0]*a-s[1]*b))%q+q)%q;A.push((1<<a)|(1<<(q+b))|(1<<(2*q+c)))}
const predicted=3*(q-1)-(q%2===0?1:0);yes(rank(A)===predicted,'mod-q rank');modCases++}}
console.log(JSON.stringify({role:'LSPV-3/520',status:'PROVED/RESTRICTED+COMPUTATIONAL',strict3_sign_charge_cases:cases,res_amo_packets:packets,res_nodes_each:12,corruptions_rejected:negatives,modq_cases_32bit:modCases,assertion_groups:checks}));