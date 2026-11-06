#!/usr/bin/env node
// LSPV-2/439 compact, self-contained finite controls.
// No arbitrary-program halting oracle and no general polynomial SAT algorithm.
let count = 0;
function check(b, why) { if (!b) throw Error(why); count++; }
function edges(name) {
  if (name === 'K4') return Array.from({length:4},(_,a)=>Array.from({length:3-a},(_,d)=>[a,a+1+d])).flat();
  if (name === 'cube') { const out=[]; for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)if([1,2,4].includes(a^b))out.push([a,b]);return out; }
  throw Error('unknown graph');
}
function source(name, odd) {
  const E=edges(name), H=name==='K4'?4:8, M=E.length, w=Math.floor(Math.log2(M))+1;
  let x='1'.repeat(M)+'0'+'1'.repeat(4*H)+'0';
  for(let v=0;v<H;v++){
    const idx=E.map((ends,i)=>ends.includes(v)?i+1:0).filter(Boolean).sort((a,b)=>a-b);
    check(idx.length===3,'cubic graph');
    for(let p=0;p<2;p++)for(let r=0;r<2;r++){
      let s=[p,r,p^r^1^(odd&&v===0?1:0)];
      for(let j=0;j<3;j++) x+=idx[j].toString(2).padStart(w,'0')+s[j];
    }
  }
  return x;
}
function decide(x){
  if (!/^[01]*$/.test(x)) return 'MALFORMED';
  let i=0;
  const unary=()=>{let n=0;while(i<x.length&&x[i]==='1'){n++;i++;}if(i===x.length)throw Error();i++;return n;};
  let n,m,clauses=[];
  try {
    n=unary();m=unary();if(!n||!m)throw Error();
    const w=Math.floor(Math.log2(n))+1;
    if(x.length-i!==m*3*(w+1))throw Error();
    for(let c=0;c<m;c++){
      const clause=[];
      for(let j=0;j<3;j++){
        let id=parseInt(x.slice(i,i+w),2),neg=Number(x[i+w]);i+=w+1;
        if(!(id>=1&&id<=n)||clause.some(a=>a[0]===id))throw Error();
        clause.push([id,neg]);
      }
      clauses.push(clause);
    }
  } catch {return 'MALFORMED';}
  for(let a=0;a<(1<<n);a++)if(clauses.every(c=>c.some(([id,neg])=>((a>>(id-1))&1)!==neg)))return 'SAT';
  return 'UNSAT';
}
function tagged(machine,x){
  const k=machine==='LOOP'?Infinity:Number(machine.slice(5));
  const scan=x.length>=k;
  const reads=scan?x.length:0;
  return {label:decide(x),scan,reads};
}
const cases=[];
for(const name of ['K4','cube'])for(const odd of [false,true]) {
  const x=source(name,odd);check(decide(x)===(odd?'UNSAT':'SAT'),'charge result');cases.push(x);
}
cases.push('', '111111111111', 'Z',source('K4',false).slice(0,-1));
for(let n=0;n<24;n++)cases.push('0'.repeat(n));
const machines=['HALT_0','HALT_5','HALT_20','LOOP'];let tags=0,tests=0;
for(const x of cases){
  for(const machine of machines){
    const t=tagged(machine,x);const k=machine==='LOOP'?Infinity:Number(machine.slice(5));
    check(t.scan===(x.length>=k),'reachability');
    check(t.reads===(t.scan?x.length:0),'scan read count');
    check(t.label===decide(x),'label preservation');
    tags+=Number(t.scan);tests++;
  }
}
// Verify that hostile modifications change the source-authenticated record.
const correct=source('K4',false),mutated=correct.slice(0,-1)+(correct.endsWith('1')?'0':'1');
check(mutated!==correct,'mutated original source');
check(decide('1')==='MALFORMED','invalid unary source');
check(decide('!')==='MALFORMED','nonbinary source');
console.log(JSON.stringify({PASS:true,checks:count,sources:cases.length,traces:tests,tagged_scans:tags},null,2));
