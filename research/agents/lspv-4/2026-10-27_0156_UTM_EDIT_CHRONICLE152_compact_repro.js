'use strict';
// UTM-EDIT-CHRONICLE152: independent finite verification; node file.js
// Every simulated source has a single sequential input head and one work head.
let n=0,pairs=0,diagonals=0,changes=0,distinct=0;
const assert=(v,msg)=>{n++;if(!v)throw Error('FAIL '+n+' '+msg);};
const bits=(i,m)=>i.toString(2).padStart(m,'0');
function run(a,b){
  const m=a.length, gap='X'.repeat(9), input='^'+a+'|'+gap+'|'+b.split('').reverse().join('')+'$';
  let ip=1,wp=0,phase='LOAD',D=0,W=0,T=0;
  const work=new Map(),log=[],crosses=[];
  const cut=1+m+1+4;
  while(T<4*input.length){
    T++;let c=input[ip],old=ip;
    if(phase==='LOAD'){
      if(c==='0'||c==='1'){
        W++;if((work.get(wp)||'0')!==c){D++;if(c==='0')work.delete(wp);else work.set(wp,c);
          log.push(['edit',wp,c]);}
        wp++;ip++;
      }else if(c==='|'){phase='GAP';wp--;ip++;}
      else throw Error('syntax load');
    }else if(phase==='GAP'){
      if(c==='X')ip++;
      else if(c==='|'){phase='CHECK';ip++;}
      else throw Error('syntax gap');
    }else if(phase==='CHECK'){
      if(c==='0'||c==='1'){
        if(c==='1'&&(work.get(wp)||'0')==='1')phase='REJECT';
        wp--;ip++;
      }else if(c==='$')phase='ACCEPT';
      else throw Error('syntax check');
    }
    if(old<cut&&ip>=cut){
      log.push(['cross',phase,wp]);
      crosses.push([...work.entries()].sort((x,y)=>x[0]-y[0]));
    }
    if(phase==='ACCEPT'||phase==='REJECT')break;
  }
  let expected=!Array.from(a).some((v,i)=>v==='1'&&b[i]==='1');
  assert((phase==='ACCEPT')===expected,'DISJ exact');
  assert(D===Array.from(a).filter(x=>x==='1').length,'real changes');
  assert(W===m,'formal writes');
  assert(crosses.length===1,'one gap crossing');
  let restored=new Map(),at=0;
  for(const e of log){
    if(e[0]==='edit')restored.set(e[1],e[2]);
    else {assert(JSON.stringify([...restored].sort((x,y)=>x[0]-y[0]))===JSON.stringify(crosses[at]),'decode');
      at++;}
  }
  assert(at===1,'reconstruct all crossings');
  return {log:JSON.stringify(log),full:JSON.stringify(crosses),crossLabel:JSON.stringify(log.filter(e=>e[0]==='cross')),D};
}
for(let m=1;m<=5;m++)for(let i=0;i<2**m;i++)for(let j=0;j<2**m;j++){
  run(bits(i,m),bits(j,m));pairs++;
}
for(let m=1;m<=10;m++){
  let A=new Set(),B=new Set(),incomplete=new Set();
  for(let i=0;i<2**m;i++){
    let a=bits(i,m),b=a.replace(/[01]/g,c=>c==='0'?'1':'0'),z=run(a,b);
    A.add(z.log);B.add(z.full);incomplete.add(z.crossLabel);diagonals++;changes+=z.D;
  }
  assert(A.size===2**m&&B.size===2**m,'diagonal injection');
  assert(incomplete.size===1,'omitted edits collide');
  distinct+=A.size;
}
const cases=[{k:1,s:.5,d:.25,old:1,refined:.75},{k:1,s:.4,d:.3,old:1,refined:.7},{k:2,s:.4,d:.3,old:1.4,refined:1.1}];
for(const z of cases){
  assert(Math.abs(z.old-(z.d+z.k*z.s+Math.min(z.d,z.s)))<1e-9,'old value');
  assert(Math.abs(z.refined-(z.d+z.k*z.s))<1e-9,'new value');
}
const out={id:'UTM-EDIT-CHRONICLE152',status:'COMPUTATIONAL, restricted toy',seed:null,assertions:n,failed:0,pairs,diagonals,changes,distinct,cases};
console.log(JSON.stringify(out,null,2));