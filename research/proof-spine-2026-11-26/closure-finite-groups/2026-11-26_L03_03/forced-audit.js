function forcedAudit(){
let checks=0;function ck(x){checks++;if(!x)throw Error("failure "+checks)}
function solve(t,n){if(t.includes(0))return false;let rows=Array(n).fill(-1),cols=Array(n).fill(-1);for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(t[i*n+j]===2){if(rows[i]>=0||cols[j]>=0)return false;rows[i]=j;cols[j]=i}let p=Array(n).fill(-1);function dfs(i,seen){for(let j=0;j<n;j++)if(cols[j]<0&&(t[i*n+j]&2)&&!seen[j]){seen[j]=1;if(p[j]<0||dfs(p[j],seen)){p[j]=i;return true}}return false}for(let i=0;i<n;i++)if(rows[i]<0&&!dfs(i,Array(n).fill(0)))return false;return true}
function ref(t,n){function dfs(i,u){if(i===n)return true;for(let j=0;j<n;j++)if(!(u>>j&1)&&(t[i*n+j]&2)&&Array.from({length:n},(_,l)=>l===j||!!(t[i*n+l]&1)).every(Boolean)&&dfs(i+1,u|(1<<j)))return true;return false}return dfs(0,0)}
let result=[];for(let n=1;n<=3;n++){let yes=0;for(let x=0;x<4**(n*n);x++){let t=Array.from({length:n*n},(_,i)=>x>>(2*i)&3),a=solve(t,n);ck(a===ref(t,n));yes+=+a}result.push({n,yes,no:4**(n*n)-yes})}return {checks,result}}
console.log(JSON.stringify(forcedAudit(), null, 2));
