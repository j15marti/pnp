"use strict";
function experiment(){
 let seed=20261124, A=0; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}, ok=(x,msg)=>{A++;if(!x)throw Error(msg)};
 const dot=(a,x)=>a.reduce((s,v,i)=>s+v*x[i],0), eq=(a,b)=>a.every((v,i)=>v===b[i]), words=m=>Array.from({length:2**m},(_,j)=>Array.from({length:m},(_,i)=>(j>>i)&1));
 let out={seed:20261124,random:0,sat:0,unsat:0,forced:0,rowScans:0,matchings:0,lifts:0,scalarComparisons:0,redPathChecks:0,large:[],oldClipFailures:0};
 function close(rows,t,m){let fixed=Array(m).fill(-1),all=words(m);for(;;){let change=false;for(let i=0;i<rows.length;i++){out.rowScans++;let w=all.filter(x=>x.every((v,j)=>fixed[j]<0||v===fixed[j])&&dot(rows[i],x)===t[i]);if(!w.length)return null;for(let j=0;j<m;j++)if(fixed[j]<0&&w.every(x=>x[j]===w[0][j])){fixed[j]=w[0][j];out.forced++;change=true;break}if(change)break}if(!change)return fixed}}
 function graph(B,b,D,m){let slots=[],ports=[],opt=[],edges=[],n=0;const k=b.map((v,i)=>v+B[i].reduce((s,w)=>s+Math.max(0,-w),0));if(k.some((v,i)=>v<0||v>B[i].reduce((s,w)=>s+Math.abs(w),0)))return null;
 const add=(u,v,coef)=>edges.push({u,v,coef});for(let i=0;i<B.length;i++)slots.push(Array.from({length:k[i]},()=>n++));
 let shift=Array(D.length).fill(0);
 for(let j=0;j<m;j++){let occ=[];B.forEach((row,i)=>{for(let h=0;h<Math.abs(row[j]);h++)occ.push([i,Math.sign(row[j])])});let c=D.map(row=>row[j]);
 if(!occ.length){let p=n++,q=n++,s=n++,t=n++;add(p,q,c);add(q,s);add(s,t);add(t,p);continue}
 let pp=occ.map(([i,s],h)=>{let p=n++;if(h===0&&s<0)shift=shift.map((v,k)=>v+c[k]);for(let v of slots[i])add(p,v,h===0?c.map(w=>w*s):undefined);return p});
 if(pp.length===1){let l=n++;opt.push(l);add(pp[0],l)}else if(occ[0][1]===occ[1][1])add(...pp);else{let z=n++;add(z,pp[0]);add(z,pp[1])}}
 if(n%2)opt.push(n++);for(let i=0;i<opt.length;i++)for(let j=i+1;j<opt.length;j++)add(opt[i],opt[j]);return{n,edges,shift}}
 function enumerate(g,fn){let adj=Array.from({length:g.n},()=>[]);g.edges.forEach((e,i)=>{adj[e.u].push(i);adj[e.v].push(i)});function go(mask,sel){if(mask===0n){fn(sel);return}let u=0;while(!(mask&(1n<<BigInt(u))))u++;for(let i of adj[u]){let e=g.edges[i],v=e.u===u?e.v:e.u;if(mask&(1n<<BigInt(v)))go(mask^(1n<<BigInt(u))^(1n<<BigInt(v)),sel.concat(i))}}go((1n<<BigInt(g.n))-1n,[])}
 for(let z=0;z<160;z++){let m=2+rnd(4),r=1+rnd(3),k=1+rnd(3),B=Array.from({length:r},()=>Array(m).fill(0));for(let j=0;j<m;j++)for(let h=0,l=rnd(3);h<l;h++)B[rnd(r)][j]+=rnd(2)?1:-1;
 let D=Array.from({length:k},()=>Array.from({length:m},()=>rnd(5)-2)),a=words(m)[rnd(2**m)],b=B.map(row=>dot(row,a)),t=D.map(row=>dot(row,a));if(z%3===0)t[rnd(k)]+=rnd(2)?1:-1;if(z%7===0)b[rnd(r)]+=1;
 let ref=words(m).filter(x=>eq(B.map(row=>dot(row,x)),b)&&eq(D.map(row=>dot(row,x)),t));let fixed=close(B.concat(D),b.concat(t),m);if(!fixed)ok(!ref.length,"closure rejection");else for(let x of ref)ok(x.every((v,i)=>fixed[i]<0||v===fixed[i]),"bad pin");
 let g=graph(B,b,D,m),got=false, U=1+Math.max(...D.map((row,i)=>row.reduce((s,v)=>s+Math.abs(v),0)+Math.abs(t[i]))),R=2*U+1,encode=v=>v.reduce((s,w,i)=>s+w*R**i,0);
 if(g)enumerate(g,sel=>{out.matchings++;let v=g.shift.slice();for(let i of sel)if(g.edges[i].coef)v=v.map((w,j)=>w+g.edges[i].coef[j]);let same=eq(v,t),scalar=encode(v)===encode(t);out.scalarComparisons++;ok(same===scalar,"scalar collision");if(same){got=true;ok(ref.length>0,"source witness absent");out.lifts++}});
 ok(got===!!ref.length,"matching decision");out.random++;out[got?"sat":"unsat"]++}
 // Explicit odd-path red adapter, with one original edge selected/unselected.
 for(let L=0;L<=7;L++)for(let c=0;c<=L+1;c++){let n=2*L+2,edges=Array.from({length:n-1},(_,i)=>({u:i,v:i+1,red:i%2===0&&i/2<c}));let g={n,edges};let vals=[];enumerate(g,sel=>vals.push(sel.filter(i=>edges[i].red).length));ok(eq(vals,[c]),"selected red");let internal={n:n-2,edges:edges.slice(1,-1).map(e=>({...e,u:e.u-1,v:e.v-1}))};vals=[];enumerate(internal,sel=>vals.push(sel.filter(i=>internal.edges[i].red).length));ok(eq(vals,[0]),"unselected red");out.redPathChecks+=2}
 // Analytic large-capacity exact target x=y,  x+y+z=L, objective min x.
 // Old relaxed anchor (0,0,0); target-aware optimum (0,0,L).
 for(let bits of [16,64,128,256,512]){let L=(1n<<BigInt(bits))+1n,m=3,k=1,H=4*m*m,R=BigInt(4*(4*k*H+1+2*m)); // Q=2 radius
 let parity=new Set();for(let x=0n;x<=R;x++){let y=x,z=L-2n*x;if(z<0n||L-z>R)continue;ok(x===y&&x+y+z===L,"large lift");parity.add(Number(x%2n)*4+Number(y%2n)*2+Number(z%2n))}
 ok(parity.size===2&&parity.has(1)&&parity.has(7),"large parity");ok(3n*BigInt(8*m)<L,"old clip");out.oldClipFailures++;
 // Odd exact quota 2x=L is impossible even though LP anchor L/2 exists.
 ok(L%2n===1n,"odd unsat");let even=L+1n;ok(2n*(even/2n)===even,"even neighbor");
 out.large.push({bits:bits+1,parityFibers:[...parity],oddQuota:"UNSAT",evenQuota:"SAT",radius:R.toString()})}
 return {...out,assertions:A}}
console.log(JSON.stringify(experiment(),null,2));
