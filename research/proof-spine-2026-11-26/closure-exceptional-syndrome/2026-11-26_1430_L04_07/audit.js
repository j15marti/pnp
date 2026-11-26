function run(){
let assertions=0;const check=x=>{assertions++;if(!x)throw Error("assertion "+assertions)};
const f=s=>"1".repeat(s.length)+"0"+s,b=n=>n.toString(2);
const M=[[0,1,0,2,2,0,0,2],[0,2,0,0,1,0,1,2],[0,0,0,1,0,0,2,2],[2,1,0,2,1,0,0,2],[2,2,0,2,2,0,0,2],[2,0,0,0,0,0,1,2]];
const deadline=m=>4*2**m-m-3;
function encode(rows,x,t,N=0){let w=f(rows.map(r=>r.map(z=>f(b(z))).join("")).join(""))+f(x)+f(b(t));return w+"0".repeat(Math.max(0,N-w.length))}
function decode(w,h,tick){tick(w.length);let j=0;function get(s,p){let z=p;while(s[z]==="1")z++;if(s[z]!=="0"||2*z+1-p>s.length)throw Error("frame");return[s.slice(z+1,2*z+1-p),2*z+1-p]}let a,x,t;[a,j]=get(w,j);[x,j]=get(w,j);[t,j]=get(w,j);if(!/^0*$/.test(w.slice(j))||!/^0+$/.test(x)||!/^(0|1[01]*)$/.test(t))throw Error("promise");let rows=[],p=0;while(p<a.length){let r=[];for(let k=0;k<8;k++){let s;[s,p]=get(a,p);if(!/^(0|1[01]*)$/.test(s))throw Error("field");r.push(parseInt(s,2))}if(r[0]===1||r[2]||r[5]||r[7]!==2||r[6]>2||r[1]>2||r[4]>2)throw Error("rule");rows.push(r)}let T=Number(t.length?parseInt(t,2):0);if(BigInt(T)>BigInt(w.length)**BigInt(h))throw Error("clock");let hash=2166136261;for(let s of w)hash=Math.imul(hash^s.charCodeAt(0),16777619);tick(w.length);return{rows,m:x.length,T,hash:(hash>>>0).toString(16)}}
function meter(N){let n=0;return {tick:v=>{n+=v;if(n>32*N)throw Error("CAP")},get:()=>n}}
function lane(w,h,method){let c=meter(w.length),hash;try{let F=decode(w,h,c.tick);hash=F.hash;return{...method(F,c.tick),hash,ops:c.get()}}catch(e){if(String(e).includes("CAP"))return{label:"UNKNOWN",hash,ops:c.get(),cap:true};throw e}}
function replay(F,tick,observe=()=>{},limit=F.T){let tape=Array(F.m).fill(1),q=0,p=0,s=0;observe(q,p,tape,s);
while(s<limit&&q!==1){let a=tape[p]||0,r=null;for(let z of F.rows){tick(1);if(z[0]===q&&z[1]===a){if(r)throw Error("nondet");r=z}}if(!r)break;if(p>=0&&p<F.m)tape[p]=r[4];else if(r[4]!==0)throw Error("outside");q=r[3];p+=[-1,1,0][r[6]];s++;observe(q,p,tape,s)}return {steps:s,label:q===1?"YES":"NO"}}
const recognize=F=>JSON.stringify(F.rows)===JSON.stringify(M);
function B(F,tick){tick(F.rows.length+F.m);if(!recognize(F))return{label:"UNKNOWN"};let d=deadline(F.m);return{label:F.T>=d?"YES":"NO",d}}
function C(F,tick){tick(F.rows.length+F.m);if(!recognize(F))return{label:"UNKNOWN"};let d=4;for(let i=2;i<=F.m;i++){tick(1);d=2*d+i+1}return{label:F.T>=d?"YES":"NO",d}}
function pc(y){let c=0;while(y){y&=y-1;c++}return c}
function potential(m,q,p,tape){let y=0;for(let i=0;i<m;i++){check(tape[i]===1||tape[i]===2);if(tape[i]===2)y+=2**i}const H=n=>4*(2**m-1-n)-m+2*pc(n)+1;if(q===1){check(p===m&&y===0);return 0}if(q===0){check(p>=0&&p<=m&&y%2**p===0);return H(y+2**p-1)-p}check(q===2&&p>=-1&&p<m);return H(y)+p+2}
let records=[],tot={A:0,B:0,C:0,I:0},refSteps=0,mutations=0,summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}};
for(let h of [2,4])for(let m of [2,4,6,8,10,12,14,16,18]){
 let d=deadline(m),N=Math.max(encode(M,"0".repeat(m),d).length,Math.ceil(d**(1/h)));while(BigInt(N)**BigInt(h)<BigInt(d))N++;
 for(let t of [d-1,d]){
 let w=encode(M,"0".repeat(m),t,N),truth=t===d?"YES":"NO";check(w.length===N);
 let A=lane(w,h,(F,tick)=>replay(F,tick)),b0=lane(w,h,B),c0=lane(w,h,C);
 let I=lane(w,h,(F,tick)=>{tick(F.rows.length+F.m);check(F.hash===b0.hash&&F.hash===c0.hash);if(!recognize(F)||b0.d!==c0.d)return{label:"UNKNOWN"};return{label:F.T>=b0.d?"YES":"NO",d:b0.d}});
 for(let [key,r] of [["A",A],["B",b0],["C",c0],["I",I]]){check(r.label===truth||r.label==="UNKNOWN");tot[key]+=r.ops;summary[key][r.label]++}check(I.label===truth);check(A.ops+b0.ops+c0.ops+I.ops<=128*N+1);
 let F=decode(w,h,()=>{});let r=replay(F,()=>{},(q,p,tape,s)=>{check(potential(m,q,p,tape)===d-s)},d);check(r.steps===d&&r.label==="YES");refSteps+=r.steps;
 records.push({h,m,N,t,d,minQuotientBlocks:d+1,hash:F.hash,A:A.label,B:b0.label,C:c0.label,I:I.label,ops:[A.ops,b0.ops,c0.ops,I.ops]});
 }
 // mutant: make blank overflow return instead of accept. Both template lanes must refuse.
 let rows=M.map(r=>r.slice());rows[2][3]=0;let w=encode(rows,"0".repeat(m),d,N);check(lane(w,h,B).label==="UNKNOWN"&&lane(w,h,C).label==="UNKNOWN");mutations++;
}
return{assertions,summary,tot,refSteps,mutations,records,scope:"exact framed deterministic counter U_h; sequential independent lanes, 32N logical scan cap with rejected over-cap probe, not bit-time; reference replay separate, no SAT or CNF backend"};
}
console.log(JSON.stringify(run(),null,2));
