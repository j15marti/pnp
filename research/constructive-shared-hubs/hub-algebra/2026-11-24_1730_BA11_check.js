function BA11check(){
 const M={solves:0,xors:0,energyQueries:0,energyPairs:0,countQueries:0,closureScans:0,pins:0,projectedTerms:0,assertions:0,referenceWords:0,lifts:0,maxTerms:0,maxInterface:0};
 const bit=i=>1n<<BigInt(i), p2=i=>bit(i);
 function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 const dot=(x,y)=>parity(x&y);
 function ok(x,msg){M.assertions++;if(!x)throw Error(msg)}
 function solve(d,eq){
   M.solves++;const rows=new Map();
   for(let [a,b] of eq){while(a){let p=a.toString(2).length-1;if(!rows.has(p)){rows.set(p,[a,b]);break}const [v,t]=rows.get(p);a^=v;b^=t;M.xors++}if(!a&&b)return null}
   const order=[...rows.keys()].sort((a,b)=>a-b);
   function fill(x,hom){for(const p of order){const [a,b]=rows.get(p);if(dot(a,x)!==(hom?0:b))x^=bit(p)}return x}
   return {a:fill(0n,false),K:Array.from({length:d},(_,i)=>i).filter(i=>!rows.has(i)).map(i=>fill(bit(i),true)),rows:order.map(p=>rows.get(p)[0])}
 }
 const hom=xs=>xs.map(x=>[x,0]), span=(d,xs)=>solve(d,hom(xs)).rows;
 const map=(W,x)=>W.reduce((s,w,i)=>s|(dot(w,x)?bit(i):0n),0n);
 function evalf(f,x){return f.reduce((v,t)=>v+(t.eq.every(([a,b])=>dot(a,x)===b)?t.c:0n),0n)}
 function count(d,f,Q=[]){M.countQueries++;let s=0n;for(const t of f){const a=solve(d,[...Q,...t.eq]);if(a)s+=t.c*p2(a.K.length)}return s}
 function product(d,f,g){const out=[];for(const t of f)for(const u of g){const eq=[...t.eq,...u.eq];if(solve(d,eq))out.push({c:t.c*u.c,eq})}M.maxTerms=Math.max(M.maxTerms,out.length);return out}
 const one=()=>[{c:1n,eq:[]}], reject=eq=>[...one(),{c:-1n,eq}];
 function word(d,f,Q){if(count(d,f,Q)<=0n)return null;let q=Q.slice(),x=0n;for(let i=0;i<d;i++){if(count(d,f,[...q,[bit(i),0]])>0n)q.push([bit(i),0]);else{q.push([bit(i),1]);x|=bit(i)}}return x}
 function hull(d,f,Q){const a=word(d,f,Q);if(a===null)return null;let B=[];for(;;){let found=false;for(const w of solve(d,hom(B)).K){const x=word(d,f,[...Q,[w,1^dot(w,a)]]);if(x!==null){B=span(d,[...B,x^a]);found=true;break}}if(!found)return solve(d,hom(B)).K.map(w=>[w,dot(w,a)])}}
 function closure(d,fs,Q){let q=Q.slice();for(;;){let g=solve(d,q);if(!g)return null;let change=false;for(const f of fs){M.closureScans++;const h=hull(d,f,q);if(!h)return null;for(const e of h){const ng=solve(d,[...q,e]);if(!ng)return null;if(ng.K.length<g.K.length){q.push(e);M.pins++;change=true;break}}if(change)break}if(!change)return q}}
 function restrict(f,G){return f.map(t=>({c:t.c,eq:t.eq.map(([a,b])=>[map(G.K,a),b^dot(a,G.a)])}))}
 function spectral(d,f){
   const terms=[];for(const t of f){const a=solve(d,t.eq);if(a)terms.push({c:t.c*p2(a.K.length),a:a.a,eq:hom(a.K)})}
   function E(Q){M.energyQueries++;let s=0n;for(const t of terms)for(const u of terms){M.energyPairs++;const A=solve(d,[...Q,...t.eq,...u.eq]);if(!A)continue;const phase=t.a^u.a;if(A.K.some(v=>dot(v,phase)))continue;s+=t.c*u.c*p2(A.K.length)*(dot(A.a,phase)?-1n:1n)}ok(s>=0n,"negative spectral energy");return s}
   let V=[];for(;;){let changed=false;for(const w of solve(d,hom(V)).K){let Q=[[w,1]];if(!E(Q))continue;let x=0n;for(let i=0;i<d;i++){if(E([...Q,[bit(i),0]]))Q.push([bit(i),0]);else{Q.push([bit(i),1]);x|=bit(i)}}V=span(d,[...V,x]);changed=true;break}if(!changed)return V}
 }
 function inter(d,V,U){return solve(d,hom([...solve(d,hom(V)).K,...solve(d,hom(U)).K])).K}
 function project(d,f,W){
   const k=W.length,out=[];for(const t of f){const A=solve(d,t.eq);if(!A)continue;const a=map(W,A.a),B=span(k,A.K.map(x=>map(W,x))),eq=solve(k,hom(B)).K.map(w=>[w,dot(w,a)]);out.push({c:t.c*p2(A.K.length-B.length),eq});M.projectedTerms++}return out
 }
 function joint(d,f,g,Q=[]){
   // Source contract: each factor is Boolean. Check that with a paid pair sum.
   for(const h of [f,g])ok(count(d,product(d,h,h),Q)===count(d,h,Q),"nonboolean");
   Q=closure(d,[f,g],Q);if(Q===null)return {n:0n,k:null};
   const G=solve(d,Q),D=G.K.length,F=restrict(f,G),H=restrict(g,G),V=spectral(D,F),U=spectral(D,H),W=inter(D,V,U),k=W.length;
   M.maxInterface=Math.max(M.maxInterface,k);
   const a=project(D,F,W),b=project(D,H,W),both=product(k,a,b),S=count(k,both),div=p2(D-k);
   ok(S%div===0n,"fiber count normalization");const n=S/div;
   if(n){const y=word(k,both,[]),q=W.map((w,i)=>[w,dot(bit(i),y)]),x=word(D,F,q),z=word(D,H,q);ok(x!==null&&z!==null,"missing lift");const j=solve(D,[...V.map(w=>[w,dot(w,x)]),...U.map(w=>[w,dot(w,z)])]);ok(j!==null,"incompatible lift");const original=G.a^G.K.reduce((s,v,i)=>s^(dot(bit(i),j.a)?v:0n),0n);ok(evalf(f,original)===1n&&evalf(g,original)===1n&&Q.every(([a,b])=>dot(a,original)===b),"invalid original witness");M.lifts++}
   return {n,k,v:V.length,u:U.length}
 }
 function reference(d,f,g,Q=[]){let c=0n;for(let x=0n;x<p2(d);x++){M.referenceWords++;if(Q.every(([a,b])=>dot(a,x)===b)&&evalf(f,x)===1n&&evalf(g,x)===1n)c++}return c}
 function audit(d,f){let V=spectral(d,f),B=[];for(let w=0n;w<p2(d);w++){let c=0n;for(let x=0n;x<p2(d);x++)c+=evalf(f,x)*(dot(w,x)?-1n:1n);if(c)B.push(w)}ok(span(d,[...B,...V]).length===V.length&&span(d,B).length===V.length,"spectral span");return V.length}
 const results={seed:1124,random:{sat:0,unsat:0},fano:[],padding:[],dense:[],caveat:[]};let state=1124;
 function rng(n){state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n}
 function randTerm(d){let eq=[];for(let j=0;j<2+rng(2);j++)eq.push([BigInt(1+rng((1<<d)-1)),rng(2)]);return reject(eq)}
 for(let i=0;i<32;i++){let d=4+i%3,F=product(d,randTerm(d),randTerm(d)),H=product(d,randTerm(d),randTerm(d)),Q=i%3===0?[[BigInt(1+rng((1<<d)-1)),rng(2)]]:[];audit(d,F);audit(d,H);const z=joint(d,F,H,Q),n=reference(d,F,H,Q);ok(z.n===n,"random count");results.random[n?"sat":"unsat"]++}
 // Standard Fano triples, one-sided neighbor leaves one forbidden monochromatic word.
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 for(let t=-1;t<14;t++){let f=one(),g=one();for(let i=0;i<7;i++){const [a,b,c]=triples[i],eq=i===Math.floor(t/2)?[[bit(a),t%2],[bit(b),t%2],[bit(c),t%2]]:[[bit(a)^bit(b),0],[bit(a)^bit(c),0]];if(i<3)f=product(7,f,reject(eq));else g=product(7,g,reject(eq))}const z=joint(7,f,g);const n=reference(7,f,g);ok(z.n===n&&n===(t<0?0n:5n),"Fano count");results.fano.push({neighbor:t,count:String(n),interface:z.k})}
 // Redundant affine packets inflate the syntactic rank while the actual function is a two-bit OR.
 for(const d of [4,8,12,16]){const eq=[[1n,0],[2n,0]],f=reject(eq);for(let i=2;i<d;i++)f.push({c:1n,eq},{c:-1n,eq:[...eq,[bit(i),0]]},{c:-1n,eq:[...eq,[bit(i),1]]});const V=spectral(d,f);ok(V.length===2,"padding rank");const g=reject([[2n,0],[bit(d-1),0]]),z=joint(d,f,g);ok(z.k===1&&z.n===5n*p2(d-3),"padding join");results.padding.push({d,terms:f.length,semantic:V.length,interface:z.k,count:String(z.n)})}
 // Dense Walsh spectra but exact two-region composition without an interface truth table.
 for(const d of [8,16,24]){const eq=Array.from({length:d},(_,i)=>[bit(i),0]),f=reject(eq),g=reject(eq.map(([w,b],i)=>[w,i===0?1:b]));const z=joint(d,f,g);ok(z.k===d&&z.n===p2(d)-2n,"dense join");results.dense.push({d,interface:z.k,count:String(z.n),nonzeroSpectrum:p2(d).toString()})}
 // Support-vs-multiplicity: project f(x,y)=x OR y onto x; fibers have counts 1,2, but both nonempty.
 const c=project(2,reject([[1n,0],[2n,0]]),[1n]);ok(evalf(c,0n)===1n&&evalf(c,1n)===2n&&spectral(1,c).length===1,"count rank caveat");results.caveat=[String(evalf(c,0n)),String(evalf(c,1n))];
 return {results,ledger:M};
}
console.log(JSON.stringify(BA11check(),null,2));
