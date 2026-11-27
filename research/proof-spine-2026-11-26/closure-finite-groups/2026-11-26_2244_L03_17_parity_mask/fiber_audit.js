function fiberAudit(){
 const key=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(","), A=(v,m)=>{if(!v)throw Error(m)};
 function build(n,b){let e=0,R=Array.from({length:n},()=>[]),H=Array.from({length:n-1},()=>[]);for(let u=0;u<n;u++)for(let h=1;h<n;h++)if((h-u+n)%n<3){R[u].push(++e);H[h-1].push(e)} // independent ordering differs at wrap, restore original edge numbering
 let id=new Map(),i=0;for(let u=0;u<n;u++)for(let d=0;d<3;d++){let h=(u+d)%n;if(h)id.set(`${u}:${h}`,++i)}
 R=Array.from({length:n},(_,u)=>Array.from({length:3},(_,d)=>id.get(`${u}:${(u+d)%n}`)).filter(Boolean));
 H=Array.from({length:n-1},(_,j)=>Array.from({length:n},(_,u)=>id.get(`${u}:${j+1}`)).filter(Boolean));
 let C=R.map(a=>a.slice());for(let s of [...R,...H])for(let j=0;j<s.length;j++)for(let k=j+1;k<s.length;k++)C.push([-s[j],-s[k]]);
 let F=[];const words=(r,p)=>Array.from({length:2**r},(_,z)=>z).filter(z=>z.toString(2).replace(/0/g,"").length%2===p);
 for(let c of C){let lists=c.map(l=>words(b,+(l<0))),out=[[]];for(let j=0;j<c.length;j++){let x=Math.abs(c[j]);out=out.flatMap(a=>lists[j].map(w=>[...a,...Array.from({length:b},(_,t)=>(w>>t&1)?-(t*e+x):t*e+x)]))}F.push(...out)}
 return {F,C,e}
 }
 function collapse(F){let occurrences=new Map(),sets=new Map();F.forEach((c,i)=>{for(let l of c){let v=Math.abs(l);if(!occurrences.has(v))occurrences.set(v,[]);occurrences.get(v).push(i)}});for(let [v,li] of occurrences){let s=li.join(":");if(!sets.has(s))sets.set(s,[]);sets.get(s).push(v)}let block=new Map(),sizes=new Map();for(let a of sets.values()){let r=Math.min(...a);sizes.set(r,a.length);for(let v of a)block.set(v,r)}let fibers=new Map();for(let c of F){let parity=new Map(),seen=new Map();for(let l of c){let r=block.get(Math.abs(l));parity.set(r,(parity.get(r)??0)^(+(l<0)));seen.set(r,(seen.get(r)??0)+1)}for(let [r,s] of seen)A(s===sizes.get(r),"complete block occurrence");let d=[...parity].map(([r,p])=>p?-r:r),k=key(d);if(!fibers.has(k))fibers.set(k,{d,count:0});fibers.get(k).count++}
 for(let {d,count} of fibers.values())if(BigInt(count)!==(1n<<BigInt(d.reduce((t,l)=>t+sizes.get(Math.abs(l))-1,0))))return null;
 return {clauses:[...fibers.values()].map(o=>o.d),blocks:sizes.size,counts:fibers.size}
 }
 let rows=[],checks=0;for(let n of [3,6,12,24,32])for(let b of [1,2,3,4]){let S=build(n,b);let Q=collapse(S.F);A(Q&&Q.blocks===S.e,"fiber blocks");let expected=new Set(S.C.map(key));A(Q.clauses.length===expected.size&&Q.clauses.every(c=>expected.has(key(c))),"fiber quotient");rows.push({n,b,expanded:S.F.length,base:Q.clauses.length,blocks:Q.blocks});checks+=S.F.length}
 let S=build(3,2),shortPins=0; // all assignments to <=2 shares, no unit or conflict
 function rec(start,remaining,p){if(!remaining){for(let c of S.F){if(c.some(l=>p.has(Math.abs(l))&&p.get(Math.abs(l))===+(l>0)))continue;A(c.filter(l=>!p.has(Math.abs(l))).length>=2,"premature unit")}shortPins++;return}for(let v=start;v<=12;v++)for(let bit of [0,1]){p.set(v,bit);rec(v+1,remaining-1,p);p.delete(v)}}
 for(let t=0;t<=2;t++)rec(1,t,new Map());A(collapse(S.F.slice(1))===null,"incomplete fiber accepted");
 return {rows,clauseFibersScanned:checks,shortPinChecks:shortPins,damagedFiberRejected:true}
}
console.log(JSON.stringify(fiberAudit(),null,2));
