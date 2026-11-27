function audit(){
 let seed=26011632;const rnd=()=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)/4294967296);
 const rng=n=>Array.from({length:n},(_,i)=>i);let checks=0;const assert=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
 const atom=rng(6).map(i=>[(i+5)%6,i,(i+1)%6]);let atomWords=[];for(let j=0;j<64;j++){let w=rng(6).map(i=>(j>>i)&1);if(atom.every(r=>r.reduce((s,i)=>s+w[i],0)===1))atomWords.push(w.join(""))}assert(atomWords.sort().join(",")==="001001,010010,100100");
 function build(m,q,R){let rows=[],guards=[],blocks=[],sel=[];const add=()=>{let b=rows.length;for(const r of atom)rows.push(r.map(i=>b+i));return b};for(let i=0;i<m;i++){let g=[];for(let a=0;a<q;a++){let b=add();g.push(b);guards.push([[b+1],0])}sel.push(g);guards.push([g,1])}
 const conflict=(x,y)=>{let b=add();guards.push([[b,x],0],[[b+1,y],0]);blocks.push([b,x,y])};for(let i=0;i<m;i++){for(let a=0;a<q;a++)for(let b=a+1;b<q;b++)conflict(sel[i][a],sel[i][b]);for(let a=0;a<q;a++)for(let b=0;b<q;b++)if(!R[i][a][b])conflict(sel[i][a],sel[(i+1)%m][b])}
 return {rows,guards,blocks,sel}}
 function lift(F,w){let x=Array(F.rows.length).fill(0);for(let i=0;i<w.length;i++)for(let a=0;a<F.sel[i].length;a++){let b=F.sel[i][a],v=+(a===w[i]);x[b]=x[b+3]=v;x[b+2]=x[b+5]=1-v}
 for(const [b,u,v] of F.blocks){x[b]=x[b+3]=x[u];x[b+1]=x[b+4]=x[v];x[b+2]=x[b+5]=1-x[u]-x[v]}
 assert(x.every(v=>v===0||v===1));assert(F.rows.every(r=>r.reduce((s,i)=>s+x[i],0)===1));assert(F.guards.every(([r,b])=>r.reduce((s,i)=>s^x[i],0)===b));return x.join("")}
 let results=[];const tally={A:0,B:0,C:0,I:0,yes:0,no:0,acReject:0,Achecks:0,Bchecks:0,Cchecks:0,ACchecks:0};
 function run(m,q,mode){let R=rng(m).map(i=>rng(q).map(a=>rng(q).map(b=>mode==="random"?+(rnd()<0.47):+(b===(a+(i===m-1&&mode==="twist"?1:0))%q))));
 let F=build(m,q,R),N=JSON.stringify([F.rows,F.guards]).length,cap=Math.min(N*N,100000),d=rng(m).map(()=>rng(q)),ac=0,change=true;
 // Arc consistency on exact selector domains; initial local pin/equality compilation is explicit in build.
 while(change){change=false;for(let i=0;i<m;i++){let j=(i+1)%m;let a=d[i].filter(a=>d[j].some(b=>{ac++;return R[i][a][b]}));let b=d[j].filter(b=>a.some(a=>{ac++;return R[i][a][b]}));if(a.length!==d[i].length||b.length!==d[j].length)change=true;d[i]=a;d[j]=b}}
 let A={s:"UNKNOWN",w:null,c:0},B={s:"NO",w:null,c:0},C={s:"UNKNOWN",w:null,c:0};
 if(d.some(x=>!x.length)){A.s="NO";tally.acReject++}else{
 // A: only admit a cycle of partial bijections on the acquired domains
 let maps=[];let ok=true;for(let i=0;i<m;i++){let j=(i+1)%m,mp={};for(let a of d[i]){let v=d[j].filter(b=>{A.c++;return R[i][a][b]});if(v.length!==1)ok=false;else mp[a]=v[0]}if(new Set(Object.values(mp)).size!==d[j].length||Object.keys(mp).length!==d[i].length)ok=false;maps.push(mp)}
 if(ok){A.s="NO";for(let a of d[0]){let w=[a];for(let i=0;i<m-1;i++){A.c++;w.push(maps[i][w[i]])}A.c++;if(maps[m-1][w[m-1]]===a){A={s:"YES",w,c:A.c};break}}}
 }
 // B: global Boolean transfer matrices, path witnesses, independent of A/AC
 for(let a=0;a<q&&!B.w;a++){let paths=Array(q).fill(null);paths[a]=[a];for(let i=0;i<m-1;i++){let next=Array(q).fill(null);for(let u=0;u<q;u++)if(paths[u])for(let v=0;v<q;v++){B.c++;if(R[i][u][v]&&!next[v])next[v]=paths[u].concat(v)}paths=next}for(let v=0;v<q;v++)if(paths[v]){B.c++;if(R[m-1][v][a]){B.s="YES";B.w=paths[v];break}}}
 // C: lexicographic categorical words, no propagation; check actual source via independent forbidden-pair list.
 let w=Array(m).fill(0);while(C.c<cap){C.c++;let valid=true;for(let i=0;i<m&&valid;i++)if(!R[i][w[i]][w[(i+1)%m]])valid=false;if(valid){C.s="YES";C.w=w.slice();break}let i=m-1;while(i>=0&&w[i]===q-1){w[i]=0;i--}if(i<0){C.s="NO";break}w[i]++}
 // Integrated import actual surviving root candidates (or AC domain deletions); reclose via exact transfer on restricted domains.
 // On admitted A result, transfer B's witness/NO cross-check; on UNKNOWN use B. No claim of exclusive synergy.
 let I=A.s==="UNKNOWN"?B:A;for(const l of [A,B,C,I]){assert(l.c<=cap);if(l.s!=="UNKNOWN")assert(l.s===B.s);if(l.w)lift(F,l.w)}
 for(const [k,l] of Object.entries({A,B,C,I}))if(l.s!=="UNKNOWN")tally[k]++;tally[B.s==="YES"?"yes":"no"]++;tally.Achecks+=A.c;tally.Bchecks+=B.c;tally.Cchecks+=C.c;tally.ACchecks+=ac;
 const witness=B.w?lift(F,B.w):null;results.push({m,q,mode,R,N,n:F.rows.length,guardCount:F.guards.length,cap,ac,domainSizes:d.map(a=>a.length),A,B,C,I:I.s,witness})
 }
 for(let m of [3,4,5,6,8,12,16,32,64,128])for(let q of [3,4])for(let mode of ["identity","twist"])run(m,q,mode);
 for(let i=0;i<80;i++)run(3+Math.floor(rnd()*5),3+Math.floor(rnd()*2),"random");
 return {seed:26011632,atomWords,checks,tally,results}
}
console.log(JSON.stringify(audit()));
