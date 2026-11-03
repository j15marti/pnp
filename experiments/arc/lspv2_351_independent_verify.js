#!/usr/bin/env node
'use strict';
// No-import independent JS implementation of LSPV-2 351 checks.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
let checks=0;
function assert(c,why){checks++;if(!c)throw Error(why||'mismatch');}
const rho=[];for(const x of [-1,0,1])for(const y of [-1,0,1])for(const z of [-1,0,1])rho.push([x,y,z]);
function truth(fn){let x=0;for(let k=0;k<8;k++){const a=[k&1,(k>>1)&1,(k>>2)&1];if(fn(a))x|=(1<<k);}return x;}
function sub(x,fix){let y=0;for(let k=0;k<8;k++){let addr=0;for(let i=0;i<3;i++)addr|=(fix[i]<0?((k>>i)&1):fix[i])<<i;y|=((x>>addr)&1)<<k;}return y;}
function support(x){let m=0;for(let i=0;i<3;i++){for(let k=0;k<8;k++){if(((x>>k)&1)!==((x>>(k^(1<<i)))&1)){m|=1<<i;break;}}}return m;}
function eqn(m,b){return truth(a=>a.reduce((s,v,i)=>s^((m>>i&1)&v),0)===b);}
function eqsub(mask,rhs,fix){for(let i=0;i<3;i++)if(fix[i]>=0&&(mask>>i&1)){rhs^=fix[i];mask&=~(1<<i);}return [mask,rhs];}
let and=0,imp=0,supp=0,aff=0,gate=0,gc=0,gn=0;
const tables=rho.map(p=>Array.from({length:256},(_,t)=>sub(t,p)));
for(let i=0;i<27;i++){
  const s=tables[i];
  for(let a=0;a<256;a++){
    assert((support(s[a])&~support(a))===0,'support');supp++;
    for(let b=0;b<256;b++){
      assert(s[a&b]===(s[a]&s[b]),'AND');and++;
      if(!(a&(~b&255))){assert(!(s[a]&(~s[b]&255)),'implication');imp++;}
    }
  }
}
for(const p of rho)for(let x=0;x<16;x++)for(let y=0;y<16;y++){
  const a=x>>1,b=x&1,c=y>>1,d=y&1;
  const [ar,br]=eqsub(a,b,p),[cr,dr]=eqsub(c,d,p),[er,fr]=eqsub(a^c,b^d,p);
  assert((ar^cr)===er&&(br^dr)===fr,'GF2 sum');
  assert(sub(eqn(a,b),p)===eqn(ar,br),'GF2 restriction');aff++;
}
for(let g=0;g<16;g++)for(const a of [-1,0,1])for(const b of [-1,0,1]){
  const values=new Set();
  for(let x=0;x<2;x++)for(let y=0;y<2;y++)values.add((g>>((a<0?x:a)+2*(b<0?y:b)))&1);
  if(a>=0||b>=0){if(values.size===1)gc++;else gn++;}gate++;
}
const z=truth(a=>a[0]),a=truth(a=>a[1]),b=truth(a=>a[2]);
const restrict=[0,-1,-1];
assert(sub(z|a,restrict)===a && sub((255^z)|b,restrict)===255,'RES pinned parents');
assert(sub(a|b,restrict)===(a|b) && (a|b)!==a,'RES weakening');
function models(cla,n){let out=0;for(let x=0;x<(1<<n);x++)if(cla.every(c=>c.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0))))out++;return out;}
assert(models([[1],[-1]],2)===0 && models([[1,2],[-1,2]],2)===2,'SAT/UNSAT');
const edges=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
function k4(ch){let n=0;for(let a=0;a<64;a++)if([0,1,2,3].every(v=>edges.reduce((s,e,j)=>s^(e.includes(v)?((a>>j)&1):0),0)===ch[v]))n++;return n;}
assert(k4([1,0,0,0])===0 && k4([0,0,0,0])===8,'K4');
function parse(src){const ss=src.trim().split('\n').filter(s=>s.trim()&&!s.startsWith('c'));
  const h=ss[0].trim().split(/\s+/);
  if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!/^\d+$/.test(h[2])||!/^\d+$/.test(h[3]))throw Error('header');
  if(ss.length!==Number(h[3])+1)throw Error('count');
  return ss.slice(1).map(line=>{const t=line.trim().split(/\s+/);
    if(t.length<2||t[t.length-1]!=='0'||t.slice(0,-1).includes('0'))throw Error('termination');
    const c=t.slice(0,-1).map(Number);
    if(c.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>Number(h[2]))||new Set(c).size!==c.length)throw Error('literal');
    return c;});
}
const bad=['p cnf 1 2\n1 0','p cnf 1 1\n2 0','p cnf 1 1\n0','p cnf 1 1\nx 0','q cnf 1 1\n1 0','p cnf 1 1\n1 1 0'];
for(const s of bad){let rejected=false;try{parse(s);}catch(e){rejected=true;}assert(rejected,'accepted malformed');}
function resolve(c,d,p){if(!c.includes(p)||!d.includes(-p))throw Error('pivot');const s=new Set([...c,...d]);s.delete(p);s.delete(-p);for(const v of s)if(s.has(-v))throw Error('tautology');return [...s];}
assert(resolve([1],[-1],1).length===0,'upper certificate');
for(const [c,d,p] of [[[1],[-1],2],[[1,2],[1,-2],1]]){let rejected=false;try{resolve(c,d,p);}catch(e){rejected=true;}assert(rejected,'forged certificate');}
const bytes=fs.readFileSync(path.resolve(__dirname,'../../results/raw/arc/2026-11-02_2216_LSPV2_LOCAL_RESTRICTION_PIVOT_FIREWALL351.json'));
const raw=JSON.parse(bytes);
const counts={and_commutations:and,local_implication_restrictions:imp,support_shrink_checks:supp,affine_row_pair_restrictions:aff,gate_partial_cases:gate,gate_constant_outputs_after_pinning:gc,gate_nonconstant_outputs_after_pinning:gn};
for(const [key,n] of Object.entries(counts))assert(raw[key]===n,'raw '+key);
assert(raw.signed_resolution_counterexample.alias_fails===true,'raw pivot');
console.log(JSON.stringify({pass:true,assertions:checks,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),...counts,odd_even_k4:[0,8],bad_inputs_rejected:6,forged_pivots_rejected:2}));
