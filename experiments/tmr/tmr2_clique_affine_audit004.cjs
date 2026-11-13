"use strict";
// TMR-2/004 exact finite affine 3-CNF controls. Asymptotic claim is in report.
function yes(b,s){if(!b)throw Error(s||"assertion failed");}
function gate(a,b,c,p){
 let out=[];for(let i=0;i<8;i++){let x=i>>2,y=(i>>1)&1,z=i&1;
 if((x^y^z)!==p)out.push([x?-a:a,y?-b:b,z?-c:c]);}return out;
}
function make(m,bits){
 let E=new Map(),Y=new Map(),next=1;
 for(let v=0;v<m;v++)for(let w=v+1;w<m;w++)E.set(v+","+w,next++);
 for(let v=0;v<m;v++)for(let j=0;j<m-4;j++)Y.set(v+","+j,next++);
 let c=[],eq=[];
 for(let v=0;v<m;v++){
  let e=[];for(let w=0;w<m;w++)if(w!==v)e.push(E.get(Math.min(v,w)+","+Math.max(v,w)));
  let y=Array.from({length:m-4},(_,j)=>Y.get(v+","+j));
  let g=[[e[0],e[1],y[0],0]];
  for(let j=1;j<m-4;j++)g.push([y[j-1],e[j+1],y[j],0]);
  g.push([y[m-5],e[m-3],e[m-2],bits[v]]);
  for(let q of g){eq.push(q);c.push(...gate(...q));}
 }
 yes(next-1===3*m*(m-3)/2&&c.length===4*m*(m-3));
 return {N:next-1,c,eq,E,Y};
}
function encode(g){
 let w=Math.max(1,Math.ceil(Math.log2(g.N)));
 return "1".repeat(g.N)+"0"+"1".repeat(g.c.length)+"0"+
  g.c.map(c=>c.map(x=>(x<0?"1":"0")+(Math.abs(x)-1).toString(2).padStart(w,"0")).join("")).join("");
}
function decode(s){
 if(!/^[01]+$/.test(s))return null;
 let p=s.indexOf("0"),q=s.indexOf("0",p+1);
 if(p<1||q<p+2||!/^[1]+$/.test(s.slice(p+1,q)))return null;
 let N=p,M=q-p-1,w=Math.max(1,Math.ceil(Math.log2(N)));
 if(s.length!==q+1+3*M*(1+w))return null;
 let c=[],i=q+1;
 for(let j=0;j<M;j++){let z=[];
  for(let k=0;k<3;k++){
   let v=parseInt(s.slice(i+1,i+1+w),2)+1;
   if(v>N)return null;z.push(s[i]==="1"?-v:v);i+=w+1;
  }
  if(new Set(z.map(Math.abs)).size!==3)return null;c.push(z);
 }
 return {N,c};
}
function affine(c){
 let groups=new Map();
 for(let cl of c){
  let ids=cl.map(Math.abs).sort((a,b)=>a-b),k=ids.join(",");
  if(new Set(ids).size!==3)return null;
  let s=ids.map(v=>cl.find(x=>Math.abs(x)===v)<0?"1":"0").join("");
  if(!groups.has(k))groups.set(k,[]);groups.get(k).push(s);
 }
 let out=[];
 for(let [k,v] of groups){
  let a=new Set(v);if(a.size!==4||v.length!==4)return null;
  let odd=["001","010","100","111"],even=["000","011","101","110"];
  let b=odd.every(x=>a.has(x))?0:even.every(x=>a.has(x))?1:-1;
  if(b<0)return null;out.push([k.split(",").map(Number),b]);
 }
 return out;
}
function solve(rows){
 let P=new Map();
 for(let [v,b] of rows){
  let x=v.reduce((a,i)=>a^(1n<<BigInt(i-1)),0n);
  while(x){let h=x.toString(2).length-1;
   if(!P.has(h)){P.set(h,[x,b]);break;}
   let r=P.get(h);x^=r[0];b^=r[1];
  }if(!x&&b)return false;
 }return true;
}
function assignment(m,g,mask){
 let a=Array(g.N+1).fill(0),j=0;
 for(let x of g.E.values())a[x]=Number((mask>>BigInt(j++))&1n);
 for(let v=0;v<m;v++){
  let e=[];for(let w=0;w<m;w++)if(w!==v)e.push(g.E.get(Math.min(v,w)+","+Math.max(v,w)));
  let z=a[e[0]]^a[e[1]];a[g.Y.get(v+",0")]=z;
  for(let i=1;i<m-4;i++){z^=a[e[i+1]];a[g.Y.get(v+","+i)]=z;}
 }return a;
}
function minor(m,g){
 let adj=Array.from({length:g.N+1},()=>new Set());
 for(let c of g.c)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
  let x=Math.abs(c[i]),y=Math.abs(c[j]);adj[x].add(y);adj[y].add(x);
 }
 let part=[];
 for(let v=0;v<m;v++){
  let s=new Set();for(let j=0;j<m-4;j++)s.add(g.Y.get(v+","+j));
  for(let w=v+1;w<m;w++)s.add(g.E.get(v+","+w));
  let seen=new Set([s.values().next().value]),todo=[...seen];
  while(todo.length)for(let q of adj[todo.pop()])if(s.has(q)&&!seen.has(q)){seen.add(q);todo.push(q);}
  yes(seen.size===s.size,"minor connectivity");part.push(s);
 }
 for(let v=0;v<m;v++)for(let w=v+1;w<m;w++){
  let exists=false;for(let x of part[v])for(let y of adj[x])if(part[w].has(y))exists=true;
  yes(exists,"minor adjacency");
 }return true;
}
function audit(){
 let r={id:"TMR2-CLIQUE-AFFINE-004",status:"COMPUTATIONAL",cases:0,sat:0,unsat:0,
  decoded:0,affine:0,minor:0,assignments:0,counts:0,renamings:0,flips:0,missing:0,failures:0,lengths:{}};
 let seed=20261113;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
 for(let m of [6,8,10,12,20,50]){
  let B=[Array(m).fill(0),[1,...Array(m-1).fill(0)]];
  for(let j=0;j<3;j++)B.push(Array.from({length:m},()=>rnd()&1));
  for(let bits of B){
   let g=make(m,bits),src=encode(g),d=decode(src);
   yes(d&&d.N===g.N&&JSON.stringify(d.c)===JSON.stringify(g.c),"decode");r.decoded++;
   r.lengths[m]={N:g.N,M:g.c.length,L:src.length};
   let sat=bits.reduce((a,b)=>a^b,0)===0;
   yes(solve(affine(g.c))===sat,"wrong affine verdict");
   r.affine++;r.cases++;r[sat?"sat":"unsat"]++;
   if(m===6){
    yes(minor(m,g));r.minor++;let count=0;
    for(let k=0;k<32768;k++){
     let a=assignment(m,g,BigInt(k));
     let e=g.eq.every(([x,y,z,p])=>(a[x]^a[y]^a[z])===p);
     let c=g.c.every(cl=>cl.some(x=>a[Math.abs(x)]===(x>0?1:0)));
     yes(e===c,"gate not CNF");count+=Number(c);r.assignments++;
    }
    yes(count===(sat?1024:0),"solution count");r.counts++;
   }
   if(m<=10){
    let u=g.c.slice().reverse().map(cl=>cl.slice().reverse().map(x=>Math.sign(x)*(g.N+1-Math.abs(x))));
    yes(solve(affine(u))===sat);r.renamings++;
    let f=g.c.map(cl=>cl.map(x=>Math.abs(x)%2?-x:x));
    yes(solve(affine(f))===sat);r.flips++;
    yes(affine(g.c.slice(1))===null);r.missing++;
   }
  }
  if(m===8||m===10||m===12){yes(minor(m,make(m,Array(m).fill(0))));r.minor++;}
 }
 return r;
}
module.exports={audit,make,affine,solve};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
