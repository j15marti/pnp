function pivotRun(q,delta=null,maxPivots=2,cap=100000){
 const R=q.rowMap.length,M=q.ownerIDs.length,own=q.rowMap.map(x=>x[0]),bits=Array.from({length:R},(_,i)=>1n<<BigInt(i)),live=q.live.slice(),p=q.pairHex.map(x=>BigInt("0x"+x)),active=Array(M).fill(true),history=[],failures=[],cnt={acScans:0,acChecks:0,acRows:0,pivots:0,fibers:0,pairTests:0,triples:0,supportTests:0,caps:0,eliminations:0};
 if(delta){for(const r of delta.removedRows)live[r]=false;for(const [r,h] of delta.delta)p[r]&=~BigInt("0x"+h)}
 const ds=()=>Array.from({length:M},(_,i)=>own.flatMap((j,r)=>j===i&&live[r]?[r]:[])),mask=d=>d.reduce((s,r)=>s|bits[r],0n);
 function ac(){let change=true;while(change){change=false;cnt.acScans++;let d=ds(),m=d.map(mask);for(let i=0;i<M;i++)if(active[i]&&!d[i].length)return false;for(let r=0;r<R;r++)if(live[r])for(let j=0;j<M;j++)if(active[j]&&j!==own[r]){cnt.acChecks++;if(!(p[r]&m[j])){live[r]=false;cnt.acRows++;change=true;break}}}return true}
 function test(i,j,d){
  cnt.pivots++;let start=cnt.pairTests+cnt.supportTests;const m=mask(d[i]),other=own.flatMap((k,r)=>live[r]&&k!==i&&k!==j?[r]:[]);
  const capped=()=>cnt.pairTests+cnt.supportTests-start>cap;
  for(const a of d[j]){
   cnt.fibers++;let da=d[i].filter(r=>p[a]&bits[r]),ma=mask(da),ext=other.filter(r=>p[a]&bits[r]),sup=ext.map(r=>p[r]&ma);
   if(!ma)return {why:"emptyPivot",a};
   for(let x=0;x<ext.length;x++){if(!sup[x])return {why:"emptyPair",a,r:ext[x]};for(let y=x+1;y<ext.length;y++){let r=ext[x],s=ext[y];if(own[r]===own[s]||!(p[r]&bits[s]))continue;cnt.pairTests++;if(capped()){cnt.caps++;return {why:"cap"}}if(!(sup[x]&sup[y]))return {why:"emptyTriple",a,r,s}}}
   const fam=[...new Set(sup)];
   for(let u=0;u<da.length;u++)for(let v=u+1;v<da.length;v++)for(let w=v+1;w<da.length;w++){
    cnt.triples++;const x=bits[da[u]],y=bits[da[v]],z=bits[da[w]];let inter=ma;
    for(const s of fam){cnt.supportTests++;if(capped()){cnt.caps++;return {why:"cap"}}if(((s&x)&&(s&y))||((s&x)&&(s&z))||((s&y)&&(s&z))){inter&=s;if(!inter)return {why:"nonHelly",a,triple:[da[u],da[v],da[w]]}}}
   }
  }
  return {yes:true}
 }
 let ok=ac();
 while(ok){const d=ds();let changed=false;
  for(let i=0;i<M;i++)if(active[i]){
   const ps=active.flatMap((a,j)=>a&&i!==j?[j]:[]).sort((a,b)=>d[a].length-d[b].length||a-b);
   if(!ps.length){history.push({i,d:d[i].slice(),sup:[]});active[i]=false;for(const r of d[i])live[r]=false;cnt.eliminations++;changed=true;break}
   for(const j of ps.slice(0,maxPivots)){let z=test(i,j,d);if(!z.yes){failures.push({i,j,...z});continue}
    const m=mask(d[i]),sup=own.flatMap((k,r)=>live[r]&&k!==i?[[r,(p[r]&m).toString(16)]]:[]);history.push({i,j,d:d[i].slice(),sup});active[i]=false;for(const r of d[i])live[r]=false;cnt.eliminations++;changed=true;ok=ac();break
   }if(changed)break;
  }if(!changed)break;
 }
 function lift(rows){let out=rows.slice();for(const h of history.slice().reverse()){let m=mask(h.d),s=new Map(h.sup.map(([r,x])=>[r,BigInt("0x"+x)]));for(const r of out){if(!s.has(r))throw Error("missing lift");m&=s.get(r)}let t=h.d.find(r=>m&bits[r]);if(t===undefined)throw Error("no lift");out.push(t)}return out.sort((a,b)=>own[a]-own[b])}
 return {status:!ok?"UNSAT":active.every(v=>!v)?"SAT":"OPEN",ok,active,live,p,history,failures,cnt,lift}
}

