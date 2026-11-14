'use strict';
// TMR4-HC5 exact finite transition-table audit. Node.js: node this_file.cjs
function audit(){
  let assertions=0,checks=0,spurious=0,rereads=0,totSteps=0,passed=0,maxT=0,maxPhi=0,workMoves=0;
  const ok=(v,m)=>{assertions++;if(!v)throw new Error(m)};
  function build(kind){
    const tab=new Map();
    const put=(state,input,work,next,write,mi,mw)=>{tab.set([state,input,work].join("|"),{next,write,mi,mw});};
    for(const w of ["_","1"]){
      put("scan","0",w,"scan",w,1,0);
      put("scan","1",w,"scan",w==="1"?"_":"1",1,0);
      if(kind==="FAST")put("scan","$",w,w==="1"?"SAT":"UNSAT",w,0,0);
      else {
        put("scan","$",w,"shift",w,0,0);
        put("shift","$",w,"restore",w,0,1);
        put("rewind","0",w,"rewind",w,-1,0);
        put("rewind","1",w,"rewind",w,-1,0);
        put("rewind","^",w,"resweep",w,1,0);
        put("resweep","0",w,"resweep",w,1,0);
        put("resweep","1",w,"resweep",w,1,0);
        put("resweep","$",w,w==="1"?"SAT":"UNSAT",w,0,0);
      }
    }
    if(kind==="SLOW")put("restore","$","_","rewind","_",-1,-1);
    return tab;
  }
  function simulate(x,kind){
    const table=build(kind), states=[];
    let c={program:kind,input:x,state:"scan",ih:0,wh:0,work:{},step:0};
    const snap=q=>({program:q.program,input:q.input,state:q.state,ih:q.ih,wh:q.wh,work:{...q.work},step:q.step});
    states.push(snap(c));
    while(!["SAT","UNSAT"].includes(c.state)){
      ok(c.step<1000,"fixture nontermination");
      const is=c.ih===-1?"^":c.ih===x.length?"$":x[c.ih];
      ok(is!==undefined,`head outside source ${c.ih}`);
      const ws=c.work[c.wh]??"_";
      const tr=table.get([c.state,is,ws].join("|"));
      ok(!!tr,`missing transition ${kind} ${c.state} ${is} ${ws}`);
      if(c.state==="resweep"&&["0","1"].includes(is))rereads++;
      if(tr.mw!==0)workMoves++;
      c.work[c.wh]=tr.write;
      c={...c,ih:c.ih+tr.mi,wh:c.wh+tr.mw,state:tr.next,step:c.step+1};
      ok(c.ih>=-1&&c.ih<=x.length,`illegal input head ${c.ih}`);
      states.push(snap(c));
    }
    let parity=0;for(const bit of x)parity^=Number(bit);
    ok(c.state===(parity?"SAT":"UNSAT"),"wrong terminal parity");
    return states;
  }
  function graph(states,B){
    const T=states.length-1, label=states[T].state, cutoff=T>B;
    const edges=[], vertices=new Set(["gSAT","gUNSAT"]);
    const add=(a,b,w)=>{vertices.add(a);vertices.add(b);edges.push({a,b,w})};
    for(let i=0;i<Math.min(B,T);i++){
      const dest=i+1===T?"g"+label:i+1===B&&cutoff?"star":"p"+(i+1);
      add("p"+i,dest,1);
    }
    if(cutoff){add("star","star",0);add("star","gSAT",0);add("star","gUNSAT",0)}
    const start=B===0&&T>0?"star":T===0?"g"+label:"p0";
    if(B===0&&T>0&&!cutoff)throw Error("unreachable");
    vertices.add(start);
    const ds={};for(const v of vertices)ds[v]=v==="gSAT"||v==="gUNSAT"?0:Infinity;
    for(let round=0;round<vertices.size+1;round++){
      let changed=false;
      for(const {a,b,w} of edges)if(ds[a]>w+ds[b]){ds[a]=w+ds[b];changed=true}
      if(!changed)break;
    }
    for(const {a,b,w} of edges)ok(ds[a]<=w+ds[b],`potential inequality ${a}->${b}`);
    ok(ds.gSAT<=0&&ds.gUNSAT<=0,"terminal values");
    ok(ds[start]===Math.min(T,B),`cap distance wrong ${T},${B},${ds[start]}`);
    for(let t=0;t<T;t++){
      const src=t>=B?"star":"p"+t;
      const target=(t+1===T)?"g"+label:(t+1>=B)?"star":"p"+(t+1);
      const e=edges.find(q=>q.a===src&&q.b===target);
      ok(!!e,`missing exact transition ${t} ${src} ${target}`);
      ok(e.w<=1,`overcharged step ${t}`);
      if(t<B){
        ok(states[t].program===states[t+1].program&&states[t].input===states[t+1].input,"lost fixed source/program");
        ok(states[t+1].step===states[t].step+1,"bad concrete transition step counter");
      }
      checks++;
    }
    if(cutoff){ok(states[B].state!=="SAT"&&states[B].state!=="UNSAT","prefix unexpectedly terminated");spurious++}
    maxPhi=Math.max(maxPhi,ds[start]);
    return ds[start];
  }
  const samples=[];
  for(const kind of ["FAST","SLOW"]){
    for(let n=0;n<=8;n++)for(let val=0;val<2**n;val++){
      const x=n===0?"":val.toString(2).padStart(n,"0");
      const states=simulate(x,kind),T=states.length-1;
      passed++;totSteps+=T;maxT=Math.max(maxT,T);
      const horizons=new Set([0,1,2,3,Math.floor(T/2),Math.max(0,T-1),T,T+1]);
      for(const B of horizons)graph(states,B);
      if(samples.length<6&&n>=1)samples.push({program:kind,input:x,T,cutoffs:[0,1,2,T-1,T].map(B=>({B,distance:Math.min(B,T)}))});
    }
  }
  return {claim:"TMR4-HC5",model:"explicit finite transition table, two-way input head, one writable tape",inputLengths:"0..8 exhaustive",programs:["FAST","SLOW"],runs:passed,concreteSteps:totSteps,maxConcreteTime:maxT,abstractSimulationChecks:checks,potentialAssertions:assertions,nonhaltingHorizonSpuriousPaths:spurious,secondPassPhysicalReads:rereads,writableHeadMoves:workMoves,failures:0,samples};
}
if (typeof module !== 'undefined' && require.main === module) console.log(JSON.stringify(audit(),null,2));
module.exports = { audit };
