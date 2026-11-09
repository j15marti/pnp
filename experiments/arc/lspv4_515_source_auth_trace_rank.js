/* LSPV-4/515 standalone V8 / Node finite source-authentication witness.
 * Signed proper 3-CNF K4 Tseitin, two fresh ternary tag clauses.
 * This is NOT a native FLMV simulator or historical R_mix341 checker. */
"use strict";
function main() {
  const marker="10110110", H=4, k=2, w=4;
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const clauseBits=3*(w+1), header=marker+"11110";
  const assert=(cond,msg)=>{if(!cond)throw Error(msg)};
  function build(d,charge=1) {
    let core=[],bits=header,tagpos=[];
    for(let v=0;v<H;v++){
      const ids=edges.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
      for(let a=0;a<8;a++){
        const t=[(a>>2)&1,(a>>1)&1,a&1];
        if((t[0]^t[1]^t[2])===(v===0?charge:0))continue;
        const cl=ids.map((id,i)=>t[i]?-id:id);
        core.push(cl);
        for(const lit of cl)
          bits+=Math.abs(lit).toString(2).padStart(w,"0")+(lit<0?"1":"0");
      }
    }
    for(let j=0;j<k;j++)for(let p=0;p<3;p++){
      const id=7+3*j+p;
      bits+=id.toString(2).padStart(w,"0");
      if(p===0)tagpos.push(bits.length);
      bits+=(p===0&&((d>>j)&1))?"1":"0";
    }
    return {src:bits+"01",core,tagpos};
  }
  function auth(src){
    const reads=[],get=i=>{const val=i<src.length?src[i]:null;reads.push([i,val]);return val};
    for(let i=0;i<marker.length;i++)if(get(i)!==marker[i])return {ok:false,reads};
    for(let i=0;i<H;i++)if(get(8+i)!=="1")return {ok:false,reads};
    if(get(12)!=="0")return {ok:false,reads};
    const cstart=13,tstart=cstart+16*clauseBits,len=tstart+k*clauseBits+2;
    if(get(len-2)!=="0"||get(len-1)!=="1"||get(len)!==null)return {ok:false,reads};
    let degree=Array(7).fill(0);
    function literal(i){
      let id=0;
      for(let b=0;b<w;b++){
        const v=get(i+b);if(v!=="0"&&v!=="1")return null;
        id=id*2+Number(v);
      }
      const sign=get(i+w);
      return sign==="0"||sign==="1"?[id,Number(sign)]:null;
    }
    for(let v=0;v<H;v++){
      let supports=[],patterns=new Set();
      for(let j=0;j<4;j++){
        let clause=[];
        for(let z=0;z<3;z++){
          const lit=literal(cstart+(v*4+j)*clauseBits+z*(w+1));
          if(!lit||lit[0]<1||lit[0]>6)return {ok:false,reads};
          clause.push(lit);
        }
        const ids=clause.map(q=>q[0]),pat=clause.map(q=>q[1]);
        if(new Set(ids).size!==3)return {ok:false,reads};
        if(j===0){supports=ids;for(const id of ids)degree[id]++}
        if(ids.join(",")!==supports.join(",")||
           pat.reduce((a,b)=>a^b,0)!==(v===0?0:1))return {ok:false,reads};
        patterns.add(pat.join(""));
      }
      if(patterns.size!==4)return {ok:false,reads};
    }
    if(degree.slice(1).some(d=>d!==2))return {ok:false,reads};
    const tagpos=[];
    for(let j=0;j<k;j++)for(let p=0;p<3;p++){
      const off=tstart+(3*j+p)*(w+1),want=7+3*j+p;
      const bin=want.toString(2).padStart(w,"0");
      for(let b=0;b<w;b++)if(get(off+b)!==bin[b])return {ok:false,reads};
      if(p>0&&get(off+w)!=="0")return {ok:false,reads};
      if(p===0)tagpos.push(off+w);
    }
    if(tagpos.some(p=>reads.some(([i])=>i===p)))throw Error("tag read leaked");
    return {ok:true,reads,tagpos};
  }
  function decodedCoreSAT(src){
    const clauses=[],base=13;
    for(let j=0;j<16;j++){
      let c=[];
      for(let p=0;p<3;p++){
        const off=base+(3*j+p)*(w+1),id=parseInt(src.slice(off,off+w),2);
        c.push(src[off+w]==="1"?-id:id);
      }
      clauses.push(c);
    }
    for(let x=0;x<64;x++)
      if(clauses.every(c=>c.some(l=>(((x>>(Math.abs(l)-1))&1)===Number(l>0)))))
        return x;
    return null;
  }
  const traces=new Set(),signs=new Set(),sources=new Set(),first=build(0);
  for(let d=0;d<4;d++){
    const obj=build(d),check=auth(obj.src);
    assert(check.ok&&check.tagpos.join(",")===obj.tagpos.join(","),"source");
    assert(decodedCoreSAT(obj.src)===null,"core UNSAT");
    traces.add(JSON.stringify(check.reads));
    signs.add(obj.tagpos.map(p=>obj.src[p]).join(""));
    sources.add(obj.src);
  }
  assert(traces.size===1&&signs.size===4&&sources.size===4,"rank classes");
  const even=build(0,0);
  assert(!auth(even.src).ok&&decodedCoreSAT(even.src)!==null,"SAT charge switch");
  // Malicious permutation within ONE parity facet: support multiset unchanged!
  const a=13+clauseBits,b=a+w+1,buf=first.src.split("");
  for(let j=0;j<w;j++){const t=buf[a+j];buf[a+j]=buf[b+j];buf[b+j]=t}
  const hostile=buf.join(""),hostileWitness=decodedCoreSAT(hostile);
  assert(hostileWitness!==null&&!auth(hostile).ok,"ordered source facets");
  const flip=first.src.slice(0,first.tagpos[0])+"1"+first.src.slice(first.tagpos[0]+1);
  assert(auth(flip).ok,"unread tag sign allowed");
  for(const bad of [first.src+"0",first.src.slice(0,-1)])
    assert(!auth(bad).ok,"length controls");
  return {status:"PASS",sample:"K4 original signed strict 3CNF",source_bits:first.src.length,
    sources:sources.size,rank_skipped:0,rank_scanned:2,
    sign_blind_trace_classes:traces.size,sign_scanned_trace_classes:signs.size,
    core_unsat_verified:true,charge_flip_sat:true,
    positional_facet_sat_witness:hostileWitness,hostile_rejected:true,
    corrupted_length_rejections:2,legal_tag_flip_accepted:true};
}
if(typeof console!=="undefined"&&typeof console.log==="function")
  console.log(JSON.stringify(main(),null,2));
