// LSPV-3/411: exact 3-input, paid arbitrary binary DEF synthesis.
"use strict";
function synth(){
const X=[170,204,240],apply=(o,a,b)=>(((o&1)?~a&~b:0)|((o&2)?~a&b:0)|((o&4)?a&~b:0)|((o&8)?a&b:0))&255;
const dist=Array(256).fill(-1),wit=Array(256).fill(null);X.forEach(f=>{dist[f]=0;wit[f]=[]});
let states=[{out:[],steps:[]}],stateCounts=[];
for(let d=1;d<=3;d++){const next=new Map();
for(const st of states){const wires=X.concat(st.out),seen=new Set();
for(let i=0;i<wires.length;i++)for(let j=i;j<wires.length;j++)for(let op=0;op<16;op++){
const f=apply(op,wires[i],wires[j]);if(wires.includes(f)||seen.has(f))continue;seen.add(f);
const steps=st.steps.concat([{i,j,op}]);if(dist[f]<0){dist[f]=d;wit[f]=steps}
const out=st.out.concat(f),key=out.join(",");if(!next.has(key))next.set(key,{out,steps});
}}states=[...next.values()];stateCounts.push(states.length)}
const missing3=dist.filter(x=>x<0).length;let remaining=missing3;
for(const st of states){if(!remaining)break;const wires=X.concat(st.out);
for(let i=0;i<wires.length&&remaining;i++)for(let j=i;j<wires.length&&remaining;j++)for(let op=0;op<16&&remaining;op++){
const f=apply(op,wires[i],wires[j]);if(dist[f]<0){dist[f]=4;wit[f]=st.steps.concat([{i,j,op}]);remaining--}
}}
if(remaining)throw Error("four gates fail");
let checks=0;for(let f=0;f<256;f++){const seq=wit[f],v=X.slice();
for(const g of seq){if(g.i>=v.length||g.j>=v.length||g.op<0||g.op>15)throw Error("index");
v.push(apply(g.op,v[g.i],v[g.j]));checks++}
if((seq.length?v.at(-1):f)!==f)throw Error("bitvector "+f);
for(let a=0;a<8;a++){const bits=[a&1,(a>>1)&1,(a>>2)&1];
for(const g of seq)bits.push((g.op>>(2*bits[g.i]+bits[g.j]))&1);
const got=seq.length?bits.at(-1):(a>>X.indexOf(f))&1;
if(got!==((f>>a)&1))throw Error("truth table "+f+" "+a);checks++;
}}
const hist=[0,0,0,0,0];for(const d of dist)hist[d]++;
const hard=p=>{let f=0;for(let a=0;a<8;a++)if(p((a&1)+((a>>1)&1)+((a>>2)&1)))f|=1<<a;return f};
const maj=hard(w=>w>=2),one=hard(w=>w===1);
if(dist[maj]!==4||dist[one]!==4)throw Error("hard controls");
const mutant=wit[maj].map(g=>({...g}));mutant.at(-1).op^=15;
const vv=X.slice();for(const g of mutant)vv.push(apply(g.op,vv[g.i],vv[g.j]));if(vv.at(-1)===maj)throw Error("corrupt witness accepted");
const countModels=F=>{let c=0;for(let a=0;a<8;a++)if(F.every(C=>C.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0))))c++;return c};
if(countModels([[1],[1,2]])!==4||countModels([[1],[-1]])!==0)throw Error("SAT control");
return {statesByDepth:stateCounts,histogram:hist,missingAfter3:missing3,missingAfter4:remaining,checks,majority:{mask:maj,steps:wit[maj]},exactlyOne:{mask:one,steps:wit[one]},models:{sat:4,unsat:0},mutantRejected:true};
}
if(typeof module!=="undefined")module.exports={synth};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(synth(),null,2));
