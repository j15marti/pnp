function runAudit(){
  'use strict';
  let assertions=0;
  const check=(p,m)=>{assertions++;if(!p)throw Error('ASSERT: '+m)};
  const sat=clauses=>{
    const n=Math.max(0,...clauses.flat().map(Math.abs));
    if(n>12)throw Error('finite test width cap exceeded');
    for(let a=0;a<2**n;a++)if(clauses.every(c=>c.some(l=>Boolean((a>>(Math.abs(l)-1))&1)===(l>0))))return true;
    return false;
  };
  const encode=cs=>{
    const n=Math.max(0,...cs.flat().map(Math.abs));
    return `p cnf ${n} ${cs.length}\n`+cs.map(c=>c.join(' ')+(c.length?' ':'')+'0\n').join('');
  };
  const parse=s=>{
    const ls=s.trimEnd().split('\n'),h=ls.shift().split(' ');
    if(h.length!==4||h[0]!=='p'||h[1]!=='cnf')throw Error('bad header');
    const n=+h[2],m=+h[3];
    if(!Number.isInteger(n)||!Number.isInteger(m)||n<0||m<0||ls.length!==m)throw Error('bad counts');
    const cs=ls.map(line=>{
      const a=line.split(' ').filter(Boolean).map(Number);
      if(!a.length||a[a.length-1]!==0||a.slice(0,-1).some(x=>!Number.isInteger(x)||!x||Math.abs(x)>n))throw Error('bad clause');
      return a.slice(0,-1);
    });
    if(Math.max(0,...cs.flat().map(Math.abs))!==n)throw Error('bad maximum');
    return cs;
  };
  const restrict=(cs,v,b)=>cs.flatMap(c=>c.some(l=>Math.abs(l)===v&&((l>0)===Boolean(b)))?[]:[c.filter(l=>Math.abs(l)!==v)]);
  const sourceStream=cs=>{
    const first=new Map(),last=new Map(),ev=[];
    cs.forEach((c,j)=>c.forEach(x=>{let v=Math.abs(x);if(!first.has(v))first.set(v,j);last.set(v,j)}));
    cs.forEach((c,j)=>{
      [...first].filter(([v,k])=>k===j).map(([v])=>v).sort((a,b)=>a-b).forEach(v=>ev.push(['O',v]));
      ev.push(['C',c]);
      [...last].filter(([v,k])=>k===j).map(([v])=>v).sort((a,b)=>a-b).forEach(v=>ev.push(['X',v]));
    });return ev;
  };
  const aliasedStream=cs=>cs.flatMap(c=>{
    const ids=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);
    return [...ids.map(v=>['O',v]),['C',c],...ids.map(v=>['X',v])];
  });
  const local=ev=>{
    let live=new Set(),peak=0;
    for(const [type,arg] of ev){
      if(type==='O'){
        if(!Number.isInteger(arg)||arg<=0||live.has(arg))return [false,peak,'bad-open'];
        live.add(arg);peak=Math.max(peak,live.size);
      }else if(type==='C'){
        if(!Array.isArray(arg)||arg.length>3||new Set(arg.map(Math.abs)).size!==arg.length||
            arg.some(x=>!Number.isInteger(x)||x===0||!live.has(Math.abs(x))))return [false,peak,'bad-clause'];
      }else if(type==='X'){
        if(!live.has(arg))return [false,peak,'bad-close'];live.delete(arg);
      }else return [false,peak,'bad-tag'];
    }return [live.size===0,peak,live.size?'unclosed':'local-valid'];
  };
  const dp=ev=>{
    const live=[];let states=new Set(['']);
    for(const [op,val] of ev){
      if(op==='O'){
        live.push(val);const next=new Set();
        for(const s of states){next.add(s+'0');next.add(s+'1')}states=next;
      }else if(op==='C'){
        states=new Set([...states].filter(s=>val.some(x=>s[live.indexOf(Math.abs(x))]===(x>0?'1':'0'))));
      }else if(op==='X'){
        let i=live.indexOf(val);states=new Set([...states].map(s=>s.slice(0,i)+s.slice(i+1)));live.splice(i,1);
      }
    }return states.size>0;
  };
  const global=ev=>{let ids=ev.filter(([t])=>t==='O').map(([,v])=>v);return ids.length===new Set(ids).size};
  const validate=(ev,b)=>{
    const m=ev.length,h=Math.max(1,Math.ceil(Math.log2(m+1)));
    let scans=0,probes=0,addressWrites=0,addressFlips=0,tableComparisons=0,peak=0;
    const at=i=>{probes++;addressWrites+=2*h;let k=i;while(k){addressFlips+=2*(k&1);k>>>=1;}return ev[i]};
    const result=passed=>({passed,scans,probes,addressWrites,addressFlips,tableComparisons,peakBufferRecords:peak,batch:b,events:m});
    for(let start=0;start<m;start+=b){
      let entries=[];
      for(let i=start;i<Math.min(m,start+b);i++){let [type,value]=at(i);if(type==='O')entries.push([value,i]);}
      entries.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);peak=Math.max(peak,entries.length);
      for(let z=1;z<entries.length;z++)if(entries[z][0]===entries[z-1][0])return result(false);
      scans++;
      for(let j=0;j<m;j++){
        const [type,value]=at(j);if(type!=='O')continue;
        let lo=0,hi=entries.length;
        while(lo<hi){let mid=(lo+hi)>>1;tableComparisons++;if(entries[mid][0]<value)lo=mid+1;else hi=mid;}
        if(lo<entries.length&&entries[lo][0]===value&&entries[lo][1]!==j)return result(false);
      }
    }return result(true);
  };
  const raw={run:'ARC-INDEXED-VALIDATOR-BATCH120',status:'COMPUTATIONAL',seed:null,
    auditKind:'finite deterministic logical event/index proxies, not literal FLMV or hardware traces',
    sourceCases:[],firstLevel:[],grandchildren:[],batchCases:[],widthThree:[],malformed:[]};
  const eight=Array.from({length:8},(_,k)=>Array.from({length:3},(_,i)=>((k>>i)&1)?-(i+1):(i+1)));
  const seven=eight.slice(0,7);
  const cycle=odd=>Array.from({length:4},(_,i)=>{
    const u=i+1,v=(i+1)%4+1;
    return (odd&&i===3)?[[u,v],[-u,-v]]:[[u,-v],[-u,v]];
  }).flat();
  const controls=[['all-eight-3CNF-UNSAT',eight],['seven-of-eight-3CNF-SAT',seven],
    ['Horn-units-UNSAT',[[1],[-1]]],['Horn-positive-SAT',[[1],[-1,2],[2]]],
    ['2SAT-affine-even-SAT',cycle(false)],['2SAT-affine-odd-UNSAT',cycle(true)],
    ['independent-SAT',[[1,2,3],[4,5,6]]],['independent-UNSAT',[...eight,[4,5,6]]]];
  for(const [name,cs] of controls){
    check(JSON.stringify(parse(encode(cs)))===JSON.stringify(cs),'ordinary root parse '+name);
    const truth=sat(cs),good=sourceStream(cs),bad=aliasedStream(cs);
    check(local(good)[0]&&local(bad)[0],'local grammar '+name);
    check(dp(good)===truth,'exact named DP '+name);
    check(dp(bad)===cs.every(c=>c.length>0),'aliased DP == conjunction of independent clause truths '+name);
    for(const [kind,ev] of [['good',good],['reopened',bad]]){
      for(const b of [1,2,3,5,8,16]){
        const result=validate(ev,b);
        check(result.passed===global(ev),'batch global freshness '+name+' '+kind+' '+b);
        if(result.passed)check(dp(ev)===truth,'accepted same source SAT label');
        if(name==='all-eight-3CNF-UNSAT')raw.batchCases.push({name,kind,...result});
      }
    }
    raw.sourceCases.push({name,rootBytes:encode(cs).length,truth,goodEvents:good.length,
      goodWidth:local(good)[1],aliasEvents:bad.length,aliasWidth:local(bad)[1],
      badLocalValid:local(bad)[0],badDP:dp(bad),badFresh:global(bad)});
  }
  check(!sat(eight)&&sat(seven),'opposite ordinary source labels');
  for(const [name,cs] of controls.slice(0,2)){
    check(sat(cs)===[0,1].some(x=>sat(restrict(cs,1,x))),'root Shannon');
    for(const x of [0,1]){
      let child=restrict(cs,1,x),childGood=sourceStream(child),childAlias=aliasedStream(child);
      check(JSON.stringify(parse(encode(child)))===JSON.stringify(child),'ordinary child parsed');
      check(dp(childGood)===sat(child),'true child DP');
      for(const b of [1,2,4,8])check(validate(childAlias,b).passed===global(childAlias),'child freshness');
      raw.firstLevel.push({name,x,bytes:encode(child).length,sat:sat(child),aliasLocal:local(childAlias)[0],
        aliasGlobal:global(childAlias),aliasDP:dp(childAlias)});
      check(sat(child)===[0,1].some(y=>sat(restrict(child,2,y))),'first-level Shannon');
      for(const y of [0,1]){
        const gc=restrict(child,2,y),gv=sourceStream(gc),ga=aliasedStream(gc),
            N0=encode(cs).length,N1=encode(child).length,N2=encode(gc).length;
        check(JSON.stringify(parse(encode(gc)))===JSON.stringify(gc),'ordinary grandchild parsed');
        check(N2<N1&&N1<N0,'two real short ordinary lengths');
        check(dp(gv)===sat(gc),'valid two-level semantics');
        check(local(ga)[0],'aliased child locally valid');
        for(const b of [1,2,4,8])check(validate(ga,b).passed===global(ga),'grandchild freshness');
        raw.grandchildren.push({name,x,y,rootBytes:N0,childBytes:N1,grandchildBytes:N2,
          rootSAT:sat(cs),childSAT:sat(child),grandchildSAT:sat(gc),
          badLocal:local(ga)[0],badGlobal:global(ga),badDP:dp(ga)});
      }
    }
  }
  for(const q of [2,4,8,16,24,48,96]){
    const ev=[];
    for(let j=1;j<=q;j++){
      const a=q+2*j-1,b=q+2*j;
      ev.push(['O',j],['O',a],['O',b],['C',[j,a,b]],['X',b],['X',a],['X',j]);
    }
    check(local(ev)[0]&&local(ev)[1]===3&&global(ev),'valid width-3');
    const corrupt=ev.map(z=>[z[0],Array.isArray(z[1])?z[1].slice():z[1]]),p=7*(q-1);
    corrupt[p]=['O',1];corrupt[p+3]=['C',[1,q+2*q-1,q+2*q]];corrupt[p+6]=['X',1];
    check(local(corrupt)[0]&&local(corrupt)[1]===3&&!global(corrupt),'malformed only globally');
    for(const b of [1,2,3,5,8,13,24,64,128].filter(z=>z<=ev.length)){
      const ok=validate(ev,b),ko=validate(corrupt,b);
      check(ok.passed&&!ko.passed,'both width3 source labels');
      check(ok.probes===ev.length+Math.ceil(ev.length/b)*ev.length,'exact valid full scan');
      raw.widthThree.push({q,...ok,corruptProbesUntilReject:ko.probes});
    }
  }
  const malformed=[[['C',[1]]],[['O',1],['C',[1,1]],['X',1]],[['O',1],['X',1],['C',[1]]],
    [['O',1]],[['O',1],['O',1],['X',1],['X',1]],[['O',1],['C',[1]],['X',1],['X',1]],[['Q',1]]];
  for(const ev of malformed){let r=local(ev);check(!r[0],'reject local malformed');raw.malformed.push({events:ev.length,reason:r[2]});}
  for(const s of ['p cnf 2 1\n1 2 0\n0\n','p cnf 2 1\n3 0\n','x cnf 1 1\n1 0\n']){
    let caught=false;try{parse(s)}catch(e){caught=true}check(caught,'reject ordinary malformed header/record');
  }
  raw.math={timeThreshold:'241/200',spaceThreshold:'11642479/23232400',
    validatorArchitectureTimeFloorAtMu1:'34822321/23232400',
    gapAboveTimeThreshold:'6827279/23232400',
    deltaTightCase:'2 - spaceThreshold > timeThreshold'};
  raw.assertions=assertions;raw.failures=0;
  raw.summary={sourceCases:raw.sourceCases.length,firstLevelCases:raw.firstLevel.length,
    twoLevelCases:raw.grandchildren.length,widthThreeBatchCases:raw.widthThree.length,
    sourceSAT:raw.sourceCases.filter(x=>x.truth).length,
    sourceUNSAT:raw.sourceCases.filter(x=>!x.truth).length};
  return raw;
}
if (typeof module !== 'undefined' && require.main === module) {
  const fs=require('fs'), raw=runAudit(), arg=process.argv[2];
  if(arg) fs.writeFileSync(arg,JSON.stringify(raw,null,2)+'\n');
  console.log(JSON.stringify({run:raw.run,checks:raw.assertions,...raw.summary,status:'PASS'}));
}
