function audit(){
 const A=(x,m)=>{if(!x)throw Error(m)},R={graphs:[],obstruction:null};
 function gp(n,k){let E=[];for(let i=0;i<n;i++)E.push([i,(i+1)%n],[i,n+i],[n+i,n+(i+k)%n]);return E}
 function all(n,E,drop,cb){
  let colors=E.map((_,i)=>drop.has(i)?-2:-1),used=Array(n).fill(0);let count=0;
  function rec(){let idx=-1,opts=0,sz=4;for(let i=0;i<E.length;i++)if(colors[i]===-1){let[a,b]=E[i],mask=7&~(used[a]|used[b]),cnt=(mask&1)+((mask>>1)&1)+((mask>>2)&1);if(cnt<sz){idx=i;sz=cnt;opts=mask;if(!cnt)return}}
   if(idx<0){count++;cb(colors.slice(),used.slice());return}
   let [a,b]=E[idx];for(let c=0;c<3;c++)if(opts&(1<<c)){let bit=1<<c;colors[idx]=c;used[a]|=bit;used[b]|=bit;rec();used[a]^=bit;used[b]^=bit;colors[idx]=-1}
  }rec();return count
 }
 function verify(n,E,c){let s=Array(n).fill(0);for(let i=0;i<E.length;i++){let[a,b]=E[i],bit=1<<c[i];A(c[i]>=0&&c[i]<3&&!(s[a]&bit)&&!(s[b]&bit),"restoration");s[a]|=bit;s[b]|=bit}A(s.every(x=>x===7),"all colors")}
 for(let [name,n,E] of [["K4",4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],["triangular prism",6,gp(3,1)],["Petersen",10,gp(5,2)],["pentagonal prism",10,gp(5,1)]]){
  let r={name,n,sourceColorings:all(n,E,new Set(),()=>{}),singleWords:0,starWords:0,twoDisjointWords:0,direct:0,kempe:0,blocked:0,starJobs:0};
  for(let v=0;v<n;v++){let ids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
   for(let z=1;z<8;z++){let del=ids.filter((_,i)=>(z>>i)&1);if(del.length===1&&E[del[0]][0]!==v)continue;r.starJobs++;
    all(n,E,new Set(del),(c,u)=>{r.starWords++;if(del.length===1)r.singleWords++;for(let i of del){let [a,b]=E[i],w=a===v?b:a,missing=7^u[w];A(missing===1||missing===2||missing===4,"leaf missing");c[i]=Math.log2(missing)}verify(n,E,c)})}
  }
  for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++){let [a,b]=E[i],[c,d]=E[j];if(new Set([a,b,c,d]).size!==4)continue;
   all(n,E,new Set([i,j]),(col,u)=>{r.twoDisjointWords++;let missing=v=>Math.log2(7^u[v]);let x=missing(a),y=missing(b),z=missing(c),w=missing(d);
    if(x===y&&z===w){r.direct++;col[i]=x;col[j]=z;verify(n,E,col);return}
    A(x!==y&&z!==w&&((x===z&&y===w)||(x===w&&y===z)),"four deficit parity");
    let adj=Array.from({length:n},()=>[]);E.forEach(([s,t],e)=>{if(col[e]===x||col[e]===y){adj[s].push([t,e]);adj[t].push([s,e])}});
    let v=a,prev=-1,path=[];do{let edge=adj[v].find(([,e])=>e!==prev);if(!edge)break;[v,prev]=edge;path.push(prev)}while(adj[v].length===2);
    A([b,c,d].includes(v),"terminal");
    if(v===b){r.blocked++;if(r.sourceColorings&&!R.obstruction)R.obstruction={name,n,edges:E,deleted:[i,j],colors:col,missing:[x,y,z,w],terminal:v,path};return}
    r.kempe++;for(let e of path)col[e]=col[e]===x?y:x;
    let miss=(v)=>{let m=0;E.forEach((e,k)=>{if(e.includes(v)&&col[k]>=0)m|=1<<col[k]});return Math.log2(7^m)};
    A(miss(a)===miss(b)&&miss(c)===miss(d),"Kempe repair");col[i]=miss(a);col[j]=miss(c);verify(n,E,col)
   })
  }R.graphs.push(r)
 }return R
}
console.log(JSON.stringify(audit(),null,2));
