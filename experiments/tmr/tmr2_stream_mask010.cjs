'use strict';
// TMR-2/010: canonical XOR-free eight-mask block template, source-level audit.
// The reader below never decrements its source cursor. Native JS execution is
// NOT a physical multitape Turing-machine simulation.
const assert = (condition, message) => { if (!condition) throw Error(message); };
const popcount = n => { let p=0; while(n>0){p+=n%2;n=Math.floor(n/2);} return p; };
const rho = i => 2*i+(popcount(i)%2);
const width = r => Math.ceil(Math.log2(6*r+2));
const isCoreId = (id,t) => {const i=Math.floor(id/2);return i>=1&&i<=t&&(id%2)===(popcount(i)%2);};
function make(r,masksByBlock) {
  assert(Number.isSafeInteger(r)&&r>0&&r<=100000,'invalid fixture size');
  const t=3*r,w=width(r),N=2**w-1;
  const mask = masksByBlock || Array.from({length:r},()=>[1,2,3,4,5,6,7,7]);
  const spare=[];for(let id=1;id<=N;id++)if(!isCoreId(id,t))spare.push(id);
  const K=Math.ceil(spare.length/3),M=8*r+K;
  let source='1'.repeat(N)+'0'+'1'.repeat(M)+'0';
  const append = (id,neg) => { source+=String(neg)+id.toString(2).padStart(w,'0'); };
  for(let g=0;g<r;g++){
    assert(mask[g].length===8,'eight masks');
    for(const m of mask[g])for(let j=0;j<3;j++)append(rho(3*g+j+1),(m>>j)&1);
  }
  for(let k=0;k<spare.length;k+=3){
    const group=spare.slice(k,k+3);
    for(const id of spare){if(group.length===3)break;if(!group.includes(id))group.push(id);}
    for(const id of group)append(id,0);
  }
  assert(source.length===N+M+2+3*M*(w+1),'length');
  return {source,r,N,M,K,w,t};
}
function scanTemplate(s) {
  let pos=0,reads=0;
  const get=()=>{reads++;return pos<s.length?s[pos++]:null;};
  const unary=()=>{let count=0,ch;while((ch=get())==='1')count++;return ch==='0'?count:null;};
  const N=unary();if(N===null)return {decision:null,reads};
  const M=unary();if(M===null)return {decision:null,reads};
  if(!Number.isSafeInteger(N)||!Number.isSafeInteger(M))return {decision:null,reads};
  if(M<=Math.ceil(N/3)||(M-Math.ceil(N/3))%7!==0)return {decision:null,reads};
  const r=(M-Math.ceil(N/3))/7;
  if(!Number.isSafeInteger(r)||r<1||r>100000)return {decision:null,reads};
  const w=width(r),t=3*r;
  if(N!==2**w-1||M!==8*r+Math.ceil((N-t)/3))return {decision:null,reads};
  if(s.length!==N+M+2+3*M*(w+1))return {decision:null,reads};
  function readField(expectedId,allowSign) {
    const sign=get();if(sign===null||(sign!=='0'&&sign!=='1'))return null;
    if(!allowSign&&sign!=='0')return null;
    const bits=expectedId.toString(2).padStart(w,'0');
    for(let k=0;k<w;k++)if(get()!==bits[k])return null;
    return +sign;
  }
  let unsat=false;
  for(let g=0;g<r;g++){
    const ids=[rho(3*g+1),rho(3*g+2),rho(3*g+3)];
    let seen=0;
    for(let c=0;c<8;c++){
      let mask=0;
      for(let j=0;j<3;j++){const z=readField(ids[j],true);if(z===null)return {decision:null,reads};mask|=z<<j;}
      seen|=1<<mask;
    }
    if(seen===255)unsat=true;
  }
  const spareCount=N-t;
  let next=1,used=0,first=[];
  function nextSpare(){
    while(next<=N&&isCoreId(next,t))next++;
    if(next>N)return null;
    const id=next++;if(first.length<2)first.push(id);used++;return id;
  }
  for(let k=0;k<Math.ceil(spareCount/3);k++){
    const ids=[];
    for(let j=0;j<3&&used<spareCount;j++)ids.push(nextSpare());
    for(let j=0;ids.length<3;j++){
      assert(j<first.length,'filler wrap');
      if(!ids.includes(first[j]))ids.push(first[j]);
    }
    for(const id of ids)if(readField(id,false)===null)return {decision:null,reads};
  }
  if(pos!==s.length)return {decision:null,reads};
  return {decision:unsat?'UNSAT':'SAT',reads,r,N,M,w};
}
function exactCoreSAT(masks) {
  const r=masks.length, t=3*r;
  for(let a=0;a<2**t;a++){
    let good=true;
    for(let g=0;g<r;g++){
      const assignment=(a>>(3*g))&7;
      if(masks[g].includes(assignment)){good=false;break;}
    }
    if(good)return true;
  }
  return false;
}
function rng(seed){let x=seed>>>0;return()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return x>>>0;};}
function flip(s,i){return s.slice(0,i)+(s[i]==='0'?'1':'0')+s.slice(i+1);}
function run(){
  const rand=rng(0x61A9E23D),out={tag:'TMR2-STREAM-MASK-010',seed:'0x61A9E23D',status:'COMPUTATIONAL',nativeNode:process.version,sizes:[],totals:{structured:0,structuredSAT:0,structuredUNSAT:0,brute:0,unsatTriples:0,malformedFallback:0,sourceReads:0},failures:0};
  for(const r of [1,2,3,4,6,8,12,16]){
    const samples=r<=4?350:200;let localSAT=0,localUNSAT=0,brute=0;
    const src=make(r),chk=scanTemplate(src.source);
    assert(chk.decision==='SAT'&&chk.reads<=src.source.length+2,'base source');
    out.totals.structured++;out.totals.structuredSAT++;out.totals.sourceReads+=chk.reads;
    for(let g=0;g<r;g++){
      const masks=Array.from({length:r},()=>[1,2,3,4,5,6,7,7]);
      masks[g][7]=0;
      const d=make(r,masks),v=scanTemplate(d.source);
      assert(v.decision==='UNSAT','triple neighbor');
      assert(d.source.length===src.source.length,'neighbor length');
      let hd=0;for(let i=0;i<d.source.length;i++)hd+=(d.source[i]!==src.source[i]);
      assert(hd===3,'triple support size');
      out.totals.unsatTriples++;out.totals.structured++;out.totals.structuredUNSAT++;
      out.totals.sourceReads+=v.reads;
    }
    for(let z=0;z<samples;z++){
      const masks=Array.from({length:r},()=>Array.from({length:8},()=>rand()%8));
      if(z%4===0)masks[z%r]=[0,1,2,3,4,5,6,7];
      const d=make(r,masks),v=scanTemplate(d.source);
      const expected=masks.some(row=>(new Set(row)).size===8)?'UNSAT':'SAT';
      assert(v.decision===expected,'mask acceptance');
      if(r<=4){assert((v.decision==='SAT')===exactCoreSAT(masks),'independent assignment brute');brute++;}
      localSAT+=(expected==='SAT');localUNSAT+=(expected==='UNSAT');
      out.totals.structured++;out.totals.structuredSAT+=(expected==='SAT');out.totals.structuredUNSAT+=(expected==='UNSAT');out.totals.brute+=r<=4?1:0;out.totals.sourceReads+=v.reads;
    }
    for(const pos of [0,src.N+1,src.N+src.M+3,src.source.length-1]){
      const bad=flip(src.source,pos),res=scanTemplate(bad);
      assert(res.decision===null,'hostile mutated template must take fallback');out.totals.malformedFallback++;
    }
    out.sizes.push({r,N:src.N,M:src.M,L:src.source.length,w:src.w,samples,randomSAT:localSAT,randomUNSAT:localUNSAT,brute});
  }
  return out;
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={make,scanTemplate,exactCoreSAT,run};
