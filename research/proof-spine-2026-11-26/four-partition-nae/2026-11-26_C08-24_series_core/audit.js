function audit(){
 const out={version:"C08-24",tests:[],controls:{},counts:{checks:0,words:0,clauses:0,steps:0},cap:2000000};const rng=n=>Array.from({length:n},(_,i)=>i);
 function ck(x,m){out.counts.checks++;if(!x)throw Error(m);if(Object.values(out.counts).reduce((a,b)=>a+b,0)>out.cap)throw Error("cap")}
 const ag=[...rng(3).map(r=>rng(3).map(c=>3*r+c)),...rng(3).map(c=>rng(3).map(r=>3*r+c)),...rng(3).map(k=>rng(3).map(r=>3*r+(r+k)%3)),...rng(3).map(k=>rng(3).map(r=>3*r+(k-r+3)%3))];
 function normalize(v,arcs){let m=new Map();for(let [w,p] of arcs){if(w===v){if(p===0)return null;continue}if(m.has(w)&&m.get(w)!==p)return null;m.set(w,p)}return [...m]}
 function reduce(rows,protectedSet,order){
   let m=new Map(rows.map(([v,a])=>[v,normalize(v,a)])),log=[];
   for(let [v,a] of m)if(a===null)m.delete(v);else if(!a.length)return {no:true,rows:[],log};
   for(let v of order){if(protectedSet.has(v))continue;
     let pred=[...m].filter(([p,a])=>p!==v&&a.some(([w])=>w===v));if(pred.length>1)continue;
     let a=m.get(v); if(a&&a.length===0)return {no:true,rows:[],log};
     if(pred.length===1){let [p,b]=pred[0];let e=b.find(([w])=>w===v)[1];let c=a===undefined?null:normalize(p,[...b.filter(([w])=>w!==v),...a.map(([w,t])=>[w,e^t])]);if(c===null)m.delete(p);else if(!c.length)return {no:true,rows:[],log};else m.set(p,c)}
     m.delete(v);log.push(v);out.counts.steps++;
   }return {no:false,rows:[...m],log}
 }
 function valid(rows,bit){return rows.every(([v,a])=>a.some(([w,p])=>(bit(v)^bit(w))===p))}
 function support(rows,B,I){let outa=[];for(let w=0;w<2**B.length;w++){let ok=false;for(let z=0;z<2**I.length;z++){out.counts.words++;let bit=v=>B.includes(v)?(w>>B.indexOf(v))&1:(z>>I.indexOf(v))&1;if(valid(rows,bit)){ok=true;break}}outa.push(ok)}return outa}
 // Separate direct truth, path composition, and adversarial control on the prior two-entry SCC.
 let ring=rng(4).map(i=>[i,[[(i+1)%4,1],[4+i,1]]]),B=[0,1,4,5,6,7],I=[2,3];
 let table=support(ring,B,I),macro=reduce(ring,new Set(B),I),compressed=support(macro.rows,B,[]);
 ck(table.every((v,i)=>v===compressed[i]),"two-entry exact");ck(table.filter(x=>!x).length===18,"18 forbidden");ck(macro.rows.length===2,"two rows");
 out.controls.twoEntry={rows:ring,boundary:B,eliminated:I,macro:macro.rows,forbidden:table.flatMap((x,i)=>x?[]:[i])};
 // Bounded arbitrary unique-predecessor local rule, signs, tautology, self-composition.
 let seed=987123;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 let admitted=0;
 for(let t=0;t<600;t++){
   let rs=[[0,[[1,rnd(2)],[2,rnd(2)]]],[1,Array.from({length:1+rnd(3)},()=>[rnd(5),rnd(2)])]];
   // additional owner never mentions eliminated v=1
   if(rnd(2))rs.push([3,[[0,rnd(2)],[4,rnd(2)]]]);
   let b=[0,2,3,4],i=[1],r=reduce(rs,new Set(b),i),orig=support(rs,b,i),next=r.no?orig.map(()=>false):support(r.rows,b,[]);
   ck(orig.every((v,j)=>v===next[j]),"local relation "+JSON.stringify(rs));admitted++;
 }
 out.controls.localCases=admitted;
 // Hostile: two predecessors demand opposite v. Owner v tautological from opposite fixed exit values.
 let hostile=[[0,[[1,0]]],[2,[[1,0]]],[1,[[3,0],[4,0]]]],hb=[0,2,3,4],hword=2|8;
 let htab=support(hostile,hb,[1]);ck(htab[hword]===false,"opposing demands");ck(reduce(hostile,new Set(hb),[1]).log.length===0,"reject multi pred");
 out.controls.multiPredecessor={rows:hostile,boundary:hb,forbiddenWord:hword};
 function complete(n,partial){
   let rows=[],colors=[],mask=new Uint8Array(n),alpha=[0,2,3,1],pairs=new Set(),seen=new Uint8Array(12*n*4);
   function add(row,c){ck(new Set(row).size===3,"distinct");for(let v of row){ck(!seen[4*v+c],"partition conflict");seen[4*v+c]=1}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=Math.min(row[i],row[j]),b=Math.max(row[i],row[j]),k=a+":"+b;ck(!pairs.has(k),"linearity");pairs.add(k)}rows.push(row);colors.push(c);out.counts.clauses++}
   for(let [r,c] of partial){for(let v of r){ck(!(mask[v]&(1<<c)),"partial partition");mask[v]|=1<<c}for(let t=0;t<12;t++)add(r.map(v=>t*n+v),c)}
   for(let v=0;v<n;v++)for(let c=0;c<4;c++)if(!(mask[v]&(1<<c)))for(let j=0;j<4;j++)add([j*n+v,(4+(j^c))*n+v,(8+(j^alpha[c]))*n+v],c);
   ck(seen.every(x=>x===1),"all perfect");return {rows,colors}
 }
 for(let L of [1,2,4,8,16,32]){
   let len=8*L,free=9*len,n=2*free,partial=[],pins={},rows=[],entry=new Set(),cores=[];
   for(let v=0;v<9;v++)for(let i=0;i<len;i++){let a=v*len+i,b=v*len+(i+1)%len,p=free+a;partial.push([[a,b,p],i%2]);pins[p]=1^(i%2);rows.push([a,[[b,1],[p,1]]]);entry.add(p)}
   ag.forEach((r,j)=>{let c=Math.floor(j/3),rr=r.map(v=>v*len+2*L*c);rr.forEach(v=>entry.add(v));cores.push(rr);partial.push([rr,2])});
   let native=complete(n,partial);
   // Track B: independent binary implication closure: y_i=x_i xor parity(i), pins force y_i=>y_i+1; all cycle entries same.
   let localChecks=0;for(let i=0;i<2;i++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){let p=1^i,x=a^i,y=b^(1^i);ck((!(x===y&&y===p))===(!a||!!b),"gauge implication");localChecks++}
   // Track A: series elimination independent of implication reasoning.
   let red=reduce(rows,new Set(entry),rng(free));ck(!red.no,"no local refutation");ck(red.rows.length===36,"36 macros");
   ck(red.log.length===free-36,"all interior removed");
   // Evaluate each macro for all endpoint phase pairs, fixed pins; must yield the implication exactly.
   for(let [v,a] of red.rows){let base=Math.floor(v/len)*len,expected=base+(v-base+2*L)%len;
     for(let x=0;x<2;x++)for(let y=0;y<2;y++){let bit=w=>w===v?x:w===expected?y:pins[w];ck(a.every(([w])=>w===expected||w in pins),"macro scope");ck(valid([[v,a]],bit)===(!x||!!y),"macro implication")}
   }
   // Track C: direct AG9 truth (same original owner IDs under phase map), independent pair count.
   let sat=0,min=100;for(let w=0;w<512;w++){out.counts.words++;let bit=v=>(w>>v)&1;
     let eq=0;for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)if(bit(i)===bit(j))eq++;
     min=Math.min(min,eq);if(ag.every(r=>r.some(v=>bit(v)!==bit(r[0]))))sat++;
   }ck(sat===0&&min===16,"AG9 NO");
   // On first instance exact boundary support of one whole ring, all 16 entry words x 16 interior words.
   if(L===1){let b=[0,2,4,6],i=[1,3,5,7],t=rows.slice(0,len);let btab=[];for(let w=0;w<16;w++){let ok=false;for(let z=0;z<16;z++){out.counts.words++;let bit=v=>v>=free?pins[v]:b.includes(v)?(w>>b.indexOf(v))&1:(z>>i.indexOf(v))&1;if(valid(t,bit)){ok=true;break}}btab.push(ok)}ck(btab.every((x,i)=>x===(i===0||i===15)),"full ring support")}
   out.tests.push({L,nativeVariables:12*n,nativeOwners:native.rows.length,encodedJSONBytes:JSON.stringify({rows:native.rows,partitions:native.colors,guard:pins}).length,projectedFree:free,protectedFree:36,eliminated:red.log.length,remainingMacros:red.rows.length,unmatchedOwners:12,coreVariables:9,coreCount:sat,minEqualPairs:min,guard:pins,sourceDescription:"deterministic generator; physical IDs t*n+v; core owner IDs after cycle rows; guard on t=0",sampleMacro:red.rows[0]});
 }
 return out;
}
console.log(JSON.stringify(audit(),null,2));
