function audit(){
 const assert=(v,m="assert")=>{if(!v)throw Error(m)};
 const parity=x=>{let b=0;while(x){b^=1;x&=x-1}return b};
 const pivot=x=>31-Math.clz32(x);
 function solve(eq,n){let B=new Map();for(let [a,b] of eq){while(a&&B.has(pivot(a))){const [v,t]=B.get(pivot(a));a^=v;b^=t}if(!a){if(b)return null;continue}B.set(pivot(a),[a,b])}let x=0;for(const p of [...B.keys()].sort((a,b)=>a-b)){let [a,b]=B.get(p);if(parity(a&x)!==b)x^=1<<p}return {x,B}}
 const bas=(rows,n)=>[...solve(rows.map(a=>[a,0]),n).B.values()].map(e=>e[0]);
 function nulls(rows,n){const E=solve(rows.map(a=>[a,0]),n);let out=[];for(let i=0;i<n;i++)if(!E.B.has(i)){let x=1<<i;for(const p of [...E.B.keys()].sort((a,b)=>a-b))if(parity(E.B.get(p)[0]&x))x^=1<<p;out.push(x)}return out}
 const inter=(a,b,n)=>nulls([...nulls(a,n),...nulls(b,n)],n);
 const obs=(a,x)=>a.reduce((s,v,i)=>s+(parity(v&x)<<i),0);
 const eqval=(a,t)=>a.map((v,i)=>[v,(t>>i)&1]);
 const eqx=(a,x)=>a.map(v=>[v,parity(v&x)]);
 const feat=(x,n,h)=>{let b=1n,p=1n;for(let i=0;i<n;i++){if(h>=1){if(x&(1<<i))b|=1n<<p;p++}if(h>=2)for(let j=i+1;j<n;j++){if((x&(1<<i))&&(x&(1<<j)))b|=1n<<p;p++}}return b};
 function insert(T,x,n,h){let a=feat(x,n,h);while(a){let p=a.toString(2).length-1;if(T.b.has(p))a^=T.b.get(p);else{T.b.set(p,a);T.x.push(x);return}}}
 const make=()=>({b:new Map(),x:[]});
 function points(eq,n,h){let s=solve(eq,n);if(!s)return [];let D=nulls(eq.map(e=>e[0]),n),out=[s.x];if(h>=1)for(let v of D)out.push(s.x^v);if(h>=2)for(let i=0;i<D.length;i++)for(let j=i+1;j<D.length;j++)out.push(s.x^D[i]^D[j]);return out}
 const legal=(P,x)=>P.every(o=>o.kind==="eq"?o.eq.every(([a,b])=>parity(a&x)===b):!o.eq.every(([a,b])=>parity(a&x)===b));
 const counts={roots:0,sat:0,unsat:0,guarded:0,guard_sat:0,guard_unsat:0,basis_checks:0,degree:2,local_states:0,joins:0,stored_witnesses:0,root_witness_checks:0,closure_calls:0,closure_probes:0,forced:0,width_max:0,compiler_checks:0};
 function norm(P,G,n){counts.closure_calls++;G=G.slice();for(;;){let q=solve(G,n);if(!q)return null;let changed=false;for(const o of P){if(!solve([...G,...o.eq],n))continue;let R=solve([...G,...o.eq],n);let d=R.B.size-q.B.size;if(!d)return null;if(d===1){let e=o.eq.find(e=>solve([...G,e],n).B.size>q.B.size);G.push([e[0],1^e[1]]);changed=true;break}}if(!changed)return G}}
 function close(P,G,n){let R=norm(P,G,n);if(!R)return null;for(;;){let changed=false;for(let i=0;i<n;i++){let a=1<<i;if(bas([...R.map(e=>e[0]),a],n).length===solve(R,n).B.size)continue;for(let t=0;t<2;t++){counts.closure_probes++;if(norm(P,[...R,[a,t]],n)===null){R=norm(P,[...R,[a,1^t]],n);counts.forced++;if(!R)return null;changed=true;break}}if(changed)break}if(!changed)return R}}
 function tree(P,n,h){if(!P.length)return points([],n,h);const all=P.map(o=>o.eq.map(e=>e[0]));function run(ids){const set=new Set(ids),U=bas(ids.flatMap(i=>all[i]),n),V=bas(all.filter((_,i)=>!set.has(i)).flat(),n),B=inter(U,V,n);counts.width_max=Math.max(counts.width_max,B.length);const tab=new Map();function put(x){const k=obs(B,x);let t=tab.get(k);if(!t){t=make();tab.set(k,t)}let y=solve(eqx(U,x),n).x;insert(t,y,n,h)}
 if(ids.length===1){const o=P[ids[0]];for(let s=0;s<2**B.length;s++){const g=eqval(B,s);const charts=o.kind==="eq"?[[...g,...o.eq]]:o.eq.map(([a,b],j)=>[...g,...o.eq.slice(0,j),[a,1^b]]);for(const c of charts)for(const x of points(c,n,h))put(x)}}else{let k=Math.floor(ids.length/2),A=run(ids.slice(0,k)),C=run(ids.slice(k)),D=inter(A.U,C.U,n);for(const a of A.tab.values())for(const b of C.tab.values()){if(obs(D,a.x[0])!==obs(D,b.x[0]))continue;for(const x of a.x)for(const y of b.x){counts.joins++;const z=solve([...eqx(A.U,x),...eqx(C.U,y)],n);assert(z,"join");put(z.x)}}}
 counts.local_states+=tab.size;counts.stored_witnesses+=[...tab.values()].reduce((s,t)=>s+t.x.length,0);return {U,tab}}
 const root=run(P.map((_,i)=>i)),out=make();for(const t of root.tab.values())for(const x of t.x)for(const y of points(eqx(root.U,x),n,h))insert(out,y,n,h);return out.x}
 function check(P,G,n,guard){let ref=[];for(let x=0;x<2**n;x++)if(legal(P,x)&&G.every(([a,b])=>parity(a&x)===b))ref.push(x);let R=close(P,G,n),out=R===null?[]:tree([...P,...(R.length?[{kind:"eq",eq:R}]:[])],n,2);let A=make(),B=make();for(let x of ref)insert(A,x,n,2);for(let x of out){assert(legal(P,x)&&G.every(([a,b])=>parity(a&x)===b),"bad witness");insert(B,x,n,2);counts.root_witness_checks++}assert(A.b.size===B.b.size,"basis rank");counts.basis_checks++;if(guard){counts.guarded++;counts[ref.length?"guard_sat":"guard_unsat"]++}else{counts.roots++;counts[ref.length?"sat":"unsat"]++}}
 let seed=20261125;const rand=k=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k};
 for(let n=2;n<=7;n++)for(let t=0;t<30;t++){let P=[];for(let i=0,m=1+rand(n+3);i<m;i++){let a=1+rand((1<<n)-1),b=1+rand((1<<n)-1);while(b===a)b=1+rand((1<<n)-1);let rows=[a,b];if(n>=3&&t%5===0){let c=1+rand((1<<n)-1);if(bas([...rows,c],n).length===3)rows.push(c)}P.push({kind:"forbid",eq:rows.map(a=>[a,rand(2)])})}check(P,[],n,false);for(let j=0;j<3;j++)check(P,[[1+rand((1<<n)-1),rand(2)]],n,true)}
 // Explicit complete forbidden pair cover and one-deletion SAT neighbors.
 let P=Array.from({length:4},(_,i)=>({kind:"forbid",eq:[[1,i&1],[2,i>>1]]}));check(P,[],2,false);for(let i=0;i<4;i++)check(P.filter((_,j)=>j!==i),[],2,false);
 for(let s=0;s<8;s++)for(let x=0;x<8;x++)for(let t=0;t<8;t++){let l=x^s;const legal=parity(t)===1&&(t&~l)===0;assert(!legal||l!==0);counts.compiler_checks++}
 return counts;
}
console.log(JSON.stringify(audit(),null,2));
