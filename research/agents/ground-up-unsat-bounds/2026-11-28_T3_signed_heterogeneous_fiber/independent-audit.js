const fs=require('node:fs');const crypto=require('node:crypto');
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const audit=function audit(R,sha){
 const A=(t,m)=>{if(!t)throw Error(m)},canon=a=>a.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=a=>a.join(","),bin=(n,k)=>{let z=1;for(let i=1;i<=k;i++)z=z*(n-i+1)/i;return z};
 function subsets(b,k){let a=[];for(let s=0;s<2**b.length;s++){let t=b.filter((_,i)=>s>>i&1);if(t.length===k)a.push(t)}return a}
 // independent enumeration in lexicographic combination order, different construction from runner.
 const lex=(a,b)=>{for(let i=0;i<a.length;i++)if(a[i]!==b[i])return a[i]-b[i];return 0};
 function choices(b){return subsets(b.map((_,i)=>i),(b.length+1)/2).sort(lex).map(s=>s.map(i=>b[i]))}
 const rec=[];
 for(const f of R.family){let C=[];for(let P of f.phase){let groups=P.map(l=>choices(f.blocks[Math.abs(l)-1]).map(s=>s.map(t=>l>0?t:-t)));let c=[];function cross(i){if(i===groups.length){C.push(canon(c));return}for(let a of groups[i]){c.push(...a);cross(i+1);c.length-=a.length}}cross(0)}
 let raw="p cnf "+f.vars+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0\n").join("");A("DIMACS-CNF-v1:sha256:"+sha(raw)===f.instance_id&&raw.length*8===f.original_N_bits,"source");
 // Compare recovered signed blocks to true blocks up to block permutations and complements. Verify every recovered phase clause by explicit adapter.
 let orient=new Map(f.recovery.orient),idMap=new Map(),pmap=new Map();f.recovery.comp.forEach((b,j)=>{let i=f.blocks.findIndex(B=>B.length===b.length&&B.every(l=>b.includes(Math.abs(l))));A(i>=0,"block partition");let s=f.blocks[i].map(l=>(+(l<0)^orient.get(Math.abs(l))));A(s.every(x=>x===s[0]),"gauge");idMap.set(j+1,[i+1,s[0]]);pmap.set(i+1,[j+1,s[0]])});
 let phaseKeys=new Set(f.phase.map(key));A(f.recovery.phase.every(P=>phaseKeys.has(key(canon(P.map(l=>{let [i,s]=idMap.get(Math.abs(l));return ((l>0)^s)?i:-i}))))),"phase adapter");A(f.recovery.phase.length===f.phase.length,"phase count");
 let no=f.yes===false;let metrics=[];
 if(no)for(let i=0;i<f.blocks.length;i++){let B=f.blocks[i],d=(B.length-1)/2,K=j=>bin(f.blocks[j-1].length,(f.blocks[j-1].length+1)/2),s=bin(2*d,d),positive=f.phase.filter(P=>P.includes(i+1)),negative=f.phase.filter(P=>P.includes(-i-1)),prod=P=>P.filter(l=>Math.abs(l)!==i+1).reduce((x,l)=>x*K(Math.abs(l)),1);
 let removed=s*[...positive,...negative].reduce((a,P)=>a+prod(P),0),count=0,terms=[];for(let P of positive)for(let Q of negative){let X=P.filter(l=>Math.abs(l)!==i+1),Y=Q.filter(l=>Math.abs(l)!==i+1);if(X.some(l=>Y.includes(-l)))continue;A(!X.some(l=>Y.some(y=>Math.abs(y)===Math.abs(l))),"cross scopes");let v=s*prod(P)*prod(Q);count+=v;terms.push({P,Q,v})}
 // Verify no exterior phase row can subsume a resolvent, for m>=4.
 let subsumptionPossible=false;for(let {P,Q} of terms){let S=new Set([...P,...Q].filter(l=>Math.abs(l)!==i+1));if(f.phase.some(C=>C.every(l=>S.has(l))))subsumptionPossible=true}
 let one=B[0],pair=f.inc.find(x=>x[0]===Math.abs(one))[1];A(pair[0]+pair[1]===removed,"removed count");A(count>removed,"no growth");
 metrics.push({phase:i+1,physical:B.map(Math.abs),removed,resolvents:count,ratio:count/removed,subsumptionPossible,terms})}
 // Independent exhaustive raw resolvent count at the smallest bucket (one pivot), to verify analytic count.
 let sample=null;if(no){let i=metrics.reduce((a,b)=>a.removed<b.removed?a:b),v=i.physical[0],p=C.filter(c=>c.includes(v)),n=C.filter(c=>c.includes(-v));let R=new Set(),pairs=0;for(let a of p)for(let b of n){pairs++;let r=new Set([...a,...b]);r.delete(v);r.delete(-v);if([...r].some(l=>r.has(-l)))continue;R.add(key(canon([...r])))}A(R.size===i.resolvents,"count replay");sample={v,pairs,resolvents:R.size,removed:p.length+n.length}}
 rec.push({instance:f.instance,instance_id:f.instance_id,original_N_bits:f.original_N_bits,sourceHash:sha(raw),phaseMap:[...idMap],rows:C.length,metrics,sample,minRatio:no?Math.min(...metrics.map(x=>x.ratio)):null,exteriorSubsumptionCandidates:metrics.filter(x=>x.subsumptionPossible).length})}
 return rec;
};
console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),sha),null,2));
