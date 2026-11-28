const fs=require('node:fs');
const run=function run(native){
 const {sha}=new Function(native+";return {sha};")(),A=(x,m)=>{if(!x)throw Error(m)},enc=x=>JSON.stringify(x)+"\n",hex=x=>x.toString(16);
 function solve(B,b,mode,cap=2048){
  let work={basisSteps:0,xor:0,coordinateSteps:0,union:0,score:0,transitions:0,verify:0},d=B.length;
  function insert(M,x){while(x){work.basisSteps++;let p=x&-x;if(!M.has(p)){M.set(p,x);return}x^=M.get(p);work.xor++}}
  function membership(M,x){while(x){work.basisSteps++;let p=x&-x;if(!M.has(p))return false;x^=M.get(p);work.xor++}return true}
  let offsets=B.map(S=>S[0]),D=B.map((S,i)=>S.map(x=>x^offsets[i])),target=b^offsets.reduce((a,c)=>a^c,0n);
  let order=B.map((_,i)=>i),groups=null,coordRank=null;
  if(mode==="direct-sum"){
   let R=new Map(),rank=0;
   // Keep coordinates in the original selected-column basis; tags pay for each elimination.
   for(let S of D)for(let v of S){let u=v,t=0n;while(u){work.coordinateSteps++;let p=u&-u;if(!R.has(p)){R.set(p,[u,t^(1n<<BigInt(rank++))]);break}let [x,z]=R.get(p);u^=x;t^=z;work.xor+=2}}
   function coords(v){let t=0n;while(v){work.coordinateSteps++;let p=v&-v;if(!R.has(p))return null;let [x,z]=R.get(p);v^=x;t^=z;work.xor+=2}return t}
   let q=coords(target);if(q===null)return {mode,decision:"NO",reason:"target outside affine span",work};
   let E=D.map(S=>S.map(coords)),p=Array.from({length:d+rank},(_,i)=>i),root=i=>{while(p[i]!==i){work.union++;i=p[i]}return i},join=(a,b)=>{work.union++;p[root(a)]=root(b)};
   for(let i=0;i<d;i++)for(let v of E[i]){while(v){let z=v&-v;join(i,d+z.toString(2).length-1);v^=z}}
   let G=new Map();for(let i=0;i<d;i++){let r=root(i);if(!G.has(r))G.set(r,[]);G.get(r).push(i)}
   groups=[...G.values()];order=groups.flat();coordRank=rank;
  }else if(mode==="row-greedy"){
   let support=D.map(S=>S.reduce((a,v)=>a|v,0n)),rows=new Map();for(let i=0;i<d;i++){let s=support[i];while(s){let p=s&-s;if(!rows.has(p))rows.set(p,[]);rows.get(p).push(i);s^=p}}
   let br=D.map(()=>[]);for(let [r,bb] of rows)for(let i of bb)br[i].push(r);let used=new Set(),left=new Map([...rows].map(([r,bb])=>[r,bb.length])),rem=new Set(order);order=[];
   while(rem.size){let best=-1,delta=Infinity,touch=-1;for(let i of rem){let a=0,b=0;for(let p of br[i]){work.score++;if(used.has(p)&&left.get(p)===1)a--;else if(!used.has(p)&&left.get(p)>1)a++;if(used.has(p))b++}if(a<delta||(a===delta&&b>touch)){best=i;delta=a;touch=b}}order.push(best);rem.delete(best);for(let p of br[best]){used.add(p);left.set(p,left.get(p)-1)}}
  }
  let suffix=Array(d+1);suffix[d]=new Map();for(let i=d-1;i>=0;i--){let M=new Map(suffix[i+1]);for(let v of D[order[i]])insert(M,v);suffix[i]=M}
  let pre=new Map(),w=[0];for(let i=0;i<d;i++){for(let v of D[order[i]])insert(pre,v);w.push(pre.size+suffix[i+1].size-suffix[0].size)}
  let S=new Map([[0n,[]]]),peak=1,stop=null,status="UNKNOWN";
  outer:for(let i=0;i<d;i++){let Q=new Map();for(let [u,p] of S)for(let j=0;j<D[order[i]].length;j++){work.transitions++;let v=u^D[order[i]][j];if(membership(suffix[i+1],target^v)&&!Q.has(v)){Q.set(v,[...p,j]);if(Q.size>cap){stop=i;peak=cap+1;break outer}}}S=Q;peak=Math.max(peak,S.size);if(!S.size){status="NO";break}}
  let witness=null;if(stop===null&&status!=="NO"){status=S.has(target)?"YES":"NO";if(status==="YES"){witness=S.get(target);let q=0n;for(let i=0;i<d;i++){q^=B[order[i]][witness[i]];work.verify++}A(q===b,"lift")}}
  return {mode,decision:status,width:Math.max(...w),peak,stop,groups:groups?.map(g=>g.length),coordRank,order,witness,work};
 }
 let out=[];
 for(let k of [8,16,32,64])for(let yes of [false,true]){
  let q=3*k,seed=1947+k,st=seed,rnd=()=>{st=(Math.imul(st,1664525)+1013904223)>>>0;return st};
  let basis=Array.from({length:q},(_,i)=>1n<<BigInt(i));
  // Invertible dense mixing: change basis columns by elementary XOR operations.
  for(let t=0;t<q*12;t++){let a=rnd()%q,b=rnd()%q;if(a!==b)basis[a]^=basis[b]}
  // LCG low bits can be correlated; additional triangular dense mixing remains invertible.
  for(let i=1;i<q;i++)basis[i]^=basis[i-1];
  let left=[],right=[],target=0n;for(let i=0;i<k;i++){let [u,v,w]=basis.slice(3*i,3*i+3);left.push([0n,u,v]);right.push([0n,u,w]);target^=v^w;if(!yes&&i===k-1)target^=u}
  let B=[...left,...right],src={schema:"EXPLICIT-XOR-SUMSET-v1",dimension:q,target:hex(target),blocks:B.map(S=>S.map(hex))},raw=enc(src),h=sha(raw);
  let arms=["source","row-greedy","direct-sum"].map(mode=>solve(B,target,mode));let a=arms[2];A(a.decision===(yes?"YES":"NO")&&a.width===1&&a.groups.length===k&&a.groups.every(x=>x===2),"direct sum");
  // Independent source-derived proof of NO via component coordinate projection using dense bit elimination from original basis, with direct-sum decomposition certified by full rank.
  // Here checker regenerates exact source and verifies all original component sums (9 per component); basis generator is used for audit, not solver.
  let M=new Map();for(let v of basis){let u=v;while(u){let p=1n<<BigInt(u.toString(2).length-1);if(!M.has(p)){M.set(p,u);break}u^=M.get(p)}}A(M.size===q,"mix full rank");
  let local=0n,missing=0,checks=0;for(let i=0;i<k;i++){let [u,v,w]=basis.slice(3*i,3*i+3),t=v^w^(!yes&&i===k-1?u:0n);local^=t;let S=new Set();for(let x of left[i])for(let y of right[i]){S.add(x^y);checks++}if(!S.has(t))missing++}A(local===target&&missing===(yes?0:1),"independent local audit");
  out.push({problem_id:"EXPLICIT-XOR-SUMSET-v1",instance:`MIXED-CUT-${k}-${yes?"YES":"NO"}@${h.slice(0,12)}`,instance_id:"EXPLICIT-XOR-SUMSET-v1:sha256:"+h,original_N_bits:raw.length*8,source:src,original_ids:{blocks:[0,B.length-1],coordinateBits:[0,q-1]},guard_id:"EMPTY",residual_id:"ROOT",recipe:{k,yes,seed},arms,audit:{rank:M.size,checks,missing}})
 }
 return out;
};
console.log(JSON.stringify(run(fs.readFileSync(process.argv[2],'utf8')),null,2));
