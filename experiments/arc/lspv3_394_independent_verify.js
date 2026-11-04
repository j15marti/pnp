#!/usr/bin/env node
'use strict';
// Independent no-dependency Node verifier for LSPV-3/394.
// No imports from Python producer; checks 268 finite cases and raw hashes.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function serialize(n,clauses){
  return Buffer.from('p cnf '+n+' '+clauses.length+'\n'+clauses.map(c=>c.join(' ')+(c.length?' ':'')+'0\n').join(''),'ascii');
}
function parse(bytes){
  const text=bytes.toString('ascii');
  if(!Buffer.from(text,'ascii').equals(bytes))throw Error('nonascii');
  const lines=text.replace(/\n$/,'').split('\n'),m=/^p cnf (\d+) (\d+)$/.exec(lines[0]);
  if(!m||lines.length!==Number(m[2])+1)throw Error('header');
  const n=Number(m[1]);
  const clauses=lines.slice(1).map(line=>{
    const vals=line.split(/\s+/).map(Number);
    if(!vals.length||vals.at(-1)!==0||vals.slice(0,-1).some(z=>!Number.isInteger(z)||z===0||Math.abs(z)>n))throw Error('clause');
    return vals.slice(0,-1);
  });
  return {n,clauses};
}
function php(h){
  const v=(i,j)=>i*h+j+1,clauses=[];
  for(let i=0;i<=h;i++)clauses.push(Array.from({length:h},(_,j)=>v(i,j)));
  for(let j=0;j<h;j++)for(let i=0;i<=h;i++)for(let k=i+1;k<=h;k++)clauses.push([-v(i,j),-v(k,j)]);
  return serialize(h*(h+1),clauses);
}
function isphp(bytes){
  let f;try{f=parse(bytes)}catch(e){return false}
  let h=1;while(h*(h+1)<f.n)h++;
  return h*(h+1)===f.n&&bytes.equals(php(h));
}
function encode(bytes){
  let original,valid=true;try{original=parse(bytes)}catch(e){valid=false;original={n:0,clauses:[]}}
  const recognized=valid&&isphp(bytes);
  const clauses=recognized?[[]]:valid?original.clauses.map(c=>c.map(z=>2*z)):[];
  for(let i=0;i<8*bytes.length;i++){
    const b=(bytes[i>>3]>>(7-(i&7)))&1;
    for(let r=0;r<2;r++){
      const j=2*i+r,a=4*j+3,z=a-2;
      clauses.push([z,-z,b?a:-a]);
    }
  }
  return serialize(Math.max(original.n*2,64*bytes.length-1,0),clauses);
}
function inverse(encoded){
  const f=parse(encoded),t=new Map();
  for(const c of f.clauses)if(c.length===3&&c[0]>0&&c[0]%4===1&&c[1]===-c[0]&&Math.abs(c[2])===c[0]+2){
    const j=(c[0]-1)/4;if(t.has(j))throw Error('duplicate tag');
    t.set(j,Number(c[2]>0));
  }
  if(t.size===0)return Buffer.alloc(0);
  if(t.size%16)throw Error('length');
  const out=Buffer.alloc(t.size/16);
  for(let i=0;i<t.size/2;i++){
    const a=t.get(2*i),b=t.get(2*i+1);
    if(a===undefined||a!==b)throw Error('bad paired tag');
    out[i>>3]|=a<<(7-(i&7));
  }
  return out;
}
function sat(f){
  for(let mask=0;mask<(1<<f.n);mask++)
    if(f.clauses.every(c=>c.some(z=>((mask>>(Math.abs(z)-1))&1)===Number(z>0))))return true;
  return false;
}
function main(){
  const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),controls=[];
  const cs=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
  for(let mask=0;mask<256;mask++)controls.push(serialize(2,cs.filter((_,j)=>(mask>>j)&1)));
  for(let h=1;h<=3;h++)controls.push(php(h));
  controls.push(Buffer.alloc(0),Buffer.from('p cnf 2 1\n1 0\n1 0\n'),Buffer.from('p cnf a b\n'),
    Buffer.from('bad'),Buffer.from([0,255]),Buffer.from('p cnf 0 1\n0\n'),
    Buffer.from('p cnf 2 1\n3 0\n'),Buffer.from('p cnf 2 1\n1 2\n'),Buffer.from('p cnf 1 0\nextra\n'));
  let valid=0,invalid=0,recognized=0,corruptions=0,phpHashes=[];
  for(const input of controls){
    const output=encode(input),rec=parse(output);
    assert(inverse(output).equals(input));
    let f;try{f=parse(input);valid++}catch(e){invalid++}
    const special=isphp(input);
    if(special){
      recognized++;assert(rec.clauses.some(c=>c.length===0));assert(!sat(f));
      phpHashes.push({source:sha(input),output:sha(output),bytes:output.length,clauses:rec.clauses.length});
    }else if(f){
      const projected=rec.clauses.slice(0,f.clauses.length).map(c=>c.map(z=>z/2));
      assert.deepStrictEqual(projected,f.clauses);
      if(f.n<=4)assert.strictEqual(sat(f),sat({n:f.n,clauses:projected}));
    }
    const tags=rec.clauses.filter(c=>c.length===3&&c[0]>0&&c[0]%4===1&&c[1]===-c[0]&&Math.abs(c[2])===c[0]+2);
    assert.strictEqual(tags.length,16*input.length);
    assert(tags.every(c=>c.includes(-c[0])));
    if(tags.length){
      tags[0][2]*=-1;
      assert.throws(()=>inverse(serialize(rec.n,rec.clauses)));
      corruptions++;
    }
  }
  assert.strictEqual(controls.length,raw.cases);
  assert.strictEqual(valid,raw.valid);assert.strictEqual(invalid,raw.invalid);
  assert.strictEqual(recognized,raw.recognized_php);
  assert.strictEqual(corruptions,raw.single_bit_corruptions_rejected);
  for(const f of phpHashes)assert(raw.php_cases.some(c=>c.source_sha256===f.source&&c.encoded_sha256===f.output&&c.output_bytes===f.bytes&&c.output_clauses===f.clauses));
  console.log(JSON.stringify({status:'PASS',cases:controls.length,valid,invalid,recognized_php:recognized,corrupted_tags_rejected:corruptions}));
}
main();
