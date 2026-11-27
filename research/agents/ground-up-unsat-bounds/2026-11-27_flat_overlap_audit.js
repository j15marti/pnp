// Independent finite audit; run with node. No dependencies.
function pts(n,f){let out=[];for(let x=0;x<2**n;x++)if(f.every(([a,b])=>par(a&x)===b))out.push(x);return out}
function par(x){let b=0;while(x){b^=1;x&=x-1}return b}
function line(a,b,s=0){let f=[];for(let w=1;w<8;w++)if(!par(w&(a^b)))f.push([w<<s,par(w&a)]);return f}
function chain(t){let g=[],f=[];for(let j=0;j<t;j++){for(let [a,b] of [[0,1],[0,2],[3,4],[3,7]])f.push(g.concat(line(a,b,3*j)));g=g.concat(line(5,6,3*j))}return [3*t,f.concat([g])]}
function dense(t){let g=line(5,6),f=[[0,1],[2,4],[3,7]].map(([a,b])=>line(a,b));for(let j=0;j<t;j++)f.push(g.concat([[1<<(j+3),0]]));f.push(g.concat([[((1<<t)-1)<<3,0]]));return [t+3,f]}
function audit(n,f){let counts=new Uint16Array(2**n),privateCounts=[],sets=f.map(x=>pts(n,x));for(let s of sets)for(let x of s)counts[x]++;for(let s of sets)privateCounts.push(s.filter(x=>counts[x]===1).length);if(counts.some(c=>!c)||privateCounts.some(c=>!c))throw Error("cover/minimality");let S1=0,S2=0,max=0;for(let c of counts){S1+=c;S2+=c*(c-1)/2;max=Math.max(max,c)}return {n,m:f.length,S1,S2,max,privateMin:Math.min(...privateCounts)}}
function rank(rows){let b={};for(let [a,c] of rows){while(a){let p=31-Math.clz32(a);if(b[p]){a^=b[p][0];c^=b[p][1]}else{b[p]=[a,c];break}}if(!a&&c)return -1}return Object.keys(b).length}
function countIE(n,f){let s=0,v=0;function dfs(start,rows,sgn){for(let i=start;i<f.length;i++){let r=rows.concat(f[i]),k=rank(r);if(k<0)continue;v++;s+=sgn*2**(n-k);dfs(i+1,r,-sgn)}}dfs(0,[],1);return {count:s,visits:v}}
function run(){let out=[];for(let t=1;t<=4;t++){let [n,f]=chain(t),a=audit(n,f),b=countIE(n,f);if(b.count!==2**n||b.visits!==6*t+1||a.max!==2||a.S1-a.S2!==2**n)throw Error("chain");out.push({family:"chain",t,...a,...b})}for(let t of [2,4,6,8,10]){let [n,f]=dense(t),a=audit(n,f),b=countIE(n,f);if(b.count!==2**n||b.visits!==2**(t+1)+2)throw Error("dense");out.push({family:"dense",t,...a,...b})}return out}
if(typeof console!=="undefined")console.log(JSON.stringify(run(),null,2));
