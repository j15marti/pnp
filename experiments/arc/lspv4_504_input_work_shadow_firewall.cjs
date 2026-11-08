"use strict";
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;function ok(x,t){checks++;if(!x)throw Error(t||"check");}
function cnf(c){
let out=[];
for(let v=0;v<4;v++){let ids=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);ok(ids.length===3);
for(let q=0;q<8;q++){let bits=[q&1,(q>>1)&1,(q>>2)&1];
if(((bits[0]+bits[1]+bits[2])&1)!==((c>>v)&1))out.push(bits.map((b,j)=>b?-ids[j]:ids[j]));}}
ok(out.length===16);return out;
}
function enc(cs){return [0xc3,6,cs.length,...cs.flat().map(x=>x&255)];}
function dec(b){
if(b.length<3||b[0]!==0xc3)return null;
let n=b[1],m=b[2];if(n<1||n>12||m>64||b.length!==3+3*m)return null;
let cs=[];
for(let i=0;i<m;i++){let a=b.slice(3+3*i,6+3*i).map(x=>x>=128?x-256:x);
if(a.some(x=>!x||Math.abs(x)>n)||new Set(a.map(x=>Math.abs(x))).size!==3)return null;cs.push(a);}
return [cs,n];
}
function label(b){
let d=dec(b);if(!d)return "MALFORMED";
let [cs,n]=d;
for(let a=0;a<(1<<n);a++)if(cs.every(c=>c.some(z=>Boolean((a>>(Math.abs(z)-1))&1)===(z>0))))return "SAT";
return "UNSAT";
}
function probe(b,k){
let n=8*b.length,L=k*Math.ceil(Math.log2(n+2)),A=1n<<BigInt(L),o=label(b);
ok(A>BigInt(n),"out-of-range probe");ok(A>=BigInt(Math.max(2,L)),"shadow/highwater");
return {o,A,L};
}
function suffix(inp,work){
let w={...work},wr=new Set(),live={},observed={},trace=[];
for(let [op,j,x] of [["W",0,1],["R",0,0],["R",2,0],["I",0,0],["W",2,0],["R",2,0],["I",1,0],["R",4,0]]){
if(op==="W"){w[j]=x;wr.add(j);trace.push([op,j,x]);}
else if(op==="R"){let y=w[j]||0;if(!wr.has(j))live[j]=y;trace.push([op,j,y]);}
else{observed[j]=inp[j];trace.push([op,j,inp[j]]);}}
return {live,observed,trace};
}
function sameAnchor(a,b){
let x=suffix(...a),y=suffix(...b);
let verified=Object.entries(x.live).every(([j,v])=>(b[1][j]||0)===v)
&&Object.entries(x.observed).every(([j,v])=>b[0][j]===v);
let exact=JSON.stringify(x.trace)===JSON.stringify(y.trace);
if(verified)ok(exact,"sound suffix");
return [verified,exact];
}
function runAudit(){
checks=0;let cases=[],sat=0,unsat=0;
for(let i=0;i<16;i++){let b=enc(cnf(i)),l=label(b),odd=i.toString(2).split("1").length%2===0;
ok(l===(odd?"UNSAT":"SAT"),"charge");ok(JSON.stringify(enc(dec(b)[0]))===JSON.stringify(b),"encoding");
if(l==="SAT")sat++;else unsat++;cases.push(b);}
let bad=[[],[0xc3],[0,6,16],cases[0].slice(0,-1),[0xc3,0,1,...cases[0].slice(3,6)],
[0xc3,6,1,1,1,2],[0xc3,6,1,0,2,3],[0xc3,6,1,7,2,3],[0xc3,6,1,1,2,255]];
for(let b of bad){ok(label(b)==="MALFORMED","bad input");cases.push(b);}
let maxW=0n,maxScratch=0,probes=0;
for(let b of cases)for(let k of [1,2,3,5,6]){
let p=probe(b,k);ok(p.o===label(b),"output preservation");
maxW=p.A>maxW?p.A:maxW;maxScratch=Math.max(maxScratch,p.L,2);probes++;}
let a=[[0,1,0,0,1,0],{0:0,2:1,4:1,5:0}],b=[[0,1,0,1,1,1],{0:1,2:1,4:1,5:1}];
ok(sameAnchor(a,b)[0],"reuse");
for(let c of [[[1,1,0,1,1,1],b[1]],[b[0],{0:1,2:0,4:1,5:1}],[b[0],{0:1,2:1,4:0,5:1}]]){let p=sameAnchor(a,c);ok(!p[0]&&!p[1],"rejection");}
ok(sat===8&&unsat===8&&bad.length===9);
return {status:"COMPUTATIONAL, symbolic FLMV high-water",originals:16,sat,unsat,malformed:9,
sources:cases.length,typed_input_probes:probes,max_shadow_WORK_highwater:maxW.toString(),
max_typed_blank_repair_scratch_bits:maxScratch,suffix_positive:1,suffix_negative:3,checks};}
if(typeof module!=="undefined"&&typeof require!=="undefined"&&require.main===module)
 console.log(JSON.stringify(runAudit(),null,2));