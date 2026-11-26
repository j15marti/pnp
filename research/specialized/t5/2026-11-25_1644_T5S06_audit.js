/* T5S06; run with node */
function audit(){
 const m=x=>(x%5+5)%5,D=[0,1,2,3,4],S={assertions:0,scans:0,series:0,full:0,leaf:0,loops:0,random:{SAT:0,UNSAT:0,UNKNOWN:0,refSAT:0,refUNSAT:0},packed:[]};
 function ok(x){S.assertions++;if(!x)throw Error("assertion "+S.assertions)}
 let seed=20261125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const R=(a,b)=>[1,3].includes(m(b-a)),C=(a,b,c)=>(R(a,b)&&R(b,c)&&R(c,a))||(R(b,a)&&R(c,b)&&R(a,c));
 function product(n,f,a=[]){if(a.length===n){f(a);return}for(let x of D)product(n,f,[...a,x])}
 let ct=[0,0,0,0,0,0];product(3,([a,b,c])=>{let d=new Set([a,b,c]).size===3,H=d&&R(a,b)!==R(a,c);ok(C(a,b,c)===(d&&D.some(i=>[a,b,c].every(v=>[i,m(i+1),m(i+2)].includes(v)))));ok(C(a,b,c)===(H&&(d&&R(b,a)!==R(b,c))));ct[0]+=+C(a,b,c);ct[1]+=+H;ct[2]+=+(R(a,b)!==R(a,c));ct[3]+=+(R(a,b)&&R(a,c));ct[4]+=+(R(a,c)&&R(b,c));ct[5]+=+(d&&R(a,c)&&R(b,c))});ok(String(ct)==="30,40,60,20,20,10");
 product(5,a=>ok(D.every(i=>C(a[i],a[m(i+1)],a[m(i+2)]))===[1,4].some(d=>D.every(i=>a[i]===m(a[0]+d*i)))));
 for(let p of [0,1])for(let q of [0,1]){let out=[];for(let x of [0,1])for(let y of D)for(let z of D)if(C(1,2,y)&&C(0,1,z)&&C(4,p,y)&&C(3,q,z)&&C(x,y,z))out.push(x);ok(String(out)===String(p|q));for(let x of [0,1])ok(C(2,p,x)===(x===1-p))}
 for(let b of D)ok([2,3,4].every(j=>D.some(h=>C(j,b,h)))===[0,1].includes(b));
 let gadget=0;product(5,([u,v,a,b,h])=>{if(C(a,u,v)&&C(u,v,b)&&C(a,h,b)){gadget++;ok([1,4].includes(m(v-u)))}});ok(gadget===20);
 for(let u of D)for(let d of [1,4]){let v=m(u+d),a=m(u-d),b=m(v+d),h=m(u+3*d);ok(C(a,u,v)&&C(u,v,b)&&C(a,h,b)&&m(a+v-2*u)===0&&m(u+b-2*v)===0&&m(a+b-2*h)===0)}
 for(let u of D)for(let v of D)ok([1,4].some(a=>[1,4].some(b=>[1,4].some(c=>m(a+b+c)===m(v-u))))===(u!==v));
 function edge(u,v,h=0){return {u,v,A:[m(h-1),m(h+1)]}}
 function verify(E,x){return E.every(e=>e.A.includes(m(x[e.v]-x[e.u])))}
 function strict(E,x){return E.every(e=>C(x[e.v],x[e.u],m(2*x[e.u]-x[e.v])))}
 function rank(n,E){let p=Array.from({length:n},(_,i)=>i);function root(i){while(i!==p[i])i=p[i];return i}for(let e of E)p[root(e.u)]=root(e.v);return E.length-n+new Set(p.map((_,i)=>root(i))).size}
 function solve(n,G){
   let V=new Set(Array.from({length:n},(_,i)=>i)),E=G.map((e,i)=>({...e,path:[i]})),stack=[];
   function close(){for(let e of E){S.scans++;if(!e.A.length||(e.u===e.v&&!e.A.includes(0)))return false;}E=E.filter(e=>e.u!==e.v);return true}
   if(!close())return {status:"UNSAT"};
   while(V.size){
     let v=[...V].find(v=>E.filter(e=>e.u===v||e.v===v).length<=2);
     if(v===undefined){ok(close());let ids=E.flatMap(e=>e.path);ok(new Set(ids).size===ids.length);ok(E.every(e=>e.path.length<=3));let r=rank(n,ids.map(i=>G[i]));ok(r>0&&ids.length<9*r);return {status:"UNKNOWN",density:[ids.length,r]}}
     let I=E.filter(e=>e.u===v||e.v===v),other=e=>e.u===v?e.v:e.u;E=E.filter(e=>!I.includes(e));V.delete(v);stack.push({v,I});
     if(I.length===1)S.leaf++;
     if(I.length===2){S.series++;let a=other(I[0]),b=other(I[1]),L=I[0].v===v?I[0].A:I[0].A.map(d=>m(-d)),M=I[1].u===v?I[1].A:I[1].A.map(d=>m(-d)),A=[...new Set(L.flatMap(l=>M.map(r=>m(l+r))))];
       if(a===b){S.loops++;if(!A.includes(0))return {status:"UNSAT"}}
       else if(A.length===5)S.full++;
       else E.push({u:a,v:b,A,path:[...I[0].path,...I[1].path]});
     }
     if(!close())return {status:"UNSAT"};
   }
   let x=Array(n).fill(-1);
   for(let {v,I} of stack.reverse()){let z=D.find(z=>I.every(e=>{let a=e.u===v?z:x[e.u],b=e.v===v?z:x[e.v];ok(a!==-1&&b!==-1);return e.A.includes(m(b-a))}));ok(z!==undefined);x[v]=z}
   ok(verify(G,x));return {status:"SAT",x}
 }
 function brute(n,E){let b=false;product(n,x=>{if(!b&&verify(E,x))b=true});return b}
 for(let k=0;k<160;k++){let n=2+rnd(5),E=[];let count=1+rnd(2*n+2);for(let j=0;j<count;j++){let u=rnd(n),v=rnd(n-1);if(v>=u)v++;E.push(edge(u,v,rnd(5)))}let ref=brute(n,E),out=solve(n,E);S.random[ref?"refSAT":"refUNSAT"]++;S.random[out.status]++;ok(out.status==="UNKNOWN"||(out.status==="SAT")===ref)}
 for(let n0 of [4,7,10,14]){let n=n0,E=[],pack=Array.from({length:9},()=>new Set());for(let i=0;i<n0-1;i++)E.push(edge(i,i+1,rnd(5)));for(let u=0;u<n0;u++)for(let v=u+2;v<n0;v++){let p=u;for(let j=0;j<9;j++){let q=j===8?v:n++;pack[j].add(E.length);E.push(edge(p,q,rnd(5)));p=q}}let r=rank(n,E);ok(new Set(pack.flatMap(s=>[...s])).size===9*r);for(let s of pack)ok(s.size===r&&rank(n,E.filter((_,i)=>!s.has(i)))===0);let out=solve(n,E);ok(out.status==="SAT");let zero=E.map(e=>edge(e.u,e.v)),z=solve(n,zero);ok(z.status==="SAT"&&strict(zero,z.x));S.packed.push({vertices:n,edges:E.length,rank:r,bases:9,status:out.status,strictLift:z.status})}
 let bad=[edge(0,1),edge(1,2),edge(2,0)];for(let i=3;i<103;i++)bad.push(edge(0,i));ok(solve(103,bad).status==="UNSAT");
 let K4=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)K4.push(edge(u,v));ok(!brute(4,K4)&&solve(4,K4).status==="UNKNOWN");
 let cy=[edge(0,1),edge(1,2),edge(2,3),edge(3,0)];let z=solve(4,cy);ok(z.status==="SAT"&&strict(cy,z.x));S.controls={triangleWith100Leaves:"UNSAT",K4:"UNKNOWN",fourCycle:"SAT"};return S
}
console.log(JSON.stringify(audit(),null,2));
