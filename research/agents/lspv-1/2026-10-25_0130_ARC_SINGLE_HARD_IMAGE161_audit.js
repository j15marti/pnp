/* ARC-SINGLE-HARD-IMAGE161: toy parity image and two-level closure falsifier.
Run: node 2026-10-25_0130_ARC_SINGLE_HARD_IMAGE161_audit.js
This does NOT model an FLMV hard language or actual Turing-machine cycles. */
function bin(v,w){return v.toString(2).padStart(w,"0")}
function formula(x){let c=[[-1]];for(let i=0;i<x.length;i++){
 const a=i+1,b=i+2;c.push(x[i]==="0"?[a,-b]:[a,b]);c.push(x[i]==="0"?[-a,b]:[-a,-b]);}
 c.push([-(x.length+1)]);return c;}
function rec(c,w){const l=v=>v===0?"0".repeat(w+1):(v>0?"1":"0")+bin(Math.abs(v),w);
return (c.length===2?"1":"0")+l(c[0]||0)+l(c[1]||0);}
function serialize(x){const w=Math.ceil(Math.log2(x.length+2)),c=formula(x);
return bin(x.length+1,16)+bin(c.length,16)+c.map(z=>rec(z,w)).join("")}
function at(x,p){const n=x.length,w=Math.ceil(Math.log2(n+2)),span=2*w+3,m=2*n+2;
if(p<0||p>=32+m*span)throw Error("index");
if(p<16)return bin(n+1,16)[p];if(p<32)return bin(m,16)[p-16];
const j=Math.floor((p-32)/span),r=(p-32)%span;
if(j===0)return rec([-1],w)[r];if(j===m-1)return rec([-(n+1)],w)[r];
const i=Math.floor((j-1)/2),second=(j-1)%2,a=i+1,b=i+2;
return rec(x[i]==="0"?(second?[-a,b]:[a,-b]):(second?[-a,-b]:[a,b]),w)[r]}
function parse(c){if(c.length<4||c.length%2||JSON.stringify(c[0])!=="[-1]")return null;
const n=(c.length-2)/2;if(JSON.stringify(c.at(-1))!==JSON.stringify([-(n+1)]))return null;
let x="";for(let i=0;i<n;i++){let a=i+1,b=i+2,p=JSON.stringify(c[1+2*i]),q=JSON.stringify(c[2+2*i]);
if(p===JSON.stringify([a,-b])&&q===JSON.stringify([-a,b]))x+="0";
else if(p===JSON.stringify([a,b])&&q===JSON.stringify([-a,-b]))x+="1";else return null;}return x;}
function imageSolve(c){const x=parse(c);return x!==null&&[...x].filter(z=>z==="1").length%2===0;}
function brute(c,v){for(let a=0;a<2**v;a++)if(c.every(cl=>cl.some(z=>((a>>(Math.abs(z)-1))&1)===(z>0?1:0))))return true;return false;}
function pin(c,v,b){return c.flatMap(cl=>cl.some(z=>Math.abs(z)===v&&((z>0)===!!b))?[]:[cl.filter(z=>Math.abs(z)!==v)]);}
function must(t,m){if(!t)throw Error(m)}
function run(){let words=0,bits=0,brutes=0;
for(let n=1;n<=9;n++)for(let a=0;a<2**n;a++){const x=bin(a,n),c=formula(x),s=serialize(x);
for(let k=0;k<s.length;k++){must(s[k]===at(x,k),"wrong virtual bit");bits++;}
const label=[...x].filter(z=>z==="1").length%2===0;
must(parse(c)===x&&imageSolve(c)===label,"wrong image bit");
if(n<=7){must(brute(c,n+1)===label,"wrong SAT");brutes++;}words++;}
const p=formula("0000"),c=pin(p,1,0),g=pin(c,2,0);
must(brute(p,5)&&brute(c,5)&&brute(g,5),"two-level semantics");
must(imageSolve(p)&&!imageSolve(c)&&!imageSolve(g),"lost image promise");
must(brute([[1]],1)&&!imageSolve([[1]]),"offimage SAT");
return {run:"ARC-SINGLE-HARD-IMAGE161",status:"PASS",source_words:words,virtual_bit_comparisons:bits,brute_sat_checks:brutes,
two_level_sat:true,two_level_exits_promise:true,off_image_sat_false_negative:true,
scope:"toy even-parity 2CNF image; no FLMV hard source or TM resource measurement"};}
if(typeof console!=="undefined")console.log(JSON.stringify(run(),null,2));
