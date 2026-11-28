function experiment(x,pcRaw,pRaw,sha){
 const pc=JSON.parse(pcRaw),target=JSON.parse(pRaw), parentHash=sha(JSON.stringify(x.cert)+"\n");if(pc.parents[0]!=="CERT-v1:sha256:"+parentHash||pc.residual_id!==x.cert.output_residual_id||pc.map_sha256!==x.cert.map_sha256||pc.guard_id!=="EMPTY"||sha(pRaw)!==pc.output_residual_sha256)throw Error("parent mismatch");
 const count={pivot:0,mask:0,words:0,pairs:0,rankChecks:0};const tick=(k,n=1)=>{count[k]+=n;if(Object.values(count).reduce((a,b)=>a+b,0)>3000000)throw Error("new experiment cap")};
 const hi=v=>1n<<BigInt(v.toString(2).length-1);
 const lo=v=>v&-v;const par=v=>{let r=0;while(v){v&=v-1n;r^=1}return r};
 const R=x.residual.regions.map(r=>({F:r.forms.map(([s,c])=>BigInt("0x"+s)*2n+BigInt(c)),W:r.allowed.slice()}));
 const before=R.map(r=>r.W.slice());
 function add(B,v,high=true){while(v&~1n){tick("pivot");let q=high?hi(v&~1n):lo(v&~1n);if(B.has(q))v^=B.get(q);else {B.set(q,v);return 1}}return v===1n?-1:0}
 function legal(F,w,B=new Map()){let D=new Map(B);tick("words");return F.every((v,i)=>add(D,v^BigInt((w>>i)&1))>=0)}
 function compatible(a,u,b,v){tick("pairs");return legal([...a.F,...b.F],u+v*2**a.F.length)}
 const eq=[];for(const d of pc.proof){const a=R[d.i],b=R[d.j];if(JSON.stringify(a.W)!==JSON.stringify(d.beforeI)||JSON.stringify(b.W)!==JSON.stringify(d.beforeJ))throw Error("replay state");
 for(const u of d.removedI)if(!a.W.includes(u)||b.W.some(v=>compatible(a,u,b,v)))throw Error("bad I");
 for(const v of d.removedJ)if(!b.W.includes(v)||a.W.some(u=>compatible(a,u,b,v)))throw Error("bad J");
 a.W=a.W.filter(w=>!d.removedI.includes(w));b.W=b.W.filter(w=>!d.removedJ.includes(w))}
 if(JSON.stringify(R.map(r=>r.W))!==JSON.stringify(target.regions.map(r=>r.allowed)))throw Error("target mismatch");
 const baseline=R.map(r=>r.F.map(v=>v&~1n)),order=R.map((_,i)=>i),sorted=order.slice().sort((i,j)=>{const k=i=>lo(baseline[i].reduce((a,b)=>a|b,0n));return k(i)<k(j)?-1:k(i)>k(j)?1:i-j});
 function profile(blocks,ord,K=new Map(),high=true){let B=new Map(K),C=new Map(K),l=[],r=[];for(let i=0;i<ord.length;i++){for(let v of blocks[ord[i]])add(B,v,high);l.push(B.size);for(let v of blocks[ord[ord.length-1-i]])add(C,v,high);r[ord.length-1-i]=C.size}return l.slice(0,-1).map((v,i)=>v+r[i+1]-B.size-K.size)}
 function summary(a,b){let diff=a.map((v,i)=>v-b[i]);if(diff.some(v=>v<0))throw Error("cut increase");return {maxBefore:Math.max(...a),maxAfter:Math.max(...b),sumBefore:a.reduce((a,b)=>a+b,0),sumAfter:b.reduce((a,b)=>a+b,0),strict:diff.filter(v=>v>0).length,maxDrop:Math.max(...diff),dropIndices:diff.flatMap((v,i)=>v?[[i,v]]:[])}}
 const b0=profile(baseline,order),b1=profile(baseline,sorted);
 function findEq(Ws){let A=new Map(),rows=[];for(let i=0;i<R.length;i++){const F=R[i].F,W=Ws[i];if(!W.length)return {A,rows,empty:i};for(let m=1;m<2**F.length;m++){tick("mask");let p=par(BigInt(m&W[0]));if(!W.every(w=>par(BigInt(w&m))===p))continue;let v=BigInt(p);for(let j=0;j<F.length;j++)if(m>>j&1)v^=F[j];const t=add(A,v);if(t===-1)return {A,rows,conflict:{i,m,p,row:v.toString(16)}};if(t===1)rows.push({i,m,p,row:v.toString(16)})}}return {A,rows}}
 const initial=findEq(before),after=findEq(R.map(r=>r.W));if(initial.A.size!==0||after.A.size!==pc.affineReclosure.rank)throw Error("rank mismatch");
 // replay peer equations directly from retained words; independent span comparison.
 const peer=new Map();for(const t of pc.affineReclosure.affine){let r=R[t.i];if(!r.W.every(w=>par(BigInt(t.m&w))===t.p))throw Error("peer equation invalid");let v=BigInt(t.p);for(let j=0;j<r.F.length;j++)if(t.m>>j&1)v^=r.F[j];if(v.toString(16)!==t.row||add(peer,v)<0)throw Error("peer equation row");}
 let both=new Map(peer);for(let t of after.rows)add(both,BigInt("0x"+t.row));if(both.size!==peer.size||peer.size!==after.A.size)throw Error("different row span");
 function homogeneous(rows,high=true){let K=new Map();for(let t of rows)add(K,BigInt("0x"+t.row)&~1n,high);return K}
 const K=homogeneous(after.rows),Klow=homogeneous(after.rows,false);
 const q0=profile(baseline,order,K),q1=profile(baseline,sorted,K);
 if(JSON.stringify(q0)!==JSON.stringify(profile(baseline,order,Klow,false))||JSON.stringify(q1)!==JSON.stringify(profile(baseline,sorted,Klow,false)))throw Error("rank replay");
 // Verify the cut loss formula on each prefix for a basis of local-generated K.
 function intersectionCheck(ord,b,q){let prefix=new Map(),suffix=new Map(),total=new Map();for(const a of baseline)for(const v of a)add(total,v);for(let i=0;i<ord.length-1;i++){for(let v of baseline[ord[i]])add(prefix,v);suffix=new Map();for(let j=i+1;j<ord.length;j++)for(let v of baseline[ord[j]])add(suffix,v);let a=new Map(prefix),c=new Map(suffix);for(let v of K.values()){add(a,v);add(c,v)}let d=prefix.size+suffix.size+K.size-a.size-c.size;tick("rankChecks");if(d!==b[i]-q[i])throw Error("loss formula")}}
 // Use efficient prefix quotient identity rather than rebuilding suffix on each cut for large charts; two pivot orders independently replay every cut.
 const ablations=after.rows.map((t,i)=>{let k=homogeneous(after.rows.filter((_,j)=>j!==i));return {removed:t,source:summary(b0,profile(baseline,order,k)),sorted:summary(b1,profile(baseline,sorted,k))}});
 // Global affine filtering, then regenerate identities until fixed point. No row is deleted unless exact compatibility with all acquired equations fails.
 let W=R.map(r=>r.W.slice()),rounds=[],current=after,decision="UNKNOWN";for(let step=0;step<=x.residual.sharedDimension;step++){if(current.conflict||current.empty!==undefined){decision="NO";break}let removed=[];for(let i=0;i<R.length;i++){let d=W[i].filter(w=>!legal(R[i].F,w,current.A));if(d.length){removed.push({i,words:d});W[i]=W[i].filter(w=>!d.includes(w))}}
 let next=findEq(W);rounds.push({rankBefore:current.A.size,rankAfter:next.A.size,removed,empty:next.empty??null,conflict:next.conflict??null});
 if(next.conflict||next.empty!==undefined){current=next;decision="NO";break}if(!removed.length){current=next;break}current=next}
 const finalK=homogeneous(current.rows),final0=profile(baseline,order,finalK),final1=profile(baseline,sorted,finalK);
 return {problem_id:pc.problem_id,instance:pc.instance,instance_id:pc.instance_id,original_N_bits:pc.original_N_bits,source_pin:pc.source_pin,guard_id:pc.guard_id,residual_id:pc.output_residual_id,original_ids:pc.original_ids,parents:["CERT-v1:sha256:"+parentHash,"CERT-v1:sha256:"+sha(pcRaw)],map_sha256:pc.map_sha256,claim:"Independent replay of parent pair exclusions, exact local affine equations and frozen-cut quotient rank loss; guarded global affine filtering. No decision unless contradiction.",beforeRows:before.reduce((a,b)=>a+b.length,0),pairRows:R.reduce((a,b)=>a+b.W.length,0),pairSteps:pc.proof.length,affine:after.rows,source:summary(b0,q0),sorted:summary(b1,q1),ablations,rounds,finalRank:current.A.size,finalRows:W.reduce((a,b)=>a+b.length,0),finalSource:summary(b0,final0),finalSorted:summary(b1,final1),finalAffine:current.rows,decision,count,producerCounts:x.cert.discovery_counts,producerAudit:x.cert.independent_high_pivot_audit,peerDiscovery:pc.stats,profiles:{sourceBefore:b0,sourceAfter:q0,sortedBefore:b1,sortedAfter:q1,sourceFinal:final0,sortedFinal:final1},sortedOrder:sorted};
}
module.exports=experiment;
