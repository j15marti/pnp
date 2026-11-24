// Node.js, deterministic exhaustive and relational controls.
function run(){
 const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n};
 const subs=m=>{let a=[];for(let s=m;;s=(s-1)&m){a.push(s);if(!s)break}return a};
 const assert=(x,msg)=>{if(!x)throw Error(msg)};
 const mask=vs=>vs.reduce((a,v)=>a|(1<<v),0);
 const bits=n=>((1<<n)-1);
 function closure(S,E){let C=S,prev;do{prev=C;for(const e of E)if(pop(e.m&C)>=2)C|=e.m}while(C!==prev);return C}
 function ok(a,e){let q=(a^e.sign)&e.m;return !(q===0&&e.lo)&&!(q===e.m&&e.hi)}
 function edge(vs,sign=0,lo=true,hi=true){return {m:mask(vs),sign,lo,hi}}
 function girth(n,E){let adj=Array.from({length:n+E.length},()=>[]);E.forEach((e,j)=>{for(let i=0;i<n;i++)if(e.m&(1<<i)){adj[i].push(n+j);adj[n+j].push(i)}});let best=Infinity;for(let start=0;start<adj.length;start++){let d=adj.map(()=>-1),p=adj.map(()=>-1),q=[start];d[start]=0;for(let k=0;k<q.length;k++){let u=q[k];for(let v of adj[u]){if(d[v]<0){d[v]=d[u]+1;p[v]=u;q.push(v)}else if(p[u]!==v&&p[v]!==u)best=Math.min(best,d[u]+d[v]+1)}}}return best===Infinity?null:best/2}
 function local(S,E){let C=closure(S,E),inside=E.filter(e=>(e.m&C)===e.m);let P=new Set();for(const a of subs(C))if(inside.every(e=>ok(a,e)))P.add(a&S);return {C,P}}
 function models(n,E){let out=[];for(let a=0;a<=bits(n);a++)if(E.every(e=>ok(a,e)))out.push(a);return out}
 function rel(n,E,w,G=0,pin=0){let free=bits(n)^G;let scopes=subs(free).filter(s=>pop(s)===w).map(s=>({s:s|G,r:subs(s).map(a=>a|pin).filter(a=>E.every(e=>(e.m&(s|G))!==e.m||ok(a,e)))}));let count=0,changed=true,comparisons=0;while(changed){changed=false;for(const a of scopes){for(const b of scopes){let I=a.s&b.s;let q=new Set(b.r.map(t=>t&I));let old=a.r.length;a.r=a.r.filter(t=>q.has(t&I));comparisons+=old;if(a.r.length!==old){count+=old-a.r.length;changed=true}if(!a.r.length)return {reject:true,deletions:count,comparisons,scopes}}}}return {reject:false,deletions:count,comparisons,scopes}}
 function loose(g,signed){return Array.from({length:g},(_,i)=>{let vs=[i,(i+1)%g,g+i];return edge(vs,signed?((i%2?1<<vs[0]:0)|(i%3===0?1<<vs[2]:0)):0)})}
 let res={algorithm:"DR01 exact integer mask tests",extension:[],rel:[],fano:[],counterexamples:[]};
 for(const [g,w,signed] of [[5,4,false],[5,4,true],[7,4,true],[9,4,false]]){
   let n=2*g,E=loose(g,signed),actual=girth(n,E);assert(actual===g,"girth");
   let table=new Map();let bound=0,restriction=0,extension=0;
   for(let S=0;S<=bits(n);S++){let s=pop(S);if(s>w)continue;let L=local(S,E);assert(L.P.size>0,"local empty");assert(pop(L.C)<=Math.max(0,2*s-1),"closure size");bound++;table.set(S,L)}
   for(const [S,L] of table){for(let i=0;i<n;i++){let b=1<<i;if(S&b){let U=S^b,Q=table.get(U).P;for(let a of L.P){assert(Q.has(a&U),"restriction");restriction++}}else if(pop(S)<w){let U=S|b,Q=table.get(U).P,proj=new Set([...Q].map(a=>a&S));for(let a of L.P){assert(proj.has(a),"extension");extension++}}}}
   let M=models(n,E);assert(M.length>0,"cycle should SAT");res.extension.push({g,n,w,signed,models:M.length,assignmentChecks:1<<n,bound,restriction,extension});
   if(g===5){for(const [G,pin,rw] of [[0,0,4],[3,0,2],[3,1,2]]){let R=rel(n,E,rw,G,pin);assert(!R.reject,"REL rejects");let protectedCount=0;for(let {s,r} of R.scopes){let P=table.get(s).P;for(let a of P)if((a&G)===pin){assert(r.includes(a),"protected tuple deleted");protectedCount++}}res.rel.push({g,signed,G,pin,w:rw,protectedCount,reject:R.reject,deletions:R.deletions,comparisons:R.comparisons})}}
 }
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(v=>edge(v));
 for(let j=-1;j<14;j++){let E=F.map((e,i)=>({...e,lo:j!==2*i,hi:j!==2*i+1}));let M=models(7,E);assert(M.length===(j<0?0:5),"Fano label");let widths=[];for(let w of [3,4,5]){let R=rel(7,E,w);assert(!R.reject||M.length===0,"false reject");for(let {s,r} of R.scopes)for(let a of M)assert(r.includes(a&s),"model deleted");widths.push({w,reject:R.reject,deletions:R.deletions,comparisons:R.comparisons})}res.fano.push({relaxedOwner:j,models:M.length,assignmentChecks:128,widths})}
 // Bad guard omitted from memo key: equal count k=1, two different tagged identities.
 const E=[edge([0,1,2])];let guardA=local(7,E).P, p0=[...guardA].filter(a=>(a&1)===0),p1=[...guardA].filter(a=>(a&1)===1);
 assert(p0.length===3&&p1.length===3,"guard example");
 res.counterexamples.push({name:"same source and same scope do not identify guard",guard0:p0,guard1:p1});
 return res;
}
console.log(JSON.stringify(run(),null,2));
