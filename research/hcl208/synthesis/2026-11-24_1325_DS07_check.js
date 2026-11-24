// Reproduce: node 2026-11-24_1325_DS07_check.js
function run(){
  let seed=20807,rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  let stat={rref:0,xors:0,projections:0,closureSweeps:0,pins:0,deletions:0,pairAttempts:0,merges:0,cancellations:0,queries:0,queryTerms:0,referenceWords:0,assertions:0,peakTable:0,retainedKeys:0,witnesses:0};
  function ok(x){stat.assertions++;if(!x)throw Error("assertion "+stat.assertions)}
  function solve(n,events,guard=[],order=null){
    const b=1n<<BigInt(n),mask=b-1n,M=b;
    const bit=i=>1n<<BigInt(i),coeff=r=>r&mask, low=x=>x&(-x);
    function rr(a){stat.rref++;a=a.slice();let k=0;for(let i=0;i<n;i++){let t=bit(i),j=k;while(j<a.length&&!(a[j]&t))j++;if(j===a.length)continue;[a[k],a[j]]=[a[j],a[k]];for(j=0;j<a.length;j++)if(j!==k&&(a[j]&t)){a[j]^=a[k];stat.xors++}k++}if(a.slice(k).some(x=>x===b))return null;return a.slice(0,k)}
    function red(x,A){for(const a of A)if(x&low(coeff(a))){x^=a;stat.xors++}return x}
    function proj(A,U){stat.projections++;let D=new Map(),out=[];for(let a of A){let q=red(coeff(a),U);while(q&&D.has(low(q))){let [v,w]=D.get(low(q));q^=v;a^=w;stat.xors+=2}if(q)D.set(low(q),[q,a]);else out.push(a)}return rr(out)}
    function closure(input,G){G=rr(G);if(!G)return null;let E=input.slice();while(true){stat.closureSweeps++;let norm=[],changed=false;for(let j=0;j<E.length;j++){let a=rr(E[j].map(x=>red(x,G)));if(!a){E.splice(j,1);stat.deletions++;changed=true;break}if(!a.length)return null;if(a.length===1){G=rr([...G,a[0]^b]);stat.pins++;if(!G)return null;E.splice(j,1);changed=true;break}norm.push(a)}if(changed)continue;for(let i=0;i<norm.length&&!changed;i++)for(let j=0;j<norm.length;j++)if(i!==j&&norm[j].every(x=>red(x,norm[i])===0n)){E.splice(i,1);stat.deletions++;changed=true;break}if(changed)continue;return {G,E:norm}}
    }
    const cl=closure(events,guard);if(!cl)return {count:0n,peak:0,work:0};let {G,E}=cl;const U=E.map(a=>rr(a.map(coeff)));let nodes=[],peak=0,work=0;
    function add(t,H,w){if(!w)return;let k=H.join(",");if(t.has(k)){stat.merges++;w+=t.get(k).w}if(w)t.set(k,{H,w});else{t.delete(k);stat.cancellations++}}
    function keep(t){peak=Math.max(peak,t.size);stat.peakTable=Math.max(stat.peakTable,t.size);stat.retainedKeys+=t.size}
    function tree(ids){if(ids.length===1)return ids[0];let k=Math.floor(ids.length/2);return [tree(ids.slice(0,k)),tree(ids.slice(k))]}
    function build(spec){let ids=Array.isArray(spec)?spec.flat(Infinity):[spec], inside=new Set(ids),A=rr(ids.flatMap(i=>U[i])),O=rr(U.flatMap((u,i)=>inside.has(i)?[]:u)),I=proj(A,O),Q=new Map(),T=new Map(),L,R,W;
      if(!Array.isArray(spec)){W=A;add(Q,[],M);add(Q,E[spec],-(M>>BigInt(E[spec].length)))}
      else{L=build(spec[0]);R=build(spec[1]);W=rr([...L.I,...R.I]);for(const a of L.T.values())for(const c of R.T.values()){stat.pairAttempts++;work++;let H=rr([...a.H,...c.H]);if(!H)continue;let o=a.H.length+c.H.length-H.length;let v=a.w*c.w*(1n<<BigInt(o));ok(v%M===0n);add(Q,H,v/M)}}
      for(const a of Q.values())add(T,proj(a.H,I),a.w);keep(Q);keep(T);let node={I,W,Q,T,L,R};nodes.push(node);return node;
    }
    let count,witness;
    if(!E.length){count=M;witness=0n}
    else{let root=build(order??tree(E.map((_,i)=>i)));count=[...root.T.values()].reduce((s,a)=>s+a.w,0n);
      let Pglobal=G.slice();
      function pin(P){let c=closure(events,[...Pglobal,...P]);ok(c!==null);Pglobal=c.G}
      function query(Q,P){stat.queries++;let s=0n;for(const a of Q.values()){stat.queryTerms++;let H=rr([...a.H,...P]);if(!H)continue;let div=1n<<BigInt(H.length-a.H.length);ok(a.w%div===0n);s+=a.w/div}return s}
      function recover(node,P){ok(query(node.Q,P)>0n);for(let a of node.W){let v=red(a,P);if(!coeff(v))continue;let T0=rr([...P,a]);if(T0&&query(node.Q,T0)>0n)P=T0;else{P=rr([...P,a^b]);ok(P&&query(node.Q,P)>0n)}pin(P)}if(node.L){recover(node.L,proj(P,node.L.I));recover(node.R,proj(P,node.R.I))}}
      if(count>0n){recover(root,[]);witness=0n;for(const a of Pglobal)if(a&b)witness|=low(coeff(a));stat.witnesses++}
    }
    if(witness!==undefined){for(const a of G){const p=low(coeff(a));witness&=~p;let v=a&witness, parity=0;while(v){v&=v-1n;parity^=1}if(parity!==Number(!!(a&b)))witness|=p}ok(guard.every(a=>holds(a,witness,b))&&events.every(E=>!E.every(a=>holds(a,witness,b))))}
    let div=1n<<BigInt(G.length);ok(count%div===0n&&count>=0n);return {count:count/div,peak,work};
  }
  function holds(a,x,b){let q=a&x,p=0;while(q){q&=q-1n;p^=1}return p===Number(!!(a&b))}
  function ref(n,E,G=[]){let b=1n<<BigInt(n),s=0n;for(let x=0n;x<b;x++){stat.referenceWords++;if(G.every(a=>holds(a,x,b))&&E.every(e=>!e.every(a=>holds(a,x,b))))s++}return s}
  function word(n,vs,w){return vs.map((v,j)=>(1n<<BigInt(v))|(((w>>j)&1)?1n<<BigInt(n):0n))}
  let groups={cube:{sat:0,unsat:0},fano:{sat:0,unsat:0},random:{sat:0,unsat:0}};
  function test(label,n,E,G=[]){let a=solve(n,E,G),r=ref(n,E,G);ok(a.count===r);groups[label][r?"sat":"unsat"]++}
  for(let s=0;s<256;s++)test("cube",3,Array.from({length:8},(_,i)=>i).filter(i=>(s>>i)&1).map(i=>word(3,[0,1,2],i)));
  const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],F=lines.flatMap(v=>[word(7,v,0),word(7,v,7)]);
  test("fano",7,F);for(let i=0;i<14;i++)test("fano",7,F.filter((_,j)=>i!==j));
  for(let t=0;t<100;t++){let n=3+rand(5),b=1n<<BigInt(n),row=()=>BigInt(1+rand((1<<n)-1))+(rand(2)?b:0n),E=Array.from({length:1+rand(9)},()=>Array.from({length:1+rand(4)},row)),G=Array.from({length:rand(3)},row);test("random",n,E,G)}
  let scales=[];for(let n=3;n<=7;n++){let edges=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)edges.push([u,v]);let m=edges.length,d=n+m,E=edges.map(([u,v],i)=>word(d,[u,v,n+i],0));let r=solve(d,E),expected=0n,c=1n;for(let k=0;k<=n;k++){expected+=c*(1n<<BigInt(m-k*(k-1)/2));if(k<n)c=c*BigInt(n-k)/BigInt(k+1)}ok(r.count===expected);if(n<=4)ok(r.count===ref(d,E));scales.push({n,m,count:String(r.count),peak:r.peak,pairs:r.work})}
  // Exhaust all nontrivial cuts of K5 and independently test signed-key noncancellation.
  let edges=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)edges.push((1<<u)|(1<<v));let cuts=0,minBalanced=Infinity;for(let J=1;J<1023;J++){let a=0,c=0;for(let i=0;i<10;i++)if(J>>i&1)a|=edges[i];else c|=edges[i];let B=a&c,tab=new Map(),seen=new Set();for(let S=J;;S=(S-1)&J){let q=0,k=0;for(let i=0;i<10;i++)if(S>>i&1){q|=edges[i];k++}let p=0;for(let z=q;z;z&=z-1)p++;let key=q&B,w=(k%2?-1n:1n)*(1n<<BigInt(15-k-p));seen.add(key);tab.set(key,(tab.get(key)??0n)+w);if(!S)break}ok([...seen].every(k=>tab.get(k)!==0n));let h=0;for(let z=J;z;z&=z-1)h++;if(h>=4&&h<=6)minBalanced=Math.min(minBalanced,seen.size);cuts++}
  return {groups,scales,cuts,minBalanced,stat,seed:20807};
}
console.log(JSON.stringify(run(),null,2));
