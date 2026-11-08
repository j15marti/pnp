'use strict';
// Self-contained independent K3,3/Q3 brute-force SAT witness verification.
// Native FLMV simulator: NO. Historical mixed calculus checker: NO.
import crypto from 'node:crypto';
const expected={K33:'5dc81af61477fdf2e4f9e3c72135ce0489dea80c6873868f6d0bd6d9ef882ef8',Q3:'80b0e7b161e48d81f4b477770a162130f325a87b95fbe739864d7046b2f3a7a1'};
const graphs=[['K33',6,Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3])],['Q3',8,Array.from({length:8},(_,i)=>Array.from({length:3},(_,k)=>[i,i^(1<<k)]).filter(e=>e[0]<e[1])).flat().sort((a,b)=>a[0]-b[0]||a[1]-b[1])]];
let checks=0;function ok(x,msg='failed'){if(!x)throw Error(msg);checks++}
function build(H,E){let adj=Array.from({length:H},()=>[]);for(const [u,v] of E){adj[u].push(v);adj[v].push(u)}let color=Array(H).fill(-1);
 for(let u=0;u<H;u++)if(color[u]<0){color[u]=0;let q=[u];for(let z=0;z<q.length;z++)for(let v of adj[q[z]]){if(color[v]<0){color[v]=1-color[q[z]];q.push(v)}else ok(color[v]!==color[q[z]])}}
 let L=Array.from({length:H},(_,i)=>i).filter(i=>color[i]===0),R=Array.from({length:H},(_,i)=>i).filter(i=>color[i]===1);
 let matching=[],used=new Set();function choose(i){if(i===L.length)return true;for(let v of adj[L[i]])if(!used.has(v)){matching.push([Math.min(L[i],v),Math.max(L[i],v)]);used.add(v);if(choose(i+1))return true;matching.pop();used.delete(v)}return false}ok(choose(0));
 let key=e=>e.join(','), mi=new Map(matching.map((e,i)=>[key(e),i])),inc=Array.from({length:H},()=>[]),num=H+1;
 for(const e of E){let j=mi.get(key(e)),id=j===undefined?num++:2*j+1;inc[e[0]].push(id);inc[e[1]].push(id)}ok(num===2*H+1);
 let C=[];for(const v of [...L,...R]){let id=inc[v].sort((a,b)=>a-b);for(let a=0;a<8;a++)if((((a>>2)&1)^((a>>1)&1)^(a&1))!==Number(v===0))C.push(id.map((x,k)=>(a>>(2-k))&1?-x:x))}
 let W=Math.ceil(Math.log2(2*H+1)),bits='11100011'+'1'.repeat(H)+'0'+'1'.repeat(2*H)+'0';for(const c of C)for(const l of c)bits+=(l<0?'1':'0')+Math.abs(l).toString(2).padStart(W,'0');bits+='10';
 return {C,bits};}
function satisfiable(C){let ids=[...new Set(C.flat().map(Math.abs))], ix=new Map(ids.map((v,i)=>[v,i]));for(let a=0;a<2**ids.length;a++){let good=C.every(c=>c.some(l=>Boolean((a>>ix.get(Math.abs(l)))&1)===(l>0)));if(good)return true}return false}
let cases=[];for(const [name,H,edges] of graphs){const {C,bits}=build(H,edges);ok(crypto.createHash('sha256').update(bits).digest('hex')===expected[name],'original source hash');ok(!satisfiable(C),'odd charge must be UNSAT');let sat=0;
 for(let j=0;j<C.length;j++)for(let k=0;k<3;k++){let copy=C.map(c=>c.slice());copy[j][k]=-copy[j][k];ok(satisfiable(copy),'every single original sign flip must be SAT');ok(new Set(copy.map(c=>c.join(','))).size===C.length,'proper distinct');sat++}cases.push({name,H,source_bits:bits.length,mutant_sat:sat})}
console.log(JSON.stringify({label:'LSPV4_499_STANDALONE_BRUTE',checks,cases,native_FLMV:false,historical_Rmix341:false},null,2));
