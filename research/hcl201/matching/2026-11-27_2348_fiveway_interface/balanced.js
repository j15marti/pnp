
function balanced(F){
 let V=sort(F.flatMap(f=>f.s)),n=V.length,need=Math.ceil(n/5),best=null,events=0;
 let inc=new Map(V.map(v=>[v,new Set(F.map((f,i)=>f.s.includes(v)?i:-1).filter(i=>i>=0))]));
 function evalSet(I){let q=new Set(I),L=F.filter(f=>f.s.some(v=>q.has(v))),R=F.filter(f=>f.s.every(v=>!q.has(v))),lv=sort(L.flatMap(f=>f.s)),rv=new Set(R.flatMap(f=>f.s)),b=lv.filter(v=>rv.has(v)),ls=lv.length-b.length,rs=rv.size-b.length;events+=F.length;return {L,R,b,ls,rs,I:[...I]}}
 const score=q=>[Math.max(0,need-q.ls)+Math.max(0,need-q.rs),q.b.length,-Math.min(q.ls,q.rs),Math.abs(q.L.length-q.R.length)];
 function better(a,b){if(!b)return true;let x=score(a),y=score(b);return x.some((v,i)=>v<y[i]&&x.slice(0,i).every((z,j)=>z===y[j]))}
 // Greedy growth tries every seed, evaluates each prefix; local swap improvement for feasible cut.
 for(let seed of V){let q=new Set([seed]);for(let k=1;k<=Math.floor(n/2);k++){let x=evalSet(q);if(x.ls>=need&&x.rs>=need&&better(x,best))best=x;if(k===Math.floor(n/2))break;let a=null;for(let v of V)if(!q.has(v)){let y=evalSet(new Set([...q,v]));if(better(y,a))a=y}q=new Set(a.I)}}
 if(best){for(let round=0;round<3;round++){let x=best;for(let v of best.I)for(let w of V)if(!best.I.includes(w)){let y=evalSet(best.I.filter(a=>a!==v).concat(w));if(y.ls>=need&&y.rs>=need&&better(y,x))x=y}if(x===best)break;best=x}}
 return best?{...best,need,events}: {need,events,b:null}
}
function decode(s){return s.map(([s,h,o])=>({s,m:BigInt("0x"+h),o}))}
function boundedResponses(L,R,B,eq,cap=1500000){
 let visits=0,checked=0,rows=[],H=0,A=0,M=0,C=0,D=0,unknown=0,first=null;
 if(B.length>12)return {status:"WIDTH-CAP",width:B.length,cap,rows:[]};
 let mapL=reindex(L),mapR=reindex(R),CL=clauses(mapL.F),CR=clauses(mapR.F),keys=new Map();
 // Fixed one proof-query per boundary state, cap shared over both regions, with independent replay.
 for(let w=0;w<2**B.length;w++){
  if(!allowed(eq,w)){A++;rows.push({w,status:"AFFINE"});continue}
  let pins=B.map((v,j)=>[v,(w>>j)&1]),l=pins.map(([v,b])=>[mapL.vars.indexOf(v)+1,b]),r=pins.map(([v,b])=>[mapR.vars.indexOf(v)+1,b]);
  let U={visits:0},ul=up(CL,l,U,cap-visits),ur=up(CR,r,U,cap-visits);visits+=U.visits;
  if(ul.status==="UNSAT"||ur.status==="UNSAT"){D++;rows.push({w,status:"UP",side:ul.status==="UNSAT"?"L":"R"});continue}
  if(visits>=cap){unknown++;break}
  let hL=hall(CL,l),hR=hall(CR,r);visits+=hL.W.visits+hR.W.visits;H+=hL.visits||0;H+=hR.visits||0;
  // No Hall exclusion consumed here unless independent UP confirms; matching candidates are leads.
  if(hL.status==="HALL-UNSAT"||hR.status==="HALL-UNSAT")M++;
  let x=solve(CL,l,Math.max(1,cap-visits),500);visits+=x.W.visits;if(x.s==="UNSAT"){let v=check(CL,x.t,l);checked+=v.visits;rows.push({w,status:"DAG",side:"L",tree:x.t});D++;continue}
  let y=solve(CR,r,Math.max(1,cap-visits),500);visits+=y.W.visits;if(y.s==="UNSAT"){let v=check(CR,y.t,r);checked+=v.visits;rows.push({w,status:"DAG",side:"R",tree:y.t});D++;continue}
  if(x.s==="SAT"&&y.s==="SAT"){first={w,x:x.a,y:y.a};rows.push({w,status:"SAT-REGIONS"});break}
  unknown++;rows.push({w,status:"UNKNOWN"});if(visits>=cap)break;
 }
 let status=first?"SAT-REGIONS":rows.length===2**B.length&&!unknown?"UNSAT-CANDIDATE":"UNKNOWN";
 return {status,width:B.length,cap,rows,visits,checked,affineExcluded:A,hallCandidates:M,hallEdgeVisits:H,dagExcluded:D,unknown,first}
}
function run2(compile,corpus,reg){
 let R=main(compile,corpus,reg);for(let x of R)for(let c of x.cases){if(!c.residual)continue;let F=decode(JSON.parse(c.residual)),Q=balanced(F);c.balanced={need:Q.need,events:Q.events,b:Q.b,ls:Q.ls,rs:Q.rs};if(Q.b){let a=projectedAffine(F,Q.b);c.balanced.affine=a;c.balanced.L=serial(Q.L);c.balanced.R=serial(Q.R);c.balanced.responses=boundedResponses(Q.L,Q.R,Q.b,a.eqs)}
 // Independently retain bounded small (nonbalanced) separator as a diagnostic; not universal contraction.
 let S=boundedResponses(decode(c.left),decode(c.right),c.boundary,c.affine.global.eqs,200000);c.smallResponses=S;
 let r=reindex(F),D=solve(clauses(r.F),[],1000000,10000);c.baseline={status:D.s,work:D.W,proof:D.t,verification:D.s==="UNSAT"?check(clauses(r.F),D.t):null};
 c.residualId="RESIDUAL-v1:sha256:"+sha(J(["PNP-RESIDUAL-v1",c.original.instance_id,"EMPTY","T1-EXACT-RESPONSE-v1",sha(c.residual),sha(J({vars:sort(F.flatMap(f=>f.s)),trace:c.reverseMap}))]));
 }return R
}

// Evaluate with pinned check.js and geometry-affine.js; call run2(compile,corpus,registry).
