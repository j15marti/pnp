function threshold(z,chart,V,G,n,trace,E){
 const eligible=chart.map((f,i)=>f.cost.includes(2)?i:-1).filter(i=>i>=0),known=new Set(z.native.results.filter(x=>x.hybrid.status==="UNSAT").map(x=>x.owner));
 const C=z.C,owners=z.owners,learned=z.native.proof.map(x=>({c:x.c,mask:BigInt("0x"+x.mask)}));
 function run(hybrid){
 let events={build:0,filter:0,search:0,check:0,nodes:0,checkNodes:0,score:0},used=0,cap=2500000,results=[],witness=null,why=null;const tick=(k,n=1)=>{if(used+n>cap)throw Error("cap");used+=n;events[k]+=n};
 function close(F,A,reverse,field){A=new Map(A);for(;;){let change=false,S=new Map();for(let j=0;j<F.length;j++){let c=F[reverse?F.length-1-j:j],open=[],sat=false;for(let l of c){tick(field);if(!A.has(Math.abs(l)))open.push(l);else if(A.get(Math.abs(l))===Number(l>0)){sat=true;break}}if(sat)continue;if(!open.length)return null;if(open.length===1){let l=open[0];A.set(Math.abs(l),Number(l>0));change=true}else for(let l of open)S.set(Math.abs(l),(S.get(Math.abs(l))||0)+1)}if(!change)return {A,S}}}
 try{for(let i of eligible){if(hybrid&&known.has(i)){results.push({i,status:"IMPORTED_OWNER_MASK_NO"});continue}
 let F=[];for(let j=0;j<C.length;j++){tick("build");if(owners[j]!==i)F.push(C[j])}
 let f=chart[i];for(let w=0;w<f.cost.length;w++){tick("build");if(f.cost[w]>2)F.push(f.vs.map((v,k)=>((w>>k)&1)?-(v+1):v+1))}
 if(hybrid){let b=1n<<BigInt(i);for(let l of learned){tick("filter");if(!(l.mask&b))F.push(l.c)}}
 function dfs(A){tick("nodes");let q=close(F,A,false,"search");if(!q)return null;if(!q.S.size)return {sat:[...q.A]};let v=[...q.S].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let x=dfs([...q.A,[v,0]]);if(x?.sat)return x;let y=dfs([...q.A,[v,1]]);if(y?.sat)return y;return [v,x,y]}
 let tree=dfs([]);if(tree?.sat){let A=new Map(tree.sat),assignment=V.map(v=>[v,A.get(v+1)||0]),M=new Map(assignment),energy=0;for(let f of chart){tick("score");energy+=f.cost[f.vs.reduce((s,v,j)=>s|((M.get(v)||0)<<j),0)]}if(energy>2)throw Error("false witness");const a=E.lift(G,n,trace,{assignment,best:energy});witness={assignment,best:energy,defects:a.defects};results.push({i,status:"SAT",energy});break}
 function check(A,t){tick("checkNodes");let q=close(F,A,true,"check");if(!q)return;if(!Array.isArray(t))throw Error("bad leaf");let v=t[0];if(q.A.has(v))check([...q.A],t[1+q.A.get(v)]);else{check([...q.A,[v,0]],t[1]);check([...q.A,[v,1]],t[2])}}
 check([],tree);results.push({i,status:"UNSAT",tree});
 }}catch(e){if(String(e)!=="Error: cap")throw e;why="cap"}
 return {results,events,used,cap,why,witness,status:witness?"ENERGY_LE_2":results.length===eligible.length?"ENERGY_GE_4":"UNKNOWN"};
 }
 return {eligible,excluded:eligible.filter(i=>known.has(i)),base:run(false),hybrid:run(true)};
}
function peerReplay(C,proof){
 let rows=C.slice(),reads=0,cap=5000000,done=0;for(let c of proof){let A=new Set(c.map(l=>-l)),dead=false;for(;;){let ch=false;for(let row of rows){let k=0,u=0,s=false;for(let l of row){if(++reads>cap)return {status:"UNKNOWN_CAP",reads,done};if(A.has(l)){s=true;break}if(!A.has(-l)){k++;u=l}}if(s)continue;if(!k){dead=true;break}if(k===1){A.add(u);ch=true}}if(dead||!ch)break}if(!dead)throw Error("peer RUP invalid");rows.push(c);done++}return {status:proof.at(-1).length===0?"UNSAT":"VERIFIED",reads,done}}
if(typeof module!=="undefined")module.exports={threshold,peerReplay};
