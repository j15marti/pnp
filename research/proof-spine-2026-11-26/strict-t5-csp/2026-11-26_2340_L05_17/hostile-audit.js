function hostileAudit(){
const assert=(x,m)=>{if(!x)throw Error(m)};let out=[];
for(let a of [3,4,5]){let b=a,k=2*a-1,t=0,regions=[],arcs=[];for(let g=0;g<3;g++){let block=()=>Array.from({length:b},()=>t++),hub=block(),branches=[a,a+1,k+2].map(L=>({L,B:[hub,...Array.from({length:L-1},block)]}));regions.push({hub,branches});for(let {L,B} of branches)for(let j=0;j<L;j++)for(let x of B[j])for(let y of B[(j+1)%L])arcs.push([g,x,y])}
let long=regions[0].branches[2].B,cy=long.slice(0,k).map(x=>x[0]),extra=[0,cy[k-1],cy[0]],key=x=>x.join(","),base=new Set(arcs.map(key)),bad=arcs.concat([extra]);assert(!base.has(key(extra))&&bad.some(e=>!base.has(key(e))),"reject unverified extra arc");
let ordinary=new Set(cy),triples=[];for(let i=0;i<t;i++)if(!ordinary.has(i))triples.push([i,i,i]);let allowed=new Set(bad.map(key));for(let i=0;i<k;i++){let p=cy[i],q=cy[(i+1)%k];assert(allowed.has(key([0,p,q])),"arc");triples.push([p,t+i,t+i],[t+i,p,q])}let H=t+k;assert(triples.length===H&&[0,1,2].every(s=>new Set(triples.map(x=>x[s])).size===H&&triples.every(x=>x[s]>=0&&x[s]<H)),"hostile cover");out.push({a,k,extra,checks:bad.length,witnessSize:triples.length,recognized:false})}
return out
}
console.log(JSON.stringify(hostileAudit(),null,2));
