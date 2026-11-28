function pg(d){let n=2**d-1,triples=[];for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++){let c=a^b;if(c>b)triples.push([a,b,c])}let F=triples.flatMap(t=>[t,t.map(x=>-x)]),dimacs=`p cnf ${n} ${F.length}\n`+F.map(c=>c.join(" ")+" 0\n").join("");return {nvars:n,dimacs,triples}}
function countCertificate(F){
 let groups=new Map(),X=[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b),work=0;for(let row of F){work+=row.length;let c=row.slice().sort((a,b)=>Math.abs(a)-Math.abs(b));if(c.length!==3||new Set(c.map(Math.abs)).size!==3)return {status:"REFUSE"};let k=c.map(Math.abs).join(",");if(!groups.has(k))groups.set(k,[]);groups.get(k).push(c)}
 let adj=new Map(X.map(x=>[x,[]])),pairs=new Map(),triples=[];
 for(let rs of groups.values()){if(rs.length!==2||rs[0].some((l,j)=>l!==-rs[1][j]))return {status:"REFUSE"};let c=rs[0],t=c.map(Math.abs);triples.push(t);for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=t[i],b=t[j],s=Number((c[i]>0)!==(c[j]>0)),k=a+","+b;work++;pairs.set(k,(pairs.get(k)||0)+1);adj.get(a).push([b,s]);adj.get(b).push([a,s])}}
 let gauge=new Map();for(let x of X)if(!gauge.has(x)){gauge.set(x,0);let q=[x];for(let a of q)for(let [b,s] of adj.get(a)){work++;let k=gauge.get(a)^s;if(!gauge.has(b)){gauge.set(b,k);q.push(b)}else if(gauge.get(b)!==k)return {status:"REFUSE_INCOHERENT"}}}
 let n=X.length,m=triples.length;if(pairs.size!==n*(n-1)/2||[...pairs.values()].some(c=>c!==1)||n<=4)return {status:"REFUSE_PAIR_COVER",n,m,work};
 return {status:"NO",n,m,square:n-2*m,gauge:[...gauge],triples,work}
}
function replay(F,cert){
 let k=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)).join(","),D=new Set(F.map(k)),g=new Map(cert.gauge),X=[...g.keys()],count=new Map(),ops=0;if(D.size!==2*cert.triples.length||D.size!==F.length)throw Error("row count");
 for(let t of cert.triples){let c=t.map(x=>g.get(x)?-x:x);if(!D.has(k(c))||!D.has(k(c.map(x=>-x))))throw Error("signed group");ops+=2;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let p=[t[i],t[j]].sort((a,b)=>a-b).join(",");count.set(p,(count.get(p)||0)+1);ops++}}
 for(let i=0;i<X.length;i++)for(let j=i+1;j<X.length;j++){ops++;if(count.get([X[i],X[j]].sort((a,b)=>a-b).join(","))!==1)throw Error("pair cover")}
 if(cert.square!==X.length-2*cert.triples.length||cert.square>=0)throw Error("nonnegative");return ops
}
module.exports={pg,countCertificate,replay};
