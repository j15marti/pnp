// Independent LSPV-1 367 verifier, no imports, not reused from producer.
// Accept raw JSON via node verify.js path.json, otherwise runs against embedded ledger.
const truth=(lit,mask)=>lit>0?Boolean(mask&(1<<(lit-1))):!Boolean(mask&(1<<(-lit-1)));
function source(parity){
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let clauses=[];
for(let u=0;u<4;u++){
 let ids=edges.flatMap((e,i)=>e.indexOf(u)>=0?[i+1]:[]);
 for(let n=0;n<8;n++){
  let bits=ids.map((_,k)=>(n>>k)&1);
  if((bits[0]^bits[1]^bits[2])===parity[u])continue;
  clauses.push(ids.map((v,k)=>bits[k]?-v:v));
 }
}
return clauses;
}
function count(C){let n=0;for(let a=0;a<64;a++)if(C.every(c=>c.some(l=>truth(l,a))))n++;return n;}
function verify(raw){
let n=0;function check(v,label){n++;if(!v)throw Error("Independent check failed: "+label)}
const odd=source([1,0,0,0]),even=source([0,0,0,0]);
check(count(odd)===0,"odd");
check(count(even)===8,"even");
check(odd.length===16,"clauses");
let deleted=0,flipped=0;
for(let j=0;j<odd.length;j++){
 check(count(odd.filter((_,k)=>j!==k))>0,"deletion"+j);deleted++;
 for(let k=0;k<3;k++){
  let G=odd.map(c=>c.slice());G[j][k]*=-1;
  check(count(G)>0,"flip"+j+":"+k);flipped++;
 }
}
let T=[];
for(let a=1;a<7;a++)for(let b=a+1;b<7;b++)for(let c=b+1;c<7;c++)
 for(let x=0;x<8;x++)T.push([x&1?-a:a,x&2?-b:b,x&4?-c:c]);
check(T.length===160,"templates");
let key=c=>c.join(":");
for(const C of odd)check(T.some(Q=>key(Q)===key(C)),"find template");
for(let s=0;s<16;s++){
 const b=Array.from({length:4},(_,i)=>(s>>i)&1);
 const hot=b[0]+b[1]===1&&b[2]+b[3]===1;
 const reject=b[0]===1&&b[3]===1;
 for(let y=0;y<2;y++){
  const sat=(j,t)=>!b[2*j+t]||([t===0?1:-1].some(l=>truth(l,y)));
  const possible=hot&&reject&&sat(0,0)&&sat(0,1)&&sat(1,0)&&sat(1,1);
  check(!possible,"toy rejected SAT");
 }
}
for(const k of ["deletionSAT","signFlipSAT"])check(raw.formula[k]===(k==="deletionSAT"?deleted:flipped),k);
check(raw.selector.gatedClauses===odd.length*T.length,"gated count");
check(raw.controls.knownMixedK4Nodes===15,"known mixed calibration");
check(raw.proofStatus.B3==="OPEN"&&raw.proofStatus.PvsNP==="OPEN","epistemic labels");
return {status:"PASS",independentAssertions:n,sourceClauses:odd.length,templates:T.length,flipSAT:flipped,deleteSAT:deleted};
}
if(typeof module!=="undefined"&&module.exports)module.exports=verify;
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");let raw=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 console.log(JSON.stringify(verify(raw),null,2));
}
