const run=function(data){
 const out=[];
 for(const x of data){for(const lane of ["native","companion"]){const a=x[lane],n=a.vs.length;
 // 2-SAT implications on actually replayed RUP clauses only, no native/provenance cross import.
 function SCC(clauses){const G=Array.from({length:2*n},()=>[]),id=l=>2*(Math.abs(l)-1)+(l<0?1:0);let ops=0;for(const c of clauses){if(!c.length)return {conflict:true,ops};if(c.length===1)G[id(-c[0])].push(id(c[0]));if(c.length===2){G[id(-c[0])].push(id(c[1]));G[id(-c[1])].push(id(c[0]))}}let reach=[];for(let i=0;i<2*n;i++){let v=new Set([i]),q=[i];for(let j=0;j<q.length;j++)for(const w of G[q[j]]){ops++;if(!v.has(w)){v.add(w);q.push(w)}}reach.push(v)}let forced=[],classes=[],seen=new Set();for(let i=0;i<2*n;i++){if(reach[i].has(i^1)&&reach[i^1].has(i))return {conflict:true,ops,variable:a.vs[Math.floor(i/2)]};if(reach[i].has(i^1))forced.push((i%2?1:-1)*a.vs[Math.floor(i/2)]);if(!seen.has(i)){let c=[...reach[i]].filter(j=>reach[j].has(i));c.forEach(j=>seen.add(j));classes.push(c)}}return {conflict:false,ops,forced,classes:classes.length,equalities:2*n-classes.length}}
 const prefixes=[0,32,64,128,256,512,a.rup.learn.length].filter((v,i,A)=>v<=a.rup.learn.length&&A.indexOf(v)===i);
 let result={id:x.id,lane,learnedOnlySCC:prefixes.map(k=>({k,...SCC(a.rup.learn.slice(0,k))}))};
 if(a.interfaces){const L=a.L.support,R=a.R.support,b=a.geometry.B.length;
 // Exact linear separation in Boolean feature space: h|L=0, h|R=1. Full row reduction or explicit dual inconsistency.
 function separate(deg){let mon=[0];function comb(i,k,m){if(!k){mon.push(m);return}for(let j=i;j<=b-k;j++)comb(j+1,k-1,m|(1<<j))}for(let k=1;k<=deg;k++)comb(0,k,0);let rows=new Map(),work=0,rank=0,con=1n<<BigInt(mon.length),contradiction=false;let feature=w=>{let z=0n;for(let j=0;j<mon.length;j++){work++;if((w&mon[j])===mon[j])z|=1n<<BigInt(j)}return z};
 outer:for(let [S,t] of [[L,0],[R,1]])for(let w of S){let v=feature(w)^(t?con:0n);for(let j=mon.length-1;j>=0;j--){let bit=1n<<BigInt(j);work++;if(!(v&bit))continue;if(rows.has(j)){v^=rows.get(j)}else{rows.set(j,v);rank++;v=0n;break}}if(v===con){contradiction=true;break outer}}
 if(contradiction)return {degree:deg,dimension:mon.length,rank,work,status:"NO_SEPARATOR"};
 let coeff=0n;for(let [j,v] of [...rows].sort((a,b)=>a[0]-b[0])){let p=0,z=v&coeff;while(z){z&=z-1n;p^=1}if(p!==Number(Boolean(v&con)))coeff|=1n<<BigInt(j)}
 let terms=mon.filter((m,j)=>Boolean(coeff&(1n<<BigInt(j))));let verification=0;for(let [S,t] of [[L,0],[R,1]])for(let w of S){let p=0;for(let m of terms){verification++;if((w&m)===m)p^=1}if(p!==t)throw Error("separator check")}return {degree:deg,dimension:mon.length,rank,work,verification,status:"SEPARATOR",terms}}
 // Cross-support unary/binary projection; each regional table forbids any absent pair. Iteratively intersect opposite marginal projections.
 function forbidden(S){let q=[];for(let i=0;i<b;i++)for(let j=i;j<b;j++){let k=i===j?2:4,seen=new Set(S.map(w=>((w>>i)&1)+(i===j?0:2*((w>>j)&1))));for(let z=0;z<k;z++)if(!seen.has(z))q.push([i,j,z])}return q}
 function filter(S,q){return S.filter(w=>q.every(([i,j,z])=>((w>>i)&1)+(i===j?0:2*((w>>j)&1))!==z))}
 let l=L.slice(),r=R.slice(),rounds=[],pl=forbidden(l),pr=forbidden(r);
 for(let t=0;t<=L.length+R.length;t++){let ql=forbidden(l),qr=forbidden(r),nl=filter(l,qr),nr=filter(r,ql);rounds.push({left:l.length,right:r.length,leftExclusions:ql.length,rightExclusions:qr.length,nextLeft:nl.length,nextRight:nr.length});if(!nl.length||!nr.length||nl.length===l.length&&nr.length===r.length)break;l=nl;r=nr}
 result.separation=[1,2,3].map(separate);result.marginalRounds=rounds;result.parents={leftInitialExclusions:pl,rightInitialExclusions:pr};
 }
 out.push(result)
 }}return out
};
if(require.main===module)console.log(JSON.stringify(run(JSON.parse(require('node:fs').readFileSync(process.argv[2],'utf8'))),null,2));
