// TMR-1/047 audit: node experiments/tmr/tmr1_tally_ne_padding047.js
function run(){
"use strict";
const magic="00110101";let assertions=0,failures=0,cases=0,totalBits=0,yes=0,no=0,minN=Infinity,maxN=0;
function ok(v,msg){assertions++;if(!v){failures++;throw Error(msg)}}
function pop(x){return [...x].filter(c=>c==="1").length}
function idx(x){return 2**x.length+Number.parseInt(x||"0",2)}
function word(n){let m=Math.floor(Math.log2(n));return m?(n-2**m).toString(2).padStart(m,"0"):""}
function gamma(n){return "0".repeat(n.toString(2).length-1)+n.toString(2)}
function parity(a){return (a&1)^((a>>1)&1)^((a>>2)&1)}
function xor(b){let out=[];for(let a=0;a<8;a++)if(parity(a)!==b)out.push([1,2,3].map((j,k)=>(a>>k)&1?-j:j));return out}
function gen(n){let x=word(n),sat=pop(x)%2===1,clauses=xor(0);if(!sat)clauses.push(...xor(1));for(let k=0;k<n;k++)clauses.push([4+3*k,5+3*k,6+3*k]);return {n,sat,vars:3+3*n,clauses}}
function serialize(F){let w=Math.ceil(Math.log2(F.vars+1)),s=magic+gamma(F.vars)+gamma(F.clauses.length);for(let c of F.clauses)for(let l of c)s+=Math.abs(l).toString(2).padStart(w,"0")+(l<0?"1":"0");return s}
function parse(s){let i=8;if(s.slice(0,8)!==magic)throw Error("magic");function g(){let z=0;while(s[i]==="0"){z++;i++}let b=s.slice(i,i+z+1);i+=z+1;return Number.parseInt(b,2)}let vars=g(),count=g();if(!(vars>=3&&count>=1&&vars<1e7&&count<1e7))throw Error("count");let w=Math.ceil(Math.log2(vars+1));if(i+3*count*(w+1)!==s.length)throw Error("length");let clauses=[];for(let j=0;j<count;j++){let c=[];for(let k=0;k<3;k++){let id=Number.parseInt(s.slice(i,i+w),2);i+=w;let sign=s[i++];if(id<1||id>vars||!["0","1"].includes(sign))throw Error("literal");c.push(sign==="1"?-id:id)}if(new Set(c.map(Math.abs)).size!==3)throw Error("proper");clauses.push(c)}return {vars,clauses}}
function exhaustive(F){for(let mask=0n;mask<(1n<<BigInt(F.vars));mask++){if(F.clauses.every(c=>c.some(l=>{let bit=(mask>>BigInt(Math.abs(l)-1))&1n;return l<0?bit===0n:bit===1n})))return true}return false}
function decide(s){let f;try{f=parse(s)}catch(_){return false}for(let n of [f.clauses.length-4,f.clauses.length-8])if(n>=1&&gen(n).vars===f.vars&&serialize(gen(n))===s)return gen(n).sat;return exhaustive(f)}
for(let m=0;m<=8;m++)for(let v=0;v<2**m;v++){let x=m?v.toString(2).padStart(m,"0"):"",n=idx(x),f=gen(n),s=serialize(f),parsed=parse(s);ok(word(n)===x,"dyadic");ok(f.sat===(pop(x)%2===1),"label");ok(f.vars===3+3*n,"vars");ok(f.clauses.length===n+(f.sat?4:8),"clauses");ok(parsed.vars===f.vars&&JSON.stringify(parsed.clauses)===JSON.stringify(f.clauses),"parser");ok(s.length>=n,"honesty");ok(f.clauses.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper");ok(decide(s)===f.sat,"recognizer");if(n<=4)ok(exhaustive(parsed)===f.sat,"exhaustive");if(f.sat)yes++;else no++;cases++;totalBits+=s.length;minN=Math.min(minN,s.length);maxN=Math.max(maxN,s.length)}
let sat=serialize({vars:3,clauses:[[1,2,3]]}),unsat=serialize({vars:3,clauses:[...xor(0),...xor(1)]});ok(decide(sat),"fallback SAT");ok(!decide(unsat),"fallback UNSAT");ok(!decide("1"+sat.slice(1)),"bad magic");ok(!decide(sat+"1"),"trailing input");ok(sat!==serialize(gen(1))&&unsat!==serialize(gen(1)),"offfamily");
return {run_id:"TMR1_TALLY_NE047",execution:"native V8 exact code",status:"COMPUTATIONAL, finite dyadic and proper 3CNF checks only",index_min:1,index_max:511,cases,sat_cases:yes,unsat_cases:no,assertions,failures,encoded_length_min:minN,encoded_length_max:maxN,total_encoded_bits_examined:totalBits,nonfamily_controls:4,encoding:"magic8/gamma-var/gamma-clause/3x fixed-width signed literals",theorem_status:"symbolic PROVED/RESTRICTED, external independent review OPEN",E_vs_NE:"OPEN",P_vs_NP:"OPEN"};
}
console.log(JSON.stringify(run(),null,2));
