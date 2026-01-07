function _S(o,e){for(var i=0;i<e.length;i++){const r=e[i];if(typeof r!="string"&&!Array.isArray(r)){for(const l in r)if(l!=="default"&&!(l in o)){const c=Object.getOwnPropertyDescriptor(r,l);c&&Object.defineProperty(o,l,c.get?c:{enumerable:!0,get:()=>r[l]})}}}return Object.freeze(Object.defineProperty(o,Symbol.toStringTag,{value:"Module"}))}function vS(o){return o&&o.__esModule&&Object.prototype.hasOwnProperty.call(o,"default")?o.default:o}var Xf={exports:{}},Ao={};var g0;function xS(){if(g0)return Ao;g0=1;var o=Symbol.for("react.transitional.element"),e=Symbol.for("react.fragment");function i(r,l,c){var h=null;if(c!==void 0&&(h=""+c),l.key!==void 0&&(h=""+l.key),"key"in l){c={};for(var d in l)d!=="key"&&(c[d]=l[d])}else c=l;return l=c.ref,{$$typeof:o,type:r,key:h,ref:l!==void 0?l:null,props:c}}return Ao.Fragment=e,Ao.jsx=i,Ao.jsxs=i,Ao}var _0;function SS(){return _0||(_0=1,Xf.exports=xS()),Xf.exports}var ZA=SS(),kf={exports:{}},ie={};var v0;function MS(){if(v0)return ie;v0=1;var o=Symbol.for("react.transitional.element"),e=Symbol.for("react.portal"),i=Symbol.for("react.fragment"),r=Symbol.for("react.strict_mode"),l=Symbol.for("react.profiler"),c=Symbol.for("react.consumer"),h=Symbol.for("react.context"),d=Symbol.for("react.forward_ref"),m=Symbol.for("react.suspense"),p=Symbol.for("react.memo"),v=Symbol.for("react.lazy"),g=Symbol.for("react.activity"),S=Symbol.iterator;function M(U){return U===null||typeof U!="object"?null:(U=S&&U[S]||U["@@iterator"],typeof U=="function"?U:null)}var A={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},C=Object.assign,y={};function x(U,et,gt){this.props=U,this.context=et,this.refs=y,this.updater=gt||A}x.prototype.isReactComponent={},x.prototype.setState=function(U,et){if(typeof U!="object"&&typeof U!="function"&&U!=null)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,U,et,"setState")},x.prototype.forceUpdate=function(U){this.updater.enqueueForceUpdate(this,U,"forceUpdate")};function P(){}P.prototype=x.prototype;function N(U,et,gt){this.props=U,this.context=et,this.refs=y,this.updater=gt||A}var L=N.prototype=new P;L.constructor=N,C(L,x.prototype),L.isPureReactComponent=!0;var B=Array.isArray;function F(){}var z={H:null,A:null,T:null,S:null},Q=Object.prototype.hasOwnProperty;function R(U,et,gt){var bt=gt.ref;return{$$typeof:o,type:U,key:et,ref:bt!==void 0?bt:null,props:gt}}function D(U,et){return R(U.type,et,U.props)}function k(U){return typeof U=="object"&&U!==null&&U.$$typeof===o}function rt(U){var et={"=":"=0",":":"=2"};return"$"+U.replace(/[=:]/g,function(gt){return et[gt]})}var at=/\/+/g;function ut(U,et){return typeof U=="object"&&U!==null&&U.key!=null?rt(""+U.key):et.toString(36)}function ht(U){switch(U.status){case"fulfilled":return U.value;case"rejected":throw U.reason;default:switch(typeof U.status=="string"?U.then(F,F):(U.status="pending",U.then(function(et){U.status==="pending"&&(U.status="fulfilled",U.value=et)},function(et){U.status==="pending"&&(U.status="rejected",U.reason=et)})),U.status){case"fulfilled":return U.value;case"rejected":throw U.reason}}throw U}function O(U,et,gt,bt,Bt){var tt=typeof U;(tt==="undefined"||tt==="boolean")&&(U=null);var ct=!1;if(U===null)ct=!0;else switch(tt){case"bigint":case"string":case"number":ct=!0;break;case"object":switch(U.$$typeof){case o:case e:ct=!0;break;case v:return ct=U._init,O(ct(U._payload),et,gt,bt,Bt)}}if(ct)return Bt=Bt(U),ct=bt===""?"."+ut(U,0):bt,B(Bt)?(gt="",ct!=null&&(gt=ct.replace(at,"$&/")+"/"),O(Bt,et,gt,"",function(It){return It})):Bt!=null&&(k(Bt)&&(Bt=D(Bt,gt+(Bt.key==null||U&&U.key===Bt.key?"":(""+Bt.key).replace(at,"$&/")+"/")+ct)),et.push(Bt)),1;ct=0;var Dt=bt===""?".":bt+":";if(B(U))for(var Vt=0;Vt<U.length;Vt++)bt=U[Vt],tt=Dt+ut(bt,Vt),ct+=O(bt,et,gt,tt,Bt);else if(Vt=M(U),typeof Vt=="function")for(U=Vt.call(U),Vt=0;!(bt=U.next()).done;)bt=bt.value,tt=Dt+ut(bt,Vt++),ct+=O(bt,et,gt,tt,Bt);else if(tt==="object"){if(typeof U.then=="function")return O(ht(U),et,gt,bt,Bt);throw et=String(U),Error("Objects are not valid as a React child (found: "+(et==="[object Object]"?"object with keys {"+Object.keys(U).join(", ")+"}":et)+"). If you meant to render a collection of children, use an array instead.")}return ct}function V(U,et,gt){if(U==null)return U;var bt=[],Bt=0;return O(U,bt,"","",function(tt){return et.call(gt,tt,Bt++)}),bt}function nt(U){if(U._status===-1){var et=U._result;et=et(),et.then(function(gt){(U._status===0||U._status===-1)&&(U._status=1,U._result=gt)},function(gt){(U._status===0||U._status===-1)&&(U._status=2,U._result=gt)}),U._status===-1&&(U._status=0,U._result=et)}if(U._status===1)return U._result.default;throw U._result}var Mt=typeof reportError=="function"?reportError:function(U){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var et=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof U=="object"&&U!==null&&typeof U.message=="string"?String(U.message):String(U),error:U});if(!window.dispatchEvent(et))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",U);return}console.error(U)},xt={map:V,forEach:function(U,et,gt){V(U,function(){et.apply(this,arguments)},gt)},count:function(U){var et=0;return V(U,function(){et++}),et},toArray:function(U){return V(U,function(et){return et})||[]},only:function(U){if(!k(U))throw Error("React.Children.only expected to receive a single React element child.");return U}};return ie.Activity=g,ie.Children=xt,ie.Component=x,ie.Fragment=i,ie.Profiler=l,ie.PureComponent=N,ie.StrictMode=r,ie.Suspense=m,ie.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=z,ie.__COMPILER_RUNTIME={__proto__:null,c:function(U){return z.H.useMemoCache(U)}},ie.cache=function(U){return function(){return U.apply(null,arguments)}},ie.cacheSignal=function(){return null},ie.cloneElement=function(U,et,gt){if(U==null)throw Error("The argument must be a React element, but you passed "+U+".");var bt=C({},U.props),Bt=U.key;if(et!=null)for(tt in et.key!==void 0&&(Bt=""+et.key),et)!Q.call(et,tt)||tt==="key"||tt==="__self"||tt==="__source"||tt==="ref"&&et.ref===void 0||(bt[tt]=et[tt]);var tt=arguments.length-2;if(tt===1)bt.children=gt;else if(1<tt){for(var ct=Array(tt),Dt=0;Dt<tt;Dt++)ct[Dt]=arguments[Dt+2];bt.children=ct}return R(U.type,Bt,bt)},ie.createContext=function(U){return U={$$typeof:h,_currentValue:U,_currentValue2:U,_threadCount:0,Provider:null,Consumer:null},U.Provider=U,U.Consumer={$$typeof:c,_context:U},U},ie.createElement=function(U,et,gt){var bt,Bt={},tt=null;if(et!=null)for(bt in et.key!==void 0&&(tt=""+et.key),et)Q.call(et,bt)&&bt!=="key"&&bt!=="__self"&&bt!=="__source"&&(Bt[bt]=et[bt]);var ct=arguments.length-2;if(ct===1)Bt.children=gt;else if(1<ct){for(var Dt=Array(ct),Vt=0;Vt<ct;Vt++)Dt[Vt]=arguments[Vt+2];Bt.children=Dt}if(U&&U.defaultProps)for(bt in ct=U.defaultProps,ct)Bt[bt]===void 0&&(Bt[bt]=ct[bt]);return R(U,tt,Bt)},ie.createRef=function(){return{current:null}},ie.forwardRef=function(U){return{$$typeof:d,render:U}},ie.isValidElement=k,ie.lazy=function(U){return{$$typeof:v,_payload:{_status:-1,_result:U},_init:nt}},ie.memo=function(U,et){return{$$typeof:p,type:U,compare:et===void 0?null:et}},ie.startTransition=function(U){var et=z.T,gt={};z.T=gt;try{var bt=U(),Bt=z.S;Bt!==null&&Bt(gt,bt),typeof bt=="object"&&bt!==null&&typeof bt.then=="function"&&bt.then(F,Mt)}catch(tt){Mt(tt)}finally{et!==null&&gt.types!==null&&(et.types=gt.types),z.T=et}},ie.unstable_useCacheRefresh=function(){return z.H.useCacheRefresh()},ie.use=function(U){return z.H.use(U)},ie.useActionState=function(U,et,gt){return z.H.useActionState(U,et,gt)},ie.useCallback=function(U,et){return z.H.useCallback(U,et)},ie.useContext=function(U){return z.H.useContext(U)},ie.useDebugValue=function(){},ie.useDeferredValue=function(U,et){return z.H.useDeferredValue(U,et)},ie.useEffect=function(U,et){return z.H.useEffect(U,et)},ie.useEffectEvent=function(U){return z.H.useEffectEvent(U)},ie.useId=function(){return z.H.useId()},ie.useImperativeHandle=function(U,et,gt){return z.H.useImperativeHandle(U,et,gt)},ie.useInsertionEffect=function(U,et){return z.H.useInsertionEffect(U,et)},ie.useLayoutEffect=function(U,et){return z.H.useLayoutEffect(U,et)},ie.useMemo=function(U,et){return z.H.useMemo(U,et)},ie.useOptimistic=function(U,et){return z.H.useOptimistic(U,et)},ie.useReducer=function(U,et,gt){return z.H.useReducer(U,et,gt)},ie.useRef=function(U){return z.H.useRef(U)},ie.useState=function(U){return z.H.useState(U)},ie.useSyncExternalStore=function(U,et,gt){return z.H.useSyncExternalStore(U,et,gt)},ie.useTransition=function(){return z.H.useTransition()},ie.version="19.2.3",ie}var x0;function Vo(){return x0||(x0=1,kf.exports=MS()),kf.exports}var w_=Vo();const Po=vS(w_),jA=_S({__proto__:null,default:Po},[w_]);var Wf={exports:{}},Ro={},qf={exports:{}},Yf={};var S0;function yS(){return S0||(S0=1,(function(o){function e(O,V){var nt=O.length;O.push(V);t:for(;0<nt;){var Mt=nt-1>>>1,xt=O[Mt];if(0<l(xt,V))O[Mt]=V,O[nt]=xt,nt=Mt;else break t}}function i(O){return O.length===0?null:O[0]}function r(O){if(O.length===0)return null;var V=O[0],nt=O.pop();if(nt!==V){O[0]=nt;t:for(var Mt=0,xt=O.length,U=xt>>>1;Mt<U;){var et=2*(Mt+1)-1,gt=O[et],bt=et+1,Bt=O[bt];if(0>l(gt,nt))bt<xt&&0>l(Bt,gt)?(O[Mt]=Bt,O[bt]=nt,Mt=bt):(O[Mt]=gt,O[et]=nt,Mt=et);else if(bt<xt&&0>l(Bt,nt))O[Mt]=Bt,O[bt]=nt,Mt=bt;else break t}}return V}function l(O,V){var nt=O.sortIndex-V.sortIndex;return nt!==0?nt:O.id-V.id}if(o.unstable_now=void 0,typeof performance=="object"&&typeof performance.now=="function"){var c=performance;o.unstable_now=function(){return c.now()}}else{var h=Date,d=h.now();o.unstable_now=function(){return h.now()-d}}var m=[],p=[],v=1,g=null,S=3,M=!1,A=!1,C=!1,y=!1,x=typeof setTimeout=="function"?setTimeout:null,P=typeof clearTimeout=="function"?clearTimeout:null,N=typeof setImmediate<"u"?setImmediate:null;function L(O){for(var V=i(p);V!==null;){if(V.callback===null)r(p);else if(V.startTime<=O)r(p),V.sortIndex=V.expirationTime,e(m,V);else break;V=i(p)}}function B(O){if(C=!1,L(O),!A)if(i(m)!==null)A=!0,F||(F=!0,rt());else{var V=i(p);V!==null&&ht(B,V.startTime-O)}}var F=!1,z=-1,Q=5,R=-1;function D(){return y?!0:!(o.unstable_now()-R<Q)}function k(){if(y=!1,F){var O=o.unstable_now();R=O;var V=!0;try{t:{A=!1,C&&(C=!1,P(z),z=-1),M=!0;var nt=S;try{e:{for(L(O),g=i(m);g!==null&&!(g.expirationTime>O&&D());){var Mt=g.callback;if(typeof Mt=="function"){g.callback=null,S=g.priorityLevel;var xt=Mt(g.expirationTime<=O);if(O=o.unstable_now(),typeof xt=="function"){g.callback=xt,L(O),V=!0;break e}g===i(m)&&r(m),L(O)}else r(m);g=i(m)}if(g!==null)V=!0;else{var U=i(p);U!==null&&ht(B,U.startTime-O),V=!1}}break t}finally{g=null,S=nt,M=!1}V=void 0}}finally{V?rt():F=!1}}}var rt;if(typeof N=="function")rt=function(){N(k)};else if(typeof MessageChannel<"u"){var at=new MessageChannel,ut=at.port2;at.port1.onmessage=k,rt=function(){ut.postMessage(null)}}else rt=function(){x(k,0)};function ht(O,V){z=x(function(){O(o.unstable_now())},V)}o.unstable_IdlePriority=5,o.unstable_ImmediatePriority=1,o.unstable_LowPriority=4,o.unstable_NormalPriority=3,o.unstable_Profiling=null,o.unstable_UserBlockingPriority=2,o.unstable_cancelCallback=function(O){O.callback=null},o.unstable_forceFrameRate=function(O){0>O||125<O?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):Q=0<O?Math.floor(1e3/O):5},o.unstable_getCurrentPriorityLevel=function(){return S},o.unstable_next=function(O){switch(S){case 1:case 2:case 3:var V=3;break;default:V=S}var nt=S;S=V;try{return O()}finally{S=nt}},o.unstable_requestPaint=function(){y=!0},o.unstable_runWithPriority=function(O,V){switch(O){case 1:case 2:case 3:case 4:case 5:break;default:O=3}var nt=S;S=O;try{return V()}finally{S=nt}},o.unstable_scheduleCallback=function(O,V,nt){var Mt=o.unstable_now();switch(typeof nt=="object"&&nt!==null?(nt=nt.delay,nt=typeof nt=="number"&&0<nt?Mt+nt:Mt):nt=Mt,O){case 1:var xt=-1;break;case 2:xt=250;break;case 5:xt=1073741823;break;case 4:xt=1e4;break;default:xt=5e3}return xt=nt+xt,O={id:v++,callback:V,priorityLevel:O,startTime:nt,expirationTime:xt,sortIndex:-1},nt>Mt?(O.sortIndex=nt,e(p,O),i(m)===null&&O===i(p)&&(C?(P(z),z=-1):C=!0,ht(B,nt-Mt))):(O.sortIndex=xt,e(m,O),A||M||(A=!0,F||(F=!0,rt()))),O},o.unstable_shouldYield=D,o.unstable_wrapCallback=function(O){var V=S;return function(){var nt=S;S=V;try{return O.apply(this,arguments)}finally{S=nt}}}})(Yf)),Yf}var M0;function ES(){return M0||(M0=1,qf.exports=yS()),qf.exports}var Zf={exports:{}},Cn={};var y0;function TS(){if(y0)return Cn;y0=1;var o=Vo();function e(m){var p="https://react.dev/errors/"+m;if(1<arguments.length){p+="?args[]="+encodeURIComponent(arguments[1]);for(var v=2;v<arguments.length;v++)p+="&args[]="+encodeURIComponent(arguments[v])}return"Minified React error #"+m+"; visit "+p+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function i(){}var r={d:{f:i,r:function(){throw Error(e(522))},D:i,C:i,L:i,m:i,X:i,S:i,M:i},p:0,findDOMNode:null},l=Symbol.for("react.portal");function c(m,p,v){var g=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:l,key:g==null?null:""+g,children:m,containerInfo:p,implementation:v}}var h=o.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function d(m,p){if(m==="font")return"";if(typeof p=="string")return p==="use-credentials"?p:""}return Cn.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=r,Cn.createPortal=function(m,p){var v=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!p||p.nodeType!==1&&p.nodeType!==9&&p.nodeType!==11)throw Error(e(299));return c(m,p,null,v)},Cn.flushSync=function(m){var p=h.T,v=r.p;try{if(h.T=null,r.p=2,m)return m()}finally{h.T=p,r.p=v,r.d.f()}},Cn.preconnect=function(m,p){typeof m=="string"&&(p?(p=p.crossOrigin,p=typeof p=="string"?p==="use-credentials"?p:"":void 0):p=null,r.d.C(m,p))},Cn.prefetchDNS=function(m){typeof m=="string"&&r.d.D(m)},Cn.preinit=function(m,p){if(typeof m=="string"&&p&&typeof p.as=="string"){var v=p.as,g=d(v,p.crossOrigin),S=typeof p.integrity=="string"?p.integrity:void 0,M=typeof p.fetchPriority=="string"?p.fetchPriority:void 0;v==="style"?r.d.S(m,typeof p.precedence=="string"?p.precedence:void 0,{crossOrigin:g,integrity:S,fetchPriority:M}):v==="script"&&r.d.X(m,{crossOrigin:g,integrity:S,fetchPriority:M,nonce:typeof p.nonce=="string"?p.nonce:void 0})}},Cn.preinitModule=function(m,p){if(typeof m=="string")if(typeof p=="object"&&p!==null){if(p.as==null||p.as==="script"){var v=d(p.as,p.crossOrigin);r.d.M(m,{crossOrigin:v,integrity:typeof p.integrity=="string"?p.integrity:void 0,nonce:typeof p.nonce=="string"?p.nonce:void 0})}}else p==null&&r.d.M(m)},Cn.preload=function(m,p){if(typeof m=="string"&&typeof p=="object"&&p!==null&&typeof p.as=="string"){var v=p.as,g=d(v,p.crossOrigin);r.d.L(m,v,{crossOrigin:g,integrity:typeof p.integrity=="string"?p.integrity:void 0,nonce:typeof p.nonce=="string"?p.nonce:void 0,type:typeof p.type=="string"?p.type:void 0,fetchPriority:typeof p.fetchPriority=="string"?p.fetchPriority:void 0,referrerPolicy:typeof p.referrerPolicy=="string"?p.referrerPolicy:void 0,imageSrcSet:typeof p.imageSrcSet=="string"?p.imageSrcSet:void 0,imageSizes:typeof p.imageSizes=="string"?p.imageSizes:void 0,media:typeof p.media=="string"?p.media:void 0})}},Cn.preloadModule=function(m,p){if(typeof m=="string")if(p){var v=d(p.as,p.crossOrigin);r.d.m(m,{as:typeof p.as=="string"&&p.as!=="script"?p.as:void 0,crossOrigin:v,integrity:typeof p.integrity=="string"?p.integrity:void 0})}else r.d.m(m)},Cn.requestFormReset=function(m){r.d.r(m)},Cn.unstable_batchedUpdates=function(m,p){return m(p)},Cn.useFormState=function(m,p,v){return h.H.useFormState(m,p,v)},Cn.useFormStatus=function(){return h.H.useHostTransitionStatus()},Cn.version="19.2.3",Cn}var E0;function bS(){if(E0)return Zf.exports;E0=1;function o(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(o)}catch(e){console.error(e)}}return o(),Zf.exports=TS(),Zf.exports}var T0;function AS(){if(T0)return Ro;T0=1;var o=ES(),e=Vo(),i=bS();function r(t){var n="https://react.dev/errors/"+t;if(1<arguments.length){n+="?args[]="+encodeURIComponent(arguments[1]);for(var a=2;a<arguments.length;a++)n+="&args[]="+encodeURIComponent(arguments[a])}return"Minified React error #"+t+"; visit "+n+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function l(t){return!(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11)}function c(t){var n=t,a=t;if(t.alternate)for(;n.return;)n=n.return;else{t=n;do n=t,(n.flags&4098)!==0&&(a=n.return),t=n.return;while(t)}return n.tag===3?a:null}function h(t){if(t.tag===13){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function d(t){if(t.tag===31){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function m(t){if(c(t)!==t)throw Error(r(188))}function p(t){var n=t.alternate;if(!n){if(n=c(t),n===null)throw Error(r(188));return n!==t?null:t}for(var a=t,s=n;;){var u=a.return;if(u===null)break;var f=u.alternate;if(f===null){if(s=u.return,s!==null){a=s;continue}break}if(u.child===f.child){for(f=u.child;f;){if(f===a)return m(u),t;if(f===s)return m(u),n;f=f.sibling}throw Error(r(188))}if(a.return!==s.return)a=u,s=f;else{for(var _=!1,T=u.child;T;){if(T===a){_=!0,a=u,s=f;break}if(T===s){_=!0,s=u,a=f;break}T=T.sibling}if(!_){for(T=f.child;T;){if(T===a){_=!0,a=f,s=u;break}if(T===s){_=!0,s=f,a=u;break}T=T.sibling}if(!_)throw Error(r(189))}}if(a.alternate!==s)throw Error(r(190))}if(a.tag!==3)throw Error(r(188));return a.stateNode.current===a?t:n}function v(t){var n=t.tag;if(n===5||n===26||n===27||n===6)return t;for(t=t.child;t!==null;){if(n=v(t),n!==null)return n;t=t.sibling}return null}var g=Object.assign,S=Symbol.for("react.element"),M=Symbol.for("react.transitional.element"),A=Symbol.for("react.portal"),C=Symbol.for("react.fragment"),y=Symbol.for("react.strict_mode"),x=Symbol.for("react.profiler"),P=Symbol.for("react.consumer"),N=Symbol.for("react.context"),L=Symbol.for("react.forward_ref"),B=Symbol.for("react.suspense"),F=Symbol.for("react.suspense_list"),z=Symbol.for("react.memo"),Q=Symbol.for("react.lazy"),R=Symbol.for("react.activity"),D=Symbol.for("react.memo_cache_sentinel"),k=Symbol.iterator;function rt(t){return t===null||typeof t!="object"?null:(t=k&&t[k]||t["@@iterator"],typeof t=="function"?t:null)}var at=Symbol.for("react.client.reference");function ut(t){if(t==null)return null;if(typeof t=="function")return t.$$typeof===at?null:t.displayName||t.name||null;if(typeof t=="string")return t;switch(t){case C:return"Fragment";case x:return"Profiler";case y:return"StrictMode";case B:return"Suspense";case F:return"SuspenseList";case R:return"Activity"}if(typeof t=="object")switch(t.$$typeof){case A:return"Portal";case N:return t.displayName||"Context";case P:return(t._context.displayName||"Context")+".Consumer";case L:var n=t.render;return t=t.displayName,t||(t=n.displayName||n.name||"",t=t!==""?"ForwardRef("+t+")":"ForwardRef"),t;case z:return n=t.displayName||null,n!==null?n:ut(t.type)||"Memo";case Q:n=t._payload,t=t._init;try{return ut(t(n))}catch{}}return null}var ht=Array.isArray,O=e.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,V=i.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,nt={pending:!1,data:null,method:null,action:null},Mt=[],xt=-1;function U(t){return{current:t}}function et(t){0>xt||(t.current=Mt[xt],Mt[xt]=null,xt--)}function gt(t,n){xt++,Mt[xt]=t.current,t.current=n}var bt=U(null),Bt=U(null),tt=U(null),ct=U(null);function Dt(t,n){switch(gt(tt,n),gt(Bt,t),gt(bt,null),n.nodeType){case 9:case 11:t=(t=n.documentElement)&&(t=t.namespaceURI)?Ig(t):0;break;default:if(t=n.tagName,n=n.namespaceURI)n=Ig(n),t=Hg(n,t);else switch(t){case"svg":t=1;break;case"math":t=2;break;default:t=0}}et(bt),gt(bt,t)}function Vt(){et(bt),et(Bt),et(tt)}function It(t){t.memoizedState!==null&&gt(ct,t);var n=bt.current,a=Hg(n,t.type);n!==a&&(gt(Bt,t),gt(bt,a))}function fe(t){Bt.current===t&&(et(bt),et(Bt)),ct.current===t&&(et(ct),yo._currentValue=nt)}var je,me;function he(t){if(je===void 0)try{throw Error()}catch(a){var n=a.stack.trim().match(/\n( *(at )?)/);je=n&&n[1]||"",me=-1<a.stack.indexOf(`
    at`)?" (<anonymous>)":-1<a.stack.indexOf("@")?"@unknown:0:0":""}return`
`+je+t+me}var Ae=!1;function re(t,n){if(!t||Ae)return"";Ae=!0;var a=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var s={DetermineComponentFrameRoot:function(){try{if(n){var mt=function(){throw Error()};if(Object.defineProperty(mt.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(mt,[])}catch(ot){var $=ot}Reflect.construct(t,[],mt)}else{try{mt.call()}catch(ot){$=ot}t.call(mt.prototype)}}else{try{throw Error()}catch(ot){$=ot}(mt=t())&&typeof mt.catch=="function"&&mt.catch(function(){})}}catch(ot){if(ot&&$&&typeof ot.stack=="string")return[ot.stack,$.stack]}return[null,null]}};s.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var u=Object.getOwnPropertyDescriptor(s.DetermineComponentFrameRoot,"name");u&&u.configurable&&Object.defineProperty(s.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var f=s.DetermineComponentFrameRoot(),_=f[0],T=f[1];if(_&&T){var I=_.split(`
`),K=T.split(`
`);for(u=s=0;s<I.length&&!I[s].includes("DetermineComponentFrameRoot");)s++;for(;u<K.length&&!K[u].includes("DetermineComponentFrameRoot");)u++;if(s===I.length||u===K.length)for(s=I.length-1,u=K.length-1;1<=s&&0<=u&&I[s]!==K[u];)u--;for(;1<=s&&0<=u;s--,u--)if(I[s]!==K[u]){if(s!==1||u!==1)do if(s--,u--,0>u||I[s]!==K[u]){var ft=`
`+I[s].replace(" at new "," at ");return t.displayName&&ft.includes("<anonymous>")&&(ft=ft.replace("<anonymous>",t.displayName)),ft}while(1<=s&&0<=u);break}}}finally{Ae=!1,Error.prepareStackTrace=a}return(a=t?t.displayName||t.name:"")?he(a):""}function Ke(t,n){switch(t.tag){case 26:case 27:case 5:return he(t.type);case 16:return he("Lazy");case 13:return t.child!==n&&n!==null?he("Suspense Fallback"):he("Suspense");case 19:return he("SuspenseList");case 0:case 15:return re(t.type,!1);case 11:return re(t.type.render,!1);case 1:return re(t.type,!0);case 31:return he("Activity");default:return""}}function H(t){try{var n="",a=null;do n+=Ke(t,a),a=t,t=t.return;while(t);return n}catch(s){return`
Error generating stack: `+s.message+`
`+s.stack}}var qe=Object.prototype.hasOwnProperty,Se=o.unstable_scheduleCallback,Le=o.unstable_cancelCallback,qt=o.unstable_shouldYield,w=o.unstable_requestPaint,E=o.unstable_now,W=o.unstable_getCurrentPriorityLevel,dt=o.unstable_ImmediatePriority,vt=o.unstable_UserBlockingPriority,lt=o.unstable_NormalPriority,Zt=o.unstable_LowPriority,Rt=o.unstable_IdlePriority,Xt=o.log,te=o.unstable_setDisableYieldValue,yt=null,Et=null;function Ft(t){if(typeof Xt=="function"&&te(t),Et&&typeof Et.setStrictMode=="function")try{Et.setStrictMode(yt,t)}catch{}}var Ot=Math.clz32?Math.clz32:X,Ct=Math.log,oe=Math.LN2;function X(t){return t>>>=0,t===0?32:31-(Ct(t)/oe|0)|0}var Ut=256,Tt=262144,Pt=4194304;function St(t){var n=t&42;if(n!==0)return n;switch(t&-t){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return t&261888;case 262144:case 524288:case 1048576:case 2097152:return t&3932160;case 4194304:case 8388608:case 16777216:case 33554432:return t&62914560;case 67108864:return 67108864;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 0;default:return t}}function _t(t,n,a){var s=t.pendingLanes;if(s===0)return 0;var u=0,f=t.suspendedLanes,_=t.pingedLanes;t=t.warmLanes;var T=s&134217727;return T!==0?(s=T&~f,s!==0?u=St(s):(_&=T,_!==0?u=St(_):a||(a=T&~t,a!==0&&(u=St(a))))):(T=s&~f,T!==0?u=St(T):_!==0?u=St(_):a||(a=s&~t,a!==0&&(u=St(a)))),u===0?0:n!==0&&n!==u&&(n&f)===0&&(f=u&-u,a=n&-n,f>=a||f===32&&(a&4194048)!==0)?n:u}function At(t,n){return(t.pendingLanes&~(t.suspendedLanes&~t.pingedLanes)&n)===0}function ee(t,n){switch(t){case 1:case 2:case 4:case 8:case 64:return n+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return n+5e3;case 4194304:case 8388608:case 16777216:case 33554432:return-1;case 67108864:case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function Oe(){var t=Pt;return Pt<<=1,(Pt&62914560)===0&&(Pt=4194304),t}function Me(t){for(var n=[],a=0;31>a;a++)n.push(t);return n}function Rn(t,n){t.pendingLanes|=n,n!==268435456&&(t.suspendedLanes=0,t.pingedLanes=0,t.warmLanes=0)}function di(t,n,a,s,u,f){var _=t.pendingLanes;t.pendingLanes=a,t.suspendedLanes=0,t.pingedLanes=0,t.warmLanes=0,t.expiredLanes&=a,t.entangledLanes&=a,t.errorRecoveryDisabledLanes&=a,t.shellSuspendCounter=0;var T=t.entanglements,I=t.expirationTimes,K=t.hiddenUpdates;for(a=_&~a;0<a;){var ft=31-Ot(a),mt=1<<ft;T[ft]=0,I[ft]=-1;var $=K[ft];if($!==null)for(K[ft]=null,ft=0;ft<$.length;ft++){var ot=$[ft];ot!==null&&(ot.lane&=-536870913)}a&=~mt}s!==0&&Zo(t,s,0),f!==0&&u===0&&t.tag!==0&&(t.suspendedLanes|=f&~(_&~n))}function Zo(t,n,a){t.pendingLanes|=n,t.suspendedLanes&=~n;var s=31-Ot(n);t.entangledLanes|=n,t.entanglements[s]=t.entanglements[s]|1073741824|a&261930}function Ns(t,n){var a=t.entangledLanes|=n;for(t=t.entanglements;a;){var s=31-Ot(a),u=1<<s;u&n|t[s]&n&&(t[s]|=n),a&=~u}}function Cr(t,n){var a=n&-n;return a=(a&42)!==0?1:Os(a),(a&(t.suspendedLanes|n))!==0?0:a}function Os(t){switch(t){case 2:t=1;break;case 8:t=4;break;case 32:t=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:t=128;break;case 268435456:t=134217728;break;default:t=0}return t}function Dr(t){return t&=-t,2<t?8<t?(t&134217727)!==0?32:268435456:8:2}function Ps(){var t=V.p;return t!==0?t:(t=window.event,t===void 0?32:u0(t.type))}function bi(t,n){var a=V.p;try{return V.p=t,n()}finally{V.p=a}}var ti=Math.random().toString(36).slice(2),an="__reactFiber$"+ti,gn="__reactProps$"+ti,pi="__reactContainer$"+ti,wr="__reactEvents$"+ti,Ur="__reactListeners$"+ti,jo="__reactHandles$"+ti,Fs="__reactResources$"+ti,Ja="__reactMarker$"+ti;function zs(t){delete t[an],delete t[gn],delete t[wr],delete t[Ur],delete t[jo]}function _a(t){var n=t[an];if(n)return n;for(var a=t.parentNode;a;){if(n=a[pi]||a[an]){if(a=n.alternate,n.child!==null||a!==null&&a.child!==null)for(t=Yg(t);t!==null;){if(a=t[an])return a;t=Yg(t)}return n}t=a,a=t.parentNode}return null}function va(t){if(t=t[an]||t[pi]){var n=t.tag;if(n===5||n===6||n===13||n===31||n===26||n===27||n===3)return t}return null}function $a(t){var n=t.tag;if(n===5||n===26||n===27||n===6)return t.stateNode;throw Error(r(33))}function xa(t){var n=t[Fs];return n||(n=t[Fs]={hoistableStyles:new Map,hoistableScripts:new Map}),n}function b(t){t[Ja]=!0}var q=new Set,st={};function J(t,n){Z(t,n),Z(t+"Capture",n)}function Z(t,n){for(st[t]=n,t=0;t<n.length;t++)q.add(n[t])}var wt=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),zt={},Lt={};function Ht(t){return qe.call(Lt,t)?!0:qe.call(zt,t)?!1:wt.test(t)?Lt[t]=!0:(zt[t]=!0,!1)}function kt(t,n,a){if(Ht(n))if(a===null)t.removeAttribute(n);else{switch(typeof a){case"undefined":case"function":case"symbol":t.removeAttribute(n);return;case"boolean":var s=n.toLowerCase().slice(0,5);if(s!=="data-"&&s!=="aria-"){t.removeAttribute(n);return}}t.setAttribute(n,""+a)}}function Qt(t,n,a){if(a===null)t.removeAttribute(n);else{switch(typeof a){case"undefined":case"function":case"symbol":case"boolean":t.removeAttribute(n);return}t.setAttribute(n,""+a)}}function Wt(t,n,a,s){if(s===null)t.removeAttribute(a);else{switch(typeof s){case"undefined":case"function":case"symbol":case"boolean":t.removeAttribute(a);return}t.setAttributeNS(n,a,""+s)}}function Jt(t){switch(typeof t){case"bigint":case"boolean":case"number":case"string":case"undefined":return t;case"object":return t;default:return""}}function Re(t){var n=t.type;return(t=t.nodeName)&&t.toLowerCase()==="input"&&(n==="checkbox"||n==="radio")}function Ye(t,n,a){var s=Object.getOwnPropertyDescriptor(t.constructor.prototype,n);if(!t.hasOwnProperty(n)&&typeof s<"u"&&typeof s.get=="function"&&typeof s.set=="function"){var u=s.get,f=s.set;return Object.defineProperty(t,n,{configurable:!0,get:function(){return u.call(this)},set:function(_){a=""+_,f.call(this,_)}}),Object.defineProperty(t,n,{enumerable:s.enumerable}),{getValue:function(){return a},setValue:function(_){a=""+_},stopTracking:function(){t._valueTracker=null,delete t[n]}}}}function Xe(t){if(!t._valueTracker){var n=Re(t)?"checked":"value";t._valueTracker=Ye(t,n,""+t[n])}}function Ne(t){if(!t)return!1;var n=t._valueTracker;if(!n)return!0;var a=n.getValue(),s="";return t&&(s=Re(t)?t.checked?"true":"false":t.value),t=s,t!==a?(n.setValue(t),!0):!1}function jt(t){if(t=t||(typeof document<"u"?document:void 0),typeof t>"u")return null;try{return t.activeElement||t.body}catch{return t.body}}var Ce=/[\n"\\]/g;function ne(t){return t.replace(Ce,function(n){return"\\"+n.charCodeAt(0).toString(16)+" "})}function _n(t,n,a,s,u,f,_,T){t.name="",_!=null&&typeof _!="function"&&typeof _!="symbol"&&typeof _!="boolean"?t.type=_:t.removeAttribute("type"),n!=null?_==="number"?(n===0&&t.value===""||t.value!=n)&&(t.value=""+Jt(n)):t.value!==""+Jt(n)&&(t.value=""+Jt(n)):_!=="submit"&&_!=="reset"||t.removeAttribute("value"),n!=null?vn(t,_,Jt(n)):a!=null?vn(t,_,Jt(a)):s!=null&&t.removeAttribute("value"),u==null&&f!=null&&(t.defaultChecked=!!f),u!=null&&(t.checked=u&&typeof u!="function"&&typeof u!="symbol"),T!=null&&typeof T!="function"&&typeof T!="symbol"&&typeof T!="boolean"?t.name=""+Jt(T):t.removeAttribute("name")}function Gi(t,n,a,s,u,f,_,T){if(f!=null&&typeof f!="function"&&typeof f!="symbol"&&typeof f!="boolean"&&(t.type=f),n!=null||a!=null){if(!(f!=="submit"&&f!=="reset"||n!=null)){Xe(t);return}a=a!=null?""+Jt(a):"",n=n!=null?""+Jt(n):a,T||n===t.value||(t.value=n),t.defaultValue=n}s=s??u,s=typeof s!="function"&&typeof s!="symbol"&&!!s,t.checked=T?t.checked:!!s,t.defaultChecked=!!s,_!=null&&typeof _!="function"&&typeof _!="symbol"&&typeof _!="boolean"&&(t.name=_),Xe(t)}function vn(t,n,a){n==="number"&&jt(t.ownerDocument)===t||t.defaultValue===""+a||(t.defaultValue=""+a)}function ei(t,n,a,s){if(t=t.options,n){n={};for(var u=0;u<a.length;u++)n["$"+a[u]]=!0;for(a=0;a<t.length;a++)u=n.hasOwnProperty("$"+t[a].value),t[a].selected!==u&&(t[a].selected=u),u&&s&&(t[a].defaultSelected=!0)}else{for(a=""+Jt(a),n=null,u=0;u<t.length;u++){if(t[u].value===a){t[u].selected=!0,s&&(t[u].defaultSelected=!0);return}n!==null||t[u].disabled||(n=t[u])}n!==null&&(n.selected=!0)}}function Pe(t,n,a){if(n!=null&&(n=""+Jt(n),n!==t.value&&(t.value=n),a==null)){t.defaultValue!==n&&(t.defaultValue=n);return}t.defaultValue=a!=null?""+Jt(a):""}function xn(t,n,a,s){if(n==null){if(s!=null){if(a!=null)throw Error(r(92));if(ht(s)){if(1<s.length)throw Error(r(93));s=s[0]}a=s}a==null&&(a=""),n=a}a=Jt(n),t.defaultValue=a,s=t.textContent,s===a&&s!==""&&s!==null&&(t.value=s),Xe(t)}function cn(t,n){if(n){var a=t.firstChild;if(a&&a===t.lastChild&&a.nodeType===3){a.nodeValue=n;return}}t.textContent=n}var Sn=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function Mn(t,n,a){var s=n.indexOf("--")===0;a==null||typeof a=="boolean"||a===""?s?t.setProperty(n,""):n==="float"?t.cssFloat="":t[n]="":s?t.setProperty(n,a):typeof a!="number"||a===0||Sn.has(n)?n==="float"?t.cssFloat=a:t[n]=(""+a).trim():t[n]=a+"px"}function Lr(t,n,a){if(n!=null&&typeof n!="object")throw Error(r(62));if(t=t.style,a!=null){for(var s in a)!a.hasOwnProperty(s)||n!=null&&n.hasOwnProperty(s)||(s.indexOf("--")===0?t.setProperty(s,""):s==="float"?t.cssFloat="":t[s]="");for(var u in n)s=n[u],n.hasOwnProperty(u)&&a[u]!==s&&Mn(t,u,s)}else for(var f in n)n.hasOwnProperty(f)&&Mn(t,f,n[f])}function mi(t){if(t.indexOf("-")===-1)return!1;switch(t){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var dv=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),pv=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function Ko(t){return pv.test(""+t)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":t}function Vi(){}var Iu=null;function Hu(t){return t=t.target||t.srcElement||window,t.correspondingUseElement&&(t=t.correspondingUseElement),t.nodeType===3?t.parentNode:t}var Nr=null,Or=null;function Bd(t){var n=va(t);if(n&&(t=n.stateNode)){var a=t[gn]||null;t:switch(t=n.stateNode,n.type){case"input":if(_n(t,a.value,a.defaultValue,a.defaultValue,a.checked,a.defaultChecked,a.type,a.name),n=a.name,a.type==="radio"&&n!=null){for(a=t;a.parentNode;)a=a.parentNode;for(a=a.querySelectorAll('input[name="'+ne(""+n)+'"][type="radio"]'),n=0;n<a.length;n++){var s=a[n];if(s!==t&&s.form===t.form){var u=s[gn]||null;if(!u)throw Error(r(90));_n(s,u.value,u.defaultValue,u.defaultValue,u.checked,u.defaultChecked,u.type,u.name)}}for(n=0;n<a.length;n++)s=a[n],s.form===t.form&&Ne(s)}break t;case"textarea":Pe(t,a.value,a.defaultValue);break t;case"select":n=a.value,n!=null&&ei(t,!!a.multiple,n,!1)}}}var Gu=!1;function Id(t,n,a){if(Gu)return t(n,a);Gu=!0;try{var s=t(n);return s}finally{if(Gu=!1,(Nr!==null||Or!==null)&&(zl(),Nr&&(n=Nr,t=Or,Or=Nr=null,Bd(n),t)))for(n=0;n<t.length;n++)Bd(t[n])}}function Bs(t,n){var a=t.stateNode;if(a===null)return null;var s=a[gn]||null;if(s===null)return null;a=s[n];t:switch(n){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(s=!s.disabled)||(t=t.type,s=!(t==="button"||t==="input"||t==="select"||t==="textarea")),t=!s;break t;default:t=!1}if(t)return null;if(a&&typeof a!="function")throw Error(r(231,n,typeof a));return a}var Xi=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),Vu=!1;if(Xi)try{var Is={};Object.defineProperty(Is,"passive",{get:function(){Vu=!0}}),window.addEventListener("test",Is,Is),window.removeEventListener("test",Is,Is)}catch{Vu=!1}var Sa=null,Xu=null,Qo=null;function Hd(){if(Qo)return Qo;var t,n=Xu,a=n.length,s,u="value"in Sa?Sa.value:Sa.textContent,f=u.length;for(t=0;t<a&&n[t]===u[t];t++);var _=a-t;for(s=1;s<=_&&n[a-s]===u[f-s];s++);return Qo=u.slice(t,1<s?1-s:void 0)}function Jo(t){var n=t.keyCode;return"charCode"in t?(t=t.charCode,t===0&&n===13&&(t=13)):t=n,t===10&&(t=13),32<=t||t===13?t:0}function $o(){return!0}function Gd(){return!1}function Fn(t){function n(a,s,u,f,_){this._reactName=a,this._targetInst=u,this.type=s,this.nativeEvent=f,this.target=_,this.currentTarget=null;for(var T in t)t.hasOwnProperty(T)&&(a=t[T],this[T]=a?a(f):f[T]);return this.isDefaultPrevented=(f.defaultPrevented!=null?f.defaultPrevented:f.returnValue===!1)?$o:Gd,this.isPropagationStopped=Gd,this}return g(n.prototype,{preventDefault:function(){this.defaultPrevented=!0;var a=this.nativeEvent;a&&(a.preventDefault?a.preventDefault():typeof a.returnValue!="unknown"&&(a.returnValue=!1),this.isDefaultPrevented=$o)},stopPropagation:function(){var a=this.nativeEvent;a&&(a.stopPropagation?a.stopPropagation():typeof a.cancelBubble!="unknown"&&(a.cancelBubble=!0),this.isPropagationStopped=$o)},persist:function(){},isPersistent:$o}),n}var tr={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(t){return t.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},tl=Fn(tr),Hs=g({},tr,{view:0,detail:0}),mv=Fn(Hs),ku,Wu,Gs,el=g({},Hs,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:Yu,button:0,buttons:0,relatedTarget:function(t){return t.relatedTarget===void 0?t.fromElement===t.srcElement?t.toElement:t.fromElement:t.relatedTarget},movementX:function(t){return"movementX"in t?t.movementX:(t!==Gs&&(Gs&&t.type==="mousemove"?(ku=t.screenX-Gs.screenX,Wu=t.screenY-Gs.screenY):Wu=ku=0,Gs=t),ku)},movementY:function(t){return"movementY"in t?t.movementY:Wu}}),Vd=Fn(el),gv=g({},el,{dataTransfer:0}),_v=Fn(gv),vv=g({},Hs,{relatedTarget:0}),qu=Fn(vv),xv=g({},tr,{animationName:0,elapsedTime:0,pseudoElement:0}),Sv=Fn(xv),Mv=g({},tr,{clipboardData:function(t){return"clipboardData"in t?t.clipboardData:window.clipboardData}}),yv=Fn(Mv),Ev=g({},tr,{data:0}),Xd=Fn(Ev),Tv={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},bv={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},Av={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function Rv(t){var n=this.nativeEvent;return n.getModifierState?n.getModifierState(t):(t=Av[t])?!!n[t]:!1}function Yu(){return Rv}var Cv=g({},Hs,{key:function(t){if(t.key){var n=Tv[t.key]||t.key;if(n!=="Unidentified")return n}return t.type==="keypress"?(t=Jo(t),t===13?"Enter":String.fromCharCode(t)):t.type==="keydown"||t.type==="keyup"?bv[t.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:Yu,charCode:function(t){return t.type==="keypress"?Jo(t):0},keyCode:function(t){return t.type==="keydown"||t.type==="keyup"?t.keyCode:0},which:function(t){return t.type==="keypress"?Jo(t):t.type==="keydown"||t.type==="keyup"?t.keyCode:0}}),Dv=Fn(Cv),wv=g({},el,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),kd=Fn(wv),Uv=g({},Hs,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:Yu}),Lv=Fn(Uv),Nv=g({},tr,{propertyName:0,elapsedTime:0,pseudoElement:0}),Ov=Fn(Nv),Pv=g({},el,{deltaX:function(t){return"deltaX"in t?t.deltaX:"wheelDeltaX"in t?-t.wheelDeltaX:0},deltaY:function(t){return"deltaY"in t?t.deltaY:"wheelDeltaY"in t?-t.wheelDeltaY:"wheelDelta"in t?-t.wheelDelta:0},deltaZ:0,deltaMode:0}),Fv=Fn(Pv),zv=g({},tr,{newState:0,oldState:0}),Bv=Fn(zv),Iv=[9,13,27,32],Zu=Xi&&"CompositionEvent"in window,Vs=null;Xi&&"documentMode"in document&&(Vs=document.documentMode);var Hv=Xi&&"TextEvent"in window&&!Vs,Wd=Xi&&(!Zu||Vs&&8<Vs&&11>=Vs),qd=" ",Yd=!1;function Zd(t,n){switch(t){case"keyup":return Iv.indexOf(n.keyCode)!==-1;case"keydown":return n.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function jd(t){return t=t.detail,typeof t=="object"&&"data"in t?t.data:null}var Pr=!1;function Gv(t,n){switch(t){case"compositionend":return jd(n);case"keypress":return n.which!==32?null:(Yd=!0,qd);case"textInput":return t=n.data,t===qd&&Yd?null:t;default:return null}}function Vv(t,n){if(Pr)return t==="compositionend"||!Zu&&Zd(t,n)?(t=Hd(),Qo=Xu=Sa=null,Pr=!1,t):null;switch(t){case"paste":return null;case"keypress":if(!(n.ctrlKey||n.altKey||n.metaKey)||n.ctrlKey&&n.altKey){if(n.char&&1<n.char.length)return n.char;if(n.which)return String.fromCharCode(n.which)}return null;case"compositionend":return Wd&&n.locale!=="ko"?null:n.data;default:return null}}var Xv={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function Kd(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n==="input"?!!Xv[t.type]:n==="textarea"}function Qd(t,n,a,s){Nr?Or?Or.push(s):Or=[s]:Nr=s,n=kl(n,"onChange"),0<n.length&&(a=new tl("onChange","change",null,a,s),t.push({event:a,listeners:n}))}var Xs=null,ks=null;function kv(t){Ng(t,0)}function nl(t){var n=$a(t);if(Ne(n))return t}function Jd(t,n){if(t==="change")return n}var $d=!1;if(Xi){var ju;if(Xi){var Ku="oninput"in document;if(!Ku){var tp=document.createElement("div");tp.setAttribute("oninput","return;"),Ku=typeof tp.oninput=="function"}ju=Ku}else ju=!1;$d=ju&&(!document.documentMode||9<document.documentMode)}function ep(){Xs&&(Xs.detachEvent("onpropertychange",np),ks=Xs=null)}function np(t){if(t.propertyName==="value"&&nl(ks)){var n=[];Qd(n,ks,t,Hu(t)),Id(kv,n)}}function Wv(t,n,a){t==="focusin"?(ep(),Xs=n,ks=a,Xs.attachEvent("onpropertychange",np)):t==="focusout"&&ep()}function qv(t){if(t==="selectionchange"||t==="keyup"||t==="keydown")return nl(ks)}function Yv(t,n){if(t==="click")return nl(n)}function Zv(t,n){if(t==="input"||t==="change")return nl(n)}function jv(t,n){return t===n&&(t!==0||1/t===1/n)||t!==t&&n!==n}var kn=typeof Object.is=="function"?Object.is:jv;function Ws(t,n){if(kn(t,n))return!0;if(typeof t!="object"||t===null||typeof n!="object"||n===null)return!1;var a=Object.keys(t),s=Object.keys(n);if(a.length!==s.length)return!1;for(s=0;s<a.length;s++){var u=a[s];if(!qe.call(n,u)||!kn(t[u],n[u]))return!1}return!0}function ip(t){for(;t&&t.firstChild;)t=t.firstChild;return t}function ap(t,n){var a=ip(t);t=0;for(var s;a;){if(a.nodeType===3){if(s=t+a.textContent.length,t<=n&&s>=n)return{node:a,offset:n-t};t=s}t:{for(;a;){if(a.nextSibling){a=a.nextSibling;break t}a=a.parentNode}a=void 0}a=ip(a)}}function rp(t,n){return t&&n?t===n?!0:t&&t.nodeType===3?!1:n&&n.nodeType===3?rp(t,n.parentNode):"contains"in t?t.contains(n):t.compareDocumentPosition?!!(t.compareDocumentPosition(n)&16):!1:!1}function sp(t){t=t!=null&&t.ownerDocument!=null&&t.ownerDocument.defaultView!=null?t.ownerDocument.defaultView:window;for(var n=jt(t.document);n instanceof t.HTMLIFrameElement;){try{var a=typeof n.contentWindow.location.href=="string"}catch{a=!1}if(a)t=n.contentWindow;else break;n=jt(t.document)}return n}function Qu(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n&&(n==="input"&&(t.type==="text"||t.type==="search"||t.type==="tel"||t.type==="url"||t.type==="password")||n==="textarea"||t.contentEditable==="true")}var Kv=Xi&&"documentMode"in document&&11>=document.documentMode,Fr=null,Ju=null,qs=null,$u=!1;function op(t,n,a){var s=a.window===a?a.document:a.nodeType===9?a:a.ownerDocument;$u||Fr==null||Fr!==jt(s)||(s=Fr,"selectionStart"in s&&Qu(s)?s={start:s.selectionStart,end:s.selectionEnd}:(s=(s.ownerDocument&&s.ownerDocument.defaultView||window).getSelection(),s={anchorNode:s.anchorNode,anchorOffset:s.anchorOffset,focusNode:s.focusNode,focusOffset:s.focusOffset}),qs&&Ws(qs,s)||(qs=s,s=kl(Ju,"onSelect"),0<s.length&&(n=new tl("onSelect","select",null,n,a),t.push({event:n,listeners:s}),n.target=Fr)))}function er(t,n){var a={};return a[t.toLowerCase()]=n.toLowerCase(),a["Webkit"+t]="webkit"+n,a["Moz"+t]="moz"+n,a}var zr={animationend:er("Animation","AnimationEnd"),animationiteration:er("Animation","AnimationIteration"),animationstart:er("Animation","AnimationStart"),transitionrun:er("Transition","TransitionRun"),transitionstart:er("Transition","TransitionStart"),transitioncancel:er("Transition","TransitionCancel"),transitionend:er("Transition","TransitionEnd")},tc={},lp={};Xi&&(lp=document.createElement("div").style,"AnimationEvent"in window||(delete zr.animationend.animation,delete zr.animationiteration.animation,delete zr.animationstart.animation),"TransitionEvent"in window||delete zr.transitionend.transition);function nr(t){if(tc[t])return tc[t];if(!zr[t])return t;var n=zr[t],a;for(a in n)if(n.hasOwnProperty(a)&&a in lp)return tc[t]=n[a];return t}var up=nr("animationend"),cp=nr("animationiteration"),fp=nr("animationstart"),Qv=nr("transitionrun"),Jv=nr("transitionstart"),$v=nr("transitioncancel"),hp=nr("transitionend"),dp=new Map,ec="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");ec.push("scrollEnd");function gi(t,n){dp.set(t,n),J(n,[t])}var il=typeof reportError=="function"?reportError:function(t){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var n=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof t=="object"&&t!==null&&typeof t.message=="string"?String(t.message):String(t),error:t});if(!window.dispatchEvent(n))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",t);return}console.error(t)},ni=[],Br=0,nc=0;function al(){for(var t=Br,n=nc=Br=0;n<t;){var a=ni[n];ni[n++]=null;var s=ni[n];ni[n++]=null;var u=ni[n];ni[n++]=null;var f=ni[n];if(ni[n++]=null,s!==null&&u!==null){var _=s.pending;_===null?u.next=u:(u.next=_.next,_.next=u),s.pending=u}f!==0&&pp(a,u,f)}}function rl(t,n,a,s){ni[Br++]=t,ni[Br++]=n,ni[Br++]=a,ni[Br++]=s,nc|=s,t.lanes|=s,t=t.alternate,t!==null&&(t.lanes|=s)}function ic(t,n,a,s){return rl(t,n,a,s),sl(t)}function ir(t,n){return rl(t,null,null,n),sl(t)}function pp(t,n,a){t.lanes|=a;var s=t.alternate;s!==null&&(s.lanes|=a);for(var u=!1,f=t.return;f!==null;)f.childLanes|=a,s=f.alternate,s!==null&&(s.childLanes|=a),f.tag===22&&(t=f.stateNode,t===null||t._visibility&1||(u=!0)),t=f,f=f.return;return t.tag===3?(f=t.stateNode,u&&n!==null&&(u=31-Ot(a),t=f.hiddenUpdates,s=t[u],s===null?t[u]=[n]:s.push(n),n.lane=a|536870912),f):null}function sl(t){if(50<mo)throw mo=0,df=null,Error(r(185));for(var n=t.return;n!==null;)t=n,n=t.return;return t.tag===3?t.stateNode:null}var Ir={};function tx(t,n,a,s){this.tag=t,this.key=a,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=n,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=s,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function Wn(t,n,a,s){return new tx(t,n,a,s)}function ac(t){return t=t.prototype,!(!t||!t.isReactComponent)}function ki(t,n){var a=t.alternate;return a===null?(a=Wn(t.tag,n,t.key,t.mode),a.elementType=t.elementType,a.type=t.type,a.stateNode=t.stateNode,a.alternate=t,t.alternate=a):(a.pendingProps=n,a.type=t.type,a.flags=0,a.subtreeFlags=0,a.deletions=null),a.flags=t.flags&65011712,a.childLanes=t.childLanes,a.lanes=t.lanes,a.child=t.child,a.memoizedProps=t.memoizedProps,a.memoizedState=t.memoizedState,a.updateQueue=t.updateQueue,n=t.dependencies,a.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext},a.sibling=t.sibling,a.index=t.index,a.ref=t.ref,a.refCleanup=t.refCleanup,a}function mp(t,n){t.flags&=65011714;var a=t.alternate;return a===null?(t.childLanes=0,t.lanes=n,t.child=null,t.subtreeFlags=0,t.memoizedProps=null,t.memoizedState=null,t.updateQueue=null,t.dependencies=null,t.stateNode=null):(t.childLanes=a.childLanes,t.lanes=a.lanes,t.child=a.child,t.subtreeFlags=0,t.deletions=null,t.memoizedProps=a.memoizedProps,t.memoizedState=a.memoizedState,t.updateQueue=a.updateQueue,t.type=a.type,n=a.dependencies,t.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext}),t}function ol(t,n,a,s,u,f){var _=0;if(s=t,typeof t=="function")ac(t)&&(_=1);else if(typeof t=="string")_=rS(t,a,bt.current)?26:t==="html"||t==="head"||t==="body"?27:5;else t:switch(t){case R:return t=Wn(31,a,n,u),t.elementType=R,t.lanes=f,t;case C:return ar(a.children,u,f,n);case y:_=8,u|=24;break;case x:return t=Wn(12,a,n,u|2),t.elementType=x,t.lanes=f,t;case B:return t=Wn(13,a,n,u),t.elementType=B,t.lanes=f,t;case F:return t=Wn(19,a,n,u),t.elementType=F,t.lanes=f,t;default:if(typeof t=="object"&&t!==null)switch(t.$$typeof){case N:_=10;break t;case P:_=9;break t;case L:_=11;break t;case z:_=14;break t;case Q:_=16,s=null;break t}_=29,a=Error(r(130,t===null?"null":typeof t,"")),s=null}return n=Wn(_,a,n,u),n.elementType=t,n.type=s,n.lanes=f,n}function ar(t,n,a,s){return t=Wn(7,t,s,n),t.lanes=a,t}function rc(t,n,a){return t=Wn(6,t,null,n),t.lanes=a,t}function gp(t){var n=Wn(18,null,null,0);return n.stateNode=t,n}function sc(t,n,a){return n=Wn(4,t.children!==null?t.children:[],t.key,n),n.lanes=a,n.stateNode={containerInfo:t.containerInfo,pendingChildren:null,implementation:t.implementation},n}var _p=new WeakMap;function ii(t,n){if(typeof t=="object"&&t!==null){var a=_p.get(t);return a!==void 0?a:(n={value:t,source:n,stack:H(n)},_p.set(t,n),n)}return{value:t,source:n,stack:H(n)}}var Hr=[],Gr=0,ll=null,Ys=0,ai=[],ri=0,Ma=null,Ai=1,Ri="";function Wi(t,n){Hr[Gr++]=Ys,Hr[Gr++]=ll,ll=t,Ys=n}function vp(t,n,a){ai[ri++]=Ai,ai[ri++]=Ri,ai[ri++]=Ma,Ma=t;var s=Ai;t=Ri;var u=32-Ot(s)-1;s&=~(1<<u),a+=1;var f=32-Ot(n)+u;if(30<f){var _=u-u%5;f=(s&(1<<_)-1).toString(32),s>>=_,u-=_,Ai=1<<32-Ot(n)+u|a<<u|s,Ri=f+t}else Ai=1<<f|a<<u|s,Ri=t}function oc(t){t.return!==null&&(Wi(t,1),vp(t,1,0))}function lc(t){for(;t===ll;)ll=Hr[--Gr],Hr[Gr]=null,Ys=Hr[--Gr],Hr[Gr]=null;for(;t===Ma;)Ma=ai[--ri],ai[ri]=null,Ri=ai[--ri],ai[ri]=null,Ai=ai[--ri],ai[ri]=null}function xp(t,n){ai[ri++]=Ai,ai[ri++]=Ri,ai[ri++]=Ma,Ai=n.id,Ri=n.overflow,Ma=t}var yn=null,ke=null,ve=!1,ya=null,si=!1,uc=Error(r(519));function Ea(t){var n=Error(r(418,1<arguments.length&&arguments[1]!==void 0&&arguments[1]?"text":"HTML",""));throw Zs(ii(n,t)),uc}function Sp(t){var n=t.stateNode,a=t.type,s=t.memoizedProps;switch(n[an]=t,n[gn]=s,a){case"dialog":pe("cancel",n),pe("close",n);break;case"iframe":case"object":case"embed":pe("load",n);break;case"video":case"audio":for(a=0;a<_o.length;a++)pe(_o[a],n);break;case"source":pe("error",n);break;case"img":case"image":case"link":pe("error",n),pe("load",n);break;case"details":pe("toggle",n);break;case"input":pe("invalid",n),Gi(n,s.value,s.defaultValue,s.checked,s.defaultChecked,s.type,s.name,!0);break;case"select":pe("invalid",n);break;case"textarea":pe("invalid",n),xn(n,s.value,s.defaultValue,s.children)}a=s.children,typeof a!="string"&&typeof a!="number"&&typeof a!="bigint"||n.textContent===""+a||s.suppressHydrationWarning===!0||zg(n.textContent,a)?(s.popover!=null&&(pe("beforetoggle",n),pe("toggle",n)),s.onScroll!=null&&pe("scroll",n),s.onScrollEnd!=null&&pe("scrollend",n),s.onClick!=null&&(n.onclick=Vi),n=!0):n=!1,n||Ea(t,!0)}function Mp(t){for(yn=t.return;yn;)switch(yn.tag){case 5:case 31:case 13:si=!1;return;case 27:case 3:si=!0;return;default:yn=yn.return}}function Vr(t){if(t!==yn)return!1;if(!ve)return Mp(t),ve=!0,!1;var n=t.tag,a;if((a=n!==3&&n!==27)&&((a=n===5)&&(a=t.type,a=!(a!=="form"&&a!=="button")||Cf(t.type,t.memoizedProps)),a=!a),a&&ke&&Ea(t),Mp(t),n===13){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(317));ke=qg(t)}else if(n===31){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(317));ke=qg(t)}else n===27?(n=ke,za(t.type)?(t=Nf,Nf=null,ke=t):ke=n):ke=yn?li(t.stateNode.nextSibling):null;return!0}function rr(){ke=yn=null,ve=!1}function cc(){var t=ya;return t!==null&&(Hn===null?Hn=t:Hn.push.apply(Hn,t),ya=null),t}function Zs(t){ya===null?ya=[t]:ya.push(t)}var fc=U(null),sr=null,qi=null;function Ta(t,n,a){gt(fc,n._currentValue),n._currentValue=a}function Yi(t){t._currentValue=fc.current,et(fc)}function hc(t,n,a){for(;t!==null;){var s=t.alternate;if((t.childLanes&n)!==n?(t.childLanes|=n,s!==null&&(s.childLanes|=n)):s!==null&&(s.childLanes&n)!==n&&(s.childLanes|=n),t===a)break;t=t.return}}function dc(t,n,a,s){var u=t.child;for(u!==null&&(u.return=t);u!==null;){var f=u.dependencies;if(f!==null){var _=u.child;f=f.firstContext;t:for(;f!==null;){var T=f;f=u;for(var I=0;I<n.length;I++)if(T.context===n[I]){f.lanes|=a,T=f.alternate,T!==null&&(T.lanes|=a),hc(f.return,a,t),s||(_=null);break t}f=T.next}}else if(u.tag===18){if(_=u.return,_===null)throw Error(r(341));_.lanes|=a,f=_.alternate,f!==null&&(f.lanes|=a),hc(_,a,t),_=null}else _=u.child;if(_!==null)_.return=u;else for(_=u;_!==null;){if(_===t){_=null;break}if(u=_.sibling,u!==null){u.return=_.return,_=u;break}_=_.return}u=_}}function Xr(t,n,a,s){t=null;for(var u=n,f=!1;u!==null;){if(!f){if((u.flags&524288)!==0)f=!0;else if((u.flags&262144)!==0)break}if(u.tag===10){var _=u.alternate;if(_===null)throw Error(r(387));if(_=_.memoizedProps,_!==null){var T=u.type;kn(u.pendingProps.value,_.value)||(t!==null?t.push(T):t=[T])}}else if(u===ct.current){if(_=u.alternate,_===null)throw Error(r(387));_.memoizedState.memoizedState!==u.memoizedState.memoizedState&&(t!==null?t.push(yo):t=[yo])}u=u.return}t!==null&&dc(n,t,a,s),n.flags|=262144}function ul(t){for(t=t.firstContext;t!==null;){if(!kn(t.context._currentValue,t.memoizedValue))return!0;t=t.next}return!1}function or(t){sr=t,qi=null,t=t.dependencies,t!==null&&(t.firstContext=null)}function En(t){return yp(sr,t)}function cl(t,n){return sr===null&&or(t),yp(t,n)}function yp(t,n){var a=n._currentValue;if(n={context:n,memoizedValue:a,next:null},qi===null){if(t===null)throw Error(r(308));qi=n,t.dependencies={lanes:0,firstContext:n},t.flags|=524288}else qi=qi.next=n;return a}var ex=typeof AbortController<"u"?AbortController:function(){var t=[],n=this.signal={aborted:!1,addEventListener:function(a,s){t.push(s)}};this.abort=function(){n.aborted=!0,t.forEach(function(a){return a()})}},nx=o.unstable_scheduleCallback,ix=o.unstable_NormalPriority,rn={$$typeof:N,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function pc(){return{controller:new ex,data:new Map,refCount:0}}function js(t){t.refCount--,t.refCount===0&&nx(ix,function(){t.controller.abort()})}var Ks=null,mc=0,kr=0,Wr=null;function ax(t,n){if(Ks===null){var a=Ks=[];mc=0,kr=xf(),Wr={status:"pending",value:void 0,then:function(s){a.push(s)}}}return mc++,n.then(Ep,Ep),n}function Ep(){if(--mc===0&&Ks!==null){Wr!==null&&(Wr.status="fulfilled");var t=Ks;Ks=null,kr=0,Wr=null;for(var n=0;n<t.length;n++)(0,t[n])()}}function rx(t,n){var a=[],s={status:"pending",value:null,reason:null,then:function(u){a.push(u)}};return t.then(function(){s.status="fulfilled",s.value=n;for(var u=0;u<a.length;u++)(0,a[u])(n)},function(u){for(s.status="rejected",s.reason=u,u=0;u<a.length;u++)(0,a[u])(void 0)}),s}var Tp=O.S;O.S=function(t,n){og=E(),typeof n=="object"&&n!==null&&typeof n.then=="function"&&ax(t,n),Tp!==null&&Tp(t,n)};var lr=U(null);function gc(){var t=lr.current;return t!==null?t:Ve.pooledCache}function fl(t,n){n===null?gt(lr,lr.current):gt(lr,n.pool)}function bp(){var t=gc();return t===null?null:{parent:rn._currentValue,pool:t}}var qr=Error(r(460)),_c=Error(r(474)),hl=Error(r(542)),dl={then:function(){}};function Ap(t){return t=t.status,t==="fulfilled"||t==="rejected"}function Rp(t,n,a){switch(a=t[a],a===void 0?t.push(n):a!==n&&(n.then(Vi,Vi),n=a),n.status){case"fulfilled":return n.value;case"rejected":throw t=n.reason,Dp(t),t;default:if(typeof n.status=="string")n.then(Vi,Vi);else{if(t=Ve,t!==null&&100<t.shellSuspendCounter)throw Error(r(482));t=n,t.status="pending",t.then(function(s){if(n.status==="pending"){var u=n;u.status="fulfilled",u.value=s}},function(s){if(n.status==="pending"){var u=n;u.status="rejected",u.reason=s}})}switch(n.status){case"fulfilled":return n.value;case"rejected":throw t=n.reason,Dp(t),t}throw cr=n,qr}}function ur(t){try{var n=t._init;return n(t._payload)}catch(a){throw a!==null&&typeof a=="object"&&typeof a.then=="function"?(cr=a,qr):a}}var cr=null;function Cp(){if(cr===null)throw Error(r(459));var t=cr;return cr=null,t}function Dp(t){if(t===qr||t===hl)throw Error(r(483))}var Yr=null,Qs=0;function pl(t){var n=Qs;return Qs+=1,Yr===null&&(Yr=[]),Rp(Yr,t,n)}function Js(t,n){n=n.props.ref,t.ref=n!==void 0?n:null}function ml(t,n){throw n.$$typeof===S?Error(r(525)):(t=Object.prototype.toString.call(n),Error(r(31,t==="[object Object]"?"object with keys {"+Object.keys(n).join(", ")+"}":t)))}function wp(t){function n(Y,G){if(t){var j=Y.deletions;j===null?(Y.deletions=[G],Y.flags|=16):j.push(G)}}function a(Y,G){if(!t)return null;for(;G!==null;)n(Y,G),G=G.sibling;return null}function s(Y){for(var G=new Map;Y!==null;)Y.key!==null?G.set(Y.key,Y):G.set(Y.index,Y),Y=Y.sibling;return G}function u(Y,G){return Y=ki(Y,G),Y.index=0,Y.sibling=null,Y}function f(Y,G,j){return Y.index=j,t?(j=Y.alternate,j!==null?(j=j.index,j<G?(Y.flags|=67108866,G):j):(Y.flags|=67108866,G)):(Y.flags|=1048576,G)}function _(Y){return t&&Y.alternate===null&&(Y.flags|=67108866),Y}function T(Y,G,j,pt){return G===null||G.tag!==6?(G=rc(j,Y.mode,pt),G.return=Y,G):(G=u(G,j),G.return=Y,G)}function I(Y,G,j,pt){var Kt=j.type;return Kt===C?ft(Y,G,j.props.children,pt,j.key):G!==null&&(G.elementType===Kt||typeof Kt=="object"&&Kt!==null&&Kt.$$typeof===Q&&ur(Kt)===G.type)?(G=u(G,j.props),Js(G,j),G.return=Y,G):(G=ol(j.type,j.key,j.props,null,Y.mode,pt),Js(G,j),G.return=Y,G)}function K(Y,G,j,pt){return G===null||G.tag!==4||G.stateNode.containerInfo!==j.containerInfo||G.stateNode.implementation!==j.implementation?(G=sc(j,Y.mode,pt),G.return=Y,G):(G=u(G,j.children||[]),G.return=Y,G)}function ft(Y,G,j,pt,Kt){return G===null||G.tag!==7?(G=ar(j,Y.mode,pt,Kt),G.return=Y,G):(G=u(G,j),G.return=Y,G)}function mt(Y,G,j){if(typeof G=="string"&&G!==""||typeof G=="number"||typeof G=="bigint")return G=rc(""+G,Y.mode,j),G.return=Y,G;if(typeof G=="object"&&G!==null){switch(G.$$typeof){case M:return j=ol(G.type,G.key,G.props,null,Y.mode,j),Js(j,G),j.return=Y,j;case A:return G=sc(G,Y.mode,j),G.return=Y,G;case Q:return G=ur(G),mt(Y,G,j)}if(ht(G)||rt(G))return G=ar(G,Y.mode,j,null),G.return=Y,G;if(typeof G.then=="function")return mt(Y,pl(G),j);if(G.$$typeof===N)return mt(Y,cl(Y,G),j);ml(Y,G)}return null}function $(Y,G,j,pt){var Kt=G!==null?G.key:null;if(typeof j=="string"&&j!==""||typeof j=="number"||typeof j=="bigint")return Kt!==null?null:T(Y,G,""+j,pt);if(typeof j=="object"&&j!==null){switch(j.$$typeof){case M:return j.key===Kt?I(Y,G,j,pt):null;case A:return j.key===Kt?K(Y,G,j,pt):null;case Q:return j=ur(j),$(Y,G,j,pt)}if(ht(j)||rt(j))return Kt!==null?null:ft(Y,G,j,pt,null);if(typeof j.then=="function")return $(Y,G,pl(j),pt);if(j.$$typeof===N)return $(Y,G,cl(Y,j),pt);ml(Y,j)}return null}function ot(Y,G,j,pt,Kt){if(typeof pt=="string"&&pt!==""||typeof pt=="number"||typeof pt=="bigint")return Y=Y.get(j)||null,T(G,Y,""+pt,Kt);if(typeof pt=="object"&&pt!==null){switch(pt.$$typeof){case M:return Y=Y.get(pt.key===null?j:pt.key)||null,I(G,Y,pt,Kt);case A:return Y=Y.get(pt.key===null?j:pt.key)||null,K(G,Y,pt,Kt);case Q:return pt=ur(pt),ot(Y,G,j,pt,Kt)}if(ht(pt)||rt(pt))return Y=Y.get(j)||null,ft(G,Y,pt,Kt,null);if(typeof pt.then=="function")return ot(Y,G,j,pl(pt),Kt);if(pt.$$typeof===N)return ot(Y,G,j,cl(G,pt),Kt);ml(G,pt)}return null}function Gt(Y,G,j,pt){for(var Kt=null,Ee=null,Yt=G,le=G=0,_e=null;Yt!==null&&le<j.length;le++){Yt.index>le?(_e=Yt,Yt=null):_e=Yt.sibling;var Te=$(Y,Yt,j[le],pt);if(Te===null){Yt===null&&(Yt=_e);break}t&&Yt&&Te.alternate===null&&n(Y,Yt),G=f(Te,G,le),Ee===null?Kt=Te:Ee.sibling=Te,Ee=Te,Yt=_e}if(le===j.length)return a(Y,Yt),ve&&Wi(Y,le),Kt;if(Yt===null){for(;le<j.length;le++)Yt=mt(Y,j[le],pt),Yt!==null&&(G=f(Yt,G,le),Ee===null?Kt=Yt:Ee.sibling=Yt,Ee=Yt);return ve&&Wi(Y,le),Kt}for(Yt=s(Yt);le<j.length;le++)_e=ot(Yt,Y,le,j[le],pt),_e!==null&&(t&&_e.alternate!==null&&Yt.delete(_e.key===null?le:_e.key),G=f(_e,G,le),Ee===null?Kt=_e:Ee.sibling=_e,Ee=_e);return t&&Yt.forEach(function(Va){return n(Y,Va)}),ve&&Wi(Y,le),Kt}function $t(Y,G,j,pt){if(j==null)throw Error(r(151));for(var Kt=null,Ee=null,Yt=G,le=G=0,_e=null,Te=j.next();Yt!==null&&!Te.done;le++,Te=j.next()){Yt.index>le?(_e=Yt,Yt=null):_e=Yt.sibling;var Va=$(Y,Yt,Te.value,pt);if(Va===null){Yt===null&&(Yt=_e);break}t&&Yt&&Va.alternate===null&&n(Y,Yt),G=f(Va,G,le),Ee===null?Kt=Va:Ee.sibling=Va,Ee=Va,Yt=_e}if(Te.done)return a(Y,Yt),ve&&Wi(Y,le),Kt;if(Yt===null){for(;!Te.done;le++,Te=j.next())Te=mt(Y,Te.value,pt),Te!==null&&(G=f(Te,G,le),Ee===null?Kt=Te:Ee.sibling=Te,Ee=Te);return ve&&Wi(Y,le),Kt}for(Yt=s(Yt);!Te.done;le++,Te=j.next())Te=ot(Yt,Y,le,Te.value,pt),Te!==null&&(t&&Te.alternate!==null&&Yt.delete(Te.key===null?le:Te.key),G=f(Te,G,le),Ee===null?Kt=Te:Ee.sibling=Te,Ee=Te);return t&&Yt.forEach(function(gS){return n(Y,gS)}),ve&&Wi(Y,le),Kt}function Ge(Y,G,j,pt){if(typeof j=="object"&&j!==null&&j.type===C&&j.key===null&&(j=j.props.children),typeof j=="object"&&j!==null){switch(j.$$typeof){case M:t:{for(var Kt=j.key;G!==null;){if(G.key===Kt){if(Kt=j.type,Kt===C){if(G.tag===7){a(Y,G.sibling),pt=u(G,j.props.children),pt.return=Y,Y=pt;break t}}else if(G.elementType===Kt||typeof Kt=="object"&&Kt!==null&&Kt.$$typeof===Q&&ur(Kt)===G.type){a(Y,G.sibling),pt=u(G,j.props),Js(pt,j),pt.return=Y,Y=pt;break t}a(Y,G);break}else n(Y,G);G=G.sibling}j.type===C?(pt=ar(j.props.children,Y.mode,pt,j.key),pt.return=Y,Y=pt):(pt=ol(j.type,j.key,j.props,null,Y.mode,pt),Js(pt,j),pt.return=Y,Y=pt)}return _(Y);case A:t:{for(Kt=j.key;G!==null;){if(G.key===Kt)if(G.tag===4&&G.stateNode.containerInfo===j.containerInfo&&G.stateNode.implementation===j.implementation){a(Y,G.sibling),pt=u(G,j.children||[]),pt.return=Y,Y=pt;break t}else{a(Y,G);break}else n(Y,G);G=G.sibling}pt=sc(j,Y.mode,pt),pt.return=Y,Y=pt}return _(Y);case Q:return j=ur(j),Ge(Y,G,j,pt)}if(ht(j))return Gt(Y,G,j,pt);if(rt(j)){if(Kt=rt(j),typeof Kt!="function")throw Error(r(150));return j=Kt.call(j),$t(Y,G,j,pt)}if(typeof j.then=="function")return Ge(Y,G,pl(j),pt);if(j.$$typeof===N)return Ge(Y,G,cl(Y,j),pt);ml(Y,j)}return typeof j=="string"&&j!==""||typeof j=="number"||typeof j=="bigint"?(j=""+j,G!==null&&G.tag===6?(a(Y,G.sibling),pt=u(G,j),pt.return=Y,Y=pt):(a(Y,G),pt=rc(j,Y.mode,pt),pt.return=Y,Y=pt),_(Y)):a(Y,G)}return function(Y,G,j,pt){try{Qs=0;var Kt=Ge(Y,G,j,pt);return Yr=null,Kt}catch(Yt){if(Yt===qr||Yt===hl)throw Yt;var Ee=Wn(29,Yt,null,Y.mode);return Ee.lanes=pt,Ee.return=Y,Ee}}}var fr=wp(!0),Up=wp(!1),ba=!1;function vc(t){t.updateQueue={baseState:t.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function xc(t,n){t=t.updateQueue,n.updateQueue===t&&(n.updateQueue={baseState:t.baseState,firstBaseUpdate:t.firstBaseUpdate,lastBaseUpdate:t.lastBaseUpdate,shared:t.shared,callbacks:null})}function Aa(t){return{lane:t,tag:0,payload:null,callback:null,next:null}}function Ra(t,n,a){var s=t.updateQueue;if(s===null)return null;if(s=s.shared,(De&2)!==0){var u=s.pending;return u===null?n.next=n:(n.next=u.next,u.next=n),s.pending=n,n=sl(t),pp(t,null,a),n}return rl(t,s,n,a),sl(t)}function $s(t,n,a){if(n=n.updateQueue,n!==null&&(n=n.shared,(a&4194048)!==0)){var s=n.lanes;s&=t.pendingLanes,a|=s,n.lanes=a,Ns(t,a)}}function Sc(t,n){var a=t.updateQueue,s=t.alternate;if(s!==null&&(s=s.updateQueue,a===s)){var u=null,f=null;if(a=a.firstBaseUpdate,a!==null){do{var _={lane:a.lane,tag:a.tag,payload:a.payload,callback:null,next:null};f===null?u=f=_:f=f.next=_,a=a.next}while(a!==null);f===null?u=f=n:f=f.next=n}else u=f=n;a={baseState:s.baseState,firstBaseUpdate:u,lastBaseUpdate:f,shared:s.shared,callbacks:s.callbacks},t.updateQueue=a;return}t=a.lastBaseUpdate,t===null?a.firstBaseUpdate=n:t.next=n,a.lastBaseUpdate=n}var Mc=!1;function to(){if(Mc){var t=Wr;if(t!==null)throw t}}function eo(t,n,a,s){Mc=!1;var u=t.updateQueue;ba=!1;var f=u.firstBaseUpdate,_=u.lastBaseUpdate,T=u.shared.pending;if(T!==null){u.shared.pending=null;var I=T,K=I.next;I.next=null,_===null?f=K:_.next=K,_=I;var ft=t.alternate;ft!==null&&(ft=ft.updateQueue,T=ft.lastBaseUpdate,T!==_&&(T===null?ft.firstBaseUpdate=K:T.next=K,ft.lastBaseUpdate=I))}if(f!==null){var mt=u.baseState;_=0,ft=K=I=null,T=f;do{var $=T.lane&-536870913,ot=$!==T.lane;if(ot?(ge&$)===$:(s&$)===$){$!==0&&$===kr&&(Mc=!0),ft!==null&&(ft=ft.next={lane:0,tag:T.tag,payload:T.payload,callback:null,next:null});t:{var Gt=t,$t=T;$=n;var Ge=a;switch($t.tag){case 1:if(Gt=$t.payload,typeof Gt=="function"){mt=Gt.call(Ge,mt,$);break t}mt=Gt;break t;case 3:Gt.flags=Gt.flags&-65537|128;case 0:if(Gt=$t.payload,$=typeof Gt=="function"?Gt.call(Ge,mt,$):Gt,$==null)break t;mt=g({},mt,$);break t;case 2:ba=!0}}$=T.callback,$!==null&&(t.flags|=64,ot&&(t.flags|=8192),ot=u.callbacks,ot===null?u.callbacks=[$]:ot.push($))}else ot={lane:$,tag:T.tag,payload:T.payload,callback:T.callback,next:null},ft===null?(K=ft=ot,I=mt):ft=ft.next=ot,_|=$;if(T=T.next,T===null){if(T=u.shared.pending,T===null)break;ot=T,T=ot.next,ot.next=null,u.lastBaseUpdate=ot,u.shared.pending=null}}while(!0);ft===null&&(I=mt),u.baseState=I,u.firstBaseUpdate=K,u.lastBaseUpdate=ft,f===null&&(u.shared.lanes=0),La|=_,t.lanes=_,t.memoizedState=mt}}function Lp(t,n){if(typeof t!="function")throw Error(r(191,t));t.call(n)}function Np(t,n){var a=t.callbacks;if(a!==null)for(t.callbacks=null,t=0;t<a.length;t++)Lp(a[t],n)}var Zr=U(null),gl=U(0);function Op(t,n){t=na,gt(gl,t),gt(Zr,n),na=t|n.baseLanes}function yc(){gt(gl,na),gt(Zr,Zr.current)}function Ec(){na=gl.current,et(Zr),et(gl)}var qn=U(null),oi=null;function Ca(t){var n=t.alternate;gt(en,en.current&1),gt(qn,t),oi===null&&(n===null||Zr.current!==null||n.memoizedState!==null)&&(oi=t)}function Tc(t){gt(en,en.current),gt(qn,t),oi===null&&(oi=t)}function Pp(t){t.tag===22?(gt(en,en.current),gt(qn,t),oi===null&&(oi=t)):Da()}function Da(){gt(en,en.current),gt(qn,qn.current)}function Yn(t){et(qn),oi===t&&(oi=null),et(en)}var en=U(0);function _l(t){for(var n=t;n!==null;){if(n.tag===13){var a=n.memoizedState;if(a!==null&&(a=a.dehydrated,a===null||Uf(a)||Lf(a)))return n}else if(n.tag===19&&(n.memoizedProps.revealOrder==="forwards"||n.memoizedProps.revealOrder==="backwards"||n.memoizedProps.revealOrder==="unstable_legacy-backwards"||n.memoizedProps.revealOrder==="together")){if((n.flags&128)!==0)return n}else if(n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return null;n=n.return}n.sibling.return=n.return,n=n.sibling}return null}var Zi=0,se=null,Ie=null,sn=null,vl=!1,jr=!1,hr=!1,xl=0,no=0,Kr=null,sx=0;function Qe(){throw Error(r(321))}function bc(t,n){if(n===null)return!1;for(var a=0;a<n.length&&a<t.length;a++)if(!kn(t[a],n[a]))return!1;return!0}function Ac(t,n,a,s,u,f){return Zi=f,se=n,n.memoizedState=null,n.updateQueue=null,n.lanes=0,O.H=t===null||t.memoizedState===null?vm:Gc,hr=!1,f=a(s,u),hr=!1,jr&&(f=zp(n,a,s,u)),Fp(t),f}function Fp(t){O.H=ro;var n=Ie!==null&&Ie.next!==null;if(Zi=0,sn=Ie=se=null,vl=!1,no=0,Kr=null,n)throw Error(r(300));t===null||on||(t=t.dependencies,t!==null&&ul(t)&&(on=!0))}function zp(t,n,a,s){se=t;var u=0;do{if(jr&&(Kr=null),no=0,jr=!1,25<=u)throw Error(r(301));if(u+=1,sn=Ie=null,t.updateQueue!=null){var f=t.updateQueue;f.lastEffect=null,f.events=null,f.stores=null,f.memoCache!=null&&(f.memoCache.index=0)}O.H=xm,f=n(a,s)}while(jr);return f}function ox(){var t=O.H,n=t.useState()[0];return n=typeof n.then=="function"?io(n):n,t=t.useState()[0],(Ie!==null?Ie.memoizedState:null)!==t&&(se.flags|=1024),n}function Rc(){var t=xl!==0;return xl=0,t}function Cc(t,n,a){n.updateQueue=t.updateQueue,n.flags&=-2053,t.lanes&=~a}function Dc(t){if(vl){for(t=t.memoizedState;t!==null;){var n=t.queue;n!==null&&(n.pending=null),t=t.next}vl=!1}Zi=0,sn=Ie=se=null,jr=!1,no=xl=0,Kr=null}function Nn(){var t={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return sn===null?se.memoizedState=sn=t:sn=sn.next=t,sn}function nn(){if(Ie===null){var t=se.alternate;t=t!==null?t.memoizedState:null}else t=Ie.next;var n=sn===null?se.memoizedState:sn.next;if(n!==null)sn=n,Ie=t;else{if(t===null)throw se.alternate===null?Error(r(467)):Error(r(310));Ie=t,t={memoizedState:Ie.memoizedState,baseState:Ie.baseState,baseQueue:Ie.baseQueue,queue:Ie.queue,next:null},sn===null?se.memoizedState=sn=t:sn=sn.next=t}return sn}function Sl(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function io(t){var n=no;return no+=1,Kr===null&&(Kr=[]),t=Rp(Kr,t,n),n=se,(sn===null?n.memoizedState:sn.next)===null&&(n=n.alternate,O.H=n===null||n.memoizedState===null?vm:Gc),t}function Ml(t){if(t!==null&&typeof t=="object"){if(typeof t.then=="function")return io(t);if(t.$$typeof===N)return En(t)}throw Error(r(438,String(t)))}function wc(t){var n=null,a=se.updateQueue;if(a!==null&&(n=a.memoCache),n==null){var s=se.alternate;s!==null&&(s=s.updateQueue,s!==null&&(s=s.memoCache,s!=null&&(n={data:s.data.map(function(u){return u.slice()}),index:0})))}if(n==null&&(n={data:[],index:0}),a===null&&(a=Sl(),se.updateQueue=a),a.memoCache=n,a=n.data[n.index],a===void 0)for(a=n.data[n.index]=Array(t),s=0;s<t;s++)a[s]=D;return n.index++,a}function ji(t,n){return typeof n=="function"?n(t):n}function yl(t){var n=nn();return Uc(n,Ie,t)}function Uc(t,n,a){var s=t.queue;if(s===null)throw Error(r(311));s.lastRenderedReducer=a;var u=t.baseQueue,f=s.pending;if(f!==null){if(u!==null){var _=u.next;u.next=f.next,f.next=_}n.baseQueue=u=f,s.pending=null}if(f=t.baseState,u===null)t.memoizedState=f;else{n=u.next;var T=_=null,I=null,K=n,ft=!1;do{var mt=K.lane&-536870913;if(mt!==K.lane?(ge&mt)===mt:(Zi&mt)===mt){var $=K.revertLane;if($===0)I!==null&&(I=I.next={lane:0,revertLane:0,gesture:null,action:K.action,hasEagerState:K.hasEagerState,eagerState:K.eagerState,next:null}),mt===kr&&(ft=!0);else if((Zi&$)===$){K=K.next,$===kr&&(ft=!0);continue}else mt={lane:0,revertLane:K.revertLane,gesture:null,action:K.action,hasEagerState:K.hasEagerState,eagerState:K.eagerState,next:null},I===null?(T=I=mt,_=f):I=I.next=mt,se.lanes|=$,La|=$;mt=K.action,hr&&a(f,mt),f=K.hasEagerState?K.eagerState:a(f,mt)}else $={lane:mt,revertLane:K.revertLane,gesture:K.gesture,action:K.action,hasEagerState:K.hasEagerState,eagerState:K.eagerState,next:null},I===null?(T=I=$,_=f):I=I.next=$,se.lanes|=mt,La|=mt;K=K.next}while(K!==null&&K!==n);if(I===null?_=f:I.next=T,!kn(f,t.memoizedState)&&(on=!0,ft&&(a=Wr,a!==null)))throw a;t.memoizedState=f,t.baseState=_,t.baseQueue=I,s.lastRenderedState=f}return u===null&&(s.lanes=0),[t.memoizedState,s.dispatch]}function Lc(t){var n=nn(),a=n.queue;if(a===null)throw Error(r(311));a.lastRenderedReducer=t;var s=a.dispatch,u=a.pending,f=n.memoizedState;if(u!==null){a.pending=null;var _=u=u.next;do f=t(f,_.action),_=_.next;while(_!==u);kn(f,n.memoizedState)||(on=!0),n.memoizedState=f,n.baseQueue===null&&(n.baseState=f),a.lastRenderedState=f}return[f,s]}function Bp(t,n,a){var s=se,u=nn(),f=ve;if(f){if(a===void 0)throw Error(r(407));a=a()}else a=n();var _=!kn((Ie||u).memoizedState,a);if(_&&(u.memoizedState=a,on=!0),u=u.queue,Pc(Gp.bind(null,s,u,t),[t]),u.getSnapshot!==n||_||sn!==null&&sn.memoizedState.tag&1){if(s.flags|=2048,Qr(9,{destroy:void 0},Hp.bind(null,s,u,a,n),null),Ve===null)throw Error(r(349));f||(Zi&127)!==0||Ip(s,n,a)}return a}function Ip(t,n,a){t.flags|=16384,t={getSnapshot:n,value:a},n=se.updateQueue,n===null?(n=Sl(),se.updateQueue=n,n.stores=[t]):(a=n.stores,a===null?n.stores=[t]:a.push(t))}function Hp(t,n,a,s){n.value=a,n.getSnapshot=s,Vp(n)&&Xp(t)}function Gp(t,n,a){return a(function(){Vp(n)&&Xp(t)})}function Vp(t){var n=t.getSnapshot;t=t.value;try{var a=n();return!kn(t,a)}catch{return!0}}function Xp(t){var n=ir(t,2);n!==null&&Gn(n,t,2)}function Nc(t){var n=Nn();if(typeof t=="function"){var a=t;if(t=a(),hr){Ft(!0);try{a()}finally{Ft(!1)}}}return n.memoizedState=n.baseState=t,n.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:ji,lastRenderedState:t},n}function kp(t,n,a,s){return t.baseState=a,Uc(t,Ie,typeof s=="function"?s:ji)}function lx(t,n,a,s,u){if(bl(t))throw Error(r(485));if(t=n.action,t!==null){var f={payload:u,action:t,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(_){f.listeners.push(_)}};O.T!==null?a(!0):f.isTransition=!1,s(f),a=n.pending,a===null?(f.next=n.pending=f,Wp(n,f)):(f.next=a.next,n.pending=a.next=f)}}function Wp(t,n){var a=n.action,s=n.payload,u=t.state;if(n.isTransition){var f=O.T,_={};O.T=_;try{var T=a(u,s),I=O.S;I!==null&&I(_,T),qp(t,n,T)}catch(K){Oc(t,n,K)}finally{f!==null&&_.types!==null&&(f.types=_.types),O.T=f}}else try{f=a(u,s),qp(t,n,f)}catch(K){Oc(t,n,K)}}function qp(t,n,a){a!==null&&typeof a=="object"&&typeof a.then=="function"?a.then(function(s){Yp(t,n,s)},function(s){return Oc(t,n,s)}):Yp(t,n,a)}function Yp(t,n,a){n.status="fulfilled",n.value=a,Zp(n),t.state=a,n=t.pending,n!==null&&(a=n.next,a===n?t.pending=null:(a=a.next,n.next=a,Wp(t,a)))}function Oc(t,n,a){var s=t.pending;if(t.pending=null,s!==null){s=s.next;do n.status="rejected",n.reason=a,Zp(n),n=n.next;while(n!==s)}t.action=null}function Zp(t){t=t.listeners;for(var n=0;n<t.length;n++)(0,t[n])()}function jp(t,n){return n}function Kp(t,n){if(ve){var a=Ve.formState;if(a!==null){t:{var s=se;if(ve){if(ke){e:{for(var u=ke,f=si;u.nodeType!==8;){if(!f){u=null;break e}if(u=li(u.nextSibling),u===null){u=null;break e}}f=u.data,u=f==="F!"||f==="F"?u:null}if(u){ke=li(u.nextSibling),s=u.data==="F!";break t}}Ea(s)}s=!1}s&&(n=a[0])}}return a=Nn(),a.memoizedState=a.baseState=n,s={pending:null,lanes:0,dispatch:null,lastRenderedReducer:jp,lastRenderedState:n},a.queue=s,a=mm.bind(null,se,s),s.dispatch=a,s=Nc(!1),f=Hc.bind(null,se,!1,s.queue),s=Nn(),u={state:n,dispatch:null,action:t,pending:null},s.queue=u,a=lx.bind(null,se,u,f,a),u.dispatch=a,s.memoizedState=t,[n,a,!1]}function Qp(t){var n=nn();return Jp(n,Ie,t)}function Jp(t,n,a){if(n=Uc(t,n,jp)[0],t=yl(ji)[0],typeof n=="object"&&n!==null&&typeof n.then=="function")try{var s=io(n)}catch(_){throw _===qr?hl:_}else s=n;n=nn();var u=n.queue,f=u.dispatch;return a!==n.memoizedState&&(se.flags|=2048,Qr(9,{destroy:void 0},ux.bind(null,u,a),null)),[s,f,t]}function ux(t,n){t.action=n}function $p(t){var n=nn(),a=Ie;if(a!==null)return Jp(n,a,t);nn(),n=n.memoizedState,a=nn();var s=a.queue.dispatch;return a.memoizedState=t,[n,s,!1]}function Qr(t,n,a,s){return t={tag:t,create:a,deps:s,inst:n,next:null},n=se.updateQueue,n===null&&(n=Sl(),se.updateQueue=n),a=n.lastEffect,a===null?n.lastEffect=t.next=t:(s=a.next,a.next=t,t.next=s,n.lastEffect=t),t}function tm(){return nn().memoizedState}function El(t,n,a,s){var u=Nn();se.flags|=t,u.memoizedState=Qr(1|n,{destroy:void 0},a,s===void 0?null:s)}function Tl(t,n,a,s){var u=nn();s=s===void 0?null:s;var f=u.memoizedState.inst;Ie!==null&&s!==null&&bc(s,Ie.memoizedState.deps)?u.memoizedState=Qr(n,f,a,s):(se.flags|=t,u.memoizedState=Qr(1|n,f,a,s))}function em(t,n){El(8390656,8,t,n)}function Pc(t,n){Tl(2048,8,t,n)}function cx(t){se.flags|=4;var n=se.updateQueue;if(n===null)n=Sl(),se.updateQueue=n,n.events=[t];else{var a=n.events;a===null?n.events=[t]:a.push(t)}}function nm(t){var n=nn().memoizedState;return cx({ref:n,nextImpl:t}),function(){if((De&2)!==0)throw Error(r(440));return n.impl.apply(void 0,arguments)}}function im(t,n){return Tl(4,2,t,n)}function am(t,n){return Tl(4,4,t,n)}function rm(t,n){if(typeof n=="function"){t=t();var a=n(t);return function(){typeof a=="function"?a():n(null)}}if(n!=null)return t=t(),n.current=t,function(){n.current=null}}function sm(t,n,a){a=a!=null?a.concat([t]):null,Tl(4,4,rm.bind(null,n,t),a)}function Fc(){}function om(t,n){var a=nn();n=n===void 0?null:n;var s=a.memoizedState;return n!==null&&bc(n,s[1])?s[0]:(a.memoizedState=[t,n],t)}function lm(t,n){var a=nn();n=n===void 0?null:n;var s=a.memoizedState;if(n!==null&&bc(n,s[1]))return s[0];if(s=t(),hr){Ft(!0);try{t()}finally{Ft(!1)}}return a.memoizedState=[s,n],s}function zc(t,n,a){return a===void 0||(Zi&1073741824)!==0&&(ge&261930)===0?t.memoizedState=n:(t.memoizedState=a,t=ug(),se.lanes|=t,La|=t,a)}function um(t,n,a,s){return kn(a,n)?a:Zr.current!==null?(t=zc(t,a,s),kn(t,n)||(on=!0),t):(Zi&42)===0||(Zi&1073741824)!==0&&(ge&261930)===0?(on=!0,t.memoizedState=a):(t=ug(),se.lanes|=t,La|=t,n)}function cm(t,n,a,s,u){var f=V.p;V.p=f!==0&&8>f?f:8;var _=O.T,T={};O.T=T,Hc(t,!1,n,a);try{var I=u(),K=O.S;if(K!==null&&K(T,I),I!==null&&typeof I=="object"&&typeof I.then=="function"){var ft=rx(I,s);ao(t,n,ft,Kn(t))}else ao(t,n,s,Kn(t))}catch(mt){ao(t,n,{then:function(){},status:"rejected",reason:mt},Kn())}finally{V.p=f,_!==null&&T.types!==null&&(_.types=T.types),O.T=_}}function fx(){}function Bc(t,n,a,s){if(t.tag!==5)throw Error(r(476));var u=fm(t).queue;cm(t,u,n,nt,a===null?fx:function(){return hm(t),a(s)})}function fm(t){var n=t.memoizedState;if(n!==null)return n;n={memoizedState:nt,baseState:nt,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:ji,lastRenderedState:nt},next:null};var a={};return n.next={memoizedState:a,baseState:a,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:ji,lastRenderedState:a},next:null},t.memoizedState=n,t=t.alternate,t!==null&&(t.memoizedState=n),n}function hm(t){var n=fm(t);n.next===null&&(n=t.alternate.memoizedState),ao(t,n.next.queue,{},Kn())}function Ic(){return En(yo)}function dm(){return nn().memoizedState}function pm(){return nn().memoizedState}function hx(t){for(var n=t.return;n!==null;){switch(n.tag){case 24:case 3:var a=Kn();t=Aa(a);var s=Ra(n,t,a);s!==null&&(Gn(s,n,a),$s(s,n,a)),n={cache:pc()},t.payload=n;return}n=n.return}}function dx(t,n,a){var s=Kn();a={lane:s,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null},bl(t)?gm(n,a):(a=ic(t,n,a,s),a!==null&&(Gn(a,t,s),_m(a,n,s)))}function mm(t,n,a){var s=Kn();ao(t,n,a,s)}function ao(t,n,a,s){var u={lane:s,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null};if(bl(t))gm(n,u);else{var f=t.alternate;if(t.lanes===0&&(f===null||f.lanes===0)&&(f=n.lastRenderedReducer,f!==null))try{var _=n.lastRenderedState,T=f(_,a);if(u.hasEagerState=!0,u.eagerState=T,kn(T,_))return rl(t,n,u,0),Ve===null&&al(),!1}catch{}if(a=ic(t,n,u,s),a!==null)return Gn(a,t,s),_m(a,n,s),!0}return!1}function Hc(t,n,a,s){if(s={lane:2,revertLane:xf(),gesture:null,action:s,hasEagerState:!1,eagerState:null,next:null},bl(t)){if(n)throw Error(r(479))}else n=ic(t,a,s,2),n!==null&&Gn(n,t,2)}function bl(t){var n=t.alternate;return t===se||n!==null&&n===se}function gm(t,n){jr=vl=!0;var a=t.pending;a===null?n.next=n:(n.next=a.next,a.next=n),t.pending=n}function _m(t,n,a){if((a&4194048)!==0){var s=n.lanes;s&=t.pendingLanes,a|=s,n.lanes=a,Ns(t,a)}}var ro={readContext:En,use:Ml,useCallback:Qe,useContext:Qe,useEffect:Qe,useImperativeHandle:Qe,useLayoutEffect:Qe,useInsertionEffect:Qe,useMemo:Qe,useReducer:Qe,useRef:Qe,useState:Qe,useDebugValue:Qe,useDeferredValue:Qe,useTransition:Qe,useSyncExternalStore:Qe,useId:Qe,useHostTransitionStatus:Qe,useFormState:Qe,useActionState:Qe,useOptimistic:Qe,useMemoCache:Qe,useCacheRefresh:Qe};ro.useEffectEvent=Qe;var vm={readContext:En,use:Ml,useCallback:function(t,n){return Nn().memoizedState=[t,n===void 0?null:n],t},useContext:En,useEffect:em,useImperativeHandle:function(t,n,a){a=a!=null?a.concat([t]):null,El(4194308,4,rm.bind(null,n,t),a)},useLayoutEffect:function(t,n){return El(4194308,4,t,n)},useInsertionEffect:function(t,n){El(4,2,t,n)},useMemo:function(t,n){var a=Nn();n=n===void 0?null:n;var s=t();if(hr){Ft(!0);try{t()}finally{Ft(!1)}}return a.memoizedState=[s,n],s},useReducer:function(t,n,a){var s=Nn();if(a!==void 0){var u=a(n);if(hr){Ft(!0);try{a(n)}finally{Ft(!1)}}}else u=n;return s.memoizedState=s.baseState=u,t={pending:null,lanes:0,dispatch:null,lastRenderedReducer:t,lastRenderedState:u},s.queue=t,t=t.dispatch=dx.bind(null,se,t),[s.memoizedState,t]},useRef:function(t){var n=Nn();return t={current:t},n.memoizedState=t},useState:function(t){t=Nc(t);var n=t.queue,a=mm.bind(null,se,n);return n.dispatch=a,[t.memoizedState,a]},useDebugValue:Fc,useDeferredValue:function(t,n){var a=Nn();return zc(a,t,n)},useTransition:function(){var t=Nc(!1);return t=cm.bind(null,se,t.queue,!0,!1),Nn().memoizedState=t,[!1,t]},useSyncExternalStore:function(t,n,a){var s=se,u=Nn();if(ve){if(a===void 0)throw Error(r(407));a=a()}else{if(a=n(),Ve===null)throw Error(r(349));(ge&127)!==0||Ip(s,n,a)}u.memoizedState=a;var f={value:a,getSnapshot:n};return u.queue=f,em(Gp.bind(null,s,f,t),[t]),s.flags|=2048,Qr(9,{destroy:void 0},Hp.bind(null,s,f,a,n),null),a},useId:function(){var t=Nn(),n=Ve.identifierPrefix;if(ve){var a=Ri,s=Ai;a=(s&~(1<<32-Ot(s)-1)).toString(32)+a,n="_"+n+"R_"+a,a=xl++,0<a&&(n+="H"+a.toString(32)),n+="_"}else a=sx++,n="_"+n+"r_"+a.toString(32)+"_";return t.memoizedState=n},useHostTransitionStatus:Ic,useFormState:Kp,useActionState:Kp,useOptimistic:function(t){var n=Nn();n.memoizedState=n.baseState=t;var a={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return n.queue=a,n=Hc.bind(null,se,!0,a),a.dispatch=n,[t,n]},useMemoCache:wc,useCacheRefresh:function(){return Nn().memoizedState=hx.bind(null,se)},useEffectEvent:function(t){var n=Nn(),a={impl:t};return n.memoizedState=a,function(){if((De&2)!==0)throw Error(r(440));return a.impl.apply(void 0,arguments)}}},Gc={readContext:En,use:Ml,useCallback:om,useContext:En,useEffect:Pc,useImperativeHandle:sm,useInsertionEffect:im,useLayoutEffect:am,useMemo:lm,useReducer:yl,useRef:tm,useState:function(){return yl(ji)},useDebugValue:Fc,useDeferredValue:function(t,n){var a=nn();return um(a,Ie.memoizedState,t,n)},useTransition:function(){var t=yl(ji)[0],n=nn().memoizedState;return[typeof t=="boolean"?t:io(t),n]},useSyncExternalStore:Bp,useId:dm,useHostTransitionStatus:Ic,useFormState:Qp,useActionState:Qp,useOptimistic:function(t,n){var a=nn();return kp(a,Ie,t,n)},useMemoCache:wc,useCacheRefresh:pm};Gc.useEffectEvent=nm;var xm={readContext:En,use:Ml,useCallback:om,useContext:En,useEffect:Pc,useImperativeHandle:sm,useInsertionEffect:im,useLayoutEffect:am,useMemo:lm,useReducer:Lc,useRef:tm,useState:function(){return Lc(ji)},useDebugValue:Fc,useDeferredValue:function(t,n){var a=nn();return Ie===null?zc(a,t,n):um(a,Ie.memoizedState,t,n)},useTransition:function(){var t=Lc(ji)[0],n=nn().memoizedState;return[typeof t=="boolean"?t:io(t),n]},useSyncExternalStore:Bp,useId:dm,useHostTransitionStatus:Ic,useFormState:$p,useActionState:$p,useOptimistic:function(t,n){var a=nn();return Ie!==null?kp(a,Ie,t,n):(a.baseState=t,[t,a.queue.dispatch])},useMemoCache:wc,useCacheRefresh:pm};xm.useEffectEvent=nm;function Vc(t,n,a,s){n=t.memoizedState,a=a(s,n),a=a==null?n:g({},n,a),t.memoizedState=a,t.lanes===0&&(t.updateQueue.baseState=a)}var Xc={enqueueSetState:function(t,n,a){t=t._reactInternals;var s=Kn(),u=Aa(s);u.payload=n,a!=null&&(u.callback=a),n=Ra(t,u,s),n!==null&&(Gn(n,t,s),$s(n,t,s))},enqueueReplaceState:function(t,n,a){t=t._reactInternals;var s=Kn(),u=Aa(s);u.tag=1,u.payload=n,a!=null&&(u.callback=a),n=Ra(t,u,s),n!==null&&(Gn(n,t,s),$s(n,t,s))},enqueueForceUpdate:function(t,n){t=t._reactInternals;var a=Kn(),s=Aa(a);s.tag=2,n!=null&&(s.callback=n),n=Ra(t,s,a),n!==null&&(Gn(n,t,a),$s(n,t,a))}};function Sm(t,n,a,s,u,f,_){return t=t.stateNode,typeof t.shouldComponentUpdate=="function"?t.shouldComponentUpdate(s,f,_):n.prototype&&n.prototype.isPureReactComponent?!Ws(a,s)||!Ws(u,f):!0}function Mm(t,n,a,s){t=n.state,typeof n.componentWillReceiveProps=="function"&&n.componentWillReceiveProps(a,s),typeof n.UNSAFE_componentWillReceiveProps=="function"&&n.UNSAFE_componentWillReceiveProps(a,s),n.state!==t&&Xc.enqueueReplaceState(n,n.state,null)}function dr(t,n){var a=n;if("ref"in n){a={};for(var s in n)s!=="ref"&&(a[s]=n[s])}if(t=t.defaultProps){a===n&&(a=g({},a));for(var u in t)a[u]===void 0&&(a[u]=t[u])}return a}function ym(t){il(t)}function Em(t){console.error(t)}function Tm(t){il(t)}function Al(t,n){try{var a=t.onUncaughtError;a(n.value,{componentStack:n.stack})}catch(s){setTimeout(function(){throw s})}}function bm(t,n,a){try{var s=t.onCaughtError;s(a.value,{componentStack:a.stack,errorBoundary:n.tag===1?n.stateNode:null})}catch(u){setTimeout(function(){throw u})}}function kc(t,n,a){return a=Aa(a),a.tag=3,a.payload={element:null},a.callback=function(){Al(t,n)},a}function Am(t){return t=Aa(t),t.tag=3,t}function Rm(t,n,a,s){var u=a.type.getDerivedStateFromError;if(typeof u=="function"){var f=s.value;t.payload=function(){return u(f)},t.callback=function(){bm(n,a,s)}}var _=a.stateNode;_!==null&&typeof _.componentDidCatch=="function"&&(t.callback=function(){bm(n,a,s),typeof u!="function"&&(Na===null?Na=new Set([this]):Na.add(this));var T=s.stack;this.componentDidCatch(s.value,{componentStack:T!==null?T:""})})}function px(t,n,a,s,u){if(a.flags|=32768,s!==null&&typeof s=="object"&&typeof s.then=="function"){if(n=a.alternate,n!==null&&Xr(n,a,u,!0),a=qn.current,a!==null){switch(a.tag){case 31:case 13:return oi===null?Bl():a.alternate===null&&Je===0&&(Je=3),a.flags&=-257,a.flags|=65536,a.lanes=u,s===dl?a.flags|=16384:(n=a.updateQueue,n===null?a.updateQueue=new Set([s]):n.add(s),gf(t,s,u)),!1;case 22:return a.flags|=65536,s===dl?a.flags|=16384:(n=a.updateQueue,n===null?(n={transitions:null,markerInstances:null,retryQueue:new Set([s])},a.updateQueue=n):(a=n.retryQueue,a===null?n.retryQueue=new Set([s]):a.add(s)),gf(t,s,u)),!1}throw Error(r(435,a.tag))}return gf(t,s,u),Bl(),!1}if(ve)return n=qn.current,n!==null?((n.flags&65536)===0&&(n.flags|=256),n.flags|=65536,n.lanes=u,s!==uc&&(t=Error(r(422),{cause:s}),Zs(ii(t,a)))):(s!==uc&&(n=Error(r(423),{cause:s}),Zs(ii(n,a))),t=t.current.alternate,t.flags|=65536,u&=-u,t.lanes|=u,s=ii(s,a),u=kc(t.stateNode,s,u),Sc(t,u),Je!==4&&(Je=2)),!1;var f=Error(r(520),{cause:s});if(f=ii(f,a),po===null?po=[f]:po.push(f),Je!==4&&(Je=2),n===null)return!0;s=ii(s,a),a=n;do{switch(a.tag){case 3:return a.flags|=65536,t=u&-u,a.lanes|=t,t=kc(a.stateNode,s,t),Sc(a,t),!1;case 1:if(n=a.type,f=a.stateNode,(a.flags&128)===0&&(typeof n.getDerivedStateFromError=="function"||f!==null&&typeof f.componentDidCatch=="function"&&(Na===null||!Na.has(f))))return a.flags|=65536,u&=-u,a.lanes|=u,u=Am(u),Rm(u,t,a,s),Sc(a,u),!1}a=a.return}while(a!==null);return!1}var Wc=Error(r(461)),on=!1;function Tn(t,n,a,s){n.child=t===null?Up(n,null,a,s):fr(n,t.child,a,s)}function Cm(t,n,a,s,u){a=a.render;var f=n.ref;if("ref"in s){var _={};for(var T in s)T!=="ref"&&(_[T]=s[T])}else _=s;return or(n),s=Ac(t,n,a,_,f,u),T=Rc(),t!==null&&!on?(Cc(t,n,u),Ki(t,n,u)):(ve&&T&&oc(n),n.flags|=1,Tn(t,n,s,u),n.child)}function Dm(t,n,a,s,u){if(t===null){var f=a.type;return typeof f=="function"&&!ac(f)&&f.defaultProps===void 0&&a.compare===null?(n.tag=15,n.type=f,wm(t,n,f,s,u)):(t=ol(a.type,null,s,n,n.mode,u),t.ref=n.ref,t.return=n,n.child=t)}if(f=t.child,!$c(t,u)){var _=f.memoizedProps;if(a=a.compare,a=a!==null?a:Ws,a(_,s)&&t.ref===n.ref)return Ki(t,n,u)}return n.flags|=1,t=ki(f,s),t.ref=n.ref,t.return=n,n.child=t}function wm(t,n,a,s,u){if(t!==null){var f=t.memoizedProps;if(Ws(f,s)&&t.ref===n.ref)if(on=!1,n.pendingProps=s=f,$c(t,u))(t.flags&131072)!==0&&(on=!0);else return n.lanes=t.lanes,Ki(t,n,u)}return qc(t,n,a,s,u)}function Um(t,n,a,s){var u=s.children,f=t!==null?t.memoizedState:null;if(t===null&&n.stateNode===null&&(n.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),s.mode==="hidden"){if((n.flags&128)!==0){if(f=f!==null?f.baseLanes|a:a,t!==null){for(s=n.child=t.child,u=0;s!==null;)u=u|s.lanes|s.childLanes,s=s.sibling;s=u&~f}else s=0,n.child=null;return Lm(t,n,f,a,s)}if((a&536870912)!==0)n.memoizedState={baseLanes:0,cachePool:null},t!==null&&fl(n,f!==null?f.cachePool:null),f!==null?Op(n,f):yc(),Pp(n);else return s=n.lanes=536870912,Lm(t,n,f!==null?f.baseLanes|a:a,a,s)}else f!==null?(fl(n,f.cachePool),Op(n,f),Da(),n.memoizedState=null):(t!==null&&fl(n,null),yc(),Da());return Tn(t,n,u,a),n.child}function so(t,n){return t!==null&&t.tag===22||n.stateNode!==null||(n.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),n.sibling}function Lm(t,n,a,s,u){var f=gc();return f=f===null?null:{parent:rn._currentValue,pool:f},n.memoizedState={baseLanes:a,cachePool:f},t!==null&&fl(n,null),yc(),Pp(n),t!==null&&Xr(t,n,s,!0),n.childLanes=u,null}function Rl(t,n){return n=Dl({mode:n.mode,children:n.children},t.mode),n.ref=t.ref,t.child=n,n.return=t,n}function Nm(t,n,a){return fr(n,t.child,null,a),t=Rl(n,n.pendingProps),t.flags|=2,Yn(n),n.memoizedState=null,t}function mx(t,n,a){var s=n.pendingProps,u=(n.flags&128)!==0;if(n.flags&=-129,t===null){if(ve){if(s.mode==="hidden")return t=Rl(n,s),n.lanes=536870912,so(null,t);if(Tc(n),(t=ke)?(t=Wg(t,si),t=t!==null&&t.data==="&"?t:null,t!==null&&(n.memoizedState={dehydrated:t,treeContext:Ma!==null?{id:Ai,overflow:Ri}:null,retryLane:536870912,hydrationErrors:null},a=gp(t),a.return=n,n.child=a,yn=n,ke=null)):t=null,t===null)throw Ea(n);return n.lanes=536870912,null}return Rl(n,s)}var f=t.memoizedState;if(f!==null){var _=f.dehydrated;if(Tc(n),u)if(n.flags&256)n.flags&=-257,n=Nm(t,n,a);else if(n.memoizedState!==null)n.child=t.child,n.flags|=128,n=null;else throw Error(r(558));else if(on||Xr(t,n,a,!1),u=(a&t.childLanes)!==0,on||u){if(s=Ve,s!==null&&(_=Cr(s,a),_!==0&&_!==f.retryLane))throw f.retryLane=_,ir(t,_),Gn(s,t,_),Wc;Bl(),n=Nm(t,n,a)}else t=f.treeContext,ke=li(_.nextSibling),yn=n,ve=!0,ya=null,si=!1,t!==null&&xp(n,t),n=Rl(n,s),n.flags|=4096;return n}return t=ki(t.child,{mode:s.mode,children:s.children}),t.ref=n.ref,n.child=t,t.return=n,t}function Cl(t,n){var a=n.ref;if(a===null)t!==null&&t.ref!==null&&(n.flags|=4194816);else{if(typeof a!="function"&&typeof a!="object")throw Error(r(284));(t===null||t.ref!==a)&&(n.flags|=4194816)}}function qc(t,n,a,s,u){return or(n),a=Ac(t,n,a,s,void 0,u),s=Rc(),t!==null&&!on?(Cc(t,n,u),Ki(t,n,u)):(ve&&s&&oc(n),n.flags|=1,Tn(t,n,a,u),n.child)}function Om(t,n,a,s,u,f){return or(n),n.updateQueue=null,a=zp(n,s,a,u),Fp(t),s=Rc(),t!==null&&!on?(Cc(t,n,f),Ki(t,n,f)):(ve&&s&&oc(n),n.flags|=1,Tn(t,n,a,f),n.child)}function Pm(t,n,a,s,u){if(or(n),n.stateNode===null){var f=Ir,_=a.contextType;typeof _=="object"&&_!==null&&(f=En(_)),f=new a(s,f),n.memoizedState=f.state!==null&&f.state!==void 0?f.state:null,f.updater=Xc,n.stateNode=f,f._reactInternals=n,f=n.stateNode,f.props=s,f.state=n.memoizedState,f.refs={},vc(n),_=a.contextType,f.context=typeof _=="object"&&_!==null?En(_):Ir,f.state=n.memoizedState,_=a.getDerivedStateFromProps,typeof _=="function"&&(Vc(n,a,_,s),f.state=n.memoizedState),typeof a.getDerivedStateFromProps=="function"||typeof f.getSnapshotBeforeUpdate=="function"||typeof f.UNSAFE_componentWillMount!="function"&&typeof f.componentWillMount!="function"||(_=f.state,typeof f.componentWillMount=="function"&&f.componentWillMount(),typeof f.UNSAFE_componentWillMount=="function"&&f.UNSAFE_componentWillMount(),_!==f.state&&Xc.enqueueReplaceState(f,f.state,null),eo(n,s,f,u),to(),f.state=n.memoizedState),typeof f.componentDidMount=="function"&&(n.flags|=4194308),s=!0}else if(t===null){f=n.stateNode;var T=n.memoizedProps,I=dr(a,T);f.props=I;var K=f.context,ft=a.contextType;_=Ir,typeof ft=="object"&&ft!==null&&(_=En(ft));var mt=a.getDerivedStateFromProps;ft=typeof mt=="function"||typeof f.getSnapshotBeforeUpdate=="function",T=n.pendingProps!==T,ft||typeof f.UNSAFE_componentWillReceiveProps!="function"&&typeof f.componentWillReceiveProps!="function"||(T||K!==_)&&Mm(n,f,s,_),ba=!1;var $=n.memoizedState;f.state=$,eo(n,s,f,u),to(),K=n.memoizedState,T||$!==K||ba?(typeof mt=="function"&&(Vc(n,a,mt,s),K=n.memoizedState),(I=ba||Sm(n,a,I,s,$,K,_))?(ft||typeof f.UNSAFE_componentWillMount!="function"&&typeof f.componentWillMount!="function"||(typeof f.componentWillMount=="function"&&f.componentWillMount(),typeof f.UNSAFE_componentWillMount=="function"&&f.UNSAFE_componentWillMount()),typeof f.componentDidMount=="function"&&(n.flags|=4194308)):(typeof f.componentDidMount=="function"&&(n.flags|=4194308),n.memoizedProps=s,n.memoizedState=K),f.props=s,f.state=K,f.context=_,s=I):(typeof f.componentDidMount=="function"&&(n.flags|=4194308),s=!1)}else{f=n.stateNode,xc(t,n),_=n.memoizedProps,ft=dr(a,_),f.props=ft,mt=n.pendingProps,$=f.context,K=a.contextType,I=Ir,typeof K=="object"&&K!==null&&(I=En(K)),T=a.getDerivedStateFromProps,(K=typeof T=="function"||typeof f.getSnapshotBeforeUpdate=="function")||typeof f.UNSAFE_componentWillReceiveProps!="function"&&typeof f.componentWillReceiveProps!="function"||(_!==mt||$!==I)&&Mm(n,f,s,I),ba=!1,$=n.memoizedState,f.state=$,eo(n,s,f,u),to();var ot=n.memoizedState;_!==mt||$!==ot||ba||t!==null&&t.dependencies!==null&&ul(t.dependencies)?(typeof T=="function"&&(Vc(n,a,T,s),ot=n.memoizedState),(ft=ba||Sm(n,a,ft,s,$,ot,I)||t!==null&&t.dependencies!==null&&ul(t.dependencies))?(K||typeof f.UNSAFE_componentWillUpdate!="function"&&typeof f.componentWillUpdate!="function"||(typeof f.componentWillUpdate=="function"&&f.componentWillUpdate(s,ot,I),typeof f.UNSAFE_componentWillUpdate=="function"&&f.UNSAFE_componentWillUpdate(s,ot,I)),typeof f.componentDidUpdate=="function"&&(n.flags|=4),typeof f.getSnapshotBeforeUpdate=="function"&&(n.flags|=1024)):(typeof f.componentDidUpdate!="function"||_===t.memoizedProps&&$===t.memoizedState||(n.flags|=4),typeof f.getSnapshotBeforeUpdate!="function"||_===t.memoizedProps&&$===t.memoizedState||(n.flags|=1024),n.memoizedProps=s,n.memoizedState=ot),f.props=s,f.state=ot,f.context=I,s=ft):(typeof f.componentDidUpdate!="function"||_===t.memoizedProps&&$===t.memoizedState||(n.flags|=4),typeof f.getSnapshotBeforeUpdate!="function"||_===t.memoizedProps&&$===t.memoizedState||(n.flags|=1024),s=!1)}return f=s,Cl(t,n),s=(n.flags&128)!==0,f||s?(f=n.stateNode,a=s&&typeof a.getDerivedStateFromError!="function"?null:f.render(),n.flags|=1,t!==null&&s?(n.child=fr(n,t.child,null,u),n.child=fr(n,null,a,u)):Tn(t,n,a,u),n.memoizedState=f.state,t=n.child):t=Ki(t,n,u),t}function Fm(t,n,a,s){return rr(),n.flags|=256,Tn(t,n,a,s),n.child}var Yc={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function Zc(t){return{baseLanes:t,cachePool:bp()}}function jc(t,n,a){return t=t!==null?t.childLanes&~a:0,n&&(t|=jn),t}function zm(t,n,a){var s=n.pendingProps,u=!1,f=(n.flags&128)!==0,_;if((_=f)||(_=t!==null&&t.memoizedState===null?!1:(en.current&2)!==0),_&&(u=!0,n.flags&=-129),_=(n.flags&32)!==0,n.flags&=-33,t===null){if(ve){if(u?Ca(n):Da(),(t=ke)?(t=Wg(t,si),t=t!==null&&t.data!=="&"?t:null,t!==null&&(n.memoizedState={dehydrated:t,treeContext:Ma!==null?{id:Ai,overflow:Ri}:null,retryLane:536870912,hydrationErrors:null},a=gp(t),a.return=n,n.child=a,yn=n,ke=null)):t=null,t===null)throw Ea(n);return Lf(t)?n.lanes=32:n.lanes=536870912,null}var T=s.children;return s=s.fallback,u?(Da(),u=n.mode,T=Dl({mode:"hidden",children:T},u),s=ar(s,u,a,null),T.return=n,s.return=n,T.sibling=s,n.child=T,s=n.child,s.memoizedState=Zc(a),s.childLanes=jc(t,_,a),n.memoizedState=Yc,so(null,s)):(Ca(n),Kc(n,T))}var I=t.memoizedState;if(I!==null&&(T=I.dehydrated,T!==null)){if(f)n.flags&256?(Ca(n),n.flags&=-257,n=Qc(t,n,a)):n.memoizedState!==null?(Da(),n.child=t.child,n.flags|=128,n=null):(Da(),T=s.fallback,u=n.mode,s=Dl({mode:"visible",children:s.children},u),T=ar(T,u,a,null),T.flags|=2,s.return=n,T.return=n,s.sibling=T,n.child=s,fr(n,t.child,null,a),s=n.child,s.memoizedState=Zc(a),s.childLanes=jc(t,_,a),n.memoizedState=Yc,n=so(null,s));else if(Ca(n),Lf(T)){if(_=T.nextSibling&&T.nextSibling.dataset,_)var K=_.dgst;_=K,s=Error(r(419)),s.stack="",s.digest=_,Zs({value:s,source:null,stack:null}),n=Qc(t,n,a)}else if(on||Xr(t,n,a,!1),_=(a&t.childLanes)!==0,on||_){if(_=Ve,_!==null&&(s=Cr(_,a),s!==0&&s!==I.retryLane))throw I.retryLane=s,ir(t,s),Gn(_,t,s),Wc;Uf(T)||Bl(),n=Qc(t,n,a)}else Uf(T)?(n.flags|=192,n.child=t.child,n=null):(t=I.treeContext,ke=li(T.nextSibling),yn=n,ve=!0,ya=null,si=!1,t!==null&&xp(n,t),n=Kc(n,s.children),n.flags|=4096);return n}return u?(Da(),T=s.fallback,u=n.mode,I=t.child,K=I.sibling,s=ki(I,{mode:"hidden",children:s.children}),s.subtreeFlags=I.subtreeFlags&65011712,K!==null?T=ki(K,T):(T=ar(T,u,a,null),T.flags|=2),T.return=n,s.return=n,s.sibling=T,n.child=s,so(null,s),s=n.child,T=t.child.memoizedState,T===null?T=Zc(a):(u=T.cachePool,u!==null?(I=rn._currentValue,u=u.parent!==I?{parent:I,pool:I}:u):u=bp(),T={baseLanes:T.baseLanes|a,cachePool:u}),s.memoizedState=T,s.childLanes=jc(t,_,a),n.memoizedState=Yc,so(t.child,s)):(Ca(n),a=t.child,t=a.sibling,a=ki(a,{mode:"visible",children:s.children}),a.return=n,a.sibling=null,t!==null&&(_=n.deletions,_===null?(n.deletions=[t],n.flags|=16):_.push(t)),n.child=a,n.memoizedState=null,a)}function Kc(t,n){return n=Dl({mode:"visible",children:n},t.mode),n.return=t,t.child=n}function Dl(t,n){return t=Wn(22,t,null,n),t.lanes=0,t}function Qc(t,n,a){return fr(n,t.child,null,a),t=Kc(n,n.pendingProps.children),t.flags|=2,n.memoizedState=null,t}function Bm(t,n,a){t.lanes|=n;var s=t.alternate;s!==null&&(s.lanes|=n),hc(t.return,n,a)}function Jc(t,n,a,s,u,f){var _=t.memoizedState;_===null?t.memoizedState={isBackwards:n,rendering:null,renderingStartTime:0,last:s,tail:a,tailMode:u,treeForkCount:f}:(_.isBackwards=n,_.rendering=null,_.renderingStartTime=0,_.last=s,_.tail=a,_.tailMode=u,_.treeForkCount=f)}function Im(t,n,a){var s=n.pendingProps,u=s.revealOrder,f=s.tail;s=s.children;var _=en.current,T=(_&2)!==0;if(T?(_=_&1|2,n.flags|=128):_&=1,gt(en,_),Tn(t,n,s,a),s=ve?Ys:0,!T&&t!==null&&(t.flags&128)!==0)t:for(t=n.child;t!==null;){if(t.tag===13)t.memoizedState!==null&&Bm(t,a,n);else if(t.tag===19)Bm(t,a,n);else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===n)break t;for(;t.sibling===null;){if(t.return===null||t.return===n)break t;t=t.return}t.sibling.return=t.return,t=t.sibling}switch(u){case"forwards":for(a=n.child,u=null;a!==null;)t=a.alternate,t!==null&&_l(t)===null&&(u=a),a=a.sibling;a=u,a===null?(u=n.child,n.child=null):(u=a.sibling,a.sibling=null),Jc(n,!1,u,a,f,s);break;case"backwards":case"unstable_legacy-backwards":for(a=null,u=n.child,n.child=null;u!==null;){if(t=u.alternate,t!==null&&_l(t)===null){n.child=u;break}t=u.sibling,u.sibling=a,a=u,u=t}Jc(n,!0,a,null,f,s);break;case"together":Jc(n,!1,null,null,void 0,s);break;default:n.memoizedState=null}return n.child}function Ki(t,n,a){if(t!==null&&(n.dependencies=t.dependencies),La|=n.lanes,(a&n.childLanes)===0)if(t!==null){if(Xr(t,n,a,!1),(a&n.childLanes)===0)return null}else return null;if(t!==null&&n.child!==t.child)throw Error(r(153));if(n.child!==null){for(t=n.child,a=ki(t,t.pendingProps),n.child=a,a.return=n;t.sibling!==null;)t=t.sibling,a=a.sibling=ki(t,t.pendingProps),a.return=n;a.sibling=null}return n.child}function $c(t,n){return(t.lanes&n)!==0?!0:(t=t.dependencies,!!(t!==null&&ul(t)))}function gx(t,n,a){switch(n.tag){case 3:Dt(n,n.stateNode.containerInfo),Ta(n,rn,t.memoizedState.cache),rr();break;case 27:case 5:It(n);break;case 4:Dt(n,n.stateNode.containerInfo);break;case 10:Ta(n,n.type,n.memoizedProps.value);break;case 31:if(n.memoizedState!==null)return n.flags|=128,Tc(n),null;break;case 13:var s=n.memoizedState;if(s!==null)return s.dehydrated!==null?(Ca(n),n.flags|=128,null):(a&n.child.childLanes)!==0?zm(t,n,a):(Ca(n),t=Ki(t,n,a),t!==null?t.sibling:null);Ca(n);break;case 19:var u=(t.flags&128)!==0;if(s=(a&n.childLanes)!==0,s||(Xr(t,n,a,!1),s=(a&n.childLanes)!==0),u){if(s)return Im(t,n,a);n.flags|=128}if(u=n.memoizedState,u!==null&&(u.rendering=null,u.tail=null,u.lastEffect=null),gt(en,en.current),s)break;return null;case 22:return n.lanes=0,Um(t,n,a,n.pendingProps);case 24:Ta(n,rn,t.memoizedState.cache)}return Ki(t,n,a)}function Hm(t,n,a){if(t!==null)if(t.memoizedProps!==n.pendingProps)on=!0;else{if(!$c(t,a)&&(n.flags&128)===0)return on=!1,gx(t,n,a);on=(t.flags&131072)!==0}else on=!1,ve&&(n.flags&1048576)!==0&&vp(n,Ys,n.index);switch(n.lanes=0,n.tag){case 16:t:{var s=n.pendingProps;if(t=ur(n.elementType),n.type=t,typeof t=="function")ac(t)?(s=dr(t,s),n.tag=1,n=Pm(null,n,t,s,a)):(n.tag=0,n=qc(null,n,t,s,a));else{if(t!=null){var u=t.$$typeof;if(u===L){n.tag=11,n=Cm(null,n,t,s,a);break t}else if(u===z){n.tag=14,n=Dm(null,n,t,s,a);break t}}throw n=ut(t)||t,Error(r(306,n,""))}}return n;case 0:return qc(t,n,n.type,n.pendingProps,a);case 1:return s=n.type,u=dr(s,n.pendingProps),Pm(t,n,s,u,a);case 3:t:{if(Dt(n,n.stateNode.containerInfo),t===null)throw Error(r(387));s=n.pendingProps;var f=n.memoizedState;u=f.element,xc(t,n),eo(n,s,null,a);var _=n.memoizedState;if(s=_.cache,Ta(n,rn,s),s!==f.cache&&dc(n,[rn],a,!0),to(),s=_.element,f.isDehydrated)if(f={element:s,isDehydrated:!1,cache:_.cache},n.updateQueue.baseState=f,n.memoizedState=f,n.flags&256){n=Fm(t,n,s,a);break t}else if(s!==u){u=ii(Error(r(424)),n),Zs(u),n=Fm(t,n,s,a);break t}else for(t=n.stateNode.containerInfo,t.nodeType===9?t=t.body:t=t.nodeName==="HTML"?t.ownerDocument.body:t,ke=li(t.firstChild),yn=n,ve=!0,ya=null,si=!0,a=Up(n,null,s,a),n.child=a;a;)a.flags=a.flags&-3|4096,a=a.sibling;else{if(rr(),s===u){n=Ki(t,n,a);break t}Tn(t,n,s,a)}n=n.child}return n;case 26:return Cl(t,n),t===null?(a=Qg(n.type,null,n.pendingProps,null))?n.memoizedState=a:ve||(a=n.type,t=n.pendingProps,s=Wl(tt.current).createElement(a),s[an]=n,s[gn]=t,bn(s,a,t),b(s),n.stateNode=s):n.memoizedState=Qg(n.type,t.memoizedProps,n.pendingProps,t.memoizedState),null;case 27:return It(n),t===null&&ve&&(s=n.stateNode=Zg(n.type,n.pendingProps,tt.current),yn=n,si=!0,u=ke,za(n.type)?(Nf=u,ke=li(s.firstChild)):ke=u),Tn(t,n,n.pendingProps.children,a),Cl(t,n),t===null&&(n.flags|=4194304),n.child;case 5:return t===null&&ve&&((u=s=ke)&&(s=qx(s,n.type,n.pendingProps,si),s!==null?(n.stateNode=s,yn=n,ke=li(s.firstChild),si=!1,u=!0):u=!1),u||Ea(n)),It(n),u=n.type,f=n.pendingProps,_=t!==null?t.memoizedProps:null,s=f.children,Cf(u,f)?s=null:_!==null&&Cf(u,_)&&(n.flags|=32),n.memoizedState!==null&&(u=Ac(t,n,ox,null,null,a),yo._currentValue=u),Cl(t,n),Tn(t,n,s,a),n.child;case 6:return t===null&&ve&&((t=a=ke)&&(a=Yx(a,n.pendingProps,si),a!==null?(n.stateNode=a,yn=n,ke=null,t=!0):t=!1),t||Ea(n)),null;case 13:return zm(t,n,a);case 4:return Dt(n,n.stateNode.containerInfo),s=n.pendingProps,t===null?n.child=fr(n,null,s,a):Tn(t,n,s,a),n.child;case 11:return Cm(t,n,n.type,n.pendingProps,a);case 7:return Tn(t,n,n.pendingProps,a),n.child;case 8:return Tn(t,n,n.pendingProps.children,a),n.child;case 12:return Tn(t,n,n.pendingProps.children,a),n.child;case 10:return s=n.pendingProps,Ta(n,n.type,s.value),Tn(t,n,s.children,a),n.child;case 9:return u=n.type._context,s=n.pendingProps.children,or(n),u=En(u),s=s(u),n.flags|=1,Tn(t,n,s,a),n.child;case 14:return Dm(t,n,n.type,n.pendingProps,a);case 15:return wm(t,n,n.type,n.pendingProps,a);case 19:return Im(t,n,a);case 31:return mx(t,n,a);case 22:return Um(t,n,a,n.pendingProps);case 24:return or(n),s=En(rn),t===null?(u=gc(),u===null&&(u=Ve,f=pc(),u.pooledCache=f,f.refCount++,f!==null&&(u.pooledCacheLanes|=a),u=f),n.memoizedState={parent:s,cache:u},vc(n),Ta(n,rn,u)):((t.lanes&a)!==0&&(xc(t,n),eo(n,null,null,a),to()),u=t.memoizedState,f=n.memoizedState,u.parent!==s?(u={parent:s,cache:s},n.memoizedState=u,n.lanes===0&&(n.memoizedState=n.updateQueue.baseState=u),Ta(n,rn,s)):(s=f.cache,Ta(n,rn,s),s!==u.cache&&dc(n,[rn],a,!0))),Tn(t,n,n.pendingProps.children,a),n.child;case 29:throw n.pendingProps}throw Error(r(156,n.tag))}function Qi(t){t.flags|=4}function tf(t,n,a,s,u){if((n=(t.mode&32)!==0)&&(n=!1),n){if(t.flags|=16777216,(u&335544128)===u)if(t.stateNode.complete)t.flags|=8192;else if(dg())t.flags|=8192;else throw cr=dl,_c}else t.flags&=-16777217}function Gm(t,n){if(n.type!=="stylesheet"||(n.state.loading&4)!==0)t.flags&=-16777217;else if(t.flags|=16777216,!n0(n))if(dg())t.flags|=8192;else throw cr=dl,_c}function wl(t,n){n!==null&&(t.flags|=4),t.flags&16384&&(n=t.tag!==22?Oe():536870912,t.lanes|=n,es|=n)}function oo(t,n){if(!ve)switch(t.tailMode){case"hidden":n=t.tail;for(var a=null;n!==null;)n.alternate!==null&&(a=n),n=n.sibling;a===null?t.tail=null:a.sibling=null;break;case"collapsed":a=t.tail;for(var s=null;a!==null;)a.alternate!==null&&(s=a),a=a.sibling;s===null?n||t.tail===null?t.tail=null:t.tail.sibling=null:s.sibling=null}}function We(t){var n=t.alternate!==null&&t.alternate.child===t.child,a=0,s=0;if(n)for(var u=t.child;u!==null;)a|=u.lanes|u.childLanes,s|=u.subtreeFlags&65011712,s|=u.flags&65011712,u.return=t,u=u.sibling;else for(u=t.child;u!==null;)a|=u.lanes|u.childLanes,s|=u.subtreeFlags,s|=u.flags,u.return=t,u=u.sibling;return t.subtreeFlags|=s,t.childLanes=a,n}function _x(t,n,a){var s=n.pendingProps;switch(lc(n),n.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return We(n),null;case 1:return We(n),null;case 3:return a=n.stateNode,s=null,t!==null&&(s=t.memoizedState.cache),n.memoizedState.cache!==s&&(n.flags|=2048),Yi(rn),Vt(),a.pendingContext&&(a.context=a.pendingContext,a.pendingContext=null),(t===null||t.child===null)&&(Vr(n)?Qi(n):t===null||t.memoizedState.isDehydrated&&(n.flags&256)===0||(n.flags|=1024,cc())),We(n),null;case 26:var u=n.type,f=n.memoizedState;return t===null?(Qi(n),f!==null?(We(n),Gm(n,f)):(We(n),tf(n,u,null,s,a))):f?f!==t.memoizedState?(Qi(n),We(n),Gm(n,f)):(We(n),n.flags&=-16777217):(t=t.memoizedProps,t!==s&&Qi(n),We(n),tf(n,u,t,s,a)),null;case 27:if(fe(n),a=tt.current,u=n.type,t!==null&&n.stateNode!=null)t.memoizedProps!==s&&Qi(n);else{if(!s){if(n.stateNode===null)throw Error(r(166));return We(n),null}t=bt.current,Vr(n)?Sp(n):(t=Zg(u,s,a),n.stateNode=t,Qi(n))}return We(n),null;case 5:if(fe(n),u=n.type,t!==null&&n.stateNode!=null)t.memoizedProps!==s&&Qi(n);else{if(!s){if(n.stateNode===null)throw Error(r(166));return We(n),null}if(f=bt.current,Vr(n))Sp(n);else{var _=Wl(tt.current);switch(f){case 1:f=_.createElementNS("http://www.w3.org/2000/svg",u);break;case 2:f=_.createElementNS("http://www.w3.org/1998/Math/MathML",u);break;default:switch(u){case"svg":f=_.createElementNS("http://www.w3.org/2000/svg",u);break;case"math":f=_.createElementNS("http://www.w3.org/1998/Math/MathML",u);break;case"script":f=_.createElement("div"),f.innerHTML="<script><\/script>",f=f.removeChild(f.firstChild);break;case"select":f=typeof s.is=="string"?_.createElement("select",{is:s.is}):_.createElement("select"),s.multiple?f.multiple=!0:s.size&&(f.size=s.size);break;default:f=typeof s.is=="string"?_.createElement(u,{is:s.is}):_.createElement(u)}}f[an]=n,f[gn]=s;t:for(_=n.child;_!==null;){if(_.tag===5||_.tag===6)f.appendChild(_.stateNode);else if(_.tag!==4&&_.tag!==27&&_.child!==null){_.child.return=_,_=_.child;continue}if(_===n)break t;for(;_.sibling===null;){if(_.return===null||_.return===n)break t;_=_.return}_.sibling.return=_.return,_=_.sibling}n.stateNode=f;t:switch(bn(f,u,s),u){case"button":case"input":case"select":case"textarea":s=!!s.autoFocus;break t;case"img":s=!0;break t;default:s=!1}s&&Qi(n)}}return We(n),tf(n,n.type,t===null?null:t.memoizedProps,n.pendingProps,a),null;case 6:if(t&&n.stateNode!=null)t.memoizedProps!==s&&Qi(n);else{if(typeof s!="string"&&n.stateNode===null)throw Error(r(166));if(t=tt.current,Vr(n)){if(t=n.stateNode,a=n.memoizedProps,s=null,u=yn,u!==null)switch(u.tag){case 27:case 5:s=u.memoizedProps}t[an]=n,t=!!(t.nodeValue===a||s!==null&&s.suppressHydrationWarning===!0||zg(t.nodeValue,a)),t||Ea(n,!0)}else t=Wl(t).createTextNode(s),t[an]=n,n.stateNode=t}return We(n),null;case 31:if(a=n.memoizedState,t===null||t.memoizedState!==null){if(s=Vr(n),a!==null){if(t===null){if(!s)throw Error(r(318));if(t=n.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(557));t[an]=n}else rr(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;We(n),t=!1}else a=cc(),t!==null&&t.memoizedState!==null&&(t.memoizedState.hydrationErrors=a),t=!0;if(!t)return n.flags&256?(Yn(n),n):(Yn(n),null);if((n.flags&128)!==0)throw Error(r(558))}return We(n),null;case 13:if(s=n.memoizedState,t===null||t.memoizedState!==null&&t.memoizedState.dehydrated!==null){if(u=Vr(n),s!==null&&s.dehydrated!==null){if(t===null){if(!u)throw Error(r(318));if(u=n.memoizedState,u=u!==null?u.dehydrated:null,!u)throw Error(r(317));u[an]=n}else rr(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;We(n),u=!1}else u=cc(),t!==null&&t.memoizedState!==null&&(t.memoizedState.hydrationErrors=u),u=!0;if(!u)return n.flags&256?(Yn(n),n):(Yn(n),null)}return Yn(n),(n.flags&128)!==0?(n.lanes=a,n):(a=s!==null,t=t!==null&&t.memoizedState!==null,a&&(s=n.child,u=null,s.alternate!==null&&s.alternate.memoizedState!==null&&s.alternate.memoizedState.cachePool!==null&&(u=s.alternate.memoizedState.cachePool.pool),f=null,s.memoizedState!==null&&s.memoizedState.cachePool!==null&&(f=s.memoizedState.cachePool.pool),f!==u&&(s.flags|=2048)),a!==t&&a&&(n.child.flags|=8192),wl(n,n.updateQueue),We(n),null);case 4:return Vt(),t===null&&Ef(n.stateNode.containerInfo),We(n),null;case 10:return Yi(n.type),We(n),null;case 19:if(et(en),s=n.memoizedState,s===null)return We(n),null;if(u=(n.flags&128)!==0,f=s.rendering,f===null)if(u)oo(s,!1);else{if(Je!==0||t!==null&&(t.flags&128)!==0)for(t=n.child;t!==null;){if(f=_l(t),f!==null){for(n.flags|=128,oo(s,!1),t=f.updateQueue,n.updateQueue=t,wl(n,t),n.subtreeFlags=0,t=a,a=n.child;a!==null;)mp(a,t),a=a.sibling;return gt(en,en.current&1|2),ve&&Wi(n,s.treeForkCount),n.child}t=t.sibling}s.tail!==null&&E()>Pl&&(n.flags|=128,u=!0,oo(s,!1),n.lanes=4194304)}else{if(!u)if(t=_l(f),t!==null){if(n.flags|=128,u=!0,t=t.updateQueue,n.updateQueue=t,wl(n,t),oo(s,!0),s.tail===null&&s.tailMode==="hidden"&&!f.alternate&&!ve)return We(n),null}else 2*E()-s.renderingStartTime>Pl&&a!==536870912&&(n.flags|=128,u=!0,oo(s,!1),n.lanes=4194304);s.isBackwards?(f.sibling=n.child,n.child=f):(t=s.last,t!==null?t.sibling=f:n.child=f,s.last=f)}return s.tail!==null?(t=s.tail,s.rendering=t,s.tail=t.sibling,s.renderingStartTime=E(),t.sibling=null,a=en.current,gt(en,u?a&1|2:a&1),ve&&Wi(n,s.treeForkCount),t):(We(n),null);case 22:case 23:return Yn(n),Ec(),s=n.memoizedState!==null,t!==null?t.memoizedState!==null!==s&&(n.flags|=8192):s&&(n.flags|=8192),s?(a&536870912)!==0&&(n.flags&128)===0&&(We(n),n.subtreeFlags&6&&(n.flags|=8192)):We(n),a=n.updateQueue,a!==null&&wl(n,a.retryQueue),a=null,t!==null&&t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(a=t.memoizedState.cachePool.pool),s=null,n.memoizedState!==null&&n.memoizedState.cachePool!==null&&(s=n.memoizedState.cachePool.pool),s!==a&&(n.flags|=2048),t!==null&&et(lr),null;case 24:return a=null,t!==null&&(a=t.memoizedState.cache),n.memoizedState.cache!==a&&(n.flags|=2048),Yi(rn),We(n),null;case 25:return null;case 30:return null}throw Error(r(156,n.tag))}function vx(t,n){switch(lc(n),n.tag){case 1:return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 3:return Yi(rn),Vt(),t=n.flags,(t&65536)!==0&&(t&128)===0?(n.flags=t&-65537|128,n):null;case 26:case 27:case 5:return fe(n),null;case 31:if(n.memoizedState!==null){if(Yn(n),n.alternate===null)throw Error(r(340));rr()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 13:if(Yn(n),t=n.memoizedState,t!==null&&t.dehydrated!==null){if(n.alternate===null)throw Error(r(340));rr()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 19:return et(en),null;case 4:return Vt(),null;case 10:return Yi(n.type),null;case 22:case 23:return Yn(n),Ec(),t!==null&&et(lr),t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 24:return Yi(rn),null;case 25:return null;default:return null}}function Vm(t,n){switch(lc(n),n.tag){case 3:Yi(rn),Vt();break;case 26:case 27:case 5:fe(n);break;case 4:Vt();break;case 31:n.memoizedState!==null&&Yn(n);break;case 13:Yn(n);break;case 19:et(en);break;case 10:Yi(n.type);break;case 22:case 23:Yn(n),Ec(),t!==null&&et(lr);break;case 24:Yi(rn)}}function lo(t,n){try{var a=n.updateQueue,s=a!==null?a.lastEffect:null;if(s!==null){var u=s.next;a=u;do{if((a.tag&t)===t){s=void 0;var f=a.create,_=a.inst;s=f(),_.destroy=s}a=a.next}while(a!==u)}}catch(T){ze(n,n.return,T)}}function wa(t,n,a){try{var s=n.updateQueue,u=s!==null?s.lastEffect:null;if(u!==null){var f=u.next;s=f;do{if((s.tag&t)===t){var _=s.inst,T=_.destroy;if(T!==void 0){_.destroy=void 0,u=n;var I=a,K=T;try{K()}catch(ft){ze(u,I,ft)}}}s=s.next}while(s!==f)}}catch(ft){ze(n,n.return,ft)}}function Xm(t){var n=t.updateQueue;if(n!==null){var a=t.stateNode;try{Np(n,a)}catch(s){ze(t,t.return,s)}}}function km(t,n,a){a.props=dr(t.type,t.memoizedProps),a.state=t.memoizedState;try{a.componentWillUnmount()}catch(s){ze(t,n,s)}}function uo(t,n){try{var a=t.ref;if(a!==null){switch(t.tag){case 26:case 27:case 5:var s=t.stateNode;break;case 30:s=t.stateNode;break;default:s=t.stateNode}typeof a=="function"?t.refCleanup=a(s):a.current=s}}catch(u){ze(t,n,u)}}function Ci(t,n){var a=t.ref,s=t.refCleanup;if(a!==null)if(typeof s=="function")try{s()}catch(u){ze(t,n,u)}finally{t.refCleanup=null,t=t.alternate,t!=null&&(t.refCleanup=null)}else if(typeof a=="function")try{a(null)}catch(u){ze(t,n,u)}else a.current=null}function Wm(t){var n=t.type,a=t.memoizedProps,s=t.stateNode;try{t:switch(n){case"button":case"input":case"select":case"textarea":a.autoFocus&&s.focus();break t;case"img":a.src?s.src=a.src:a.srcSet&&(s.srcset=a.srcSet)}}catch(u){ze(t,t.return,u)}}function ef(t,n,a){try{var s=t.stateNode;Hx(s,t.type,a,n),s[gn]=n}catch(u){ze(t,t.return,u)}}function qm(t){return t.tag===5||t.tag===3||t.tag===26||t.tag===27&&za(t.type)||t.tag===4}function nf(t){t:for(;;){for(;t.sibling===null;){if(t.return===null||qm(t.return))return null;t=t.return}for(t.sibling.return=t.return,t=t.sibling;t.tag!==5&&t.tag!==6&&t.tag!==18;){if(t.tag===27&&za(t.type)||t.flags&2||t.child===null||t.tag===4)continue t;t.child.return=t,t=t.child}if(!(t.flags&2))return t.stateNode}}function af(t,n,a){var s=t.tag;if(s===5||s===6)t=t.stateNode,n?(a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a).insertBefore(t,n):(n=a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a,n.appendChild(t),a=a._reactRootContainer,a!=null||n.onclick!==null||(n.onclick=Vi));else if(s!==4&&(s===27&&za(t.type)&&(a=t.stateNode,n=null),t=t.child,t!==null))for(af(t,n,a),t=t.sibling;t!==null;)af(t,n,a),t=t.sibling}function Ul(t,n,a){var s=t.tag;if(s===5||s===6)t=t.stateNode,n?a.insertBefore(t,n):a.appendChild(t);else if(s!==4&&(s===27&&za(t.type)&&(a=t.stateNode),t=t.child,t!==null))for(Ul(t,n,a),t=t.sibling;t!==null;)Ul(t,n,a),t=t.sibling}function Ym(t){var n=t.stateNode,a=t.memoizedProps;try{for(var s=t.type,u=n.attributes;u.length;)n.removeAttributeNode(u[0]);bn(n,s,a),n[an]=t,n[gn]=a}catch(f){ze(t,t.return,f)}}var Ji=!1,ln=!1,rf=!1,Zm=typeof WeakSet=="function"?WeakSet:Set,pn=null;function xx(t,n){if(t=t.containerInfo,Af=Jl,t=sp(t),Qu(t)){if("selectionStart"in t)var a={start:t.selectionStart,end:t.selectionEnd};else t:{a=(a=t.ownerDocument)&&a.defaultView||window;var s=a.getSelection&&a.getSelection();if(s&&s.rangeCount!==0){a=s.anchorNode;var u=s.anchorOffset,f=s.focusNode;s=s.focusOffset;try{a.nodeType,f.nodeType}catch{a=null;break t}var _=0,T=-1,I=-1,K=0,ft=0,mt=t,$=null;e:for(;;){for(var ot;mt!==a||u!==0&&mt.nodeType!==3||(T=_+u),mt!==f||s!==0&&mt.nodeType!==3||(I=_+s),mt.nodeType===3&&(_+=mt.nodeValue.length),(ot=mt.firstChild)!==null;)$=mt,mt=ot;for(;;){if(mt===t)break e;if($===a&&++K===u&&(T=_),$===f&&++ft===s&&(I=_),(ot=mt.nextSibling)!==null)break;mt=$,$=mt.parentNode}mt=ot}a=T===-1||I===-1?null:{start:T,end:I}}else a=null}a=a||{start:0,end:0}}else a=null;for(Rf={focusedElem:t,selectionRange:a},Jl=!1,pn=n;pn!==null;)if(n=pn,t=n.child,(n.subtreeFlags&1028)!==0&&t!==null)t.return=n,pn=t;else for(;pn!==null;){switch(n=pn,f=n.alternate,t=n.flags,n.tag){case 0:if((t&4)!==0&&(t=n.updateQueue,t=t!==null?t.events:null,t!==null))for(a=0;a<t.length;a++)u=t[a],u.ref.impl=u.nextImpl;break;case 11:case 15:break;case 1:if((t&1024)!==0&&f!==null){t=void 0,a=n,u=f.memoizedProps,f=f.memoizedState,s=a.stateNode;try{var Gt=dr(a.type,u);t=s.getSnapshotBeforeUpdate(Gt,f),s.__reactInternalSnapshotBeforeUpdate=t}catch($t){ze(a,a.return,$t)}}break;case 3:if((t&1024)!==0){if(t=n.stateNode.containerInfo,a=t.nodeType,a===9)wf(t);else if(a===1)switch(t.nodeName){case"HEAD":case"HTML":case"BODY":wf(t);break;default:t.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;default:if((t&1024)!==0)throw Error(r(163))}if(t=n.sibling,t!==null){t.return=n.return,pn=t;break}pn=n.return}}function jm(t,n,a){var s=a.flags;switch(a.tag){case 0:case 11:case 15:ta(t,a),s&4&&lo(5,a);break;case 1:if(ta(t,a),s&4)if(t=a.stateNode,n===null)try{t.componentDidMount()}catch(_){ze(a,a.return,_)}else{var u=dr(a.type,n.memoizedProps);n=n.memoizedState;try{t.componentDidUpdate(u,n,t.__reactInternalSnapshotBeforeUpdate)}catch(_){ze(a,a.return,_)}}s&64&&Xm(a),s&512&&uo(a,a.return);break;case 3:if(ta(t,a),s&64&&(t=a.updateQueue,t!==null)){if(n=null,a.child!==null)switch(a.child.tag){case 27:case 5:n=a.child.stateNode;break;case 1:n=a.child.stateNode}try{Np(t,n)}catch(_){ze(a,a.return,_)}}break;case 27:n===null&&s&4&&Ym(a);case 26:case 5:ta(t,a),n===null&&s&4&&Wm(a),s&512&&uo(a,a.return);break;case 12:ta(t,a);break;case 31:ta(t,a),s&4&&Jm(t,a);break;case 13:ta(t,a),s&4&&$m(t,a),s&64&&(t=a.memoizedState,t!==null&&(t=t.dehydrated,t!==null&&(a=Cx.bind(null,a),Zx(t,a))));break;case 22:if(s=a.memoizedState!==null||Ji,!s){n=n!==null&&n.memoizedState!==null||ln,u=Ji;var f=ln;Ji=s,(ln=n)&&!f?ea(t,a,(a.subtreeFlags&8772)!==0):ta(t,a),Ji=u,ln=f}break;case 30:break;default:ta(t,a)}}function Km(t){var n=t.alternate;n!==null&&(t.alternate=null,Km(n)),t.child=null,t.deletions=null,t.sibling=null,t.tag===5&&(n=t.stateNode,n!==null&&zs(n)),t.stateNode=null,t.return=null,t.dependencies=null,t.memoizedProps=null,t.memoizedState=null,t.pendingProps=null,t.stateNode=null,t.updateQueue=null}var Ze=null,zn=!1;function $i(t,n,a){for(a=a.child;a!==null;)Qm(t,n,a),a=a.sibling}function Qm(t,n,a){if(Et&&typeof Et.onCommitFiberUnmount=="function")try{Et.onCommitFiberUnmount(yt,a)}catch{}switch(a.tag){case 26:ln||Ci(a,n),$i(t,n,a),a.memoizedState?a.memoizedState.count--:a.stateNode&&(a=a.stateNode,a.parentNode.removeChild(a));break;case 27:ln||Ci(a,n);var s=Ze,u=zn;za(a.type)&&(Ze=a.stateNode,zn=!1),$i(t,n,a),xo(a.stateNode),Ze=s,zn=u;break;case 5:ln||Ci(a,n);case 6:if(s=Ze,u=zn,Ze=null,$i(t,n,a),Ze=s,zn=u,Ze!==null)if(zn)try{(Ze.nodeType===9?Ze.body:Ze.nodeName==="HTML"?Ze.ownerDocument.body:Ze).removeChild(a.stateNode)}catch(f){ze(a,n,f)}else try{Ze.removeChild(a.stateNode)}catch(f){ze(a,n,f)}break;case 18:Ze!==null&&(zn?(t=Ze,Xg(t.nodeType===9?t.body:t.nodeName==="HTML"?t.ownerDocument.body:t,a.stateNode),us(t)):Xg(Ze,a.stateNode));break;case 4:s=Ze,u=zn,Ze=a.stateNode.containerInfo,zn=!0,$i(t,n,a),Ze=s,zn=u;break;case 0:case 11:case 14:case 15:wa(2,a,n),ln||wa(4,a,n),$i(t,n,a);break;case 1:ln||(Ci(a,n),s=a.stateNode,typeof s.componentWillUnmount=="function"&&km(a,n,s)),$i(t,n,a);break;case 21:$i(t,n,a);break;case 22:ln=(s=ln)||a.memoizedState!==null,$i(t,n,a),ln=s;break;default:$i(t,n,a)}}function Jm(t,n){if(n.memoizedState===null&&(t=n.alternate,t!==null&&(t=t.memoizedState,t!==null))){t=t.dehydrated;try{us(t)}catch(a){ze(n,n.return,a)}}}function $m(t,n){if(n.memoizedState===null&&(t=n.alternate,t!==null&&(t=t.memoizedState,t!==null&&(t=t.dehydrated,t!==null))))try{us(t)}catch(a){ze(n,n.return,a)}}function Sx(t){switch(t.tag){case 31:case 13:case 19:var n=t.stateNode;return n===null&&(n=t.stateNode=new Zm),n;case 22:return t=t.stateNode,n=t._retryCache,n===null&&(n=t._retryCache=new Zm),n;default:throw Error(r(435,t.tag))}}function Ll(t,n){var a=Sx(t);n.forEach(function(s){if(!a.has(s)){a.add(s);var u=Dx.bind(null,t,s);s.then(u,u)}})}function Bn(t,n){var a=n.deletions;if(a!==null)for(var s=0;s<a.length;s++){var u=a[s],f=t,_=n,T=_;t:for(;T!==null;){switch(T.tag){case 27:if(za(T.type)){Ze=T.stateNode,zn=!1;break t}break;case 5:Ze=T.stateNode,zn=!1;break t;case 3:case 4:Ze=T.stateNode.containerInfo,zn=!0;break t}T=T.return}if(Ze===null)throw Error(r(160));Qm(f,_,u),Ze=null,zn=!1,f=u.alternate,f!==null&&(f.return=null),u.return=null}if(n.subtreeFlags&13886)for(n=n.child;n!==null;)tg(n,t),n=n.sibling}var _i=null;function tg(t,n){var a=t.alternate,s=t.flags;switch(t.tag){case 0:case 11:case 14:case 15:Bn(n,t),In(t),s&4&&(wa(3,t,t.return),lo(3,t),wa(5,t,t.return));break;case 1:Bn(n,t),In(t),s&512&&(ln||a===null||Ci(a,a.return)),s&64&&Ji&&(t=t.updateQueue,t!==null&&(s=t.callbacks,s!==null&&(a=t.shared.hiddenCallbacks,t.shared.hiddenCallbacks=a===null?s:a.concat(s))));break;case 26:var u=_i;if(Bn(n,t),In(t),s&512&&(ln||a===null||Ci(a,a.return)),s&4){var f=a!==null?a.memoizedState:null;if(s=t.memoizedState,a===null)if(s===null)if(t.stateNode===null){t:{s=t.type,a=t.memoizedProps,u=u.ownerDocument||u;e:switch(s){case"title":f=u.getElementsByTagName("title")[0],(!f||f[Ja]||f[an]||f.namespaceURI==="http://www.w3.org/2000/svg"||f.hasAttribute("itemprop"))&&(f=u.createElement(s),u.head.insertBefore(f,u.querySelector("head > title"))),bn(f,s,a),f[an]=t,b(f),s=f;break t;case"link":var _=t0("link","href",u).get(s+(a.href||""));if(_){for(var T=0;T<_.length;T++)if(f=_[T],f.getAttribute("href")===(a.href==null||a.href===""?null:a.href)&&f.getAttribute("rel")===(a.rel==null?null:a.rel)&&f.getAttribute("title")===(a.title==null?null:a.title)&&f.getAttribute("crossorigin")===(a.crossOrigin==null?null:a.crossOrigin)){_.splice(T,1);break e}}f=u.createElement(s),bn(f,s,a),u.head.appendChild(f);break;case"meta":if(_=t0("meta","content",u).get(s+(a.content||""))){for(T=0;T<_.length;T++)if(f=_[T],f.getAttribute("content")===(a.content==null?null:""+a.content)&&f.getAttribute("name")===(a.name==null?null:a.name)&&f.getAttribute("property")===(a.property==null?null:a.property)&&f.getAttribute("http-equiv")===(a.httpEquiv==null?null:a.httpEquiv)&&f.getAttribute("charset")===(a.charSet==null?null:a.charSet)){_.splice(T,1);break e}}f=u.createElement(s),bn(f,s,a),u.head.appendChild(f);break;default:throw Error(r(468,s))}f[an]=t,b(f),s=f}t.stateNode=s}else e0(u,t.type,t.stateNode);else t.stateNode=$g(u,s,t.memoizedProps);else f!==s?(f===null?a.stateNode!==null&&(a=a.stateNode,a.parentNode.removeChild(a)):f.count--,s===null?e0(u,t.type,t.stateNode):$g(u,s,t.memoizedProps)):s===null&&t.stateNode!==null&&ef(t,t.memoizedProps,a.memoizedProps)}break;case 27:Bn(n,t),In(t),s&512&&(ln||a===null||Ci(a,a.return)),a!==null&&s&4&&ef(t,t.memoizedProps,a.memoizedProps);break;case 5:if(Bn(n,t),In(t),s&512&&(ln||a===null||Ci(a,a.return)),t.flags&32){u=t.stateNode;try{cn(u,"")}catch(Gt){ze(t,t.return,Gt)}}s&4&&t.stateNode!=null&&(u=t.memoizedProps,ef(t,u,a!==null?a.memoizedProps:u)),s&1024&&(rf=!0);break;case 6:if(Bn(n,t),In(t),s&4){if(t.stateNode===null)throw Error(r(162));s=t.memoizedProps,a=t.stateNode;try{a.nodeValue=s}catch(Gt){ze(t,t.return,Gt)}}break;case 3:if(Zl=null,u=_i,_i=ql(n.containerInfo),Bn(n,t),_i=u,In(t),s&4&&a!==null&&a.memoizedState.isDehydrated)try{us(n.containerInfo)}catch(Gt){ze(t,t.return,Gt)}rf&&(rf=!1,eg(t));break;case 4:s=_i,_i=ql(t.stateNode.containerInfo),Bn(n,t),In(t),_i=s;break;case 12:Bn(n,t),In(t);break;case 31:Bn(n,t),In(t),s&4&&(s=t.updateQueue,s!==null&&(t.updateQueue=null,Ll(t,s)));break;case 13:Bn(n,t),In(t),t.child.flags&8192&&t.memoizedState!==null!=(a!==null&&a.memoizedState!==null)&&(Ol=E()),s&4&&(s=t.updateQueue,s!==null&&(t.updateQueue=null,Ll(t,s)));break;case 22:u=t.memoizedState!==null;var I=a!==null&&a.memoizedState!==null,K=Ji,ft=ln;if(Ji=K||u,ln=ft||I,Bn(n,t),ln=ft,Ji=K,In(t),s&8192)t:for(n=t.stateNode,n._visibility=u?n._visibility&-2:n._visibility|1,u&&(a===null||I||Ji||ln||pr(t)),a=null,n=t;;){if(n.tag===5||n.tag===26){if(a===null){I=a=n;try{if(f=I.stateNode,u)_=f.style,typeof _.setProperty=="function"?_.setProperty("display","none","important"):_.display="none";else{T=I.stateNode;var mt=I.memoizedProps.style,$=mt!=null&&mt.hasOwnProperty("display")?mt.display:null;T.style.display=$==null||typeof $=="boolean"?"":(""+$).trim()}}catch(Gt){ze(I,I.return,Gt)}}}else if(n.tag===6){if(a===null){I=n;try{I.stateNode.nodeValue=u?"":I.memoizedProps}catch(Gt){ze(I,I.return,Gt)}}}else if(n.tag===18){if(a===null){I=n;try{var ot=I.stateNode;u?kg(ot,!0):kg(I.stateNode,!1)}catch(Gt){ze(I,I.return,Gt)}}}else if((n.tag!==22&&n.tag!==23||n.memoizedState===null||n===t)&&n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break t;for(;n.sibling===null;){if(n.return===null||n.return===t)break t;a===n&&(a=null),n=n.return}a===n&&(a=null),n.sibling.return=n.return,n=n.sibling}s&4&&(s=t.updateQueue,s!==null&&(a=s.retryQueue,a!==null&&(s.retryQueue=null,Ll(t,a))));break;case 19:Bn(n,t),In(t),s&4&&(s=t.updateQueue,s!==null&&(t.updateQueue=null,Ll(t,s)));break;case 30:break;case 21:break;default:Bn(n,t),In(t)}}function In(t){var n=t.flags;if(n&2){try{for(var a,s=t.return;s!==null;){if(qm(s)){a=s;break}s=s.return}if(a==null)throw Error(r(160));switch(a.tag){case 27:var u=a.stateNode,f=nf(t);Ul(t,f,u);break;case 5:var _=a.stateNode;a.flags&32&&(cn(_,""),a.flags&=-33);var T=nf(t);Ul(t,T,_);break;case 3:case 4:var I=a.stateNode.containerInfo,K=nf(t);af(t,K,I);break;default:throw Error(r(161))}}catch(ft){ze(t,t.return,ft)}t.flags&=-3}n&4096&&(t.flags&=-4097)}function eg(t){if(t.subtreeFlags&1024)for(t=t.child;t!==null;){var n=t;eg(n),n.tag===5&&n.flags&1024&&n.stateNode.reset(),t=t.sibling}}function ta(t,n){if(n.subtreeFlags&8772)for(n=n.child;n!==null;)jm(t,n.alternate,n),n=n.sibling}function pr(t){for(t=t.child;t!==null;){var n=t;switch(n.tag){case 0:case 11:case 14:case 15:wa(4,n,n.return),pr(n);break;case 1:Ci(n,n.return);var a=n.stateNode;typeof a.componentWillUnmount=="function"&&km(n,n.return,a),pr(n);break;case 27:xo(n.stateNode);case 26:case 5:Ci(n,n.return),pr(n);break;case 22:n.memoizedState===null&&pr(n);break;case 30:pr(n);break;default:pr(n)}t=t.sibling}}function ea(t,n,a){for(a=a&&(n.subtreeFlags&8772)!==0,n=n.child;n!==null;){var s=n.alternate,u=t,f=n,_=f.flags;switch(f.tag){case 0:case 11:case 15:ea(u,f,a),lo(4,f);break;case 1:if(ea(u,f,a),s=f,u=s.stateNode,typeof u.componentDidMount=="function")try{u.componentDidMount()}catch(K){ze(s,s.return,K)}if(s=f,u=s.updateQueue,u!==null){var T=s.stateNode;try{var I=u.shared.hiddenCallbacks;if(I!==null)for(u.shared.hiddenCallbacks=null,u=0;u<I.length;u++)Lp(I[u],T)}catch(K){ze(s,s.return,K)}}a&&_&64&&Xm(f),uo(f,f.return);break;case 27:Ym(f);case 26:case 5:ea(u,f,a),a&&s===null&&_&4&&Wm(f),uo(f,f.return);break;case 12:ea(u,f,a);break;case 31:ea(u,f,a),a&&_&4&&Jm(u,f);break;case 13:ea(u,f,a),a&&_&4&&$m(u,f);break;case 22:f.memoizedState===null&&ea(u,f,a),uo(f,f.return);break;case 30:break;default:ea(u,f,a)}n=n.sibling}}function sf(t,n){var a=null;t!==null&&t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(a=t.memoizedState.cachePool.pool),t=null,n.memoizedState!==null&&n.memoizedState.cachePool!==null&&(t=n.memoizedState.cachePool.pool),t!==a&&(t!=null&&t.refCount++,a!=null&&js(a))}function of(t,n){t=null,n.alternate!==null&&(t=n.alternate.memoizedState.cache),n=n.memoizedState.cache,n!==t&&(n.refCount++,t!=null&&js(t))}function vi(t,n,a,s){if(n.subtreeFlags&10256)for(n=n.child;n!==null;)ng(t,n,a,s),n=n.sibling}function ng(t,n,a,s){var u=n.flags;switch(n.tag){case 0:case 11:case 15:vi(t,n,a,s),u&2048&&lo(9,n);break;case 1:vi(t,n,a,s);break;case 3:vi(t,n,a,s),u&2048&&(t=null,n.alternate!==null&&(t=n.alternate.memoizedState.cache),n=n.memoizedState.cache,n!==t&&(n.refCount++,t!=null&&js(t)));break;case 12:if(u&2048){vi(t,n,a,s),t=n.stateNode;try{var f=n.memoizedProps,_=f.id,T=f.onPostCommit;typeof T=="function"&&T(_,n.alternate===null?"mount":"update",t.passiveEffectDuration,-0)}catch(I){ze(n,n.return,I)}}else vi(t,n,a,s);break;case 31:vi(t,n,a,s);break;case 13:vi(t,n,a,s);break;case 23:break;case 22:f=n.stateNode,_=n.alternate,n.memoizedState!==null?f._visibility&2?vi(t,n,a,s):co(t,n):f._visibility&2?vi(t,n,a,s):(f._visibility|=2,Jr(t,n,a,s,(n.subtreeFlags&10256)!==0||!1)),u&2048&&sf(_,n);break;case 24:vi(t,n,a,s),u&2048&&of(n.alternate,n);break;default:vi(t,n,a,s)}}function Jr(t,n,a,s,u){for(u=u&&((n.subtreeFlags&10256)!==0||!1),n=n.child;n!==null;){var f=t,_=n,T=a,I=s,K=_.flags;switch(_.tag){case 0:case 11:case 15:Jr(f,_,T,I,u),lo(8,_);break;case 23:break;case 22:var ft=_.stateNode;_.memoizedState!==null?ft._visibility&2?Jr(f,_,T,I,u):co(f,_):(ft._visibility|=2,Jr(f,_,T,I,u)),u&&K&2048&&sf(_.alternate,_);break;case 24:Jr(f,_,T,I,u),u&&K&2048&&of(_.alternate,_);break;default:Jr(f,_,T,I,u)}n=n.sibling}}function co(t,n){if(n.subtreeFlags&10256)for(n=n.child;n!==null;){var a=t,s=n,u=s.flags;switch(s.tag){case 22:co(a,s),u&2048&&sf(s.alternate,s);break;case 24:co(a,s),u&2048&&of(s.alternate,s);break;default:co(a,s)}n=n.sibling}}var fo=8192;function $r(t,n,a){if(t.subtreeFlags&fo)for(t=t.child;t!==null;)ig(t,n,a),t=t.sibling}function ig(t,n,a){switch(t.tag){case 26:$r(t,n,a),t.flags&fo&&t.memoizedState!==null&&sS(a,_i,t.memoizedState,t.memoizedProps);break;case 5:$r(t,n,a);break;case 3:case 4:var s=_i;_i=ql(t.stateNode.containerInfo),$r(t,n,a),_i=s;break;case 22:t.memoizedState===null&&(s=t.alternate,s!==null&&s.memoizedState!==null?(s=fo,fo=16777216,$r(t,n,a),fo=s):$r(t,n,a));break;default:$r(t,n,a)}}function ag(t){var n=t.alternate;if(n!==null&&(t=n.child,t!==null)){n.child=null;do n=t.sibling,t.sibling=null,t=n;while(t!==null)}}function ho(t){var n=t.deletions;if((t.flags&16)!==0){if(n!==null)for(var a=0;a<n.length;a++){var s=n[a];pn=s,sg(s,t)}ag(t)}if(t.subtreeFlags&10256)for(t=t.child;t!==null;)rg(t),t=t.sibling}function rg(t){switch(t.tag){case 0:case 11:case 15:ho(t),t.flags&2048&&wa(9,t,t.return);break;case 3:ho(t);break;case 12:ho(t);break;case 22:var n=t.stateNode;t.memoizedState!==null&&n._visibility&2&&(t.return===null||t.return.tag!==13)?(n._visibility&=-3,Nl(t)):ho(t);break;default:ho(t)}}function Nl(t){var n=t.deletions;if((t.flags&16)!==0){if(n!==null)for(var a=0;a<n.length;a++){var s=n[a];pn=s,sg(s,t)}ag(t)}for(t=t.child;t!==null;){switch(n=t,n.tag){case 0:case 11:case 15:wa(8,n,n.return),Nl(n);break;case 22:a=n.stateNode,a._visibility&2&&(a._visibility&=-3,Nl(n));break;default:Nl(n)}t=t.sibling}}function sg(t,n){for(;pn!==null;){var a=pn;switch(a.tag){case 0:case 11:case 15:wa(8,a,n);break;case 23:case 22:if(a.memoizedState!==null&&a.memoizedState.cachePool!==null){var s=a.memoizedState.cachePool.pool;s!=null&&s.refCount++}break;case 24:js(a.memoizedState.cache)}if(s=a.child,s!==null)s.return=a,pn=s;else t:for(a=t;pn!==null;){s=pn;var u=s.sibling,f=s.return;if(Km(s),s===a){pn=null;break t}if(u!==null){u.return=f,pn=u;break t}pn=f}}}var Mx={getCacheForType:function(t){var n=En(rn),a=n.data.get(t);return a===void 0&&(a=t(),n.data.set(t,a)),a},cacheSignal:function(){return En(rn).controller.signal}},yx=typeof WeakMap=="function"?WeakMap:Map,De=0,Ve=null,de=null,ge=0,Fe=0,Zn=null,Ua=!1,ts=!1,lf=!1,na=0,Je=0,La=0,mr=0,uf=0,jn=0,es=0,po=null,Hn=null,cf=!1,Ol=0,og=0,Pl=1/0,Fl=null,Na=null,fn=0,Oa=null,ns=null,ia=0,ff=0,hf=null,lg=null,mo=0,df=null;function Kn(){return(De&2)!==0&&ge!==0?ge&-ge:O.T!==null?xf():Ps()}function ug(){if(jn===0)if((ge&536870912)===0||ve){var t=Tt;Tt<<=1,(Tt&3932160)===0&&(Tt=262144),jn=t}else jn=536870912;return t=qn.current,t!==null&&(t.flags|=32),jn}function Gn(t,n,a){(t===Ve&&(Fe===2||Fe===9)||t.cancelPendingCommit!==null)&&(is(t,0),Pa(t,ge,jn,!1)),Rn(t,a),((De&2)===0||t!==Ve)&&(t===Ve&&((De&2)===0&&(mr|=a),Je===4&&Pa(t,ge,jn,!1)),Di(t))}function cg(t,n,a){if((De&6)!==0)throw Error(r(327));var s=!a&&(n&127)===0&&(n&t.expiredLanes)===0||At(t,n),u=s?bx(t,n):mf(t,n,!0),f=s;do{if(u===0){ts&&!s&&Pa(t,n,0,!1);break}else{if(a=t.current.alternate,f&&!Ex(a)){u=mf(t,n,!1),f=!1;continue}if(u===2){if(f=n,t.errorRecoveryDisabledLanes&f)var _=0;else _=t.pendingLanes&-536870913,_=_!==0?_:_&536870912?536870912:0;if(_!==0){n=_;t:{var T=t;u=po;var I=T.current.memoizedState.isDehydrated;if(I&&(is(T,_).flags|=256),_=mf(T,_,!1),_!==2){if(lf&&!I){T.errorRecoveryDisabledLanes|=f,mr|=f,u=4;break t}f=Hn,Hn=u,f!==null&&(Hn===null?Hn=f:Hn.push.apply(Hn,f))}u=_}if(f=!1,u!==2)continue}}if(u===1){is(t,0),Pa(t,n,0,!0);break}t:{switch(s=t,f=u,f){case 0:case 1:throw Error(r(345));case 4:if((n&4194048)!==n)break;case 6:Pa(s,n,jn,!Ua);break t;case 2:Hn=null;break;case 3:case 5:break;default:throw Error(r(329))}if((n&62914560)===n&&(u=Ol+300-E(),10<u)){if(Pa(s,n,jn,!Ua),_t(s,0,!0)!==0)break t;ia=n,s.timeoutHandle=Gg(fg.bind(null,s,a,Hn,Fl,cf,n,jn,mr,es,Ua,f,"Throttled",-0,0),u);break t}fg(s,a,Hn,Fl,cf,n,jn,mr,es,Ua,f,null,-0,0)}}break}while(!0);Di(t)}function fg(t,n,a,s,u,f,_,T,I,K,ft,mt,$,ot){if(t.timeoutHandle=-1,mt=n.subtreeFlags,mt&8192||(mt&16785408)===16785408){mt={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:Vi},ig(n,f,mt);var Gt=(f&62914560)===f?Ol-E():(f&4194048)===f?og-E():0;if(Gt=oS(mt,Gt),Gt!==null){ia=f,t.cancelPendingCommit=Gt(xg.bind(null,t,n,f,a,s,u,_,T,I,ft,mt,null,$,ot)),Pa(t,f,_,!K);return}}xg(t,n,f,a,s,u,_,T,I)}function Ex(t){for(var n=t;;){var a=n.tag;if((a===0||a===11||a===15)&&n.flags&16384&&(a=n.updateQueue,a!==null&&(a=a.stores,a!==null)))for(var s=0;s<a.length;s++){var u=a[s],f=u.getSnapshot;u=u.value;try{if(!kn(f(),u))return!1}catch{return!1}}if(a=n.child,n.subtreeFlags&16384&&a!==null)a.return=n,n=a;else{if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return!0;n=n.return}n.sibling.return=n.return,n=n.sibling}}return!0}function Pa(t,n,a,s){n&=~uf,n&=~mr,t.suspendedLanes|=n,t.pingedLanes&=~n,s&&(t.warmLanes|=n),s=t.expirationTimes;for(var u=n;0<u;){var f=31-Ot(u),_=1<<f;s[f]=-1,u&=~_}a!==0&&Zo(t,a,n)}function zl(){return(De&6)===0?(go(0),!1):!0}function pf(){if(de!==null){if(Fe===0)var t=de.return;else t=de,qi=sr=null,Dc(t),Yr=null,Qs=0,t=de;for(;t!==null;)Vm(t.alternate,t),t=t.return;de=null}}function is(t,n){var a=t.timeoutHandle;a!==-1&&(t.timeoutHandle=-1,Xx(a)),a=t.cancelPendingCommit,a!==null&&(t.cancelPendingCommit=null,a()),ia=0,pf(),Ve=t,de=a=ki(t.current,null),ge=n,Fe=0,Zn=null,Ua=!1,ts=At(t,n),lf=!1,es=jn=uf=mr=La=Je=0,Hn=po=null,cf=!1,(n&8)!==0&&(n|=n&32);var s=t.entangledLanes;if(s!==0)for(t=t.entanglements,s&=n;0<s;){var u=31-Ot(s),f=1<<u;n|=t[u],s&=~f}return na=n,al(),a}function hg(t,n){se=null,O.H=ro,n===qr||n===hl?(n=Cp(),Fe=3):n===_c?(n=Cp(),Fe=4):Fe=n===Wc?8:n!==null&&typeof n=="object"&&typeof n.then=="function"?6:1,Zn=n,de===null&&(Je=1,Al(t,ii(n,t.current)))}function dg(){var t=qn.current;return t===null?!0:(ge&4194048)===ge?oi===null:(ge&62914560)===ge||(ge&536870912)!==0?t===oi:!1}function pg(){var t=O.H;return O.H=ro,t===null?ro:t}function mg(){var t=O.A;return O.A=Mx,t}function Bl(){Je=4,Ua||(ge&4194048)!==ge&&qn.current!==null||(ts=!0),(La&134217727)===0&&(mr&134217727)===0||Ve===null||Pa(Ve,ge,jn,!1)}function mf(t,n,a){var s=De;De|=2;var u=pg(),f=mg();(Ve!==t||ge!==n)&&(Fl=null,is(t,n)),n=!1;var _=Je;t:do try{if(Fe!==0&&de!==null){var T=de,I=Zn;switch(Fe){case 8:pf(),_=6;break t;case 3:case 2:case 9:case 6:qn.current===null&&(n=!0);var K=Fe;if(Fe=0,Zn=null,as(t,T,I,K),a&&ts){_=0;break t}break;default:K=Fe,Fe=0,Zn=null,as(t,T,I,K)}}Tx(),_=Je;break}catch(ft){hg(t,ft)}while(!0);return n&&t.shellSuspendCounter++,qi=sr=null,De=s,O.H=u,O.A=f,de===null&&(Ve=null,ge=0,al()),_}function Tx(){for(;de!==null;)gg(de)}function bx(t,n){var a=De;De|=2;var s=pg(),u=mg();Ve!==t||ge!==n?(Fl=null,Pl=E()+500,is(t,n)):ts=At(t,n);t:do try{if(Fe!==0&&de!==null){n=de;var f=Zn;e:switch(Fe){case 1:Fe=0,Zn=null,as(t,n,f,1);break;case 2:case 9:if(Ap(f)){Fe=0,Zn=null,_g(n);break}n=function(){Fe!==2&&Fe!==9||Ve!==t||(Fe=7),Di(t)},f.then(n,n);break t;case 3:Fe=7;break t;case 4:Fe=5;break t;case 7:Ap(f)?(Fe=0,Zn=null,_g(n)):(Fe=0,Zn=null,as(t,n,f,7));break;case 5:var _=null;switch(de.tag){case 26:_=de.memoizedState;case 5:case 27:var T=de;if(_?n0(_):T.stateNode.complete){Fe=0,Zn=null;var I=T.sibling;if(I!==null)de=I;else{var K=T.return;K!==null?(de=K,Il(K)):de=null}break e}}Fe=0,Zn=null,as(t,n,f,5);break;case 6:Fe=0,Zn=null,as(t,n,f,6);break;case 8:pf(),Je=6;break t;default:throw Error(r(462))}}Ax();break}catch(ft){hg(t,ft)}while(!0);return qi=sr=null,O.H=s,O.A=u,De=a,de!==null?0:(Ve=null,ge=0,al(),Je)}function Ax(){for(;de!==null&&!qt();)gg(de)}function gg(t){var n=Hm(t.alternate,t,na);t.memoizedProps=t.pendingProps,n===null?Il(t):de=n}function _g(t){var n=t,a=n.alternate;switch(n.tag){case 15:case 0:n=Om(a,n,n.pendingProps,n.type,void 0,ge);break;case 11:n=Om(a,n,n.pendingProps,n.type.render,n.ref,ge);break;case 5:Dc(n);default:Vm(a,n),n=de=mp(n,na),n=Hm(a,n,na)}t.memoizedProps=t.pendingProps,n===null?Il(t):de=n}function as(t,n,a,s){qi=sr=null,Dc(n),Yr=null,Qs=0;var u=n.return;try{if(px(t,u,n,a,ge)){Je=1,Al(t,ii(a,t.current)),de=null;return}}catch(f){if(u!==null)throw de=u,f;Je=1,Al(t,ii(a,t.current)),de=null;return}n.flags&32768?(ve||s===1?t=!0:ts||(ge&536870912)!==0?t=!1:(Ua=t=!0,(s===2||s===9||s===3||s===6)&&(s=qn.current,s!==null&&s.tag===13&&(s.flags|=16384))),vg(n,t)):Il(n)}function Il(t){var n=t;do{if((n.flags&32768)!==0){vg(n,Ua);return}t=n.return;var a=_x(n.alternate,n,na);if(a!==null){de=a;return}if(n=n.sibling,n!==null){de=n;return}de=n=t}while(n!==null);Je===0&&(Je=5)}function vg(t,n){do{var a=vx(t.alternate,t);if(a!==null){a.flags&=32767,de=a;return}if(a=t.return,a!==null&&(a.flags|=32768,a.subtreeFlags=0,a.deletions=null),!n&&(t=t.sibling,t!==null)){de=t;return}de=t=a}while(t!==null);Je=6,de=null}function xg(t,n,a,s,u,f,_,T,I){t.cancelPendingCommit=null;do Hl();while(fn!==0);if((De&6)!==0)throw Error(r(327));if(n!==null){if(n===t.current)throw Error(r(177));if(f=n.lanes|n.childLanes,f|=nc,di(t,a,f,_,T,I),t===Ve&&(de=Ve=null,ge=0),ns=n,Oa=t,ia=a,ff=f,hf=u,lg=s,(n.subtreeFlags&10256)!==0||(n.flags&10256)!==0?(t.callbackNode=null,t.callbackPriority=0,wx(lt,function(){return Tg(),null})):(t.callbackNode=null,t.callbackPriority=0),s=(n.flags&13878)!==0,(n.subtreeFlags&13878)!==0||s){s=O.T,O.T=null,u=V.p,V.p=2,_=De,De|=4;try{xx(t,n,a)}finally{De=_,V.p=u,O.T=s}}fn=1,Sg(),Mg(),yg()}}function Sg(){if(fn===1){fn=0;var t=Oa,n=ns,a=(n.flags&13878)!==0;if((n.subtreeFlags&13878)!==0||a){a=O.T,O.T=null;var s=V.p;V.p=2;var u=De;De|=4;try{tg(n,t);var f=Rf,_=sp(t.containerInfo),T=f.focusedElem,I=f.selectionRange;if(_!==T&&T&&T.ownerDocument&&rp(T.ownerDocument.documentElement,T)){if(I!==null&&Qu(T)){var K=I.start,ft=I.end;if(ft===void 0&&(ft=K),"selectionStart"in T)T.selectionStart=K,T.selectionEnd=Math.min(ft,T.value.length);else{var mt=T.ownerDocument||document,$=mt&&mt.defaultView||window;if($.getSelection){var ot=$.getSelection(),Gt=T.textContent.length,$t=Math.min(I.start,Gt),Ge=I.end===void 0?$t:Math.min(I.end,Gt);!ot.extend&&$t>Ge&&(_=Ge,Ge=$t,$t=_);var Y=ap(T,$t),G=ap(T,Ge);if(Y&&G&&(ot.rangeCount!==1||ot.anchorNode!==Y.node||ot.anchorOffset!==Y.offset||ot.focusNode!==G.node||ot.focusOffset!==G.offset)){var j=mt.createRange();j.setStart(Y.node,Y.offset),ot.removeAllRanges(),$t>Ge?(ot.addRange(j),ot.extend(G.node,G.offset)):(j.setEnd(G.node,G.offset),ot.addRange(j))}}}}for(mt=[],ot=T;ot=ot.parentNode;)ot.nodeType===1&&mt.push({element:ot,left:ot.scrollLeft,top:ot.scrollTop});for(typeof T.focus=="function"&&T.focus(),T=0;T<mt.length;T++){var pt=mt[T];pt.element.scrollLeft=pt.left,pt.element.scrollTop=pt.top}}Jl=!!Af,Rf=Af=null}finally{De=u,V.p=s,O.T=a}}t.current=n,fn=2}}function Mg(){if(fn===2){fn=0;var t=Oa,n=ns,a=(n.flags&8772)!==0;if((n.subtreeFlags&8772)!==0||a){a=O.T,O.T=null;var s=V.p;V.p=2;var u=De;De|=4;try{jm(t,n.alternate,n)}finally{De=u,V.p=s,O.T=a}}fn=3}}function yg(){if(fn===4||fn===3){fn=0,w();var t=Oa,n=ns,a=ia,s=lg;(n.subtreeFlags&10256)!==0||(n.flags&10256)!==0?fn=5:(fn=0,ns=Oa=null,Eg(t,t.pendingLanes));var u=t.pendingLanes;if(u===0&&(Na=null),Dr(a),n=n.stateNode,Et&&typeof Et.onCommitFiberRoot=="function")try{Et.onCommitFiberRoot(yt,n,void 0,(n.current.flags&128)===128)}catch{}if(s!==null){n=O.T,u=V.p,V.p=2,O.T=null;try{for(var f=t.onRecoverableError,_=0;_<s.length;_++){var T=s[_];f(T.value,{componentStack:T.stack})}}finally{O.T=n,V.p=u}}(ia&3)!==0&&Hl(),Di(t),u=t.pendingLanes,(a&261930)!==0&&(u&42)!==0?t===df?mo++:(mo=0,df=t):mo=0,go(0)}}function Eg(t,n){(t.pooledCacheLanes&=n)===0&&(n=t.pooledCache,n!=null&&(t.pooledCache=null,js(n)))}function Hl(){return Sg(),Mg(),yg(),Tg()}function Tg(){if(fn!==5)return!1;var t=Oa,n=ff;ff=0;var a=Dr(ia),s=O.T,u=V.p;try{V.p=32>a?32:a,O.T=null,a=hf,hf=null;var f=Oa,_=ia;if(fn=0,ns=Oa=null,ia=0,(De&6)!==0)throw Error(r(331));var T=De;if(De|=4,rg(f.current),ng(f,f.current,_,a),De=T,go(0,!1),Et&&typeof Et.onPostCommitFiberRoot=="function")try{Et.onPostCommitFiberRoot(yt,f)}catch{}return!0}finally{V.p=u,O.T=s,Eg(t,n)}}function bg(t,n,a){n=ii(a,n),n=kc(t.stateNode,n,2),t=Ra(t,n,2),t!==null&&(Rn(t,2),Di(t))}function ze(t,n,a){if(t.tag===3)bg(t,t,a);else for(;n!==null;){if(n.tag===3){bg(n,t,a);break}else if(n.tag===1){var s=n.stateNode;if(typeof n.type.getDerivedStateFromError=="function"||typeof s.componentDidCatch=="function"&&(Na===null||!Na.has(s))){t=ii(a,t),a=Am(2),s=Ra(n,a,2),s!==null&&(Rm(a,s,n,t),Rn(s,2),Di(s));break}}n=n.return}}function gf(t,n,a){var s=t.pingCache;if(s===null){s=t.pingCache=new yx;var u=new Set;s.set(n,u)}else u=s.get(n),u===void 0&&(u=new Set,s.set(n,u));u.has(a)||(lf=!0,u.add(a),t=Rx.bind(null,t,n,a),n.then(t,t))}function Rx(t,n,a){var s=t.pingCache;s!==null&&s.delete(n),t.pingedLanes|=t.suspendedLanes&a,t.warmLanes&=~a,Ve===t&&(ge&a)===a&&(Je===4||Je===3&&(ge&62914560)===ge&&300>E()-Ol?(De&2)===0&&is(t,0):uf|=a,es===ge&&(es=0)),Di(t)}function Ag(t,n){n===0&&(n=Oe()),t=ir(t,n),t!==null&&(Rn(t,n),Di(t))}function Cx(t){var n=t.memoizedState,a=0;n!==null&&(a=n.retryLane),Ag(t,a)}function Dx(t,n){var a=0;switch(t.tag){case 31:case 13:var s=t.stateNode,u=t.memoizedState;u!==null&&(a=u.retryLane);break;case 19:s=t.stateNode;break;case 22:s=t.stateNode._retryCache;break;default:throw Error(r(314))}s!==null&&s.delete(n),Ag(t,a)}function wx(t,n){return Se(t,n)}var Gl=null,rs=null,_f=!1,Vl=!1,vf=!1,Fa=0;function Di(t){t!==rs&&t.next===null&&(rs===null?Gl=rs=t:rs=rs.next=t),Vl=!0,_f||(_f=!0,Lx())}function go(t,n){if(!vf&&Vl){vf=!0;do for(var a=!1,s=Gl;s!==null;){if(t!==0){var u=s.pendingLanes;if(u===0)var f=0;else{var _=s.suspendedLanes,T=s.pingedLanes;f=(1<<31-Ot(42|t)+1)-1,f&=u&~(_&~T),f=f&201326741?f&201326741|1:f?f|2:0}f!==0&&(a=!0,wg(s,f))}else f=ge,f=_t(s,s===Ve?f:0,s.cancelPendingCommit!==null||s.timeoutHandle!==-1),(f&3)===0||At(s,f)||(a=!0,wg(s,f));s=s.next}while(a);vf=!1}}function Ux(){Rg()}function Rg(){Vl=_f=!1;var t=0;Fa!==0&&Vx()&&(t=Fa);for(var n=E(),a=null,s=Gl;s!==null;){var u=s.next,f=Cg(s,n);f===0?(s.next=null,a===null?Gl=u:a.next=u,u===null&&(rs=a)):(a=s,(t!==0||(f&3)!==0)&&(Vl=!0)),s=u}fn!==0&&fn!==5||go(t),Fa!==0&&(Fa=0)}function Cg(t,n){for(var a=t.suspendedLanes,s=t.pingedLanes,u=t.expirationTimes,f=t.pendingLanes&-62914561;0<f;){var _=31-Ot(f),T=1<<_,I=u[_];I===-1?((T&a)===0||(T&s)!==0)&&(u[_]=ee(T,n)):I<=n&&(t.expiredLanes|=T),f&=~T}if(n=Ve,a=ge,a=_t(t,t===n?a:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),s=t.callbackNode,a===0||t===n&&(Fe===2||Fe===9)||t.cancelPendingCommit!==null)return s!==null&&s!==null&&Le(s),t.callbackNode=null,t.callbackPriority=0;if((a&3)===0||At(t,a)){if(n=a&-a,n===t.callbackPriority)return n;switch(s!==null&&Le(s),Dr(a)){case 2:case 8:a=vt;break;case 32:a=lt;break;case 268435456:a=Rt;break;default:a=lt}return s=Dg.bind(null,t),a=Se(a,s),t.callbackPriority=n,t.callbackNode=a,n}return s!==null&&s!==null&&Le(s),t.callbackPriority=2,t.callbackNode=null,2}function Dg(t,n){if(fn!==0&&fn!==5)return t.callbackNode=null,t.callbackPriority=0,null;var a=t.callbackNode;if(Hl()&&t.callbackNode!==a)return null;var s=ge;return s=_t(t,t===Ve?s:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),s===0?null:(cg(t,s,n),Cg(t,E()),t.callbackNode!=null&&t.callbackNode===a?Dg.bind(null,t):null)}function wg(t,n){if(Hl())return null;cg(t,n,!0)}function Lx(){kx(function(){(De&6)!==0?Se(dt,Ux):Rg()})}function xf(){if(Fa===0){var t=kr;t===0&&(t=Ut,Ut<<=1,(Ut&261888)===0&&(Ut=256)),Fa=t}return Fa}function Ug(t){return t==null||typeof t=="symbol"||typeof t=="boolean"?null:typeof t=="function"?t:Ko(""+t)}function Lg(t,n){var a=n.ownerDocument.createElement("input");return a.name=n.name,a.value=n.value,t.id&&a.setAttribute("form",t.id),n.parentNode.insertBefore(a,n),t=new FormData(t),a.parentNode.removeChild(a),t}function Nx(t,n,a,s,u){if(n==="submit"&&a&&a.stateNode===u){var f=Ug((u[gn]||null).action),_=s.submitter;_&&(n=(n=_[gn]||null)?Ug(n.formAction):_.getAttribute("formAction"),n!==null&&(f=n,_=null));var T=new tl("action","action",null,s,u);t.push({event:T,listeners:[{instance:null,listener:function(){if(s.defaultPrevented){if(Fa!==0){var I=_?Lg(u,_):new FormData(u);Bc(a,{pending:!0,data:I,method:u.method,action:f},null,I)}}else typeof f=="function"&&(T.preventDefault(),I=_?Lg(u,_):new FormData(u),Bc(a,{pending:!0,data:I,method:u.method,action:f},f,I))},currentTarget:u}]})}}for(var Sf=0;Sf<ec.length;Sf++){var Mf=ec[Sf],Ox=Mf.toLowerCase(),Px=Mf[0].toUpperCase()+Mf.slice(1);gi(Ox,"on"+Px)}gi(up,"onAnimationEnd"),gi(cp,"onAnimationIteration"),gi(fp,"onAnimationStart"),gi("dblclick","onDoubleClick"),gi("focusin","onFocus"),gi("focusout","onBlur"),gi(Qv,"onTransitionRun"),gi(Jv,"onTransitionStart"),gi($v,"onTransitionCancel"),gi(hp,"onTransitionEnd"),Z("onMouseEnter",["mouseout","mouseover"]),Z("onMouseLeave",["mouseout","mouseover"]),Z("onPointerEnter",["pointerout","pointerover"]),Z("onPointerLeave",["pointerout","pointerover"]),J("onChange","change click focusin focusout input keydown keyup selectionchange".split(" ")),J("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")),J("onBeforeInput",["compositionend","keypress","textInput","paste"]),J("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" ")),J("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" ")),J("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var _o="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),Fx=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(_o));function Ng(t,n){n=(n&4)!==0;for(var a=0;a<t.length;a++){var s=t[a],u=s.event;s=s.listeners;t:{var f=void 0;if(n)for(var _=s.length-1;0<=_;_--){var T=s[_],I=T.instance,K=T.currentTarget;if(T=T.listener,I!==f&&u.isPropagationStopped())break t;f=T,u.currentTarget=K;try{f(u)}catch(ft){il(ft)}u.currentTarget=null,f=I}else for(_=0;_<s.length;_++){if(T=s[_],I=T.instance,K=T.currentTarget,T=T.listener,I!==f&&u.isPropagationStopped())break t;f=T,u.currentTarget=K;try{f(u)}catch(ft){il(ft)}u.currentTarget=null,f=I}}}}function pe(t,n){var a=n[wr];a===void 0&&(a=n[wr]=new Set);var s=t+"__bubble";a.has(s)||(Og(n,t,2,!1),a.add(s))}function yf(t,n,a){var s=0;n&&(s|=4),Og(a,t,s,n)}var Xl="_reactListening"+Math.random().toString(36).slice(2);function Ef(t){if(!t[Xl]){t[Xl]=!0,q.forEach(function(a){a!=="selectionchange"&&(Fx.has(a)||yf(a,!1,t),yf(a,!0,t))});var n=t.nodeType===9?t:t.ownerDocument;n===null||n[Xl]||(n[Xl]=!0,yf("selectionchange",!1,n))}}function Og(t,n,a,s){switch(u0(n)){case 2:var u=cS;break;case 8:u=fS;break;default:u=Bf}a=u.bind(null,n,a,t),u=void 0,!Vu||n!=="touchstart"&&n!=="touchmove"&&n!=="wheel"||(u=!0),s?u!==void 0?t.addEventListener(n,a,{capture:!0,passive:u}):t.addEventListener(n,a,!0):u!==void 0?t.addEventListener(n,a,{passive:u}):t.addEventListener(n,a,!1)}function Tf(t,n,a,s,u){var f=s;if((n&1)===0&&(n&2)===0&&s!==null)t:for(;;){if(s===null)return;var _=s.tag;if(_===3||_===4){var T=s.stateNode.containerInfo;if(T===u)break;if(_===4)for(_=s.return;_!==null;){var I=_.tag;if((I===3||I===4)&&_.stateNode.containerInfo===u)return;_=_.return}for(;T!==null;){if(_=_a(T),_===null)return;if(I=_.tag,I===5||I===6||I===26||I===27){s=f=_;continue t}T=T.parentNode}}s=s.return}Id(function(){var K=f,ft=Hu(a),mt=[];t:{var $=dp.get(t);if($!==void 0){var ot=tl,Gt=t;switch(t){case"keypress":if(Jo(a)===0)break t;case"keydown":case"keyup":ot=Dv;break;case"focusin":Gt="focus",ot=qu;break;case"focusout":Gt="blur",ot=qu;break;case"beforeblur":case"afterblur":ot=qu;break;case"click":if(a.button===2)break t;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":ot=Vd;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":ot=_v;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":ot=Lv;break;case up:case cp:case fp:ot=Sv;break;case hp:ot=Ov;break;case"scroll":case"scrollend":ot=mv;break;case"wheel":ot=Fv;break;case"copy":case"cut":case"paste":ot=yv;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":ot=kd;break;case"toggle":case"beforetoggle":ot=Bv}var $t=(n&4)!==0,Ge=!$t&&(t==="scroll"||t==="scrollend"),Y=$t?$!==null?$+"Capture":null:$;$t=[];for(var G=K,j;G!==null;){var pt=G;if(j=pt.stateNode,pt=pt.tag,pt!==5&&pt!==26&&pt!==27||j===null||Y===null||(pt=Bs(G,Y),pt!=null&&$t.push(vo(G,pt,j))),Ge)break;G=G.return}0<$t.length&&($=new ot($,Gt,null,a,ft),mt.push({event:$,listeners:$t}))}}if((n&7)===0){t:{if($=t==="mouseover"||t==="pointerover",ot=t==="mouseout"||t==="pointerout",$&&a!==Iu&&(Gt=a.relatedTarget||a.fromElement)&&(_a(Gt)||Gt[pi]))break t;if((ot||$)&&($=ft.window===ft?ft:($=ft.ownerDocument)?$.defaultView||$.parentWindow:window,ot?(Gt=a.relatedTarget||a.toElement,ot=K,Gt=Gt?_a(Gt):null,Gt!==null&&(Ge=c(Gt),$t=Gt.tag,Gt!==Ge||$t!==5&&$t!==27&&$t!==6)&&(Gt=null)):(ot=null,Gt=K),ot!==Gt)){if($t=Vd,pt="onMouseLeave",Y="onMouseEnter",G="mouse",(t==="pointerout"||t==="pointerover")&&($t=kd,pt="onPointerLeave",Y="onPointerEnter",G="pointer"),Ge=ot==null?$:$a(ot),j=Gt==null?$:$a(Gt),$=new $t(pt,G+"leave",ot,a,ft),$.target=Ge,$.relatedTarget=j,pt=null,_a(ft)===K&&($t=new $t(Y,G+"enter",Gt,a,ft),$t.target=j,$t.relatedTarget=Ge,pt=$t),Ge=pt,ot&&Gt)e:{for($t=zx,Y=ot,G=Gt,j=0,pt=Y;pt;pt=$t(pt))j++;pt=0;for(var Kt=G;Kt;Kt=$t(Kt))pt++;for(;0<j-pt;)Y=$t(Y),j--;for(;0<pt-j;)G=$t(G),pt--;for(;j--;){if(Y===G||G!==null&&Y===G.alternate){$t=Y;break e}Y=$t(Y),G=$t(G)}$t=null}else $t=null;ot!==null&&Pg(mt,$,ot,$t,!1),Gt!==null&&Ge!==null&&Pg(mt,Ge,Gt,$t,!0)}}t:{if($=K?$a(K):window,ot=$.nodeName&&$.nodeName.toLowerCase(),ot==="select"||ot==="input"&&$.type==="file")var Ee=Jd;else if(Kd($))if($d)Ee=Zv;else{Ee=qv;var Yt=Wv}else ot=$.nodeName,!ot||ot.toLowerCase()!=="input"||$.type!=="checkbox"&&$.type!=="radio"?K&&mi(K.elementType)&&(Ee=Jd):Ee=Yv;if(Ee&&(Ee=Ee(t,K))){Qd(mt,Ee,a,ft);break t}Yt&&Yt(t,$,K),t==="focusout"&&K&&$.type==="number"&&K.memoizedProps.value!=null&&vn($,"number",$.value)}switch(Yt=K?$a(K):window,t){case"focusin":(Kd(Yt)||Yt.contentEditable==="true")&&(Fr=Yt,Ju=K,qs=null);break;case"focusout":qs=Ju=Fr=null;break;case"mousedown":$u=!0;break;case"contextmenu":case"mouseup":case"dragend":$u=!1,op(mt,a,ft);break;case"selectionchange":if(Kv)break;case"keydown":case"keyup":op(mt,a,ft)}var le;if(Zu)t:{switch(t){case"compositionstart":var _e="onCompositionStart";break t;case"compositionend":_e="onCompositionEnd";break t;case"compositionupdate":_e="onCompositionUpdate";break t}_e=void 0}else Pr?Zd(t,a)&&(_e="onCompositionEnd"):t==="keydown"&&a.keyCode===229&&(_e="onCompositionStart");_e&&(Wd&&a.locale!=="ko"&&(Pr||_e!=="onCompositionStart"?_e==="onCompositionEnd"&&Pr&&(le=Hd()):(Sa=ft,Xu="value"in Sa?Sa.value:Sa.textContent,Pr=!0)),Yt=kl(K,_e),0<Yt.length&&(_e=new Xd(_e,t,null,a,ft),mt.push({event:_e,listeners:Yt}),le?_e.data=le:(le=jd(a),le!==null&&(_e.data=le)))),(le=Hv?Gv(t,a):Vv(t,a))&&(_e=kl(K,"onBeforeInput"),0<_e.length&&(Yt=new Xd("onBeforeInput","beforeinput",null,a,ft),mt.push({event:Yt,listeners:_e}),Yt.data=le)),Nx(mt,t,K,a,ft)}Ng(mt,n)})}function vo(t,n,a){return{instance:t,listener:n,currentTarget:a}}function kl(t,n){for(var a=n+"Capture",s=[];t!==null;){var u=t,f=u.stateNode;if(u=u.tag,u!==5&&u!==26&&u!==27||f===null||(u=Bs(t,a),u!=null&&s.unshift(vo(t,u,f)),u=Bs(t,n),u!=null&&s.push(vo(t,u,f))),t.tag===3)return s;t=t.return}return[]}function zx(t){if(t===null)return null;do t=t.return;while(t&&t.tag!==5&&t.tag!==27);return t||null}function Pg(t,n,a,s,u){for(var f=n._reactName,_=[];a!==null&&a!==s;){var T=a,I=T.alternate,K=T.stateNode;if(T=T.tag,I!==null&&I===s)break;T!==5&&T!==26&&T!==27||K===null||(I=K,u?(K=Bs(a,f),K!=null&&_.unshift(vo(a,K,I))):u||(K=Bs(a,f),K!=null&&_.push(vo(a,K,I)))),a=a.return}_.length!==0&&t.push({event:n,listeners:_})}var Bx=/\r\n?/g,Ix=/\u0000|\uFFFD/g;function Fg(t){return(typeof t=="string"?t:""+t).replace(Bx,`
`).replace(Ix,"")}function zg(t,n){return n=Fg(n),Fg(t)===n}function He(t,n,a,s,u,f){switch(a){case"children":typeof s=="string"?n==="body"||n==="textarea"&&s===""||cn(t,s):(typeof s=="number"||typeof s=="bigint")&&n!=="body"&&cn(t,""+s);break;case"className":Qt(t,"class",s);break;case"tabIndex":Qt(t,"tabindex",s);break;case"dir":case"role":case"viewBox":case"width":case"height":Qt(t,a,s);break;case"style":Lr(t,s,f);break;case"data":if(n!=="object"){Qt(t,"data",s);break}case"src":case"href":if(s===""&&(n!=="a"||a!=="href")){t.removeAttribute(a);break}if(s==null||typeof s=="function"||typeof s=="symbol"||typeof s=="boolean"){t.removeAttribute(a);break}s=Ko(""+s),t.setAttribute(a,s);break;case"action":case"formAction":if(typeof s=="function"){t.setAttribute(a,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}else typeof f=="function"&&(a==="formAction"?(n!=="input"&&He(t,n,"name",u.name,u,null),He(t,n,"formEncType",u.formEncType,u,null),He(t,n,"formMethod",u.formMethod,u,null),He(t,n,"formTarget",u.formTarget,u,null)):(He(t,n,"encType",u.encType,u,null),He(t,n,"method",u.method,u,null),He(t,n,"target",u.target,u,null)));if(s==null||typeof s=="symbol"||typeof s=="boolean"){t.removeAttribute(a);break}s=Ko(""+s),t.setAttribute(a,s);break;case"onClick":s!=null&&(t.onclick=Vi);break;case"onScroll":s!=null&&pe("scroll",t);break;case"onScrollEnd":s!=null&&pe("scrollend",t);break;case"dangerouslySetInnerHTML":if(s!=null){if(typeof s!="object"||!("__html"in s))throw Error(r(61));if(a=s.__html,a!=null){if(u.children!=null)throw Error(r(60));t.innerHTML=a}}break;case"multiple":t.multiple=s&&typeof s!="function"&&typeof s!="symbol";break;case"muted":t.muted=s&&typeof s!="function"&&typeof s!="symbol";break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":break;case"autoFocus":break;case"xlinkHref":if(s==null||typeof s=="function"||typeof s=="boolean"||typeof s=="symbol"){t.removeAttribute("xlink:href");break}a=Ko(""+s),t.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",a);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":s!=null&&typeof s!="function"&&typeof s!="symbol"?t.setAttribute(a,""+s):t.removeAttribute(a);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":s&&typeof s!="function"&&typeof s!="symbol"?t.setAttribute(a,""):t.removeAttribute(a);break;case"capture":case"download":s===!0?t.setAttribute(a,""):s!==!1&&s!=null&&typeof s!="function"&&typeof s!="symbol"?t.setAttribute(a,s):t.removeAttribute(a);break;case"cols":case"rows":case"size":case"span":s!=null&&typeof s!="function"&&typeof s!="symbol"&&!isNaN(s)&&1<=s?t.setAttribute(a,s):t.removeAttribute(a);break;case"rowSpan":case"start":s==null||typeof s=="function"||typeof s=="symbol"||isNaN(s)?t.removeAttribute(a):t.setAttribute(a,s);break;case"popover":pe("beforetoggle",t),pe("toggle",t),kt(t,"popover",s);break;case"xlinkActuate":Wt(t,"http://www.w3.org/1999/xlink","xlink:actuate",s);break;case"xlinkArcrole":Wt(t,"http://www.w3.org/1999/xlink","xlink:arcrole",s);break;case"xlinkRole":Wt(t,"http://www.w3.org/1999/xlink","xlink:role",s);break;case"xlinkShow":Wt(t,"http://www.w3.org/1999/xlink","xlink:show",s);break;case"xlinkTitle":Wt(t,"http://www.w3.org/1999/xlink","xlink:title",s);break;case"xlinkType":Wt(t,"http://www.w3.org/1999/xlink","xlink:type",s);break;case"xmlBase":Wt(t,"http://www.w3.org/XML/1998/namespace","xml:base",s);break;case"xmlLang":Wt(t,"http://www.w3.org/XML/1998/namespace","xml:lang",s);break;case"xmlSpace":Wt(t,"http://www.w3.org/XML/1998/namespace","xml:space",s);break;case"is":kt(t,"is",s);break;case"innerText":case"textContent":break;default:(!(2<a.length)||a[0]!=="o"&&a[0]!=="O"||a[1]!=="n"&&a[1]!=="N")&&(a=dv.get(a)||a,kt(t,a,s))}}function bf(t,n,a,s,u,f){switch(a){case"style":Lr(t,s,f);break;case"dangerouslySetInnerHTML":if(s!=null){if(typeof s!="object"||!("__html"in s))throw Error(r(61));if(a=s.__html,a!=null){if(u.children!=null)throw Error(r(60));t.innerHTML=a}}break;case"children":typeof s=="string"?cn(t,s):(typeof s=="number"||typeof s=="bigint")&&cn(t,""+s);break;case"onScroll":s!=null&&pe("scroll",t);break;case"onScrollEnd":s!=null&&pe("scrollend",t);break;case"onClick":s!=null&&(t.onclick=Vi);break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":break;case"innerText":case"textContent":break;default:if(!st.hasOwnProperty(a))t:{if(a[0]==="o"&&a[1]==="n"&&(u=a.endsWith("Capture"),n=a.slice(2,u?a.length-7:void 0),f=t[gn]||null,f=f!=null?f[a]:null,typeof f=="function"&&t.removeEventListener(n,f,u),typeof s=="function")){typeof f!="function"&&f!==null&&(a in t?t[a]=null:t.hasAttribute(a)&&t.removeAttribute(a)),t.addEventListener(n,s,u);break t}a in t?t[a]=s:s===!0?t.setAttribute(a,""):kt(t,a,s)}}}function bn(t,n,a){switch(n){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":pe("error",t),pe("load",t);var s=!1,u=!1,f;for(f in a)if(a.hasOwnProperty(f)){var _=a[f];if(_!=null)switch(f){case"src":s=!0;break;case"srcSet":u=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(r(137,n));default:He(t,n,f,_,a,null)}}u&&He(t,n,"srcSet",a.srcSet,a,null),s&&He(t,n,"src",a.src,a,null);return;case"input":pe("invalid",t);var T=f=_=u=null,I=null,K=null;for(s in a)if(a.hasOwnProperty(s)){var ft=a[s];if(ft!=null)switch(s){case"name":u=ft;break;case"type":_=ft;break;case"checked":I=ft;break;case"defaultChecked":K=ft;break;case"value":f=ft;break;case"defaultValue":T=ft;break;case"children":case"dangerouslySetInnerHTML":if(ft!=null)throw Error(r(137,n));break;default:He(t,n,s,ft,a,null)}}Gi(t,f,T,I,K,_,u,!1);return;case"select":pe("invalid",t),s=_=f=null;for(u in a)if(a.hasOwnProperty(u)&&(T=a[u],T!=null))switch(u){case"value":f=T;break;case"defaultValue":_=T;break;case"multiple":s=T;default:He(t,n,u,T,a,null)}n=f,a=_,t.multiple=!!s,n!=null?ei(t,!!s,n,!1):a!=null&&ei(t,!!s,a,!0);return;case"textarea":pe("invalid",t),f=u=s=null;for(_ in a)if(a.hasOwnProperty(_)&&(T=a[_],T!=null))switch(_){case"value":s=T;break;case"defaultValue":u=T;break;case"children":f=T;break;case"dangerouslySetInnerHTML":if(T!=null)throw Error(r(91));break;default:He(t,n,_,T,a,null)}xn(t,s,u,f);return;case"option":for(I in a)a.hasOwnProperty(I)&&(s=a[I],s!=null)&&(I==="selected"?t.selected=s&&typeof s!="function"&&typeof s!="symbol":He(t,n,I,s,a,null));return;case"dialog":pe("beforetoggle",t),pe("toggle",t),pe("cancel",t),pe("close",t);break;case"iframe":case"object":pe("load",t);break;case"video":case"audio":for(s=0;s<_o.length;s++)pe(_o[s],t);break;case"image":pe("error",t),pe("load",t);break;case"details":pe("toggle",t);break;case"embed":case"source":case"link":pe("error",t),pe("load",t);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(K in a)if(a.hasOwnProperty(K)&&(s=a[K],s!=null))switch(K){case"children":case"dangerouslySetInnerHTML":throw Error(r(137,n));default:He(t,n,K,s,a,null)}return;default:if(mi(n)){for(ft in a)a.hasOwnProperty(ft)&&(s=a[ft],s!==void 0&&bf(t,n,ft,s,a,void 0));return}}for(T in a)a.hasOwnProperty(T)&&(s=a[T],s!=null&&He(t,n,T,s,a,null))}function Hx(t,n,a,s){switch(n){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var u=null,f=null,_=null,T=null,I=null,K=null,ft=null;for(ot in a){var mt=a[ot];if(a.hasOwnProperty(ot)&&mt!=null)switch(ot){case"checked":break;case"value":break;case"defaultValue":I=mt;default:s.hasOwnProperty(ot)||He(t,n,ot,null,s,mt)}}for(var $ in s){var ot=s[$];if(mt=a[$],s.hasOwnProperty($)&&(ot!=null||mt!=null))switch($){case"type":f=ot;break;case"name":u=ot;break;case"checked":K=ot;break;case"defaultChecked":ft=ot;break;case"value":_=ot;break;case"defaultValue":T=ot;break;case"children":case"dangerouslySetInnerHTML":if(ot!=null)throw Error(r(137,n));break;default:ot!==mt&&He(t,n,$,ot,s,mt)}}_n(t,_,T,I,K,ft,f,u);return;case"select":ot=_=T=$=null;for(f in a)if(I=a[f],a.hasOwnProperty(f)&&I!=null)switch(f){case"value":break;case"multiple":ot=I;default:s.hasOwnProperty(f)||He(t,n,f,null,s,I)}for(u in s)if(f=s[u],I=a[u],s.hasOwnProperty(u)&&(f!=null||I!=null))switch(u){case"value":$=f;break;case"defaultValue":T=f;break;case"multiple":_=f;default:f!==I&&He(t,n,u,f,s,I)}n=T,a=_,s=ot,$!=null?ei(t,!!a,$,!1):!!s!=!!a&&(n!=null?ei(t,!!a,n,!0):ei(t,!!a,a?[]:"",!1));return;case"textarea":ot=$=null;for(T in a)if(u=a[T],a.hasOwnProperty(T)&&u!=null&&!s.hasOwnProperty(T))switch(T){case"value":break;case"children":break;default:He(t,n,T,null,s,u)}for(_ in s)if(u=s[_],f=a[_],s.hasOwnProperty(_)&&(u!=null||f!=null))switch(_){case"value":$=u;break;case"defaultValue":ot=u;break;case"children":break;case"dangerouslySetInnerHTML":if(u!=null)throw Error(r(91));break;default:u!==f&&He(t,n,_,u,s,f)}Pe(t,$,ot);return;case"option":for(var Gt in a)$=a[Gt],a.hasOwnProperty(Gt)&&$!=null&&!s.hasOwnProperty(Gt)&&(Gt==="selected"?t.selected=!1:He(t,n,Gt,null,s,$));for(I in s)$=s[I],ot=a[I],s.hasOwnProperty(I)&&$!==ot&&($!=null||ot!=null)&&(I==="selected"?t.selected=$&&typeof $!="function"&&typeof $!="symbol":He(t,n,I,$,s,ot));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var $t in a)$=a[$t],a.hasOwnProperty($t)&&$!=null&&!s.hasOwnProperty($t)&&He(t,n,$t,null,s,$);for(K in s)if($=s[K],ot=a[K],s.hasOwnProperty(K)&&$!==ot&&($!=null||ot!=null))switch(K){case"children":case"dangerouslySetInnerHTML":if($!=null)throw Error(r(137,n));break;default:He(t,n,K,$,s,ot)}return;default:if(mi(n)){for(var Ge in a)$=a[Ge],a.hasOwnProperty(Ge)&&$!==void 0&&!s.hasOwnProperty(Ge)&&bf(t,n,Ge,void 0,s,$);for(ft in s)$=s[ft],ot=a[ft],!s.hasOwnProperty(ft)||$===ot||$===void 0&&ot===void 0||bf(t,n,ft,$,s,ot);return}}for(var Y in a)$=a[Y],a.hasOwnProperty(Y)&&$!=null&&!s.hasOwnProperty(Y)&&He(t,n,Y,null,s,$);for(mt in s)$=s[mt],ot=a[mt],!s.hasOwnProperty(mt)||$===ot||$==null&&ot==null||He(t,n,mt,$,s,ot)}function Bg(t){switch(t){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}function Gx(){if(typeof performance.getEntriesByType=="function"){for(var t=0,n=0,a=performance.getEntriesByType("resource"),s=0;s<a.length;s++){var u=a[s],f=u.transferSize,_=u.initiatorType,T=u.duration;if(f&&T&&Bg(_)){for(_=0,T=u.responseEnd,s+=1;s<a.length;s++){var I=a[s],K=I.startTime;if(K>T)break;var ft=I.transferSize,mt=I.initiatorType;ft&&Bg(mt)&&(I=I.responseEnd,_+=ft*(I<T?1:(T-K)/(I-K)))}if(--s,n+=8*(f+_)/(u.duration/1e3),t++,10<t)break}}if(0<t)return n/t/1e6}return navigator.connection&&(t=navigator.connection.downlink,typeof t=="number")?t:5}var Af=null,Rf=null;function Wl(t){return t.nodeType===9?t:t.ownerDocument}function Ig(t){switch(t){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function Hg(t,n){if(t===0)switch(n){case"svg":return 1;case"math":return 2;default:return 0}return t===1&&n==="foreignObject"?0:t}function Cf(t,n){return t==="textarea"||t==="noscript"||typeof n.children=="string"||typeof n.children=="number"||typeof n.children=="bigint"||typeof n.dangerouslySetInnerHTML=="object"&&n.dangerouslySetInnerHTML!==null&&n.dangerouslySetInnerHTML.__html!=null}var Df=null;function Vx(){var t=window.event;return t&&t.type==="popstate"?t===Df?!1:(Df=t,!0):(Df=null,!1)}var Gg=typeof setTimeout=="function"?setTimeout:void 0,Xx=typeof clearTimeout=="function"?clearTimeout:void 0,Vg=typeof Promise=="function"?Promise:void 0,kx=typeof queueMicrotask=="function"?queueMicrotask:typeof Vg<"u"?function(t){return Vg.resolve(null).then(t).catch(Wx)}:Gg;function Wx(t){setTimeout(function(){throw t})}function za(t){return t==="head"}function Xg(t,n){var a=n,s=0;do{var u=a.nextSibling;if(t.removeChild(a),u&&u.nodeType===8)if(a=u.data,a==="/$"||a==="/&"){if(s===0){t.removeChild(u),us(n);return}s--}else if(a==="$"||a==="$?"||a==="$~"||a==="$!"||a==="&")s++;else if(a==="html")xo(t.ownerDocument.documentElement);else if(a==="head"){a=t.ownerDocument.head,xo(a);for(var f=a.firstChild;f;){var _=f.nextSibling,T=f.nodeName;f[Ja]||T==="SCRIPT"||T==="STYLE"||T==="LINK"&&f.rel.toLowerCase()==="stylesheet"||a.removeChild(f),f=_}}else a==="body"&&xo(t.ownerDocument.body);a=u}while(a);us(n)}function kg(t,n){var a=t;t=0;do{var s=a.nextSibling;if(a.nodeType===1?n?(a._stashedDisplay=a.style.display,a.style.display="none"):(a.style.display=a._stashedDisplay||"",a.getAttribute("style")===""&&a.removeAttribute("style")):a.nodeType===3&&(n?(a._stashedText=a.nodeValue,a.nodeValue=""):a.nodeValue=a._stashedText||""),s&&s.nodeType===8)if(a=s.data,a==="/$"){if(t===0)break;t--}else a!=="$"&&a!=="$?"&&a!=="$~"&&a!=="$!"||t++;a=s}while(a)}function wf(t){var n=t.firstChild;for(n&&n.nodeType===10&&(n=n.nextSibling);n;){var a=n;switch(n=n.nextSibling,a.nodeName){case"HTML":case"HEAD":case"BODY":wf(a),zs(a);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if(a.rel.toLowerCase()==="stylesheet")continue}t.removeChild(a)}}function qx(t,n,a,s){for(;t.nodeType===1;){var u=a;if(t.nodeName.toLowerCase()!==n.toLowerCase()){if(!s&&(t.nodeName!=="INPUT"||t.type!=="hidden"))break}else if(s){if(!t[Ja])switch(n){case"meta":if(!t.hasAttribute("itemprop"))break;return t;case"link":if(f=t.getAttribute("rel"),f==="stylesheet"&&t.hasAttribute("data-precedence"))break;if(f!==u.rel||t.getAttribute("href")!==(u.href==null||u.href===""?null:u.href)||t.getAttribute("crossorigin")!==(u.crossOrigin==null?null:u.crossOrigin)||t.getAttribute("title")!==(u.title==null?null:u.title))break;return t;case"style":if(t.hasAttribute("data-precedence"))break;return t;case"script":if(f=t.getAttribute("src"),(f!==(u.src==null?null:u.src)||t.getAttribute("type")!==(u.type==null?null:u.type)||t.getAttribute("crossorigin")!==(u.crossOrigin==null?null:u.crossOrigin))&&f&&t.hasAttribute("async")&&!t.hasAttribute("itemprop"))break;return t;default:return t}}else if(n==="input"&&t.type==="hidden"){var f=u.name==null?null:""+u.name;if(u.type==="hidden"&&t.getAttribute("name")===f)return t}else return t;if(t=li(t.nextSibling),t===null)break}return null}function Yx(t,n,a){if(n==="")return null;for(;t.nodeType!==3;)if((t.nodeType!==1||t.nodeName!=="INPUT"||t.type!=="hidden")&&!a||(t=li(t.nextSibling),t===null))return null;return t}function Wg(t,n){for(;t.nodeType!==8;)if((t.nodeType!==1||t.nodeName!=="INPUT"||t.type!=="hidden")&&!n||(t=li(t.nextSibling),t===null))return null;return t}function Uf(t){return t.data==="$?"||t.data==="$~"}function Lf(t){return t.data==="$!"||t.data==="$?"&&t.ownerDocument.readyState!=="loading"}function Zx(t,n){var a=t.ownerDocument;if(t.data==="$~")t._reactRetry=n;else if(t.data!=="$?"||a.readyState!=="loading")n();else{var s=function(){n(),a.removeEventListener("DOMContentLoaded",s)};a.addEventListener("DOMContentLoaded",s),t._reactRetry=s}}function li(t){for(;t!=null;t=t.nextSibling){var n=t.nodeType;if(n===1||n===3)break;if(n===8){if(n=t.data,n==="$"||n==="$!"||n==="$?"||n==="$~"||n==="&"||n==="F!"||n==="F")break;if(n==="/$"||n==="/&")return null}}return t}var Nf=null;function qg(t){t=t.nextSibling;for(var n=0;t;){if(t.nodeType===8){var a=t.data;if(a==="/$"||a==="/&"){if(n===0)return li(t.nextSibling);n--}else a!=="$"&&a!=="$!"&&a!=="$?"&&a!=="$~"&&a!=="&"||n++}t=t.nextSibling}return null}function Yg(t){t=t.previousSibling;for(var n=0;t;){if(t.nodeType===8){var a=t.data;if(a==="$"||a==="$!"||a==="$?"||a==="$~"||a==="&"){if(n===0)return t;n--}else a!=="/$"&&a!=="/&"||n++}t=t.previousSibling}return null}function Zg(t,n,a){switch(n=Wl(a),t){case"html":if(t=n.documentElement,!t)throw Error(r(452));return t;case"head":if(t=n.head,!t)throw Error(r(453));return t;case"body":if(t=n.body,!t)throw Error(r(454));return t;default:throw Error(r(451))}}function xo(t){for(var n=t.attributes;n.length;)t.removeAttributeNode(n[0]);zs(t)}var ui=new Map,jg=new Set;function ql(t){return typeof t.getRootNode=="function"?t.getRootNode():t.nodeType===9?t:t.ownerDocument}var aa=V.d;V.d={f:jx,r:Kx,D:Qx,C:Jx,L:$x,m:tS,X:nS,S:eS,M:iS};function jx(){var t=aa.f(),n=zl();return t||n}function Kx(t){var n=va(t);n!==null&&n.tag===5&&n.type==="form"?hm(n):aa.r(t)}var ss=typeof document>"u"?null:document;function Kg(t,n,a){var s=ss;if(s&&typeof n=="string"&&n){var u=ne(n);u='link[rel="'+t+'"][href="'+u+'"]',typeof a=="string"&&(u+='[crossorigin="'+a+'"]'),jg.has(u)||(jg.add(u),t={rel:t,crossOrigin:a,href:n},s.querySelector(u)===null&&(n=s.createElement("link"),bn(n,"link",t),b(n),s.head.appendChild(n)))}}function Qx(t){aa.D(t),Kg("dns-prefetch",t,null)}function Jx(t,n){aa.C(t,n),Kg("preconnect",t,n)}function $x(t,n,a){aa.L(t,n,a);var s=ss;if(s&&t&&n){var u='link[rel="preload"][as="'+ne(n)+'"]';n==="image"&&a&&a.imageSrcSet?(u+='[imagesrcset="'+ne(a.imageSrcSet)+'"]',typeof a.imageSizes=="string"&&(u+='[imagesizes="'+ne(a.imageSizes)+'"]')):u+='[href="'+ne(t)+'"]';var f=u;switch(n){case"style":f=os(t);break;case"script":f=ls(t)}ui.has(f)||(t=g({rel:"preload",href:n==="image"&&a&&a.imageSrcSet?void 0:t,as:n},a),ui.set(f,t),s.querySelector(u)!==null||n==="style"&&s.querySelector(So(f))||n==="script"&&s.querySelector(Mo(f))||(n=s.createElement("link"),bn(n,"link",t),b(n),s.head.appendChild(n)))}}function tS(t,n){aa.m(t,n);var a=ss;if(a&&t){var s=n&&typeof n.as=="string"?n.as:"script",u='link[rel="modulepreload"][as="'+ne(s)+'"][href="'+ne(t)+'"]',f=u;switch(s){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":f=ls(t)}if(!ui.has(f)&&(t=g({rel:"modulepreload",href:t},n),ui.set(f,t),a.querySelector(u)===null)){switch(s){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(a.querySelector(Mo(f)))return}s=a.createElement("link"),bn(s,"link",t),b(s),a.head.appendChild(s)}}}function eS(t,n,a){aa.S(t,n,a);var s=ss;if(s&&t){var u=xa(s).hoistableStyles,f=os(t);n=n||"default";var _=u.get(f);if(!_){var T={loading:0,preload:null};if(_=s.querySelector(So(f)))T.loading=5;else{t=g({rel:"stylesheet",href:t,"data-precedence":n},a),(a=ui.get(f))&&Of(t,a);var I=_=s.createElement("link");b(I),bn(I,"link",t),I._p=new Promise(function(K,ft){I.onload=K,I.onerror=ft}),I.addEventListener("load",function(){T.loading|=1}),I.addEventListener("error",function(){T.loading|=2}),T.loading|=4,Yl(_,n,s)}_={type:"stylesheet",instance:_,count:1,state:T},u.set(f,_)}}}function nS(t,n){aa.X(t,n);var a=ss;if(a&&t){var s=xa(a).hoistableScripts,u=ls(t),f=s.get(u);f||(f=a.querySelector(Mo(u)),f||(t=g({src:t,async:!0},n),(n=ui.get(u))&&Pf(t,n),f=a.createElement("script"),b(f),bn(f,"link",t),a.head.appendChild(f)),f={type:"script",instance:f,count:1,state:null},s.set(u,f))}}function iS(t,n){aa.M(t,n);var a=ss;if(a&&t){var s=xa(a).hoistableScripts,u=ls(t),f=s.get(u);f||(f=a.querySelector(Mo(u)),f||(t=g({src:t,async:!0,type:"module"},n),(n=ui.get(u))&&Pf(t,n),f=a.createElement("script"),b(f),bn(f,"link",t),a.head.appendChild(f)),f={type:"script",instance:f,count:1,state:null},s.set(u,f))}}function Qg(t,n,a,s){var u=(u=tt.current)?ql(u):null;if(!u)throw Error(r(446));switch(t){case"meta":case"title":return null;case"style":return typeof a.precedence=="string"&&typeof a.href=="string"?(n=os(a.href),a=xa(u).hoistableStyles,s=a.get(n),s||(s={type:"style",instance:null,count:0,state:null},a.set(n,s)),s):{type:"void",instance:null,count:0,state:null};case"link":if(a.rel==="stylesheet"&&typeof a.href=="string"&&typeof a.precedence=="string"){t=os(a.href);var f=xa(u).hoistableStyles,_=f.get(t);if(_||(u=u.ownerDocument||u,_={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},f.set(t,_),(f=u.querySelector(So(t)))&&!f._p&&(_.instance=f,_.state.loading=5),ui.has(t)||(a={rel:"preload",as:"style",href:a.href,crossOrigin:a.crossOrigin,integrity:a.integrity,media:a.media,hrefLang:a.hrefLang,referrerPolicy:a.referrerPolicy},ui.set(t,a),f||aS(u,t,a,_.state))),n&&s===null)throw Error(r(528,""));return _}if(n&&s!==null)throw Error(r(529,""));return null;case"script":return n=a.async,a=a.src,typeof a=="string"&&n&&typeof n!="function"&&typeof n!="symbol"?(n=ls(a),a=xa(u).hoistableScripts,s=a.get(n),s||(s={type:"script",instance:null,count:0,state:null},a.set(n,s)),s):{type:"void",instance:null,count:0,state:null};default:throw Error(r(444,t))}}function os(t){return'href="'+ne(t)+'"'}function So(t){return'link[rel="stylesheet"]['+t+"]"}function Jg(t){return g({},t,{"data-precedence":t.precedence,precedence:null})}function aS(t,n,a,s){t.querySelector('link[rel="preload"][as="style"]['+n+"]")?s.loading=1:(n=t.createElement("link"),s.preload=n,n.addEventListener("load",function(){return s.loading|=1}),n.addEventListener("error",function(){return s.loading|=2}),bn(n,"link",a),b(n),t.head.appendChild(n))}function ls(t){return'[src="'+ne(t)+'"]'}function Mo(t){return"script[async]"+t}function $g(t,n,a){if(n.count++,n.instance===null)switch(n.type){case"style":var s=t.querySelector('style[data-href~="'+ne(a.href)+'"]');if(s)return n.instance=s,b(s),s;var u=g({},a,{"data-href":a.href,"data-precedence":a.precedence,href:null,precedence:null});return s=(t.ownerDocument||t).createElement("style"),b(s),bn(s,"style",u),Yl(s,a.precedence,t),n.instance=s;case"stylesheet":u=os(a.href);var f=t.querySelector(So(u));if(f)return n.state.loading|=4,n.instance=f,b(f),f;s=Jg(a),(u=ui.get(u))&&Of(s,u),f=(t.ownerDocument||t).createElement("link"),b(f);var _=f;return _._p=new Promise(function(T,I){_.onload=T,_.onerror=I}),bn(f,"link",s),n.state.loading|=4,Yl(f,a.precedence,t),n.instance=f;case"script":return f=ls(a.src),(u=t.querySelector(Mo(f)))?(n.instance=u,b(u),u):(s=a,(u=ui.get(f))&&(s=g({},a),Pf(s,u)),t=t.ownerDocument||t,u=t.createElement("script"),b(u),bn(u,"link",s),t.head.appendChild(u),n.instance=u);case"void":return null;default:throw Error(r(443,n.type))}else n.type==="stylesheet"&&(n.state.loading&4)===0&&(s=n.instance,n.state.loading|=4,Yl(s,a.precedence,t));return n.instance}function Yl(t,n,a){for(var s=a.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),u=s.length?s[s.length-1]:null,f=u,_=0;_<s.length;_++){var T=s[_];if(T.dataset.precedence===n)f=T;else if(f!==u)break}f?f.parentNode.insertBefore(t,f.nextSibling):(n=a.nodeType===9?a.head:a,n.insertBefore(t,n.firstChild))}function Of(t,n){t.crossOrigin==null&&(t.crossOrigin=n.crossOrigin),t.referrerPolicy==null&&(t.referrerPolicy=n.referrerPolicy),t.title==null&&(t.title=n.title)}function Pf(t,n){t.crossOrigin==null&&(t.crossOrigin=n.crossOrigin),t.referrerPolicy==null&&(t.referrerPolicy=n.referrerPolicy),t.integrity==null&&(t.integrity=n.integrity)}var Zl=null;function t0(t,n,a){if(Zl===null){var s=new Map,u=Zl=new Map;u.set(a,s)}else u=Zl,s=u.get(a),s||(s=new Map,u.set(a,s));if(s.has(t))return s;for(s.set(t,null),a=a.getElementsByTagName(t),u=0;u<a.length;u++){var f=a[u];if(!(f[Ja]||f[an]||t==="link"&&f.getAttribute("rel")==="stylesheet")&&f.namespaceURI!=="http://www.w3.org/2000/svg"){var _=f.getAttribute(n)||"";_=t+_;var T=s.get(_);T?T.push(f):s.set(_,[f])}}return s}function e0(t,n,a){t=t.ownerDocument||t,t.head.insertBefore(a,n==="title"?t.querySelector("head > title"):null)}function rS(t,n,a){if(a===1||n.itemProp!=null)return!1;switch(t){case"meta":case"title":return!0;case"style":if(typeof n.precedence!="string"||typeof n.href!="string"||n.href==="")break;return!0;case"link":if(typeof n.rel!="string"||typeof n.href!="string"||n.href===""||n.onLoad||n.onError)break;return n.rel==="stylesheet"?(t=n.disabled,typeof n.precedence=="string"&&t==null):!0;case"script":if(n.async&&typeof n.async!="function"&&typeof n.async!="symbol"&&!n.onLoad&&!n.onError&&n.src&&typeof n.src=="string")return!0}return!1}function n0(t){return!(t.type==="stylesheet"&&(t.state.loading&3)===0)}function sS(t,n,a,s){if(a.type==="stylesheet"&&(typeof s.media!="string"||matchMedia(s.media).matches!==!1)&&(a.state.loading&4)===0){if(a.instance===null){var u=os(s.href),f=n.querySelector(So(u));if(f){n=f._p,n!==null&&typeof n=="object"&&typeof n.then=="function"&&(t.count++,t=jl.bind(t),n.then(t,t)),a.state.loading|=4,a.instance=f,b(f);return}f=n.ownerDocument||n,s=Jg(s),(u=ui.get(u))&&Of(s,u),f=f.createElement("link"),b(f);var _=f;_._p=new Promise(function(T,I){_.onload=T,_.onerror=I}),bn(f,"link",s),a.instance=f}t.stylesheets===null&&(t.stylesheets=new Map),t.stylesheets.set(a,n),(n=a.state.preload)&&(a.state.loading&3)===0&&(t.count++,a=jl.bind(t),n.addEventListener("load",a),n.addEventListener("error",a))}}var Ff=0;function oS(t,n){return t.stylesheets&&t.count===0&&Ql(t,t.stylesheets),0<t.count||0<t.imgCount?function(a){var s=setTimeout(function(){if(t.stylesheets&&Ql(t,t.stylesheets),t.unsuspend){var f=t.unsuspend;t.unsuspend=null,f()}},6e4+n);0<t.imgBytes&&Ff===0&&(Ff=62500*Gx());var u=setTimeout(function(){if(t.waitingForImages=!1,t.count===0&&(t.stylesheets&&Ql(t,t.stylesheets),t.unsuspend)){var f=t.unsuspend;t.unsuspend=null,f()}},(t.imgBytes>Ff?50:800)+n);return t.unsuspend=a,function(){t.unsuspend=null,clearTimeout(s),clearTimeout(u)}}:null}function jl(){if(this.count--,this.count===0&&(this.imgCount===0||!this.waitingForImages)){if(this.stylesheets)Ql(this,this.stylesheets);else if(this.unsuspend){var t=this.unsuspend;this.unsuspend=null,t()}}}var Kl=null;function Ql(t,n){t.stylesheets=null,t.unsuspend!==null&&(t.count++,Kl=new Map,n.forEach(lS,t),Kl=null,jl.call(t))}function lS(t,n){if(!(n.state.loading&4)){var a=Kl.get(t);if(a)var s=a.get(null);else{a=new Map,Kl.set(t,a);for(var u=t.querySelectorAll("link[data-precedence],style[data-precedence]"),f=0;f<u.length;f++){var _=u[f];(_.nodeName==="LINK"||_.getAttribute("media")!=="not all")&&(a.set(_.dataset.precedence,_),s=_)}s&&a.set(null,s)}u=n.instance,_=u.getAttribute("data-precedence"),f=a.get(_)||s,f===s&&a.set(null,u),a.set(_,u),this.count++,s=jl.bind(this),u.addEventListener("load",s),u.addEventListener("error",s),f?f.parentNode.insertBefore(u,f.nextSibling):(t=t.nodeType===9?t.head:t,t.insertBefore(u,t.firstChild)),n.state.loading|=4}}var yo={$$typeof:N,Provider:null,Consumer:null,_currentValue:nt,_currentValue2:nt,_threadCount:0};function uS(t,n,a,s,u,f,_,T,I){this.tag=1,this.containerInfo=t,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=Me(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Me(0),this.hiddenUpdates=Me(null),this.identifierPrefix=s,this.onUncaughtError=u,this.onCaughtError=f,this.onRecoverableError=_,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=I,this.incompleteTransitions=new Map}function i0(t,n,a,s,u,f,_,T,I,K,ft,mt){return t=new uS(t,n,a,_,I,K,ft,mt,T),n=1,f===!0&&(n|=24),f=Wn(3,null,null,n),t.current=f,f.stateNode=t,n=pc(),n.refCount++,t.pooledCache=n,n.refCount++,f.memoizedState={element:s,isDehydrated:a,cache:n},vc(f),t}function a0(t){return t?(t=Ir,t):Ir}function r0(t,n,a,s,u,f){u=a0(u),s.context===null?s.context=u:s.pendingContext=u,s=Aa(n),s.payload={element:a},f=f===void 0?null:f,f!==null&&(s.callback=f),a=Ra(t,s,n),a!==null&&(Gn(a,t,n),$s(a,t,n))}function s0(t,n){if(t=t.memoizedState,t!==null&&t.dehydrated!==null){var a=t.retryLane;t.retryLane=a!==0&&a<n?a:n}}function zf(t,n){s0(t,n),(t=t.alternate)&&s0(t,n)}function o0(t){if(t.tag===13||t.tag===31){var n=ir(t,67108864);n!==null&&Gn(n,t,67108864),zf(t,67108864)}}function l0(t){if(t.tag===13||t.tag===31){var n=Kn();n=Os(n);var a=ir(t,n);a!==null&&Gn(a,t,n),zf(t,n)}}var Jl=!0;function cS(t,n,a,s){var u=O.T;O.T=null;var f=V.p;try{V.p=2,Bf(t,n,a,s)}finally{V.p=f,O.T=u}}function fS(t,n,a,s){var u=O.T;O.T=null;var f=V.p;try{V.p=8,Bf(t,n,a,s)}finally{V.p=f,O.T=u}}function Bf(t,n,a,s){if(Jl){var u=If(s);if(u===null)Tf(t,n,s,$l,a),c0(t,s);else if(dS(u,t,n,a,s))s.stopPropagation();else if(c0(t,s),n&4&&-1<hS.indexOf(t)){for(;u!==null;){var f=va(u);if(f!==null)switch(f.tag){case 3:if(f=f.stateNode,f.current.memoizedState.isDehydrated){var _=St(f.pendingLanes);if(_!==0){var T=f;for(T.pendingLanes|=2,T.entangledLanes|=2;_;){var I=1<<31-Ot(_);T.entanglements[1]|=I,_&=~I}Di(f),(De&6)===0&&(Pl=E()+500,go(0))}}break;case 31:case 13:T=ir(f,2),T!==null&&Gn(T,f,2),zl(),zf(f,2)}if(f=If(s),f===null&&Tf(t,n,s,$l,a),f===u)break;u=f}u!==null&&s.stopPropagation()}else Tf(t,n,s,null,a)}}function If(t){return t=Hu(t),Hf(t)}var $l=null;function Hf(t){if($l=null,t=_a(t),t!==null){var n=c(t);if(n===null)t=null;else{var a=n.tag;if(a===13){if(t=h(n),t!==null)return t;t=null}else if(a===31){if(t=d(n),t!==null)return t;t=null}else if(a===3){if(n.stateNode.current.memoizedState.isDehydrated)return n.tag===3?n.stateNode.containerInfo:null;t=null}else n!==t&&(t=null)}}return $l=t,null}function u0(t){switch(t){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(W()){case dt:return 2;case vt:return 8;case lt:case Zt:return 32;case Rt:return 268435456;default:return 32}default:return 32}}var Gf=!1,Ba=null,Ia=null,Ha=null,Eo=new Map,To=new Map,Ga=[],hS="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function c0(t,n){switch(t){case"focusin":case"focusout":Ba=null;break;case"dragenter":case"dragleave":Ia=null;break;case"mouseover":case"mouseout":Ha=null;break;case"pointerover":case"pointerout":Eo.delete(n.pointerId);break;case"gotpointercapture":case"lostpointercapture":To.delete(n.pointerId)}}function bo(t,n,a,s,u,f){return t===null||t.nativeEvent!==f?(t={blockedOn:n,domEventName:a,eventSystemFlags:s,nativeEvent:f,targetContainers:[u]},n!==null&&(n=va(n),n!==null&&o0(n)),t):(t.eventSystemFlags|=s,n=t.targetContainers,u!==null&&n.indexOf(u)===-1&&n.push(u),t)}function dS(t,n,a,s,u){switch(n){case"focusin":return Ba=bo(Ba,t,n,a,s,u),!0;case"dragenter":return Ia=bo(Ia,t,n,a,s,u),!0;case"mouseover":return Ha=bo(Ha,t,n,a,s,u),!0;case"pointerover":var f=u.pointerId;return Eo.set(f,bo(Eo.get(f)||null,t,n,a,s,u)),!0;case"gotpointercapture":return f=u.pointerId,To.set(f,bo(To.get(f)||null,t,n,a,s,u)),!0}return!1}function f0(t){var n=_a(t.target);if(n!==null){var a=c(n);if(a!==null){if(n=a.tag,n===13){if(n=h(a),n!==null){t.blockedOn=n,bi(t.priority,function(){l0(a)});return}}else if(n===31){if(n=d(a),n!==null){t.blockedOn=n,bi(t.priority,function(){l0(a)});return}}else if(n===3&&a.stateNode.current.memoizedState.isDehydrated){t.blockedOn=a.tag===3?a.stateNode.containerInfo:null;return}}}t.blockedOn=null}function tu(t){if(t.blockedOn!==null)return!1;for(var n=t.targetContainers;0<n.length;){var a=If(t.nativeEvent);if(a===null){a=t.nativeEvent;var s=new a.constructor(a.type,a);Iu=s,a.target.dispatchEvent(s),Iu=null}else return n=va(a),n!==null&&o0(n),t.blockedOn=a,!1;n.shift()}return!0}function h0(t,n,a){tu(t)&&a.delete(n)}function pS(){Gf=!1,Ba!==null&&tu(Ba)&&(Ba=null),Ia!==null&&tu(Ia)&&(Ia=null),Ha!==null&&tu(Ha)&&(Ha=null),Eo.forEach(h0),To.forEach(h0)}function eu(t,n){t.blockedOn===n&&(t.blockedOn=null,Gf||(Gf=!0,o.unstable_scheduleCallback(o.unstable_NormalPriority,pS)))}var nu=null;function d0(t){nu!==t&&(nu=t,o.unstable_scheduleCallback(o.unstable_NormalPriority,function(){nu===t&&(nu=null);for(var n=0;n<t.length;n+=3){var a=t[n],s=t[n+1],u=t[n+2];if(typeof s!="function"){if(Hf(s||a)===null)continue;break}var f=va(a);f!==null&&(t.splice(n,3),n-=3,Bc(f,{pending:!0,data:u,method:a.method,action:s},s,u))}}))}function us(t){function n(I){return eu(I,t)}Ba!==null&&eu(Ba,t),Ia!==null&&eu(Ia,t),Ha!==null&&eu(Ha,t),Eo.forEach(n),To.forEach(n);for(var a=0;a<Ga.length;a++){var s=Ga[a];s.blockedOn===t&&(s.blockedOn=null)}for(;0<Ga.length&&(a=Ga[0],a.blockedOn===null);)f0(a),a.blockedOn===null&&Ga.shift();if(a=(t.ownerDocument||t).$$reactFormReplay,a!=null)for(s=0;s<a.length;s+=3){var u=a[s],f=a[s+1],_=u[gn]||null;if(typeof f=="function")_||d0(a);else if(_){var T=null;if(f&&f.hasAttribute("formAction")){if(u=f,_=f[gn]||null)T=_.formAction;else if(Hf(u)!==null)continue}else T=_.action;typeof T=="function"?a[s+1]=T:(a.splice(s,3),s-=3),d0(a)}}}function p0(){function t(f){f.canIntercept&&f.info==="react-transition"&&f.intercept({handler:function(){return new Promise(function(_){return u=_})},focusReset:"manual",scroll:"manual"})}function n(){u!==null&&(u(),u=null),s||setTimeout(a,20)}function a(){if(!s&&!navigation.transition){var f=navigation.currentEntry;f&&f.url!=null&&navigation.navigate(f.url,{state:f.getState(),info:"react-transition",history:"replace"})}}if(typeof navigation=="object"){var s=!1,u=null;return navigation.addEventListener("navigate",t),navigation.addEventListener("navigatesuccess",n),navigation.addEventListener("navigateerror",n),setTimeout(a,100),function(){s=!0,navigation.removeEventListener("navigate",t),navigation.removeEventListener("navigatesuccess",n),navigation.removeEventListener("navigateerror",n),u!==null&&(u(),u=null)}}}function Vf(t){this._internalRoot=t}iu.prototype.render=Vf.prototype.render=function(t){var n=this._internalRoot;if(n===null)throw Error(r(409));var a=n.current,s=Kn();r0(a,s,t,n,null,null)},iu.prototype.unmount=Vf.prototype.unmount=function(){var t=this._internalRoot;if(t!==null){this._internalRoot=null;var n=t.containerInfo;r0(t.current,2,null,t,null,null),zl(),n[pi]=null}};function iu(t){this._internalRoot=t}iu.prototype.unstable_scheduleHydration=function(t){if(t){var n=Ps();t={blockedOn:null,target:t,priority:n};for(var a=0;a<Ga.length&&n!==0&&n<Ga[a].priority;a++);Ga.splice(a,0,t),a===0&&f0(t)}};var m0=e.version;if(m0!=="19.2.3")throw Error(r(527,m0,"19.2.3"));V.findDOMNode=function(t){var n=t._reactInternals;if(n===void 0)throw typeof t.render=="function"?Error(r(188)):(t=Object.keys(t).join(","),Error(r(268,t)));return t=p(n),t=t!==null?v(t):null,t=t===null?null:t.stateNode,t};var mS={bundleType:0,version:"19.2.3",rendererPackageName:"react-dom",currentDispatcherRef:O,reconcilerVersion:"19.2.3"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var au=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!au.isDisabled&&au.supportsFiber)try{yt=au.inject(mS),Et=au}catch{}}return Ro.createRoot=function(t,n){if(!l(t))throw Error(r(299));var a=!1,s="",u=ym,f=Em,_=Tm;return n!=null&&(n.unstable_strictMode===!0&&(a=!0),n.identifierPrefix!==void 0&&(s=n.identifierPrefix),n.onUncaughtError!==void 0&&(u=n.onUncaughtError),n.onCaughtError!==void 0&&(f=n.onCaughtError),n.onRecoverableError!==void 0&&(_=n.onRecoverableError)),n=i0(t,1,!1,null,null,a,s,null,u,f,_,p0),t[pi]=n.current,Ef(t),new Vf(n)},Ro.hydrateRoot=function(t,n,a){if(!l(t))throw Error(r(299));var s=!1,u="",f=ym,_=Em,T=Tm,I=null;return a!=null&&(a.unstable_strictMode===!0&&(s=!0),a.identifierPrefix!==void 0&&(u=a.identifierPrefix),a.onUncaughtError!==void 0&&(f=a.onUncaughtError),a.onCaughtError!==void 0&&(_=a.onCaughtError),a.onRecoverableError!==void 0&&(T=a.onRecoverableError),a.formState!==void 0&&(I=a.formState)),n=i0(t,1,!0,n,a??null,s,u,I,f,_,T,p0),n.context=a0(null),a=n.current,s=Kn(),s=Os(s),u=Aa(s),u.callback=null,Ra(a,u,s),a=s,n.current.lanes=a,Rn(n,a),Di(n),t[pi]=n.current,Ef(t),new iu(n)},Ro.version="19.2.3",Ro}var b0;function RS(){if(b0)return Wf.exports;b0=1;function o(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(o)}catch(e){console.error(e)}}return o(),Wf.exports=AS(),Wf.exports}var KA=RS();const CS="modulepreload",DS=function(o){return"/"+o},A0={},QA=function(e,i,r){let l=Promise.resolve();if(i&&i.length>0){let m=function(p){return Promise.all(p.map(v=>Promise.resolve(v).then(g=>({status:"fulfilled",value:g}),g=>({status:"rejected",reason:g}))))};document.getElementsByTagName("link");const h=document.querySelector("meta[property=csp-nonce]"),d=h?.nonce||h?.getAttribute("nonce");l=m(i.map(p=>{if(p=DS(p),p in A0)return;A0[p]=!0;const v=p.endsWith(".css"),g=v?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${p}"]${g}`))return;const S=document.createElement("link");if(S.rel=v?"stylesheet":CS,v||(S.as="script"),S.crossOrigin="",S.href=p,d&&S.setAttribute("nonce",d),document.head.appendChild(S),v)return new Promise((M,A)=>{S.addEventListener("load",M),S.addEventListener("error",()=>A(new Error(`Unable to preload CSS for ${p}`)))})}))}function c(h){const d=new Event("vite:preloadError",{cancelable:!0});if(d.payload=h,window.dispatchEvent(d),!d.defaultPrevented)throw h}return l.then(h=>{for(const d of h||[])d.status==="rejected"&&c(d.reason);return e().catch(c)})},R0=o=>{let e;const i=new Set,r=(p,v)=>{const g=typeof p=="function"?p(e):p;if(!Object.is(g,e)){const S=e;e=v??(typeof g!="object"||g===null)?g:Object.assign({},e,g),i.forEach(M=>M(e,S))}},l=()=>e,d={setState:r,getState:l,getInitialState:()=>m,subscribe:p=>(i.add(p),()=>i.delete(p))},m=e=o(r,l,d);return d},wS=(o=>o?R0(o):R0),US=o=>o;function LS(o,e=US){const i=Po.useSyncExternalStore(o.subscribe,Po.useCallback(()=>e(o.getState()),[o,e]),Po.useCallback(()=>e(o.getInitialState()),[o,e]));return Po.useDebugValue(i),i}const C0=o=>{const e=wS(o),i=r=>LS(e,r);return Object.assign(i,e),i},JA=(o=>o?C0(o):C0);const bd="182",NS=0,D0=1,OS=2,Au=1,PS=2,Fo=3,Qa=0,Xn=1,ca=2,ha=0,Ts=1,w0=2,U0=3,L0=4,FS=5,Er=100,zS=101,BS=102,IS=103,HS=104,GS=200,VS=201,XS=202,kS=203,Uh=204,Lh=205,WS=206,qS=207,YS=208,ZS=209,jS=210,KS=211,QS=212,JS=213,$S=214,Nh=0,Oh=1,Ph=2,As=3,Fh=4,zh=5,Bh=6,Ih=7,U_=0,tM=1,eM=2,Oi=0,L_=1,N_=2,O_=3,P_=4,F_=5,z_=6,B_=7,I_=300,Rr=301,Rs=302,Hh=303,Gh=304,Pu=306,Vh=1e3,fa=1001,Xh=1002,An=1003,nM=1004,ru=1005,Un=1006,jf=1007,br=1008,$n=1009,H_=1010,G_=1011,Bo=1012,Ad=1013,zi=1014,Li=1015,pa=1016,Rd=1017,Cd=1018,Io=1020,V_=35902,X_=35899,k_=1021,W_=1022,Ti=1023,ma=1026,Ar=1027,q_=1028,Dd=1029,Cs=1030,wd=1031,Ud=1033,Ru=33776,Cu=33777,Du=33778,wu=33779,kh=35840,Wh=35841,qh=35842,Yh=35843,Zh=36196,jh=37492,Kh=37496,Qh=37488,Jh=37489,$h=37490,td=37491,ed=37808,nd=37809,id=37810,ad=37811,rd=37812,sd=37813,od=37814,ld=37815,ud=37816,cd=37817,fd=37818,hd=37819,dd=37820,pd=37821,md=36492,gd=36494,_d=36495,vd=36283,xd=36284,Sd=36285,Md=36286,iM=3200,Y_=0,aM=1,ja="",fi="srgb",Ds="srgb-linear",Lu="linear",Be="srgb",cs=7680,N0=519,rM=512,sM=513,oM=514,Ld=515,lM=516,uM=517,Nd=518,cM=519,O0=35044,P0="300 es",Ni=2e3,Nu=2001;function Z_(o){for(let e=o.length-1;e>=0;--e)if(o[e]>=65535)return!0;return!1}function Ou(o){return document.createElementNS("http://www.w3.org/1999/xhtml",o)}function fM(){const o=Ou("canvas");return o.style.display="block",o}const F0={};function z0(...o){const e="THREE."+o.shift();console.log(e,...o)}function ae(...o){const e="THREE."+o.shift();console.warn(e,...o)}function be(...o){const e="THREE."+o.shift();console.error(e,...o)}function Ho(...o){const e=o.join(" ");e in F0||(F0[e]=!0,ae(...o))}function hM(o,e,i){return new Promise(function(r,l){function c(){switch(o.clientWaitSync(e,o.SYNC_FLUSH_COMMANDS_BIT,0)){case o.WAIT_FAILED:l();break;case o.TIMEOUT_EXPIRED:setTimeout(c,i);break;default:r()}}setTimeout(c,i)})}class Us{addEventListener(e,i){this._listeners===void 0&&(this._listeners={});const r=this._listeners;r[e]===void 0&&(r[e]=[]),r[e].indexOf(i)===-1&&r[e].push(i)}hasEventListener(e,i){const r=this._listeners;return r===void 0?!1:r[e]!==void 0&&r[e].indexOf(i)!==-1}removeEventListener(e,i){const r=this._listeners;if(r===void 0)return;const l=r[e];if(l!==void 0){const c=l.indexOf(i);c!==-1&&l.splice(c,1)}}dispatchEvent(e){const i=this._listeners;if(i===void 0)return;const r=i[e.type];if(r!==void 0){e.target=this;const l=r.slice(0);for(let c=0,h=l.length;c<h;c++)l[c].call(this,e);e.target=null}}}const Dn=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Kf=Math.PI/180,yd=180/Math.PI;function Xo(){const o=Math.random()*4294967295|0,e=Math.random()*4294967295|0,i=Math.random()*4294967295|0,r=Math.random()*4294967295|0;return(Dn[o&255]+Dn[o>>8&255]+Dn[o>>16&255]+Dn[o>>24&255]+"-"+Dn[e&255]+Dn[e>>8&255]+"-"+Dn[e>>16&15|64]+Dn[e>>24&255]+"-"+Dn[i&63|128]+Dn[i>>8&255]+"-"+Dn[i>>16&255]+Dn[i>>24&255]+Dn[r&255]+Dn[r>>8&255]+Dn[r>>16&255]+Dn[r>>24&255]).toLowerCase()}function xe(o,e,i){return Math.max(e,Math.min(i,o))}function dM(o,e){return(o%e+e)%e}function Qf(o,e,i){return(1-i)*o+i*e}function Co(o,e){switch(e.constructor){case Float32Array:return o;case Uint32Array:return o/4294967295;case Uint16Array:return o/65535;case Uint8Array:return o/255;case Int32Array:return Math.max(o/2147483647,-1);case Int16Array:return Math.max(o/32767,-1);case Int8Array:return Math.max(o/127,-1);default:throw new Error("Invalid component type.")}}function Vn(o,e){switch(e.constructor){case Float32Array:return o;case Uint32Array:return Math.round(o*4294967295);case Uint16Array:return Math.round(o*65535);case Uint8Array:return Math.round(o*255);case Int32Array:return Math.round(o*2147483647);case Int16Array:return Math.round(o*32767);case Int8Array:return Math.round(o*127);default:throw new Error("Invalid component type.")}}class Ue{constructor(e=0,i=0){Ue.prototype.isVector2=!0,this.x=e,this.y=i}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,i){return this.x=e,this.y=i,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const i=this.x,r=this.y,l=e.elements;return this.x=l[0]*i+l[3]*r+l[6],this.y=l[1]*i+l[4]*r+l[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,i){return this.x=xe(this.x,e.x,i.x),this.y=xe(this.y,e.y,i.y),this}clampScalar(e,i){return this.x=xe(this.x,e,i),this.y=xe(this.y,e,i),this}clampLength(e,i){const r=this.length();return this.divideScalar(r||1).multiplyScalar(xe(r,e,i))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const i=Math.sqrt(this.lengthSq()*e.lengthSq());if(i===0)return Math.PI/2;const r=this.dot(e)/i;return Math.acos(xe(r,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const i=this.x-e.x,r=this.y-e.y;return i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this}lerpVectors(e,i,r){return this.x=e.x+(i.x-e.x)*r,this.y=e.y+(i.y-e.y)*r,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this}rotateAround(e,i){const r=Math.cos(i),l=Math.sin(i),c=this.x-e.x,h=this.y-e.y;return this.x=c*r-h*l+e.x,this.y=c*l+h*r+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class ko{constructor(e=0,i=0,r=0,l=1){this.isQuaternion=!0,this._x=e,this._y=i,this._z=r,this._w=l}static slerpFlat(e,i,r,l,c,h,d){let m=r[l+0],p=r[l+1],v=r[l+2],g=r[l+3],S=c[h+0],M=c[h+1],A=c[h+2],C=c[h+3];if(d<=0){e[i+0]=m,e[i+1]=p,e[i+2]=v,e[i+3]=g;return}if(d>=1){e[i+0]=S,e[i+1]=M,e[i+2]=A,e[i+3]=C;return}if(g!==C||m!==S||p!==M||v!==A){let y=m*S+p*M+v*A+g*C;y<0&&(S=-S,M=-M,A=-A,C=-C,y=-y);let x=1-d;if(y<.9995){const P=Math.acos(y),N=Math.sin(P);x=Math.sin(x*P)/N,d=Math.sin(d*P)/N,m=m*x+S*d,p=p*x+M*d,v=v*x+A*d,g=g*x+C*d}else{m=m*x+S*d,p=p*x+M*d,v=v*x+A*d,g=g*x+C*d;const P=1/Math.sqrt(m*m+p*p+v*v+g*g);m*=P,p*=P,v*=P,g*=P}}e[i]=m,e[i+1]=p,e[i+2]=v,e[i+3]=g}static multiplyQuaternionsFlat(e,i,r,l,c,h){const d=r[l],m=r[l+1],p=r[l+2],v=r[l+3],g=c[h],S=c[h+1],M=c[h+2],A=c[h+3];return e[i]=d*A+v*g+m*M-p*S,e[i+1]=m*A+v*S+p*g-d*M,e[i+2]=p*A+v*M+d*S-m*g,e[i+3]=v*A-d*g-m*S-p*M,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,i,r,l){return this._x=e,this._y=i,this._z=r,this._w=l,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,i=!0){const r=e._x,l=e._y,c=e._z,h=e._order,d=Math.cos,m=Math.sin,p=d(r/2),v=d(l/2),g=d(c/2),S=m(r/2),M=m(l/2),A=m(c/2);switch(h){case"XYZ":this._x=S*v*g+p*M*A,this._y=p*M*g-S*v*A,this._z=p*v*A+S*M*g,this._w=p*v*g-S*M*A;break;case"YXZ":this._x=S*v*g+p*M*A,this._y=p*M*g-S*v*A,this._z=p*v*A-S*M*g,this._w=p*v*g+S*M*A;break;case"ZXY":this._x=S*v*g-p*M*A,this._y=p*M*g+S*v*A,this._z=p*v*A+S*M*g,this._w=p*v*g-S*M*A;break;case"ZYX":this._x=S*v*g-p*M*A,this._y=p*M*g+S*v*A,this._z=p*v*A-S*M*g,this._w=p*v*g+S*M*A;break;case"YZX":this._x=S*v*g+p*M*A,this._y=p*M*g+S*v*A,this._z=p*v*A-S*M*g,this._w=p*v*g-S*M*A;break;case"XZY":this._x=S*v*g-p*M*A,this._y=p*M*g-S*v*A,this._z=p*v*A+S*M*g,this._w=p*v*g+S*M*A;break;default:ae("Quaternion: .setFromEuler() encountered an unknown order: "+h)}return i===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,i){const r=i/2,l=Math.sin(r);return this._x=e.x*l,this._y=e.y*l,this._z=e.z*l,this._w=Math.cos(r),this._onChangeCallback(),this}setFromRotationMatrix(e){const i=e.elements,r=i[0],l=i[4],c=i[8],h=i[1],d=i[5],m=i[9],p=i[2],v=i[6],g=i[10],S=r+d+g;if(S>0){const M=.5/Math.sqrt(S+1);this._w=.25/M,this._x=(v-m)*M,this._y=(c-p)*M,this._z=(h-l)*M}else if(r>d&&r>g){const M=2*Math.sqrt(1+r-d-g);this._w=(v-m)/M,this._x=.25*M,this._y=(l+h)/M,this._z=(c+p)/M}else if(d>g){const M=2*Math.sqrt(1+d-r-g);this._w=(c-p)/M,this._x=(l+h)/M,this._y=.25*M,this._z=(m+v)/M}else{const M=2*Math.sqrt(1+g-r-d);this._w=(h-l)/M,this._x=(c+p)/M,this._y=(m+v)/M,this._z=.25*M}return this._onChangeCallback(),this}setFromUnitVectors(e,i){let r=e.dot(i)+1;return r<1e-8?(r=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=r):(this._x=0,this._y=-e.z,this._z=e.y,this._w=r)):(this._x=e.y*i.z-e.z*i.y,this._y=e.z*i.x-e.x*i.z,this._z=e.x*i.y-e.y*i.x,this._w=r),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(xe(this.dot(e),-1,1)))}rotateTowards(e,i){const r=this.angleTo(e);if(r===0)return this;const l=Math.min(1,i/r);return this.slerp(e,l),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,i){const r=e._x,l=e._y,c=e._z,h=e._w,d=i._x,m=i._y,p=i._z,v=i._w;return this._x=r*v+h*d+l*p-c*m,this._y=l*v+h*m+c*d-r*p,this._z=c*v+h*p+r*m-l*d,this._w=h*v-r*d-l*m-c*p,this._onChangeCallback(),this}slerp(e,i){if(i<=0)return this;if(i>=1)return this.copy(e);let r=e._x,l=e._y,c=e._z,h=e._w,d=this.dot(e);d<0&&(r=-r,l=-l,c=-c,h=-h,d=-d);let m=1-i;if(d<.9995){const p=Math.acos(d),v=Math.sin(p);m=Math.sin(m*p)/v,i=Math.sin(i*p)/v,this._x=this._x*m+r*i,this._y=this._y*m+l*i,this._z=this._z*m+c*i,this._w=this._w*m+h*i,this._onChangeCallback()}else this._x=this._x*m+r*i,this._y=this._y*m+l*i,this._z=this._z*m+c*i,this._w=this._w*m+h*i,this.normalize();return this}slerpQuaternions(e,i,r){return this.copy(e).slerp(i,r)}random(){const e=2*Math.PI*Math.random(),i=2*Math.PI*Math.random(),r=Math.random(),l=Math.sqrt(1-r),c=Math.sqrt(r);return this.set(l*Math.sin(e),l*Math.cos(e),c*Math.sin(i),c*Math.cos(i))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,i=0){return this._x=e[i],this._y=e[i+1],this._z=e[i+2],this._w=e[i+3],this._onChangeCallback(),this}toArray(e=[],i=0){return e[i]=this._x,e[i+1]=this._y,e[i+2]=this._z,e[i+3]=this._w,e}fromBufferAttribute(e,i){return this._x=e.getX(i),this._y=e.getY(i),this._z=e.getZ(i),this._w=e.getW(i),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class it{constructor(e=0,i=0,r=0){it.prototype.isVector3=!0,this.x=e,this.y=i,this.z=r}set(e,i,r){return r===void 0&&(r=this.z),this.x=e,this.y=i,this.z=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;case 2:this.z=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this.z=e.z+i.z,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this.z+=e.z*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this.z=e.z-i.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,i){return this.x=e.x*i.x,this.y=e.y*i.y,this.z=e.z*i.z,this}applyEuler(e){return this.applyQuaternion(B0.setFromEuler(e))}applyAxisAngle(e,i){return this.applyQuaternion(B0.setFromAxisAngle(e,i))}applyMatrix3(e){const i=this.x,r=this.y,l=this.z,c=e.elements;return this.x=c[0]*i+c[3]*r+c[6]*l,this.y=c[1]*i+c[4]*r+c[7]*l,this.z=c[2]*i+c[5]*r+c[8]*l,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const i=this.x,r=this.y,l=this.z,c=e.elements,h=1/(c[3]*i+c[7]*r+c[11]*l+c[15]);return this.x=(c[0]*i+c[4]*r+c[8]*l+c[12])*h,this.y=(c[1]*i+c[5]*r+c[9]*l+c[13])*h,this.z=(c[2]*i+c[6]*r+c[10]*l+c[14])*h,this}applyQuaternion(e){const i=this.x,r=this.y,l=this.z,c=e.x,h=e.y,d=e.z,m=e.w,p=2*(h*l-d*r),v=2*(d*i-c*l),g=2*(c*r-h*i);return this.x=i+m*p+h*g-d*v,this.y=r+m*v+d*p-c*g,this.z=l+m*g+c*v-h*p,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const i=this.x,r=this.y,l=this.z,c=e.elements;return this.x=c[0]*i+c[4]*r+c[8]*l,this.y=c[1]*i+c[5]*r+c[9]*l,this.z=c[2]*i+c[6]*r+c[10]*l,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,i){return this.x=xe(this.x,e.x,i.x),this.y=xe(this.y,e.y,i.y),this.z=xe(this.z,e.z,i.z),this}clampScalar(e,i){return this.x=xe(this.x,e,i),this.y=xe(this.y,e,i),this.z=xe(this.z,e,i),this}clampLength(e,i){const r=this.length();return this.divideScalar(r||1).multiplyScalar(xe(r,e,i))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this.z+=(e.z-this.z)*i,this}lerpVectors(e,i,r){return this.x=e.x+(i.x-e.x)*r,this.y=e.y+(i.y-e.y)*r,this.z=e.z+(i.z-e.z)*r,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,i){const r=e.x,l=e.y,c=e.z,h=i.x,d=i.y,m=i.z;return this.x=l*m-c*d,this.y=c*h-r*m,this.z=r*d-l*h,this}projectOnVector(e){const i=e.lengthSq();if(i===0)return this.set(0,0,0);const r=e.dot(this)/i;return this.copy(e).multiplyScalar(r)}projectOnPlane(e){return Jf.copy(this).projectOnVector(e),this.sub(Jf)}reflect(e){return this.sub(Jf.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const i=Math.sqrt(this.lengthSq()*e.lengthSq());if(i===0)return Math.PI/2;const r=this.dot(e)/i;return Math.acos(xe(r,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const i=this.x-e.x,r=this.y-e.y,l=this.z-e.z;return i*i+r*r+l*l}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,i,r){const l=Math.sin(i)*e;return this.x=l*Math.sin(r),this.y=Math.cos(i)*e,this.z=l*Math.cos(r),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,i,r){return this.x=e*Math.sin(i),this.y=r,this.z=e*Math.cos(i),this}setFromMatrixPosition(e){const i=e.elements;return this.x=i[12],this.y=i[13],this.z=i[14],this}setFromMatrixScale(e){const i=this.setFromMatrixColumn(e,0).length(),r=this.setFromMatrixColumn(e,1).length(),l=this.setFromMatrixColumn(e,2).length();return this.x=i,this.y=r,this.z=l,this}setFromMatrixColumn(e,i){return this.fromArray(e.elements,i*4)}setFromMatrix3Column(e,i){return this.fromArray(e.elements,i*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this.z=e[i+2],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e[i+2]=this.z,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this.z=e.getZ(i),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=Math.random()*Math.PI*2,i=Math.random()*2-1,r=Math.sqrt(1-i*i);return this.x=r*Math.cos(e),this.y=i,this.z=r*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const Jf=new it,B0=new ko;class ue{constructor(e,i,r,l,c,h,d,m,p){ue.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,i,r,l,c,h,d,m,p)}set(e,i,r,l,c,h,d,m,p){const v=this.elements;return v[0]=e,v[1]=l,v[2]=d,v[3]=i,v[4]=c,v[5]=m,v[6]=r,v[7]=h,v[8]=p,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const i=this.elements,r=e.elements;return i[0]=r[0],i[1]=r[1],i[2]=r[2],i[3]=r[3],i[4]=r[4],i[5]=r[5],i[6]=r[6],i[7]=r[7],i[8]=r[8],this}extractBasis(e,i,r){return e.setFromMatrix3Column(this,0),i.setFromMatrix3Column(this,1),r.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const i=e.elements;return this.set(i[0],i[4],i[8],i[1],i[5],i[9],i[2],i[6],i[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,i){const r=e.elements,l=i.elements,c=this.elements,h=r[0],d=r[3],m=r[6],p=r[1],v=r[4],g=r[7],S=r[2],M=r[5],A=r[8],C=l[0],y=l[3],x=l[6],P=l[1],N=l[4],L=l[7],B=l[2],F=l[5],z=l[8];return c[0]=h*C+d*P+m*B,c[3]=h*y+d*N+m*F,c[6]=h*x+d*L+m*z,c[1]=p*C+v*P+g*B,c[4]=p*y+v*N+g*F,c[7]=p*x+v*L+g*z,c[2]=S*C+M*P+A*B,c[5]=S*y+M*N+A*F,c[8]=S*x+M*L+A*z,this}multiplyScalar(e){const i=this.elements;return i[0]*=e,i[3]*=e,i[6]*=e,i[1]*=e,i[4]*=e,i[7]*=e,i[2]*=e,i[5]*=e,i[8]*=e,this}determinant(){const e=this.elements,i=e[0],r=e[1],l=e[2],c=e[3],h=e[4],d=e[5],m=e[6],p=e[7],v=e[8];return i*h*v-i*d*p-r*c*v+r*d*m+l*c*p-l*h*m}invert(){const e=this.elements,i=e[0],r=e[1],l=e[2],c=e[3],h=e[4],d=e[5],m=e[6],p=e[7],v=e[8],g=v*h-d*p,S=d*m-v*c,M=p*c-h*m,A=i*g+r*S+l*M;if(A===0)return this.set(0,0,0,0,0,0,0,0,0);const C=1/A;return e[0]=g*C,e[1]=(l*p-v*r)*C,e[2]=(d*r-l*h)*C,e[3]=S*C,e[4]=(v*i-l*m)*C,e[5]=(l*c-d*i)*C,e[6]=M*C,e[7]=(r*m-p*i)*C,e[8]=(h*i-r*c)*C,this}transpose(){let e;const i=this.elements;return e=i[1],i[1]=i[3],i[3]=e,e=i[2],i[2]=i[6],i[6]=e,e=i[5],i[5]=i[7],i[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const i=this.elements;return e[0]=i[0],e[1]=i[3],e[2]=i[6],e[3]=i[1],e[4]=i[4],e[5]=i[7],e[6]=i[2],e[7]=i[5],e[8]=i[8],this}setUvTransform(e,i,r,l,c,h,d){const m=Math.cos(c),p=Math.sin(c);return this.set(r*m,r*p,-r*(m*h+p*d)+h+e,-l*p,l*m,-l*(-p*h+m*d)+d+i,0,0,1),this}scale(e,i){return this.premultiply($f.makeScale(e,i)),this}rotate(e){return this.premultiply($f.makeRotation(-e)),this}translate(e,i){return this.premultiply($f.makeTranslation(e,i)),this}makeTranslation(e,i){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,i,0,0,1),this}makeRotation(e){const i=Math.cos(e),r=Math.sin(e);return this.set(i,-r,0,r,i,0,0,0,1),this}makeScale(e,i){return this.set(e,0,0,0,i,0,0,0,1),this}equals(e){const i=this.elements,r=e.elements;for(let l=0;l<9;l++)if(i[l]!==r[l])return!1;return!0}fromArray(e,i=0){for(let r=0;r<9;r++)this.elements[r]=e[r+i];return this}toArray(e=[],i=0){const r=this.elements;return e[i]=r[0],e[i+1]=r[1],e[i+2]=r[2],e[i+3]=r[3],e[i+4]=r[4],e[i+5]=r[5],e[i+6]=r[6],e[i+7]=r[7],e[i+8]=r[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const $f=new ue,I0=new ue().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),H0=new ue().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function pM(){const o={enabled:!0,workingColorSpace:Ds,spaces:{},convert:function(l,c,h){return this.enabled===!1||c===h||!c||!h||(this.spaces[c].transfer===Be&&(l.r=da(l.r),l.g=da(l.g),l.b=da(l.b)),this.spaces[c].primaries!==this.spaces[h].primaries&&(l.applyMatrix3(this.spaces[c].toXYZ),l.applyMatrix3(this.spaces[h].fromXYZ)),this.spaces[h].transfer===Be&&(l.r=bs(l.r),l.g=bs(l.g),l.b=bs(l.b))),l},workingToColorSpace:function(l,c){return this.convert(l,this.workingColorSpace,c)},colorSpaceToWorking:function(l,c){return this.convert(l,c,this.workingColorSpace)},getPrimaries:function(l){return this.spaces[l].primaries},getTransfer:function(l){return l===ja?Lu:this.spaces[l].transfer},getToneMappingMode:function(l){return this.spaces[l].outputColorSpaceConfig.toneMappingMode||"standard"},getLuminanceCoefficients:function(l,c=this.workingColorSpace){return l.fromArray(this.spaces[c].luminanceCoefficients)},define:function(l){Object.assign(this.spaces,l)},_getMatrix:function(l,c,h){return l.copy(this.spaces[c].toXYZ).multiply(this.spaces[h].fromXYZ)},_getDrawingBufferColorSpace:function(l){return this.spaces[l].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(l=this.workingColorSpace){return this.spaces[l].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(l,c){return Ho("ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),o.workingToColorSpace(l,c)},toWorkingColorSpace:function(l,c){return Ho("ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),o.colorSpaceToWorking(l,c)}},e=[.64,.33,.3,.6,.15,.06],i=[.2126,.7152,.0722],r=[.3127,.329];return o.define({[Ds]:{primaries:e,whitePoint:r,transfer:Lu,toXYZ:I0,fromXYZ:H0,luminanceCoefficients:i,workingColorSpaceConfig:{unpackColorSpace:fi},outputColorSpaceConfig:{drawingBufferColorSpace:fi}},[fi]:{primaries:e,whitePoint:r,transfer:Be,toXYZ:I0,fromXYZ:H0,luminanceCoefficients:i,outputColorSpaceConfig:{drawingBufferColorSpace:fi}}}),o}const ye=pM();function da(o){return o<.04045?o*.0773993808:Math.pow(o*.9478672986+.0521327014,2.4)}function bs(o){return o<.0031308?o*12.92:1.055*Math.pow(o,.41666)-.055}let fs;class mM{static getDataURL(e,i="image/png"){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let r;if(e instanceof HTMLCanvasElement)r=e;else{fs===void 0&&(fs=Ou("canvas")),fs.width=e.width,fs.height=e.height;const l=fs.getContext("2d");e instanceof ImageData?l.putImageData(e,0,0):l.drawImage(e,0,0,e.width,e.height),r=fs}return r.toDataURL(i)}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const i=Ou("canvas");i.width=e.width,i.height=e.height;const r=i.getContext("2d");r.drawImage(e,0,0,e.width,e.height);const l=r.getImageData(0,0,e.width,e.height),c=l.data;for(let h=0;h<c.length;h++)c[h]=da(c[h]/255)*255;return r.putImageData(l,0,0),i}else if(e.data){const i=e.data.slice(0);for(let r=0;r<i.length;r++)i instanceof Uint8Array||i instanceof Uint8ClampedArray?i[r]=Math.floor(da(i[r]/255)*255):i[r]=da(i[r]);return{data:i,width:e.width,height:e.height}}else return ae("ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let gM=0;class Od{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:gM++}),this.uuid=Xo(),this.data=e,this.dataReady=!0,this.version=0}getSize(e){const i=this.data;return typeof HTMLVideoElement<"u"&&i instanceof HTMLVideoElement?e.set(i.videoWidth,i.videoHeight,0):typeof VideoFrame<"u"&&i instanceof VideoFrame?e.set(i.displayHeight,i.displayWidth,0):i!==null?e.set(i.width,i.height,i.depth||0):e.set(0,0,0),e}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const i=e===void 0||typeof e=="string";if(!i&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const r={uuid:this.uuid,url:""},l=this.data;if(l!==null){let c;if(Array.isArray(l)){c=[];for(let h=0,d=l.length;h<d;h++)l[h].isDataTexture?c.push(th(l[h].image)):c.push(th(l[h]))}else c=th(l);r.url=c}return i||(e.images[this.uuid]=r),r}}function th(o){return typeof HTMLImageElement<"u"&&o instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&o instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&o instanceof ImageBitmap?mM.getDataURL(o):o.data?{data:Array.from(o.data),width:o.width,height:o.height,type:o.data.constructor.name}:(ae("Texture: Unable to serialize Texture."),{})}let _M=0;const eh=new it;class Pn extends Us{constructor(e=Pn.DEFAULT_IMAGE,i=Pn.DEFAULT_MAPPING,r=fa,l=fa,c=Un,h=br,d=Ti,m=$n,p=Pn.DEFAULT_ANISOTROPY,v=ja){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:_M++}),this.uuid=Xo(),this.name="",this.source=new Od(e),this.mipmaps=[],this.mapping=i,this.channel=0,this.wrapS=r,this.wrapT=l,this.magFilter=c,this.minFilter=h,this.anisotropy=p,this.format=d,this.internalFormat=null,this.type=m,this.offset=new Ue(0,0),this.repeat=new Ue(1,1),this.center=new Ue(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new ue,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=v,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(e&&e.depth&&e.depth>1),this.pmremVersion=0}get width(){return this.source.getSize(eh).x}get height(){return this.source.getSize(eh).y}get depth(){return this.source.getSize(eh).z}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(e,i){this.updateRanges.push({start:e,count:i})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.isArrayTexture=e.isArrayTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}setValues(e){for(const i in e){const r=e[i];if(r===void 0){ae(`Texture.setValues(): parameter '${i}' has value of undefined.`);continue}const l=this[i];if(l===void 0){ae(`Texture.setValues(): property '${i}' does not exist.`);continue}l&&r&&l.isVector2&&r.isVector2||l&&r&&l.isVector3&&r.isVector3||l&&r&&l.isMatrix3&&r.isMatrix3?l.copy(r):this[i]=r}}toJSON(e){const i=e===void 0||typeof e=="string";if(!i&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const r={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(r.userData=this.userData),i||(e.textures[this.uuid]=r),r}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==I_)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Vh:e.x=e.x-Math.floor(e.x);break;case fa:e.x=e.x<0?0:1;break;case Xh:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Vh:e.y=e.y-Math.floor(e.y);break;case fa:e.y=e.y<0?0:1;break;case Xh:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}}Pn.DEFAULT_IMAGE=null;Pn.DEFAULT_MAPPING=I_;Pn.DEFAULT_ANISOTROPY=1;class $e{constructor(e=0,i=0,r=0,l=1){$e.prototype.isVector4=!0,this.x=e,this.y=i,this.z=r,this.w=l}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,i,r,l){return this.x=e,this.y=i,this.z=r,this.w=l,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;case 2:this.z=i;break;case 3:this.w=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this.z=e.z+i.z,this.w=e.w+i.w,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this.z+=e.z*i,this.w+=e.w*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this.z=e.z-i.z,this.w=e.w-i.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const i=this.x,r=this.y,l=this.z,c=this.w,h=e.elements;return this.x=h[0]*i+h[4]*r+h[8]*l+h[12]*c,this.y=h[1]*i+h[5]*r+h[9]*l+h[13]*c,this.z=h[2]*i+h[6]*r+h[10]*l+h[14]*c,this.w=h[3]*i+h[7]*r+h[11]*l+h[15]*c,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const i=Math.sqrt(1-e.w*e.w);return i<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/i,this.y=e.y/i,this.z=e.z/i),this}setAxisAngleFromRotationMatrix(e){let i,r,l,c;const m=e.elements,p=m[0],v=m[4],g=m[8],S=m[1],M=m[5],A=m[9],C=m[2],y=m[6],x=m[10];if(Math.abs(v-S)<.01&&Math.abs(g-C)<.01&&Math.abs(A-y)<.01){if(Math.abs(v+S)<.1&&Math.abs(g+C)<.1&&Math.abs(A+y)<.1&&Math.abs(p+M+x-3)<.1)return this.set(1,0,0,0),this;i=Math.PI;const N=(p+1)/2,L=(M+1)/2,B=(x+1)/2,F=(v+S)/4,z=(g+C)/4,Q=(A+y)/4;return N>L&&N>B?N<.01?(r=0,l=.707106781,c=.707106781):(r=Math.sqrt(N),l=F/r,c=z/r):L>B?L<.01?(r=.707106781,l=0,c=.707106781):(l=Math.sqrt(L),r=F/l,c=Q/l):B<.01?(r=.707106781,l=.707106781,c=0):(c=Math.sqrt(B),r=z/c,l=Q/c),this.set(r,l,c,i),this}let P=Math.sqrt((y-A)*(y-A)+(g-C)*(g-C)+(S-v)*(S-v));return Math.abs(P)<.001&&(P=1),this.x=(y-A)/P,this.y=(g-C)/P,this.z=(S-v)/P,this.w=Math.acos((p+M+x-1)/2),this}setFromMatrixPosition(e){const i=e.elements;return this.x=i[12],this.y=i[13],this.z=i[14],this.w=i[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,i){return this.x=xe(this.x,e.x,i.x),this.y=xe(this.y,e.y,i.y),this.z=xe(this.z,e.z,i.z),this.w=xe(this.w,e.w,i.w),this}clampScalar(e,i){return this.x=xe(this.x,e,i),this.y=xe(this.y,e,i),this.z=xe(this.z,e,i),this.w=xe(this.w,e,i),this}clampLength(e,i){const r=this.length();return this.divideScalar(r||1).multiplyScalar(xe(r,e,i))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this.z+=(e.z-this.z)*i,this.w+=(e.w-this.w)*i,this}lerpVectors(e,i,r){return this.x=e.x+(i.x-e.x)*r,this.y=e.y+(i.y-e.y)*r,this.z=e.z+(i.z-e.z)*r,this.w=e.w+(i.w-e.w)*r,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this.z=e[i+2],this.w=e[i+3],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e[i+2]=this.z,e[i+3]=this.w,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this.z=e.getZ(i),this.w=e.getW(i),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class vM extends Us{constructor(e=1,i=1,r={}){super(),r=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:Un,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1,depth:1,multiview:!1},r),this.isRenderTarget=!0,this.width=e,this.height=i,this.depth=r.depth,this.scissor=new $e(0,0,e,i),this.scissorTest=!1,this.viewport=new $e(0,0,e,i);const l={width:e,height:i,depth:r.depth},c=new Pn(l);this.textures=[];const h=r.count;for(let d=0;d<h;d++)this.textures[d]=c.clone(),this.textures[d].isRenderTargetTexture=!0,this.textures[d].renderTarget=this;this._setTextureOptions(r),this.depthBuffer=r.depthBuffer,this.stencilBuffer=r.stencilBuffer,this.resolveDepthBuffer=r.resolveDepthBuffer,this.resolveStencilBuffer=r.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=r.depthTexture,this.samples=r.samples,this.multiview=r.multiview}_setTextureOptions(e={}){const i={minFilter:Un,generateMipmaps:!1,flipY:!1,internalFormat:null};e.mapping!==void 0&&(i.mapping=e.mapping),e.wrapS!==void 0&&(i.wrapS=e.wrapS),e.wrapT!==void 0&&(i.wrapT=e.wrapT),e.wrapR!==void 0&&(i.wrapR=e.wrapR),e.magFilter!==void 0&&(i.magFilter=e.magFilter),e.minFilter!==void 0&&(i.minFilter=e.minFilter),e.format!==void 0&&(i.format=e.format),e.type!==void 0&&(i.type=e.type),e.anisotropy!==void 0&&(i.anisotropy=e.anisotropy),e.colorSpace!==void 0&&(i.colorSpace=e.colorSpace),e.flipY!==void 0&&(i.flipY=e.flipY),e.generateMipmaps!==void 0&&(i.generateMipmaps=e.generateMipmaps),e.internalFormat!==void 0&&(i.internalFormat=e.internalFormat);for(let r=0;r<this.textures.length;r++)this.textures[r].setValues(i)}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),e!==null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,i,r=1){if(this.width!==e||this.height!==i||this.depth!==r){this.width=e,this.height=i,this.depth=r;for(let l=0,c=this.textures.length;l<c;l++)this.textures[l].image.width=e,this.textures[l].image.height=i,this.textures[l].image.depth=r,this.textures[l].isData3DTexture!==!0&&(this.textures[l].isArrayTexture=this.textures[l].image.depth>1);this.dispose()}this.viewport.set(0,0,e,i),this.scissor.set(0,0,e,i)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let i=0,r=e.textures.length;i<r;i++){this.textures[i]=e.textures[i].clone(),this.textures[i].isRenderTargetTexture=!0,this.textures[i].renderTarget=this;const l=Object.assign({},e.textures[i].image);this.textures[i].source=new Od(l)}return this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class Pi extends vM{constructor(e=1,i=1,r={}){super(e,i,r),this.isWebGLRenderTarget=!0}}class j_ extends Pn{constructor(e=null,i=1,r=1,l=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:i,height:r,depth:l},this.magFilter=An,this.minFilter=An,this.wrapR=fa,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}}class xM extends Pn{constructor(e=null,i=1,r=1,l=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:i,height:r,depth:l},this.magFilter=An,this.minFilter=An,this.wrapR=fa,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Wo{constructor(e=new it(1/0,1/0,1/0),i=new it(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=i}set(e,i){return this.min.copy(e),this.max.copy(i),this}setFromArray(e){this.makeEmpty();for(let i=0,r=e.length;i<r;i+=3)this.expandByPoint(xi.fromArray(e,i));return this}setFromBufferAttribute(e){this.makeEmpty();for(let i=0,r=e.count;i<r;i++)this.expandByPoint(xi.fromBufferAttribute(e,i));return this}setFromPoints(e){this.makeEmpty();for(let i=0,r=e.length;i<r;i++)this.expandByPoint(e[i]);return this}setFromCenterAndSize(e,i){const r=xi.copy(i).multiplyScalar(.5);return this.min.copy(e).sub(r),this.max.copy(e).add(r),this}setFromObject(e,i=!1){return this.makeEmpty(),this.expandByObject(e,i)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,i=!1){e.updateWorldMatrix(!1,!1);const r=e.geometry;if(r!==void 0){const c=r.getAttribute("position");if(i===!0&&c!==void 0&&e.isInstancedMesh!==!0)for(let h=0,d=c.count;h<d;h++)e.isMesh===!0?e.getVertexPosition(h,xi):xi.fromBufferAttribute(c,h),xi.applyMatrix4(e.matrixWorld),this.expandByPoint(xi);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),su.copy(e.boundingBox)):(r.boundingBox===null&&r.computeBoundingBox(),su.copy(r.boundingBox)),su.applyMatrix4(e.matrixWorld),this.union(su)}const l=e.children;for(let c=0,h=l.length;c<h;c++)this.expandByObject(l[c],i);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,i){return i.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,xi),xi.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let i,r;return e.normal.x>0?(i=e.normal.x*this.min.x,r=e.normal.x*this.max.x):(i=e.normal.x*this.max.x,r=e.normal.x*this.min.x),e.normal.y>0?(i+=e.normal.y*this.min.y,r+=e.normal.y*this.max.y):(i+=e.normal.y*this.max.y,r+=e.normal.y*this.min.y),e.normal.z>0?(i+=e.normal.z*this.min.z,r+=e.normal.z*this.max.z):(i+=e.normal.z*this.max.z,r+=e.normal.z*this.min.z),i<=-e.constant&&r>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(Do),ou.subVectors(this.max,Do),hs.subVectors(e.a,Do),ds.subVectors(e.b,Do),ps.subVectors(e.c,Do),Xa.subVectors(ds,hs),ka.subVectors(ps,ds),gr.subVectors(hs,ps);let i=[0,-Xa.z,Xa.y,0,-ka.z,ka.y,0,-gr.z,gr.y,Xa.z,0,-Xa.x,ka.z,0,-ka.x,gr.z,0,-gr.x,-Xa.y,Xa.x,0,-ka.y,ka.x,0,-gr.y,gr.x,0];return!nh(i,hs,ds,ps,ou)||(i=[1,0,0,0,1,0,0,0,1],!nh(i,hs,ds,ps,ou))?!1:(lu.crossVectors(Xa,ka),i=[lu.x,lu.y,lu.z],nh(i,hs,ds,ps,ou))}clampPoint(e,i){return i.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,xi).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(xi).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(ra[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),ra[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),ra[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),ra[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),ra[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),ra[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),ra[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),ra[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(ra),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(e){return this.min.fromArray(e.min),this.max.fromArray(e.max),this}}const ra=[new it,new it,new it,new it,new it,new it,new it,new it],xi=new it,su=new Wo,hs=new it,ds=new it,ps=new it,Xa=new it,ka=new it,gr=new it,Do=new it,ou=new it,lu=new it,_r=new it;function nh(o,e,i,r,l){for(let c=0,h=o.length-3;c<=h;c+=3){_r.fromArray(o,c);const d=l.x*Math.abs(_r.x)+l.y*Math.abs(_r.y)+l.z*Math.abs(_r.z),m=e.dot(_r),p=i.dot(_r),v=r.dot(_r);if(Math.max(-Math.max(m,p,v),Math.min(m,p,v))>d)return!1}return!0}const SM=new Wo,wo=new it,ih=new it;class Pd{constructor(e=new it,i=-1){this.isSphere=!0,this.center=e,this.radius=i}set(e,i){return this.center.copy(e),this.radius=i,this}setFromPoints(e,i){const r=this.center;i!==void 0?r.copy(i):SM.setFromPoints(e).getCenter(r);let l=0;for(let c=0,h=e.length;c<h;c++)l=Math.max(l,r.distanceToSquared(e[c]));return this.radius=Math.sqrt(l),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const i=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=i*i}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,i){const r=this.center.distanceToSquared(e);return i.copy(e),r>this.radius*this.radius&&(i.sub(this.center).normalize(),i.multiplyScalar(this.radius).add(this.center)),i}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;wo.subVectors(e,this.center);const i=wo.lengthSq();if(i>this.radius*this.radius){const r=Math.sqrt(i),l=(r-this.radius)*.5;this.center.addScaledVector(wo,l/r),this.radius+=l}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(ih.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(wo.copy(e.center).add(ih)),this.expandByPoint(wo.copy(e.center).sub(ih))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(e){return this.radius=e.radius,this.center.fromArray(e.center),this}}const sa=new it,ah=new it,uu=new it,Wa=new it,rh=new it,cu=new it,sh=new it;class MM{constructor(e=new it,i=new it(0,0,-1)){this.origin=e,this.direction=i}set(e,i){return this.origin.copy(e),this.direction.copy(i),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,i){return i.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,sa)),this}closestPointToPoint(e,i){i.subVectors(e,this.origin);const r=i.dot(this.direction);return r<0?i.copy(this.origin):i.copy(this.origin).addScaledVector(this.direction,r)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const i=sa.subVectors(e,this.origin).dot(this.direction);return i<0?this.origin.distanceToSquared(e):(sa.copy(this.origin).addScaledVector(this.direction,i),sa.distanceToSquared(e))}distanceSqToSegment(e,i,r,l){ah.copy(e).add(i).multiplyScalar(.5),uu.copy(i).sub(e).normalize(),Wa.copy(this.origin).sub(ah);const c=e.distanceTo(i)*.5,h=-this.direction.dot(uu),d=Wa.dot(this.direction),m=-Wa.dot(uu),p=Wa.lengthSq(),v=Math.abs(1-h*h);let g,S,M,A;if(v>0)if(g=h*m-d,S=h*d-m,A=c*v,g>=0)if(S>=-A)if(S<=A){const C=1/v;g*=C,S*=C,M=g*(g+h*S+2*d)+S*(h*g+S+2*m)+p}else S=c,g=Math.max(0,-(h*S+d)),M=-g*g+S*(S+2*m)+p;else S=-c,g=Math.max(0,-(h*S+d)),M=-g*g+S*(S+2*m)+p;else S<=-A?(g=Math.max(0,-(-h*c+d)),S=g>0?-c:Math.min(Math.max(-c,-m),c),M=-g*g+S*(S+2*m)+p):S<=A?(g=0,S=Math.min(Math.max(-c,-m),c),M=S*(S+2*m)+p):(g=Math.max(0,-(h*c+d)),S=g>0?c:Math.min(Math.max(-c,-m),c),M=-g*g+S*(S+2*m)+p);else S=h>0?-c:c,g=Math.max(0,-(h*S+d)),M=-g*g+S*(S+2*m)+p;return r&&r.copy(this.origin).addScaledVector(this.direction,g),l&&l.copy(ah).addScaledVector(uu,S),M}intersectSphere(e,i){sa.subVectors(e.center,this.origin);const r=sa.dot(this.direction),l=sa.dot(sa)-r*r,c=e.radius*e.radius;if(l>c)return null;const h=Math.sqrt(c-l),d=r-h,m=r+h;return m<0?null:d<0?this.at(m,i):this.at(d,i)}intersectsSphere(e){return e.radius<0?!1:this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const i=e.normal.dot(this.direction);if(i===0)return e.distanceToPoint(this.origin)===0?0:null;const r=-(this.origin.dot(e.normal)+e.constant)/i;return r>=0?r:null}intersectPlane(e,i){const r=this.distanceToPlane(e);return r===null?null:this.at(r,i)}intersectsPlane(e){const i=e.distanceToPoint(this.origin);return i===0||e.normal.dot(this.direction)*i<0}intersectBox(e,i){let r,l,c,h,d,m;const p=1/this.direction.x,v=1/this.direction.y,g=1/this.direction.z,S=this.origin;return p>=0?(r=(e.min.x-S.x)*p,l=(e.max.x-S.x)*p):(r=(e.max.x-S.x)*p,l=(e.min.x-S.x)*p),v>=0?(c=(e.min.y-S.y)*v,h=(e.max.y-S.y)*v):(c=(e.max.y-S.y)*v,h=(e.min.y-S.y)*v),r>h||c>l||((c>r||isNaN(r))&&(r=c),(h<l||isNaN(l))&&(l=h),g>=0?(d=(e.min.z-S.z)*g,m=(e.max.z-S.z)*g):(d=(e.max.z-S.z)*g,m=(e.min.z-S.z)*g),r>m||d>l)||((d>r||r!==r)&&(r=d),(m<l||l!==l)&&(l=m),l<0)?null:this.at(r>=0?r:l,i)}intersectsBox(e){return this.intersectBox(e,sa)!==null}intersectTriangle(e,i,r,l,c){rh.subVectors(i,e),cu.subVectors(r,e),sh.crossVectors(rh,cu);let h=this.direction.dot(sh),d;if(h>0){if(l)return null;d=1}else if(h<0)d=-1,h=-h;else return null;Wa.subVectors(this.origin,e);const m=d*this.direction.dot(cu.crossVectors(Wa,cu));if(m<0)return null;const p=d*this.direction.dot(rh.cross(Wa));if(p<0||m+p>h)return null;const v=-d*Wa.dot(sh);return v<0?null:this.at(v/h,c)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class tn{constructor(e,i,r,l,c,h,d,m,p,v,g,S,M,A,C,y){tn.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,i,r,l,c,h,d,m,p,v,g,S,M,A,C,y)}set(e,i,r,l,c,h,d,m,p,v,g,S,M,A,C,y){const x=this.elements;return x[0]=e,x[4]=i,x[8]=r,x[12]=l,x[1]=c,x[5]=h,x[9]=d,x[13]=m,x[2]=p,x[6]=v,x[10]=g,x[14]=S,x[3]=M,x[7]=A,x[11]=C,x[15]=y,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new tn().fromArray(this.elements)}copy(e){const i=this.elements,r=e.elements;return i[0]=r[0],i[1]=r[1],i[2]=r[2],i[3]=r[3],i[4]=r[4],i[5]=r[5],i[6]=r[6],i[7]=r[7],i[8]=r[8],i[9]=r[9],i[10]=r[10],i[11]=r[11],i[12]=r[12],i[13]=r[13],i[14]=r[14],i[15]=r[15],this}copyPosition(e){const i=this.elements,r=e.elements;return i[12]=r[12],i[13]=r[13],i[14]=r[14],this}setFromMatrix3(e){const i=e.elements;return this.set(i[0],i[3],i[6],0,i[1],i[4],i[7],0,i[2],i[5],i[8],0,0,0,0,1),this}extractBasis(e,i,r){return this.determinant()===0?(e.set(1,0,0),i.set(0,1,0),r.set(0,0,1),this):(e.setFromMatrixColumn(this,0),i.setFromMatrixColumn(this,1),r.setFromMatrixColumn(this,2),this)}makeBasis(e,i,r){return this.set(e.x,i.x,r.x,0,e.y,i.y,r.y,0,e.z,i.z,r.z,0,0,0,0,1),this}extractRotation(e){if(e.determinant()===0)return this.identity();const i=this.elements,r=e.elements,l=1/ms.setFromMatrixColumn(e,0).length(),c=1/ms.setFromMatrixColumn(e,1).length(),h=1/ms.setFromMatrixColumn(e,2).length();return i[0]=r[0]*l,i[1]=r[1]*l,i[2]=r[2]*l,i[3]=0,i[4]=r[4]*c,i[5]=r[5]*c,i[6]=r[6]*c,i[7]=0,i[8]=r[8]*h,i[9]=r[9]*h,i[10]=r[10]*h,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,this}makeRotationFromEuler(e){const i=this.elements,r=e.x,l=e.y,c=e.z,h=Math.cos(r),d=Math.sin(r),m=Math.cos(l),p=Math.sin(l),v=Math.cos(c),g=Math.sin(c);if(e.order==="XYZ"){const S=h*v,M=h*g,A=d*v,C=d*g;i[0]=m*v,i[4]=-m*g,i[8]=p,i[1]=M+A*p,i[5]=S-C*p,i[9]=-d*m,i[2]=C-S*p,i[6]=A+M*p,i[10]=h*m}else if(e.order==="YXZ"){const S=m*v,M=m*g,A=p*v,C=p*g;i[0]=S+C*d,i[4]=A*d-M,i[8]=h*p,i[1]=h*g,i[5]=h*v,i[9]=-d,i[2]=M*d-A,i[6]=C+S*d,i[10]=h*m}else if(e.order==="ZXY"){const S=m*v,M=m*g,A=p*v,C=p*g;i[0]=S-C*d,i[4]=-h*g,i[8]=A+M*d,i[1]=M+A*d,i[5]=h*v,i[9]=C-S*d,i[2]=-h*p,i[6]=d,i[10]=h*m}else if(e.order==="ZYX"){const S=h*v,M=h*g,A=d*v,C=d*g;i[0]=m*v,i[4]=A*p-M,i[8]=S*p+C,i[1]=m*g,i[5]=C*p+S,i[9]=M*p-A,i[2]=-p,i[6]=d*m,i[10]=h*m}else if(e.order==="YZX"){const S=h*m,M=h*p,A=d*m,C=d*p;i[0]=m*v,i[4]=C-S*g,i[8]=A*g+M,i[1]=g,i[5]=h*v,i[9]=-d*v,i[2]=-p*v,i[6]=M*g+A,i[10]=S-C*g}else if(e.order==="XZY"){const S=h*m,M=h*p,A=d*m,C=d*p;i[0]=m*v,i[4]=-g,i[8]=p*v,i[1]=S*g+C,i[5]=h*v,i[9]=M*g-A,i[2]=A*g-M,i[6]=d*v,i[10]=C*g+S}return i[3]=0,i[7]=0,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,this}makeRotationFromQuaternion(e){return this.compose(yM,e,EM)}lookAt(e,i,r){const l=this.elements;return Qn.subVectors(e,i),Qn.lengthSq()===0&&(Qn.z=1),Qn.normalize(),qa.crossVectors(r,Qn),qa.lengthSq()===0&&(Math.abs(r.z)===1?Qn.x+=1e-4:Qn.z+=1e-4,Qn.normalize(),qa.crossVectors(r,Qn)),qa.normalize(),fu.crossVectors(Qn,qa),l[0]=qa.x,l[4]=fu.x,l[8]=Qn.x,l[1]=qa.y,l[5]=fu.y,l[9]=Qn.y,l[2]=qa.z,l[6]=fu.z,l[10]=Qn.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,i){const r=e.elements,l=i.elements,c=this.elements,h=r[0],d=r[4],m=r[8],p=r[12],v=r[1],g=r[5],S=r[9],M=r[13],A=r[2],C=r[6],y=r[10],x=r[14],P=r[3],N=r[7],L=r[11],B=r[15],F=l[0],z=l[4],Q=l[8],R=l[12],D=l[1],k=l[5],rt=l[9],at=l[13],ut=l[2],ht=l[6],O=l[10],V=l[14],nt=l[3],Mt=l[7],xt=l[11],U=l[15];return c[0]=h*F+d*D+m*ut+p*nt,c[4]=h*z+d*k+m*ht+p*Mt,c[8]=h*Q+d*rt+m*O+p*xt,c[12]=h*R+d*at+m*V+p*U,c[1]=v*F+g*D+S*ut+M*nt,c[5]=v*z+g*k+S*ht+M*Mt,c[9]=v*Q+g*rt+S*O+M*xt,c[13]=v*R+g*at+S*V+M*U,c[2]=A*F+C*D+y*ut+x*nt,c[6]=A*z+C*k+y*ht+x*Mt,c[10]=A*Q+C*rt+y*O+x*xt,c[14]=A*R+C*at+y*V+x*U,c[3]=P*F+N*D+L*ut+B*nt,c[7]=P*z+N*k+L*ht+B*Mt,c[11]=P*Q+N*rt+L*O+B*xt,c[15]=P*R+N*at+L*V+B*U,this}multiplyScalar(e){const i=this.elements;return i[0]*=e,i[4]*=e,i[8]*=e,i[12]*=e,i[1]*=e,i[5]*=e,i[9]*=e,i[13]*=e,i[2]*=e,i[6]*=e,i[10]*=e,i[14]*=e,i[3]*=e,i[7]*=e,i[11]*=e,i[15]*=e,this}determinant(){const e=this.elements,i=e[0],r=e[4],l=e[8],c=e[12],h=e[1],d=e[5],m=e[9],p=e[13],v=e[2],g=e[6],S=e[10],M=e[14],A=e[3],C=e[7],y=e[11],x=e[15],P=m*M-p*S,N=d*M-p*g,L=d*S-m*g,B=h*M-p*v,F=h*S-m*v,z=h*g-d*v;return i*(C*P-y*N+x*L)-r*(A*P-y*B+x*F)+l*(A*N-C*B+x*z)-c*(A*L-C*F+y*z)}transpose(){const e=this.elements;let i;return i=e[1],e[1]=e[4],e[4]=i,i=e[2],e[2]=e[8],e[8]=i,i=e[6],e[6]=e[9],e[9]=i,i=e[3],e[3]=e[12],e[12]=i,i=e[7],e[7]=e[13],e[13]=i,i=e[11],e[11]=e[14],e[14]=i,this}setPosition(e,i,r){const l=this.elements;return e.isVector3?(l[12]=e.x,l[13]=e.y,l[14]=e.z):(l[12]=e,l[13]=i,l[14]=r),this}invert(){const e=this.elements,i=e[0],r=e[1],l=e[2],c=e[3],h=e[4],d=e[5],m=e[6],p=e[7],v=e[8],g=e[9],S=e[10],M=e[11],A=e[12],C=e[13],y=e[14],x=e[15],P=g*y*p-C*S*p+C*m*M-d*y*M-g*m*x+d*S*x,N=A*S*p-v*y*p-A*m*M+h*y*M+v*m*x-h*S*x,L=v*C*p-A*g*p+A*d*M-h*C*M-v*d*x+h*g*x,B=A*g*m-v*C*m-A*d*S+h*C*S+v*d*y-h*g*y,F=i*P+r*N+l*L+c*B;if(F===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const z=1/F;return e[0]=P*z,e[1]=(C*S*c-g*y*c-C*l*M+r*y*M+g*l*x-r*S*x)*z,e[2]=(d*y*c-C*m*c+C*l*p-r*y*p-d*l*x+r*m*x)*z,e[3]=(g*m*c-d*S*c-g*l*p+r*S*p+d*l*M-r*m*M)*z,e[4]=N*z,e[5]=(v*y*c-A*S*c+A*l*M-i*y*M-v*l*x+i*S*x)*z,e[6]=(A*m*c-h*y*c-A*l*p+i*y*p+h*l*x-i*m*x)*z,e[7]=(h*S*c-v*m*c+v*l*p-i*S*p-h*l*M+i*m*M)*z,e[8]=L*z,e[9]=(A*g*c-v*C*c-A*r*M+i*C*M+v*r*x-i*g*x)*z,e[10]=(h*C*c-A*d*c+A*r*p-i*C*p-h*r*x+i*d*x)*z,e[11]=(v*d*c-h*g*c-v*r*p+i*g*p+h*r*M-i*d*M)*z,e[12]=B*z,e[13]=(v*C*l-A*g*l+A*r*S-i*C*S-v*r*y+i*g*y)*z,e[14]=(A*d*l-h*C*l-A*r*m+i*C*m+h*r*y-i*d*y)*z,e[15]=(h*g*l-v*d*l+v*r*m-i*g*m-h*r*S+i*d*S)*z,this}scale(e){const i=this.elements,r=e.x,l=e.y,c=e.z;return i[0]*=r,i[4]*=l,i[8]*=c,i[1]*=r,i[5]*=l,i[9]*=c,i[2]*=r,i[6]*=l,i[10]*=c,i[3]*=r,i[7]*=l,i[11]*=c,this}getMaxScaleOnAxis(){const e=this.elements,i=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],r=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],l=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(i,r,l))}makeTranslation(e,i,r){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,i,0,0,1,r,0,0,0,1),this}makeRotationX(e){const i=Math.cos(e),r=Math.sin(e);return this.set(1,0,0,0,0,i,-r,0,0,r,i,0,0,0,0,1),this}makeRotationY(e){const i=Math.cos(e),r=Math.sin(e);return this.set(i,0,r,0,0,1,0,0,-r,0,i,0,0,0,0,1),this}makeRotationZ(e){const i=Math.cos(e),r=Math.sin(e);return this.set(i,-r,0,0,r,i,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,i){const r=Math.cos(i),l=Math.sin(i),c=1-r,h=e.x,d=e.y,m=e.z,p=c*h,v=c*d;return this.set(p*h+r,p*d-l*m,p*m+l*d,0,p*d+l*m,v*d+r,v*m-l*h,0,p*m-l*d,v*m+l*h,c*m*m+r,0,0,0,0,1),this}makeScale(e,i,r){return this.set(e,0,0,0,0,i,0,0,0,0,r,0,0,0,0,1),this}makeShear(e,i,r,l,c,h){return this.set(1,r,c,0,e,1,h,0,i,l,1,0,0,0,0,1),this}compose(e,i,r){const l=this.elements,c=i._x,h=i._y,d=i._z,m=i._w,p=c+c,v=h+h,g=d+d,S=c*p,M=c*v,A=c*g,C=h*v,y=h*g,x=d*g,P=m*p,N=m*v,L=m*g,B=r.x,F=r.y,z=r.z;return l[0]=(1-(C+x))*B,l[1]=(M+L)*B,l[2]=(A-N)*B,l[3]=0,l[4]=(M-L)*F,l[5]=(1-(S+x))*F,l[6]=(y+P)*F,l[7]=0,l[8]=(A+N)*z,l[9]=(y-P)*z,l[10]=(1-(S+C))*z,l[11]=0,l[12]=e.x,l[13]=e.y,l[14]=e.z,l[15]=1,this}decompose(e,i,r){const l=this.elements;if(e.x=l[12],e.y=l[13],e.z=l[14],this.determinant()===0)return r.set(1,1,1),i.identity(),this;let c=ms.set(l[0],l[1],l[2]).length();const h=ms.set(l[4],l[5],l[6]).length(),d=ms.set(l[8],l[9],l[10]).length();this.determinant()<0&&(c=-c),Si.copy(this);const p=1/c,v=1/h,g=1/d;return Si.elements[0]*=p,Si.elements[1]*=p,Si.elements[2]*=p,Si.elements[4]*=v,Si.elements[5]*=v,Si.elements[6]*=v,Si.elements[8]*=g,Si.elements[9]*=g,Si.elements[10]*=g,i.setFromRotationMatrix(Si),r.x=c,r.y=h,r.z=d,this}makePerspective(e,i,r,l,c,h,d=Ni,m=!1){const p=this.elements,v=2*c/(i-e),g=2*c/(r-l),S=(i+e)/(i-e),M=(r+l)/(r-l);let A,C;if(m)A=c/(h-c),C=h*c/(h-c);else if(d===Ni)A=-(h+c)/(h-c),C=-2*h*c/(h-c);else if(d===Nu)A=-h/(h-c),C=-h*c/(h-c);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+d);return p[0]=v,p[4]=0,p[8]=S,p[12]=0,p[1]=0,p[5]=g,p[9]=M,p[13]=0,p[2]=0,p[6]=0,p[10]=A,p[14]=C,p[3]=0,p[7]=0,p[11]=-1,p[15]=0,this}makeOrthographic(e,i,r,l,c,h,d=Ni,m=!1){const p=this.elements,v=2/(i-e),g=2/(r-l),S=-(i+e)/(i-e),M=-(r+l)/(r-l);let A,C;if(m)A=1/(h-c),C=h/(h-c);else if(d===Ni)A=-2/(h-c),C=-(h+c)/(h-c);else if(d===Nu)A=-1/(h-c),C=-c/(h-c);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+d);return p[0]=v,p[4]=0,p[8]=0,p[12]=S,p[1]=0,p[5]=g,p[9]=0,p[13]=M,p[2]=0,p[6]=0,p[10]=A,p[14]=C,p[3]=0,p[7]=0,p[11]=0,p[15]=1,this}equals(e){const i=this.elements,r=e.elements;for(let l=0;l<16;l++)if(i[l]!==r[l])return!1;return!0}fromArray(e,i=0){for(let r=0;r<16;r++)this.elements[r]=e[r+i];return this}toArray(e=[],i=0){const r=this.elements;return e[i]=r[0],e[i+1]=r[1],e[i+2]=r[2],e[i+3]=r[3],e[i+4]=r[4],e[i+5]=r[5],e[i+6]=r[6],e[i+7]=r[7],e[i+8]=r[8],e[i+9]=r[9],e[i+10]=r[10],e[i+11]=r[11],e[i+12]=r[12],e[i+13]=r[13],e[i+14]=r[14],e[i+15]=r[15],e}}const ms=new it,Si=new tn,yM=new it(0,0,0),EM=new it(1,1,1),qa=new it,fu=new it,Qn=new it,G0=new tn,V0=new ko;class Bi{constructor(e=0,i=0,r=0,l=Bi.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=i,this._z=r,this._order=l}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,i,r,l=this._order){return this._x=e,this._y=i,this._z=r,this._order=l,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,i=this._order,r=!0){const l=e.elements,c=l[0],h=l[4],d=l[8],m=l[1],p=l[5],v=l[9],g=l[2],S=l[6],M=l[10];switch(i){case"XYZ":this._y=Math.asin(xe(d,-1,1)),Math.abs(d)<.9999999?(this._x=Math.atan2(-v,M),this._z=Math.atan2(-h,c)):(this._x=Math.atan2(S,p),this._z=0);break;case"YXZ":this._x=Math.asin(-xe(v,-1,1)),Math.abs(v)<.9999999?(this._y=Math.atan2(d,M),this._z=Math.atan2(m,p)):(this._y=Math.atan2(-g,c),this._z=0);break;case"ZXY":this._x=Math.asin(xe(S,-1,1)),Math.abs(S)<.9999999?(this._y=Math.atan2(-g,M),this._z=Math.atan2(-h,p)):(this._y=0,this._z=Math.atan2(m,c));break;case"ZYX":this._y=Math.asin(-xe(g,-1,1)),Math.abs(g)<.9999999?(this._x=Math.atan2(S,M),this._z=Math.atan2(m,c)):(this._x=0,this._z=Math.atan2(-h,p));break;case"YZX":this._z=Math.asin(xe(m,-1,1)),Math.abs(m)<.9999999?(this._x=Math.atan2(-v,p),this._y=Math.atan2(-g,c)):(this._x=0,this._y=Math.atan2(d,M));break;case"XZY":this._z=Math.asin(-xe(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(S,p),this._y=Math.atan2(d,c)):(this._x=Math.atan2(-v,M),this._y=0);break;default:ae("Euler: .setFromRotationMatrix() encountered an unknown order: "+i)}return this._order=i,r===!0&&this._onChangeCallback(),this}setFromQuaternion(e,i,r){return G0.makeRotationFromQuaternion(e),this.setFromRotationMatrix(G0,i,r)}setFromVector3(e,i=this._order){return this.set(e.x,e.y,e.z,i)}reorder(e){return V0.setFromEuler(this),this.setFromQuaternion(V0,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],i=0){return e[i]=this._x,e[i+1]=this._y,e[i+2]=this._z,e[i+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}Bi.DEFAULT_ORDER="XYZ";class K_{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let TM=0;const X0=new it,gs=new ko,oa=new tn,hu=new it,Uo=new it,bM=new it,AM=new ko,k0=new it(1,0,0),W0=new it(0,1,0),q0=new it(0,0,1),Y0={type:"added"},RM={type:"removed"},_s={type:"childadded",child:null},oh={type:"childremoved",child:null};class Ln extends Us{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:TM++}),this.uuid=Xo(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Ln.DEFAULT_UP.clone();const e=new it,i=new Bi,r=new ko,l=new it(1,1,1);function c(){r.setFromEuler(i,!1)}function h(){i.setFromQuaternion(r,void 0,!1)}i._onChange(c),r._onChange(h),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:i},quaternion:{configurable:!0,enumerable:!0,value:r},scale:{configurable:!0,enumerable:!0,value:l},modelViewMatrix:{value:new tn},normalMatrix:{value:new ue}}),this.matrix=new tn,this.matrixWorld=new tn,this.matrixAutoUpdate=Ln.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Ln.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new K_,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,i){this.quaternion.setFromAxisAngle(e,i)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,i){return gs.setFromAxisAngle(e,i),this.quaternion.multiply(gs),this}rotateOnWorldAxis(e,i){return gs.setFromAxisAngle(e,i),this.quaternion.premultiply(gs),this}rotateX(e){return this.rotateOnAxis(k0,e)}rotateY(e){return this.rotateOnAxis(W0,e)}rotateZ(e){return this.rotateOnAxis(q0,e)}translateOnAxis(e,i){return X0.copy(e).applyQuaternion(this.quaternion),this.position.add(X0.multiplyScalar(i)),this}translateX(e){return this.translateOnAxis(k0,e)}translateY(e){return this.translateOnAxis(W0,e)}translateZ(e){return this.translateOnAxis(q0,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(oa.copy(this.matrixWorld).invert())}lookAt(e,i,r){e.isVector3?hu.copy(e):hu.set(e,i,r);const l=this.parent;this.updateWorldMatrix(!0,!1),Uo.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?oa.lookAt(Uo,hu,this.up):oa.lookAt(hu,Uo,this.up),this.quaternion.setFromRotationMatrix(oa),l&&(oa.extractRotation(l.matrixWorld),gs.setFromRotationMatrix(oa),this.quaternion.premultiply(gs.invert()))}add(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.add(arguments[i]);return this}return e===this?(be("Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(Y0),_s.child=e,this.dispatchEvent(_s),_s.child=null):be("Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let r=0;r<arguments.length;r++)this.remove(arguments[r]);return this}const i=this.children.indexOf(e);return i!==-1&&(e.parent=null,this.children.splice(i,1),e.dispatchEvent(RM),oh.child=e,this.dispatchEvent(oh),oh.child=null),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),oa.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),oa.multiply(e.parent.matrixWorld)),e.applyMatrix4(oa),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(Y0),_s.child=e,this.dispatchEvent(_s),_s.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,i){if(this[e]===i)return this;for(let r=0,l=this.children.length;r<l;r++){const h=this.children[r].getObjectByProperty(e,i);if(h!==void 0)return h}}getObjectsByProperty(e,i,r=[]){this[e]===i&&r.push(this);const l=this.children;for(let c=0,h=l.length;c<h;c++)l[c].getObjectsByProperty(e,i,r);return r}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Uo,e,bM),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Uo,AM,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const i=this.matrixWorld.elements;return e.set(i[8],i[9],i[10]).normalize()}raycast(){}traverse(e){e(this);const i=this.children;for(let r=0,l=i.length;r<l;r++)i[r].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const i=this.children;for(let r=0,l=i.length;r<l;r++)i[r].traverseVisible(e)}traverseAncestors(e){const i=this.parent;i!==null&&(e(i),i.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);const i=this.children;for(let r=0,l=i.length;r<l;r++)i[r].updateMatrixWorld(e)}updateWorldMatrix(e,i){const r=this.parent;if(e===!0&&r!==null&&r.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),i===!0){const l=this.children;for(let c=0,h=l.length;c<h;c++)l[c].updateWorldMatrix(!1,!0)}}toJSON(e){const i=e===void 0||typeof e=="string",r={};i&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},r.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});const l={};l.uuid=this.uuid,l.type=this.type,this.name!==""&&(l.name=this.name),this.castShadow===!0&&(l.castShadow=!0),this.receiveShadow===!0&&(l.receiveShadow=!0),this.visible===!1&&(l.visible=!1),this.frustumCulled===!1&&(l.frustumCulled=!1),this.renderOrder!==0&&(l.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(l.userData=this.userData),l.layers=this.layers.mask,l.matrix=this.matrix.toArray(),l.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(l.matrixAutoUpdate=!1),this.isInstancedMesh&&(l.type="InstancedMesh",l.count=this.count,l.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(l.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(l.type="BatchedMesh",l.perObjectFrustumCulled=this.perObjectFrustumCulled,l.sortObjects=this.sortObjects,l.drawRanges=this._drawRanges,l.reservedRanges=this._reservedRanges,l.geometryInfo=this._geometryInfo.map(d=>({...d,boundingBox:d.boundingBox?d.boundingBox.toJSON():void 0,boundingSphere:d.boundingSphere?d.boundingSphere.toJSON():void 0})),l.instanceInfo=this._instanceInfo.map(d=>({...d})),l.availableInstanceIds=this._availableInstanceIds.slice(),l.availableGeometryIds=this._availableGeometryIds.slice(),l.nextIndexStart=this._nextIndexStart,l.nextVertexStart=this._nextVertexStart,l.geometryCount=this._geometryCount,l.maxInstanceCount=this._maxInstanceCount,l.maxVertexCount=this._maxVertexCount,l.maxIndexCount=this._maxIndexCount,l.geometryInitialized=this._geometryInitialized,l.matricesTexture=this._matricesTexture.toJSON(e),l.indirectTexture=this._indirectTexture.toJSON(e),this._colorsTexture!==null&&(l.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(l.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(l.boundingBox=this.boundingBox.toJSON()));function c(d,m){return d[m.uuid]===void 0&&(d[m.uuid]=m.toJSON(e)),m.uuid}if(this.isScene)this.background&&(this.background.isColor?l.background=this.background.toJSON():this.background.isTexture&&(l.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(l.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){l.geometry=c(e.geometries,this.geometry);const d=this.geometry.parameters;if(d!==void 0&&d.shapes!==void 0){const m=d.shapes;if(Array.isArray(m))for(let p=0,v=m.length;p<v;p++){const g=m[p];c(e.shapes,g)}else c(e.shapes,m)}}if(this.isSkinnedMesh&&(l.bindMode=this.bindMode,l.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(c(e.skeletons,this.skeleton),l.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const d=[];for(let m=0,p=this.material.length;m<p;m++)d.push(c(e.materials,this.material[m]));l.material=d}else l.material=c(e.materials,this.material);if(this.children.length>0){l.children=[];for(let d=0;d<this.children.length;d++)l.children.push(this.children[d].toJSON(e).object)}if(this.animations.length>0){l.animations=[];for(let d=0;d<this.animations.length;d++){const m=this.animations[d];l.animations.push(c(e.animations,m))}}if(i){const d=h(e.geometries),m=h(e.materials),p=h(e.textures),v=h(e.images),g=h(e.shapes),S=h(e.skeletons),M=h(e.animations),A=h(e.nodes);d.length>0&&(r.geometries=d),m.length>0&&(r.materials=m),p.length>0&&(r.textures=p),v.length>0&&(r.images=v),g.length>0&&(r.shapes=g),S.length>0&&(r.skeletons=S),M.length>0&&(r.animations=M),A.length>0&&(r.nodes=A)}return r.object=l,r;function h(d){const m=[];for(const p in d){const v=d[p];delete v.metadata,m.push(v)}return m}}clone(e){return new this.constructor().copy(this,e)}copy(e,i=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),i===!0)for(let r=0;r<e.children.length;r++){const l=e.children[r];this.add(l.clone())}return this}}Ln.DEFAULT_UP=new it(0,1,0);Ln.DEFAULT_MATRIX_AUTO_UPDATE=!0;Ln.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const Mi=new it,la=new it,lh=new it,ua=new it,vs=new it,xs=new it,Z0=new it,uh=new it,ch=new it,fh=new it,hh=new $e,dh=new $e,ph=new $e;class Ei{constructor(e=new it,i=new it,r=new it){this.a=e,this.b=i,this.c=r}static getNormal(e,i,r,l){l.subVectors(r,i),Mi.subVectors(e,i),l.cross(Mi);const c=l.lengthSq();return c>0?l.multiplyScalar(1/Math.sqrt(c)):l.set(0,0,0)}static getBarycoord(e,i,r,l,c){Mi.subVectors(l,i),la.subVectors(r,i),lh.subVectors(e,i);const h=Mi.dot(Mi),d=Mi.dot(la),m=Mi.dot(lh),p=la.dot(la),v=la.dot(lh),g=h*p-d*d;if(g===0)return c.set(0,0,0),null;const S=1/g,M=(p*m-d*v)*S,A=(h*v-d*m)*S;return c.set(1-M-A,A,M)}static containsPoint(e,i,r,l){return this.getBarycoord(e,i,r,l,ua)===null?!1:ua.x>=0&&ua.y>=0&&ua.x+ua.y<=1}static getInterpolation(e,i,r,l,c,h,d,m){return this.getBarycoord(e,i,r,l,ua)===null?(m.x=0,m.y=0,"z"in m&&(m.z=0),"w"in m&&(m.w=0),null):(m.setScalar(0),m.addScaledVector(c,ua.x),m.addScaledVector(h,ua.y),m.addScaledVector(d,ua.z),m)}static getInterpolatedAttribute(e,i,r,l,c,h){return hh.setScalar(0),dh.setScalar(0),ph.setScalar(0),hh.fromBufferAttribute(e,i),dh.fromBufferAttribute(e,r),ph.fromBufferAttribute(e,l),h.setScalar(0),h.addScaledVector(hh,c.x),h.addScaledVector(dh,c.y),h.addScaledVector(ph,c.z),h}static isFrontFacing(e,i,r,l){return Mi.subVectors(r,i),la.subVectors(e,i),Mi.cross(la).dot(l)<0}set(e,i,r){return this.a.copy(e),this.b.copy(i),this.c.copy(r),this}setFromPointsAndIndices(e,i,r,l){return this.a.copy(e[i]),this.b.copy(e[r]),this.c.copy(e[l]),this}setFromAttributeAndIndices(e,i,r,l){return this.a.fromBufferAttribute(e,i),this.b.fromBufferAttribute(e,r),this.c.fromBufferAttribute(e,l),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return Mi.subVectors(this.c,this.b),la.subVectors(this.a,this.b),Mi.cross(la).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return Ei.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,i){return Ei.getBarycoord(e,this.a,this.b,this.c,i)}getInterpolation(e,i,r,l,c){return Ei.getInterpolation(e,this.a,this.b,this.c,i,r,l,c)}containsPoint(e){return Ei.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return Ei.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,i){const r=this.a,l=this.b,c=this.c;let h,d;vs.subVectors(l,r),xs.subVectors(c,r),uh.subVectors(e,r);const m=vs.dot(uh),p=xs.dot(uh);if(m<=0&&p<=0)return i.copy(r);ch.subVectors(e,l);const v=vs.dot(ch),g=xs.dot(ch);if(v>=0&&g<=v)return i.copy(l);const S=m*g-v*p;if(S<=0&&m>=0&&v<=0)return h=m/(m-v),i.copy(r).addScaledVector(vs,h);fh.subVectors(e,c);const M=vs.dot(fh),A=xs.dot(fh);if(A>=0&&M<=A)return i.copy(c);const C=M*p-m*A;if(C<=0&&p>=0&&A<=0)return d=p/(p-A),i.copy(r).addScaledVector(xs,d);const y=v*A-M*g;if(y<=0&&g-v>=0&&M-A>=0)return Z0.subVectors(c,l),d=(g-v)/(g-v+(M-A)),i.copy(l).addScaledVector(Z0,d);const x=1/(y+C+S);return h=C*x,d=S*x,i.copy(r).addScaledVector(vs,h).addScaledVector(xs,d)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Q_={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Ya={h:0,s:0,l:0},du={h:0,s:0,l:0};function mh(o,e,i){return i<0&&(i+=1),i>1&&(i-=1),i<1/6?o+(e-o)*6*i:i<1/2?e:i<2/3?o+(e-o)*6*(2/3-i):o}class we{constructor(e,i,r){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,i,r)}set(e,i,r){if(i===void 0&&r===void 0){const l=e;l&&l.isColor?this.copy(l):typeof l=="number"?this.setHex(l):typeof l=="string"&&this.setStyle(l)}else this.setRGB(e,i,r);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,i=fi){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,ye.colorSpaceToWorking(this,i),this}setRGB(e,i,r,l=ye.workingColorSpace){return this.r=e,this.g=i,this.b=r,ye.colorSpaceToWorking(this,l),this}setHSL(e,i,r,l=ye.workingColorSpace){if(e=dM(e,1),i=xe(i,0,1),r=xe(r,0,1),i===0)this.r=this.g=this.b=r;else{const c=r<=.5?r*(1+i):r+i-r*i,h=2*r-c;this.r=mh(h,c,e+1/3),this.g=mh(h,c,e),this.b=mh(h,c,e-1/3)}return ye.colorSpaceToWorking(this,l),this}setStyle(e,i=fi){function r(c){c!==void 0&&parseFloat(c)<1&&ae("Color: Alpha component of "+e+" will be ignored.")}let l;if(l=/^(\w+)\(([^\)]*)\)/.exec(e)){let c;const h=l[1],d=l[2];switch(h){case"rgb":case"rgba":if(c=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(d))return r(c[4]),this.setRGB(Math.min(255,parseInt(c[1],10))/255,Math.min(255,parseInt(c[2],10))/255,Math.min(255,parseInt(c[3],10))/255,i);if(c=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(d))return r(c[4]),this.setRGB(Math.min(100,parseInt(c[1],10))/100,Math.min(100,parseInt(c[2],10))/100,Math.min(100,parseInt(c[3],10))/100,i);break;case"hsl":case"hsla":if(c=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(d))return r(c[4]),this.setHSL(parseFloat(c[1])/360,parseFloat(c[2])/100,parseFloat(c[3])/100,i);break;default:ae("Color: Unknown color model "+e)}}else if(l=/^\#([A-Fa-f\d]+)$/.exec(e)){const c=l[1],h=c.length;if(h===3)return this.setRGB(parseInt(c.charAt(0),16)/15,parseInt(c.charAt(1),16)/15,parseInt(c.charAt(2),16)/15,i);if(h===6)return this.setHex(parseInt(c,16),i);ae("Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,i);return this}setColorName(e,i=fi){const r=Q_[e.toLowerCase()];return r!==void 0?this.setHex(r,i):ae("Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=da(e.r),this.g=da(e.g),this.b=da(e.b),this}copyLinearToSRGB(e){return this.r=bs(e.r),this.g=bs(e.g),this.b=bs(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=fi){return ye.workingToColorSpace(wn.copy(this),e),Math.round(xe(wn.r*255,0,255))*65536+Math.round(xe(wn.g*255,0,255))*256+Math.round(xe(wn.b*255,0,255))}getHexString(e=fi){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,i=ye.workingColorSpace){ye.workingToColorSpace(wn.copy(this),i);const r=wn.r,l=wn.g,c=wn.b,h=Math.max(r,l,c),d=Math.min(r,l,c);let m,p;const v=(d+h)/2;if(d===h)m=0,p=0;else{const g=h-d;switch(p=v<=.5?g/(h+d):g/(2-h-d),h){case r:m=(l-c)/g+(l<c?6:0);break;case l:m=(c-r)/g+2;break;case c:m=(r-l)/g+4;break}m/=6}return e.h=m,e.s=p,e.l=v,e}getRGB(e,i=ye.workingColorSpace){return ye.workingToColorSpace(wn.copy(this),i),e.r=wn.r,e.g=wn.g,e.b=wn.b,e}getStyle(e=fi){ye.workingToColorSpace(wn.copy(this),e);const i=wn.r,r=wn.g,l=wn.b;return e!==fi?`color(${e} ${i.toFixed(3)} ${r.toFixed(3)} ${l.toFixed(3)})`:`rgb(${Math.round(i*255)},${Math.round(r*255)},${Math.round(l*255)})`}offsetHSL(e,i,r){return this.getHSL(Ya),this.setHSL(Ya.h+e,Ya.s+i,Ya.l+r)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,i){return this.r=e.r+i.r,this.g=e.g+i.g,this.b=e.b+i.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,i){return this.r+=(e.r-this.r)*i,this.g+=(e.g-this.g)*i,this.b+=(e.b-this.b)*i,this}lerpColors(e,i,r){return this.r=e.r+(i.r-e.r)*r,this.g=e.g+(i.g-e.g)*r,this.b=e.b+(i.b-e.b)*r,this}lerpHSL(e,i){this.getHSL(Ya),e.getHSL(du);const r=Qf(Ya.h,du.h,i),l=Qf(Ya.s,du.s,i),c=Qf(Ya.l,du.l,i);return this.setHSL(r,l,c),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const i=this.r,r=this.g,l=this.b,c=e.elements;return this.r=c[0]*i+c[3]*r+c[6]*l,this.g=c[1]*i+c[4]*r+c[7]*l,this.b=c[2]*i+c[5]*r+c[8]*l,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,i=0){return this.r=e[i],this.g=e[i+1],this.b=e[i+2],this}toArray(e=[],i=0){return e[i]=this.r,e[i+1]=this.g,e[i+2]=this.b,e}fromBufferAttribute(e,i){return this.r=e.getX(i),this.g=e.getY(i),this.b=e.getZ(i),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const wn=new we;we.NAMES=Q_;let CM=0;class qo extends Us{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:CM++}),this.uuid=Xo(),this.name="",this.type="Material",this.blending=Ts,this.side=Qa,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Uh,this.blendDst=Lh,this.blendEquation=Er,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new we(0,0,0),this.blendAlpha=0,this.depthFunc=As,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=N0,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=cs,this.stencilZFail=cs,this.stencilZPass=cs,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.allowOverride=!0,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const i in e){const r=e[i];if(r===void 0){ae(`Material: parameter '${i}' has value of undefined.`);continue}const l=this[i];if(l===void 0){ae(`Material: '${i}' is not a property of THREE.${this.type}.`);continue}l&&l.isColor?l.set(r):l&&l.isVector3&&r&&r.isVector3?l.copy(r):this[i]=r}}toJSON(e){const i=e===void 0||typeof e=="string";i&&(e={textures:{},images:{}});const r={metadata:{version:4.7,type:"Material",generator:"Material.toJSON"}};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.color&&this.color.isColor&&(r.color=this.color.getHex()),this.roughness!==void 0&&(r.roughness=this.roughness),this.metalness!==void 0&&(r.metalness=this.metalness),this.sheen!==void 0&&(r.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(r.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(r.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(r.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(r.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(r.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(r.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(r.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(r.shininess=this.shininess),this.clearcoat!==void 0&&(r.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(r.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(r.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(r.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(r.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,r.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.sheenColorMap&&this.sheenColorMap.isTexture&&(r.sheenColorMap=this.sheenColorMap.toJSON(e).uuid),this.sheenRoughnessMap&&this.sheenRoughnessMap.isTexture&&(r.sheenRoughnessMap=this.sheenRoughnessMap.toJSON(e).uuid),this.dispersion!==void 0&&(r.dispersion=this.dispersion),this.iridescence!==void 0&&(r.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(r.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(r.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(r.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(r.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(r.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(r.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(r.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(r.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(r.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(r.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(r.lightMap=this.lightMap.toJSON(e).uuid,r.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(r.aoMap=this.aoMap.toJSON(e).uuid,r.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(r.bumpMap=this.bumpMap.toJSON(e).uuid,r.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(r.normalMap=this.normalMap.toJSON(e).uuid,r.normalMapType=this.normalMapType,r.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(r.displacementMap=this.displacementMap.toJSON(e).uuid,r.displacementScale=this.displacementScale,r.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(r.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(r.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(r.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(r.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(r.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(r.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(r.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(r.combine=this.combine)),this.envMapRotation!==void 0&&(r.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(r.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(r.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(r.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(r.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(r.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(r.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(r.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(r.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(r.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(r.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(r.size=this.size),this.shadowSide!==null&&(r.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(r.sizeAttenuation=this.sizeAttenuation),this.blending!==Ts&&(r.blending=this.blending),this.side!==Qa&&(r.side=this.side),this.vertexColors===!0&&(r.vertexColors=!0),this.opacity<1&&(r.opacity=this.opacity),this.transparent===!0&&(r.transparent=!0),this.blendSrc!==Uh&&(r.blendSrc=this.blendSrc),this.blendDst!==Lh&&(r.blendDst=this.blendDst),this.blendEquation!==Er&&(r.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(r.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(r.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(r.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(r.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(r.blendAlpha=this.blendAlpha),this.depthFunc!==As&&(r.depthFunc=this.depthFunc),this.depthTest===!1&&(r.depthTest=this.depthTest),this.depthWrite===!1&&(r.depthWrite=this.depthWrite),this.colorWrite===!1&&(r.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(r.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==N0&&(r.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(r.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(r.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==cs&&(r.stencilFail=this.stencilFail),this.stencilZFail!==cs&&(r.stencilZFail=this.stencilZFail),this.stencilZPass!==cs&&(r.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(r.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(r.rotation=this.rotation),this.polygonOffset===!0&&(r.polygonOffset=!0),this.polygonOffsetFactor!==0&&(r.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(r.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(r.linewidth=this.linewidth),this.dashSize!==void 0&&(r.dashSize=this.dashSize),this.gapSize!==void 0&&(r.gapSize=this.gapSize),this.scale!==void 0&&(r.scale=this.scale),this.dithering===!0&&(r.dithering=!0),this.alphaTest>0&&(r.alphaTest=this.alphaTest),this.alphaHash===!0&&(r.alphaHash=!0),this.alphaToCoverage===!0&&(r.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(r.premultipliedAlpha=!0),this.forceSinglePass===!0&&(r.forceSinglePass=!0),this.allowOverride===!1&&(r.allowOverride=!1),this.wireframe===!0&&(r.wireframe=!0),this.wireframeLinewidth>1&&(r.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(r.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(r.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(r.flatShading=!0),this.visible===!1&&(r.visible=!1),this.toneMapped===!1&&(r.toneMapped=!1),this.fog===!1&&(r.fog=!1),Object.keys(this.userData).length>0&&(r.userData=this.userData);function l(c){const h=[];for(const d in c){const m=c[d];delete m.metadata,h.push(m)}return h}if(i){const c=l(e.textures),h=l(e.images);c.length>0&&(r.textures=c),h.length>0&&(r.images=h)}return r}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const i=e.clippingPlanes;let r=null;if(i!==null){const l=i.length;r=new Array(l);for(let c=0;c!==l;++c)r[c]=i[c].clone()}return this.clippingPlanes=r,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.allowOverride=e.allowOverride,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}}class J_ extends qo{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new we(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Bi,this.combine=U_,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const un=new it,pu=new Ue;let DM=0;class Fi{constructor(e,i,r=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:DM++}),this.name="",this.array=e,this.itemSize=i,this.count=e!==void 0?e.length/i:0,this.normalized=r,this.usage=O0,this.updateRanges=[],this.gpuType=Li,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,i){this.updateRanges.push({start:e,count:i})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,i,r){e*=this.itemSize,r*=i.itemSize;for(let l=0,c=this.itemSize;l<c;l++)this.array[e+l]=i.array[r+l];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let i=0,r=this.count;i<r;i++)pu.fromBufferAttribute(this,i),pu.applyMatrix3(e),this.setXY(i,pu.x,pu.y);else if(this.itemSize===3)for(let i=0,r=this.count;i<r;i++)un.fromBufferAttribute(this,i),un.applyMatrix3(e),this.setXYZ(i,un.x,un.y,un.z);return this}applyMatrix4(e){for(let i=0,r=this.count;i<r;i++)un.fromBufferAttribute(this,i),un.applyMatrix4(e),this.setXYZ(i,un.x,un.y,un.z);return this}applyNormalMatrix(e){for(let i=0,r=this.count;i<r;i++)un.fromBufferAttribute(this,i),un.applyNormalMatrix(e),this.setXYZ(i,un.x,un.y,un.z);return this}transformDirection(e){for(let i=0,r=this.count;i<r;i++)un.fromBufferAttribute(this,i),un.transformDirection(e),this.setXYZ(i,un.x,un.y,un.z);return this}set(e,i=0){return this.array.set(e,i),this}getComponent(e,i){let r=this.array[e*this.itemSize+i];return this.normalized&&(r=Co(r,this.array)),r}setComponent(e,i,r){return this.normalized&&(r=Vn(r,this.array)),this.array[e*this.itemSize+i]=r,this}getX(e){let i=this.array[e*this.itemSize];return this.normalized&&(i=Co(i,this.array)),i}setX(e,i){return this.normalized&&(i=Vn(i,this.array)),this.array[e*this.itemSize]=i,this}getY(e){let i=this.array[e*this.itemSize+1];return this.normalized&&(i=Co(i,this.array)),i}setY(e,i){return this.normalized&&(i=Vn(i,this.array)),this.array[e*this.itemSize+1]=i,this}getZ(e){let i=this.array[e*this.itemSize+2];return this.normalized&&(i=Co(i,this.array)),i}setZ(e,i){return this.normalized&&(i=Vn(i,this.array)),this.array[e*this.itemSize+2]=i,this}getW(e){let i=this.array[e*this.itemSize+3];return this.normalized&&(i=Co(i,this.array)),i}setW(e,i){return this.normalized&&(i=Vn(i,this.array)),this.array[e*this.itemSize+3]=i,this}setXY(e,i,r){return e*=this.itemSize,this.normalized&&(i=Vn(i,this.array),r=Vn(r,this.array)),this.array[e+0]=i,this.array[e+1]=r,this}setXYZ(e,i,r,l){return e*=this.itemSize,this.normalized&&(i=Vn(i,this.array),r=Vn(r,this.array),l=Vn(l,this.array)),this.array[e+0]=i,this.array[e+1]=r,this.array[e+2]=l,this}setXYZW(e,i,r,l,c){return e*=this.itemSize,this.normalized&&(i=Vn(i,this.array),r=Vn(r,this.array),l=Vn(l,this.array),c=Vn(c,this.array)),this.array[e+0]=i,this.array[e+1]=r,this.array[e+2]=l,this.array[e+3]=c,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==O0&&(e.usage=this.usage),e}}class $_ extends Fi{constructor(e,i,r){super(new Uint16Array(e),i,r)}}class tv extends Fi{constructor(e,i,r){super(new Uint32Array(e),i,r)}}class hi extends Fi{constructor(e,i,r){super(new Float32Array(e),i,r)}}let wM=0;const ci=new tn,gh=new Ln,Ss=new it,Jn=new Wo,Lo=new Wo,mn=new it;class Hi extends Us{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:wM++}),this.uuid=Xo(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.indirectOffset=0,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Z_(e)?tv:$_)(e,1):this.index=e,this}setIndirect(e,i=0){return this.indirect=e,this.indirectOffset=i,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,i){return this.attributes[e]=i,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,i,r=0){this.groups.push({start:e,count:i,materialIndex:r})}clearGroups(){this.groups=[]}setDrawRange(e,i){this.drawRange.start=e,this.drawRange.count=i}applyMatrix4(e){const i=this.attributes.position;i!==void 0&&(i.applyMatrix4(e),i.needsUpdate=!0);const r=this.attributes.normal;if(r!==void 0){const c=new ue().getNormalMatrix(e);r.applyNormalMatrix(c),r.needsUpdate=!0}const l=this.attributes.tangent;return l!==void 0&&(l.transformDirection(e),l.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return ci.makeRotationFromQuaternion(e),this.applyMatrix4(ci),this}rotateX(e){return ci.makeRotationX(e),this.applyMatrix4(ci),this}rotateY(e){return ci.makeRotationY(e),this.applyMatrix4(ci),this}rotateZ(e){return ci.makeRotationZ(e),this.applyMatrix4(ci),this}translate(e,i,r){return ci.makeTranslation(e,i,r),this.applyMatrix4(ci),this}scale(e,i,r){return ci.makeScale(e,i,r),this.applyMatrix4(ci),this}lookAt(e){return gh.lookAt(e),gh.updateMatrix(),this.applyMatrix4(gh.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(Ss).negate(),this.translate(Ss.x,Ss.y,Ss.z),this}setFromPoints(e){const i=this.getAttribute("position");if(i===void 0){const r=[];for(let l=0,c=e.length;l<c;l++){const h=e[l];r.push(h.x,h.y,h.z||0)}this.setAttribute("position",new hi(r,3))}else{const r=Math.min(e.length,i.count);for(let l=0;l<r;l++){const c=e[l];i.setXYZ(l,c.x,c.y,c.z||0)}e.length>i.count&&ae("BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),i.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Wo);const e=this.attributes.position,i=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){be("BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new it(-1/0,-1/0,-1/0),new it(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),i)for(let r=0,l=i.length;r<l;r++){const c=i[r];Jn.setFromBufferAttribute(c),this.morphTargetsRelative?(mn.addVectors(this.boundingBox.min,Jn.min),this.boundingBox.expandByPoint(mn),mn.addVectors(this.boundingBox.max,Jn.max),this.boundingBox.expandByPoint(mn)):(this.boundingBox.expandByPoint(Jn.min),this.boundingBox.expandByPoint(Jn.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&be('BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Pd);const e=this.attributes.position,i=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){be("BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new it,1/0);return}if(e){const r=this.boundingSphere.center;if(Jn.setFromBufferAttribute(e),i)for(let c=0,h=i.length;c<h;c++){const d=i[c];Lo.setFromBufferAttribute(d),this.morphTargetsRelative?(mn.addVectors(Jn.min,Lo.min),Jn.expandByPoint(mn),mn.addVectors(Jn.max,Lo.max),Jn.expandByPoint(mn)):(Jn.expandByPoint(Lo.min),Jn.expandByPoint(Lo.max))}Jn.getCenter(r);let l=0;for(let c=0,h=e.count;c<h;c++)mn.fromBufferAttribute(e,c),l=Math.max(l,r.distanceToSquared(mn));if(i)for(let c=0,h=i.length;c<h;c++){const d=i[c],m=this.morphTargetsRelative;for(let p=0,v=d.count;p<v;p++)mn.fromBufferAttribute(d,p),m&&(Ss.fromBufferAttribute(e,p),mn.add(Ss)),l=Math.max(l,r.distanceToSquared(mn))}this.boundingSphere.radius=Math.sqrt(l),isNaN(this.boundingSphere.radius)&&be('BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,i=this.attributes;if(e===null||i.position===void 0||i.normal===void 0||i.uv===void 0){be("BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const r=i.position,l=i.normal,c=i.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Fi(new Float32Array(4*r.count),4));const h=this.getAttribute("tangent"),d=[],m=[];for(let Q=0;Q<r.count;Q++)d[Q]=new it,m[Q]=new it;const p=new it,v=new it,g=new it,S=new Ue,M=new Ue,A=new Ue,C=new it,y=new it;function x(Q,R,D){p.fromBufferAttribute(r,Q),v.fromBufferAttribute(r,R),g.fromBufferAttribute(r,D),S.fromBufferAttribute(c,Q),M.fromBufferAttribute(c,R),A.fromBufferAttribute(c,D),v.sub(p),g.sub(p),M.sub(S),A.sub(S);const k=1/(M.x*A.y-A.x*M.y);isFinite(k)&&(C.copy(v).multiplyScalar(A.y).addScaledVector(g,-M.y).multiplyScalar(k),y.copy(g).multiplyScalar(M.x).addScaledVector(v,-A.x).multiplyScalar(k),d[Q].add(C),d[R].add(C),d[D].add(C),m[Q].add(y),m[R].add(y),m[D].add(y))}let P=this.groups;P.length===0&&(P=[{start:0,count:e.count}]);for(let Q=0,R=P.length;Q<R;++Q){const D=P[Q],k=D.start,rt=D.count;for(let at=k,ut=k+rt;at<ut;at+=3)x(e.getX(at+0),e.getX(at+1),e.getX(at+2))}const N=new it,L=new it,B=new it,F=new it;function z(Q){B.fromBufferAttribute(l,Q),F.copy(B);const R=d[Q];N.copy(R),N.sub(B.multiplyScalar(B.dot(R))).normalize(),L.crossVectors(F,R);const k=L.dot(m[Q])<0?-1:1;h.setXYZW(Q,N.x,N.y,N.z,k)}for(let Q=0,R=P.length;Q<R;++Q){const D=P[Q],k=D.start,rt=D.count;for(let at=k,ut=k+rt;at<ut;at+=3)z(e.getX(at+0)),z(e.getX(at+1)),z(e.getX(at+2))}}computeVertexNormals(){const e=this.index,i=this.getAttribute("position");if(i!==void 0){let r=this.getAttribute("normal");if(r===void 0)r=new Fi(new Float32Array(i.count*3),3),this.setAttribute("normal",r);else for(let S=0,M=r.count;S<M;S++)r.setXYZ(S,0,0,0);const l=new it,c=new it,h=new it,d=new it,m=new it,p=new it,v=new it,g=new it;if(e)for(let S=0,M=e.count;S<M;S+=3){const A=e.getX(S+0),C=e.getX(S+1),y=e.getX(S+2);l.fromBufferAttribute(i,A),c.fromBufferAttribute(i,C),h.fromBufferAttribute(i,y),v.subVectors(h,c),g.subVectors(l,c),v.cross(g),d.fromBufferAttribute(r,A),m.fromBufferAttribute(r,C),p.fromBufferAttribute(r,y),d.add(v),m.add(v),p.add(v),r.setXYZ(A,d.x,d.y,d.z),r.setXYZ(C,m.x,m.y,m.z),r.setXYZ(y,p.x,p.y,p.z)}else for(let S=0,M=i.count;S<M;S+=3)l.fromBufferAttribute(i,S+0),c.fromBufferAttribute(i,S+1),h.fromBufferAttribute(i,S+2),v.subVectors(h,c),g.subVectors(l,c),v.cross(g),r.setXYZ(S+0,v.x,v.y,v.z),r.setXYZ(S+1,v.x,v.y,v.z),r.setXYZ(S+2,v.x,v.y,v.z);this.normalizeNormals(),r.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let i=0,r=e.count;i<r;i++)mn.fromBufferAttribute(e,i),mn.normalize(),e.setXYZ(i,mn.x,mn.y,mn.z)}toNonIndexed(){function e(d,m){const p=d.array,v=d.itemSize,g=d.normalized,S=new p.constructor(m.length*v);let M=0,A=0;for(let C=0,y=m.length;C<y;C++){d.isInterleavedBufferAttribute?M=m[C]*d.data.stride+d.offset:M=m[C]*v;for(let x=0;x<v;x++)S[A++]=p[M++]}return new Fi(S,v,g)}if(this.index===null)return ae("BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const i=new Hi,r=this.index.array,l=this.attributes;for(const d in l){const m=l[d],p=e(m,r);i.setAttribute(d,p)}const c=this.morphAttributes;for(const d in c){const m=[],p=c[d];for(let v=0,g=p.length;v<g;v++){const S=p[v],M=e(S,r);m.push(M)}i.morphAttributes[d]=m}i.morphTargetsRelative=this.morphTargetsRelative;const h=this.groups;for(let d=0,m=h.length;d<m;d++){const p=h[d];i.addGroup(p.start,p.count,p.materialIndex)}return i}toJSON(){const e={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const m=this.parameters;for(const p in m)m[p]!==void 0&&(e[p]=m[p]);return e}e.data={attributes:{}};const i=this.index;i!==null&&(e.data.index={type:i.array.constructor.name,array:Array.prototype.slice.call(i.array)});const r=this.attributes;for(const m in r){const p=r[m];e.data.attributes[m]=p.toJSON(e.data)}const l={};let c=!1;for(const m in this.morphAttributes){const p=this.morphAttributes[m],v=[];for(let g=0,S=p.length;g<S;g++){const M=p[g];v.push(M.toJSON(e.data))}v.length>0&&(l[m]=v,c=!0)}c&&(e.data.morphAttributes=l,e.data.morphTargetsRelative=this.morphTargetsRelative);const h=this.groups;h.length>0&&(e.data.groups=JSON.parse(JSON.stringify(h)));const d=this.boundingSphere;return d!==null&&(e.data.boundingSphere=d.toJSON()),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const i={};this.name=e.name;const r=e.index;r!==null&&this.setIndex(r.clone());const l=e.attributes;for(const p in l){const v=l[p];this.setAttribute(p,v.clone(i))}const c=e.morphAttributes;for(const p in c){const v=[],g=c[p];for(let S=0,M=g.length;S<M;S++)v.push(g[S].clone(i));this.morphAttributes[p]=v}this.morphTargetsRelative=e.morphTargetsRelative;const h=e.groups;for(let p=0,v=h.length;p<v;p++){const g=h[p];this.addGroup(g.start,g.count,g.materialIndex)}const d=e.boundingBox;d!==null&&(this.boundingBox=d.clone());const m=e.boundingSphere;return m!==null&&(this.boundingSphere=m.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const j0=new tn,vr=new MM,mu=new Pd,K0=new it,gu=new it,_u=new it,vu=new it,_h=new it,xu=new it,Q0=new it,Su=new it;class ga extends Ln{constructor(e=new Hi,i=new J_){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=i,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.count=1,this.updateMorphTargets()}copy(e,i){return super.copy(e,i),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const i=this.geometry.morphAttributes,r=Object.keys(i);if(r.length>0){const l=i[r[0]];if(l!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let c=0,h=l.length;c<h;c++){const d=l[c].name||String(c);this.morphTargetInfluences.push(0),this.morphTargetDictionary[d]=c}}}}getVertexPosition(e,i){const r=this.geometry,l=r.attributes.position,c=r.morphAttributes.position,h=r.morphTargetsRelative;i.fromBufferAttribute(l,e);const d=this.morphTargetInfluences;if(c&&d){xu.set(0,0,0);for(let m=0,p=c.length;m<p;m++){const v=d[m],g=c[m];v!==0&&(_h.fromBufferAttribute(g,e),h?xu.addScaledVector(_h,v):xu.addScaledVector(_h.sub(i),v))}i.add(xu)}return i}raycast(e,i){const r=this.geometry,l=this.material,c=this.matrixWorld;l!==void 0&&(r.boundingSphere===null&&r.computeBoundingSphere(),mu.copy(r.boundingSphere),mu.applyMatrix4(c),vr.copy(e.ray).recast(e.near),!(mu.containsPoint(vr.origin)===!1&&(vr.intersectSphere(mu,K0)===null||vr.origin.distanceToSquared(K0)>(e.far-e.near)**2))&&(j0.copy(c).invert(),vr.copy(e.ray).applyMatrix4(j0),!(r.boundingBox!==null&&vr.intersectsBox(r.boundingBox)===!1)&&this._computeIntersections(e,i,vr)))}_computeIntersections(e,i,r){let l;const c=this.geometry,h=this.material,d=c.index,m=c.attributes.position,p=c.attributes.uv,v=c.attributes.uv1,g=c.attributes.normal,S=c.groups,M=c.drawRange;if(d!==null)if(Array.isArray(h))for(let A=0,C=S.length;A<C;A++){const y=S[A],x=h[y.materialIndex],P=Math.max(y.start,M.start),N=Math.min(d.count,Math.min(y.start+y.count,M.start+M.count));for(let L=P,B=N;L<B;L+=3){const F=d.getX(L),z=d.getX(L+1),Q=d.getX(L+2);l=Mu(this,x,e,r,p,v,g,F,z,Q),l&&(l.faceIndex=Math.floor(L/3),l.face.materialIndex=y.materialIndex,i.push(l))}}else{const A=Math.max(0,M.start),C=Math.min(d.count,M.start+M.count);for(let y=A,x=C;y<x;y+=3){const P=d.getX(y),N=d.getX(y+1),L=d.getX(y+2);l=Mu(this,h,e,r,p,v,g,P,N,L),l&&(l.faceIndex=Math.floor(y/3),i.push(l))}}else if(m!==void 0)if(Array.isArray(h))for(let A=0,C=S.length;A<C;A++){const y=S[A],x=h[y.materialIndex],P=Math.max(y.start,M.start),N=Math.min(m.count,Math.min(y.start+y.count,M.start+M.count));for(let L=P,B=N;L<B;L+=3){const F=L,z=L+1,Q=L+2;l=Mu(this,x,e,r,p,v,g,F,z,Q),l&&(l.faceIndex=Math.floor(L/3),l.face.materialIndex=y.materialIndex,i.push(l))}}else{const A=Math.max(0,M.start),C=Math.min(m.count,M.start+M.count);for(let y=A,x=C;y<x;y+=3){const P=y,N=y+1,L=y+2;l=Mu(this,h,e,r,p,v,g,P,N,L),l&&(l.faceIndex=Math.floor(y/3),i.push(l))}}}}function UM(o,e,i,r,l,c,h,d){let m;if(e.side===Xn?m=r.intersectTriangle(h,c,l,!0,d):m=r.intersectTriangle(l,c,h,e.side===Qa,d),m===null)return null;Su.copy(d),Su.applyMatrix4(o.matrixWorld);const p=i.ray.origin.distanceTo(Su);return p<i.near||p>i.far?null:{distance:p,point:Su.clone(),object:o}}function Mu(o,e,i,r,l,c,h,d,m,p){o.getVertexPosition(d,gu),o.getVertexPosition(m,_u),o.getVertexPosition(p,vu);const v=UM(o,e,i,r,gu,_u,vu,Q0);if(v){const g=new it;Ei.getBarycoord(Q0,gu,_u,vu,g),l&&(v.uv=Ei.getInterpolatedAttribute(l,d,m,p,g,new Ue)),c&&(v.uv1=Ei.getInterpolatedAttribute(c,d,m,p,g,new Ue)),h&&(v.normal=Ei.getInterpolatedAttribute(h,d,m,p,g,new it),v.normal.dot(r.direction)>0&&v.normal.multiplyScalar(-1));const S={a:d,b:m,c:p,normal:new it,materialIndex:0};Ei.getNormal(gu,_u,vu,S.normal),v.face=S,v.barycoord=g}return v}class Yo extends Hi{constructor(e=1,i=1,r=1,l=1,c=1,h=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:i,depth:r,widthSegments:l,heightSegments:c,depthSegments:h};const d=this;l=Math.floor(l),c=Math.floor(c),h=Math.floor(h);const m=[],p=[],v=[],g=[];let S=0,M=0;A("z","y","x",-1,-1,r,i,e,h,c,0),A("z","y","x",1,-1,r,i,-e,h,c,1),A("x","z","y",1,1,e,r,i,l,h,2),A("x","z","y",1,-1,e,r,-i,l,h,3),A("x","y","z",1,-1,e,i,r,l,c,4),A("x","y","z",-1,-1,e,i,-r,l,c,5),this.setIndex(m),this.setAttribute("position",new hi(p,3)),this.setAttribute("normal",new hi(v,3)),this.setAttribute("uv",new hi(g,2));function A(C,y,x,P,N,L,B,F,z,Q,R){const D=L/z,k=B/Q,rt=L/2,at=B/2,ut=F/2,ht=z+1,O=Q+1;let V=0,nt=0;const Mt=new it;for(let xt=0;xt<O;xt++){const U=xt*k-at;for(let et=0;et<ht;et++){const gt=et*D-rt;Mt[C]=gt*P,Mt[y]=U*N,Mt[x]=ut,p.push(Mt.x,Mt.y,Mt.z),Mt[C]=0,Mt[y]=0,Mt[x]=F>0?1:-1,v.push(Mt.x,Mt.y,Mt.z),g.push(et/z),g.push(1-xt/Q),V+=1}}for(let xt=0;xt<Q;xt++)for(let U=0;U<z;U++){const et=S+U+ht*xt,gt=S+U+ht*(xt+1),bt=S+(U+1)+ht*(xt+1),Bt=S+(U+1)+ht*xt;m.push(et,gt,Bt),m.push(gt,bt,Bt),nt+=6}d.addGroup(M,nt,R),M+=nt,S+=V}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Yo(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function ws(o){const e={};for(const i in o){e[i]={};for(const r in o[i]){const l=o[i][r];l&&(l.isColor||l.isMatrix3||l.isMatrix4||l.isVector2||l.isVector3||l.isVector4||l.isTexture||l.isQuaternion)?l.isRenderTargetTexture?(ae("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[i][r]=null):e[i][r]=l.clone():Array.isArray(l)?e[i][r]=l.slice():e[i][r]=l}}return e}function On(o){const e={};for(let i=0;i<o.length;i++){const r=ws(o[i]);for(const l in r)e[l]=r[l]}return e}function LM(o){const e=[];for(let i=0;i<o.length;i++)e.push(o[i].clone());return e}function ev(o){const e=o.getRenderTarget();return e===null?o.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:ye.workingColorSpace}const NM={clone:ws,merge:On};var OM=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,PM=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class Ii extends qo{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=OM,this.fragmentShader=PM,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=ws(e.uniforms),this.uniformsGroups=LM(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this.defaultAttributeValues=Object.assign({},e.defaultAttributeValues),this.index0AttributeName=e.index0AttributeName,this.uniformsNeedUpdate=e.uniformsNeedUpdate,this}toJSON(e){const i=super.toJSON(e);i.glslVersion=this.glslVersion,i.uniforms={};for(const l in this.uniforms){const h=this.uniforms[l].value;h&&h.isTexture?i.uniforms[l]={type:"t",value:h.toJSON(e).uuid}:h&&h.isColor?i.uniforms[l]={type:"c",value:h.getHex()}:h&&h.isVector2?i.uniforms[l]={type:"v2",value:h.toArray()}:h&&h.isVector3?i.uniforms[l]={type:"v3",value:h.toArray()}:h&&h.isVector4?i.uniforms[l]={type:"v4",value:h.toArray()}:h&&h.isMatrix3?i.uniforms[l]={type:"m3",value:h.toArray()}:h&&h.isMatrix4?i.uniforms[l]={type:"m4",value:h.toArray()}:i.uniforms[l]={value:h}}Object.keys(this.defines).length>0&&(i.defines=this.defines),i.vertexShader=this.vertexShader,i.fragmentShader=this.fragmentShader,i.lights=this.lights,i.clipping=this.clipping;const r={};for(const l in this.extensions)this.extensions[l]===!0&&(r[l]=!0);return Object.keys(r).length>0&&(i.extensions=r),i}}class nv extends Ln{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new tn,this.projectionMatrix=new tn,this.projectionMatrixInverse=new tn,this.coordinateSystem=Ni,this._reversedDepth=!1}get reversedDepth(){return this._reversedDepth}copy(e,i){return super.copy(e,i),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,i){super.updateWorldMatrix(e,i),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}const Za=new it,J0=new Ue,$0=new Ue;class yi extends nv{constructor(e=50,i=1,r=.1,l=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=r,this.far=l,this.focus=10,this.aspect=i,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,i){return super.copy(e,i),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const i=.5*this.getFilmHeight()/e;this.fov=yd*2*Math.atan(i),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(Kf*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return yd*2*Math.atan(Math.tan(Kf*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,i,r){Za.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),i.set(Za.x,Za.y).multiplyScalar(-e/Za.z),Za.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),r.set(Za.x,Za.y).multiplyScalar(-e/Za.z)}getViewSize(e,i){return this.getViewBounds(e,J0,$0),i.subVectors($0,J0)}setViewOffset(e,i,r,l,c,h){this.aspect=e/i,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=i,this.view.offsetX=r,this.view.offsetY=l,this.view.width=c,this.view.height=h,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let i=e*Math.tan(Kf*.5*this.fov)/this.zoom,r=2*i,l=this.aspect*r,c=-.5*l;const h=this.view;if(this.view!==null&&this.view.enabled){const m=h.fullWidth,p=h.fullHeight;c+=h.offsetX*l/m,i-=h.offsetY*r/p,l*=h.width/m,r*=h.height/p}const d=this.filmOffset;d!==0&&(c+=e*d/this.getFilmWidth()),this.projectionMatrix.makePerspective(c,c+l,i,i-r,e,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const i=super.toJSON(e);return i.object.fov=this.fov,i.object.zoom=this.zoom,i.object.near=this.near,i.object.far=this.far,i.object.focus=this.focus,i.object.aspect=this.aspect,this.view!==null&&(i.object.view=Object.assign({},this.view)),i.object.filmGauge=this.filmGauge,i.object.filmOffset=this.filmOffset,i}}const Ms=-90,ys=1;class FM extends Ln{constructor(e,i,r){super(),this.type="CubeCamera",this.renderTarget=r,this.coordinateSystem=null,this.activeMipmapLevel=0;const l=new yi(Ms,ys,e,i);l.layers=this.layers,this.add(l);const c=new yi(Ms,ys,e,i);c.layers=this.layers,this.add(c);const h=new yi(Ms,ys,e,i);h.layers=this.layers,this.add(h);const d=new yi(Ms,ys,e,i);d.layers=this.layers,this.add(d);const m=new yi(Ms,ys,e,i);m.layers=this.layers,this.add(m);const p=new yi(Ms,ys,e,i);p.layers=this.layers,this.add(p)}updateCoordinateSystem(){const e=this.coordinateSystem,i=this.children.concat(),[r,l,c,h,d,m]=i;for(const p of i)this.remove(p);if(e===Ni)r.up.set(0,1,0),r.lookAt(1,0,0),l.up.set(0,1,0),l.lookAt(-1,0,0),c.up.set(0,0,-1),c.lookAt(0,1,0),h.up.set(0,0,1),h.lookAt(0,-1,0),d.up.set(0,1,0),d.lookAt(0,0,1),m.up.set(0,1,0),m.lookAt(0,0,-1);else if(e===Nu)r.up.set(0,-1,0),r.lookAt(-1,0,0),l.up.set(0,-1,0),l.lookAt(1,0,0),c.up.set(0,0,1),c.lookAt(0,1,0),h.up.set(0,0,-1),h.lookAt(0,-1,0),d.up.set(0,-1,0),d.lookAt(0,0,1),m.up.set(0,-1,0),m.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const p of i)this.add(p),p.updateMatrixWorld()}update(e,i){this.parent===null&&this.updateMatrixWorld();const{renderTarget:r,activeMipmapLevel:l}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[c,h,d,m,p,v]=this.children,g=e.getRenderTarget(),S=e.getActiveCubeFace(),M=e.getActiveMipmapLevel(),A=e.xr.enabled;e.xr.enabled=!1;const C=r.texture.generateMipmaps;r.texture.generateMipmaps=!1,e.setRenderTarget(r,0,l),e.render(i,c),e.setRenderTarget(r,1,l),e.render(i,h),e.setRenderTarget(r,2,l),e.render(i,d),e.setRenderTarget(r,3,l),e.render(i,m),e.setRenderTarget(r,4,l),e.render(i,p),r.texture.generateMipmaps=C,e.setRenderTarget(r,5,l),e.render(i,v),e.setRenderTarget(g,S,M),e.xr.enabled=A,r.texture.needsPMREMUpdate=!0}}class iv extends Pn{constructor(e=[],i=Rr,r,l,c,h,d,m,p,v){super(e,i,r,l,c,h,d,m,p,v),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class av extends Pi{constructor(e=1,i={}){super(e,e,i),this.isWebGLCubeRenderTarget=!0;const r={width:e,height:e,depth:1},l=[r,r,r,r,r,r];this.texture=new iv(l),this._setTextureOptions(i),this.texture.isRenderTargetTexture=!0}fromEquirectangularTexture(e,i){this.texture.type=i.type,this.texture.colorSpace=i.colorSpace,this.texture.generateMipmaps=i.generateMipmaps,this.texture.minFilter=i.minFilter,this.texture.magFilter=i.magFilter;const r={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},l=new Yo(5,5,5),c=new Ii({name:"CubemapFromEquirect",uniforms:ws(r.uniforms),vertexShader:r.vertexShader,fragmentShader:r.fragmentShader,side:Xn,blending:ha});c.uniforms.tEquirect.value=i;const h=new ga(l,c),d=i.minFilter;return i.minFilter===br&&(i.minFilter=Un),new FM(1,10,this).update(e,h),i.minFilter=d,h.geometry.dispose(),h.material.dispose(),this}clear(e,i=!0,r=!0,l=!0){const c=e.getRenderTarget();for(let h=0;h<6;h++)e.setRenderTarget(this,h),e.clear(i,r,l);e.setRenderTarget(c)}}class yu extends Ln{constructor(){super(),this.isGroup=!0,this.type="Group"}}const zM={type:"move"};class vh{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new yu,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new yu,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new it,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new it),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new yu,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new it,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new it),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const i=this._hand;if(i)for(const r of e.hand.values())this._getHandJoint(i,r)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,i,r){let l=null,c=null,h=null;const d=this._targetRay,m=this._grip,p=this._hand;if(e&&i.session.visibilityState!=="visible-blurred"){if(p&&e.hand){h=!0;for(const C of e.hand.values()){const y=i.getJointPose(C,r),x=this._getHandJoint(p,C);y!==null&&(x.matrix.fromArray(y.transform.matrix),x.matrix.decompose(x.position,x.rotation,x.scale),x.matrixWorldNeedsUpdate=!0,x.jointRadius=y.radius),x.visible=y!==null}const v=p.joints["index-finger-tip"],g=p.joints["thumb-tip"],S=v.position.distanceTo(g.position),M=.02,A=.005;p.inputState.pinching&&S>M+A?(p.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!p.inputState.pinching&&S<=M-A&&(p.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else m!==null&&e.gripSpace&&(c=i.getPose(e.gripSpace,r),c!==null&&(m.matrix.fromArray(c.transform.matrix),m.matrix.decompose(m.position,m.rotation,m.scale),m.matrixWorldNeedsUpdate=!0,c.linearVelocity?(m.hasLinearVelocity=!0,m.linearVelocity.copy(c.linearVelocity)):m.hasLinearVelocity=!1,c.angularVelocity?(m.hasAngularVelocity=!0,m.angularVelocity.copy(c.angularVelocity)):m.hasAngularVelocity=!1));d!==null&&(l=i.getPose(e.targetRaySpace,r),l===null&&c!==null&&(l=c),l!==null&&(d.matrix.fromArray(l.transform.matrix),d.matrix.decompose(d.position,d.rotation,d.scale),d.matrixWorldNeedsUpdate=!0,l.linearVelocity?(d.hasLinearVelocity=!0,d.linearVelocity.copy(l.linearVelocity)):d.hasLinearVelocity=!1,l.angularVelocity?(d.hasAngularVelocity=!0,d.angularVelocity.copy(l.angularVelocity)):d.hasAngularVelocity=!1,this.dispatchEvent(zM)))}return d!==null&&(d.visible=l!==null),m!==null&&(m.visible=c!==null),p!==null&&(p.visible=h!==null),this}_getHandJoint(e,i){if(e.joints[i.jointName]===void 0){const r=new yu;r.matrixAutoUpdate=!1,r.visible=!1,e.joints[i.jointName]=r,e.add(r)}return e.joints[i.jointName]}}class $A extends Ln{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new Bi,this.environmentIntensity=1,this.environmentRotation=new Bi,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,i){return super.copy(e,i),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const i=super.toJSON(e);return this.fog!==null&&(i.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(i.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(i.object.backgroundIntensity=this.backgroundIntensity),i.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(i.object.environmentIntensity=this.environmentIntensity),i.object.environmentRotation=this.environmentRotation.toArray(),i}}class BM extends Pn{constructor(e=null,i=1,r=1,l,c,h,d,m,p=An,v=An,g,S){super(null,h,d,m,p,v,l,c,g,S),this.isDataTexture=!0,this.image={data:e,width:i,height:r},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}const xh=new it,IM=new it,HM=new ue;class yr{constructor(e=new it(1,0,0),i=0){this.isPlane=!0,this.normal=e,this.constant=i}set(e,i){return this.normal.copy(e),this.constant=i,this}setComponents(e,i,r,l){return this.normal.set(e,i,r),this.constant=l,this}setFromNormalAndCoplanarPoint(e,i){return this.normal.copy(e),this.constant=-i.dot(this.normal),this}setFromCoplanarPoints(e,i,r){const l=xh.subVectors(r,i).cross(IM.subVectors(e,i)).normalize();return this.setFromNormalAndCoplanarPoint(l,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,i){return i.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,i){const r=e.delta(xh),l=this.normal.dot(r);if(l===0)return this.distanceToPoint(e.start)===0?i.copy(e.start):null;const c=-(e.start.dot(this.normal)+this.constant)/l;return c<0||c>1?null:i.copy(e.start).addScaledVector(r,c)}intersectsLine(e){const i=this.distanceToPoint(e.start),r=this.distanceToPoint(e.end);return i<0&&r>0||r<0&&i>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,i){const r=i||HM.getNormalMatrix(e),l=this.coplanarPoint(xh).applyMatrix4(e),c=this.normal.applyMatrix3(r).normalize();return this.constant=-l.dot(c),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const xr=new Pd,GM=new Ue(.5,.5),Eu=new it;class Fd{constructor(e=new yr,i=new yr,r=new yr,l=new yr,c=new yr,h=new yr){this.planes=[e,i,r,l,c,h]}set(e,i,r,l,c,h){const d=this.planes;return d[0].copy(e),d[1].copy(i),d[2].copy(r),d[3].copy(l),d[4].copy(c),d[5].copy(h),this}copy(e){const i=this.planes;for(let r=0;r<6;r++)i[r].copy(e.planes[r]);return this}setFromProjectionMatrix(e,i=Ni,r=!1){const l=this.planes,c=e.elements,h=c[0],d=c[1],m=c[2],p=c[3],v=c[4],g=c[5],S=c[6],M=c[7],A=c[8],C=c[9],y=c[10],x=c[11],P=c[12],N=c[13],L=c[14],B=c[15];if(l[0].setComponents(p-h,M-v,x-A,B-P).normalize(),l[1].setComponents(p+h,M+v,x+A,B+P).normalize(),l[2].setComponents(p+d,M+g,x+C,B+N).normalize(),l[3].setComponents(p-d,M-g,x-C,B-N).normalize(),r)l[4].setComponents(m,S,y,L).normalize(),l[5].setComponents(p-m,M-S,x-y,B-L).normalize();else if(l[4].setComponents(p-m,M-S,x-y,B-L).normalize(),i===Ni)l[5].setComponents(p+m,M+S,x+y,B+L).normalize();else if(i===Nu)l[5].setComponents(m,S,y,L).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+i);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),xr.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const i=e.geometry;i.boundingSphere===null&&i.computeBoundingSphere(),xr.copy(i.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(xr)}intersectsSprite(e){xr.center.set(0,0,0);const i=GM.distanceTo(e.center);return xr.radius=.7071067811865476+i,xr.applyMatrix4(e.matrixWorld),this.intersectsSphere(xr)}intersectsSphere(e){const i=this.planes,r=e.center,l=-e.radius;for(let c=0;c<6;c++)if(i[c].distanceToPoint(r)<l)return!1;return!0}intersectsBox(e){const i=this.planes;for(let r=0;r<6;r++){const l=i[r];if(Eu.x=l.normal.x>0?e.max.x:e.min.x,Eu.y=l.normal.y>0?e.max.y:e.min.y,Eu.z=l.normal.z>0?e.max.z:e.min.z,l.distanceToPoint(Eu)<0)return!1}return!0}containsPoint(e){const i=this.planes;for(let r=0;r<6;r++)if(i[r].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}class Go extends Pn{constructor(e,i,r=zi,l,c,h,d=An,m=An,p,v=ma,g=1){if(v!==ma&&v!==Ar)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");const S={width:e,height:i,depth:g};super(S,l,c,h,d,m,v,r,p),this.isDepthTexture=!0,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Od(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){const i=super.toJSON(e);return this.compareFunction!==null&&(i.compareFunction=this.compareFunction),i}}class VM extends Go{constructor(e,i=zi,r=Rr,l,c,h=An,d=An,m,p=ma){const v={width:e,height:e,depth:1},g=[v,v,v,v,v,v];super(e,e,i,r,l,c,h,d,m,p),this.image=g,this.isCubeDepthTexture=!0,this.isCubeTexture=!0}get images(){return this.image}set images(e){this.image=e}}class rv extends Pn{constructor(e=null){super(),this.sourceTexture=e,this.isExternalTexture=!0}copy(e){return super.copy(e),this.sourceTexture=e.sourceTexture,this}}class Fu extends Hi{constructor(e=1,i=1,r=1,l=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:i,widthSegments:r,heightSegments:l};const c=e/2,h=i/2,d=Math.floor(r),m=Math.floor(l),p=d+1,v=m+1,g=e/d,S=i/m,M=[],A=[],C=[],y=[];for(let x=0;x<v;x++){const P=x*S-h;for(let N=0;N<p;N++){const L=N*g-c;A.push(L,-P,0),C.push(0,0,1),y.push(N/d),y.push(1-x/m)}}for(let x=0;x<m;x++)for(let P=0;P<d;P++){const N=P+p*x,L=P+p*(x+1),B=P+1+p*(x+1),F=P+1+p*x;M.push(N,L,F),M.push(L,B,F)}this.setIndex(M),this.setAttribute("position",new hi(A,3)),this.setAttribute("normal",new hi(C,3)),this.setAttribute("uv",new hi(y,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Fu(e.width,e.height,e.widthSegments,e.heightSegments)}}class sv extends Hi{constructor(e=1,i=32,r=16,l=0,c=Math.PI*2,h=0,d=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:i,heightSegments:r,phiStart:l,phiLength:c,thetaStart:h,thetaLength:d},i=Math.max(3,Math.floor(i)),r=Math.max(2,Math.floor(r));const m=Math.min(h+d,Math.PI);let p=0;const v=[],g=new it,S=new it,M=[],A=[],C=[],y=[];for(let x=0;x<=r;x++){const P=[],N=x/r;let L=0;x===0&&h===0?L=.5/i:x===r&&m===Math.PI&&(L=-.5/i);for(let B=0;B<=i;B++){const F=B/i;g.x=-e*Math.cos(l+F*c)*Math.sin(h+N*d),g.y=e*Math.cos(h+N*d),g.z=e*Math.sin(l+F*c)*Math.sin(h+N*d),A.push(g.x,g.y,g.z),S.copy(g).normalize(),C.push(S.x,S.y,S.z),y.push(F+L,1-N),P.push(p++)}v.push(P)}for(let x=0;x<r;x++)for(let P=0;P<i;P++){const N=v[x][P+1],L=v[x][P],B=v[x+1][P],F=v[x+1][P+1];(x!==0||h>0)&&M.push(N,L,F),(x!==r-1||m<Math.PI)&&M.push(L,B,F)}this.setIndex(M),this.setAttribute("position",new hi(A,3)),this.setAttribute("normal",new hi(C,3)),this.setAttribute("uv",new hi(y,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new sv(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class XM extends Ii{constructor(e){super(e),this.isRawShaderMaterial=!0,this.type="RawShaderMaterial"}}class t1 extends qo{constructor(e){super(),this.isMeshStandardMaterial=!0,this.type="MeshStandardMaterial",this.defines={STANDARD:""},this.color=new we(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new we(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=Y_,this.normalScale=new Ue(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Bi,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class kM extends qo{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=iM,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class WM extends qo{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}class ov extends Ln{constructor(e,i=1){super(),this.isLight=!0,this.type="Light",this.color=new we(e),this.intensity=i}dispose(){this.dispatchEvent({type:"dispose"})}copy(e,i){return super.copy(e,i),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const i=super.toJSON(e);return i.object.color=this.color.getHex(),i.object.intensity=this.intensity,i}}const Sh=new tn,t_=new it,e_=new it;class qM{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new Ue(512,512),this.mapType=$n,this.map=null,this.mapPass=null,this.matrix=new tn,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Fd,this._frameExtents=new Ue(1,1),this._viewportCount=1,this._viewports=[new $e(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const i=this.camera,r=this.matrix;t_.setFromMatrixPosition(e.matrixWorld),i.position.copy(t_),e_.setFromMatrixPosition(e.target.matrixWorld),i.lookAt(e_),i.updateMatrixWorld(),Sh.multiplyMatrices(i.projectionMatrix,i.matrixWorldInverse),this._frustum.setFromProjectionMatrix(Sh,i.coordinateSystem,i.reversedDepth),i.reversedDepth?r.set(.5,0,0,.5,0,.5,0,.5,0,0,1,0,0,0,0,1):r.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),r.multiply(Sh)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.autoUpdate=e.autoUpdate,this.needsUpdate=e.needsUpdate,this.normalBias=e.normalBias,this.blurSamples=e.blurSamples,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.intensity!==1&&(e.intensity=this.intensity),this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class zd extends nv{constructor(e=-1,i=1,r=1,l=-1,c=.1,h=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=i,this.top=r,this.bottom=l,this.near=c,this.far=h,this.updateProjectionMatrix()}copy(e,i){return super.copy(e,i),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,i,r,l,c,h){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=i,this.view.offsetX=r,this.view.offsetY=l,this.view.width=c,this.view.height=h,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),i=(this.top-this.bottom)/(2*this.zoom),r=(this.right+this.left)/2,l=(this.top+this.bottom)/2;let c=r-e,h=r+e,d=l+i,m=l-i;if(this.view!==null&&this.view.enabled){const p=(this.right-this.left)/this.view.fullWidth/this.zoom,v=(this.top-this.bottom)/this.view.fullHeight/this.zoom;c+=p*this.view.offsetX,h=c+p*this.view.width,d-=v*this.view.offsetY,m=d-v*this.view.height}this.projectionMatrix.makeOrthographic(c,h,d,m,this.near,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const i=super.toJSON(e);return i.object.zoom=this.zoom,i.object.left=this.left,i.object.right=this.right,i.object.top=this.top,i.object.bottom=this.bottom,i.object.near=this.near,i.object.far=this.far,this.view!==null&&(i.object.view=Object.assign({},this.view)),i}}class YM extends qM{constructor(){super(new zd(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class e1 extends ov{constructor(e,i){super(e,i),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Ln.DEFAULT_UP),this.updateMatrix(),this.target=new Ln,this.shadow=new YM}dispose(){super.dispose(),this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}toJSON(e){const i=super.toJSON(e);return i.object.shadow=this.shadow.toJSON(),i.object.target=this.target.uuid,i}}class n1 extends ov{constructor(e,i){super(e,i),this.isAmbientLight=!0,this.type="AmbientLight"}}class ZM extends yi{constructor(e=[]){super(),this.isArrayCamera=!0,this.isMultiViewCamera=!1,this.cameras=e}}function n_(o,e,i,r){const l=jM(r);switch(i){case k_:return o*e;case q_:return o*e/l.components*l.byteLength;case Dd:return o*e/l.components*l.byteLength;case Cs:return o*e*2/l.components*l.byteLength;case wd:return o*e*2/l.components*l.byteLength;case W_:return o*e*3/l.components*l.byteLength;case Ti:return o*e*4/l.components*l.byteLength;case Ud:return o*e*4/l.components*l.byteLength;case Ru:case Cu:return Math.floor((o+3)/4)*Math.floor((e+3)/4)*8;case Du:case wu:return Math.floor((o+3)/4)*Math.floor((e+3)/4)*16;case Wh:case Yh:return Math.max(o,16)*Math.max(e,8)/4;case kh:case qh:return Math.max(o,8)*Math.max(e,8)/2;case Zh:case jh:case Qh:case Jh:return Math.floor((o+3)/4)*Math.floor((e+3)/4)*8;case Kh:case $h:case td:return Math.floor((o+3)/4)*Math.floor((e+3)/4)*16;case ed:return Math.floor((o+3)/4)*Math.floor((e+3)/4)*16;case nd:return Math.floor((o+4)/5)*Math.floor((e+3)/4)*16;case id:return Math.floor((o+4)/5)*Math.floor((e+4)/5)*16;case ad:return Math.floor((o+5)/6)*Math.floor((e+4)/5)*16;case rd:return Math.floor((o+5)/6)*Math.floor((e+5)/6)*16;case sd:return Math.floor((o+7)/8)*Math.floor((e+4)/5)*16;case od:return Math.floor((o+7)/8)*Math.floor((e+5)/6)*16;case ld:return Math.floor((o+7)/8)*Math.floor((e+7)/8)*16;case ud:return Math.floor((o+9)/10)*Math.floor((e+4)/5)*16;case cd:return Math.floor((o+9)/10)*Math.floor((e+5)/6)*16;case fd:return Math.floor((o+9)/10)*Math.floor((e+7)/8)*16;case hd:return Math.floor((o+9)/10)*Math.floor((e+9)/10)*16;case dd:return Math.floor((o+11)/12)*Math.floor((e+9)/10)*16;case pd:return Math.floor((o+11)/12)*Math.floor((e+11)/12)*16;case md:case gd:case _d:return Math.ceil(o/4)*Math.ceil(e/4)*16;case vd:case xd:return Math.ceil(o/4)*Math.ceil(e/4)*8;case Sd:case Md:return Math.ceil(o/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${i} format.`)}function jM(o){switch(o){case $n:case H_:return{byteLength:1,components:1};case Bo:case G_:case pa:return{byteLength:2,components:1};case Rd:case Cd:return{byteLength:2,components:4};case zi:case Ad:case Li:return{byteLength:4,components:1};case V_:case X_:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${o}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:bd}}));typeof window<"u"&&(window.__THREE__?ae("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=bd);function lv(){let o=null,e=!1,i=null,r=null;function l(c,h){i(c,h),r=o.requestAnimationFrame(l)}return{start:function(){e!==!0&&i!==null&&(r=o.requestAnimationFrame(l),e=!0)},stop:function(){o.cancelAnimationFrame(r),e=!1},setAnimationLoop:function(c){i=c},setContext:function(c){o=c}}}function KM(o){const e=new WeakMap;function i(d,m){const p=d.array,v=d.usage,g=p.byteLength,S=o.createBuffer();o.bindBuffer(m,S),o.bufferData(m,p,v),d.onUploadCallback();let M;if(p instanceof Float32Array)M=o.FLOAT;else if(typeof Float16Array<"u"&&p instanceof Float16Array)M=o.HALF_FLOAT;else if(p instanceof Uint16Array)d.isFloat16BufferAttribute?M=o.HALF_FLOAT:M=o.UNSIGNED_SHORT;else if(p instanceof Int16Array)M=o.SHORT;else if(p instanceof Uint32Array)M=o.UNSIGNED_INT;else if(p instanceof Int32Array)M=o.INT;else if(p instanceof Int8Array)M=o.BYTE;else if(p instanceof Uint8Array)M=o.UNSIGNED_BYTE;else if(p instanceof Uint8ClampedArray)M=o.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+p);return{buffer:S,type:M,bytesPerElement:p.BYTES_PER_ELEMENT,version:d.version,size:g}}function r(d,m,p){const v=m.array,g=m.updateRanges;if(o.bindBuffer(p,d),g.length===0)o.bufferSubData(p,0,v);else{g.sort((M,A)=>M.start-A.start);let S=0;for(let M=1;M<g.length;M++){const A=g[S],C=g[M];C.start<=A.start+A.count+1?A.count=Math.max(A.count,C.start+C.count-A.start):(++S,g[S]=C)}g.length=S+1;for(let M=0,A=g.length;M<A;M++){const C=g[M];o.bufferSubData(p,C.start*v.BYTES_PER_ELEMENT,v,C.start,C.count)}m.clearUpdateRanges()}m.onUploadCallback()}function l(d){return d.isInterleavedBufferAttribute&&(d=d.data),e.get(d)}function c(d){d.isInterleavedBufferAttribute&&(d=d.data);const m=e.get(d);m&&(o.deleteBuffer(m.buffer),e.delete(d))}function h(d,m){if(d.isInterleavedBufferAttribute&&(d=d.data),d.isGLBufferAttribute){const v=e.get(d);(!v||v.version<d.version)&&e.set(d,{buffer:d.buffer,type:d.type,bytesPerElement:d.elementSize,version:d.version});return}const p=e.get(d);if(p===void 0)e.set(d,i(d,m));else if(p.version<d.version){if(p.size!==d.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");r(p.buffer,d,m),p.version=d.version}}return{get:l,remove:c,update:h}}var QM=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,JM=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,$M=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,ty=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,ey=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,ny=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,iy=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,ay=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,ry=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec3 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 ).rgb;
	}
#endif`,sy=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,oy=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,ly=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,uy=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,cy=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,fy=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,hy=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,dy=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,py=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,my=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,gy=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,_y=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,vy=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec3 vColor;
#endif`,xy=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif
#ifdef USE_BATCHING_COLOR
	vec3 batchingColor = getBatchingColor( getIndirectIndex( gl_DrawID ) );
	vColor.xyz *= batchingColor.xyz;
#endif`,Sy=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,My=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,yy=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
	#ifdef FLIP_SIDED
		transformedTangent = - transformedTangent;
	#endif
#endif`,Ey=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Ty=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,by=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,Ay=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Ry="gl_FragColor = linearToOutputTexel( gl_FragColor );",Cy=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Dy=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * vec3( flipEnvMap * reflectVec.x, reflectVec.yz ) );
	#else
		vec4 envColor = vec4( 0.0 );
	#endif
	#ifdef ENVMAP_BLENDING_MULTIPLY
		outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_MIX )
		outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
	#elif defined( ENVMAP_BLENDING_ADD )
		outgoingLight += envColor.xyz * specularStrength * reflectivity;
	#endif
#endif`,wy=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
#endif`,Uy=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,Ly=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Ny=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,Oy=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Py=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,Fy=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,zy=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,By=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,Iy=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,Hy=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Gy=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Vy=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif`,Xy=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, pow4( roughness ) ) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
#endif`,ky=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,Wy=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,qy=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Yy=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Zy=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.diffuseContribution = diffuseColor.rgb * ( 1.0 - metalnessFactor );
material.metalness = metalnessFactor;
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor;
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = vec3( 0.04 );
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.0001, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,jy=`uniform sampler2D dfgLUT;
struct PhysicalMaterial {
	vec3 diffuseColor;
	vec3 diffuseContribution;
	vec3 specularColor;
	vec3 specularColorBlended;
	float roughness;
	float metalness;
	float specularF90;
	float dispersion;
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0;
		vec3 iridescenceFresnelDielectric;
		vec3 iridescenceFresnelMetallic;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		float v = 0.5 / ( gv + gl );
		return v;
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColorBlended;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transpose( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float rInv = 1.0 / ( roughness + 0.1 );
	float a = -1.9362 + 1.0678 * roughness + 0.4573 * r2 - 0.8469 * rInv;
	float b = -0.6014 + 0.5538 * roughness - 0.4670 * r2 - 0.1255 * rInv;
	float DG = exp( a * dotNV + b );
	return saturate( DG );
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 fab = texture2D( dfgLUT, vec2( roughness, dotNV ) ).rg;
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 fab = texture2D( dfgLUT, vec2( roughness, dotNV ) ).rg;
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
vec3 BRDF_GGX_Multiscatter( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 singleScatter = BRDF_GGX( lightDir, viewDir, normal, material );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 dfgV = texture2D( dfgLUT, vec2( material.roughness, dotNV ) ).rg;
	vec2 dfgL = texture2D( dfgLUT, vec2( material.roughness, dotNL ) ).rg;
	vec3 FssEss_V = material.specularColorBlended * dfgV.x + material.specularF90 * dfgV.y;
	vec3 FssEss_L = material.specularColorBlended * dfgL.x + material.specularF90 * dfgL.y;
	float Ess_V = dfgV.x + dfgV.y;
	float Ess_L = dfgL.x + dfgL.y;
	float Ems_V = 1.0 - Ess_V;
	float Ems_L = 1.0 - Ess_L;
	vec3 Favg = material.specularColorBlended + ( 1.0 - material.specularColorBlended ) * 0.047619;
	vec3 Fms = FssEss_V * FssEss_L * Favg / ( 1.0 - Ems_V * Ems_L * Favg + EPSILON );
	float compensationFactor = Ems_V * Ems_L;
	vec3 multiScatter = Fms * compensationFactor;
	return singleScatter + multiScatter;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColorBlended * t2.x + ( vec3( 1.0 ) - material.specularColorBlended ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseContribution * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
 
 		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
 
 		float sheenAlbedoV = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
 		float sheenAlbedoL = IBLSheenBRDF( geometryNormal, directLight.direction, material.sheenRoughness );
 
 		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * max( sheenAlbedoV, sheenAlbedoL );
 
 		irradiance *= sheenEnergyComp;
 
 	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX_Multiscatter( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 diffuse = irradiance * BRDF_Lambert( material.diffuseContribution );
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		diffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectDiffuse += diffuse;
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness ) * RECIPROCAL_PI;
 	#endif
	vec3 singleScatteringDielectric = vec3( 0.0 );
	vec3 multiScatteringDielectric = vec3( 0.0 );
	vec3 singleScatteringMetallic = vec3( 0.0 );
	vec3 multiScatteringMetallic = vec3( 0.0 );
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnelDielectric, material.roughness, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.diffuseColor, material.specularF90, material.iridescence, material.iridescenceFresnelMetallic, material.roughness, singleScatteringMetallic, multiScatteringMetallic );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscattering( geometryNormal, geometryViewDir, material.diffuseColor, material.specularF90, material.roughness, singleScatteringMetallic, multiScatteringMetallic );
	#endif
	vec3 singleScattering = mix( singleScatteringDielectric, singleScatteringMetallic, material.metalness );
	vec3 multiScattering = mix( multiScatteringDielectric, multiScatteringMetallic, material.metalness );
	vec3 totalScatteringDielectric = singleScatteringDielectric + multiScatteringDielectric;
	vec3 diffuse = material.diffuseContribution * ( 1.0 - totalScatteringDielectric );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	vec3 indirectSpecular = radiance * singleScattering;
	indirectSpecular += multiScattering * cosineWeightedIrradiance;
	vec3 indirectDiffuse = diffuse * cosineWeightedIrradiance;
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		indirectSpecular *= sheenEnergyComp;
		indirectDiffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectSpecular += indirectSpecular;
	reflectedLight.indirectDiffuse += indirectDiffuse;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,Ky=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		material.iridescenceFresnelDielectric = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		material.iridescenceFresnelMetallic = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.diffuseColor );
		material.iridescenceFresnel = mix( material.iridescenceFresnelDielectric, material.iridescenceFresnelMetallic, material.metalness );
		material.iridescenceF0 = Schlick_to_F0( material.iridescenceFresnel, 1.0, dotNVi );
	}
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS ) && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,Qy=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD ) && defined( ENVMAP_TYPE_CUBE_UV )
		iblIrradiance += getIBLIrradiance( geometryNormal );
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		radiance += getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		radiance += getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,Jy=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,$y=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,tE=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,eE=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,nE=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,iE=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,aE=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,rE=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,sE=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,oE=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,lE=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,uE=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,cE=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,fE=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,hE=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,dE=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,pE=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,mE=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,gE=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,_E=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,vE=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,xE=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,SE=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,ME=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,yE=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,EE=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,TE=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,bE=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return depth * ( near - far ) - near;
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	return ( near * far ) / ( ( far - near ) * depth - far );
}`,AE=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,RE=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,CE=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,DE=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,wE=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,UE=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,LE=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#else
			uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#endif
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#else
			uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#endif
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform samplerCubeShadow pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#elif defined( SHADOWMAP_TYPE_BASIC )
			uniform samplerCube pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#endif
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float interleavedGradientNoise( vec2 position ) {
			return fract( 52.9829189 * fract( dot( position, vec2( 0.06711056, 0.00583715 ) ) ) );
		}
		vec2 vogelDiskSample( int sampleIndex, int samplesCount, float phi ) {
			const float goldenAngle = 2.399963229728653;
			float r = sqrt( ( float( sampleIndex ) + 0.5 ) / float( samplesCount ) );
			float theta = float( sampleIndex ) * goldenAngle + phi;
			return vec2( cos( theta ), sin( theta ) ) * r;
		}
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float getShadow( sampler2DShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			shadowCoord.z += shadowBias;
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
				float radius = shadowRadius * texelSize.x;
				float phi = interleavedGradientNoise( gl_FragCoord.xy ) * 6.28318530718;
				shadow = (
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 0, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 1, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 2, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 3, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 4, 5, phi ) * radius, shadowCoord.z ) )
				) * 0.2;
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#elif defined( SHADOWMAP_TYPE_VSM )
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			shadowCoord.z += shadowBias;
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 distribution = texture2D( shadowMap, shadowCoord.xy ).rg;
				float mean = distribution.x;
				float variance = distribution.y * distribution.y;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					float hard_shadow = step( mean, shadowCoord.z );
				#else
					float hard_shadow = step( shadowCoord.z, mean );
				#endif
				if ( hard_shadow == 1.0 ) {
					shadow = 1.0;
				} else {
					variance = max( variance, 0.0000001 );
					float d = shadowCoord.z - mean;
					float p_max = variance / ( variance + d * d );
					p_max = clamp( ( p_max - 0.3 ) / 0.65, 0.0, 1.0 );
					shadow = max( hard_shadow, p_max );
				}
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#else
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			shadowCoord.z += shadowBias;
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				float depth = texture2D( shadowMap, shadowCoord.xy ).r;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					shadow = step( depth, shadowCoord.z );
				#else
					shadow = step( shadowCoord.z, depth );
				#endif
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	#if defined( SHADOWMAP_TYPE_PCF )
	float getPointShadow( samplerCubeShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 bd3D = normalize( lightToPosition );
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
			dp += shadowBias;
			float texelSize = shadowRadius / shadowMapSize.x;
			vec3 absDir = abs( bd3D );
			vec3 tangent = absDir.x > absDir.z ? vec3( 0.0, 1.0, 0.0 ) : vec3( 1.0, 0.0, 0.0 );
			tangent = normalize( cross( bd3D, tangent ) );
			vec3 bitangent = cross( bd3D, tangent );
			float phi = interleavedGradientNoise( gl_FragCoord.xy ) * 6.28318530718;
			shadow = (
				texture( shadowMap, vec4( bd3D + ( tangent * vogelDiskSample( 0, 5, phi ).x + bitangent * vogelDiskSample( 0, 5, phi ).y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * vogelDiskSample( 1, 5, phi ).x + bitangent * vogelDiskSample( 1, 5, phi ).y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * vogelDiskSample( 2, 5, phi ).x + bitangent * vogelDiskSample( 2, 5, phi ).y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * vogelDiskSample( 3, 5, phi ).x + bitangent * vogelDiskSample( 3, 5, phi ).y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * vogelDiskSample( 4, 5, phi ).x + bitangent * vogelDiskSample( 4, 5, phi ).y ) * texelSize, dp ) )
			) * 0.2;
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#elif defined( SHADOWMAP_TYPE_BASIC )
	float getPointShadow( samplerCube shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 bd3D = normalize( lightToPosition );
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
			dp += shadowBias;
			float depth = textureCube( shadowMap, bd3D ).r;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadow = step( depth, dp );
			#else
				shadow = step( dp, depth );
			#endif
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#endif
	#endif
#endif`,NE=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,OE=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	vec3 shadowWorldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,PE=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0 && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,FE=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,zE=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,BE=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,IE=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,HE=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,GE=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,VE=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,XE=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,kE=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = inverseTransformDirection( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseContribution, material.specularColorBlended, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,WE=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,qE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,YE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,ZE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,jE=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const KE=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,QE=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,JE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,$E=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float flipEnvMap;
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vec3( flipEnvMap * vWorldDirection.x, vWorldDirection.yz ) );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,tT=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,eT=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,nT=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,iT=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	#ifdef USE_REVERSED_DEPTH_BUFFER
		float fragCoordZ = vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ];
	#else
		float fragCoordZ = 0.5 * vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ] + 0.5;
	#endif
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,aT=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,rT=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = vec4( dist, 0.0, 0.0, 1.0 );
}`,sT=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,oT=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,lT=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,uT=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,cT=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,fT=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,hT=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,dT=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,pT=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,mT=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,gT=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,_T=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( normalize( normal ) * 0.5 + 0.5, diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,vT=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,xT=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,ST=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,MT=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
 
		outgoingLight = outgoingLight + sheenSpecularDirect + sheenSpecularIndirect;
 
 	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,yT=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,ET=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,TT=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,bT=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,AT=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,RT=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,CT=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,DT=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,ce={alphahash_fragment:QM,alphahash_pars_fragment:JM,alphamap_fragment:$M,alphamap_pars_fragment:ty,alphatest_fragment:ey,alphatest_pars_fragment:ny,aomap_fragment:iy,aomap_pars_fragment:ay,batching_pars_vertex:ry,batching_vertex:sy,begin_vertex:oy,beginnormal_vertex:ly,bsdfs:uy,iridescence_fragment:cy,bumpmap_pars_fragment:fy,clipping_planes_fragment:hy,clipping_planes_pars_fragment:dy,clipping_planes_pars_vertex:py,clipping_planes_vertex:my,color_fragment:gy,color_pars_fragment:_y,color_pars_vertex:vy,color_vertex:xy,common:Sy,cube_uv_reflection_fragment:My,defaultnormal_vertex:yy,displacementmap_pars_vertex:Ey,displacementmap_vertex:Ty,emissivemap_fragment:by,emissivemap_pars_fragment:Ay,colorspace_fragment:Ry,colorspace_pars_fragment:Cy,envmap_fragment:Dy,envmap_common_pars_fragment:wy,envmap_pars_fragment:Uy,envmap_pars_vertex:Ly,envmap_physical_pars_fragment:Xy,envmap_vertex:Ny,fog_vertex:Oy,fog_pars_vertex:Py,fog_fragment:Fy,fog_pars_fragment:zy,gradientmap_pars_fragment:By,lightmap_pars_fragment:Iy,lights_lambert_fragment:Hy,lights_lambert_pars_fragment:Gy,lights_pars_begin:Vy,lights_toon_fragment:ky,lights_toon_pars_fragment:Wy,lights_phong_fragment:qy,lights_phong_pars_fragment:Yy,lights_physical_fragment:Zy,lights_physical_pars_fragment:jy,lights_fragment_begin:Ky,lights_fragment_maps:Qy,lights_fragment_end:Jy,logdepthbuf_fragment:$y,logdepthbuf_pars_fragment:tE,logdepthbuf_pars_vertex:eE,logdepthbuf_vertex:nE,map_fragment:iE,map_pars_fragment:aE,map_particle_fragment:rE,map_particle_pars_fragment:sE,metalnessmap_fragment:oE,metalnessmap_pars_fragment:lE,morphinstance_vertex:uE,morphcolor_vertex:cE,morphnormal_vertex:fE,morphtarget_pars_vertex:hE,morphtarget_vertex:dE,normal_fragment_begin:pE,normal_fragment_maps:mE,normal_pars_fragment:gE,normal_pars_vertex:_E,normal_vertex:vE,normalmap_pars_fragment:xE,clearcoat_normal_fragment_begin:SE,clearcoat_normal_fragment_maps:ME,clearcoat_pars_fragment:yE,iridescence_pars_fragment:EE,opaque_fragment:TE,packing:bE,premultiplied_alpha_fragment:AE,project_vertex:RE,dithering_fragment:CE,dithering_pars_fragment:DE,roughnessmap_fragment:wE,roughnessmap_pars_fragment:UE,shadowmap_pars_fragment:LE,shadowmap_pars_vertex:NE,shadowmap_vertex:OE,shadowmask_pars_fragment:PE,skinbase_vertex:FE,skinning_pars_vertex:zE,skinning_vertex:BE,skinnormal_vertex:IE,specularmap_fragment:HE,specularmap_pars_fragment:GE,tonemapping_fragment:VE,tonemapping_pars_fragment:XE,transmission_fragment:kE,transmission_pars_fragment:WE,uv_pars_fragment:qE,uv_pars_vertex:YE,uv_vertex:ZE,worldpos_vertex:jE,background_vert:KE,background_frag:QE,backgroundCube_vert:JE,backgroundCube_frag:$E,cube_vert:tT,cube_frag:eT,depth_vert:nT,depth_frag:iT,distance_vert:aT,distance_frag:rT,equirect_vert:sT,equirect_frag:oT,linedashed_vert:lT,linedashed_frag:uT,meshbasic_vert:cT,meshbasic_frag:fT,meshlambert_vert:hT,meshlambert_frag:dT,meshmatcap_vert:pT,meshmatcap_frag:mT,meshnormal_vert:gT,meshnormal_frag:_T,meshphong_vert:vT,meshphong_frag:xT,meshphysical_vert:ST,meshphysical_frag:MT,meshtoon_vert:yT,meshtoon_frag:ET,points_vert:TT,points_frag:bT,shadow_vert:AT,shadow_frag:RT,sprite_vert:CT,sprite_frag:DT},Nt={common:{diffuse:{value:new we(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new ue},alphaMap:{value:null},alphaMapTransform:{value:new ue},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new ue}},envmap:{envMap:{value:null},envMapRotation:{value:new ue},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98},dfgLUT:{value:null}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new ue}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new ue}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new ue},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new ue},normalScale:{value:new Ue(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new ue},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new ue}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new ue}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new ue}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new we(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new we(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new ue},alphaTest:{value:0},uvTransform:{value:new ue}},sprite:{diffuse:{value:new we(16777215)},opacity:{value:1},center:{value:new Ue(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new ue},alphaMap:{value:null},alphaMapTransform:{value:new ue},alphaTest:{value:0}}},Ui={basic:{uniforms:On([Nt.common,Nt.specularmap,Nt.envmap,Nt.aomap,Nt.lightmap,Nt.fog]),vertexShader:ce.meshbasic_vert,fragmentShader:ce.meshbasic_frag},lambert:{uniforms:On([Nt.common,Nt.specularmap,Nt.envmap,Nt.aomap,Nt.lightmap,Nt.emissivemap,Nt.bumpmap,Nt.normalmap,Nt.displacementmap,Nt.fog,Nt.lights,{emissive:{value:new we(0)}}]),vertexShader:ce.meshlambert_vert,fragmentShader:ce.meshlambert_frag},phong:{uniforms:On([Nt.common,Nt.specularmap,Nt.envmap,Nt.aomap,Nt.lightmap,Nt.emissivemap,Nt.bumpmap,Nt.normalmap,Nt.displacementmap,Nt.fog,Nt.lights,{emissive:{value:new we(0)},specular:{value:new we(1118481)},shininess:{value:30}}]),vertexShader:ce.meshphong_vert,fragmentShader:ce.meshphong_frag},standard:{uniforms:On([Nt.common,Nt.envmap,Nt.aomap,Nt.lightmap,Nt.emissivemap,Nt.bumpmap,Nt.normalmap,Nt.displacementmap,Nt.roughnessmap,Nt.metalnessmap,Nt.fog,Nt.lights,{emissive:{value:new we(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:ce.meshphysical_vert,fragmentShader:ce.meshphysical_frag},toon:{uniforms:On([Nt.common,Nt.aomap,Nt.lightmap,Nt.emissivemap,Nt.bumpmap,Nt.normalmap,Nt.displacementmap,Nt.gradientmap,Nt.fog,Nt.lights,{emissive:{value:new we(0)}}]),vertexShader:ce.meshtoon_vert,fragmentShader:ce.meshtoon_frag},matcap:{uniforms:On([Nt.common,Nt.bumpmap,Nt.normalmap,Nt.displacementmap,Nt.fog,{matcap:{value:null}}]),vertexShader:ce.meshmatcap_vert,fragmentShader:ce.meshmatcap_frag},points:{uniforms:On([Nt.points,Nt.fog]),vertexShader:ce.points_vert,fragmentShader:ce.points_frag},dashed:{uniforms:On([Nt.common,Nt.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:ce.linedashed_vert,fragmentShader:ce.linedashed_frag},depth:{uniforms:On([Nt.common,Nt.displacementmap]),vertexShader:ce.depth_vert,fragmentShader:ce.depth_frag},normal:{uniforms:On([Nt.common,Nt.bumpmap,Nt.normalmap,Nt.displacementmap,{opacity:{value:1}}]),vertexShader:ce.meshnormal_vert,fragmentShader:ce.meshnormal_frag},sprite:{uniforms:On([Nt.sprite,Nt.fog]),vertexShader:ce.sprite_vert,fragmentShader:ce.sprite_frag},background:{uniforms:{uvTransform:{value:new ue},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:ce.background_vert,fragmentShader:ce.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new ue}},vertexShader:ce.backgroundCube_vert,fragmentShader:ce.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:ce.cube_vert,fragmentShader:ce.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:ce.equirect_vert,fragmentShader:ce.equirect_frag},distance:{uniforms:On([Nt.common,Nt.displacementmap,{referencePosition:{value:new it},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:ce.distance_vert,fragmentShader:ce.distance_frag},shadow:{uniforms:On([Nt.lights,Nt.fog,{color:{value:new we(0)},opacity:{value:1}}]),vertexShader:ce.shadow_vert,fragmentShader:ce.shadow_frag}};Ui.physical={uniforms:On([Ui.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new ue},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new ue},clearcoatNormalScale:{value:new Ue(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new ue},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new ue},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new ue},sheen:{value:0},sheenColor:{value:new we(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new ue},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new ue},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new ue},transmissionSamplerSize:{value:new Ue},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new ue},attenuationDistance:{value:0},attenuationColor:{value:new we(0)},specularColor:{value:new we(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new ue},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new ue},anisotropyVector:{value:new Ue},anisotropyMap:{value:null},anisotropyMapTransform:{value:new ue}}]),vertexShader:ce.meshphysical_vert,fragmentShader:ce.meshphysical_frag};const Tu={r:0,b:0,g:0},Sr=new Bi,wT=new tn;function UT(o,e,i,r,l,c,h){const d=new we(0);let m=c===!0?0:1,p,v,g=null,S=0,M=null;function A(N){let L=N.isScene===!0?N.background:null;return L&&L.isTexture&&(L=(N.backgroundBlurriness>0?i:e).get(L)),L}function C(N){let L=!1;const B=A(N);B===null?x(d,m):B&&B.isColor&&(x(B,1),L=!0);const F=o.xr.getEnvironmentBlendMode();F==="additive"?r.buffers.color.setClear(0,0,0,1,h):F==="alpha-blend"&&r.buffers.color.setClear(0,0,0,0,h),(o.autoClear||L)&&(r.buffers.depth.setTest(!0),r.buffers.depth.setMask(!0),r.buffers.color.setMask(!0),o.clear(o.autoClearColor,o.autoClearDepth,o.autoClearStencil))}function y(N,L){const B=A(L);B&&(B.isCubeTexture||B.mapping===Pu)?(v===void 0&&(v=new ga(new Yo(1,1,1),new Ii({name:"BackgroundCubeMaterial",uniforms:ws(Ui.backgroundCube.uniforms),vertexShader:Ui.backgroundCube.vertexShader,fragmentShader:Ui.backgroundCube.fragmentShader,side:Xn,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),v.geometry.deleteAttribute("normal"),v.geometry.deleteAttribute("uv"),v.onBeforeRender=function(F,z,Q){this.matrixWorld.copyPosition(Q.matrixWorld)},Object.defineProperty(v.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),l.update(v)),Sr.copy(L.backgroundRotation),Sr.x*=-1,Sr.y*=-1,Sr.z*=-1,B.isCubeTexture&&B.isRenderTargetTexture===!1&&(Sr.y*=-1,Sr.z*=-1),v.material.uniforms.envMap.value=B,v.material.uniforms.flipEnvMap.value=B.isCubeTexture&&B.isRenderTargetTexture===!1?-1:1,v.material.uniforms.backgroundBlurriness.value=L.backgroundBlurriness,v.material.uniforms.backgroundIntensity.value=L.backgroundIntensity,v.material.uniforms.backgroundRotation.value.setFromMatrix4(wT.makeRotationFromEuler(Sr)),v.material.toneMapped=ye.getTransfer(B.colorSpace)!==Be,(g!==B||S!==B.version||M!==o.toneMapping)&&(v.material.needsUpdate=!0,g=B,S=B.version,M=o.toneMapping),v.layers.enableAll(),N.unshift(v,v.geometry,v.material,0,0,null)):B&&B.isTexture&&(p===void 0&&(p=new ga(new Fu(2,2),new Ii({name:"BackgroundMaterial",uniforms:ws(Ui.background.uniforms),vertexShader:Ui.background.vertexShader,fragmentShader:Ui.background.fragmentShader,side:Qa,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),p.geometry.deleteAttribute("normal"),Object.defineProperty(p.material,"map",{get:function(){return this.uniforms.t2D.value}}),l.update(p)),p.material.uniforms.t2D.value=B,p.material.uniforms.backgroundIntensity.value=L.backgroundIntensity,p.material.toneMapped=ye.getTransfer(B.colorSpace)!==Be,B.matrixAutoUpdate===!0&&B.updateMatrix(),p.material.uniforms.uvTransform.value.copy(B.matrix),(g!==B||S!==B.version||M!==o.toneMapping)&&(p.material.needsUpdate=!0,g=B,S=B.version,M=o.toneMapping),p.layers.enableAll(),N.unshift(p,p.geometry,p.material,0,0,null))}function x(N,L){N.getRGB(Tu,ev(o)),r.buffers.color.setClear(Tu.r,Tu.g,Tu.b,L,h)}function P(){v!==void 0&&(v.geometry.dispose(),v.material.dispose(),v=void 0),p!==void 0&&(p.geometry.dispose(),p.material.dispose(),p=void 0)}return{getClearColor:function(){return d},setClearColor:function(N,L=1){d.set(N),m=L,x(d,m)},getClearAlpha:function(){return m},setClearAlpha:function(N){m=N,x(d,m)},render:C,addToRenderList:y,dispose:P}}function LT(o,e){const i=o.getParameter(o.MAX_VERTEX_ATTRIBS),r={},l=S(null);let c=l,h=!1;function d(D,k,rt,at,ut){let ht=!1;const O=g(at,rt,k);c!==O&&(c=O,p(c.object)),ht=M(D,at,rt,ut),ht&&A(D,at,rt,ut),ut!==null&&e.update(ut,o.ELEMENT_ARRAY_BUFFER),(ht||h)&&(h=!1,L(D,k,rt,at),ut!==null&&o.bindBuffer(o.ELEMENT_ARRAY_BUFFER,e.get(ut).buffer))}function m(){return o.createVertexArray()}function p(D){return o.bindVertexArray(D)}function v(D){return o.deleteVertexArray(D)}function g(D,k,rt){const at=rt.wireframe===!0;let ut=r[D.id];ut===void 0&&(ut={},r[D.id]=ut);let ht=ut[k.id];ht===void 0&&(ht={},ut[k.id]=ht);let O=ht[at];return O===void 0&&(O=S(m()),ht[at]=O),O}function S(D){const k=[],rt=[],at=[];for(let ut=0;ut<i;ut++)k[ut]=0,rt[ut]=0,at[ut]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:k,enabledAttributes:rt,attributeDivisors:at,object:D,attributes:{},index:null}}function M(D,k,rt,at){const ut=c.attributes,ht=k.attributes;let O=0;const V=rt.getAttributes();for(const nt in V)if(V[nt].location>=0){const xt=ut[nt];let U=ht[nt];if(U===void 0&&(nt==="instanceMatrix"&&D.instanceMatrix&&(U=D.instanceMatrix),nt==="instanceColor"&&D.instanceColor&&(U=D.instanceColor)),xt===void 0||xt.attribute!==U||U&&xt.data!==U.data)return!0;O++}return c.attributesNum!==O||c.index!==at}function A(D,k,rt,at){const ut={},ht=k.attributes;let O=0;const V=rt.getAttributes();for(const nt in V)if(V[nt].location>=0){let xt=ht[nt];xt===void 0&&(nt==="instanceMatrix"&&D.instanceMatrix&&(xt=D.instanceMatrix),nt==="instanceColor"&&D.instanceColor&&(xt=D.instanceColor));const U={};U.attribute=xt,xt&&xt.data&&(U.data=xt.data),ut[nt]=U,O++}c.attributes=ut,c.attributesNum=O,c.index=at}function C(){const D=c.newAttributes;for(let k=0,rt=D.length;k<rt;k++)D[k]=0}function y(D){x(D,0)}function x(D,k){const rt=c.newAttributes,at=c.enabledAttributes,ut=c.attributeDivisors;rt[D]=1,at[D]===0&&(o.enableVertexAttribArray(D),at[D]=1),ut[D]!==k&&(o.vertexAttribDivisor(D,k),ut[D]=k)}function P(){const D=c.newAttributes,k=c.enabledAttributes;for(let rt=0,at=k.length;rt<at;rt++)k[rt]!==D[rt]&&(o.disableVertexAttribArray(rt),k[rt]=0)}function N(D,k,rt,at,ut,ht,O){O===!0?o.vertexAttribIPointer(D,k,rt,ut,ht):o.vertexAttribPointer(D,k,rt,at,ut,ht)}function L(D,k,rt,at){C();const ut=at.attributes,ht=rt.getAttributes(),O=k.defaultAttributeValues;for(const V in ht){const nt=ht[V];if(nt.location>=0){let Mt=ut[V];if(Mt===void 0&&(V==="instanceMatrix"&&D.instanceMatrix&&(Mt=D.instanceMatrix),V==="instanceColor"&&D.instanceColor&&(Mt=D.instanceColor)),Mt!==void 0){const xt=Mt.normalized,U=Mt.itemSize,et=e.get(Mt);if(et===void 0)continue;const gt=et.buffer,bt=et.type,Bt=et.bytesPerElement,tt=bt===o.INT||bt===o.UNSIGNED_INT||Mt.gpuType===Ad;if(Mt.isInterleavedBufferAttribute){const ct=Mt.data,Dt=ct.stride,Vt=Mt.offset;if(ct.isInstancedInterleavedBuffer){for(let It=0;It<nt.locationSize;It++)x(nt.location+It,ct.meshPerAttribute);D.isInstancedMesh!==!0&&at._maxInstanceCount===void 0&&(at._maxInstanceCount=ct.meshPerAttribute*ct.count)}else for(let It=0;It<nt.locationSize;It++)y(nt.location+It);o.bindBuffer(o.ARRAY_BUFFER,gt);for(let It=0;It<nt.locationSize;It++)N(nt.location+It,U/nt.locationSize,bt,xt,Dt*Bt,(Vt+U/nt.locationSize*It)*Bt,tt)}else{if(Mt.isInstancedBufferAttribute){for(let ct=0;ct<nt.locationSize;ct++)x(nt.location+ct,Mt.meshPerAttribute);D.isInstancedMesh!==!0&&at._maxInstanceCount===void 0&&(at._maxInstanceCount=Mt.meshPerAttribute*Mt.count)}else for(let ct=0;ct<nt.locationSize;ct++)y(nt.location+ct);o.bindBuffer(o.ARRAY_BUFFER,gt);for(let ct=0;ct<nt.locationSize;ct++)N(nt.location+ct,U/nt.locationSize,bt,xt,U*Bt,U/nt.locationSize*ct*Bt,tt)}}else if(O!==void 0){const xt=O[V];if(xt!==void 0)switch(xt.length){case 2:o.vertexAttrib2fv(nt.location,xt);break;case 3:o.vertexAttrib3fv(nt.location,xt);break;case 4:o.vertexAttrib4fv(nt.location,xt);break;default:o.vertexAttrib1fv(nt.location,xt)}}}}P()}function B(){Q();for(const D in r){const k=r[D];for(const rt in k){const at=k[rt];for(const ut in at)v(at[ut].object),delete at[ut];delete k[rt]}delete r[D]}}function F(D){if(r[D.id]===void 0)return;const k=r[D.id];for(const rt in k){const at=k[rt];for(const ut in at)v(at[ut].object),delete at[ut];delete k[rt]}delete r[D.id]}function z(D){for(const k in r){const rt=r[k];if(rt[D.id]===void 0)continue;const at=rt[D.id];for(const ut in at)v(at[ut].object),delete at[ut];delete rt[D.id]}}function Q(){R(),h=!0,c!==l&&(c=l,p(c.object))}function R(){l.geometry=null,l.program=null,l.wireframe=!1}return{setup:d,reset:Q,resetDefaultState:R,dispose:B,releaseStatesOfGeometry:F,releaseStatesOfProgram:z,initAttributes:C,enableAttribute:y,disableUnusedAttributes:P}}function NT(o,e,i){let r;function l(p){r=p}function c(p,v){o.drawArrays(r,p,v),i.update(v,r,1)}function h(p,v,g){g!==0&&(o.drawArraysInstanced(r,p,v,g),i.update(v,r,g))}function d(p,v,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(r,p,0,v,0,g);let M=0;for(let A=0;A<g;A++)M+=v[A];i.update(M,r,1)}function m(p,v,g,S){if(g===0)return;const M=e.get("WEBGL_multi_draw");if(M===null)for(let A=0;A<p.length;A++)h(p[A],v[A],S[A]);else{M.multiDrawArraysInstancedWEBGL(r,p,0,v,0,S,0,g);let A=0;for(let C=0;C<g;C++)A+=v[C]*S[C];i.update(A,r,1)}}this.setMode=l,this.render=c,this.renderInstances=h,this.renderMultiDraw=d,this.renderMultiDrawInstances=m}function OT(o,e,i,r){let l;function c(){if(l!==void 0)return l;if(e.has("EXT_texture_filter_anisotropic")===!0){const z=e.get("EXT_texture_filter_anisotropic");l=o.getParameter(z.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else l=0;return l}function h(z){return!(z!==Ti&&r.convert(z)!==o.getParameter(o.IMPLEMENTATION_COLOR_READ_FORMAT))}function d(z){const Q=z===pa&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(z!==$n&&r.convert(z)!==o.getParameter(o.IMPLEMENTATION_COLOR_READ_TYPE)&&z!==Li&&!Q)}function m(z){if(z==="highp"){if(o.getShaderPrecisionFormat(o.VERTEX_SHADER,o.HIGH_FLOAT).precision>0&&o.getShaderPrecisionFormat(o.FRAGMENT_SHADER,o.HIGH_FLOAT).precision>0)return"highp";z="mediump"}return z==="mediump"&&o.getShaderPrecisionFormat(o.VERTEX_SHADER,o.MEDIUM_FLOAT).precision>0&&o.getShaderPrecisionFormat(o.FRAGMENT_SHADER,o.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let p=i.precision!==void 0?i.precision:"highp";const v=m(p);v!==p&&(ae("WebGLRenderer:",p,"not supported, using",v,"instead."),p=v);const g=i.logarithmicDepthBuffer===!0,S=i.reversedDepthBuffer===!0&&e.has("EXT_clip_control"),M=o.getParameter(o.MAX_TEXTURE_IMAGE_UNITS),A=o.getParameter(o.MAX_VERTEX_TEXTURE_IMAGE_UNITS),C=o.getParameter(o.MAX_TEXTURE_SIZE),y=o.getParameter(o.MAX_CUBE_MAP_TEXTURE_SIZE),x=o.getParameter(o.MAX_VERTEX_ATTRIBS),P=o.getParameter(o.MAX_VERTEX_UNIFORM_VECTORS),N=o.getParameter(o.MAX_VARYING_VECTORS),L=o.getParameter(o.MAX_FRAGMENT_UNIFORM_VECTORS),B=o.getParameter(o.MAX_SAMPLES),F=o.getParameter(o.SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:c,getMaxPrecision:m,textureFormatReadable:h,textureTypeReadable:d,precision:p,logarithmicDepthBuffer:g,reversedDepthBuffer:S,maxTextures:M,maxVertexTextures:A,maxTextureSize:C,maxCubemapSize:y,maxAttributes:x,maxVertexUniforms:P,maxVaryings:N,maxFragmentUniforms:L,maxSamples:B,samples:F}}function PT(o){const e=this;let i=null,r=0,l=!1,c=!1;const h=new yr,d=new ue,m={value:null,needsUpdate:!1};this.uniform=m,this.numPlanes=0,this.numIntersection=0,this.init=function(g,S){const M=g.length!==0||S||r!==0||l;return l=S,r=g.length,M},this.beginShadows=function(){c=!0,v(null)},this.endShadows=function(){c=!1},this.setGlobalState=function(g,S){i=v(g,S,0)},this.setState=function(g,S,M){const A=g.clippingPlanes,C=g.clipIntersection,y=g.clipShadows,x=o.get(g);if(!l||A===null||A.length===0||c&&!y)c?v(null):p();else{const P=c?0:r,N=P*4;let L=x.clippingState||null;m.value=L,L=v(A,S,N,M);for(let B=0;B!==N;++B)L[B]=i[B];x.clippingState=L,this.numIntersection=C?this.numPlanes:0,this.numPlanes+=P}};function p(){m.value!==i&&(m.value=i,m.needsUpdate=r>0),e.numPlanes=r,e.numIntersection=0}function v(g,S,M,A){const C=g!==null?g.length:0;let y=null;if(C!==0){if(y=m.value,A!==!0||y===null){const x=M+C*4,P=S.matrixWorldInverse;d.getNormalMatrix(P),(y===null||y.length<x)&&(y=new Float32Array(x));for(let N=0,L=M;N!==C;++N,L+=4)h.copy(g[N]).applyMatrix4(P,d),h.normal.toArray(y,L),y[L+3]=h.constant}m.value=y,m.needsUpdate=!0}return e.numPlanes=C,e.numIntersection=0,y}}function FT(o){let e=new WeakMap;function i(h,d){return d===Hh?h.mapping=Rr:d===Gh&&(h.mapping=Rs),h}function r(h){if(h&&h.isTexture){const d=h.mapping;if(d===Hh||d===Gh)if(e.has(h)){const m=e.get(h).texture;return i(m,h.mapping)}else{const m=h.image;if(m&&m.height>0){const p=new av(m.height);return p.fromEquirectangularTexture(o,h),e.set(h,p),h.addEventListener("dispose",l),i(p.texture,h.mapping)}else return null}}return h}function l(h){const d=h.target;d.removeEventListener("dispose",l);const m=e.get(d);m!==void 0&&(e.delete(d),m.dispose())}function c(){e=new WeakMap}return{get:r,dispose:c}}const Ka=4,i_=[.125,.215,.35,.446,.526,.582],Tr=20,zT=256,No=new zd,a_=new we;let Mh=null,yh=0,Eh=0,Th=!1;const BT=new it;class r_{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._sizeLods=[],this._sigmas=[],this._lodMeshes=[],this._backgroundBox=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._blurMaterial=null,this._ggxMaterial=null}fromScene(e,i=0,r=.1,l=100,c={}){const{size:h=256,position:d=BT}=c;Mh=this._renderer.getRenderTarget(),yh=this._renderer.getActiveCubeFace(),Eh=this._renderer.getActiveMipmapLevel(),Th=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(h);const m=this._allocateTargets();return m.depthBuffer=!0,this._sceneToCubeUV(e,r,l,m,d),i>0&&this._blur(m,0,0,i),this._applyPMREM(m),this._cleanup(m),m}fromEquirectangular(e,i=null){return this._fromTexture(e,i)}fromCubemap(e,i=null){return this._fromTexture(e,i)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=l_(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=o_(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose(),this._backgroundBox!==null&&(this._backgroundBox.geometry.dispose(),this._backgroundBox.material.dispose())}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._ggxMaterial!==null&&this._ggxMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodMeshes.length;e++)this._lodMeshes[e].geometry.dispose()}_cleanup(e){this._renderer.setRenderTarget(Mh,yh,Eh),this._renderer.xr.enabled=Th,e.scissorTest=!1,Es(e,0,0,e.width,e.height)}_fromTexture(e,i){e.mapping===Rr||e.mapping===Rs?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),Mh=this._renderer.getRenderTarget(),yh=this._renderer.getActiveCubeFace(),Eh=this._renderer.getActiveMipmapLevel(),Th=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;const r=i||this._allocateTargets();return this._textureToCubeUV(e,r),this._applyPMREM(r),this._cleanup(r),r}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),i=4*this._cubeSize,r={magFilter:Un,minFilter:Un,generateMipmaps:!1,type:pa,format:Ti,colorSpace:Ds,depthBuffer:!1},l=s_(e,i,r);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==i){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=s_(e,i,r);const{_lodMax:c}=this;({lodMeshes:this._lodMeshes,sizeLods:this._sizeLods,sigmas:this._sigmas}=IT(c)),this._blurMaterial=GT(c,e,i),this._ggxMaterial=HT(c,e,i)}return l}_compileMaterial(e){const i=new ga(new Hi,e);this._renderer.compile(i,No)}_sceneToCubeUV(e,i,r,l,c){const m=new yi(90,1,i,r),p=[1,-1,1,1,1,1],v=[1,1,1,-1,-1,-1],g=this._renderer,S=g.autoClear,M=g.toneMapping;g.getClearColor(a_),g.toneMapping=Oi,g.autoClear=!1,g.state.buffers.depth.getReversed()&&(g.setRenderTarget(l),g.clearDepth(),g.setRenderTarget(null)),this._backgroundBox===null&&(this._backgroundBox=new ga(new Yo,new J_({name:"PMREM.Background",side:Xn,depthWrite:!1,depthTest:!1})));const C=this._backgroundBox,y=C.material;let x=!1;const P=e.background;P?P.isColor&&(y.color.copy(P),e.background=null,x=!0):(y.color.copy(a_),x=!0);for(let N=0;N<6;N++){const L=N%3;L===0?(m.up.set(0,p[N],0),m.position.set(c.x,c.y,c.z),m.lookAt(c.x+v[N],c.y,c.z)):L===1?(m.up.set(0,0,p[N]),m.position.set(c.x,c.y,c.z),m.lookAt(c.x,c.y+v[N],c.z)):(m.up.set(0,p[N],0),m.position.set(c.x,c.y,c.z),m.lookAt(c.x,c.y,c.z+v[N]));const B=this._cubeSize;Es(l,L*B,N>2?B:0,B,B),g.setRenderTarget(l),x&&g.render(C,m),g.render(e,m)}g.toneMapping=M,g.autoClear=S,e.background=P}_textureToCubeUV(e,i){const r=this._renderer,l=e.mapping===Rr||e.mapping===Rs;l?(this._cubemapMaterial===null&&(this._cubemapMaterial=l_()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=o_());const c=l?this._cubemapMaterial:this._equirectMaterial,h=this._lodMeshes[0];h.material=c;const d=c.uniforms;d.envMap.value=e;const m=this._cubeSize;Es(i,0,0,3*m,2*m),r.setRenderTarget(i),r.render(h,No)}_applyPMREM(e){const i=this._renderer,r=i.autoClear;i.autoClear=!1;const l=this._lodMeshes.length;for(let c=1;c<l;c++)this._applyGGXFilter(e,c-1,c);i.autoClear=r}_applyGGXFilter(e,i,r){const l=this._renderer,c=this._pingPongRenderTarget,h=this._ggxMaterial,d=this._lodMeshes[r];d.material=h;const m=h.uniforms,p=r/(this._lodMeshes.length-1),v=i/(this._lodMeshes.length-1),g=Math.sqrt(p*p-v*v),S=0+p*1.25,M=g*S,{_lodMax:A}=this,C=this._sizeLods[r],y=3*C*(r>A-Ka?r-A+Ka:0),x=4*(this._cubeSize-C);m.envMap.value=e.texture,m.roughness.value=M,m.mipInt.value=A-i,Es(c,y,x,3*C,2*C),l.setRenderTarget(c),l.render(d,No),m.envMap.value=c.texture,m.roughness.value=0,m.mipInt.value=A-r,Es(e,y,x,3*C,2*C),l.setRenderTarget(e),l.render(d,No)}_blur(e,i,r,l,c){const h=this._pingPongRenderTarget;this._halfBlur(e,h,i,r,l,"latitudinal",c),this._halfBlur(h,e,r,r,l,"longitudinal",c)}_halfBlur(e,i,r,l,c,h,d){const m=this._renderer,p=this._blurMaterial;h!=="latitudinal"&&h!=="longitudinal"&&be("blur direction must be either latitudinal or longitudinal!");const v=3,g=this._lodMeshes[l];g.material=p;const S=p.uniforms,M=this._sizeLods[r]-1,A=isFinite(c)?Math.PI/(2*M):2*Math.PI/(2*Tr-1),C=c/A,y=isFinite(c)?1+Math.floor(v*C):Tr;y>Tr&&ae(`sigmaRadians, ${c}, is too large and will clip, as it requested ${y} samples when the maximum is set to ${Tr}`);const x=[];let P=0;for(let z=0;z<Tr;++z){const Q=z/C,R=Math.exp(-Q*Q/2);x.push(R),z===0?P+=R:z<y&&(P+=2*R)}for(let z=0;z<x.length;z++)x[z]=x[z]/P;S.envMap.value=e.texture,S.samples.value=y,S.weights.value=x,S.latitudinal.value=h==="latitudinal",d&&(S.poleAxis.value=d);const{_lodMax:N}=this;S.dTheta.value=A,S.mipInt.value=N-r;const L=this._sizeLods[l],B=3*L*(l>N-Ka?l-N+Ka:0),F=4*(this._cubeSize-L);Es(i,B,F,3*L,2*L),m.setRenderTarget(i),m.render(g,No)}}function IT(o){const e=[],i=[],r=[];let l=o;const c=o-Ka+1+i_.length;for(let h=0;h<c;h++){const d=Math.pow(2,l);e.push(d);let m=1/d;h>o-Ka?m=i_[h-o+Ka-1]:h===0&&(m=0),i.push(m);const p=1/(d-2),v=-p,g=1+p,S=[v,v,g,v,g,g,v,v,g,g,v,g],M=6,A=6,C=3,y=2,x=1,P=new Float32Array(C*A*M),N=new Float32Array(y*A*M),L=new Float32Array(x*A*M);for(let F=0;F<M;F++){const z=F%3*2/3-1,Q=F>2?0:-1,R=[z,Q,0,z+2/3,Q,0,z+2/3,Q+1,0,z,Q,0,z+2/3,Q+1,0,z,Q+1,0];P.set(R,C*A*F),N.set(S,y*A*F);const D=[F,F,F,F,F,F];L.set(D,x*A*F)}const B=new Hi;B.setAttribute("position",new Fi(P,C)),B.setAttribute("uv",new Fi(N,y)),B.setAttribute("faceIndex",new Fi(L,x)),r.push(new ga(B,null)),l>Ka&&l--}return{lodMeshes:r,sizeLods:e,sigmas:i}}function s_(o,e,i){const r=new Pi(o,e,i);return r.texture.mapping=Pu,r.texture.name="PMREM.cubeUv",r.scissorTest=!0,r}function Es(o,e,i,r,l){o.viewport.set(e,i,r,l),o.scissor.set(e,i,r,l)}function HT(o,e,i){return new Ii({name:"PMREMGGXConvolution",defines:{GGX_SAMPLES:zT,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/i,CUBEUV_MAX_MIP:`${o}.0`},uniforms:{envMap:{value:null},roughness:{value:0},mipInt:{value:0}},vertexShader:zu(),fragmentShader:`

			precision highp float;
			precision highp int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform float roughness;
			uniform float mipInt;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			#define PI 3.14159265359

			// Van der Corput radical inverse
			float radicalInverse_VdC(uint bits) {
				bits = (bits << 16u) | (bits >> 16u);
				bits = ((bits & 0x55555555u) << 1u) | ((bits & 0xAAAAAAAAu) >> 1u);
				bits = ((bits & 0x33333333u) << 2u) | ((bits & 0xCCCCCCCCu) >> 2u);
				bits = ((bits & 0x0F0F0F0Fu) << 4u) | ((bits & 0xF0F0F0F0u) >> 4u);
				bits = ((bits & 0x00FF00FFu) << 8u) | ((bits & 0xFF00FF00u) >> 8u);
				return float(bits) * 2.3283064365386963e-10; // / 0x100000000
			}

			// Hammersley sequence
			vec2 hammersley(uint i, uint N) {
				return vec2(float(i) / float(N), radicalInverse_VdC(i));
			}

			// GGX VNDF importance sampling (Eric Heitz 2018)
			// "Sampling the GGX Distribution of Visible Normals"
			// https://jcgt.org/published/0007/04/01/
			vec3 importanceSampleGGX_VNDF(vec2 Xi, vec3 V, float roughness) {
				float alpha = roughness * roughness;

				// Section 3.2: Transform view direction to hemisphere configuration
				vec3 Vh = normalize(vec3(alpha * V.x, alpha * V.y, V.z));

				// Section 4.1: Orthonormal basis
				float lensq = Vh.x * Vh.x + Vh.y * Vh.y;
				vec3 T1 = lensq > 0.0 ? vec3(-Vh.y, Vh.x, 0.0) / sqrt(lensq) : vec3(1.0, 0.0, 0.0);
				vec3 T2 = cross(Vh, T1);

				// Section 4.2: Parameterization of projected area
				float r = sqrt(Xi.x);
				float phi = 2.0 * PI * Xi.y;
				float t1 = r * cos(phi);
				float t2 = r * sin(phi);
				float s = 0.5 * (1.0 + Vh.z);
				t2 = (1.0 - s) * sqrt(1.0 - t1 * t1) + s * t2;

				// Section 4.3: Reprojection onto hemisphere
				vec3 Nh = t1 * T1 + t2 * T2 + sqrt(max(0.0, 1.0 - t1 * t1 - t2 * t2)) * Vh;

				// Section 3.4: Transform back to ellipsoid configuration
				return normalize(vec3(alpha * Nh.x, alpha * Nh.y, max(0.0, Nh.z)));
			}

			void main() {
				vec3 N = normalize(vOutputDirection);
				vec3 V = N; // Assume view direction equals normal for pre-filtering

				vec3 prefilteredColor = vec3(0.0);
				float totalWeight = 0.0;

				// For very low roughness, just sample the environment directly
				if (roughness < 0.001) {
					gl_FragColor = vec4(bilinearCubeUV(envMap, N, mipInt), 1.0);
					return;
				}

				// Tangent space basis for VNDF sampling
				vec3 up = abs(N.z) < 0.999 ? vec3(0.0, 0.0, 1.0) : vec3(1.0, 0.0, 0.0);
				vec3 tangent = normalize(cross(up, N));
				vec3 bitangent = cross(N, tangent);

				for(uint i = 0u; i < uint(GGX_SAMPLES); i++) {
					vec2 Xi = hammersley(i, uint(GGX_SAMPLES));

					// For PMREM, V = N, so in tangent space V is always (0, 0, 1)
					vec3 H_tangent = importanceSampleGGX_VNDF(Xi, vec3(0.0, 0.0, 1.0), roughness);

					// Transform H back to world space
					vec3 H = normalize(tangent * H_tangent.x + bitangent * H_tangent.y + N * H_tangent.z);
					vec3 L = normalize(2.0 * dot(V, H) * H - V);

					float NdotL = max(dot(N, L), 0.0);

					if(NdotL > 0.0) {
						// Sample environment at fixed mip level
						// VNDF importance sampling handles the distribution filtering
						vec3 sampleColor = bilinearCubeUV(envMap, L, mipInt);

						// Weight by NdotL for the split-sum approximation
						// VNDF PDF naturally accounts for the visible microfacet distribution
						prefilteredColor += sampleColor * NdotL;
						totalWeight += NdotL;
					}
				}

				if (totalWeight > 0.0) {
					prefilteredColor = prefilteredColor / totalWeight;
				}

				gl_FragColor = vec4(prefilteredColor, 1.0);
			}
		`,blending:ha,depthTest:!1,depthWrite:!1})}function GT(o,e,i){const r=new Float32Array(Tr),l=new it(0,1,0);return new Ii({name:"SphericalGaussianBlur",defines:{n:Tr,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/i,CUBEUV_MAX_MIP:`${o}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:r},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:l}},vertexShader:zu(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform int samples;
			uniform float weights[ n ];
			uniform bool latitudinal;
			uniform float dTheta;
			uniform float mipInt;
			uniform vec3 poleAxis;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			vec3 getSample( float theta, vec3 axis ) {

				float cosTheta = cos( theta );
				// Rodrigues' axis-angle rotation
				vec3 sampleDirection = vOutputDirection * cosTheta
					+ cross( axis, vOutputDirection ) * sin( theta )
					+ axis * dot( axis, vOutputDirection ) * ( 1.0 - cosTheta );

				return bilinearCubeUV( envMap, sampleDirection, mipInt );

			}

			void main() {

				vec3 axis = latitudinal ? poleAxis : cross( poleAxis, vOutputDirection );

				if ( all( equal( axis, vec3( 0.0 ) ) ) ) {

					axis = vec3( vOutputDirection.z, 0.0, - vOutputDirection.x );

				}

				axis = normalize( axis );

				gl_FragColor = vec4( 0.0, 0.0, 0.0, 1.0 );
				gl_FragColor.rgb += weights[ 0 ] * getSample( 0.0, axis );

				for ( int i = 1; i < n; i++ ) {

					if ( i >= samples ) {

						break;

					}

					float theta = dTheta * float( i );
					gl_FragColor.rgb += weights[ i ] * getSample( -1.0 * theta, axis );
					gl_FragColor.rgb += weights[ i ] * getSample( theta, axis );

				}

			}
		`,blending:ha,depthTest:!1,depthWrite:!1})}function o_(){return new Ii({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:zu(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:ha,depthTest:!1,depthWrite:!1})}function l_(){return new Ii({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:zu(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:ha,depthTest:!1,depthWrite:!1})}function zu(){return`

		precision mediump float;
		precision mediump int;

		attribute float faceIndex;

		varying vec3 vOutputDirection;

		// RH coordinate system; PMREM face-indexing convention
		vec3 getDirection( vec2 uv, float face ) {

			uv = 2.0 * uv - 1.0;

			vec3 direction = vec3( uv, 1.0 );

			if ( face == 0.0 ) {

				direction = direction.zyx; // ( 1, v, u ) pos x

			} else if ( face == 1.0 ) {

				direction = direction.xzy;
				direction.xz *= -1.0; // ( -u, 1, -v ) pos y

			} else if ( face == 2.0 ) {

				direction.x *= -1.0; // ( -u, v, 1 ) pos z

			} else if ( face == 3.0 ) {

				direction = direction.zyx;
				direction.xz *= -1.0; // ( -1, v, -u ) neg x

			} else if ( face == 4.0 ) {

				direction = direction.xzy;
				direction.xy *= -1.0; // ( -u, -1, v ) neg y

			} else if ( face == 5.0 ) {

				direction.z *= -1.0; // ( u, v, -1 ) neg z

			}

			return direction;

		}

		void main() {

			vOutputDirection = getDirection( uv, faceIndex );
			gl_Position = vec4( position, 1.0 );

		}
	`}function VT(o){let e=new WeakMap,i=null;function r(d){if(d&&d.isTexture){const m=d.mapping,p=m===Hh||m===Gh,v=m===Rr||m===Rs;if(p||v){let g=e.get(d);const S=g!==void 0?g.texture.pmremVersion:0;if(d.isRenderTargetTexture&&d.pmremVersion!==S)return i===null&&(i=new r_(o)),g=p?i.fromEquirectangular(d,g):i.fromCubemap(d,g),g.texture.pmremVersion=d.pmremVersion,e.set(d,g),g.texture;if(g!==void 0)return g.texture;{const M=d.image;return p&&M&&M.height>0||v&&M&&l(M)?(i===null&&(i=new r_(o)),g=p?i.fromEquirectangular(d):i.fromCubemap(d),g.texture.pmremVersion=d.pmremVersion,e.set(d,g),d.addEventListener("dispose",c),g.texture):null}}}return d}function l(d){let m=0;const p=6;for(let v=0;v<p;v++)d[v]!==void 0&&m++;return m===p}function c(d){const m=d.target;m.removeEventListener("dispose",c);const p=e.get(m);p!==void 0&&(e.delete(m),p.dispose())}function h(){e=new WeakMap,i!==null&&(i.dispose(),i=null)}return{get:r,dispose:h}}function XT(o){const e={};function i(r){if(e[r]!==void 0)return e[r];const l=o.getExtension(r);return e[r]=l,l}return{has:function(r){return i(r)!==null},init:function(){i("EXT_color_buffer_float"),i("WEBGL_clip_cull_distance"),i("OES_texture_float_linear"),i("EXT_color_buffer_half_float"),i("WEBGL_multisampled_render_to_texture"),i("WEBGL_render_shared_exponent")},get:function(r){const l=i(r);return l===null&&Ho("WebGLRenderer: "+r+" extension not supported."),l}}}function kT(o,e,i,r){const l={},c=new WeakMap;function h(g){const S=g.target;S.index!==null&&e.remove(S.index);for(const A in S.attributes)e.remove(S.attributes[A]);S.removeEventListener("dispose",h),delete l[S.id];const M=c.get(S);M&&(e.remove(M),c.delete(S)),r.releaseStatesOfGeometry(S),S.isInstancedBufferGeometry===!0&&delete S._maxInstanceCount,i.memory.geometries--}function d(g,S){return l[S.id]===!0||(S.addEventListener("dispose",h),l[S.id]=!0,i.memory.geometries++),S}function m(g){const S=g.attributes;for(const M in S)e.update(S[M],o.ARRAY_BUFFER)}function p(g){const S=[],M=g.index,A=g.attributes.position;let C=0;if(M!==null){const P=M.array;C=M.version;for(let N=0,L=P.length;N<L;N+=3){const B=P[N+0],F=P[N+1],z=P[N+2];S.push(B,F,F,z,z,B)}}else if(A!==void 0){const P=A.array;C=A.version;for(let N=0,L=P.length/3-1;N<L;N+=3){const B=N+0,F=N+1,z=N+2;S.push(B,F,F,z,z,B)}}else return;const y=new(Z_(S)?tv:$_)(S,1);y.version=C;const x=c.get(g);x&&e.remove(x),c.set(g,y)}function v(g){const S=c.get(g);if(S){const M=g.index;M!==null&&S.version<M.version&&p(g)}else p(g);return c.get(g)}return{get:d,update:m,getWireframeAttribute:v}}function WT(o,e,i){let r;function l(S){r=S}let c,h;function d(S){c=S.type,h=S.bytesPerElement}function m(S,M){o.drawElements(r,M,c,S*h),i.update(M,r,1)}function p(S,M,A){A!==0&&(o.drawElementsInstanced(r,M,c,S*h,A),i.update(M,r,A))}function v(S,M,A){if(A===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(r,M,0,c,S,0,A);let y=0;for(let x=0;x<A;x++)y+=M[x];i.update(y,r,1)}function g(S,M,A,C){if(A===0)return;const y=e.get("WEBGL_multi_draw");if(y===null)for(let x=0;x<S.length;x++)p(S[x]/h,M[x],C[x]);else{y.multiDrawElementsInstancedWEBGL(r,M,0,c,S,0,C,0,A);let x=0;for(let P=0;P<A;P++)x+=M[P]*C[P];i.update(x,r,1)}}this.setMode=l,this.setIndex=d,this.render=m,this.renderInstances=p,this.renderMultiDraw=v,this.renderMultiDrawInstances=g}function qT(o){const e={geometries:0,textures:0},i={frame:0,calls:0,triangles:0,points:0,lines:0};function r(c,h,d){switch(i.calls++,h){case o.TRIANGLES:i.triangles+=d*(c/3);break;case o.LINES:i.lines+=d*(c/2);break;case o.LINE_STRIP:i.lines+=d*(c-1);break;case o.LINE_LOOP:i.lines+=d*c;break;case o.POINTS:i.points+=d*c;break;default:be("WebGLInfo: Unknown draw mode:",h);break}}function l(){i.calls=0,i.triangles=0,i.points=0,i.lines=0}return{memory:e,render:i,programs:null,autoReset:!0,reset:l,update:r}}function YT(o,e,i){const r=new WeakMap,l=new $e;function c(h,d,m){const p=h.morphTargetInfluences,v=d.morphAttributes.position||d.morphAttributes.normal||d.morphAttributes.color,g=v!==void 0?v.length:0;let S=r.get(d);if(S===void 0||S.count!==g){let R=function(){z.dispose(),r.delete(d),d.removeEventListener("dispose",R)};S!==void 0&&S.texture.dispose();const M=d.morphAttributes.position!==void 0,A=d.morphAttributes.normal!==void 0,C=d.morphAttributes.color!==void 0,y=d.morphAttributes.position||[],x=d.morphAttributes.normal||[],P=d.morphAttributes.color||[];let N=0;M===!0&&(N=1),A===!0&&(N=2),C===!0&&(N=3);let L=d.attributes.position.count*N,B=1;L>e.maxTextureSize&&(B=Math.ceil(L/e.maxTextureSize),L=e.maxTextureSize);const F=new Float32Array(L*B*4*g),z=new j_(F,L,B,g);z.type=Li,z.needsUpdate=!0;const Q=N*4;for(let D=0;D<g;D++){const k=y[D],rt=x[D],at=P[D],ut=L*B*4*D;for(let ht=0;ht<k.count;ht++){const O=ht*Q;M===!0&&(l.fromBufferAttribute(k,ht),F[ut+O+0]=l.x,F[ut+O+1]=l.y,F[ut+O+2]=l.z,F[ut+O+3]=0),A===!0&&(l.fromBufferAttribute(rt,ht),F[ut+O+4]=l.x,F[ut+O+5]=l.y,F[ut+O+6]=l.z,F[ut+O+7]=0),C===!0&&(l.fromBufferAttribute(at,ht),F[ut+O+8]=l.x,F[ut+O+9]=l.y,F[ut+O+10]=l.z,F[ut+O+11]=at.itemSize===4?l.w:1)}}S={count:g,texture:z,size:new Ue(L,B)},r.set(d,S),d.addEventListener("dispose",R)}if(h.isInstancedMesh===!0&&h.morphTexture!==null)m.getUniforms().setValue(o,"morphTexture",h.morphTexture,i);else{let M=0;for(let C=0;C<p.length;C++)M+=p[C];const A=d.morphTargetsRelative?1:1-M;m.getUniforms().setValue(o,"morphTargetBaseInfluence",A),m.getUniforms().setValue(o,"morphTargetInfluences",p)}m.getUniforms().setValue(o,"morphTargetsTexture",S.texture,i),m.getUniforms().setValue(o,"morphTargetsTextureSize",S.size)}return{update:c}}function ZT(o,e,i,r){let l=new WeakMap;function c(m){const p=r.render.frame,v=m.geometry,g=e.get(m,v);if(l.get(g)!==p&&(e.update(g),l.set(g,p)),m.isInstancedMesh&&(m.hasEventListener("dispose",d)===!1&&m.addEventListener("dispose",d),l.get(m)!==p&&(i.update(m.instanceMatrix,o.ARRAY_BUFFER),m.instanceColor!==null&&i.update(m.instanceColor,o.ARRAY_BUFFER),l.set(m,p))),m.isSkinnedMesh){const S=m.skeleton;l.get(S)!==p&&(S.update(),l.set(S,p))}return g}function h(){l=new WeakMap}function d(m){const p=m.target;p.removeEventListener("dispose",d),i.remove(p.instanceMatrix),p.instanceColor!==null&&i.remove(p.instanceColor)}return{update:c,dispose:h}}const jT={[L_]:"LINEAR_TONE_MAPPING",[N_]:"REINHARD_TONE_MAPPING",[O_]:"CINEON_TONE_MAPPING",[P_]:"ACES_FILMIC_TONE_MAPPING",[z_]:"AGX_TONE_MAPPING",[B_]:"NEUTRAL_TONE_MAPPING",[F_]:"CUSTOM_TONE_MAPPING"};function KT(o,e,i,r,l){const c=new Pi(e,i,{type:o,depthBuffer:r,stencilBuffer:l}),h=new Pi(e,i,{type:pa,depthBuffer:!1,stencilBuffer:!1}),d=new Hi;d.setAttribute("position",new hi([-1,3,0,-1,-1,0,3,-1,0],3)),d.setAttribute("uv",new hi([0,2,0,0,2,0],2));const m=new XM({uniforms:{tDiffuse:{value:null}},vertexShader:`
			precision highp float;

			uniform mat4 modelViewMatrix;
			uniform mat4 projectionMatrix;

			attribute vec3 position;
			attribute vec2 uv;

			varying vec2 vUv;

			void main() {
				vUv = uv;
				gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
			}`,fragmentShader:`
			precision highp float;

			uniform sampler2D tDiffuse;

			varying vec2 vUv;

			#include <tonemapping_pars_fragment>
			#include <colorspace_pars_fragment>

			void main() {
				gl_FragColor = texture2D( tDiffuse, vUv );

				#ifdef LINEAR_TONE_MAPPING
					gl_FragColor.rgb = LinearToneMapping( gl_FragColor.rgb );
				#elif defined( REINHARD_TONE_MAPPING )
					gl_FragColor.rgb = ReinhardToneMapping( gl_FragColor.rgb );
				#elif defined( CINEON_TONE_MAPPING )
					gl_FragColor.rgb = CineonToneMapping( gl_FragColor.rgb );
				#elif defined( ACES_FILMIC_TONE_MAPPING )
					gl_FragColor.rgb = ACESFilmicToneMapping( gl_FragColor.rgb );
				#elif defined( AGX_TONE_MAPPING )
					gl_FragColor.rgb = AgXToneMapping( gl_FragColor.rgb );
				#elif defined( NEUTRAL_TONE_MAPPING )
					gl_FragColor.rgb = NeutralToneMapping( gl_FragColor.rgb );
				#elif defined( CUSTOM_TONE_MAPPING )
					gl_FragColor.rgb = CustomToneMapping( gl_FragColor.rgb );
				#endif

				#ifdef SRGB_TRANSFER
					gl_FragColor = sRGBTransferOETF( gl_FragColor );
				#endif
			}`,depthTest:!1,depthWrite:!1}),p=new ga(d,m),v=new zd(-1,1,1,-1,0,1);let g=null,S=null,M=!1,A,C=null,y=[],x=!1;this.setSize=function(P,N){c.setSize(P,N),h.setSize(P,N);for(let L=0;L<y.length;L++){const B=y[L];B.setSize&&B.setSize(P,N)}},this.setEffects=function(P){y=P,x=y.length>0&&y[0].isRenderPass===!0;const N=c.width,L=c.height;for(let B=0;B<y.length;B++){const F=y[B];F.setSize&&F.setSize(N,L)}},this.begin=function(P,N){if(M||P.toneMapping===Oi&&y.length===0)return!1;if(C=N,N!==null){const L=N.width,B=N.height;(c.width!==L||c.height!==B)&&this.setSize(L,B)}return x===!1&&P.setRenderTarget(c),A=P.toneMapping,P.toneMapping=Oi,!0},this.hasRenderPass=function(){return x},this.end=function(P,N){P.toneMapping=A,M=!0;let L=c,B=h;for(let F=0;F<y.length;F++){const z=y[F];if(z.enabled!==!1&&(z.render(P,B,L,N),z.needsSwap!==!1)){const Q=L;L=B,B=Q}}if(g!==P.outputColorSpace||S!==P.toneMapping){g=P.outputColorSpace,S=P.toneMapping,m.defines={},ye.getTransfer(g)===Be&&(m.defines.SRGB_TRANSFER="");const F=jT[S];F&&(m.defines[F]=""),m.needsUpdate=!0}m.uniforms.tDiffuse.value=L.texture,P.setRenderTarget(C),P.render(p,v),C=null,M=!1},this.isCompositing=function(){return M},this.dispose=function(){c.dispose(),h.dispose(),d.dispose(),m.dispose()}}const uv=new Pn,Ed=new Go(1,1),cv=new j_,fv=new xM,hv=new iv,u_=[],c_=[],f_=new Float32Array(16),h_=new Float32Array(9),d_=new Float32Array(4);function Ls(o,e,i){const r=o[0];if(r<=0||r>0)return o;const l=e*i;let c=u_[l];if(c===void 0&&(c=new Float32Array(l),u_[l]=c),e!==0){r.toArray(c,0);for(let h=1,d=0;h!==e;++h)d+=i,o[h].toArray(c,d)}return c}function hn(o,e){if(o.length!==e.length)return!1;for(let i=0,r=o.length;i<r;i++)if(o[i]!==e[i])return!1;return!0}function dn(o,e){for(let i=0,r=e.length;i<r;i++)o[i]=e[i]}function Bu(o,e){let i=c_[e];i===void 0&&(i=new Int32Array(e),c_[e]=i);for(let r=0;r!==e;++r)i[r]=o.allocateTextureUnit();return i}function QT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1f(this.addr,e),i[0]=e)}function JT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2f(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(hn(i,e))return;o.uniform2fv(this.addr,e),dn(i,e)}}function $T(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3f(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else if(e.r!==void 0)(i[0]!==e.r||i[1]!==e.g||i[2]!==e.b)&&(o.uniform3f(this.addr,e.r,e.g,e.b),i[0]=e.r,i[1]=e.g,i[2]=e.b);else{if(hn(i,e))return;o.uniform3fv(this.addr,e),dn(i,e)}}function tb(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4f(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(hn(i,e))return;o.uniform4fv(this.addr,e),dn(i,e)}}function eb(o,e){const i=this.cache,r=e.elements;if(r===void 0){if(hn(i,e))return;o.uniformMatrix2fv(this.addr,!1,e),dn(i,e)}else{if(hn(i,r))return;d_.set(r),o.uniformMatrix2fv(this.addr,!1,d_),dn(i,r)}}function nb(o,e){const i=this.cache,r=e.elements;if(r===void 0){if(hn(i,e))return;o.uniformMatrix3fv(this.addr,!1,e),dn(i,e)}else{if(hn(i,r))return;h_.set(r),o.uniformMatrix3fv(this.addr,!1,h_),dn(i,r)}}function ib(o,e){const i=this.cache,r=e.elements;if(r===void 0){if(hn(i,e))return;o.uniformMatrix4fv(this.addr,!1,e),dn(i,e)}else{if(hn(i,r))return;f_.set(r),o.uniformMatrix4fv(this.addr,!1,f_),dn(i,r)}}function ab(o,e){const i=this.cache;i[0]!==e&&(o.uniform1i(this.addr,e),i[0]=e)}function rb(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2i(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(hn(i,e))return;o.uniform2iv(this.addr,e),dn(i,e)}}function sb(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3i(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else{if(hn(i,e))return;o.uniform3iv(this.addr,e),dn(i,e)}}function ob(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4i(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(hn(i,e))return;o.uniform4iv(this.addr,e),dn(i,e)}}function lb(o,e){const i=this.cache;i[0]!==e&&(o.uniform1ui(this.addr,e),i[0]=e)}function ub(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2ui(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(hn(i,e))return;o.uniform2uiv(this.addr,e),dn(i,e)}}function cb(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3ui(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else{if(hn(i,e))return;o.uniform3uiv(this.addr,e),dn(i,e)}}function fb(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4ui(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(hn(i,e))return;o.uniform4uiv(this.addr,e),dn(i,e)}}function hb(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l);let c;this.type===o.SAMPLER_2D_SHADOW?(Ed.compareFunction=i.isReversedDepthBuffer()?Nd:Ld,c=Ed):c=uv,i.setTexture2D(e||c,l)}function db(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l),i.setTexture3D(e||fv,l)}function pb(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l),i.setTextureCube(e||hv,l)}function mb(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l),i.setTexture2DArray(e||cv,l)}function gb(o){switch(o){case 5126:return QT;case 35664:return JT;case 35665:return $T;case 35666:return tb;case 35674:return eb;case 35675:return nb;case 35676:return ib;case 5124:case 35670:return ab;case 35667:case 35671:return rb;case 35668:case 35672:return sb;case 35669:case 35673:return ob;case 5125:return lb;case 36294:return ub;case 36295:return cb;case 36296:return fb;case 35678:case 36198:case 36298:case 36306:case 35682:return hb;case 35679:case 36299:case 36307:return db;case 35680:case 36300:case 36308:case 36293:return pb;case 36289:case 36303:case 36311:case 36292:return mb}}function _b(o,e){o.uniform1fv(this.addr,e)}function vb(o,e){const i=Ls(e,this.size,2);o.uniform2fv(this.addr,i)}function xb(o,e){const i=Ls(e,this.size,3);o.uniform3fv(this.addr,i)}function Sb(o,e){const i=Ls(e,this.size,4);o.uniform4fv(this.addr,i)}function Mb(o,e){const i=Ls(e,this.size,4);o.uniformMatrix2fv(this.addr,!1,i)}function yb(o,e){const i=Ls(e,this.size,9);o.uniformMatrix3fv(this.addr,!1,i)}function Eb(o,e){const i=Ls(e,this.size,16);o.uniformMatrix4fv(this.addr,!1,i)}function Tb(o,e){o.uniform1iv(this.addr,e)}function bb(o,e){o.uniform2iv(this.addr,e)}function Ab(o,e){o.uniform3iv(this.addr,e)}function Rb(o,e){o.uniform4iv(this.addr,e)}function Cb(o,e){o.uniform1uiv(this.addr,e)}function Db(o,e){o.uniform2uiv(this.addr,e)}function wb(o,e){o.uniform3uiv(this.addr,e)}function Ub(o,e){o.uniform4uiv(this.addr,e)}function Lb(o,e,i){const r=this.cache,l=e.length,c=Bu(i,l);hn(r,c)||(o.uniform1iv(this.addr,c),dn(r,c));let h;this.type===o.SAMPLER_2D_SHADOW?h=Ed:h=uv;for(let d=0;d!==l;++d)i.setTexture2D(e[d]||h,c[d])}function Nb(o,e,i){const r=this.cache,l=e.length,c=Bu(i,l);hn(r,c)||(o.uniform1iv(this.addr,c),dn(r,c));for(let h=0;h!==l;++h)i.setTexture3D(e[h]||fv,c[h])}function Ob(o,e,i){const r=this.cache,l=e.length,c=Bu(i,l);hn(r,c)||(o.uniform1iv(this.addr,c),dn(r,c));for(let h=0;h!==l;++h)i.setTextureCube(e[h]||hv,c[h])}function Pb(o,e,i){const r=this.cache,l=e.length,c=Bu(i,l);hn(r,c)||(o.uniform1iv(this.addr,c),dn(r,c));for(let h=0;h!==l;++h)i.setTexture2DArray(e[h]||cv,c[h])}function Fb(o){switch(o){case 5126:return _b;case 35664:return vb;case 35665:return xb;case 35666:return Sb;case 35674:return Mb;case 35675:return yb;case 35676:return Eb;case 5124:case 35670:return Tb;case 35667:case 35671:return bb;case 35668:case 35672:return Ab;case 35669:case 35673:return Rb;case 5125:return Cb;case 36294:return Db;case 36295:return wb;case 36296:return Ub;case 35678:case 36198:case 36298:case 36306:case 35682:return Lb;case 35679:case 36299:case 36307:return Nb;case 35680:case 36300:case 36308:case 36293:return Ob;case 36289:case 36303:case 36311:case 36292:return Pb}}class zb{constructor(e,i,r){this.id=e,this.addr=r,this.cache=[],this.type=i.type,this.setValue=gb(i.type)}}class Bb{constructor(e,i,r){this.id=e,this.addr=r,this.cache=[],this.type=i.type,this.size=i.size,this.setValue=Fb(i.type)}}class Ib{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,i,r){const l=this.seq;for(let c=0,h=l.length;c!==h;++c){const d=l[c];d.setValue(e,i[d.id],r)}}}const bh=/(\w+)(\])?(\[|\.)?/g;function p_(o,e){o.seq.push(e),o.map[e.id]=e}function Hb(o,e,i){const r=o.name,l=r.length;for(bh.lastIndex=0;;){const c=bh.exec(r),h=bh.lastIndex;let d=c[1];const m=c[2]==="]",p=c[3];if(m&&(d=d|0),p===void 0||p==="["&&h+2===l){p_(i,p===void 0?new zb(d,o,e):new Bb(d,o,e));break}else{let g=i.map[d];g===void 0&&(g=new Ib(d),p_(i,g)),i=g}}}class Uu{constructor(e,i){this.seq=[],this.map={};const r=e.getProgramParameter(i,e.ACTIVE_UNIFORMS);for(let h=0;h<r;++h){const d=e.getActiveUniform(i,h),m=e.getUniformLocation(i,d.name);Hb(d,m,this)}const l=[],c=[];for(const h of this.seq)h.type===e.SAMPLER_2D_SHADOW||h.type===e.SAMPLER_CUBE_SHADOW||h.type===e.SAMPLER_2D_ARRAY_SHADOW?l.push(h):c.push(h);l.length>0&&(this.seq=l.concat(c))}setValue(e,i,r,l){const c=this.map[i];c!==void 0&&c.setValue(e,r,l)}setOptional(e,i,r){const l=i[r];l!==void 0&&this.setValue(e,r,l)}static upload(e,i,r,l){for(let c=0,h=i.length;c!==h;++c){const d=i[c],m=r[d.id];m.needsUpdate!==!1&&d.setValue(e,m.value,l)}}static seqWithValue(e,i){const r=[];for(let l=0,c=e.length;l!==c;++l){const h=e[l];h.id in i&&r.push(h)}return r}}function m_(o,e,i){const r=o.createShader(e);return o.shaderSource(r,i),o.compileShader(r),r}const Gb=37297;let Vb=0;function Xb(o,e){const i=o.split(`
`),r=[],l=Math.max(e-6,0),c=Math.min(e+6,i.length);for(let h=l;h<c;h++){const d=h+1;r.push(`${d===e?">":" "} ${d}: ${i[h]}`)}return r.join(`
`)}const g_=new ue;function kb(o){ye._getMatrix(g_,ye.workingColorSpace,o);const e=`mat3( ${g_.elements.map(i=>i.toFixed(4))} )`;switch(ye.getTransfer(o)){case Lu:return[e,"LinearTransferOETF"];case Be:return[e,"sRGBTransferOETF"];default:return ae("WebGLProgram: Unsupported color space: ",o),[e,"LinearTransferOETF"]}}function __(o,e,i){const r=o.getShaderParameter(e,o.COMPILE_STATUS),c=(o.getShaderInfoLog(e)||"").trim();if(r&&c==="")return"";const h=/ERROR: 0:(\d+)/.exec(c);if(h){const d=parseInt(h[1]);return i.toUpperCase()+`

`+c+`

`+Xb(o.getShaderSource(e),d)}else return c}function Wb(o,e){const i=kb(e);return[`vec4 ${o}( vec4 value ) {`,`	return ${i[1]}( vec4( value.rgb * ${i[0]}, value.a ) );`,"}"].join(`
`)}const qb={[L_]:"Linear",[N_]:"Reinhard",[O_]:"Cineon",[P_]:"ACESFilmic",[z_]:"AgX",[B_]:"Neutral",[F_]:"Custom"};function Yb(o,e){const i=qb[e];return i===void 0?(ae("WebGLProgram: Unsupported toneMapping:",e),"vec3 "+o+"( vec3 color ) { return LinearToneMapping( color ); }"):"vec3 "+o+"( vec3 color ) { return "+i+"ToneMapping( color ); }"}const bu=new it;function Zb(){ye.getLuminanceCoefficients(bu);const o=bu.x.toFixed(4),e=bu.y.toFixed(4),i=bu.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${o}, ${e}, ${i} );`,"	return dot( weights, rgb );","}"].join(`
`)}function jb(o){return[o.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",o.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(zo).join(`
`)}function Kb(o){const e=[];for(const i in o){const r=o[i];r!==!1&&e.push("#define "+i+" "+r)}return e.join(`
`)}function Qb(o,e){const i={},r=o.getProgramParameter(e,o.ACTIVE_ATTRIBUTES);for(let l=0;l<r;l++){const c=o.getActiveAttrib(e,l),h=c.name;let d=1;c.type===o.FLOAT_MAT2&&(d=2),c.type===o.FLOAT_MAT3&&(d=3),c.type===o.FLOAT_MAT4&&(d=4),i[h]={type:c.type,location:o.getAttribLocation(e,h),locationSize:d}}return i}function zo(o){return o!==""}function v_(o,e){const i=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return o.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,i).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function x_(o,e){return o.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Jb=/^[ \t]*#include +<([\w\d./]+)>/gm;function Td(o){return o.replace(Jb,tA)}const $b=new Map;function tA(o,e){let i=ce[e];if(i===void 0){const r=$b.get(e);if(r!==void 0)i=ce[r],ae('WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,r);else throw new Error("Can not resolve #include <"+e+">")}return Td(i)}const eA=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function S_(o){return o.replace(eA,nA)}function nA(o,e,i,r){let l="";for(let c=parseInt(e);c<parseInt(i);c++)l+=r.replace(/\[\s*i\s*\]/g,"[ "+c+" ]").replace(/UNROLLED_LOOP_INDEX/g,c);return l}function M_(o){let e=`precision ${o.precision} float;
	precision ${o.precision} int;
	precision ${o.precision} sampler2D;
	precision ${o.precision} samplerCube;
	precision ${o.precision} sampler3D;
	precision ${o.precision} sampler2DArray;
	precision ${o.precision} sampler2DShadow;
	precision ${o.precision} samplerCubeShadow;
	precision ${o.precision} sampler2DArrayShadow;
	precision ${o.precision} isampler2D;
	precision ${o.precision} isampler3D;
	precision ${o.precision} isamplerCube;
	precision ${o.precision} isampler2DArray;
	precision ${o.precision} usampler2D;
	precision ${o.precision} usampler3D;
	precision ${o.precision} usamplerCube;
	precision ${o.precision} usampler2DArray;
	`;return o.precision==="highp"?e+=`
#define HIGH_PRECISION`:o.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:o.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}const iA={[Au]:"SHADOWMAP_TYPE_PCF",[Fo]:"SHADOWMAP_TYPE_VSM"};function aA(o){return iA[o.shadowMapType]||"SHADOWMAP_TYPE_BASIC"}const rA={[Rr]:"ENVMAP_TYPE_CUBE",[Rs]:"ENVMAP_TYPE_CUBE",[Pu]:"ENVMAP_TYPE_CUBE_UV"};function sA(o){return o.envMap===!1?"ENVMAP_TYPE_CUBE":rA[o.envMapMode]||"ENVMAP_TYPE_CUBE"}const oA={[Rs]:"ENVMAP_MODE_REFRACTION"};function lA(o){return o.envMap===!1?"ENVMAP_MODE_REFLECTION":oA[o.envMapMode]||"ENVMAP_MODE_REFLECTION"}const uA={[U_]:"ENVMAP_BLENDING_MULTIPLY",[tM]:"ENVMAP_BLENDING_MIX",[eM]:"ENVMAP_BLENDING_ADD"};function cA(o){return o.envMap===!1?"ENVMAP_BLENDING_NONE":uA[o.combine]||"ENVMAP_BLENDING_NONE"}function fA(o){const e=o.envMapCubeUVHeight;if(e===null)return null;const i=Math.log2(e)-2,r=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,i),112)),texelHeight:r,maxMip:i}}function hA(o,e,i,r){const l=o.getContext(),c=i.defines;let h=i.vertexShader,d=i.fragmentShader;const m=aA(i),p=sA(i),v=lA(i),g=cA(i),S=fA(i),M=jb(i),A=Kb(c),C=l.createProgram();let y,x,P=i.glslVersion?"#version "+i.glslVersion+`
`:"";i.isRawShaderMaterial?(y=["#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A].filter(zo).join(`
`),y.length>0&&(y+=`
`),x=["#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A].filter(zo).join(`
`),x.length>0&&(x+=`
`)):(y=[M_(i),"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A,i.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",i.batching?"#define USE_BATCHING":"",i.batchingColor?"#define USE_BATCHING_COLOR":"",i.instancing?"#define USE_INSTANCING":"",i.instancingColor?"#define USE_INSTANCING_COLOR":"",i.instancingMorph?"#define USE_INSTANCING_MORPH":"",i.useFog&&i.fog?"#define USE_FOG":"",i.useFog&&i.fogExp2?"#define FOG_EXP2":"",i.map?"#define USE_MAP":"",i.envMap?"#define USE_ENVMAP":"",i.envMap?"#define "+v:"",i.lightMap?"#define USE_LIGHTMAP":"",i.aoMap?"#define USE_AOMAP":"",i.bumpMap?"#define USE_BUMPMAP":"",i.normalMap?"#define USE_NORMALMAP":"",i.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",i.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",i.displacementMap?"#define USE_DISPLACEMENTMAP":"",i.emissiveMap?"#define USE_EMISSIVEMAP":"",i.anisotropy?"#define USE_ANISOTROPY":"",i.anisotropyMap?"#define USE_ANISOTROPYMAP":"",i.clearcoatMap?"#define USE_CLEARCOATMAP":"",i.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",i.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",i.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",i.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",i.specularMap?"#define USE_SPECULARMAP":"",i.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",i.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",i.roughnessMap?"#define USE_ROUGHNESSMAP":"",i.metalnessMap?"#define USE_METALNESSMAP":"",i.alphaMap?"#define USE_ALPHAMAP":"",i.alphaHash?"#define USE_ALPHAHASH":"",i.transmission?"#define USE_TRANSMISSION":"",i.transmissionMap?"#define USE_TRANSMISSIONMAP":"",i.thicknessMap?"#define USE_THICKNESSMAP":"",i.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",i.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",i.mapUv?"#define MAP_UV "+i.mapUv:"",i.alphaMapUv?"#define ALPHAMAP_UV "+i.alphaMapUv:"",i.lightMapUv?"#define LIGHTMAP_UV "+i.lightMapUv:"",i.aoMapUv?"#define AOMAP_UV "+i.aoMapUv:"",i.emissiveMapUv?"#define EMISSIVEMAP_UV "+i.emissiveMapUv:"",i.bumpMapUv?"#define BUMPMAP_UV "+i.bumpMapUv:"",i.normalMapUv?"#define NORMALMAP_UV "+i.normalMapUv:"",i.displacementMapUv?"#define DISPLACEMENTMAP_UV "+i.displacementMapUv:"",i.metalnessMapUv?"#define METALNESSMAP_UV "+i.metalnessMapUv:"",i.roughnessMapUv?"#define ROUGHNESSMAP_UV "+i.roughnessMapUv:"",i.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+i.anisotropyMapUv:"",i.clearcoatMapUv?"#define CLEARCOATMAP_UV "+i.clearcoatMapUv:"",i.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+i.clearcoatNormalMapUv:"",i.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+i.clearcoatRoughnessMapUv:"",i.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+i.iridescenceMapUv:"",i.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+i.iridescenceThicknessMapUv:"",i.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+i.sheenColorMapUv:"",i.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+i.sheenRoughnessMapUv:"",i.specularMapUv?"#define SPECULARMAP_UV "+i.specularMapUv:"",i.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+i.specularColorMapUv:"",i.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+i.specularIntensityMapUv:"",i.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+i.transmissionMapUv:"",i.thicknessMapUv?"#define THICKNESSMAP_UV "+i.thicknessMapUv:"",i.vertexTangents&&i.flatShading===!1?"#define USE_TANGENT":"",i.vertexColors?"#define USE_COLOR":"",i.vertexAlphas?"#define USE_COLOR_ALPHA":"",i.vertexUv1s?"#define USE_UV1":"",i.vertexUv2s?"#define USE_UV2":"",i.vertexUv3s?"#define USE_UV3":"",i.pointsUvs?"#define USE_POINTS_UV":"",i.flatShading?"#define FLAT_SHADED":"",i.skinning?"#define USE_SKINNING":"",i.morphTargets?"#define USE_MORPHTARGETS":"",i.morphNormals&&i.flatShading===!1?"#define USE_MORPHNORMALS":"",i.morphColors?"#define USE_MORPHCOLORS":"",i.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+i.morphTextureStride:"",i.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+i.morphTargetsCount:"",i.doubleSided?"#define DOUBLE_SIDED":"",i.flipSided?"#define FLIP_SIDED":"",i.shadowMapEnabled?"#define USE_SHADOWMAP":"",i.shadowMapEnabled?"#define "+m:"",i.sizeAttenuation?"#define USE_SIZEATTENUATION":"",i.numLightProbes>0?"#define USE_LIGHT_PROBES":"",i.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",i.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(zo).join(`
`),x=[M_(i),"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A,i.useFog&&i.fog?"#define USE_FOG":"",i.useFog&&i.fogExp2?"#define FOG_EXP2":"",i.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",i.map?"#define USE_MAP":"",i.matcap?"#define USE_MATCAP":"",i.envMap?"#define USE_ENVMAP":"",i.envMap?"#define "+p:"",i.envMap?"#define "+v:"",i.envMap?"#define "+g:"",S?"#define CUBEUV_TEXEL_WIDTH "+S.texelWidth:"",S?"#define CUBEUV_TEXEL_HEIGHT "+S.texelHeight:"",S?"#define CUBEUV_MAX_MIP "+S.maxMip+".0":"",i.lightMap?"#define USE_LIGHTMAP":"",i.aoMap?"#define USE_AOMAP":"",i.bumpMap?"#define USE_BUMPMAP":"",i.normalMap?"#define USE_NORMALMAP":"",i.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",i.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",i.emissiveMap?"#define USE_EMISSIVEMAP":"",i.anisotropy?"#define USE_ANISOTROPY":"",i.anisotropyMap?"#define USE_ANISOTROPYMAP":"",i.clearcoat?"#define USE_CLEARCOAT":"",i.clearcoatMap?"#define USE_CLEARCOATMAP":"",i.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",i.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",i.dispersion?"#define USE_DISPERSION":"",i.iridescence?"#define USE_IRIDESCENCE":"",i.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",i.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",i.specularMap?"#define USE_SPECULARMAP":"",i.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",i.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",i.roughnessMap?"#define USE_ROUGHNESSMAP":"",i.metalnessMap?"#define USE_METALNESSMAP":"",i.alphaMap?"#define USE_ALPHAMAP":"",i.alphaTest?"#define USE_ALPHATEST":"",i.alphaHash?"#define USE_ALPHAHASH":"",i.sheen?"#define USE_SHEEN":"",i.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",i.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",i.transmission?"#define USE_TRANSMISSION":"",i.transmissionMap?"#define USE_TRANSMISSIONMAP":"",i.thicknessMap?"#define USE_THICKNESSMAP":"",i.vertexTangents&&i.flatShading===!1?"#define USE_TANGENT":"",i.vertexColors||i.instancingColor||i.batchingColor?"#define USE_COLOR":"",i.vertexAlphas?"#define USE_COLOR_ALPHA":"",i.vertexUv1s?"#define USE_UV1":"",i.vertexUv2s?"#define USE_UV2":"",i.vertexUv3s?"#define USE_UV3":"",i.pointsUvs?"#define USE_POINTS_UV":"",i.gradientMap?"#define USE_GRADIENTMAP":"",i.flatShading?"#define FLAT_SHADED":"",i.doubleSided?"#define DOUBLE_SIDED":"",i.flipSided?"#define FLIP_SIDED":"",i.shadowMapEnabled?"#define USE_SHADOWMAP":"",i.shadowMapEnabled?"#define "+m:"",i.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",i.numLightProbes>0?"#define USE_LIGHT_PROBES":"",i.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",i.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",i.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",i.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",i.toneMapping!==Oi?"#define TONE_MAPPING":"",i.toneMapping!==Oi?ce.tonemapping_pars_fragment:"",i.toneMapping!==Oi?Yb("toneMapping",i.toneMapping):"",i.dithering?"#define DITHERING":"",i.opaque?"#define OPAQUE":"",ce.colorspace_pars_fragment,Wb("linearToOutputTexel",i.outputColorSpace),Zb(),i.useDepthPacking?"#define DEPTH_PACKING "+i.depthPacking:"",`
`].filter(zo).join(`
`)),h=Td(h),h=v_(h,i),h=x_(h,i),d=Td(d),d=v_(d,i),d=x_(d,i),h=S_(h),d=S_(d),i.isRawShaderMaterial!==!0&&(P=`#version 300 es
`,y=[M,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+y,x=["#define varying in",i.glslVersion===P0?"":"layout(location = 0) out highp vec4 pc_fragColor;",i.glslVersion===P0?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+x);const N=P+y+h,L=P+x+d,B=m_(l,l.VERTEX_SHADER,N),F=m_(l,l.FRAGMENT_SHADER,L);l.attachShader(C,B),l.attachShader(C,F),i.index0AttributeName!==void 0?l.bindAttribLocation(C,0,i.index0AttributeName):i.morphTargets===!0&&l.bindAttribLocation(C,0,"position"),l.linkProgram(C);function z(k){if(o.debug.checkShaderErrors){const rt=l.getProgramInfoLog(C)||"",at=l.getShaderInfoLog(B)||"",ut=l.getShaderInfoLog(F)||"",ht=rt.trim(),O=at.trim(),V=ut.trim();let nt=!0,Mt=!0;if(l.getProgramParameter(C,l.LINK_STATUS)===!1)if(nt=!1,typeof o.debug.onShaderError=="function")o.debug.onShaderError(l,C,B,F);else{const xt=__(l,B,"vertex"),U=__(l,F,"fragment");be("THREE.WebGLProgram: Shader Error "+l.getError()+" - VALIDATE_STATUS "+l.getProgramParameter(C,l.VALIDATE_STATUS)+`

Material Name: `+k.name+`
Material Type: `+k.type+`

Program Info Log: `+ht+`
`+xt+`
`+U)}else ht!==""?ae("WebGLProgram: Program Info Log:",ht):(O===""||V==="")&&(Mt=!1);Mt&&(k.diagnostics={runnable:nt,programLog:ht,vertexShader:{log:O,prefix:y},fragmentShader:{log:V,prefix:x}})}l.deleteShader(B),l.deleteShader(F),Q=new Uu(l,C),R=Qb(l,C)}let Q;this.getUniforms=function(){return Q===void 0&&z(this),Q};let R;this.getAttributes=function(){return R===void 0&&z(this),R};let D=i.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return D===!1&&(D=l.getProgramParameter(C,Gb)),D},this.destroy=function(){r.releaseStatesOfProgram(this),l.deleteProgram(C),this.program=void 0},this.type=i.shaderType,this.name=i.shaderName,this.id=Vb++,this.cacheKey=e,this.usedTimes=1,this.program=C,this.vertexShader=B,this.fragmentShader=F,this}let dA=0;class pA{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const i=e.vertexShader,r=e.fragmentShader,l=this._getShaderStage(i),c=this._getShaderStage(r),h=this._getShaderCacheForMaterial(e);return h.has(l)===!1&&(h.add(l),l.usedTimes++),h.has(c)===!1&&(h.add(c),c.usedTimes++),this}remove(e){const i=this.materialCache.get(e);for(const r of i)r.usedTimes--,r.usedTimes===0&&this.shaderCache.delete(r.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const i=this.materialCache;let r=i.get(e);return r===void 0&&(r=new Set,i.set(e,r)),r}_getShaderStage(e){const i=this.shaderCache;let r=i.get(e);return r===void 0&&(r=new mA(e),i.set(e,r)),r}}class mA{constructor(e){this.id=dA++,this.code=e,this.usedTimes=0}}function gA(o,e,i,r,l,c,h){const d=new K_,m=new pA,p=new Set,v=[],g=new Map,S=l.logarithmicDepthBuffer;let M=l.precision;const A={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distance",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function C(R){return p.add(R),R===0?"uv":`uv${R}`}function y(R,D,k,rt,at){const ut=rt.fog,ht=at.geometry,O=R.isMeshStandardMaterial?rt.environment:null,V=(R.isMeshStandardMaterial?i:e).get(R.envMap||O),nt=V&&V.mapping===Pu?V.image.height:null,Mt=A[R.type];R.precision!==null&&(M=l.getMaxPrecision(R.precision),M!==R.precision&&ae("WebGLProgram.getParameters:",R.precision,"not supported, using",M,"instead."));const xt=ht.morphAttributes.position||ht.morphAttributes.normal||ht.morphAttributes.color,U=xt!==void 0?xt.length:0;let et=0;ht.morphAttributes.position!==void 0&&(et=1),ht.morphAttributes.normal!==void 0&&(et=2),ht.morphAttributes.color!==void 0&&(et=3);let gt,bt,Bt,tt;if(Mt){const Me=Ui[Mt];gt=Me.vertexShader,bt=Me.fragmentShader}else gt=R.vertexShader,bt=R.fragmentShader,m.update(R),Bt=m.getVertexShaderID(R),tt=m.getFragmentShaderID(R);const ct=o.getRenderTarget(),Dt=o.state.buffers.depth.getReversed(),Vt=at.isInstancedMesh===!0,It=at.isBatchedMesh===!0,fe=!!R.map,je=!!R.matcap,me=!!V,he=!!R.aoMap,Ae=!!R.lightMap,re=!!R.bumpMap,Ke=!!R.normalMap,H=!!R.displacementMap,qe=!!R.emissiveMap,Se=!!R.metalnessMap,Le=!!R.roughnessMap,qt=R.anisotropy>0,w=R.clearcoat>0,E=R.dispersion>0,W=R.iridescence>0,dt=R.sheen>0,vt=R.transmission>0,lt=qt&&!!R.anisotropyMap,Zt=w&&!!R.clearcoatMap,Rt=w&&!!R.clearcoatNormalMap,Xt=w&&!!R.clearcoatRoughnessMap,te=W&&!!R.iridescenceMap,yt=W&&!!R.iridescenceThicknessMap,Et=dt&&!!R.sheenColorMap,Ft=dt&&!!R.sheenRoughnessMap,Ot=!!R.specularMap,Ct=!!R.specularColorMap,oe=!!R.specularIntensityMap,X=vt&&!!R.transmissionMap,Ut=vt&&!!R.thicknessMap,Tt=!!R.gradientMap,Pt=!!R.alphaMap,St=R.alphaTest>0,_t=!!R.alphaHash,At=!!R.extensions;let ee=Oi;R.toneMapped&&(ct===null||ct.isXRRenderTarget===!0)&&(ee=o.toneMapping);const Oe={shaderID:Mt,shaderType:R.type,shaderName:R.name,vertexShader:gt,fragmentShader:bt,defines:R.defines,customVertexShaderID:Bt,customFragmentShaderID:tt,isRawShaderMaterial:R.isRawShaderMaterial===!0,glslVersion:R.glslVersion,precision:M,batching:It,batchingColor:It&&at._colorsTexture!==null,instancing:Vt,instancingColor:Vt&&at.instanceColor!==null,instancingMorph:Vt&&at.morphTexture!==null,outputColorSpace:ct===null?o.outputColorSpace:ct.isXRRenderTarget===!0?ct.texture.colorSpace:Ds,alphaToCoverage:!!R.alphaToCoverage,map:fe,matcap:je,envMap:me,envMapMode:me&&V.mapping,envMapCubeUVHeight:nt,aoMap:he,lightMap:Ae,bumpMap:re,normalMap:Ke,displacementMap:H,emissiveMap:qe,normalMapObjectSpace:Ke&&R.normalMapType===aM,normalMapTangentSpace:Ke&&R.normalMapType===Y_,metalnessMap:Se,roughnessMap:Le,anisotropy:qt,anisotropyMap:lt,clearcoat:w,clearcoatMap:Zt,clearcoatNormalMap:Rt,clearcoatRoughnessMap:Xt,dispersion:E,iridescence:W,iridescenceMap:te,iridescenceThicknessMap:yt,sheen:dt,sheenColorMap:Et,sheenRoughnessMap:Ft,specularMap:Ot,specularColorMap:Ct,specularIntensityMap:oe,transmission:vt,transmissionMap:X,thicknessMap:Ut,gradientMap:Tt,opaque:R.transparent===!1&&R.blending===Ts&&R.alphaToCoverage===!1,alphaMap:Pt,alphaTest:St,alphaHash:_t,combine:R.combine,mapUv:fe&&C(R.map.channel),aoMapUv:he&&C(R.aoMap.channel),lightMapUv:Ae&&C(R.lightMap.channel),bumpMapUv:re&&C(R.bumpMap.channel),normalMapUv:Ke&&C(R.normalMap.channel),displacementMapUv:H&&C(R.displacementMap.channel),emissiveMapUv:qe&&C(R.emissiveMap.channel),metalnessMapUv:Se&&C(R.metalnessMap.channel),roughnessMapUv:Le&&C(R.roughnessMap.channel),anisotropyMapUv:lt&&C(R.anisotropyMap.channel),clearcoatMapUv:Zt&&C(R.clearcoatMap.channel),clearcoatNormalMapUv:Rt&&C(R.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:Xt&&C(R.clearcoatRoughnessMap.channel),iridescenceMapUv:te&&C(R.iridescenceMap.channel),iridescenceThicknessMapUv:yt&&C(R.iridescenceThicknessMap.channel),sheenColorMapUv:Et&&C(R.sheenColorMap.channel),sheenRoughnessMapUv:Ft&&C(R.sheenRoughnessMap.channel),specularMapUv:Ot&&C(R.specularMap.channel),specularColorMapUv:Ct&&C(R.specularColorMap.channel),specularIntensityMapUv:oe&&C(R.specularIntensityMap.channel),transmissionMapUv:X&&C(R.transmissionMap.channel),thicknessMapUv:Ut&&C(R.thicknessMap.channel),alphaMapUv:Pt&&C(R.alphaMap.channel),vertexTangents:!!ht.attributes.tangent&&(Ke||qt),vertexColors:R.vertexColors,vertexAlphas:R.vertexColors===!0&&!!ht.attributes.color&&ht.attributes.color.itemSize===4,pointsUvs:at.isPoints===!0&&!!ht.attributes.uv&&(fe||Pt),fog:!!ut,useFog:R.fog===!0,fogExp2:!!ut&&ut.isFogExp2,flatShading:R.flatShading===!0&&R.wireframe===!1,sizeAttenuation:R.sizeAttenuation===!0,logarithmicDepthBuffer:S,reversedDepthBuffer:Dt,skinning:at.isSkinnedMesh===!0,morphTargets:ht.morphAttributes.position!==void 0,morphNormals:ht.morphAttributes.normal!==void 0,morphColors:ht.morphAttributes.color!==void 0,morphTargetsCount:U,morphTextureStride:et,numDirLights:D.directional.length,numPointLights:D.point.length,numSpotLights:D.spot.length,numSpotLightMaps:D.spotLightMap.length,numRectAreaLights:D.rectArea.length,numHemiLights:D.hemi.length,numDirLightShadows:D.directionalShadowMap.length,numPointLightShadows:D.pointShadowMap.length,numSpotLightShadows:D.spotShadowMap.length,numSpotLightShadowsWithMaps:D.numSpotLightShadowsWithMaps,numLightProbes:D.numLightProbes,numClippingPlanes:h.numPlanes,numClipIntersection:h.numIntersection,dithering:R.dithering,shadowMapEnabled:o.shadowMap.enabled&&k.length>0,shadowMapType:o.shadowMap.type,toneMapping:ee,decodeVideoTexture:fe&&R.map.isVideoTexture===!0&&ye.getTransfer(R.map.colorSpace)===Be,decodeVideoTextureEmissive:qe&&R.emissiveMap.isVideoTexture===!0&&ye.getTransfer(R.emissiveMap.colorSpace)===Be,premultipliedAlpha:R.premultipliedAlpha,doubleSided:R.side===ca,flipSided:R.side===Xn,useDepthPacking:R.depthPacking>=0,depthPacking:R.depthPacking||0,index0AttributeName:R.index0AttributeName,extensionClipCullDistance:At&&R.extensions.clipCullDistance===!0&&r.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(At&&R.extensions.multiDraw===!0||It)&&r.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:r.has("KHR_parallel_shader_compile"),customProgramCacheKey:R.customProgramCacheKey()};return Oe.vertexUv1s=p.has(1),Oe.vertexUv2s=p.has(2),Oe.vertexUv3s=p.has(3),p.clear(),Oe}function x(R){const D=[];if(R.shaderID?D.push(R.shaderID):(D.push(R.customVertexShaderID),D.push(R.customFragmentShaderID)),R.defines!==void 0)for(const k in R.defines)D.push(k),D.push(R.defines[k]);return R.isRawShaderMaterial===!1&&(P(D,R),N(D,R),D.push(o.outputColorSpace)),D.push(R.customProgramCacheKey),D.join()}function P(R,D){R.push(D.precision),R.push(D.outputColorSpace),R.push(D.envMapMode),R.push(D.envMapCubeUVHeight),R.push(D.mapUv),R.push(D.alphaMapUv),R.push(D.lightMapUv),R.push(D.aoMapUv),R.push(D.bumpMapUv),R.push(D.normalMapUv),R.push(D.displacementMapUv),R.push(D.emissiveMapUv),R.push(D.metalnessMapUv),R.push(D.roughnessMapUv),R.push(D.anisotropyMapUv),R.push(D.clearcoatMapUv),R.push(D.clearcoatNormalMapUv),R.push(D.clearcoatRoughnessMapUv),R.push(D.iridescenceMapUv),R.push(D.iridescenceThicknessMapUv),R.push(D.sheenColorMapUv),R.push(D.sheenRoughnessMapUv),R.push(D.specularMapUv),R.push(D.specularColorMapUv),R.push(D.specularIntensityMapUv),R.push(D.transmissionMapUv),R.push(D.thicknessMapUv),R.push(D.combine),R.push(D.fogExp2),R.push(D.sizeAttenuation),R.push(D.morphTargetsCount),R.push(D.morphAttributeCount),R.push(D.numDirLights),R.push(D.numPointLights),R.push(D.numSpotLights),R.push(D.numSpotLightMaps),R.push(D.numHemiLights),R.push(D.numRectAreaLights),R.push(D.numDirLightShadows),R.push(D.numPointLightShadows),R.push(D.numSpotLightShadows),R.push(D.numSpotLightShadowsWithMaps),R.push(D.numLightProbes),R.push(D.shadowMapType),R.push(D.toneMapping),R.push(D.numClippingPlanes),R.push(D.numClipIntersection),R.push(D.depthPacking)}function N(R,D){d.disableAll(),D.instancing&&d.enable(0),D.instancingColor&&d.enable(1),D.instancingMorph&&d.enable(2),D.matcap&&d.enable(3),D.envMap&&d.enable(4),D.normalMapObjectSpace&&d.enable(5),D.normalMapTangentSpace&&d.enable(6),D.clearcoat&&d.enable(7),D.iridescence&&d.enable(8),D.alphaTest&&d.enable(9),D.vertexColors&&d.enable(10),D.vertexAlphas&&d.enable(11),D.vertexUv1s&&d.enable(12),D.vertexUv2s&&d.enable(13),D.vertexUv3s&&d.enable(14),D.vertexTangents&&d.enable(15),D.anisotropy&&d.enable(16),D.alphaHash&&d.enable(17),D.batching&&d.enable(18),D.dispersion&&d.enable(19),D.batchingColor&&d.enable(20),D.gradientMap&&d.enable(21),R.push(d.mask),d.disableAll(),D.fog&&d.enable(0),D.useFog&&d.enable(1),D.flatShading&&d.enable(2),D.logarithmicDepthBuffer&&d.enable(3),D.reversedDepthBuffer&&d.enable(4),D.skinning&&d.enable(5),D.morphTargets&&d.enable(6),D.morphNormals&&d.enable(7),D.morphColors&&d.enable(8),D.premultipliedAlpha&&d.enable(9),D.shadowMapEnabled&&d.enable(10),D.doubleSided&&d.enable(11),D.flipSided&&d.enable(12),D.useDepthPacking&&d.enable(13),D.dithering&&d.enable(14),D.transmission&&d.enable(15),D.sheen&&d.enable(16),D.opaque&&d.enable(17),D.pointsUvs&&d.enable(18),D.decodeVideoTexture&&d.enable(19),D.decodeVideoTextureEmissive&&d.enable(20),D.alphaToCoverage&&d.enable(21),R.push(d.mask)}function L(R){const D=A[R.type];let k;if(D){const rt=Ui[D];k=NM.clone(rt.uniforms)}else k=R.uniforms;return k}function B(R,D){let k=g.get(D);return k!==void 0?++k.usedTimes:(k=new hA(o,D,R,c),v.push(k),g.set(D,k)),k}function F(R){if(--R.usedTimes===0){const D=v.indexOf(R);v[D]=v[v.length-1],v.pop(),g.delete(R.cacheKey),R.destroy()}}function z(R){m.remove(R)}function Q(){m.dispose()}return{getParameters:y,getProgramCacheKey:x,getUniforms:L,acquireProgram:B,releaseProgram:F,releaseShaderCache:z,programs:v,dispose:Q}}function _A(){let o=new WeakMap;function e(h){return o.has(h)}function i(h){let d=o.get(h);return d===void 0&&(d={},o.set(h,d)),d}function r(h){o.delete(h)}function l(h,d,m){o.get(h)[d]=m}function c(){o=new WeakMap}return{has:e,get:i,remove:r,update:l,dispose:c}}function vA(o,e){return o.groupOrder!==e.groupOrder?o.groupOrder-e.groupOrder:o.renderOrder!==e.renderOrder?o.renderOrder-e.renderOrder:o.material.id!==e.material.id?o.material.id-e.material.id:o.z!==e.z?o.z-e.z:o.id-e.id}function y_(o,e){return o.groupOrder!==e.groupOrder?o.groupOrder-e.groupOrder:o.renderOrder!==e.renderOrder?o.renderOrder-e.renderOrder:o.z!==e.z?e.z-o.z:o.id-e.id}function E_(){const o=[];let e=0;const i=[],r=[],l=[];function c(){e=0,i.length=0,r.length=0,l.length=0}function h(g,S,M,A,C,y){let x=o[e];return x===void 0?(x={id:g.id,object:g,geometry:S,material:M,groupOrder:A,renderOrder:g.renderOrder,z:C,group:y},o[e]=x):(x.id=g.id,x.object=g,x.geometry=S,x.material=M,x.groupOrder=A,x.renderOrder=g.renderOrder,x.z=C,x.group=y),e++,x}function d(g,S,M,A,C,y){const x=h(g,S,M,A,C,y);M.transmission>0?r.push(x):M.transparent===!0?l.push(x):i.push(x)}function m(g,S,M,A,C,y){const x=h(g,S,M,A,C,y);M.transmission>0?r.unshift(x):M.transparent===!0?l.unshift(x):i.unshift(x)}function p(g,S){i.length>1&&i.sort(g||vA),r.length>1&&r.sort(S||y_),l.length>1&&l.sort(S||y_)}function v(){for(let g=e,S=o.length;g<S;g++){const M=o[g];if(M.id===null)break;M.id=null,M.object=null,M.geometry=null,M.material=null,M.group=null}}return{opaque:i,transmissive:r,transparent:l,init:c,push:d,unshift:m,finish:v,sort:p}}function xA(){let o=new WeakMap;function e(r,l){const c=o.get(r);let h;return c===void 0?(h=new E_,o.set(r,[h])):l>=c.length?(h=new E_,c.push(h)):h=c[l],h}function i(){o=new WeakMap}return{get:e,dispose:i}}function SA(){const o={};return{get:function(e){if(o[e.id]!==void 0)return o[e.id];let i;switch(e.type){case"DirectionalLight":i={direction:new it,color:new we};break;case"SpotLight":i={position:new it,direction:new it,color:new we,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":i={position:new it,color:new we,distance:0,decay:0};break;case"HemisphereLight":i={direction:new it,skyColor:new we,groundColor:new we};break;case"RectAreaLight":i={color:new we,position:new it,halfWidth:new it,halfHeight:new it};break}return o[e.id]=i,i}}}function MA(){const o={};return{get:function(e){if(o[e.id]!==void 0)return o[e.id];let i;switch(e.type){case"DirectionalLight":i={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ue};break;case"SpotLight":i={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ue};break;case"PointLight":i={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ue,shadowCameraNear:1,shadowCameraFar:1e3};break}return o[e.id]=i,i}}}let yA=0;function EA(o,e){return(e.castShadow?2:0)-(o.castShadow?2:0)+(e.map?1:0)-(o.map?1:0)}function TA(o){const e=new SA,i=MA(),r={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let p=0;p<9;p++)r.probe.push(new it);const l=new it,c=new tn,h=new tn;function d(p){let v=0,g=0,S=0;for(let R=0;R<9;R++)r.probe[R].set(0,0,0);let M=0,A=0,C=0,y=0,x=0,P=0,N=0,L=0,B=0,F=0,z=0;p.sort(EA);for(let R=0,D=p.length;R<D;R++){const k=p[R],rt=k.color,at=k.intensity,ut=k.distance;let ht=null;if(k.shadow&&k.shadow.map&&(k.shadow.map.texture.format===Cs?ht=k.shadow.map.texture:ht=k.shadow.map.depthTexture||k.shadow.map.texture),k.isAmbientLight)v+=rt.r*at,g+=rt.g*at,S+=rt.b*at;else if(k.isLightProbe){for(let O=0;O<9;O++)r.probe[O].addScaledVector(k.sh.coefficients[O],at);z++}else if(k.isDirectionalLight){const O=e.get(k);if(O.color.copy(k.color).multiplyScalar(k.intensity),k.castShadow){const V=k.shadow,nt=i.get(k);nt.shadowIntensity=V.intensity,nt.shadowBias=V.bias,nt.shadowNormalBias=V.normalBias,nt.shadowRadius=V.radius,nt.shadowMapSize=V.mapSize,r.directionalShadow[M]=nt,r.directionalShadowMap[M]=ht,r.directionalShadowMatrix[M]=k.shadow.matrix,P++}r.directional[M]=O,M++}else if(k.isSpotLight){const O=e.get(k);O.position.setFromMatrixPosition(k.matrixWorld),O.color.copy(rt).multiplyScalar(at),O.distance=ut,O.coneCos=Math.cos(k.angle),O.penumbraCos=Math.cos(k.angle*(1-k.penumbra)),O.decay=k.decay,r.spot[C]=O;const V=k.shadow;if(k.map&&(r.spotLightMap[B]=k.map,B++,V.updateMatrices(k),k.castShadow&&F++),r.spotLightMatrix[C]=V.matrix,k.castShadow){const nt=i.get(k);nt.shadowIntensity=V.intensity,nt.shadowBias=V.bias,nt.shadowNormalBias=V.normalBias,nt.shadowRadius=V.radius,nt.shadowMapSize=V.mapSize,r.spotShadow[C]=nt,r.spotShadowMap[C]=ht,L++}C++}else if(k.isRectAreaLight){const O=e.get(k);O.color.copy(rt).multiplyScalar(at),O.halfWidth.set(k.width*.5,0,0),O.halfHeight.set(0,k.height*.5,0),r.rectArea[y]=O,y++}else if(k.isPointLight){const O=e.get(k);if(O.color.copy(k.color).multiplyScalar(k.intensity),O.distance=k.distance,O.decay=k.decay,k.castShadow){const V=k.shadow,nt=i.get(k);nt.shadowIntensity=V.intensity,nt.shadowBias=V.bias,nt.shadowNormalBias=V.normalBias,nt.shadowRadius=V.radius,nt.shadowMapSize=V.mapSize,nt.shadowCameraNear=V.camera.near,nt.shadowCameraFar=V.camera.far,r.pointShadow[A]=nt,r.pointShadowMap[A]=ht,r.pointShadowMatrix[A]=k.shadow.matrix,N++}r.point[A]=O,A++}else if(k.isHemisphereLight){const O=e.get(k);O.skyColor.copy(k.color).multiplyScalar(at),O.groundColor.copy(k.groundColor).multiplyScalar(at),r.hemi[x]=O,x++}}y>0&&(o.has("OES_texture_float_linear")===!0?(r.rectAreaLTC1=Nt.LTC_FLOAT_1,r.rectAreaLTC2=Nt.LTC_FLOAT_2):(r.rectAreaLTC1=Nt.LTC_HALF_1,r.rectAreaLTC2=Nt.LTC_HALF_2)),r.ambient[0]=v,r.ambient[1]=g,r.ambient[2]=S;const Q=r.hash;(Q.directionalLength!==M||Q.pointLength!==A||Q.spotLength!==C||Q.rectAreaLength!==y||Q.hemiLength!==x||Q.numDirectionalShadows!==P||Q.numPointShadows!==N||Q.numSpotShadows!==L||Q.numSpotMaps!==B||Q.numLightProbes!==z)&&(r.directional.length=M,r.spot.length=C,r.rectArea.length=y,r.point.length=A,r.hemi.length=x,r.directionalShadow.length=P,r.directionalShadowMap.length=P,r.pointShadow.length=N,r.pointShadowMap.length=N,r.spotShadow.length=L,r.spotShadowMap.length=L,r.directionalShadowMatrix.length=P,r.pointShadowMatrix.length=N,r.spotLightMatrix.length=L+B-F,r.spotLightMap.length=B,r.numSpotLightShadowsWithMaps=F,r.numLightProbes=z,Q.directionalLength=M,Q.pointLength=A,Q.spotLength=C,Q.rectAreaLength=y,Q.hemiLength=x,Q.numDirectionalShadows=P,Q.numPointShadows=N,Q.numSpotShadows=L,Q.numSpotMaps=B,Q.numLightProbes=z,r.version=yA++)}function m(p,v){let g=0,S=0,M=0,A=0,C=0;const y=v.matrixWorldInverse;for(let x=0,P=p.length;x<P;x++){const N=p[x];if(N.isDirectionalLight){const L=r.directional[g];L.direction.setFromMatrixPosition(N.matrixWorld),l.setFromMatrixPosition(N.target.matrixWorld),L.direction.sub(l),L.direction.transformDirection(y),g++}else if(N.isSpotLight){const L=r.spot[M];L.position.setFromMatrixPosition(N.matrixWorld),L.position.applyMatrix4(y),L.direction.setFromMatrixPosition(N.matrixWorld),l.setFromMatrixPosition(N.target.matrixWorld),L.direction.sub(l),L.direction.transformDirection(y),M++}else if(N.isRectAreaLight){const L=r.rectArea[A];L.position.setFromMatrixPosition(N.matrixWorld),L.position.applyMatrix4(y),h.identity(),c.copy(N.matrixWorld),c.premultiply(y),h.extractRotation(c),L.halfWidth.set(N.width*.5,0,0),L.halfHeight.set(0,N.height*.5,0),L.halfWidth.applyMatrix4(h),L.halfHeight.applyMatrix4(h),A++}else if(N.isPointLight){const L=r.point[S];L.position.setFromMatrixPosition(N.matrixWorld),L.position.applyMatrix4(y),S++}else if(N.isHemisphereLight){const L=r.hemi[C];L.direction.setFromMatrixPosition(N.matrixWorld),L.direction.transformDirection(y),C++}}}return{setup:d,setupView:m,state:r}}function T_(o){const e=new TA(o),i=[],r=[];function l(v){p.camera=v,i.length=0,r.length=0}function c(v){i.push(v)}function h(v){r.push(v)}function d(){e.setup(i)}function m(v){e.setupView(i,v)}const p={lightsArray:i,shadowsArray:r,camera:null,lights:e,transmissionRenderTarget:{}};return{init:l,state:p,setupLights:d,setupLightsView:m,pushLight:c,pushShadow:h}}function bA(o){let e=new WeakMap;function i(l,c=0){const h=e.get(l);let d;return h===void 0?(d=new T_(o),e.set(l,[d])):c>=h.length?(d=new T_(o),h.push(d)):d=h[c],d}function r(){e=new WeakMap}return{get:i,dispose:r}}const AA=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,RA=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ).rg;
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ).r;
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( max( 0.0, squared_mean - mean * mean ) );
	gl_FragColor = vec4( mean, std_dev, 0.0, 1.0 );
}`,CA=[new it(1,0,0),new it(-1,0,0),new it(0,1,0),new it(0,-1,0),new it(0,0,1),new it(0,0,-1)],DA=[new it(0,-1,0),new it(0,-1,0),new it(0,0,1),new it(0,0,-1),new it(0,-1,0),new it(0,-1,0)],b_=new tn,Oo=new it,Ah=new it;function wA(o,e,i){let r=new Fd;const l=new Ue,c=new Ue,h=new $e,d=new kM,m=new WM,p={},v=i.maxTextureSize,g={[Qa]:Xn,[Xn]:Qa,[ca]:ca},S=new Ii({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Ue},radius:{value:4}},vertexShader:AA,fragmentShader:RA}),M=S.clone();M.defines.HORIZONTAL_PASS=1;const A=new Hi;A.setAttribute("position",new Fi(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const C=new ga(A,S),y=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=Au;let x=this.type;this.render=function(F,z,Q){if(y.enabled===!1||y.autoUpdate===!1&&y.needsUpdate===!1||F.length===0)return;F.type===PS&&(ae("WebGLShadowMap: PCFSoftShadowMap has been deprecated. Using PCFShadowMap instead."),F.type=Au);const R=o.getRenderTarget(),D=o.getActiveCubeFace(),k=o.getActiveMipmapLevel(),rt=o.state;rt.setBlending(ha),rt.buffers.depth.getReversed()===!0?rt.buffers.color.setClear(0,0,0,0):rt.buffers.color.setClear(1,1,1,1),rt.buffers.depth.setTest(!0),rt.setScissorTest(!1);const at=x!==this.type;at&&z.traverse(function(ut){ut.material&&(Array.isArray(ut.material)?ut.material.forEach(ht=>ht.needsUpdate=!0):ut.material.needsUpdate=!0)});for(let ut=0,ht=F.length;ut<ht;ut++){const O=F[ut],V=O.shadow;if(V===void 0){ae("WebGLShadowMap:",O,"has no shadow.");continue}if(V.autoUpdate===!1&&V.needsUpdate===!1)continue;l.copy(V.mapSize);const nt=V.getFrameExtents();if(l.multiply(nt),c.copy(V.mapSize),(l.x>v||l.y>v)&&(l.x>v&&(c.x=Math.floor(v/nt.x),l.x=c.x*nt.x,V.mapSize.x=c.x),l.y>v&&(c.y=Math.floor(v/nt.y),l.y=c.y*nt.y,V.mapSize.y=c.y)),V.map===null||at===!0){if(V.map!==null&&(V.map.depthTexture!==null&&(V.map.depthTexture.dispose(),V.map.depthTexture=null),V.map.dispose()),this.type===Fo){if(O.isPointLight){ae("WebGLShadowMap: VSM shadow maps are not supported for PointLights. Use PCF or BasicShadowMap instead.");continue}V.map=new Pi(l.x,l.y,{format:Cs,type:pa,minFilter:Un,magFilter:Un,generateMipmaps:!1}),V.map.texture.name=O.name+".shadowMap",V.map.depthTexture=new Go(l.x,l.y,Li),V.map.depthTexture.name=O.name+".shadowMapDepth",V.map.depthTexture.format=ma,V.map.depthTexture.compareFunction=null,V.map.depthTexture.minFilter=An,V.map.depthTexture.magFilter=An}else{O.isPointLight?(V.map=new av(l.x),V.map.depthTexture=new VM(l.x,zi)):(V.map=new Pi(l.x,l.y),V.map.depthTexture=new Go(l.x,l.y,zi)),V.map.depthTexture.name=O.name+".shadowMap",V.map.depthTexture.format=ma;const xt=o.state.buffers.depth.getReversed();this.type===Au?(V.map.depthTexture.compareFunction=xt?Nd:Ld,V.map.depthTexture.minFilter=Un,V.map.depthTexture.magFilter=Un):(V.map.depthTexture.compareFunction=null,V.map.depthTexture.minFilter=An,V.map.depthTexture.magFilter=An)}V.camera.updateProjectionMatrix()}const Mt=V.map.isWebGLCubeRenderTarget?6:1;for(let xt=0;xt<Mt;xt++){if(V.map.isWebGLCubeRenderTarget)o.setRenderTarget(V.map,xt),o.clear();else{xt===0&&(o.setRenderTarget(V.map),o.clear());const U=V.getViewport(xt);h.set(c.x*U.x,c.y*U.y,c.x*U.z,c.y*U.w),rt.viewport(h)}if(O.isPointLight){const U=V.camera,et=V.matrix,gt=O.distance||U.far;gt!==U.far&&(U.far=gt,U.updateProjectionMatrix()),Oo.setFromMatrixPosition(O.matrixWorld),U.position.copy(Oo),Ah.copy(U.position),Ah.add(CA[xt]),U.up.copy(DA[xt]),U.lookAt(Ah),U.updateMatrixWorld(),et.makeTranslation(-Oo.x,-Oo.y,-Oo.z),b_.multiplyMatrices(U.projectionMatrix,U.matrixWorldInverse),V._frustum.setFromProjectionMatrix(b_,U.coordinateSystem,U.reversedDepth)}else V.updateMatrices(O);r=V.getFrustum(),L(z,Q,V.camera,O,this.type)}V.isPointLightShadow!==!0&&this.type===Fo&&P(V,Q),V.needsUpdate=!1}x=this.type,y.needsUpdate=!1,o.setRenderTarget(R,D,k)};function P(F,z){const Q=e.update(C);S.defines.VSM_SAMPLES!==F.blurSamples&&(S.defines.VSM_SAMPLES=F.blurSamples,M.defines.VSM_SAMPLES=F.blurSamples,S.needsUpdate=!0,M.needsUpdate=!0),F.mapPass===null&&(F.mapPass=new Pi(l.x,l.y,{format:Cs,type:pa})),S.uniforms.shadow_pass.value=F.map.depthTexture,S.uniforms.resolution.value=F.mapSize,S.uniforms.radius.value=F.radius,o.setRenderTarget(F.mapPass),o.clear(),o.renderBufferDirect(z,null,Q,S,C,null),M.uniforms.shadow_pass.value=F.mapPass.texture,M.uniforms.resolution.value=F.mapSize,M.uniforms.radius.value=F.radius,o.setRenderTarget(F.map),o.clear(),o.renderBufferDirect(z,null,Q,M,C,null)}function N(F,z,Q,R){let D=null;const k=Q.isPointLight===!0?F.customDistanceMaterial:F.customDepthMaterial;if(k!==void 0)D=k;else if(D=Q.isPointLight===!0?m:d,o.localClippingEnabled&&z.clipShadows===!0&&Array.isArray(z.clippingPlanes)&&z.clippingPlanes.length!==0||z.displacementMap&&z.displacementScale!==0||z.alphaMap&&z.alphaTest>0||z.map&&z.alphaTest>0||z.alphaToCoverage===!0){const rt=D.uuid,at=z.uuid;let ut=p[rt];ut===void 0&&(ut={},p[rt]=ut);let ht=ut[at];ht===void 0&&(ht=D.clone(),ut[at]=ht,z.addEventListener("dispose",B)),D=ht}if(D.visible=z.visible,D.wireframe=z.wireframe,R===Fo?D.side=z.shadowSide!==null?z.shadowSide:z.side:D.side=z.shadowSide!==null?z.shadowSide:g[z.side],D.alphaMap=z.alphaMap,D.alphaTest=z.alphaToCoverage===!0?.5:z.alphaTest,D.map=z.map,D.clipShadows=z.clipShadows,D.clippingPlanes=z.clippingPlanes,D.clipIntersection=z.clipIntersection,D.displacementMap=z.displacementMap,D.displacementScale=z.displacementScale,D.displacementBias=z.displacementBias,D.wireframeLinewidth=z.wireframeLinewidth,D.linewidth=z.linewidth,Q.isPointLight===!0&&D.isMeshDistanceMaterial===!0){const rt=o.properties.get(D);rt.light=Q}return D}function L(F,z,Q,R,D){if(F.visible===!1)return;if(F.layers.test(z.layers)&&(F.isMesh||F.isLine||F.isPoints)&&(F.castShadow||F.receiveShadow&&D===Fo)&&(!F.frustumCulled||r.intersectsObject(F))){F.modelViewMatrix.multiplyMatrices(Q.matrixWorldInverse,F.matrixWorld);const at=e.update(F),ut=F.material;if(Array.isArray(ut)){const ht=at.groups;for(let O=0,V=ht.length;O<V;O++){const nt=ht[O],Mt=ut[nt.materialIndex];if(Mt&&Mt.visible){const xt=N(F,Mt,R,D);F.onBeforeShadow(o,F,z,Q,at,xt,nt),o.renderBufferDirect(Q,null,at,xt,F,nt),F.onAfterShadow(o,F,z,Q,at,xt,nt)}}}else if(ut.visible){const ht=N(F,ut,R,D);F.onBeforeShadow(o,F,z,Q,at,ht,null),o.renderBufferDirect(Q,null,at,ht,F,null),F.onAfterShadow(o,F,z,Q,at,ht,null)}}const rt=F.children;for(let at=0,ut=rt.length;at<ut;at++)L(rt[at],z,Q,R,D)}function B(F){F.target.removeEventListener("dispose",B);for(const Q in p){const R=p[Q],D=F.target.uuid;D in R&&(R[D].dispose(),delete R[D])}}}const UA={[Nh]:Oh,[Ph]:Bh,[Fh]:Ih,[As]:zh,[Oh]:Nh,[Bh]:Ph,[Ih]:Fh,[zh]:As};function LA(o,e){function i(){let X=!1;const Ut=new $e;let Tt=null;const Pt=new $e(0,0,0,0);return{setMask:function(St){Tt!==St&&!X&&(o.colorMask(St,St,St,St),Tt=St)},setLocked:function(St){X=St},setClear:function(St,_t,At,ee,Oe){Oe===!0&&(St*=ee,_t*=ee,At*=ee),Ut.set(St,_t,At,ee),Pt.equals(Ut)===!1&&(o.clearColor(St,_t,At,ee),Pt.copy(Ut))},reset:function(){X=!1,Tt=null,Pt.set(-1,0,0,0)}}}function r(){let X=!1,Ut=!1,Tt=null,Pt=null,St=null;return{setReversed:function(_t){if(Ut!==_t){const At=e.get("EXT_clip_control");_t?At.clipControlEXT(At.LOWER_LEFT_EXT,At.ZERO_TO_ONE_EXT):At.clipControlEXT(At.LOWER_LEFT_EXT,At.NEGATIVE_ONE_TO_ONE_EXT),Ut=_t;const ee=St;St=null,this.setClear(ee)}},getReversed:function(){return Ut},setTest:function(_t){_t?ct(o.DEPTH_TEST):Dt(o.DEPTH_TEST)},setMask:function(_t){Tt!==_t&&!X&&(o.depthMask(_t),Tt=_t)},setFunc:function(_t){if(Ut&&(_t=UA[_t]),Pt!==_t){switch(_t){case Nh:o.depthFunc(o.NEVER);break;case Oh:o.depthFunc(o.ALWAYS);break;case Ph:o.depthFunc(o.LESS);break;case As:o.depthFunc(o.LEQUAL);break;case Fh:o.depthFunc(o.EQUAL);break;case zh:o.depthFunc(o.GEQUAL);break;case Bh:o.depthFunc(o.GREATER);break;case Ih:o.depthFunc(o.NOTEQUAL);break;default:o.depthFunc(o.LEQUAL)}Pt=_t}},setLocked:function(_t){X=_t},setClear:function(_t){St!==_t&&(Ut&&(_t=1-_t),o.clearDepth(_t),St=_t)},reset:function(){X=!1,Tt=null,Pt=null,St=null,Ut=!1}}}function l(){let X=!1,Ut=null,Tt=null,Pt=null,St=null,_t=null,At=null,ee=null,Oe=null;return{setTest:function(Me){X||(Me?ct(o.STENCIL_TEST):Dt(o.STENCIL_TEST))},setMask:function(Me){Ut!==Me&&!X&&(o.stencilMask(Me),Ut=Me)},setFunc:function(Me,Rn,di){(Tt!==Me||Pt!==Rn||St!==di)&&(o.stencilFunc(Me,Rn,di),Tt=Me,Pt=Rn,St=di)},setOp:function(Me,Rn,di){(_t!==Me||At!==Rn||ee!==di)&&(o.stencilOp(Me,Rn,di),_t=Me,At=Rn,ee=di)},setLocked:function(Me){X=Me},setClear:function(Me){Oe!==Me&&(o.clearStencil(Me),Oe=Me)},reset:function(){X=!1,Ut=null,Tt=null,Pt=null,St=null,_t=null,At=null,ee=null,Oe=null}}}const c=new i,h=new r,d=new l,m=new WeakMap,p=new WeakMap;let v={},g={},S=new WeakMap,M=[],A=null,C=!1,y=null,x=null,P=null,N=null,L=null,B=null,F=null,z=new we(0,0,0),Q=0,R=!1,D=null,k=null,rt=null,at=null,ut=null;const ht=o.getParameter(o.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let O=!1,V=0;const nt=o.getParameter(o.VERSION);nt.indexOf("WebGL")!==-1?(V=parseFloat(/^WebGL (\d)/.exec(nt)[1]),O=V>=1):nt.indexOf("OpenGL ES")!==-1&&(V=parseFloat(/^OpenGL ES (\d)/.exec(nt)[1]),O=V>=2);let Mt=null,xt={};const U=o.getParameter(o.SCISSOR_BOX),et=o.getParameter(o.VIEWPORT),gt=new $e().fromArray(U),bt=new $e().fromArray(et);function Bt(X,Ut,Tt,Pt){const St=new Uint8Array(4),_t=o.createTexture();o.bindTexture(X,_t),o.texParameteri(X,o.TEXTURE_MIN_FILTER,o.NEAREST),o.texParameteri(X,o.TEXTURE_MAG_FILTER,o.NEAREST);for(let At=0;At<Tt;At++)X===o.TEXTURE_3D||X===o.TEXTURE_2D_ARRAY?o.texImage3D(Ut,0,o.RGBA,1,1,Pt,0,o.RGBA,o.UNSIGNED_BYTE,St):o.texImage2D(Ut+At,0,o.RGBA,1,1,0,o.RGBA,o.UNSIGNED_BYTE,St);return _t}const tt={};tt[o.TEXTURE_2D]=Bt(o.TEXTURE_2D,o.TEXTURE_2D,1),tt[o.TEXTURE_CUBE_MAP]=Bt(o.TEXTURE_CUBE_MAP,o.TEXTURE_CUBE_MAP_POSITIVE_X,6),tt[o.TEXTURE_2D_ARRAY]=Bt(o.TEXTURE_2D_ARRAY,o.TEXTURE_2D_ARRAY,1,1),tt[o.TEXTURE_3D]=Bt(o.TEXTURE_3D,o.TEXTURE_3D,1,1),c.setClear(0,0,0,1),h.setClear(1),d.setClear(0),ct(o.DEPTH_TEST),h.setFunc(As),re(!1),Ke(D0),ct(o.CULL_FACE),he(ha);function ct(X){v[X]!==!0&&(o.enable(X),v[X]=!0)}function Dt(X){v[X]!==!1&&(o.disable(X),v[X]=!1)}function Vt(X,Ut){return g[X]!==Ut?(o.bindFramebuffer(X,Ut),g[X]=Ut,X===o.DRAW_FRAMEBUFFER&&(g[o.FRAMEBUFFER]=Ut),X===o.FRAMEBUFFER&&(g[o.DRAW_FRAMEBUFFER]=Ut),!0):!1}function It(X,Ut){let Tt=M,Pt=!1;if(X){Tt=S.get(Ut),Tt===void 0&&(Tt=[],S.set(Ut,Tt));const St=X.textures;if(Tt.length!==St.length||Tt[0]!==o.COLOR_ATTACHMENT0){for(let _t=0,At=St.length;_t<At;_t++)Tt[_t]=o.COLOR_ATTACHMENT0+_t;Tt.length=St.length,Pt=!0}}else Tt[0]!==o.BACK&&(Tt[0]=o.BACK,Pt=!0);Pt&&o.drawBuffers(Tt)}function fe(X){return A!==X?(o.useProgram(X),A=X,!0):!1}const je={[Er]:o.FUNC_ADD,[zS]:o.FUNC_SUBTRACT,[BS]:o.FUNC_REVERSE_SUBTRACT};je[IS]=o.MIN,je[HS]=o.MAX;const me={[GS]:o.ZERO,[VS]:o.ONE,[XS]:o.SRC_COLOR,[Uh]:o.SRC_ALPHA,[jS]:o.SRC_ALPHA_SATURATE,[YS]:o.DST_COLOR,[WS]:o.DST_ALPHA,[kS]:o.ONE_MINUS_SRC_COLOR,[Lh]:o.ONE_MINUS_SRC_ALPHA,[ZS]:o.ONE_MINUS_DST_COLOR,[qS]:o.ONE_MINUS_DST_ALPHA,[KS]:o.CONSTANT_COLOR,[QS]:o.ONE_MINUS_CONSTANT_COLOR,[JS]:o.CONSTANT_ALPHA,[$S]:o.ONE_MINUS_CONSTANT_ALPHA};function he(X,Ut,Tt,Pt,St,_t,At,ee,Oe,Me){if(X===ha){C===!0&&(Dt(o.BLEND),C=!1);return}if(C===!1&&(ct(o.BLEND),C=!0),X!==FS){if(X!==y||Me!==R){if((x!==Er||L!==Er)&&(o.blendEquation(o.FUNC_ADD),x=Er,L=Er),Me)switch(X){case Ts:o.blendFuncSeparate(o.ONE,o.ONE_MINUS_SRC_ALPHA,o.ONE,o.ONE_MINUS_SRC_ALPHA);break;case w0:o.blendFunc(o.ONE,o.ONE);break;case U0:o.blendFuncSeparate(o.ZERO,o.ONE_MINUS_SRC_COLOR,o.ZERO,o.ONE);break;case L0:o.blendFuncSeparate(o.DST_COLOR,o.ONE_MINUS_SRC_ALPHA,o.ZERO,o.ONE);break;default:be("WebGLState: Invalid blending: ",X);break}else switch(X){case Ts:o.blendFuncSeparate(o.SRC_ALPHA,o.ONE_MINUS_SRC_ALPHA,o.ONE,o.ONE_MINUS_SRC_ALPHA);break;case w0:o.blendFuncSeparate(o.SRC_ALPHA,o.ONE,o.ONE,o.ONE);break;case U0:be("WebGLState: SubtractiveBlending requires material.premultipliedAlpha = true");break;case L0:be("WebGLState: MultiplyBlending requires material.premultipliedAlpha = true");break;default:be("WebGLState: Invalid blending: ",X);break}P=null,N=null,B=null,F=null,z.set(0,0,0),Q=0,y=X,R=Me}return}St=St||Ut,_t=_t||Tt,At=At||Pt,(Ut!==x||St!==L)&&(o.blendEquationSeparate(je[Ut],je[St]),x=Ut,L=St),(Tt!==P||Pt!==N||_t!==B||At!==F)&&(o.blendFuncSeparate(me[Tt],me[Pt],me[_t],me[At]),P=Tt,N=Pt,B=_t,F=At),(ee.equals(z)===!1||Oe!==Q)&&(o.blendColor(ee.r,ee.g,ee.b,Oe),z.copy(ee),Q=Oe),y=X,R=!1}function Ae(X,Ut){X.side===ca?Dt(o.CULL_FACE):ct(o.CULL_FACE);let Tt=X.side===Xn;Ut&&(Tt=!Tt),re(Tt),X.blending===Ts&&X.transparent===!1?he(ha):he(X.blending,X.blendEquation,X.blendSrc,X.blendDst,X.blendEquationAlpha,X.blendSrcAlpha,X.blendDstAlpha,X.blendColor,X.blendAlpha,X.premultipliedAlpha),h.setFunc(X.depthFunc),h.setTest(X.depthTest),h.setMask(X.depthWrite),c.setMask(X.colorWrite);const Pt=X.stencilWrite;d.setTest(Pt),Pt&&(d.setMask(X.stencilWriteMask),d.setFunc(X.stencilFunc,X.stencilRef,X.stencilFuncMask),d.setOp(X.stencilFail,X.stencilZFail,X.stencilZPass)),qe(X.polygonOffset,X.polygonOffsetFactor,X.polygonOffsetUnits),X.alphaToCoverage===!0?ct(o.SAMPLE_ALPHA_TO_COVERAGE):Dt(o.SAMPLE_ALPHA_TO_COVERAGE)}function re(X){D!==X&&(X?o.frontFace(o.CW):o.frontFace(o.CCW),D=X)}function Ke(X){X!==NS?(ct(o.CULL_FACE),X!==k&&(X===D0?o.cullFace(o.BACK):X===OS?o.cullFace(o.FRONT):o.cullFace(o.FRONT_AND_BACK))):Dt(o.CULL_FACE),k=X}function H(X){X!==rt&&(O&&o.lineWidth(X),rt=X)}function qe(X,Ut,Tt){X?(ct(o.POLYGON_OFFSET_FILL),(at!==Ut||ut!==Tt)&&(o.polygonOffset(Ut,Tt),at=Ut,ut=Tt)):Dt(o.POLYGON_OFFSET_FILL)}function Se(X){X?ct(o.SCISSOR_TEST):Dt(o.SCISSOR_TEST)}function Le(X){X===void 0&&(X=o.TEXTURE0+ht-1),Mt!==X&&(o.activeTexture(X),Mt=X)}function qt(X,Ut,Tt){Tt===void 0&&(Mt===null?Tt=o.TEXTURE0+ht-1:Tt=Mt);let Pt=xt[Tt];Pt===void 0&&(Pt={type:void 0,texture:void 0},xt[Tt]=Pt),(Pt.type!==X||Pt.texture!==Ut)&&(Mt!==Tt&&(o.activeTexture(Tt),Mt=Tt),o.bindTexture(X,Ut||tt[X]),Pt.type=X,Pt.texture=Ut)}function w(){const X=xt[Mt];X!==void 0&&X.type!==void 0&&(o.bindTexture(X.type,null),X.type=void 0,X.texture=void 0)}function E(){try{o.compressedTexImage2D(...arguments)}catch(X){be("WebGLState:",X)}}function W(){try{o.compressedTexImage3D(...arguments)}catch(X){be("WebGLState:",X)}}function dt(){try{o.texSubImage2D(...arguments)}catch(X){be("WebGLState:",X)}}function vt(){try{o.texSubImage3D(...arguments)}catch(X){be("WebGLState:",X)}}function lt(){try{o.compressedTexSubImage2D(...arguments)}catch(X){be("WebGLState:",X)}}function Zt(){try{o.compressedTexSubImage3D(...arguments)}catch(X){be("WebGLState:",X)}}function Rt(){try{o.texStorage2D(...arguments)}catch(X){be("WebGLState:",X)}}function Xt(){try{o.texStorage3D(...arguments)}catch(X){be("WebGLState:",X)}}function te(){try{o.texImage2D(...arguments)}catch(X){be("WebGLState:",X)}}function yt(){try{o.texImage3D(...arguments)}catch(X){be("WebGLState:",X)}}function Et(X){gt.equals(X)===!1&&(o.scissor(X.x,X.y,X.z,X.w),gt.copy(X))}function Ft(X){bt.equals(X)===!1&&(o.viewport(X.x,X.y,X.z,X.w),bt.copy(X))}function Ot(X,Ut){let Tt=p.get(Ut);Tt===void 0&&(Tt=new WeakMap,p.set(Ut,Tt));let Pt=Tt.get(X);Pt===void 0&&(Pt=o.getUniformBlockIndex(Ut,X.name),Tt.set(X,Pt))}function Ct(X,Ut){const Pt=p.get(Ut).get(X);m.get(Ut)!==Pt&&(o.uniformBlockBinding(Ut,Pt,X.__bindingPointIndex),m.set(Ut,Pt))}function oe(){o.disable(o.BLEND),o.disable(o.CULL_FACE),o.disable(o.DEPTH_TEST),o.disable(o.POLYGON_OFFSET_FILL),o.disable(o.SCISSOR_TEST),o.disable(o.STENCIL_TEST),o.disable(o.SAMPLE_ALPHA_TO_COVERAGE),o.blendEquation(o.FUNC_ADD),o.blendFunc(o.ONE,o.ZERO),o.blendFuncSeparate(o.ONE,o.ZERO,o.ONE,o.ZERO),o.blendColor(0,0,0,0),o.colorMask(!0,!0,!0,!0),o.clearColor(0,0,0,0),o.depthMask(!0),o.depthFunc(o.LESS),h.setReversed(!1),o.clearDepth(1),o.stencilMask(4294967295),o.stencilFunc(o.ALWAYS,0,4294967295),o.stencilOp(o.KEEP,o.KEEP,o.KEEP),o.clearStencil(0),o.cullFace(o.BACK),o.frontFace(o.CCW),o.polygonOffset(0,0),o.activeTexture(o.TEXTURE0),o.bindFramebuffer(o.FRAMEBUFFER,null),o.bindFramebuffer(o.DRAW_FRAMEBUFFER,null),o.bindFramebuffer(o.READ_FRAMEBUFFER,null),o.useProgram(null),o.lineWidth(1),o.scissor(0,0,o.canvas.width,o.canvas.height),o.viewport(0,0,o.canvas.width,o.canvas.height),v={},Mt=null,xt={},g={},S=new WeakMap,M=[],A=null,C=!1,y=null,x=null,P=null,N=null,L=null,B=null,F=null,z=new we(0,0,0),Q=0,R=!1,D=null,k=null,rt=null,at=null,ut=null,gt.set(0,0,o.canvas.width,o.canvas.height),bt.set(0,0,o.canvas.width,o.canvas.height),c.reset(),h.reset(),d.reset()}return{buffers:{color:c,depth:h,stencil:d},enable:ct,disable:Dt,bindFramebuffer:Vt,drawBuffers:It,useProgram:fe,setBlending:he,setMaterial:Ae,setFlipSided:re,setCullFace:Ke,setLineWidth:H,setPolygonOffset:qe,setScissorTest:Se,activeTexture:Le,bindTexture:qt,unbindTexture:w,compressedTexImage2D:E,compressedTexImage3D:W,texImage2D:te,texImage3D:yt,updateUBOMapping:Ot,uniformBlockBinding:Ct,texStorage2D:Rt,texStorage3D:Xt,texSubImage2D:dt,texSubImage3D:vt,compressedTexSubImage2D:lt,compressedTexSubImage3D:Zt,scissor:Et,viewport:Ft,reset:oe}}function NA(o,e,i,r,l,c,h){const d=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,m=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),p=new Ue,v=new WeakMap;let g;const S=new WeakMap;let M=!1;try{M=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function A(w,E){return M?new OffscreenCanvas(w,E):Ou("canvas")}function C(w,E,W){let dt=1;const vt=qt(w);if((vt.width>W||vt.height>W)&&(dt=W/Math.max(vt.width,vt.height)),dt<1)if(typeof HTMLImageElement<"u"&&w instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&w instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&w instanceof ImageBitmap||typeof VideoFrame<"u"&&w instanceof VideoFrame){const lt=Math.floor(dt*vt.width),Zt=Math.floor(dt*vt.height);g===void 0&&(g=A(lt,Zt));const Rt=E?A(lt,Zt):g;return Rt.width=lt,Rt.height=Zt,Rt.getContext("2d").drawImage(w,0,0,lt,Zt),ae("WebGLRenderer: Texture has been resized from ("+vt.width+"x"+vt.height+") to ("+lt+"x"+Zt+")."),Rt}else return"data"in w&&ae("WebGLRenderer: Image in DataTexture is too big ("+vt.width+"x"+vt.height+")."),w;return w}function y(w){return w.generateMipmaps}function x(w){o.generateMipmap(w)}function P(w){return w.isWebGLCubeRenderTarget?o.TEXTURE_CUBE_MAP:w.isWebGL3DRenderTarget?o.TEXTURE_3D:w.isWebGLArrayRenderTarget||w.isCompressedArrayTexture?o.TEXTURE_2D_ARRAY:o.TEXTURE_2D}function N(w,E,W,dt,vt=!1){if(w!==null){if(o[w]!==void 0)return o[w];ae("WebGLRenderer: Attempt to use non-existing WebGL internal format '"+w+"'")}let lt=E;if(E===o.RED&&(W===o.FLOAT&&(lt=o.R32F),W===o.HALF_FLOAT&&(lt=o.R16F),W===o.UNSIGNED_BYTE&&(lt=o.R8)),E===o.RED_INTEGER&&(W===o.UNSIGNED_BYTE&&(lt=o.R8UI),W===o.UNSIGNED_SHORT&&(lt=o.R16UI),W===o.UNSIGNED_INT&&(lt=o.R32UI),W===o.BYTE&&(lt=o.R8I),W===o.SHORT&&(lt=o.R16I),W===o.INT&&(lt=o.R32I)),E===o.RG&&(W===o.FLOAT&&(lt=o.RG32F),W===o.HALF_FLOAT&&(lt=o.RG16F),W===o.UNSIGNED_BYTE&&(lt=o.RG8)),E===o.RG_INTEGER&&(W===o.UNSIGNED_BYTE&&(lt=o.RG8UI),W===o.UNSIGNED_SHORT&&(lt=o.RG16UI),W===o.UNSIGNED_INT&&(lt=o.RG32UI),W===o.BYTE&&(lt=o.RG8I),W===o.SHORT&&(lt=o.RG16I),W===o.INT&&(lt=o.RG32I)),E===o.RGB_INTEGER&&(W===o.UNSIGNED_BYTE&&(lt=o.RGB8UI),W===o.UNSIGNED_SHORT&&(lt=o.RGB16UI),W===o.UNSIGNED_INT&&(lt=o.RGB32UI),W===o.BYTE&&(lt=o.RGB8I),W===o.SHORT&&(lt=o.RGB16I),W===o.INT&&(lt=o.RGB32I)),E===o.RGBA_INTEGER&&(W===o.UNSIGNED_BYTE&&(lt=o.RGBA8UI),W===o.UNSIGNED_SHORT&&(lt=o.RGBA16UI),W===o.UNSIGNED_INT&&(lt=o.RGBA32UI),W===o.BYTE&&(lt=o.RGBA8I),W===o.SHORT&&(lt=o.RGBA16I),W===o.INT&&(lt=o.RGBA32I)),E===o.RGB&&(W===o.UNSIGNED_INT_5_9_9_9_REV&&(lt=o.RGB9_E5),W===o.UNSIGNED_INT_10F_11F_11F_REV&&(lt=o.R11F_G11F_B10F)),E===o.RGBA){const Zt=vt?Lu:ye.getTransfer(dt);W===o.FLOAT&&(lt=o.RGBA32F),W===o.HALF_FLOAT&&(lt=o.RGBA16F),W===o.UNSIGNED_BYTE&&(lt=Zt===Be?o.SRGB8_ALPHA8:o.RGBA8),W===o.UNSIGNED_SHORT_4_4_4_4&&(lt=o.RGBA4),W===o.UNSIGNED_SHORT_5_5_5_1&&(lt=o.RGB5_A1)}return(lt===o.R16F||lt===o.R32F||lt===o.RG16F||lt===o.RG32F||lt===o.RGBA16F||lt===o.RGBA32F)&&e.get("EXT_color_buffer_float"),lt}function L(w,E){let W;return w?E===null||E===zi||E===Io?W=o.DEPTH24_STENCIL8:E===Li?W=o.DEPTH32F_STENCIL8:E===Bo&&(W=o.DEPTH24_STENCIL8,ae("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):E===null||E===zi||E===Io?W=o.DEPTH_COMPONENT24:E===Li?W=o.DEPTH_COMPONENT32F:E===Bo&&(W=o.DEPTH_COMPONENT16),W}function B(w,E){return y(w)===!0||w.isFramebufferTexture&&w.minFilter!==An&&w.minFilter!==Un?Math.log2(Math.max(E.width,E.height))+1:w.mipmaps!==void 0&&w.mipmaps.length>0?w.mipmaps.length:w.isCompressedTexture&&Array.isArray(w.image)?E.mipmaps.length:1}function F(w){const E=w.target;E.removeEventListener("dispose",F),Q(E),E.isVideoTexture&&v.delete(E)}function z(w){const E=w.target;E.removeEventListener("dispose",z),D(E)}function Q(w){const E=r.get(w);if(E.__webglInit===void 0)return;const W=w.source,dt=S.get(W);if(dt){const vt=dt[E.__cacheKey];vt.usedTimes--,vt.usedTimes===0&&R(w),Object.keys(dt).length===0&&S.delete(W)}r.remove(w)}function R(w){const E=r.get(w);o.deleteTexture(E.__webglTexture);const W=w.source,dt=S.get(W);delete dt[E.__cacheKey],h.memory.textures--}function D(w){const E=r.get(w);if(w.depthTexture&&(w.depthTexture.dispose(),r.remove(w.depthTexture)),w.isWebGLCubeRenderTarget)for(let dt=0;dt<6;dt++){if(Array.isArray(E.__webglFramebuffer[dt]))for(let vt=0;vt<E.__webglFramebuffer[dt].length;vt++)o.deleteFramebuffer(E.__webglFramebuffer[dt][vt]);else o.deleteFramebuffer(E.__webglFramebuffer[dt]);E.__webglDepthbuffer&&o.deleteRenderbuffer(E.__webglDepthbuffer[dt])}else{if(Array.isArray(E.__webglFramebuffer))for(let dt=0;dt<E.__webglFramebuffer.length;dt++)o.deleteFramebuffer(E.__webglFramebuffer[dt]);else o.deleteFramebuffer(E.__webglFramebuffer);if(E.__webglDepthbuffer&&o.deleteRenderbuffer(E.__webglDepthbuffer),E.__webglMultisampledFramebuffer&&o.deleteFramebuffer(E.__webglMultisampledFramebuffer),E.__webglColorRenderbuffer)for(let dt=0;dt<E.__webglColorRenderbuffer.length;dt++)E.__webglColorRenderbuffer[dt]&&o.deleteRenderbuffer(E.__webglColorRenderbuffer[dt]);E.__webglDepthRenderbuffer&&o.deleteRenderbuffer(E.__webglDepthRenderbuffer)}const W=w.textures;for(let dt=0,vt=W.length;dt<vt;dt++){const lt=r.get(W[dt]);lt.__webglTexture&&(o.deleteTexture(lt.__webglTexture),h.memory.textures--),r.remove(W[dt])}r.remove(w)}let k=0;function rt(){k=0}function at(){const w=k;return w>=l.maxTextures&&ae("WebGLTextures: Trying to use "+w+" texture units while this GPU supports only "+l.maxTextures),k+=1,w}function ut(w){const E=[];return E.push(w.wrapS),E.push(w.wrapT),E.push(w.wrapR||0),E.push(w.magFilter),E.push(w.minFilter),E.push(w.anisotropy),E.push(w.internalFormat),E.push(w.format),E.push(w.type),E.push(w.generateMipmaps),E.push(w.premultiplyAlpha),E.push(w.flipY),E.push(w.unpackAlignment),E.push(w.colorSpace),E.join()}function ht(w,E){const W=r.get(w);if(w.isVideoTexture&&Se(w),w.isRenderTargetTexture===!1&&w.isExternalTexture!==!0&&w.version>0&&W.__version!==w.version){const dt=w.image;if(dt===null)ae("WebGLRenderer: Texture marked for update but no image data found.");else if(dt.complete===!1)ae("WebGLRenderer: Texture marked for update but image is incomplete");else{tt(W,w,E);return}}else w.isExternalTexture&&(W.__webglTexture=w.sourceTexture?w.sourceTexture:null);i.bindTexture(o.TEXTURE_2D,W.__webglTexture,o.TEXTURE0+E)}function O(w,E){const W=r.get(w);if(w.isRenderTargetTexture===!1&&w.version>0&&W.__version!==w.version){tt(W,w,E);return}else w.isExternalTexture&&(W.__webglTexture=w.sourceTexture?w.sourceTexture:null);i.bindTexture(o.TEXTURE_2D_ARRAY,W.__webglTexture,o.TEXTURE0+E)}function V(w,E){const W=r.get(w);if(w.isRenderTargetTexture===!1&&w.version>0&&W.__version!==w.version){tt(W,w,E);return}i.bindTexture(o.TEXTURE_3D,W.__webglTexture,o.TEXTURE0+E)}function nt(w,E){const W=r.get(w);if(w.isCubeDepthTexture!==!0&&w.version>0&&W.__version!==w.version){ct(W,w,E);return}i.bindTexture(o.TEXTURE_CUBE_MAP,W.__webglTexture,o.TEXTURE0+E)}const Mt={[Vh]:o.REPEAT,[fa]:o.CLAMP_TO_EDGE,[Xh]:o.MIRRORED_REPEAT},xt={[An]:o.NEAREST,[nM]:o.NEAREST_MIPMAP_NEAREST,[ru]:o.NEAREST_MIPMAP_LINEAR,[Un]:o.LINEAR,[jf]:o.LINEAR_MIPMAP_NEAREST,[br]:o.LINEAR_MIPMAP_LINEAR},U={[rM]:o.NEVER,[cM]:o.ALWAYS,[sM]:o.LESS,[Ld]:o.LEQUAL,[oM]:o.EQUAL,[Nd]:o.GEQUAL,[lM]:o.GREATER,[uM]:o.NOTEQUAL};function et(w,E){if(E.type===Li&&e.has("OES_texture_float_linear")===!1&&(E.magFilter===Un||E.magFilter===jf||E.magFilter===ru||E.magFilter===br||E.minFilter===Un||E.minFilter===jf||E.minFilter===ru||E.minFilter===br)&&ae("WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),o.texParameteri(w,o.TEXTURE_WRAP_S,Mt[E.wrapS]),o.texParameteri(w,o.TEXTURE_WRAP_T,Mt[E.wrapT]),(w===o.TEXTURE_3D||w===o.TEXTURE_2D_ARRAY)&&o.texParameteri(w,o.TEXTURE_WRAP_R,Mt[E.wrapR]),o.texParameteri(w,o.TEXTURE_MAG_FILTER,xt[E.magFilter]),o.texParameteri(w,o.TEXTURE_MIN_FILTER,xt[E.minFilter]),E.compareFunction&&(o.texParameteri(w,o.TEXTURE_COMPARE_MODE,o.COMPARE_REF_TO_TEXTURE),o.texParameteri(w,o.TEXTURE_COMPARE_FUNC,U[E.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(E.magFilter===An||E.minFilter!==ru&&E.minFilter!==br||E.type===Li&&e.has("OES_texture_float_linear")===!1)return;if(E.anisotropy>1||r.get(E).__currentAnisotropy){const W=e.get("EXT_texture_filter_anisotropic");o.texParameterf(w,W.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(E.anisotropy,l.getMaxAnisotropy())),r.get(E).__currentAnisotropy=E.anisotropy}}}function gt(w,E){let W=!1;w.__webglInit===void 0&&(w.__webglInit=!0,E.addEventListener("dispose",F));const dt=E.source;let vt=S.get(dt);vt===void 0&&(vt={},S.set(dt,vt));const lt=ut(E);if(lt!==w.__cacheKey){vt[lt]===void 0&&(vt[lt]={texture:o.createTexture(),usedTimes:0},h.memory.textures++,W=!0),vt[lt].usedTimes++;const Zt=vt[w.__cacheKey];Zt!==void 0&&(vt[w.__cacheKey].usedTimes--,Zt.usedTimes===0&&R(E)),w.__cacheKey=lt,w.__webglTexture=vt[lt].texture}return W}function bt(w,E,W){return Math.floor(Math.floor(w/W)/E)}function Bt(w,E,W,dt){const lt=w.updateRanges;if(lt.length===0)i.texSubImage2D(o.TEXTURE_2D,0,0,0,E.width,E.height,W,dt,E.data);else{lt.sort((yt,Et)=>yt.start-Et.start);let Zt=0;for(let yt=1;yt<lt.length;yt++){const Et=lt[Zt],Ft=lt[yt],Ot=Et.start+Et.count,Ct=bt(Ft.start,E.width,4),oe=bt(Et.start,E.width,4);Ft.start<=Ot+1&&Ct===oe&&bt(Ft.start+Ft.count-1,E.width,4)===Ct?Et.count=Math.max(Et.count,Ft.start+Ft.count-Et.start):(++Zt,lt[Zt]=Ft)}lt.length=Zt+1;const Rt=o.getParameter(o.UNPACK_ROW_LENGTH),Xt=o.getParameter(o.UNPACK_SKIP_PIXELS),te=o.getParameter(o.UNPACK_SKIP_ROWS);o.pixelStorei(o.UNPACK_ROW_LENGTH,E.width);for(let yt=0,Et=lt.length;yt<Et;yt++){const Ft=lt[yt],Ot=Math.floor(Ft.start/4),Ct=Math.ceil(Ft.count/4),oe=Ot%E.width,X=Math.floor(Ot/E.width),Ut=Ct,Tt=1;o.pixelStorei(o.UNPACK_SKIP_PIXELS,oe),o.pixelStorei(o.UNPACK_SKIP_ROWS,X),i.texSubImage2D(o.TEXTURE_2D,0,oe,X,Ut,Tt,W,dt,E.data)}w.clearUpdateRanges(),o.pixelStorei(o.UNPACK_ROW_LENGTH,Rt),o.pixelStorei(o.UNPACK_SKIP_PIXELS,Xt),o.pixelStorei(o.UNPACK_SKIP_ROWS,te)}}function tt(w,E,W){let dt=o.TEXTURE_2D;(E.isDataArrayTexture||E.isCompressedArrayTexture)&&(dt=o.TEXTURE_2D_ARRAY),E.isData3DTexture&&(dt=o.TEXTURE_3D);const vt=gt(w,E),lt=E.source;i.bindTexture(dt,w.__webglTexture,o.TEXTURE0+W);const Zt=r.get(lt);if(lt.version!==Zt.__version||vt===!0){i.activeTexture(o.TEXTURE0+W);const Rt=ye.getPrimaries(ye.workingColorSpace),Xt=E.colorSpace===ja?null:ye.getPrimaries(E.colorSpace),te=E.colorSpace===ja||Rt===Xt?o.NONE:o.BROWSER_DEFAULT_WEBGL;o.pixelStorei(o.UNPACK_FLIP_Y_WEBGL,E.flipY),o.pixelStorei(o.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),o.pixelStorei(o.UNPACK_ALIGNMENT,E.unpackAlignment),o.pixelStorei(o.UNPACK_COLORSPACE_CONVERSION_WEBGL,te);let yt=C(E.image,!1,l.maxTextureSize);yt=Le(E,yt);const Et=c.convert(E.format,E.colorSpace),Ft=c.convert(E.type);let Ot=N(E.internalFormat,Et,Ft,E.colorSpace,E.isVideoTexture);et(dt,E);let Ct;const oe=E.mipmaps,X=E.isVideoTexture!==!0,Ut=Zt.__version===void 0||vt===!0,Tt=lt.dataReady,Pt=B(E,yt);if(E.isDepthTexture)Ot=L(E.format===Ar,E.type),Ut&&(X?i.texStorage2D(o.TEXTURE_2D,1,Ot,yt.width,yt.height):i.texImage2D(o.TEXTURE_2D,0,Ot,yt.width,yt.height,0,Et,Ft,null));else if(E.isDataTexture)if(oe.length>0){X&&Ut&&i.texStorage2D(o.TEXTURE_2D,Pt,Ot,oe[0].width,oe[0].height);for(let St=0,_t=oe.length;St<_t;St++)Ct=oe[St],X?Tt&&i.texSubImage2D(o.TEXTURE_2D,St,0,0,Ct.width,Ct.height,Et,Ft,Ct.data):i.texImage2D(o.TEXTURE_2D,St,Ot,Ct.width,Ct.height,0,Et,Ft,Ct.data);E.generateMipmaps=!1}else X?(Ut&&i.texStorage2D(o.TEXTURE_2D,Pt,Ot,yt.width,yt.height),Tt&&Bt(E,yt,Et,Ft)):i.texImage2D(o.TEXTURE_2D,0,Ot,yt.width,yt.height,0,Et,Ft,yt.data);else if(E.isCompressedTexture)if(E.isCompressedArrayTexture){X&&Ut&&i.texStorage3D(o.TEXTURE_2D_ARRAY,Pt,Ot,oe[0].width,oe[0].height,yt.depth);for(let St=0,_t=oe.length;St<_t;St++)if(Ct=oe[St],E.format!==Ti)if(Et!==null)if(X){if(Tt)if(E.layerUpdates.size>0){const At=n_(Ct.width,Ct.height,E.format,E.type);for(const ee of E.layerUpdates){const Oe=Ct.data.subarray(ee*At/Ct.data.BYTES_PER_ELEMENT,(ee+1)*At/Ct.data.BYTES_PER_ELEMENT);i.compressedTexSubImage3D(o.TEXTURE_2D_ARRAY,St,0,0,ee,Ct.width,Ct.height,1,Et,Oe)}E.clearLayerUpdates()}else i.compressedTexSubImage3D(o.TEXTURE_2D_ARRAY,St,0,0,0,Ct.width,Ct.height,yt.depth,Et,Ct.data)}else i.compressedTexImage3D(o.TEXTURE_2D_ARRAY,St,Ot,Ct.width,Ct.height,yt.depth,0,Ct.data,0,0);else ae("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else X?Tt&&i.texSubImage3D(o.TEXTURE_2D_ARRAY,St,0,0,0,Ct.width,Ct.height,yt.depth,Et,Ft,Ct.data):i.texImage3D(o.TEXTURE_2D_ARRAY,St,Ot,Ct.width,Ct.height,yt.depth,0,Et,Ft,Ct.data)}else{X&&Ut&&i.texStorage2D(o.TEXTURE_2D,Pt,Ot,oe[0].width,oe[0].height);for(let St=0,_t=oe.length;St<_t;St++)Ct=oe[St],E.format!==Ti?Et!==null?X?Tt&&i.compressedTexSubImage2D(o.TEXTURE_2D,St,0,0,Ct.width,Ct.height,Et,Ct.data):i.compressedTexImage2D(o.TEXTURE_2D,St,Ot,Ct.width,Ct.height,0,Ct.data):ae("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):X?Tt&&i.texSubImage2D(o.TEXTURE_2D,St,0,0,Ct.width,Ct.height,Et,Ft,Ct.data):i.texImage2D(o.TEXTURE_2D,St,Ot,Ct.width,Ct.height,0,Et,Ft,Ct.data)}else if(E.isDataArrayTexture)if(X){if(Ut&&i.texStorage3D(o.TEXTURE_2D_ARRAY,Pt,Ot,yt.width,yt.height,yt.depth),Tt)if(E.layerUpdates.size>0){const St=n_(yt.width,yt.height,E.format,E.type);for(const _t of E.layerUpdates){const At=yt.data.subarray(_t*St/yt.data.BYTES_PER_ELEMENT,(_t+1)*St/yt.data.BYTES_PER_ELEMENT);i.texSubImage3D(o.TEXTURE_2D_ARRAY,0,0,0,_t,yt.width,yt.height,1,Et,Ft,At)}E.clearLayerUpdates()}else i.texSubImage3D(o.TEXTURE_2D_ARRAY,0,0,0,0,yt.width,yt.height,yt.depth,Et,Ft,yt.data)}else i.texImage3D(o.TEXTURE_2D_ARRAY,0,Ot,yt.width,yt.height,yt.depth,0,Et,Ft,yt.data);else if(E.isData3DTexture)X?(Ut&&i.texStorage3D(o.TEXTURE_3D,Pt,Ot,yt.width,yt.height,yt.depth),Tt&&i.texSubImage3D(o.TEXTURE_3D,0,0,0,0,yt.width,yt.height,yt.depth,Et,Ft,yt.data)):i.texImage3D(o.TEXTURE_3D,0,Ot,yt.width,yt.height,yt.depth,0,Et,Ft,yt.data);else if(E.isFramebufferTexture){if(Ut)if(X)i.texStorage2D(o.TEXTURE_2D,Pt,Ot,yt.width,yt.height);else{let St=yt.width,_t=yt.height;for(let At=0;At<Pt;At++)i.texImage2D(o.TEXTURE_2D,At,Ot,St,_t,0,Et,Ft,null),St>>=1,_t>>=1}}else if(oe.length>0){if(X&&Ut){const St=qt(oe[0]);i.texStorage2D(o.TEXTURE_2D,Pt,Ot,St.width,St.height)}for(let St=0,_t=oe.length;St<_t;St++)Ct=oe[St],X?Tt&&i.texSubImage2D(o.TEXTURE_2D,St,0,0,Et,Ft,Ct):i.texImage2D(o.TEXTURE_2D,St,Ot,Et,Ft,Ct);E.generateMipmaps=!1}else if(X){if(Ut){const St=qt(yt);i.texStorage2D(o.TEXTURE_2D,Pt,Ot,St.width,St.height)}Tt&&i.texSubImage2D(o.TEXTURE_2D,0,0,0,Et,Ft,yt)}else i.texImage2D(o.TEXTURE_2D,0,Ot,Et,Ft,yt);y(E)&&x(dt),Zt.__version=lt.version,E.onUpdate&&E.onUpdate(E)}w.__version=E.version}function ct(w,E,W){if(E.image.length!==6)return;const dt=gt(w,E),vt=E.source;i.bindTexture(o.TEXTURE_CUBE_MAP,w.__webglTexture,o.TEXTURE0+W);const lt=r.get(vt);if(vt.version!==lt.__version||dt===!0){i.activeTexture(o.TEXTURE0+W);const Zt=ye.getPrimaries(ye.workingColorSpace),Rt=E.colorSpace===ja?null:ye.getPrimaries(E.colorSpace),Xt=E.colorSpace===ja||Zt===Rt?o.NONE:o.BROWSER_DEFAULT_WEBGL;o.pixelStorei(o.UNPACK_FLIP_Y_WEBGL,E.flipY),o.pixelStorei(o.UNPACK_PREMULTIPLY_ALPHA_WEBGL,E.premultiplyAlpha),o.pixelStorei(o.UNPACK_ALIGNMENT,E.unpackAlignment),o.pixelStorei(o.UNPACK_COLORSPACE_CONVERSION_WEBGL,Xt);const te=E.isCompressedTexture||E.image[0].isCompressedTexture,yt=E.image[0]&&E.image[0].isDataTexture,Et=[];for(let _t=0;_t<6;_t++)!te&&!yt?Et[_t]=C(E.image[_t],!0,l.maxCubemapSize):Et[_t]=yt?E.image[_t].image:E.image[_t],Et[_t]=Le(E,Et[_t]);const Ft=Et[0],Ot=c.convert(E.format,E.colorSpace),Ct=c.convert(E.type),oe=N(E.internalFormat,Ot,Ct,E.colorSpace),X=E.isVideoTexture!==!0,Ut=lt.__version===void 0||dt===!0,Tt=vt.dataReady;let Pt=B(E,Ft);et(o.TEXTURE_CUBE_MAP,E);let St;if(te){X&&Ut&&i.texStorage2D(o.TEXTURE_CUBE_MAP,Pt,oe,Ft.width,Ft.height);for(let _t=0;_t<6;_t++){St=Et[_t].mipmaps;for(let At=0;At<St.length;At++){const ee=St[At];E.format!==Ti?Ot!==null?X?Tt&&i.compressedTexSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At,0,0,ee.width,ee.height,Ot,ee.data):i.compressedTexImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At,oe,ee.width,ee.height,0,ee.data):ae("WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):X?Tt&&i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At,0,0,ee.width,ee.height,Ot,Ct,ee.data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At,oe,ee.width,ee.height,0,Ot,Ct,ee.data)}}}else{if(St=E.mipmaps,X&&Ut){St.length>0&&Pt++;const _t=qt(Et[0]);i.texStorage2D(o.TEXTURE_CUBE_MAP,Pt,oe,_t.width,_t.height)}for(let _t=0;_t<6;_t++)if(yt){X?Tt&&i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,0,0,0,Et[_t].width,Et[_t].height,Ot,Ct,Et[_t].data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,0,oe,Et[_t].width,Et[_t].height,0,Ot,Ct,Et[_t].data);for(let At=0;At<St.length;At++){const Oe=St[At].image[_t].image;X?Tt&&i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At+1,0,0,Oe.width,Oe.height,Ot,Ct,Oe.data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At+1,oe,Oe.width,Oe.height,0,Ot,Ct,Oe.data)}}else{X?Tt&&i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,0,0,0,Ot,Ct,Et[_t]):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,0,oe,Ot,Ct,Et[_t]);for(let At=0;At<St.length;At++){const ee=St[At];X?Tt&&i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At+1,0,0,Ot,Ct,ee.image[_t]):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+_t,At+1,oe,Ot,Ct,ee.image[_t])}}}y(E)&&x(o.TEXTURE_CUBE_MAP),lt.__version=vt.version,E.onUpdate&&E.onUpdate(E)}w.__version=E.version}function Dt(w,E,W,dt,vt,lt){const Zt=c.convert(W.format,W.colorSpace),Rt=c.convert(W.type),Xt=N(W.internalFormat,Zt,Rt,W.colorSpace),te=r.get(E),yt=r.get(W);if(yt.__renderTarget=E,!te.__hasExternalTextures){const Et=Math.max(1,E.width>>lt),Ft=Math.max(1,E.height>>lt);vt===o.TEXTURE_3D||vt===o.TEXTURE_2D_ARRAY?i.texImage3D(vt,lt,Xt,Et,Ft,E.depth,0,Zt,Rt,null):i.texImage2D(vt,lt,Xt,Et,Ft,0,Zt,Rt,null)}i.bindFramebuffer(o.FRAMEBUFFER,w),qe(E)?d.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,dt,vt,yt.__webglTexture,0,H(E)):(vt===o.TEXTURE_2D||vt>=o.TEXTURE_CUBE_MAP_POSITIVE_X&&vt<=o.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&o.framebufferTexture2D(o.FRAMEBUFFER,dt,vt,yt.__webglTexture,lt),i.bindFramebuffer(o.FRAMEBUFFER,null)}function Vt(w,E,W){if(o.bindRenderbuffer(o.RENDERBUFFER,w),E.depthBuffer){const dt=E.depthTexture,vt=dt&&dt.isDepthTexture?dt.type:null,lt=L(E.stencilBuffer,vt),Zt=E.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT;qe(E)?d.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,H(E),lt,E.width,E.height):W?o.renderbufferStorageMultisample(o.RENDERBUFFER,H(E),lt,E.width,E.height):o.renderbufferStorage(o.RENDERBUFFER,lt,E.width,E.height),o.framebufferRenderbuffer(o.FRAMEBUFFER,Zt,o.RENDERBUFFER,w)}else{const dt=E.textures;for(let vt=0;vt<dt.length;vt++){const lt=dt[vt],Zt=c.convert(lt.format,lt.colorSpace),Rt=c.convert(lt.type),Xt=N(lt.internalFormat,Zt,Rt,lt.colorSpace);qe(E)?d.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,H(E),Xt,E.width,E.height):W?o.renderbufferStorageMultisample(o.RENDERBUFFER,H(E),Xt,E.width,E.height):o.renderbufferStorage(o.RENDERBUFFER,Xt,E.width,E.height)}}o.bindRenderbuffer(o.RENDERBUFFER,null)}function It(w,E,W){const dt=E.isWebGLCubeRenderTarget===!0;if(i.bindFramebuffer(o.FRAMEBUFFER,w),!(E.depthTexture&&E.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");const vt=r.get(E.depthTexture);if(vt.__renderTarget=E,(!vt.__webglTexture||E.depthTexture.image.width!==E.width||E.depthTexture.image.height!==E.height)&&(E.depthTexture.image.width=E.width,E.depthTexture.image.height=E.height,E.depthTexture.needsUpdate=!0),dt){if(vt.__webglInit===void 0&&(vt.__webglInit=!0,E.depthTexture.addEventListener("dispose",F)),vt.__webglTexture===void 0){vt.__webglTexture=o.createTexture(),i.bindTexture(o.TEXTURE_CUBE_MAP,vt.__webglTexture),et(o.TEXTURE_CUBE_MAP,E.depthTexture);const te=c.convert(E.depthTexture.format),yt=c.convert(E.depthTexture.type);let Et;E.depthTexture.format===ma?Et=o.DEPTH_COMPONENT24:E.depthTexture.format===Ar&&(Et=o.DEPTH24_STENCIL8);for(let Ft=0;Ft<6;Ft++)o.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+Ft,0,Et,E.width,E.height,0,te,yt,null)}}else ht(E.depthTexture,0);const lt=vt.__webglTexture,Zt=H(E),Rt=dt?o.TEXTURE_CUBE_MAP_POSITIVE_X+W:o.TEXTURE_2D,Xt=E.depthTexture.format===Ar?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT;if(E.depthTexture.format===ma)qe(E)?d.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,Xt,Rt,lt,0,Zt):o.framebufferTexture2D(o.FRAMEBUFFER,Xt,Rt,lt,0);else if(E.depthTexture.format===Ar)qe(E)?d.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,Xt,Rt,lt,0,Zt):o.framebufferTexture2D(o.FRAMEBUFFER,Xt,Rt,lt,0);else throw new Error("Unknown depthTexture format")}function fe(w){const E=r.get(w),W=w.isWebGLCubeRenderTarget===!0;if(E.__boundDepthTexture!==w.depthTexture){const dt=w.depthTexture;if(E.__depthDisposeCallback&&E.__depthDisposeCallback(),dt){const vt=()=>{delete E.__boundDepthTexture,delete E.__depthDisposeCallback,dt.removeEventListener("dispose",vt)};dt.addEventListener("dispose",vt),E.__depthDisposeCallback=vt}E.__boundDepthTexture=dt}if(w.depthTexture&&!E.__autoAllocateDepthBuffer)if(W)for(let dt=0;dt<6;dt++)It(E.__webglFramebuffer[dt],w,dt);else{const dt=w.texture.mipmaps;dt&&dt.length>0?It(E.__webglFramebuffer[0],w,0):It(E.__webglFramebuffer,w,0)}else if(W){E.__webglDepthbuffer=[];for(let dt=0;dt<6;dt++)if(i.bindFramebuffer(o.FRAMEBUFFER,E.__webglFramebuffer[dt]),E.__webglDepthbuffer[dt]===void 0)E.__webglDepthbuffer[dt]=o.createRenderbuffer(),Vt(E.__webglDepthbuffer[dt],w,!1);else{const vt=w.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT,lt=E.__webglDepthbuffer[dt];o.bindRenderbuffer(o.RENDERBUFFER,lt),o.framebufferRenderbuffer(o.FRAMEBUFFER,vt,o.RENDERBUFFER,lt)}}else{const dt=w.texture.mipmaps;if(dt&&dt.length>0?i.bindFramebuffer(o.FRAMEBUFFER,E.__webglFramebuffer[0]):i.bindFramebuffer(o.FRAMEBUFFER,E.__webglFramebuffer),E.__webglDepthbuffer===void 0)E.__webglDepthbuffer=o.createRenderbuffer(),Vt(E.__webglDepthbuffer,w,!1);else{const vt=w.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT,lt=E.__webglDepthbuffer;o.bindRenderbuffer(o.RENDERBUFFER,lt),o.framebufferRenderbuffer(o.FRAMEBUFFER,vt,o.RENDERBUFFER,lt)}}i.bindFramebuffer(o.FRAMEBUFFER,null)}function je(w,E,W){const dt=r.get(w);E!==void 0&&Dt(dt.__webglFramebuffer,w,w.texture,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,0),W!==void 0&&fe(w)}function me(w){const E=w.texture,W=r.get(w),dt=r.get(E);w.addEventListener("dispose",z);const vt=w.textures,lt=w.isWebGLCubeRenderTarget===!0,Zt=vt.length>1;if(Zt||(dt.__webglTexture===void 0&&(dt.__webglTexture=o.createTexture()),dt.__version=E.version,h.memory.textures++),lt){W.__webglFramebuffer=[];for(let Rt=0;Rt<6;Rt++)if(E.mipmaps&&E.mipmaps.length>0){W.__webglFramebuffer[Rt]=[];for(let Xt=0;Xt<E.mipmaps.length;Xt++)W.__webglFramebuffer[Rt][Xt]=o.createFramebuffer()}else W.__webglFramebuffer[Rt]=o.createFramebuffer()}else{if(E.mipmaps&&E.mipmaps.length>0){W.__webglFramebuffer=[];for(let Rt=0;Rt<E.mipmaps.length;Rt++)W.__webglFramebuffer[Rt]=o.createFramebuffer()}else W.__webglFramebuffer=o.createFramebuffer();if(Zt)for(let Rt=0,Xt=vt.length;Rt<Xt;Rt++){const te=r.get(vt[Rt]);te.__webglTexture===void 0&&(te.__webglTexture=o.createTexture(),h.memory.textures++)}if(w.samples>0&&qe(w)===!1){W.__webglMultisampledFramebuffer=o.createFramebuffer(),W.__webglColorRenderbuffer=[],i.bindFramebuffer(o.FRAMEBUFFER,W.__webglMultisampledFramebuffer);for(let Rt=0;Rt<vt.length;Rt++){const Xt=vt[Rt];W.__webglColorRenderbuffer[Rt]=o.createRenderbuffer(),o.bindRenderbuffer(o.RENDERBUFFER,W.__webglColorRenderbuffer[Rt]);const te=c.convert(Xt.format,Xt.colorSpace),yt=c.convert(Xt.type),Et=N(Xt.internalFormat,te,yt,Xt.colorSpace,w.isXRRenderTarget===!0),Ft=H(w);o.renderbufferStorageMultisample(o.RENDERBUFFER,Ft,Et,w.width,w.height),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+Rt,o.RENDERBUFFER,W.__webglColorRenderbuffer[Rt])}o.bindRenderbuffer(o.RENDERBUFFER,null),w.depthBuffer&&(W.__webglDepthRenderbuffer=o.createRenderbuffer(),Vt(W.__webglDepthRenderbuffer,w,!0)),i.bindFramebuffer(o.FRAMEBUFFER,null)}}if(lt){i.bindTexture(o.TEXTURE_CUBE_MAP,dt.__webglTexture),et(o.TEXTURE_CUBE_MAP,E);for(let Rt=0;Rt<6;Rt++)if(E.mipmaps&&E.mipmaps.length>0)for(let Xt=0;Xt<E.mipmaps.length;Xt++)Dt(W.__webglFramebuffer[Rt][Xt],w,E,o.COLOR_ATTACHMENT0,o.TEXTURE_CUBE_MAP_POSITIVE_X+Rt,Xt);else Dt(W.__webglFramebuffer[Rt],w,E,o.COLOR_ATTACHMENT0,o.TEXTURE_CUBE_MAP_POSITIVE_X+Rt,0);y(E)&&x(o.TEXTURE_CUBE_MAP),i.unbindTexture()}else if(Zt){for(let Rt=0,Xt=vt.length;Rt<Xt;Rt++){const te=vt[Rt],yt=r.get(te);let Et=o.TEXTURE_2D;(w.isWebGL3DRenderTarget||w.isWebGLArrayRenderTarget)&&(Et=w.isWebGL3DRenderTarget?o.TEXTURE_3D:o.TEXTURE_2D_ARRAY),i.bindTexture(Et,yt.__webglTexture),et(Et,te),Dt(W.__webglFramebuffer,w,te,o.COLOR_ATTACHMENT0+Rt,Et,0),y(te)&&x(Et)}i.unbindTexture()}else{let Rt=o.TEXTURE_2D;if((w.isWebGL3DRenderTarget||w.isWebGLArrayRenderTarget)&&(Rt=w.isWebGL3DRenderTarget?o.TEXTURE_3D:o.TEXTURE_2D_ARRAY),i.bindTexture(Rt,dt.__webglTexture),et(Rt,E),E.mipmaps&&E.mipmaps.length>0)for(let Xt=0;Xt<E.mipmaps.length;Xt++)Dt(W.__webglFramebuffer[Xt],w,E,o.COLOR_ATTACHMENT0,Rt,Xt);else Dt(W.__webglFramebuffer,w,E,o.COLOR_ATTACHMENT0,Rt,0);y(E)&&x(Rt),i.unbindTexture()}w.depthBuffer&&fe(w)}function he(w){const E=w.textures;for(let W=0,dt=E.length;W<dt;W++){const vt=E[W];if(y(vt)){const lt=P(w),Zt=r.get(vt).__webglTexture;i.bindTexture(lt,Zt),x(lt),i.unbindTexture()}}}const Ae=[],re=[];function Ke(w){if(w.samples>0){if(qe(w)===!1){const E=w.textures,W=w.width,dt=w.height;let vt=o.COLOR_BUFFER_BIT;const lt=w.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT,Zt=r.get(w),Rt=E.length>1;if(Rt)for(let te=0;te<E.length;te++)i.bindFramebuffer(o.FRAMEBUFFER,Zt.__webglMultisampledFramebuffer),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+te,o.RENDERBUFFER,null),i.bindFramebuffer(o.FRAMEBUFFER,Zt.__webglFramebuffer),o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0+te,o.TEXTURE_2D,null,0);i.bindFramebuffer(o.READ_FRAMEBUFFER,Zt.__webglMultisampledFramebuffer);const Xt=w.texture.mipmaps;Xt&&Xt.length>0?i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Zt.__webglFramebuffer[0]):i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Zt.__webglFramebuffer);for(let te=0;te<E.length;te++){if(w.resolveDepthBuffer&&(w.depthBuffer&&(vt|=o.DEPTH_BUFFER_BIT),w.stencilBuffer&&w.resolveStencilBuffer&&(vt|=o.STENCIL_BUFFER_BIT)),Rt){o.framebufferRenderbuffer(o.READ_FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.RENDERBUFFER,Zt.__webglColorRenderbuffer[te]);const yt=r.get(E[te]).__webglTexture;o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,yt,0)}o.blitFramebuffer(0,0,W,dt,0,0,W,dt,vt,o.NEAREST),m===!0&&(Ae.length=0,re.length=0,Ae.push(o.COLOR_ATTACHMENT0+te),w.depthBuffer&&w.resolveDepthBuffer===!1&&(Ae.push(lt),re.push(lt),o.invalidateFramebuffer(o.DRAW_FRAMEBUFFER,re)),o.invalidateFramebuffer(o.READ_FRAMEBUFFER,Ae))}if(i.bindFramebuffer(o.READ_FRAMEBUFFER,null),i.bindFramebuffer(o.DRAW_FRAMEBUFFER,null),Rt)for(let te=0;te<E.length;te++){i.bindFramebuffer(o.FRAMEBUFFER,Zt.__webglMultisampledFramebuffer),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+te,o.RENDERBUFFER,Zt.__webglColorRenderbuffer[te]);const yt=r.get(E[te]).__webglTexture;i.bindFramebuffer(o.FRAMEBUFFER,Zt.__webglFramebuffer),o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0+te,o.TEXTURE_2D,yt,0)}i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Zt.__webglMultisampledFramebuffer)}else if(w.depthBuffer&&w.resolveDepthBuffer===!1&&m){const E=w.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT;o.invalidateFramebuffer(o.DRAW_FRAMEBUFFER,[E])}}}function H(w){return Math.min(l.maxSamples,w.samples)}function qe(w){const E=r.get(w);return w.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&E.__useRenderToTexture!==!1}function Se(w){const E=h.render.frame;v.get(w)!==E&&(v.set(w,E),w.update())}function Le(w,E){const W=w.colorSpace,dt=w.format,vt=w.type;return w.isCompressedTexture===!0||w.isVideoTexture===!0||W!==Ds&&W!==ja&&(ye.getTransfer(W)===Be?(dt!==Ti||vt!==$n)&&ae("WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):be("WebGLTextures: Unsupported texture color space:",W)),E}function qt(w){return typeof HTMLImageElement<"u"&&w instanceof HTMLImageElement?(p.width=w.naturalWidth||w.width,p.height=w.naturalHeight||w.height):typeof VideoFrame<"u"&&w instanceof VideoFrame?(p.width=w.displayWidth,p.height=w.displayHeight):(p.width=w.width,p.height=w.height),p}this.allocateTextureUnit=at,this.resetTextureUnits=rt,this.setTexture2D=ht,this.setTexture2DArray=O,this.setTexture3D=V,this.setTextureCube=nt,this.rebindTextures=je,this.setupRenderTarget=me,this.updateRenderTargetMipmap=he,this.updateMultisampleRenderTarget=Ke,this.setupDepthRenderbuffer=fe,this.setupFrameBufferTexture=Dt,this.useMultisampledRTT=qe,this.isReversedDepthBuffer=function(){return i.buffers.depth.getReversed()}}function OA(o,e){function i(r,l=ja){let c;const h=ye.getTransfer(l);if(r===$n)return o.UNSIGNED_BYTE;if(r===Rd)return o.UNSIGNED_SHORT_4_4_4_4;if(r===Cd)return o.UNSIGNED_SHORT_5_5_5_1;if(r===V_)return o.UNSIGNED_INT_5_9_9_9_REV;if(r===X_)return o.UNSIGNED_INT_10F_11F_11F_REV;if(r===H_)return o.BYTE;if(r===G_)return o.SHORT;if(r===Bo)return o.UNSIGNED_SHORT;if(r===Ad)return o.INT;if(r===zi)return o.UNSIGNED_INT;if(r===Li)return o.FLOAT;if(r===pa)return o.HALF_FLOAT;if(r===k_)return o.ALPHA;if(r===W_)return o.RGB;if(r===Ti)return o.RGBA;if(r===ma)return o.DEPTH_COMPONENT;if(r===Ar)return o.DEPTH_STENCIL;if(r===q_)return o.RED;if(r===Dd)return o.RED_INTEGER;if(r===Cs)return o.RG;if(r===wd)return o.RG_INTEGER;if(r===Ud)return o.RGBA_INTEGER;if(r===Ru||r===Cu||r===Du||r===wu)if(h===Be)if(c=e.get("WEBGL_compressed_texture_s3tc_srgb"),c!==null){if(r===Ru)return c.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(r===Cu)return c.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(r===Du)return c.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(r===wu)return c.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(c=e.get("WEBGL_compressed_texture_s3tc"),c!==null){if(r===Ru)return c.COMPRESSED_RGB_S3TC_DXT1_EXT;if(r===Cu)return c.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(r===Du)return c.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(r===wu)return c.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(r===kh||r===Wh||r===qh||r===Yh)if(c=e.get("WEBGL_compressed_texture_pvrtc"),c!==null){if(r===kh)return c.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(r===Wh)return c.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(r===qh)return c.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(r===Yh)return c.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(r===Zh||r===jh||r===Kh||r===Qh||r===Jh||r===$h||r===td)if(c=e.get("WEBGL_compressed_texture_etc"),c!==null){if(r===Zh||r===jh)return h===Be?c.COMPRESSED_SRGB8_ETC2:c.COMPRESSED_RGB8_ETC2;if(r===Kh)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:c.COMPRESSED_RGBA8_ETC2_EAC;if(r===Qh)return c.COMPRESSED_R11_EAC;if(r===Jh)return c.COMPRESSED_SIGNED_R11_EAC;if(r===$h)return c.COMPRESSED_RG11_EAC;if(r===td)return c.COMPRESSED_SIGNED_RG11_EAC}else return null;if(r===ed||r===nd||r===id||r===ad||r===rd||r===sd||r===od||r===ld||r===ud||r===cd||r===fd||r===hd||r===dd||r===pd)if(c=e.get("WEBGL_compressed_texture_astc"),c!==null){if(r===ed)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:c.COMPRESSED_RGBA_ASTC_4x4_KHR;if(r===nd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:c.COMPRESSED_RGBA_ASTC_5x4_KHR;if(r===id)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:c.COMPRESSED_RGBA_ASTC_5x5_KHR;if(r===ad)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:c.COMPRESSED_RGBA_ASTC_6x5_KHR;if(r===rd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:c.COMPRESSED_RGBA_ASTC_6x6_KHR;if(r===sd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:c.COMPRESSED_RGBA_ASTC_8x5_KHR;if(r===od)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:c.COMPRESSED_RGBA_ASTC_8x6_KHR;if(r===ld)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:c.COMPRESSED_RGBA_ASTC_8x8_KHR;if(r===ud)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:c.COMPRESSED_RGBA_ASTC_10x5_KHR;if(r===cd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:c.COMPRESSED_RGBA_ASTC_10x6_KHR;if(r===fd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:c.COMPRESSED_RGBA_ASTC_10x8_KHR;if(r===hd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:c.COMPRESSED_RGBA_ASTC_10x10_KHR;if(r===dd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:c.COMPRESSED_RGBA_ASTC_12x10_KHR;if(r===pd)return h===Be?c.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:c.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(r===md||r===gd||r===_d)if(c=e.get("EXT_texture_compression_bptc"),c!==null){if(r===md)return h===Be?c.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:c.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(r===gd)return c.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(r===_d)return c.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(r===vd||r===xd||r===Sd||r===Md)if(c=e.get("EXT_texture_compression_rgtc"),c!==null){if(r===vd)return c.COMPRESSED_RED_RGTC1_EXT;if(r===xd)return c.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(r===Sd)return c.COMPRESSED_RED_GREEN_RGTC2_EXT;if(r===Md)return c.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return r===Io?o.UNSIGNED_INT_24_8:o[r]!==void 0?o[r]:null}return{convert:i}}const PA=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,FA=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`;class zA{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,i){if(this.texture===null){const r=new rv(e.texture);(e.depthNear!==i.depthNear||e.depthFar!==i.depthFar)&&(this.depthNear=e.depthNear,this.depthFar=e.depthFar),this.texture=r}}getMesh(e){if(this.texture!==null&&this.mesh===null){const i=e.cameras[0].viewport,r=new Ii({vertexShader:PA,fragmentShader:FA,uniforms:{depthColor:{value:this.texture},depthWidth:{value:i.z},depthHeight:{value:i.w}}});this.mesh=new ga(new Fu(20,20),r)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}}class BA extends Us{constructor(e,i){super();const r=this;let l=null,c=1,h=null,d="local-floor",m=1,p=null,v=null,g=null,S=null,M=null,A=null;const C=typeof XRWebGLBinding<"u",y=new zA,x={},P=i.getContextAttributes();let N=null,L=null;const B=[],F=[],z=new Ue;let Q=null;const R=new yi;R.viewport=new $e;const D=new yi;D.viewport=new $e;const k=[R,D],rt=new ZM;let at=null,ut=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(tt){let ct=B[tt];return ct===void 0&&(ct=new vh,B[tt]=ct),ct.getTargetRaySpace()},this.getControllerGrip=function(tt){let ct=B[tt];return ct===void 0&&(ct=new vh,B[tt]=ct),ct.getGripSpace()},this.getHand=function(tt){let ct=B[tt];return ct===void 0&&(ct=new vh,B[tt]=ct),ct.getHandSpace()};function ht(tt){const ct=F.indexOf(tt.inputSource);if(ct===-1)return;const Dt=B[ct];Dt!==void 0&&(Dt.update(tt.inputSource,tt.frame,p||h),Dt.dispatchEvent({type:tt.type,data:tt.inputSource}))}function O(){l.removeEventListener("select",ht),l.removeEventListener("selectstart",ht),l.removeEventListener("selectend",ht),l.removeEventListener("squeeze",ht),l.removeEventListener("squeezestart",ht),l.removeEventListener("squeezeend",ht),l.removeEventListener("end",O),l.removeEventListener("inputsourceschange",V);for(let tt=0;tt<B.length;tt++){const ct=F[tt];ct!==null&&(F[tt]=null,B[tt].disconnect(ct))}at=null,ut=null,y.reset();for(const tt in x)delete x[tt];e.setRenderTarget(N),M=null,S=null,g=null,l=null,L=null,Bt.stop(),r.isPresenting=!1,e.setPixelRatio(Q),e.setSize(z.width,z.height,!1),r.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(tt){c=tt,r.isPresenting===!0&&ae("WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(tt){d=tt,r.isPresenting===!0&&ae("WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return p||h},this.setReferenceSpace=function(tt){p=tt},this.getBaseLayer=function(){return S!==null?S:M},this.getBinding=function(){return g===null&&C&&(g=new XRWebGLBinding(l,i)),g},this.getFrame=function(){return A},this.getSession=function(){return l},this.setSession=async function(tt){if(l=tt,l!==null){if(N=e.getRenderTarget(),l.addEventListener("select",ht),l.addEventListener("selectstart",ht),l.addEventListener("selectend",ht),l.addEventListener("squeeze",ht),l.addEventListener("squeezestart",ht),l.addEventListener("squeezeend",ht),l.addEventListener("end",O),l.addEventListener("inputsourceschange",V),P.xrCompatible!==!0&&await i.makeXRCompatible(),Q=e.getPixelRatio(),e.getSize(z),C&&"createProjectionLayer"in XRWebGLBinding.prototype){let Dt=null,Vt=null,It=null;P.depth&&(It=P.stencil?i.DEPTH24_STENCIL8:i.DEPTH_COMPONENT24,Dt=P.stencil?Ar:ma,Vt=P.stencil?Io:zi);const fe={colorFormat:i.RGBA8,depthFormat:It,scaleFactor:c};g=this.getBinding(),S=g.createProjectionLayer(fe),l.updateRenderState({layers:[S]}),e.setPixelRatio(1),e.setSize(S.textureWidth,S.textureHeight,!1),L=new Pi(S.textureWidth,S.textureHeight,{format:Ti,type:$n,depthTexture:new Go(S.textureWidth,S.textureHeight,Vt,void 0,void 0,void 0,void 0,void 0,void 0,Dt),stencilBuffer:P.stencil,colorSpace:e.outputColorSpace,samples:P.antialias?4:0,resolveDepthBuffer:S.ignoreDepthValues===!1,resolveStencilBuffer:S.ignoreDepthValues===!1})}else{const Dt={antialias:P.antialias,alpha:!0,depth:P.depth,stencil:P.stencil,framebufferScaleFactor:c};M=new XRWebGLLayer(l,i,Dt),l.updateRenderState({baseLayer:M}),e.setPixelRatio(1),e.setSize(M.framebufferWidth,M.framebufferHeight,!1),L=new Pi(M.framebufferWidth,M.framebufferHeight,{format:Ti,type:$n,colorSpace:e.outputColorSpace,stencilBuffer:P.stencil,resolveDepthBuffer:M.ignoreDepthValues===!1,resolveStencilBuffer:M.ignoreDepthValues===!1})}L.isXRRenderTarget=!0,this.setFoveation(m),p=null,h=await l.requestReferenceSpace(d),Bt.setContext(l),Bt.start(),r.isPresenting=!0,r.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(l!==null)return l.environmentBlendMode},this.getDepthTexture=function(){return y.getDepthTexture()};function V(tt){for(let ct=0;ct<tt.removed.length;ct++){const Dt=tt.removed[ct],Vt=F.indexOf(Dt);Vt>=0&&(F[Vt]=null,B[Vt].disconnect(Dt))}for(let ct=0;ct<tt.added.length;ct++){const Dt=tt.added[ct];let Vt=F.indexOf(Dt);if(Vt===-1){for(let fe=0;fe<B.length;fe++)if(fe>=F.length){F.push(Dt),Vt=fe;break}else if(F[fe]===null){F[fe]=Dt,Vt=fe;break}if(Vt===-1)break}const It=B[Vt];It&&It.connect(Dt)}}const nt=new it,Mt=new it;function xt(tt,ct,Dt){nt.setFromMatrixPosition(ct.matrixWorld),Mt.setFromMatrixPosition(Dt.matrixWorld);const Vt=nt.distanceTo(Mt),It=ct.projectionMatrix.elements,fe=Dt.projectionMatrix.elements,je=It[14]/(It[10]-1),me=It[14]/(It[10]+1),he=(It[9]+1)/It[5],Ae=(It[9]-1)/It[5],re=(It[8]-1)/It[0],Ke=(fe[8]+1)/fe[0],H=je*re,qe=je*Ke,Se=Vt/(-re+Ke),Le=Se*-re;if(ct.matrixWorld.decompose(tt.position,tt.quaternion,tt.scale),tt.translateX(Le),tt.translateZ(Se),tt.matrixWorld.compose(tt.position,tt.quaternion,tt.scale),tt.matrixWorldInverse.copy(tt.matrixWorld).invert(),It[10]===-1)tt.projectionMatrix.copy(ct.projectionMatrix),tt.projectionMatrixInverse.copy(ct.projectionMatrixInverse);else{const qt=je+Se,w=me+Se,E=H-Le,W=qe+(Vt-Le),dt=he*me/w*qt,vt=Ae*me/w*qt;tt.projectionMatrix.makePerspective(E,W,dt,vt,qt,w),tt.projectionMatrixInverse.copy(tt.projectionMatrix).invert()}}function U(tt,ct){ct===null?tt.matrixWorld.copy(tt.matrix):tt.matrixWorld.multiplyMatrices(ct.matrixWorld,tt.matrix),tt.matrixWorldInverse.copy(tt.matrixWorld).invert()}this.updateCamera=function(tt){if(l===null)return;let ct=tt.near,Dt=tt.far;y.texture!==null&&(y.depthNear>0&&(ct=y.depthNear),y.depthFar>0&&(Dt=y.depthFar)),rt.near=D.near=R.near=ct,rt.far=D.far=R.far=Dt,(at!==rt.near||ut!==rt.far)&&(l.updateRenderState({depthNear:rt.near,depthFar:rt.far}),at=rt.near,ut=rt.far),rt.layers.mask=tt.layers.mask|6,R.layers.mask=rt.layers.mask&3,D.layers.mask=rt.layers.mask&5;const Vt=tt.parent,It=rt.cameras;U(rt,Vt);for(let fe=0;fe<It.length;fe++)U(It[fe],Vt);It.length===2?xt(rt,R,D):rt.projectionMatrix.copy(R.projectionMatrix),et(tt,rt,Vt)};function et(tt,ct,Dt){Dt===null?tt.matrix.copy(ct.matrixWorld):(tt.matrix.copy(Dt.matrixWorld),tt.matrix.invert(),tt.matrix.multiply(ct.matrixWorld)),tt.matrix.decompose(tt.position,tt.quaternion,tt.scale),tt.updateMatrixWorld(!0),tt.projectionMatrix.copy(ct.projectionMatrix),tt.projectionMatrixInverse.copy(ct.projectionMatrixInverse),tt.isPerspectiveCamera&&(tt.fov=yd*2*Math.atan(1/tt.projectionMatrix.elements[5]),tt.zoom=1)}this.getCamera=function(){return rt},this.getFoveation=function(){if(!(S===null&&M===null))return m},this.setFoveation=function(tt){m=tt,S!==null&&(S.fixedFoveation=tt),M!==null&&M.fixedFoveation!==void 0&&(M.fixedFoveation=tt)},this.hasDepthSensing=function(){return y.texture!==null},this.getDepthSensingMesh=function(){return y.getMesh(rt)},this.getCameraTexture=function(tt){return x[tt]};let gt=null;function bt(tt,ct){if(v=ct.getViewerPose(p||h),A=ct,v!==null){const Dt=v.views;M!==null&&(e.setRenderTargetFramebuffer(L,M.framebuffer),e.setRenderTarget(L));let Vt=!1;Dt.length!==rt.cameras.length&&(rt.cameras.length=0,Vt=!0);for(let me=0;me<Dt.length;me++){const he=Dt[me];let Ae=null;if(M!==null)Ae=M.getViewport(he);else{const Ke=g.getViewSubImage(S,he);Ae=Ke.viewport,me===0&&(e.setRenderTargetTextures(L,Ke.colorTexture,Ke.depthStencilTexture),e.setRenderTarget(L))}let re=k[me];re===void 0&&(re=new yi,re.layers.enable(me),re.viewport=new $e,k[me]=re),re.matrix.fromArray(he.transform.matrix),re.matrix.decompose(re.position,re.quaternion,re.scale),re.projectionMatrix.fromArray(he.projectionMatrix),re.projectionMatrixInverse.copy(re.projectionMatrix).invert(),re.viewport.set(Ae.x,Ae.y,Ae.width,Ae.height),me===0&&(rt.matrix.copy(re.matrix),rt.matrix.decompose(rt.position,rt.quaternion,rt.scale)),Vt===!0&&rt.cameras.push(re)}const It=l.enabledFeatures;if(It&&It.includes("depth-sensing")&&l.depthUsage=="gpu-optimized"&&C){g=r.getBinding();const me=g.getDepthInformation(Dt[0]);me&&me.isValid&&me.texture&&y.init(me,l.renderState)}if(It&&It.includes("camera-access")&&C){e.state.unbindTexture(),g=r.getBinding();for(let me=0;me<Dt.length;me++){const he=Dt[me].camera;if(he){let Ae=x[he];Ae||(Ae=new rv,x[he]=Ae);const re=g.getCameraImage(he);Ae.sourceTexture=re}}}}for(let Dt=0;Dt<B.length;Dt++){const Vt=F[Dt],It=B[Dt];Vt!==null&&It!==void 0&&It.update(Vt,ct,p||h)}gt&&gt(tt,ct),ct.detectedPlanes&&r.dispatchEvent({type:"planesdetected",data:ct}),A=null}const Bt=new lv;Bt.setAnimationLoop(bt),this.setAnimationLoop=function(tt){gt=tt},this.dispose=function(){}}}const Mr=new Bi,IA=new tn;function HA(o,e){function i(y,x){y.matrixAutoUpdate===!0&&y.updateMatrix(),x.value.copy(y.matrix)}function r(y,x){x.color.getRGB(y.fogColor.value,ev(o)),x.isFog?(y.fogNear.value=x.near,y.fogFar.value=x.far):x.isFogExp2&&(y.fogDensity.value=x.density)}function l(y,x,P,N,L){x.isMeshBasicMaterial||x.isMeshLambertMaterial?c(y,x):x.isMeshToonMaterial?(c(y,x),g(y,x)):x.isMeshPhongMaterial?(c(y,x),v(y,x)):x.isMeshStandardMaterial?(c(y,x),S(y,x),x.isMeshPhysicalMaterial&&M(y,x,L)):x.isMeshMatcapMaterial?(c(y,x),A(y,x)):x.isMeshDepthMaterial?c(y,x):x.isMeshDistanceMaterial?(c(y,x),C(y,x)):x.isMeshNormalMaterial?c(y,x):x.isLineBasicMaterial?(h(y,x),x.isLineDashedMaterial&&d(y,x)):x.isPointsMaterial?m(y,x,P,N):x.isSpriteMaterial?p(y,x):x.isShadowMaterial?(y.color.value.copy(x.color),y.opacity.value=x.opacity):x.isShaderMaterial&&(x.uniformsNeedUpdate=!1)}function c(y,x){y.opacity.value=x.opacity,x.color&&y.diffuse.value.copy(x.color),x.emissive&&y.emissive.value.copy(x.emissive).multiplyScalar(x.emissiveIntensity),x.map&&(y.map.value=x.map,i(x.map,y.mapTransform)),x.alphaMap&&(y.alphaMap.value=x.alphaMap,i(x.alphaMap,y.alphaMapTransform)),x.bumpMap&&(y.bumpMap.value=x.bumpMap,i(x.bumpMap,y.bumpMapTransform),y.bumpScale.value=x.bumpScale,x.side===Xn&&(y.bumpScale.value*=-1)),x.normalMap&&(y.normalMap.value=x.normalMap,i(x.normalMap,y.normalMapTransform),y.normalScale.value.copy(x.normalScale),x.side===Xn&&y.normalScale.value.negate()),x.displacementMap&&(y.displacementMap.value=x.displacementMap,i(x.displacementMap,y.displacementMapTransform),y.displacementScale.value=x.displacementScale,y.displacementBias.value=x.displacementBias),x.emissiveMap&&(y.emissiveMap.value=x.emissiveMap,i(x.emissiveMap,y.emissiveMapTransform)),x.specularMap&&(y.specularMap.value=x.specularMap,i(x.specularMap,y.specularMapTransform)),x.alphaTest>0&&(y.alphaTest.value=x.alphaTest);const P=e.get(x),N=P.envMap,L=P.envMapRotation;N&&(y.envMap.value=N,Mr.copy(L),Mr.x*=-1,Mr.y*=-1,Mr.z*=-1,N.isCubeTexture&&N.isRenderTargetTexture===!1&&(Mr.y*=-1,Mr.z*=-1),y.envMapRotation.value.setFromMatrix4(IA.makeRotationFromEuler(Mr)),y.flipEnvMap.value=N.isCubeTexture&&N.isRenderTargetTexture===!1?-1:1,y.reflectivity.value=x.reflectivity,y.ior.value=x.ior,y.refractionRatio.value=x.refractionRatio),x.lightMap&&(y.lightMap.value=x.lightMap,y.lightMapIntensity.value=x.lightMapIntensity,i(x.lightMap,y.lightMapTransform)),x.aoMap&&(y.aoMap.value=x.aoMap,y.aoMapIntensity.value=x.aoMapIntensity,i(x.aoMap,y.aoMapTransform))}function h(y,x){y.diffuse.value.copy(x.color),y.opacity.value=x.opacity,x.map&&(y.map.value=x.map,i(x.map,y.mapTransform))}function d(y,x){y.dashSize.value=x.dashSize,y.totalSize.value=x.dashSize+x.gapSize,y.scale.value=x.scale}function m(y,x,P,N){y.diffuse.value.copy(x.color),y.opacity.value=x.opacity,y.size.value=x.size*P,y.scale.value=N*.5,x.map&&(y.map.value=x.map,i(x.map,y.uvTransform)),x.alphaMap&&(y.alphaMap.value=x.alphaMap,i(x.alphaMap,y.alphaMapTransform)),x.alphaTest>0&&(y.alphaTest.value=x.alphaTest)}function p(y,x){y.diffuse.value.copy(x.color),y.opacity.value=x.opacity,y.rotation.value=x.rotation,x.map&&(y.map.value=x.map,i(x.map,y.mapTransform)),x.alphaMap&&(y.alphaMap.value=x.alphaMap,i(x.alphaMap,y.alphaMapTransform)),x.alphaTest>0&&(y.alphaTest.value=x.alphaTest)}function v(y,x){y.specular.value.copy(x.specular),y.shininess.value=Math.max(x.shininess,1e-4)}function g(y,x){x.gradientMap&&(y.gradientMap.value=x.gradientMap)}function S(y,x){y.metalness.value=x.metalness,x.metalnessMap&&(y.metalnessMap.value=x.metalnessMap,i(x.metalnessMap,y.metalnessMapTransform)),y.roughness.value=x.roughness,x.roughnessMap&&(y.roughnessMap.value=x.roughnessMap,i(x.roughnessMap,y.roughnessMapTransform)),x.envMap&&(y.envMapIntensity.value=x.envMapIntensity)}function M(y,x,P){y.ior.value=x.ior,x.sheen>0&&(y.sheenColor.value.copy(x.sheenColor).multiplyScalar(x.sheen),y.sheenRoughness.value=x.sheenRoughness,x.sheenColorMap&&(y.sheenColorMap.value=x.sheenColorMap,i(x.sheenColorMap,y.sheenColorMapTransform)),x.sheenRoughnessMap&&(y.sheenRoughnessMap.value=x.sheenRoughnessMap,i(x.sheenRoughnessMap,y.sheenRoughnessMapTransform))),x.clearcoat>0&&(y.clearcoat.value=x.clearcoat,y.clearcoatRoughness.value=x.clearcoatRoughness,x.clearcoatMap&&(y.clearcoatMap.value=x.clearcoatMap,i(x.clearcoatMap,y.clearcoatMapTransform)),x.clearcoatRoughnessMap&&(y.clearcoatRoughnessMap.value=x.clearcoatRoughnessMap,i(x.clearcoatRoughnessMap,y.clearcoatRoughnessMapTransform)),x.clearcoatNormalMap&&(y.clearcoatNormalMap.value=x.clearcoatNormalMap,i(x.clearcoatNormalMap,y.clearcoatNormalMapTransform),y.clearcoatNormalScale.value.copy(x.clearcoatNormalScale),x.side===Xn&&y.clearcoatNormalScale.value.negate())),x.dispersion>0&&(y.dispersion.value=x.dispersion),x.iridescence>0&&(y.iridescence.value=x.iridescence,y.iridescenceIOR.value=x.iridescenceIOR,y.iridescenceThicknessMinimum.value=x.iridescenceThicknessRange[0],y.iridescenceThicknessMaximum.value=x.iridescenceThicknessRange[1],x.iridescenceMap&&(y.iridescenceMap.value=x.iridescenceMap,i(x.iridescenceMap,y.iridescenceMapTransform)),x.iridescenceThicknessMap&&(y.iridescenceThicknessMap.value=x.iridescenceThicknessMap,i(x.iridescenceThicknessMap,y.iridescenceThicknessMapTransform))),x.transmission>0&&(y.transmission.value=x.transmission,y.transmissionSamplerMap.value=P.texture,y.transmissionSamplerSize.value.set(P.width,P.height),x.transmissionMap&&(y.transmissionMap.value=x.transmissionMap,i(x.transmissionMap,y.transmissionMapTransform)),y.thickness.value=x.thickness,x.thicknessMap&&(y.thicknessMap.value=x.thicknessMap,i(x.thicknessMap,y.thicknessMapTransform)),y.attenuationDistance.value=x.attenuationDistance,y.attenuationColor.value.copy(x.attenuationColor)),x.anisotropy>0&&(y.anisotropyVector.value.set(x.anisotropy*Math.cos(x.anisotropyRotation),x.anisotropy*Math.sin(x.anisotropyRotation)),x.anisotropyMap&&(y.anisotropyMap.value=x.anisotropyMap,i(x.anisotropyMap,y.anisotropyMapTransform))),y.specularIntensity.value=x.specularIntensity,y.specularColor.value.copy(x.specularColor),x.specularColorMap&&(y.specularColorMap.value=x.specularColorMap,i(x.specularColorMap,y.specularColorMapTransform)),x.specularIntensityMap&&(y.specularIntensityMap.value=x.specularIntensityMap,i(x.specularIntensityMap,y.specularIntensityMapTransform))}function A(y,x){x.matcap&&(y.matcap.value=x.matcap)}function C(y,x){const P=e.get(x).light;y.referencePosition.value.setFromMatrixPosition(P.matrixWorld),y.nearDistance.value=P.shadow.camera.near,y.farDistance.value=P.shadow.camera.far}return{refreshFogUniforms:r,refreshMaterialUniforms:l}}function GA(o,e,i,r){let l={},c={},h=[];const d=o.getParameter(o.MAX_UNIFORM_BUFFER_BINDINGS);function m(P,N){const L=N.program;r.uniformBlockBinding(P,L)}function p(P,N){let L=l[P.id];L===void 0&&(A(P),L=v(P),l[P.id]=L,P.addEventListener("dispose",y));const B=N.program;r.updateUBOMapping(P,B);const F=e.render.frame;c[P.id]!==F&&(S(P),c[P.id]=F)}function v(P){const N=g();P.__bindingPointIndex=N;const L=o.createBuffer(),B=P.__size,F=P.usage;return o.bindBuffer(o.UNIFORM_BUFFER,L),o.bufferData(o.UNIFORM_BUFFER,B,F),o.bindBuffer(o.UNIFORM_BUFFER,null),o.bindBufferBase(o.UNIFORM_BUFFER,N,L),L}function g(){for(let P=0;P<d;P++)if(h.indexOf(P)===-1)return h.push(P),P;return be("WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function S(P){const N=l[P.id],L=P.uniforms,B=P.__cache;o.bindBuffer(o.UNIFORM_BUFFER,N);for(let F=0,z=L.length;F<z;F++){const Q=Array.isArray(L[F])?L[F]:[L[F]];for(let R=0,D=Q.length;R<D;R++){const k=Q[R];if(M(k,F,R,B)===!0){const rt=k.__offset,at=Array.isArray(k.value)?k.value:[k.value];let ut=0;for(let ht=0;ht<at.length;ht++){const O=at[ht],V=C(O);typeof O=="number"||typeof O=="boolean"?(k.__data[0]=O,o.bufferSubData(o.UNIFORM_BUFFER,rt+ut,k.__data)):O.isMatrix3?(k.__data[0]=O.elements[0],k.__data[1]=O.elements[1],k.__data[2]=O.elements[2],k.__data[3]=0,k.__data[4]=O.elements[3],k.__data[5]=O.elements[4],k.__data[6]=O.elements[5],k.__data[7]=0,k.__data[8]=O.elements[6],k.__data[9]=O.elements[7],k.__data[10]=O.elements[8],k.__data[11]=0):(O.toArray(k.__data,ut),ut+=V.storage/Float32Array.BYTES_PER_ELEMENT)}o.bufferSubData(o.UNIFORM_BUFFER,rt,k.__data)}}}o.bindBuffer(o.UNIFORM_BUFFER,null)}function M(P,N,L,B){const F=P.value,z=N+"_"+L;if(B[z]===void 0)return typeof F=="number"||typeof F=="boolean"?B[z]=F:B[z]=F.clone(),!0;{const Q=B[z];if(typeof F=="number"||typeof F=="boolean"){if(Q!==F)return B[z]=F,!0}else if(Q.equals(F)===!1)return Q.copy(F),!0}return!1}function A(P){const N=P.uniforms;let L=0;const B=16;for(let z=0,Q=N.length;z<Q;z++){const R=Array.isArray(N[z])?N[z]:[N[z]];for(let D=0,k=R.length;D<k;D++){const rt=R[D],at=Array.isArray(rt.value)?rt.value:[rt.value];for(let ut=0,ht=at.length;ut<ht;ut++){const O=at[ut],V=C(O),nt=L%B,Mt=nt%V.boundary,xt=nt+Mt;L+=Mt,xt!==0&&B-xt<V.storage&&(L+=B-xt),rt.__data=new Float32Array(V.storage/Float32Array.BYTES_PER_ELEMENT),rt.__offset=L,L+=V.storage}}}const F=L%B;return F>0&&(L+=B-F),P.__size=L,P.__cache={},this}function C(P){const N={boundary:0,storage:0};return typeof P=="number"||typeof P=="boolean"?(N.boundary=4,N.storage=4):P.isVector2?(N.boundary=8,N.storage=8):P.isVector3||P.isColor?(N.boundary=16,N.storage=12):P.isVector4?(N.boundary=16,N.storage=16):P.isMatrix3?(N.boundary=48,N.storage=48):P.isMatrix4?(N.boundary=64,N.storage=64):P.isTexture?ae("WebGLRenderer: Texture samplers can not be part of an uniforms group."):ae("WebGLRenderer: Unsupported uniform value type.",P),N}function y(P){const N=P.target;N.removeEventListener("dispose",y);const L=h.indexOf(N.__bindingPointIndex);h.splice(L,1),o.deleteBuffer(l[N.id]),delete l[N.id],delete c[N.id]}function x(){for(const P in l)o.deleteBuffer(l[P]);h=[],l={},c={}}return{bind:m,update:p,dispose:x}}const VA=new Uint16Array([12469,15057,12620,14925,13266,14620,13807,14376,14323,13990,14545,13625,14713,13328,14840,12882,14931,12528,14996,12233,15039,11829,15066,11525,15080,11295,15085,10976,15082,10705,15073,10495,13880,14564,13898,14542,13977,14430,14158,14124,14393,13732,14556,13410,14702,12996,14814,12596,14891,12291,14937,11834,14957,11489,14958,11194,14943,10803,14921,10506,14893,10278,14858,9960,14484,14039,14487,14025,14499,13941,14524,13740,14574,13468,14654,13106,14743,12678,14818,12344,14867,11893,14889,11509,14893,11180,14881,10751,14852,10428,14812,10128,14765,9754,14712,9466,14764,13480,14764,13475,14766,13440,14766,13347,14769,13070,14786,12713,14816,12387,14844,11957,14860,11549,14868,11215,14855,10751,14825,10403,14782,10044,14729,9651,14666,9352,14599,9029,14967,12835,14966,12831,14963,12804,14954,12723,14936,12564,14917,12347,14900,11958,14886,11569,14878,11247,14859,10765,14828,10401,14784,10011,14727,9600,14660,9289,14586,8893,14508,8533,15111,12234,15110,12234,15104,12216,15092,12156,15067,12010,15028,11776,14981,11500,14942,11205,14902,10752,14861,10393,14812,9991,14752,9570,14682,9252,14603,8808,14519,8445,14431,8145,15209,11449,15208,11451,15202,11451,15190,11438,15163,11384,15117,11274,15055,10979,14994,10648,14932,10343,14871,9936,14803,9532,14729,9218,14645,8742,14556,8381,14461,8020,14365,7603,15273,10603,15272,10607,15267,10619,15256,10631,15231,10614,15182,10535,15118,10389,15042,10167,14963,9787,14883,9447,14800,9115,14710,8665,14615,8318,14514,7911,14411,7507,14279,7198,15314,9675,15313,9683,15309,9712,15298,9759,15277,9797,15229,9773,15166,9668,15084,9487,14995,9274,14898,8910,14800,8539,14697,8234,14590,7790,14479,7409,14367,7067,14178,6621,15337,8619,15337,8631,15333,8677,15325,8769,15305,8871,15264,8940,15202,8909,15119,8775,15022,8565,14916,8328,14804,8009,14688,7614,14569,7287,14448,6888,14321,6483,14088,6171,15350,7402,15350,7419,15347,7480,15340,7613,15322,7804,15287,7973,15229,8057,15148,8012,15046,7846,14933,7611,14810,7357,14682,7069,14552,6656,14421,6316,14251,5948,14007,5528,15356,5942,15356,5977,15353,6119,15348,6294,15332,6551,15302,6824,15249,7044,15171,7122,15070,7050,14949,6861,14818,6611,14679,6349,14538,6067,14398,5651,14189,5311,13935,4958,15359,4123,15359,4153,15356,4296,15353,4646,15338,5160,15311,5508,15263,5829,15188,6042,15088,6094,14966,6001,14826,5796,14678,5543,14527,5287,14377,4985,14133,4586,13869,4257,15360,1563,15360,1642,15358,2076,15354,2636,15341,3350,15317,4019,15273,4429,15203,4732,15105,4911,14981,4932,14836,4818,14679,4621,14517,4386,14359,4156,14083,3795,13808,3437,15360,122,15360,137,15358,285,15355,636,15344,1274,15322,2177,15281,2765,15215,3223,15120,3451,14995,3569,14846,3567,14681,3466,14511,3305,14344,3121,14037,2800,13753,2467,15360,0,15360,1,15359,21,15355,89,15346,253,15325,479,15287,796,15225,1148,15133,1492,15008,1749,14856,1882,14685,1886,14506,1783,14324,1608,13996,1398,13702,1183]);let wi=null;function XA(){return wi===null&&(wi=new BM(VA,16,16,Cs,pa),wi.name="DFG_LUT",wi.minFilter=Un,wi.magFilter=Un,wi.wrapS=fa,wi.wrapT=fa,wi.generateMipmaps=!1,wi.needsUpdate=!0),wi}class i1{constructor(e={}){const{canvas:i=fM(),context:r=null,depth:l=!0,stencil:c=!1,alpha:h=!1,antialias:d=!1,premultipliedAlpha:m=!0,preserveDrawingBuffer:p=!1,powerPreference:v="default",failIfMajorPerformanceCaveat:g=!1,reversedDepthBuffer:S=!1,outputBufferType:M=$n}=e;this.isWebGLRenderer=!0;let A;if(r!==null){if(typeof WebGLRenderingContext<"u"&&r instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");A=r.getContextAttributes().alpha}else A=h;const C=M,y=new Set([Ud,wd,Dd]),x=new Set([$n,zi,Bo,Io,Rd,Cd]),P=new Uint32Array(4),N=new Int32Array(4);let L=null,B=null;const F=[],z=[];let Q=null;this.domElement=i,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this.toneMapping=Oi,this.toneMappingExposure=1,this.transmissionResolutionScale=1;const R=this;let D=!1;this._outputColorSpace=fi;let k=0,rt=0,at=null,ut=-1,ht=null;const O=new $e,V=new $e;let nt=null;const Mt=new we(0);let xt=0,U=i.width,et=i.height,gt=1,bt=null,Bt=null;const tt=new $e(0,0,U,et),ct=new $e(0,0,U,et);let Dt=!1;const Vt=new Fd;let It=!1,fe=!1;const je=new tn,me=new it,he=new $e,Ae={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};let re=!1;function Ke(){return at===null?gt:1}let H=r;function qe(b,q){return i.getContext(b,q)}try{const b={alpha:!0,depth:l,stencil:c,antialias:d,premultipliedAlpha:m,preserveDrawingBuffer:p,powerPreference:v,failIfMajorPerformanceCaveat:g};if("setAttribute"in i&&i.setAttribute("data-engine",`three.js r${bd}`),i.addEventListener("webglcontextlost",ee,!1),i.addEventListener("webglcontextrestored",Oe,!1),i.addEventListener("webglcontextcreationerror",Me,!1),H===null){const q="webgl2";if(H=qe(q,b),H===null)throw qe(q)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(b){throw be("WebGLRenderer: "+b.message),b}let Se,Le,qt,w,E,W,dt,vt,lt,Zt,Rt,Xt,te,yt,Et,Ft,Ot,Ct,oe,X,Ut,Tt,Pt,St;function _t(){Se=new XT(H),Se.init(),Tt=new OA(H,Se),Le=new OT(H,Se,e,Tt),qt=new LA(H,Se),Le.reversedDepthBuffer&&S&&qt.buffers.depth.setReversed(!0),w=new qT(H),E=new _A,W=new NA(H,Se,qt,E,Le,Tt,w),dt=new FT(R),vt=new VT(R),lt=new KM(H),Pt=new LT(H,lt),Zt=new kT(H,lt,w,Pt),Rt=new ZT(H,Zt,lt,w),oe=new YT(H,Le,W),Ft=new PT(E),Xt=new gA(R,dt,vt,Se,Le,Pt,Ft),te=new HA(R,E),yt=new xA,Et=new bA(Se),Ct=new UT(R,dt,vt,qt,Rt,A,m),Ot=new wA(R,Rt,Le),St=new GA(H,w,Le,qt),X=new NT(H,Se,w),Ut=new WT(H,Se,w),w.programs=Xt.programs,R.capabilities=Le,R.extensions=Se,R.properties=E,R.renderLists=yt,R.shadowMap=Ot,R.state=qt,R.info=w}_t(),C!==$n&&(Q=new KT(C,i.width,i.height,l,c));const At=new BA(R,H);this.xr=At,this.getContext=function(){return H},this.getContextAttributes=function(){return H.getContextAttributes()},this.forceContextLoss=function(){const b=Se.get("WEBGL_lose_context");b&&b.loseContext()},this.forceContextRestore=function(){const b=Se.get("WEBGL_lose_context");b&&b.restoreContext()},this.getPixelRatio=function(){return gt},this.setPixelRatio=function(b){b!==void 0&&(gt=b,this.setSize(U,et,!1))},this.getSize=function(b){return b.set(U,et)},this.setSize=function(b,q,st=!0){if(At.isPresenting){ae("WebGLRenderer: Can't change size while VR device is presenting.");return}U=b,et=q,i.width=Math.floor(b*gt),i.height=Math.floor(q*gt),st===!0&&(i.style.width=b+"px",i.style.height=q+"px"),Q!==null&&Q.setSize(i.width,i.height),this.setViewport(0,0,b,q)},this.getDrawingBufferSize=function(b){return b.set(U*gt,et*gt).floor()},this.setDrawingBufferSize=function(b,q,st){U=b,et=q,gt=st,i.width=Math.floor(b*st),i.height=Math.floor(q*st),this.setViewport(0,0,b,q)},this.setEffects=function(b){if(C===$n){console.error("THREE.WebGLRenderer: setEffects() requires outputBufferType set to HalfFloatType or FloatType.");return}if(b){for(let q=0;q<b.length;q++)if(b[q].isOutputPass===!0){console.warn("THREE.WebGLRenderer: OutputPass is not needed in setEffects(). Tone mapping and color space conversion are applied automatically.");break}}Q.setEffects(b||[])},this.getCurrentViewport=function(b){return b.copy(O)},this.getViewport=function(b){return b.copy(tt)},this.setViewport=function(b,q,st,J){b.isVector4?tt.set(b.x,b.y,b.z,b.w):tt.set(b,q,st,J),qt.viewport(O.copy(tt).multiplyScalar(gt).round())},this.getScissor=function(b){return b.copy(ct)},this.setScissor=function(b,q,st,J){b.isVector4?ct.set(b.x,b.y,b.z,b.w):ct.set(b,q,st,J),qt.scissor(V.copy(ct).multiplyScalar(gt).round())},this.getScissorTest=function(){return Dt},this.setScissorTest=function(b){qt.setScissorTest(Dt=b)},this.setOpaqueSort=function(b){bt=b},this.setTransparentSort=function(b){Bt=b},this.getClearColor=function(b){return b.copy(Ct.getClearColor())},this.setClearColor=function(){Ct.setClearColor(...arguments)},this.getClearAlpha=function(){return Ct.getClearAlpha()},this.setClearAlpha=function(){Ct.setClearAlpha(...arguments)},this.clear=function(b=!0,q=!0,st=!0){let J=0;if(b){let Z=!1;if(at!==null){const wt=at.texture.format;Z=y.has(wt)}if(Z){const wt=at.texture.type,zt=x.has(wt),Lt=Ct.getClearColor(),Ht=Ct.getClearAlpha(),kt=Lt.r,Qt=Lt.g,Wt=Lt.b;zt?(P[0]=kt,P[1]=Qt,P[2]=Wt,P[3]=Ht,H.clearBufferuiv(H.COLOR,0,P)):(N[0]=kt,N[1]=Qt,N[2]=Wt,N[3]=Ht,H.clearBufferiv(H.COLOR,0,N))}else J|=H.COLOR_BUFFER_BIT}q&&(J|=H.DEPTH_BUFFER_BIT),st&&(J|=H.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),H.clear(J)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){i.removeEventListener("webglcontextlost",ee,!1),i.removeEventListener("webglcontextrestored",Oe,!1),i.removeEventListener("webglcontextcreationerror",Me,!1),Ct.dispose(),yt.dispose(),Et.dispose(),E.dispose(),dt.dispose(),vt.dispose(),Rt.dispose(),Pt.dispose(),St.dispose(),Xt.dispose(),At.dispose(),At.removeEventListener("sessionstart",Dr),At.removeEventListener("sessionend",Ps),bi.stop()};function ee(b){b.preventDefault(),z0("WebGLRenderer: Context Lost."),D=!0}function Oe(){z0("WebGLRenderer: Context Restored."),D=!1;const b=w.autoReset,q=Ot.enabled,st=Ot.autoUpdate,J=Ot.needsUpdate,Z=Ot.type;_t(),w.autoReset=b,Ot.enabled=q,Ot.autoUpdate=st,Ot.needsUpdate=J,Ot.type=Z}function Me(b){be("WebGLRenderer: A WebGL context could not be created. Reason: ",b.statusMessage)}function Rn(b){const q=b.target;q.removeEventListener("dispose",Rn),di(q)}function di(b){Zo(b),E.remove(b)}function Zo(b){const q=E.get(b).programs;q!==void 0&&(q.forEach(function(st){Xt.releaseProgram(st)}),b.isShaderMaterial&&Xt.releaseShaderCache(b))}this.renderBufferDirect=function(b,q,st,J,Z,wt){q===null&&(q=Ae);const zt=Z.isMesh&&Z.matrixWorld.determinant()<0,Lt=Ja(b,q,st,J,Z);qt.setMaterial(J,zt);let Ht=st.index,kt=1;if(J.wireframe===!0){if(Ht=Zt.getWireframeAttribute(st),Ht===void 0)return;kt=2}const Qt=st.drawRange,Wt=st.attributes.position;let Jt=Qt.start*kt,Re=(Qt.start+Qt.count)*kt;wt!==null&&(Jt=Math.max(Jt,wt.start*kt),Re=Math.min(Re,(wt.start+wt.count)*kt)),Ht!==null?(Jt=Math.max(Jt,0),Re=Math.min(Re,Ht.count)):Wt!=null&&(Jt=Math.max(Jt,0),Re=Math.min(Re,Wt.count));const Ye=Re-Jt;if(Ye<0||Ye===1/0)return;Pt.setup(Z,J,Lt,st,Ht);let Xe,Ne=X;if(Ht!==null&&(Xe=lt.get(Ht),Ne=Ut,Ne.setIndex(Xe)),Z.isMesh)J.wireframe===!0?(qt.setLineWidth(J.wireframeLinewidth*Ke()),Ne.setMode(H.LINES)):Ne.setMode(H.TRIANGLES);else if(Z.isLine){let jt=J.linewidth;jt===void 0&&(jt=1),qt.setLineWidth(jt*Ke()),Z.isLineSegments?Ne.setMode(H.LINES):Z.isLineLoop?Ne.setMode(H.LINE_LOOP):Ne.setMode(H.LINE_STRIP)}else Z.isPoints?Ne.setMode(H.POINTS):Z.isSprite&&Ne.setMode(H.TRIANGLES);if(Z.isBatchedMesh)if(Z._multiDrawInstances!==null)Ho("WebGLRenderer: renderMultiDrawInstances has been deprecated and will be removed in r184. Append to renderMultiDraw arguments and use indirection."),Ne.renderMultiDrawInstances(Z._multiDrawStarts,Z._multiDrawCounts,Z._multiDrawCount,Z._multiDrawInstances);else if(Se.get("WEBGL_multi_draw"))Ne.renderMultiDraw(Z._multiDrawStarts,Z._multiDrawCounts,Z._multiDrawCount);else{const jt=Z._multiDrawStarts,Ce=Z._multiDrawCounts,ne=Z._multiDrawCount,_n=Ht?lt.get(Ht).bytesPerElement:1,Gi=E.get(J).currentProgram.getUniforms();for(let vn=0;vn<ne;vn++)Gi.setValue(H,"_gl_DrawID",vn),Ne.render(jt[vn]/_n,Ce[vn])}else if(Z.isInstancedMesh)Ne.renderInstances(Jt,Ye,Z.count);else if(st.isInstancedBufferGeometry){const jt=st._maxInstanceCount!==void 0?st._maxInstanceCount:1/0,Ce=Math.min(st.instanceCount,jt);Ne.renderInstances(Jt,Ye,Ce)}else Ne.render(Jt,Ye)};function Ns(b,q,st){b.transparent===!0&&b.side===ca&&b.forceSinglePass===!1?(b.side=Xn,b.needsUpdate=!0,Ur(b,q,st),b.side=Qa,b.needsUpdate=!0,Ur(b,q,st),b.side=ca):Ur(b,q,st)}this.compile=function(b,q,st=null){st===null&&(st=b),B=Et.get(st),B.init(q),z.push(B),st.traverseVisible(function(Z){Z.isLight&&Z.layers.test(q.layers)&&(B.pushLight(Z),Z.castShadow&&B.pushShadow(Z))}),b!==st&&b.traverseVisible(function(Z){Z.isLight&&Z.layers.test(q.layers)&&(B.pushLight(Z),Z.castShadow&&B.pushShadow(Z))}),B.setupLights();const J=new Set;return b.traverse(function(Z){if(!(Z.isMesh||Z.isPoints||Z.isLine||Z.isSprite))return;const wt=Z.material;if(wt)if(Array.isArray(wt))for(let zt=0;zt<wt.length;zt++){const Lt=wt[zt];Ns(Lt,st,Z),J.add(Lt)}else Ns(wt,st,Z),J.add(wt)}),B=z.pop(),J},this.compileAsync=function(b,q,st=null){const J=this.compile(b,q,st);return new Promise(Z=>{function wt(){if(J.forEach(function(zt){E.get(zt).currentProgram.isReady()&&J.delete(zt)}),J.size===0){Z(b);return}setTimeout(wt,10)}Se.get("KHR_parallel_shader_compile")!==null?wt():setTimeout(wt,10)})};let Cr=null;function Os(b){Cr&&Cr(b)}function Dr(){bi.stop()}function Ps(){bi.start()}const bi=new lv;bi.setAnimationLoop(Os),typeof self<"u"&&bi.setContext(self),this.setAnimationLoop=function(b){Cr=b,At.setAnimationLoop(b),b===null?bi.stop():bi.start()},At.addEventListener("sessionstart",Dr),At.addEventListener("sessionend",Ps),this.render=function(b,q){if(q!==void 0&&q.isCamera!==!0){be("WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(D===!0)return;const st=At.enabled===!0&&At.isPresenting===!0,J=Q!==null&&(at===null||st)&&Q.begin(R,at);if(b.matrixWorldAutoUpdate===!0&&b.updateMatrixWorld(),q.parent===null&&q.matrixWorldAutoUpdate===!0&&q.updateMatrixWorld(),At.enabled===!0&&At.isPresenting===!0&&(Q===null||Q.isCompositing()===!1)&&(At.cameraAutoUpdate===!0&&At.updateCamera(q),q=At.getCamera()),b.isScene===!0&&b.onBeforeRender(R,b,q,at),B=Et.get(b,z.length),B.init(q),z.push(B),je.multiplyMatrices(q.projectionMatrix,q.matrixWorldInverse),Vt.setFromProjectionMatrix(je,Ni,q.reversedDepth),fe=this.localClippingEnabled,It=Ft.init(this.clippingPlanes,fe),L=yt.get(b,F.length),L.init(),F.push(L),At.enabled===!0&&At.isPresenting===!0){const zt=R.xr.getDepthSensingMesh();zt!==null&&ti(zt,q,-1/0,R.sortObjects)}ti(b,q,0,R.sortObjects),L.finish(),R.sortObjects===!0&&L.sort(bt,Bt),re=At.enabled===!1||At.isPresenting===!1||At.hasDepthSensing()===!1,re&&Ct.addToRenderList(L,b),this.info.render.frame++,It===!0&&Ft.beginShadows();const Z=B.state.shadowsArray;if(Ot.render(Z,b,q),It===!0&&Ft.endShadows(),this.info.autoReset===!0&&this.info.reset(),(J&&Q.hasRenderPass())===!1){const zt=L.opaque,Lt=L.transmissive;if(B.setupLights(),q.isArrayCamera){const Ht=q.cameras;if(Lt.length>0)for(let kt=0,Qt=Ht.length;kt<Qt;kt++){const Wt=Ht[kt];gn(zt,Lt,b,Wt)}re&&Ct.render(b);for(let kt=0,Qt=Ht.length;kt<Qt;kt++){const Wt=Ht[kt];an(L,b,Wt,Wt.viewport)}}else Lt.length>0&&gn(zt,Lt,b,q),re&&Ct.render(b),an(L,b,q)}at!==null&&rt===0&&(W.updateMultisampleRenderTarget(at),W.updateRenderTargetMipmap(at)),J&&Q.end(R),b.isScene===!0&&b.onAfterRender(R,b,q),Pt.resetDefaultState(),ut=-1,ht=null,z.pop(),z.length>0?(B=z[z.length-1],It===!0&&Ft.setGlobalState(R.clippingPlanes,B.state.camera)):B=null,F.pop(),F.length>0?L=F[F.length-1]:L=null};function ti(b,q,st,J){if(b.visible===!1)return;if(b.layers.test(q.layers)){if(b.isGroup)st=b.renderOrder;else if(b.isLOD)b.autoUpdate===!0&&b.update(q);else if(b.isLight)B.pushLight(b),b.castShadow&&B.pushShadow(b);else if(b.isSprite){if(!b.frustumCulled||Vt.intersectsSprite(b)){J&&he.setFromMatrixPosition(b.matrixWorld).applyMatrix4(je);const zt=Rt.update(b),Lt=b.material;Lt.visible&&L.push(b,zt,Lt,st,he.z,null)}}else if((b.isMesh||b.isLine||b.isPoints)&&(!b.frustumCulled||Vt.intersectsObject(b))){const zt=Rt.update(b),Lt=b.material;if(J&&(b.boundingSphere!==void 0?(b.boundingSphere===null&&b.computeBoundingSphere(),he.copy(b.boundingSphere.center)):(zt.boundingSphere===null&&zt.computeBoundingSphere(),he.copy(zt.boundingSphere.center)),he.applyMatrix4(b.matrixWorld).applyMatrix4(je)),Array.isArray(Lt)){const Ht=zt.groups;for(let kt=0,Qt=Ht.length;kt<Qt;kt++){const Wt=Ht[kt],Jt=Lt[Wt.materialIndex];Jt&&Jt.visible&&L.push(b,zt,Jt,st,he.z,Wt)}}else Lt.visible&&L.push(b,zt,Lt,st,he.z,null)}}const wt=b.children;for(let zt=0,Lt=wt.length;zt<Lt;zt++)ti(wt[zt],q,st,J)}function an(b,q,st,J){const{opaque:Z,transmissive:wt,transparent:zt}=b;B.setupLightsView(st),It===!0&&Ft.setGlobalState(R.clippingPlanes,st),J&&qt.viewport(O.copy(J)),Z.length>0&&pi(Z,q,st),wt.length>0&&pi(wt,q,st),zt.length>0&&pi(zt,q,st),qt.buffers.depth.setTest(!0),qt.buffers.depth.setMask(!0),qt.buffers.color.setMask(!0),qt.setPolygonOffset(!1)}function gn(b,q,st,J){if((st.isScene===!0?st.overrideMaterial:null)!==null)return;if(B.state.transmissionRenderTarget[J.id]===void 0){const Jt=Se.has("EXT_color_buffer_half_float")||Se.has("EXT_color_buffer_float");B.state.transmissionRenderTarget[J.id]=new Pi(1,1,{generateMipmaps:!0,type:Jt?pa:$n,minFilter:br,samples:Le.samples,stencilBuffer:c,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:ye.workingColorSpace})}const wt=B.state.transmissionRenderTarget[J.id],zt=J.viewport||O;wt.setSize(zt.z*R.transmissionResolutionScale,zt.w*R.transmissionResolutionScale);const Lt=R.getRenderTarget(),Ht=R.getActiveCubeFace(),kt=R.getActiveMipmapLevel();R.setRenderTarget(wt),R.getClearColor(Mt),xt=R.getClearAlpha(),xt<1&&R.setClearColor(16777215,.5),R.clear(),re&&Ct.render(st);const Qt=R.toneMapping;R.toneMapping=Oi;const Wt=J.viewport;if(J.viewport!==void 0&&(J.viewport=void 0),B.setupLightsView(J),It===!0&&Ft.setGlobalState(R.clippingPlanes,J),pi(b,st,J),W.updateMultisampleRenderTarget(wt),W.updateRenderTargetMipmap(wt),Se.has("WEBGL_multisampled_render_to_texture")===!1){let Jt=!1;for(let Re=0,Ye=q.length;Re<Ye;Re++){const Xe=q[Re],{object:Ne,geometry:jt,material:Ce,group:ne}=Xe;if(Ce.side===ca&&Ne.layers.test(J.layers)){const _n=Ce.side;Ce.side=Xn,Ce.needsUpdate=!0,wr(Ne,st,J,jt,Ce,ne),Ce.side=_n,Ce.needsUpdate=!0,Jt=!0}}Jt===!0&&(W.updateMultisampleRenderTarget(wt),W.updateRenderTargetMipmap(wt))}R.setRenderTarget(Lt,Ht,kt),R.setClearColor(Mt,xt),Wt!==void 0&&(J.viewport=Wt),R.toneMapping=Qt}function pi(b,q,st){const J=q.isScene===!0?q.overrideMaterial:null;for(let Z=0,wt=b.length;Z<wt;Z++){const zt=b[Z],{object:Lt,geometry:Ht,group:kt}=zt;let Qt=zt.material;Qt.allowOverride===!0&&J!==null&&(Qt=J),Lt.layers.test(st.layers)&&wr(Lt,q,st,Ht,Qt,kt)}}function wr(b,q,st,J,Z,wt){b.onBeforeRender(R,q,st,J,Z,wt),b.modelViewMatrix.multiplyMatrices(st.matrixWorldInverse,b.matrixWorld),b.normalMatrix.getNormalMatrix(b.modelViewMatrix),Z.onBeforeRender(R,q,st,J,b,wt),Z.transparent===!0&&Z.side===ca&&Z.forceSinglePass===!1?(Z.side=Xn,Z.needsUpdate=!0,R.renderBufferDirect(st,q,J,Z,b,wt),Z.side=Qa,Z.needsUpdate=!0,R.renderBufferDirect(st,q,J,Z,b,wt),Z.side=ca):R.renderBufferDirect(st,q,J,Z,b,wt),b.onAfterRender(R,q,st,J,Z,wt)}function Ur(b,q,st){q.isScene!==!0&&(q=Ae);const J=E.get(b),Z=B.state.lights,wt=B.state.shadowsArray,zt=Z.state.version,Lt=Xt.getParameters(b,Z.state,wt,q,st),Ht=Xt.getProgramCacheKey(Lt);let kt=J.programs;J.environment=b.isMeshStandardMaterial?q.environment:null,J.fog=q.fog,J.envMap=(b.isMeshStandardMaterial?vt:dt).get(b.envMap||J.environment),J.envMapRotation=J.environment!==null&&b.envMap===null?q.environmentRotation:b.envMapRotation,kt===void 0&&(b.addEventListener("dispose",Rn),kt=new Map,J.programs=kt);let Qt=kt.get(Ht);if(Qt!==void 0){if(J.currentProgram===Qt&&J.lightsStateVersion===zt)return Fs(b,Lt),Qt}else Lt.uniforms=Xt.getUniforms(b),b.onBeforeCompile(Lt,R),Qt=Xt.acquireProgram(Lt,Ht),kt.set(Ht,Qt),J.uniforms=Lt.uniforms;const Wt=J.uniforms;return(!b.isShaderMaterial&&!b.isRawShaderMaterial||b.clipping===!0)&&(Wt.clippingPlanes=Ft.uniform),Fs(b,Lt),J.needsLights=_a(b),J.lightsStateVersion=zt,J.needsLights&&(Wt.ambientLightColor.value=Z.state.ambient,Wt.lightProbe.value=Z.state.probe,Wt.directionalLights.value=Z.state.directional,Wt.directionalLightShadows.value=Z.state.directionalShadow,Wt.spotLights.value=Z.state.spot,Wt.spotLightShadows.value=Z.state.spotShadow,Wt.rectAreaLights.value=Z.state.rectArea,Wt.ltc_1.value=Z.state.rectAreaLTC1,Wt.ltc_2.value=Z.state.rectAreaLTC2,Wt.pointLights.value=Z.state.point,Wt.pointLightShadows.value=Z.state.pointShadow,Wt.hemisphereLights.value=Z.state.hemi,Wt.directionalShadowMap.value=Z.state.directionalShadowMap,Wt.directionalShadowMatrix.value=Z.state.directionalShadowMatrix,Wt.spotShadowMap.value=Z.state.spotShadowMap,Wt.spotLightMatrix.value=Z.state.spotLightMatrix,Wt.spotLightMap.value=Z.state.spotLightMap,Wt.pointShadowMap.value=Z.state.pointShadowMap,Wt.pointShadowMatrix.value=Z.state.pointShadowMatrix),J.currentProgram=Qt,J.uniformsList=null,Qt}function jo(b){if(b.uniformsList===null){const q=b.currentProgram.getUniforms();b.uniformsList=Uu.seqWithValue(q.seq,b.uniforms)}return b.uniformsList}function Fs(b,q){const st=E.get(b);st.outputColorSpace=q.outputColorSpace,st.batching=q.batching,st.batchingColor=q.batchingColor,st.instancing=q.instancing,st.instancingColor=q.instancingColor,st.instancingMorph=q.instancingMorph,st.skinning=q.skinning,st.morphTargets=q.morphTargets,st.morphNormals=q.morphNormals,st.morphColors=q.morphColors,st.morphTargetsCount=q.morphTargetsCount,st.numClippingPlanes=q.numClippingPlanes,st.numIntersection=q.numClipIntersection,st.vertexAlphas=q.vertexAlphas,st.vertexTangents=q.vertexTangents,st.toneMapping=q.toneMapping}function Ja(b,q,st,J,Z){q.isScene!==!0&&(q=Ae),W.resetTextureUnits();const wt=q.fog,zt=J.isMeshStandardMaterial?q.environment:null,Lt=at===null?R.outputColorSpace:at.isXRRenderTarget===!0?at.texture.colorSpace:Ds,Ht=(J.isMeshStandardMaterial?vt:dt).get(J.envMap||zt),kt=J.vertexColors===!0&&!!st.attributes.color&&st.attributes.color.itemSize===4,Qt=!!st.attributes.tangent&&(!!J.normalMap||J.anisotropy>0),Wt=!!st.morphAttributes.position,Jt=!!st.morphAttributes.normal,Re=!!st.morphAttributes.color;let Ye=Oi;J.toneMapped&&(at===null||at.isXRRenderTarget===!0)&&(Ye=R.toneMapping);const Xe=st.morphAttributes.position||st.morphAttributes.normal||st.morphAttributes.color,Ne=Xe!==void 0?Xe.length:0,jt=E.get(J),Ce=B.state.lights;if(It===!0&&(fe===!0||b!==ht)){const Sn=b===ht&&J.id===ut;Ft.setState(J,b,Sn)}let ne=!1;J.version===jt.__version?(jt.needsLights&&jt.lightsStateVersion!==Ce.state.version||jt.outputColorSpace!==Lt||Z.isBatchedMesh&&jt.batching===!1||!Z.isBatchedMesh&&jt.batching===!0||Z.isBatchedMesh&&jt.batchingColor===!0&&Z.colorTexture===null||Z.isBatchedMesh&&jt.batchingColor===!1&&Z.colorTexture!==null||Z.isInstancedMesh&&jt.instancing===!1||!Z.isInstancedMesh&&jt.instancing===!0||Z.isSkinnedMesh&&jt.skinning===!1||!Z.isSkinnedMesh&&jt.skinning===!0||Z.isInstancedMesh&&jt.instancingColor===!0&&Z.instanceColor===null||Z.isInstancedMesh&&jt.instancingColor===!1&&Z.instanceColor!==null||Z.isInstancedMesh&&jt.instancingMorph===!0&&Z.morphTexture===null||Z.isInstancedMesh&&jt.instancingMorph===!1&&Z.morphTexture!==null||jt.envMap!==Ht||J.fog===!0&&jt.fog!==wt||jt.numClippingPlanes!==void 0&&(jt.numClippingPlanes!==Ft.numPlanes||jt.numIntersection!==Ft.numIntersection)||jt.vertexAlphas!==kt||jt.vertexTangents!==Qt||jt.morphTargets!==Wt||jt.morphNormals!==Jt||jt.morphColors!==Re||jt.toneMapping!==Ye||jt.morphTargetsCount!==Ne)&&(ne=!0):(ne=!0,jt.__version=J.version);let _n=jt.currentProgram;ne===!0&&(_n=Ur(J,q,Z));let Gi=!1,vn=!1,ei=!1;const Pe=_n.getUniforms(),xn=jt.uniforms;if(qt.useProgram(_n.program)&&(Gi=!0,vn=!0,ei=!0),J.id!==ut&&(ut=J.id,vn=!0),Gi||ht!==b){qt.buffers.depth.getReversed()&&b.reversedDepth!==!0&&(b._reversedDepth=!0,b.updateProjectionMatrix()),Pe.setValue(H,"projectionMatrix",b.projectionMatrix),Pe.setValue(H,"viewMatrix",b.matrixWorldInverse);const Mn=Pe.map.cameraPosition;Mn!==void 0&&Mn.setValue(H,me.setFromMatrixPosition(b.matrixWorld)),Le.logarithmicDepthBuffer&&Pe.setValue(H,"logDepthBufFC",2/(Math.log(b.far+1)/Math.LN2)),(J.isMeshPhongMaterial||J.isMeshToonMaterial||J.isMeshLambertMaterial||J.isMeshBasicMaterial||J.isMeshStandardMaterial||J.isShaderMaterial)&&Pe.setValue(H,"isOrthographic",b.isOrthographicCamera===!0),ht!==b&&(ht=b,vn=!0,ei=!0)}if(jt.needsLights&&(Ce.state.directionalShadowMap.length>0&&Pe.setValue(H,"directionalShadowMap",Ce.state.directionalShadowMap,W),Ce.state.spotShadowMap.length>0&&Pe.setValue(H,"spotShadowMap",Ce.state.spotShadowMap,W),Ce.state.pointShadowMap.length>0&&Pe.setValue(H,"pointShadowMap",Ce.state.pointShadowMap,W)),Z.isSkinnedMesh){Pe.setOptional(H,Z,"bindMatrix"),Pe.setOptional(H,Z,"bindMatrixInverse");const Sn=Z.skeleton;Sn&&(Sn.boneTexture===null&&Sn.computeBoneTexture(),Pe.setValue(H,"boneTexture",Sn.boneTexture,W))}Z.isBatchedMesh&&(Pe.setOptional(H,Z,"batchingTexture"),Pe.setValue(H,"batchingTexture",Z._matricesTexture,W),Pe.setOptional(H,Z,"batchingIdTexture"),Pe.setValue(H,"batchingIdTexture",Z._indirectTexture,W),Pe.setOptional(H,Z,"batchingColorTexture"),Z._colorsTexture!==null&&Pe.setValue(H,"batchingColorTexture",Z._colorsTexture,W));const cn=st.morphAttributes;if((cn.position!==void 0||cn.normal!==void 0||cn.color!==void 0)&&oe.update(Z,st,_n),(vn||jt.receiveShadow!==Z.receiveShadow)&&(jt.receiveShadow=Z.receiveShadow,Pe.setValue(H,"receiveShadow",Z.receiveShadow)),J.isMeshGouraudMaterial&&J.envMap!==null&&(xn.envMap.value=Ht,xn.flipEnvMap.value=Ht.isCubeTexture&&Ht.isRenderTargetTexture===!1?-1:1),J.isMeshStandardMaterial&&J.envMap===null&&q.environment!==null&&(xn.envMapIntensity.value=q.environmentIntensity),xn.dfgLUT!==void 0&&(xn.dfgLUT.value=XA()),vn&&(Pe.setValue(H,"toneMappingExposure",R.toneMappingExposure),jt.needsLights&&zs(xn,ei),wt&&J.fog===!0&&te.refreshFogUniforms(xn,wt),te.refreshMaterialUniforms(xn,J,gt,et,B.state.transmissionRenderTarget[b.id]),Uu.upload(H,jo(jt),xn,W)),J.isShaderMaterial&&J.uniformsNeedUpdate===!0&&(Uu.upload(H,jo(jt),xn,W),J.uniformsNeedUpdate=!1),J.isSpriteMaterial&&Pe.setValue(H,"center",Z.center),Pe.setValue(H,"modelViewMatrix",Z.modelViewMatrix),Pe.setValue(H,"normalMatrix",Z.normalMatrix),Pe.setValue(H,"modelMatrix",Z.matrixWorld),J.isShaderMaterial||J.isRawShaderMaterial){const Sn=J.uniformsGroups;for(let Mn=0,Lr=Sn.length;Mn<Lr;Mn++){const mi=Sn[Mn];St.update(mi,_n),St.bind(mi,_n)}}return _n}function zs(b,q){b.ambientLightColor.needsUpdate=q,b.lightProbe.needsUpdate=q,b.directionalLights.needsUpdate=q,b.directionalLightShadows.needsUpdate=q,b.pointLights.needsUpdate=q,b.pointLightShadows.needsUpdate=q,b.spotLights.needsUpdate=q,b.spotLightShadows.needsUpdate=q,b.rectAreaLights.needsUpdate=q,b.hemisphereLights.needsUpdate=q}function _a(b){return b.isMeshLambertMaterial||b.isMeshToonMaterial||b.isMeshPhongMaterial||b.isMeshStandardMaterial||b.isShadowMaterial||b.isShaderMaterial&&b.lights===!0}this.getActiveCubeFace=function(){return k},this.getActiveMipmapLevel=function(){return rt},this.getRenderTarget=function(){return at},this.setRenderTargetTextures=function(b,q,st){const J=E.get(b);J.__autoAllocateDepthBuffer=b.resolveDepthBuffer===!1,J.__autoAllocateDepthBuffer===!1&&(J.__useRenderToTexture=!1),E.get(b.texture).__webglTexture=q,E.get(b.depthTexture).__webglTexture=J.__autoAllocateDepthBuffer?void 0:st,J.__hasExternalTextures=!0},this.setRenderTargetFramebuffer=function(b,q){const st=E.get(b);st.__webglFramebuffer=q,st.__useDefaultFramebuffer=q===void 0};const va=H.createFramebuffer();this.setRenderTarget=function(b,q=0,st=0){at=b,k=q,rt=st;let J=null,Z=!1,wt=!1;if(b){const Lt=E.get(b);if(Lt.__useDefaultFramebuffer!==void 0){qt.bindFramebuffer(H.FRAMEBUFFER,Lt.__webglFramebuffer),O.copy(b.viewport),V.copy(b.scissor),nt=b.scissorTest,qt.viewport(O),qt.scissor(V),qt.setScissorTest(nt),ut=-1;return}else if(Lt.__webglFramebuffer===void 0)W.setupRenderTarget(b);else if(Lt.__hasExternalTextures)W.rebindTextures(b,E.get(b.texture).__webglTexture,E.get(b.depthTexture).__webglTexture);else if(b.depthBuffer){const Qt=b.depthTexture;if(Lt.__boundDepthTexture!==Qt){if(Qt!==null&&E.has(Qt)&&(b.width!==Qt.image.width||b.height!==Qt.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");W.setupDepthRenderbuffer(b)}}const Ht=b.texture;(Ht.isData3DTexture||Ht.isDataArrayTexture||Ht.isCompressedArrayTexture)&&(wt=!0);const kt=E.get(b).__webglFramebuffer;b.isWebGLCubeRenderTarget?(Array.isArray(kt[q])?J=kt[q][st]:J=kt[q],Z=!0):b.samples>0&&W.useMultisampledRTT(b)===!1?J=E.get(b).__webglMultisampledFramebuffer:Array.isArray(kt)?J=kt[st]:J=kt,O.copy(b.viewport),V.copy(b.scissor),nt=b.scissorTest}else O.copy(tt).multiplyScalar(gt).floor(),V.copy(ct).multiplyScalar(gt).floor(),nt=Dt;if(st!==0&&(J=va),qt.bindFramebuffer(H.FRAMEBUFFER,J)&&qt.drawBuffers(b,J),qt.viewport(O),qt.scissor(V),qt.setScissorTest(nt),Z){const Lt=E.get(b.texture);H.framebufferTexture2D(H.FRAMEBUFFER,H.COLOR_ATTACHMENT0,H.TEXTURE_CUBE_MAP_POSITIVE_X+q,Lt.__webglTexture,st)}else if(wt){const Lt=q;for(let Ht=0;Ht<b.textures.length;Ht++){const kt=E.get(b.textures[Ht]);H.framebufferTextureLayer(H.FRAMEBUFFER,H.COLOR_ATTACHMENT0+Ht,kt.__webglTexture,st,Lt)}}else if(b!==null&&st!==0){const Lt=E.get(b.texture);H.framebufferTexture2D(H.FRAMEBUFFER,H.COLOR_ATTACHMENT0,H.TEXTURE_2D,Lt.__webglTexture,st)}ut=-1},this.readRenderTargetPixels=function(b,q,st,J,Z,wt,zt,Lt=0){if(!(b&&b.isWebGLRenderTarget)){be("WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Ht=E.get(b).__webglFramebuffer;if(b.isWebGLCubeRenderTarget&&zt!==void 0&&(Ht=Ht[zt]),Ht){qt.bindFramebuffer(H.FRAMEBUFFER,Ht);try{const kt=b.textures[Lt],Qt=kt.format,Wt=kt.type;if(!Le.textureFormatReadable(Qt)){be("WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!Le.textureTypeReadable(Wt)){be("WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}q>=0&&q<=b.width-J&&st>=0&&st<=b.height-Z&&(b.textures.length>1&&H.readBuffer(H.COLOR_ATTACHMENT0+Lt),H.readPixels(q,st,J,Z,Tt.convert(Qt),Tt.convert(Wt),wt))}finally{const kt=at!==null?E.get(at).__webglFramebuffer:null;qt.bindFramebuffer(H.FRAMEBUFFER,kt)}}},this.readRenderTargetPixelsAsync=async function(b,q,st,J,Z,wt,zt,Lt=0){if(!(b&&b.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Ht=E.get(b).__webglFramebuffer;if(b.isWebGLCubeRenderTarget&&zt!==void 0&&(Ht=Ht[zt]),Ht)if(q>=0&&q<=b.width-J&&st>=0&&st<=b.height-Z){qt.bindFramebuffer(H.FRAMEBUFFER,Ht);const kt=b.textures[Lt],Qt=kt.format,Wt=kt.type;if(!Le.textureFormatReadable(Qt))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!Le.textureTypeReadable(Wt))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");const Jt=H.createBuffer();H.bindBuffer(H.PIXEL_PACK_BUFFER,Jt),H.bufferData(H.PIXEL_PACK_BUFFER,wt.byteLength,H.STREAM_READ),b.textures.length>1&&H.readBuffer(H.COLOR_ATTACHMENT0+Lt),H.readPixels(q,st,J,Z,Tt.convert(Qt),Tt.convert(Wt),0);const Re=at!==null?E.get(at).__webglFramebuffer:null;qt.bindFramebuffer(H.FRAMEBUFFER,Re);const Ye=H.fenceSync(H.SYNC_GPU_COMMANDS_COMPLETE,0);return H.flush(),await hM(H,Ye,4),H.bindBuffer(H.PIXEL_PACK_BUFFER,Jt),H.getBufferSubData(H.PIXEL_PACK_BUFFER,0,wt),H.deleteBuffer(Jt),H.deleteSync(Ye),wt}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")},this.copyFramebufferToTexture=function(b,q=null,st=0){const J=Math.pow(2,-st),Z=Math.floor(b.image.width*J),wt=Math.floor(b.image.height*J),zt=q!==null?q.x:0,Lt=q!==null?q.y:0;W.setTexture2D(b,0),H.copyTexSubImage2D(H.TEXTURE_2D,st,0,0,zt,Lt,Z,wt),qt.unbindTexture()};const $a=H.createFramebuffer(),xa=H.createFramebuffer();this.copyTextureToTexture=function(b,q,st=null,J=null,Z=0,wt=null){wt===null&&(Z!==0?(Ho("WebGLRenderer: copyTextureToTexture function signature has changed to support src and dst mipmap levels."),wt=Z,Z=0):wt=0);let zt,Lt,Ht,kt,Qt,Wt,Jt,Re,Ye;const Xe=b.isCompressedTexture?b.mipmaps[wt]:b.image;if(st!==null)zt=st.max.x-st.min.x,Lt=st.max.y-st.min.y,Ht=st.isBox3?st.max.z-st.min.z:1,kt=st.min.x,Qt=st.min.y,Wt=st.isBox3?st.min.z:0;else{const cn=Math.pow(2,-Z);zt=Math.floor(Xe.width*cn),Lt=Math.floor(Xe.height*cn),b.isDataArrayTexture?Ht=Xe.depth:b.isData3DTexture?Ht=Math.floor(Xe.depth*cn):Ht=1,kt=0,Qt=0,Wt=0}J!==null?(Jt=J.x,Re=J.y,Ye=J.z):(Jt=0,Re=0,Ye=0);const Ne=Tt.convert(q.format),jt=Tt.convert(q.type);let Ce;q.isData3DTexture?(W.setTexture3D(q,0),Ce=H.TEXTURE_3D):q.isDataArrayTexture||q.isCompressedArrayTexture?(W.setTexture2DArray(q,0),Ce=H.TEXTURE_2D_ARRAY):(W.setTexture2D(q,0),Ce=H.TEXTURE_2D),H.pixelStorei(H.UNPACK_FLIP_Y_WEBGL,q.flipY),H.pixelStorei(H.UNPACK_PREMULTIPLY_ALPHA_WEBGL,q.premultiplyAlpha),H.pixelStorei(H.UNPACK_ALIGNMENT,q.unpackAlignment);const ne=H.getParameter(H.UNPACK_ROW_LENGTH),_n=H.getParameter(H.UNPACK_IMAGE_HEIGHT),Gi=H.getParameter(H.UNPACK_SKIP_PIXELS),vn=H.getParameter(H.UNPACK_SKIP_ROWS),ei=H.getParameter(H.UNPACK_SKIP_IMAGES);H.pixelStorei(H.UNPACK_ROW_LENGTH,Xe.width),H.pixelStorei(H.UNPACK_IMAGE_HEIGHT,Xe.height),H.pixelStorei(H.UNPACK_SKIP_PIXELS,kt),H.pixelStorei(H.UNPACK_SKIP_ROWS,Qt),H.pixelStorei(H.UNPACK_SKIP_IMAGES,Wt);const Pe=b.isDataArrayTexture||b.isData3DTexture,xn=q.isDataArrayTexture||q.isData3DTexture;if(b.isDepthTexture){const cn=E.get(b),Sn=E.get(q),Mn=E.get(cn.__renderTarget),Lr=E.get(Sn.__renderTarget);qt.bindFramebuffer(H.READ_FRAMEBUFFER,Mn.__webglFramebuffer),qt.bindFramebuffer(H.DRAW_FRAMEBUFFER,Lr.__webglFramebuffer);for(let mi=0;mi<Ht;mi++)Pe&&(H.framebufferTextureLayer(H.READ_FRAMEBUFFER,H.COLOR_ATTACHMENT0,E.get(b).__webglTexture,Z,Wt+mi),H.framebufferTextureLayer(H.DRAW_FRAMEBUFFER,H.COLOR_ATTACHMENT0,E.get(q).__webglTexture,wt,Ye+mi)),H.blitFramebuffer(kt,Qt,zt,Lt,Jt,Re,zt,Lt,H.DEPTH_BUFFER_BIT,H.NEAREST);qt.bindFramebuffer(H.READ_FRAMEBUFFER,null),qt.bindFramebuffer(H.DRAW_FRAMEBUFFER,null)}else if(Z!==0||b.isRenderTargetTexture||E.has(b)){const cn=E.get(b),Sn=E.get(q);qt.bindFramebuffer(H.READ_FRAMEBUFFER,$a),qt.bindFramebuffer(H.DRAW_FRAMEBUFFER,xa);for(let Mn=0;Mn<Ht;Mn++)Pe?H.framebufferTextureLayer(H.READ_FRAMEBUFFER,H.COLOR_ATTACHMENT0,cn.__webglTexture,Z,Wt+Mn):H.framebufferTexture2D(H.READ_FRAMEBUFFER,H.COLOR_ATTACHMENT0,H.TEXTURE_2D,cn.__webglTexture,Z),xn?H.framebufferTextureLayer(H.DRAW_FRAMEBUFFER,H.COLOR_ATTACHMENT0,Sn.__webglTexture,wt,Ye+Mn):H.framebufferTexture2D(H.DRAW_FRAMEBUFFER,H.COLOR_ATTACHMENT0,H.TEXTURE_2D,Sn.__webglTexture,wt),Z!==0?H.blitFramebuffer(kt,Qt,zt,Lt,Jt,Re,zt,Lt,H.COLOR_BUFFER_BIT,H.NEAREST):xn?H.copyTexSubImage3D(Ce,wt,Jt,Re,Ye+Mn,kt,Qt,zt,Lt):H.copyTexSubImage2D(Ce,wt,Jt,Re,kt,Qt,zt,Lt);qt.bindFramebuffer(H.READ_FRAMEBUFFER,null),qt.bindFramebuffer(H.DRAW_FRAMEBUFFER,null)}else xn?b.isDataTexture||b.isData3DTexture?H.texSubImage3D(Ce,wt,Jt,Re,Ye,zt,Lt,Ht,Ne,jt,Xe.data):q.isCompressedArrayTexture?H.compressedTexSubImage3D(Ce,wt,Jt,Re,Ye,zt,Lt,Ht,Ne,Xe.data):H.texSubImage3D(Ce,wt,Jt,Re,Ye,zt,Lt,Ht,Ne,jt,Xe):b.isDataTexture?H.texSubImage2D(H.TEXTURE_2D,wt,Jt,Re,zt,Lt,Ne,jt,Xe.data):b.isCompressedTexture?H.compressedTexSubImage2D(H.TEXTURE_2D,wt,Jt,Re,Xe.width,Xe.height,Ne,Xe.data):H.texSubImage2D(H.TEXTURE_2D,wt,Jt,Re,zt,Lt,Ne,jt,Xe);H.pixelStorei(H.UNPACK_ROW_LENGTH,ne),H.pixelStorei(H.UNPACK_IMAGE_HEIGHT,_n),H.pixelStorei(H.UNPACK_SKIP_PIXELS,Gi),H.pixelStorei(H.UNPACK_SKIP_ROWS,vn),H.pixelStorei(H.UNPACK_SKIP_IMAGES,ei),wt===0&&q.generateMipmaps&&H.generateMipmap(Ce),qt.unbindTexture()},this.initRenderTarget=function(b){E.get(b).__webglFramebuffer===void 0&&W.setupRenderTarget(b)},this.initTexture=function(b){b.isCubeTexture?W.setTextureCube(b,0):b.isData3DTexture?W.setTexture3D(b,0):b.isDataArrayTexture||b.isCompressedArrayTexture?W.setTexture2DArray(b,0):W.setTexture2D(b,0),qt.unbindTexture()},this.resetState=function(){k=0,rt=0,at=null,qt.reset(),Pt.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return Ni}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const i=this.getContext();i.drawingBufferColorSpace=ye._getDrawingBufferColorSpace(e),i.unpackColorSpace=ye._getUnpackColorSpace()}}var Rh={exports:{}},Ch={},Dh={exports:{}},wh={};var A_;function kA(){if(A_)return wh;A_=1;var o=Vo();function e(g,S){return g===S&&(g!==0||1/g===1/S)||g!==g&&S!==S}var i=typeof Object.is=="function"?Object.is:e,r=o.useState,l=o.useEffect,c=o.useLayoutEffect,h=o.useDebugValue;function d(g,S){var M=S(),A=r({inst:{value:M,getSnapshot:S}}),C=A[0].inst,y=A[1];return c(function(){C.value=M,C.getSnapshot=S,m(C)&&y({inst:C})},[g,M,S]),l(function(){return m(C)&&y({inst:C}),g(function(){m(C)&&y({inst:C})})},[g]),h(M),M}function m(g){var S=g.getSnapshot;g=g.value;try{var M=S();return!i(g,M)}catch{return!0}}function p(g,S){return S()}var v=typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"?p:d;return wh.useSyncExternalStore=o.useSyncExternalStore!==void 0?o.useSyncExternalStore:v,wh}var R_;function WA(){return R_||(R_=1,Dh.exports=kA()),Dh.exports}var C_;function qA(){if(C_)return Ch;C_=1;var o=Vo(),e=WA();function i(p,v){return p===v&&(p!==0||1/p===1/v)||p!==p&&v!==v}var r=typeof Object.is=="function"?Object.is:i,l=e.useSyncExternalStore,c=o.useRef,h=o.useEffect,d=o.useMemo,m=o.useDebugValue;return Ch.useSyncExternalStoreWithSelector=function(p,v,g,S,M){var A=c(null);if(A.current===null){var C={hasValue:!1,value:null};A.current=C}else C=A.current;A=d(function(){function x(F){if(!P){if(P=!0,N=F,F=S(F),M!==void 0&&C.hasValue){var z=C.value;if(M(z,F))return L=z}return L=F}if(z=L,r(N,F))return z;var Q=S(F);return M!==void 0&&M(z,Q)?(N=F,z):(N=F,L=Q)}var P=!1,N,L,B=g===void 0?null:g;return[function(){return x(v())},B===null?void 0:function(){return x(B())}]},[v,g,S,M]);var y=l(p,A[0],A[1]);return h(function(){C.hasValue=!0,C.value=y},[y]),m(y),y},Ch}var D_;function YA(){return D_||(D_=1,Rh.exports=qA()),Rh.exports}var a1=YA();export{n1 as A,Yo as B,we as C,e1 as D,t1 as M,yi as P,jA as R,$A as S,i1 as W,QA as _,w_ as a,Vo as b,JA as c,KA as d,PS as e,ga as f,vS as g,sv as h,ZA as j,bS as r,a1 as w};
