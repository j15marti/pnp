
function thresholdChart(F,i,B){return F.map((f,j)=>({...f,cost:f.cost.map(x=>Number(x>(j===i?B:0)))}))}
function searchBudget(C,metrics,cap){
 function close(A){A=new Map(A);for(;;){let changed=false,score=new Map();for(let c of C){if(++metrics.scans>cap)throw Error("cap");let free=[],sat=false;for(let l of c){metrics.lits++;let v=A.get(Math.abs(l));if(v===undefined)free.push(l);else if(v===Number(l>0)){sat=true;break}}if(sat)continue;if(!free.length)return {dead:true};if(free.length===1){A.set(Math.abs(free[0]),Number(free[0]>0));changed=true}else for(let l of free)score.set(Math.abs(l),(score.get(Math.abs(l))||0)+1)}if(!changed)return {A,score}}}
 function visit(p){metrics.nodes++;let r=close(p);if(r.dead)return {tree:null};if(!r.score.size)return {witness:[...r.A].map(([v,b])=>[v-1,b])};let v=[...r.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let a=visit([...r.A,[v,0]]);if(a.witness)return a;let b=visit([...r.A,[v,1]]);if(b.witness)return b;return {tree:[v,a.tree,b.tree]}}
 return visit([]);
}
// Proof replay using exact support sets, not clause UP; stronger closure may avoid an already-dead subtree.
function checkBudget(F,t,M,cap){function close(A){A=new Map(A);for(;;){let change=false;for(let f of F){let good=[];for(let w=0;w<f.cost.length;w++){if(++M.rows>cap)throw Error("check cap");if(f.cost[w]===0&&f.vs.every((v,i)=>!A.has(v)||A.get(v)===((w>>i)&1)))good.push(w)}if(!good.length)return null;for(let [i,v] of f.vs.entries())if(!A.has(v)&&good.every(w=>((w>>i)&1)===((good[0]>>i)&1))){A.set(v,(good[0]>>i)&1);change=true}}if(!change)return A}}
 function visit(A,t){M.nodes++;let r=close(A);if(!r)return;if(t===null)throw Error("false threshold leaf");let v=t[0]-1;if(r.has(v))return visit(r,t[1+r.get(v)]);visit([...r,[v,0]],t[1]);visit([...r,[v,1]],t[2])}visit([],t)}
function threshold(F,asCNF,cap=2000000,checkCap=3000000){
 const m={scans:0,lits:0,nodes:0},c={rows:0,nodes:0},cases=[];
 const candidates=F.map((f,i)=>i).filter(i=>F[i].cost.includes(2));
 for(let i of candidates){let H=thresholdChart(F,i,2);try{let s=searchBudget(asCNF(H).clauses,m,cap);if(s.witness){let A=new Map(s.witness);let V=[...new Set(F.flatMap(f=>f.vs))];for(let v of V)if(!A.has(v))A.set(v,0);let best=F.reduce((z,f)=>z+f.cost[f.vs.reduce((w,v,i)=>w|(A.get(v)<<i),0)],0);if(best>2)throw Error("bad witness");return {status:"AT_MOST_2",cases,candidates,m,c,witness:{best,assignment:[...A]}}}checkBudget(H,s.tree,c,checkCap);cases.push({i,tree:s.tree})}catch(e){if(e.message==="cap"||e.message==="check cap")return {status:"UNKNOWN",cases,candidates,m,c,reason:e.message};throw e}}
 return {status:"NO_AT_MOST_2",cases,candidates,m,c}
}

if(typeof module!=="undefined")module.exports={threshold,checkBudget,thresholdChart};
