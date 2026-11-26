// N4FN09: independent small-graph audits of affine-basis cut discovery and filtered exact cap gluing.
function audit(){
let seed=1720261126,checks=0;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function ok(x){checks++;if(!x)throw Error("assertion "+checks)}
function rank(A){let piv=Array(16).fill(0),r=0;for(let x of A)while(x){let i=31-Math.clz32(x);if(piv[i])x^=piv[i];else{piv[i]=x;r++;break}}return r}
function graph(n,extra){let E=[];for(let i=1;i<n;i++)E.push([i,rnd(i)]);while(extra--){let a=rnd(n),b=rnd(n-1);if(b>=a)b++;E.push([a,b])}return E}
function cut(E,A){return E.map(([u,v],i)=>(((A>>u)^(A>>v))&1)?i:-1).filter(i=>i>=0)}
function pop(x){let z=0;while(x){z++;x&=x-1}return z}
function discover(n,E,F,r){let ans=null,probes=0;
function test(B){probes++;let d=rank(B),A=Array.from({length:n},()=>[]);for(let i=0;i<E.length;i++)if(rank([...B,F[i]])>d){let [u,v]=E[i];A[u].push(v);A[v].push(u)}let cs=[],seen=new Set;for(let i=0;i<n;i++)if(!seen.has(i)){let q=[i],m=0;seen.add(i);for(let j=0;j<q.length;j++){let u=q[j];m|=1<<u;for(let v of A[u])if(!seen.has(v)){seen.add(v);q.push(v)}}cs.push(m)}
for(let a of cs)if(pop(a)>=2&&pop(a)<=n-2){ans=a;return}
let s=cs.filter(a=>pop(a)===1);if(s.length>=2&&n>=4)ans=s[0]|s[1]}
function rec(B,j){test(B);if(ans!==null||B.length===r)return;for(let i=j;i<F.length;i++){if(rank([...B,F[i]])===B.length+1)rec([...B,F[i]],i+1);if(ans!==null)return}}rec([],0);return {ans,probes}}
let discovery={jobs:0,positive:0,negative:0,probes:0};
for(let job=0;job<200;job++){let n=4+rnd(5),E=graph(n,rnd(4)),F=E.map(()=>rnd(32));for(let r=0;r<=3;r++){let expected=false;for(let a=0;a<1<<n;a++)if(pop(a)>=2&&pop(a)<=n-2&&rank(cut(E,a).map(i=>F[i]))<=r){expected=true;break}
let d=discover(n,E,F,r);ok((d.ans!==null)===expected);if(d.ans!==null){ok(pop(d.ans)>=2&&pop(d.ans)<=n-2);ok(rank(cut(E,d.ans).map(i=>F[i]))<=r)}discovery.jobs++;discovery.probes+=d.probes;discovery[expected?"positive":"negative"]++}}
let gluing={jobs:0,sat:0,unsat:0,strictGlobalFilter:0,selfdual:0,guarded:0,profiles:0};
function tuple(es,w){return es.reduce((x,e,i)=>x|(((w>>e)&1)<<i),0)}
function affineHull(rows){if(!rows.length)return new Set;let a=rows[0],S=new Set([0]);for(let x of rows){let d=x^a;for(let y of [...S])S.add(y^d)}return new Set([...S].map(x=>x^a))}
for(let job=0;job<400;job++){let n=4+rnd(3),E=graph(n,1+rnd(3)),m=E.length,es=Array.from({length:n},()=>[]);E.forEach(([a,b],i)=>{es[a].push(i);es[b].push(i)});let dual=job%2===0,R=es.map(a=>{let q=1<<a.length,rows=[];for(let i=0;i<q;i++){if(dual&&i>(i^(q-1)))continue;if(rnd(4)<3){rows.push(i);if(dual)rows.push(i^(q-1))}}return new Set(rows)}),H=R.map(r=>affineHull([...r]));
let A=(1<<(2+rnd(n-3)))-1,B=((1<<n)-1)^A,S=cut(E,A),mask=(1<<S.length)-1,allowed=new Set,wa=new Map,wb=new Map,expected=false;
for(let w=0;w<(1<<m);w++){let s=tuple(S,w),a=true,b=true,h=true;for(let i=0;i<n;i++){let x=tuple(es[i],w);if(!H[i].has(x))h=false;if(!R[i].has(x)){if(A>>i&1)a=false;else b=false}}if(a)wa.set(s,w);if(b)wb.set(s,w);if(a&&b)expected=true;if(h)allowed.add(s)}
let D=new Map;for(let s of allowed){if(dual&&s>(s^mask))continue;gluing.profiles++;if(wa.has(s)){D.set(s,wa.get(s));if(dual)D.set(s^mask,wa.get(s)^((1<<m)-1))}}
let common=[...D].find(([s])=>wb.has(s));ok(!!common===expected);
if(common){let [s,u]=common,v=wb.get(s),w=0;E.forEach(([i,j],e)=>{let z=(A>>i&1)||(A>>j&1)?u:v;w|=(z>>e&1)<<e});ok(es.every((a,i)=>R[i].has(tuple(a,w))));ok(tuple(S,w)===s)}
if([...wa.keys()].some(x=>!allowed.has(x)))gluing.strictGlobalFilter++;
if(dual)for(let s of allowed)ok(allowed.has(s^mask));
gluing.jobs++;gluing[expected?"sat":"unsat"]++;gluing[dual?"selfdual":"guarded"]++}
return {checks,seed:1720261126,discovery,gluing,limits:"small synthetic explicit affine-coordinate cuts and local affine-hull filtered caps; no large recursive generic implementation"}
}
console.log(JSON.stringify(audit(),null,2));