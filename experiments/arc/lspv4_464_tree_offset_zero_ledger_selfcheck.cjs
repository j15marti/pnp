/* LSPV-4/464 finite host-language verifier: not a native FLMV measurement. */
const result = (function(){
"use strict";
const S={cases:0, sat:0, unsat:0, blocks:0, guestCalls:0, guestBitsChecked:0, offsetHeaderReads:0, malformedRejected:0, k4Controls:0, maxSourceBits:0, maxBlockBits:0, maxLiveMessages:0, checks:0};
function ok(b,m){S.checks++;if(!b)throw Error(m||"failed")}
function bits(n,w){if(n<0||n>=2**w)throw Error("overflow");return n.toString(2).padStart(w,"0")}
function parity(a){return a.reduce((p,v)=>p^v,0)}
function vid(k,v,j,h){return 4*(k*h+v)+j}
function clauseBits(cl,r){return Array.from({length:3},(_,i)=>{let x=cl[i]||0;return (x<0?"1":"0")+bits(Math.abs(x),r)}).join("")}
function pin(id,force,owner,h){let u=vid(0,owner,1,h),v=vid(0,owner,2,h);let L=force?id:-id;return [[L,u,v],[L,u,-v],[L,-u,v],[L,-u,-v]]}
function build(h,conflict){let r=Math.ceil(Math.log2(8*h+8)), m=[], start=bits(h,16)+bits(r,8);
for(let v=1;v<=h;v++){let c=[];let edges=[v>=2?v:null,2*v<=h?2*v:null,2*v+1<=h?2*v+1:null].filter(Boolean);
for(let e of edges){let force=!(conflict&&v===1&&e===2);c.push(...pin(vid(1,e,1,h),force,v,h))}
while(c.length<Math.max(h,16)){c.push([vid(0,v,1,h),vid(0,v,2,h),vid(0,v,3,h)])}
m.push(c);start+=bits(c.length,16)+c.map(x=>clauseBits(x,r)).join("")}
return {h,r,m,src:start}}
function parse(src){if(!/^[01]+$/.test(src)||src.length<24)throw Error("bad bit string");let h=parseInt(src.slice(0,16),2),r=parseInt(src.slice(16,24),2);if(h<1||((h+1)&h)!==0||r!==Math.ceil(Math.log2(8*h+8)))throw Error("tree header");let i=24, m=[],base=[],R=3*(r+1);
for(let v=1;v<=h;v++){if(i+16>src.length)throw Error("block header");let count=parseInt(src.slice(i,i+16),2);i+=16;let b=i;if(!count||i+count*R>src.length)throw Error("length");let c=[];
for(let j=0;j<count;j++){let lits=[];for(let k=0;k<3;k++){let pos=i+j*R+k*(r+1),q=src.slice(pos,pos+r+1),id=parseInt(q.slice(1),2),neg=q[0]==="1";if(id===0)throw Error("strict-zero");let rem=id%4, z=Math.floor(id/4), kind=z>h?1:0,owner=kind?z-h:z;
if(rem<1||rem>3||owner<1||owner>h||kind===1&&(owner<2||rem!==1)||!(kind===0&&owner===v||kind===1&&(owner===v||Math.floor(owner/2)===v)))throw Error("bad type");
lits.push(neg?-id:id)}if(new Set(lits.map(Math.abs)).size!==3)throw Error("repeat");c.push(lits)}i+=count*R;m.push(c);base.push(b)}
if(i!==src.length)throw Error("trailing");return {h,r,m,base,src}}
function offset(p,v){let a=24,R=3*(p.r+1);for(let u=1;u<v;u++){let n=parseInt(p.src.slice(a,a+16),2);S.offsetHeaderReads++;a+=16+n*R}let n=parseInt(p.src.slice(a,a+16),2);S.offsetHeaderReads++;a+=16;ok(a===p.base[v-1]&&n===p.m[v-1].length,"offset");return a}
function sat(clauses){let state=new Map();
function go(){for(;;){let moved=false;for(let cl of clauses){let yes=false,unknown=[];for(let l of cl){let a=Math.abs(l),v=state.get(a);if(v===undefined)unknown.push(l);else if(v===(l>0)){yes=true;break}}if(yes)continue;if(!unknown.length)return false;if(unknown.length===1){let a=Math.abs(unknown[0]),val=unknown[0]>0;if(state.has(a)&&state.get(a)!==val)return false;if(!state.has(a)){state.set(a,val);moved=true}}}if(!moved)break}
let candidate;for(let cl of clauses){if(cl.every(l=>state.has(Math.abs(l))&&state.get(Math.abs(l))===(l>0)))continue;candidate=cl.find(l=>!state.has(Math.abs(l)));if(candidate)break}
if(candidate===undefined)return true;let a=Math.abs(candidate),snap=new Map(state);for(let val of [true,false]){state=new Map(snap);state.set(a,val);if(go())return true}state=snap;return false}
return go()}
function view(p,v,base,aux){let n=p.m[v-1].length+aux.length,head=bits(n,16),payload=p.src.slice(base,base+p.m[v-1].length*3*(p.r+1)),suffix=aux.map(x=>clauseBits(x,p.r)).join("");return {bit(i){if(i<16)return head[i];i-=16;if(i<payload.length)return p.src[base+i];i-=payload.length;return suffix[i]||"0"},full:head+payload+suffix,original:payload.length}}
function check(h,conflict){let x=build(h,conflict),p=parse(x.src);ok(p.m.length===h);S.blocks+=h;S.maxSourceBits=Math.max(S.maxSourceBits,x.src.length);
let live=0;function visit(v){let children=[2*v,2*v+1].filter(z=>z<=h);let cm=children.map(visit);live+=cm.reduce((a,t)=>a+t.length,0);S.maxLiveMessages=Math.max(S.maxLiveMessages,live);let b=offset(p,v),parent=v===1?[null]:[false,true],out=[];
for(let a of parent){let aux=[];if(a!==null)aux.push([a?vid(1,v,1,h):-vid(1,v,1,h)]);
for(let z=0;z<children.length;z++){for(let j=0;j<2;j++){if(!cm[z][j])aux.push([j===0?vid(1,children[z],1,h):-vid(1,children[z],1,h)])}}
let clauses=p.m[v-1].concat(aux),vw=view(p,v,b,aux),expected=bits(clauses.length,16)+clauses.map(c=>clauseBits(c,p.r)).join("");
ok(vw.full===expected,"virtual exact");for(let k=0;k<expected.length;k++){ok(vw.bit(k)===expected[k],"bit");S.guestBitsChecked++}
S.maxBlockBits=Math.max(S.maxBlockBits,vw.full.length);S.guestCalls++;out.push(sat(clauses))}
live-=cm.reduce((a,t)=>a+t.length,0);return out}
let root=visit(1)[0],expected=!conflict;ok(root===expected,"SAT/UNSAT classification");
let witness=new Map();if(!conflict){for(let v=1;v<=h;v++)for(let j=1;j<=3;j++)witness.set(vid(0,v,j,h),true);for(let v=2;v<=h;v++)witness.set(vid(1,v,1,h),true);ok(p.m.flat().every(c=>c.some(l=>witness.get(Math.abs(l))===(l>0))),"witness")}
else {let rootE=vid(1,2,1,h);ok(sat(p.m[0])&&sat(p.m[1]),"local SAT");ok(!sat(pin(rootE,false,1,h).concat(pin(rootE,true,2,h))),"interface inconsistency")}
let edits=[x.src.slice(0,-1),x.src+"1",x.src.slice(0,24)+"0".repeat(16)+x.src.slice(40),x.src.slice(0,40)+"0".repeat(p.r+1)+x.src.slice(40+p.r+1)];
for(let a of edits){let rejected=false;try{parse(a)}catch(e){rejected=true}ok(rejected,"corrupt accepted");S.malformedRejected++}
S.cases++;if(root)S.sat++;else S.unsat++}
for(let h of [3,7,15,31])for(let conflict of [false,true])check(h,conflict);
function k4(odd){let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],rows=[0,0,0,odd?1:0],F=[];
for(let v=0;v<4;v++){let ids=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);for(let m=0;m<8;m++){let a=[m&1,(m>>1)&1,(m>>2)&1];if(parity(a)!==rows[v])F.push(a.map((b,i)=>b?-ids[i]:ids[i]))}}
let expected=!odd;let yes=false;for(let x=0;x<64;x++){let assign=Array.from({length:6},(_,i)=>Boolean((x>>i)&1));if(F.every(c=>c.some(l=>assign[Math.abs(l)-1]===(l>0)))){yes=true;break}}ok(yes===expected,"K4 parity");ok(F.length===16);S.k4Controls++}
k4(true);k4(false);
ok(S.offsetHeaderReads>0&&S.guestCalls>0);
return S;
})();
console.log(JSON.stringify(result,null,2));
