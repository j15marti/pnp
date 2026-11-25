function run(q,delta=null,cap=1000000){
 const R=q.rowMap.length, M=q.ownerIDs.length, bits=Array.from({length:R},(_,i)=>1n<<BigInt(i)), own=q.rowMap.map(x=>x[0]), live=q.live.slice(), p=q.pairHex.map(x=>BigInt("0x"+x)), active=Array(M).fill(true), history=[], cnt={acScans:0,acChecks:0,acRows:0,hellyTests:0,triples:0,supportTests:0,fillTests:0,fillPairs:0,eliminations:0,caps:0}, failures=[];
 if(delta){for(const r of delta.removedRows)live[r]=false;for(const [r,h] of delta.delta)p[r]&=~BigInt("0x"+h)}
 const domains=()=>Array.from({length:M},(_,i)=>own.flatMap((j,r)=>j===i&&live[r]?[r]:[]));
 function mask(rs){return rs.reduce((s,r)=>s|bits[r],0n)}
 function ac(){let change=true;while(change){change=false;cnt.acScans++;const ds=domains(), ms=ds.map(mask);for(let i=0;i<M;i++)if(active[i]&&!ds[i].length)return false;for(let r=0;r<R;r++)if(live[r])for(let j=0;j<M;j++)if(active[j]&&j!==own[r]){cnt.acChecks++;if(!(p[r]&ms[j])){live[r]=false;cnt.acRows++;change=true;break}}}return true}
 function candidate(i,ds){
  cnt.hellyTests++;const d=ds[i], m=mask(d), ext=own.flatMap((j,r)=>live[r]&&j!==i?[r]:[]), sup=new Map(ext.map(r=>[r,p[r]&m])), fam=[...new Set(sup.values())];let start=cnt.supportTests;
  for(let a=0;a<d.length;a++)for(let b=a+1;b<d.length;b++)for(let c=b+1;c<d.length;c++){
   cnt.triples++;const x=bits[d[a]],y=bits[d[b]],z=bits[d[c]];let inter=m;
   for(const s of fam){if(++cnt.supportTests-start>cap){cnt.caps++;return {why:"cap",d:d.length,fam:fam.length}}if(((s&x)&&(s&y))||((s&x)&&(s&z))||((s&y)&&(s&z))){inter&=s;if(!inter)return {why:"nonHelly",triple:[d[a],d[b],d[c]],d:d.length,fam:fam.length}}}
  }
  return {sup,ext,d}
 }
 let ok=ac();
 while(ok){const ds=domains();let chosen=false;
  for(let i=0;i<M;i++)if(active[i]){
   const a=candidate(i,ds);
   if(!a.sup){failures.push({i,...a});continue}
   const {sup,ext,d}=a;
   for(let x=0;x<ext.length;x++)for(let y=x+1;y<ext.length;y++){const r=ext[x],s=ext[y];if(own[r]===own[s]||!(p[r]&bits[s]))continue;cnt.fillTests++;if(!(sup.get(r)&sup.get(s))){p[r]&=~bits[s];p[s]&=~bits[r];cnt.fillPairs++}}
   history.push({i,d:d.slice(),support:[...sup.entries()].map(([r,m])=>[r,m.toString(16)])});active[i]=false;for(const r of d)live[r]=false;cnt.eliminations++;chosen=true;ok=ac();break;
  }
  if(!chosen)break
 }
 function lift(rows){let out=rows.slice();for(const h of history.slice().reverse()){const support=new Map(h.support.map(([r,m])=>[r,BigInt("0x"+m)]));let m=mask(h.d);for(const r of out){if(!support.has(r))throw Error("bad lift");m&=support.get(r)}const t=h.d.find(r=>m&bits[r]);if(t===undefined)throw Error("no lift");out.push(t)}return out.sort((a,b)=>own[a]-own[b])}
 return {id:q.id,guard:q.guard,ok,status:!ok?"UNSAT":active.every(x=>!x)?"SAT":"OPEN",active,live,p,history,lift,cnt,failures,summary:{initial:q.live.filter(Boolean).length,final:live.filter(Boolean).length,active:active.filter(Boolean).length,eliminated:history.map(h=>q.ownerIDs[h.i])}}
}

