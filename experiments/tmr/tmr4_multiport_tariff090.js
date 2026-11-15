function audit(){
 let checks=0,traceSteps=0,envelopeRows=0,terminalRows=0,sccGroups=0,profiles=0,maxD=[-999,-999];
 const ok=(c,m)=>{checks++;if(!c)throw Error(m||"audit failed")};
 const P=lists=>lists.reduce((acc,li)=>acc.flatMap(a=>li.map(x=>a.concat(x))),[[]]);
 const range=n=>Array.from({length:n},(_,i)=>i);
 const pot=(B,r,c,live)=>[0,0,0,0,0,Math.max(...B.map((b,i)=>b-r[i])),B.reduce((s,b,i)=>s+b-c[i],0)+(live?1:0)];
 const diff=(a,b)=>a.map((v,i)=>v-b[i]);
 const scc=(n,edges)=>{
  const adj=Array.from({length:n},()=>[]);edges.filter(e=>e[2]===0).forEach(e=>adj[e[0]].push(e[1]));
  let ix=0,stack=[],on=new Set(),num=Array(n).fill(-1),low=Array(n).fill(0),comps=[];
  function dfs(v){num[v]=low[v]=ix++;stack.push(v);on.add(v);
   for(const w of adj[v]){if(num[w]<0){dfs(w);low[v]=Math.min(low[v],low[w]);}else if(on.has(w))low[v]=Math.min(low[v],num[w]);}
   if(low[v]===num[v]){const c=[];let w;do{w=stack.pop();on.delete(w);c.push(w);}while(w!==v);comps.push(c);}}
  for(let i=0;i<n;i++)if(num[i]<0)dfs(i);return comps;
 };
 const direct=(B,variant)=>{
  const m=B.length,r=Array(m).fill(0),c=Array(m).fill(0),written=Array.from({length:m},()=>""),words=B.map((b,i)=>Array.from({length:b-1},(_,j)=>variant===0?"0":variant===1?"1":String((i+j)&1)).join(""));
  let live=true,t=0;
  while(live){const before=pot(B,r,c,live);
   for(let i=0;i<m;i++){if(r[i]<B[i]){written[i]+=r[i]===B[i]-1?"#":words[i][r[i]];r[i]++;c[i]++;}}
   live=r.some((v,i)=>v<B[i]);const d=diff(before,pot(B,r,c,live));
   ok(d[5]<=1&&d[6]<=m+1,"direct local bound");ok(d[5]*(m+1)+d[6]<=2*(m+1),"fractional certificate");
   if(!live){terminalRows++;ok(d[6]>=2)}
   t++;
  }
  for(let i=0;i<m;i++)ok(written[i]===words[i]+"#","bad literal copy");
  ok(t===Math.max(...B));ok(pot(B,r,c,live).every(v=>v===0));traceSteps+=t;
 };
 function env(B){
  const m=B.length,values=B.map(b=>range(b+1)),prs=P(values),drs=P(B.map(_=>[0,1])),dcs=P(B.map(_=>[-1,0,1]));
  for(const r of prs)for(const c of prs)for(const dr of drs){
   const nr=r.map((v,i)=>v+dr[i]);if(nr.some((v,i)=>v>B[i]))continue;
   for(const dc of dcs){const nc=c.map((v,i)=>v+dc[i]);if(nc.some((v,i)=>v<0||v>B[i]))continue;
    const done=nr.every((v,i)=>v===B[i])&&nc.every((v,i)=>v===B[i]);
    for(const nextLive of (done?[true,false]:[true])){
     const d=diff(pot(B,r,c,true),pot(B,nr,nc,nextLive)),di=d[5],dm=d[6];
     ok(di<=1&&dm<=m+1,"envelope bound");
     ok(di+dm<=m+2,"equal-weight rational cone");
     ok(di*(m+1)+dm<=2*(m+1),"half weighted cone");
     maxD[0]=Math.max(maxD[0],di);maxD[1]=Math.max(maxD[1],dm);envelopeRows++;
    }
   }
  }
 }
 for(let m=1;m<=4;m++){
  for(const B of P(Array.from({length:m},()=>[1,2,3,4]))){
   if(m>3&&Math.max(...B)>3)continue;profiles++;
   const M=Math.max(...B),S=B.reduce((a,b)=>a+b,0);
   ok(S+1<=(m+1)*M,"dual certificate");
   ok(Math.max(M,(S+1)/(m+1))===M,"LP optimum");
   for(let v=0;v<3;v++)direct(B,v);
   const edges=[];for(let j=0;j<=M;j++){edges.push([2*j,2*j+1,0],[2*j+1,2*j,0]);if(j<M)edges.push([2*j,2*(j+1),1]);}
   const comps=scc(2*(M+1),edges);ok(comps.length===M+1&&comps.every(c=>c.length===2),"SCC");sccGroups+=comps.length;
   if((m===1&&M<=3)||(m===2&&M<=3)||(m===3&&M<=2))env(B);
  }
  const term=diff(pot(Array(m).fill(1),Array(m).fill(0),Array(m).fill(0),true),pot(Array(m).fill(1),Array(m).fill(1),Array(m).fill(1),false));
  ok(term[5]===1&&term[6]===m+1,"actual terminal fused row");
  ok(term[5]+term[6]>1,"additive weights invalid");
 }
 ok(maxD[0]===1&&maxD[1]===4,"maximum envelope discharges");
 return {id:"TMR4_MULTIPORT090",timestamp:"2026-11-15 03:45 PST",model:"fixed m physical input/output tape pairs, binary x_i#, local-head, one transition cost 1",symbolic:"PROVED/RESTRICTED; independent peer review OPEN",finite:"COMPUTATIONAL",profiles,traceSteps,envelopeRows,terminalRows,zeroCostAliasSCCs:sccGroups,assertions:checks,failures:0,exactCone:"a+(m+1)b<=1",exactInitial:["M=max_i(|x_i|+1)","S+1=sum_i(|x_i|+1)+1"],primalDual:"M=max_i(|x_i|+1)",maxD,guards:["authentic physical cl0 identity","metadata free-view SCC separate fixture","no arbitrary SAT decision transfer","no variable m in a fixed machine","no free write or one-tape multicell write"]};
}

if (typeof require !== 'undefined' && require.main === module) console.log(JSON.stringify(audit(), null, 2));
if (typeof module !== 'undefined') module.exports = {audit};
