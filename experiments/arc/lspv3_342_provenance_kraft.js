#!/usr/bin/env node
"use strict";
function check(a,msg){if(!a)throw Error(msg)}
function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}
function graph(h){let e=[];if(h===4){for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j])}
else{check(h>=6&&h%2===0,"h");let k=h/2;for(let i=0;i<k;i++)e.push([i,(i+1)%k]);for(let i=0;i<k;i++)e.push([k+i,k+(i+1)%k]);for(let i=0;i<k;i++)e.push([i,k+i])}
let inc=Array.from({length:h},()=>[]);e.forEach(([u,v],j)=>{inc[u].push(j);inc[v].push(j)});check(inc.every(x=>x.length===3),"cubic");return {h,n:e.length,edges:e,inc}}
function src(g,odd){let charge=Array(g.h).fill(0);if(odd)charge[0]=1;let F=[];
for(let v=0;v<g.h;v++)for(let z=0;z<8;z++){let b=[z&1,(z>>1)&1,(z>>2)&1];if((b[0]^b[1]^b[2])===(charge[v]^1))F.push(g.inc[v].map((e,j)=>b[j]?-(e+1):e+1))}
check(F.length===4*g.h,"sources");return {F,charge}}
function satcl(C,x){return C.some(l=>Number((x>>BigInt(Math.abs(l)-1))&1n)===(l>0?1:0))}
function solve(n,eq){let basis=Array(n).fill(null);for(let [a0,b0]of eq){let a=a0,b=b0,found=false;for(let k=n-1;k>=0;k--)if(a&(1n<<BigInt(k))){if(basis[k]){a^=basis[k][0];b^=basis[k][1]}else{basis[k]=[a,b];found=true;break}}if(!found)check(a===0n&&b===0,"inconsistent")}let x=0n;for(let k=0;k<n;k++)if(basis[k]){let [a,b]=basis[k];if(b^parity(x&(a^(1n<<BigInt(k)))))x|=1n<<BigInt(k)}for(let [a,b]of eq)check(parity(x&a)===b,"bad gaussian");return x}
function witness(g,F,charge,j){let v=Math.floor(j/4),eq=[];for(let u=0;u<g.h;u++)if(u!==v){let mask=0n;for(let e of g.inc[u])mask|=1n<<BigInt(e);eq.push([mask,charge[u]])}for(let l of F[j])eq.push([1n<<BigInt(Math.abs(l)-1),l<0?1:0]);let x=solve(g.n,eq);check(!satcl(F[j],x),"wrong deleted clause");F.forEach((c,k)=>{if(j!==k)check(satcl(c,x),"bad deletion witness "+j+" "+k)});return x.toString(16)}
function union(a,b){return [...new Set([...a,...b])].sort((x,y)=>x-y)}
function xor(a,b){let s=new Set(a);for(let x of b){if(s.has(x))s.delete(x);else s.add(x)}return [...s].sort((x,y)=>x-y)}
function clauseTab(C,vs){let tab=0;for(let a=0;a<8;a++)if(C.some(l=>{let k=vs.indexOf(Math.abs(l)-1);check(k>=0,"clause vars");return ((a>>k)&1)===(l>0?1:0)}))tab|=1<<a;return tab}
function rowTab(vs,rhs){let tab=0;for(let a=0;a<8;a++)if((((a&1)^((a>>1)&1)^((a>>2)&1)))===rhs)tab|=1<<a;return tab}
function shortest(m){let k=Math.floor(Math.log2(m));return m*k+2*(m-(2**k))}
function build(h){let g=graph(h),{F,charge}=src(g,true),even=src(g,false),m=F.length;
let nodes=F.map((clause,j)=>({kind:"source",clause,source:j}));
let S=F.map((_,j)=>[j]),tab=F.map((c,j)=>clauseTab(c,g.inc[Math.floor(j/4)])),volume=0,rows=[];
function add(p,q,obj){volume+=S[p].length+S[q].length;let id=nodes.length;nodes.push({...obj,parents:[p,q]});S.push(union(S[p],S[q]));return id}
for(let v=0;v<h;v++){let b=4*v;let x=tab[b]&tab[b+1],y=tab[b+2]&tab[b+3];let a=add(b,b+1,{kind:"factor",v,table:x});tab.push(x);let c=add(b+2,b+3,{kind:"factor",v,table:y});tab.push(y);
let out=tab[a]&tab[c];check(out===rowTab(g.inc[v],charge[v]),"parity extraction");
let r=add(a,c,{kind:"row",v,mask:g.inc[v],rhs:charge[v]});tab.push(out);rows.push(r)}
while(rows.length>1){rows.sort((x,y)=>S[x].length-S[y].length||x-y);let a=rows.shift(),b=rows.shift(),A=nodes[a],B=nodes[b];rows.push(add(a,b,{kind:"xor",mask:xor(A.mask,B.mask),rhs:A.rhs^B.rhs}))}
let root=rows[0];check(nodes[root].mask.length===0&&nodes[root].rhs===1,"not contradiction");
let q=nodes.length-m;check(q===m-1&&volume===shortest(m),"not optimal");
let deleted=F.map((_,j)=>witness(g,F,charge,j));check(even.F.every(c=>satcl(c,0n)),"even SAT");
let dimacs="p cnf "+g.n+" "+m+"\n"+F.map(c=>c.join(" ")+" 0\n").join("");
let proof={h,n:g.n,edges:g.edges,charge,clauses:F,nodes,root,deleted,evenClauses:even.F};
return {summary:{h,n:g.n,m,q,N_bits:8*dimacs.length,source_reads:volume,L_m:shortest(m),unit_W:m-1,proof_bytes:JSON.stringify(proof).length,deletions:m},proof}}
function run(){return {id:"LSPV3-PROVENANCE-KRAFT342",seed:null,status:"symbolic theorem separately; finite arithmetic exact",cases:[4,6,8,10,16,20,40].map(build)}}
if(require.main===module)process.stdout.write(JSON.stringify(run())+"\n");
module.exports={run,build,graph,src,shortest};
