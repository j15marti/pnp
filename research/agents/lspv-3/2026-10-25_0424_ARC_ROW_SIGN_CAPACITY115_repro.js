#!/usr/bin/env node
'use strict';
// ARC-ROW-SIGN-CAPACITY115 reproducible ordinary proper-3CNF two-level audit.
// node research/agents/lspv-3/2026-10-25_0424_ARC_ROW_SIGN_CAPACITY115_repro.js
const run = function () {
  const summary={run_id:"ARC-ROW-SIGN-CAPACITY115",revision:"1.0.0",timestamp:"2026-10-25T11:24:35Z",seed:null,method:"deterministic exhaustive w=3 and selected w=4 exact CNF+DPLL; no stochastic sampling",assertions:0,failures:0,root_decisions:0,level1_decisions:0,level2_decisions:0,context_decisions:0,controls_decisions:0,instances_by_width:{},max_root_width:0,max_encoded_bits:0,source_sign_only_pairs:0,source_sign_flips_checked:0,source_lookups:0,labels:{root_sat:0,root_unsat:0,level1_sat:0,level1_unsat:0,level2_sat:0,level2_unsat:0},examples:[],model_scope:"ordinary proper signed 3CNF, indexed binary text; not FLMV instruction or peak-space measurement"};
  function check(c,m){summary.assertions++;if(!c){summary.failures++;throw Error(m);}}
  function freshPin(lit,alloc){const a=alloc(),b=alloc();return [[lit,a,b],[lit,a,-b],[lit,-a,b],[lit,-a,-b]];}
  function properClause(lits,alloc){if(lits.length===3)return [lits.slice()];check(lits.length>3,"nonproper long gate");let z=alloc(),out=[[lits[0],lits[1],z]];for(let i=2;i<lits.length-2;i++){const zn=alloc();out.push([-z,lits[i],zn]);z=zn;}out.push([-z,lits[lits.length-2],lits[lits.length-1]]);return out;}
  function build(w,mask){
    let next=w+2,clauses=[];const alloc=()=>++next,p=w+1,q=w+2,controls=[];
    clauses.push(...freshPin(-p,alloc));clauses.push(...freshPin(-q,alloc));
    for(let alpha=0;alpha<2**w;alpha++){
      const c=alloc(),allowed=(mask>>>alpha)&1;
      controls.push(clauses.length);
      clauses.push([allowed?c:-c,p,q]);
      const gate=[c];for(let i=0;i<w;i++)gate.push((alpha&(1<<i))?-(i+1):(i+1));
      clauses.push(...properClause(gate,alloc));
    }
    return {w,mask,n:next,clauses,controls};
  }
  function extend(f,pins){let next=f.n,clauses=f.clauses.map(c=>c.slice());const alloc=()=>++next;for(const lit of pins)clauses.push(...freshPin(lit,alloc));return{w:f.w,n:next,clauses};}
  function serialize(f){
    const h=Math.floor(Math.log2(2*Math.max(f.n,f.clauses.length)+1))+1;
    const b=(x)=>{check(Number.isInteger(x)&&x>=0&&x<2**h,"binary field overflow");return x.toString(2).padStart(h,"0");};
    let s="1".repeat(h)+"0"+b(f.n)+b(f.clauses.length);
    for(const cl of f.clauses){check(cl.length===3&&new Set(cl.map(Math.abs)).size===3,"not proper");for(const lit of cl)s+=b(2*(Math.abs(lit)-1)+(lit<0?1:0));}
    check(s.length===1+(3+3*f.clauses.length)*h,"size incorrect");return s;
  }
  function parse(s){
    let h=0;while(h<s.length&&s[h]==="1")h++;if(h===0||h>=s.length||s[h]!=="0")throw Error("malformed prefix");let k=h+1;
    const get=()=>{if(k+h>s.length)throw Error("truncated");const v=parseInt(s.slice(k,k+h),2);k+=h;return v;};
    const n=get(),m=get(),expectH=Math.floor(Math.log2(2*Math.max(n,m)+1))+1;
    if(h!==expectH||s.length!==1+(3+3*m)*h||n<3)throw Error("malformed length/header");
    const clauses=[];for(let j=0;j<m;j++){let cl=[];for(let z=0;z<3;z++){const v=get(),id=(v>>1)+1; if(id>n||id<1)throw Error("bad literal");cl.push((v&1)?-id:id);}if(new Set(cl.map(Math.abs)).size!==3)throw Error("repeated identifier");clauses.push(cl);}return{n,clauses};
  }
  function scope(f){
    let first=new Array(f.n+1).fill(-1),last=new Array(f.n+1).fill(-1);
    for(let j=0;j<f.clauses.length;j++)for(const lit of f.clauses[j]){const v=Math.abs(lit);if(first[v]===-1)first[v]=j;last[v]=j;}
    let count=f.w+2,max=count,next=f.w+3,opened=0;
    for(let j=0;j<f.clauses.length;j++){
      const os=[];for(let v=f.w+3;v<=f.n;v++)if(first[v]===j)os.push(v);
      for(const v of os){check(v===next++,"helper open order");count++;opened++;}
      max=Math.max(max,count);
      for(const v of os)check(last[v]>=j,"helper closed early");
      for(let v=f.w+3;v<=f.n;v++)if(last[v]===j)count--;
    }
    check(opened===f.n-(f.w+2),"helper completeness");check(count===f.w+2,"nonclosed helper");return max;
  }
  function decide(f,w){
    const clauses=f.clauses,n=f.n;
    function go(init){
      const a=init.slice();
      while(true){
        let changed=false,allSat=true;
        for(const cl of clauses){
          let sat=false,free=0,unit=0;
          for(const lit of cl){let val=a[Math.abs(lit)];if(val===0){free++;unit=lit;}else if((val===1)===(lit>0)){sat=true;break;}}
          if(sat)continue;allSat=false;if(free===0)return false;
          if(free===1){let v=Math.abs(unit),val=unit>0?1:2;if(a[v]!==0&&a[v]!==val)return false;if(a[v]===0){a[v]=val;changed=true;}}
        }
        if(allSat)return true;if(!changed)break;
      }
      let v=0;for(let k=1;k<=w;k++)if(a[k]===0){v=k;break;}
      if(!v){const count=new Uint16Array(n+1);for(const cl of clauses){let sat=cl.some(l=>a[Math.abs(l)]&&((a[Math.abs(l)]===1)===(l>0)));if(!sat)for(const lit of cl)if(a[Math.abs(lit)]===0)count[Math.abs(lit)]++;}let best=0;for(let k=1;k<=n;k++)if(a[k]===0&&count[k]>best){v=k;best=count[k];}}
      if(!v)return true;for(const x of [1,2]){let b=a.slice();b[v]=x;if(go(b))return true;}return false;
    }
    return go(new Uint8Array(n+1));
  }
  function expectedFirst(mask,w,x1){for(let k=0;k<2**w;k++)if((k&1)===x1&&((mask>>>k)&1))return true;return false;}
  function popcount(x){let k=0;while(x){k+=x&1;x>>>=1;}return k;}
  function join(a,b,share){
    check(a.w===b.w,"join width");const w=a.w,offset=share?a.n-w:a.n;
    let B=b.clauses.map(cl=>cl.map(l=>{let v=Math.abs(l);let id=share?(v<=w?v:offset+v):offset+v;return l>0?id:-id;}));
    return{n:share?a.n+b.n-w:a.n+b.n,clauses:a.clauses.concat(B)};
  }
  for(const w of [3,4]){
    const masks=w===3?Array.from({length:256},(_,i)=>i):[0,65535,0xAAAA,0x5555,0xF00F,0x0FF0,0x8421,0x1248,0xCCCC,0x3333,0x6996,0x9669,0x8001,0x7ffe];
    let prior=null,baseline=null;
    summary.instances_by_width[w]={relations:masks.length,all_relations_exhausted:w===3,source_variables:w,root_variables:w+6+(w-1)*2**w,root_clauses:8+w*2**w,headers_identical:true,supports_identical:true};
    for(const mask of masks){
      const f=build(w,mask);
      check(f.n===w+6+(w-1)*2**w,"variable count formula");check(f.clauses.length===8+w*2**w,"clause count formula");
      const str=serialize(f),q=parse(str);check(JSON.stringify(q.clauses)===JSON.stringify(f.clauses),"exact root bytes");check(q.n===f.n,"header variable count");
      const sw=scope(f);check(sw<=w+5,"scope width");summary.max_root_width=Math.max(sw,summary.max_root_width);
      summary.max_encoded_bits=Math.max(summary.max_encoded_bits,str.length);
      const layout=f.clauses.map(cl=>cl.map(Math.abs).join(",")).join(";");
      if(prior===null){prior=layout;baseline=serialize(build(w,0));}else check(prior===layout,"support mismatch");
      let flips=0;for(let i=0;i<str.length;i++)if(str[i]!==baseline[i])flips++;check(flips===popcount(mask),"source signs not sole changes");
      summary.source_sign_only_pairs++;summary.source_sign_flips_checked+=flips;
      const root=decide(q,w),wantRoot=mask!==0;summary.root_decisions++;summary.labels[root?"root_sat":"root_unsat"]++;check(root===wantRoot,"root SAT");
      const f1={};
      for(const x1 of [0,1]){
        const child=extend(f,[x1?1:-1]),bytes=serialize(child),parsed=parse(bytes);check(scope(child)<=w+5,"first scope");summary.max_encoded_bits=Math.max(summary.max_encoded_bits,bytes.length);
        const label=decide(parsed,w),want=expectedFirst(mask,w,x1);summary.level1_decisions++;summary.labels[label?"level1_sat":"level1_unsat"]++;check(label===want,"first label");
        check(bytes.length>str.length,"first copy+pin must grow");f1[x1]=child;
      }
      for(let beta=0;beta<2**w;beta++){
        const pins=[];for(let i=1;i<w;i++)pins.push((beta&(1<<i))?i+1:-(i+1));
        const child=extend(f1[beta&1],pins),bytes=serialize(child),parsed=parse(bytes);
        check(scope(child)<=w+5,"second scope");summary.max_encoded_bits=Math.max(summary.max_encoded_bits,bytes.length);
        const label=decide(parsed,w),want=((mask>>>beta)&1)===1;summary.level2_decisions++;summary.labels[label?"level2_sat":"level2_unsat"]++;check(label===want,"second full-pin semantics");
        check(bytes.length>serialize(f1[beta&1]).length,"second copy+pin must grow");summary.source_lookups++;
      }
      if(w===3&&[0,1,85,170,255].includes(mask))summary.examples.push({w,mask,root_sat:root,root_encoded_bits:str.length,scope_width:sw});
    }
  }
  const even=Array.from({length:8},(_,i)=>i).filter(i=>popcount(i)%2===0).reduce((z,i)=>z|(1<<i),0),odd=(255^even);
  const a=build(3,even),b=build(3,odd);
  const both=join(a,b,true),disjoint=join(a,b,false);
  check(decide(a,3)&&decide(b,3),"separate parity SAT");summary.controls_decisions+=2;
  check(!decide(both,3),"incompatible same-name parity modules must be UNSAT");summary.controls_decisions++;
  check(decide(disjoint,3),"incorrect private-name gluing SAT hostile");summary.controls_decisions++;
  for(let beta=0;beta<8;beta++){
    let context={w:3,n:3,clauses:[]};context=extend(context,Array.from({length:3},(_,j)=>(beta&(1<<j))?j+1:-(j+1)));
    const glued=join(a,context,true);
    const got=decide(parse(serialize(glued)),3);summary.context_decisions++;check(got===((even>>>beta)&1?true:false),"all-context named join");
  }
  let badRejected=false;try{parse("000");}catch(e){badRejected=true;}check(badRejected,"malformed header not rejected");
  summary.hostile_controls={same_named_even_odd_modules_sat:false,disjoint_name_even_odd_modules_sat:true,modules_separately_sat:true,full_pin_contexts:8,malformed_header_rejected:badRejected,parity_even_mask:even,parity_odd_mask:odd};
  summary.proved_results_not_machine_measurements=["fixed-support one-sign-bit-per-row 3CNF realization","two level exact both-label named pins (tested finite)","information-theoretic counting floor for all extensional rows (mathematical proof in report)"];
  check(summary.labels.root_sat>0&&summary.labels.root_unsat>0&&summary.labels.level1_sat>0&&summary.labels.level1_unsat>0&&summary.labels.level2_sat>0&&summary.labels.level2_unsat>0,"missing both labels");
  return summary;
};
console.log(JSON.stringify(run(),null,2));
