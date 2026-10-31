// ARC-MULTIPIN-WARM-CACHE272: deterministic restricted-source both-label controls.
// Reproduce in Node.js: node arc_multipin_cache272.js > arc_multipin_cache272_raw.json
"use strict";
const Q=[3,4,8,16,32], statuses=["allzero","lastone","alternating"];
const id=(x)=>x>0?x:-x, P=(q)=>Math.ceil(Math.pow(q,5/3)), H=(q)=>Math.max(1,Math.ceil(Math.sqrt(P(q)/Math.log2(q+2))));
function forcing(v,a,b){let out=[];for(let s of [-1,1])for(let t of [-1,1])out.push([v,s*a,t*b]);return out;}
function build(q,b,childIndex=null){
 let c=[],n,tag=[];
 function add(x,s){c.push(x);tag.push(s);}
 if(childIndex===null){
  n=q===3?12:2*q+6;
  forcing(1,3,4).forEach(x=>add(x,"force_t"));
  forcing(-2,5,6).forEach(x=>add(x,"force_not_p"));
  for(let j=0;j<q;j++)add([b[j]?1:-1,-(10+j),2],"pin_"+j);
  if(q===3)add([10,11,12],"OR");
  else {add([10,11,10+q],"OR_0");for(let j=0;j<q-4;j++)add([-(10+q+j),12+j,11+q+j],"OR_"+(j+1));
    add([-(10+q+q-4),8+q,9+q],"OR_last");}
  for(let i=0;i<P(q);i++)add([7,8,9],"pad_"+i);
 }else{
  let p=H(q);n=9+3*p;
  forcing(1,4,5).forEach(x=>add(x,"force_t"));
  forcing(-2,6,7).forEach(x=>add(x,"force_not_p"));
  forcing(3,8,9).forEach(x=>add(x,"force_r"));
  add([b[childIndex]?1:-1,-3,2],"child_pin");
  for(let i=0;i<p;i++)add([10+3*i,11+3*i,12+3*i],"child_pad_"+i);
 }
 return {q,n,c,tag,childIndex,model:childIndex===null?"source":"child"};
}
function litFormat(l,w){const d=String(Math.abs(l)).padStart(w-1,"0");return l<0?"-"+d:"0"+d;}
function serialize(f){const w=String(f.n).length+1,h="p cnf "+f.n+" "+f.c.length+"\n";
 const cl=x=>x.map(l=>litFormat(l,w)).join(" ")+" 0\n";
 return {value:h+f.c.map(cl).join(""),head:h,width:w,stride:3*w+5};}
