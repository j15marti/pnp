#!/usr/bin/env node
// ARC-SUPPORT-VISIBILITY114, deterministic no-dependency reproducer.
// Source-name semantic controls, no FLMV physical machine simulation.
const arc114=function arc114(){
  const st={run_id:"ARC-SUPPORT-VISIBILITY114",timestamp_local:"2026-10-25 03:24 America/Los_Angeles",
    kind:"deterministic exhaustive finite signed proper-3CNF audit",seed:null,b_values:[3,4,5,6],
    assertions:0,sat_calls:0,dpll_nodes:0,dpll_units:0,roundtrips:0,
    serialized_bits_written:0,parsed_bits_read:0,
    parents:[],contexts:{},levels:[],complete_face_queries:0,semantic_mismatches:0,
    physical_FLMV_machine_steps_measured:false};
  function ck(a,m){st.assertions++;if(!a){st.semantic_mismatches++;throw Error(m)}}
  function alloc(start){return {id:start}}
  function fresh(a){return ++a.id}
  function xor3(a,b,c){let out=[];for(let k=0;k<8;k++){let av=(k>>2)&1,bv=(k>>1)&1,cv=k&1;if(cv!==(av^bv))out.push([av?-a:a,bv?-b:b,cv?-c:c]);}return out;}
  function pin(lit,alloc){let p=fresh(alloc),q=fresh(alloc);return [[lit,p,q],[lit,p,-q],[lit,-p,q],[lit,-p,-q]];}
  function or2(u,v,alloc){let h=fresh(alloc);return [[u,v,h],[u,v,-h]];}
  function mod(b,u){
    let a=alloc(b),z=[],w=[],R=[],Q=[];
    for(let i=0;i<=b;i++)z.push(fresh(a));
    R.push(...pin(-z[0],a),...pin(-z[b],a));
    for(let i=0;i<b;i++)R.push(...xor3(z[i],i+1,z[i+1]));
    for(let i=0;i<=b;i++)w.push(fresh(a));
    Q.push(...pin(-w[0],a));
    for(let i=0;i<b;i++)Q.push(...xor3(w[i],i+1,w[i+1]));
    const selector=fresh(a);
    Q.push(...or2(selector,w[b],a));
    for(let i=0;i<b;i++)Q.push(...or2(-selector,u[i]?(i+1):-(i+1),a));
    return {R,Q,n:a.id,F:[...R,...Q]};
  }
  function serialize(C,n){
    const m=C.length,h=Math.floor(Math.log2(2*Math.max(n,m)+1))+1;
    const fmt=x=>x.toString(2).padStart(h,"0");
    let bits="1".repeat(h)+"0"+fmt(n)+fmt(m);
    for(const c of C){ck(c.length===3&&new Set(c.map(Math.abs)).size===3,"not proper");for(const x of c){ck(Math.abs(x)<=n&&Math.abs(x)>0,"bad name");bits+=fmt(2*(Math.abs(x)-1)+(x<0?1:0));}}
    ck(bits.length===1+(3+3*m)*h,"bad length");st.serialized_bits_written+=bits.length;
    return bits;
  }
  function parse(bits){
    let h=0;while(h<bits.length&&bits[h]==="1")h++;
    if(h===0||bits[h]!=="0")throw Error("bad unary header");
    let n=parseInt(bits.slice(h+1,2*h+1),2),m=parseInt(bits.slice(2*h+1,3*h+1),2);
    if(h!==Math.floor(Math.log2(2*Math.max(n,m)+1))+1)throw Error("noncanonical header");
    if(bits.length!==1+(3+3*m)*h)throw Error("bad body length");
    let p=3*h+1,C=[];
    for(let j=0;j<m;j++){let clause=[];for(let k=0;k<3;k++){const code=parseInt(bits.slice(p,p+h),2);p+=h;const v=Math.floor(code/2)+1;if(v>n||v<1)throw Error("out of header");clause.push(code%2?-v:v);}if(new Set(clause.map(Math.abs)).size!==3)throw Error("improper");C.push(clause);}
    st.parsed_bits_read+=bits.length;return {C,n};
  }
  function serialRound(C,n){let bits=serialize(C,n),p=parse(bits);ck(p.n===n&&JSON.stringify(p.C)===JSON.stringify(C),"roundtrip");st.roundtrips++;return {bits,C:p.C,n:p.n};}
  function sat(C){
    st.sat_calls++;
    function dfs(A){
      st.dpll_nodes++;
      let work=C;
      while(true){
        let rem=[],units=[];
        for(const c of work){
          let good=false,un=[];
          for(const x of c){const v=Math.abs(x);if(v in A){if(A[v]===(x>0)){good=true;break;}}else un.push(x);}
          if(good)continue;if(un.length===0)return false;rem.push(un);if(un.length===1)units.push(un[0]);
        }
        if(!rem.length)return true;
        if(!units.length){work=rem;break}
        let changed=false;
        for(const x of units){const v=Math.abs(x),val=x>0;if(v in A){if(A[v]!==val)return false;}else{A[v]=val;st.dpll_units++;changed=true;}}
        if(!changed){work=rem;break}
        work=rem;
      }
      let score={};for(const c of work)for(const x of c)if(!(Math.abs(x) in A)){let v=Math.abs(x);score[v]=(score[v]||0)+1;}
      const v=Number(Object.keys(score).reduce((a,b)=>score[a]>=score[b]?a:b));
      for(const truth of [true,false]){let B={...A,[v]:truth};if(dfs(B))return true;}return false;
    }
    return dfs({});
  }
  function contextSet(b,rootN){
    let list=[{name:"empty",C:[],n:rootN}];
    function add(name,make){let a=alloc(rootN),C=make(a);list.push({name,C,n:a.id})}
    add("one_pin",a=>pin(1,a));
    add("horn",a=>[[1,-2,fresh(a)]]);
    add("two_sat",a=>or2(1,-2,a));
    add("affine",a=>{let y=fresh(a);return [...xor3(1,2,y),...pin(-y,a)]});
    add("unsat_private",a=>{let v=[fresh(a),fresh(a),fresh(a)],C=[];for(let k=0;k<8;k++)C.push(v.map((x,j)=>(k>>(2-j))&1?-x:x));return C});
    add("all_but_one_pin",a=>{let C=[];for(let i=1;i<b;i++)C.push(...pin(-i,a));return C});
    return list;
  }
  for(const b of st.b_values){
    const roots={YES:mod(b,Array(b).fill(0)),NO:mod(b,[...Array(b-1).fill(0),1])};
    for(const label of ["YES","NO"]){
      let root=roots[label];
      ck(root.R.length===4*b+8&&root.Q.length===6*b+6&&root.n===4*b+10,"module count");
      let p=serialRound(root.F,root.n);
      ck(sat(p.C)===(label==="YES"),"parent label");
      root.bits=p.bits;
      for(const {name,C:H,n} of contextSet(b,root.n)){
        const mentions=new Set(H.flat().filter(x=>Math.abs(x)<=b).map(Math.abs));
        ck(mentions.size<b,"context complete");
        const expect=sat(H);
        for(const key of ["R","Q"]){
          let child=serialRound([...root[key],...H],n);
          let got=sat(child.C);
          ck(got===expect,`visibility ${b} ${label} ${key} ${name}`);
          let d=st.contexts[name]??{checks:0,SAT:0,UNSAT:0};
          d.checks++;d[got?"SAT":"UNSAT"]++;st.contexts[name]=d;
        }
      }
      for(const key of ["R","Q","F"]){
        let a=alloc(root.n),one=serialRound([...root[key],...pin(-1,a)],a.id);
        let got1=sat(one.C),two=serialRound([...one.C,...pin(-2,a)],a.id),got2=sat(two.C);
        const expected=key==="F"?label==="YES":true;
        ck(got1===expected&&got2===expected,"two real descendants");
        st.levels.push({b,label,key,N_parent:root.bits.length,
          N_base:serialize(root[key],root.n).length,N_child_1:one.bits.length,N_child_2:two.bits.length,
          child_1_label:got1,child_2_label:got2,source_names:"x_i = i, original 1..b"});
      }
      let a=alloc(root.n),H=[];
      for(let i=1;i<=b;i++)H.push(...pin(-i,a));
      let all=serialRound([...root.Q,...H],a.id);
      ck(sat(all.C)===(label==="YES"),"all-name query");
      ck(serialize(H,a.id).length>=b*b.toString(2).length,"full support syntax size");
      if(b<=4)for(let mask=0;mask<(1<<b);mask++){
        let a=alloc(root.n),H=[],weight=0,word=[];
        for(let i=0;i<b;i++){let bit=(mask>>i)&1;weight+=bit;word.push(bit);H.push(...pin(bit?i+1:-(i+1),a));}
        for(const key of ["R","Q"]){
          const child=serialRound([...root[key],...H],a.id);
          const pred=key==="R"?(weight%2===0):(weight%2===1||JSON.stringify(word)===JSON.stringify(label==="YES"?Array(b).fill(0):[...Array(b-1).fill(0),1]));
          ck(sat(child.C)===pred,"complete face semantics");st.complete_face_queries++;
        }
      }
    }
    const yes=roots.YES,no=roots.NO;
    ck(yes.bits.length===no.bits.length,"matched header length");
    ck([...yes.bits].filter((x,i)=>x!==no.bits[i]).length===2,"matched pair 2 flips");
    ck(JSON.stringify(yes.F.map(c=>c.map(Math.abs)))===JSON.stringify(no.F.map(c=>c.map(Math.abs))),"source support identity");
    st.parents.push({b,m:yes.F.length,n:yes.n,N_root:yes.bits.length,
      R_clauses:yes.R.length,Q_clauses:yes.Q.length,
      N_R:serialize(yes.R,yes.n).length,N_Q:serialize(yes.Q,yes.n).length,
      support_field_lower_bound_bits:b*b.toString(2).length,
      literal_sign_flips:2,YES_target:"0".repeat(b),NO_target:"0".repeat(b-1)+"1"});
  }
  try{parse(roots.NO.bits.slice(0,-1));throw Error("TRUNCATION UNDETECTED")}catch(e){ck(String(e)!=="Error: TRUNCATION UNDETECTED","truncated parser must reject")}
  st.status="COMPUTATIONAL finite zero-failure controls; separate PROVED/EXACT restricted lemmas await peer review";
  return st;
};
console.log(JSON.stringify(arc114(),null,2));
