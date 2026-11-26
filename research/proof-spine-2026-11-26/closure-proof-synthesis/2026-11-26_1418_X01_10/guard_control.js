function guardControl(){
let checks=0;const ok=(p,m)=>{checks++;if(!p)throw Error(m||"check "+checks)};
const ATOM=[[0,2,4],[0,2,5],[0,3,5],[1,2,4],[1,3,4],[1,3,5]];
const W=[];for(let w=0;w<64;w++){let cnt=Array(6).fill(0);ATOM.forEach((t,i)=>{if(w>>i&1)t.forEach(v=>cnt[v]++)});if(cnt.every(x=>x===1))W.push(w)}ok(W.length===3);
function compile(F,n){let T=[],guards=[],V=[],C=[];
 function atom(){let j=T.length;T.push(...ATOM.map(t=>t.map(v=>v+j)));return j}
 for(let i=0;i<n;i++)V.push(atom());
 for(let clause of F){let s=atom(),I=[];for(let j=0;j<3;j++){let h=atom(),lit=clause[j];I.push(h);guards.push([h,s+j,0],[h+1,V[Math.abs(lit)-1],lit>0?1:0])}C.push({s,I})}return {T,guards,V,C,F}}
function lift(Q,x){let a=Array(Q.T.length).fill(0),set=(o,w)=>{for(let j=0;j<6;j++)a[o+j]=w>>j&1};Q.V.forEach((v,i)=>set(v,W.find(w=>(w&1)===(x>>i&1))));
 for(let i=0;i<Q.F.length;i++){let {s,I}=Q.C[i],ls=Q.F[i].map(l=>((x>>(Math.abs(l)-1))&1)^(l<0?1:0)),good=[];for(let w of W){let ws=I.map((v,j)=>W.find(h=>(h&1)===(w>>j&1)&&(h>>1&1)===(1-ls[j])));if(ws.every(h=>h!==undefined))good.push({w,ws})}ok(good.length===ls.reduce((p,v)=>p+v,0));if(!good.length)return null;let g=good[0];set(s,g.w);I.forEach((o,j)=>set(o,g.ws[j]))}
 const cnt=Array(Q.T.length).fill(0);Q.T.forEach((t,i)=>{if(a[i])t.forEach(v=>cnt[v]++)});ok(cnt.every(v=>v===1));ok(Q.guards.every(([i,j,b])=>(a[i]^a[j])===b));return a}
let all=Array.from({length:8},(_,a)=>[1,2,3].map((v,j)=>a>>j&1?v:-v)),Y=all.map(x=>x.slice());Y[0][0]*=-1;let results=[];for(let [yes,F] of [[false,all],[true,Y]]){let Q=compile(F,3),solutions=0;for(let x=0;x<8;x++){let ref=F.every(C=>C.some(l=>!!(x>>(Math.abs(l)-1)&1)===(l>0)));let w=lift(Q,x);ok(!!w===ref);if(w)solutions++}ok((solutions>0)===yes);results.push({yes,triples:Q.T.length,affineRows:Q.guards.length,sourceAssignmentsAccepted:solutions})}
 // All 8 truth patterns and all 3 one-hot choices, verify exact implication.
 for(let lit=0;lit<8;lit++)for(let sw of W){for(let j=0;j<3;j++){let a=sw>>j&1,b=1-(lit>>j&1);let options=W.filter(w=>(w&1)===a&&(w>>1&1)===b);ok((options.length===1)===(a<=1-b))}}
 return {checks,atomWords:W,results,scope:"native disjoint selector atoms, signed guards; full source witnesses verified; no universal guarded solver claimed"}
}
console.log(JSON.stringify(guardControl(),null,2));
