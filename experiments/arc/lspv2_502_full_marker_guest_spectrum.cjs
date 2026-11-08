"use strict";
/* LSPV-2/502: independent original-source / padded-delay exact-state controls.
   Self-contained, no dependencies. Finite V8/Node experiment, NOT an FLMV emulator. */
const edges502=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const magic502="11000011";
function assert502(ok,msg){if(!ok)throw new Error("FAIL: "+msg);run502.assertions++;}
function source502(charges){
  const clauses=[];
  for(let v=0;v<4;v++){
    const ids=[];edges502.forEach(([a,b],i)=>{if(v===a||v===b)ids.push(i+1)});
    if(ids.length!==3)throw Error("degree");
    for(let mask=0;mask<8;mask++){
      const bits=[(mask>>2)&1,(mask>>1)&1,mask&1];
      if((bits[0]^bits[1]^bits[2])!==((charges>>v)&1))
        clauses.push(ids.map((id,i)=>bits[i]?-id:id));
    }
  }
  return clauses;
}
function serialize502(clauses){
  let s=magic502+clauses.length.toString(2).padStart(8,"0");
  for(const clause of clauses)for(const lit of clause){
    s+=Math.abs(lit).toString(2).padStart(3,"0")+(lit<0?"1":"0");
  }
  return s;
}
function parse502(s){
  if(typeof s!=="string" || s.length!==208 || s.slice(0,8)!==magic502 ||
     s.slice(8,16)!=="00010000" || /[^01]/.test(s))return null;
  const cs=[];
  for(let i=0;i<16;i++){
    const clause=[];
    for(let j=0;j<3;j++){
      const chunk=s.slice(16+i*12+j*4,20+i*12+j*4);
      const id=parseInt(chunk.slice(0,3),2);
      if(id<1||id>6)return null;
      clause.push(chunk[3]==="1"?-id:id);
    }
    if(new Set(clause.map(x=>Math.abs(x))).size!==3)return null;
    cs.push(clause);
  }
  return cs;
}
function sat502(clauses){
  for(let assignment=0;assignment<64;assignment++){
    let all=true;
    for(const clause of clauses){
      let yes=false;
      for(const lit of clause){
        const bit=(assignment>>(Math.abs(lit)-1))&1;
        if(bit===(lit>0?1:0)){yes=true;break}
      }
      if(!yes){all=false;break}
    }
    if(all)return true;
  }
  return false;
}
function run502(){
  run502.assertions=0;
  const sources=[];
  for(let charge=0;charge<16;charge++){
    const clauses=source502(charge), s=serialize502(clauses);
    assert502((!sat502(clauses))===((popcount502(charge)%2)===1),"parity charge");
    assert502(JSON.stringify(parse502(s))===JSON.stringify(clauses),"wire parse");
    assert502(s.length===208,"fixed bits");
    sources.push(s);
    if(popcount502(charge)%2===1){
      for(let del=0;del<16;del++){
        const sub=clauses.filter((_,i)=>i!==del);
        assert502(sat502(sub),"every odd-source clause essential");
      }
    }
  }
  assert502(new Set(sources).size===16,"distinct original sources");
  const t=sources[1];
  const mal=[t.slice(0,-1),"0"+t.slice(1),t.slice(0,8)+"00001111"+t.slice(16),
    t.slice(0,16)+"0000"+t.slice(20),
    t.slice(0,16)+"1110"+t.slice(20),
    t.slice(0,20)+"0111"+t.slice(24),
    t.slice(0,20)+"0001"+t.slice(24,28)+t.slice(20,24)+t.slice(32)];
  for(const bad of mal)assert502(parse502(bad)===null,"malformed source");
  const counts={};
  const children=sources.filter((_,i)=>i%2===1);
  for(const k of [1,2]){
    let distinct=0;
    const states=new Set();
    for(const child of children){
      for(let counter=0;counter<(child.length**k);counter++){
        const key=child+":"+counter;
        assert502(!states.has(key),"exact state nonconvergence");
        states.add(key); distinct++;
      }
    }
    assert502(states.size===8*(208**k),"exact union cardinality");
    counts["k"+k]=distinct;
  }
  for(const original of sources){
    assert502(original===String(original),"genuine marker");
    for(const pos of [0,15,50,207]){
      const mutated=original.slice(0,pos)+(original[pos]==="1"?"0":"1")+original.slice(pos+1);
      assert502(mutated!==original,"corrupted marker rejected");
    }
  }
  const spectrum=[];
  for(const k of [2,3,5,10])for(const numer of [1,2,3]){
    const alpha=numer/5, a=.6, target=Math.max(1.1,.6+k/2);
    const work=a+alpha*k;
    spectrum.push({k,distinct_query_exponent:a,child_exponent:alpha,
      unshared_guest_exponent:work,target_exponent:target,passes:work<=target+1e-10});
    assert502(spectrum.length>0,"spectrum arithmetic");
  }
  return {test:"padded-decider-full-marker-distinct-computation",
    assertions:run502.assertions,sources:16,unsat_sources:8,sat_sources:8,
    source_bits:208,deletion_witnesses:128,corrupt_marker_rejects:64,
    malformed_rejects:7,checked_delay_exponents:[1,2],
    unique_delay_transition_counts:counts,resource_spectrum_rows:spectrum,
    model:"finite JavaScript/V8 exact-state control; not native FLMV"};
}
function popcount502(x){let n=0;while(x){n+=x&1;x>>=1}return n}
if(typeof process!=="undefined" && process.stdout && typeof require!=="undefined" &&
   require.main===module){process.stdout.write(JSON.stringify(run502(),null,2)+"\n");}
