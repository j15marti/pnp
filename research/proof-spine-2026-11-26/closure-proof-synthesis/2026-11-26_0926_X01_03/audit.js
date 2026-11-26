function audit(){
let checks=0, calls=0;const ok=(x,msg)=>{checks++;if(!x)throw Error(msg||`check ${checks}`)};
let seed=20261126;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
const A3=[[1,1,1],[1,0,1],[1,1,0]], A2=[[1,1],[1,1]], P3=[0,2,1];
function pm(A,pins=[]){calls++;let n=A.length,adj=A.map((r,i)=>r.flatMap((v,j)=>v&&pins.every(p=>p.row!==i||+(j<=p.t)===p.val)?[j]:[])),M=Array(n).fill(-1);
 function aug(i,seen){for(let j of adj[i])if(!seen[j]){seen[j]=1;if(M[j]<0||aug(M[j],seen)){M[j]=i;return true}}return false}
 for(let i=0;i<n;i++)if(!aug(i,Array(n).fill(0)))return null;let a=[];M.forEach((i,j)=>a[i]=j);return a
}
function bit(M,p){return +(M[p.row]<=p.t)^p.s}
function solve(I,cap=4096){let {A,P,h}=I,B=A.length,dom=Array(h).fill(3),base=calls;
 function query(b,v,extra=[]){let pins=extra.slice();for(let p of P[b])if(v.has(p.g))pins.push({...p,val:v.get(p.g)^p.s});return pm(A[b],pins)}
 function fixed(){let v=new Map();dom.forEach((d,g)=>{if(d===1||d===2)v.set(g,d===2?1:0)});return v}
 for(;;){let changed=false,v=fixed();
  for(let b=0;b<B;b++){if(!query(b,v))return {answer:"NO",closure:true,calls:calls-base};for(let g of new Set(P[b].map(p=>p.g)))if(dom[g]===3){let d=0;for(let z=0;z<2;z++){let f=new Map(v);f.set(g,z);if(query(b,f))d|=1<<z}
    if(!d)return {answer:"NO",closure:true,calls:calls-base};if(d!==3){dom[g]=d;changed=true;v=fixed()}}}
  if(!changed)break
 }
 const F=fixed(),par=Array.from({length:B+h},(_,i)=>i);function root(x){while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x}
 let K=new Set();for(let b=0;b<B;b++)for(let p of P[b])if(!F.has(p.g)){let u=root(b),v=root(B+p.g);if(u===v)K.add(p.g);else par[u]=v}
 const kk=[...K].sort((a,b)=>a-b),adj=Array.from({length:B+h},()=>[]);
 for(let b=0;b<B;b++)for(let p of P[b])if(!F.has(p.g)&&!K.has(p.g)){adj[b].push(B+p.g);adj[B+p.g].push(b)}
 let seen=new Set(),trees=[];
 function tree(u,parent){ok(!seen.has(u),"forest");seen.add(u);return {u,children:adj[u].filter(w=>w!==parent).map(w=>tree(w,u))}}
 for(let b=0;b<B;b++)if(!seen.has(b))trees.push(tree(b,-1));
 function forest(v){let M=Array(B),all=new Map(v);
  function build(node,parent){let u=node.u,ch=node.children.map(t=>build(t,u)),tab=new Map();
    if(u>=B){for(let z of [0,1])if(ch.every(t=>t.tab.has(z)))tab.set(z,{})}
    else{let b=u;for(let z of parent<0?[-1]:[0,1]){
      if(ch.some(t=>!t.tab.size))continue;let f=new Map(v);if(parent>=0)f.set(parent-B,z);
      for(let t of ch)if(t.tab.size===1)f.set(t.u-B,[...t.tab.keys()][0]);
      let m=query(b,f);if(m){let vals=ch.map(t=>bit(m,P[b].find(p=>p.g===t.u-B)));ok(vals.every((x,i)=>ch[i].tab.has(x)));tab.set(z,{m,vals})}
    }}
    return {u,ch,tab}
  }
  function lift(t,z){let r=t.tab.get(z);ok(!!r);if(t.u>=B){all.set(t.u-B,z);for(let c of t.ch)lift(c,z)}else{M[t.u]=r.m;for(let i=0;i<t.ch.length;i++)lift(t.ch[i],r.vals[i])}}
  for(let t of trees){let T=build(t,-1);if(!T.tab.has(-1))return null;lift(T,-1)}
  for(let b=0;b<B;b++)for(let p of P[b])ok(bit(M[b],p)===all.get(p.g),"guard lift");
  return M
 }
 const reps=kk.map(g=>{for(let b=0;b<B;b++){let p=P[b].find(p=>p.g===g);if(p)return {b,p}}throw Error("missing")});
 let lists=Array.from({length:B},()=>[]),v=new Map(F),states=0,accepted=0,witness=null,overflow=false;
 function visit(i){if(overflow)return;if(i===kk.length){states++;if(states>cap){overflow=true;return}let M=forest(v);if(M){accepted++;witness=M}return}
  let {b,p}=reps[i];for(let z of [0,1]){lists[b].push({...p,val:z^p.s});if(query(b,F,lists[b])){v.set(kk[i],z);visit(i+1);v.delete(kk[i])}lists[b].pop();if(overflow)break}
 }
 visit(0);return {answer:witness?"YES":overflow?"UNKNOWN":"NO",h:kk.length,states,accepted,overflow,pins:F.size,calls:calls-base,M:witness}
}
function perm(A){let out=[],n=A.length;function go(v,S){if(v.length===n){out.push(v.slice());return}for(let j=0;j<n;j++)if(A[v.length][j]&&!S.has(j)){S.add(j);v.push(j);go(v,S);v.pop();S.delete(j)}}go([],new Set());return out}
function ref(I){let L=I.A.map(perm),v=new Map();function go(b){if(b===L.length)return true;for(let m of L[b]){let f=new Map(v),valid=true;for(let p of I.P[b]){let x=bit(m,p);if(f.has(p.g)&&f.get(p.g)!==x){valid=false;break}f.set(p.g,x)}if(valid){let old=v;v=f;if(go(b+1))return true;v=old}}return false}return go(0)}
function verifyGrid(I,M){let off=0,sel=[],A=[];for(let b=0;b<I.A.length;b++){let n=I.A[b].length;for(let i=0;i<n;i++){sel.push(off+M[b][i]);A.push([b,off,i,n])}off+=n}
 let inv=[];sel.forEach((j,i)=>inv[j]=i);ok(new Set(sel).size===off);
 for(let i=0;i<off;i++)for(let j=0;j<off;j++){let [b,o,r,n]=A[i],a=j>=o&&j<o+n&&I.A[b][r][j-o],N=+(inv[j]<i),E=+(sel[i]<=j),S=+(inv[j]<=i),W=+(sel[i]<j);ok((E===W&&S===N)||(a&&N===0&&E===1&&S===1&&W===0),"grid cell")}
 return off
}
function star(h,unsat){let n=h+1,A=[Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===0||j===0||i===j)))],P=[Array.from({length:h},(_,g)=>({g,row:g+1,t:0,s:0}))];
 for(let i=0;i<h;i+=2){A.push(A3);let j=i/2;P.push([{g:i,row:P3[0],t:0,s:j===0||j===1&&unsat?1:0},{g:i+1,row:P3[1],t:0,s:j<2?1:0}])}return {A,P,h}}
