/* P4SW12 independent exact JS controls, Node.js. */
function audit(){
 const D=[[0,0,5,1],[0,1,0,1],[2,1,1,0],[1,0,0,1],[1,0,1,0],[1,1,0,0],[2,2,3,3],[0,3,2,3],[2,4,3,2],[3,2,2,3],[3,2,3,2],[3,3,2,2],[4,3,5,5],[4,5,4,5],[4,5,5,4],[5,4,4,5],[5,4,1,4],[5,5,4,4]];
 const U=[[3,5,0,0],[2,0,4,2],[1,1,2,2],[0,5,1,3],[1,4,2,4],[5,0,4,5],[3,2,5,0],[0,4,2,2],[5,3,4,1],[4,2,0,0],[4,2,5,1],[0,4,1,4],[5,3,3,5],[2,1,3,3],[3,3,5,3],[2,0,3,5],[4,5,0,1],[1,1,1,4]];
 const ok=(x,m)=>{if(!x)throw Error(m)},bits=x=>x.toString(2).replace(/0/g,"").length,ix=(x,i)=>x>>i&1;
 function covers(T,skip=-1){let rows=Array(4*T.length/3).fill(0);T.forEach((t,j)=>t.forEach((v,c)=>rows[c*T.length/3+v]|=1<<j));ok(rows.every(x=>bits(x)===3),"degrees");let w=[];for(let z=0;z<1<<T.length;z++)if(bits(z)===T.length/3&&rows.every((x,i)=>i===skip||bits(x&z)===1))w.push(z);return w}
 let W=covers(D),P=covers(D,0),V=covers(U),Q=Array.from({length:16},(_,i)=>i).filter(i=>bits(i)===2).map(i=>[0,1,2,3].map(j=>ix(i,j)));
 ok(W.length===4&&P.length===4&&V.length===0,"core supports");ok(W.every(x=>ix(x,2)===ix(x,7)&&ix(x,16)===ix(x,0)),"port identities");ok(new Set(W.filter(x=>ix(x,1)).map(x=>ix(x,8))).size===2,"private variation");
 ok(Array.from({length:18},(_,i)=>new Set(W.map(x=>ix(x,i))).size).every(x=>x===2),"full support");
 let q=covers(Q,0);ok(q.length===3,"Q cap");
 // Enumerate all signed color multiplicity distributions for 1,2,3 cut edges.
 let patterns=[0,0,0,0],valid=[0,0,0,0];
 for(let k=1;k<=3;k++)for(let mask=0;mask<8**k;mask++){let a=mask,d=[0,0,0,0],cols=[];for(let j=0;j<k;j++){let x=a%8;a=Math.floor(a/8);d[x>>1]+=x%2?1:-1;cols.push(x)}patterns[k]++;if(!d.every(x=>x%3===0))continue;valid[k]++;ok(k!==1&&cols.every(x=>x>>1===cols[0]>>1)&&(k===2?cols[0]!==cols[1]:cols.every(x=>x===cols[0])),"cut classification")}
 let checks=0;for(let n=24;n<=600;n+=3)for(let s=12;s<=n/2;s+=3){ok(3n*BigInt(s+6)**6n+BigInt(n-s+6)**6n<=BigInt(n)**6n-1n,"recurrence");checks++}
 // Cycle-expanded 2x2 grid. Enumerate every matching, then rank projections of each choice of one owner per D block.
 let vs=[[0,0],[0,1],[1,0],[1,1]],ds=[[0,1],[1,0],[0,-1],[-1,0]],ls=[],rs=[],E=[];
 for(let v of vs){let ns=ds.map(([a,b])=>[v[0]+a,v[1]+b]).filter(([a,b])=>a>=0&&a<2&&b>=0&&b<2);for(let u of ns){ls.push([v,u]);rs.push([v,u])}}
 let key=x=>JSON.stringify(x),rmap=new Map(rs.map((x,i)=>[key(x),i]));
 for(let i=0;i<ls.length;i++){let [v,u]=ls[i],ns=ls.filter(x=>key(x[0])===key(v)).map(x=>x[1]),p=ns[(ns.findIndex(x=>key(x)===key(u))+ns.length-1)%ns.length];E.push([rmap.get(key([v,p])),rmap.get(key([u,v])),rmap.get(key([v,u]))])}
 let PM=[];function go(i,used,w){if(i===E.length){PM.push(w.slice());return}for(let j=0;j<3;j++){let r=E[i][j];if(!(used>>r&1)){w.push(j);go(i+1,used|1<<r,w);w.pop()}}}go(0,0,[]);
 // Ports 0,1,7 mapped to slot edges in a fixed order. Actual block owner2=port7, owner16=port0, owner8 varies within port1.
 let masks=PM.map(w=>w.map(j=>j===0?0:j===1?1:7));
 function rank(A,p){let a=A.map(x=>x.map(v=>(v%p+p)%p)),r=0;for(let j=0;j<(a[0]?.length||0)&&r<a.length;j++){let k=a.findIndex((x,i)=>i>=r&&x[j]);if(k<0)continue;[a[r],a[k]]=[a[k],a[r]];let v=a[r][j];for(let c=j;c<a[r].length;c++)a[r][c]=a[r][c]*(v===2&&p===3?2:1)%p;for(let i=r+1;i<a.length;i++){let d=a[i][j];for(let c=j;c<a[r].length;c++)a[i][c]=(a[i][c]-d*a[r][c]+p*p)%p}r++}return r}
 let count=0,min=99,dim=ls.length;
 for(let b=0;b<3**dim;b++){let x=b,c=[];for(let i=0;i<dim;i++){c.push(x%3);x=Math.floor(x/3)}let priv=c.filter(v=>v===1).length,sel=c.map((v,i)=>v===1?null:[i,v===0?7:0]).filter(Boolean),a=masks.map(w=>sel.map(([i,j])=>+(w[i]===j))),base=a[0],r=priv+rank(a.slice(1).map(v=>v.map((x,i)=>x-base[i])),3);ok(r>=Math.ceil(dim/3),"rank bound");min=Math.min(min,r);count++}
 return {core_covers:W.map(z=>Array.from({length:18},(_,i)=>i).filter(i=>ix(z,i))),U_covers:V.length,Q_cap_words:q.length,signed_cut_patterns:patterns,valid_patterns:valid,recurrence_checks:checks,macro_matchings:PM.length,owner_choices:count,min_GF3_rank:min,proved_bound:Math.ceil(dim/3)}
}
console.log(JSON.stringify(audit(),null,2));
