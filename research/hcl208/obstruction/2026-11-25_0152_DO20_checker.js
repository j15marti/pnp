function controls(){
 const out={cycles:[],fano:[],assertions:0}; const ck=x=>{out.assertions++;if(!x)throw Error("assertion "+out.assertions)};
 const pop=x=>{let k=0;for(;x;x&=x-1)k++;return k};
 const subs=function*(x){for(let a=x;;a=(a-1)&x){yield a;if(!a)break}};
 const bit=(w,i)=>(w>>>i)&1;
 const legal=(e,w)=>{let a=e.t.reduce((z,v,i)=>z|(bit(w,v)<<i),0)^e.p;return a!==0&&a!==7};
 const closure=(E,S)=>{let V=S,F=0,change=true;while(change){change=false;E.forEach((e,i)=>{let m=e.t.reduce((a,v)=>a|(1<<v),0);if(!(F>>i&1)&&pop(m&V)>=2){F|=1<<i;V|=m;change=true}})}return {V,F}};
 const forced=(E,S,w)=>{let V=S,A=w,change=true;while(change){change=false;for(const e of E){let known=[],unknown=[];for(let i=0;i<3;i++)if(V>>e.t[i]&1)known.push(bit(A,e.t[i])^bit(e.p,i));else unknown.push(i);
 if(known.length===3&&known.every(x=>x===known[0]))return false;
 if(known.length===2&&known[0]===known[1]){let i=unknown[0],v=e.t[i],b=1^known[0]^bit(e.p,i);V|=1<<v;if(b)A|=1<<v;else A&=~(1<<v);change=true;}
 }}return true};
 for(const [m,k] of [[5,3],[6,3],[7,3]]){
 let n=2*m, full=(1<<n)-1,E=Array.from({length:m},(_,i)=>({t:[i,(i+1)%m,m+i],p:(i*3+m)%8})),T=new Map(), stats={m,n,k,scopes:0,pinWords:0,extensionChecks:0,freeBitChecks:0,forestQueries:0,globalModels:0};
 let models=[];let forestModels=Array.from({length:m},()=>[]);for(let w=0;w<=full;w++){let f=0;E.forEach((e,i)=>{if(!legal(e,w))f|=1<<i});if(!f)models.push(w);for(let i=0;i<m;i++)if(!(f&~(1<<i)))forestModels[i].push(w)}
 stats.globalModels=models.length;
 for(let S=0;S<=full;S++){if(pop(S)>k)continue;let C=closure(E,S);let support=new Set();for(let w of subs(C.V))if(E.every((e,i)=>!(C.F>>i&1)||legal(e,w)))support.add(w&S);T.set(S,{C,support});stats.scopes++;
 ck(pop(C.F)<=Math.max(0,pop(S)-1));ck(pop(C.V)<=Math.max(0,2*pop(S)-1));
 let projections=forestModels.map(L=>new Set(L.map(w=>w&S)));
 for(let p of subs(S)){stats.pinWords++;ck(forced(E,S,p)===support.has(p));let all=true;for(let i=0;i<m;i++){stats.forestQueries++;let a=projections[i].has(p);ck(forced(E.filter((_,j)=>j!==i),S,p)===a);if(support.has(p))ck(a);all&&=a;}ck(all===support.has(p));}
 }
 for(const [S,{C,support}] of T){if(pop(S)===k)continue;for(let v=0;v<n;v++){let b=1<<v;if(S&b)continue;let next=T.get(S|b).support;for(const p of support){stats.extensionChecks++;ck(next.has(p)||next.has(p|b));if(!(C.V&b)){stats.freeBitChecks++;ck(next.has(p)&&next.has(p|b));}}}}
 out.cycles.push(stats);
 }
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 for(let j=-1;j<7;j++){let E=lines.map((t,i)=>({t,p:i===j?1:0}));let count=0;for(let w=0;w<128;w++)if(E.every(e=>legal(e,w)))count++;ck(count===(j<0?0:10));ck(forced(E,0,0));out.fano.push({flippedOwner:j,models:count,rootCoordinateClosure:"OPEN"})}
 return out;
}
function replay(lifts,sources){
 let out={witnesses:0,owners:0,guards:0,byMode:{}};
 for(const z of lifts){let src=sources[z.id],E=src.registry??src.O??src.owners; if(E.length!==z.owners)throw Error("owner count");
 let w=z.witness; if(w.reduce((a,b,i)=>a+b*2**i,0)!==z.integer)throw Error("word");
 for(const [v,b] of z.guard){if(w[v]!==b)throw Error("guard");out.guards++}
 // Peer source field p is provenance, not a literal sign mask. Actual bad list is authoritative.
 for(const e of E){let local=e.t.reduce((a,v,i)=>a+(w[v]<<i),0);if((e.bad??[0,7]).includes(local))throw Error("owner "+z.id+" "+z.mode);out.owners++}
 out.witnesses++;out.byMode[z.mode]=(out.byMode[z.mode]??0)+1;
 }return out;
}
// Run node checker.js [lifts.json DR17.json BW17.json M23.json]
const fs=require('fs');const args=process.argv.slice(2);let r={controls:controls()};if(args.length===4){const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));r.sourceReplay=replay(read(args[0]),{DR17:read(args[1]),BW17:read(args[2]),M23:read(args[3])});}console.log(JSON.stringify(r,null,2));
