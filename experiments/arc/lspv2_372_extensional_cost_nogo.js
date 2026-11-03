// LSPV-2 372. Node.js 18+, no packages. Finite hostile controls, not shortest-proof search.
"use strict";
function yes(b,m){if(!b)throw Error(m)}
function parse(s){
 let h=null,C=[],c=[];
 for(const line of s.split(/\r?\n/)){
  let q=line.trim();if(!q||/^c(\s|$)/.test(q))continue;
  if(/^p(\s|$)/.test(q)){
   let a=q.split(/\s+/);yes(!h&&a.length===4&&a[1]==="cnf"&&/^\d+$/.test(a[2])&&/^\d+$/.test(a[3]),"header");
   h={n:+a[2],m:+a[3]};yes(Number.isSafeInteger(h.n)&&Number.isSafeInteger(h.m),"header integer");continue;
  }
  yes(h,"header required");
  for(const t of q.split(/\s+/)){
   yes(/^-?\d+$/.test(t),"noninteger literal");
   let x=+t;yes(Number.isSafeInteger(x)&&Math.abs(x)<=h.n,"literal range");
   if(!x){yes(new Set(c.map(Math.abs)).size===c.length,"repeated variable");C.push(c);c=[]}else c.push(x);
  }
 }
 yes(h&&c.length===0&&C.length===h.m,"count/terminator");return{n:h.n,C};
}
function dim(n,C){return"p cnf "+n+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0\n").join("")}
function brute(n,C){yes(n<=16,"finite brute cap");let count=0;
 for(let a=0;a<2**n;a++)if(C.every(c=>c.some(l=>Boolean((a>>(Math.abs(l)-1))&1)===(l>0))))count++;
 return count;
}
function extract(C){
 let groups=new Map(),vars=new Set();
 for(const c of C){
  if(c.length!==3)return null;
  const v=c.map(Math.abs).sort((a,b)=>a-b);if(new Set(v).size!==3)return null;
  const key=v.join(",");if(!groups.has(key))groups.set(key,new Set());
  let b=0;for(let i=0;i<3;i++)if(c.includes(-v[i]))b|=1<<i;
  groups.get(key).add(b);v.forEach(x=>vars.add(x));
 }
 let ids=[...vars].sort((a,b)=>a-b),ix=new Map(ids.map((x,i)=>[x,i])),rows=[];
 for(const [key,vals] of groups){
  if(vals.size!==4)return null;let parity=null;
  for(const b of vals){let p=(b&1)^((b>>1)&1)^((b>>2)&1);
   if(parity===null)parity=p;else if(parity!==p)return null}
  let mask=0n;for(const x of key.split(",").map(Number))mask|=1n<<BigInt(ix.get(x));
  rows.push([mask,1^parity]);
 }
 return rows;
}
function gf(rows){
 let basis=new Map(),xor=0;
 for(const [mask,bit] of rows){
  let x=mask,b=bit;
  while(x){
   let pivot=x.toString(2).length-1;
   if(!basis.has(pivot)){basis.set(pivot,[x,b]);break}
   let v=basis.get(pivot);x^=v[0];b^=v[1];xor++;
  }
  if(!x&&b)return{sat:false,xor};
 }
 return{sat:true,xor};
}
function decide(src){
 let f;try{f=parse(src)}catch(_){return{label:"MALFORMED"}}
 let rows=extract(f.C);
 if(rows){let a=gf(rows);return{label:a.sat?"SAT":"UNSAT",method:"GF2",xors:a.xor}}
 if(f.n<=16)return{label:brute(f.n,f.C)?"SAT":"UNSAT",method:"BRUTE"};
 return{label:"FINITE_PROTOTYPE_LIMIT",method:"formal uniform total version has exhaustive fallback without cutoff"};
}
function graph(edges,odd){
 let h=1+Math.max(...edges.flat()),v=Array.from({length:h},()=>[]);
 edges.forEach(([a,b],i)=>{v[a].push(i+1);v[b].push(i+1)});
 yes(v.every(s=>s.length===3),"graph must be cubic");let C=[];
 for(let i=0;i<h;i++)for(let k=0;k<8;k++){
  let bits=[k&1,(k>>1)&1,(k>>2)&1];
  if((bits[0]^bits[1]^bits[2])!==(odd&&i===0?1:0))
    C.push(v[i].map((id,j)=>bits[j]?-id:id));
 }
 return{h,n:edges.length,C};
}
function run(){
 let assertions=0,bad=0,results=[];const ck=(b,m)=>{yes(b,m);assertions++};
 const graphs=[
 ["K4",[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],15],
 ["K33",[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]],23],
 ["cube",[[0,1],[0,2],[0,4],[1,3],[1,5],[2,3],[2,6],[3,7],[4,5],[4,6],[5,7],[6,7]],31],
 ["Petersen",[[0,1],[1,2],[2,3],[3,4],[4,0],[0,5],[1,6],[2,7],[3,8],[4,9],[5,7],[7,9],[9,6],[6,8],[8,5]],39]
 ];
 for(const [name,E,opt] of graphs){
  for(const odd of [false,true]){
   const F=graph(E,odd),src=dim(F.n,F.C),r=decide(src),cnt=brute(F.n,F.C);
   ck(!!extract(F.C),"recognition");ck(r.method==="GF2"&&r.label===(odd?"UNSAT":"SAT"),"GF2 label");
   ck(cnt===(odd?0:2**(F.n-F.h+1)),"brute model count");
   ck(F.C.length===4*F.h,"clause count");
   ck(decide(dim(F.n,[...F.C].reverse().map(c=>[...c].reverse()))).label===r.label,"reorder");
   const flips=F.C.map(c=>c.map(x=>Math.abs(x)===1?-x:x));
   ck(decide(dim(F.n,flips)).label===r.label,"variable complementation");
   const ren=F.C.map(c=>c.map(x=>Math.sign(x)*(F.n+1-Math.abs(x))));
   ck(decide(dim(F.n,ren)).label===r.label,"variable renaming");
   results.push({name,odd,variables:F.n,vertices:F.h,clauses:F.C.length,ascii_bytes:src.length,models:cnt,gauss_xors:r.xors,prior_certified_W_mix:odd?opt:null});
  }
  const F=graph(E,true),a=dim(F.n,F.C),b=dim(F.n,[[1],[-1]]),gap=a.length-b.length;
  ck(brute(F.n,parse(b).C)===0,"easy UNSAT same n");
  ck(decide(b).label==="UNSAT","fallback label");
  ck(gap>=4,"padding room");
  const pad=b+"c "+"x".repeat(gap-3)+"\n";
  ck(pad.length===a.length&&decide(pad).label==="UNSAT","same byte length");
 }
 const huge=dim(1000000000,[[999999997,999999998,999999999],[999999997,-999999998,-999999999],[-999999997,999999998,-999999999],[-999999997,-999999998,999999999]]);
 ck(decide(huge).method==="GF2"&&decide(huge).label==="SAT","active-id compression");
 const G=parse(dim(3,[[1],[2]])).C,Gp=parse(dim(3,[[1],[-1,2]])).C;
 for(let a=0;a<8;a++){
  const evalc=C=>C.every(c=>c.some(l=>Boolean((a>>(Math.abs(l)-1))&1)===(l>0)));
  ck(evalc(G)===evalc(Gp),"nonempty extensional pair");
 }
 for(const s of ["","p cnf 2 1\n1 0\n-1 0\n","p cnf x 1\n1 0\n","p cnf 2 1\n3 0\n","p cnf 2 1\n1\n","p cnf 2 1\n1 1 0\n","p cnf 2 1\n1 -1 0\n"]){
  ck(decide(s).label==="MALFORMED","malformed");bad++;
 }
 return{run:"LSPV2_EXTENSIONAL_COST_NOGO372",assertions,malformed_rejected:bad,fixtures:results.length,results,
 theorem:"Identical empty satisfying sets over n=3h/2 variables, while established exact W_Rmix341(F_oddTseitin)=4h-1 and W_Rmix341(H_n)=1",
 status:"PROVED/EXACT symbolically using inherited 341 theorem; COMPUTATIONAL finite controls",
 implementation_limit:"Finite prototype brute-force fallback n<=16. Formal general decider has unbounded exhaustive fallback. Not a polynomial-time worst-case SAT decider."};
}
if(typeof module!=="undefined"&&module.exports)module.exports={parse,extract,gf,decide,run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
