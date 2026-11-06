#!/usr/bin/env node
// LSPV-4/429 finite independent construction/verifier. Not native FLMV timing.
import fs from 'node:fs';
import crypto from 'node:crypto';
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const mag='10101110';
function graph(which){const n=which==='K4'?4:8,edges=[];
  for(let a=0;a<n;a++) for(let b=a+1;b<n;b++){
    const x=a^b;
    if(which==='K4'||(x>0&&(x&(x-1))===0))edges.push([a,b]);
  } return [n,edges];
}
function parityClauses(which,odd){const [n,edges]=graph(which),cls=[];
  for(let v=0;v<n;v++){const inc=edges.flatMap(([a,b],idx)=>(a===v||b===v)?[idx+1]:[]);
    if(inc.length!==3)throw Error('noncubic graph');
    for(let z=0;z<8;z++){
      const bits=[(z>>2)&1,(z>>1)&1,z&1];
      if((bits[0]^bits[1]^bits[2])!==((odd&&v===0)?1:0))
        cls.push(inc.map((e,j)=>bits[j]?-e:e));
    }
  }return [cls,edges.length];
}
function code(l){const s=Math.abs(l).toString(2);
  return (l<0?'1':'0')+'1'.repeat(s.length)+'0'+s;
}
function enc(core,tail,b){return mag+'1'.repeat(b)+'0'+
  core.map(c=>'10'+c.map(code).join('')).join('')+
  tail.map(c=>'11'+c.map(code).join('')).join('')+'00';
}
function tailFor(vars,k,x){const b=vars.toString(2).length,base=2**b;
  return Array.from({length:k},(_,i)=>[(x&(1<<i))?base+3*i:-(base+3*i),
    base+3*i+1,base+3*i+2]);
}
function parse(str){
  let i=0;
  const rd=()=>{if(i>=str.length||!/[01]/.test(str[i]))throw Error('invalid input');return str[i++];};
  if(Array.from({length:8},rd).join('')!==mag)throw Error('wrong magic');
  let b=0;while(rd()==='1')b++;
  let nCore=0,nTail=0,tail=false,cut=-1;
  while(true){
    const start=i,tag=rd()+rd();
    if(tag==='00'){
      if(i!==str.length||nCore===0)throw Error('invalid end');
      if(cut<0)cut=start;return {cut,nCore,nTail};
    }
    if(tag!=='10'&&tag!=='11')throw Error('invalid clause tag');
    const t=(tag==='11');
    if(t){nTail++;if(!tail)cut=start;tail=true;}
    else{if(tail)throw Error('invalid core ordering');nCore++;}
    let positive=false;
    for(let j=0;j<3;j++){
      const sign=rd();if(sign==='0')positive=true;
      let k=0;while(rd()==='1')k++;
      if(k===0||rd()!=='1')throw Error('noncanonical ID');
      for(let a=1;a<k;a++)rd();
      if(t&&k<=b)throw Error('tail aliases core');
      if(!t&&k>b)throw Error('core beyond namespace');
    }
    if(t&&!positive)throw Error('no tail witness');
  }
}
// If supplied, replay raw JSON from the expanded Python producer.
// Otherwise a self-contained 4 x 16-source independent construction check.
const filename=process.argv[2],raw=filename?JSON.parse(fs.readFileSync(filename,'utf8')):null;
let checks=0,calls=0,full=0;
const cases=raw?raw.cases:[
 {graph:'K4',odd:false},{graph:'K4',odd:true},
 {graph:'cube',odd:false},{graph:'cube',odd:true}
];
for(const row of cases){
  const [core,n]=parityClauses(row.graph,row.odd),b=n.toString(2).length;
  let projected=null,distinct=new Set();
  for(let t=0;t<16;t++){
    const src=enc(core,tailFor(n,4,t),b),p=parse(src);checks++;
    const coreSource=src.slice(0,p.cut)+'00';parse(coreSource);checks++;
    if(projected!==null&&coreSource!==projected)throw Error('mismatched core');
    projected=coreSource;distinct.add(src);checks++;
    if(t===0&&raw&&sha(src)!==row.source_sha256)throw Error('source hash mismatch');
    checks++;
  }
  if(distinct.size!==16)throw Error('duplicate descendants');checks++;
  if(raw&&(projected.length!==row.core_bits||[...distinct][0].length!==row.child_bits))
    throw Error('length mismatch');
  checks+=2;
  if(raw&&(row.full_read_runs!==16||row.certified_projected_runs!==1))
    throw Error('guest count mismatch');
  checks+=2;calls++;full+=16;
}
if(raw&&(calls!==raw.certified_projected_guest_calls||
         full!==raw.full_read_anchor_guest_calls||raw.malformed_acceptance!==0))
  throw Error('summary mismatch');
checks+=3;
console.log(JSON.stringify({independent_checks:checks,portfolios:cases.length,
  children:full,guest_calls_after_projection:calls},null,2));