function validate(f){return f.c.every(c=>c.length===3&&new Set(c.map(id)).size===3&&c.every(l=>id(l)<=f.n&&id(l)>0));}
function solver(f){
 let nodes=0,tests=0,contradictions=0;
 function go(a){nodes++;
  while(true){let changed=false, allsat=true;
   for(const c of f.c){let sat=false,num=0,unit=0;
    for(const l of c){tests++;let x=a[id(l)];if(x===null){num++;unit=l;}else if(x===(l>0?1:0)){sat=true;break;}}
    if(sat)continue;allsat=false;
    if(num===0){contradictions++;return null;}
    if(num===1){let v=id(unit),value=unit>0?1:0;if(a[v]!==null&&a[v]!==value){contradictions++;return null;}
       if(a[v]===null){a[v]=value;changed=true;}}
   }
   if(allsat)return a;
   if(!changed)break;
  }
  let branch=0;
  for(const c of f.c){let sat=false;for(const l of c){let x=a[id(l)];if(x!==null&&x===(l>0?1:0)){sat=true;break;}}
   if(!sat){for(const l of c)if(a[id(l)]===null){branch=id(l);break;}if(branch)break;}}
  if(!branch)return a;
  for(const b of [0,1]){let a2=a.slice();a2[branch]=b;const r=go(a2);if(r)return r;}return null;
 }
 const witness=go(Array(f.n+1).fill(null));return {sat:!!witness,nodes,tests,contradictions,witness:witness?witness.map(x=>x??0).slice(1):null};
}
function counts(f,a){let N=[0,0,0,0],vec=[];for(const c of f.c){let t=c.filter(l=>a[id(l)-1]===(l>0?1:0)).length;N[t]++;vec.push(t);}return{N,vec,sat:N[0]===0};}
function extreme(c){return c.map(l=>({variable:id(l),literal:l,S:l>0?1:0,invertS:l>0?0:1,U:l>0?0:1,invertU:l>0?1:0}));}
function compatibility(c,d){
 let same=false,opposite=false;
 for(const l of c)for(const r of d)if(id(l)===id(r)){if(Math.sign(l)===Math.sign(r))same=true;else opposite=true;}
 const expected={SS:!opposite,SU:!same,US:!same,UU:!opposite};
 let empirical={SS:false,SU:false,US:false,UU:false};
 const v=[...new Set([...c,...d].map(id))], max=1<<v.length;
 for(let a=0;a<max;a++){const x={};v.forEach((w,i)=>x[w]=(a>>i)&1);
  let t=c.filter(l=>x[id(l)]===(l>0?1:0)).length,u=d.filter(l=>x[id(l)]===(l>0?1:0)).length;
  if(t===3&&u===3)empirical.SS=true;if(t===3&&u===0)empirical.SU=true;
  if(t===0&&u===3)empirical.US=true;if(t===0&&u===0)empirical.UU=true;
 }
 if(Object.keys(expected).some(k=>expected[k]!==empirical[k]))throw Error("pair compatibility");
 return {expected,same,opposite};
}
function proofUnsat(f,q){
 const nodes=f.c.map((cl,i)=>({id:i+1,cl,sourceClause:i+1})), steps=[];
 const clause=i=>nodes[i-1].cl;
 function res(a,b,v){let A=clause(a),B=clause(b);if(!((A.includes(v)&&B.includes(-v))||(A.includes(-v)&&B.includes(v))))throw Error("bad pivot");
  const z=[...new Set([...A,...B].filter(x=>id(x)!==v))].sort((x,y)=>id(x)-id(y)||x-y);
  if(z.some(x=>z.includes(-x)))throw Error("tautology");
  nodes.push({id:nodes.length+1,cl:z,parents:[a,b],pivot:v});steps.push(nodes[nodes.length-1]);return nodes.length;}
 const ta=res(res(1,2,4),res(3,4,4),3);
 const np=res(res(5,6,6),res(7,8,6),5);
 if(JSON.stringify(clause(ta))!=="[1]"||JSON.stringify(clause(np))!=="[-2]")throw Error("forced units");
 const neg=[];
 for(let j=0;j<q;j++){
  const r1=res(ta,9+j,1),r2=res(r1,np,2);if(JSON.stringify(clause(r2))!==JSON.stringify([-(10+j)]))throw Error("neg pin");neg.push(r2);
 }
 let cur=9+q, next=10+q;
 for(let j=0;j<q;j++){
   cur=res(cur,neg[j],10+j);
   if(j<q-1&&clause(cur).length===1&&clause(cur)[0]>0&&id(clause(cur)[0])>=10+q){
     cur=res(cur,next,clause(cur)[0]);next++;
   }
 }
 if(clause(cur).length)throw Error("not empty");
 return {sourceClauses:f.c.length,steps:steps.length,finalNode:cur,root:clause(cur),steps:steps.map(x=>({id:x.id,parents:x.parents,pivot:x.pivot,cl:x.cl}))};
}
function oracle(f,sourceSerial,j,address){
 const p=H(f.q),c=build(f.q,Array(f.q).fill(false),j),desc=serialize(c),h=desc.head.length,d=desc.stride;
 if(address<0||address>=desc.value.length)return " ";
 if(address<h)return desc.head[address];
 let k=Math.floor((address-h)/d),r=(address-h)%d;
 let cl=c.c[k];
 if(k===12){const src=serialize(f);const sign=sourceSerial[src.head.length+(8+j)*src.stride];cl=[sign==="-"?-1:1,-3,2];}
 return (cl.map(l=>litFormat(l,desc.width)).join(" ")+" 0\n")[r];
}
const cases=[], assertions={labels:0,oracle:0,pairs:0,complements:0,proof:0,witnesses:0};
for(const q of Q)for(const mode of statuses){
 const b=Array.from({length:q},(_,i)=>mode==="lastone"?i===q-1:mode==="alternating"?i%2===0:false);
 const f=build(q,b),src=serialize(f),baseline=solver(f);
 if(!validate(f)||baseline.sat!==b.some(Boolean))throw Error("source label");
 const children=Array.from({length:q},(_,j)=>solver(build(q,b,j)));
 if(children.some((r,j)=>r.sat!==b[j])||children.some(r=>r.nodes<1)||baseline.sat!==children.some(r=>r.sat))throw Error("child label");assertions.labels+=q+1;
 function checkedWitness(g,w){if(!w||!g.c.every(c=>c.some(l=>w[id(l)-1]===(l>0?1:0))))throw Error("invalid original or child witness");assertions.witnesses++;}
 if(baseline.sat)checkedWitness(f,baseline.witness);
 children.forEach((v,j)=>{if(v.sat)checkedWitness(build(q,b,j),v.witness);});
 const zero=counts(f,Array(q===3?12:2*q+6).fill(0)),one=counts(f,Array(f.n).fill(1));
 if(zero.vec.some((t,j)=>t+one.vec[j]!==3))throw Error("complements");assertions.complements+=f.c.length;
 const flips=[];let a=Array(f.n).fill(0);for(const variable of [1,2,10,11]){a[variable-1]^=1;let s=counts(f,a);flips.push({flipped:variable,N:s.N,sat:s.sat});}
 let pairs=[],occ=[];
 const limit=q<=8?f.c.length:Math.min(20,f.c.length);
 for(let j=0;j<limit;j++){occ.push({index:j+1,tag:f.tag[j],extremes:extreme(f.c[j])});for(let k=j+1;k<limit;k++){pairs.push({j:j+1,k:k+1,...compatibility(f.c[j],f.c[k])});assertions.pairs++;}}
 const oracleIndex=[0,1,13,1000];const tested=q<=8?Array.from({length:serialize(build(q,b,0)).value.length+2},(_,i)=>i-1):oracleIndex;
 for(let j of [...new Set([0,q-1])]){const child=serialize(build(q,b,j));for(let i of tested){if(oracle(f,src.value,j,i)!==(child.value[i]??" "))throw Error("oracle "+q+"/"+j+"/"+i);assertions.oracle++;}}
 let proof=null;if(mode==="allzero"){proof=proofUnsat(f,q);assertions.proof+=proof.steps.length;}
 cases.push({q,mode,pins:b.map(Number),sourceBits:src.value.length*8,childBits:serialize(build(q,b,0)).value.length*8,
 qChildren:q,padSource:P(q),padChild:H(q),baseline:{sat:baseline.sat,nodes:baseline.nodes,tests:baseline.tests,contradictions:baseline.contradictions,witness:baseline.witness},
 childTotals:{witnesses:children.map(r=>r.witness),nodes:children.reduce((s,r)=>s+r.nodes,0),tests:children.reduce((s,r)=>s+r.tests,0),
  contradictions:children.reduce((s,r)=>s+r.contradictions,0)},
 matchedLabel:baseline.sat,sourceScanBytes:src.value.length,requestedPinSourceReads:q,
 zero:{N:zero.N,counts:q<=8?zero.vec:null},one:{N:one.N,counts:q<=8?one.vec:null},flipTrail:flips,
 diagnostics:{pairScope:limit,occurrences:occ,pairs},proof:proof&&q<=8?proof:{steps:proof?.steps||0,final:proof?.root||null}});
}
const result={title:"ARC-MULTIPIN-WARM-CACHE272",datePacific:"2026-10-31 05:36 PDT",epistemic:"COMPUTATIONAL; restricted formal lemma in accompanying report; P vs NP OPEN",seed:null,deterministic:true,
 specification:{q:Q,modes:statuses,padSource:"ceil(q^(5/3))",padChild:"ceil(sqrt(padSource/log2(q+2)))",encoding:"DIMACS-compatible, fixed-width signed decimal literals with leading zeroes, 3W+5 bytes per clause",
  machineCaveat:"JavaScript solver operation proxies only; not native FLMV machine transitions"},
 assertions,cases};
function run(){return result}
if(typeof module!=="undefined"&&module?.exports)module.exports={run,build,solver,serialize,proofUnsat,compatibility,oracle};
if(typeof process!=="undefined"&&process?.stdout&&require.main===module)process.stdout.write(JSON.stringify(result,null,2)+"\n");
