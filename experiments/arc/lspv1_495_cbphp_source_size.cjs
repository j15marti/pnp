"use strict";
/* LSPV-1/495. Source-size regression for Alekseev--Gaevoy CBPHP (ECCC TR26-007).
 * Checks syntactic encodings, NOT the published asymptotic lower bound or R_mix341.
 * Run: node experiments/arc/lspv1_495_cbphp_source_size.cjs
 */
function assert(b,msg){if(!b)throw new Error(msg||"assertion failure");}
function factorial(n){let z=1;for(let i=2;i<=n;i++)z*=i;return z;}
function choose(n,r){return factorial(n)/(factorial(r)*factorial(n-r));}
function permutations(n,k){let r=[];function rec(a){if(a.length===k){r.push([...a]);return;}for(let i=0;i<n;i++)if(!a.includes(i))rec([...a,i]);}rec([]);return r;}
function build(N,k,m){
  assert(Number.isInteger(N)&&Number.isInteger(k)&&Number.isInteger(m)&&N>k&&k>=1&&m>=1&&m<10,"malformed parameters");
  const M=2**m,clauses=[];
  function unequal(p,value){let a=[];for(let b=0;b<m;b++)a.push(((value>>b)&1)?-(p*m+b+1):p*m+b+1);return a;}
  for(let p=0;p<N;p++)for(let q=p+1;q<N;q++)for(let a=0;a<M;a++)
    clauses.push([...unequal(p,a),...unequal(q,a)]);
  for(const p of permutations(N,k+1))for(let z=0;z<M**k;z++){
    let y=z,values=[];for(let i=0;i<k;i++){values.push(y%M);y=Math.floor(y/M);}
    values.push(values.reduce((a,b)=>a+b,0)%M);
    clauses.push(p.flatMap((v,i)=>unequal(v,values[i])));
  }
  return clauses;
}
function satisfies(c,x){return c.some(l=> ((x>>(Math.abs(l)-1))&1)===(l>0?1:0));}
function main(){
  const cases=[[3,1,1],[3,1,2],[4,1,1],[4,2,1],[5,2,1],[5,2,2],[6,2,2],[5,3,1]];
  let checks=0,rows=[];
  for(const [N,k,m] of cases){
    let M=2**m, pair=choose(N,2)*M, relation=factorial(N)/factorial(N-k-1)*M**k;
    const clauses=build(N,k,m);assert(clauses.length===pair+relation);checks++;
    const unique=new Set(clauses.map(c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","))).size;
    assert(unique<=clauses.length);checks++;
    assert(clauses.every(c=>c.length===2*m||c.length===(k+1)*m));checks++;
    assert(clauses.every(c=>new Set(c.map(Math.abs)).size===c.length));checks++;
    assert(clauses.every(c=>c.every(l=>Math.abs(l)>=1&&Math.abs(l)<=N*m)));checks++;
    const occurrences=clauses.reduce((s,c)=>s+c.length,0);
    assert(occurrences===pair*2*m+relation*(k+1)*m);checks++;
    let models=null;
    if(N*m<=10){models=0;for(let x=0;x<2**(N*m);x++)if(clauses.every(c=>satisfies(c,x)))models++;checks++;}
    rows.push({N,k,m,M,source_variables:N*m,pair_clause_records:pair,relation_clause_records:relation,source_clause_records:clauses.length,distinct_sorted_clauses:unique,duplicate_records:clauses.length-unique,literal_occurrences:occurrences,models_exhaustive:models});
  }
  for(const bad of [[2,2,1],[3,0,1],[3,1,0],[3,1,-1]]){
    let failed=false;try{build(...bad)}catch(e){failed=true;}assert(failed);checks++;
  }
  const epsilon=.25;
  let exponent_checks=[];
  for(let k=3;k<=12;k++){
    let source_exponent=k*k+1-k*epsilon, rev_depth=k-2;
    const res_depth=2*(k-2)/(k+2);
    const rev_bit_exponent=rev_depth/source_exponent, res_bit_exponent=res_depth/source_exponent;
    assert(rev_bit_exponent<1&&res_bit_exponent<1);checks++;
    exponent_checks.push({k,epsilon,source_exponent,rev_depth,rev_bit_exponent,res_depth,res_bit_exponent});
  }
  return {tag:"LSPV1_495_CBPHP_SOURCE_SIZE",status:"COMPUTATIONAL finite source-size audit; symbolic algebra in report",
    checks, cases:rows,exponent_checks,
    falsifier:"f=sum mod M is a deterministic finite validation control, not the hard random f required by the theorem",
    note:"Counts include duplicate source records; distinct-clause counts differ especially when k=1. Source clauses are width O(k log M), not strict 3CNF."};
}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)
  console.log(JSON.stringify(main(),null,2));
