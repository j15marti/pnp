function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m||"assertion")};
 const rank=xs=>{const B=new Map();for(let x of xs){while(x){const k=x.toString(2).length-1;if(B.has(k))x^=B.get(k);else{B.set(k,x);break}}}return B.size};
 const bit=i=>1n<<BigInt(i), form=(i,j)=>bit(i)^bit(j);
 const rowOK=(r,w)=>r.reduce((s,i)=>s+w[i],0)===2;
 const build=q=>{let n=3;const reg=[],ext=[],groups=[];const a=0,b=1,d=2;
 for(let i=0;i<q;i++){const c=n++,e=n++,u=n++,v=n++;groups.push({c,e,u,v});reg.push([a,b,c,u],[a,d,e,v]);}
 for(const [i,j] of [[a,b],[a,d],...groups.map(g=>[g.c,g.e])])ext.push([i,j,n++,n++]);
 return {n,reg,ext,groups,guard:[]}};
 const localA=(F,g)=>{const ids=[0,1,2,g.c,g.e,g.u,g.v],R=F.reg.filter(r=>r.includes(g.u)||r.includes(g.v));const S=new Map();for(let k=0;k<128;k++){const w={};ids.forEach((id,j)=>w[id]=(k>>j)&1);if(R.every(r=>rowOK(r,w))){const x=w[0]^w[1],y=w[0]^w[2],z=w[g.c]^w[g.e];S.set(4*x+2*y+z,w)}}return S};
 const localC=(x,y,z)=>{let count=0;for(let a=0;a<2;a++)for(let c=0;c<2;c++){const b=a^x,d=a^y,e=c^z;const u=2-a-b-c,v=2-a-d-e;if((u===0||u===1)&&(v===0||v===1))count++}return count>0};
 const B=(x,y,z)=>Boolean(x||y||!z);
 const fullC=F=>{const S=new Set();for(let k=0;k<2**F.n;k++){const w=Array.from({length:F.n},(_,i)=>(k>>i)&1);if([...F.reg,...F.ext].every(r=>rowOK(r,w))){let s=4*(w[0]^w[1])+2*(w[0]^w[2])+(w[F.groups[0].c]^w[F.groups[0].e]);S.add(s)}}return S};
 const fingerprint=o=>{let h=2166136261;for(const c of JSON.stringify(o)){h=Math.imul(h^c.charCodeAt(0),16777619)}return (h>>>0).toString(16)};
 const out=[];
 for(const q of [1,2,4,8,16,32,64,128]){
 const F=build(q),A=JSON.parse(JSON.stringify(F)),BB=JSON.parse(JSON.stringify(F)),C=JSON.parse(JSON.stringify(F)),I=JSON.parse(JSON.stringify(F));
 // The last coordinate in each row is a unique private completion, so free physical
 // coordinates directly give the parity quotient. Verify that premise.
 const rows=[...BB.reg,...BB.ext];assert(rows.every(r=>rows.filter(s=>s.includes(r[3])).length===1));
 const pa=BB.reg.flatMap(r=>[form(r[0],r[1]),form(r[0],r[2])]);
 const pe=BB.ext.flatMap(r=>[form(r[0],r[1]),form(r[0],r[2])]);
 const boundary=[form(0,1),form(0,2),...BB.groups.map(g=>form(g.c,g.e))];
 const rb=rank(pa)+rank(pe)-rank([...pa,...pe]);assert(rb===q+2&&rank(boundary)===rb);
 assert(rank([...pa,...boundary])===rank(pa)&&rank([...pe,...boundary])===rank(pe));
 const reps=BB.groups.map(g=>form(0,g.c));assert(rank([...boundary,...reps])===rb+q);
 // No rank-zero or rank-one local factor exists before any import.
 assert(rows.every(r=>rank([form(r[0],r[1]),form(r[0],r[2])])===2));
 const SA=A.groups.map(g=>localA(A,g));let tests=0;
 for(const s of SA)for(let w=0;w<8;w++){const x=w>>2,y=(w>>1)&1,z=w&1;assert(s.has(w)===B(x,y,z));assert(s.has(w)===localC(x,y,z));tests++}
 let globalC=null;if(q===1){const s=fullC(C);assert(s.size===7&& !s.has(1));globalC={assignments:2**F.n,support:[...s].sort()}}
 // Integrated lift: each local attained witness from A is complemented if necessary
 // to agree on anchor a=0; x,y are shared, hence actual b,d agree too.
 let lifts=0;
 for(let x=0;x<2;x++)for(let y=0;y<2;y++)for(let pattern=0;pattern<4;pattern++){
 const zs=I.groups.map((_,j)=>pattern===0?0:pattern===1?1:pattern===2?j%2:1-j%2);
 if(!zs.every(z=>B(x,y,z)))continue;
 const w=Array(I.n).fill(-1);w[0]=0;w[1]=x;w[2]=y;
 for(let j=0;j<q;j++){const g=I.groups[j],v=SA[j].get(4*x+2*y+zs[j]);assert(v);for(const id of [0,1,2,g.c,g.e,g.u,g.v]){const a=v[id]^v[0];assert(w[id]===-1||w[id]===a);w[id]=a}}
 for(const [a,b,c,d] of I.ext){const s=2-w[a]-w[b];w[c]=s>0?1:0;w[d]=s===2?1:0}
 assert([...I.reg,...I.ext].every(r=>rowOK(r,w)));lifts++}
 // Exact compact factors have full affine hull individually and collectively:
 // x=y=1 gives all z, and (x,y)=(1,0),(0,1) at z=0 span remaining directions.
 // No new unary/affine deductions are imported by the exact replacements.
 const states=3n*(1n<<BigInt(q))+1n;
 out.push({q,n:F.n,m:rows.length,N:8*JSON.stringify(F).length,fingerprint:fingerprint(F),boundaryRank:rb,privateRank:q,A_nativeAssignments:128*q,B_resolvents:q,C_localBoundaryChecks:8*q,comparisons:tests,globalC,verifiedFullLifts:lifts,exactSupportSize:states.toString(),explicitTableCap256:states<=256n?"admitted":"UNKNOWN",rank2Only:"UNKNOWN",integratedRank3:"exact projected relation"});
 }
 // General pairwise exclusion formula, independent of source-family simplification:
 // arbitrary boundary assignments for random rank-one-private groups.
 let seed=20261126;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};let generic=0;
 const evalf=(v,w)=>{let z=v&w,p=0;while(z){p^=1;z&=z-1}return p};
 for(let j=0;j<300;j++){const d=1+rng()%7,m=1+rng()%9;const fac=Array.from({length:m},()=>({l:1+rng()%((1<<d)-1),g:rng()%(1<<d),a:rng()%2,b:rng()%2}));
 for(let w=0;w<1<<d;w++){const exact=[0,1].some(t=>fac.every(f=>evalf(f.l,w)!==f.a||(t^evalf(f.g,w))!==f.b));let good=true;
 for(let i=0;i<m;i++)for(let k=i+1;k<m;k++){const f=fac[i],g=fac[k];if(evalf(f.l,w)===f.a&&evalf(g.l,w)===g.a&&evalf(f.g^g.g,w)===(1^f.b^g.b))good=false}
 assert(exact===good);generic++}
 }
 return {out,genericChartBoundaryComparisons:generic,seed:20261126,mode:"sequential copies, no full solver or independent proof build"};
}
console.log(JSON.stringify(audit(),null,2));
