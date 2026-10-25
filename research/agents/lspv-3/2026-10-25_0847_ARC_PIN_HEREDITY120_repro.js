const test = function test(){
  const started="2026-10-25"; let checks=0;
  function assert(a,m){checks++;if(!a)throw Error("ASSERT: "+m);}
  const bit=(w,i)=>(w>>i)&1;
  const contains=(M,w)=>((M>>w)&1)!==0;
  const support=(a)=>a.reduce((m,w)=>m|(1<<w),0);
  const words=(M,n)=>Array.from({length:1<<n},(_,w)=>w).filter(w=>contains(M,w));
  function cojoin(P,Q,h,n,p){
    const L=words(P,n).filter(w=>p.every((v,i)=>v<0||bit(w,i)===v));
    const R=words(Q,n).filter(w=>p.every((v,i)=>v<0||bit(w,i)===v));
    return {exact:L.some(w=>R.includes(w)),coarse:L.some(u=>R.some(v=>h[u]===h[v])),L,R};
  }
  function pairWitness(P,Q,h,n){
    for(const u of words(P,n))for(const v of words(Q,n)){
      if(h[u]!==h[v])continue;
      const agreement=Array.from({length:n},(_,i)=>i).filter(i=>bit(u,i)===bit(v,i));
      const matching=words(P&Q,n).some(w=>agreement.every(i=>bit(w,i)===bit(u,i)));
      if(!matching)return {valid:false,u,v,agreement};
    }
    return {valid:true};
  }
  function pins(n){
    const a=[];
    for(let x=0;x<3**n;x++){let y=x,p=[];for(let j=0;j<n;j++){p.push(y%3-1);y=Math.floor(y/3);}a.push(p);}
    return a;
  }
  function safe(P,Q,h,n){return pins(n).every(p=>{const j=cojoin(P,Q,h,n,p);return j.exact===j.coarse;});}
  function partitions(n){
    const out=[],a=Array(n).fill(0);
    function rec(i,max){
      if(i===n){out.push(a.slice());return;}
      for(let v=0;v<=max+1;v++){a[i]=v;rec(i+1,Math.max(max,v));}
    }
    rec(1,0);return out;
  }
  const h2=partitions(4);assert(h2.length===15,"Bell(4)");
  let exhaust=0,unsafe=0,random=0;
  for(let P=0;P<16;P++)for(let Q=0;Q<16;Q++)for(const h of h2){
    const criterion=pairWitness(P,Q,h,2).valid;
    const actual=safe(P,Q,h,2);
    assert(criterion===actual,"all-pins pairwise iff n2 "+P+"/"+Q);
    exhaust++;if(!actual)unsafe++;
  }
  let seed=120;
  function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
  for(let j=0;j<1024;j++){
    const P=rnd()%256,Q=rnd()%256,h=Array.from({length:8},()=>rnd()%4);
    assert(pairWitness(P,Q,h,3).valid===safe(P,Q,h,3),"sampled n3 "+j);random++;
  }
  const P=support([0,3,7]),Q=support([1,3,7]),h=Array.from({length:8},(_,i)=>i>>1);
  const pre=pins(3);
  const j0=cojoin(P,Q,h,3,[-1,-1,-1]);
  const j1=cojoin(P,Q,h,3,[-1,-1,0]);
  const j2=cojoin(P,Q,h,3,[-1,0,0]);
  assert(j0.exact&&j0.coarse&&j1.exact&&j1.coarse&&!j2.exact&&j2.coarse,"two-level counterexample statuses");
  let pw=pairWitness(P,Q,h,3);
  assert(!pw.valid&&pw.u===0&&pw.v===1,"smallest expected separating pair");
  function bodyFor(M){
    let c=[];for(let w=0;w<8;w++)if(!contains(M,w))c.push(Array.from({length:3},(_,i)=>bit(w,2-i)?-(i+1):i+1));
    return c;
  }
  function pin(lit,a,b){return [[lit,a,b],[lit,a,-b],[lit,-a,b],[lit,-a,-b]];}
  function copy(c){return c.map(t=>t.slice());}
  function maxvar(c){return Math.max(0,...c.flat().map(Math.abs));}
  function serialize(c){
    const n=maxvar(c),m=c.length,h=Math.max(1,Math.ceil(Math.log2(Math.max(n,m)+1)));
    const B=(v)=>v.toString(2).padStart(h,"0");
    for(const clause of c){assert(clause.length===3,"proper ternary");assert(new Set(clause.map(Math.abs)).size===3,"different vars");}
    const str="1".repeat(h)+"0"+B(n)+B(m)+c.map(row=>row.map(lit=>(lit<0?"1":"0")+B(Math.abs(lit))).join("")).join("");
    assert(str.length===3*h+1+3*m*(h+1),"exact encoding length");
    return str;
  }
  function deserialize(s){
    let h=0;while(s[h]==="1")h++;
    assert(s[h]==="0"&&h>=1,"self delimiter");let o=h+1;
    const rd=(k)=>{let v=parseInt(s.slice(o,o+k),2);o+=k;return v;};
    const n=rd(h),m=rd(h),c=[];
    for(let i=0;i<m;i++){let row=[];for(let j=0;j<3;j++){let sign=s[o++],id=rd(h);assert(id>=1&&id<=n,"in header index");row.push(sign==="1"?-id:id);}c.push(row);}
    assert(o===s.length&&n===maxvar(c),"no trailing bits/header exact");
    return c;
  }
  function sat(C,pinMap={}){
    const n=maxvar(C);
    const base=Array(n+1).fill(-1);
    for(const [k,v] of Object.entries(pinMap)){if(+k>n)return false;base[+k]=v;}
    function rec(a){
      let changed;
      do{
        changed=false;
        for(const c of C){
          let ok=false,unknown=0,last=0;
          for(const lit of c){
            let v=a[Math.abs(lit)];
            if(v<0){unknown++;last=lit;}
            else if((lit>0&&v===1)||(lit<0&&v===0)){ok=true;break;}
          }
          if(ok)continue;
          if(unknown===0)return false;
          if(unknown===1){
            const idx=Math.abs(last),v=last>0?1:0;
            if(a[idx]!==-1&&a[idx]!==v)return false;
            if(a[idx]===-1){a[idx]=v;changed=true;}
          }
        }
      }while(changed);
      for(let i=1;i<=n;i++)if(a[i]<0){
        const aa=a.slice();aa[i]=0;if(rec(aa))return true;
        const ab=a.slice();ab[i]=1;return rec(ab);
      }
      return true;
    }
    return rec(base);
  }
  const parents=[{P:bodyFor(P),Q:bodyFor(Q)}];
  parents.push({P:parents[0].P.concat(pin(-1,4,5)),Q:parents[0].Q.concat(pin(-1,6,7))});
  parents.push({P:parents[1].P.concat(pin(-2,8,9)),Q:parents[1].Q.concat(pin(-2,10,11))});
  const stages=[];
  for(let lvl=0;lvl<3;lvl++){
    const c=parents[lvl],both=c.P.concat(c.Q),p1=deserialize(serialize(c.P)),p2=deserialize(serialize(c.Q));
    const pSup=[],qSup=[];
    for(let w=0;w<8;w++){
      const fixed={1:bit(w,2),2:bit(w,1),3:bit(w,0)};
      if(sat(p1,fixed))pSup.push(w);
      if(sat(p2,fixed))qSup.push(w);
    }
    const exact=sat(both),bySupport=pSup.some(w=>qSup.includes(w));
    const coarse=pSup.some(u=>qSup.some(v=>(u>>1)===(v>>1)));
    assert(exact===bySupport&&exact===[true,true,false][lvl]&&coarse===true,"two genuine serialized levels "+lvl);
    assert(sat(p1)&&sat(p2),"both sides nonempty "+lvl);
    const expected=[j0,j1,j2][lvl];assert(JSON.stringify(pSup)===JSON.stringify(expected.L)&&JSON.stringify(qSup)===JSON.stringify(expected.R),"name-consistent support "+lvl);
    stages.push({level:lvl,left_support:pSup,right_support:qSup,left_length:serialize(c.P).length,right_length:serialize(c.Q).length,parent_length:serialize(both).length,left_clauses:c.P.length,right_clauses:c.Q.length,real_joint_SAT:exact,quotient_SAT:coarse});
  }
  const aliasedQ=parents[2].Q.map(cl=>cl.map(v=>Math.abs(v)===3?(v<0?-12:12):v));
  assert(sat(parents[2].P.concat(aliasedQ)),"false gluing if original z source identity lost");
  // Easy Horn, 2-CNF through proper-3CNF lift, affine, and independent controls.
  const horn=[[-1,-2,3]];
  assert(sat(horn),"Horn SAT");
  assert(!sat(horn.concat(pin(1,4,5),pin(2,6,7),pin(-3,8,9))),"Horn UNSAT with signed pins");
  const or2=[[1,2,4],[1,2,-4]];
  assert(sat(or2),"lifted 2SAT yes");
  assert(!sat(or2.concat(pin(-1,5,6),pin(-2,7,8))),"lifted 2SAT no");
  const even=support([0,3,5,6]),odd=support([1,2,4,7]);
  assert(sat(bodyFor(even))&&sat(bodyFor(odd))&&!sat(bodyFor(even).concat(bodyFor(odd))),"affine parity relation joins");
  assert(sat(pin(1,4,5).concat(pin(-3,6,7))),"disconnected easy independent");
  const res={run_id:"ARC-PIN-HEREDITY120",date:started,model:"extensional named Boolean support and explicitly encoded ordinary proper ternary CNF; not a timed FLMV TM simulation",seed:120,exact_exhaustive_n2:{support_pairs:256,partitions:15,cases:exhaust,unsafe_cases:unsafe,pin_patterns_each:9},seeded_n3:{cases:random,pin_patterns_each:27},pair_witness_failure:pw,stages,source_name_alias_false_SAT:true,hostile_controls:["Horn SAT/UNSAT","2SAT-lift SAT/UNSAT","affine parity SAT/SAT-to-UNSAT","disconnected SAT","source-name alias false SAT"],assertions:checks,failed:0,physical_bit_flips:null,circuit_hardware:null,bit_time:null,FLMV_peak_writable_bits:null};
  return res;
};
console.log(JSON.stringify(test(),null,2));
