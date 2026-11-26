function audit(){
  const frame=s=>"1".repeat(s.length)+"0"+s;
  const rule=(q,a,b,p,c,d,u,v)=>[q,a,b,p,c,d,u,v].map(i=>i.toString(2)).map(frame).join("");
  const machine=[... [0,2,3].flatMap(q=>[1,2].map(a=>rule(q,a,0,a===1?2:3,a,0,1,2))),rule(3,0,0,1,0,0,2,2)].join("");
  const encode=(M,x,t,p=0)=>frame(M)+frame(x)+frame(t.toString(2))+"0".repeat(p);
  let checks=0;
  const ok=(x,msg)=>{checks++;if(!x)throw Error(msg)};
  function parse(w,h=2){
    let i=0;
    function read(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||k+1+k-j>s.length)throw Error("frame");return [s.slice(k+1,k+1+k-j),k+1+k-j]}
    if(!/^[01]+$/.test(w))throw Error("alphabet");
    let M,x,t;[M,i]=read(w,i);[x,i]=read(w,i);[t,i]=read(w,i);
    if(!/^0*$/.test(w.slice(i))||! /^(0|1[01]*)$/.test(t))throw Error("tail or clock");
    let T=BigInt("0b"+t);if(T>BigInt(w.length)**BigInt(h))throw Error("clock cap");
    let j=0,R=[];
    while(j<M.length){let a=[];for(let k=0;k<8;k++){let v;[v,j]=read(M,j);if(!/^(0|1[01]*)$/.test(v))throw Error("rule field");a.push(v)}if(!["0","1","10"].includes(a[6])||!["0","1","10"].includes(a[7]))throw Error("move");R.push(a)}
    return {x,T:Number(T),R};
  }
  function solve(w,h=2){
    let P;try{P=parse(w,h)}catch{return false}
    const {x,T,R}=P;
    const move={"0":-1,"1":1,"10":0};
    let st=[{q:"0",p:[0,0],t:[new Map(Array.from(x,(c,i)=>[i,c==="0"?"1":"10"])),new Map()]}];
    for(let k=0;k<=T;k++){
      if(st.some(s=>s.q==="1"))return true;
      if(k===T)return false;
      let next=[];
      for(const s of st){
        const [a,b]=s.t.map((t,i)=>t.get(s.p[i])??"0");
        for(const r of R)if(r[0]===s.q&&r[1]===a&&r[2]===b){
          const t=s.t.map((v,i)=>{const z=new Map(v);z.set(s.p[i],r[4+i]);return z});
          next.push({q:r[3],p:s.p.map((v,i)=>v+move[r[6+i]]),t});
        }
      }
      st=next;if(!st.length)return false;
    }
    return false;
  }
  let pairs=[];
  for(const m of [1,2,4,8,16,32,64,128,256,512]){
    const y=encode(machine,"0".repeat(m-1)+"1",m+1);
    const n=encode(machine,"0".repeat(m),m+1);
    ok(y.length===n.length,"same size");
    ok(solve(y)&&!solve(n),"labels");
    ok(!solve(encode(machine,"0".repeat(m-1)+"1",m)),"clock boundary");
    pairs.push({m,N:y.length,clock:m+1,yes:solve(y),no:solve(n)});
  }
  const nondet=rule(0,2,0,4,2,0,2,2)+rule(0,2,0,1,2,0,2,2);
  ok(solve(encode(nondet,"1",1))&&!solve(encode(nondet,"0",1)),"nondet");
  for(const w of ["", "1","00","101",encode(machine,"1",1)+"1",encode(machine,"1",1000000000),encode(frame("1"),"1",1)])ok(!solve(w),"malformed");
  const U=(l,a,b)=>[1,-1].flatMap(s=>[1,-1].map(t=>[l,s*a,t*b]));
  const Q=[U(1,2,3).concat(U(1,4,5)),U(1,2,3).concat(U(-1,4,5)),U(-1,2,3).concat(U(-1,4,5))];
  const queryWords=Q.map(F=>F.map(C=>C.join(",")).join(";"));
  ok(new Set(queryWords).size===3,"query identities");
  const sat=Q.map(F=>Array.from({length:32},(_,b)=>b).filter(b=>F.every(C=>C.some(l=>Boolean(b&(1<<(Math.abs(l)-1)))===(l>0)))));
  ok(sat[0].length===16&&sat[1].length===0&&sat[2].length===16,"formula truth tables");
  const trueMask=sat.reduce((m,s,i)=>m|(s.length?1<<i:0),0);
  const subsets=Array.from({length:8},(_,i)=>i).filter(m=>(m&~trueMask)===0);
  function run(node,mask){while(typeof node!=="number")node=node[(mask>>node[0]&1)?2:1];return node===1}
  function transcripts(node,seen=new Map(),consistent=true){
    if(typeof node==="number")return node===1;
    const q=node[0];
    for(let a=0;a<=1;a++){
      if(a&&!sat[q].length)continue;
      if(consistent&&seen.has(q)&&seen.get(q)!==a)continue;
      const next=new Map(seen);next.set(q,a);
      if(transcripts(node[a+1],next,consistent))return true;
    }
    return false;
  }
  let controllers=0,forged=0,occurrenceOnly=0,actualYes=0;
  for(let a=0;a<3;a++)for(let b=0;b<3;b++)for(let c=0;c<3;c++)for(let f=0;f<16;f++){
    const tree=[a,[b,f&1,(f>>1)&1],[c,(f>>2)&1,(f>>3)&1]];
    const exact=run(tree,trueMask),any=subsets.some(s=>run(tree,s)),cert=transcripts(tree);
    ok(any===cert,"consistent transcript equivalence");
    ok(!exact||cert,"true path preserved");
    if(exact)actualYes++;
    if(any&&!exact)forged++;
    if(transcripts(tree,new Map(),false)&&!any)occurrenceOnly++;
    controllers++;
  }
  const repeated=[0,[0,0,1],0];
  ok(transcripts(repeated,new Map(),false)&&!transcripts(repeated),"repeat consistency essential");
  const antitone=[0,1,0];ok(!run(antitone,trueMask)&&transcripts(antitone),"false negative");
  const monotone=[0,0,1];ok(run(monotone,trueMask)&&transcripts(monotone),"positive");
  return {checks,pairs,controllers,actualYes,forged,occurrenceOnly,queryModelCounts:sat.map(s=>s.length),trueMask,subsets,scope:"finite parser/clock and adaptive transcript controls; no asymptotic hierarchy witness execution; simulator is intentionally naive and not the near-linear verifier"};
}
console.log(JSON.stringify(audit(),null,2));
