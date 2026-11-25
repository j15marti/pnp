function BD11(){
 const stats={assertions:0,gauss:0,counts:0,termPairs:0,augmentations:0,exchangeTests:0,closurePins:0,closureScans:0,coreRounds:0,referenceWords:0,lifts:0,subsetAudits:0};
 const ok=(x,m)=>{stats.assertions++;if(!x)throw Error(m)};
 const parity=x=>{let p=0n;while(x){p^=1n;x&=x-1n}return Number(p)};
 function rr(n,rows){stats.gauss++;let a=rows.map(r=>r.slice()),k=0,p=[];for(let j=n-1;j>=0;j--){let bit=1n<<BigInt(j),i=a.findIndex((r,i)=>i>=k&&(r[0]&bit)!==0n);if(i<0)continue;[a[k],a[i]]=[a[i],a[k]];for(let l=0;l<a.length;l++)if(l!==k&&(a[l][0]&bit)){a[l][0]^=a[k][0];a[l][1]^=a[k][1]}p.push(j);k++}return a.slice(k).some(r=>r[1])?null:{rows:a.slice(0,k),p}}
 const size=(n,g)=>{let r=rr(n,g);return r?1n<<BigInt(n-r.p.length):0n};
 const rank=(n,a)=>rr(n,a.map(x=>[x,0])).p.length;
 function nullspace(n,rows){let r=rr(n,rows.map(a=>[a,0])),out=[];for(let j=0;j<n;j++)if(!r.p.includes(j)){let v=1n<<BigInt(j);r.rows.forEach(([a],i)=>{if(parity(a&v))v^=1n<<BigInt(r.p[i])});out.push(v)}return out}
 const holds=(g,x)=>g.every(([a,b])=>parity(a&x)===b);
 const value=(f,x)=>f.reduce((s,t)=>s+(holds(t.g,x)?t.c:0n),0n);
 const term=(c,g=[])=>({c:BigInt(c),g});
 function count(n,f,g){stats.counts++;return f.reduce((s,t)=>s+t.c*size(n,[...g,...t.g]),0n)}
 function verify(n,f){let a=count(n,f,[]),b=0n;for(let t of f)for(let u of f){stats.termPairs++;b+=t.c*u.c*size(n,[...t.g,...u.g])}return a===b}
 const complement=f=>[term(1),...f.map(t=>term(-t.c,t.g))];
 function witness(n,f,g){if(count(n,f,g)===0n)return null;let h=g.slice(),x=0n;for(let j=0;j<n;j++){let a=1n<<BigInt(j),b=count(n,f,[...h,[a,0]])===0n?1:0;h.push([a,b]);if(b)x|=a}return x}
 function hull(n,f,g){let a=witness(n,f,g);if(a===null)return null;let dif=[];for(;;){let eq=nullspace(n,dif).map(v=>[v,parity(v&a)]),found=false;for(let [v,b] of eq){let h=[...g,[v,1-b]];if(count(n,f,h)>0n){let x=witness(n,f,h);dif.push(x^a);found=true;break}}if(!found)return eq}}
 function closure(n,fs,g){g=g.slice();for(;;){let r=rr(n,g);if(!r)return null;g=r.rows;let changed=false;for(let f of fs){stats.closureScans++;let h=hull(n,f,g);if(h===null)return null;let z=rr(n,[...g,...h]);if(!z)return null;if(z.rows.length>g.length){stats.closurePins+=z.rows.length-g.length;g=z.rows;changed=true;break}}if(!changed)return g}}
 function match(n,hs,ids,base){let M=new Map(),r0=rank(n,base);for(;;){let q=ids.filter(i=>!M.has(i)),seen=new Set(q),prev=new Map(),end=null;for(let t=0;t<q.length&&!end;t++){let i=q[t];for(let row of hs[i]){let a=row[0],entries=[...M.entries()];stats.exchangeTests++;if(rank(n,[...base,...entries.map(e=>e[1][0]),a])===r0+M.size+1){end=[i,row];break}for(let [j] of entries){if(seen.has(j))continue;stats.exchangeTests++;if(rank(n,[...base,...entries.filter(e=>e[0]!==j).map(e=>e[1][0]),a])===r0+M.size){seen.add(j);q.push(j);prev.set(j,[i,row])}}}}if(!end)return {M,core:[...seen].sort((a,b)=>a-b)};let [i,row]=end;M.set(i,row);while(prev.has(i)){[i,row]=prev.get(i);M.set(i,row)}stats.augmentations++;ok(rank(n,[...base,...[...M.values()].map(r=>r[0])])===r0+M.size,"augmentation independence")}}
 const scope=f=>f.flatMap(t=>t.g.map(r=>r[0]));
 function peel(n,fs,g,W){for(let f of fs)ok(verify(n,f),"Boolean packet validation");g=closure(n,fs,g);if(g===null)return {g:null};let hs=fs.map(f=>hull(n,complement(f),g)),ids=hs.map((h,i)=>h===null?-1:i).filter(i=>i>=0),S=[],rounds=[];for(;;){stats.coreRounds++;let base=[...g.map(r=>r[0]),...W,...S.flatMap(i=>scope(fs[i]))],a=match(n,hs,ids.filter(i=>!S.includes(i)),base);if(!a.core.length)return {g,S,hs,ids,M:a.M,rounds};rounds.push(a.core);S.push(...a.core);S.sort((a,b)=>a-b)}}
 function lift(n,fs,W,p,x){let rows=[...p.g,...W.map(a=>[a,parity(a&x)]),...p.S.flatMap(i=>scope(fs[i]).map(a=>[a,parity(a&x)])),...[...p.M.values()].map(([a,b])=>[a,1-b])];let r=rr(n,rows);ok(!!r,"lift exists");let y=0n;r.rows.forEach((row,i)=>{if(row[1])y|=1n<<BigInt(r.p[i])});ok(holds(p.g,y)&&W.every(a=>parity(a&y)===parity(a&x))&&fs.every(f=>value(f,y)===1n),"lift correct");stats.lifts++;return y}
 function audit(n,fs,g,W){let p=peel(n,fs,g,W),orig=new Set(),red=new Set(),lab=x=>W.map(a=>parity(a&x)).join("");for(let x=0n;x<(1n<<BigInt(n));x++){stats.referenceWords++;if(holds(g,x)&&fs.every(f=>value(f,x)===1n))orig.add(lab(x));if(p.g&&holds(p.g,x)&&p.S.every(i=>value(fs[i],x)===1n)){red.add(lab(x));lift(n,fs,W,p,x)}}ok(orig.size===red.size&&[...orig].every(x=>red.has(x)),"fiber equivalence");if(p.g&&p.ids.length<=9){let ids=p.ids;for(let mask=0;mask<1<<ids.length;mask++){let S=ids.filter((_,j)=>mask>>j&1),base=[...p.g.map(r=>r[0]),...W,...S.flatMap(i=>scope(fs[i]))],outside=ids.filter(i=>!S.includes(i)); // independent exhaustive Hall criterion (not matching)
 let feasible=true,rb=rank(n,base);for(let k=1;k<1<<outside.length;k++){let J=outside.filter((_,j)=>k>>j&1);stats.subsetAudits++;if(rank(n,[...base,...J.flatMap(i=>p.hs[i].map(r=>r[0]))])-rb<J.length){feasible=false;break}}
 if(feasible)ok(p.S.every(i=>S.includes(i)),"minimal fixed point")}}
 return {sat:orig.size>0,retained:p.S?.length??null,rounds:p.rounds??[]}}
 const bit=i=>1n<<BigInt(i),point=(coords,x)=>coords.map((i,j)=>[bit(i),x>>j&1]);
 const badPoints=(coords,words)=>[term(1),...words.map(x=>term(-1,point(coords,x)))];
 const rejection=g=>[term(1),term(-1,g)];
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const fano=triples.map(([a,b,c])=>rejection([[bit(a)^bit(b),0],[bit(a)^bit(c),0]]));
 let fanoTests=[];for(let i=-1;i<14;i++){let fs=fano.slice();if(i>=0){let e=Math.floor(i/2),t=triples[e];fs[e]=rejection(point(t,i%2?7:0))}fanoTests.push(audit(7,fs,[],[]));ok(fanoTests.at(-1).sat===(i>=0),"Fano label")}
 let hostile=[badPoints([0,1,2],[2,4,6]),badPoints([0,1,2],[3,5,7]),badPoints([0,1,2],[0,1,4])];
 let h=audit(3,hostile,[],[]);ok(!h.sat&&h.retained===3&&h.rounds.length===2,"hostile cascade");let neighbor=hostile.slice();neighbor[2]=badPoints([0,1,2],[1,4]);let hn=audit(3,neighbor,[],[]);ok(hn.sat,"hostile neighbor");
 let seed=2081124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 let random={sat:0,unsat:0,removed:0};for(let t=0;t<90;t++){let n=5,fs=[];for(let i=0;i<1+rnd(6);i++){let c=[];while(c.length<3){let j=rnd(n);if(!c.includes(j))c.push(j)}let w=[];for(let x=0;x<8;x++)if(rnd(3)===0)w.push(x);fs.push(badPoints(c,w))}let g=t%3===0?[[bit(rnd(n)),rnd(2)]]:[],W=t%2===0?[bit(rnd(n))]:[];let r=audit(n,fs,g,W);random[r.sat?"sat":"unsat"]++;if(r.retained!==null)random.removed+=fs.length-r.retained}
 let scaling=[];for(let k of [1,4,12,32]){let n=7+k,tail=Array.from({length:k},(_,i)=>badPoints([7+i,0,1],[0,2,4]));for(let relax of [false,true]){let fs=[...fano,...tail];if(relax)fs[0]=rejection(point(triples[0],0));let p=peel(n,fs,[],[]);ok(p.g!==null&&p.S.length===(relax?0:7),"scaling core");if(relax)lift(n,fs,[],p,0n);scaling.push({k,relax,retained:p.S.length,rounds:p.rounds.length})}}
 let invalid=[term(2,[[1n,0]])];ok(!verify(1,invalid),"nonboolean decline");
 return {seed:2081124,fanoTests,hostile:h,hostileNeighbor:hn,random,scaling,stats};
}
console.log(JSON.stringify(BD11(),null,2));
