function verify(chart,expected,cap=10000000){
 let work=0;const tick=(n=1)=>{work+=n;if(work>cap)throw Error("cap")},rows=new Map();
 function reduce(v){let rem=0n;while(v>1n){tick();const i=v.toString(2).length-1,b=rows.get(i);if(b)v^=b;else{const bit=1n<<BigInt(i);rem|=bit;v^=bit}}return rem|v}
 function admit(v){v=reduce(v);if(v===1n)throw Error("inconsistent");if(!v)return false;rows.set(v.toString(2).length-1,v);return true}
 const parity=chart.rows.map(({x})=>x[0]^x[1]^x[2]^x[3]);for(const v of parity)admit(v);const base=rows.size;
 const fs=[0n],idx=new Map([[0n,0]]),clauses=[],ownerForms=[];
 const get=v=>{const w=v&~1n;if(!idx.has(w)){idx.set(w,fs.length);fs.push(w)}return [idx.get(w),Number(v&1n)]};
 for(const {v,x} of chart.rows){const a=reduce(x[0]^x[1]),b=reduce(x[0]^x[2]);const ff=[get(a),get(b),get(a^b)];ownerForms.push([v,a,b]); // enumerate signed parity words rather than assume three clause formula
 for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let A=ff[i],B=ff[j];clauses.push([2*A[0]+(1^A[1]),2*B[0]+(1^B[1])]);}}
 const L=fs.length*2,G=Array.from({length:L},()=>new Set());G[1].add(0);
 const forbid=(a,b)=>{let old=G[a].size+G[b].size;G[a].add(b^1);G[b].add(a^1);return G[a].size+G[b].size>old};
 for(const [a,b] of clauses)forbid(a^1,b^1);
 const tri=[];for(let a=1;a<fs.length;a++)for(let b=a+1;b<fs.length;b++){tick();let c=idx.get(fs[a]^fs[b]);if(c>b)tri.push([a,b,c])}
 let passes=0,steps=[],reach;
 while(true){passes++;reach=G.map((_,a)=>{const visited=new Set([a]),q=[a];for(let j=0;j<q.length;j++)for(const b of G[q[j]]){tick();if(!visited.has(b)){visited.add(b);q.push(b)}}return visited});
 let changed=0;
 for(const [a,b,c] of tri)for(let x=0;x<2;x++)for(let y=0;y<2;y++){tick();let w=[2*a+x,2*b+y,2*c+(x^y)];let conflict=w.some(i=>w.some(j=>reach[i].has(j^1)));if(conflict){let n=0;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(forbid(w[i],w[j]))n++;if(n){changed+=n;steps.push([a,b,c,x,y])}}}
 if(!changed)break;
 }
 let eq=[];for(let i=1;i<fs.length;i++){for(let x=0;x<2;x++)if(reach[2*i+x].has(2*i+(x^1)))eq.push(fs[i]^BigInt(x^1));for(let j=1;j<i;j++){tick();for(let b=0;b<2;b++)if(reach[2*i].has(2*j+b)&&reach[2*j+b].has(2*i))eq.push(fs[i]^fs[j]^BigInt(b));}}
 const before=new Map(rows),admitted=[];for(const v of eq)if(admit(v))admitted.push(v.toString(16));
 const verified=expected.every(v=>reduce(BigInt("0x"+v))===0n),after=new Map(rows);
 // Original-owner observation-plane cut (not the coordinator's star-syndrome rank).
 function rank(vs){let m=new Map();for(let v of vs){v&=~1n;while(v){tick();let i=v.toString(2).length-1;if(m.has(i))v^=m.get(i);else{m.set(i,v);break}}}return m.size}
 const cuts=[];for(let f of [0.125,0.25,0.375,0.5,0.625,0.75,0.875]){let k=Math.floor(chart.rows.length*f);const item={k};for(const [name,b] of [["before",before],["after",after]]){rows.clear();for(const [i,v] of b)rows.set(i,v);const a=ownerForms.slice(0,k).flatMap(z=>[reduce(z[1]),reduce(z[2])]),c=ownerForms.slice(k).flatMap(z=>[reduce(z[1]),reduce(z[2])]);item[name]=rank(a)+rank(c)-rank([...a,...c]);}cuts.push(item)}
 rows.clear();for(const [i,v] of after)rows.set(i,v);
 return {verified,base,rank:after.size,forms:fs.length-1,triangles:tri.length,passes,steps,admitted,expected,work,cuts,sourceEquationSupports:expected.map(h=>{const v=BigInt("0x"+h),carriers=[];for(let i=0;i<chart.r;i++)if(v&(1n<<BigInt(i+1)))carriers.push(i);return {hex:h,constant:Number(v&1n),carriers,representativePorts:carriers.map(i=>chart.map.findIndex(([j,t])=>j===i&&t===0))}})};
}
module.exports={verify};