function control(dom,compatible,id){let rowMap=dom.flatMap((n,i)=>Array.from({length:n},(_,j)=>[i,String(j)]));return {id,guard:[],rowMap,ownerIDs:dom.map((_,i)=>i),live:rowMap.map(()=>true),pairHex:rowMap.map(([i,a])=>rowMap.reduce((s,[j,b],r)=>i!==j&&compatible(i,+a,j,+b)?s|(1n<<BigInt(r)):s,0n).toString(16))}}

function enumModels(q,active=q.ownerIDs.map(()=>true),live=q.live,p=q.pairHex.map(x=>BigInt("0x"+x))){let out=[],own=q.rowMap.map(x=>x[0]),d=q.ownerIDs.map((_,i)=>own.flatMap((j,r)=>i===j&&active[i]&&live[r]?[r]:[]));function f(i,a){if(i===d.length){out.push(a);return}if(!active[i])return f(i+1,a);for(const r of d[i])if(a.every(s=>p[r]&(1n<<BigInt(s))))f(i+1,[...a,r])}f(0,[]);return out}

function check(q){let a=pivotRun(q,null,99),s=enumModels(q),e=new Set(s.map(m=>m.filter(r=>a.active[q.rowMap[r][0]]).join(","))),p=enumModels(q,a.active,a.live,a.p);if(!a.ok){if(s.length)throw Error("false UNSAT")}else{if(e.size!==p.length||p.some(m=>!e.has(m.join(","))))throw Error("projection");for(const m of p)if(!s.some(z=>z.join(",")===a.lift(m).join(",")))throw Error("lift")}return {id:q.id,models:s.length,projected:p.length,status:a.status,cnt:a.cnt,first:a.history[0]&&{i:a.history[0].i,j:a.history[0].j}}}

function experiments(){let controls=[];const s=[[0,1],[1,2],[0,2]];for(const allow of [false,true])controls.push(check(control([3,2,2,2],(i,a,j,b)=>i===0?(b===1||s[j-1].includes(a)):j===0?(a===1||s[i-1].includes(b)):allow||!((i===1&&j===2||i===2&&j===1)&&a===0&&b===0),"pivot-cover-"+allow)));
 let seed=429;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};for(let k=0;k<100;k++){const d=Array.from({length:5},()=>2+Math.floor(rand()*3)),e=new Map();for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)for(let a=0;a<d[i];a++)for(let b=0;b<d[j];b++)e.set([i,a,j,b].join(","),rand()>.25);controls.push(check(control(d,(i,a,j,b)=>i<j?e.get([i,a,j,b].join(",")):e.get([j,b,i,a].join(",")),"random-"+k)))}return controls}
if(require.main===module){const fs=require('fs'),paths=process.argv.slice(2),controls=experiments(),jobs=[];if(paths.length){if(paths.length!==6)throw Error('usage: node checker.js pair0.json ... pair4.json MS24_results.json');const d=JSON.parse(fs.readFileSync(paths[5]));for(let i=0;i<5;i++){const q=JSON.parse(fs.readFileSync(paths[i]));for(const mode of [false,true]){const z=pivotRun(q,mode?d.jobs[i].combined:null);jobs.push({id:q.id,guard:q.guard,mode,status:z.status,final:z.live.filter(Boolean).length,cnt:z.cnt,history:z.history,failures:z.failures})}}}console.log(JSON.stringify({controls,jobs}));}
module.exports={pivotRun,experiments};
