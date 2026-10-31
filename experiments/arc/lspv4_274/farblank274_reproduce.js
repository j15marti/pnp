'use strict';
// LSPV-4 FARBLANK274 self-contained Node.js reproducible audit.
const result = (()=>{
const cases=[],U=[0,1,2,3,4,5,6,7],forbid=a=>[1,2,3].map(i=>(a>>(i-1))&1?-i:i);
const uns=U.map(forbid),sat=U.filter(a=>a!==5).map(forbid),ren=F=>F.map(c=>c.map(l=>Math.abs(l)===1?-l:l));
for(const [name,cls] of [["U8",uns],["S7",sat],["PARITY_SAT",[1,2,4,7].map(forbid)],["U8_RENAME",ren(uns)],["S7_RENAME",ren(sat)],["HORN_SAT",[[-1,-2,3],[-1,-3,2]]],["KROM_SAT",[[1,2,3],[1,2,-3],[-1,-2,3],[-1,-2,-3]]],["U8_DUP",uns.concat(uns)],["S7_DUP",sat.concat(sat)]])cases.push({name,n:3,clauses:cls});
let tests=0;const ck=(p,m)=>{tests++;if(!p)throw Error(m)};
const tc=(C,a)=>C.reduce((z,l)=>z+((((a>>(Math.abs(l)-1))&1)===(l>0?1:0))?1:0),0);
const holds=(F,a)=>F.clauses.every(c=>tc(c,a)>0);
const cnt=(F,a)=>[0,1,2,3].map(v=>F.clauses.filter(c=>tc(c,a)===v).length);
const serial=F=>"p cnf "+F.n+" "+F.clauses.length+"\n"+F.clauses.map(c=>c.join(" ")+" 0\n").join("");
function dpll(F){const stat={nodes:0,branch:0,literals:0};
function walk(a){stat.nodes++;for(;;){let change=false;for(const C of F.clauses){let ok=false,u=[];for(const l of C){stat.literals++;const v=a[Math.abs(l)];if(v===-1)u.push(l);else if(v===(l>0?1:0)){ok=true;break}}if(ok)continue;if(!u.length)return false;if(u.length===1){let l=u[0],j=Math.abs(l),v=l>0?1:0;if(a[j]!==-1&&a[j]!==v)return false;if(a[j]===-1){a[j]=v;change=true}}}if(!change)break}
let all=true;for(const C of F.clauses){let yes=false,unk=false;for(const l of C){stat.literals++;const v=a[Math.abs(l)];if(v===-1)unk=true;else if(v===(l>0?1:0)){yes=true;break}}if(!yes){if(!unk)return false;all=false}}if(all)return true;
const i=a.findIndex((x,j)=>j>0&&x===-1);if(i<0)throw Error("bad residual");stat.branch++;for(const v of [0,1]){const b=a.slice();b[i]=v;if(walk(b))return true}return false}
return {sat:walk(Array(F.n+1).fill(-1)),...stat}}
function vm(s){const M=s.length,h=2*Math.ceil(Math.log2(M+2))+4,tape=Array(h).fill(0);let ih=0,head=0n,erase=0,checks=[],accessBits=0;function jump(){let a=0n;for(let i=0;i<h;i++)if(tape[i])a|=1n<<BigInt(i);tape.fill(0);erase+=h;head=a;checks.push({type:"jump",address:String(a),indexHead:ih})}function read(){let v=head<BigInt(M)?s[Number(head)]:null;checks.push({type:"read",address:String(head),value:v});if(v!==null)accessBits+=Math.ceil(Math.log2(M+2))}
for(let i=0;i<h;i++){ih=i;tape[i]=1}jump();read();
ih=0;tape[0]=1;jump();read();head++;read();
for(let i=0;i<h;i++){ih=i;tape[i]=1}jump();head--;read();
ih=0;jump();read();
const far=(1n<<BigInt(h))-1n;
ck(far>BigInt(M*M),"nonlinear far address");ck(checks.filter(x=>x.type==="read").map(x=>x.value).join(",")===[null,s[1],s[2],null,s[0]].join(","),"guest reads");ck(checks.filter(x=>x.type==="jump").map(x=>x.indexHead).join(",")===[h-1,0,h-1,0].join(","),"index head preserved");
return {M,h,far:String(far),indexEraseCells:erase,childBufferCells:M,childAddressBits:accessBits,nearReads:3,blankReads:2,trace:checks}}
const out=[];
for(const F of cases){const n=F.n, models=[],occ=[],pairs=[],flips=[],res=[];
for(let a=0;a<(1<<n);a++){if(holds(F,a))models.push(a);for(let r=0;r<4;r++)ck(cnt(F,a)[r]===cnt(F,((1<<n)-1)^a)[3-r],"complements")}
for(let j=0;j<F.clauses.length;j++){const C=F.clauses[j];occ.push({j:j+1,original:C,occurrences:C.map((l,z)=>({j:j+1,k:z+1,l,S:l>0?1:0,invS:l>0?0:1,U:l>0?0:1,invU:l>0?1:0}))});
for(let k=j+1;k<F.clauses.length;k++){const D=F.clauses[k],states={SS:false,SU:false,US:false,UU:false};for(let a=0;a<(1<<n);a++){let u=tc(C,a),v=tc(D,a);if(u===3&&v===3)states.SS=true;if(u===3&&v===0)states.SU=true;if(u===0&&v===3)states.US=true;if(u===0&&v===0)states.UU=true}let same=false,opp=false;for(const x of C)for(const y of D)if(Math.abs(x)===Math.abs(y)){if(x===y)same=true;else opp=true}ck(states.SS===!opp&&states.UU===!opp&&states.SU===!same&&states.US===!same,"compatibility");pairs.push({j:j+1,k:k+1,states})}}
let a=0;flips.push({step:0,mask:a,counts:cnt(F,a)});for(let i=0;i<n;i++){const b=a^(1<<i);for(const C of F.clauses){const l=C.find(x=>Math.abs(x)===i+1),expected=l?(((((a>>i)&1)===(l>0?1:0)))?-1:1):0;ck(tc(C,b)-tc(C,a)===expected,"flip delta")}a=b;flips.push({step:i+1,mask:a,counts:cnt(F,a)})}
for(let j=0;j<F.clauses.length;j++)for(let k=j+1;k<F.clauses.length;k++)for(const x of F.clauses[j])if(F.clauses[k].includes(-x)){const c=[...new Set(F.clauses[j].filter(v=>v!==x).concat(F.clauses[k].filter(v=>v!==-x)))];if(c.some(v=>c.includes(-v)))continue;for(const v of models)ck(c.some(l=>(((v>>(Math.abs(l)-1))&1)===(l>0?1:0))),"resolvent");if(res.length<4)res.push({parents:[j+1,k+1],pivot:x,clause:c,forbidden:c.map(l=>[Math.abs(l),l<0?1:0])})}
const G={n,clauses:[...new Map(F.clauses.map(c=>[c.join(","),c])).values()]},baseline=dpll(F),guest=dpll(G),source=serial(F),child=serial(G),trace=vm(child);ck(baseline.sat===guest.sat,"SAT/UNSAT faithful");for(let v=0;v<(1<<n);v++)ck(holds(F,v)===holds(G,v),"dedup projection");
out.push({name:F.name,n,original:F.clauses,originalBytes:source.length,childBytes:child.length,sourceReadBytes:source.length,policyAttempts:1,failedTrials:0,guestCalls:1,workspaceResetCost:"separate charged term, not measured",label:baseline.sat?"SAT":"UNSAT",models,baseline,guest,endpoint0:cnt(F,0),endpoint1:cnt(F,(1<<n)-1),occ,pairs,flips,res,vm:trace})}
const gcd=(a,b)=>b?gcd(b,a%b):a;const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);let g=gcd(a<0n?-a:a,b);return [a/g,b/g]},add=(a,b)=>R(a[0]*b[1]+a[1]*b[0],a[1]*b[1]),sub=(a,b)=>R(a[0]*b[1]-a[1]*b[0],a[1]*b[1]),mul=(a,b)=>R(a[0]*b[0],a[1]*b[1]),div=(a,b)=>R(a[0]*b[1],a[1]*b[0]),cmp=(a,b)=>a[0]*b[1]-b[0]*a[1],repr=a=>a[0]+"/"+a[1];
function flmv(c){let f=R(1),p=R(1),best=R(-1),kbest=0,terms=[];for(let k=1;k<100;k++){f=div(mul(c,f),add(R(1),f));p=div(p,c);const x=div(sub(div(R(1),f),c),R(k)),d=cmp(x,p)<0?x:p;terms.push({k,d:repr(d)});if(cmp(d,best)>0){best=d;kbest=k}let tail=div(p,c);if(cmp(tail,best)<0)return {c:repr(c),best:repr(best),kbest,checkedK:k,tailMax:repr(tail),terms}}throw Error("no tail")}
const bounds=[flmv(R(6,5)),flmv(R(241,200)),flmv(R(7,5)),flmv(R(3,2)),flmv(R(8,5))];ck(bounds[0].best==="23/45"&&bounds[1].best==="11642479/23232400","FLMV exact");ck(bounds[0].kbest===2&&bounds[1].kbest===2,"maximizers");
return {run:"LSPV4_FARBLANK274_GITHUB",timestamp:"2026-10-31 06:36 America/Los_Angeles",method:"finite abstract trace and original-source exhaustive tests; not native FLMV hardware/machine transition benchmark",tests,cases:out,bounds}
})();
if(typeof module!== 'undefined' && require.main===module){console.log(JSON.stringify(result,null,2));}
module.exports=result;
