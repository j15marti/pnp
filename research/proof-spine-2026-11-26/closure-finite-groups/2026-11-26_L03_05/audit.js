function audit(){
const assert=(x,msg)=>{checks++;if(!x)throw Error(msg||"assertion")}; let checks=0;
const N=0,E=1,S=2,W=3, dr=[-1,0,1,0],dc=[0,1,0,-1],op=d=>(d+2)%4,b=(x,d)=>(x>>d)&1;
const mask=f=>{let a=0;for(let x=0;x<16;x++)if(f(x))a|=1<<x;return a};
const pop=x=>{let t=0;while(x){x&=x-1;t++}return t};
function layout(r){
 let t=2**r,m=Math.floor(t/r),w=r+2,temp=r,acc=r+1,ins=[{kind:"init"}],id=0;
 for(let j=0;j<r;j++)for(let i=0;i<m;i++)ins.push({kind:"input",dst:j,fn:"xor",id:id++});
 for(let a=0;a<t;a++){ins.push({kind:"reset",dst:temp});for(let j=0;j<r;j++)ins.push({kind:"binary",src:j,dst:temp,fn:((a>>j)&1)?"and":"andnot"});ins.push({kind:"input",dst:temp,fn:"and",id:id++});ins.push({kind:"binary",src:temp,dst:acc,fn:"or"})}
 ins.push({kind:"end",dst:acc});
 let H=Math.ceil(Math.sqrt(ins.length*w)),L=Math.ceil(ins.length/H),K=Math.max(H+2*w,L*w),a=new Int32Array(K*K),v=new Int32Array(K*K).fill(-1),alt=new Int32Array(K*K),used=new Uint8Array(K*K),routes=new Map();
 const idx=(i,j)=>i*K+j,baseline=(i,d)=>+(i===K-1&&d===S);
 function put(i,j,f,g,vi=-1){let q=idx(i,j);assert(!used[q],"cell reused");used[q]=1;a[q]=mask(f);alt[q]=g?mask(g):a[q];v[q]=vi;assert(pop(a[q])===4&&pop(alt[q])===4,"not exact4")}
 function wire(i,j,p,q){let f=[0,1,2,3].find(x=>x!==p&&x!==q);put(i,j,z=>b(z,p)===b(z,q)&&b(z,f)===baseline(i,f))}
 function val(f,x,y){if(f==="and")return x&y;if(f==="andnot")return x&(1-y);if(f==="or")return x|y;if(f==="xor")return x^y;throw Error("op")}
 for(let s=0;s<ins.length;s++){
   let lane=Math.floor(s/H),down=lane%2===0,i=w+(down?s%H:H-1-s%H),ci=lane*w,P=down?N:S,Q=down?S:N,I=ins[s];
   for(let j=0;j<w;j++){
     let c=ci+j;
     if(I.kind==="init"){put(i,c,z=>b(z,Q)===0&&b(z,E)===0);continue}
     if(I.kind==="end"){put(i,c,z=>b(z,E)===0&&(j===acc?b(z,P)===1:b(z,W)===0));continue}
     if(I.kind==="reset"&&j===I.dst){put(i,c,z=>b(z,Q)===1&&b(z,E)===0);continue}
     if(I.kind==="input"&&j===I.dst){let f=y=>z=>b(z,Q)===val(I.fn,b(z,P),y)&&b(z,E)===0;put(i,c,f(0),f(1),I.id);continue}
     if(I.kind==="binary"){
       let forward=I.src<I.dst,A=forward?E:W,B=forward?W:E;
       if(j===I.src){put(i,c,z=>b(z,P)===b(z,Q)&&b(z,P)===b(z,A));continue}
       if(j===I.dst){put(i,c,z=>b(z,Q)===val(I.fn,b(z,P),b(z,B))&&b(z,A)===0);continue}
       if(j>Math.min(I.src,I.dst)&&j<Math.max(I.src,I.dst)){put(i,c,z=>b(z,P)===b(z,Q)&&b(z,E)===b(z,W));continue}
     }
     wire(i,c,P,Q);
   }
 }
 function dir(a,b){let di=b[0]-a[0],dj=b[1]-a[1];let d=dr.findIndex((x,i)=>x===di&&dc[i]===dj);assert(d>=0,"nonadjacent");return d}
 for(let lane=0;lane<L-1;lane++){
   let down=lane%2===0,edge=w+(down?H-1:0),sgn=down?1:-1;
   for(let j=0;j<w;j++){
     let c=lane*w+j,target=c+w,turn=edge+sgn*(j+1),path=[[edge,c]];
     for(let i=edge+sgn;;i+=sgn){path.push([i,c]);if(i===turn)break}
     for(let x=c+1;x<=target;x++)path.push([turn,x]);
     for(let i=turn-sgn;;i-=sgn){path.push([i,target]);if(i===edge)break}
     for(let h=1;h<path.length-1;h++){let [i,c]=path[h],q=idx(i,c),ports=[dir(path[h],path[h-1]),dir(path[h],path[h+1])];assert(!used[q],"turn intersects register");if(!routes.has(q))routes.set(q,[]);routes.get(q).push(ports)}
   }
 }
 for(let [q,ps] of routes){let i=Math.floor(q/K),j=q%K;assert(ps.length<=2&&new Set(ps.flat()).size===2*ps.length,"routing conflict");if(ps.length===1)wire(i,j,...ps[0]);else put(i,j,z=>ps.every(([p,q])=>b(z,p)===b(z,q)))}
 for(let i=0;i<K;i++)for(let j=0;j<K;j++)if(!used[idx(i,j)])put(i,j,z=>b(z,N)===0&&b(z,E)===0);
 assert(id===r*m+t,"inputs");assert(v.filter(x=>x>=0).length===id,"one cell per input");
 return {r,t,m,w,H,L,K,a,v,alt,ins,id};
}
function ref(g,x){let z=0;for(let j=0;j<g.r;j++){let p=0;for(let i=0;i<g.m;i++)p^=x[j*g.m+i];z|=p<<j}return x[g.r*g.m+z]}
function solve(g,x){
 let K=g.K,d=Int32Array.from(g.a,(a,i)=>g.v[i]>=0&&x[g.v[i]]?g.alt[i]:a);
 let port=Array.from({length:4},(_,p)=>[mask(z=>b(z,p)===0),mask(z=>b(z,p)===1)]);
 let q=[],inq=new Uint8Array(d.length);
 function enqueue(i){if(!inq[i]){inq[i]=1;q.push(i)}}
 function narrow(i,m){let a=d[i]&m;if(a!==d[i]){d[i]=a;enqueue(i)}return a!==0}
 for(let j=0;j<K;j++){if(!narrow(j,port[N][0])||!narrow((K-1)*K+j,port[S][1]))return false}
 for(let i=0;i<d.length;i++)enqueue(i);
 for(let h=0;h<q.length;h++){let i=q[h];inq[i]=0;if(!d[i])return false;let row=Math.floor(i/K),col=i%K;for(let p=0;p<4;p++){let R=row+dr[p],C=col+dc[p];if(R<0||R>=K||C<0||C>=K)continue;let m=0;for(let z=0;z<2;z++)if(d[i]&port[p][z])m|=port[op(p)][z];if(!narrow(R*K+C,m))return false}}
 let words=new Uint8Array(d.length);
 for(let i=0;i<d.length;i++){let row=Math.floor(i/K),col=i%K;for(let p=0;p<4;p++){let R=row+dr[p],C=col+dc[p];let z=R>=0&&R<K&&C>=0&&C<K?+!(d[i]&port[p][0]&65535):+(p===S);if(R>=0&&R<K&&C>=0&&C<K){let j=R*K+C;assert(z===+!(d[j]&port[op(p)][0]),"support mismatch")}words[i]|=z<<p}assert(d[i]&(1<<words[i]),"joint witness failed")}
 return true;
}
let seed=26112605;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>31};
let results=[];
for(let r of [1,2,3,4,5,6,7,8,9]){
 let g=layout(r),yes=0,no=0,tests=r<=2?2**g.id:12;
 for(let j=0;j<tests;j++){
  let x=Array.from({length:g.id},(_,i)=>r<=2?(j>>i)&1:rnd());
  if(r>2){let z=0;for(let k=0;k<g.r;k++){let p=0;for(let i=0;i<g.m;i++)p^=x[k*g.m+i];z|=p<<k}x[g.r*g.m+z]=j%2}
  let want=ref(g,x),got=solve(g,x);assert(got===!!want,"decision mismatch");if(got)yes++;else no++;
 }
 results.push({r,inputs:g.id,side:g.K,cells:g.K*g.K,steps:g.ins.length,lanes:g.L,yes,no});
}
return {checks,seed:26112605,results};
}
console.log(JSON.stringify(audit(),null,2));
