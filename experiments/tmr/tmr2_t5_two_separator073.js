// TMR-2/073, pure JavaScript, no dependencies, seed 202611171850.
// Genuine five-symbol original-label source and two-terminal parallel K3,3.
"use strict";
const R=(a,b)=>[1,3].includes((b-a+5)%5);
const vectors=()=>[10,0,2,2,0];
function family(b,extra=0) {
  let E=[];
  for(let i=0;i<b;i++) {
    const c=2+4*i;
    for(let w=c+1;w<=c+3;w++)for(const v of [0,1,c])E.push([v,w]);
  }
  if(extra&1)E.push([0,1]);
  if(extra&2)E.push([1,0]);
  E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  return [4*b+2,E];
}
function encode(n,E) {
  let out="p t5 "+n+" "+E.length+"\n";
  for(let i=0;i<n;i++)out+="v "+i+"\n";
  for(const [u,v] of E)out+="a "+u+" "+v+"\n";
  return out;
}
function parse(src) {
  if(!src.endsWith("\n")||src.includes("\r"))throw Error("source");
  const ls=src.slice(0,-1).split("\n"), h=ls[0].split(" ");
  if(h.length!==4||h[0]!=="p"||h[1]!=="t5")throw Error("header");
  const canonical=x=>/^(0|[1-9][0-9]*)$/.test(x)&&Number.isSafeInteger(Number(x));
  if(!canonical(h[2])||!canonical(h[3]))throw Error("numbers");
  const n=+h[2],m=+h[3];
  if(n>src.length||m>src.length||ls.length!==1+n+m)throw Error("length");
  for(let i=0;i<n;i++)if(ls[1+i]!=="v "+i)throw Error("vertices");
  const E=[];
  for(const l of ls.slice(1+n)) {
    const p=l.split(" ");
    if(p.length!==3||p[0]!=="a"||!canonical(p[1])||!canonical(p[2]))throw Error("arc");
    const u=+p[1],v=+p[2];
    if(u>=n||v>=n)throw Error("range");
    E.push([u,v]);
  }
  if(encode(n,E)!==src)throw Error("canonical");
  for(let i=1;i<m;i++)if(E[i-1][0]>E[i][0]||
    (E[i-1][0]===E[i][0]&&E[i-1][1]>=E[i][1]))throw Error("sorted");
  return [n,E];
}
function recognize(n,E) {
  if(n<10||(n-2)%4!==0)return null;
  const b=(n-2)/4, incoming=Array.from({length:n},()=>new Set()),
    outgoing=Array.from({length:n},()=>new Set());
  for(const [u,v] of E) {
    if(u===v)return null;
    incoming[v].add(u);outgoing[u].add(v);
  }
  const sinks=new Set();
  for(let v=0;v<n;v++)if(outgoing[v].size===0&&incoming[v].size===3)sinks.add(v);
  if(sinks.size!==3*b)return null;
  for(let s=0;s<n;s++)for(let t=s+1;t<n;t++) {
    const sinkOut=v=>[...outgoing[v]].filter(w=>sinks.has(w)).length;
    if(sinkOut(s)!==3*b||sinkOut(t)!==3*b)continue;
    const others=Array.from({length:n},(_,i)=>i).filter(v=>v!==s&&v!==t&&!sinks.has(v));
    if(others.length!==b)continue;
    const used=new Set();let ok=true,expected=new Set();
    for(const c of others) {
      if(incoming[c].size!==0||outgoing[c].size!==3) {ok=false;break}
      for(const w of outgoing[c]) {
        if(!sinks.has(w)||used.has(w)||incoming[w].size!==3||
            !incoming[w].has(s)||!incoming[w].has(t)||!incoming[w].has(c)) {
          ok=false;break
        }
        used.add(w);
        for(const u of [s,t,c])expected.add(u+","+w);
      }
      if(!ok)break;
    }
    if(!ok||used.size!==sinks.size)continue;
    const extras=E.filter(([u,v])=>!expected.has(u+","+v));
    if(extras.some(([u,v])=>!((u===s&&v===t)||(u===t&&v===s))))continue;
    if(expected.size+extras.length!==E.length)continue;
    return {s,t,b,extra:extras.map(([u,v])=>u===s?1:2).reduce((a,b)=>a|b,0)};
  }
  return null;
}
function fast(n,E) {
  const cert=recognize(n,E);
  if(!cert)return null;
  const f=vectors();
  let answer=0n;
  for(let d=0;d<5;d++) {
    if((cert.extra&1)&&!R(0,d))continue;
    if((cert.extra&2)&&!R(d,0))continue;
    answer+=BigInt(f[d])**BigInt(cert.b);
  }
  return 5n*answer;
}
function brute(n,E) {
  const xs=Array(n).fill(-1),checks=Array.from({length:n},()=>[]);
  for(const [u,v] of E)checks[Math.max(u,v)].push([u,v]);
  function go(k){
    if(k===n)return 1n;
    let z=0n;
    for(let a=0;a<5;a++){
      xs[k]=a;
      if(checks[k].every(([u,v])=>R(xs[u],xs[v])))z+=go(k+1);
    }
    xs[k]=-1;return z;
  }
  return go(0);
}
function runAudit(){
  let assertions=0,seed=202611171850>>>0,records=[];
  const rand=()=>((seed=(1664525*seed+1013904223)>>>0)/4294967296);
  function check(b,m){assertions++;if(!b)throw Error("check "+assertions+" "+m)}
  for(let a=0;a<5;a++)for(let b=0;b<5;b++){
    const f=vectors();
    let original=0;
    for(let c=0;c<5;c++) {
      let compatible=0;
      for(let w=0;w<5;w++)if(R(a,w)&&R(b,w)&&R(c,w))compatible++;
      original+=compatible**3;
    }
    check(original===f[(b-a+5)%5],"K33 direct block");
  }
  for(let b=2;b<=17;b++)for(let extra=0;extra<4;extra++){
    const [n,E]=family(b,extra),[n2,E2]=parse(encode(n,E));
    check(n===n2&&E2.length===E.length,"source");
    const z=fast(n2,E2);
    const expected=extra===0?5n*(10n**BigInt(b)+2n*2n**BigInt(b)):
      extra===3?0n:5n*2n**BigInt(b);
    check(z===expected,"fast exact transfer");
    if(b===2&&extra<4) {
      // Independent original-label count, conditioned only on actual terminals.
      let t=0n;
      for(let x=0;x<5;x++)for(let y=0;y<5;y++) {
        if((extra&1)&&!R(x,y))continue;
        if((extra&2)&&!R(y,x))continue;
        let ways=0;
        for(let c=0;c<5;c++)for(let u=0;u<5;u++)
          for(let v=0;v<5;v++)for(let w=0;w<5;w++)
            if([x,y,c].every(z=>[u,v,w].every(q=>R(z,q))))ways++;
        t+=BigInt(ways)**BigInt(b);
      }
      check(t===z,"original source semantics");
    }
    if(extra===0&&[2,3,8,17].includes(b))
      records.push({b,n,m:E.length,exact_count:z.toString(),raw_cycle_excess:5*b-1});
  }
  for(let k=0;k<24;k++){
    const b=2+k%5,extra=k%4,[n,E]=family(b,extra);
    const p=Array.from({length:n},(_,i)=>i);
    for(let i=n-1;i>0;i--){const j=Math.floor(rand()*(i+1));[p[i],p[j]]=[p[j],p[i]]}
    const E2=E.map(([u,v])=>[p[u],p[v]]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
    check(fast(...parse(encode(n,E2)))===
      (extra===0?5n*(10n**BigInt(b)+2n*2n**BigInt(b)):
       extra===3?0n:5n*2n**BigInt(b)),"relabel");
  }
  const [n,E]=family(3,0);
  check(recognize(n,E.slice(1))===null,"missing arc");
  check(recognize(n,[...E,[2,6]])===null,"wrong new arc");
  for(const src of [encode(n,E).slice(0,-1),encode(n,E).replace("v 1\n","v 01\n")]){
    try{parse(src);check(false,"accepted malformed")}catch(e){check(true,"rejected malformed")}
  }
  return {revision:"tmr2-t5-2separator073-js.v1",seed:202611171850,
    assertions,failures:0,records,science:"finite COMPUTATIONAL; theorem separately proved"};
}
if(typeof require==="function"&&typeof module==="object"&&require.main===module){
  const fs=require("fs");
  const arg=process.argv[2];
  if(arg==="--audit")console.log(JSON.stringify(runAudit(),null,2));
  else {
    const [n,E]=parse(fs.readFileSync(arg||0,"utf8"));
    const result=fast(n,E);
    console.log((result===null?brute(n,E):result).toString());
  }
}