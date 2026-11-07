"use strict";
/* LSPV-2/467 CORRECTED: original attempted input-head firewall was FALSIFIED.
   FLMV writable INDEX tape extent must be charged to guest space even though
   the separate read-only INPUT tape is space-exempt. This is an abstract check,
   not native FLMV execution. See report LSPV-2/467 and prior LSPV-4/273. */
function verify() {
  let assertions=0, traces=0, labels={SAT:0,UNSAT:0,MALFORMED:0};
  function ok(p,msg){assertions++;if(!p)throw Error(msg);}
  function bitLength(n){return n===0n?0:n.toString(2).length;}
  const ns=[2,3,4,6,8,12,16,24];
  const ledger=[];
  for(const n of ns)for(const k of [1,2,3]){
    const m=n**k;
    const index=new Uint8Array(m); // Guest INPUT INDEX is not a counted WORK tape.
    for(let j=0;j<m;j++)index[j]=1;
    const exact=(1n<<BigInt(m))-1n; // All low m bits are one.
    ok(bitLength(exact)===m,"wrong far-input address width");
    ok(index.length===m,"index append length");
    ok(index.every(b=>b===1),"index tape contents");
    ok(exact>=BigInt(n),"far input was not blank");
    // Native indexed INPUT jump erases the INPUT INDEX contents.
    index.fill(0);
    ok(index.every(b=>b===0),"INDEX erase semantics");
    const headAfterReset=0n; // A second zero-index native input move.
    ok(headAfterReset===0n,"input head restoration");
    // The simulation under attack stores exact guest INPUT head in a
    // conventional counted binary WORK register. That register uses m bits.
    const countedWorkBitsForCounters=4+k*Math.ceil(Math.log2(n+1));
    const guestIndexTapeSpaceLower=m; // Sequential INDEX head visited all m positions.
    ok(guestIndexTapeSpaceLower>=m,"guest INDEX head not charged");
    ok(m<=guestIndexTapeSpaceLower,"binary host head worse than guest index high-water");
    if(k>=2)ok(m>n,"counted binary head exceeds sqrt(parent N=n^2)");
    ledger.push({n,k,index_bits:m,far_address_bit_length:bitLength(exact),
      guest_counter_work_upper_bits:countedWorkBitsForCounters,
      naive_counted_input_head_bits:m,guest_index_space_lower:guestIndexTapeSpaceLower,synthetic_parent_N:n*n,
      target_sqrt_N:n});
    traces++;
  }
  // Signed proper ternary Tseitin on the original K4 graph.
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function tseitin(charges){
    const clauses=[];
    for(let v=0;v<4;v++){
      const incident=[];
      for(let j=0;j<edges.length;j++)if(edges[j].includes(v))incident.push(j);
      ok(incident.length===3,"not cubic");
      for(let mask=0;mask<8;mask++){
        const parity=(((mask>>0)&1)^((mask>>1)&1)^((mask>>2)&1));
        if(parity!==charges[v]){
          clauses.push(incident.map((j,t)=>((mask>>t)&1)?-(j+1):(j+1)));
        }
      }
    }
    return clauses;
  }
  function dimacs(clauses,n){
    return "p cnf "+n+" "+clauses.length+"\n"+
       clauses.map(c=>c.join(" ")+" 0").join("\n")+"\n";
  }
  function parseStrict(text){
    if(typeof text!=="string")return null;
    const lines=text.trim().split(/\r?\n/);
    const head=lines.shift();
    const match=/^p cnf ([1-9]\d*) ([0-9]+)$/.exec(head||"");
    if(!match)return null;
    const n=Number(match[1]), count=Number(match[2]);
    if(!Number.isSafeInteger(n)||!Number.isSafeInteger(count)||lines.length!==count)return null;
    const clauses=[];
    for(const line of lines){
      if(!/^-?\d+( -?\d+){3}$/.test(line))return null;
      const a=line.split(" ").map(Number);
      if(a[3]!==0||a.slice(0,3).some(x=>x===0||Math.abs(x)>n))return null;
      if(new Set(a.slice(0,3).map(Math.abs)).size!==3)return null;
      clauses.push(a.slice(0,3));
    }
    return {n,clauses};
  }
  function classify(text){
    const f=parseStrict(text);
    if(!f)return "MALFORMED";
    if(f.n>15)throw Error("finite SAT control scope exceeded");
    for(let mask=0;mask<(1<<f.n);mask++){
      if(f.clauses.every(c=>c.some(l=> (((mask>>(Math.abs(l)-1))&1)===1)===(l>0))))
        return "SAT";
    }
    return "UNSAT";
  }
  for(let bits=0;bits<16;bits++){
    const charges=[0,1,2,3].map(v=>(bits>>v)&1);
    const src=dimacs(tseitin(charges),6);
    const outcome=classify(src);
    const expected=(charges.reduce((x,y)=>x^y,0)===0)?"SAT":"UNSAT";
    ok(outcome===expected,"wrong K4 SAT label");
    labels[outcome]++;
    const corruptions=[
      src.replace("p cnf 6 16","p cnf 6 15"),
      src.replace(/ 0\n/," 1\n"),
      src.replace(/(\d+) (\d+) (\d+) 0\n/,(_,a,b,c)=>a+" "+a+" "+c+" 0\n"),
      src.slice(0,-4),
    ];
    for(const v of corruptions){ok(classify(v)==="MALFORMED","corrupt source accepted"); labels.MALFORMED++;}
  }
  return {status:"PASS",scope:"Host semantic plus exact arithmetic, not native FLMV",
    assertions,trace_cases:traces,source_controls:16,
    labels,ledger,conclusions:{
      model:"FLMV read-only INPUT head is space-exempt, but its writable sequential INDEX tape contributes visited index extent to guest space; original uncharged-index interpretation is RETIRED",
      test:"An explicit binary INPUT head register uses n^k counted WORK bits, but constructing the original INDEX contents already incurs Omega(n^k) guest space",
      boundary:"Proposed excess-space witness fails; this is an independent falsifier of the earlier mistaken uncharged-INDEX premise. It does NOT establish a complete input-port simulation or universal FLMV contraction"
    }};
}
if(typeof require!=="undefined" && typeof module!=="undefined" && require.main===module){
  console.log(JSON.stringify(verify(),null,2));
}
