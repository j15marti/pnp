import assert from "node:assert/strict";
import crypto from "node:crypto";

function step(m,t,state,b){
  const [a,q]=state, wa=(a+1+b+(q&1))%m, wv=b^(t&1)^(q&1), nq=q^b, na=(wa+nq+1)%m;
  return [[na,nq],[{time:2*t,kind:"R",addr:a,value:b},{time:2*t+1,kind:"W",addr:wa,value:wv}]];
}
function build(m,source,guesses){
  let state=[0,0], states=[[0,0]], events=[];
  guesses.forEach((b,t)=>{const [ns,es]=step(m,t,state,b); state=ns; states.push(ns); events.push(...es);});
  const route=[...events.keys()].sort((i,j)=>events[i].addr-events[j].addr||events[i].time-events[j].time);
  return {m,source:[...source],guesses:[...guesses],states,events,route,output:state};
}
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function verify(c){
  if(!Number.isInteger(c.m)||c.m<=0||c.source.length!==c.m) return false;
  if([...c.source,...c.guesses].some(x=>x!==0&&x!==1)) return false;
  if(c.states.length!==c.guesses.length+1||!eq(c.states[0],[0,0])) return false;
  if(c.events.length!==2*c.guesses.length||!eq(c.output,c.states.at(-1))) return false;
  for(let t=0;t<c.guesses.length;t++){const [ns,es]=step(c.m,t,c.states[t],c.guesses[t]); if(!eq(ns,c.states[t+1])||!eq(es,c.events.slice(2*t,2*t+2))) return false;}
  if(!eq([...c.route].sort((a,b)=>a-b),[...c.events.keys()])) return false;
  const routed=c.route.map(i=>c.events[i]);
  for(let i=0;i+1<routed.length;i++) if(routed[i].addr>routed[i+1].addr||(routed[i].addr===routed[i+1].addr&&routed[i].time>routed[i+1].time)) return false;
  const last=[...c.source];
  for(const e of routed){if(e.addr<0||e.addr>=c.m||(e.value!==0&&e.value!==1)) return false; if(e.kind==="W") last[e.addr]=e.value; else if(e.kind==="R"){if(e.value!==last[e.addr]) return false;} else return false;}
  return true;
}
function actual(m,source,depth){let mem=[...source], state=[0,0], reads=[]; for(let t=0;t<depth;t++){const b=mem[state[0]]; reads.push(b); const [ns,es]=step(m,t,state,b); state=ns; mem[es[1].addr]=es[1].value;} return [reads,state];}
function bits(n,w){return [...Array(w)].map((_,i)=>(n>>(w-1-i))&1);}

let candidates=0,accepted=0,cases=0,corruptions=0,assertions=0; const hash=crypto.createHash("sha256"), per={};
for(const m of [2,4,8]){let mc=0,mk=0; for(let s=0;s<2**m;s++){const source=bits(s,m); for(let d=1;d<=8;d++){cases++;mc++; const [reads,out]=actual(m,source,d), good=build(m,source,reads); assert.equal(verify(good),true); assert.deepEqual(good.output,out); assertions+=2; let ac=0; for(let g=0;g<2**d;g++){const guess=bits(g,d), ok=verify(build(m,source,guess)); candidates++;mk++;ac+=ok?1:0; assert.equal(ok,eq(guess,reads));assertions++;} assert.equal(ac,1);accepted+=ac;assertions++; const br=structuredClone(good); [br.route[0],br.route[1]]=[br.route[1],br.route[0]]; assert.equal(verify(br),false);corruptions++;assertions++; const bo=structuredClone(good);bo.output[1]^=1;assert.equal(verify(bo),false);corruptions++;assertions++;hash.update(Buffer.from([...source,...reads,...out])); }} per[m]={cases:mc,candidates:mk};}
const malformed=build(2,[0,1],[0]);malformed.source=[0,2];assert.equal(verify(malformed),false);assertions++;
console.log(JSON.stringify({status:"COMPUTATIONAL",model:"deterministic adaptive bit-RAM trace relation",depths:[1,8],memory_cells:[2,4,8],cases,candidate_transcripts:candidates,accepted_transcripts:accepted,corruption_rejections:corruptions+1,assertions,unique_accepting_trace_per_case:accepted===cases,digest:hash.digest("hex"),per_memory_size:per,limitation:"enumeration demonstrates the acquisition/verification gap; it is not a search lower bound"},null,2));
