'use strict';
// LSPV-3/392 independent finite reviewer: direct assignment evaluation and
// independently reconstructed chain/guard refutation, no producer import.
function valid(C,mask){for(const row of C){let ok=false;for(const lit of row){let b=(mask>>BigInt(Math.abs(lit)-1))&1n;if(b===(lit>0?1n:0n)){ok=true;break;}}if(!ok)return false;}return true;}
function clauses(h,guard){let a=[[1]];for(let i=1;i<=h;i++)a.push([-i,i+1]);a.push([-(h+1)]);return guard?[...a.map(x=>[-(h+2),...x]),[h+2]]:a;}
function resolvent(A,B,v){if(!A.includes(v)||!B.includes(-v))throw Error('pivot');return [...new Set([...A.filter(k=>k!==v),...B.filter(k=>k!==-v)])];}
function inspect(h,guard){let C=clauses(h,guard), current=C[0],steps=0;for(let i=1;i<=h+1;i++){current=resolvent(current,C[i],i);steps++;}
if(guard){current=resolvent(current,C[C.length-1],-(h+2));steps++;}
if(current.length||steps!==(guard?h+2:h+1))throw Error('final contradiction or size');
return {sources:C.length,steps};}
function run(){let assert=0;
for(let h=1;h<=7;h++){for(const guard of [false,true]){let x=inspect(h,guard);assert+=2;
let f=clauses(h,guard),n=BigInt(h+1+(guard?1:0));
if(n>10n)throw Error('too many vars');
let count=0;for(let mask=0n;mask<(1n<<n);mask++)if(valid(f,mask))count++;
if(count!==0)throw Error('UNSAT failed');assert++;
for(let i=0;i<f.length;i++){let z=f.filter((_,j)=>j!==i),found=false;
for(let mask=0n;mask<(1n<<n);mask++)if(valid(z,mask)){found=true;break;}
if(!found)throw Error('source not essential');assert++;
}
} }
let bad=0;try{resolvent([-1],[2],3)}catch(e){bad++;}
if(bad!==1)throw Error('bad pivot accepted');return {schema:'LSPV-3-392-independent/v1',h_range:[1,7],all_sat_unsat_and_deletion_enumerated:true,checks:assert,corruption_rejections:bad};}
if(typeof process!=='undefined')console.log(JSON.stringify(run(),null,2));
