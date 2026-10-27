/* ARC-VIRTUAL-GUEST-CHECKPOINT145 standalone ECMAScript verifier, no dependencies. */
function main(){
 let checks=0;const ok=(x,m)=>{checks++;if(!x)throw Error(m)};
 let seed=1452026;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
 const rows=[];
 for(const [n,m] of [[3,8],[7,7],[43,41],[345,89],[10000,256],[999999,513]]){
  const clauses=[];
  for(let i=0;i<m;i++){
    if(n===3&&m===8){const a=i;clauses.push([0,1,2].map(j=>((a>>j)&1)?-(j+1):j+1))}
    else{
      let ids=new Set();while(ids.size<3)ids.add(1+(rand()%n));
      clauses.push([...ids].map(v=>(rand()&1)?v:-v));
    }
  }
  const src='p cnf '+n+' '+m+'\n'+clauses.map(c=>c.join(' ')+' 0\n').join('');
  let cursor=src.indexOf('\n')+1;let starts=[];
  for(const c of clauses){starts.push(cursor);cursor+=c.join(' ').length+3}
  ok(cursor===src.length,'source cursor');
  if(n===3){
    const SAT=(a)=>clauses.every(c=>c.some(z=>Boolean((a>>(Math.abs(z)-1))&1)===(z>0)));
    ok(!Array.from({length:8},(_,i)=>i).some(SAT),'3var complete UNSAT');
  }
  for(const B of [1,2,3,5,8,16,32,64,128]){
    const cp=starts.filter((_,i)=>i%B===0);
    ok(cp.length===Math.ceil(m/B),'cp count');
    let reads=0;
    for(let j=0;j<m;j++){
      let p=cp[Math.floor(j/B)];
      for(let k=Math.floor(j/B)*B;k<j;k++){let e=src.indexOf('\n',p);ok(e>=0,'scan delimiter');reads+=e+1-p;p=e+1}
      let e=src.indexOf('\n',p);reads+=e+1-p;
      ok(p===starts[j],'indexed locator exact');
      ok(src.slice(p,e)===clauses[j].join(' ')+' 0','authenticated clause');
    }
    rows.push({n,m,B,indexBits:cp.length*Math.ceil(Math.log2(8*src.length+1)),reads});
  }
 }
 let neighbors=0;for(const m of [3,5,16,27,64,127]){
  for(const [a,b] of [[1,1],[2,3],[4,4],[7,2],[9,5]]){
    const x=Array(m).fill(0);let visited=[];
    function first(i){let v=0;for(let j=i*a;j<Math.min(m,(i+1)*a);j++){visited.push(j);v|=x[j]}return v}
    const L1=Math.ceil(m/a),L2=Math.ceil(L1/b);
    function second(k){let v=0;for(let i=k*b;i<Math.min(L1,(k+1)*b);i++)v|=first(i);return v}
    let z=Array.from({length:L2},(_,k)=>second(k));ok(!z.some(Boolean),'zero output');
    ok(visited.length===m,'zero source full cover');ok(m<=a*b*L2,'guest cover');
    for(let j=0;j<m;j++){x[j]=1;visited=[];z=Array.from({length:L2},(_,k)=>second(k));ok(z.some(Boolean),'singleton changed');x[j]=0;neighbors++}
  }
 }
 for(const m of [1,2,5,31,127]){
  let x=Array(m).fill(0), reads=0;
  const len=()=>{let v=0;for(const b of x){reads++;v|=b}return 1+v};
  ok(len()===1&&reads===m,'zero len');
  for(let j=0;j<m;j++){x[j]=1;reads=0;ok(len()===2&&reads===m,'length source dependency');x[j]=0}
 }
 return {status:'COMPUTATIONAL compact JS replica',assertions:checks,failures:0,checkpoint_parameter_rows:rows.length,source_OR_singleton_neighbors:neighbors,
  largest_example:rows.filter(x=>x.m===513 && [1,128].includes(x.B)),
  notes:'This compact replica checks indexed offsets and OR cover; full Python controls additionally authenticate malformed inputs and 288 connected-prism singleton mutants.'};
}
const result=main();
if(typeof console!=='undefined')console.log(JSON.stringify(result,null,2));
return result;
