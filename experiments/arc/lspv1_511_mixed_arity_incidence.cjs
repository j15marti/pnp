'use strict';
// LSPV-1/511 independent finite verifier. Signed original-source controls.
// Not an execution of the historical R_mix341 checker.
const S=[[1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
 [2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
 [1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
 [4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]];
const Q=[[-1,-3,7],[1,-7],[3,-7]];
const R=[['S13','S02',4],['S10','S07',5],['R01','R02',2],
 ['S11','S05',-5],['S03','S14',4],['R04','R05',2],['R03','R06',-6],
 ['S09','S08',-5],['R08','S12',-6],['S00','S01',2],['R09','R10',4],
 ['S02','S12',-4],['S06','S11',5],['R12','R13',2],['S03','S15',4],
 ['S04','S10',-5],['R15','R16',-2],['R14','R17',6],['R18','R11',-1]];
let checks=0;
function check(c,msg){checks++;if(!c)throw new Error(msg)}
function sat(c,a){return c.some(v=>Boolean((a>>(Math.abs(v)-1))&1)===(v>0))}
function same(a,b){return a.length===b.length&&a.every(v=>b.includes(v))}
function resolution(a,b,p){if(!a.includes(p)||!b.includes(-p)){let t=a;a=b;b=t}
 check(a.includes(p)&&b.includes(-p),'bad pivot');
 let out=[...new Set([...a.filter(v=>v!==p),...b.filter(v=>v!==-p)])];
 check(out.every(v=>!out.includes(-v)),'tautological resolvent');return out}
function audit(n,rows,goals){
 let graph=new Map();for(let i=0;i<n;i++)graph.set('S'+i,[]);
 for(let [name,parents] of rows){check(!graph.has(name),'duplicate label');
  check(new Set(parents).size===parents.length,'duplicated parent');
  check(parents.every(p=>graph.has(p)),'missing/forward parent');graph.set(name,parents)}
 check(goals.every(g=>graph.has(g)),'missing goal');
 let used=new Set(goals),todo=[...goals];
 while(todo.length){let u=todo.pop();for(let p of graph.get(u)){
  if(!used.has(p)){used.add(p);todo.push(p)}}}
 let sources=[...used].filter(v=>v[0]==='S'),paid=[...used].filter(v=>v[0]!=='S');
 let edges=paid.reduce((s,v)=>s+graph.get(v).length,0),
     adj=new Map([...used].map(u=>[u,new Set()]));
 for(let v of paid)for(let p of graph.get(v)){adj.get(v).add(p);adj.get(p).add(v)}
 let left=new Set(used),parts=0;
 while(left.size){parts++;let u=left.values().next().value;left.delete(u);
  let stack=[u];while(stack.length){let v=stack.pop();
   for(let z of adj.get(v))if(left.delete(z))stack.push(z)}}
 let mu=edges-used.size+parts,
     excess=paid.reduce((s,v)=>s+graph.get(v).length-1,0);
 check(mu>=0&&excess===sources.length-parts+mu,'general incidence equality failed');
 return {m:sources.length,q:paid.length,e:edges,c:parts,mu,excess};
}
let deleted=[];
for(let i=0;i<S.length;i++){
 let w=-1;for(let a=0;a<128;a++)
  if(S.every((c,j)=>j===i||sat(c,a))&&!Q.every(g=>sat(g,a))){w=a;break}
 check(w>=0&&!sat(S[i],w),'deletion necessity witness wrong');deleted.push(w)
}
const clauses=new Map(S.map((s,i)=>['S'+String(i).padStart(2,'0'),s]));
let rows=[];
for(let j=0;j<R.length;j++){
 let [a,b,p]=R[j];check(clauses.has(a)&&clauses.has(b),'bad reference');
 clauses.set('R'+String(j+1).padStart(2,'0'),resolution(clauses.get(a),clauses.get(b),p));
 let tr=x=>x[0]==='S'?'S'+Number(x.slice(1)):'I'+(Number(x.slice(1))-1);
 rows.push(['I'+j,[tr(a),tr(b)]])
}
check(same(clauses.get('R07'),Q[0])&&same(clauses.get('R11'),Q[1])&&
      same(clauses.get('R19'),Q[2]),'19-proof terminal mismatch');
let observed=audit(16,rows,['I6','I10','I18']);
check(observed.q===19&&observed.mu===4&&observed.m===16,'19-proof mismatch');
let q=Array.from({length:17},(_,i)=>'S'+i),tri=[];
for(let i=0;i<8;i++){
 let parents=q.splice(0,3),tag='I'+i;tri.push([tag,parents]);q.push(tag)}
let tree=audit(17,tri,q);
check(tree.m===17&&tree.q===8&&tree.mu===0&&tree.excess===16,'ternary tree mismatch');
let rejects=0;
for(let [r,g] of [
 [[['I0',['S0','S0']]],['I0']],
 [[['I0',['I1','S0']]],['I0']],
 [[['I0',['S0','S1']]],['I1']]
]){try{audit(2,r,g)}catch(e){rejects++}}
check(rejects===3,'adversarial graph accepted');
const out={status:'PROVED_RESTRICTED_THEOREM_COMPUTATIONAL_CONTROLS',
 source_deletion_witnesses:deleted,legal_resolution:observed,
 sharp_ternary:tree,corrupt_rejected:rejects,checks,
 notes:'independent JS; 19-resolution replay and 16-clause deletion controls; historical R_mix341 not executed'};
console.log(JSON.stringify(out,null,2));
