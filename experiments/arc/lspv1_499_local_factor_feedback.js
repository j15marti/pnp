"use strict";
// LSPV-1/499. Finite independent native-rule checks for Res(PC_1/F_2).
// NOT historical R_mix341. Run: node experiments/arc/lspv1_499_local_factor_feedback.js
function run(){
  const eq=(m,r)=>m*2+r, truth=(m,r,a)=>((pop(m&a)&1)===r);
  function pop(v){let n=0;for(;v;v>>=1)n+=v&1;return n;}
  const d=(a,scope=7)=>new Set([0,1,2].filter(i=>scope&(1<<i)).map(i=>eq(1<<i,1-((a>>i)&1))));
  const addset=(a,b)=>new Set([...a,...b]);
  const equal=(a,b)=>a.size===b.size&&[...a].every(v=>b.has(v));
  const B=[0,1,2].map(i=>new Set([eq(1<<i,0),eq(1<<i,1)]));
  let lines=[],counter={};let n=0;
  function add(rule,out,parents=[],arg=null){
    const c=new Set(out);if(parents.some(p=>p<0||p>=lines.length))throw Error("bad reference");
    if(rule==="bool"){if(parents.length||!equal(c,B[arg]))throw Error("bad bool");}
    else if(rule==="source"){if(parents.length)throw Error("bad source");}
    else if(rule==="weak"){if(parents.length!==1||[...lines[parents[0]]].some(v=>!c.has(v)))throw Error("bad weak");}
    else if(rule==="combine"){
      if(parents.length!==2||!arg||arg.length!==2)throw Error("bad rule");
      const [f,g]=arg,[p,q]=parents;
      if(!lines[p].has(f)||!lines[q].has(g))throw Error("absent premise equation");
      const expect=addset(new Set([...lines[p]].filter(x=>x!==f)),new Set([...lines[q]].filter(x=>x!==g)));
      expect.add(f^g);
      if(!equal(c,expect))throw Error("bad combine");
    }else if(rule==="delete"){
      if(parents.length!==1||!lines[parents[0]].has(eq(0,1)))throw Error("bad delete");
      const expect=new Set([...lines[parents[0]]].filter(v=>v!==eq(0,1)));
      if(!equal(expect,c))throw Error("bad delete result");
    }else throw Error("unknown rule");
    lines.push(c);counter[rule]=(counter[rule]||0)+1;n++;return lines.length-1;
  }
  const bid=B.map((c,i)=>add("bool",c,[],i));
  function fromEq(src,m,r,a){
    if(truth(m,r,a))throw Error("true source cannot exclude assignment");
    const D=d(a), coords=[];
    for(let i=0;i<3;i++)if(m&(1<<i)){
      let f=eq(1<<i,(a>>i)&1);
      coords.push([add("weak",addset(D,new Set([f])),[bid[i]]),f]);
    }
    let k;
    if(coords.length){
      let [p,f]=coords[0];
      for(let j=1;j<coords.length;j++){
        const [q,g]=coords[j],h=f^g;
        p=add("combine",addset(D,new Set([h])),[p,q],[f,g]);f=h;
      }
      k=add("combine",addset(D,new Set([eq(0,1)])),[src,p],[eq(m,r),f]);
    }else k=add("weak",addset(D,new Set([eq(0,1)])),[src]);
    return add("delete",D,[k]);
  }
  let forbidden=0;
  for(let m=0;m<8;m++)for(let r=0;r<=1;r++){
    const s=add("source",new Set([eq(m,r)]));
    for(let a=0;a<8;a++)if(!truth(m,r,a)){
      const k=fromEq(s,m,r,a);if(!equal(lines[k],d(a)))throw Error("minterm mismatch");forbidden++;
    }
  }
  const x=add("source",new Set([eq(3,0)])),y=add("source",new Set([eq(3,1)]));
  let live=new Map();
  for(let a=0;a<8;a++)live.set(a,truth(3,0,a)?fromEq(y,3,1,a):fromEq(x,3,0,a));
  for(let i=0;i<3;i++){
    let next=new Map();
    for(const [a,p] of live)if(!(a&(1<<i))){
      const q=live.get(a|(1<<i)),f=eq(1<<i,1),g=eq(1<<i,0);
      const tail=addset(new Set([...lines[p]].filter(v=>v!==f)),new Set([...lines[q]].filter(v=>v!==g)));
      const v=add("combine",addset(tail,new Set([eq(0,1)])),[p,q],[f,g]);
      next.set(a,add("delete",tail,[v]));
    }
    live=next;
  }
  if(live.size!==1||lines[[...live.values()][0]].size)throw Error("no contradiction");
  const small=add("source",d(3,3));let factorControls=0;
  for(let a of [3,7]){let k=add("weak",d(a),[small]);if(!equal(lines[k],d(a)))throw Error("bad factor");factorControls++;}
  let total=0,implied=0;
  for(let A=0;A<256;A++)for(let C=0;C<256;C++){total++;if((A&(~C&255))===0)implied++;}
  if(total!==65536||implied!==6561||forbidden!==64)throw Error("exhaustion error");
  let rejected=0;
  const mutants=[
    ()=>add("weak",new Set(),[small]),
    ()=>add("combine",new Set([eq(0,1)]),[x,y],[eq(3,1),eq(3,1)]),
    ()=>add("delete",new Set(),[small]),
    ()=>add("weak",d(0),[lines.length+1]),
    ()=>add("bool",d(0),[],0)];
  for(let fn of mutants){try{fn();}catch(e){rejected++;continue;}throw Error("mutation accepted");}
  return {model:"syntactic Res(PC_1/F2), local 3-support feedback, not R_mix341",
    affine_cases:16,affine_forbidden_minterms:forbidden,factor_implication_pairs_exhaustive:total,
    true_factor_implications:implied,nodes:n,counts:counter,contradiction_sink:[...live.values()][0],
    factor_weakening_controls:factorControls,hostile_rejections:rejected,status:"PASS finite controls; no historical checker or external asymptotic theorem replay"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
