function audit(){
let checks=0;function ck(v){checks++;if(!v)throw Error("assertion "+checks);}
const mask=pred=>{let a=0;for(let w=0;w<16;w++)if(pred(w>>3&1,w>>2&1,w>>1&1,w&1))a|=1<<w;return a};
const pop=x=>{let s=0;while(x){x&=x-1;s++}return s};
const B=mask((n,e,s,w)=>n===s&&e===w), INC=1<<6;
function grid(a,n){const k=n+2,g=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++){
if(i<n&&j>0&&j<=n)g.push(B|(a[i*n+j-1]?INC:0));
else if(j===0)g.push(mask((N,E,S,W)=>E===0&&(i===k-1?S===1:N===S)));
else if(j===k-1)g.push(mask((N,E,S,W)=>W===(i<n?1:0)&&(i===k-1?S===1:N===S)));
else g.push(B);
}return g}
function match(a,n){let p=Array(n).fill(-1);function dfs(i,seen){for(let j=0;j<n;j++)if(a[i*n+j]&&!seen[j]){seen[j]=1;if(p[j]<0||dfs(p[j],seen)){p[j]=i;return true}}return false}for(let i=0;i<n;i++)if(!dfs(i,Array(n).fill(0)))return null;let q=Array(n);p.forEach((i,j)=>q[i]=j);return q;}
function witness(q,n){let k=n+2,z=[],inverse=Array(n);q.forEach((j,i)=>inverse[j]=i);for(let i=0;i<k;i++)for(let j=0;j<k;j++){let N=0,E=0,S=0,W=0;if(i<n&&j>0&&j<=n){let c=j-1;N=+(inverse[c]<i);S=+(inverse[c]<=i);W=+(q[i]<c);E=+(q[i]<=c)}else if(j===0||j===k-1){W=+(j===k-1&&i<n);S=+(i===k-1)}else{N=S=1}z.push(8*N+4*E+2*S+W)}return z}
function verify(g,z,k){for(let i=0;i<k;i++)for(let j=0;j<k;j++){let t=i*k+j,w=z[t];if(!(g[t]>>w&1))return false;if(i===0&&(w>>3&1))return false;if(i===k-1&&!(w>>1&1))return false;if(j&&((z[t-1]>>2&1)!==(w&1)))return false;if(i&&((z[t-k]>>1&1)!==(w>>3&1)))return false}return true}
function dp(g,k){let north=new Set([0]);for(let i=0;i<k;i++){let next=new Set();for(let a of north){let states=new Set([0,1]);for(let j=0;j<k;j++){let temp=new Set();for(let v of states)for(let w=0;w<16;w++)if((g[i*k+j]>>w&1)&&(w&1)===(v&1)&&(w>>3&1)===(a>>j&1))temp.add((v&~1)|((w>>1&1)<<(j+1))|(w>>2&1));states=temp}for(let v of states)next.add(v>>1)}north=next}return north.has((1<<k)-1)}
function closure(g,k){let d=g.slice(),runs=0;const support=(m,p)=>{let r=0;for(let w=0;w<16;w++)if(m>>w&1)r|=1<<(w>>p&1);return r};let changed=true;while(changed){changed=false;runs++;for(let i=0;i<k;i++)for(let j=0;j<k;j++){let t=i*k+j,dom=[i? support(d[t-k],1):1,j===k-1?3:support(d[t+1],0),i===k-1?2:support(d[t+k],3),j?support(d[t-1],2):3];let m=d[t];for(let w=0;w<16;w++)if(m>>w&1){if(![3,2,1,0].every((p,h)=>dom[h]>>(w>>p&1)&1))m&=~(1<<w)}if(!m)return {ok:false,runs};if(m!==d[t]){d[t]=m;changed=true}}}return {ok:true,runs}}
function run(a,n,doDP){let k=n+2,g=grid(a,n),q=match(a,n),yes=!!q,cl=closure(g,k);ck(g.every(x=>pop(x)===4||pop(x)===5));ck(yes?cl.ok:true);if(doDP)ck(dp(g,k)===yes);if(yes){let z=witness(q,n);ck(verify(g,z,k));let trim=g.map((m,t)=>{if(pop(m)===5){for(let w=0;w<16;w++)if(w!==z[t]&&(m>>w&1))return m&~(1<<w)}return m});ck(trim.every(m=>pop(m)===4));ck(verify(trim,z,k));if(doDP)ck(dp(trim,k));}let upper=a.some(Boolean);ck(!yes||upper);return {yes,closure:cl.ok,upper}}
let exhaustive=[],hall=[];
for(let n=1;n<=3;n++){let yes=0,no=0,falseUpper=0,postClosureNo=0;for(let x=0;x<(1<<(n*n));x++){let a=Array.from({length:n*n},(_,i)=>x>>i&1);let r=run(a,n,true);if(r.yes)yes++;else{no++;if(r.upper)falseUpper++;if(r.closure)postClosureNo++}}exhaustive.push({n,yes,no,falseUpper,postClosureNo})}
for(let n=2;n<=4;n++){let maxima=[];for(let s=1;s<(1<<n);s++)for(let t=1;t<(1<<n);t++)if(pop(s)+pop(t)===n+1){let a=Array.from({length:n*n},(_,p)=>+!((s>>Math.floor(p/n)&1)&&(t>>(p%n)&1)));ck(!match(a,n));ck(a.some(Boolean));for(let p=0;p<a.length;p++)if(!a[p]){let b=a.slice();b[p]=1;ck(!!match(b,n))}maxima.push(a)}for(let i=0;i<maxima.length;i++)for(let j=0;j<maxima.length;j++){let excludes=!maxima[i].some((b,p)=>!b&&maxima[j][p]);ck(excludes===(i===j))}let actual=0;for(let x=0;x<(1<<(n*n));x++){let a=Array.from({length:n*n},(_,i)=>x>>i&1);if(match(a,n))continue;if(a.every((v,i)=>{if(v)return true;let b=a.slice();b[i]=1;return !!match(b,n)})){actual++;ck(maxima.some(b=>b.every((v,i)=>v===a[i])))}}ck(actual===maxima.length);hall.push({n,maximalNo:actual})}
let large=[];for(let n of [4,8,16,32,64,128]){let a=Array.from({length:n*n},(_,p)=>+(Math.floor(p/n)>=3||p%n<2));let b=a.slice();b[2*n+2]=1;let r=run(a,n,n<=4),s=run(b,n,n<=4);ck(!r.yes&&s.yes&&r.upper&&s.upper);large.push({n,gridCells:(n+2)**2,noClosureSurvives:r.closure,yes:s.yes})}
return {checks,exhaustive,hall,large,scope:"Exact native source table projection, DP independent for all n<=3 and neighbor n=4; augmenting paths, actual witness and domain closure at all scales; no circuit lower-bound experiment."}
}
console.log(JSON.stringify(audit(), null, 2));
