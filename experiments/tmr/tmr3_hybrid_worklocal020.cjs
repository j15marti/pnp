'use strict';
// Directly executed hosted V8 functions, reproducible in Node.js.
// Models local physical reads/writes after a symbolic preprocessing fixture.
function sourceSymbol(x,j){return j===0?"<":j===x.length+1?">":j>=1&&j<=x.length?x[j-1]:"_"}

function workSymbol(t,j){return t.has(j)?t.get(j):"_"}

function precompute(x,mode){
  const L=x.length, val=parseInt(x,2), tape=new Map();
  if(mode==="copy"||mode==="mirror"||mode==="xor"){let parity=0;for(let i=0;i<L;i++){parity^=+x[i];tape.set(i+1,mode==="copy"?x[i]:mode==="mirror"?x[L-1-i]:String(parity));}}
  if(mode==="parity")tape.set(0,String([...x].reduce((a,b)=>a+(+b),0)%2));
  const sh=mode==="far"?-5*L-val:mode==="center"?Math.floor((L+1)/2):mode==="mirror"?L+1:1;
  const wh=mode==="far"?8*L+val:mode==="copy"?Math.floor((L+1)/2):mode==="mirror"?L:mode==="xor"?1:0;
  const q=[...x].reduce((a,b)=>a+(+b),0)%3;
  const ends=[0,wh,...tape.keys()],low=Math.min(...ends),high=Math.max(...ends),s=high-low+1;
  return {sh,wh,q,tape,s};
}

function fp(x,c,t){
 const b=(h,read)=>Array.from({length:2*t+1},(_,i)=>read(h+i-t)).join("");
 const pos=c.sh< -t?"LEFT":c.sh>x.length+1+t?"RIGHT":String(c.sh);
 return JSON.stringify([c.q,pos,b(c.sh,j=>sourceSymbol(x,j)),b(c.wh,j=>workSymbol(c.tape,j))]);
}

function querySymbol(p,i){let b=p.toString(2);return i===0?"<":i===b.length+1?">":i>=1&&i<=b.length?b[i-1]:"_"}

function trace(x,c,p,t){
 let sh=c.sh,wh=c.wh,q=c.q,qi=0,tape=new Map(c.tape),out=[];
 for(let step=0;step<t;step++){
  const a=sourceSymbol(x,sh),b=workSymbol(tape,wh),z=querySymbol(p,qi);
  const seed=q*31+a.charCodeAt(0)*7+b.charCodeAt(0)*11+z.charCodeAt(0)*17;
  const sm=seed%3-1,wm=Math.floor(seed/3)%3-1,qm=Math.floor(seed/9)%3-1;
  const write=["0","1","_"][Math.floor(seed/27)%3],nq=(q+seed)%17,halt=seed%41===0,ans=seed%2?"SAT":"UNSAT";
  out.push([q,a,b,z,sm,wm,qm,write,nq,halt?ans:null]);
  tape.set(wh,write);sh+=sm;wh+=wm;qi+=qm;q=nq;
  if(halt)break;
 }
 return JSON.stringify(out);
}

function sensingCounterexample(){
 const hA=[0,0],hB=[0,1],t=1;
 const windows=h=>h.map(j=>Array.from({length:2*t+1},(_,i)=>workSymbol(new Map(),j+i-t)).join(""));
 if(JSON.stringify(windows(hA))!==JSON.stringify(windows(hB)))throw Error("naive windows do not coincide");
 if(hA[0]===hA[1] && hB[0]!==hB[1] && (hA[1]-hA[0])!==(hB[1]-hB[0]))return {naive_local_views_equal:true,collision_A:true,collision_B:false,offset_A:0,offset_B:1};
 throw Error("hostile collision case failed");
}

function run(){
 const n={case_count:0,subset_cases:0,work_cap_branch:0,local_branch:0,collisions:0,queries_replayed:0,transitions_replayed:0,far_source_collisions:0,work_cache_collisions:0,assert_failures:0},examples=[];
 for(let L=3;L<=9;L++){const xs=Array.from({length:1<<L},(_,i)=>i.toString(2).padStart(L,"0"));
 for(const mode of ["empty","parity","copy","xor","mirror","center","far"])for(let t=0;t<=3;t++){
  n.case_count++;let bkt=new Map(),S=0;
  for(const x of xs){const c=precompute(x,mode);S=Math.max(S,c.s);const k=fp(x,c,t);if(!bkt.has(k))bkt.set(k,[]);if(bkt.get(k).length<2)bkt.get(k).push({x,c});}
  const logstore=3*Math.log2(2*S+3)+S*Math.log2(3),loglocal=(2*t+1)*Math.log2(4);
  if(logstore<loglocal)n.work_cap_branch++;else n.local_branch++;
  if(S<=L)n.subset_cases++;
  for(const arr of bkt.values()){if(arr.length!==2)continue;const [a,b]=arr;
   if(a.x===b.x)throw Error("same input collision");
   const p=[...a.x].findIndex((v,i)=>v!==b.x[i])+1;
   n.collisions++;if(mode==="far")n.far_source_collisions++;if(["copy","xor","mirror"].includes(mode))n.work_cache_collisions++;
   for(const j of new Set([p,1,L,Math.floor((L+1)/2)])){let z=trace(a.x,a.c,j,t),y=trace(b.x,b.c,j,t);
    if(z!==y)throw Error(`coupling failed ${L}/${mode}/${t}/${a.x}/${b.x}/${j}`);
    n.queries_replayed++;n.transitions_replayed+=JSON.parse(z).length;
   }
   if(examples.length<9)examples.push({L,mode,t,x:a.x,y:b.x,p,preprocessing_work_cells_a:a.c.s,preprocessing_work_cells_b:b.c.s});
  }
 }}
 return {label:"TMR-3/020 hybrid local/configuration work-info capacity",status:"COMPUTATIONAL",source:"direct hosted V8 execution",counts:n,geometry:sensingCounterexample(),examples}
}

console.log(JSON.stringify(run(),null,2));
