module.exports={audit:function audit(g,cert,api){
 const b=api.norm(g),canon=api.canon,key=api.key;
 if(b.gauge!==cert.gauge)throw Error("gauge");let F=[],seen=new Set(),initialWords=0;
 for(let v=0;v<g.types.length;v++)if(g.types[v]==="B"){let ps=[0,1,2,3].map(j=>4*v+j),vs=canon(ps.map(p=>b.root[p])),ok=[];for(let w=0;w<2**vs.length;w++){initialWords++;if(ps.reduce((a,p)=>a+(((w>>vs.indexOf(b.root[p]))&1)^b.sign[p]),0)===2)ok.push(w)}let k=JSON.stringify([vs,ok]);if(!seen.has(k)){seen.add(k);F.push({vs,ok})}}
 F.push({vs:[cert.gauge],ok:[0]});let checks=0,pins=0,elims=0;
 for(let [kind,v,val] of cert.trace){let bucket=F.filter(f=>f.vs.includes(v));if(!bucket.length)throw Error("empty bucket");if(kind==="pin"){pins++;if(!bucket.some(f=>f.ok.length&&f.ok.every(w=>{checks++;return ((w>>f.vs.indexOf(v))&1)===val})))throw Error("unsupported pin");F=F.map(f=>{let j=f.vs.indexOf(v);if(j<0)return f;let ok=[];for(let w of f.ok){checks++;if(((w>>j)&1)===val)ok.push((w&((1<<j)-1))|((w>>(j+1))<<j))}return {vs:f.vs.filter(x=>x!==v),ok}}).filter(f=>f.ok.length!==2**f.vs.length)}
 else if(kind==="elim"){elims++;let vs=canon(bucket.flatMap(f=>f.vs).filter(x=>x!==v));if(vs.length>11)throw Error("cap");let ok=[];for(let w=0;w<2**vs.length;w++){for(let a of [0,1]){let hit=true;for(let f of bucket){checks++;let t=f.vs.reduce((s,x,i)=>s|((x===v?a:(w>>vs.indexOf(x))&1)<<i),0);if(!f.ok.includes(t)){hit=false;break}}if(hit){ok.push(w);break}}}F=F.filter(f=>!f.vs.includes(v));if(ok.length!==2**vs.length)F.push({vs,ok})}
 else throw Error("kind")}
 // Match semantic support rather than trusting the imported factor IDs/order.
 let rowChecks=0,factorTests=0;for(let z of cert.base){if(z.f<0)throw Error("unexpected import");if(!F.some(f=>{factorTests++;return z.c.every(l=>f.vs.includes(Math.abs(l)))&&f.ok.every(w=>{rowChecks++;return z.c.some(l=>((w>>f.vs.indexOf(Math.abs(l)))&1)===Number(l>0))})}))throw Error("base entailment")}
 const D=cert.standalone.D;let baseNodes=0,resNodes=0,localWords=0,depth=[],maxWidth=0;
 for(let i=0;i<D.length;i++){let {c,p}=D[i];maxWidth=Math.max(maxWidth,c.length);if(p[0]==="base"){if(key(c)!==key(cert.base[p[1]].c))throw Error("base");baseNodes++;depth[i]=1}
 else {let [,a,b,l]=p;if(a>=i||b>=i||!D[a].c.includes(l)||!D[b].c.includes(-l))throw Error("pivot");let r=canon([...D[a].c.filter(x=>x!==l),...D[b].c.filter(x=>x!==-l)]);if(key(r)!==key(c))throw Error("resolvent");resNodes++;depth[i]=1+Math.max(depth[a],depth[b]);let vs=canon([...D[a].c,...D[b].c].map(Math.abs));let h=(c,w)=>Number(c.every(l=>((w>>vs.indexOf(Math.abs(l)))&1)===Number(l<0)));for(let w=0;w<2**vs.length;w++){localWords++;let t=h(c,w);if(t!==(t*h(D[a].c,w)^t*h(D[b].c,w)))throw Error("local syzygy")}}}
 if(D.at(-1).c.length!==0)throw Error("no empty");
 // Independent sample evaluates first-failure partition; correctness is symbolic local identity.
 let state=271828182,random=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state>>>31},vs=canon(D.flatMap(d=>d.c.map(Math.abs))),sampleWords=512;
 for(let w=0;w<sampleWords;w++){let A=new Map(vs.map(v=>[v,random()])),first=D.findIndex(d=>d.c.every(l=>A.get(Math.abs(l))===Number(l<0)));if(first<0||D[first].p[0]!=="base")throw Error("first failure")}
 return {initialWords,checks,pins,elims,remainingFactors:F.length,rowChecks,factorTests,baseNodes,resNodes,localWords,dagDepth:depth.at(-1),maxWidth,sampleWords,firstFailureCircuit:{nodes:D.length,independentPrefixProductGateUpperBound:D.length*(D.length-1)/2,balancedPrefixDepth:Math.ceil(Math.log2(D.length)),indicatorDepth:Math.ceil(Math.log2(maxWidth)),baseSumDepth:Math.ceil(Math.log2(baseNodes))}};
},mfcAudit:function mfcAudit(){
 const orig=[[15n,32n],[13n,17n],[14n,36n],[11n,53n],[10n,39n]],words=[];for(let i=0;i<243;i++){let j=i,a=[];for(let k=0;k<5;k++){a.push(1+j%3);j=Math.floor(j/3)}words.push(a)}
 function val(p,t){return (t&1?p[0]:0n)^(t&2?p[1]:0n)}
 let counts=Array(64).fill(0);for(let w of words){let s=w.reduce((a,t,i)=>a^val(orig[i],t),0n);counts[Number(s)]++}
 let dp=[1,...Array(63).fill(0)];for(let p of orig){let next=Array(64).fill(0);for(let i=0;i<64;i++)for(let t=1;t<4;t++)next[i^Number(val(p,t))]+=dp[i];dp=next}
 if(JSON.stringify(dp)!==JSON.stringify(counts)||counts[29]!==0||counts.filter(x=>x===0).length!==1)throw Error("MFC");
 let planes=orig,assignments=words,dim=6,levels=[];
 for(let d=0;d<=5;d++){let checks=0;for(let i=0;i<words.length;i++){let s=assignments[i].reduce((a,t,j)=>{checks++;if(!t)throw Error("zero owner");return a^val(planes[j],t)},0n),old=words[i].reduce((a,t,j)=>a^val(orig[j],t),0n);if(s!==old)throw Error("reciprocal private target")}
 levels.push({d,owners:planes.length,dimension:dim,checks,rootWords:words.length});
 if(d===5)break;let P=[];for(let [u,v] of planes){let a=1n<<BigInt(dim++),b=1n<<BigInt(dim++);P.push([a,b^u],[b,a^v])}planes=P;assignments=assignments.map(w=>w.flatMap(t=>[((t&1)<<1)|((t&2)>>1),t]));}
 return {counts,levels,missing:29};
}};
