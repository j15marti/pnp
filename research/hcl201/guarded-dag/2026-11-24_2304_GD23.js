// Node >=18. Run: node GD23.js <immutable BS16 JSON path>
function experiment(hostile){
 const owner=(p,t,bad=[0,7])=>({p,t,bad});
 function ring(q){let L=12*q,O=[];for(let i=0;i<L;i++)for(let j=0;j<3;j++)O.push(owner((i+j)%3,[3*i+j,3*((i+1)%L)+j,3*((i+1)%L)+(j+1)%3]));for(let b=0;b<q;b++)for(let j=0;j<3;j++){let T=j===2?[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]:[[0,2,5],[1,3,8],[4,7,10],[6,9,11]];if(!b&&!j)T=[[0,4,8],[1,3,6],[2,9,11],[5,7,10]];for(let t of T)O.push(owner(3,t.map(i=>3*(12*b+i)+j)));}return {n:3*L,O};}
 function plane(){let O=[];for(let i=0;i<3;i++)O.push(owner(0,[3*i,3*i+1,3*i+2]));for(let d=0;d<3;d++)for(let b=0;b<3;b++)O.push(owner(d+1,[b,3+(b+d)%3,6+(b+2*d)%3]));return {n:9,O};}
 const F={n:7,O:['012','034','056','135','146','236','245'].map(t=>owner(-1,[...t].map(Number)))};
 let checks=0;function check(b){checks++;if(!b)throw Error("assert "+checks);}
 function legal(O,x,pin){return (pin<0||x[0]===pin)&&O.every(o=>!o.bad.includes(o.t.reduce((m,v,j)=>m+(x[v]<<j),0)));}
 function solve(n,O,pin,mode,cap=1000000){
   let S={nodes:0,scans:0,patterns:0,forced:0,probes:0,probeForced:0,contradictions:0,branches:0,peakDepth:0,finds:0,guardAdds:0,copyCells:0};
   let fresh=()=>({p:Array.from({length:n+1},(_,i)=>i),z:Array(n+1).fill(0)});let clone=d=>{S.copyCells+=2*(n+1);return {p:d.p.slice(),z:d.z.slice()};};
   function find(d,v){S.finds++;let z=0;while(d.p[v]!==v){z^=d.z[v];v=d.p[v];}return [v,z];}
   function rel(d,a,b){let A=find(d,a),B=find(d,b);return A[0]===B[0]?A[1]^B[1]:-1;}
   function add(d,a,b,w){let A=find(d,a),B=find(d,b);if(A[0]===B[0])return (A[1]^B[1])===w?0:-1;let z=A[1]^B[1]^w;let [u,v]=A[0]>B[0]?[A[0],B[0]]:[B[0],A[0]];d.p[u]=v;d.z[u]=z;S.guardAdds++;return 1;}
   const pairs=[[0,1],[0,2],[1,2]];
   function close(d){for(;;){if(S.patterns>=cap)return {tag:"UNKNOWN"};S.scans++;let pending=[],change=false;
      outer:for(let o of O){let T=o.t,known=T.map(v=>rel(d,v,n)),rr=pairs.map(([i,j])=>rel(d,T[i],T[j])),allowed=[],possible=0;
        for(let w=0;w<8;w++){S.patterns++;if(known.some((v,i)=>v>=0&&v!==((w>>i)&1)))continue;if(rr.some((v,k)=>v>=0&&v!==(((w>>pairs[k][0])^(w>>pairs[k][1]))&1)))continue;possible++;if(!o.bad.includes(w))allowed.push(w);}
        if(!allowed.length){S.contradictions++;return {tag:"UNSAT"};}
        for(let i=0;i<3;i++)if(known[i]<0&&allowed.every(w=>((w>>i)&1)===(allowed[0]>>i&1))){add(d,T[i],n,allowed[0]>>i&1);S.forced++;change=true;break outer;}
        if(mode!=="coord")for(let k=0;k<3;k++)if(rr[k]<0){let [i,j]=pairs[k],w=(allowed[0]>>i^allowed[0]>>j)&1;if(allowed.every(z=>((z>>i^z>>j)&1)===w)){add(d,T[i],T[j],w);S.forced++;change=true;break outer;}}
        if(allowed.length<possible)pending.push({o,known,rr});
      }
      if(change)continue;return {tag:pending.length?"OPEN":"SAT",pending};
   }}
   function candidates(pending){let M=new Map();for(let {o,known,rr} of pending){if(mode!=="coord")for(let k=0;k<3;k++)if(rr[k]<0){let [i,j]=pairs[k],a=o.t[i],b=o.t[j];if(a>b)[a,b]=[b,a];let key=a+","+b,w=o.bad.length?1-((o.bad[0]>>i^o.bad[0]>>j)&1):1;let q=M.get(key)||{a,b,w,count:0};q.count++;M.set(key,q);}for(let i=0;i<3;i++)if(known[i]<0){let a=o.t[i],b=n,key=a+","+b,q=M.get(key)||{a,b,w:0,count:0};q.count++;M.set(key,q);}}
      let C=[...M.values()];C.sort((x,y)=>(mode==="coord"?0:(x.b===n)-(y.b===n))||y.count-x.count||x.a-y.a||x.b-y.b);return C;
   }
   function witness(d){let K=find(d,n);return Array.from({length:n},(_,i)=>{let A=find(d,i);return A[1]^(A[0]===K[0]?K[1]:0);});}
   function dfs(d,depth){S.nodes++;S.peakDepth=Math.max(S.peakDepth,depth);for(;;){let c=close(d);if(c.tag==="UNSAT"||c.tag==="UNKNOWN")return {tag:c.tag};if(c.tag==="SAT"){let x=witness(d);check(legal(O,x,pin));return {tag:"SAT",x};}
       let C=candidates(c.pending);check(C.length>0);
       if(mode==="probe"){let found=false;for(let q of C){let y=clone(d),z=clone(d);add(y,q.a,q.b,0);add(z,q.a,q.b,1);S.probes+=2;let A=close(y),B=close(z);if(A.tag==="SAT"){let x=witness(y);check(legal(O,x,pin));return {tag:"SAT",x};}if(B.tag==="SAT"){let x=witness(z);check(legal(O,x,pin));return {tag:"SAT",x};}if(A.tag==="UNKNOWN"||B.tag==="UNKNOWN")return {tag:"UNKNOWN"};if(A.tag==="UNSAT"&&B.tag==="UNSAT")return {tag:"UNSAT"};if(A.tag==="UNSAT"||B.tag==="UNSAT"){add(d,q.a,q.b,A.tag==="UNSAT"?1:0);S.probeForced++;found=true;break;}}
          if(found)continue;
       }
       let q=C[0];S.branches++;for(let w of [q.w,1-q.w]){let y=clone(d);add(y,q.a,q.b,w);let A=dfs(y,depth+1);if(A.tag!=="UNSAT")return A;}return {tag:"UNSAT"};
   }}
   let d=fresh();if(pin>=0)add(d,0,n,pin);let out=dfs(d,0);return {...out,S};
 }
 let rows=[];function run(label,G,pin,expected,ref=false){let row={label,n:G.n,pin,expected};if(ref){let k=0;for(let a=0;a<2**G.n;a++)if(legal(G.O,Array.from({length:G.n},(_,i)=>a>>i&1),pin))k++;check((k>0?"SAT":"UNSAT")===expected);row.models=k;}
 for(let mode of ["coord","parity","probe"]){let v=solve(G.n,G.O,pin,mode);check(v.tag==="UNKNOWN"||v.tag===expected);row[mode]=v;}rows.push(row);}
 for(let G of [F,plane()])for(let pin of [-1,0,1])run(G.n===7?"Fano":"M22",G,pin,"UNSAT",true);
 for(let i=0;i<7;i++){for(let j=0;j<3;j++)run("Fano sign "+i+":"+j,{n:7,O:F.O.map((o,k)=>k===i?owner(-1,o.t,[1<<j,7^(1<<j)]):o)},-1,"SAT",true);for(let b of [0,7])run("Fano budget "+i+":"+b,{n:7,O:F.O.map((o,k)=>k===i?owner(-1,o.t,[b]):o)},-1,"SAT",true);}
 for(let pin of [-1,0,1])run("BS16 planted",{n:hostile.n,O:hostile.O},pin,"SAT");
 for(let q of [1,2])for(let pin of [-1,0,1])run("BS15 q="+q,ring(q),pin,"SAT");
 // Independently enumerate all selector words for series diamonds. Each chosen edge is
 // a guarded equality; alternative dummy leaf equality has no terminal effect.
 let diamonds=[];for(let k=1;k<=4;k++){let E=[];for(let i=0;i<k;i++){let a=i,b=i+1,u=k+1+2*i,v=u+1;E.push([a,u],[u,b],[a,v],[v,b]);}let minimal=0,reject=0;function reach(mask){let V=new Set([0]);for(let change=true;change;){change=false;E.forEach(([a,b],j)=>{if(mask>>j&1&&V.has(a)!==V.has(b)){V.add(a);V.add(b);change=true;}});}return V.has(k);}
 for(let w=0;w<2**(4*k);w++){let fact=true;for(let i=0;i<k;i++)fact&&=((w>>(4*i)&3)===3||(w>>(4*i+2)&3)===3);let bad=reach(w);check(bad===fact);if(bad){reject++;if(E.every((_,j)=>!(w>>j&1)||!reach(w^(1<<j))))minimal++;}}
 check(minimal===2**k);diamonds.push({k,selectorWords:2**(4*k),reject,minimal});}
 return {checks,rows,diamonds,cap:1000000,source:"BS16 immutable JSON, hostile.O only; witness never supplied to solver"};
}
const raw=JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'));console.log(JSON.stringify(experiment(raw.hostile),null,2));
