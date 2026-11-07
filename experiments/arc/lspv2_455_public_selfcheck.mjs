// LSPV-2/455 standalone finite CONTROL, not native FLMV or a general SAT compiler.
import assert from 'node:assert/strict';
let checks=0;
const eq=(a,b)=>{assert.equal(a,b);checks++;};
function sat(F){const V=[...new Set(F.flat().map(Math.abs))];
 if(F.some(C=>!C.length))return false;
 for(let m=0;m<2**V.length;m++){
  const a=new Map(V.map((v,i)=>[v,Boolean((m>>i)&1)]));
  if(F.every(C=>C.some(l=>a.get(Math.abs(l))===(l>0))))return true;
 }return false;}
function k4(start){let E=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);
 let F=[];for(let v=0;v<4;v++){
  let ids=E.map((e,i)=>e.includes(v)?start+i:null).filter(x=>x!==null);
  for(let p=0;p<2;p++)for(let q=0;q<2;q++){
   let r=p^q^1;F.push([p?-ids[0]:ids[0],q?-ids[1]:ids[1],r?-ids[2]:ids[2]]);
  }}return F;}
function port(z,a,b,t){let F=[];for(let x of [0,1])for(let y of [0,1])
 F.push([t?z:-z,x?a:-a,y?b:-b]);return F;}
function restrict(F,z){return F.map(C=>{
 let satClause=C.some(l=>Math.abs(l)===1&&((l>0)===z));
 return satClause?null:C.filter(l=>Math.abs(l)!==1);
 }).filter(C=>C!==null);}
for(let l of [0,1])for(let r of [0,1]){
 const L=k4(2).concat(port(1,8,9,l)),R=k4(10).concat(port(1,16,17,r));
 eq(L.length,20);eq(R.length,20);let join=false;
 for(let z of [false,true])if(sat(restrict(L,z))&&sat(restrict(R,z))){join=true;break;}
 eq(join,Boolean(l===r));eq(join,sat(L.concat(R)));
}
function graph(s){if(s==='K4'){let E=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E.push([i,j]);return [4,E];}
 if(s==='Cube'){let E=[];for(let i=0;i<8;i++)for(let d of [1,2,4])if(i<(i^d))E.push([i,i^d]);return [8,E];}
 let E=[];for(let i=0;i<5;i++)E.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);return [10,E];}
function minCut(n,E){let groups=[],best=E.length;
 function rec(v){if(v===n){let label=Array(n);groups.forEach((g,i)=>g.forEach(x=>label[x]=i));
  best=Math.min(best,E.filter(([x,y])=>label[x]!==label[y]).length);return;}
  for(let g of groups)if(g.length<2){g.push(v);rec(v+1);g.pop();}
  groups.push([v]);rec(v+1);groups.pop();}
 rec(0);return best;}
for(let [name,want] of [['K4',4],['Cube',8],['Petersen',10]]){
 const [n,E]=graph(name);eq(E.length,3*n/2);eq(minCut(n,E),want);
}
console.log(JSON.stringify({status:'PASS',checks,scope:'finite signed K4 SAT joins and exact bounded packet cuts; not native FLMV'}));
