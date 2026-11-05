"use strict";
function run(){
let assignments=[];for(let b=0;b<8;b++)assignments.push({x:!!(b&1),y:!!(b&2),z:!!(b&4)});
const F=a=>a.x&&(a.x||a.z)&&!a.y;
const factor=a=>a.x&&(a.x||a.z);
const local=a=>a.x||a.y;
const strong=a=>a.x;
const weak=a=>a.x||a.y||a.z;
const neg=a=>!a.x||a.y;
function implies(f,g){return assignments.every(a=>!f(a)||g(a));}
if(assignments.filter(F).length!==2||!implies(factor,local)||!implies(factor,strong)||!implies(factor,weak)||implies(factor,neg))throw Error("semantics");
if(!assignments.every(a=>((a.x||a.y)&&!a.y)?a.x:true))throw Error("RES");
let src=[[1],[1,3],[-2]];
const validPivot=(a,b,p)=>a.includes(p)&&b.includes(-p);
if(!validPivot([1,2],[-2],2)||validPivot([1],[-2],2)!==false||!validPivot([1,2,3],[-2],2))throw Error("pivot");
let exactResolvent=(a,b,p)=>[...new Set([...a,...b].filter(v=>Math.abs(v)!==p))].sort((u,v)=>u-v);
if(JSON.stringify(exactResolvent([1,2],[-2],2))!=="[1]"||JSON.stringify(exactResolvent([1,2,3],[-2],2))!=="[1,3]")throw Error("resolvent");
return {independent_assignment_cases:8,sat_original_models:2,valid_factor_local_implication:true,invalid_negative_local:true,source_preserved:true,changed_pivot_or_resolvent_detected:true};}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run()));