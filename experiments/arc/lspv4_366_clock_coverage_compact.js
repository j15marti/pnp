"use strict";
// LSPV4 366 no-import finite reflection/transfer falsifier. No general Rmix checker.
let k=0;function ck(x,m){k++;if(!x)throw Error(m||"check");}
const H=(b,wrong=false)=>{let f=[[1,2],[-1,2],[-1,-2]];
 if(!(wrong&&b>=2))f.push([1]);if(b<6)f.push([-1]);return f;};
function models(f,n){let total=0;for(let a=0;a<(1<<n);a++)
 if(f.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))total++;return total;}
function restrict(c,v,b){return c.some(l=>Math.abs(l)===v&&(l>0)===b)
 ?null:c.filter(l=>Math.abs(l)!==v);}
function res(a,b,v){ck(a.includes(v)&&b.includes(-v),"pivot");
let c=[...new Set([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)])];
ck(!c.some(l=>c.includes(-l)),"tautology");return c.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const src=H(6),p=src.map(x=>x.slice());ck(models(src,2)===0,"H6 UNSAT");
p.push(res(p[3],p[1],1));p.push(res(p[3],p[2],1));p.push(res(p[4],p[5],2));
ck(eq(p[6],[]),"refutation");ck(eq(restrict(src[1],1,true),[2]),"source y");
ck(eq(restrict(src[2],1,true),[-2]),"source -y");
ck(restrict(src[3],1,true)===null,"reject gate true");
for(let b=0;b<8;b++){const f=H(b);ck(models(f,2)===0,"honest H");
const residual=f.map(c=>restrict(c,1,true)).filter(c=>c!==null);
if(b<6)ck(residual.some(c=>!c.length),"underclock false source");
else ck(!residual.some(c=>!c.length),"clock covered");}
for(let b=2;b<8;b++)ck(models(H(b,true),2)>0,"wrong decider must have witness");
function php(h){let p=h+1,v=(i,j)=>1+i*h+j,r=[];
for(let i=0;i<p;i++)r.push(Array.from({length:h},(_,j)=>v(i,j)));
for(let j=0;j<h;j++)for(let i=0;i<p;i++)for(let z=i+1;z<p;z++)r.push([-v(i,j),-v(z,j)]);
return [r,p*h];}
for(let h=1;h<=3;h++){let [f,n]=php(h);ck(models(f,n)===0,"PHP UNSAT");
for(let j=0;j<f.length;j++)ck(models(f.filter((_,i)=>i!==j),n)>0,"deleted PHP SAT");}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function countParity(charge){let n=0;for(let mask=0;mask<64;mask++){
let good=true;for(let v=0;v<4;v++){let x=0;for(let e=0;e<6;e++)
if(edges[e].includes(v))x^=(mask>>e)&1;if(x!==charge[v])good=false;}if(good)n++;}return n;}
ck(countParity([1,0,0,0])===0,"odd K4");ck(countParity([0,0,0,0])===8,"even K4");
const xor=(a,b)=>[a[0].filter(x=>!b[0].includes(x)).concat(b[0].filter(x=>!a[0].includes(x))).sort(),a[1]^b[1]];
const rr=(r,v,b)=>[r[0].filter(x=>x!==v),r[1]^(r[0].includes(v)?b:0)];
const r1=[[0,1],1],r2=[[1,2],0];
for(let v=0;v<3;v++)for(let b=0;b<2;b++)
ck(eq(rr(xor(r1,r2),v,b),xor(rr(r1,v,b),rr(r2,v,b))),"XOR restriction");
ck(eq(xor(r1,r1),[[],0]),"repeated parent");
ck(!eq([-2],[2]),"fake parent");
process.stdout.write(JSON.stringify({status:"PASS",assertions:k,scope:"restricted RES/XOR and clock/source both-label controls"})+"\n");
