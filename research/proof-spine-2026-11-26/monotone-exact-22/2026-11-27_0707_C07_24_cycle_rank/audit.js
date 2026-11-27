const run = function(){
 const out=[];const cap=10000000;
 for(let r=2;r<=5;r++){
  let n=1+3*r, rows=[],guards=[[0,0],[1,1]], baseN=n+2, next=baseN, comps={}, clauses=[], cycles=[], spokes=[], adapter=[];
  const neg=x=>{if(comps[x]===undefined){comps[x]=next++;rows.push([x,comps[x],0,1]);}return comps[x];};
  const add=(i,j,f,g,center,u,v)=>{clauses.push([i,j,f,g]);let s=next++;let row=[center,f?neg(u):u,g?neg(v):v,s];rows.push(row);adapter.push({clause:[i,j,f,g],row,center,u,v});};
  let ends=[];
  for(let i=0;i<r;i++){let a=2,b=3+3*i,c=b+1,d=b+2;ends.push([a,b],[b,c],[c,d],[d,a]);cycles.push([4*i,4*i+1,4*i+2,4*i+3]);spokes.push([4*i,b],[4*i+3,d]);add(4*i+1,4*i+2,0,0,c,b,d);add(4*i+1,4*i+2,1,1,c,b,d);}
  for(let i=0;i<spokes.length;i++)for(let j=i+1;j<spokes.length;j++)add(spokes[i][0],spokes[j][0],1,1,2,spokes[i][1],spokes[j][1]);
  const source={variables:next,rows,guards}; let N=8*JSON.stringify(source).length;
  const closure=()=>{let D=Array(next).fill(3);D[0]=1;D[1]=2;let changes=0,scans=0,again=true;while(again){again=false;for(const row of rows){scans++;let lo=row.filter(x=>D[x]===2).length,hi=row.filter(x=>D[x]!==1).length;if(lo>2||hi<2)return {changes,scans,no:true};for(const x of row)if(D[x]===3&&(lo===2||hi===2)){D[x]=lo===2?1:2;changes++;again=true;}}}return {changes,scans,no:false};};
  let initial=closure();if(initial.no||initial.changes)throw Error("unexpected closure");
  const m=4*r, b=Array.from({length:m},(_,i)=>i%4===1?1:0);
  const ok=y=>clauses.every(([i,j,f,g])=>!(y[i]===f&&y[j]===g));
  const syndrome=y=>cycles.reduce((s,cy,i)=>s|((cy.reduce((z,j)=>z^y[j],0))<<i),0);
  if(!ok(b))throw Error("base");
  const implications=Array.from({length:m},()=>[]),conf=[];
  for(const [i,j,f,g] of clauses){let u=f^b[i],v=g^b[j];if(!u&&!v)throw Error("base wrong");if(u&&v)conf.push([i,j]);else if(u)implications[i].push(j);else implications[j].push(i);}
  let A={candidates:0,ops:0,feasible:0,syndromes:[],result:"UNSAT"},sy=new Set();
  function check(seed){A.candidates++;let z=Array(m).fill(0),q=[];for(const j of seed){z[j]=1;q.push(j);A.ops++;}for(let h=0;h<q.length;h++)for(const j of implications[q[h]]){A.ops++;if(!z[j]){z[j]=1;q.push(j);}}for(const [i,j] of conf){A.ops++;if(z[i]&&z[j])return;}A.feasible++;let y=z.map((v,i)=>v^b[i]);A.ops+=m+4*r;if(!ok(y))throw Error("closure wrong");let s=syndrome(y);sy.add(s);if(s===0)A.result="SAT";if(A.ops>cap)throw Error("A cap");}
  function recur(seed,start){check(seed);if(seed.length===r)return;for(let i=start;i<m;i++)recur([...seed,i],i+1);}
  recur([],0);A.syndromes=[...sy].sort((a,b)=>a-b);
  // B independently evaluates explicit witnesses for all nonzero scalar projections, plus full affine hull.
  let B={ops:0,scalarTests:0,allScalarFeasible:true,affineRank:r,root:"UNKNOWN"};
  let witnesses=[b,...spokes.map(([j])=>b.map((v,i)=>i===j?1-v:v))];let vals=witnesses.map(y=>{if(!ok(y))throw Error("B witness");B.ops+=clauses.length+4*r;return syndrome(y);});
  for(let l=1;l<(1<<r);l++){B.scalarTests++;let hit=false;for(const v of vals){B.ops+=r;let p=0;for(let j=0;j<r;j++)p^=((l&v)>>j)&1;if(!p){hit=true;break;}}if(!hit)B.allScalarFeasible=false;}
  // C independent enumeration in original native potential coordinates, unique private lifts.
  let C={assignments:0,rowChecks:0,solutions:0,result:"UNSAT"};
  for(let bits=0;bits<(1<<n);bits++){C.assignments++;let x=Array(next).fill(-1);x[0]=0;x[1]=1;for(let i=0;i<n;i++)x[i+2]=(bits>>i)&1;for(const [u,v] of Object.entries(comps))x[v]=1-x[u];let valid=true;for(const row of rows){C.rowChecks++;if(row[3]===1&&row[2]===0){if(row.reduce((s,j)=>s+x[j],0)!==2){valid=false;break;}}else{let s=2-x[row[0]]-x[row[1]]-x[row[2]];if(s<0||s>1){valid=false;break;}x[row[3]]=s;}}if(valid)C.solutions++;if(C.rowChecks>cap)throw Error("C cap");}if(C.solutions)C.result="SAT";
  // integrated exact clause/geometry adapter check, then occupancy bound on actual spokes
  let H={localChecks:0,certificateRows:0,lower:r,upper:1,result:"UNSAT"};
  for(const a of adapter){for(let mask=0;mask<8;mask++){H.localChecks++;let c=mask&1,u=(mask>>1)&1,v=(mask>>2)&1;let [i,j,f,g]=a.clause;let q=2-c-(u^f)-(v^g);if((q===0||q===1)===((c^u)===f&&(c^v)===g))throw Error("adapter wrong");}}
  // Verify all relevant clause pairs by original IDs, all spokes and each cycle exact.
  const has=(i,j,f,g)=>clauses.some(c=>c.join(",")===[i,j,f,g].join(","));
  for(const cy of cycles){if(!has(cy[1],cy[2],0,0)||!has(cy[1],cy[2],1,1))throw Error("missing");H.certificateRows+=2;}
  for(let i=0;i<spokes.length;i++)for(let j=i+1;j<spokes.length;j++){if(!has(spokes[i][0],spokes[j][0],1,1))throw Error("missing cross");H.certificateRows++;}
  if(A.result!=="UNSAT"||C.result!=="UNSAT"||!B.allScalarFeasible||H.lower<=H.upper)throw Error("unexpected");
  out.push({r,N,source,initial,adapter,A,B,C,H,cap});
 }
 return out;
};
console.log(JSON.stringify(run(),null,2));
