#!/usr/bin/env node
// Independent strict 3-CNF bit-PHP verifier. Reconstructs source without Python imports.
// Run Python generator with --out experiments/arc, then run this Node file.
"use strict";
const fs=require("fs"),crypto=require("crypto"),path=require("path");
let checks=0;
function claim(ok,msg){checks++;if(!ok)throw Error(msg||"bad check")}
function parseDIMACS(t){
 const lines=t.split(/\r?\n/);let n=null,m=null,clauses=[];
 for(const line of lines){let s=line.trim();if(!s||s.startsWith("c"))continue;
   if(s.startsWith("p ")){
     if(n!==null)throw Error("duplicate header");
     let x=/^p cnf (\d+) (\d+)$/.exec(s);if(!x)throw Error("malformed header");
     n=+x[1];m=+x[2];if(n<1||m<1)throw Error("bad n/m");continue;
   }
   if(n===null)throw Error("no header");
   let x=s.split(/\s+/).map(Number);
   if(!x.every(Number.isSafeInteger)||x.at(-1)!==0||x.length<2||
      x.slice(0,-1).some(v=>v===0||Math.abs(v)>n))throw Error("bad literal");
   let c=x.slice(0,-1);
   if(new Set(c.map(Math.abs)).size!==c.length)throw Error("duplicate or tautological clause");
   clauses.push(c);
 }
 if(m===null||clauses.length!==m)throw Error("clause-count mismatch");
 return {n,m,clauses};
}
function expectFor(n){
 const ell=Math.log2(n),m=n+1,original=[],v=(p,b)=>1+p*ell+b;
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let z=0;z<n;z++){
   let lits=[];
   for(let p of [i,j])for(let b=0;b<ell;b++)lits.push(((z>>b)&1)?-v(p,b):v(p,b));
   original.push({i,j,z,lits});
 }
 let next=m*ell+1,clauses=[],meta=[];
 for(const parent of original){
   let l=parent.lits,k=l.length,ys=[];
   for(let z=0;z<k-3;z++)ys.push(next++);
   let C=[[l[0],l[1],ys[0]]];
   for(let t=1;t<ys.length;t++)C.push([-ys[t-1],l[t+1],ys[t]]);
   C.push([-ys.at(-1),l.at(-2),l.at(-1)]);
   clauses.push(...C);meta.push({parent,ys});
 }
 return {vars:next-1,clauses,meta,ell,m};
}
function witness(info,position){
 const {meta,ell,m,vars}=info,q=2*ell-2,parentId=Math.floor(position/q),part=position%q;
 const selected=meta[parentId].parent,ls=Array(m).fill(-1);
 ls[selected.i]=selected.z;ls[selected.j]=selected.z;
 let remain=[];for(let i=0;i<(1<<ell);i++)if(i!==selected.z)remain.push(i);
 for(let p=0;p<m;p++)if(ls[p]===-1)ls[p]=remain.shift();
 claim(remain.length===0,"unused labels");
 let a=Array(vars+1).fill(false);
 for(let p=0;p<m;p++)for(let b=0;b<ell;b++)a[1+p*ell+b]=!!(ls[p]&(1<<b));
 for(let index=0;index<meta.length;index++){
   let {parent,ys}=meta[index];
   const litTrue=l=>a[Math.abs(l)]===(l>0);
   const vals=parent.lits.map(litTrue);
   if(index===parentId){
     claim(vals.every(x=>!x),"selected original clause was true");
     for(let t=0;t<ys.length;t++)a[ys[t]]=t<part;
   }else{
     claim(vals.some(Boolean),"second original clause false");
     for(let t=0;t<ys.length;t++)a[ys[t]]=!vals.slice(0,t+2).some(Boolean);
   }
 }
 return a;
}
function audit(file,n){
 const t=fs.readFileSync(file,"utf8"),p=parseDIMACS(t),a=expectFor(n);
 claim(p.n===a.vars&&p.m===a.clauses.length,"headers");
 p.clauses.forEach((c,i)=>claim(c.length===3&&
  c.every((x,j)=>x===a.clauses[i][j]),"literal mismatch "+i));
 for(let i=0;i<p.m;i++){
   let w=witness(a,i),viol=0,violIdx=-1;
   for(let j=0;j<p.m;j++){
     if(!p.clauses[j].some(l=>w[Math.abs(l)]===(l>0))){viol++;violIdx=j;}
   }
   claim(viol===1&&violIdx===i,"deletion witness fails "+i);
   for(const l of p.clauses[i])claim(w[Math.abs(l)]!==(l>0),"sign flip does not repair");
 }
 let bad=[t.replace(/p cnf \d+ \d+/,"p cnf "+a.vars+" "+(p.m+1)),
    t.replace(/p cnf \d+ \d+/,"p cnf "+(a.vars-1)+" "+p.m),
    t.replace(/\d+ 0\n/,(a.vars+20)+" 0\n"),
    t.replace(/ 0\n/," 12\n"),t.replace(/p cnf \d+ \d+/,"p cat 1 1")];
 for(const b of bad){let rejected=false;try{
    const x=parseDIMACS(b);
    if(x.n!==a.vars||x.m!==p.m||JSON.stringify(x.clauses)!==JSON.stringify(a.clauses))rejected=true;
   }catch(e){rejected=true;}claim(rejected,"malformed source accepted")}
 return {n,vars:p.n,clauses:p.m,source_deletions_checked:p.m,
    sign_flips_certified:3*p.m,
    sha256:crypto.createHash("sha256").update(t).digest("hex"),checks};
}
let results=[];
for(const n of [4,8])results.push(audit(path.join(__dirname,"bphp3_n"+n+".cnf"),n));
console.log(JSON.stringify({status:"PASS",independent_checks:checks,results},null,2));
