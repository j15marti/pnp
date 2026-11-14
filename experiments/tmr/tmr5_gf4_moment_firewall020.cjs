'use strict';
const audit20 = function audit20(){
"use strict";
const ok=(v,msg)=>{if(!v)throw Error(msg)};
const mul=(a,b)=>{let x=a&1,y=(a>>1)&1,u=b&1,v=(b>>1)&1;return ((x*u)^(y*v))|(((x*v)^(y*u)^(y*v))<<1)};
const pow=(a,n)=>{let p=1;for(let i=0;i<n;i++)p=mul(p,a);return p};
const ext=(f,n)=>{let q=0;for(let a=0;a<(1<<n);a++){if(!f(a))continue;let z=1;for(let i=0;i<n;i++)z=mul(z,((a>>i)&1)?2:3);q^=z;}return q};
const bits=F=>F.map(s=>[0,1,2].map(j=>(s>>j)&1).join("")).join("");
const moments=F=>[F.length,...[1,2,3,4,5,6,7].map(S=>F.reduce((v,s)=>v+(((s&S).toString(2).replace(/0/g,"").length%2)?-1:1),0))];
const scan=B=>{let p=-1,t=0,seen=0,first=null,partial=0,k=0,malformed=false; p++;t++;for(let j=0;j<B.length;j++){let bit=B[p];if(bit!=="0"&&bit!=="1")malformed=true;if(!malformed){partial|=Number(bit)<<k;k++;if(k===3){if(first===null)first=partial;seen|=1<<partial;partial=0;k=0;}}p++;t++;}if(k)malformed=true;if(first===0&&!malformed){while(p>-1){p--;t++;}while(p<B.length){p++;t++;}}t+=2;return{T:t,S:1,label:malformed?"MALFORMED":seen===255?"UNSAT":"SAT",first,seen,head:p}};
for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++)ok(mul(mul(a,b),c)===mul(a,mul(b,c)),"field associative");
ok(pow(2,3)===1&&pow(3,3)===1,"field order");
let fnCount=0,zeros={};
for(let n=1;n<=4;n++){let count=0;for(let tt=0;tt<(1<<(1<<n));tt++){let v=ext(a=>(tt>>a)&1,n);if(tt!==0&&v===0)count++;fnCount++;}zeros[n]=count;}
ok(zeros[1]===0&&zeros[2]===3&&zeros[3]===63&&zeros[4]===16383,"zero collision count");
ok(ext(a=>a!==0,3)===0,"OR3 true yet extension zero");
ok(ext(a=>((a&1)^((a>>1)&1)),2)===0,"XOR2 true yet extension zero");
let weights=0;for(let b=1;b<=10;b++)for(let a=0;a<(1<<b);a++){let q=1;for(let i=0;i<b;i++)q=mul(q,((a>>i)&1)?2:3);ok(q!==0&&q===pow(2,2*b-a.toString(2).replace(/0/g,"").length),"oracle weight");weights++;}
let pairs=0,tracePairs=0,examples=[];
for(let r=1;r<=128;r++){let U=[],S=Array(8*r).fill(0);for(let s=0;s<8;s++)for(let j=0;j<r;j++)U.push(s);
const fU=a=>U.every(s=>s!==a),fS=a=>S.every(s=>s!==a);
ok(Array.from({length:8},(_,a)=>fU(a)).filter(Boolean).length===0,"U UNSAT");
ok(Array.from({length:8},(_,a)=>fS(a)).filter(Boolean).length===7,"S SAT");
ok(ext(fU,3)===0&&ext(fS,3)===0,"GF4 same-label collision");
ok(bits(U).length===bits(S).length&&bits(S).length===24*r,"equal L");
ok(JSON.stringify(moments(U))!==JSON.stringify(moments(S)),"degree3 detects labels");pairs++;
let G=U.slice();[G[0],G[r]]=[G[r],G[0]];
ok(JSON.stringify(moments(U))===JSON.stringify(moments(G)),"H3 permutation equality");
let a=scan(bits(U)),b=scan(bits(G)),L=24*r;
ok(a.label==="UNSAT"&&b.label==="UNSAT"&&a.seen===255&&b.seen===255,"both-label physical");
ok(a.first===0&&b.first===1&&a.T===3*(L+1)+2&&b.T===L+3,"physical exact charged trace");
ok(a.S===1&&b.S===1&&a.head===L&&b.head===L,"space,head");tracePairs++;
if([1,2,16,128].includes(r))examples.push({r,L,delay_input:a,permuted_input:b});}
let controls=0;for(let m=0;m<=3;m++){const max=8**m;for(let t=0;t<max;t++){let z=t,F=[];for(let j=0;j<m;j++){F.push(z%8);z=Math.floor(z/8);}let s=scan(bits(F));ok(s.label==="SAT"&&s.S===1,"easy E3");controls++;}}
for(let s of ["0","01","0001","10100"]){ok(scan(s).label==="MALFORMED","malformed");controls++;}
const cases=[["Horn",3,[[1],[-1,2],[-2,3]]],["Horn_unsat",3,[[1],[-1,2],[-2,3],[-3]]],["2SAT",3,[[1,2],[-1,3],[-2,-3]]],["XOR_even",3,[[1,2,3],[-1,-2,3],[-1,2,-3],[1,-2,-3]]],["XOR_odd",3,[[-1,-2,-3],[1,2,-3],[1,-2,3],[-1,2,3]]],["product",6,[[1,2,3],[-1,-2,-3],[4,5,6],[-4,-5,-6]]],["aux_lift",4,[[1,2,4],[1,2,-4]]],["renamed",5,[[2,4,5],[-2,4,5]]],["duplicate",3,Array(16).fill([1,2,3])]];
let genericAssignments=0;
for(let [name,n,F]of cases){let models=0;for(let a=0;a<(1<<n);a++){let satisfied=F.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0))));models+=Number(satisfied);genericAssignments++;}if(name==="Horn_unsat")ok(models===0,"Horn unsat");if(name==="aux_lift")ok(models===12,"aux lift");}
return{status:"COMPUTATIONAL",model:"fixed 3-variable three-sign-bit clause stream E3, physical one-head finite control",oracle_model:"opaque Boolean-value oracle only",all_boolean_functions_b1_to_b4:fnCount,sat_functions_with_zero_extension_by_b:zeros,oracle_nonzero_weights:weights,equal_length_opposite_label_pairs_r1_to128:pairs,same_complete_H3_different_trace_pairs_r1_to128:tracePairs,physical_examples:examples,scanner_controls:controls,generic_cnf_controls:cases.length,generic_cnf_truth_assignments:genericAssignments,failures:0,note:"hosted V8 directly evaluated exact published function. Not a generic 3-SAT TM compiler."};
};
const result = audit20();
if (typeof console !== 'undefined') console.log(JSON.stringify(result, null, 2));
