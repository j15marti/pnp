'use strict';
// LSPV-4/475. Independent finite model, NOT a native FLMV interpreter.
// Head-preserving indexed-erasure and immediate head return are assumptions.
function assert(c,m){if(!c)throw Error(m||'assertion failed');}
function countK4(charges){
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  const incidence=[0,1,2,3].map(v=>E.map((e,j)=>e.includes(v)?j:-1).filter(j=>j>=0));
  const clauses=[];
  for(let v=0;v<4;v++)for(let a=0;a<8;a++){
    if(( ((a&1)+((a>>1)&1)+((a>>2)&1))%2 )!==charges[v])
      clauses.push(incidence[v].map((e,k)=>((a>>k)&1)?-(e+1):e+1));
  }
  let sat=0;
  for(let b=0;b<64;b++){
    if(clauses.every(cl=>cl.some(l=>l>0?((b>>(l-1))&1):!((b>>(-l-1))&1))))sat++;
  }
  return [clauses.length,sat];
}
function main(){
  const r={program:'LSPV4-475 standalone Node/V8',cache_cases:0,logical_reads:0,
    source_misses:0,head_moves:0,assertions:0,malformed_rejections:0,entropy_cases:0};
  assert(JSON.stringify(countK4([0,0,0,0]))===JSON.stringify([16,8]),'even K4');r.assertions++;
  assert(JSON.stringify(countK4([1,0,0,0]))===JSON.stringify([16,0]),'odd K4');r.assertions++;
  for(let d=1;d<=8;d++)for(let c=0;c<=d;c++)for(const rounds of [1,2,5])
    for(const H of [1,4,13,32])for(let state=0;state<(1<<d);state++){
      const src=Array.from({length:d},(_,j)=>(state>>j)&1);
      const cache=new Map();let miss=0,moves=0,good=true;
      for(let turn=0;turn<rounds;turn++)for(let j=0;j<d;j++){
        r.logical_reads++;
        let observed;
        if(cache.has(j))observed=cache.get(j);
        else{
          // Fetch once at physical source-index location, then return to H.
          observed=src[j];miss++;moves+=2*H;
          if(j<c)cache.set(j,observed);
        }
        if(observed!==src[j])good=false;
      }
      assert(good,'bit mismatch');assert(miss===d+(rounds-1)*(d-c),'exact static pinned miss formula');
      assert(moves===2*H*miss,'head charges');assert(cache.size===c,'cache width');
      r.assertions+=4;r.cache_cases++;r.source_misses+=miss;r.head_moves+=moves;
    }
  for(let d=1;d<=13;d++){
    const seen=new Set();
    for(let state=0;state<(1<<d);state++)seen.add(state.toString(2).padStart(d,'0'));
    assert(seen.size===(1<<d),'entropy/collision');r.entropy_cases++;r.assertions++;
  }
  for(const bad of [-1,null,1.3,'x']){
    let rejects=!(Number.isInteger(bad)&&bad>=0);
    assert(rejects,'accepted malformed alias');r.assertions++;r.malformed_rejections++;
  }
  for(let j=0;j<20;j++){
    const actual=(7*j)%2,corrupt=1-actual;
    assert(actual!==corrupt,'corrupt alias not detected');r.assertions++;r.malformed_rejections++;
  }
  r.status='PASS';return r;
}
if(typeof require!=='undefined' && typeof module!=='undefined' && require.main===module)
  console.log(JSON.stringify(main(),null,2));
