"use strict";
const seed=20261107; let state=seed;
function rnd(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
function bit(v){let p=0;while(v){p^=1;v&=v-1;}return p;}
function rank(rows,n){rows=rows.slice();let r=0;for(let c=0;c<n;c++){let j=r;while(j<n&&!((rows[j]>>>c)&1))j++;if(j===n)continue;[rows[r],rows[j]]=[rows[j],rows[r]];for(let k=0;k<n;k++)if(k!==r&&((rows[k]>>>c)&1))rows[k]^=rows[r];r++;}return r;}
function value(q,x){let y=0;for(let k=0;k<q.length;k++){let b=0;for(let e of q[k])b^=((x>>>e[0])&1)&((x>>>e[1])&1);y|=b<<k;}return y;}
function ranks(q,n){let out=[];for(let s=0;s<(1<<q.length);s++){let rows=Array(n).fill(0);for(let i=0;i<q.length;i++)if((s>>>i)&1)for(const [a,b] of q[i]){rows[a]^=1<<b;rows[b]^=1<<a;}let r=rank(rows,n);if(r%2)throw Error("odd polar rank");out.push(r);}return out;}
function boundScaled(q,n){let rs=ranks(q,n);let maxrank=Math.max(...rs)/2;let numerator=rs.reduce((v,r)=>v+(1<<(maxrank-r/2)),0)*(1<<(n-q.length));return [numerator,1<<maxrank,rs];}
function score(q,n,coeff,b){let total=0;for(let x=0;x<(1<<n);x++){let y=0;for(let i=0;i<q.length;i++)y|=(bit(coeff[i]&x)^((b>>>i)&1))<<i;if(y===value(q,x))total++;}return total;}
function assert(x,label){if(!x)throw Error(label);}
function run(){let checks=0,random=0,negative=0,walsh=0,affine=0;let controls=[];
function checkCase(name,q,n,expected){let [top,den,rs]=boundScaled(q,n);assert(top===expected*den,"bound "+name);checks++;let hits=score(q,n,Array(q.length).fill(0),0);assert(hits===expected,"hits "+name);checks++;controls.push({name,bound:expected,zero_template_agreements:hits,ranks:rs});}
for(let g=1;g<=3;g++){let q=Array.from({length:g},(_,i)=>[[2*i,2*i+1]]);checkCase("independentAND"+g,q,2*g,3**g);}
checkCase("overlap_u",[[[0,1]],[[0,2]]],3,5);
checkCase("duplicate",[[[0,1]],[[0,1]]],2,3);
checkCase("duplicate_plus_zero",[[[0,1]],[[0,1]],[]],3,6);
checkCase("affine_only",[[],[]],4,16);
for(let n=3;n<=6;n++)for(let m=1;m<=Math.min(n,4);m++)for(let trial=0;trial<75;trial++){
let q=Array.from({length:m},()=>{let terms=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rnd()&1)terms.push([i,j]);return terms;});
const [u,d,rs]=boundScaled(q,n);
for(let t=0;t<10;t++){let coeff=Array.from({length:m},()=>rnd()%(1<<n)),b=rnd()%(1<<m);assert(score(q,n,coeff,b)*d<=u,"rank agreement");affine++;}
if(n<=4)for(let s=0;s<(1<<m);s++)for(let a=0;a<(1<<n);a++){
let W=0;for(let x=0;x<(1<<n);x++)W+=(bit(s&value(q,x))^bit(a&x))?-1:1;
let expected=1<<(n-rs[s]/2);assert(Math.abs(W)===0||Math.abs(W)===expected,"Walsh amplitude");walsh++;}
random++;
}
let q=[[[0,1]],[[2,3]]],rs=ranks(q,4);assert(rs[0]===0,"zero character rank");negative++;
let exact=[];
for(const [name,q,n] of [["independentAND2",[[[0,1]],[[2,3]]],4],["overlap",[[[0,1]],[[0,2]]],3],["duplicate",[[[0,1]],[[0,1]]],2]]){
let biggest=0,ways=0,m=q.length,coeff=Array(m).fill(0),num=1<<n,total=1<<(m*(n+1));
for(let code=0;code<total;code++){let t=code,b=t&((1<<m)-1);t>>>=m;for(let i=0;i<m;i++){coeff[i]=t&(num-1);t>>>=n;}let cnt=score(q,n,coeff,b);if(cnt>biggest){biggest=cnt;ways=1;}else if(cnt===biggest)ways++;}
let [up,den]=boundScaled(q,n);assert(biggest*den===up,"exact exhaustive");exact.push({name,max:biggest,maximizers:ways,templates:total});checks++;
}
return {seed,classification:"COMPUTATIONAL, restricted rank-spectrum controls only",counts:{random_maps:random,affine_controls:affine,walsh_coefficients:walsh,negative_controls:negative,exact_control_checks:checks},controls,exact,limitations:"Not a native R_mix341 checker, all-rule bound, or P-vs-NP proof"};}
if(typeof require!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
