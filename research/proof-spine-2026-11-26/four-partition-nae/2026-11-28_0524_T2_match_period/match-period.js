function family(q,yes){
 const h=Math.floor(Math.log2(q)),H=2**h,bad=1n<<BigInt(h+q),rows=Array.from({length:2*q},()=>[]);
 const add=(i,j,words)=>{for(const v of words)rows[i].push({j,v:v.toString(16)})};
 for(let c=0;c<q;c++){let a=2*c,b=a+1,v=1n<<BigInt(h+c),words=Array.from({length:H},(_,j)=>BigInt(j));add(a,a,words);add(a,b,words.map(w=>w^v));add(b,b,[0n]);add(b,a,[0n]);if(c+1<q)add(a,a+2,[bad]);}
 return {format:"MATCH-SYNDROME-v1",dimension:h+q+1,rows,target:(yes?1n<<BigInt(h):bad).toString(16)};
}

function solve(F,skipFilter=false){
 const n=F.rows.length,rows=F.rows.map(r=>r.map(({j,v},id)=>({j,v:BigInt("0x"+v),id}))),adj=rows.map(r=>[...new Set(r.map(e=>e.j))]),counts={matchArc:0,matchCalls:0,wordPairs:0,periodChecks:0,rankXors:0}; 
 function matching(forceI=-1,forceJ=-1){counts.matchCalls++;let M=new Int32Array(n).fill(-1);if(forceI>=0)M[forceJ]=forceI;function dfs(i,seen){for(const j of adj[i]){counts.matchArc++;if(j===forceJ||seen[j])continue;seen[j]=1;if(M[j]<0||dfs(M[j],seen)){M[j]=i;return true}}return false}for(let i=0;i<n;i++)if(i!==forceI&&!dfs(i,new Uint8Array(n)))return false;return true}
 if(!matching())return {status:"NO matching",counts};
 const supported=adj.map((a,i)=>a.filter(j=>skipFilter||matching(i,j))),sets=supported.map(a=>new Set(a)),removed=adj.reduce((s,a,i)=>s+a.length-supported[i].length,0);
 const R=Array.from({length:n},()=>[]);supported.forEach((a,i)=>a.forEach(j=>R[j].push(i)));
 let used=new Set(),components=[];for(let i=0;i<n;i++)if(!used.has(i)){let left=[i],right=new Set();used.add(i);for(let k=0;k<left.length;k++)for(const j of supported[left[k]]){right.add(j);for(const a of R[j])if(!used.has(a)){used.add(a);left.push(a)}}components.push({left,right:[...right]})}
 const D=[],target=BigInt("0x"+F.target);
 // This implemented recognizer accepts K2,2 and forced edges only, not all cycles.
 for(const {left,right} of components){if(left.length!==right.length||left.length>2)return {status:"UNKNOWN component",removed,components:components.length,counts};let words=new Map();function visit(k,used,x,sel){if(k===left.length){if(!words.has(x))words.set(x,sel);return}let i=left[k];for(const e of rows[i]){counts.wordPairs++;if(sets[i].has(e.j)&&!used.has(e.j)){let U=new Set(used);U.add(e.j);visit(k+1,U,x^e.v,[...sel,[i,e.id]])}}}visit(0,new Set(),0n,[]);if(!words.size)return {status:"NO component",removed,counts};const vals=[...words.keys()],anchor=vals[0],S=new Set(vals.map(x=>x^anchor));let H=[];for(const h of S){let ok=true;for(const x of S){counts.periodChecks++;if(!S.has(h^x)){ok=false;break}}if(ok)H.push(h)}if(H.length!==S.size)return {status:"UNKNOWN nonaffine",removed,counts};D.push({words,anchor,H})}
 function makeBasis(){let b=new Map();return {b,insert(x,tag=0n){while(x){let k=x.toString(2).length-1;if(!b.has(k)){b.set(k,[x,tag]);return}let [y,t]=b.get(k);x^=y;tag^=t;counts.rankXors++}},reduce(x){let tag=0n;while(x){let k=x.toString(2).length-1;if(!b.has(k))return [x,tag];let [y,t]=b.get(k);x^=y;tag^=t;counts.rankXors++}return [0n,tag]}}}
 const G=makeBasis(),ids=[];let b=target;for(let i=0;i<D.length;i++){const {anchor,H}=D[i];b^=anchor;let local=makeBasis();for(const h of H) local.insert(h);for(const [v] of local.b.values()){let tag=1n<<BigInt(ids.length);ids.push([i,v]);G.insert(v,tag)}}
 const [res,tag]=G.reduce(b);const cut=components.length>1?Math.floor(components.length/2):0,rankSide=(d)=>{let b=makeBasis();for(const x of d)for(const v of x.H)b.insert(v);return b.b.size};
 const cutRank=rankSide(D.slice(0,cut))+rankSide(D.slice(cut))-G.b.size;
 if(res)return {status:"NO affine",removed,components:components.length,rank:G.b.size,cutRank,counts};
 const vals=D.map(x=>x.anchor);for(let i=0;i<ids.length;i++)if((tag>>BigInt(i))&1n){const [j,v]=ids[i];vals[j]^=v}let selection=[];for(let i=0;i<D.length;i++){if(!D[i].words.has(vals[i]))throw Error("lift");selection.push(...D[i].words.get(vals[i]))}
 return {status:"YES",removed,components:components.length,rank:G.b.size,cutRank,selection,counts};
}

function verify(F,R){if(R.status==="YES"){let rows=new Set(),resources=new Set(),sum=0n;for(const [i,id] of R.selection){if(rows.has(i)||!F.rows[i]?.[id])return false;let e=F.rows[i][id];if(resources.has(e.j))return false;rows.add(i);resources.add(e.j);sum^=BigInt("0x"+e.v)}return rows.size===F.rows.length&&sum===BigInt("0x"+F.target)}
 if(R.status!=="NO affine")return false;
 // Independent special-family certificate: each prefix of pairs has no incoming cross edge;
 // any outgoing edge strands a prefix resource. Highest syndrome bit appears only on outgoing edges.
 let d=F.dimension-1,mask=1n<<BigInt(d);if(!(BigInt("0x"+F.target)&mask))return false;
 for(let i=0;i<F.rows.length;i++)for(const e of F.rows[i]){if(e.j<0||e.j>=F.rows.length)return false;let a=i>>1,b=e.j>>1;if(b<a)return false;if((BigInt("0x"+e.v)&mask)&&b===a)return false}return true
}

function rawAffine(F){let B=new Map(),b=BigInt("0x"+F.target);function insert(x){while(x){let k=x.toString(2).length-1;if(!B.has(k)){B.set(k,x);return}x^=B.get(k)}}for(const row of F.rows){let a=BigInt("0x"+row[0].v);b^=a;for(const e of row)insert(a^BigInt("0x"+e.v))}while(b){let k=b.toString(2).length-1;if(!B.has(k))return false;b^=B.get(k)}return true}
module.exports={family,solve,verify,rawAffine};
