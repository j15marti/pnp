function assert(b,m){if(!b)throw Error(m)}
function rank(A){const piv=new Map();for(let x of A){while(x){let b=x.toString(2).length-1;if(!piv.has(b)){piv.set(b,x);break}x^=piv.get(b)}}return piv.size}
function affine(ell){const H=2**ell;const a=[];for(let x=0;x<H;x++)for(let y=0;y<H;y++)if(x!==y)a.push(BigInt(x)|(BigInt(y)<<BigInt(ell))|(BigInt(x|y)<<BigInt(2*ell)));return {ell,points:a.length,rank:rank(a.map(x=>x^a[0]))}}
function domains(ell,guards,positive){const H=2**ell;const rows=guards.map(g=>Array.from({length:H},(_,x)=>x).filter(x=>g.every((b,j)=>b===-1||b===((x>>j)&1))));return positive?[rows[0].filter(x=>rows[1].includes(x)),...rows.slice(2)]:rows}
function matching(D,H){const owner=Array(H).fill(-1);function augment(i,seen){for(const x of D[i])if(!seen.has(x)){seen.add(x);if(owner[x]<0||augment(owner[x],seen)){owner[x]=i;return true}}return false}for(let i=0;i<D.length;i++)if(!augment(i,new Set()))return null;const labels=Array(D.length);owner.forEach((v,x)=>{if(v>=0)labels[v]=x});return labels}
function brute(D,i=0,used=new Set()){if(i===D.length)return true;for(const x of D[i])if(!used.has(x)){used.add(x);if(brute(D,i+1,used))return true;used.delete(x)}return false}
function audit(){const ranks=[1,2,3,4,5,6,7].map(affine);for(const r of ranks.filter(r=>r.ell>=3))assert(r.rank===3*r.ell,"augmented affine rank");
let seed=21973;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};let comparisons=0,yes=0,no=0,larger=0;
for(const ell of [2,3,4,5,6]){const H=2**ell;for(let t=0;t<100;t++){const G=Array.from({length:H+1},()=>Array.from({length:ell},()=>[-1,-1,-1,0,1][rnd(5)]));for(const positive of [true,false]){const D=domains(ell,G,positive),M=matching(D,H);if(ell===2){assert(Boolean(M)===brute(D),"matching vs exhaustive");comparisons++}else larger++;
if(M){yes++;assert(new Set(M).size===M.length&&M.every((x,i)=>D[i].includes(x)),"match");const labels=positive?[M[0],M[0],...M.slice(1)]:M;assert(labels.every((x,i)=>G[i].every((b,j)=>b===-1||b===((x>>j)&1))),"guard lift");}else no++;
if(!positive)assert(!M,"pigeonhole");
}}}return {ranks,comparisons,larger,yes,no}}
console.log(JSON.stringify(audit(),null,2));
