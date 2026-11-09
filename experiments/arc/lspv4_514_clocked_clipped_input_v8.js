// LSPV-4/514: independent V8 symbolic index-tape and clipped-input monitor.
// This is NOT a native FLMV interpreter or general SAT solver.
function verify(){
  function check(x,msg){if(!x)throw Error(msg);}
  function clauses(q){let E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],out=[];
    for(let v=0;v<4;v++){let a=E.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
      for(let b=0;b<8;b++){let p=((b&1)+((b>>1)&1)+((b>>2)&1))&1;
        if(p===((q>>v)&1))continue;
        out.push(a.map((x,j)=>((b>>j)&1)?-x:x));}}
    return out;}
  function packet(cs){let s='10100101'+cs.length.toString(2).padStart(8,'0');
    for(let c of cs)for(let x of c)s+=Math.abs(x).toString(2).padStart(3,'0')+(x<0?'1':'0');
    return Array.from(s+'01',Number);}
  function sat(cs){for(let x=0;x<64;x++)if(cs.every(c=>c.some(l=>Boolean((x>>(Math.abs(l)-1))&1)===(l>0))))return true;return false;}
  function simulation(ev,input,H,clip){
    let ix=0,idx=new Set(),head=0n,obs=[],idxObs=[],far=false,local=0,lo=0n,hi=0;
    let L=BigInt(input.length+H),bits=Math.ceil(Math.log2(input.length+H+2));
    for(let e of ev.slice(0,H)){let [op,b]=e;
      if(op==='>')ix++;
      else if(op==='<')ix=Math.max(0,ix-1);
      else if(op==='W'){let old=idx.has(ix)?1:0;
        if(b)idx.add(ix);else idx.delete(ix);
        if(clip){if(ix<bits){let m=1n<<BigInt(ix);lo=b?(lo|m):(lo&~m);}else hi+=b-old;check(hi>=0,'high count');}}
      else if(op==='Q')idxObs.push(idx.has(ix)?1:0);
      else if(op==='J'){
        if(clip){if(hi||lo>L)far=true;else{far=false;local=Number(lo);}lo=0n;hi=0;}
        else head=Array.from(idx).reduce((s,i)=>s+(1n<<BigInt(i)),0n);
        idx.clear();}
      else if(op==='-'){if(clip){if(!far)local=Math.max(0,local-1);}else if(head>0n)head--;}
      else if(op==='+'){if(clip){if(!far&&++local>Number(L))far=true;}else head++;}
      else if(op==='R')obs.push(clip?(far||local>=input.length?0:input[local]):(head>=BigInt(input.length)?0:input[Number(head)]));
      else throw Error('bad event');
    }
    return {obs,idxObs};
  }
  function events(seed,n){let a=[],s=seed>>>0;
    for(let i=0;i<n;i++){s=(Math.imul(s,1664525)+1013904223)>>>0;let r=s%100;
      if(r<20)a.push(['>']);else if(r<24)a.push(['<']);
      else if(r<53)a.push(['W',(s>>>13)&1]);
      else if(r<60)a.push(['Q']);else if(r<68)a.push(['J']);
      else if(r<83)a.push(['R']);else if(r<91)a.push(['-']);else a.push(['+']);}
    return a;}
  let cases=0,assertions=0,guestSteps=0,clockedSteps=0,outputReads=0;
  for(let charge=0;charge<16;charge++){
    let cs=clauses(charge),p=packet(cs);check(cs.length===16&&p.length===210,'original 3CNF encoding');
    check(sat(cs)===(Number(charge.toString(2).replace(/0/g,'').length)%2===0),'parity label');
    for(let z=0;z<23;z++){
      let ev=events(21+z*873+charge*911,31+(z*43+charge*19)%163);
      if(z%2===0){let i=19+z;ev=[...Array.from({length:i},()=>['>']),['W',1],['J'],['R'],...ev];}
      let full=simulation(ev,p,ev.length,false),H=1,work=0,run;
      while(true){run=simulation(ev,p,H,true);work+=Math.min(H,ev.length);
        if(H>=ev.length)break;H*=2;}
      check(JSON.stringify(run)===JSON.stringify(full),'full trace mismatch');
      check(work<3*ev.length,'clock cost');guestSteps+=ev.length;clockedSteps+=work;outputReads+=full.obs.length;
      for(let h of [1,2,3,7,15,31,63,127,ev.length]){
        if(h>ev.length)continue;
        check(JSON.stringify(simulation(ev,p,h,false))===JSON.stringify(simulation(ev,p,h,true)),'prefix mismatch');assertions++;}
      cases++;
    }
  }
  return {status:'PASS',scope:'hosted symbolic indexed-input trace equivalence; NOT native FLMV',cases,assertions,SAT_sources:8,UNSAT_sources:8,source_bits:210,guestSteps,clockedSteps,outputReads,clock_ratio:clockedSteps/guestSteps};
}
