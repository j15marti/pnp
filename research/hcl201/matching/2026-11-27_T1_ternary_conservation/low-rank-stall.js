module.exports=function test(sha){
const M=x=>(x%3+3)%3,enc=x=>JSON.stringify(x)+"\n";let state=0x9261f03a,draws=0;function rnd(){state^=state<<13;state^=state>>>17;state^=state<<5;draws++;return (state>>>0)%3}
let d=8,m=24,dirs=Array.from({length:d},(_,i)=>Array.from({length:d},(_,j)=>+(i===j))),candidateTests=0,directionChecks=0;
function key(a){let k=a.find(x=>x);return k?a.map(x=>M(k*x)).join(""):"zero"}
let forbidden=new Set(dirs.map(key));function mark(a,b){for(let c of [1,2])forbidden.add(key(a.map((x,i)=>M(x+c*b[i]))))}
for(let i=0;i<dirs.length;i++)for(let j=0;j<i;j++)mark(dirs[i],dirs[j]);
while(dirs.length<m&&candidateTests<10000){candidateTests++;let a=Array.from({length:d},rnd);let k=key(a);if(k==="zero"||forbidden.has(k))continue;a=k.split("").map(Number);for(let b of dirs)mark(a,b);dirs.push(a);forbidden.add(k)}
if(dirs.length!==m)throw Error("direction budget");
for(let i=0;i<m;i++)for(let j=0;j<i;j++)for(let k=0;k<j;k++){directionChecks++;let u=key(dirs[i]),v=key(dirs[j]),w=key(dirs[k]);if(u===v||u===w||v===w||[1,2].some(c=>key(dirs[j].map((x,t)=>M(x+c*dirs[k][t])))===u))throw Error("dependent triple")}
let offsetAttempts=0,evaluationWork=0;
function enumerate(b){let count=0,witness=null;for(let i=0;i<3**d;i++){let z=[],w=i;for(let j=0;j<d;j++){z.push(w%3);w=Math.floor(w/3)}let ok=true;for(let j=0;j<m;j++){evaluationWork++;let x=M(b[j]+dirs[j].reduce((q,a,k)=>q+a*z[k],0));if(x===2){ok=false;break}}if(ok){count++;witness=z}}return{count,witness}}
let b,result;do{offsetAttempts++;b=Array.from({length:m},rnd);result=enumerate(b)}while(result.count&&offsetAttempts<1000);
if(result.count)throw Error("offset budget");
let satB=Array(m).fill(0),sat=enumerate(satB);
let proof={format:"T1-F3-BOOL-AFFINE-v1",d,directions:dirs,offsets:b},control={format:proof.format,d,directions:dirs,offsets:satB};let artifact={format:"T1-F3-LOW-RANK-STALL-CERT-v1",model:proof.format,instance_id:proof.format+":sha256:"+sha(enc(proof)),N_bits:enc(proof).length*8,input:proof,guard_id:"EMPTY",residual_id:"ROOT",original_ids:Array.from({length:m},(_,i)=>i+1),parent_ids:[],claim:"No Boolean point in the affine carrier, but all rank<=2 observation subspaces have full affine hull after their own coordinate exclusions. Every triple of distinct normalized directions is independent. Scope: explicit affine chart only, no strict E/B adapter asserted.",control:{instance_id:control.format+":sha256:"+sha(enc(control)),N_bits:enc(control).length*8,input:control,...sat},result,metrics:{candidateTests,directionChecks,offsetAttempts,evaluationWork,draws,seed:"0x9261f03a"},checker:"recompute directions, independence of every triple, enumerate all 3^d chart words (diagnostic finite check); rank<=2 proof uses independent constraints allowing two values each."};
return artifact;
}
