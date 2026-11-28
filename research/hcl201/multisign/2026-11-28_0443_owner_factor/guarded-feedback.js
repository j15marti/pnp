function feedback(syn,corpus,registry){
 const sha=Function("const module={exports:{}};"+syn+";return module.exports.sha;")(),cor=JSON.parse(corpus),reg=JSON.parse(registry),enc=x=>JSON.stringify(x)+"\n";
 const norm=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b), key=x=>norm(x).join(",");
 const cases=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40","FANO-NAE-7","SAT-CONTROL"]){
  let x=cor.instances.find(x=>x.id===alias);
  if(!x&&alias==="SAT-CONTROL")x={id:alias,nvars:4,dimacs:"p cnf 4 3\n1 2 3 0\n-1 2 -3 0\n-2 4 0\n"};
  if(!x){cases.push({alias,missing:true});continue}
  const F=x.dimacs.trimEnd().split("\n").slice(1).map(l=>norm(l.trim().split(/\s+/).map(Number).slice(0,-1))),N=x.dimacs.length*8,h=sha(x.dimacs),instance_id="DIMACS-CNF-v1:sha256:"+h,n=x.nvars,entry=reg.instances.find(y=>y.source_cnf.alias===alias)?.source_cnf;
  if(entry&&(entry.sha256!==h||entry.N_bits!==N))throw Error("CNF hash");
  const guards=Array.from({length:5},(_,i)=>Array.from({length:Math.min(i+1,4)},(_,j)=>[j+1,i===4||j<i?1:0]));
  const guardRecords=[];
  const initCount={visits:0,forced:0};
  function propagate(rows,ass,charge){let a=ass.slice();for(;;){let change=false;for(let r of rows){let sat=false,unknown=[];for(let l of r.lits){charge();let v=a[Math.abs(l)];if(v===undefined)unknown.push(l);else if(v===Number(l>0)){sat=true;break}}if(sat)continue;if(!unknown.length)return {a,conflict:r.id};if(unknown.length===1){a[Math.abs(unknown[0])]=Number(unknown[0]>0);change=true}}if(!change)return {a,conflict:null}}}
  const original=F.map((lits,i)=>({id:i+1,lits}));
  for(let pins of guards){
   let a=[];for(let [v,b] of pins)a[v]=b;
   let gschema="CNF-VAR-PINS-v1",gbytes=enc(pins),guard_id="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",instance_id,gschema,sha(gbytes)]));
   let u=propagate(original,a,()=>initCount.visits++),forced=[];for(let i=1;i<=n;i++)if(u.a[i]!==undefined&&a[i]===undefined)forced.push([i,u.a[i]]);initCount.forced+=forced.length;
   let rows=[];if(!u.conflict)for(let r of original){if(r.lits.some(l=>u.a[Math.abs(l)]===Number(l>0)))continue;rows.push({id:r.id,lits:r.lits.filter(l=>u.a[Math.abs(l)]===undefined)})}
   let art=enc({rows,conflict:u.conflict}),map=enc({pins,forced,originalClauses:rows.map(r=>r.id)}),residual_id="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",instance_id,guard_id,"CNF-GUARDED-UP-v1",sha(art),sha(map)]));
   guardRecords.push({pins,guard_id,residual_id,rows,forced,conflict:u.conflict,artifact:art,map,assign:u.a});
  }
  let results=[];
  for(let width of [2,4])for(let mode of ["baseline","flips","deductions","table","residue"]){
   let c={events:0,literals:0,pairs:0,learned:0,flips:0,changedTies:0,check:0,nodes:0,peakRows:0,peakDepth:0},arms=[],cap=150000,start=Date.now();
   const tick=(kind="literals")=>{if(c.events>=cap)throw Error("cap");c.events++;c[kind]++};
   for(let G of guardRecords){
    if(G.conflict!==null){arms.push({guard_id:G.guard_id,residual_id:G.residual_id,decision:"NO",stage:"unreachable: early UP",conflict:G.conflict});continue}
    const rows=G.rows.map(r=>({...r,lits:r.lits.slice()})),learn=[],moves=[];let result="UNKNOWN",proof=null,witness=null,free=Array.from({length:n},(_,i)=>i+1).filter(i=>G.assign[i]===undefined);
    try{
     if(["deductions","table","residue"].includes(mode)){
      let seen=new Set(rows.map(r=>key(r.lits))),pairs=0,next=F.length+1;
      outer:for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++){
       if(pairs>=700||learn.length>=64)break outer;pairs++;tick("pairs");
       let r=rows[i],s=rows[j];for(let v of r.lits){tick();if(!s.lits.includes(-v))continue;let a=norm([...r.lits.filter(x=>x!==v),...s.lits.filter(x=>x!==-v)]);if(a.length>width||a.some(x=>a.includes(-x))||seen.has(key(a)))continue;
        // independently recompute resolvent from parent literals
        let z=new Set();for(let l of r.lits)if(l!==v){tick("check");z.add(l)}for(let l of s.lits)if(l!==-v){tick("check");z.add(l)}
        if(key([...z])!==key(a))throw Error("resolution");
        seen.add(key(a));let item={id:next++,lits:a,parents:[r.id,s.id],pivot:v};rows.push(item);learn.push(item);c.learned++;if(!a.length)break outer;
       }
      }
     }
     c.peakRows=Math.max(c.peakRows,rows.length);
     let seed=G.assign.slice();for(let v of free)seed[v]=0;
     function score(a){let bad=0,zero=0,fields=[];for(let r of rows){let k=0,sum=0;for(let l of r.lits){tick();if(a[Math.abs(l)]===Number(l>0)){k++;sum+=l>0?1:-1}}let sr=((sum%3)+3)%3;fields.push([r.id,k,k%3,sr]);if(!k)bad++;else if(!sr)zero++}return {bad,zero,fields}}
     if(["flips","table","residue"].includes(mode)){
      let now=score(seed);
      for(let step=0;step<8&&now.bad;step++){
       let best=null,plain=null;for(let v of free){let a=seed.slice();a[v]^=1;let s=score(a);if(s.bad>=now.bad)continue;if(!plain||s.bad<plain.s.bad||s.bad===plain.s.bad&&v<plain.v)plain={v,s,a};if(!best||s.bad<best.s.bad||s.bad===best.s.bad&&(mode==="residue"?(s.zero<best.s.zero||s.zero===best.s.zero&&v<best.v):v<best.v))best={v,s,a}}
       if(!best)break;if(best.v!==plain.v)c.changedTies++;moves.push({v:best.v,baselineTie:plain.v,before:now.bad,after:best.s.bad,fields:best.s.fields});seed=best.a;now=best.s;c.flips++;
      }
     }
     function go(a,depth){c.nodes++;c.peakDepth=Math.max(c.peakDepth,depth);let u=propagate(rows,a,()=>tick());if(u.conflict!==null)return {kind:"leaf",id:u.conflict};let v=free.find(x=>u.a[x]===undefined);if(v===undefined){witness=u.a;return {kind:"sat"}};let b=seed[v]??0,L=u.a.slice();L[v]=b;let p=go(L,depth+1);if(witness)return p;let R=u.a.slice();R[v]=1-b;let q=go(R,depth+1);return witness?q:{kind:"branch",v,b,p,q}}
     let p=go(G.assign,0);
     if(witness){for(let r of original){for(let l of r.lits)tick("check");if(!r.lits.some(l=>witness[Math.abs(l)]===Number(l>0)))throw Error("SAT source check")}if(G.pins.some(([v,b])=>witness[v]!==b))throw Error("guard witness");result="YES"}
     else{
      function verify(node,a){let u=propagate(rows,a,()=>tick("check"));if(node.kind==="leaf")return u.conflict===node.id;if(node.kind!=="branch"||u.conflict!==null||u.a[node.v]!==undefined)return false;let l=u.a.slice(),r=u.a.slice();l[node.v]=node.b;r[node.v]=1-node.b;return verify(node.p,l)&&verify(node.q,r)}
      if(!verify(p,G.assign))throw Error("tree replay");proof=p;result="NO";
     }
    }catch(e){if(String(e).includes("cap"))result="UNKNOWN";else throw e}
    arms.push({guard_id:G.guard_id,residual_id:G.residual_id,decision:result,learn,moves,proof,witness:result==="YES"?witness:null});
   }
   let dec=arms.some(a=>a.decision==="YES")?"YES":arms.every(a=>a.decision==="NO")?"NO":"UNKNOWN";
   results.push({width,mode,decision:dec,count:c,ms:Date.now()-start,arms});
  }
  cases.push({alias,instance_id,N,registryMatch:!!entry,source:x.dimacs,original_ids:{variables:[1,n],clauses:[1,F.length]},guards:guardRecords.map(({assign,...x})=>x),initialClosure:initCount,results});
 }
 return {cases,scope:"companion CNF only; exact exhaustive five prefix guards, early UP, guarded feedback before disjunctive recombination; independent resolution and DPLL tree replay with same propagation function; cap aggregate per width/mode arm; no native projection/import; no physical RSS; serial"};
}
module.exports={feedback};
