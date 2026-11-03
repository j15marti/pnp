"use strict";
// LSPV-2 360 independent checker: no import from producer, own parser/rank and proof replay.
function verify(data){
let checks=0;function ck(t,s){checks++;if(!t)throw Error("verification failed: "+s);}
function parity(a){let p=0;for(;a;a>>=1)p^=a&1;return p;}
function matrixRank(rows,width){let r=rows.slice(),i=0;for(let col=width-1;col>=0;col--){let pivot=-1;for(let j=i;j<r.length;j++)if((r[j]>>col)&1){pivot=j;break;}if(pivot===-1)continue;[r[i],r[pivot]]=[r[pivot],r[i]];for(let j=i+1;j<r.length;j++)if((r[j]>>col)&1)r[j]^=r[i];i++;}return i;}
function parseDimacs(src){
const lines=src.trim().split(/\r?\n/),hdr=lines.shift().trim().split(/\s+/);
if(hdr.length!==4||hdr[0]!=="p"||hdr[1]!=="cnf"||!/^[0-9]+$/.test(hdr[2])||!/^[0-9]+$/.test(hdr[3]))throw Error("malformed header");
const n=Number(hdr[2]),m=Number(hdr[3]);if(!Number.isSafeInteger(n)||n<1||n>20||m!==lines.length)throw Error("invalid n or clause count");
const clauses=lines.map(line=>{
const ts=line.trim().split(/\s+/);if(ts.length<2||ts[ts.length-1]!=="0")throw Error("missing clause terminator");
const lits=ts.slice(0,-1).map(s=>{if(!/^-?[1-9][0-9]*$/.test(s))throw Error("bad literal");return Number(s);});
const abs=lits.map(Math.abs);if(lits.some(x=>Math.abs(x)>n)||new Set(abs).size!==abs.length)throw Error("bad source clause");
return lits;
});return {n,clauses};
}
const allClauses=(a,cs,skip=-1,mutation=null)=>cs.every((cl,i)=>{if(i===skip)return true;return cl.some((lit,k)=>{const l=mutation&&mutation[0]===i&&mutation[1]===k?-lit:lit;return l>0?!!(a&(1<<(l-1))):!(a&(1<<(-l-1)));});});
function mustReject(fn,name){let rejected=false;try{fn();}catch(_){rejected=true;}ck(rejected,"should reject "+name);}
ck(data.id==="LSPV2_XOR_LOCAL_PROJECTION360","data id");
let tested=0,paid=0,clausesCount=0,satMut=0,rankChecks=0;
for(const f of data.fixtures){
tested++;const parsed=parseDimacs(f.dimacs),cs=parsed.clauses,n=parsed.n,rows=f.rows;
ck(f.vars.length===n&&cs.length===f.clauses.length,"source dimensions "+f.name);
ck(rows.length>=2,"row count");
for(let i=0;i<cs.length;i++)ck(cs[i].join(",")===f.clauses[i].lits.join(","),"source order");
const allMask=(1<<n)-1,A=rows.map(r=>r.vars.reduce((x,v)=>x|(1<<(v-1)),0)),rank=matrixRank(A,n),rankPlus=matrixRank(A.map((x,i)=>x|(rows[i].rhs<<n)),n+1);
ck(rank===f.controls.rank&&rankPlus===f.controls.rankAug&&rankPlus===rank+1,"inconsistent linear system");
for(let i=0;i<rows.length;i++){
let r=rows[i], bad=[];
ck(r.vars.length===3&&new Set(r.vars).size===3,"proper triple");
for(let pat=0;pat<8;pat++)if(parity(pat)!==r.rhs)bad.push(pat);
const actual=new Set();
for(let j=0;j<4;j++){let cl=cs[4*i+j],pat=r.vars.reduce((p,v,k)=>{
const lit=cl[k];ck(Math.abs(lit)===v,"row support");return p|((lit<0?1:0)<<k);
},0);ck(bad.includes(pat),"forbidden wrong parity");actual.add(pat);}
ck(actual.size===4,"all four distinct blockers");
let projection=new Set(),delSystemModels=0,flippedEqModels=0;
for(let assign=0;assign<(1<<n);assign++){
let others=rows.every((r,j)=>j===i||parity(A[j]&assign)===r.rhs);
if(others){delSystemModels++;let pat=r.vars.reduce((x,v,k)=>x|(((assign>>(v-1))&1)<<k),0);projection.add(pat);}
if(rows.every((r,j)=>parity(A[j]&assign)===(r.rhs^(j===i?1:0))))flippedEqModels++;
}
ck(delSystemModels>0&&flippedEqModels===f.controls.rowFlipModelCounts[i],"equation critical");
let remaining=A.filter((_,j)=>j!==i),outside=allMask&~A[i],d=3-matrixRank(remaining,n)+matrixRank(remaining.map(x=>x&outside),n);
ck(d===f.controls.rowStats[i].dimension&&projection.size===(1<<d),"projection dimension");
ck([...projection].sort((a,b)=>a-b).join(",")===f.controls.rowStats[i].projectedWrongPatterns.join(","),"projection patterns");
rankChecks++;
}
let models=0,delWitness=[],flipWitness=[];
for(let ass=0;ass<(1<<n);ass++)if(allClauses(ass,cs))models++;
ck(models===0&&models===f.controls.satModels,"unsat source");
for(let i=0;i<cs.length;i++){
let witness=-1;for(let ass=0;ass<(1<<n);ass++)if(allClauses(ass,cs,i)){witness=ass;break;}
delWitness.push(witness);ck(witness===f.controls.deleteWitnesses[i],"source deletion SAT control");
let flips=[];for(let k=0;k<3;k++){let w=-1;for(let ass=0;ass<(1<<n);ass++)if(allClauses(ass,cs,-1,[i,k])){w=ass;break;}flips.push(w);if(w!==-1)satMut++;}
flipWitness.push(flips);ck(flips.join(",")===f.controls.signFlipWitnesses[i].join(","),"one-sign flip controls");
}
const src=new Map();for(let i=0;i<cs.length;i++){const r=rows[f.clauses[i].row],ref=f.clauses[i].id;ck(!src.has(ref),"unique source id");let truthMask=0;for(let p=0;p<8;p++){if(cs[i].some((l,k)=>l>0?!!((p>>k)&1):!((p>>k)&1)))truthMask|=1<<p;}src.set(ref,{type:"factor",row:f.clauses[i].row,truthMask});}
const byID=new Map(src),nodes=f.proof.nodes;
for(let i=0;i<nodes.length;i++){
let node=nodes[i];ck(node.id==="n"+i&&node.parents.length===2&&!byID.has(node.id),"node identifier and binary arity");
const p=byID.get(node.parents[0]),q=byID.get(node.parents[1]);ck(!!p&&!!q,"antecedents exist");
if(node.type==="AND3"){
ck(p.type==="factor"&&q.type==="factor"&&p.row===q.row&&p.row===node.row,"typed local conjunction");
const truthMask=p.truthMask&q.truthMask;ck(truthMask===node.truthMask,"exact AND3 truth-table");
let item={type:"factor",row:node.row,truthMask};
if(node.affine){let row=rows[node.row],expect=row.vars.reduce((m,v)=>m^(1<<(v-1)),0);ck(node.affine.mask===expect&&node.affine.rhs===row.rhs,"row GF2 annotation");
let target=0;for(let a=0;a<8;a++)if(parity(a)===row.rhs)target|=1<<a;
ck(target===truthMask,"valid free local affine annotation");item={type:"affine",mask:expect,rhs:row.rhs};}
byID.set(node.id,item);
}else if(node.type==="XOR"){
ck(p.type==="affine"&&q.type==="affine","typed GF2 sum");
ck(node.affine.mask===(p.mask^q.mask)&&node.affine.rhs===(p.rhs^q.rhs),"exact XOR");
byID.set(node.id,{type:"affine",mask:node.affine.mask,rhs:node.affine.rhs});
}else throw Error("unknown rule");
}
const root=byID.get(f.proof.root);
ck(root&&root.type==="affine"&&root.mask===0&&root.rhs===1,"derived contradiction");
ck(nodes.length===4*rows.length-1,"proof upper charge");
let essential=delWitness.filter(x=>x!==-1).length;ck(essential===f.controls.essential,"essential count");
for(let i=0;i<rows.length;i++){
let observed=delWitness.slice(4*i,4*i+4).filter(x=>x!==-1).length;
ck(observed===f.controls.rowStats[i].observedEssential&&observed===2**f.controls.rowStats[i].dimension,"per-row essential iff reachable");
}
ck(f.controls.exactW===(essential===cs.length?nodes.length:null),"exact coverage status");
ck(f.accounting.sourceBytes===f.dimacs.length&&f.accounting.proofNodeJsonBytes===JSON.stringify(nodes).length,"encoded evidence bytes");
paid+=nodes.length;clausesCount+=cs.length;
mustReject(()=>parseDimacs(f.dimacs.replace(/ 0\n/," \n")),"missing first terminator");
mustReject(()=>parseDimacs(f.dimacs.replace(/^(p cnf \d+ )(\d+)/,(s,a,b)=>a+(+b+1))),"header count");
const corrupt=JSON.parse(JSON.stringify(f));corrupt.proof.nodes[0].truthMask^=1;
mustReject(()=>{const nd=corrupt.proof.nodes[0],p=byID.get(nd.parents[0]),q=byID.get(nd.parents[1]);if(nd.truthMask!==(p.truthMask&q.truthMask))throw Error("corrupt truthmask");},"corrupted proof");
}
ck(tested===4&&rankChecks===18,"expected fixed test cases");
return {status:"PASS",fixtures:tested,sourceClauses:clausesCount,paidNodes:paid,signFlipSAT:satMut,rankChecks,assertions:checks};
}
if(typeof module!=="undefined"&&module.exports)module.exports={verify};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
const fs=require("fs");const input=process.argv[2];if(!input)throw Error("usage: node verifier.js result.json");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(input,"utf8")))));
}
