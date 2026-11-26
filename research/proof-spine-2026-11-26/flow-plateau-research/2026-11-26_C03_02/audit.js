const audit = function audit(){
let checks=0;const A=(v,msg)=>{checks++;if(!v)throw Error(msg)};
const ints=Array.from({length:10},(_,i)=>i);
const internal=ints.filter(i=>i!==4).map(i=>[i,(i+1)%10]).concat([[4,7],[5,8],[6,9]]);
function localColor(p){let mask=Array(10).fill(0);for(let i=0;i<4;i++)mask[i]=1<<p[i];mask[4]=mask[5]=8;let c=[];
function rec(k){if(k===internal.length)return true;let [u,v]=internal[k];for(let i=1;i<=3;i++){let b=1<<i;if((mask[u]|mask[v])&b)continue;mask[u]|=b;mask[v]|=b;c[k]=i;if(rec(k+1))return true;mask[u]^=b;mask[v]^=b;}return false;}
A(rec(0),"patch coloring");return c.slice();}
let table={};for(let p of [[3,3,3,3],[1,1,3,3],[2,2,3,3],[3,1,1,3],[3,2,2,3]])table[p.join("")]=localColor(p);
function compile(F){
const r=F.length+4,events=[];
for(let j=0;j<r-1;j++)for(let k=0;k<2;k++)events.push({i:j,j:j+1,key:"p"+j,zero:false});
F.forEach((cl,h)=>{for(let z=0;z<3;z++)events.push({i:z,j:z+1,key:"x"+Math.abs(cl[z]),zero:cl[z]>0});events.push({swap:[3,4+h]});for(let z=2;z>=0;z--)events.push({i:z,j:z+1,key:"x"+Math.abs(cl[z]),zero:cl[z]>0});});
let G=[],group=new Map(),ends=[],count=0;const edge=(u,v,a,b,col)=>G.push({u,v,a,b,col});
for(let cp=0;cp<2;cp++){
let inits=Array(r).fill(-1),tails=Array(r).fill(-1);
for(let ev of events){if(ev.swap){let [i,j]=ev.swap;[tails[i],tails[j]]=[tails[j],tails[i]];continue;}
let base=10*count++,i=ev.i,j=ev.j,p=[i,j],q=ev.zero?[j,i]:[i,j];
if(i===0&&ev.zero){p.reverse();q.reverse();}
let ports=[p[0],q[0],p[1],q[1]],pc=ports.map(x=>x===0?cp+1:3),c=table[pc.join("")];A(!!c,"local port color");
for(let [k,[u,v]] of internal.entries())edge(base+u,base+v,k<9?1:0,k<9?(u%2===0?1:0):1,c[k]);
if(!group.has(ev.key))group.set(ev.key,[]);group.get(ev.key).push(base);
for(let k of [0,2]){let z=ports[k],u=base+k;if(tails[z]===-1)inits[z]=u;else edge(tails[z],u,0,1,pc[k]);}
for(let k of [1,3])tails[ports[k]]=base+k;
}
ends.push([inits,tails]);
}
for(let gs of group.values())for(let i=0;i<gs.length;i++)edge(gs[i]+5,gs[(i+1)%gs.length]+4,1,1,3);
let s=10*count,t=s+1,n=t+1;
for(let k=1;k<r;k++){edge(ends[0][0][k],ends[1][0][k],0,1,3);edge(ends[0][1][k],ends[1][1][k],0,1,3);}
for(let cp=0;cp<2;cp++){edge(s,ends[cp][0][0],0,1,cp+1);edge(t,ends[cp][1][0],0,1,cp+1);}edge(s,t,0,0,3);
let adj=Array.from({length:n},()=>[]),uniq=new Set();for(let [k,e] of G.entries()){A(e.u!==e.v,"loop");let id=Math.min(e.u,e.v)+":"+Math.max(e.u,e.v);A(!uniq.has(id),"duplicate");uniq.add(id);adj[e.u].push(k);adj[e.v].push(k);}
let comp=new Int32Array(n).fill(-1),sz=[],component=0;
const other=(e,u)=>e.u===u?e.v:e.u;
for(let u=0;u<n;u++){let es=adj[u].map(i=>G[i]);A(es.length===3,"cubic");A(new Set(es.map(e=>e.col)).size===3,"proper witness");A(es.reduce((z,e)=>z^e.a,0)===0&&es.reduce((z,e)=>z^e.b,0)===0,"flow");
if(comp[u]>=0)continue;let todo=[u],cnt=0;comp[u]=component;
for(let v of todo){cnt++;for(let i of adj[v])if(G[i].a){let w=other(G[i],v);if(comp[w]<0){comp[w]=component;todo.push(w);}}}sz.push(cnt);component++;}
let seen=new Set([0]),todo=[0];for(let u of todo)for(let i of adj[u]){let v=other(G[i],u);if(!seen.has(v)){seen.add(v);todo.push(v);}}A(seen.size===n,"connected");
let cls=new Map();for(let [key,bases] of group){let c=comp[bases[0]];A(!cls.has(c)&&sz[c]===10*bases.length,"class size");for(let base of bases)for(let z=0;z<10;z++)A(comp[base+z]===c,"physical equality");cls.set(c,key);}
A(sz.filter(z=>z===1).length===2&&sz[comp[s]]===1&&sz[comp[t]]===1,"isolates");
A(G.filter(e=>!e.a&&!e.b).length===1&&!G.at(-1).b,"defect");
return {G,adj,n,s,t,comp,cls,sz,other,group};
}
function evaluate(R,word){let {G,adj,n,s,t,comp,cls,other}=R;
let bit=G.map(e=>e.a?e.b^(word[cls.get(comp[e.u])]||0):e.b);
let visited=new Uint8Array(n),good=true,same=false,odd=0;
for(let u=0;u<n;u++){A(adj[u].reduce((a,k)=>a+bit[k],0)===2,"2-factor");if(visited[u])continue;let todo=[u];visited[u]=1;for(let v of todo)for(let k of adj[v])if(bit[k]){let w=other(G[k],v);if(!visited[w]){visited[w]=1;todo.push(w);}}
if(todo.length%2){good=false;odd++;}if(todo.includes(s))same=todo.includes(t);}
A(good===same,"terminal parity");A(odd===(good?0:2),"odd count");return good;}
const clauses=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>(i>>j&1)?v:-v));
const truth=(F,w)=>F.every(c=>c.some(l=>Boolean(w["x"+Math.abs(l)])===(l>0)));
let formulas=0,words=0,yes=0,accepted=0;
for(let mask=1;mask<256;mask++){let F=clauses.filter((_,i)=>mask>>i&1),R=compile(F),ok=false;formulas++;
for(let m=0;m<8;m++){let w={x1:m&1,x2:(m>>1)&1,x3:(m>>2)&1};let got=evaluate(R,w);A(got===truth(F,w),"formula equivalence");words++;if(got){accepted++;ok=true;}}if(ok)yes++;}
let full=compile([[1,-2,3]]),keys=[...full.group.keys()],allWords=0,allYes=0;for(let mask=0;mask<2**keys.length;mask++){let w={};keys.forEach((k,j)=>w[k]=(mask>>j)&1);let got=evaluate(full,w);A(got===truth([[1,-2,3]],w),"padding");allWords++;if(got)allYes++;}
return {formulas,words,yes,accepted,allWords,allYes,checks,localColorTable:table};
};
console.log(JSON.stringify(audit(),null,2));
