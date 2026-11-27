function project(F,own,peer){
const eligible=F.map((f,i)=>f.cost.includes(2)?i:-1).filter(i=>i>=0),ownSets=own.map(l=>l.tree.core.filter(i=>eligible.includes(i))),peerSets=peer.map(l=>l.selected.filter(i=>eligible.includes(i)));
const all=new Set(),perOwn=own.map(()=>new Set()),cells=[],coords=[...new Set([...own.flatMap(l=>l.guard.map(p=>p[0])),...peer.flatMap(l=>l.ps.map(p=>p[0]))])].sort((a,b)=>a-b);
let rowChecks=0;
function can(f,M){for(let w=0;w<f.cost.length;w++){rowChecks++;if(f.cost[w]===2&&f.vs.every((v,i)=>!M.has(v)||M.get(v)===((w>>i)&1)))return true}return false}
for(let i=0;i<own.length;i++)for(let j=0;j<peer.length;j++){let M=new Map(own[i].guard),bad=false;for(let [v,x] of peer[j].ps){if(M.has(v)&&M.get(v)!==x)bad=true;M.set(v,x)}if(bad)continue;
let common=ownSets[i].filter(x=>peerSets[j].includes(x)),filtered=common.filter(x=>can(F[x],M));for(let x of filtered){perOwn[i].add(x);all.add(x)}cells.push({i,j,pins:[...M],before:common.length,after:filtered.length,candidates:filtered})}
let verifiedWords=0;for(let w=0;w<2**coords.length;w++){const good=p=>p.every(([v,x])=>((w>>coords.indexOf(v))&1)===x);let a=own.map(l=>good(l.guard)),b=peer.map(l=>good(l.ps));if(a.filter(Boolean).length!==1||b.filter(Boolean).length!==1)throw Error("not two partitions");let z=cells.filter(c=>good(c.pins));if(z.length!==1||!a[z[0].i]||!b[z[0].j])throw Error("joint partition");verifiedWords++}
return {allEligible:eligible.length,ownCandidateVisits:ownSets.reduce((s,a)=>s+a.length,0),ownUnique:[...new Set(ownSets.flat())].length,peerUnique:[...new Set(peerSets.flat())].length,refinedCandidateVisits:cells.reduce((s,c)=>s+c.before,0),refinedAfterRows:cells.reduce((s,c)=>s+c.after,0),projectedGuardCandidateVisits:perOwn.reduce((s,a)=>s+a.size,0),projectedGlobalCandidates:all.size,globalCandidates:[...all].sort((a,b)=>a-b),perOwn:perOwn.map(s=>[...s].sort((a,b)=>a-b)),cells,coords,verifiedWords,rowChecks}}
module.exports={project};
