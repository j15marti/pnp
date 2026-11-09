'use strict';
// Independent JS finite replay of LSPV-2/508; not native FLMV or R_mix341.
const crypto=require('crypto');
const assert=require('node:assert/strict');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;
function source(charge){
  let out=['p cnf 6 16'];
  for(let v=0;v<4;v++){
    const inc=[];
    edges.forEach(([a,b],i)=>{if(a===v||b===v)inc.push(i+1)});
    assert.equal(inc.length,3);checks++;
    for(let mask=0;mask<8;mask++){
      const bits=[mask>>2&1,mask>>1&1,mask&1];
      if((bits[0]^bits[1]^bits[2])!==charge[v]){
        out.push(inc.map((e,i)=>(bits[i]?-e:e)).join(' ')+' 0');
      }
    }
  }
  assert.equal(out.length,17);checks++;
  return out.join('\n')+'\n';
}
function parse(src){
  if(!src.endsWith('\n')||src.includes('\r'))return null;
  const rows=src.slice(0,-1).split('\n');
  if(rows.length!==17||rows[0]!=='p cnf 6 16')return null;
  const clauses=[];
  for(const row of rows.slice(1)){
    const tokens=row.split(' ');
    if(tokens.length!==4||tokens[3]!=='0')return null;
    const lits=[];
    for(let i=0;i<3;i++){
      const t=tokens[i],n=Number(t);
      if(!Number.isInteger(n)||String(n)!==t||Math.abs(n)<1||Math.abs(n)>6)return null;
      lits.push(n);
    }
    if(new Set(lits.map(Math.abs)).size!==3)return null;
    clauses.push(lits);
  }
  return clauses;
}
function decide(src){
  const clauses=parse(src);if(!clauses)return 'MALFORMED';
  for(let mask=0;mask<64;mask++){
    let success=true;
    for(const clause of clauses){
      let sat=false;
      for(const lit of clause){
        let bit=(mask>>(Math.abs(lit)-1))&1;
        if(lit<0)bit^=1;
        if(bit){sat=true;break}
      }
      if(!sat){success=false;break}
    }
    if(success)return 'SAT';
  }
  return 'UNSAT';
}
function guest(src,checkpoint,writeH=false){
  return {label:decide(src),post:{pc:'CONTINUE',h:writeH?0:checkpoint.h,scope:checkpoint.scope},reads:Buffer.byteLength(src)*8,liveInH:false};
}
function follow(res,even,odd,overwrite=false){
  let h=overwrite?0:res.post.h;
  return [res.label,decide(h?odd:even)];
}
function check(){
  const even=source([0,0,0,0]);const odd=source([1,0,0,0]);const malformed=odd.replace('p cnf 6 16','p cnf 6 17');
  assert.equal(decide(even),'SAT');checks++;
  assert.equal(decide(odd),'UNSAT');checks++;
  assert.equal(decide(malformed),'MALFORMED');checks++;
  for(let v=0;v<16;v++){
    const chi=[v&1,v>>1&1,v>>2&1,v>>3&1],src=source(chi),clauses=parse(src);
    assert.equal(decide(src),(chi.reduce((a,b)=>a^b,0))?'UNSAT':'SAT');checks++;
    for(let mask=0;mask<64;mask++){
      const x=Array.from({length:6},(_,i)=>mask>>i&1);
      const model=clauses.every(C=>C.some(lit=>x[Math.abs(lit)-1]===(lit>0?1:0)));
      const parity=Array.from({length:4},(_,node)=>{
        let value=0;edges.forEach(([a,b],i)=>{if(a===node||b===node)value^=x[i]});return value===chi[node];
      }).every(Boolean);
      assert.equal(model,parity);checks++;
    }
  }
  const summary={test:'LSPV2-508 independent JS',checks:0,pairs:0,unsafe:0,correct_output_caches:0,safe_early_overwrites:0,
    sha256_even_source:crypto.createHash('sha256').update(even).digest('hex'),sha256_odd_source:crypto.createHash('sha256').update(odd).digest('hex'),source_bytes_even:Buffer.byteLength(even)};
  for(const [label,src] of [['SAT',even],['UNSAT',odd],['MALFORMED',malformed]]){
    for(const [a,b] of [[0,1],[1,0]]){
      const cp0={pc:'GUEST',h:a,scope:'shared'};const cp1={pc:'GUEST',h:b,scope:'shared'};
      const v0=guest(src,cp0),v1=guest(src,cp1);
      assert.equal(v0.label,label);assert.equal(v1.label,label);checks+=2;
      assert.equal(v0.reads,v1.reads);assert.equal(v0.liveInH,false);checks+=2;
      assert.notEqual(v0.post.h,v1.post.h);checks++;
      const correct0=follow(v0,even,odd),correct1=follow(v1,even,odd);
      assert.notDeepEqual(correct0,correct1);checks++;
      const illegal={...v1,post:v0.post};
      assert.deepEqual(follow(illegal,even,odd),correct0);checks++;
      assert.notDeepEqual(follow(illegal,even,odd),correct1);checks++;
      const legal={...v1,label:v0.label};
      assert.deepEqual(follow(legal,even,odd),correct1);checks++;
      assert.deepEqual(follow(v0,even,odd,true),follow(v1,even,odd,true));checks++;
      assert.deepEqual(follow(guest(src,cp0,true),even,odd),follow(guest(src,cp1,true),even,odd));checks++;
      summary.pairs++;summary.unsafe++;summary.correct_output_caches++;summary.safe_early_overwrites++;
    }
  }
  summary.checks=checks;
  console.log(JSON.stringify(summary,null,2));
}
check();
