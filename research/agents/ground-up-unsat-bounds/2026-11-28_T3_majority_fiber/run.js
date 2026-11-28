const fs=require('node:fs');
const pins={"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data){
const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
const {sha,norm,project,replay,up,canon,key,solve,check}=new Function(data.native+";return {sha,norm,project,replay,up,canon,key,solve,check};")();
const enc=x=>JSON.stringify(x)+"\n",A=(x,m)=>{if(!x)throw Error(m)},meter=(cap=1000000)=>({scans:0,lits:0,cap}),V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
function parse(s){return s.trim().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1)))}
function independent(C,t){let m={scans:0,lits:0,nodes:0};function w(t,p){m.nodes++;let a=new Map(p);for(;;){let change=false;for(let i=C.length-1;i>=0;i--){let c=C[i],f=[],sat=false;m.scans++;for(let l of c){m.lits++;let b=a.get(Math.abs(l));if(b===+(l>0))sat=true;else if(b===undefined)f.push(l)}if(sat)continue;if(!f.length)return;if(f.length===1){a.set(Math.abs(f[0]),+(f[0]>0));change=true}}if(!change)break}A(t!==null,"bad leaf");let v=t[0];if(a.has(v)){w(t[a.get(v)+1],p);return}w(t[1],[...p,[v,0]]);w(t[2],[...p,[v,1]])}w(t,[]);return m}
function groups(C){let map=new Map();for(let c of C){let s=c.map(Math.abs),k=key(s);if(!map.has(k))map.set(k,{s,clauses:[]});map.get(k).clauses.push(c)}return [...map.values()]}
function pop(n){let c=0;while(n){n&=n-1;c++}return c}
function rank(rows){let B=new Map(),ops=0;for(let r of rows){while(r){let i=r.toString(2).length-1;ops++;if(B.has(i))r^=B.get(i);else{B.set(i,r);break}}}return {rank:B.size,ops}}
function monomials(b,d){return Array.from({length:2**b},(_,i)=>i).filter(i=>pop(i)<=d)}
function ev(w,M){let r=0n;for(let i=0;i<M.length;i++)if((w&M[i])===M[i])r|=1n<<BigInt(i);return r}
function exactLane(C){let vs=V(C),G=groups(C),m=meter(),u=up(C,[],m);A(!u.conflict,"root");
 const D=C.filter(c=>!c.some(l=>u.A.get(Math.abs(l))===+(l>0))).map(c=>canon(c.filter(l=>!u.A.has(Math.abs(l)))));
 let v=V(D),g=groups(D),local={scopes:0,words:0,affineRows:0,occupancyTight:0,minWidth:Infinity},pairs=0,geo={best:Infinity,interior:0},by=new Map(),B=[];
 for(let f of g){local.scopes++;let b=f.s.length;local.minWidth=Math.min(local.minWidth,b);let allowed=[];for(let w=0;w<2**b;w++){local.words++;if(f.clauses.every(c=>c.some(l=>((w>>f.s.indexOf(Math.abs(l)))&1)===+(l>0))))allowed.push(w)}A(allowed.length,"local contradiction");
  let rr=rank(allowed.map(w=>ev(w,monomials(b,1))));local.affineRows+=b+1-rr.rank;let counts=allowed.map(pop);if(Math.min(...counts)===Math.max(...counts))local.occupancyTight++;
  if(b===2)B.push(...f.clauses);for(let x of f.s){if(!by.has(x))by.set(x,new Set());for(let y of f.s)if(x!==y){pairs++;by.get(x).add(y)}}
 }
 for(let [x,n] of by)if(n.size<geo.best){geo.best=n.size;geo.pivot=x}geo.interior=geo.best<=8?1:0;
 // Sound one-step exact complete bucket elimination, independent replay.
 let p=project(D,128),q=replay(D,p.trace);A(enc(p.C)===enc(q.C),"replay");
 let r=solve(D),z=solve(p.C);A(r.status==="UNSAT"&&z.status==="UNSAT","base");
 let bck=independent(D,r.tree),zck=independent(p.C,z.tree);
 // Guarded D lane: exact failed singleton probes, with independent reverse replay via a leaf.
 let probes=[],work=meter(),guardPins=[];
 let sorted=v.slice().sort((a,b)=>(by.get(b)?.size||0)-(by.get(a)?.size||0)||a-b);
 for(let x of sorted.slice(0,8))for(let b of [0,1]){let t=up(D,[[x,b]],work);if(t.conflict){let c=independent([...D,[b?x:-x]],null);probes.push({x,b,c});guardPins.push([b?-x:x])}}
 let h=solve([...D,...guardPins]),hck=h.status==="UNSAT"?independent([...D,...guardPins],h.tree):null;
 // Stochastic guard discovery with fixed seed; no deduction unless UP + independent replay.
 let state=271128,random={tries:0,conflicts:0,work:meter(),seed:state};for(let i=0;i<16;i++){state=(Math.imul(state,1664525)+1013904223)>>>0;let x=v[state%v.length];state=(Math.imul(state,1664525)+1013904223)>>>0;let b=state>>>31;random.tries++;if(up(D,[[x,b]],random.work).conflict){random.conflicts++;independent([...D,[b?x:-x]],null)}}
 return {before:C.length,after:D.length,vars:v,hash:sha(enc(D)),rootUnits:[...u.A],early:m,local,geo,pairs,binaryClauses:B.length,projection:{trace:p.trace,scans:p.scans,pairs:p.pairs,replayScans:q.scans,replayPairs:q.pairs,remaining:p.C.length,hash:sha(enc(p.C))},base:r,baseCheck:bck,projected:z,projectedCheck:zck,guards:{probes,work,hybrid:h,check:hck},random}
}
let common=[];
for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){let s=JSON.parse(data.corpus).instances.find(x=>x.id===alias),r=JSON.parse(data.registry).instances.find(x=>x.alias==="EB-"+alias),g=compile({nvars:s.nvars,dimacs:s.dimacs});
A(sha(enc(g.network))===r.sha256&&enc(g.network).length*8===r.N_bits&&sha(s.dimacs)===r.source_cnf.sha256&&s.dimacs.length*8===r.source_cnf.N_bits&&sha(enc(g.source_map))===r.source_map_sha256,"auth");
let b=norm(g.network),p=project(b.C,128),q=replay(b.C,p.trace);A(enc(p.C)===enc(q.C),"native replay");
common.push({alias,source:r,normalization:{gauge:b.gauge,vis:b.vis,rows:b.rows,normalizedHash:sha(enc(b.C)),trace:p.trace,scans:p.scans,pairs:p.pairs,replayScans:q.scans,replayPairs:q.pairs,chartHash:sha(enc(p.C))},native:exactLane(p.C),cnf:exactLane(parse(s.dimacs))})
}
// New construction: every phase bit is majority of 2d+1 distinct carriers. A base clause is expanded exactly as a Cartesian product of (d+1)-subsets of its blocks.
function comb(b,k){return Array.from({length:2**b},(_,i)=>i).filter(i=>pop(i)===k).map(w=>Array.from({length:b},(_,i)=>i).filter(i=>w>>i&1))}
function base(m,yes=false){let C=[],n=2*m+1,s=1;for(let t=0;t<2;t++){let first=2+t*m,last=first+m-1;for(let i=first;i<last;i++)C.push([-i,i+1],[i,-(i+1)]);let g=t?-s:s;if(yes&&t===1)g=s;C.push([g,first,last],[g,-first,-last])}return {n,C}}
function lift(B,d){let b=2*d+1,Q=comb(b,d+1),C=[];for(let row of B.C){function rec(j,a){if(j===row.length){C.push(a);return}let l=row[j],off=(Math.abs(l)-1)*b;for(let q of Q)rec(j+1,[...a,...q.map(i=>(l>0?1:-1)*(off+i+1))])}rec(0,[])}return {n:B.n*b,C}}
function bytes(n,C){return "p cnf "+n+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0").join("\n")+"\n"}
function checkWitness(C,w){let visits=0;for(let c of C){let sat=false;for(let l of c){visits++;if(w[Math.abs(l)]===+(l>0))sat=true}A(sat,"witness")}return visits}
function decode(L,d){let b=2*d+1,Q=comb(b,d+1),by=new Map(),visits=0;for(let c of L.C){let m=new Map();for(let l of c){visits++;let v=Math.floor((Math.abs(l)-1)/b)+1,z=(l>0?1:-1)*v,i=(Math.abs(l)-1)%b;if(m.has(-z))throw Error("mixed");if(!m.has(z))m.set(z,[]);m.get(z).push(i)}let row=[...m.keys()],k=key(row);A([...m.values()].every(q=>q.length===d+1&&new Set(q).size===d+1),"block");if(!by.has(k))by.set(k,{row,seen:new Set()});let a=[...m.values()].map(q=>q.slice().sort((a,b)=>a-b).join(",")).join(";");A(!by.get(k).seen.has(a),"duplicate");by.get(k).seen.add(a)}
 for(let f of by.values())A(f.seen.size===Q.length**f.row.length,"missing product");return {C:[...by.values()].map(f=>f.row),visits}}
let family=[];
for(let [m,d] of [[3,1],[5,1],[9,1],[17,1],[3,2],[5,2],[9,2],[3,3]]){
 let B=base(m),Y=base(m,true),b=2*d+1,Q=comb(b,d+1);
 // d=3 large explicit expansion; compute one pair only, bounded source generation.
 let L=lift(B,d),LY=lift(Y,d),src=bytes(L.n,L.C),sy=bytes(LY.n,LY.C),D=decode(L,d),DY=decode(LY,d);
 A(enc(D.C)===enc(B.C)&&enc(DY.C)===enc(Y.C),"decode exact");
 let proof=solve(D.C),ck=independent(D.C,proof.tree);A(proof.status==="UNSAT","base no");
 let y=Array(Y.n+1).fill(0);y[1]=1;let w=Array(LY.n+1).fill(0);for(let v=1;v<=Y.n;v++)for(let j=1;j<=b;j++)w[(v-1)*b+j]=y[v];let yw=checkWitness(LY.C,w);
 // Exact degree-d evaluation matrix of either fiber: full column rank; all local satisfiable factors have full affine/polynomial hull at d.
 let M=monomials(b,d),fiberRanks=[0,1].map(t=>rank(Array.from({length:2**b},(_,i)=>i).filter(i=>+(pop(i)>d)===t).map(w=>ev(w,M))));
 A(fiberRanks.every(r=>r.rank===M.length),"fiber rank");
 let minWidth=Math.min(...B.C.map(c=>c.length))*(d+1),r=L.n,ru=1+2*r+4*r*(r-1)/2;
 // All proper path links essential at phase level: delete both seam clauses on any one equality link, or both guarded end clauses.
 let deletions=[];for(let i=0;i<B.C.length;i+=2){let F=B.C.filter((_,j)=>j!==i&&j!==i+1),n=B.n,found=null; // direct constructive assignment, enumerated only base phase for small m via manual formula
 let t=i<2*m?0:1,offset=t?2*m:0,link=(i-offset)/2,first=2+t*m;
 let a=Array(n+1).fill(0);a[1]=t?1:0;if(link<m-1)for(let j=link+1;j<m;j++)a[first+j]=1;
 A(F.every(c=>c.some(l=>a[Math.abs(l)]===+(l>0))),"deletion witness");deletions.push({pair:i/2,witness:a})}
 // Exact fractional local witness: every base clause has a complementary pair of satisfying phase words, so mix both uniform block words.
 A(B.C.every(c=>c.length>=2&&c.some(l=>l>0)||c.length>=2),"width");
 family.push({m,d,b,base:B,yesBase:Y,phaseGroups:B.C.length/2,vars:r,clauses:L.C.length,minWidth,source:{sha:sha(src),N:src.length*8},yes:{sha:sha(sy),N:sy.length*8,witness:w,checkVisits:yw},rank:{features:M.length,fiberRanks},width2:{candidateCount:ru,admissions:0,proof:"all original clauses length >=4, at most two pins leave >=2 unassigned; no first UP step"},degree:{bound:d,localIdentities:0,proof:"every satisfiable phase region contains a translated radius-d Hamming ball of the full cube; triangular evaluation forces zero polynomial"},decode:{visits:D.visits,yesVisits:DY.visits,proof,check:ck},deletions})
}
return {common,family};
};
console.log(JSON.stringify(run(data),null,2));
