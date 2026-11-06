// LSPV-2/440: independently executable finite structural/source controls.
// Standard graph formulas, NOT a native FLMV machine or a P-vs-NP result.
let tests=0;const ok=(x)=>{tests++;if(!x)throw Error('failed '+tests)};
function run(H,edges,odd){
 const A=Array.from({length:H},()=>[]);
 for(let [u,v] of edges){A[u].push(v);A[v].push(u)}
 A.forEach(a=>a.sort((x,y)=>x-y));
 const p=Array(H).fill(-1),d=Array(H).fill(-1);p[0]=d[0]=0;
 const q=[0];for(let v of q)for(let u of A[v])if(d[u]<0){p[u]=v;d[u]=d[v]+1;q.push(u)}
 function valid(B,pp,dd){
  if(pp[0]!==0||dd[0]!==0)return false;
  for(let v=0;v<H;v++){
   let a=B[v];if(a.length!==3||new Set(a).size!==3||a.some((u,j)=>u<0||u>=H||u===v||(j&&u<=a[j-1])||!B[u].includes(v)))return false;
   if(v&&(!a.includes(pp[v])||dd[v]<1||dd[pp[v]]!==dd[v]-1))return false;
  }return true;
 }
 ok(q.length===H&&valid(A,p,d));
 const B=A.map(a=>a.slice());B[0][0]=B[0][1];ok(!valid(B,p,d));
 const badp=p.slice();badp[1]=1;ok(!valid(A,badp,d));
 const charges=Array(H).fill(0);charges[0]=Number(odd);
 const id=(u,v)=>{let a=Math.min(u,v),b=Math.max(u,v);return 3*a+A[a].indexOf(b)+1};
 let clauses=[];
 for(let v=0;v<H;v++){
  const ids=A[v].map(u=>id(v,u)).sort((a,b)=>a-b);let local=0;
  for(let a=0;a<8;a++){
   let b=[a>>2,(a>>1)&1,a&1];
   if((b[0]^b[1]^b[2])===charges[v])continue;
   clauses.push(ids.map((n,j)=>b[j]?-n:n));local++;
  }ok(local===4);
 }
 ok(clauses.length===4*H&&new Set(clauses.flat().map(Math.abs)).size===3*H/2);
 if(edges.length<=15){
  const vars=[...new Set(clauses.flat().map(Math.abs))];let models=0;
  for(let m=0;m<2**vars.length;m++)if(clauses.every(c=>c.some(l=>Boolean(m&(1<<vars.indexOf(Math.abs(l))))===(l>0))))models++;
  ok(models===(odd?0:2**(H/2+1)));
 }
 return {H,clauses:clauses.length,treeDepth:Math.max(...d),charge:odd?'UNSAT':'SAT'};
}
const K4=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)K4.push([u,v]);
const cube=[];for(let u=0;u<8;u++)for(let b=0;b<3;b++){let v=u^(1<<b);if(u<v)cube.push([u,v])}
const pent=[];for(let i=0;i<5;i++){pent.push([i,(i+1)%5],[5+i,5+(i+2)%5],[i,5+i])}
let output=[];for(let [h,e] of [[4,K4],[8,cube],[10,pent]])for(let odd of [false,true])output.push(run(h,e,odd));
console.log(JSON.stringify({status:'PASS',checks:tests,controls:output}));
