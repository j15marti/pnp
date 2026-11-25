function run(){
 const ledger={rankInsertions:0,rankXors:0,closureScans:0,closurePinsArchived:0,localWords:0,transitionAttempts:0,positiveTransitions:0,keyMerges:0,referenceWords:0,assertions:0}; const check=(x)=>{ledger.assertions++;if(!x)throw Error("assertion "+ledger.assertions)};
 const bit=i=>1n<<BigInt(i);
 function reduce(B,v){while(v){const p=v.toString(2).length-1;if(!B[p])break;v^=B[p];ledger.rankXors++}return v}
 function add(B,v){ledger.rankInsertions++;v=reduce(B,v);if(v)B[v.toString(2).length-1]=v}
 const rank=B=>B.filter(Boolean).length;
 function merge(dst,src){if(!dst)return {count:src.count,anchor:src.anchor,basis:src.basis.slice()};dst.count+=src.count;add(dst.basis,dst.anchor^src.anchor);for(const v of src.basis)if(v)add(dst.basis,v);return dst}
 function compile(blocks){const vars=[...new Set(blocks.flatMap(b=>b.v))].sort((a,b)=>a-b), last=new Map(), cols=Array(3*blocks.length).fill(0n), edges=[];let g=0;blocks.forEach((b,i)=>{check(new Set(b.v).size===3);b.v.forEach((v,j)=>{const o=3*i+j;if(last.has(v)){const p=last.get(v);cols[p]^=bit(g);cols[o]^=bit(g);edges.push([p,o]);g++}last.set(v,o)})});return {blocks,vars,cols,edges,g}}
 function verify(c,w){for(const [a,b] of c.edges)if(Boolean(w&bit(a))!==Boolean(w&bit(b)))return false;return c.blocks.every((b,i)=>Boolean(b.mask&(1<<Number((w>>BigInt(3*i))&7n))))}
 function solve(c){const {blocks,cols,g}=c,m=blocks.length;let suffix=Array(m+1);suffix[m]=[];for(let i=m-1;i>=0;i--){let B=suffix[i+1].slice();for(let j=0;j<3;j++)add(B,cols[3*i+j]);suffix[i]=B}check(rank(suffix[0])===g);let prefix=[],width=0,peak=1;let dp=new Map([[0n,{count:1n,anchor:0n,basis:[]}]]);
 // Before deductions: exact owner-local affine-hull closure on actual equality guard.
 // Each owner has three distinct source variables; hence guard projection onto it is surjective.
 let locals=blocks.map((b,i)=>{ledger.closureScans++;let B=[],a=null,groups=new Map();for(let w=0;w<8;w++){ledger.localWords++;if(!(b.mask&(1<<w)))continue;let s=0n;for(let j=0;j<3;j++)if(w&(1<<j))s^=cols[3*i+j];if(a===null)a=BigInt(w);else add(B,BigInt(w)^a);let x=BigInt(w)<<BigInt(3*i);groups.set(s,merge(groups.get(s),{count:1n,anchor:x,basis:[]}))}check(rank(B)===3);return groups});
 for(let i=0;i<m;i++){for(let j=0;j<3;j++)add(prefix,cols[3*i+j]);const w=rank(prefix)+rank(suffix[i+1])-g;width=Math.max(width,w);let next=new Map();for(const [s,p] of dp)for(const [u,l] of locals[i]){ledger.transitionAttempts++;const t=s^u;if(reduce(suffix[i+1],t)!==0n)continue;ledger.positiveTransitions++;let b=p.basis.slice();for(const v of l.basis)if(v)add(b,v);if(next.has(t))ledger.keyMerges++;next.set(t,merge(next.get(t),{count:p.count*l.count,anchor:p.anchor^l.anchor,basis:b}))}check(BigInt(next.size)<=bit(w));peak=Math.max(peak,next.size);dp=next}
 const root=dp.get(0n);ledger.closureScans++;if(root){check(verify(c,root.anchor));ledger.closurePinsArchived+=3*m-rank(root.basis); // entire affine hull is exact; adding its necessary equations leaves support unchanged.
 ledger.closureScans++;check(root.count>0n)}return {count:root?.count??0n,anchor:root?.anchor,basis:root?.basis??[],width,peak,guardRank:g}}
 function reference(c){let ref=null;for(let w=0;w<2**c.vars.length;w++){ledger.referenceWords++;let x=0n;c.blocks.forEach((b,i)=>b.v.forEach((v,j)=>{if(w&(1<<c.vars.indexOf(v)))x|=bit(3*i+j)}));if(verify(c,x))ref=merge(ref,{count:1n,anchor:x,basis:[]})}return ref??{count:0n,basis:[]}}
 function audit(c){const a=solve(c),b=reference(c);check(a.count===b.count);check(rank(a.basis)===rank(b.basis));if(a.count){check(reduce(a.basis,a.anchor^b.anchor)===0n);for(const v of b.basis)if(v)check(reduce(a.basis,v)===0n)}return a}
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(v=>({v,mask:126}));
 const cases=[F];for(let i=0;i<7;i++)for(const mask of [127,254])cases.push(F.map((b,j)=>i===j?{v:b.v,mask}:b));
 const rows=cases.map((b,i)=>{const a=audit(compile(b));check(a.count===BigInt(i?5:0));return {case:i,count:String(a.count),width:a.width,peak:a.peak,guardRank:a.guardRank,hullRank:rank(a.basis)}});
 let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let random={SAT:0,UNSAT:0};
 for(let i=0;i<80;i++){let blocks=[];for(let j=0;j<3+rnd(7);j++){let v=[];while(v.length<3){const k=rnd(7);if(!v.includes(k))v.push(k)}blocks.push({v,mask:[126,127,254][rnd(3)]})}let a=audit(compile(blocks));random[a.count?"SAT":"UNSAT"]++}
 let scaling=[];for(const k of [4,16,64,128]){let chain=Array.from({length:k},(_,i)=>({v:[7+2*i,8+2*i,9+2*i],mask:126}));for(const i of [0,1]){const a=solve(compile([...cases[i],...chain]));check(a.count===BigInt(i?5:0)*2n*3n**BigInt(k));if(i)check(rank(a.basis)===rows[1].hullRank+2*k+1);scaling.push({chain:k,SAT:!!i,count:String(a.count),guardRank:a.guardRank,width:a.width,peak:a.peak,hullRank:rank(a.basis)})}}
 return {fano:rows,random,scaling,ledger,scope:"Explicit 3-bit supports; no general signed Gaussian fiber implementation, no physical compiler, no measured bytes/CM."}
}
console.log(JSON.stringify(run(),null,2));
