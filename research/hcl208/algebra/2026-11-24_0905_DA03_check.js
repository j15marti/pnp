"use strict";
function run(){
 let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const out={seed:20261124,graphs:0,guardCases:0,satGuards:0,unsatGuards:0,modelChecks:0,closureScans:0,rankChecks:0,cutChecks:0,dualChecks:0,removedEdges:0,merges:0,fullGuardWords:0,fanoCounts:[],cascade:null};
 function basis(rows){let b=new Map();for(let x of rows){while(x){let j=x.toString(2).length-1;if(b.has(j))x^=b.get(j);else{b.set(j,x);break}}}return b}
 function rank(rows){out.rankChecks++;return basis(rows).size}
 function parity(x){let z=0;while(x){x&=x-1n;z^=1}return z}
 function obs(e){let [u,v]=e;let d=(1n<<BigInt(2*u))^(1n<<BigInt(2*v));return [d,d<<1n]}
 function val(x,e){let [a,b]=obs(e);return parity(x&a)+2*parity(x&b)}
 function close(edges,guard){let eq=guard.map(a=>a.slice()),active=edges.map((_,i)=>i),removed=[],initial=rank(eq.map(a=>a[0])),history=[];function reduce(x,t){let b=new Map();for(let [y,s] of eq){while(y){let j=y.toString(2).length-1;if(!b.has(j)){b.set(j,[y,s]);break}let q=b.get(j);y^=q[0];s^=q[1]}if(!y&&s)return null}while(x){let j=x.toString(2).length-1;if(!b.has(j))break;let q=b.get(j);x^=q[0];t^=q[1]} // membership needs lower-pivot elimination too
 return [x,t]}
 function query(x){ // row membership via augmented rank; constant from consistent affine system
 let b=new Map();for(let [y,s] of eq){while(y){let j=y.toString(2).length-1;if(!b.has(j)){b.set(j,[y,s]);break}let q=b.get(j);y^=q[0];s^=q[1]}if(!y&&s)throw Error("inconsistent input")}
 let t=0;while(x){let j=x.toString(2).length-1;if(!b.has(j))return null;let q=b.get(j);x^=q[0];t^=q[1]}return t}
 let bad=false;while(true){let found=false;for(let i of active){out.closureScans++;let [a,b]=obs(edges[i]),q=edges[i][2],v=[query(a),query(b),query(a^b)];if(v.every(z=>z===null))continue;let rows=[0,1,2,3].filter(z=>z!==q&&[z&1,z>>1,(z&1)^(z>>1)].every((w,j)=>v[j]===null||w===v[j]));if(!rows.length){bad=true;break}for(let [j,h] of [a,b,a^b].entries()){let bits=rows.map(z=>j===0?z&1:j===1?z>>1:(z&1)^(z>>1));if(bits.every(z=>z===bits[0])&&v[j]===null)eq.push([h,bits[0]])}removed.push(i);active=active.filter(z=>z!==i);history.push(i);found=true;break}if(bad||!found)break}
 let H=removed.flatMap(i=>obs(edges[i])),hr=rank(H),lr=rank(eq.map(a=>a[0])),kr=rank([...guard.map(a=>a[0]),...H]);if(hr>2*initial||kr>2*initial||lr>kr)throw Error("rank budget");out.removedEdges+=removed.length;out.merges+=hr/2;return {bad,eq,active,removed,history,initial,H}}
 function check(n,edges,guard){let R=close(edges,guard);let lhs=0,rhs=0;for(let j=0;j<4**n;j++){let x=BigInt(j);if(!guard.every(([v,t])=>parity(x&v)===t))continue;out.modelChecks++;let a=edges.every(e=>val(x,e)!==e[2]);let b=!R.bad&&R.eq.every(([v,t])=>parity(x&v)===t)&&R.active.every(i=>val(x,edges[i])!==edges[i][2]);if(a!==b)throw Error("model discrepancy");lhs+=+a;rhs+=+b}
 out.guardCases++;out[lhs?"satGuards":"unsatGuards"]++;if(!R.bad){let L=R.eq.map(a=>a[0]);for(let z=0;z<12;z++){let S=R.active.filter(()=>rnd(17)<8),ss=new Set(S),A=S.flatMap(i=>obs(edges[i])),B=R.active.filter(i=>!ss.has(i)).flatMap(i=>obs(edges[i]));let old=rank(A)+rank([...B,...R.H])-rank([...A,...B,...R.H]);let nw=rank([...A,...L])+rank([...B,...L])-rank([...A,...B,...L])-rank(L);if(old>nw+2*R.initial)throw Error("cut budget");out.cutChecks++}}
 return {count:lhs,R}}
 function dual(n,edges){let cols=edges.map(([u,v])=>(1n<<BigInt(u))^(1n<<BigInt(v))),cycles=[];for(let x=1;x<2**edges.length;x++){let t=0n;for(let i=0;i<cols.length;i++)if(x&(1<<i))t^=cols[i];if(!t)cycles.push(BigInt(x))}let cb=[...basis(cycles).values()],cc=cols.map((_,i)=>cb.reduce((a,x,j)=>a|(((x>>BigInt(i))&1n)<<BigInt(j)),0n));for(let j=0;j<20;j++){let S=cols.map((_,i)=>i).filter(()=>rnd(17)<8),ss=new Set(S),T=cols.map((_,i)=>i).filter(i=>!ss.has(i));let w=A=>rank(S.map(i=>A[i]))+rank(T.map(i=>A[i]))-rank(A);if(w(cols)!==w(cc))throw Error("dual width");out.dualChecks++}}
 const K=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)K.push([i,j,0]);
 for(let q=-1;q<K.length;q++){let e=K.filter((_,i)=>i!==q);out.graphs++;dual(5,e);let total=0;for(let bits=0;bits<16;bits++){let g=[];for(let j=1;j<5;j++)g.push([obs([0,j])[0],(bits>>(j-1))&1]);let a=check(5,e,g);total+=a.count;out.fullGuardWords++;if(!a.R.bad&&a.R.active.length)throw Error("full guard not affine")}if(total!==(q<0?0:24))throw Error("K5 count")}
 for(let k=0;k<70;k++){let n=3+rnd(4),e=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rnd(19)<12)e.push([i,j,rnd(4)]);out.graphs++;dual(n,e);check(n,e,[]);for(let z=0;z<4;z++){let g=[],base=BigInt(rnd(4**n)),q=rnd(5);for(let i=0;i<q;i++){let h=BigInt(1+rnd(4**n-1));g.push([h,parity(base&h)])}check(n,e,g)}}
 let e=[[0,1,0],[1,2,0]],g=[[obs(e[0])[0],0],[obs(e[0])[1]^obs(e[1])[0],1]];let a=check(3,e,g);if(a.R.removed.length!==2)throw Error("cascade");out.cascade={initialRank:a.R.initial,removed:a.R.history,finalRank:rank(a.R.eq.map(x=>x[0])),models:a.count};
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 for(let skip=-1;skip<14;skip++){let ct=0;for(let x=0;x<128;x++){let ok=true;for(let i=0;i<7;i++){let t=fano[i].map(v=>(x>>v)&1).reduce((a,b)=>a+b,0);if((t===0&&skip!==2*i)||(t===3&&skip!==2*i+1))ok=false}ct+=+ok}if(ct!==(skip<0?0:5))throw Error("Fano");out.fanoCounts.push(ct)}
 return out;
}
console.log(JSON.stringify(run(),null,2));
