#!/usr/bin/env node
/* Independent finite JS verifier of LSPV-2/399. No producer imports.
 * Exhaustive truth-table SAT and violated-clause enumeration.
 */
'use strict';
function ok(cond,msg){ if(!cond) throw Error(msg); verified++; }
let verified=0;
function graph(n){let e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(n===4 || ((i<3)!==(j<3)))e.push([i,j]);return e;}
function make(n,e,odd){let a=Array.from({length:n},()=>[]);e.forEach(([u,v],j)=>{a[u].push(j+1);a[v].push(j+1)}); let out=[];for(let v=0;v<n;v++){ok(a[v].length===3,'cubic'); for(let bits=0;bits<8;bits++){let parity=((bits&1)+((bits>>1)&1)+((bits>>2)&1))&1;if(parity===(v===0&&odd?1:0))continue;out.push(a[v].map((x,k)=>(bits&(1<<k))?-x:x));}}return out;}
function holds(cl,a){return cl.some(x=>((a>>(Math.abs(x)-1))&1)===(x>0?1:0));}
function firstSat(cs,n){for(let a=0;a<(1<<n);a++)if(cs.every(c=>holds(c,a)))return a;return null;}
function minViol(cs,n){let min=cs.length;for(let a=0;a<(1<<n);a++){let q=0;for(let c of cs)if(!holds(c,a))q++;if(q<min)min=q;}return min;}
function pad(cs,n,r){let arr=[];for(let c of cs){arr.push(c.slice());for(let j=0;j<r;j++){arr.push([...c,n+1+j]);arr.push([...c,-(n+1+j)]);}}return arr;}
function gamma(n){let b=n.toString(2);return '0'.repeat(b.length-1)+b;}
function enc(n,cs){let w=n.toString(2).length,s='110101'+gamma(n)+gamma(cs.length+1);let p=[];for(let c of cs){s+=gamma(c.length+1);for(let x of c){p.push(s.length);s+=(x<0?'1':'0')+Math.abs(x).toString(2).padStart(w,'0');}}return {s,p};}
function parse(s){if(!s.startsWith('110101')||!/^[01]+$/.test(s))throw Error('magic');let i=6;function rd(){let z=0;while(i<s.length&&s[i]==='0')i++,z++;if(i+z>=s.length)throw Error('gamma');let v=parseInt(s.slice(i,i+z+1),2);i+=z+1;return v;}let n=rd(),m=rd()-1;if(n<1||m<0||m>s.length)throw Error('header');let w=n.toString(2).length,cs=[];for(let j=0;j<m;j++){let k=rd()-1;if(k<0||k*(w+1)>s.length-i)throw Error('size');let c=[];for(let t=0;t<k;t++){let sign=s[i],v=parseInt(s.slice(i+1,i+w+1),2);i+=w+1;if(v<1||v>n)throw Error('variable');c.push(sign==='1'?-v:v);}cs.push(c);}if(i!==s.length)throw Error('trail');return cs;}
function toggle(s,p){return s.slice(0,p)+(s[p]==='0'?'1':'0')+s.slice(p+1);}
const results=[];
for(const nV of [4,6]){
 let edges=graph(nV),n=edges.length,odd=make(nV,edges,true),even=make(nV,edges,false);
 ok(firstSat(odd,n)===null,'odd unsat');ok(firstSat(even,n)!==null,'even SAT');
 let {s,p}=enc(n,odd);ok(JSON.stringify(parse(s))===JSON.stringify(odd),'encoding');
 let pivotal=0;
 for(let i=0;i<odd.length;i++)for(let k=0;k<3;k++){
   let changed=parse(toggle(s,p[3*i+k]));ok(firstSat(changed,n)!==null,'source sign pivotal');pivotal++;
 }
 for(const r of [1,2,3]){
   const R=pad(odd,n,r),S=pad(even,n,r),min=minViol(R,n+r);
   ok(min===r+1,'minimum violated clauses');
   ok(firstSat(S,n+r)!==null,'even padding SAT');
   if(r!==1)continue;
   const pp=enc(n+1,R),idx=[];for(let ci=0,flat=0;ci<R.length;ci++){idx.push(flat);flat+=R[ci].length;}
   let single=0,two=0;
   for(let ci=0;ci<R.length;ci++)for(let li=0;li<R[ci].length;li++){
      let mutated=parse(toggle(pp.s,pp.p[idx[ci]+li]));
      ok(firstSat(mutated,n+1)===null,'singleton padded sign');single++;
   }
   for(let ci=0;ci<odd.length;ci++)for(let li=0;li<3;li++){
      let x=pp.p[idx[3*ci]+li],y=pp.p[idx[3*ci+1]+li];
      let mutated=parse(toggle(toggle(pp.s,x),y));
      ok(firstSat(mutated,n+1)!==null,'two-bit block pivotal');two++;
   }
   results.push({vertices:nV,variables:n,clauses:odd.length,original_pivotal:pivotal,all_padded_sign_flips_tested:single,disjoint_pairs_tested:two,min_violated:min});
 }
}
for(const x of ['', '111010','1101010000']){let reject=false;try{parse(x)}catch(e){reject=true;}ok(reject,'malformed rejection');}
const result={status:'COMPUTATIONAL',method:'independent exhaustive JS truth table',assertions:verified,seed:null,results,malformed_rejected:3};
console.log(JSON.stringify(result,null,2));