function control(dom,compatible,id){let rowMap=dom.flatMap((n,i)=>Array.from({length:n},(_,j)=>[i,String(j)]));let p=rowMap.map(([i,a])=>rowMap.reduce((s,[j,b],r)=>i!==j&&compatible(i,+a,j,+b)?s|(1n<<BigInt(r)):s,0n).toString(16));return {id,guard:[],rowMap,ownerIDs:dom.map((_,i)=>i),live:rowMap.map(()=>true),pairHex:p}}

function enumModels(q,active=q.ownerIDs.map(()=>true),live=q.live,p=q.pairHex.map(x=>BigInt("0x"+x))){let out=[],own=q.rowMap.map(x=>x[0]),d=q.ownerIDs.map((_,i)=>own.flatMap((j,r)=>i===j&&active[i]&&live[r]?[r]:[]));function f(i,a){if(i===d.length){out.push(a);return}if(!active[i])return f(i+1,a);for(const r of d[i])if(a.every(s=>p[r]&(1n<<BigInt(s))))f(i+1,[...a,r])}f(0,[]);return out}

function check(q){let a=run(q),source=enumModels(q), projected=enumModels(q,a.active,a.live,a.p);let expected=new Set(source.map(m=>m.filter(r=>a.active[q.rowMap[r][0]]).join(","))), actual=new Set(projected.map(m=>m.join(",")));if(!a.ok){if(source.length)throw Error("false UNSAT "+q.id); }else{if(expected.size!==actual.size||[...expected].some(x=>!actual.has(x)))throw Error("projection "+q.id);for(const m of projected)if(!source.some(s=>s.join(",")===a.lift(m).join(",")))throw Error("lift "+q.id)}return {id:q.id,models:source.length,projected:projected.length,status:a.status,summary:a.summary,cnt:a.cnt}}

function experiments(){let controls=[];const cycle=[[0,1],[1,2],[2,3],[3,0]];for(const fixed of [false,true])controls.push(check(control([4,...cycle.map(()=>fixed?1:2)],(i,a,j,b)=>i===0?(b===1||cycle[j-1].includes(a)):j===0?(a===1||cycle[i-1].includes(b)):true,"non-tree-Helly-"+fixed)));
 let seed=713;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 for(let k=0;k<100;k++){const d=Array.from({length:5},()=>2+Math.floor(rand()*3)),edges=new Map();for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)for(let a=0;a<d[i];a++)for(let b=0;b<d[j];b++)edges.set([i,a,j,b].join(","),rand()>.25);controls.push(check(control(d,(i,a,j,b)=>i<j?edges.get([i,a,j,b].join(",")):edges.get([j,b,i,a].join(",")),"random-"+k)))}
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 for(const relaxed of [false,true]){const words=lines.map((_,i)=>[1,2,3,4,5,6,...(relaxed&&i===0?[0]:[])]);controls.push(check(control(words.map(x=>x.length),(i,a,j,b)=>lines[i].every((v,k)=>!lines[j].includes(v)||((words[i][a]>>k)&1)===((words[j][b]>>lines[j].indexOf(v))&1)),"Fano-"+relaxed)))}
 return controls}
if(require.main===module){const fs=require('fs');const paths=process.argv.slice(2);const controls=experiments();const jobs=[];if(paths.length){if(paths.length!==6)throw Error('usage: node checker.js pair0.json ... pair4.json MS24_results.json');const d=JSON.parse(fs.readFileSync(paths[5]));for(let i=0;i<5;i++){const q=JSON.parse(fs.readFileSync(paths[i]));for(const mode of [false,true]){const z=run(q,mode?d.jobs[i].combined:null,100000);jobs.push({id:q.id,guard:q.guard,mode,status:z.status,summary:z.summary,cnt:z.cnt,failures:z.failures,history:z.history,removedLive:q.live.flatMap((v,r)=>v&&!z.live[r]?[r]:[])})}}}console.log(JSON.stringify({controls,jobs}));}
module.exports={run,experiments};
