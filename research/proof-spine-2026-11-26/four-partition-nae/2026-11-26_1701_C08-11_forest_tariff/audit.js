function audit(){
let checks=0;function A(p,m){if(!p)throw Error(m);checks++}
const pop=x=>{let n=0;for(;x;x&=x-1)n++;return n};
const nae=(c,w,s=0)=>{let a=(w>>c[0]^s)&1,b=(w>>c[1]^s>>1)&1,d=(w>>c[2]^s>>2)&1;return a!==b||a!==d};
const lines=[];for(let r=0;r<3;r++)lines.push({p:0,v:[3*r,3*r+1,3*r+2]});for(let c=0;c<3;c++)lines.push({p:1,v:[c,3+c,6+c]});for(let s=1;s<=2;s++)for(let b=0;b<3;b++)lines.push({p:s+1,v:[0,1,2].map(r=>3*r+(s*r+b)%3)});
const retained=lines.filter((_,i)=>i!==0&&i!==3).map(x=>x.v);
function forest(cls){let d=Array.from({length:9+cls.length},(_,i)=>i);function root(i){while(d[i]!==i)i=d[i];return i}for(let i=0;i<cls.length;i++)for(let v of cls[i]){let a=root(9+i),b=root(v);if(a===b)return false;d[a]=b}return true}
function rank(cls,mask){let m=Array(9).fill(-1);function dfs(i,s){for(let v of cls[i])if((mask>>v&1)&&!s[v]){s[v]=1;if(m[v]<0||dfs(m[v],s)){m[v]=i;return true}}return false}return cls.reduce((n,_,i)=>n+Number(dfs(i,Array(9).fill(0))),0)}
let forestRegions=0,freeCases=0,signedCases=0,modelTests=0;
for(let subset=1;subset<1024;subset++){let cls=retained.filter((_,i)=>subset>>i&1);if(!forest(cls))continue;forestRegions++;
for(let mode=0;mode<2;mode++){let signs=cls.map((_,i)=>mode?((subset*13+i*5)&7):0),models=[];for(let w=0;w<512;w++){if(cls.every((c,i)=>nae(c,w,signs[i])))models.push(w);modelTests++}
for(let free=0;free<512;free++){let actual=new Set(models.map(w=>w&(511^free))).size===2**(9-pop(free));A(actual===(rank(cls,free)===cls.length),"forest matching mismatch");freeCases++;if(mode)signedCases++}}}
const B=1|2|4|8|64,I=511^B,models=[];for(let w=0;w<512;w++)if(retained.every(c=>nae(c,w)))models.push(w);
let support=[...new Set(models.map(w=>w&B))];A(models.length===2&&support.includes(0)&&support.includes(B),"cyclic equality");
let demand=9;for(let j=0;j<512;j++)if((j&B)===j){let fix=B^j;if(new Set(support.map(w=>w&fix)).size===2**pop(fix))demand=Math.min(demand,pop(j))}
A(demand===4&&rank(retained,I)===4,"cyclic demand");
function ring(k,yes){let F=[];for(let i=0;i<k;i++){for(let [idx,l] of lines.entries())if(idx!==0&&idx!==3)F.push({p:l.p,v:l.v.map(v=>9*i+v),id:12*i+idx});let j=(i+1)%k,sw=yes&&i<2?1-i:i;F.push({p:0,v:[9*i+1,9*sw+2,9*j],id:12*i});F.push({p:1,v:[9*i+3,9*sw+6,9*j],id:12*i+3})}return F}
function auth(F,n){let pair=new Set,ids=new Set,cnt=Array.from({length:4},()=>new Uint8Array(n));for(let {p,v,id} of F){A(!ids.has(id),"IDs");ids.add(id);A(new Set(v).size===3,"arity");for(let x of v)cnt[p][x]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=Math.min(v[i],v[j])*n+Math.max(v[i],v[j]);A(!pair.has(key),"linearity");pair.add(key)}}for(let p=0;p<4;p++)A(cnt[p].every(c=>c===1),"partition");let adj=Array.from({length:n},()=>[]);for(let {v} of F)for(let i=1;i<3;i++){adj[v[0]].push(v[i]);adj[v[i]].push(v[0])}let seen=new Set([0]),q=[0];for(let i=0;i<q.length;i++)for(let v of adj[q[i]])if(!seen.has(v)){seen.add(v);q.push(v)}A(q.length===n,"connected")}
let records=[];
for(let k of [3,5,9,17,33,65,129])for(let yes of [false,true]){
let F=ring(k,yes),n=9*k;auth(F,n);let immutable=JSON.stringify(F),chosen=null,tries=0,wordChecks=0;
for(let p=0;p<4&&!chosen;p++)for(let q=p+1;q<4&&!chosen;q++){tries++;let adj=Array.from({length:n},()=>[]);for(let l of F)if(l.p===p||l.p===q)for(let i=1;i<3;i++){adj[l.v[0]].push(l.v[i]);adj[l.v[i]].push(l.v[0])}let seen=new Set,groups=[];for(let x=0;x<n;x++)if(!seen.has(x)){let g=[x];seen.add(x);for(let i=0;i<g.length;i++)for(let y of adj[g[i]])if(!seen.has(y)){seen.add(y);g.push(y)}groups.push(g)}if(groups.some(g=>g.length!==9))continue;
let map=new Map;groups.forEach((g,i)=>g.forEach((v,j)=>map.set(v,[i,j])));let internal=groups.map(()=>[]),external=[];for(let l of F){let a=l.v.map(v=>map.get(v));if(a.every(x=>x[0]===a[0][0]))internal[a[0][0]].push(a.map(x=>x[1]));else external.push(l)}let supports=internal.map(cls=>{let m=[];for(let w=0;w<512;w++){wordChecks++;if(cls.every(c=>nae(c,w)))m.push(w)}return m});if(supports.every(m=>m.length===2&&(m[0]^m[1])===511))chosen={groups,map,internal,external,supports};}
A(chosen!==null,"geometry");let {groups,map,external,supports}=chosen,eq=groups.map(()=>[]),contr=false,ternary=0;
for(let l of external){let a=l.v.map(v=>{let [i,j]=map.get(v);return [i,(supports[i][0]>>j)&1]}),uniq=[...new Set(a.map(x=>x[0]))];if(a.some((x,i)=>a.some((y,j)=>i!==j&&x[0]===y[0]&&x[1]!==y[1])))continue;if(uniq.length===3){ternary++;continue}if(uniq.length===1){contr=true;continue}let x=a.find(x=>x[0]===uniq[0]),y=a.find(x=>x[0]===uniq[1]),b=1^x[1]^y[1];eq[x[0]].push([y[0],b]);eq[y[0]].push([x[0],b])}
let z=Array(k).fill(-1);for(let i=0;i<k;i++)if(z[i]<0){z[i]=0;let q=[i];for(let t=0;t<q.length;t++)for(let [j,b] of eq[q[t]]){let val=z[q[t]]^b;if(z[j]<0){z[j]=val;q.push(j)}else if(z[j]!==val)contr=true}}
A(!contr===yes,"label");if(!contr){let w=new Uint8Array(n);groups.forEach((g,i)=>g.forEach((v,j)=>w[v]=(supports[i][z[i]]>>j)&1));for(let l of F)A(new Set(l.v.map(x=>w[x])).size>1,"lift")}
A(JSON.stringify(F)===immutable,"source mutation");records.push({k,n,yes,rawDef:3*k,compactRepairDef:k,phaseVariables:k,wordChecks,tries,ternary})
}
return {checks,forestRegions,freeCases,signedCases,modelTests,cyclic:{models,support,demand,interiorRank:4,originalLocalDef:6,savings:2},records}
}
console.log(JSON.stringify(audit(),null,2));
