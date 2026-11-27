function run(){
 let checks=0;const ck=(x,s="")=>{checks++;if(!x)throw Error("check "+checks+" "+s)};
 const cap=200000, f=s=>"1".repeat(s.length)+"0"+s,b=x=>x.toString(2),key=r=>r.join(",");
 function catalogue(q){let st=[],map=new Map();for(let fl=0;fl<4;fl++)for(let a=0;a<5;a++){if(a>0&&(fl&(1<<Math.floor((a-1)/2))))continue;map.set([fl,a].join(","),st.length);st.push([fl,a])}
 let code=(fl,a,i)=>3+q*map.get([fl,a].join(","))+i,setup=[[0,1,0,0,1,1,1,1],[0,2,0,0,2,1,1,1],[0,0,0,2,0,0,0,0],[2,1,1,2,1,1,0,0],[2,2,1,2,2,1,0,0],[2,0,0,code(0,0,0),0,0,1,1]],cat=[];
 let sym=(fl,a,t)=>fl&(1<<t)?[0]:a===1+2*t?[0,1,2]:a===2+2*t?[0,1]:[1,2];
 for(let [fl,a] of st)for(let x of sym(fl,a,0))for(let y of sym(fl,a,1))for(let i=0;i<q;i++){let u=code(fl,a,i);
 for(let j=0;j<q;j++)cat.push({r:[u,x,y,code(fl,a,j),x,y,2,2],g:[fl,"S",i,j].join(",")});
 if(fl===3){cat.push({r:[u,x,y,1,x,y,2,2],g:["Z",i].join(",")});continue}
 for(let t=0;t<2;t++){if(fl&(1<<t)||a&&Math.floor((a-1)/2)!==t)continue;let s=t?y:x,k=-1,v=s,d=2,na=0,nf=fl;
 if(a===0||a===1+2*t){if(s===2){k=0;v=1;d=1;na=1+2*t}else if(s===1){k=1;v=2;d=0;na=2+2*t}else if(a!==0&&s===0){k=4;nf=fl|(1<<t)}}else if(a===2+2*t){if(s===1){k=2;d=0;na=a}else if(s===0){k=3;d=1;na=0}}
 if(k<0)continue;for(let j=0;j<q;j++){let dst=code(nf,na,j);cat.push({r:t?[u,x,y,dst,x,v,2,d]:[u,x,y,dst,v,y,d,2],g:[fl,t,k,i,j].join(",")})}}
 }return{setup,cat}}
 function build(q,G){let c=catalogue(q);return [...c.setup,...c.cat.filter(x=>G.has(x.g)).map(x=>x.r)]}
 function encode(rows,x,t,N=0){let z=f(rows.map(r=>r.map(v=>f(b(v))).join("")).join(""))+f(x)+f(b(t));return z+"0".repeat(Math.max(0,N-z.length))}
 function decode(w,h){let p=0;function get(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||2*k+1-j>s.length)throw Error("frame");return[s.slice(k+1,2*k+1-j),2*k+1-j]}let raw,x,t;[raw,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);ck(/^[01]+$/.test(x)&&/^0*$/.test(w.slice(p))&&/^(0|1[01]*)$/.test(t));let T=BigInt("0b"+t);ck(T<=BigInt(w.length)**BigInt(h));let rows=[],j=0;while(j<raw.length){let a=[];for(let k=0;k<8;k++){let s;[s,j]=get(raw,j);ck(/^(0|1[01]*)$/.test(s));a.push(parseInt(s,2))}rows.push(a)}return{w,rows,x,m:x.length,T}}
 function recognize(F,q){let c=catalogue(q),actual=new Set(F.rows.map(key)),G=new Set();for(let e of c.cat)if(actual.has(key(e.r)))G.add(e.g);let expected=new Set(build(q,G).map(key));if(expected.size!==actual.size||[...actual].some(x=>!expected.has(x)))return null;return G}
 function nval(F){let n=0n;for(let i=0;i<F.m;i++)if(F.x[i]==="1")n|=1n<<BigInt(i);return n}
 function H(m,n){let c=0n;for(let v=n;v;v>>=1n)c+=v&1n;return 4n*((1n<<BigInt(m))-1n-n)-BigInt(m)+2n*c+1n}
 function closure(F){if(F.m>=F.T.toString(2).length)return{NO:true,reason:"zero counter overflow needs >=2^m macros"};let n=nval(F),base=BigInt(2*F.m+3)+H(F.m,n)+H(F.m,0n);return{NO:base>F.T,base,n}}
 let inf=Infinity,mat=(q,fun=()=>inf)=>Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>fun(i,j))),id=q=>mat(q,(i,j)=>i===j?0:inf),mul=(a,b)=>mat(a.length,(i,j)=>Math.min(...a[i].map((v,k)=>v+b[k][j]))),vec=(v,a)=>a[0].map((_,j)=>Math.min(...v.map((x,i)=>x+a[i][j]))),same=(a,b)=>a.every((x,i)=>x===b[i]);
 function macros(F,q,G){let D=[];for(let fl=0;fl<4;fl++){let X=id(q);for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(G.has([fl,"S",i,j].join(",")))X[i][j]=Math.min(X[i][j],1);
 for(let k=0;k<q;k++)for(let i=0;i<q;i++)for(let j=0;j<q;j++)X[i][j]=Math.min(X[i][j],X[i][k]+X[k][j]);D.push(X);
 for(let i=0;i<q;i++){let ds=Array(q).fill(inf),Q=[i];ds[i]=0;for(let k=0;k<Q.length;k++)for(let j=0;j<q;j++)if(G.has([fl,"S",Q[k],j].join(","))&&ds[j]===inf){ds[j]=ds[Q[k]]+1;Q.push(j)}ck(same(ds,X[i]),"stationary closure")}}
 function mk(fl,t){let L=Array.from({length:5},(_,k)=>mul(D[fl],mat(q,(i,j)=>G.has([fl,t,k,i,j].join(","))?1:inf))),P=id(q),Q=id(q),M=[];for(let k=0;k<F.m;k++){M.push(mul(mul(mul(P,L[1]),Q),L[3]));P=mul(P,L[0]);Q=mul(Q,L[2])}M.push(mul(P,L[4]));return M}
 return{A:mk(0,0),B:mk(0,1),TA:mk(2,0),TB:mk(1,1),Z:D[3].map(row=>Math.min(...row.map((v,j)=>G.has(["Z",j].join(","))?v+1:inf)))}}
 function grid(F,q,G,rolling){let n=Number(nval(F)),L=2**F.m,A=L-n,B=L,M=macros(F,q,G),v=()=>Array(q).fill(inf),cost=0;
 let carry=(i,t)=>{let x=(t?0:n)+i+1;if(x===L)return F.m;let k=0;while(x%2===0){x/=2;k++}return k};
 // common transition examination cap, matrix acquisition outside recorded core and separately charged
 if(A>B||B>100000|| (A+1)*(B+1)>cap)return{status:"UNKNOWN",cost};
 let rows=rolling?null:Array.from({length:A+1},()=>Array.from({length:B+1},v));
 let row=rolling?Array.from({length:B+1},v):rows[0];row[0][0]=2*F.m+2;let ans=inf;
 for(let i=0;i<=A;i++){if(!rolling)row=rows[i];let next=rolling?Array.from({length:B+1},v):i<A?rows[i+1]:null;for(let j=0;j<=B;j++){let x=row[j];if(x.every(y=>y===inf))continue;if(i===A&&j===B){ans=Math.min(...x.map((y,u)=>y+M.Z[u]));continue}
 for(let t=0;t<2;t++){if(t?j===B:i===A)continue;if(cost+q*q>cap)return{status:"UNKNOWN",cost};cost+=q*q;let Y=t?(i===A?M.TB:M.B):(j===B?M.TA:M.A),z=vec(x,Y[carry(t?j:i,t)]),dest=t?row[j+1]:next[j];for(let u=0;u<q;u++)dest[u]=Math.min(dest[u],z[u])}}
 if(rolling)row=next}
 return{status:ans<=Number(F.T)?"YES":"NO",distance:Number.isFinite(ans)?ans:null,cost}}
 function raw(F,layered){let idx=new Map();for(let r of F.rows){let k=r.slice(0,3).join(",");if(!idx.has(k))idx.set(k,[]);idx.get(k).push(r)}let initial=[0,0,0,nval(F),0n,0],cost=0,rd=(p,v,L)=>p<0||p>=L?0:((v>>BigInt(p))&1n)?2:1;
 function step(z){let [s,p1,p2,v1,v2,l]=z,out=[];for(let r of idx.get([s,rd(p1,v1,F.m),rd(p2,v2,l)].join(","))||[]){cost++;if(cost>cap)throw Error("cap");let a=v1,c=v2,L=l;if(p1>=0&&p1<F.m){let bit=1n<<BigInt(p1);a=r[4]===2?a|bit:a&~bit}if(p2===L&&r[5])L++;if(p2>=0&&p2<L){let bit=1n<<BigInt(p2);c=r[5]===2?c|bit:c&~bit}out.push([r[3],p1+[-1,1,0][r[6]],p2+[-1,1,0][r[7]],a,c,L])}return out}
 try{let Q=[initial],seen=new Set([key(initial)]);if(layered){for(let t=0;t<=Number(F.T);t++){if(Q.some(z=>z[0]===1))return{status:"YES",distance:t,cost};if(!Q.length||t===Number(F.T))break;let next=new Map();for(let z of Q)for(let y of step(z))next.set(key(y),y);Q=[...next.values()]}return{status:"NO",cost}}
 for(let k=0;k<Q.length;k++){let z=Q[k];if(z[0]===1)return{status:z[6]<=Number(F.T)?"YES":"NO",distance:z[6],cost};let d=z[6]||0;if(d>=Number(F.T))continue;for(let y of step(z)){let s=key(y);if(!seen.has(s)){seen.add(s);Q.push([...y,d+1])}}}return{status:"NO",cost};
 }catch(e){if(e.message==="cap")return{status:"UNKNOWN",cost:cap};throw e}}
 // raw BFS key excludes depth (step destructures first six); initial at depth zero, acceptance never at initial
 let seed=352177;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 let data=[],summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}},mutants=0;
 function test(rows,q,x,t,tag,expect){let word=encode(rows,x,BigInt(t)),Fs=Array.from({length:4},()=>decode(word,4)),Gs=Fs.map(F=>recognize(F,q));ck(Gs.every(Boolean));ck(Fs.every(F=>F.w===word));ck(Gs.every(G=>G.size===Gs[0].size&&[...G].every(g=>Gs[0].has(g))));
 let cl=Fs.map(closure);ck(cl.every(C=>C.NO===cl[0].NO&&C.base===cl[0].base));
 let A=cl[0].NO?{status:"NO",cost:0}:grid(Fs[0],q,Gs[0],false),B=cl[1].NO?{status:"NO",cost:0}:raw(Fs[1],false),C=cl[2].NO?{status:"NO",cost:0}:raw(Fs[2],true);
 // integrated imports only exact group set and compulsory bound; independently re-close and use rolling grid
 let I=cl[3].NO?{status:"NO",cost:0}:grid(Fs[3],q,Gs[3],true);let vals={A,B,C,I},def=Object.values(vals).filter(a=>a.status!=="UNKNOWN");ck(def.every(a=>a.status===def[0].status),"replica mismatch");if(expect)ck(def.every(a=>a.status===expect),"known answer");for(let [k,a] of Object.entries(vals))summary[k][a.status]++;
 data.push({tag,q,m:x.length,N:word.length,t,base:cl[0].base?.toString(),...vals});
 }
 function graphGroups(q,E){let G=new Set(["Z,"+(q-1)]);for(let fl=0;fl<3;fl++)for(let t=0;t<2;t++)for(let k=0;k<5;k++)G.add([fl,t,k,0,0].join(","));for(let [i,j] of E)G.add([3,"S",i,j].join(","));return G}
 let graphTests=0,graphYes=0;
 for(let z=0;z<72;z++){let q=2+z%5,E=[];for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(rnd()<.28)E.push([i,j]);let dist=Array(q).fill(inf),Q=[0];dist[0]=0;for(let k=0;k<Q.length;k++)for(let [i,j] of E)if(i===Q[k]&&dist[j]===inf){dist[j]=dist[i]+1;Q.push(j)}let rows=build(q,graphGroups(q,E));test(rows,q,"0",13+q-1,"ST",""+(dist[q-1]<inf?"YES":"NO"));graphTests++;if(dist[q-1]<inf){graphYes++;test(rows,q,"0",13+dist[q-1]-1,"ST-1","NO");test(rows,q,"0",13+dist[q-1],"ST-exact","YES")}}
 for(let z=0;z<40;z++){let q=2+z%2,m=1+z%4,G=new Set();for(let fl=0;fl<4;fl++)for(let i=0;i<q;i++)for(let j=0;j<q;j++){if(rnd()<.33)G.add([fl,"S",i,j].join(","));if(fl<3)for(let t=0;t<2;t++)for(let k=0;k<5;k++)if(rnd()<.65)G.add([fl,t,k,i,j].join(","))}for(let i=0;i<q;i++)if(rnd()<.7)G.add(["Z",i].join(","));if(z%4===0){for(let fl=0;fl<3;fl++)for(let t=0;t<2;t++)for(let k=0;k<5;k++)G.add([fl,t,k,0,0].join(","));G.add("Z,0")}
 let x=Array.from({length:m},()=>rnd()<.5?"0":"1").join(""),rows=build(q,G),n=nval({m,x}),base=Number(BigInt(2*m+3)+H(m,n)+H(m,0n));test(rows,q,x,base+z%5,"random");test(rows,q,x,base-1,"base-1","NO");
 if(z<8){let i=rows.findIndex((r,i)=>i>=6);if(i>=0){let mut=rows.slice();mut.splice(i,1);let F=decode(encode(mut,x,0n),4);if(!recognize(F,q))mutants++;}}}
 for(let m of [16,64,256,1024]){let q=2,rows=build(q,graphGroups(q,[[0,1]]));test(rows,q,"0".repeat(m),100,"clock-precheck","NO")}
 return{checks,graphTests,graphYes,mutants,summary,cases:data.length,data,cap,scope:"sequential copies; same numerical core candidate-transition cap but different primitive units; preprocessing separately counted symbolically; no measured bit-operation equivalence; q supplied in tests; full recognizer search proved separately"};
}
console.log(JSON.stringify(run(),null,2));
