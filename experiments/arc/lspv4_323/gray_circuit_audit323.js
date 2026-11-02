"use strict";
/**
 * LSPV-4 2026-11-01 20:40 PST. No third-party modules.
 * Run in Node: node gray_circuit_audit323.js [original_U198_fixture.txt] [198-bit_V198_witness]
 * Independent F9/Y6/F15, OBDD subset DP, shared-pair gate DAG, Gray incremental
 * clause-count solver, same-original pins, U198/V198 streamed-prefix controls.
 */
function run(inputs) {
  const check=(p,m)=>{if(!p)throw Error(m)};
  const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
    [-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
  const Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
    [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
  const P15=[[1,2,7],[1,3,8],[4,5,9],[4,6,10],[2,3,5],
    [6,11,12],[7,11,13],[8,12,14],[9,13,15],[10,14,15]];
  const N15=[[1,2,11],[2,3,11],[1,3,12],[4,5,13],[5,6,14],
    [4,6,15],[7,8,12],[8,9,13],[9,10,14],[10,7,15]];
  const F15=P15.concat(N15.map(c=>c.map(v=>-v)));
  function validate(C,n) {
    if(n<3||n%3!==0||C.length*3!==4*n)return false;
    const occ=Array.from({length:n+1},()=>[0,0]), seen=new Set();
    for(const c of C){
      if(c.length!==3||new Set(c.map(Math.abs)).size!==3||
          !c.every(z=>Number.isInteger(z)&&z!==0&&Math.abs(z)<=n&&
            (z>0)===(c[0]>0)))return false;
      const k=c.slice().sort((a,b)=>a-b).join(",");
      if(seen.has(k))return false;seen.add(k);
      for(const z of c)occ[Math.abs(z)][+(z>0)]++;
    }
    return occ.slice(1).every(x=>x[0]===2&&x[1]===2);
  }
  function val(C,a){for(const c of C){let sat=false;for(const z of c){
      const lit=a[Math.abs(z)]===+(z>0);
      if(lit){sat=true;break;}
    }if(!sat)return 0;}return 1;}
  function pairs(C) {
    const occ=new Map();
    for(let j=0;j<C.length;j++){const c=C[j].map(Math.abs);
      for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){
        const i=Math.min(c[a],c[b]),k=Math.max(c[a],c[b]);
        const name=(C[j][0]>0?"P":"N")+","+i+","+k;
        if(!occ.has(name))occ.set(name,[]);
        occ.get(name).push(j);
      }
    }
    const matches=[...occ.entries()].filter(([key,js])=>js.length===2);
    check([...occ.values()].every(x=>x.length<=2),"pair has >2 uses");
    const used=new Set();
    for(const [key,js] of matches){
      check(!js.some(j=>used.has(j)),"repeated-pair matching violated");
      js.forEach(j=>used.add(j));
    }
    const perClause=Array(C.length);
    for(const [key,js] of matches)js.forEach(j=>perClause[j]=key);
    for(let j=0;j<C.length;j++)if(!perClause[j]){
      const c=C[j].map(Math.abs).sort((a,b)=>a-b);
      perClause[j]=(C[j][0]>0?"P":"N")+","+c[0]+","+c[1];
    }
    return {d:matches.length,perClause};
  }
  function circuit(C,n) {
    const {d,perClause}=pairs(C), cache=new Map(), gates=[],depth={};
    function mk(op,u,v) {
      const id=n+1+gates.length;
      const dep=1+Math.max(depth[u]||0,depth[v]||0);
      gates.push([op,u,v,id]);depth[id]=dep;return id;
    }
    function pairGate(key) {
      if(cache.has(key))return cache.get(key);
      const [pol,i,k]=key.split(",");
      const id=mk(pol==="P"?"OR":"AND",+i,+k);
      cache.set(key,id);return id;
    }
    let layer=C.map((c,j)=>{
      const key=perClause[j],parts=key.split(",").slice(1).map(Number);
      const other=c.map(Math.abs).find(v=>!parts.includes(v));
      return mk(c[0]>0?"OR":"NAND",pairGate(key),other);
    });
    while(layer.length>1) {
      const next=[];
      for(let k=0;k<layer.length;k+=2)
        next.push(k+1<layer.length?mk("AND",layer[k],layer[k+1]):layer[k]);
      layer=next;
    }
    check(gates.length===3*C.length-1-d,"gate count mismatch");
    return {n,gates,output:layer[0],depth:depth[layer[0]],d};
  }
  function evalGate(G,a) {
    const v=new Uint8Array(G.n+G.gates.length+2);
    for(let i=1;i<=G.n;i++)v[i]=a[i];
    for(const [op,x,y,z] of G.gates) {
      v[z]=op==="OR"?(v[x]|v[y]):op==="AND"?(v[x]&v[y]):(1-(v[x]&v[y]));
    }return v[G.output];
  }
  function fromIndex(n,i){const a=new Uint8Array(n+1);
    for(let k=1;k<=n;k++)a[k]=(i>>(k-1))&1;return a;}
  function grayAudit(C,n,count) {
    const inc=Array.from({length:n+1},()=>[]);
    for(let j=0;j<C.length;j++)for(const z of C[j])inc[Math.abs(z)].push([j,z>0]);
    check(inc.slice(1).every(x=>x.length===4&&new Set(x.map(y=>y[0])).size===4),"degree error");
    const a=new Uint8Array(n+1), c=new Uint8Array(C.length);
    let dead=0,models=0,transitions=0,clauseUpdates=0,statusFlips=0,deltaCount=0;
    for(let j=0;j<C.length;j++){c[j]=C[j].filter(z=>z<0).length;if(c[j]===0)dead++;}
    let prev=0;
    for(let t=0;t<count;t++){
      if(t>0){const g=t^(t>>1), diff=prev^g;
        check(diff>0&&(diff&(diff-1))===0,"non-Gray step");
        const v=1+Math.round(Math.log2(diff));
        a[v]^=1;
        for(const [j,pos] of inc[v]){
          const was=c[j];const now=was+(a[v]===+(pos)?1:-1);
          check(now>=0&&now<=3,"count out of range");
          c[j]=now;clauseUpdates++;
          deltaCount+=(was^now).toString(2).replaceAll("0","").length;
          if(was===0&&now!==0){dead--;statusFlips++;}
          if(was!==0&&now===0){dead++;statusFlips++;}
        }
        prev=g;transitions++;
      }
      if(dead===0)models++;
      check((dead===0?1:0)===val(C,a),"source-versus-incremental mismatch at "+t);
    }
    check(clauseUpdates===4*(count-1),"four fixed incidence updates");
    return {states:count,transitions,models_in_prefix:models,
      clause_updates:clauseUpdates,clause_status_bit_flips:statusFlips,
      two_bit_count_hamming:deltaCount,naive_three_literal_source_reads:count*3*C.length};
  }
  function cofactorDp(F,n){
    const size=1<<n,full=size-1,truth=new Uint8Array(size);
    for(let v=0;v<size;v++)truth[v]=val(F,fromIndex(n,v));
    const sig=Array.from({length:size},()=>new Map());
    for(let mask=0;mask<size;mask++){
      const rest=full^mask,ts=[];
      for(let t=rest;;t=(t-1)&rest){ts.push(t);if(t===0)break;}
      ts.reverse();
      for(let a=mask;;a=(a-1)&mask){
        let bits=0n;
        for(let z=0;z<ts.length;z++)
          if(truth[a|ts[z]])bits|=1n<<BigInt(z);
        sig[mask].set(a,bits);
        if(a===0)break;
      }
    }
    const cost=Array.from({length:size},()=>new Map());
    for(let mask=0;mask<size;mask++){
      for(let v=0;v<n;v++)if(!(mask&(1<<v))){
        const bit=1<<v,next=mask|bit,seen=new Set();
        for(const [a,s] of sig[mask])if(sig[next].get(a)!==sig[next].get(a|bit))
            seen.add(s.toString(16));
        cost[mask].set(bit,seen.size);
      }
    }
    const min=new Int32Array(size),max=new Int32Array(size),mv=new Int32Array(size);
    for(let mask=full-1;mask>=0;mask--){
      let lo=1e9,hi=-1;
      for(const [bit,c] of cost[mask]){
        const v=c+min[mask|bit],w=c+max[mask|bit];
        if(v<lo){lo=v;mv[mask]=bit;}if(w>hi)hi=w;
      }min[mask]=lo;max[mask]=hi;
    }
    const best=[];let mask=0;
    while(mask!==full){const bit=mv[mask];check(bit!==0,"missing dp choice");
      best.push(1+Math.round(Math.log2(bit)));mask|=bit;}
    function score(order) {let s=0,mask=0;
      for(const v of order){const bit=1<<(v-1);s+=cost[mask].get(bit);mask|=bit;}
      return s;}
    const nat=Array.from({length:n},(_,i)=>i+1);
    let pivotal=[];
    for(let v=0;v<n;v++){
      let t=0;for(let i=0;i<size;i++)if(!(i&(1<<v))&&truth[i]!==truth[i|(1<<v)])t++;
      pivotal.push(t);
    }
    return {exact_min:min[0],exact_max:max[0],natural:score(nat),
      reverse:score(nat.slice().reverse()),min_order:best,pivotal_pairs:pivotal,
      masks:size,candidate_subset_extensions:n*(size/2)};
  }
  function pinAudit(){
    const fixed={3:0,5:1,6:0,7:0,8:0};
    const result={};
    for(const x1 of [0,1]){
      let models=0,clauses=[];
      for(let free=0;free<8;free++){
        const a=new Uint8Array(10);
        for(const [k,v] of Object.entries(fixed))a[+k]=v;
        a[1]=x1;a[2]=free&1;a[4]=(free>>1)&1;a[9]=(free>>2)&1;
        if(val(F9,a))models++;
        else clauses.push(F9.findIndex(c=>c.every(z=>a[Math.abs(z)]!==+(z>0)))+1);
      }
      result["x1="+x1]={models,falsifying_clause_per_failed_leaf:clauses};
    }
    check(result["x1=0"].models===2&&result["x1=1"].models===0,"pin counts");
    return result;
  }
  function malformedChecks() {
    let tests=0;
    const bad=[
      F9.slice(0,-1),F9.concat([F9[0]]),
      [[1,-5,6]].concat(F9.slice(1)),
      [[1,1,5]].concat(F9.slice(1)),
      [[0,5,6]].concat(F9.slice(1)),
      [[1,5,10]].concat(F9.slice(1))
    ];
    for(const x of bad){check(!validate(x,9),"malformed accepted");tests++;}
    return tests;
  }
  function caseStats(C,n,limit) {
    check(validate(C,n),"invalid canonical input n="+n);
    const G=circuit(C,n);
    const sample=n<=15?(1<<n):64;
    for(let t=0;t<sample;t++){
      let a;
      if(n<=15)a=fromIndex(n,t);
      else {a=new Uint8Array(n+1);for(let i=1;i<=n;i++)a[i]=((t*1103515245+i*12345)>>>((i-1)%30))&1;}
      check(val(C,a)===evalGate(G,a),"gate mismatch n="+n+" row="+t);
    }
    return {n,clauses:C.length,valid:true,d:G.d,gates:G.gates.length,
      unshared_gates:3*C.length-1,circuit_depth:G.depth,
      tseitin_clauses:3*G.gates.length+1,
      circuit_rows_checked:sample,gray:grayAudit(C,n,limit)};
  }
  const out={
    experiment:"LSPV4-GRAY-CIRCUIT-AUDIT323",
    statuses:{restricted_gate:"PROVED/EXACT",gray_ledger:"PROVED/EXACT",
      OBDD_F9:"COMPUTATIONAL exhaustive subset DP",all_input:"OPEN"},
    F9:caseStats(F9,9,512),Y6:caseStats(Y6,6,64),
    F15:caseStats(F15,15,32768),
    OBDD_F9:cofactorDp(F9,9),
    same_original_F9_pins:pinAudit(),
    malformed_rejections:malformedChecks()
  };
  if(inputs && inputs.U198_text){
    const txt=inputs.U198_text;
    const U=JSON.parse(txt.slice(txt.indexOf("[[")));
    const V=U.map(c=>c.slice());
    [V[2][2],V[44][2]]=[V[44][2],V[2][2]];
    out.U198=caseStats(U,198,1025);
    out.V198=caseStats(V,198,1025);
    if(inputs.V198_witness){
      const s=inputs.V198_witness;
      check(s.length===198&&/^[01]+$/.test(s),"bad witness text");
      const a=new Uint8Array(199);
      for(let i=1;i<=198;i++)a[i]=+s[i-1];
      check(val(V,a)===1&&evalGate(circuit(V,198),a)===1,"V witness fails");
      out.V198.witness_input_checked=true;
    }
  }
  return out;
}
if(typeof module!=="undefined"&&typeof require==="function"&&require.main===module) {
  const fs=require("fs"),root=require("path").resolve(__dirname,"../../..");
  const source=process.argv[2]||root+"/experiments/arc/lspv2_315/U198.txt";
  const witness=process.argv[3]||"001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101";
  console.log(JSON.stringify(run({U198_text:fs.readFileSync(source,"utf8"),V198_witness:witness}),null,2));
}