let random={yes:0,no:0,unknown:0,closures:0};
for(let t=0;t<180;t++){let B=2+rnd(4),h=2+rnd(5),A=[],P=[];for(let b=0;b<B;b++){let n=2+rnd(2);A.push(Array.from({length:n},()=>Array.from({length:n},()=>+(rnd(5)!==0))));P.push(Array.from({length:n},(_,row)=>({g:rnd(h),row,t:0,s:rnd(2)})))}let I={A,P,h},r=solve(I);let y=ref(I);ok(r.answer==="YES"===y);ok(r.answer!=="UNKNOWN");random[y?"yes":"no"]++;if(r.closure)random.closures++;if(y)verifyGrid(I,r.M)}
let scales=[];
for(let h of [4,8,16,32,64,128]){let Y=star(h,false),U=star(h,true),a=solve(Y,h+1),b=solve(U,h+1);
 ok(a.answer==="YES"&&b.answer==="NO");ok(a.pins===0&&b.pins===0&&!b.closure);ok(a.h===h/2&&b.h===h/2);ok(a.states===h/2+1&&b.states===h/2+1);let side=verifyGrid(Y,a.M);
 scales.push({guards:h,feedback:a.h,candidates:a.states,acceptedYes:a.accepted,acceptedNo:b.accepted,yesCalls:a.calls,noCalls:b.calls,side,cells:side*side});
}
let capped=solve(star(16,true),2);ok(capped.answer==="UNKNOWN"&&capped.overflow);
let gadget=perm(A3);ok(gadget.length===3&&gadget.every((v,i)=>P3.every((r,j)=>+(v[r]===0)===+(i===j))));
return {checks,matchingCalls:calls,random,scales,capped:{answer:capped.answer,states:capped.states,cap:2},gadget,seed:20261126}
}
console.log(JSON.stringify(audit(),null,2));
