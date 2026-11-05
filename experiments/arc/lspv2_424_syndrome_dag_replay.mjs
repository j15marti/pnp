"use strict";
function yes(v,m){if(!v)throw Error(m)}
const fix={
K4:[4,[[0,5],"matching"],[[0,1,3],"cycle"]],
cube:[8,[[0,5,8,11],"matching"],[[0,1,3,5],"cycle"],[[2,4,6,7],"cut"]],
Petersen:[10,[[0,2,9,10,11],"matching"],[[0,1,2,3,4],"cycle"]],
Heawood:[14,[[0,4,7,9,13,17,18],"matching"],[[0,1,3,4,9,10],"cycle"]]
};
function graph(n){let e=[];
if(n==="K4")for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)e.push([a,b]);
if(n==="cube")for(let a=0;a<8;a++)for(let j=0;j<3;j++){let b=a^(1<<j);if(a<b)e.push([a,b]);}
if(n==="Petersen"){for(let a=0;a<5;a++)e.push([a,(a+1)%5]);for(let a=0;a<5;a++)e.push([a,a+5]);for(let a=0;a<5;a++)e.push([5+a,5+(a+2)%5]);}
if(n==="Heawood")[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].forEach((L,j)=>L.forEach(a=>e.push([a,7+j])));
return e;}
function comps(H,E){let adj=Array.from({length:H},()=>[]),seen=new Set(),out=[];
for(let [a,b]of E){adj[a].push(b);adj[b].push(a)}
for(let v=0;v<H;v++)if(!seen.has(v)){let st=[v],C=[];seen.add(v);while(st.length){let w=st.pop();C.push(w);for(let z of adj[w])if(!seen.has(z)){seen.add(z);st.push(z)}}out.push(C)}
return out;}
function source(H,E,chi){let inc=Array.from({length:H},()=>[]);E.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i)});
let C=[];for(let v=0;v<H;v++){yes(inc[v].length===3,"not cubic");for(let b=0;b<8;b++)if((((b>>0)&1)^((b>>1)&1)^((b>>2)&1))!==chi[v])C.push(inc[v].map((e,i)=>(b>>i)&1?-(e+1):e+1));}
yes(C.length===4*H,"source length");return C;}
function quotient(H,E,S,a,chi){let K=new Set(S),out=chi.slice(),inc=Array.from({length:H},()=>[]);
S.forEach((e,j)=>{if((a>>j)&1){let [v,w]=E[e];out[v]^=1;out[w]^=1}});
E.forEach(([v,w],i)=>{if(!K.has(i)){inc[v].push(i);inc[w].push(i)}});
let C=[];for(let v=0;v<H;v++)for(let b=0;b<(1<<inc[v].length);b++){let p=0;for(let i=0;i<inc[v].length;i++)p^=(b>>i)&1;if(p!==out[v])C.push(inc[v].map((e,i)=>(b>>i)&1?-(e+1):e+1))}
return {out,C};}
function cofactor(C,S,a){let map=new Map(S.map((e,i)=>[e+1,(a>>i)&1]));let out=[];
for(let c of C){let d=[],sat=false;for(let x of c){let b=map.get(Math.abs(x));if(b===undefined)d.push(x);else if(b===(x>0?1:0)){sat=true;break}}if(!sat)out.push(d);}
return out;}
function key(C){return [...new Set(C.map(c=>c.join(",")))].sort().join("|")}
let records=[],assertions=0;
for(let [name,[H,...specs]]of Object.entries(fix)){let E=graph(name);
yes(E.length===3*H/2,"incorrect graph");
for(let [S,kind]of specs){let k=S.length,r=H-comps(H,S.map(i=>E[i])).length,remaining=comps(H,E.filter((_,i)=>!S.includes(i))),c=remaining.length;
for(let parity of [0,1]){let chi=Array(H).fill(0);chi[0]=parity;let C=source(H,E,chi),seen=new Set(),synd=new Set(),sat=0;
for(let a=0;a<2**k;a++){let q=quotient(H,E,S,a,chi);
yes(key(cofactor(C,S,a))===key(q.C),"cofactor not parity");
assertions++;seen.add(key(q.C));synd.add(q.out.join(""));
let compbits=remaining.map(V=>V.reduce((b,v)=>b^q.out[v],0));
if(compbits.every(z=>z===0))sat++;
}
yes(synd.size===2**r,"syndrome-rank");assertions++;
yes(sat===(parity?0:2**(k-c+1)),"component parity join");assertions++;
if(kind==="matching"){yes(seen.size===2**k,"matching syntactic cache");assertions++;}
records.push({graph:name,kind,charge:parity,k,rank:r,residual_components:c,distinct_syndromes:synd.size,distinct_flattened_cofactors:seen.size,SAT_branches:sat,branches:2**k});
}}}
let cube=records.find(r=>r.graph==="cube"&&r.kind==="cut"&&r.charge===0);
yes(cube.SAT_branches===8&&cube.distinct_flattened_cofactors===16,"cube falsifier");assertions++;
console.log(JSON.stringify({run:"LSPV-2/424",status:"restricted computational control only",cases:records.length,assertions,records},null,2));