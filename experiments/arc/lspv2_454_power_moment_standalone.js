// LSPV-2/454 self-contained, independent signed original 3-CNF / moment control.
// No native-Turing-machine timing or workspace guarantee.
function assert(x,msg){if(!x)throw new Error(msg);}
function facets(L,odd){
 const edges=[];
 for(let i=0;i<L;i++){edges.push([i,(i+1)%L]);edges.push([L+i,L+(i+1)%L]);edges.push([i,L+i]);}
 const es=edges.map(e=>e.slice().sort((a,b)=>a-b)).sort((u,v)=>u[0]-v[0]||u[1]-v[1]);
 const inc=Array.from({length:2*L},()=>[]);
 es.forEach((e,i)=>e.forEach(v=>inc[v].push(i+1)));
 const out=[];
 inc.forEach((e,v)=>{e.sort((a,b)=>a-b);assert(e.length===3,"degree");
  for(let a=0;a<2;a++)for(let b=0;b<2;b++){
   const signs=[a,b,a^b^1^Number(odd&&v===0)];
   out.push([4*v+2*a+b+1,e.map((x,j)=>signs[j]?-x:x)]);
  }
 });
 return out;
}
function same(x,y){return JSON.stringify(x)===JSON.stringify(y);}
function moments(rows,k){
 const p=65537, out=Array(k+1).fill(0);
 for(const [id] of rows){let z=1;for(let j=0;j<=k;j++){out[j]=(out[j]+z)%p;z=z*id%p;}}
 return out;
}
function accepts(rows,canonical,k){
 if(rows.length!==canonical.length)return false;
 for(const [id,cl] of rows){if(id<1||id>canonical.length||!same([id,cl],canonical[id-1]))return false;}
 return same(moments(rows,k),moments(canonical,k));
}
function mutate(canonical,A,B){
 const rows=canonical.slice();A.forEach((a,i)=>rows[a-1]=canonical[B[i]-1]);return rows;
}
function prouhet(k){
 const A=[],B=[];
 for(let i=0;i<2**(k+1);i++){
  let z=i,parity=0;while(z){parity^=z&1;z=Math.floor(z/2);}
  (parity?B:A).push(i+1);
 }
 return [A,B];
}
function main(){
 let checks=0,good=0,rejected=0,collisions=0;
 for(const odd of [false,true]){
  const F=facets(16,odd),m=F.length;
  for(let k=1;k<=5;k++){
   assert(accepts(F.slice().reverse(),F,k),"perm");checks++;good++;
   for(let r=1;r<=k;r++){
    const A=Array.from({length:r},(_,i)=>i+1),B=Array.from({length:r},(_,i)=>m-r+i+1);
    assert(!accepts(mutate(F,A,B),F,k),"bounded-edit");checks++;rejected++;
   }
   const [A,B]=prouhet(k);
   assert(accepts(mutate(F,A,B),F,k),"Prouhet missed");checks++;collisions++;
   assert(!accepts(F.slice(1),F,k),"count");checks++;
   const signed=F.slice();signed[0]=[signed[0][0],signed[0][1].map(x=>-x)];
   assert(!accepts(signed,F,k),"sign");checks++;
  }
 }
 return {status:"PASS",checks,good,rejected,collisions,model:"host JS; promise only; no all-input certificate"};
}
main();
