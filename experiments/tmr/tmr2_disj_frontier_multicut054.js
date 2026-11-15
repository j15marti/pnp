// TMR-2/054 exact DISJ matching prefix and balanced multicut benchmark
// Revision tmr2-disj-frontier-multicut054.v1, seed 20261115.
// node experiments/tmr/tmr2_disj_frontier_multicut054.js
"use strict";
const result=(function(){
let checks=0,cuts=0,rankCases=0,prefixCases=0,pinEvaluations=0;
function ok(b,msg){checks++;if(!b)throw Error("FAILED "+msg);}
function choose(n,r){if(r<0||r>n)return 0n;let z=1n;for(let j=1;j<=r;j++)z=z*BigInt(n-j+1)/BigInt(j);return z;}
function bitCount(x){let c=0;while(x){x&=x-1;c++;}return c;}
function pairState(k,mask){let open=0,closed=0;for(let j=0;j<k;j++){let t=(mask>>(2*j))&3;if(t===1||t===2)open++;if(t===3)closed++;}return {open,closed};}
function evalMatching(k,mask){for(let j=0;j<k;j++)if(((mask>>(2*j))&3)===3)return 0;return 1;}
function coeff(k,a){let p=[1n];for(let j=0;j<k;j++){let v=j<a?4n:2n,q=Array(p.length+2).fill(0n);for(let i=0;i<p.length;i++){q[i]+=p[i];q[i+1]+=v*p[i];q[i+2]+=p[i];}p=q;}return p[k];}
function matrix(k,L,R){let rows=[],mat=[],cols=1<<R.length;for(let a=0;a<(1<<L.length);a++){let row=0n,m=[];for(let b=0;b<cols;b++){let z=0;for(let j=0;j<L.length;j++)if(a&(1<<j))z|=1<<L[j];for(let j=0;j<R.length;j++)if(b&(1<<j))z|=1<<R[j];let f=evalMatching(k,z);m.push(f);if(f)row|=1n<<BigInt(b);}rows.push(row);mat.push(m);}return {rows,mat,cols};}
function rank2(rows,cols){let piv=Array(cols).fill(0n),rank=0;for(let r of rows){for(let j=0;j<cols;j++){if(((r>>BigInt(j))&1n)===0n)continue;if(piv[j])r^=piv[j];else{piv[j]=r;rank++;break;}}}return rank;}
function rankMod(A,p){let a=A.map(x=>x.slice()),r=0;for(let c=0;c<a[0].length&&r<a.length;c++){let i=r;while(i<a.length&&a[i][c]===0)i++;if(i===a.length)continue;[a[i],a[r]]=[a[r],a[i]];let inv=1;while((inv*a[r][c])%p!==1)inv++;for(let j=c;j<a[0].length;j++)a[r][j]=(a[r][j]*inv)%p;for(let h=r+1;h<a.length;h++){let v=a[h][c];if(v)for(let j=c;j<a[0].length;j++)a[h][j]=(a[h][j]-v*a[r][j]%p+p)%p;}r++;}return r;}
function allOrders(a,fn){function rec(i){if(i===a.length){fn(a.slice());return;}for(let j=i;j<a.length;j++){[a[i],a[j]]=[a[j],a[i]];rec(i+1);[a[i],a[j]]=[a[j],a[i]];}}rec(0);}
let state=20261115>>>0;function rnd(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
function checkOrder(k,order){let mask=0,max=1;for(let t=0;t<=2*k;t++){if(t)mask|=1<<order[t-1];let {open,closed}=pairState(k,mask),q=(1<<open)+(closed?1:0);let M=matrix(k,order.slice(0,t),order.slice(t));ok(new Set(M.rows.map(String)).size===q,"cofactor classes "+k+"/"+t);ok(rank2(M.rows,M.cols)===(1<<open),"prefix GF2 rank "+k+"/"+t);prefixCases++;max=Math.max(max,q);}return max;}
function pins(k){let q=2*k,cl=[];for(let i=0;i<k;i++)cl.push([-(2*i+1),-(2*i+2),q+1]);for(let a=1;a<8;a++){let c=[];for(let j=0;j<3;j++)c.push(a&(1<<j)?-(q+j+1):q+j+1);cl.push(c);}ok(cl.length===k+7,"strict 3CNF clause count");for(let x=0;x<(1<<(2*k));x++){let count=0;for(let p=0;p<8;p++){let m=x|(p<<(2*k)),good=cl.every(c=>c.some(l=>((m>>(Math.abs(l)-1))&1)===(l>0?1:0)));count+=good?1:0;pinEvaluations++;}ok(count===evalMatching(k,x),"unique extension "+k+"/"+x);}}
let histogram=[],tariffs=[],enumerations=[],orderRuns=[],peaks={};
for(let k=1;k<=12;k++){
 let H=choose(2*k,k),A=coeff(k,k),sum=0n,total=0n,logsum=0n,dist={};
 for(let c=0;c<=k;c++){if((k-c)%2)continue;let z=choose(k,c)*(1n<<BigInt(c))*choose(k-c,(k-c)/2);dist[c]=String(z);total+=z;sum+=z*(1n<<BigInt(c));logsum+=BigInt(c)*z;}
 ok(total===H&&sum===A,"matching rank distribution "+k);
 ok(logsum*BigInt(2*k-1)===H*BigInt(k*k),"mean log rank "+k);
 let deltas=[],previous=H;for(let j=1;j<=k;j++){let now=coeff(k,j),d=now-previous;ok(d===2n*coeff(k-1,j-1),"activation coefficient "+k+"/"+j);if(j>1)ok(d>=deltas[j-2],"delta monotonic");deltas.push(d);previous=now;}
 ok(previous===A && A-H<=BigInt(k)*deltas[k-1],"linear optimal tariff "+k);
 histogram.push({k,balanced_cut_count:String(H),rank_sum:String(A),log2_rank_sum:String(logsum),distribution:dist});
 tariffs.push({k,activation_deltas:deltas.map(String),lambda_max_exact:"1/"+deltas[k-1],optimal_initial_surplus_exact:(A-H)+"/"+deltas[k-1],upper_bound:k});
 if(k<=6){let observed={},number=0,actual=0;for(let mask=0;mask<(1<<(2*k));mask++){if(bitCount(mask)!==k)continue;number++;let c=pairState(k,mask).open;observed[c]=(observed[c]||0)+1;
 if(k<=4){let L=[],R=[];for(let i=0;i<2*k;i++)((mask>>i)&1?L:R).push(i);let M=matrix(k,L,R);ok(rank2(M.rows,M.cols)===(1<<c),"balanced rank GF2");ok(rankMod(M.mat,101)===(1<<c),"balanced rank F101");actual++;rankCases+=2;}}
 cuts+=number;ok(BigInt(number)===H,"enumerate H "+k);for(let c=0;c<=k;c++)ok((observed[c]||0)===Number(dist[c]||"0"),"hist exhaustive "+k+"/"+c);enumerations.push({k,enumerated_balanced_cuts:number,actual_GF2_F101_matrix_pairs:actual});}
 if(k<=4)pins(k);
 let interleaved=Array.from({length:2*k},(_,i)=>i),grouped=[];for(let j=0;j<k;j++)grouped.push(2*j);for(let j=0;j<k;j++)grouped.push(2*j+1);
 function analyticPeak(o){let b=0,m=1;for(let j=0;j<=o.length;j++){if(j)b|=1<<o[j-1];let {open,closed}=pairState(k,b);m=Math.max(m,2**open+(closed?1:0));}return m;}
 let small=k<=4?checkOrder(k,interleaved):analyticPeak(interleaved),large=k<=4?checkOrder(k,grouped):analyticPeak(grouped);
 ok(small===(k===1?2:3)&&large===2**k,"order peaks "+k);peaks[k]={interleaved:small,grouped:large};
}
for(let k=1;k<=3;k++){let low=Infinity,high=0,num=0;allOrders(Array.from({length:2*k},(_,i)=>i),o=>{let a=checkOrder(k,o);low=Math.min(low,a);high=Math.max(high,a);num++;});ok(low===(k===1?2:3)&&high===2**k,"all orders extrema "+k);orderRuns.push({k,orders:num,minimum_peak:low,maximum_peak:high,exhaustive:true});}
let low=Infinity,high=0;for(let t=0;t<120;t++){let p=Array.from({length:8},(_,i)=>i);for(let i=7;i>0;i--){let j=rnd()%(i+1);[p[i],p[j]]=[p[j],p[i]];}let q=checkOrder(4,p);low=Math.min(low,q);high=Math.max(high,q);}orderRuns.push({k:4,orders:120,sampled_min:low,sampled_max:high,exhaustive:false,seed:20261115});
return {revision:"tmr2-disj-frontier-multicut054.v1",seed:20261115,method:"exact BigInt coefficients and exhaustive finite binary-matrix/cofactor controls",assertions:checks,enumerated_balanced_cuts:cuts,actual_field_rank_checks:rankCases,prefix_boundary_checks:prefixCases,pin_clause_truth_evaluations:pinEvaluations,failures:0,histogram,tariffs,enumberations:enumerations,orderRuns,analyticPeaks:peaks,qualification:"fixed-formula assignment indicator; restricted ordered read-once branching programs; symbolic activation calculus, NOT SAT-encoding decision time",limitations:"k<=3 exhaustive orders; k4 sampled; k<=4 explicit two-field cut ranks; k<=6 full cut enumerations; k<=12 exact coefficient identities; independent mathematical review open"};
})();
if(typeof module!=="undefined" && module.exports){module.exports=result;if(require.main===module)process.stdout.write(JSON.stringify(result,null,2)+"\n");}
