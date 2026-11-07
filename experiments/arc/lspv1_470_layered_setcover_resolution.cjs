'use strict';
// LSPV-1/470. Restricted layered ordinary-Resolution plans and Set Cover.
// Run: node lspv1_470_layered_setcover_resolution.cjs
// No claim about unrestricted Resolution or historical R_mix341 minimum.
let checks=0;
function req(x,msg){checks++;if(!x)throw Error(msg);}
function norm(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b);}
function pop(x){let c=0;while(x){c+=x&1;x>>>=1;}return c;}
function make(k,masks){
 const r=masks.length,vars=1+r+k,clauses=[],ids={};
 const add=(tag,c)=>{const id='S'+clauses.length;ids[tag]=id;clauses.push({id,clause:norm(c)});};
 add('A',[1]);
 for(let j=0;j<r;j++)add('SET'+j,[-1,2+j]);
 for(let j=0;j<r;j++)for(let i=0;i<k;i++)if(masks[j]&(1<<i))add('MEM'+j+'_'+i,[-(2+j),2+r+i]);
 add('FINAL',Array.from({length:k},(_,i)=>-(2+r+i)));
 return {k,r,vars,masks,clauses,ids};
}
function resol(a,b,p){
 const ap=a.includes(p),an=a.includes(-p),bp=b.includes(p),bn=b.includes(-p);
 if(!((ap&&bn)||(an&&bp))||ap===an||bp===bn)throw Error('bad pivot');
 const o=norm([...a.filter(x=>Math.abs(x)!==p),...b.filter(x=>Math.abs(x)!==p)]);
 if(o.some(x=>o.includes(-x)))throw Error('tautology');
 return o;
}
function setCover(k,masks){
 const full=(1<<k)-1,r=masks.length;let best=r+1;
 for(let s=0;s<(1<<r);s++){let u=0;for(let j=0;j<r;j++)if(s&(1<<j))u|=masks[j];if(u===full)best=Math.min(best,pop(s));}
 return best<=r?best:null;
}
function bestAssignment(k,masks){
 let best=masks.length+1,selected=null,choices=Array(k).fill(-1);
 function go(i,used){
  if(i===k){const b=pop(used);if(b<best){best=b;selected=choices.slice();}return;}
  for(let j=0;j<masks.length;j++)if(masks[j]&(1<<i)){choices[i]=j;go(i+1,used|(1<<j));}
 }
 go(0,0);return selected?{tau:best,choices:selected}:null;
}
function produce(src,choices){
 const {k,r,ids,clauses}=src;
 const nodes=new Map(clauses.map(x=>[x.id,x.clause])),steps=[];
 function add(id,a,b,p){
   const clause=resol(nodes.get(a),nodes.get(b),p);nodes.set(id,clause);
   steps.push({id,parents:[a,b],pivot:p,clause});return id;
 }
 const used=[...new Set(choices)].sort((a,b)=>a-b);
 for(const j of used)add('T'+j,ids.A,ids['SET'+j],1);
 for(let i=0;i<k;i++){
   const j=choices[i];
   if(!(src.masks[j]&(1<<i)))throw Error('illegal membership');
   add('G'+i,'T'+j,ids['MEM'+j+'_'+i],2+j);
 }
 let current=ids.FINAL;
 for(let i=0;i<k;i++)current=add('R'+i,current,'G'+i,2+r+i);
 return {steps,terminal:current,choices};
}
function verify(src,proof){
 const clauses=new Map(src.clauses.map(x=>[x.id,x.clause]));
 const seen=new Set(clauses.keys());
 for(const node of proof.steps){
   if(seen.has(node.id)||!Array.isArray(node.parents)||node.parents.length!==2)throw Error('id/arity');
   const a=clauses.get(node.parents[0]),b=clauses.get(node.parents[1]);
   if(!a||!b)throw Error('dangling');
   const out=resol(a,b,node.pivot);
   if(!eq(out,node.clause))throw Error('output');
   seen.add(node.id);clauses.set(node.id,out);
 }
 if(proof.terminal!==proof.steps.at(-1)?.id||!eq(clauses.get(proof.terminal),[]))throw Error('no terminal');
 return proof.steps.length;
}
function bruteSAT(src){
 if(src.vars>12)throw Error('control bound');
 for(let a=0;a<(1<<src.vars);a++){
  if(src.clauses.every(x=>x.clause.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0))))return true;
 }
 return false;
}
function negativeTests(){
 const src=make(3,[3,6,5]),a=bestAssignment(3,src.masks),p=produce(src,a.choices);
 req(verify(src,p)===8,'canonical 8');req(bruteSAT(src)===false,'canonical unsat');
 const edits=[
   x=>{x.steps[0].pivot=2;},
   x=>{x.steps[0].clause=[99];},
   x=>{x.steps[1].parents[0]='FAKE';},
   x=>{x.steps.at(-1).clause=[-4];},
   x=>{x.terminal='G0';},
   x=>{x.steps[1].id=x.steps[0].id;},
   x=>{x.steps.at(-1).parents[0]='R'+(src.k-1);},
   x=>{x.steps.splice(-1,1);},
   x=>{x.steps[0].parents.reverse();x.steps[0].pivot=999;},
 ];
 let rejected=0;
 for(const edit of edits){
  const c=JSON.parse(JSON.stringify(p));edit(c);try{verify(src,c);}catch(e){rejected++;}
 }
 req(rejected===edits.length,'corruption rejection');
 const no=make(3,[1,2]);req(bruteSAT(no),'uncovered SAT');
 const yes=make(3,[1,2,4]);req(!bruteSAT(yes),'singleton cover UNSAT');
 return rejected;
}
function run(){
 let instances=0,covered=0,uncovered=0,proofs=0,models=0, maxGap=0;
 const examples=[];
 for(let k=1;k<=4;k++)for(let r=1;r<=4;r++){
  const base=(1<<k)-1,total=base**r;
  for(let index=0;index<total;index++){
   let x=index;const masks=[];
   for(let j=0;j<r;j++){masks.push(1+(x%base));x=Math.floor(x/base);}
   const tau=setCover(k,masks),assignment=bestAssignment(k,masks);
   req((tau===null)===(assignment===null),'cover vs plans');
   if(tau!==null)req(tau===assignment.tau,'optimal cover/assignment');
   instances++;
   const src=make(k,masks);
   if(index%257===0){req(bruteSAT(src)===(tau===null),'independent SAT label');models++;}
   if(tau===null){uncovered++;continue;}covered++;
   if(index%31===0||total<=12){
    const p=produce(src,assignment.choices),cost=verify(src,p);
    req(cost===2*k+tau,'paid count');
    proofs++;
    const naive=k+2*k;maxGap=Math.max(maxGap,naive-cost);
   }
   if(k===3&&r===3&&masks.join(',')==='3,6,5')examples.push({k,r,masks,tau,cost:2*k+tau});
  }
 }
 return {run:'LSPV1-470-LAYERED-RES-SETCOVER/v1',model:'restricted layered source-authenticated ordinary Resolution DAG plans',instances,covered,uncovered,checkedProofs:proofs,checkedSATModels:models,negativeControls:negativeTests(),maxIndependentMinusShared:maxGap,examples,assertions:checks,status:'PROVED/RESTRICTED exact symbolic reduction; finite checks; global R_mix341 min and B3 OPEN'};
}
const RAW=run();
if(typeof process!=='undefined'&&process.stdout)process.stdout.write(JSON.stringify(RAW,null,2)+'\n');