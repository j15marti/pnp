const fs=require('fs');
function run(src){
 let checks=0; const eq=(a,b)=>{checks++;if(a!==b)throw Error(`${a} != ${b}`)};
 // equations on v_0,...,v_k, RHS stored as last bit.
 function rows(k,mask,s){const out=[s?1|(1<<(k+1)):0];for(let j=1;j<=k;j++){const f=((mask>>(j-1))&1);out.push((s<<j)|(f<<(j-1)));}out.push(s<<k);return out;}
 function gauss(k,mask,s){const a=rows(k,mask,s);let rank=0;for(let j=0;j<=k;j++){let p=a.findIndex((x,i)=>i>=rank&&((x>>j)&1));if(p<0)continue;[a[p],a[rank]]=[a[rank],a[p]];for(let i=rank+1;i<a.length;i++)if((a[i]>>j)&1)a[i]^=a[rank];rank++;}if(a.includes(1<<(k+1)))return 0;return 2**(k+2+k+1-rank);}
 function brute(k,mask,s){let z=0;const a=rows(k,mask,s);for(let v=0;v<2**(k+1);v++){let b=0;for(let j=0;j<a.length;j++){let t=a[j]&(v|(1<<(k+1))),p=0;while(t){p^=1;t&=t-1;}b|=p<<j;}for(let u=0;u<2**(k+2);u++){let t=b&u,p=0;while(t){p^=1;t&=t-1;}z+=p?-1:1;}}return z;}
 const cache=new Map();function table(k){if(!cache.has(k)){if(k>20)throw Error("test cap");let t=[];for(let m=0;m<2**k;m++){let g=gauss(k,m,1);eq(g,m===2**k-1?0:2**(k+2));if(k<=3){eq(g,brute(k,m,1));eq(gauss(k,m,0),brute(k,m,0));}t.push(g!==0);}cache.set(k,t);}return cache.get(k);}
 const lit=(x,l)=>((x[Math.abs(l)]||0)^(l<0?1:0));
 const nae=(C,x)=>C.every(c=>{let b=lit(x,c[0]);return c.some(l=>lit(x,l)!==b)});
 function check(C,label,log=[],source=null){const vars=[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);const clauses=C.flatMap(c=>[c,c.map(l=>-l)]);let count=0,first=null,visits=0;
 // Certified root coordinate closure: each owner has >=3 distinct vars, no pins; full complement symmetry means no absolute forced bits in a satisfiable chart.
 for(const c of C){eq(new Set(c.map(Math.abs)).size,c.length);if(c.length<3)throw Error("unexpected binary closure");}
 for(let m=0;m<2**vars.length;m++){const x={};vars.forEach((v,j)=>x[v]=(m>>j)&1);let ok=true;for(const c of clauses){let mask=0;c.forEach((l,j)=>mask|=(1^lit(x,l))<<j);visits++;if(!table(c.length)[mask]){ok=false;break;}}eq(ok,nae(C,x));if(ok){count++;if(!first)first=x;}}
 let lifted=null;if(first&&source){const x={...first};for(const {v,bucket} of [...log].reverse()){let allowed=[0,1].filter(b=>{x[v]=b;return bucket.every(c=>c.some(l=>lit(x,l)!==b));});if(!allowed.length)throw Error("lift");x[v]=allowed[0];}eq(nae(source,x),true);lifted=Object.entries(x).reduce((s,[v,b])=>s+(b?2**(Number(v)-1):0),0);}
 return {label,variables:vars.length,owners:C.length,clauseBlocks:clauses.length,primalBits:clauses.reduce((s,c)=>s+2*c.length+3,0),maxWidth:Math.max(...C.map(c=>c.length)),modes:2**vars.length,nonzeroModes:count,visitedFactors:visits,first,lifted};}
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
 let tests=[check(fano,"Fano")];eq(tests[0].nonzeroModes,0);
 for(let i=0;i<7;i++)for(let j=0;j<3;j++){let C=fano.map(c=>c.slice());C[i][j]*=-1;const t=check(C,`Fano sign ${i}:${j}`);eq(t.nonzeroModes,10);tests.push(t);}
 let k=src.common.find(x=>x.K===16).residual;let raw=src.common[0].residual.C;
 tests.push(check(k.C,"BW17 K16",k.log,raw));eq(tests.at(-1).nonzeroModes>0,true);
 // Same source lift independently check published BH19 and DS19 words.
 for(const word of [13310626,13308834,12130883]){let x={};for(let i=1;i<=24;i++)x[i]=(word>>(i-1))&1;eq(nae(raw,x),true);}
 return {checks,tests,localTables:[...cache.keys()].map(k=>({width:k,words:2**k})),guard:[],sourceRef:"ff92a1c3d44e4b48dc9a7bf215825075396cae5a"};
}
console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
