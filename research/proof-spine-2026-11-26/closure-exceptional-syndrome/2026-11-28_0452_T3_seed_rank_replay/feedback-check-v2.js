function verifyExperiment(E){
let n=0,scans=0,flips=0,proofSteps=0,tieChanges=0,criticalPairs=0;const ck=(v,m)=>{if(!v)throw Error(m)};
ck(!E.early.pins.length&&!E.early.conflict,"unexpected pins");
let k=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
function field(c,a){let u=c.filter(l=>a.get(Math.abs(l))===+(l>0));scans+=c.length;return{n:u.length,r:((u.reduce((s,l)=>s+(l>0?1:-1),0)%3)+3)%3}}
function score(rows,a){let b=0,t=0;for(let c of rows){let q=field(c,a);if(!q.n)b++;else if(!q.r)t++}return[b,t]}
for(let r of E.arms[0].firstRows){let c=E.base.find(x=>x.id===r.id).c;for(let b of [0,1]){let a=new Map(E.W.map(v=>[v,b])),f=field(c,a),g=b?r.allTrue:r.allFalse;ck(g.k===f.n&&g.km===f.n%3&&g.sm===f.r,"field")}}
function contradiction(C,g){let a=new Map(g.map(l=>[Math.abs(l),+(l>0)]));while(true){let u0=null;for(let c of C){scans+=c.length;if(c.some(l=>a.get(Math.abs(l))===+(l>0)))continue;let U=c.filter(l=>!a.has(Math.abs(l)));if(!U.length)return true;if(U.length===1){u0=U[0];break}}if(u0===null)return false;a.set(Math.abs(u0),+(u0>0))}}
function tree(C,g,t){if(t===0){ck(contradiction(C,g),"leaf");return}ck(Array.isArray(t)&&t.length===3&&!g.some(l=>Math.abs(l)===t[0]),"split");tree(C,g.concat(-t[0]),t[1]);tree(C,g.concat(t[0]),t[2])}
for(let arm of E.arms){let D=new Map(E.base.map(r=>[r.id,r.c]));for(let p of arm.learned){let [a,b]=p.parents.map(id=>D.get(id));ck(a&&b&&a.includes(p.pivot)&&b.includes(-p.pivot),"parent/pivot");let C=[...new Set(a.filter(l=>l!==p.pivot).concat(b.filter(l=>l!==-p.pivot)))];ck(!C.some(l=>C.includes(-l))&&k(C)===k(p.c)&&C.length<=arm.width,"resolution");D.set(p.id,p.c);proofSteps++}
if(arm.result.status==="NO")tree([...D.values()],[],arm.result.t);else throw Error("expected known test NO");
let phaseCounts=new Map();for(let p of arm.phases){let i=phaseCounts.get(p.round)||0;phaseCounts.set(p.round,i+1);let rows=E.base.map(r=>r.c).concat(arm.learned.slice(0,p.round*16).map(r=>r.c)),a=new Map(E.W.map(v=>[v,i===0?0:1]));let bad=score(rows,a)[0];for(let move of p.path){let best=0,plain=null,chosen=null,tie=Infinity;for(let v of E.W){a.set(v,1-a.get(v));let [u,t]=score(rows,a);a.set(v,1-a.get(v));let g=bad-u;if(g>best){best=g;plain=v;chosen=v;tie=t}else if(g===best&&g>0&&arm.mode==="residue"&&t<tie){chosen=v;tie=t}}ck(best>0&&chosen===move.v&&plain===move.plain&&best===move.gain,"flip policy");a.set(chosen,1-a.get(chosen));bad-=best;flips++;if(chosen!==plain)tieChanges++}
ck(bad===p.bad&&p.word.every(([v,b])=>a.get(v)===b),"phase word");ck(p.fields.length===rows.length,"phase field length");for(let j=0;j<rows.length;j++){let f=field(rows[j],a),g=p.fields[j];ck(g.k===f.n&&g.km===f.n%3&&g.sm===f.r,"final field") }if(p.stalled){for(let v of E.W){a.set(v,1-a.get(v));ck(score(rows,a)[0]>=bad,"not stalled");a.set(v,1-a.get(v))}}}
n++}
for(let p of (E.critical||[])){for(let c of p.candidates){let A=E.base.find(x=>x.id===c.parents[0]).c,B=E.base.find(x=>x.id===c.parents[1]).c;ck(A.includes(c.pivot)&&B.includes(-c.pivot)&&k(A.filter(l=>l!==c.pivot).concat(B.filter(l=>l!==-c.pivot)))===k(c.clause),"critical");criticalPairs++}}
return{arms:n,literalVisits:scans,flips,proofSteps,tieChanges,criticalCandidates:criticalPairs}}

const fs=require('node:fs');let r=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));for(let q of r.cases){console.log(JSON.stringify({id:q.e.short_id,native:verifyExperiment(q.native),direct:verifyExperiment(q.direct)}))}console.log(JSON.stringify(verifyExperiment(r.fano.experiment)));
