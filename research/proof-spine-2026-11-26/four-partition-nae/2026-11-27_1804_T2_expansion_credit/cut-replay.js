function cutCheck(O,p,flow){
 if(flow.status!=="UNSAT")return null;
 let J=new Set(flow.sinkSideOwners),V=new Set(flow.sourceSideCarriers),map=new Map(),demand=0,cross=0,otherDemand=0;
 for(let o of O){demand+=o.d;if(!J.has(o.id))otherDemand+=o.d;for(let l of o.lits){let v=Math.abs(l),s=+(l<0);if(p.has(v)&&p.get(v)!==1-s)continue;let c=map.get(v)||[0,0];c[s]++;map.set(v,c);if(J.has(o.id)&&V.has(v))cross++}}
 let cut=otherDemand+cross;for(let [v,c] of map)if(!V.has(v))cut+=p.has(v)?c[1-p.get(v)]:Math.max(...c);
 if(cut!==flow.cut||cut>=demand)throw Error("cut replay invalid");return{cut,demand,owners:J.size,verified:true};
}
module.exports=cutCheck;
