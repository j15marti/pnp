function propagate(q,delta,failures,combined){
 const R=q.rowMap.length,M=q.ownerIDs.length,own=q.rowMap.map(x=>x[0]),bits=Array.from({length:R},(_,i)=>1n<<BigInt(i)),live=q.live.slice(),p=q.pairHex.map(x=>BigInt("0x"+x));
 for(const r of delta.removedRows)live[r]=false;for(const [r,h] of delta.delta)p[r]&=~BigInt("0x"+h);
 const init=p.slice(),initial=live.slice(),nogoods=[],seen=new Set(),cnt={validated:0,probes:0,globalScans:0,conditionalScans:0,supportChecks:0,deletedRows:0,deletedPairs:0,localRows:0,acceptedBatches:0};
 const masks=ls=>{let m=Array(M).fill(0n);for(let r=0;r<R;r++)if(ls[r])m[own[r]]|=bits[r];return m};
 for(const f of failures)if(f.why==="emptyTriple"){let rs=[f.a,f.r,f.s].sort((a,b)=>a-b),k=rs.join(",");if(seen.has(k))continue;let m=masks(live)[f.i];if(rs.some(r=>!live[r]||own[r]===f.i)||new Set(rs.map(r=>own[r])).size!==3||rs.some((r,i)=>rs.slice(i+1).some(s=>!(p[r]&bits[s])))||rs.reduce((v,r)=>v&p[r],m)!==0n)throw Error("invalid triple");seen.add(k);nogoods.push({rows:rs,owner:f.i});cnt.validated++}
 const by=new Map();for(const t of nogoods)for(const a of t.rows){if(!by.has(a))by.set(a,[]);by.get(a).push(t.rows.filter(r=>r!==a))}
 function ac(ls,bad,cond){let change=true;while(change){change=false;cnt[cond?"conditionalScans":"globalScans"]++;const m=masks(ls);if(m.some(x=>!x))return false;for(let r=0;r<R;r++)if(ls[r])for(let j=0;j<M;j++)if(j!==own[r]){cnt.supportChecks++;if(!(p[r]&m[j]&~(bad?.get(r)||0n))){ls[r]=false;cnt[cond?"localRows":"deletedRows"]++;change=true;break}}}return true}
 let ok=ac(live,null,false);
 for(const a of [...by.keys()].sort((a,b)=>a-b)){if(!ok||!live[a])continue;cnt.probes++;const before=live.map((v,r)=>v&&(own[r]===own[a]?r===a:!!(p[a]&bits[r]))),ls=before.slice(),bad=new Map();if(combined)for(const [r,s] of by.get(a)){bad.set(r,(bad.get(r)||0n)|bits[s]);bad.set(s,(bad.get(s)||0n)|bits[r])}
  let good=ac(ls,bad,true),changed=false;if(!good){live[a]=false;cnt.deletedRows++;changed=true}else for(let r=0;r<R;r++)if(before[r]&&!ls[r]&&r!==a&&live[r]&&(p[a]&bits[r])){p[a]&=~bits[r];p[r]&=~bits[a];cnt.deletedPairs++;changed=true}
  if(changed){cnt.acceptedBatches++;ok=ac(live,null,false)}
 }
 return {id:q.id,guard:q.guard,mode:combined,status:ok?"OPEN":"UNSAT",nogoods,cnt,removedRows:initial.flatMap((v,r)=>v&&!live[r]?[r]:[]),delta:init.flatMap((v,r)=>v!==p[r]?[[r,(v&~p[r]).toString(16)]]:[])}
}
if(require.main===module){const fs=require('fs'),paths=process.argv.slice(2);if(paths.length!==7)throw Error('usage: node checker.js pair0.json ... pair4.json MS24_results.json BH18_pivot_results.json');const d=JSON.parse(fs.readFileSync(paths[5])),prev=JSON.parse(fs.readFileSync(paths[6])),jobs=[];for(let i=0;i<5;i++){let q=JSON.parse(fs.readFileSync(paths[i]));for(let m of [false,true])jobs.push(propagate(q,d.jobs[i].combined,prev.jobs[2*i+1].failures,m))}console.log(JSON.stringify({jobs}));}
module.exports={propagate};
