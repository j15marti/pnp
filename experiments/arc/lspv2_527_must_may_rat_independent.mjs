#!/usr/bin/env node
// LSPV-2/527 standalone independent restricted DRAT-minus MUST/MAY audit.
// Exact R_mix341 grammar and same-FLMV-machine costs are NOT implemented.
let checks=0;
function ok(p,m){checks++;if(!p)throw Error(m)}
function F(k){let a=[];for(let i=0;i<k;i++){let b=2+3*i,c=b+1,d=b+2;a.push([-1,b,c],[1,b,d],[-d,b,c])}return a}
function encoded(f,n){return 'p cnf '+n+' '+f.length+'\n'+f.map(c=>c.join(' ')+' 0\n').join('')}
function read(raw){if(!/^[\x00-\x7f]*$/.test(raw))throw Error('ascii');
 let l=raw.trimEnd().split('\n'),h=l.shift().split(' '),n=+h[2],m=+h[3];
 if(h.length!==4||h[0]!=='p'||h[1]!=='cnf'||!Number.isSafeInteger(n)||n<1||!Number.isSafeInteger(m)||m<0||l.length!==m)throw Error('header');
 return l.map(line=>{let v=line.split(' ').map(Number);if(v.length!==4||v[3]!==0||v.slice(0,3).some(x=>!Number.isSafeInteger(x)||x===0||Math.abs(x)>n)||new Set(v.slice(0,3).map(Math.abs)).size!==3)throw Error('proper clause');return v.slice(0,3)})}
function conflict(F,ass){let map=new Map();for(let x of ass){let a=Math.abs(x),v=x>0;if(map.has(a)&&map.get(a)!==v)return true;map.set(a,v)}
 let more=true;while(more){more=false;for(let d of F){let free=[],sat=false;for(let x of d){let v=map.get(Math.abs(x));if(v===undefined)free.push(x);else if(v===(x>0)){sat=true;break}}if(sat)continue;if(!free.length)return true;if(free.length===1){let x=free[0],a=Math.abs(x),v=x>0;if(map.has(a)){if(map.get(a)!==v)return true}else{map.set(a,v);more=true}}}}return false}
function rup(F,C){return conflict(F,C.map(x=>-x))}
function resolvent(C,D,p){let r=[...new Set([...C.filter(x=>x!==p),...D.filter(x=>x!==-p)])];return r.some(x=>r.includes(-x))?null:r}
function rat(F,C){if(!C.length)return rup(F,C);let p=C[0];for(let d of F){if(d.includes(-p)){let r=resolvent(C,d,p);if(r!==null&&!rup(F,r))return false}}return true}
function projected(M,U,C){if(!C.length)return rup(U,C);let p=C[0];for(let d of M){if(d.includes(-p)){let r=resolvent(C,d,p);if(r!==null&&!rup(U,r))return false}}return true}
let tested=0,rows=[];
for(let k=1;k<=7;k++){let f=F(k),n=3*k+1;ok(JSON.stringify(read(encoded(f,n)))===JSON.stringify(f),'source roundtrip');
 let states=[];for(let mask=0;mask<2**k;mask++){let s=[];for(let i=0;i<k;i++)s.push(f[3*i],f[3*i+(mask>>i&1?1:2)]);states.push(s)}
 let M=Array.from({length:k},(_,i)=>f[3*i]);
 ok(projected(M,f,[1]),'abstract may-RAT');ok(!rup(f,[1]),'nonRUP');
 for(let s of states){ok(!rat(s,[1]),'no actual RAT after policy');ok(!projected(s,s,[1]),'CEGAR singleton refinement');
 for(let c of [[1],[-1],[2],[-2],[1,2],[]]){
 if(rat(s,c))ok(projected(M,f,c),'abstract RAT covers concrete');
 if(rup(s,c))ok(rup(f,c),'abstract RUP covers concrete')
 }tested++}
 ok(rat(f,[1]),'early genuine RAT is allowed');rows.push({k,post_deletion_states:states.length,spurious_abstract:true,concrete_shortcuts:0})}
for(let bad of ['','p cnf 4 1\n-1 2 0\n','p cnf 4 1\n-1 2 2 0\n','p cnf 4 1\n-1 2 5 0\n','p cnf 4 2\n-1 2 3 0\n','p cnf x 1\n-1 2 3 0\n','p cnf 4 1\n-1 2 3 0\né']){let failed=false;try{read(bad)}catch(e){failed=true}ok(failed,'bad source rejected')}
const result={experiment:'LSPV2_527_INDEPENDENT_JS',assertions:checks,post_deletion_sources:tested,malformed:7,rows};
if(typeof console!=='undefined')console.log(JSON.stringify(result,null,2));