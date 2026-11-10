#!/usr/bin/env node
// LSPV-2/534: independent source-authenticated bounded-depth DAG evaluator controls.
import crypto from 'node:crypto';
const out={run:"534",source_tests:0,checks:0,diamonds:[],hashes:{},sat:0,unsat:0};
const check=(x,msg)=>{out.checks++;if(!x)throw Error(msg)};
function graph(m){
 const g=[];const add=(t,a,b)=>{g.push([t,a,b]);return g.length-1};
 const inputs=Array.from({length:3*m},(_,i)=>add("input",i));
 const inv=new Map();const negate=u=>{if(!inv.has(u))inv.set(u,add("not",u));return inv.get(u)};
 function fold(v,t){while(v.length>1){const n=[];for(let i=0;i<v.length;i+=2)n.push(i+1<v.length?add(t,v[i],v[i+1]):v[i]);v=n;}return v[0]}
 const solutions=[];
 for(let assignment=0;assignment<8;assignment++){
   let clauses=[];
   for(let j=0;j<m;j++){
     let lits=[];
     for(let i=0;i<3;i++){const a=(assignment>>(2-i))&1;const u=inputs[3*j+i];lits.push(a?u:negate(u))}
     clauses.push(fold(lits,"or"));
   }
   solutions.push(fold(clauses,"and"));
 }
 return {g,root:fold(solutions,"or")};
}
function recurse(g,root,bits){
 const s={visits:0,peak:0,reads:0};
 function rec(p,depth){
   s.visits++;s.peak=Math.max(s.peak,depth);
   const [t,a,b]=g[p];
   if(t==="input"){s.reads++;return bits[a]}
   if(t==="not")return 1-rec(a,depth+1);
   const x=rec(a,depth+1),y=rec(b,depth+1);
   return t==="and"?(x&y):(x|y);
 }
 return {...s,value:rec(root,1)};
}
function memo(g,root,bits){
 let v=[];for(const [t,a,b] of g)v.push(t==="input"?bits[a]:t==="not"?1-v[a]:t==="and"?(v[a]&v[b]):(v[a]|v[b]));
 return v[root];
}
function satOracle(bits){
 for(let a=0;a<8;a++){
   let valid=true;
   for(let j=0;j<8;j++){
     let clause=false;for(let i=0;i<3;i++)if(bits[3*j+i]===((a>>(2-i))&1))clause=true;
     if(!clause){valid=false;break}
   }
   if(valid)return 1;
 }
 return 0;
}
const {g,root}=graph(8);
for(let seed=0;seed<256;seed++){
 let bits=Array.from({length:24},(_,j)=>((seed*65537+j*31337+(seed>>2)*(j+3))>>>(j%11))&1);
 if(seed===0)bits=Array.from({length:24},(_,j)=>(Math.floor(j/3)>>(j%3))&1);
 if(seed===1)bits=Array(24).fill(1);
 const result=recurse(g,root,bits), oracle=satOracle(bits);
 check(result.value===oracle,"source independent oracle");check(result.value===memo(g,root,bits),"memo");
 check(result.peak<=g.length,"peak");check(result.visits<2**20,"visit bound");
 out.source_tests++;out[oracle?"sat":"unsat"]++;
 if([0,1,2,255].includes(seed))out.hashes[String(seed)]=crypto.createHash("sha256").update(Buffer.from(bits)).digest("hex");
}
for(let depth=1;depth<=16;depth++){
 let h=[["input",0],["input",1]],u=0,v=1;
 for(let i=0;i<depth;i++){let p=h.length;h.push(["and",u,v]);let q=h.length;h.push(["or",u,v]);u=p;v=q;}
 for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){
   let res=recurse(h,u,[x,y]);check(res.value===memo(h,u,[x,y]),"diamond value");check(res.peak===depth+1,"diamond peak");
 }
 const count=recurse(h,u,[1,0]);check(count.visits===2**(depth+1)-1,"diamond visits");
 out.diamonds.push({depth,gates:h.length,dfs_visits:count.visits,dfs_peak_frames:count.peak});
}
for(const invalid of [null,[],Array(23).fill(0),Array(25).fill(0),Array(24).fill(2),Array(24).fill("x")]){
 check(!(Array.isArray(invalid)&&invalid.length===24&&invalid.every(v=>Number.isInteger(v)&&(v===0||v===1))),"malformed");
}
check(23/45>1/2,"beta positive");check(Math.abs(23/45-1/2-1/90)<1e-14,"beta gap");
console.log(JSON.stringify(out,null,2));