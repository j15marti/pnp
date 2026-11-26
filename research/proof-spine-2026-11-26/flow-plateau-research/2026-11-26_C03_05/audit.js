function audit(){
const out=[];
const pairs=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], old=[0,1,1,2,2,3];
for(const L of [0,1,2]){
 let E=[], f=[],n=4;
 function edge(u,v,c){E.push([u,v]);f.push(c);}
 for(let i=0;i<6;i++){
  let [u,v]=pairs[i],p=old[i],last=u;
  for(let j=0;j<(i===0?0:L);j++){
    let a=n++,b=n++,x=n++,y=n++;
    edge(last,a,p); let q=p===1?2:1,r=p^q;
    edge(a,x,q);edge(b,x,r);edge(a,y,r);edge(b,y,q);edge(x,y,p);last=b;
  }
  edge(last,v,p);
 }
 let incidence=Array.from({length:n},()=>[]);
 for(let i=0;i<E.length;i++) for(const v of E[i])incidence[v].push(i);
 if(!incidence.every(es=>es.length===3&&es.reduce((a,i)=>a^f[i],0)===0)||f.filter(x=>x===0).length!==1)throw Error("source");
 let m=E.length, labels=new Array(m).fill(0),used=new Array(n).fill(0),nodes=0,count=0,best=Infinity;
 function dfs(cost,remaining){
  nodes++;
  if(!remaining){count++;best=Math.min(best,cost);return;}
  let j=-1,mask=0,k=4;
  for(let i=0;i<m;i++)if(!labels[i]){
   let [u,v]=E[i],a=7&~(used[u]|used[v]),q=(a&1)+((a>>1)&1)+((a>>2)&1);
   if(q<k){j=i;mask=a;k=q;if(!k)return;}
  }
  let [u,v]=E[j];
  for(let c=1;c<=3;c++){let bit=1<<(c-1);if(mask&bit){labels[j]=c;used[u]|=bit;used[v]|=bit;dfs(cost+Number(c!==f[j]),remaining-1);used[u]^=bit;used[v]^=bit;labels[j]=0;}}
 }
 dfs(0,m);
 if(best!==8*L+3||count!==6*2**(5*L))throw Error("distance");
 out.push({L,n,edges:m,count,best,nodes});
}
return out;
}
console.log(JSON.stringify(audit(),null,2));
