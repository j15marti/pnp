const run = function(){
 const stats={pairs:0,projections:0,merges:0,closureScans:0,pins:0,massQueries:0,messages:0,peakKeys:0,witnesses:0,referenceWords:0,assertions:0};
 function ck(b){stats.assertions++;if(!b)throw Error("assertion "+stats.assertions)}
 function pc(x){let c=0;while(x){x&=x-1n;c++}return c}
 const bit=i=>1n<<BigInt(i);
 const key=(m,v)=>m+":"+v;
 function add(a,m,v,c){if(!c)return;let k=key(m,v),old=a.get(k);if(old){stats.merges++;c+=old.c}if(c)a.set(k,{m,v,c});else a.delete(k)}
 function finish(a,e){stats.peakKeys=Math.max(stats.peakKeys,a.size);return {a,e}}
 function one(){let a=new Map;add(a,0n,0n,1n);return finish(a,0)}
 function fac(f,deleted=false){let a=new Map;add(a,0n,0n,1n);if(!deleted&&f) add(a,f.m,f.v,-1n);return finish(a,0)}
 function mul(x,y){let a=new Map;for(const p of x.a.values())for(const q of y.a.values()){stats.pairs++;if(((p.v^q.v)&p.m&q.m)!==0n)continue;add(a,p.m|q.m,p.v|q.v,p.c*q.c)}return finish(a,x.e+y.e)}
 function proj(x,s,n){let a=new Map;for(const p of x.a.values()){stats.projections++;add(a,p.m&s,p.v&s,p.c<<BigInt(n-pc(p.m&~s)))}return finish(a,x.e+n)}
 function mass(x,n,m=0n,v=0n){stats.massQueries++;let t=0n;for(const p of x.a.values())if(((p.v^v)&p.m&m)===0n)t+=p.c<<BigInt(n-pc(p.m|m));return {t,e:x.e}}
 function cn(m){ck(m.t>=0n);let d=bit(m.e);ck(m.t%d===0n);return m.t/d}
 function clause(vars,bad){let m=0n,v=0n;vars.forEach((i,j)=>{m|=bit(i);if((bad>>j)&1)v|=bit(i)});return {m,v}}
 function setup(n,F,comb=false){
  let adj=F.map(()=>[]), root=-1;
  function link(a,b){adj[a].push(b);adj[b].push(a)}
  function join(a,b){let k=adj.length;adj.push([]);link(k,a);link(k,b);return k}
  function balanced(ids){if(ids.length===1)return ids[0];let h=ids.length>>1;return join(balanced(ids.slice(0,h)),balanced(ids.slice(h)))}
  if(comb){root=balanced(Array.from({length:14},(_,i)=>i));for(let i=14;i<F.length;i++)root=join(root,i)}
  else root=balanced(F.map((_,i)=>i));
  const scopes=new Map,msgs=new Map;
  function scope(a,b){let k=a+":"+b;if(scopes.has(k))return scopes.get(k);let s=a<F.length?(F[a]?.m??0n):0n;for(let c of adj[a])if(c!==b)s|=scope(c,a);scopes.set(k,s);return s}
  function cut(a,b){return scope(a,b)&scope(b,a)}
  function msg(a,b){let k=a+":"+b;if(msgs.has(k))return msgs.get(k);let x=a<F.length?fac(F[a]):one();for(let c of adj[a])if(c!==b)x=mul(x,msg(c,a));if(b>=0)x=proj(x,cut(a,b),n);msgs.set(k,x);stats.messages++;return x}
  function close(p,del){let changed=true;while(changed){changed=false;for(let i=0;i<F.length;i++){if(i===del||!F[i])continue;stats.closureScans++;let f=F[i];if(((p.v^f.v)&p.m&f.m)!==0n)continue;let rem=f.m&~p.m;if(!rem)return false;if((rem&(rem-1n))===0n){p.m|=rem;p.v=(p.v&~rem)|((~f.v)&rem);stats.pins++;changed=true;break}}}return true}
  function query(del=-1,witness=true){
    let p={m:0n,v:0n};let ok=close(p,del);
    let a=del<0?0:del,b=adj[a][0]??-1;
    let x=mul(fac(F[a],del===a),b<0?one():msg(b,a));
    let count=cn(mass(x,n));if(!ok)ck(count===0n);
    if(count===0n||!witness)return {count:String(count)};
    function choose(x,s){
      ck(mass(x,n,p.m&s,p.v&s).t>0n);
      for(let i=0;i<n;i++){let h=bit(i);if(!(s&h)||p.m&h)continue;
        let m=(p.m&s)|h,v=p.v&s;
        let z=mass(x,n,m,v).t;if(z===0n)v|=h;else ck(z>0n);
        p.m|=h;p.v=(p.v&~h)|(v&h);ck(close(p,del));
      }
    }
    function descend(a,b){
      let y=a<F.length?fac(F[a],a===del):one(),s=a<F.length?(F[a]?.m??0n):0n;
      for(let c of adj[a])if(c!==b){y=mul(y,msg(c,a));s|=cut(c,a)}
      if(b>=0)s|=cut(a,b);
      choose(y,s);for(let c of adj[a])if(c!==b)descend(c,a)
    }
    choose(x,F[a]?.m??0n);if(b>=0)descend(b,a);
    for(let i=0;i<F.length;i++)if(i!==del&&F[i])ck((p.v&F[i].m)!==F[i].v);
    stats.witnesses++;return {count:String(count),witness:String(p.v)}
  }
  return {query,msg,adj,root,scopes,msgs};
 }
 function ref(n,F,del){let c=0;for(let z=0;z<2**n;z++){stats.referenceWords++;let x=BigInt(z);if(F.every((f,i)=>i===del||!f||(x&f.m)!==f.v))c++}return c}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(t=>[clause(t,0),clause(t,7)]);
 const cases=[];let sat=0,unsat=0;
 function test(n,F,label){if(!F.length)F=[null];let s=setup(n,F);let counts=[];for(let d=-1;d<F.length;d++){let a=s.query(d),b=ref(n,F,d);ck(BigInt(a.count)===BigInt(b));if(b)sat++;else unsat++;counts.push(a.count)}cases.push({label,n,m:F.length,counts})}
 test(7,fano,"Fano");
 let cube=Array.from({length:8},(_,i)=>clause([0,1,2],i));
 for(let i=0;i<256;i++)test(3,cube.filter((_,j)=>i&(1<<j)),"cube-"+i);
 let seed=2081545;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 for(let i=0;i<40;i++){let F=[];for(let j=0;j<8+(i%7);j++){let ids=[];while(ids.length<3){let a=rnd()%7;if(!ids.includes(a))ids.push(a)}F.push(clause(ids,rnd()%8))}test(7,F,"random-"+i)}
 const scales=[];
 for(let k of [2,4,8,12]){
   let n=7+3*k,F=[...fano];
   for(let j=0;j<k;j++)F.push(clause([7+3*j,8+3*j,9+3*j],7));
   for(let j=0;j<k;j++)F.push(clause([7+3*j,8+3*j,9+3*j],0));
   let s=setup(n,F,true),r=s.root;let children=s.adj[r];for(let c of children)s.msg(c,r);
   let forwardMax=Math.max(...Array.from(s.msgs.values(),x=>x.a.size));
   // Edge between the Fano+broad prefix and its next comb parent.
   let prefix=s.adj[13+k][0],parent=s.adj[prefix].find(a=>a!==13+k&&a>=F.length&&s.adj[a].some(b=>b===14+k));
   ck(parent!==undefined);
   let rev=s.msg(parent,prefix).a.size;ck(rev===2**k);
   let base=s.query(-1,false),neighbor=s.query(0,false);
   ck(base.count==="0");ck(BigInt(neighbor.count)===5n*6n**BigInt(k));
   scales.push({k,n,forwardMax,reverseKeys:rev,base:base.count,neighbor:neighbor.count})
 }
 return {seed:2081545,counts:{sat,unsat,cases:cases.length},cases,scales,stats}
};


console.log(JSON.stringify(run(),null,2));
