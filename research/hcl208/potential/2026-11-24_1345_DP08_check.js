function DP08(){
const stat={gaussian:0,xors:0,closure:0,pins:0,deleted:0,dualWords:0,fourier:0,reference:0,assertions:0,witnesses:0,counts:0};
const pow=n=>1n<<BigInt(n), bit=i=>pow(i), hi=x=>x.toString(2).length-1;
function check(x,msg){stat.assertions++;if(!x)throw Error(msg);}
function parity(x){let p=0;while(x){x&=x-1n;p^=1;}return p;}
function reduce(a,b,B){for(const [v,c] of B)if(a&bit(hi(v))){a^=v;b^=c;stat.xors++;}return [a,b];}
function insert(B,a,b){[a,b]=reduce(a,b,B);if(!a)return b? -1:0;B.push([a,b]);B.sort((x,y)=>hi(y[0])-hi(x[0]));return 1;}
function basis(rows){stat.gaussian++;let B=[];for(const [a,b] of rows)if(insert(B,a,b)<0)return null;return B;}
function hit(E,x){return E.every(([a,b])=>parity(a&x)===b);}
function legal(F,G,x){return hit(G,x)&&F.every(es=>es.every(e=>!hit(e,x)));}
function close(n,F,G){
 let B=basis(G);if(!B)return null;
 for(;;){stat.closure++;let out=[],forced=null;
 for(const es of F){let fs=[],bad=0n;
 for(const E of es){let A=basis(E.map(([a,b])=>reduce(a,b,B)));
 if(!A){stat.deleted++;continue;}if(!A.length)return null;
 if(A.length===1){forced=[A[0][0],A[0][1]^1];break;}
 fs.push(A);bad+=pow(n-B.length-A.length);}
 if(forced)break;
 if(bad===pow(n-B.length))return null;
 if(fs.length)out.push(fs);}
 if(forced){check(insert(B,...forced)===1,"strict closure");stat.pins++;continue;}
 return {B,F:out};}
}
function layout(F){
 let cols=[], spaces=[], owner=[];
 for(let i=0;i<F.length;i++){let A=basis(F[i].flat().map(([a])=>[a,0]));spaces.push(A);
 for(const [a] of A){cols.push(a);owner.push(i);}}
 let M=[],K=[];
 for(let j=0;j<cols.length;j++){let [a,c]=reduce(cols[j],bit(j),M);if(a){M.push([a,c]);M.sort((x,y)=>hi(y[0])-hi(x[0]));}else K.push(c);}
 let parent=F.map((_,i)=>i);
 function find(i){while(parent[i]!==i){i=parent[i];}return i;}
 function union(a,b){a=find(a);b=find(b);if(a!==b)parent[b]=a;}
 function owners(k){let s=[];for(let j=0;j<cols.length;j++)if(k&bit(j))s.push(owner[j]);return [...new Set(s)];}
 for(const k of K){let s=owners(k);for(const i of s)union(s[0],i);}
 let C=new Map();for(let i=0;i<F.length;i++){let p=find(i);if(!C.has(p))C.set(p,{is:[],ks:[]});C.get(p).is.push(i);}
 let U=[];for(const k of K){let s=owners(k);C.get(find(s[0])).ks.push(k);let w=F.map(()=>0n);for(let j=0;j<cols.length;j++)if(k&bit(j))w[owner[j]]^=cols[j];for(const a of w)insert(U,a,0);}
 return {cols,spaces,owner,K,C:[...C.values()],R:M.length,U:U.length};
}
function count(n,F,G=[]){
 stat.counts++;let cl=close(n,F,G);if(!cl)return {Z:0n,delta:null,U:null,A:0n,cl:null};
 let {B,F:H}=cl,L=layout(H),Z=pow(n-B.length-L.R),A=0n;
 for(const {is,ks} of L.C){let s=0n;A+=pow(ks.length);
 if(ks.length>22)throw Error("test cap");
 for(let t=0;t<2**ks.length;t++){stat.dualWords++;let k=0n;for(let j=0;j<ks.length;j++)if(t&(1<<j))k^=ks[j];
 let w=H.map(()=>0n);for(let j=0;j<L.cols.length;j++)if(k&bit(j))w[L.owner[j]]^=L.cols[j];
 let p=1n;for(const i of is){stat.fourier++;let r=L.spaces[i].length,v=w[i]?0n:pow(r);
 for(const E of H[i]){let [a,b]=reduce(w[i],0,E);if(!a)v-=(b?-1n:1n)*pow(r-E.length);}p*=v;}
 s+=p;}
 check(s%pow(ks.length)===0n&&s>=0n,"component count exact");Z*=s/pow(ks.length);}
 return {Z,delta:L.K.length,U:L.U,A,cl,L};
}
function witness(n,F,G,q){
 if(!q.Z)return null;let P=G.slice(),cur=q,limit=n+1;
 while(cur.cl&&cur.L.cols.length){if(--limit<0)throw Error("too many pins");
 let a=cur.L.cols[0],r=count(n,F,[...P,[a,0]]);
 P.push([a,r.Z?0:1]);cur=r.Z?r:count(n,F,P);check(cur.Z>0n,"positive branch");}
 let B=cur.cl.B,x=0n;
 for(const [a,b] of B.slice().reverse())if(parity(a&x)!==b)x^=bit(hi(a));
 check(legal(F,G,x),"original witness");stat.witnesses++;return x;
}
function brute(n,F,G){let c=0n;for(let x=0n;x<pow(n);x++){stat.reference++;if(legal(F,G,x))c++;}return c;}
const eq=(v,b)=>[bit(v),b], evt=(vs,b)=>vs.map(v=>eq(v,b)), cube=Array.from({length:8},(_,i)=>[[eq(0,i&1),eq(1,(i>>1)&1),eq(2,(i>>2)&1)]]);
const totals={};function test(name,n,F,G=[]){let q=count(n,F,G),z=brute(n,F,G);check(q.Z===z,"reference "+name);if(z)witness(n,F,G,q);let a=totals[name]??={sat:0,unsat:0};a[z?"sat":"unsat"]++;return q;}
for(let k=0;k<256;k++)test("cube",3,cube.filter((_,i)=>k&(1<<i)));
const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],fano=lines.map(v=>[evt(v,0),evt(v,1)]);
test("Fano",7,fano);for(let i=0;i<7;i++)for(let j=0;j<2;j++)test("Fano",7,fano.map((e,k)=>k===i?e.filter((_,l)=>l!==j):e));
let seed=2081345;function rand(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*k);}
for(let t=0;t<80;t++){let n=3+rand(4),F=Array.from({length:1+rand(7)},()=>[Array.from({length:1+rand(3)},()=>[BigInt(1+rand(2**n-1)),rand(2)])]);let G=Array.from({length:rand(3)},()=>[BigInt(1+rand(2**n-1)),rand(2)]);test("random",n,F,G);}
function cycle(m,priv=1,phase=0){let a=Array.from({length:m-1},(_,i)=>bit(i));a.push(pow(m-1)-1n);
return {n:m-1+m*priv,F:a.map((v,i)=>[[[v,i===m-1?phase:0],...Array.from({length:priv},(_,j)=>eq(m-1+i*priv+j,0))]])};}
const scales=[];for(const m of [4,8,16,32,64]){let {n,F}=cycle(m);let q=count(n,F);check(q.Z===(3n**BigInt(m)+1n)/2n,"scale count");check(q.delta===1&&q.U===m-1&&q.A===2n,"dual gap");witness(n,F,[],q);scales.push({m,n,delta:q.delta,U:q.U,credit:String(q.A),count:String(q.Z)});}
let {n,F}=cycle(8,2);let q=count(n,F),a=count(n,F,[eq(7,0)]),b=count(n,F,[eq(7,1)]);check(q.Z===a.Z+b.Z,"partition");check(q.delta===a.delta&&b.Z>0n&&a.Z>0n,"branch failure");
let dis=[[[eq(0,0),eq(1,0)]],[[eq(2,0),eq(3,0)]]];let d0=count(4,dis),d1=count(4,dis,[[bit(0)^bit(2),0]]);check(d0.delta===0&&d1.delta===1,"cross guard");
let copies=[];for(let c=0;c<32;c++){let {F}=cycle(4);for(let es of F)copies.push(es.map(E=>E.map(([a,b])=>[a<<BigInt(c*7),b])));}
let cq=count(224,copies);check(cq.delta===32&&cq.A===64n&&cq.Z===41n**32n,"component sum");
return {totals,scales,branch:{parent:{delta:q.delta,A:String(q.A)},zero:{delta:a.delta,A:String(a.A)},one:{delta:b.delta,A:String(b.A)}},cross:{before:d0.delta,after:d1.delta},copies:{delta:cq.delta,A:String(cq.A),count:String(cq.Z)},stat};
}
console.log(JSON.stringify(DP08(),null,2));
