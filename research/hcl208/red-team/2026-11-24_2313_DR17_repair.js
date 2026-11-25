function repair(j){
const {registry:O,x,y}=j,n=x.length,d=0;
const A=O.filter(o=>o.p<2),B=O.filter(o=>o.p>=2);
const ok=(w,t)=>t.some(i=>w[i]!==w[t[0]]);
const flip=(w,J)=>w.map((v,i)=>v^Number(J.includes(i)));
const check=(a,b)=>A.every(o=>ok(a,o.t))&&B.every(o=>ok(b,o.t));
let startS=[1,2,31,34],a=flip(x,startS),b=flip(y,startS);if(!check(a,b))throw Error("bad jump");
let Q=[{a,b,path:[{s:"joint4",J:startS}]}],seen=new Set([a.join("")+b.join("")]),visits=0,edges=0,goal=null;
for(let idx=0;idx<Q.length&&idx<n*n&&!goal;idx++){let {a,b,path}=Q[idx];visits++;let d=a.findIndex((v,i)=>v!==b[i]);if(d<0){goal={a,path};break;}
function offer(s,J){edges++;let aa=s===1?a:flip(a,J),bb=s===0?b:flip(b,J);if(!check(aa,bb))return;if(aa.every((v,i)=>v===bb[i])){goal={a:aa,path:[...path,{s,J}]};return}let k=aa.join("")+bb.join("");if(!seen.has(k)&&Q.length<n*n){seen.add(k);Q.push({a:aa,b:bb,path:[...path,{s,J}]})}}
for(let s=0;s<2&&!goal;s++){offer(s,[d]);for(let i=0;i<n&&!goal;i++)if(i!==d)offer(s,[d,i]);}
for(let i=0;i<n&&!goal;i++)if(i!==d)offer(2,[i]);
}
// Exact target-mask encoding, solve both side choices via singleton Boolean propagation.
const minorities=O.map(o=>{let w=o.p<2?x:y;let m=o.t.find(i=>o.t.filter(k=>w[k]===w[i]).length===1);return {t:[m,...o.t.filter(i=>i!==m)],p:o.p}});
let jobs=[];
for(let side=0;side<2;side++){
let P=(side===0?A:B).filter(o=>o.t.includes(d)).map(o=>{let [u,v]=o.t.filter(i=>i!==d),w=side===0?x:y;return {u,v,b:1^w[u]^w[v]}});let nodes=0,scans=0,forces=0;
let R=minorities.map(o=>({t:o.t,bad:[[1,0,0],[0,1,1]]}));for(let {u,v,b} of P)R.push({t:[u,v],bad:[[0,1^b],[1,b]]});
function dfs(z){if(++nodes>100000)return null;z=z.slice();for(;;){let change=false;for(let o of R){scans++;for(let pat of o.bad){let unk=[];let inactive=false;for(let i=0;i<o.t.length;i++){let a=z[o.t[i]];if(a<0)unk.push(i);else if(a!==pat[i]){inactive=true;break}}if(inactive)continue;if(unk.length===0)return null;if(unk.length===1){let i=unk[0];z[o.t[i]]=1^pat[i];forces++;change=true;}}}if(!change)break}let i=z.indexOf(-1);if(i<0)return z;for(let v of [0,1]){let q=z.slice();q[i]=v;let a=dfs(q);if(a)return a}return null}
let z=Array(n).fill(-1);z[d]=0;let S=dfs(z);let target=null;if(S){let J=S.map((v,i)=>v?i:-1).filter(i=>i>=0);let aa=flip(x,J),bb=flip(y,J);if(!check(aa,bb))throw Error("mask failed");target=side===0?flip(aa,[d]):flip(bb,[d]);if(!O.every(o=>ok(target,o.t)))throw Error("target failed");}
jobs.push({side,P,nodes,scans,forces,mask:S,target});
}
return {jump:{startS,visits,edges,states:Q.length,goal},targetMask:jobs};
}
if(require.main===module)console.log(JSON.stringify(repair(JSON.parse(require("fs").readFileSync(process.argv[2],"utf8"))),null,2));
