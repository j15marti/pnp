const R=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));
function verify(r){
 let log=r.hybrid.log, live=new Map(); // final bucket tables: an eliminated output is consumed iff its eliminated boundary variable later enters a bucket
 let consumed=new Set();for(let i=0;i<log.length;i++){for(const [j,f] of live)if(f.s.includes(log[i].v)){consumed.add(j);live.delete(j)}live.set(i,log[i])}
 let fs=[...live.values()],ids=fs.flatMap(f=>f.ids);if(ids.length!==r.B||new Set(ids).size!==r.B)throw Error("not all B rows covered");
 if(fs.length!==r.hybrid.factors)throw Error("factor count");
 // All partial assignments which have no compatible zero row become nogoods (prime not required).
 let C=[],partialChecks=0,even=fs.every(f=>f.t.every(v=>v%2===0));
 for(const f of fs)for(let w=0;w<3**f.s.length;w++){let z=w,p=[];for(const v of f.s){let d=z%3;z=Math.floor(z/3);if(d<2)p.push([v,d])}let ok=false;for(let k=0;k<f.t.length;k++){partialChecks++;if(f.t[k]===0&&p.every(([v,d])=>((k>>f.s.indexOf(v))&1)===d)){ok=true;break}}if(!ok)C.push(p.map(([v,d])=>[v,1-d]))}
 let ins=0,nodes=0,leaves=0;
 function close(a){for(;;){let change=false;for(const c of C){let hit=false,u=[];for(const [v,d] of c){ins++;if(!a.has(v))u.push([v,d]);else if(a.get(v)===d){hit=true;break}}if(hit)continue;if(!u.length)return false;if(u.length===1){a.set(...u[0]);change=true}}if(!change)return true}}
 function go(t,a){nodes++;let ok=close(a);if(!ok){leaves++;return true}if(t[0]!=="split")return false;let v=t[1];if(a.has(v))return go(t[2+a.get(v)],a);let x=new Map(a),y=new Map(a);x.set(v,0);y.set(v,1);return go(t[2],x)&&go(t[3],y)}
 if(!go(r.hybrid.search.tree,new Map()))throw Error("tree replay failed");
 // exhaustive independent truth tables for private slack and split NAE with unequal positive weights
 let localChecks=0;for(let i=0;i<8;i++){let v=[0,1,2].map(j=>(i>>j)&1);let m=Math.min(...[0,1].map(b=>Number(v.reduce((x,y)=>x+y,b)!==2)));if(m!==Number(i===0||i===7))throw Error("slack");localChecks++}
 for(let i=0;i<16;i++)for(let p=1;p<=3;p++)for(let q=1;q<=3;q++){let [a,b,c,d]=[0,1,2,3].map(j=>(i>>j)&1),m=Math.min(...[0,1].map(z=>p*Number(a===b&&b===z)+q*Number((1-z)===c&&c===d)));if(m!==(i===0||i===15?Math.min(p,q):0))throw Error("split");localChecks++}
 return {id:r.id,finalFactors:fs.length,coveredOriginalB:ids.length,allEven:even,lowerBound:even?2:1,nogoods:C.length,partialChecks,treeNodes:nodes,conflictLeaves:leaves,literalInspections:ins,localChecks};
}
console.log(JSON.stringify(R.map(verify),null,2));
