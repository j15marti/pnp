function groupTest(){
 const assert=(a,m)=>{if(!a)throw Error(m);};let out=[];
 function make(s){const n=3*s*s,inc=Array.from({length:2*s*s},()=>[]);let e=0;const id=(i,j)=>(i%s)*s+j%s;
 for(let i=0;i<s;i++)for(let j=0;j<s;j++)for(const b of [id(i,j),id(i+1,j),id(i,j+1)]){inc[id(i,j)].push(e);inc[s*s+b].push(e++);}
 const owners=[];for(let v=0;v<inc.length;v++)for(let k=0;k<8;k++)if(((k&1)+((k>>1)&1)+((k>>2)&1))%2!==Number(v===0)){
   owners.push({cost:inc[v].map((i,j)=>({i,c:(k>>j)&1?[0,1]:[1,0]})),budget:2});
 }return {n,owners};}
 // Accept only actual explicit owner row-cost records, not source graph or charge labels.
 function solve(n,owners){
  let groups=new Map();for(let O of owners){const l=O.cost.slice().sort((a,b)=>a.i-b.i);const key=l.map(z=>z.i).join(",");if(!groups.has(key))groups.set(key,{ids:l.map(z=>z.i),owners:[]});groups.get(key).owners.push({l,budget:O.budget});}
  const equations=[],non=[],odd=(a)=>{let b=0;while(a){b^=a&1;a>>=1;}return b;};
  for(let {ids,owners:os} of groups.values()){let d=ids.length,allowed=[];for(let x=0;x<2**d;x++)if(os.every(o=>o.l.reduce((a,z,j)=>a+z.c[(x>>j)&1],0)<=o.budget))allowed.push(x);
   if(!allowed.length)return {sat:false,nonaffine:0,queries:0};
   let eq=[];for(let w=1;w<2**d;w++){let r=odd(w&allowed[0]);if(allowed.every(x=>odd(w&x)===r)){let mask=0n;for(let i=0;i<d;i++)if((w>>i)&1)mask|=1n<<BigInt(ids[i]);eq.push([mask,r,w]);}}
   const hull=Array.from({length:2**d},(_,i)=>i).filter(x=>eq.every(([m,r,w])=>odd(w&x)===r));
   if(hull.length===allowed.length)equations.push(...eq.map(([m,r])=>[m,r]));else non.push({ids,allowed});
  }
  const U=[...new Set(non.flatMap(o=>o.ids))];let queries=0,answer=null;
  for(let a=0;a<2**U.length;a++){
   const pins=new Map(U.map((u,i)=>[u,(a>>i)&1]));if(!non.every(o=>o.allowed.includes(o.ids.reduce((m,u,i)=>m|(pins.get(u)<<i),0))))continue;
   queries++;let basis=new Map(),bad=false;
   for(let [m,r] of equations.concat(U.map(u=>[1n<<BigInt(u),pins.get(u)]))){while(m){let p=m&(-m);if(basis.has(p)){let [v,t]=basis.get(p);m^=v;r^=t;}else{basis.set(p,[m,r]);break;}}if(m===0n&&r){bad=true;break;}}
   if(bad)continue;
   let x=0n;for(let [p,[m,r]] of [...basis].sort((a,b)=>a[0]>b[0]?-1:1)){let v=(m^p)&x,b=r;while(v){v&=v-1n;b^=1;}if(b)x|=p;}
   assert(owners.every(o=>o.cost.reduce((s,z)=>s+z.c[Number((x>>BigInt(z.i))&1n)],0)<=o.budget),"lift");answer=x;break;
  }
  return {sat:answer!==null,groups:groups.size,affineEquations:equations.length,nonaffine:non.length,conditionedBits:U.length,queries};
 }
 for(let s of [2,3,4,8,16,32]){const {n,owners}=make(s);let a=solve(n,owners);let B=owners.map((o,i)=>i===0?{...o,budget:3}:o),b=solve(n,B);assert(!a.sat&&b.sat&&a.nonaffine===0&&b.nonaffine===1,"grouping");out.push({s,n,unsat:a,satNeighbor:b});}
 return out;
}
console.log(JSON.stringify(groupTest(),null,2));
