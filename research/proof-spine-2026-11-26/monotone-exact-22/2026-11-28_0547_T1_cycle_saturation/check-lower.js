// Independently validate stored affine lower carrier, selected cycles and exact rank claim.
function checkLower(F,R){
 if(R.status==="NO_MATCHING")return {skip:true};
 const n=F.rows.length,M=R.base,ct={records:0,rankXor:0,checks:0};const v=x=>BigInt("0x"+x);
 function space(xs){let b=[];function red(x){for(const y of b){let z=x^y;ct.rankXor++;if(z<x)x=z}return x}for(let x of xs){x=red(x);if(x){b.push(x);b.sort((a,b)=>a>b?-1:1)}}return {b,red}}
 function labels(i,j){const L=[...new Set(F.rows[i].filter(e=>e.j===j).map(e=>e.v))].map(v);ct.records+=L.length;if(!L.length)throw Error("missing edge");const a=L[0],s=space(L.map(x=>x^a));return {a,vec:BigInt(L.length)===(1n<<BigInt(s.b.length))?s.b:[]}}
 let seen=new Set(),spans=[];
 for(const C of R.selected){
  if(C.length<2||new Set(C).size!==C.length)throw Error("cycle shape");for(const i of C){ct.checks++;if(i<0||i>=n||seen.has(i))throw Error("cycle overlap");seen.add(i)}
  let Z=C.map(i=>labels(i,M[i])),A=C.map((i,k)=>labels(i,M[C[(k+1)%C.length]]));
  let H=space(Z.flatMap(x=>x.vec)),J=space(A.flatMap(x=>x.vec));for(const h of H.b)if(J.red(h))throw Error("period not contained");
  spans.push(...H.b,Z.concat(A).reduce((z,e)=>z^e.a,0n));
 }
 for(let i=0;i<n;i++)if(!seen.has(i))spans.push(...labels(i,M[i]).vec);
 const L=space(spans),U=space(R.upper.map(v));if(L.b.length!==R.lowerRank||space(R.lower.map(v)).b.length!==L.b.length||R.lower.some(x=>L.red(v(x)))||L.b.some(x=>U.red(x)))throw Error("span");
 if(R.exact!==(L.b.length===U.b.length))throw Error("exact rank mismatch");
 const t=v(F.target)^v(R.origin);if(R.status==="YES"&&L.red(t)||R.status==="UNKNOWN"&&(!L.red(t)||U.red(t)))throw Error("status mismatch");
 return ct;
}
const fs=require('node:fs');const E=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(E.tests.map(z=>({id:z.result.instance_id,cert:z.certificate_id,checks:z.result.arms.map(a=>checkLower(z.result.source,a))}))));
