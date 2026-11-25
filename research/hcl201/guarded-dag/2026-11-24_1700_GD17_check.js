// GD17 deterministic finite checker. Run with Node.js.
function main(){
const C={norm:0,merge:0,contain:0,ie_nodes:0,oracle_calls:0,closure_scans:0,closure_sweeps:0,pins:0,local_pins:0,summary_vertices:0,peak_packets:0,edge_lifts:0,reference_words:0,assertions:0};
const assert=(x,msg)=>{C.assertions++;if(!x)throw Error(msg)};
const key=A=>A===null?"!":A.join(",");
const same=(A,B)=>key(A)===key(B);
const piv=a=>a===0n?0:a.toString(2).length-1;
const bit=i=>1n<<BigInt(i+1);
const row=(i,b)=>bit(i)|BigInt(b);
const parity=a=>{let x=0n;while(a){a&=a-1n;x^=1n}return x};
function norm(rs){C.norm++;let a=[];for(let r of rs){for(const q of a)if(r&(1n<<BigInt(piv(q))))r^=q;if(r===1n)return null;if(!r)continue;let b=1n<<BigInt(piv(r));a=a.map(q=>q&b?q^r:q);a.push(r);a.sort((x,y)=>piv(y)-piv(x));}return a}
const inter=(A,B)=>A===null||B===null?null:norm([...A,...B]);
const size=(H,n)=>H===null?0n:1n<<BigInt(n-H.length);
const point=H=>H.reduce((v,r)=>v|((r&1n)?1n<<BigInt(piv(r)):0n),0n);
const evalH=(H,x)=>H!==null&&H.every(r=>parity((r&~1n)&x)===(r&1n));
function dirs(H,n){let ps=new Set(H.map(piv)),out=[];for(let i=0;i<n;i++)if(!ps.has(i+1)){let v=bit(i);for(const r of H)if(parity(r&v))v|=1n<<BigInt(piv(r));out.push(v)}return out}
function hull(pts,n){if(!pts.length)return null;let d=norm(pts.slice(1).map(x=>x^pts[0]));return norm(dirs(d,n).map(a=>a|parity(a&pts[0])))}
function splitComplement(H,A){if(A===null)return[H];let G=H,out=[];for(const r of A){let B=inter(G,[r^1n]);if(B!==null)out.push(B);G=inter(G,[r]);if(G===null)break;}return out}
function simplify(H,Es){let E=Es.map(x=>inter(H,x)).filter(x=>x!==null);let changed=true;while(changed){changed=false;outer:for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++){let A=E[i],B=E[j],I=inter(A,B);C.contain++;if(same(I,A)){E.splice(i,1);changed=true;break outer}if(same(I,B)){E.splice(j,1);changed=true;break outer}
if(A.length===B.length&&A.every((r,k)=>(r&~1n)===(B[k]&~1n))){let q=A.findIndex((r,k)=>r!==B[k]);if(q>=0){let R=norm(A.filter((_,k)=>k!==q).map(r=>r)); // correct other RHS differences using original indices
R=norm(A.flatMap((r,k)=>k===q?[]:[r!==B[k]?r^A[q]:r]));
E.splice(j,1);E[i]=R;C.merge++;changed=true;break outer;}}
}}return E}
const BOUND=7;
function safeOracle(H,events,n){let G=H,E=simplify(G,events);while(true){if(E.some(x=>same(x,G))){return {q:()=>0n,total:0n,aff:null}}let i=E.findIndex(x=>x.length===G.length+1);if(i<0)break;let r=E[i].find(a=>inter(G,[a^1n])!==null);assert(r!==undefined,"rank1 witness");G=inter(G,[r^1n]);C.local_pins++;if(G===null)return{q:()=>0n,total:0n,aff:null};E=simplify(G,E)}
if(!E.length){let q=Q=>{C.oracle_calls++;return size(inter(G,Q),n)};return{q,total:size(G,n),aff:G}}
let packets=[[G,1n]],bad=false;
function walk(start,A,depth){for(let i=start;i<E.length&&!bad;i++){C.ie_nodes++;let I=inter(A,E[i]);if(I===null)continue;if(depth===BOUND){bad=true;break}packets.push([I,depth%2===0?-1n:1n]);walk(i+1,I,depth+1)}}
walk(0,G,0);if(bad)return null;C.peak_packets=Math.max(C.peak_packets,packets.length);
let q=Q=>{C.oracle_calls++;return packets.reduce((s,[A,w])=>s+w*size(inter(A,Q),n),0n)};
return{q,total:q(H),aff:undefined}}
function findPoint(H,q,n){if(q(H)<=0n)return null;let G=H;for(let i=0;i<n;i++){let A=inter(G,[row(i,0)]),B=inter(G,[row(i,1)]);if(A===null||B===null){G=A??B;continue}G=q(A)>0n?A:B;assert(q(G)>0n,"positive branch")}return point(G)}
function recognize(H,q,total,n){if(total===0n)return{yes:true,A:null};if((total&(total-1n))!==0n)return{yes:false};let p=findPoint(H,q,n),pts=[p];while(true){let A=hull(pts,n);if(size(A,n)>total)return{yes:false};let added=false;for(const r of A){let Q=inter(H,[r^1n]);if(Q!==null&&q(Q)>0n){pts.push(findPoint(Q,q,n));added=true;break}}if(!added)return size(A,n)===total?{yes:true,A}:{yes:false};}}
function local(H,Es,n,root){Es=simplify(H,Es);if(!root&&Es.length<=1)return{type:"A",A:Es[0]??null};let o=safeOracle(H,Es,n);if(!o)return null;if(root)return{o};if(o.total===0n)return{type:"A",A:H};if(o.total===size(H,n))return{type:"A",A:null};if(o.aff!==undefined)return{type:"C",A:o.aff};let a=recognize(H,o.q,o.total,n);if(a.yes)return{type:"C",A:a.A};let q=Q=>size(Q,n)-o.q(Q);a=recognize(H,q,size(H,n)-o.total,n);return a.yes?{type:"A",A:a.A}:null}
function evaluate(B,x){let R=Array(B.V).fill(false);R[0]=true;for(const [u,v,g] of B.E){C.edge_lifts++;if(R[u]&&evalH(g,x))R[v]=true}return R[B.V-1]}
function concat(Bs){let V=1,E=[];for(const B of Bs){let k=V-1;E.push(...B.E.map(([u,v,g])=>[u+k,v+k,g]));V+=B.V-1}return{V,E}}
function close(B,H,n){while(H!==null){C.closure_sweeps++;let es=B.E.map(([u,v,g])=>{C.closure_scans++;return[u,v,inter(H,g)]});let f=Array(B.V).fill(false),p=f.slice(),b=f.slice();f[0]=p[0]=b[B.V-1]=true;for(const [u,v,g] of es){if(g!==null&&p[u])p[v]=true;if(same(g,H)&&f[u])f[v]=true}if(f[B.V-1])return{H:null,label:"UNSAT"};if(!p[B.V-1])return{H,label:"SAT",x:point(H)};for(let i=es.length-1;i>=0;i--){let[u,v,g]=es[i];if(same(g,H)&&b[v])b[u]=true}let r=null;for(const[u,v,g]of es)if(f[u]&&b[v]&&g!==null&&g.length===H.length+1){r=g.find(a=>inter(H,[a^1n])!==null);break}if(r===null||r===undefined)return{H};H=inter(H,[r^1n]);C.pins++}return{H:null,label:"UNSAT"}}
function solveBlock(B,H,n){let out=Array.from({length:B.V},()=>[]);for(const [u,v,g] of B.E)out[u].push([v,g]);let s=Array(B.V);s[B.V-1]={type:"A",A:H};for(let u=B.V-2;u>=0;u--){C.summary_vertices++;let es=[];for(const[v,g]of out[u]){if(!s[v])return{label:"UNKNOWN"};let G=inter(H,g);if(G===null)continue;const q=s[v];if(q.type==="A"){let A=inter(G,q.A);if(A!==null)es.push(A)}else es.push(...splitComplement(G,q.A))}
let r=local(H,es,n,u===0);if(!r)return{label:"UNKNOWN"};if(u===0){let o=r.o;if(o.total===0n)return{label:"UNSAT"};let x=findPoint(H,o.q,n);assert(x!==null&&!evaluate(B,x),"block lift");return{label:"SAT",x}}s[u]=r}throw Error("empty graph")}
function solve(Bs,H,n){const G=concat(Bs);let c=close(G,H,n);if(c.label)return c;let unknown=false;for(const B of Bs){let r=solveBlock(B,c.H,n);if(r.label==="SAT"){assert(evalH(H,r.x)&&!evaluate(G,r.x),"source lift");return r}if(r.label==="UNKNOWN")unknown=true}return{label:unknown?"UNKNOWN":"UNSAT"}}
function graph(V,E){return{V,E:E.sort((a,b)=>a[0]-b[0]||a[1]-b[1])}}
function clauseGraph(clauses){let E=[],V=clauses.length+2;for(let i=0;i<clauses.length;i++){E.push([0,i+1,[]],[i+1,V-1,norm(clauses[i])])}return graph(V,E)}
let totals={},scale=[];function check(name,Bs,H,n,expected=null,enumerate=true){let r=solve(Bs,H,n);let ref=expected;if(enumerate){let count=0;let G=concat(Bs);for(let x=0;x<2**n;x++){C.reference_words++;let w=BigInt(x)<<1n;if(evalH(H,w)&&!evaluate(G,w))count++}ref=count?"SAT":"UNSAT";if(expected)assert(expected===ref,"reference expectation")}if(r.label!=="UNKNOWN")assert(r.label===ref,name+" decision");if(r.label==="SAT")assert(evalH(H,r.x)&&!evaluate(concat(Bs),r.x),name+" lift");let z=totals[name]??={SAT:0,UNSAT:0,UNKNOWN:0};z[r.label]++;return r.label}
for(let mask=0;mask<256;mask++){let cs=[];for(let w=0;w<8;w++)if(mask>>w&1)cs.push([0,1,2].map(i=>row(i,w>>i&1)));check("cube",[clauseGraph(cs)],[],3)}
const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
const fano=lines.flatMap(L=>[0,1].map(b=>L.map(i=>row(i,b))));
check("Fano",[clauseGraph(fano)],[],7,"UNSAT");
for(let i=0;i<fano.length;i++)check("Fano",[clauseGraph(fano.filter((_,j)=>j!==i))],[],7,"SAT");
let seed=20261124;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let j=0;j<120;j++){let n=5,V=7,E=[];for(let u=0;u<V-1;u++)for(let v=u+1;v<V;v++)if(rng(4)!==0){let g=[];for(let a=0;a<rng(3);a++){let r=BigInt(1+rng(31))<<1n;g.push(r|BigInt(rng(2)))}let H=norm(g);if(H!==null)E.push([u,v,H])}let H=j%3?[]:[row(0,j%2)];check("random",[graph(V,E)],H,n)}
function neutral(k,offset,reverse=false){let E=[],V=1,prev=[];for(let i=0;i<4*k;i++){prev.push(V++);E.push([0,prev[i],[]])}
for(let l=0;l<2*k;l++){let next=prev.map(()=>V++);for(let i=0;i<4*k;i++){let group=i>>2,word=i%4;E.push([prev[i],next[i],group===(l>>1)?[row(offset+l,(word>>(l%2))&1)]:[]])}prev=next}
for(let l=0;l<2*k;l++){let next=prev.map(()=>V++);for(let i=0;i<4*k;i++){let mult=l===0?i%4+1:l<=2*(i>>2)?2:1;for(let a=0;a<mult;a++)E.push([prev[i],next[i],[]])}prev=next}
let t=V++;for(const v of prev)E.push([v,t,[]]);if(reverse)E=E.map(([u,v,g])=>[V-1-v,V-1-u,g]);return graph(V,E)}
function core(k,offset,odd){let V=1,E=[],prev=[];for(let i=0;i<2*k;i++){prev.push(V++);E.push([0,prev[i],[]])}let p=[V++,V++];E.push([0,p[0],[]]);for(let l=0;l<2*k;l++){let next=prev.map(()=>V++),q=[V++,V++];for(let i=0;i<2*k;i++){let pair=i>>1,pat=i%2;E.push([prev[i],next[i],pair===(l>>1)?[row(offset+l,l%2?1-pat:pat)]:[]])}for(let s=0;s<2;s++)for(let b=0;b<2;b++)E.push([p[s],q[s^b],[row(offset+l,b)]]);prev=next;p=q}
for(let l=0;l<k;l++){let next=prev.map(()=>V++);let q=p.map(()=>V++);for(let i=0;i<2*k;i++)for(let a=0;a<(l<=(i>>1)?2:1);a++)E.push([prev[i],next[i],[]]);for(let s=0;s<2;s++)E.push([p[s],q[s],[]]);prev=next;p=q}
let t=V++;for(let v of prev)E.push([v,t,[]]);E.push([p[odd?0:1],t,[]]);return graph(V,E)}
for(let k of [1,2,4,8,12]){let before=C.summary_vertices,es=0,vs=0;let labs=[];for(let odd of [false,true]){let Bs=[neutral(k,0),core(k,2*k,odd),neutral(k,4*k,true)];es=concat(Bs).E.length;vs=concat(Bs).V;labs.push(check("DR10",[...Bs],[],6*k,odd?"UNSAT":"SAT",k===1));}scale.push({k,vertices:vs,edges:es,labels:labs,local_vertices:C.summary_vertices-before})}
let high=[];for(let i=0;i<8;i++)high.push([row(2*i,0),row(2*i+1,0)]);
assert(check("high_overlap",[clauseGraph(high)],[],16,"SAT",false)==="UNKNOWN","cap");
let E=[[0,1,[]],[0,2,[]],[1,3,[row(0,0),row(1,0),row(2,0)]],[1,3,[row(0,0),row(1,0),row(2,1)]],[1,3,[row(0,1),row(1,1),row(2,0)]],[2,3,[row(0,1),row(1,0),row(2,0)]]];
assert(check("nonaffine",[graph(4,E)],[],3,"SAT")==="UNKNOWN","nonaffine decline");
return {bound:BOUND,seed:20261124,totals,scale,ledger:C};
}
console.log(JSON.stringify(main(),null,2));
