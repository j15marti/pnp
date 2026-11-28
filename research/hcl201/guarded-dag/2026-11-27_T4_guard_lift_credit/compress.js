function compression(data,lift){
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b), key=c=>canon(c).join(",");
function check(F,neg,stats,cap=10000000){let A=new Map(neg.map(l=>[Math.abs(l),l>0])),change=true;while(change){change=false;for(let C of F){let cnt=0,last=0,sat=false;for(let l of C){if(++stats.visits>cap)return null;let v=A.get(Math.abs(l));if(v===undefined){cnt++;last=l}else if(v===(l>0)){sat=true;break}}if(sat)continue;if(!cnt)return true;if(cnt===1){A.set(Math.abs(last),last>0);change=true}}}return false}
function* subs(C,k,start=0,P=[]){if(!k){yield P;return}for(let i=start;i<=C.length-k;i++)yield*subs(C,k-1,i+1,P.concat(C[i]))}
let reports=[];
for(const o of data.raw.out){const C=o.chart.clauses,trace=lift.report.find(t=>t.id===o.id).globalLifted;let modes=[];
for(const w of [2,4,6]){const start=Date.now(),F=C.slice(),S=new Set(F.map(key)),stat={visits:0},records=[],refused=[];let skipped=0,probes=0,terminal=false,capped=false;
for(const c of trace){if(S.has(key(c))){skipped++;continue}let got=null;
for(let j=0;j<=Math.min(w,c.length)&&got===null&&!capped;j++)for(let q of subs(c,j)){if(S.has(key(q)))continue;probes++;let ok=check(F,q.map(l=>-l),stat);if(ok===null){capped=true;break}if(ok){got=q;break}}
if(capped)break;if(got===null){refused.push(c);continue}F.push(got);S.add(key(got));records.push({parent:c,learned:got});let r=check(F,[],stat);if(r===null){capped=true;break}if(r){terminal=true;break}}
let independent={visits:0};const D=C.slice();for(let rec of records){if(check(D,rec.learned.map(l=>-l),independent)!==true)throw Error("replay");D.push(rec.learned)}if(terminal&&check(D,[],independent)!==true)throw Error("terminal replay");
modes.push({w,terminal,capped,records,refused,skipped,probes,visits:stat.visits,replay:independent.visits,peakRows:F.length,peakLits:F.reduce((s,c)=>s+c.length,0),ms:Date.now()-start})}reports.push({id:o.id,guard:o.guard_id,residual:o.residual_id,modes})}
return reports}
module.exports=compression;
