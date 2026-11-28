
function auditPairCertificates(R,sha){
const A=(b,m)=>{if(!b)throw Error(m)},enc=x=>JSON.stringify(x)+"\n",rows=[];
for(let {cert:c,certificate_id:id} of R){
 A("CERT-v1:sha256:"+sha(enc(c))===id,"cert hash");A("DELETION-SYNDROME-v1:sha256:"+sha(enc(c.source))===c.instance_id&&enc(c.source).length*8===c.N,"source");
 let S=c.source.labels.map(s=>[0n,...s.map(x=>BigInt("0x"+x))]),target=BigInt("0x"+c.source.target),n=S.length,used=new Set(),T=S.map(x=>x.slice()),bad=false,localChecks=0;
 A(c.source.q===3&&JSON.stringify(c.source.adj)==="[[0,1,2],[0,1,2]]","shell");
 for(let p of c.pairs){let {i,j}=p,k=BigInt("0x"+p.mask);A(i!==j&&i>=0&&j>=0&&i<n&&j<n&&!used.has(i)&&!used.has(j),"pair");used.add(i);used.add(j);
 A(S.every((s,t)=>t===i||t===j||s.every(x=>!(x&k))),"private mask");let E=[];for(let a=0;a<4;a++)for(let b=0;b<4;b++){localChecks++;let y=S[i][a]^S[j][b];if(!((target^y)&k))E.push([a,b,y.toString(16)])}
 A(JSON.stringify(E)===JSON.stringify(p.out),"exact pair response");
 if(!E.length){bad=true;continue}T[i]=[...new Set(E.map(x=>S[i][x[0]]))];T[j]=[...new Set(E.map(x=>S[j][x[1]]))];
 }A(used.size===n,"cover");
 if(bad){A(c.decision==="NO","NO");rows.push({id:c.instance_id,verified:"NO-empty-pair",localChecks});continue}
 A(T.every(s=>s.length===2),"two option terminal");
 // Linear solve on all surviving local two-option dictionaries, WITHOUT fusing pairs.
 let rhs=target;let cols=T.map(s=>{rhs^=s[0];return s[0]^s[1]});let basis=new Map(),xors=0;
 for(let i=0;i<n;i++){let y=cols[i],tag=1n<<BigInt(i);while(y){let p=y&-y;if(!basis.has(p)){basis.set(p,[y,tag]);break}let [a,b]=basis.get(p);y^=a;tag^=b;xors++}}
 let word=0n,y=rhs;while(y){let p=y&-y;A(basis.has(p),"GE unexpected NO");let [a,b]=basis.get(p);y^=a;word^=b;xors++}
 let options=T.map((s,i)=>s[Number(word>>BigInt(i)&1n)]),sum=options.reduce((a,b)=>a^b,0n);A(sum===target&&c.decision==="YES","GE target");
 let lift=options.map((v,i)=>{let a=S[i].indexOf(v),D=a?1<<(a-1):0;let bins=[0,1,2].filter(r=>!(D>>r&1));A(bins.length>=2,"matching");return bins.slice(0,2)});
 rows.push({id:c.instance_id,verified:"YES-GE",localChecks,xors,rank:basis.size,originalOptions:n*4,retainedOptions:n*2,lift});
 }return rows}
