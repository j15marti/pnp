"use strict";
// LSPV-3 BPHP-FULL-COOK-CERTIFICATE346. Exact finite signed-source tests.
// This public script does not replay full RES/DEF DAGs: full independent
// Python checker, producer, and 3 complete certificates are in companion ZIP.
const assert=(v,m)=>{if(!v)throw Error(m);};
function source(h){
 const ell=Math.log2(h);assert(Number.isInteger(ell)&&ell>=2,"power-of-two holes");
 const clauses=[],indices=[],nv=(h+1)*ell,bit=(i,b)=>i*ell+b+1;
 for(let i=0;i<=h;i++)for(let j=i+1;j<=h;j++)for(let a=0;a<h;a++){
  const c=[];
  for(let b=0;b<ell;b++)c.push((a>>b&1)?-bit(i,b):bit(i,b));
  for(let b=0;b<ell;b++)c.push((a>>b&1)?-bit(j,b):bit(j,b));
  clauses.push(c);indices.push([i,j,a]);
 }
 return{ell,nv,clauses,indices};
}
function evalClause(c,holes,ell){
 return c.some(l=>{const v=Math.abs(l)-1,p=Math.floor(v/ell),b=v%ell;
   const value=(holes[p]>>b)&1;return l>0?value===1:value===0;});
}
function witness(h,i,j,a){
 const holes=new Array(h+1).fill(-1);holes[i]=a;holes[j]=a;
 const rest=[];for(let b=0;b<h;b++)if(b!==a)rest.push(b);
 let n=0;for(let p=0;p<=h;p++)if(holes[p]<0)holes[p]=rest[n++];
 return holes;
}
function checkSources(h){
 const d=source(h),m=d.clauses.length;
 assert(m===h*h*(h+1)/2,"source size");
 let deletion=0,sign=0;
 for(let t=0;t<m;t++){
  const[i,j,a]=d.indices[t],ass=witness(h,i,j,a);
  let falses=0,idx=-1;
  for(let k=0;k<m;k++)if(!evalClause(d.clauses[k],ass,d.ell)){falses++;idx=k;}
  assert(falses===1&&idx===t,"sole false original "+h+"/"+t);deletion++;
  const clause=d.clauses[t];
  for(let z=0;z<clause.length;z++){
   const flip=clause.slice();flip[z]=-flip[z];
   assert(evalClause(flip,ass,d.ell),"signed occurrence flip");sign++;
  }
 }
 const positive=new Array(h);for(let i=0;i<h;i++)positive[i]=i;
 for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)for(let a=0;a<h;a++){
  const c=[];
  for(let b=0;b<d.ell;b++)c.push((a>>b&1)?-(i*d.ell+b+1):i*d.ell+b+1);
  for(let b=0;b<d.ell;b++)c.push((a>>b&1)?-(j*d.ell+b+1):j*d.ell+b+1);
  assert(evalClause(c,positive,d.ell),"h-to-h injective SAT control");
 }
 if(h===4)for(let mask=0;mask<Math.pow(h,h+1);mask++){
  let z=mask;const ass=[];
  for(let i=0;i<=h;i++){ass.push(z%h);z=Math.floor(z/h);}
  assert(d.clauses.some(c=>!evalClause(c,ass,d.ell)),"exhaustive h4 UNSAT");
 }
 return{h,variables:d.nv,clauses:m,essential_sources:deletion,sign_flip_SAT_controls:sign,lower_bound:m-1};
}
function cookProjector(){
 let mask=0;
 for(let w=0;w<32;w++){
  const[a,b,c,d,e]=[0,1,2,3,4].map(i=>(w>>i)&1);
  if(a&&d||a&&c||d&&c||b&&e)continue;
  const t=b&&c,q=a||t,tp=e&&c,qp=d||tp;
  assert(!(q&&qp),"Cook collision contradiction");
  mask|=1<<((q?2:0)+(qp?1:0));
 }
 assert(mask===7,"projection exactly NOT q OR NOT qprime");
 return{projected_relation_mask:mask,base_assignments:32};
}
const result={
 run_id:"LSPV3_BPHP_FULL_COOK_CERTIFICATE346",
 status:"COMPUTATIONAL signed controls only, neither full-DAG replay nor minimum certificate",
 cases:[checkSources(4),checkSources(8),checkSources(16)],
 cook_collision:cookProjector()
};
process.stdout.write(JSON.stringify(result,null,2)+"\n");