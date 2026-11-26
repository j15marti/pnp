function orderProof(ell){
 const H=2**ell,lines=[],width=2*ell;let ax=0,weak=0,res=0;
 const norm=c=>[...new Set(c)].sort((a,b)=>a-b),same=(a,b)=>a.join()===b.join();
 const add=(c,rule,parents=[])=>{c=norm(c);lines.push(c);if(rule==="axiom")ax++;else if(rule==="weak")weak++;else res++;return lines.length-1}
 const bad=(row,t)=>Array.from({length:ell},(_,j)=>((t>>j)&1)?-(row*ell+j+1):row*ell+j+1);
 function resolve(i,j,v){const a=lines[i],b=lines[j];if(!(a.includes(v)&&b.includes(-v)||a.includes(-v)&&b.includes(v)))throw Error("pivot");const c=norm([...a.filter(x=>Math.abs(x)!==v),...b.filter(x=>Math.abs(x)!==v)]);if(c.some(x=>c.includes(-x)))throw Error("tautology");return add(c,"resolve",[i,j])}
 function weaken(i,c){c=norm(c);if(!lines[i].every(x=>c.includes(x)))throw Error("weak");return add(c,"weak",[i])}
 function eliminate(ids,row,tail){let layer=ids.slice();for(let bit=0;bit<ell;bit++){let next=[];for(let k=0;k<layer.length;k+=2)next.push(resolve(layer[k],layer[k+1],row*ell+bit+1));layer=next}if(!same(lines[layer[0]],norm(tail)))throw Error("tail");return layer[0]}
 let prev=[];
 for(let row=1;row<=H;row++){
 const current=[];
 for(let u=0;u<row;u++){const tail=bad(row,u),ids=[];for(let t=0;t<H;t++){const c=[...bad(row-1,t),...tail];if(t<row-1)ids.push(weaken(prev[t],c));else{if(t<u)throw Error("invalid order axiom");ids.push(add(c,"axiom"))}}
 current[u]=eliminate(ids,row-1,tail)}
 prev=current;
 }
 const last=eliminate(prev,H,[]);if(lines[last].length)throw Error("not refuted");return {ell,H,lines:lines.length,axiomOccurrences:ax,weakening:weak,resolutions:res,maxWidth:width,verifiedEmpty:true}
}

function supplement(api){
 const {assert,C,source,fp,close,valid,domains,laneA,laneB,laneC}=api,results={orderProofs:[],tightHall:[],ell5Closure:[]};
 const slim=q=>({...q,forced:q.forced?.length});
 for(const ell of [1,2,3,4,5])results.orderProofs.push(orderProof(ell));
 for(const ell of [2,3,4,5]){
 const H=2**ell,P=H+1,lab=Array.from({length:P},(_,i)=>Math.max(0,i-1)),base=Array.from({length:H/2},(_,j)=>[j+2,ell-1,0]),baseNo=[...base,[H/2+2,ell-1,0]];
 for(const no of [false,true]){
 const guards=no?baseNo:base,F=source(ell,true,lab,guards),pre=close(F),cap=Math.min(F.N,4096);assert(!pre.NO,"Hall native initial should survive");
 const A=laneA(ell,true,guards,cap),B=laneB(ell,true,guards),Cc=laneC(ell,true,guards,cap);
 assert(B.answer===(no?"NO":"YES"),"Hall mode");assert(A.answer==="UNKNOWN"||A.answer===B.answer,"A");assert(Cc.answer==="UNKNOWN"||Cc.answer===B.answer,"C");
 const d=domains(ell,true,guards),S=d.G.map((g,i)=>({g,i})).filter(({g})=>g.some(j=>guards.some(x=>x[0]===j))).map(({i})=>i),Y=new Set(S.flatMap(i=>d.D[i]));assert(Y.size===H/2&&S.length===H/2+Number(no),"tight Hall certificate");
 let imported=[],after=null,again=null;
 if(!no){for(let i=0;i<d.G.length;i++)if(!S.includes(i)){const remain=d.D[i].filter(x=>!Y.has(x));assert(remain.length&&remain.every(x=>x>=H/2),"outside high");for(const j of d.G[i])imported.push([j,ell-1,1])}
 assert(imported.every(g=>!pre.forced.some(p=>p.join()===g.join())),"new deductions");
 const G=[...guards,...imported];const old=source(ell,true,B.labels,G),newF=source(ell,true,B.labels,G,true);assert(valid(B.labels,true,G)&&old.K.every(k=>C(...k.map(i=>old.V[i])))&&newF.K.every(k=>C(...k.map(i=>newF.V[i]))),"native lift after import");after=close(old);assert(!after.NO&&imported.every(g=>after.forced.some(p=>p.join()===g.join())),"native reclosure");again=laneA(ell,true,G,cap);assert(again.answer!=="NO","new A")}
 results.tightHall.push({ell,H,no,N:F.N,fp:fp(F),initial:slim(pre),A:{answer:A.answer,nodes:A.nodes},B:{answer:B.answer,probes:B.probes},C:{answer:Cc.answer,tried:Cc.tried},certificate:{groups:S,neighborLabels:[...Y]},imported,after:after?slim(after):null,integrated:no?"NO":again.answer==="YES"?"YES":"YES by verified B witness",postA:again?{answer:again.answer,nodes:again.nodes}:null})
 }
 }
 const ell=5,H=32,P=33,lab=Array.from({length:P},(_,i)=>Math.max(0,i-1));for(const [name,pos,guards] of [["yes",true,[]],["no",false,[]],["guarded Hall NO",true,Array.from({length:H/2+1},(_,j)=>[j+2,ell-1,0])],["opposite equality guard NO",true,[[0,0,0],[1,0,1]]],["guarded YES",true,[[0,0,0],[P-1,ell-1,1]]]]){const F=source(ell,pos,lab,guards),p=close(F);const B=laneB(ell,pos,guards);let post=null;if(B.answer==="YES"){const old=source(ell,pos,B.labels,guards);post=close(old);assert(!post.NO,"post closure")};assert(!p.NO||B.answer==="NO","closure contradicts witness");results.ell5Closure.push({name,fp:fp(F),N:F.N,initial:slim(p),post:post?slim(post):null})}
 return results
}

const fs=require('node:fs');const path=require('node:path');const s=fs.readFileSync(path.join(__dirname,'audit.js'),'utf8');const api=new Function(s.replace(/console\.log\(JSON\.stringify\(audit\(\),null,2\)\);\s*$/,'return {assert,C,source,fp,close,valid,domains,laneA,laneB,laneC};'))();console.log(JSON.stringify(supplement(api),null,2));
