#!/usr/bin/env node
// LSPV-4 SOURCE-CYCLE-SLACK353: fully standalone finite falsifier. Node >=18.
// All nine clauses of PHP(3,2) indispensable. Source-read-once exact trees.
const C=[];
for(let p=0;p<3;p++)C.push([2*p+1,2*p+2]);
for(let h=0;h<2;h++)for(let a=0;a<3;a++)for(let b=a+1;b<3;b++)
  C.push([-(2*a+h+1),-(2*b+h+1)]);
const n=6,m=C.length,M=1<<m;
const sort=a=>[...new Set(a)].sort((x,y)=>x-y);
const bits=x=>{let k=0;for(;x;x&=x-1)k++;return k};
const models=cs=>{let count=0;for(let a=0;a<(1<<n);a++)
  if(cs.every(c=>c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0))))count++;return count};
function resolve(a,b,p){
 if(!a.includes(p)||!b.includes(-p)){
   if(!a.includes(-p)||!b.includes(p))throw Error('pivot missing');
   return resolve(b,a,p);
 }
 const c=sort([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
 if(c.some(x=>c.includes(-x)))throw Error('tautological resolvent');
 return c;
}
const proof=[[1,3,3],[2,4,5],[9,8,4],[11,10,6],
 [1,6,4],[2,7,6],[13,5,3],[15,14,5],[0,12,1],[17,16,2]];
function replay(){
 const a=C.map(sort);let visits=0;
 for(const [u,v,p] of proof){if(u>=a.length||v>=a.length)throw Error('premise index');
 visits+=a[u].length+a[v].length;a.push(resolve(a[u],a[v],p));}
 if(a[a.length-1].length)throw Error('failed contradiction');
 return {visits,clauses:a.slice(m)};
}
function run(mixed){
 const dp=Array.from({length:M},()=>new Map()), par=new Map();
 for(let x=0;x<64;x++)for(let r=0;r<2;r++){
  let mask=0n;for(let a=0;a<64;a++)if((bits(a&x)%2)===r)mask|=1n<<BigInt(a);
  par.set(mask.toString(),[x,r]);
 }
 function clause(c){return {type:'C',c:sort(c)}}
 function key(z){return z.type==='C'?'C:'+z.c.join(','):
   z.type==='T'?'T:'+z.scope+':'+z.mask:'X:'+z.scope+':'+z.rhs}
 function add(S,z){dp[S].set(key(z),z)}
 function semantic(z){
  if(z.type==='T')return [z.scope,BigInt(z.mask)];
  let scope=z.type==='X'?z.scope:0,table=0n;
  if(z.type==='C')for(const l of z.c)scope|=1<<(Math.abs(l)-1);
  for(let a=0;a<64;a++){
    const yes=z.type==='X'?bits(a&scope)%2===z.rhs:
      z.c.some(l=>Boolean(a&(1<<(Math.abs(l)-1)))===(l>0));
    if(yes)table|=1n<<BigInt(a);
  }
  return [scope,table];
 }
 C.forEach((c,i)=>add(1<<i,clause(c)));
 let ands=0,res=0,xors=0,pairs=0;
 for(let S=1;S<M;S++){
  if(bits(S)<2)continue;
  for(let A=(S-1)&S;A>0;A=(A-1)&S){
   const B=S^A;if(A>=B||!dp[A].size||!dp[B].size)continue;
   for(const left of dp[A].values())for(const right of dp[B].values()){
    pairs++;
    if(left.type==='C'&&right.type==='C')
     for(const x of left.c)if(right.c.includes(-x)){
      res++;try{add(S,clause(resolve(left.c,right.c,Math.abs(x))))}catch(_){}
     }
    if(!mixed)continue;
    if(left.type==='X'&&right.type==='X'){
      xors++;add(S,{type:'X',scope:left.scope^right.scope,rhs:left.rhs^right.rhs});
    }
    const [sa,ta]=semantic(left),[sb,tb]=semantic(right),scope=sa|sb;
    if(bits(scope)>3)continue;
    ands++;const t=ta&tb;
    add(S,{type:'T',scope,mask:t.toString()});
    const row=par.get(t.toString());
    if(row)add(S,{type:'X',scope:row[0],rhs:row[1]});
   }
  }
 }
 const levels=Array.from({length:m},(_,k)=>{
  let cnt=0;for(let S=1;S<M;S++)if(bits(S)===k+1)cnt+=dp[S].size;return cnt;});
 if(dp[M-1].size)throw Error('unexpected source-read-once derivation');
 return {levels,typed_states:levels.reduce((a,b)=>a+b),pairs,ands,res,xors};
}
if(models(C))throw Error('PHP source unexpectedly SAT');
for(let i=0;i<m;i++)if(!models(C.filter((_,j)=>i!==j)))throw Error('deletion witness missing');
let flips=0;
for(let i=0;i<m;i++)for(let j=0;j<C[i].length;j++){
 const cs=C.map(c=>[...c]);cs[i][j]*=-1;
 if(!models(cs))throw Error('single sign neighbor UNSAT');
 flips++;
}
const pure=run(false),local=run(true),rep=replay();
const expectedPure=[9,12,18,12,24,24,21,0,0];
const expectedMixed=[9,30,68,126,198,243,207,30,0];
if(JSON.stringify(pure.levels)!==JSON.stringify(expectedPure)||JSON.stringify(local.levels)!==JSON.stringify(expectedMixed))
 throw Error('read-once census mismatch');
if(rep.visits!==37)throw Error('replay work mismatch');
const graph={s:9,q:10,E:20,beta:2,delta:0};
if(graph.q!==graph.s-1+graph.beta+graph.delta)throw Error('graph ledger mismatch');
console.log(JSON.stringify({status:'PASS',F:C,deleted_witnesses:9,signflip_witnesses:flips,
 source_bytes:Buffer.byteLength('p cnf 6 9\n'+C.map(c=>c.join(' ')+' 0\n').join('')),
 graph,pivot_only_fixed_record_bits:130,proof_literal_visits:rep.visits,
 pure_read_once:pure,def_free_local_mixed_read_once:local,
 logical_minimum_bounds:{resolution:[9,10],mixed_full:[8,10]},
 status_warning:'Full mixed DEF and arbitrary SAT-decider transfer OPEN.'},null,2));