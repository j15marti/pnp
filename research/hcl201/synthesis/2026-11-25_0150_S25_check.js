'use strict';
function run(bw){
 const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n},bits=x=>{const a=[];for(let i=0;x;i++,x>>>=1)if(x&1)a.push(i);return a},word=(w,t)=>t.reduce((s,v,i)=>s+((w>>>v)&1)*2**i,0),assert=(a,m)=>{if(!a)throw Error(m)};
 const masks=(n,k)=>{const a=[0];function go(m,i,d){if(!d)return;for(let j=i;j<n;j++){let t=m|(1<<j);a.push(t);go(t,j+1,d-1)}}go(0,0,k);return a.sort((a,b)=>pop(a)-pop(b)||a-b)};
 const subwords=m=>{const a=[];for(let s=m;;s=(s-1)&m){a.push(s);if(!s)break}return a};
 const edges=O=>O.map(o=>({...o,m:o.t.reduce((s,v)=>s|(1<<v),0)}));
 const legal=(w,O)=>O.every(o=>!o.bad.includes(word(w,o.t)));
 function closure(s,O){let c=s;while(true){let old=c;for(const o of O)if(pop(c&o.m)>=2)c|=o.m;if(old===c)return c}}
 function forest(c,O){const p=new Map();function root(v){if(!p.has(v))p.set(v,v);while(p.get(v)!==v)v=p.get(v);return v}for(const o of O)if((o.m&c)===o.m){const v=o.t.map(root);if(new Set(v).size!==3)return false;p.set(v[1],v[0]);p.set(v[2],v[0])}return true}
 function forestCheck(n,raw,k){const O=edges(raw),M=masks(n,k),P=new Map();let words=0,extensions=0,localWords=0,pairWords=0,peak=0;for(const s of M){const c=closure(s,O);assert(pop(c)<=Math.max(0,2*pop(s)-1),"closure cap");assert(forest(c,O),"forest");peak=Math.max(peak,pop(c));const local=O.filter(o=>(o.m&c)===o.m),p=new Set();for(const w of subwords(c)){words++;if(legal(w,local))p.add(w&s)}assert(p.size,"nonempty");P.set(s,p);localWords+=p.size}
 for(const t of M)for(const v of bits(t)){const s=t^(1<<v),p=P.get(s),q=P.get(t);const project=new Set([...q].map(w=>w&s));assert(project.size===p.size&&[...p].every(w=>project.has(w)),"extension");extensions++}
 if(k>=6)for(let i=0;i<O.length;i++)for(let j=i;j<O.length;j++){const s=O[i].m|O[j].m;for(const w of subwords(s))if(legal(w,[O[i],O[j]])){assert(P.get(s).has(w),"owner pair");pairWords++}}
 return {n,k,scopes:M.length,words,extensions,localWords,pairWords,peak}}
 function consistency(n,raw,k,witness){const O=edges(raw),M=masks(n,k),D=new Map();let scans=0,removed=0,initial=0;for(const s of M){const e=O.filter(o=>(o.m&s)===o.m),p=new Set(subwords(s).filter(w=>legal(w,e)));D.set(s,p);initial+=p.size}let sweeps=0;while(true){let changed=0;sweeps++;for(const t of M)for(const v of bits(t)){const s=t^(1<<v),p=D.get(s),q=D.get(t);for(const w of q){scans++;if(!p.has(w&s)){q.delete(w);changed++}}const pro=new Set([...q].map(w=>w&s));for(const w of p){scans++;if(!pro.has(w)){p.delete(w);changed++}}}removed+=changed;if(!changed||!D.get(0).size)break}if(witness!==undefined){assert(legal(witness,O),"source witness");assert(M.every(s=>D.get(s).has(witness&s)),"witness preserved")}return{n,k,scopes:M.length,initial,removed,sweeps,scans,rejected:!D.get(0).size}}
 const loose=(m,signed)=>Array.from({length:m},(_,i)=>{const a=signed?(i*5+3)%8:0;return{t:[i,(i+1)%m,m+i],bad:[a,a^7]}});
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,bad:[0,7]}));
 const neighbor=fano.map((o,i)=>i?o:{...o,bad:[1,6]});
 const fanoCounts=[fano,neighbor].map(O=>subwords(127).filter(w=>legal(w,O)).length);assert(fanoCounts[0]===0&&fanoCounts[1]>0,"opposite labels");
 const forestResults=[forestCheck(14,loose(7,false),6),forestCheck(14,loose(7,true),6),forestCheck(16,loose(8,true),4),forestCheck(18,loose(9,false),4)];
 const controls=[];for(const [id,O] of [["Fano",fano],["Fano-sign",neighbor]])for(const k of [3,4,7])controls.push({id,...consistency(7,O,k)});
 const bwResults=[3,4].map(k=>consistency(bw.n,bw.O,k,13310626));assert(legal(13308834,bw.O),"DS19 witness");
 return {fanoCounts,forestResults,controls,bwResults,sourceRef:"9164cb11c6fcdf96d470de9d86b061e3201a591f",sourceWitnesses:[13310626,13308834],guard:[]}
}
const fs=require('fs');
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
