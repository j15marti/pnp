'use strict';
function main(){
 const stats={checks:0,gauss:0,xors:0,closureScans:0,forcedRows:0,compiled:0,declined:0,pieces:0,pairProjections:0,fibers:0,sat:0,unsat:0,lifts:0,strictStarts:0,collisionStarts:0,conditionalEvaluations:0,referenceWords:0};
 const check=(x,msg)=>{stats.checks++;if(!x)throw Error(msg)};
 const bit=i=>1n<<BigInt(i), low=n=>bit(n)-1n;
 const parity=x=>{let v=0;while(x){x&=x-1n;v^=1}return v};
 const eq=(rows,x)=>rows.every(([a,b])=>parity(a&x)===b);
 function gauss(rows,n){
  stats.gauss++;let basis=Array(n).fill(null);
  for(let [a,b] of rows){while(a){let j=a.toString(2).length-1;if(j>=n)throw Error("bad mask");if(!basis[j]){basis[j]=[a,b];break}a^=basis[j][0];b^=basis[j][1];stats.xors++}if(!a&&b)return null}
  let x=0n;for(let j=0;j<n;j++)if(basis[j]&&parity(basis[j][0]&x)!==basis[j][1])x|=bit(j);
  return {rows:basis.filter(Boolean),rank:basis.filter(Boolean).length,x};
 }
 const project=(rows,z,p)=>{let g=gauss(rows,z+p);return g?g.rows.filter(([a])=>a<=low(z)):null};
 function closure(packets,n,initial=[]){
  let H=initial.slice();
  restart:while(true){stats.closureScans++;let g=gauss(H,n);if(!g)return null;H=g.rows;
   for(let P of packets){let q=gauss(H.concat(P),n);if(!q)continue;if(q.rank===g.rank)return null;
    if(q.rank===g.rank+1){for(let [a,b] of P){let r=gauss(H.concat([[a,b]]),n);if(r&&r.rank>g.rank){H.push([a,1^b]);stats.forcedRows++;continue restart}}throw Error("no independent row")}
   }return H;
  }
 }
 function compile(packets,z,p){
  // Certified root local affine closure; its rows are retained as metadata.
  let closed=closure(packets,z+p);
  let cap=bit(p),B=0n;for(let P of packets){let g=gauss(P.map(([a])=>[a>>BigInt(z),0]),p);B+=bit(p-g.rank)}
  if(B>cap){stats.declined++;return null}
  let pieces=[];stats.compiled++;
  if(closed===null) return {pieces,closed,B};
  if(B<cap)pieces.push([]);
  else{
   for(let P of packets){let a=project(P,z,p);if(a===null)pieces.push([]);else for(let [v,b] of a)pieces.push([[v,1^b]])}
   for(let i=0;i<packets.length;i++)for(let j=0;j<i;j++){stats.pairProjections++;let a=project(packets[i].concat(packets[j]),z,p);if(a!==null)pieces.push(a)}
  }
  stats.pieces+=pieces.length;return {pieces,closed,B};
 }
 function fix(P,z,x){return P.map(([a,b])=>[a>>BigInt(z),b^parity(a&x)])}
 function lift(packets,z,p,x){
  let Ps=packets.map(P=>fix(P,z,x));let H=closure(Ps,p);if(H===null)return null;
  let den=bit(p),prefix=[],count=0;
  const size=(P,pre)=>{let g=gauss(P.concat(pre),p);return g?bit(p-g.rank):0n};
  const mass=pre=>{stats.conditionalEvaluations++;let sum=0n;for(let P of Ps)sum+=size(P,pre);return sum};
  let m=mass(prefix);
  if(m>den)throw Error("unqualified lift");
  if(m===den){let hit=null;
   outer:for(let i=0;i<Ps.length;i++)for(let j=0;j<i;j++){let g=gauss(Ps[i].concat(Ps[j]),p);if(g){hit=g.x;break outer}}
   if(hit===null)return null;stats.collisionStarts++;
   for(let j=0;j<p;j++){let v=Number((hit>>BigInt(j))&1n),same=prefix.concat([[bit(j),v]]);let half=den>>1n;
    if(mass(same)>half){prefix=prefix.concat([[bit(j),1^v]]);den=half;count=j+1;break}
    prefix=same;den=half;
   }check(mass(prefix)<den,"strict sibling exists");
  }else stats.strictStarts++;
  // Prefix choices are witness construction, not globally forced deductions.
  for(let j=count;j<p;j++){let zero=prefix.concat([[bit(j),0]]);let half=den>>1n;prefix=mass(zero)<half?zero:prefix.concat([[bit(j),1]]);den=half}
  let y=gauss(prefix,p).x;check(Ps.every(P=>!eq(P,y)),"bad lift");check(eq(H,y),"lost forced row");stats.lifts++;return y;
 }
 function audit(packets,z,p){
  let C=compile(packets,z,p);check(C!==null,"expected eligible");
  let yes=0,no=0;
  for(let x=0n;x<bit(z);x++){stats.fibers++;let expected=false;
   for(let y=0n;y<bit(p);y++){stats.referenceWords++;if(packets.every(P=>!eq(P,x|(y<<BigInt(z)))))expected=true}
   let got=C.pieces.some(P=>eq(P,x));check(got===expected,"projection disagreement");let y=lift(packets,z,p,x);check((y!==null)===expected,"lift decision disagreement");
   if(got){yes++;stats.sat++;check(eq(C.closed,x|(y<<BigInt(z))),"global closure lost witness")}else{no++;stats.unsat++}
  }return {yes,no};
 }
 let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const native=(signs,eta)=>{let z=6;return [[0,signs&1],[0,(signs&1)^2],[2,((signs>>1)&1)^1],[4,((signs>>2)&1)^3^(eta*2)]].map(([o,s])=>[[bit(z)|bit(o),s&1],[bit(z+1)|bit(o+1),(s>>1)&1]])};
 let nativeResults=[];for(let s=0;s<8;s++)for(let e=0;e<2;e++){let P=native(s,e),r=audit(P,6,2),C=compile(P,6,2);for(let x=0n;x<64n;x++){let a=Number(x&3n),b=Number((x>>2n)&3n),c=Number((x>>4n)&3n);let active=((a^(s&1))&1)===((b^((s>>1)&1))&1)&&((a^(s&1))&1)===((c^((s>>2)&1))&1);let pred=!active||(((b>>1)^(c>>1))===(1^e));check(C.pieces.some(Q=>eq(Q,x))===pred,"BW13 star formula")}nativeResults.push(r)}
 let random=[];for(let t=0;t<120;t++){let z=1+rnd(4),p=2+rnd(5),r=1+rnd(Math.min(p,3)),m=1+rnd(1<<r),P=[];for(let i=0;i<m;i++){let A=[];for(let j=0;j<r;j++){let v=bit(z+j)|(BigInt(rnd(1<<(p-r)))<<BigInt(z+r))|BigInt(rnd(1<<z));A.push([v,rnd(2)])}if(rnd(3)===0)A.push([BigInt(rnd(1<<z)),rnd(2)]);P.push(A)}random.push(audit(P,z,p))}
 // NAE and single-budget Fano controls, exact independent private centers.
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function owner(v,s,budget=-1){let [a,b,c]=v,z=7;let fixed=[0,1,2].map(w=>[[bit(z),w&1],[bit(z+1),(w>>1)&1]]);
  if(budget>=0){let bad=[[bit(z),1],[bit(z+1),1],...v.map(i=>[bit(i),budget])];return fixed.concat([bad])}
  return fixed.concat([[[bit(z)|bit(a)|bit(b),1^(s&1)^((s>>1)&1)],[bit(z+1)|bit(a)|bit(c),1^(s&1)^((s>>2)&1)]]]);
 }
 let fano=[];
 for(let type of ["root","sign","budget"]){let lim=type==="root"?1:type==="sign"?21:14;for(let j=0;j<lim;j++){
  let P=F.map((v,i)=>owner(v,type==="sign"&&Math.floor(j/3)===i?1<<(j%3):0,type==="budget"&&Math.floor(j/2)===i?j%2:-1));
  let C=P.map(Q=>compile(Q,7,2)),models=0;for(let x=0n;x<128n;x++){let expected=F.every((v,i)=>{let w=v.map((u,k)=>Number((x>>BigInt(u))&1n)^(type==="sign"&&Math.floor(j/3)===i&&j%3===k?1:0));return type==="budget"&&Math.floor(j/2)===i?!w.every(b=>b===j%2):!w.every(b=>b===w[0])});let got=C.every(Q=>Q.pieces.some(R=>eq(R,x)));check(got===expected,"Fano projection");if(got){models++;for(let Q of P)check(lift(Q,7,2,x)!==null,"Fano lift")}}
  check(models===(type==="root"?0:type==="sign"?10:5),"Fano count");fano.push({type,j,models});
 }}
 // Above-budget collision is not sufficient (same private halfspace twice + opposite halfspace).
 const hostile=[[[1n,0]],[[1n,0]],[[1n,1]]];check(compile(hostile,0,1)===null,"must decline overbudget");check([0n,1n].every(y=>hostile.some(P=>eq(P,y))),"hostile UNSAT");
 // 64-bit private domain, 48-bit exterior guard, two rank-one halves.
 // Packet 2 active only when z=0; both active and disjoint => rejection.
 let z=48,p=64;let P=[[[bit(z),0]],[[bit(z),1],...Array.from({length:z},(_,i)=>[bit(i),0])]];
 let C=compile(P,z,p),scaling=[];
 for(let x of [0n,1n,bit(47),low(z)]){let got=C.pieces.some(Q=>eq(Q,x));check(got===(x!==0n),"dense guard");let y=lift(P,z,p,x);check((y!==null)===got,"dense lift");scaling.push({guard:x.toString(),sat:got})}
 return {seed:20261124,stats,nativeResults,random,fano,scaling,hostile:"declined; independently UNSAT"};
}
console.log(JSON.stringify(main(), null, 2));
