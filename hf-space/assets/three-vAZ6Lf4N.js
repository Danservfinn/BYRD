function jS(o,e){for(var i=0;i<e.length;i++){const r=e[i];if(typeof r!="string"&&!Array.isArray(r)){for(const l in r)if(l!=="default"&&!(l in o)){const c=Object.getOwnPropertyDescriptor(r,l);c&&Object.defineProperty(o,l,c.get?c:{enumerable:!0,get:()=>r[l]})}}}return Object.freeze(Object.defineProperty(o,Symbol.toStringTag,{value:"Module"}))}function ZS(o){return o&&o.__esModule&&Object.prototype.hasOwnProperty.call(o,"default")?o.default:o}var Df={exports:{}},go={};var Sg;function KS(){if(Sg)return go;Sg=1;var o=Symbol.for("react.transitional.element"),e=Symbol.for("react.fragment");function i(r,l,c){var d=null;if(c!==void 0&&(d=""+c),l.key!==void 0&&(d=""+l.key),"key"in l){c={};for(var h in l)h!=="key"&&(c[h]=l[h])}else c=l;return l=c.ref,{$$typeof:o,type:r,key:d,ref:l!==void 0?l:null,props:c}}return go.Fragment=e,go.jsx=i,go.jsxs=i,go}var xg;function QS(){return xg||(xg=1,Df.exports=KS()),Df.exports}var TA=QS(),Lf={exports:{}},te={};var Mg;function JS(){if(Mg)return te;Mg=1;var o=Symbol.for("react.transitional.element"),e=Symbol.for("react.portal"),i=Symbol.for("react.fragment"),r=Symbol.for("react.strict_mode"),l=Symbol.for("react.profiler"),c=Symbol.for("react.consumer"),d=Symbol.for("react.context"),h=Symbol.for("react.forward_ref"),m=Symbol.for("react.suspense"),p=Symbol.for("react.memo"),g=Symbol.for("react.lazy"),_=Symbol.for("react.activity"),x=Symbol.iterator;function y(L){return L===null||typeof L!="object"?null:(L=x&&L[x]||L["@@iterator"],typeof L=="function"?L:null)}var b={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},A=Object.assign,M={};function v(L,W,G){this.props=L,this.context=W,this.refs=M,this.updater=G||b}v.prototype.isReactComponent={},v.prototype.setState=function(L,W){if(typeof L!="object"&&typeof L!="function"&&L!=null)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,L,W,"setState")},v.prototype.forceUpdate=function(L){this.updater.enqueueForceUpdate(this,L,"forceUpdate")};function D(){}D.prototype=v.prototype;function T(L,W,G){this.props=L,this.context=W,this.refs=M,this.updater=G||b}var z=T.prototype=new D;z.constructor=T,A(z,v.prototype),z.isPureReactComponent=!0;var V=Array.isArray;function B(){}var O={H:null,A:null,T:null,S:null},ut=Object.prototype.hasOwnProperty;function C(L,W,G){var K=G.ref;return{$$typeof:o,type:L,key:W,ref:K!==void 0?K:null,props:G}}function N(L,W){return C(L.type,W,L.props)}function rt(L){return typeof L=="object"&&L!==null&&L.$$typeof===o}function dt(L){var W={"=":"=0",":":"=2"};return"$"+L.replace(/[=:]/g,function(G){return W[G]})}var Et=/\/+/g;function X(L,W){return typeof L=="object"&&L!==null&&L.key!=null?dt(""+L.key):W.toString(36)}function tt(L){switch(L.status){case"fulfilled":return L.value;case"rejected":throw L.reason;default:switch(typeof L.status=="string"?L.then(B,B):(L.status="pending",L.then(function(W){L.status==="pending"&&(L.status="fulfilled",L.value=W)},function(W){L.status==="pending"&&(L.status="rejected",L.reason=W)})),L.status){case"fulfilled":return L.value;case"rejected":throw L.reason}}throw L}function P(L,W,G,K,mt){var xt=typeof L;(xt==="undefined"||xt==="boolean")&&(L=null);var Mt=!1;if(L===null)Mt=!0;else switch(xt){case"bigint":case"string":case"number":Mt=!0;break;case"object":switch(L.$$typeof){case o:case e:Mt=!0;break;case g:return Mt=L._init,P(Mt(L._payload),W,G,K,mt)}}if(Mt)return mt=mt(L),Mt=K===""?"."+X(L,0):K,V(mt)?(G="",Mt!=null&&(G=Mt.replace(Et,"$&/")+"/"),P(mt,W,G,"",function(kt){return kt})):mt!=null&&(rt(mt)&&(mt=N(mt,G+(mt.key==null||L&&L.key===mt.key?"":(""+mt.key).replace(Et,"$&/")+"/")+Mt)),W.push(mt)),1;Mt=0;var It=K===""?".":K+":";if(V(L))for(var Nt=0;Nt<L.length;Nt++)K=L[Nt],xt=It+X(K,Nt),Mt+=P(K,W,G,xt,mt);else if(Nt=y(L),typeof Nt=="function")for(L=Nt.call(L),Nt=0;!(K=L.next()).done;)K=K.value,xt=It+X(K,Nt++),Mt+=P(K,W,G,xt,mt);else if(xt==="object"){if(typeof L.then=="function")return P(tt(L),W,G,K,mt);throw W=String(L),Error("Objects are not valid as a React child (found: "+(W==="[object Object]"?"object with keys {"+Object.keys(L).join(", ")+"}":W)+"). If you meant to render a collection of children, use an array instead.")}return Mt}function q(L,W,G){if(L==null)return L;var K=[],mt=0;return P(L,K,"","",function(xt){return W.call(G,xt,mt++)}),K}function J(L){if(L._status===-1){var W=L._result;W=W(),W.then(function(G){(L._status===0||L._status===-1)&&(L._status=1,L._result=G)},function(G){(L._status===0||L._status===-1)&&(L._status=2,L._result=G)}),L._status===-1&&(L._status=0,L._result=W)}if(L._status===1)return L._result.default;throw L._result}var lt=typeof reportError=="function"?reportError:function(L){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var W=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof L=="object"&&L!==null&&typeof L.message=="string"?String(L.message):String(L),error:L});if(!window.dispatchEvent(W))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",L);return}console.error(L)},ft={map:q,forEach:function(L,W,G){q(L,function(){W.apply(this,arguments)},G)},count:function(L){var W=0;return q(L,function(){W++}),W},toArray:function(L){return q(L,function(W){return W})||[]},only:function(L){if(!rt(L))throw Error("React.Children.only expected to receive a single React element child.");return L}};return te.Activity=_,te.Children=ft,te.Component=v,te.Fragment=i,te.Profiler=l,te.PureComponent=T,te.StrictMode=r,te.Suspense=m,te.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=O,te.__COMPILER_RUNTIME={__proto__:null,c:function(L){return O.H.useMemoCache(L)}},te.cache=function(L){return function(){return L.apply(null,arguments)}},te.cacheSignal=function(){return null},te.cloneElement=function(L,W,G){if(L==null)throw Error("The argument must be a React element, but you passed "+L+".");var K=A({},L.props),mt=L.key;if(W!=null)for(xt in W.key!==void 0&&(mt=""+W.key),W)!ut.call(W,xt)||xt==="key"||xt==="__self"||xt==="__source"||xt==="ref"&&W.ref===void 0||(K[xt]=W[xt]);var xt=arguments.length-2;if(xt===1)K.children=G;else if(1<xt){for(var Mt=Array(xt),It=0;It<xt;It++)Mt[It]=arguments[It+2];K.children=Mt}return C(L.type,mt,K)},te.createContext=function(L){return L={$$typeof:d,_currentValue:L,_currentValue2:L,_threadCount:0,Provider:null,Consumer:null},L.Provider=L,L.Consumer={$$typeof:c,_context:L},L},te.createElement=function(L,W,G){var K,mt={},xt=null;if(W!=null)for(K in W.key!==void 0&&(xt=""+W.key),W)ut.call(W,K)&&K!=="key"&&K!=="__self"&&K!=="__source"&&(mt[K]=W[K]);var Mt=arguments.length-2;if(Mt===1)mt.children=G;else if(1<Mt){for(var It=Array(Mt),Nt=0;Nt<Mt;Nt++)It[Nt]=arguments[Nt+2];mt.children=It}if(L&&L.defaultProps)for(K in Mt=L.defaultProps,Mt)mt[K]===void 0&&(mt[K]=Mt[K]);return C(L,xt,mt)},te.createRef=function(){return{current:null}},te.forwardRef=function(L){return{$$typeof:h,render:L}},te.isValidElement=rt,te.lazy=function(L){return{$$typeof:g,_payload:{_status:-1,_result:L},_init:J}},te.memo=function(L,W){return{$$typeof:p,type:L,compare:W===void 0?null:W}},te.startTransition=function(L){var W=O.T,G={};O.T=G;try{var K=L(),mt=O.S;mt!==null&&mt(G,K),typeof K=="object"&&K!==null&&typeof K.then=="function"&&K.then(B,lt)}catch(xt){lt(xt)}finally{W!==null&&G.types!==null&&(W.types=G.types),O.T=W}},te.unstable_useCacheRefresh=function(){return O.H.useCacheRefresh()},te.use=function(L){return O.H.use(L)},te.useActionState=function(L,W,G){return O.H.useActionState(L,W,G)},te.useCallback=function(L,W){return O.H.useCallback(L,W)},te.useContext=function(L){return O.H.useContext(L)},te.useDebugValue=function(){},te.useDeferredValue=function(L,W){return O.H.useDeferredValue(L,W)},te.useEffect=function(L,W){return O.H.useEffect(L,W)},te.useEffectEvent=function(L){return O.H.useEffectEvent(L)},te.useId=function(){return O.H.useId()},te.useImperativeHandle=function(L,W,G){return O.H.useImperativeHandle(L,W,G)},te.useInsertionEffect=function(L,W){return O.H.useInsertionEffect(L,W)},te.useLayoutEffect=function(L,W){return O.H.useLayoutEffect(L,W)},te.useMemo=function(L,W){return O.H.useMemo(L,W)},te.useOptimistic=function(L,W){return O.H.useOptimistic(L,W)},te.useReducer=function(L,W,G){return O.H.useReducer(L,W,G)},te.useRef=function(L){return O.H.useRef(L)},te.useState=function(L){return O.H.useState(L)},te.useSyncExternalStore=function(L,W,G){return O.H.useSyncExternalStore(L,W,G)},te.useTransition=function(){return O.H.useTransition()},te.version="19.2.3",te}var yg;function Co(){return yg||(yg=1,Lf.exports=JS()),Lf.exports}var rv=Co();const To=ZS(rv),bA=jS({__proto__:null,default:To},[rv]);var Uf={exports:{}},_o={},Nf={exports:{}},Of={};var Eg;function $S(){return Eg||(Eg=1,(function(o){function e(P,q){var J=P.length;P.push(q);t:for(;0<J;){var lt=J-1>>>1,ft=P[lt];if(0<l(ft,q))P[lt]=q,P[J]=ft,J=lt;else break t}}function i(P){return P.length===0?null:P[0]}function r(P){if(P.length===0)return null;var q=P[0],J=P.pop();if(J!==q){P[0]=J;t:for(var lt=0,ft=P.length,L=ft>>>1;lt<L;){var W=2*(lt+1)-1,G=P[W],K=W+1,mt=P[K];if(0>l(G,J))K<ft&&0>l(mt,G)?(P[lt]=mt,P[K]=J,lt=K):(P[lt]=G,P[W]=J,lt=W);else if(K<ft&&0>l(mt,J))P[lt]=mt,P[K]=J,lt=K;else break t}}return q}function l(P,q){var J=P.sortIndex-q.sortIndex;return J!==0?J:P.id-q.id}if(o.unstable_now=void 0,typeof performance=="object"&&typeof performance.now=="function"){var c=performance;o.unstable_now=function(){return c.now()}}else{var d=Date,h=d.now();o.unstable_now=function(){return d.now()-h}}var m=[],p=[],g=1,_=null,x=3,y=!1,b=!1,A=!1,M=!1,v=typeof setTimeout=="function"?setTimeout:null,D=typeof clearTimeout=="function"?clearTimeout:null,T=typeof setImmediate<"u"?setImmediate:null;function z(P){for(var q=i(p);q!==null;){if(q.callback===null)r(p);else if(q.startTime<=P)r(p),q.sortIndex=q.expirationTime,e(m,q);else break;q=i(p)}}function V(P){if(A=!1,z(P),!b)if(i(m)!==null)b=!0,B||(B=!0,dt());else{var q=i(p);q!==null&&tt(V,q.startTime-P)}}var B=!1,O=-1,ut=5,C=-1;function N(){return M?!0:!(o.unstable_now()-C<ut)}function rt(){if(M=!1,B){var P=o.unstable_now();C=P;var q=!0;try{t:{b=!1,A&&(A=!1,D(O),O=-1),y=!0;var J=x;try{e:{for(z(P),_=i(m);_!==null&&!(_.expirationTime>P&&N());){var lt=_.callback;if(typeof lt=="function"){_.callback=null,x=_.priorityLevel;var ft=lt(_.expirationTime<=P);if(P=o.unstable_now(),typeof ft=="function"){_.callback=ft,z(P),q=!0;break e}_===i(m)&&r(m),z(P)}else r(m);_=i(m)}if(_!==null)q=!0;else{var L=i(p);L!==null&&tt(V,L.startTime-P),q=!1}}break t}finally{_=null,x=J,y=!1}q=void 0}}finally{q?dt():B=!1}}}var dt;if(typeof T=="function")dt=function(){T(rt)};else if(typeof MessageChannel<"u"){var Et=new MessageChannel,X=Et.port2;Et.port1.onmessage=rt,dt=function(){X.postMessage(null)}}else dt=function(){v(rt,0)};function tt(P,q){O=v(function(){P(o.unstable_now())},q)}o.unstable_IdlePriority=5,o.unstable_ImmediatePriority=1,o.unstable_LowPriority=4,o.unstable_NormalPriority=3,o.unstable_Profiling=null,o.unstable_UserBlockingPriority=2,o.unstable_cancelCallback=function(P){P.callback=null},o.unstable_forceFrameRate=function(P){0>P||125<P?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):ut=0<P?Math.floor(1e3/P):5},o.unstable_getCurrentPriorityLevel=function(){return x},o.unstable_next=function(P){switch(x){case 1:case 2:case 3:var q=3;break;default:q=x}var J=x;x=q;try{return P()}finally{x=J}},o.unstable_requestPaint=function(){M=!0},o.unstable_runWithPriority=function(P,q){switch(P){case 1:case 2:case 3:case 4:case 5:break;default:P=3}var J=x;x=P;try{return q()}finally{x=J}},o.unstable_scheduleCallback=function(P,q,J){var lt=o.unstable_now();switch(typeof J=="object"&&J!==null?(J=J.delay,J=typeof J=="number"&&0<J?lt+J:lt):J=lt,P){case 1:var ft=-1;break;case 2:ft=250;break;case 5:ft=1073741823;break;case 4:ft=1e4;break;default:ft=5e3}return ft=J+ft,P={id:g++,callback:q,priorityLevel:P,startTime:J,expirationTime:ft,sortIndex:-1},J>lt?(P.sortIndex=J,e(p,P),i(m)===null&&P===i(p)&&(A?(D(O),O=-1):A=!0,tt(V,J-lt))):(P.sortIndex=ft,e(m,P),b||y||(b=!0,B||(B=!0,dt()))),P},o.unstable_shouldYield=N,o.unstable_wrapCallback=function(P){var q=x;return function(){var J=x;x=q;try{return P.apply(this,arguments)}finally{x=J}}}})(Of)),Of}var Tg;function tx(){return Tg||(Tg=1,Nf.exports=$S()),Nf.exports}var zf={exports:{}},Mn={};var bg;function ex(){if(bg)return Mn;bg=1;var o=Co();function e(m){var p="https://react.dev/errors/"+m;if(1<arguments.length){p+="?args[]="+encodeURIComponent(arguments[1]);for(var g=2;g<arguments.length;g++)p+="&args[]="+encodeURIComponent(arguments[g])}return"Minified React error #"+m+"; visit "+p+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function i(){}var r={d:{f:i,r:function(){throw Error(e(522))},D:i,C:i,L:i,m:i,X:i,S:i,M:i},p:0,findDOMNode:null},l=Symbol.for("react.portal");function c(m,p,g){var _=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:l,key:_==null?null:""+_,children:m,containerInfo:p,implementation:g}}var d=o.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function h(m,p){if(m==="font")return"";if(typeof p=="string")return p==="use-credentials"?p:""}return Mn.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=r,Mn.createPortal=function(m,p){var g=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!p||p.nodeType!==1&&p.nodeType!==9&&p.nodeType!==11)throw Error(e(299));return c(m,p,null,g)},Mn.flushSync=function(m){var p=d.T,g=r.p;try{if(d.T=null,r.p=2,m)return m()}finally{d.T=p,r.p=g,r.d.f()}},Mn.preconnect=function(m,p){typeof m=="string"&&(p?(p=p.crossOrigin,p=typeof p=="string"?p==="use-credentials"?p:"":void 0):p=null,r.d.C(m,p))},Mn.prefetchDNS=function(m){typeof m=="string"&&r.d.D(m)},Mn.preinit=function(m,p){if(typeof m=="string"&&p&&typeof p.as=="string"){var g=p.as,_=h(g,p.crossOrigin),x=typeof p.integrity=="string"?p.integrity:void 0,y=typeof p.fetchPriority=="string"?p.fetchPriority:void 0;g==="style"?r.d.S(m,typeof p.precedence=="string"?p.precedence:void 0,{crossOrigin:_,integrity:x,fetchPriority:y}):g==="script"&&r.d.X(m,{crossOrigin:_,integrity:x,fetchPriority:y,nonce:typeof p.nonce=="string"?p.nonce:void 0})}},Mn.preinitModule=function(m,p){if(typeof m=="string")if(typeof p=="object"&&p!==null){if(p.as==null||p.as==="script"){var g=h(p.as,p.crossOrigin);r.d.M(m,{crossOrigin:g,integrity:typeof p.integrity=="string"?p.integrity:void 0,nonce:typeof p.nonce=="string"?p.nonce:void 0})}}else p==null&&r.d.M(m)},Mn.preload=function(m,p){if(typeof m=="string"&&typeof p=="object"&&p!==null&&typeof p.as=="string"){var g=p.as,_=h(g,p.crossOrigin);r.d.L(m,g,{crossOrigin:_,integrity:typeof p.integrity=="string"?p.integrity:void 0,nonce:typeof p.nonce=="string"?p.nonce:void 0,type:typeof p.type=="string"?p.type:void 0,fetchPriority:typeof p.fetchPriority=="string"?p.fetchPriority:void 0,referrerPolicy:typeof p.referrerPolicy=="string"?p.referrerPolicy:void 0,imageSrcSet:typeof p.imageSrcSet=="string"?p.imageSrcSet:void 0,imageSizes:typeof p.imageSizes=="string"?p.imageSizes:void 0,media:typeof p.media=="string"?p.media:void 0})}},Mn.preloadModule=function(m,p){if(typeof m=="string")if(p){var g=h(p.as,p.crossOrigin);r.d.m(m,{as:typeof p.as=="string"&&p.as!=="script"?p.as:void 0,crossOrigin:g,integrity:typeof p.integrity=="string"?p.integrity:void 0})}else r.d.m(m)},Mn.requestFormReset=function(m){r.d.r(m)},Mn.unstable_batchedUpdates=function(m,p){return m(p)},Mn.useFormState=function(m,p,g){return d.H.useFormState(m,p,g)},Mn.useFormStatus=function(){return d.H.useHostTransitionStatus()},Mn.version="19.2.3",Mn}var Ag;function nx(){if(Ag)return zf.exports;Ag=1;function o(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(o)}catch(e){console.error(e)}}return o(),zf.exports=ex(),zf.exports}var Rg;function ix(){if(Rg)return _o;Rg=1;var o=tx(),e=Co(),i=nx();function r(t){var n="https://react.dev/errors/"+t;if(1<arguments.length){n+="?args[]="+encodeURIComponent(arguments[1]);for(var a=2;a<arguments.length;a++)n+="&args[]="+encodeURIComponent(arguments[a])}return"Minified React error #"+t+"; visit "+n+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function l(t){return!(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11)}function c(t){var n=t,a=t;if(t.alternate)for(;n.return;)n=n.return;else{t=n;do n=t,(n.flags&4098)!==0&&(a=n.return),t=n.return;while(t)}return n.tag===3?a:null}function d(t){if(t.tag===13){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function h(t){if(t.tag===31){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function m(t){if(c(t)!==t)throw Error(r(188))}function p(t){var n=t.alternate;if(!n){if(n=c(t),n===null)throw Error(r(188));return n!==t?null:t}for(var a=t,s=n;;){var u=a.return;if(u===null)break;var f=u.alternate;if(f===null){if(s=u.return,s!==null){a=s;continue}break}if(u.child===f.child){for(f=u.child;f;){if(f===a)return m(u),t;if(f===s)return m(u),n;f=f.sibling}throw Error(r(188))}if(a.return!==s.return)a=u,s=f;else{for(var S=!1,E=u.child;E;){if(E===a){S=!0,a=u,s=f;break}if(E===s){S=!0,s=u,a=f;break}E=E.sibling}if(!S){for(E=f.child;E;){if(E===a){S=!0,a=f,s=u;break}if(E===s){S=!0,s=f,a=u;break}E=E.sibling}if(!S)throw Error(r(189))}}if(a.alternate!==s)throw Error(r(190))}if(a.tag!==3)throw Error(r(188));return a.stateNode.current===a?t:n}function g(t){var n=t.tag;if(n===5||n===26||n===27||n===6)return t;for(t=t.child;t!==null;){if(n=g(t),n!==null)return n;t=t.sibling}return null}var _=Object.assign,x=Symbol.for("react.element"),y=Symbol.for("react.transitional.element"),b=Symbol.for("react.portal"),A=Symbol.for("react.fragment"),M=Symbol.for("react.strict_mode"),v=Symbol.for("react.profiler"),D=Symbol.for("react.consumer"),T=Symbol.for("react.context"),z=Symbol.for("react.forward_ref"),V=Symbol.for("react.suspense"),B=Symbol.for("react.suspense_list"),O=Symbol.for("react.memo"),ut=Symbol.for("react.lazy"),C=Symbol.for("react.activity"),N=Symbol.for("react.memo_cache_sentinel"),rt=Symbol.iterator;function dt(t){return t===null||typeof t!="object"?null:(t=rt&&t[rt]||t["@@iterator"],typeof t=="function"?t:null)}var Et=Symbol.for("react.client.reference");function X(t){if(t==null)return null;if(typeof t=="function")return t.$$typeof===Et?null:t.displayName||t.name||null;if(typeof t=="string")return t;switch(t){case A:return"Fragment";case v:return"Profiler";case M:return"StrictMode";case V:return"Suspense";case B:return"SuspenseList";case C:return"Activity"}if(typeof t=="object")switch(t.$$typeof){case b:return"Portal";case T:return t.displayName||"Context";case D:return(t._context.displayName||"Context")+".Consumer";case z:var n=t.render;return t=t.displayName,t||(t=n.displayName||n.name||"",t=t!==""?"ForwardRef("+t+")":"ForwardRef"),t;case O:return n=t.displayName||null,n!==null?n:X(t.type)||"Memo";case ut:n=t._payload,t=t._init;try{return X(t(n))}catch{}}return null}var tt=Array.isArray,P=e.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,q=i.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,J={pending:!1,data:null,method:null,action:null},lt=[],ft=-1;function L(t){return{current:t}}function W(t){0>ft||(t.current=lt[ft],lt[ft]=null,ft--)}function G(t,n){ft++,lt[ft]=t.current,t.current=n}var K=L(null),mt=L(null),xt=L(null),Mt=L(null);function It(t,n){switch(G(xt,n),G(mt,t),G(K,null),n.nodeType){case 9:case 11:t=(t=n.documentElement)&&(t=t.namespaceURI)?Vm(t):0;break;default:if(t=n.tagName,n=n.namespaceURI)n=Vm(n),t=Xm(n,t);else switch(t){case"svg":t=1;break;case"math":t=2;break;default:t=0}}W(K),G(K,t)}function Nt(){W(K),W(mt),W(xt)}function kt(t){t.memoizedState!==null&&G(Mt,t);var n=K.current,a=Xm(n,t.type);n!==a&&(G(mt,t),G(K,a))}function ue(t){mt.current===t&&(W(K),W(mt)),Mt.current===t&&(W(Mt),fo._currentValue=J)}var et,un;function Ft(t){if(et===void 0)try{throw Error()}catch(a){var n=a.stack.trim().match(/\n( *(at )?)/);et=n&&n[1]||"",un=-1<a.stack.indexOf(`
    at`)?" (<anonymous>)":-1<a.stack.indexOf("@")?"@unknown:0:0":""}return`
`+et+t+un}var Qt=!1;function Pt(t,n){if(!t||Qt)return"";Qt=!0;var a=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var s={DetermineComponentFrameRoot:function(){try{if(n){var pt=function(){throw Error()};if(Object.defineProperty(pt.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(pt,[])}catch(ot){var $=ot}Reflect.construct(t,[],pt)}else{try{pt.call()}catch(ot){$=ot}t.call(pt.prototype)}}else{try{throw Error()}catch(ot){$=ot}(pt=t())&&typeof pt.catch=="function"&&pt.catch(function(){})}}catch(ot){if(ot&&$&&typeof ot.stack=="string")return[ot.stack,$.stack]}return[null,null]}};s.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var u=Object.getOwnPropertyDescriptor(s.DetermineComponentFrameRoot,"name");u&&u.configurable&&Object.defineProperty(s.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var f=s.DetermineComponentFrameRoot(),S=f[0],E=f[1];if(S&&E){var I=S.split(`
`),Q=E.split(`
`);for(u=s=0;s<I.length&&!I[s].includes("DetermineComponentFrameRoot");)s++;for(;u<Q.length&&!Q[u].includes("DetermineComponentFrameRoot");)u++;if(s===I.length||u===Q.length)for(s=I.length-1,u=Q.length-1;1<=s&&0<=u&&I[s]!==Q[u];)u--;for(;1<=s&&0<=u;s--,u--)if(I[s]!==Q[u]){if(s!==1||u!==1)do if(s--,u--,0>u||I[s]!==Q[u]){var ct=`
`+I[s].replace(" at new "," at ");return t.displayName&&ct.includes("<anonymous>")&&(ct=ct.replace("<anonymous>",t.displayName)),ct}while(1<=s&&0<=u);break}}}finally{Qt=!1,Error.prepareStackTrace=a}return(a=t?t.displayName||t.name:"")?Ft(a):""}function Pe(t,n){switch(t.tag){case 26:case 27:case 5:return Ft(t.type);case 16:return Ft("Lazy");case 13:return t.child!==n&&n!==null?Ft("Suspense Fallback"):Ft("Suspense");case 19:return Ft("SuspenseList");case 0:case 15:return Pt(t.type,!1);case 11:return Pt(t.type.render,!1);case 1:return Pt(t.type,!0);case 31:return Ft("Activity");default:return""}}function ee(t){try{var n="",a=null;do n+=Pe(t,a),a=t,t=t.return;while(t);return n}catch(s){return`
Error generating stack: `+s.message+`
`+s.stack}}var U=Object.prototype.hasOwnProperty,R=o.unstable_scheduleCallback,it=o.unstable_cancelCallback,St=o.unstable_shouldYield,vt=o.unstable_requestPaint,gt=o.unstable_now,Ht=o.unstable_getCurrentPriorityLevel,Rt=o.unstable_ImmediatePriority,Ut=o.unstable_UserBlockingPriority,qt=o.unstable_NormalPriority,ie=o.unstable_LowPriority,_t=o.unstable_IdlePriority,ye=o.log,le=o.unstable_setDisableYieldValue,Kt=null,Dt=null;function wt(t){if(typeof ye=="function"&&le(t),Dt&&typeof Dt.setStrictMode=="function")try{Dt.setStrictMode(Kt,t)}catch{}}var Xt=Math.clz32?Math.clz32:re,Se=Math.log,He=Math.LN2;function re(t){return t>>>=0,t===0?32:31-(Se(t)/He|0)|0}var yt=256,F=262144,At=4194304;function Tt(t){var n=t&42;if(n!==0)return n;switch(t&-t){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return t&261888;case 262144:case 524288:case 1048576:case 2097152:return t&3932160;case 4194304:case 8388608:case 16777216:case 33554432:return t&62914560;case 67108864:return 67108864;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 0;default:return t}}function jt(t,n,a){var s=t.pendingLanes;if(s===0)return 0;var u=0,f=t.suspendedLanes,S=t.pingedLanes;t=t.warmLanes;var E=s&134217727;return E!==0?(s=E&~f,s!==0?u=Tt(s):(S&=E,S!==0?u=Tt(S):a||(a=E&~t,a!==0&&(u=Tt(a))))):(E=s&~f,E!==0?u=Tt(E):S!==0?u=Tt(S):a||(a=s&~t,a!==0&&(u=Tt(a)))),u===0?0:n!==0&&n!==u&&(n&f)===0&&(f=u&-u,a=n&-n,f>=a||f===32&&(a&4194048)!==0)?n:u}function Gt(t,n){return(t.pendingLanes&~(t.suspendedLanes&~t.pingedLanes)&n)===0}function Re(t,n){switch(t){case 1:case 2:case 4:case 8:case 64:return n+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return n+5e3;case 4194304:case 8388608:case 16777216:case 33554432:return-1;case 67108864:case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function Ee(){var t=At;return At<<=1,(At&62914560)===0&&(At=4194304),t}function Xe(t){for(var n=[],a=0;31>a;a++)n.push(t);return n}function qe(t,n){t.pendingLanes|=n,n!==268435456&&(t.suspendedLanes=0,t.pingedLanes=0,t.warmLanes=0)}function Ce(t,n,a,s,u,f){var S=t.pendingLanes;t.pendingLanes=a,t.suspendedLanes=0,t.pingedLanes=0,t.warmLanes=0,t.expiredLanes&=a,t.entangledLanes&=a,t.errorRecoveryDisabledLanes&=a,t.shellSuspendCounter=0;var E=t.entanglements,I=t.expirationTimes,Q=t.hiddenUpdates;for(a=S&~a;0<a;){var ct=31-Xt(a),pt=1<<ct;E[ct]=0,I[ct]=-1;var $=Q[ct];if($!==null)for(Q[ct]=null,ct=0;ct<$.length;ct++){var ot=$[ct];ot!==null&&(ot.lane&=-536870913)}a&=~pt}s!==0&&cn(t,s,0),f!==0&&u===0&&t.tag!==0&&(t.suspendedLanes|=f&~(S&~n))}function cn(t,n,a){t.pendingLanes|=n,t.suspendedLanes&=~n;var s=31-Xt(n);t.entangledLanes|=n,t.entanglements[s]=t.entanglements[s]|1073741824|a&261930}function Hn(t,n){var a=t.entangledLanes|=n;for(t=t.entanglements;a;){var s=31-Xt(a),u=1<<s;u&n|t[s]&n&&(t[s]|=n),a&=~u}}function Ms(t,n){var a=n&-n;return a=(a&42)!==0?1:ys(a),(a&(t.suspendedLanes|n))!==0?0:a}function ys(t){switch(t){case 2:t=1;break;case 8:t=4;break;case 32:t=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:t=128;break;case 268435456:t=134217728;break;default:t=0}return t}function ta(t){return t&=-t,2<t?8<t?(t&134217727)!==0?32:268435456:8:2}function Es(){var t=q.p;return t!==0?t:(t=window.event,t===void 0?32:hg(t.type))}function Ha(t,n){var a=q.p;try{return q.p=t,n()}finally{q.p=a}}var ci=Math.random().toString(36).slice(2),Ze="__reactFiber$"+ci,Sn="__reactProps$"+ci,ea="__reactContainer$"+ci,Ts="__reactEvents$"+ci,w="__reactListeners$"+ci,j="__reactHandles$"+ci,at="__reactResources$"+ci,st="__reactMarker$"+ci;function nt(t){delete t[Ze],delete t[Sn],delete t[Ts],delete t[w],delete t[j]}function Ct(t){var n=t[Ze];if(n)return n;for(var a=t.parentNode;a;){if(n=a[ea]||a[Ze]){if(a=n.alternate,n.child!==null||a!==null&&a.child!==null)for(t=Km(t);t!==null;){if(a=t[Ze])return a;t=Km(t)}return n}t=a,a=t.parentNode}return null}function Ot(t){if(t=t[Ze]||t[ea]){var n=t.tag;if(n===5||n===6||n===13||n===31||n===26||n===27||n===3)return t}return null}function Wt(t){var n=t.tag;if(n===5||n===26||n===27||n===6)return t.stateNode;throw Error(r(33))}function Yt(t){var n=t[at];return n||(n=t[at]={hoistableStyles:new Map,hoistableScripts:new Map}),n}function Bt(t){t[st]=!0}var Jt=new Set,$t={};function Te(t,n){Ke(t,n),Ke(t+"Capture",n)}function Ke(t,n){for($t[t]=n,t=0;t<n.length;t++)Jt.add(n[t])}var Qe=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),Qn={},ze={};function se(t){return U.call(ze,t)?!0:U.call(Qn,t)?!1:Qe.test(t)?ze[t]=!0:(Qn[t]=!0,!1)}function na(t,n,a){if(se(n))if(a===null)t.removeAttribute(n);else{switch(typeof a){case"undefined":case"function":case"symbol":t.removeAttribute(n);return;case"boolean":var s=n.toLowerCase().slice(0,5);if(s!=="data-"&&s!=="aria-"){t.removeAttribute(n);return}}t.setAttribute(n,""+a)}}function Ne(t,n,a){if(a===null)t.removeAttribute(n);else{switch(typeof a){case"undefined":case"function":case"symbol":case"boolean":t.removeAttribute(n);return}t.setAttribute(n,""+a)}}function dn(t,n,a,s){if(s===null)t.removeAttribute(a);else{switch(typeof s){case"undefined":case"function":case"symbol":case"boolean":t.removeAttribute(a);return}t.setAttributeNS(n,a,""+s)}}function An(t){switch(typeof t){case"bigint":case"boolean":case"number":case"string":case"undefined":return t;case"object":return t;default:return""}}function ia(t){var n=t.type;return(t=t.nodeName)&&t.toLowerCase()==="input"&&(n==="checkbox"||n==="radio")}function bs(t,n,a){var s=Object.getOwnPropertyDescriptor(t.constructor.prototype,n);if(!t.hasOwnProperty(n)&&typeof s<"u"&&typeof s.get=="function"&&typeof s.set=="function"){var u=s.get,f=s.set;return Object.defineProperty(t,n,{configurable:!0,get:function(){return u.call(this)},set:function(S){a=""+S,f.call(this,S)}}),Object.defineProperty(t,n,{enumerable:s.enumerable}),{getValue:function(){return a},setValue:function(S){a=""+S},stopTracking:function(){t._valueTracker=null,delete t[n]}}}}function Je(t){if(!t._valueTracker){var n=ia(t)?"checked":"value";t._valueTracker=bs(t,n,""+t[n])}}function xi(t){if(!t)return!1;var n=t._valueTracker;if(!n)return!0;var a=n.getValue(),s="";return t&&(s=ia(t)?t.checked?"true":"false":t.value),t=s,t!==a?(n.setValue(t),!0):!1}function aa(t){if(t=t||(typeof document<"u"?document:void 0),typeof t>"u")return null;try{return t.activeElement||t.body}catch{return t.body}}var Ln=/[\n"\\]/g;function xn(t){return t.replace(Ln,function(n){return"\\"+n.charCodeAt(0).toString(16)+" "})}function As(t,n,a,s,u,f,S,E){t.name="",S!=null&&typeof S!="function"&&typeof S!="symbol"&&typeof S!="boolean"?t.type=S:t.removeAttribute("type"),n!=null?S==="number"?(n===0&&t.value===""||t.value!=n)&&(t.value=""+An(n)):t.value!==""+An(n)&&(t.value=""+An(n)):S!=="submit"&&S!=="reset"||t.removeAttribute("value"),n!=null?Tu(t,S,An(n)):a!=null?Tu(t,S,An(a)):s!=null&&t.removeAttribute("value"),u==null&&f!=null&&(t.defaultChecked=!!f),u!=null&&(t.checked=u&&typeof u!="function"&&typeof u!="symbol"),E!=null&&typeof E!="function"&&typeof E!="symbol"&&typeof E!="boolean"?t.name=""+An(E):t.removeAttribute("name")}function Rs(t,n,a,s,u,f,S,E){if(f!=null&&typeof f!="function"&&typeof f!="symbol"&&typeof f!="boolean"&&(t.type=f),n!=null||a!=null){if(!(f!=="submit"&&f!=="reset"||n!=null)){Je(t);return}a=a!=null?""+An(a):"",n=n!=null?""+An(n):a,E||n===t.value||(t.value=n),t.defaultValue=n}s=s??u,s=typeof s!="function"&&typeof s!="symbol"&&!!s,t.checked=E?t.checked:!!s,t.defaultChecked=!!s,S!=null&&typeof S!="function"&&typeof S!="symbol"&&typeof S!="boolean"&&(t.name=S),Je(t)}function Tu(t,n,a){n==="number"&&aa(t.ownerDocument)===t||t.defaultValue===""+a||(t.defaultValue=""+a)}function gr(t,n,a,s){if(t=t.options,n){n={};for(var u=0;u<a.length;u++)n["$"+a[u]]=!0;for(a=0;a<t.length;a++)u=n.hasOwnProperty("$"+t[a].value),t[a].selected!==u&&(t[a].selected=u),u&&s&&(t[a].defaultSelected=!0)}else{for(a=""+An(a),n=null,u=0;u<t.length;u++){if(t[u].value===a){t[u].selected=!0,s&&(t[u].defaultSelected=!0);return}n!==null||t[u].disabled||(n=t[u])}n!==null&&(n.selected=!0)}}function Bh(t,n,a){if(n!=null&&(n=""+An(n),n!==t.value&&(t.value=n),a==null)){t.defaultValue!==n&&(t.defaultValue=n);return}t.defaultValue=a!=null?""+An(a):""}function Ih(t,n,a,s){if(n==null){if(s!=null){if(a!=null)throw Error(r(92));if(tt(s)){if(1<s.length)throw Error(r(93));s=s[0]}a=s}a==null&&(a=""),n=a}a=An(n),t.defaultValue=a,s=t.textContent,s===a&&s!==""&&s!==null&&(t.value=s),Je(t)}function _r(t,n){if(n){var a=t.firstChild;if(a&&a===t.lastChild&&a.nodeType===3){a.nodeValue=n;return}}t.textContent=n}var Xv=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function Fh(t,n,a){var s=n.indexOf("--")===0;a==null||typeof a=="boolean"||a===""?s?t.setProperty(n,""):n==="float"?t.cssFloat="":t[n]="":s?t.setProperty(n,a):typeof a!="number"||a===0||Xv.has(n)?n==="float"?t.cssFloat=a:t[n]=(""+a).trim():t[n]=a+"px"}function Hh(t,n,a){if(n!=null&&typeof n!="object")throw Error(r(62));if(t=t.style,a!=null){for(var s in a)!a.hasOwnProperty(s)||n!=null&&n.hasOwnProperty(s)||(s.indexOf("--")===0?t.setProperty(s,""):s==="float"?t.cssFloat="":t[s]="");for(var u in n)s=n[u],n.hasOwnProperty(u)&&a[u]!==s&&Fh(t,u,s)}else for(var f in n)n.hasOwnProperty(f)&&Fh(t,f,n[f])}function bu(t){if(t.indexOf("-")===-1)return!1;switch(t){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var Wv=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),kv=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function Oo(t){return kv.test(""+t)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":t}function Ci(){}var Au=null;function Ru(t){return t=t.target||t.srcElement||window,t.correspondingUseElement&&(t=t.correspondingUseElement),t.nodeType===3?t.parentNode:t}var vr=null,Sr=null;function Gh(t){var n=Ot(t);if(n&&(t=n.stateNode)){var a=t[Sn]||null;t:switch(t=n.stateNode,n.type){case"input":if(As(t,a.value,a.defaultValue,a.defaultValue,a.checked,a.defaultChecked,a.type,a.name),n=a.name,a.type==="radio"&&n!=null){for(a=t;a.parentNode;)a=a.parentNode;for(a=a.querySelectorAll('input[name="'+xn(""+n)+'"][type="radio"]'),n=0;n<a.length;n++){var s=a[n];if(s!==t&&s.form===t.form){var u=s[Sn]||null;if(!u)throw Error(r(90));As(s,u.value,u.defaultValue,u.defaultValue,u.checked,u.defaultChecked,u.type,u.name)}}for(n=0;n<a.length;n++)s=a[n],s.form===t.form&&xi(s)}break t;case"textarea":Bh(t,a.value,a.defaultValue);break t;case"select":n=a.value,n!=null&&gr(t,!!a.multiple,n,!1)}}}var Cu=!1;function Vh(t,n,a){if(Cu)return t(n,a);Cu=!0;try{var s=t(n);return s}finally{if(Cu=!1,(vr!==null||Sr!==null)&&(Ml(),vr&&(n=vr,t=Sr,Sr=vr=null,Gh(n),t)))for(n=0;n<t.length;n++)Gh(t[n])}}function Cs(t,n){var a=t.stateNode;if(a===null)return null;var s=a[Sn]||null;if(s===null)return null;a=s[n];t:switch(n){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(s=!s.disabled)||(t=t.type,s=!(t==="button"||t==="input"||t==="select"||t==="textarea")),t=!s;break t;default:t=!1}if(t)return null;if(a&&typeof a!="function")throw Error(r(231,n,typeof a));return a}var wi=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),wu=!1;if(wi)try{var ws={};Object.defineProperty(ws,"passive",{get:function(){wu=!0}}),window.addEventListener("test",ws,ws),window.removeEventListener("test",ws,ws)}catch{wu=!1}var ra=null,Du=null,zo=null;function Xh(){if(zo)return zo;var t,n=Du,a=n.length,s,u="value"in ra?ra.value:ra.textContent,f=u.length;for(t=0;t<a&&n[t]===u[t];t++);var S=a-t;for(s=1;s<=S&&n[a-s]===u[f-s];s++);return zo=u.slice(t,1<s?1-s:void 0)}function Po(t){var n=t.keyCode;return"charCode"in t?(t=t.charCode,t===0&&n===13&&(t=13)):t=n,t===10&&(t=13),32<=t||t===13?t:0}function Bo(){return!0}function Wh(){return!1}function Un(t){function n(a,s,u,f,S){this._reactName=a,this._targetInst=u,this.type=s,this.nativeEvent=f,this.target=S,this.currentTarget=null;for(var E in t)t.hasOwnProperty(E)&&(a=t[E],this[E]=a?a(f):f[E]);return this.isDefaultPrevented=(f.defaultPrevented!=null?f.defaultPrevented:f.returnValue===!1)?Bo:Wh,this.isPropagationStopped=Wh,this}return _(n.prototype,{preventDefault:function(){this.defaultPrevented=!0;var a=this.nativeEvent;a&&(a.preventDefault?a.preventDefault():typeof a.returnValue!="unknown"&&(a.returnValue=!1),this.isDefaultPrevented=Bo)},stopPropagation:function(){var a=this.nativeEvent;a&&(a.stopPropagation?a.stopPropagation():typeof a.cancelBubble!="unknown"&&(a.cancelBubble=!0),this.isPropagationStopped=Bo)},persist:function(){},isPersistent:Bo}),n}var Ga={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(t){return t.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},Io=Un(Ga),Ds=_({},Ga,{view:0,detail:0}),qv=Un(Ds),Lu,Uu,Ls,Fo=_({},Ds,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:Ou,button:0,buttons:0,relatedTarget:function(t){return t.relatedTarget===void 0?t.fromElement===t.srcElement?t.toElement:t.fromElement:t.relatedTarget},movementX:function(t){return"movementX"in t?t.movementX:(t!==Ls&&(Ls&&t.type==="mousemove"?(Lu=t.screenX-Ls.screenX,Uu=t.screenY-Ls.screenY):Uu=Lu=0,Ls=t),Lu)},movementY:function(t){return"movementY"in t?t.movementY:Uu}}),kh=Un(Fo),Yv=_({},Fo,{dataTransfer:0}),jv=Un(Yv),Zv=_({},Ds,{relatedTarget:0}),Nu=Un(Zv),Kv=_({},Ga,{animationName:0,elapsedTime:0,pseudoElement:0}),Qv=Un(Kv),Jv=_({},Ga,{clipboardData:function(t){return"clipboardData"in t?t.clipboardData:window.clipboardData}}),$v=Un(Jv),t0=_({},Ga,{data:0}),qh=Un(t0),e0={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},n0={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},i0={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function a0(t){var n=this.nativeEvent;return n.getModifierState?n.getModifierState(t):(t=i0[t])?!!n[t]:!1}function Ou(){return a0}var r0=_({},Ds,{key:function(t){if(t.key){var n=e0[t.key]||t.key;if(n!=="Unidentified")return n}return t.type==="keypress"?(t=Po(t),t===13?"Enter":String.fromCharCode(t)):t.type==="keydown"||t.type==="keyup"?n0[t.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:Ou,charCode:function(t){return t.type==="keypress"?Po(t):0},keyCode:function(t){return t.type==="keydown"||t.type==="keyup"?t.keyCode:0},which:function(t){return t.type==="keypress"?Po(t):t.type==="keydown"||t.type==="keyup"?t.keyCode:0}}),s0=Un(r0),o0=_({},Fo,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),Yh=Un(o0),l0=_({},Ds,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:Ou}),u0=Un(l0),c0=_({},Ga,{propertyName:0,elapsedTime:0,pseudoElement:0}),f0=Un(c0),h0=_({},Fo,{deltaX:function(t){return"deltaX"in t?t.deltaX:"wheelDeltaX"in t?-t.wheelDeltaX:0},deltaY:function(t){return"deltaY"in t?t.deltaY:"wheelDeltaY"in t?-t.wheelDeltaY:"wheelDelta"in t?-t.wheelDelta:0},deltaZ:0,deltaMode:0}),d0=Un(h0),p0=_({},Ga,{newState:0,oldState:0}),m0=Un(p0),g0=[9,13,27,32],zu=wi&&"CompositionEvent"in window,Us=null;wi&&"documentMode"in document&&(Us=document.documentMode);var _0=wi&&"TextEvent"in window&&!Us,jh=wi&&(!zu||Us&&8<Us&&11>=Us),Zh=" ",Kh=!1;function Qh(t,n){switch(t){case"keyup":return g0.indexOf(n.keyCode)!==-1;case"keydown":return n.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function Jh(t){return t=t.detail,typeof t=="object"&&"data"in t?t.data:null}var xr=!1;function v0(t,n){switch(t){case"compositionend":return Jh(n);case"keypress":return n.which!==32?null:(Kh=!0,Zh);case"textInput":return t=n.data,t===Zh&&Kh?null:t;default:return null}}function S0(t,n){if(xr)return t==="compositionend"||!zu&&Qh(t,n)?(t=Xh(),zo=Du=ra=null,xr=!1,t):null;switch(t){case"paste":return null;case"keypress":if(!(n.ctrlKey||n.altKey||n.metaKey)||n.ctrlKey&&n.altKey){if(n.char&&1<n.char.length)return n.char;if(n.which)return String.fromCharCode(n.which)}return null;case"compositionend":return jh&&n.locale!=="ko"?null:n.data;default:return null}}var x0={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function $h(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n==="input"?!!x0[t.type]:n==="textarea"}function td(t,n,a,s){vr?Sr?Sr.push(s):Sr=[s]:vr=s,n=Cl(n,"onChange"),0<n.length&&(a=new Io("onChange","change",null,a,s),t.push({event:a,listeners:n}))}var Ns=null,Os=null;function M0(t){Pm(t,0)}function Ho(t){var n=Wt(t);if(xi(n))return t}function ed(t,n){if(t==="change")return n}var nd=!1;if(wi){var Pu;if(wi){var Bu="oninput"in document;if(!Bu){var id=document.createElement("div");id.setAttribute("oninput","return;"),Bu=typeof id.oninput=="function"}Pu=Bu}else Pu=!1;nd=Pu&&(!document.documentMode||9<document.documentMode)}function ad(){Ns&&(Ns.detachEvent("onpropertychange",rd),Os=Ns=null)}function rd(t){if(t.propertyName==="value"&&Ho(Os)){var n=[];td(n,Os,t,Ru(t)),Vh(M0,n)}}function y0(t,n,a){t==="focusin"?(ad(),Ns=n,Os=a,Ns.attachEvent("onpropertychange",rd)):t==="focusout"&&ad()}function E0(t){if(t==="selectionchange"||t==="keyup"||t==="keydown")return Ho(Os)}function T0(t,n){if(t==="click")return Ho(n)}function b0(t,n){if(t==="input"||t==="change")return Ho(n)}function A0(t,n){return t===n&&(t!==0||1/t===1/n)||t!==t&&n!==n}var Gn=typeof Object.is=="function"?Object.is:A0;function zs(t,n){if(Gn(t,n))return!0;if(typeof t!="object"||t===null||typeof n!="object"||n===null)return!1;var a=Object.keys(t),s=Object.keys(n);if(a.length!==s.length)return!1;for(s=0;s<a.length;s++){var u=a[s];if(!U.call(n,u)||!Gn(t[u],n[u]))return!1}return!0}function sd(t){for(;t&&t.firstChild;)t=t.firstChild;return t}function od(t,n){var a=sd(t);t=0;for(var s;a;){if(a.nodeType===3){if(s=t+a.textContent.length,t<=n&&s>=n)return{node:a,offset:n-t};t=s}t:{for(;a;){if(a.nextSibling){a=a.nextSibling;break t}a=a.parentNode}a=void 0}a=sd(a)}}function ld(t,n){return t&&n?t===n?!0:t&&t.nodeType===3?!1:n&&n.nodeType===3?ld(t,n.parentNode):"contains"in t?t.contains(n):t.compareDocumentPosition?!!(t.compareDocumentPosition(n)&16):!1:!1}function ud(t){t=t!=null&&t.ownerDocument!=null&&t.ownerDocument.defaultView!=null?t.ownerDocument.defaultView:window;for(var n=aa(t.document);n instanceof t.HTMLIFrameElement;){try{var a=typeof n.contentWindow.location.href=="string"}catch{a=!1}if(a)t=n.contentWindow;else break;n=aa(t.document)}return n}function Iu(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n&&(n==="input"&&(t.type==="text"||t.type==="search"||t.type==="tel"||t.type==="url"||t.type==="password")||n==="textarea"||t.contentEditable==="true")}var R0=wi&&"documentMode"in document&&11>=document.documentMode,Mr=null,Fu=null,Ps=null,Hu=!1;function cd(t,n,a){var s=a.window===a?a.document:a.nodeType===9?a:a.ownerDocument;Hu||Mr==null||Mr!==aa(s)||(s=Mr,"selectionStart"in s&&Iu(s)?s={start:s.selectionStart,end:s.selectionEnd}:(s=(s.ownerDocument&&s.ownerDocument.defaultView||window).getSelection(),s={anchorNode:s.anchorNode,anchorOffset:s.anchorOffset,focusNode:s.focusNode,focusOffset:s.focusOffset}),Ps&&zs(Ps,s)||(Ps=s,s=Cl(Fu,"onSelect"),0<s.length&&(n=new Io("onSelect","select",null,n,a),t.push({event:n,listeners:s}),n.target=Mr)))}function Va(t,n){var a={};return a[t.toLowerCase()]=n.toLowerCase(),a["Webkit"+t]="webkit"+n,a["Moz"+t]="moz"+n,a}var yr={animationend:Va("Animation","AnimationEnd"),animationiteration:Va("Animation","AnimationIteration"),animationstart:Va("Animation","AnimationStart"),transitionrun:Va("Transition","TransitionRun"),transitionstart:Va("Transition","TransitionStart"),transitioncancel:Va("Transition","TransitionCancel"),transitionend:Va("Transition","TransitionEnd")},Gu={},fd={};wi&&(fd=document.createElement("div").style,"AnimationEvent"in window||(delete yr.animationend.animation,delete yr.animationiteration.animation,delete yr.animationstart.animation),"TransitionEvent"in window||delete yr.transitionend.transition);function Xa(t){if(Gu[t])return Gu[t];if(!yr[t])return t;var n=yr[t],a;for(a in n)if(n.hasOwnProperty(a)&&a in fd)return Gu[t]=n[a];return t}var hd=Xa("animationend"),dd=Xa("animationiteration"),pd=Xa("animationstart"),C0=Xa("transitionrun"),w0=Xa("transitionstart"),D0=Xa("transitioncancel"),md=Xa("transitionend"),gd=new Map,Vu="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");Vu.push("scrollEnd");function fi(t,n){gd.set(t,n),Te(n,[t])}var Go=typeof reportError=="function"?reportError:function(t){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var n=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof t=="object"&&t!==null&&typeof t.message=="string"?String(t.message):String(t),error:t});if(!window.dispatchEvent(n))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",t);return}console.error(t)},Jn=[],Er=0,Xu=0;function Vo(){for(var t=Er,n=Xu=Er=0;n<t;){var a=Jn[n];Jn[n++]=null;var s=Jn[n];Jn[n++]=null;var u=Jn[n];Jn[n++]=null;var f=Jn[n];if(Jn[n++]=null,s!==null&&u!==null){var S=s.pending;S===null?u.next=u:(u.next=S.next,S.next=u),s.pending=u}f!==0&&_d(a,u,f)}}function Xo(t,n,a,s){Jn[Er++]=t,Jn[Er++]=n,Jn[Er++]=a,Jn[Er++]=s,Xu|=s,t.lanes|=s,t=t.alternate,t!==null&&(t.lanes|=s)}function Wu(t,n,a,s){return Xo(t,n,a,s),Wo(t)}function Wa(t,n){return Xo(t,null,null,n),Wo(t)}function _d(t,n,a){t.lanes|=a;var s=t.alternate;s!==null&&(s.lanes|=a);for(var u=!1,f=t.return;f!==null;)f.childLanes|=a,s=f.alternate,s!==null&&(s.childLanes|=a),f.tag===22&&(t=f.stateNode,t===null||t._visibility&1||(u=!0)),t=f,f=f.return;return t.tag===3?(f=t.stateNode,u&&n!==null&&(u=31-Xt(a),t=f.hiddenUpdates,s=t[u],s===null?t[u]=[n]:s.push(n),n.lane=a|536870912),f):null}function Wo(t){if(50<ao)throw ao=0,$c=null,Error(r(185));for(var n=t.return;n!==null;)t=n,n=t.return;return t.tag===3?t.stateNode:null}var Tr={};function L0(t,n,a,s){this.tag=t,this.key=a,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=n,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=s,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function Vn(t,n,a,s){return new L0(t,n,a,s)}function ku(t){return t=t.prototype,!(!t||!t.isReactComponent)}function Di(t,n){var a=t.alternate;return a===null?(a=Vn(t.tag,n,t.key,t.mode),a.elementType=t.elementType,a.type=t.type,a.stateNode=t.stateNode,a.alternate=t,t.alternate=a):(a.pendingProps=n,a.type=t.type,a.flags=0,a.subtreeFlags=0,a.deletions=null),a.flags=t.flags&65011712,a.childLanes=t.childLanes,a.lanes=t.lanes,a.child=t.child,a.memoizedProps=t.memoizedProps,a.memoizedState=t.memoizedState,a.updateQueue=t.updateQueue,n=t.dependencies,a.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext},a.sibling=t.sibling,a.index=t.index,a.ref=t.ref,a.refCleanup=t.refCleanup,a}function vd(t,n){t.flags&=65011714;var a=t.alternate;return a===null?(t.childLanes=0,t.lanes=n,t.child=null,t.subtreeFlags=0,t.memoizedProps=null,t.memoizedState=null,t.updateQueue=null,t.dependencies=null,t.stateNode=null):(t.childLanes=a.childLanes,t.lanes=a.lanes,t.child=a.child,t.subtreeFlags=0,t.deletions=null,t.memoizedProps=a.memoizedProps,t.memoizedState=a.memoizedState,t.updateQueue=a.updateQueue,t.type=a.type,n=a.dependencies,t.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext}),t}function ko(t,n,a,s,u,f){var S=0;if(s=t,typeof t=="function")ku(t)&&(S=1);else if(typeof t=="string")S=PS(t,a,K.current)?26:t==="html"||t==="head"||t==="body"?27:5;else t:switch(t){case C:return t=Vn(31,a,n,u),t.elementType=C,t.lanes=f,t;case A:return ka(a.children,u,f,n);case M:S=8,u|=24;break;case v:return t=Vn(12,a,n,u|2),t.elementType=v,t.lanes=f,t;case V:return t=Vn(13,a,n,u),t.elementType=V,t.lanes=f,t;case B:return t=Vn(19,a,n,u),t.elementType=B,t.lanes=f,t;default:if(typeof t=="object"&&t!==null)switch(t.$$typeof){case T:S=10;break t;case D:S=9;break t;case z:S=11;break t;case O:S=14;break t;case ut:S=16,s=null;break t}S=29,a=Error(r(130,t===null?"null":typeof t,"")),s=null}return n=Vn(S,a,n,u),n.elementType=t,n.type=s,n.lanes=f,n}function ka(t,n,a,s){return t=Vn(7,t,s,n),t.lanes=a,t}function qu(t,n,a){return t=Vn(6,t,null,n),t.lanes=a,t}function Sd(t){var n=Vn(18,null,null,0);return n.stateNode=t,n}function Yu(t,n,a){return n=Vn(4,t.children!==null?t.children:[],t.key,n),n.lanes=a,n.stateNode={containerInfo:t.containerInfo,pendingChildren:null,implementation:t.implementation},n}var xd=new WeakMap;function $n(t,n){if(typeof t=="object"&&t!==null){var a=xd.get(t);return a!==void 0?a:(n={value:t,source:n,stack:ee(n)},xd.set(t,n),n)}return{value:t,source:n,stack:ee(n)}}var br=[],Ar=0,qo=null,Bs=0,ti=[],ei=0,sa=null,Mi=1,yi="";function Li(t,n){br[Ar++]=Bs,br[Ar++]=qo,qo=t,Bs=n}function Md(t,n,a){ti[ei++]=Mi,ti[ei++]=yi,ti[ei++]=sa,sa=t;var s=Mi;t=yi;var u=32-Xt(s)-1;s&=~(1<<u),a+=1;var f=32-Xt(n)+u;if(30<f){var S=u-u%5;f=(s&(1<<S)-1).toString(32),s>>=S,u-=S,Mi=1<<32-Xt(n)+u|a<<u|s,yi=f+t}else Mi=1<<f|a<<u|s,yi=t}function ju(t){t.return!==null&&(Li(t,1),Md(t,1,0))}function Zu(t){for(;t===qo;)qo=br[--Ar],br[Ar]=null,Bs=br[--Ar],br[Ar]=null;for(;t===sa;)sa=ti[--ei],ti[ei]=null,yi=ti[--ei],ti[ei]=null,Mi=ti[--ei],ti[ei]=null}function yd(t,n){ti[ei++]=Mi,ti[ei++]=yi,ti[ei++]=sa,Mi=n.id,yi=n.overflow,sa=t}var pn=null,Be=null,me=!1,oa=null,ni=!1,Ku=Error(r(519));function la(t){var n=Error(r(418,1<arguments.length&&arguments[1]!==void 0&&arguments[1]?"text":"HTML",""));throw Is($n(n,t)),Ku}function Ed(t){var n=t.stateNode,a=t.type,s=t.memoizedProps;switch(n[Ze]=t,n[Sn]=s,a){case"dialog":he("cancel",n),he("close",n);break;case"iframe":case"object":case"embed":he("load",n);break;case"video":case"audio":for(a=0;a<so.length;a++)he(so[a],n);break;case"source":he("error",n);break;case"img":case"image":case"link":he("error",n),he("load",n);break;case"details":he("toggle",n);break;case"input":he("invalid",n),Rs(n,s.value,s.defaultValue,s.checked,s.defaultChecked,s.type,s.name,!0);break;case"select":he("invalid",n);break;case"textarea":he("invalid",n),Ih(n,s.value,s.defaultValue,s.children)}a=s.children,typeof a!="string"&&typeof a!="number"&&typeof a!="bigint"||n.textContent===""+a||s.suppressHydrationWarning===!0||Hm(n.textContent,a)?(s.popover!=null&&(he("beforetoggle",n),he("toggle",n)),s.onScroll!=null&&he("scroll",n),s.onScrollEnd!=null&&he("scrollend",n),s.onClick!=null&&(n.onclick=Ci),n=!0):n=!1,n||la(t,!0)}function Td(t){for(pn=t.return;pn;)switch(pn.tag){case 5:case 31:case 13:ni=!1;return;case 27:case 3:ni=!0;return;default:pn=pn.return}}function Rr(t){if(t!==pn)return!1;if(!me)return Td(t),me=!0,!1;var n=t.tag,a;if((a=n!==3&&n!==27)&&((a=n===5)&&(a=t.type,a=!(a!=="form"&&a!=="button")||mf(t.type,t.memoizedProps)),a=!a),a&&Be&&la(t),Td(t),n===13){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(317));Be=Zm(t)}else if(n===31){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(317));Be=Zm(t)}else n===27?(n=Be,ya(t.type)?(t=xf,xf=null,Be=t):Be=n):Be=pn?ai(t.stateNode.nextSibling):null;return!0}function qa(){Be=pn=null,me=!1}function Qu(){var t=oa;return t!==null&&(Pn===null?Pn=t:Pn.push.apply(Pn,t),oa=null),t}function Is(t){oa===null?oa=[t]:oa.push(t)}var Ju=L(null),Ya=null,Ui=null;function ua(t,n,a){G(Ju,n._currentValue),n._currentValue=a}function Ni(t){t._currentValue=Ju.current,W(Ju)}function $u(t,n,a){for(;t!==null;){var s=t.alternate;if((t.childLanes&n)!==n?(t.childLanes|=n,s!==null&&(s.childLanes|=n)):s!==null&&(s.childLanes&n)!==n&&(s.childLanes|=n),t===a)break;t=t.return}}function tc(t,n,a,s){var u=t.child;for(u!==null&&(u.return=t);u!==null;){var f=u.dependencies;if(f!==null){var S=u.child;f=f.firstContext;t:for(;f!==null;){var E=f;f=u;for(var I=0;I<n.length;I++)if(E.context===n[I]){f.lanes|=a,E=f.alternate,E!==null&&(E.lanes|=a),$u(f.return,a,t),s||(S=null);break t}f=E.next}}else if(u.tag===18){if(S=u.return,S===null)throw Error(r(341));S.lanes|=a,f=S.alternate,f!==null&&(f.lanes|=a),$u(S,a,t),S=null}else S=u.child;if(S!==null)S.return=u;else for(S=u;S!==null;){if(S===t){S=null;break}if(u=S.sibling,u!==null){u.return=S.return,S=u;break}S=S.return}u=S}}function Cr(t,n,a,s){t=null;for(var u=n,f=!1;u!==null;){if(!f){if((u.flags&524288)!==0)f=!0;else if((u.flags&262144)!==0)break}if(u.tag===10){var S=u.alternate;if(S===null)throw Error(r(387));if(S=S.memoizedProps,S!==null){var E=u.type;Gn(u.pendingProps.value,S.value)||(t!==null?t.push(E):t=[E])}}else if(u===Mt.current){if(S=u.alternate,S===null)throw Error(r(387));S.memoizedState.memoizedState!==u.memoizedState.memoizedState&&(t!==null?t.push(fo):t=[fo])}u=u.return}t!==null&&tc(n,t,a,s),n.flags|=262144}function Yo(t){for(t=t.firstContext;t!==null;){if(!Gn(t.context._currentValue,t.memoizedValue))return!0;t=t.next}return!1}function ja(t){Ya=t,Ui=null,t=t.dependencies,t!==null&&(t.firstContext=null)}function mn(t){return bd(Ya,t)}function jo(t,n){return Ya===null&&ja(t),bd(t,n)}function bd(t,n){var a=n._currentValue;if(n={context:n,memoizedValue:a,next:null},Ui===null){if(t===null)throw Error(r(308));Ui=n,t.dependencies={lanes:0,firstContext:n},t.flags|=524288}else Ui=Ui.next=n;return a}var U0=typeof AbortController<"u"?AbortController:function(){var t=[],n=this.signal={aborted:!1,addEventListener:function(a,s){t.push(s)}};this.abort=function(){n.aborted=!0,t.forEach(function(a){return a()})}},N0=o.unstable_scheduleCallback,O0=o.unstable_NormalPriority,$e={$$typeof:T,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function ec(){return{controller:new U0,data:new Map,refCount:0}}function Fs(t){t.refCount--,t.refCount===0&&N0(O0,function(){t.controller.abort()})}var Hs=null,nc=0,wr=0,Dr=null;function z0(t,n){if(Hs===null){var a=Hs=[];nc=0,wr=sf(),Dr={status:"pending",value:void 0,then:function(s){a.push(s)}}}return nc++,n.then(Ad,Ad),n}function Ad(){if(--nc===0&&Hs!==null){Dr!==null&&(Dr.status="fulfilled");var t=Hs;Hs=null,wr=0,Dr=null;for(var n=0;n<t.length;n++)(0,t[n])()}}function P0(t,n){var a=[],s={status:"pending",value:null,reason:null,then:function(u){a.push(u)}};return t.then(function(){s.status="fulfilled",s.value=n;for(var u=0;u<a.length;u++)(0,a[u])(n)},function(u){for(s.status="rejected",s.reason=u,u=0;u<a.length;u++)(0,a[u])(void 0)}),s}var Rd=P.S;P.S=function(t,n){cm=gt(),typeof n=="object"&&n!==null&&typeof n.then=="function"&&z0(t,n),Rd!==null&&Rd(t,n)};var Za=L(null);function ic(){var t=Za.current;return t!==null?t:Oe.pooledCache}function Zo(t,n){n===null?G(Za,Za.current):G(Za,n.pool)}function Cd(){var t=ic();return t===null?null:{parent:$e._currentValue,pool:t}}var Lr=Error(r(460)),ac=Error(r(474)),Ko=Error(r(542)),Qo={then:function(){}};function wd(t){return t=t.status,t==="fulfilled"||t==="rejected"}function Dd(t,n,a){switch(a=t[a],a===void 0?t.push(n):a!==n&&(n.then(Ci,Ci),n=a),n.status){case"fulfilled":return n.value;case"rejected":throw t=n.reason,Ud(t),t;default:if(typeof n.status=="string")n.then(Ci,Ci);else{if(t=Oe,t!==null&&100<t.shellSuspendCounter)throw Error(r(482));t=n,t.status="pending",t.then(function(s){if(n.status==="pending"){var u=n;u.status="fulfilled",u.value=s}},function(s){if(n.status==="pending"){var u=n;u.status="rejected",u.reason=s}})}switch(n.status){case"fulfilled":return n.value;case"rejected":throw t=n.reason,Ud(t),t}throw Qa=n,Lr}}function Ka(t){try{var n=t._init;return n(t._payload)}catch(a){throw a!==null&&typeof a=="object"&&typeof a.then=="function"?(Qa=a,Lr):a}}var Qa=null;function Ld(){if(Qa===null)throw Error(r(459));var t=Qa;return Qa=null,t}function Ud(t){if(t===Lr||t===Ko)throw Error(r(483))}var Ur=null,Gs=0;function Jo(t){var n=Gs;return Gs+=1,Ur===null&&(Ur=[]),Dd(Ur,t,n)}function Vs(t,n){n=n.props.ref,t.ref=n!==void 0?n:null}function $o(t,n){throw n.$$typeof===x?Error(r(525)):(t=Object.prototype.toString.call(n),Error(r(31,t==="[object Object]"?"object with keys {"+Object.keys(n).join(", ")+"}":t)))}function Nd(t){function n(k,H){if(t){var Z=k.deletions;Z===null?(k.deletions=[H],k.flags|=16):Z.push(H)}}function a(k,H){if(!t)return null;for(;H!==null;)n(k,H),H=H.sibling;return null}function s(k){for(var H=new Map;k!==null;)k.key!==null?H.set(k.key,k):H.set(k.index,k),k=k.sibling;return H}function u(k,H){return k=Di(k,H),k.index=0,k.sibling=null,k}function f(k,H,Z){return k.index=Z,t?(Z=k.alternate,Z!==null?(Z=Z.index,Z<H?(k.flags|=67108866,H):Z):(k.flags|=67108866,H)):(k.flags|=1048576,H)}function S(k){return t&&k.alternate===null&&(k.flags|=67108866),k}function E(k,H,Z,ht){return H===null||H.tag!==6?(H=qu(Z,k.mode,ht),H.return=k,H):(H=u(H,Z),H.return=k,H)}function I(k,H,Z,ht){var Vt=Z.type;return Vt===A?ct(k,H,Z.props.children,ht,Z.key):H!==null&&(H.elementType===Vt||typeof Vt=="object"&&Vt!==null&&Vt.$$typeof===ut&&Ka(Vt)===H.type)?(H=u(H,Z.props),Vs(H,Z),H.return=k,H):(H=ko(Z.type,Z.key,Z.props,null,k.mode,ht),Vs(H,Z),H.return=k,H)}function Q(k,H,Z,ht){return H===null||H.tag!==4||H.stateNode.containerInfo!==Z.containerInfo||H.stateNode.implementation!==Z.implementation?(H=Yu(Z,k.mode,ht),H.return=k,H):(H=u(H,Z.children||[]),H.return=k,H)}function ct(k,H,Z,ht,Vt){return H===null||H.tag!==7?(H=ka(Z,k.mode,ht,Vt),H.return=k,H):(H=u(H,Z),H.return=k,H)}function pt(k,H,Z){if(typeof H=="string"&&H!==""||typeof H=="number"||typeof H=="bigint")return H=qu(""+H,k.mode,Z),H.return=k,H;if(typeof H=="object"&&H!==null){switch(H.$$typeof){case y:return Z=ko(H.type,H.key,H.props,null,k.mode,Z),Vs(Z,H),Z.return=k,Z;case b:return H=Yu(H,k.mode,Z),H.return=k,H;case ut:return H=Ka(H),pt(k,H,Z)}if(tt(H)||dt(H))return H=ka(H,k.mode,Z,null),H.return=k,H;if(typeof H.then=="function")return pt(k,Jo(H),Z);if(H.$$typeof===T)return pt(k,jo(k,H),Z);$o(k,H)}return null}function $(k,H,Z,ht){var Vt=H!==null?H.key:null;if(typeof Z=="string"&&Z!==""||typeof Z=="number"||typeof Z=="bigint")return Vt!==null?null:E(k,H,""+Z,ht);if(typeof Z=="object"&&Z!==null){switch(Z.$$typeof){case y:return Z.key===Vt?I(k,H,Z,ht):null;case b:return Z.key===Vt?Q(k,H,Z,ht):null;case ut:return Z=Ka(Z),$(k,H,Z,ht)}if(tt(Z)||dt(Z))return Vt!==null?null:ct(k,H,Z,ht,null);if(typeof Z.then=="function")return $(k,H,Jo(Z),ht);if(Z.$$typeof===T)return $(k,H,jo(k,Z),ht);$o(k,Z)}return null}function ot(k,H,Z,ht,Vt){if(typeof ht=="string"&&ht!==""||typeof ht=="number"||typeof ht=="bigint")return k=k.get(Z)||null,E(H,k,""+ht,Vt);if(typeof ht=="object"&&ht!==null){switch(ht.$$typeof){case y:return k=k.get(ht.key===null?Z:ht.key)||null,I(H,k,ht,Vt);case b:return k=k.get(ht.key===null?Z:ht.key)||null,Q(H,k,ht,Vt);case ut:return ht=Ka(ht),ot(k,H,Z,ht,Vt)}if(tt(ht)||dt(ht))return k=k.get(Z)||null,ct(H,k,ht,Vt,null);if(typeof ht.then=="function")return ot(k,H,Z,Jo(ht),Vt);if(ht.$$typeof===T)return ot(k,H,Z,jo(H,ht),Vt);$o(H,ht)}return null}function Lt(k,H,Z,ht){for(var Vt=null,_e=null,zt=H,ae=H=0,pe=null;zt!==null&&ae<Z.length;ae++){zt.index>ae?(pe=zt,zt=null):pe=zt.sibling;var ve=$(k,zt,Z[ae],ht);if(ve===null){zt===null&&(zt=pe);break}t&&zt&&ve.alternate===null&&n(k,zt),H=f(ve,H,ae),_e===null?Vt=ve:_e.sibling=ve,_e=ve,zt=pe}if(ae===Z.length)return a(k,zt),me&&Li(k,ae),Vt;if(zt===null){for(;ae<Z.length;ae++)zt=pt(k,Z[ae],ht),zt!==null&&(H=f(zt,H,ae),_e===null?Vt=zt:_e.sibling=zt,_e=zt);return me&&Li(k,ae),Vt}for(zt=s(zt);ae<Z.length;ae++)pe=ot(zt,k,ae,Z[ae],ht),pe!==null&&(t&&pe.alternate!==null&&zt.delete(pe.key===null?ae:pe.key),H=f(pe,H,ae),_e===null?Vt=pe:_e.sibling=pe,_e=pe);return t&&zt.forEach(function(Ra){return n(k,Ra)}),me&&Li(k,ae),Vt}function Zt(k,H,Z,ht){if(Z==null)throw Error(r(151));for(var Vt=null,_e=null,zt=H,ae=H=0,pe=null,ve=Z.next();zt!==null&&!ve.done;ae++,ve=Z.next()){zt.index>ae?(pe=zt,zt=null):pe=zt.sibling;var Ra=$(k,zt,ve.value,ht);if(Ra===null){zt===null&&(zt=pe);break}t&&zt&&Ra.alternate===null&&n(k,zt),H=f(Ra,H,ae),_e===null?Vt=Ra:_e.sibling=Ra,_e=Ra,zt=pe}if(ve.done)return a(k,zt),me&&Li(k,ae),Vt;if(zt===null){for(;!ve.done;ae++,ve=Z.next())ve=pt(k,ve.value,ht),ve!==null&&(H=f(ve,H,ae),_e===null?Vt=ve:_e.sibling=ve,_e=ve);return me&&Li(k,ae),Vt}for(zt=s(zt);!ve.done;ae++,ve=Z.next())ve=ot(zt,k,ae,ve.value,ht),ve!==null&&(t&&ve.alternate!==null&&zt.delete(ve.key===null?ae:ve.key),H=f(ve,H,ae),_e===null?Vt=ve:_e.sibling=ve,_e=ve);return t&&zt.forEach(function(YS){return n(k,YS)}),me&&Li(k,ae),Vt}function Le(k,H,Z,ht){if(typeof Z=="object"&&Z!==null&&Z.type===A&&Z.key===null&&(Z=Z.props.children),typeof Z=="object"&&Z!==null){switch(Z.$$typeof){case y:t:{for(var Vt=Z.key;H!==null;){if(H.key===Vt){if(Vt=Z.type,Vt===A){if(H.tag===7){a(k,H.sibling),ht=u(H,Z.props.children),ht.return=k,k=ht;break t}}else if(H.elementType===Vt||typeof Vt=="object"&&Vt!==null&&Vt.$$typeof===ut&&Ka(Vt)===H.type){a(k,H.sibling),ht=u(H,Z.props),Vs(ht,Z),ht.return=k,k=ht;break t}a(k,H);break}else n(k,H);H=H.sibling}Z.type===A?(ht=ka(Z.props.children,k.mode,ht,Z.key),ht.return=k,k=ht):(ht=ko(Z.type,Z.key,Z.props,null,k.mode,ht),Vs(ht,Z),ht.return=k,k=ht)}return S(k);case b:t:{for(Vt=Z.key;H!==null;){if(H.key===Vt)if(H.tag===4&&H.stateNode.containerInfo===Z.containerInfo&&H.stateNode.implementation===Z.implementation){a(k,H.sibling),ht=u(H,Z.children||[]),ht.return=k,k=ht;break t}else{a(k,H);break}else n(k,H);H=H.sibling}ht=Yu(Z,k.mode,ht),ht.return=k,k=ht}return S(k);case ut:return Z=Ka(Z),Le(k,H,Z,ht)}if(tt(Z))return Lt(k,H,Z,ht);if(dt(Z)){if(Vt=dt(Z),typeof Vt!="function")throw Error(r(150));return Z=Vt.call(Z),Zt(k,H,Z,ht)}if(typeof Z.then=="function")return Le(k,H,Jo(Z),ht);if(Z.$$typeof===T)return Le(k,H,jo(k,Z),ht);$o(k,Z)}return typeof Z=="string"&&Z!==""||typeof Z=="number"||typeof Z=="bigint"?(Z=""+Z,H!==null&&H.tag===6?(a(k,H.sibling),ht=u(H,Z),ht.return=k,k=ht):(a(k,H),ht=qu(Z,k.mode,ht),ht.return=k,k=ht),S(k)):a(k,H)}return function(k,H,Z,ht){try{Gs=0;var Vt=Le(k,H,Z,ht);return Ur=null,Vt}catch(zt){if(zt===Lr||zt===Ko)throw zt;var _e=Vn(29,zt,null,k.mode);return _e.lanes=ht,_e.return=k,_e}}}var Ja=Nd(!0),Od=Nd(!1),ca=!1;function rc(t){t.updateQueue={baseState:t.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function sc(t,n){t=t.updateQueue,n.updateQueue===t&&(n.updateQueue={baseState:t.baseState,firstBaseUpdate:t.firstBaseUpdate,lastBaseUpdate:t.lastBaseUpdate,shared:t.shared,callbacks:null})}function fa(t){return{lane:t,tag:0,payload:null,callback:null,next:null}}function ha(t,n,a){var s=t.updateQueue;if(s===null)return null;if(s=s.shared,(xe&2)!==0){var u=s.pending;return u===null?n.next=n:(n.next=u.next,u.next=n),s.pending=n,n=Wo(t),_d(t,null,a),n}return Xo(t,s,n,a),Wo(t)}function Xs(t,n,a){if(n=n.updateQueue,n!==null&&(n=n.shared,(a&4194048)!==0)){var s=n.lanes;s&=t.pendingLanes,a|=s,n.lanes=a,Hn(t,a)}}function oc(t,n){var a=t.updateQueue,s=t.alternate;if(s!==null&&(s=s.updateQueue,a===s)){var u=null,f=null;if(a=a.firstBaseUpdate,a!==null){do{var S={lane:a.lane,tag:a.tag,payload:a.payload,callback:null,next:null};f===null?u=f=S:f=f.next=S,a=a.next}while(a!==null);f===null?u=f=n:f=f.next=n}else u=f=n;a={baseState:s.baseState,firstBaseUpdate:u,lastBaseUpdate:f,shared:s.shared,callbacks:s.callbacks},t.updateQueue=a;return}t=a.lastBaseUpdate,t===null?a.firstBaseUpdate=n:t.next=n,a.lastBaseUpdate=n}var lc=!1;function Ws(){if(lc){var t=Dr;if(t!==null)throw t}}function ks(t,n,a,s){lc=!1;var u=t.updateQueue;ca=!1;var f=u.firstBaseUpdate,S=u.lastBaseUpdate,E=u.shared.pending;if(E!==null){u.shared.pending=null;var I=E,Q=I.next;I.next=null,S===null?f=Q:S.next=Q,S=I;var ct=t.alternate;ct!==null&&(ct=ct.updateQueue,E=ct.lastBaseUpdate,E!==S&&(E===null?ct.firstBaseUpdate=Q:E.next=Q,ct.lastBaseUpdate=I))}if(f!==null){var pt=u.baseState;S=0,ct=Q=I=null,E=f;do{var $=E.lane&-536870913,ot=$!==E.lane;if(ot?(de&$)===$:(s&$)===$){$!==0&&$===wr&&(lc=!0),ct!==null&&(ct=ct.next={lane:0,tag:E.tag,payload:E.payload,callback:null,next:null});t:{var Lt=t,Zt=E;$=n;var Le=a;switch(Zt.tag){case 1:if(Lt=Zt.payload,typeof Lt=="function"){pt=Lt.call(Le,pt,$);break t}pt=Lt;break t;case 3:Lt.flags=Lt.flags&-65537|128;case 0:if(Lt=Zt.payload,$=typeof Lt=="function"?Lt.call(Le,pt,$):Lt,$==null)break t;pt=_({},pt,$);break t;case 2:ca=!0}}$=E.callback,$!==null&&(t.flags|=64,ot&&(t.flags|=8192),ot=u.callbacks,ot===null?u.callbacks=[$]:ot.push($))}else ot={lane:$,tag:E.tag,payload:E.payload,callback:E.callback,next:null},ct===null?(Q=ct=ot,I=pt):ct=ct.next=ot,S|=$;if(E=E.next,E===null){if(E=u.shared.pending,E===null)break;ot=E,E=ot.next,ot.next=null,u.lastBaseUpdate=ot,u.shared.pending=null}}while(!0);ct===null&&(I=pt),u.baseState=I,u.firstBaseUpdate=Q,u.lastBaseUpdate=ct,f===null&&(u.shared.lanes=0),_a|=S,t.lanes=S,t.memoizedState=pt}}function zd(t,n){if(typeof t!="function")throw Error(r(191,t));t.call(n)}function Pd(t,n){var a=t.callbacks;if(a!==null)for(t.callbacks=null,t=0;t<a.length;t++)zd(a[t],n)}var Nr=L(null),tl=L(0);function Bd(t,n){t=Vi,G(tl,t),G(Nr,n),Vi=t|n.baseLanes}function uc(){G(tl,Vi),G(Nr,Nr.current)}function cc(){Vi=tl.current,W(Nr),W(tl)}var Xn=L(null),ii=null;function da(t){var n=t.alternate;G(Ye,Ye.current&1),G(Xn,t),ii===null&&(n===null||Nr.current!==null||n.memoizedState!==null)&&(ii=t)}function fc(t){G(Ye,Ye.current),G(Xn,t),ii===null&&(ii=t)}function Id(t){t.tag===22?(G(Ye,Ye.current),G(Xn,t),ii===null&&(ii=t)):pa()}function pa(){G(Ye,Ye.current),G(Xn,Xn.current)}function Wn(t){W(Xn),ii===t&&(ii=null),W(Ye)}var Ye=L(0);function el(t){for(var n=t;n!==null;){if(n.tag===13){var a=n.memoizedState;if(a!==null&&(a=a.dehydrated,a===null||vf(a)||Sf(a)))return n}else if(n.tag===19&&(n.memoizedProps.revealOrder==="forwards"||n.memoizedProps.revealOrder==="backwards"||n.memoizedProps.revealOrder==="unstable_legacy-backwards"||n.memoizedProps.revealOrder==="together")){if((n.flags&128)!==0)return n}else if(n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return null;n=n.return}n.sibling.return=n.return,n=n.sibling}return null}var Oi=0,ne=null,we=null,tn=null,nl=!1,Or=!1,$a=!1,il=0,qs=0,zr=null,B0=0;function We(){throw Error(r(321))}function hc(t,n){if(n===null)return!1;for(var a=0;a<n.length&&a<t.length;a++)if(!Gn(t[a],n[a]))return!1;return!0}function dc(t,n,a,s,u,f){return Oi=f,ne=n,n.memoizedState=null,n.updateQueue=null,n.lanes=0,P.H=t===null||t.memoizedState===null?Mp:Cc,$a=!1,f=a(s,u),$a=!1,Or&&(f=Hd(n,a,s,u)),Fd(t),f}function Fd(t){P.H=Zs;var n=we!==null&&we.next!==null;if(Oi=0,tn=we=ne=null,nl=!1,qs=0,zr=null,n)throw Error(r(300));t===null||en||(t=t.dependencies,t!==null&&Yo(t)&&(en=!0))}function Hd(t,n,a,s){ne=t;var u=0;do{if(Or&&(zr=null),qs=0,Or=!1,25<=u)throw Error(r(301));if(u+=1,tn=we=null,t.updateQueue!=null){var f=t.updateQueue;f.lastEffect=null,f.events=null,f.stores=null,f.memoCache!=null&&(f.memoCache.index=0)}P.H=yp,f=n(a,s)}while(Or);return f}function I0(){var t=P.H,n=t.useState()[0];return n=typeof n.then=="function"?Ys(n):n,t=t.useState()[0],(we!==null?we.memoizedState:null)!==t&&(ne.flags|=1024),n}function pc(){var t=il!==0;return il=0,t}function mc(t,n,a){n.updateQueue=t.updateQueue,n.flags&=-2053,t.lanes&=~a}function gc(t){if(nl){for(t=t.memoizedState;t!==null;){var n=t.queue;n!==null&&(n.pending=null),t=t.next}nl=!1}Oi=0,tn=we=ne=null,Or=!1,qs=il=0,zr=null}function Rn(){var t={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return tn===null?ne.memoizedState=tn=t:tn=tn.next=t,tn}function je(){if(we===null){var t=ne.alternate;t=t!==null?t.memoizedState:null}else t=we.next;var n=tn===null?ne.memoizedState:tn.next;if(n!==null)tn=n,we=t;else{if(t===null)throw ne.alternate===null?Error(r(467)):Error(r(310));we=t,t={memoizedState:we.memoizedState,baseState:we.baseState,baseQueue:we.baseQueue,queue:we.queue,next:null},tn===null?ne.memoizedState=tn=t:tn=tn.next=t}return tn}function al(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function Ys(t){var n=qs;return qs+=1,zr===null&&(zr=[]),t=Dd(zr,t,n),n=ne,(tn===null?n.memoizedState:tn.next)===null&&(n=n.alternate,P.H=n===null||n.memoizedState===null?Mp:Cc),t}function rl(t){if(t!==null&&typeof t=="object"){if(typeof t.then=="function")return Ys(t);if(t.$$typeof===T)return mn(t)}throw Error(r(438,String(t)))}function _c(t){var n=null,a=ne.updateQueue;if(a!==null&&(n=a.memoCache),n==null){var s=ne.alternate;s!==null&&(s=s.updateQueue,s!==null&&(s=s.memoCache,s!=null&&(n={data:s.data.map(function(u){return u.slice()}),index:0})))}if(n==null&&(n={data:[],index:0}),a===null&&(a=al(),ne.updateQueue=a),a.memoCache=n,a=n.data[n.index],a===void 0)for(a=n.data[n.index]=Array(t),s=0;s<t;s++)a[s]=N;return n.index++,a}function zi(t,n){return typeof n=="function"?n(t):n}function sl(t){var n=je();return vc(n,we,t)}function vc(t,n,a){var s=t.queue;if(s===null)throw Error(r(311));s.lastRenderedReducer=a;var u=t.baseQueue,f=s.pending;if(f!==null){if(u!==null){var S=u.next;u.next=f.next,f.next=S}n.baseQueue=u=f,s.pending=null}if(f=t.baseState,u===null)t.memoizedState=f;else{n=u.next;var E=S=null,I=null,Q=n,ct=!1;do{var pt=Q.lane&-536870913;if(pt!==Q.lane?(de&pt)===pt:(Oi&pt)===pt){var $=Q.revertLane;if($===0)I!==null&&(I=I.next={lane:0,revertLane:0,gesture:null,action:Q.action,hasEagerState:Q.hasEagerState,eagerState:Q.eagerState,next:null}),pt===wr&&(ct=!0);else if((Oi&$)===$){Q=Q.next,$===wr&&(ct=!0);continue}else pt={lane:0,revertLane:Q.revertLane,gesture:null,action:Q.action,hasEagerState:Q.hasEagerState,eagerState:Q.eagerState,next:null},I===null?(E=I=pt,S=f):I=I.next=pt,ne.lanes|=$,_a|=$;pt=Q.action,$a&&a(f,pt),f=Q.hasEagerState?Q.eagerState:a(f,pt)}else $={lane:pt,revertLane:Q.revertLane,gesture:Q.gesture,action:Q.action,hasEagerState:Q.hasEagerState,eagerState:Q.eagerState,next:null},I===null?(E=I=$,S=f):I=I.next=$,ne.lanes|=pt,_a|=pt;Q=Q.next}while(Q!==null&&Q!==n);if(I===null?S=f:I.next=E,!Gn(f,t.memoizedState)&&(en=!0,ct&&(a=Dr,a!==null)))throw a;t.memoizedState=f,t.baseState=S,t.baseQueue=I,s.lastRenderedState=f}return u===null&&(s.lanes=0),[t.memoizedState,s.dispatch]}function Sc(t){var n=je(),a=n.queue;if(a===null)throw Error(r(311));a.lastRenderedReducer=t;var s=a.dispatch,u=a.pending,f=n.memoizedState;if(u!==null){a.pending=null;var S=u=u.next;do f=t(f,S.action),S=S.next;while(S!==u);Gn(f,n.memoizedState)||(en=!0),n.memoizedState=f,n.baseQueue===null&&(n.baseState=f),a.lastRenderedState=f}return[f,s]}function Gd(t,n,a){var s=ne,u=je(),f=me;if(f){if(a===void 0)throw Error(r(407));a=a()}else a=n();var S=!Gn((we||u).memoizedState,a);if(S&&(u.memoizedState=a,en=!0),u=u.queue,yc(Wd.bind(null,s,u,t),[t]),u.getSnapshot!==n||S||tn!==null&&tn.memoizedState.tag&1){if(s.flags|=2048,Pr(9,{destroy:void 0},Xd.bind(null,s,u,a,n),null),Oe===null)throw Error(r(349));f||(Oi&127)!==0||Vd(s,n,a)}return a}function Vd(t,n,a){t.flags|=16384,t={getSnapshot:n,value:a},n=ne.updateQueue,n===null?(n=al(),ne.updateQueue=n,n.stores=[t]):(a=n.stores,a===null?n.stores=[t]:a.push(t))}function Xd(t,n,a,s){n.value=a,n.getSnapshot=s,kd(n)&&qd(t)}function Wd(t,n,a){return a(function(){kd(n)&&qd(t)})}function kd(t){var n=t.getSnapshot;t=t.value;try{var a=n();return!Gn(t,a)}catch{return!0}}function qd(t){var n=Wa(t,2);n!==null&&Bn(n,t,2)}function xc(t){var n=Rn();if(typeof t=="function"){var a=t;if(t=a(),$a){wt(!0);try{a()}finally{wt(!1)}}}return n.memoizedState=n.baseState=t,n.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:zi,lastRenderedState:t},n}function Yd(t,n,a,s){return t.baseState=a,vc(t,we,typeof s=="function"?s:zi)}function F0(t,n,a,s,u){if(ul(t))throw Error(r(485));if(t=n.action,t!==null){var f={payload:u,action:t,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(S){f.listeners.push(S)}};P.T!==null?a(!0):f.isTransition=!1,s(f),a=n.pending,a===null?(f.next=n.pending=f,jd(n,f)):(f.next=a.next,n.pending=a.next=f)}}function jd(t,n){var a=n.action,s=n.payload,u=t.state;if(n.isTransition){var f=P.T,S={};P.T=S;try{var E=a(u,s),I=P.S;I!==null&&I(S,E),Zd(t,n,E)}catch(Q){Mc(t,n,Q)}finally{f!==null&&S.types!==null&&(f.types=S.types),P.T=f}}else try{f=a(u,s),Zd(t,n,f)}catch(Q){Mc(t,n,Q)}}function Zd(t,n,a){a!==null&&typeof a=="object"&&typeof a.then=="function"?a.then(function(s){Kd(t,n,s)},function(s){return Mc(t,n,s)}):Kd(t,n,a)}function Kd(t,n,a){n.status="fulfilled",n.value=a,Qd(n),t.state=a,n=t.pending,n!==null&&(a=n.next,a===n?t.pending=null:(a=a.next,n.next=a,jd(t,a)))}function Mc(t,n,a){var s=t.pending;if(t.pending=null,s!==null){s=s.next;do n.status="rejected",n.reason=a,Qd(n),n=n.next;while(n!==s)}t.action=null}function Qd(t){t=t.listeners;for(var n=0;n<t.length;n++)(0,t[n])()}function Jd(t,n){return n}function $d(t,n){if(me){var a=Oe.formState;if(a!==null){t:{var s=ne;if(me){if(Be){e:{for(var u=Be,f=ni;u.nodeType!==8;){if(!f){u=null;break e}if(u=ai(u.nextSibling),u===null){u=null;break e}}f=u.data,u=f==="F!"||f==="F"?u:null}if(u){Be=ai(u.nextSibling),s=u.data==="F!";break t}}la(s)}s=!1}s&&(n=a[0])}}return a=Rn(),a.memoizedState=a.baseState=n,s={pending:null,lanes:0,dispatch:null,lastRenderedReducer:Jd,lastRenderedState:n},a.queue=s,a=vp.bind(null,ne,s),s.dispatch=a,s=xc(!1),f=Rc.bind(null,ne,!1,s.queue),s=Rn(),u={state:n,dispatch:null,action:t,pending:null},s.queue=u,a=F0.bind(null,ne,u,f,a),u.dispatch=a,s.memoizedState=t,[n,a,!1]}function tp(t){var n=je();return ep(n,we,t)}function ep(t,n,a){if(n=vc(t,n,Jd)[0],t=sl(zi)[0],typeof n=="object"&&n!==null&&typeof n.then=="function")try{var s=Ys(n)}catch(S){throw S===Lr?Ko:S}else s=n;n=je();var u=n.queue,f=u.dispatch;return a!==n.memoizedState&&(ne.flags|=2048,Pr(9,{destroy:void 0},H0.bind(null,u,a),null)),[s,f,t]}function H0(t,n){t.action=n}function np(t){var n=je(),a=we;if(a!==null)return ep(n,a,t);je(),n=n.memoizedState,a=je();var s=a.queue.dispatch;return a.memoizedState=t,[n,s,!1]}function Pr(t,n,a,s){return t={tag:t,create:a,deps:s,inst:n,next:null},n=ne.updateQueue,n===null&&(n=al(),ne.updateQueue=n),a=n.lastEffect,a===null?n.lastEffect=t.next=t:(s=a.next,a.next=t,t.next=s,n.lastEffect=t),t}function ip(){return je().memoizedState}function ol(t,n,a,s){var u=Rn();ne.flags|=t,u.memoizedState=Pr(1|n,{destroy:void 0},a,s===void 0?null:s)}function ll(t,n,a,s){var u=je();s=s===void 0?null:s;var f=u.memoizedState.inst;we!==null&&s!==null&&hc(s,we.memoizedState.deps)?u.memoizedState=Pr(n,f,a,s):(ne.flags|=t,u.memoizedState=Pr(1|n,f,a,s))}function ap(t,n){ol(8390656,8,t,n)}function yc(t,n){ll(2048,8,t,n)}function G0(t){ne.flags|=4;var n=ne.updateQueue;if(n===null)n=al(),ne.updateQueue=n,n.events=[t];else{var a=n.events;a===null?n.events=[t]:a.push(t)}}function rp(t){var n=je().memoizedState;return G0({ref:n,nextImpl:t}),function(){if((xe&2)!==0)throw Error(r(440));return n.impl.apply(void 0,arguments)}}function sp(t,n){return ll(4,2,t,n)}function op(t,n){return ll(4,4,t,n)}function lp(t,n){if(typeof n=="function"){t=t();var a=n(t);return function(){typeof a=="function"?a():n(null)}}if(n!=null)return t=t(),n.current=t,function(){n.current=null}}function up(t,n,a){a=a!=null?a.concat([t]):null,ll(4,4,lp.bind(null,n,t),a)}function Ec(){}function cp(t,n){var a=je();n=n===void 0?null:n;var s=a.memoizedState;return n!==null&&hc(n,s[1])?s[0]:(a.memoizedState=[t,n],t)}function fp(t,n){var a=je();n=n===void 0?null:n;var s=a.memoizedState;if(n!==null&&hc(n,s[1]))return s[0];if(s=t(),$a){wt(!0);try{t()}finally{wt(!1)}}return a.memoizedState=[s,n],s}function Tc(t,n,a){return a===void 0||(Oi&1073741824)!==0&&(de&261930)===0?t.memoizedState=n:(t.memoizedState=a,t=hm(),ne.lanes|=t,_a|=t,a)}function hp(t,n,a,s){return Gn(a,n)?a:Nr.current!==null?(t=Tc(t,a,s),Gn(t,n)||(en=!0),t):(Oi&42)===0||(Oi&1073741824)!==0&&(de&261930)===0?(en=!0,t.memoizedState=a):(t=hm(),ne.lanes|=t,_a|=t,n)}function dp(t,n,a,s,u){var f=q.p;q.p=f!==0&&8>f?f:8;var S=P.T,E={};P.T=E,Rc(t,!1,n,a);try{var I=u(),Q=P.S;if(Q!==null&&Q(E,I),I!==null&&typeof I=="object"&&typeof I.then=="function"){var ct=P0(I,s);js(t,n,ct,Yn(t))}else js(t,n,s,Yn(t))}catch(pt){js(t,n,{then:function(){},status:"rejected",reason:pt},Yn())}finally{q.p=f,S!==null&&E.types!==null&&(S.types=E.types),P.T=S}}function V0(){}function bc(t,n,a,s){if(t.tag!==5)throw Error(r(476));var u=pp(t).queue;dp(t,u,n,J,a===null?V0:function(){return mp(t),a(s)})}function pp(t){var n=t.memoizedState;if(n!==null)return n;n={memoizedState:J,baseState:J,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:zi,lastRenderedState:J},next:null};var a={};return n.next={memoizedState:a,baseState:a,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:zi,lastRenderedState:a},next:null},t.memoizedState=n,t=t.alternate,t!==null&&(t.memoizedState=n),n}function mp(t){var n=pp(t);n.next===null&&(n=t.alternate.memoizedState),js(t,n.next.queue,{},Yn())}function Ac(){return mn(fo)}function gp(){return je().memoizedState}function _p(){return je().memoizedState}function X0(t){for(var n=t.return;n!==null;){switch(n.tag){case 24:case 3:var a=Yn();t=fa(a);var s=ha(n,t,a);s!==null&&(Bn(s,n,a),Xs(s,n,a)),n={cache:ec()},t.payload=n;return}n=n.return}}function W0(t,n,a){var s=Yn();a={lane:s,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null},ul(t)?Sp(n,a):(a=Wu(t,n,a,s),a!==null&&(Bn(a,t,s),xp(a,n,s)))}function vp(t,n,a){var s=Yn();js(t,n,a,s)}function js(t,n,a,s){var u={lane:s,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null};if(ul(t))Sp(n,u);else{var f=t.alternate;if(t.lanes===0&&(f===null||f.lanes===0)&&(f=n.lastRenderedReducer,f!==null))try{var S=n.lastRenderedState,E=f(S,a);if(u.hasEagerState=!0,u.eagerState=E,Gn(E,S))return Xo(t,n,u,0),Oe===null&&Vo(),!1}catch{}if(a=Wu(t,n,u,s),a!==null)return Bn(a,t,s),xp(a,n,s),!0}return!1}function Rc(t,n,a,s){if(s={lane:2,revertLane:sf(),gesture:null,action:s,hasEagerState:!1,eagerState:null,next:null},ul(t)){if(n)throw Error(r(479))}else n=Wu(t,a,s,2),n!==null&&Bn(n,t,2)}function ul(t){var n=t.alternate;return t===ne||n!==null&&n===ne}function Sp(t,n){Or=nl=!0;var a=t.pending;a===null?n.next=n:(n.next=a.next,a.next=n),t.pending=n}function xp(t,n,a){if((a&4194048)!==0){var s=n.lanes;s&=t.pendingLanes,a|=s,n.lanes=a,Hn(t,a)}}var Zs={readContext:mn,use:rl,useCallback:We,useContext:We,useEffect:We,useImperativeHandle:We,useLayoutEffect:We,useInsertionEffect:We,useMemo:We,useReducer:We,useRef:We,useState:We,useDebugValue:We,useDeferredValue:We,useTransition:We,useSyncExternalStore:We,useId:We,useHostTransitionStatus:We,useFormState:We,useActionState:We,useOptimistic:We,useMemoCache:We,useCacheRefresh:We};Zs.useEffectEvent=We;var Mp={readContext:mn,use:rl,useCallback:function(t,n){return Rn().memoizedState=[t,n===void 0?null:n],t},useContext:mn,useEffect:ap,useImperativeHandle:function(t,n,a){a=a!=null?a.concat([t]):null,ol(4194308,4,lp.bind(null,n,t),a)},useLayoutEffect:function(t,n){return ol(4194308,4,t,n)},useInsertionEffect:function(t,n){ol(4,2,t,n)},useMemo:function(t,n){var a=Rn();n=n===void 0?null:n;var s=t();if($a){wt(!0);try{t()}finally{wt(!1)}}return a.memoizedState=[s,n],s},useReducer:function(t,n,a){var s=Rn();if(a!==void 0){var u=a(n);if($a){wt(!0);try{a(n)}finally{wt(!1)}}}else u=n;return s.memoizedState=s.baseState=u,t={pending:null,lanes:0,dispatch:null,lastRenderedReducer:t,lastRenderedState:u},s.queue=t,t=t.dispatch=W0.bind(null,ne,t),[s.memoizedState,t]},useRef:function(t){var n=Rn();return t={current:t},n.memoizedState=t},useState:function(t){t=xc(t);var n=t.queue,a=vp.bind(null,ne,n);return n.dispatch=a,[t.memoizedState,a]},useDebugValue:Ec,useDeferredValue:function(t,n){var a=Rn();return Tc(a,t,n)},useTransition:function(){var t=xc(!1);return t=dp.bind(null,ne,t.queue,!0,!1),Rn().memoizedState=t,[!1,t]},useSyncExternalStore:function(t,n,a){var s=ne,u=Rn();if(me){if(a===void 0)throw Error(r(407));a=a()}else{if(a=n(),Oe===null)throw Error(r(349));(de&127)!==0||Vd(s,n,a)}u.memoizedState=a;var f={value:a,getSnapshot:n};return u.queue=f,ap(Wd.bind(null,s,f,t),[t]),s.flags|=2048,Pr(9,{destroy:void 0},Xd.bind(null,s,f,a,n),null),a},useId:function(){var t=Rn(),n=Oe.identifierPrefix;if(me){var a=yi,s=Mi;a=(s&~(1<<32-Xt(s)-1)).toString(32)+a,n="_"+n+"R_"+a,a=il++,0<a&&(n+="H"+a.toString(32)),n+="_"}else a=B0++,n="_"+n+"r_"+a.toString(32)+"_";return t.memoizedState=n},useHostTransitionStatus:Ac,useFormState:$d,useActionState:$d,useOptimistic:function(t){var n=Rn();n.memoizedState=n.baseState=t;var a={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return n.queue=a,n=Rc.bind(null,ne,!0,a),a.dispatch=n,[t,n]},useMemoCache:_c,useCacheRefresh:function(){return Rn().memoizedState=X0.bind(null,ne)},useEffectEvent:function(t){var n=Rn(),a={impl:t};return n.memoizedState=a,function(){if((xe&2)!==0)throw Error(r(440));return a.impl.apply(void 0,arguments)}}},Cc={readContext:mn,use:rl,useCallback:cp,useContext:mn,useEffect:yc,useImperativeHandle:up,useInsertionEffect:sp,useLayoutEffect:op,useMemo:fp,useReducer:sl,useRef:ip,useState:function(){return sl(zi)},useDebugValue:Ec,useDeferredValue:function(t,n){var a=je();return hp(a,we.memoizedState,t,n)},useTransition:function(){var t=sl(zi)[0],n=je().memoizedState;return[typeof t=="boolean"?t:Ys(t),n]},useSyncExternalStore:Gd,useId:gp,useHostTransitionStatus:Ac,useFormState:tp,useActionState:tp,useOptimistic:function(t,n){var a=je();return Yd(a,we,t,n)},useMemoCache:_c,useCacheRefresh:_p};Cc.useEffectEvent=rp;var yp={readContext:mn,use:rl,useCallback:cp,useContext:mn,useEffect:yc,useImperativeHandle:up,useInsertionEffect:sp,useLayoutEffect:op,useMemo:fp,useReducer:Sc,useRef:ip,useState:function(){return Sc(zi)},useDebugValue:Ec,useDeferredValue:function(t,n){var a=je();return we===null?Tc(a,t,n):hp(a,we.memoizedState,t,n)},useTransition:function(){var t=Sc(zi)[0],n=je().memoizedState;return[typeof t=="boolean"?t:Ys(t),n]},useSyncExternalStore:Gd,useId:gp,useHostTransitionStatus:Ac,useFormState:np,useActionState:np,useOptimistic:function(t,n){var a=je();return we!==null?Yd(a,we,t,n):(a.baseState=t,[t,a.queue.dispatch])},useMemoCache:_c,useCacheRefresh:_p};yp.useEffectEvent=rp;function wc(t,n,a,s){n=t.memoizedState,a=a(s,n),a=a==null?n:_({},n,a),t.memoizedState=a,t.lanes===0&&(t.updateQueue.baseState=a)}var Dc={enqueueSetState:function(t,n,a){t=t._reactInternals;var s=Yn(),u=fa(s);u.payload=n,a!=null&&(u.callback=a),n=ha(t,u,s),n!==null&&(Bn(n,t,s),Xs(n,t,s))},enqueueReplaceState:function(t,n,a){t=t._reactInternals;var s=Yn(),u=fa(s);u.tag=1,u.payload=n,a!=null&&(u.callback=a),n=ha(t,u,s),n!==null&&(Bn(n,t,s),Xs(n,t,s))},enqueueForceUpdate:function(t,n){t=t._reactInternals;var a=Yn(),s=fa(a);s.tag=2,n!=null&&(s.callback=n),n=ha(t,s,a),n!==null&&(Bn(n,t,a),Xs(n,t,a))}};function Ep(t,n,a,s,u,f,S){return t=t.stateNode,typeof t.shouldComponentUpdate=="function"?t.shouldComponentUpdate(s,f,S):n.prototype&&n.prototype.isPureReactComponent?!zs(a,s)||!zs(u,f):!0}function Tp(t,n,a,s){t=n.state,typeof n.componentWillReceiveProps=="function"&&n.componentWillReceiveProps(a,s),typeof n.UNSAFE_componentWillReceiveProps=="function"&&n.UNSAFE_componentWillReceiveProps(a,s),n.state!==t&&Dc.enqueueReplaceState(n,n.state,null)}function tr(t,n){var a=n;if("ref"in n){a={};for(var s in n)s!=="ref"&&(a[s]=n[s])}if(t=t.defaultProps){a===n&&(a=_({},a));for(var u in t)a[u]===void 0&&(a[u]=t[u])}return a}function bp(t){Go(t)}function Ap(t){console.error(t)}function Rp(t){Go(t)}function cl(t,n){try{var a=t.onUncaughtError;a(n.value,{componentStack:n.stack})}catch(s){setTimeout(function(){throw s})}}function Cp(t,n,a){try{var s=t.onCaughtError;s(a.value,{componentStack:a.stack,errorBoundary:n.tag===1?n.stateNode:null})}catch(u){setTimeout(function(){throw u})}}function Lc(t,n,a){return a=fa(a),a.tag=3,a.payload={element:null},a.callback=function(){cl(t,n)},a}function wp(t){return t=fa(t),t.tag=3,t}function Dp(t,n,a,s){var u=a.type.getDerivedStateFromError;if(typeof u=="function"){var f=s.value;t.payload=function(){return u(f)},t.callback=function(){Cp(n,a,s)}}var S=a.stateNode;S!==null&&typeof S.componentDidCatch=="function"&&(t.callback=function(){Cp(n,a,s),typeof u!="function"&&(va===null?va=new Set([this]):va.add(this));var E=s.stack;this.componentDidCatch(s.value,{componentStack:E!==null?E:""})})}function k0(t,n,a,s,u){if(a.flags|=32768,s!==null&&typeof s=="object"&&typeof s.then=="function"){if(n=a.alternate,n!==null&&Cr(n,a,u,!0),a=Xn.current,a!==null){switch(a.tag){case 31:case 13:return ii===null?yl():a.alternate===null&&ke===0&&(ke=3),a.flags&=-257,a.flags|=65536,a.lanes=u,s===Qo?a.flags|=16384:(n=a.updateQueue,n===null?a.updateQueue=new Set([s]):n.add(s),nf(t,s,u)),!1;case 22:return a.flags|=65536,s===Qo?a.flags|=16384:(n=a.updateQueue,n===null?(n={transitions:null,markerInstances:null,retryQueue:new Set([s])},a.updateQueue=n):(a=n.retryQueue,a===null?n.retryQueue=new Set([s]):a.add(s)),nf(t,s,u)),!1}throw Error(r(435,a.tag))}return nf(t,s,u),yl(),!1}if(me)return n=Xn.current,n!==null?((n.flags&65536)===0&&(n.flags|=256),n.flags|=65536,n.lanes=u,s!==Ku&&(t=Error(r(422),{cause:s}),Is($n(t,a)))):(s!==Ku&&(n=Error(r(423),{cause:s}),Is($n(n,a))),t=t.current.alternate,t.flags|=65536,u&=-u,t.lanes|=u,s=$n(s,a),u=Lc(t.stateNode,s,u),oc(t,u),ke!==4&&(ke=2)),!1;var f=Error(r(520),{cause:s});if(f=$n(f,a),io===null?io=[f]:io.push(f),ke!==4&&(ke=2),n===null)return!0;s=$n(s,a),a=n;do{switch(a.tag){case 3:return a.flags|=65536,t=u&-u,a.lanes|=t,t=Lc(a.stateNode,s,t),oc(a,t),!1;case 1:if(n=a.type,f=a.stateNode,(a.flags&128)===0&&(typeof n.getDerivedStateFromError=="function"||f!==null&&typeof f.componentDidCatch=="function"&&(va===null||!va.has(f))))return a.flags|=65536,u&=-u,a.lanes|=u,u=wp(u),Dp(u,t,a,s),oc(a,u),!1}a=a.return}while(a!==null);return!1}var Uc=Error(r(461)),en=!1;function gn(t,n,a,s){n.child=t===null?Od(n,null,a,s):Ja(n,t.child,a,s)}function Lp(t,n,a,s,u){a=a.render;var f=n.ref;if("ref"in s){var S={};for(var E in s)E!=="ref"&&(S[E]=s[E])}else S=s;return ja(n),s=dc(t,n,a,S,f,u),E=pc(),t!==null&&!en?(mc(t,n,u),Pi(t,n,u)):(me&&E&&ju(n),n.flags|=1,gn(t,n,s,u),n.child)}function Up(t,n,a,s,u){if(t===null){var f=a.type;return typeof f=="function"&&!ku(f)&&f.defaultProps===void 0&&a.compare===null?(n.tag=15,n.type=f,Np(t,n,f,s,u)):(t=ko(a.type,null,s,n,n.mode,u),t.ref=n.ref,t.return=n,n.child=t)}if(f=t.child,!Hc(t,u)){var S=f.memoizedProps;if(a=a.compare,a=a!==null?a:zs,a(S,s)&&t.ref===n.ref)return Pi(t,n,u)}return n.flags|=1,t=Di(f,s),t.ref=n.ref,t.return=n,n.child=t}function Np(t,n,a,s,u){if(t!==null){var f=t.memoizedProps;if(zs(f,s)&&t.ref===n.ref)if(en=!1,n.pendingProps=s=f,Hc(t,u))(t.flags&131072)!==0&&(en=!0);else return n.lanes=t.lanes,Pi(t,n,u)}return Nc(t,n,a,s,u)}function Op(t,n,a,s){var u=s.children,f=t!==null?t.memoizedState:null;if(t===null&&n.stateNode===null&&(n.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),s.mode==="hidden"){if((n.flags&128)!==0){if(f=f!==null?f.baseLanes|a:a,t!==null){for(s=n.child=t.child,u=0;s!==null;)u=u|s.lanes|s.childLanes,s=s.sibling;s=u&~f}else s=0,n.child=null;return zp(t,n,f,a,s)}if((a&536870912)!==0)n.memoizedState={baseLanes:0,cachePool:null},t!==null&&Zo(n,f!==null?f.cachePool:null),f!==null?Bd(n,f):uc(),Id(n);else return s=n.lanes=536870912,zp(t,n,f!==null?f.baseLanes|a:a,a,s)}else f!==null?(Zo(n,f.cachePool),Bd(n,f),pa(),n.memoizedState=null):(t!==null&&Zo(n,null),uc(),pa());return gn(t,n,u,a),n.child}function Ks(t,n){return t!==null&&t.tag===22||n.stateNode!==null||(n.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),n.sibling}function zp(t,n,a,s,u){var f=ic();return f=f===null?null:{parent:$e._currentValue,pool:f},n.memoizedState={baseLanes:a,cachePool:f},t!==null&&Zo(n,null),uc(),Id(n),t!==null&&Cr(t,n,s,!0),n.childLanes=u,null}function fl(t,n){return n=dl({mode:n.mode,children:n.children},t.mode),n.ref=t.ref,t.child=n,n.return=t,n}function Pp(t,n,a){return Ja(n,t.child,null,a),t=fl(n,n.pendingProps),t.flags|=2,Wn(n),n.memoizedState=null,t}function q0(t,n,a){var s=n.pendingProps,u=(n.flags&128)!==0;if(n.flags&=-129,t===null){if(me){if(s.mode==="hidden")return t=fl(n,s),n.lanes=536870912,Ks(null,t);if(fc(n),(t=Be)?(t=jm(t,ni),t=t!==null&&t.data==="&"?t:null,t!==null&&(n.memoizedState={dehydrated:t,treeContext:sa!==null?{id:Mi,overflow:yi}:null,retryLane:536870912,hydrationErrors:null},a=Sd(t),a.return=n,n.child=a,pn=n,Be=null)):t=null,t===null)throw la(n);return n.lanes=536870912,null}return fl(n,s)}var f=t.memoizedState;if(f!==null){var S=f.dehydrated;if(fc(n),u)if(n.flags&256)n.flags&=-257,n=Pp(t,n,a);else if(n.memoizedState!==null)n.child=t.child,n.flags|=128,n=null;else throw Error(r(558));else if(en||Cr(t,n,a,!1),u=(a&t.childLanes)!==0,en||u){if(s=Oe,s!==null&&(S=Ms(s,a),S!==0&&S!==f.retryLane))throw f.retryLane=S,Wa(t,S),Bn(s,t,S),Uc;yl(),n=Pp(t,n,a)}else t=f.treeContext,Be=ai(S.nextSibling),pn=n,me=!0,oa=null,ni=!1,t!==null&&yd(n,t),n=fl(n,s),n.flags|=4096;return n}return t=Di(t.child,{mode:s.mode,children:s.children}),t.ref=n.ref,n.child=t,t.return=n,t}function hl(t,n){var a=n.ref;if(a===null)t!==null&&t.ref!==null&&(n.flags|=4194816);else{if(typeof a!="function"&&typeof a!="object")throw Error(r(284));(t===null||t.ref!==a)&&(n.flags|=4194816)}}function Nc(t,n,a,s,u){return ja(n),a=dc(t,n,a,s,void 0,u),s=pc(),t!==null&&!en?(mc(t,n,u),Pi(t,n,u)):(me&&s&&ju(n),n.flags|=1,gn(t,n,a,u),n.child)}function Bp(t,n,a,s,u,f){return ja(n),n.updateQueue=null,a=Hd(n,s,a,u),Fd(t),s=pc(),t!==null&&!en?(mc(t,n,f),Pi(t,n,f)):(me&&s&&ju(n),n.flags|=1,gn(t,n,a,f),n.child)}function Ip(t,n,a,s,u){if(ja(n),n.stateNode===null){var f=Tr,S=a.contextType;typeof S=="object"&&S!==null&&(f=mn(S)),f=new a(s,f),n.memoizedState=f.state!==null&&f.state!==void 0?f.state:null,f.updater=Dc,n.stateNode=f,f._reactInternals=n,f=n.stateNode,f.props=s,f.state=n.memoizedState,f.refs={},rc(n),S=a.contextType,f.context=typeof S=="object"&&S!==null?mn(S):Tr,f.state=n.memoizedState,S=a.getDerivedStateFromProps,typeof S=="function"&&(wc(n,a,S,s),f.state=n.memoizedState),typeof a.getDerivedStateFromProps=="function"||typeof f.getSnapshotBeforeUpdate=="function"||typeof f.UNSAFE_componentWillMount!="function"&&typeof f.componentWillMount!="function"||(S=f.state,typeof f.componentWillMount=="function"&&f.componentWillMount(),typeof f.UNSAFE_componentWillMount=="function"&&f.UNSAFE_componentWillMount(),S!==f.state&&Dc.enqueueReplaceState(f,f.state,null),ks(n,s,f,u),Ws(),f.state=n.memoizedState),typeof f.componentDidMount=="function"&&(n.flags|=4194308),s=!0}else if(t===null){f=n.stateNode;var E=n.memoizedProps,I=tr(a,E);f.props=I;var Q=f.context,ct=a.contextType;S=Tr,typeof ct=="object"&&ct!==null&&(S=mn(ct));var pt=a.getDerivedStateFromProps;ct=typeof pt=="function"||typeof f.getSnapshotBeforeUpdate=="function",E=n.pendingProps!==E,ct||typeof f.UNSAFE_componentWillReceiveProps!="function"&&typeof f.componentWillReceiveProps!="function"||(E||Q!==S)&&Tp(n,f,s,S),ca=!1;var $=n.memoizedState;f.state=$,ks(n,s,f,u),Ws(),Q=n.memoizedState,E||$!==Q||ca?(typeof pt=="function"&&(wc(n,a,pt,s),Q=n.memoizedState),(I=ca||Ep(n,a,I,s,$,Q,S))?(ct||typeof f.UNSAFE_componentWillMount!="function"&&typeof f.componentWillMount!="function"||(typeof f.componentWillMount=="function"&&f.componentWillMount(),typeof f.UNSAFE_componentWillMount=="function"&&f.UNSAFE_componentWillMount()),typeof f.componentDidMount=="function"&&(n.flags|=4194308)):(typeof f.componentDidMount=="function"&&(n.flags|=4194308),n.memoizedProps=s,n.memoizedState=Q),f.props=s,f.state=Q,f.context=S,s=I):(typeof f.componentDidMount=="function"&&(n.flags|=4194308),s=!1)}else{f=n.stateNode,sc(t,n),S=n.memoizedProps,ct=tr(a,S),f.props=ct,pt=n.pendingProps,$=f.context,Q=a.contextType,I=Tr,typeof Q=="object"&&Q!==null&&(I=mn(Q)),E=a.getDerivedStateFromProps,(Q=typeof E=="function"||typeof f.getSnapshotBeforeUpdate=="function")||typeof f.UNSAFE_componentWillReceiveProps!="function"&&typeof f.componentWillReceiveProps!="function"||(S!==pt||$!==I)&&Tp(n,f,s,I),ca=!1,$=n.memoizedState,f.state=$,ks(n,s,f,u),Ws();var ot=n.memoizedState;S!==pt||$!==ot||ca||t!==null&&t.dependencies!==null&&Yo(t.dependencies)?(typeof E=="function"&&(wc(n,a,E,s),ot=n.memoizedState),(ct=ca||Ep(n,a,ct,s,$,ot,I)||t!==null&&t.dependencies!==null&&Yo(t.dependencies))?(Q||typeof f.UNSAFE_componentWillUpdate!="function"&&typeof f.componentWillUpdate!="function"||(typeof f.componentWillUpdate=="function"&&f.componentWillUpdate(s,ot,I),typeof f.UNSAFE_componentWillUpdate=="function"&&f.UNSAFE_componentWillUpdate(s,ot,I)),typeof f.componentDidUpdate=="function"&&(n.flags|=4),typeof f.getSnapshotBeforeUpdate=="function"&&(n.flags|=1024)):(typeof f.componentDidUpdate!="function"||S===t.memoizedProps&&$===t.memoizedState||(n.flags|=4),typeof f.getSnapshotBeforeUpdate!="function"||S===t.memoizedProps&&$===t.memoizedState||(n.flags|=1024),n.memoizedProps=s,n.memoizedState=ot),f.props=s,f.state=ot,f.context=I,s=ct):(typeof f.componentDidUpdate!="function"||S===t.memoizedProps&&$===t.memoizedState||(n.flags|=4),typeof f.getSnapshotBeforeUpdate!="function"||S===t.memoizedProps&&$===t.memoizedState||(n.flags|=1024),s=!1)}return f=s,hl(t,n),s=(n.flags&128)!==0,f||s?(f=n.stateNode,a=s&&typeof a.getDerivedStateFromError!="function"?null:f.render(),n.flags|=1,t!==null&&s?(n.child=Ja(n,t.child,null,u),n.child=Ja(n,null,a,u)):gn(t,n,a,u),n.memoizedState=f.state,t=n.child):t=Pi(t,n,u),t}function Fp(t,n,a,s){return qa(),n.flags|=256,gn(t,n,a,s),n.child}var Oc={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function zc(t){return{baseLanes:t,cachePool:Cd()}}function Pc(t,n,a){return t=t!==null?t.childLanes&~a:0,n&&(t|=qn),t}function Hp(t,n,a){var s=n.pendingProps,u=!1,f=(n.flags&128)!==0,S;if((S=f)||(S=t!==null&&t.memoizedState===null?!1:(Ye.current&2)!==0),S&&(u=!0,n.flags&=-129),S=(n.flags&32)!==0,n.flags&=-33,t===null){if(me){if(u?da(n):pa(),(t=Be)?(t=jm(t,ni),t=t!==null&&t.data!=="&"?t:null,t!==null&&(n.memoizedState={dehydrated:t,treeContext:sa!==null?{id:Mi,overflow:yi}:null,retryLane:536870912,hydrationErrors:null},a=Sd(t),a.return=n,n.child=a,pn=n,Be=null)):t=null,t===null)throw la(n);return Sf(t)?n.lanes=32:n.lanes=536870912,null}var E=s.children;return s=s.fallback,u?(pa(),u=n.mode,E=dl({mode:"hidden",children:E},u),s=ka(s,u,a,null),E.return=n,s.return=n,E.sibling=s,n.child=E,s=n.child,s.memoizedState=zc(a),s.childLanes=Pc(t,S,a),n.memoizedState=Oc,Ks(null,s)):(da(n),Bc(n,E))}var I=t.memoizedState;if(I!==null&&(E=I.dehydrated,E!==null)){if(f)n.flags&256?(da(n),n.flags&=-257,n=Ic(t,n,a)):n.memoizedState!==null?(pa(),n.child=t.child,n.flags|=128,n=null):(pa(),E=s.fallback,u=n.mode,s=dl({mode:"visible",children:s.children},u),E=ka(E,u,a,null),E.flags|=2,s.return=n,E.return=n,s.sibling=E,n.child=s,Ja(n,t.child,null,a),s=n.child,s.memoizedState=zc(a),s.childLanes=Pc(t,S,a),n.memoizedState=Oc,n=Ks(null,s));else if(da(n),Sf(E)){if(S=E.nextSibling&&E.nextSibling.dataset,S)var Q=S.dgst;S=Q,s=Error(r(419)),s.stack="",s.digest=S,Is({value:s,source:null,stack:null}),n=Ic(t,n,a)}else if(en||Cr(t,n,a,!1),S=(a&t.childLanes)!==0,en||S){if(S=Oe,S!==null&&(s=Ms(S,a),s!==0&&s!==I.retryLane))throw I.retryLane=s,Wa(t,s),Bn(S,t,s),Uc;vf(E)||yl(),n=Ic(t,n,a)}else vf(E)?(n.flags|=192,n.child=t.child,n=null):(t=I.treeContext,Be=ai(E.nextSibling),pn=n,me=!0,oa=null,ni=!1,t!==null&&yd(n,t),n=Bc(n,s.children),n.flags|=4096);return n}return u?(pa(),E=s.fallback,u=n.mode,I=t.child,Q=I.sibling,s=Di(I,{mode:"hidden",children:s.children}),s.subtreeFlags=I.subtreeFlags&65011712,Q!==null?E=Di(Q,E):(E=ka(E,u,a,null),E.flags|=2),E.return=n,s.return=n,s.sibling=E,n.child=s,Ks(null,s),s=n.child,E=t.child.memoizedState,E===null?E=zc(a):(u=E.cachePool,u!==null?(I=$e._currentValue,u=u.parent!==I?{parent:I,pool:I}:u):u=Cd(),E={baseLanes:E.baseLanes|a,cachePool:u}),s.memoizedState=E,s.childLanes=Pc(t,S,a),n.memoizedState=Oc,Ks(t.child,s)):(da(n),a=t.child,t=a.sibling,a=Di(a,{mode:"visible",children:s.children}),a.return=n,a.sibling=null,t!==null&&(S=n.deletions,S===null?(n.deletions=[t],n.flags|=16):S.push(t)),n.child=a,n.memoizedState=null,a)}function Bc(t,n){return n=dl({mode:"visible",children:n},t.mode),n.return=t,t.child=n}function dl(t,n){return t=Vn(22,t,null,n),t.lanes=0,t}function Ic(t,n,a){return Ja(n,t.child,null,a),t=Bc(n,n.pendingProps.children),t.flags|=2,n.memoizedState=null,t}function Gp(t,n,a){t.lanes|=n;var s=t.alternate;s!==null&&(s.lanes|=n),$u(t.return,n,a)}function Fc(t,n,a,s,u,f){var S=t.memoizedState;S===null?t.memoizedState={isBackwards:n,rendering:null,renderingStartTime:0,last:s,tail:a,tailMode:u,treeForkCount:f}:(S.isBackwards=n,S.rendering=null,S.renderingStartTime=0,S.last=s,S.tail=a,S.tailMode=u,S.treeForkCount=f)}function Vp(t,n,a){var s=n.pendingProps,u=s.revealOrder,f=s.tail;s=s.children;var S=Ye.current,E=(S&2)!==0;if(E?(S=S&1|2,n.flags|=128):S&=1,G(Ye,S),gn(t,n,s,a),s=me?Bs:0,!E&&t!==null&&(t.flags&128)!==0)t:for(t=n.child;t!==null;){if(t.tag===13)t.memoizedState!==null&&Gp(t,a,n);else if(t.tag===19)Gp(t,a,n);else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===n)break t;for(;t.sibling===null;){if(t.return===null||t.return===n)break t;t=t.return}t.sibling.return=t.return,t=t.sibling}switch(u){case"forwards":for(a=n.child,u=null;a!==null;)t=a.alternate,t!==null&&el(t)===null&&(u=a),a=a.sibling;a=u,a===null?(u=n.child,n.child=null):(u=a.sibling,a.sibling=null),Fc(n,!1,u,a,f,s);break;case"backwards":case"unstable_legacy-backwards":for(a=null,u=n.child,n.child=null;u!==null;){if(t=u.alternate,t!==null&&el(t)===null){n.child=u;break}t=u.sibling,u.sibling=a,a=u,u=t}Fc(n,!0,a,null,f,s);break;case"together":Fc(n,!1,null,null,void 0,s);break;default:n.memoizedState=null}return n.child}function Pi(t,n,a){if(t!==null&&(n.dependencies=t.dependencies),_a|=n.lanes,(a&n.childLanes)===0)if(t!==null){if(Cr(t,n,a,!1),(a&n.childLanes)===0)return null}else return null;if(t!==null&&n.child!==t.child)throw Error(r(153));if(n.child!==null){for(t=n.child,a=Di(t,t.pendingProps),n.child=a,a.return=n;t.sibling!==null;)t=t.sibling,a=a.sibling=Di(t,t.pendingProps),a.return=n;a.sibling=null}return n.child}function Hc(t,n){return(t.lanes&n)!==0?!0:(t=t.dependencies,!!(t!==null&&Yo(t)))}function Y0(t,n,a){switch(n.tag){case 3:It(n,n.stateNode.containerInfo),ua(n,$e,t.memoizedState.cache),qa();break;case 27:case 5:kt(n);break;case 4:It(n,n.stateNode.containerInfo);break;case 10:ua(n,n.type,n.memoizedProps.value);break;case 31:if(n.memoizedState!==null)return n.flags|=128,fc(n),null;break;case 13:var s=n.memoizedState;if(s!==null)return s.dehydrated!==null?(da(n),n.flags|=128,null):(a&n.child.childLanes)!==0?Hp(t,n,a):(da(n),t=Pi(t,n,a),t!==null?t.sibling:null);da(n);break;case 19:var u=(t.flags&128)!==0;if(s=(a&n.childLanes)!==0,s||(Cr(t,n,a,!1),s=(a&n.childLanes)!==0),u){if(s)return Vp(t,n,a);n.flags|=128}if(u=n.memoizedState,u!==null&&(u.rendering=null,u.tail=null,u.lastEffect=null),G(Ye,Ye.current),s)break;return null;case 22:return n.lanes=0,Op(t,n,a,n.pendingProps);case 24:ua(n,$e,t.memoizedState.cache)}return Pi(t,n,a)}function Xp(t,n,a){if(t!==null)if(t.memoizedProps!==n.pendingProps)en=!0;else{if(!Hc(t,a)&&(n.flags&128)===0)return en=!1,Y0(t,n,a);en=(t.flags&131072)!==0}else en=!1,me&&(n.flags&1048576)!==0&&Md(n,Bs,n.index);switch(n.lanes=0,n.tag){case 16:t:{var s=n.pendingProps;if(t=Ka(n.elementType),n.type=t,typeof t=="function")ku(t)?(s=tr(t,s),n.tag=1,n=Ip(null,n,t,s,a)):(n.tag=0,n=Nc(null,n,t,s,a));else{if(t!=null){var u=t.$$typeof;if(u===z){n.tag=11,n=Lp(null,n,t,s,a);break t}else if(u===O){n.tag=14,n=Up(null,n,t,s,a);break t}}throw n=X(t)||t,Error(r(306,n,""))}}return n;case 0:return Nc(t,n,n.type,n.pendingProps,a);case 1:return s=n.type,u=tr(s,n.pendingProps),Ip(t,n,s,u,a);case 3:t:{if(It(n,n.stateNode.containerInfo),t===null)throw Error(r(387));s=n.pendingProps;var f=n.memoizedState;u=f.element,sc(t,n),ks(n,s,null,a);var S=n.memoizedState;if(s=S.cache,ua(n,$e,s),s!==f.cache&&tc(n,[$e],a,!0),Ws(),s=S.element,f.isDehydrated)if(f={element:s,isDehydrated:!1,cache:S.cache},n.updateQueue.baseState=f,n.memoizedState=f,n.flags&256){n=Fp(t,n,s,a);break t}else if(s!==u){u=$n(Error(r(424)),n),Is(u),n=Fp(t,n,s,a);break t}else for(t=n.stateNode.containerInfo,t.nodeType===9?t=t.body:t=t.nodeName==="HTML"?t.ownerDocument.body:t,Be=ai(t.firstChild),pn=n,me=!0,oa=null,ni=!0,a=Od(n,null,s,a),n.child=a;a;)a.flags=a.flags&-3|4096,a=a.sibling;else{if(qa(),s===u){n=Pi(t,n,a);break t}gn(t,n,s,a)}n=n.child}return n;case 26:return hl(t,n),t===null?(a=tg(n.type,null,n.pendingProps,null))?n.memoizedState=a:me||(a=n.type,t=n.pendingProps,s=wl(xt.current).createElement(a),s[Ze]=n,s[Sn]=t,_n(s,a,t),Bt(s),n.stateNode=s):n.memoizedState=tg(n.type,t.memoizedProps,n.pendingProps,t.memoizedState),null;case 27:return kt(n),t===null&&me&&(s=n.stateNode=Qm(n.type,n.pendingProps,xt.current),pn=n,ni=!0,u=Be,ya(n.type)?(xf=u,Be=ai(s.firstChild)):Be=u),gn(t,n,n.pendingProps.children,a),hl(t,n),t===null&&(n.flags|=4194304),n.child;case 5:return t===null&&me&&((u=s=Be)&&(s=ES(s,n.type,n.pendingProps,ni),s!==null?(n.stateNode=s,pn=n,Be=ai(s.firstChild),ni=!1,u=!0):u=!1),u||la(n)),kt(n),u=n.type,f=n.pendingProps,S=t!==null?t.memoizedProps:null,s=f.children,mf(u,f)?s=null:S!==null&&mf(u,S)&&(n.flags|=32),n.memoizedState!==null&&(u=dc(t,n,I0,null,null,a),fo._currentValue=u),hl(t,n),gn(t,n,s,a),n.child;case 6:return t===null&&me&&((t=a=Be)&&(a=TS(a,n.pendingProps,ni),a!==null?(n.stateNode=a,pn=n,Be=null,t=!0):t=!1),t||la(n)),null;case 13:return Hp(t,n,a);case 4:return It(n,n.stateNode.containerInfo),s=n.pendingProps,t===null?n.child=Ja(n,null,s,a):gn(t,n,s,a),n.child;case 11:return Lp(t,n,n.type,n.pendingProps,a);case 7:return gn(t,n,n.pendingProps,a),n.child;case 8:return gn(t,n,n.pendingProps.children,a),n.child;case 12:return gn(t,n,n.pendingProps.children,a),n.child;case 10:return s=n.pendingProps,ua(n,n.type,s.value),gn(t,n,s.children,a),n.child;case 9:return u=n.type._context,s=n.pendingProps.children,ja(n),u=mn(u),s=s(u),n.flags|=1,gn(t,n,s,a),n.child;case 14:return Up(t,n,n.type,n.pendingProps,a);case 15:return Np(t,n,n.type,n.pendingProps,a);case 19:return Vp(t,n,a);case 31:return q0(t,n,a);case 22:return Op(t,n,a,n.pendingProps);case 24:return ja(n),s=mn($e),t===null?(u=ic(),u===null&&(u=Oe,f=ec(),u.pooledCache=f,f.refCount++,f!==null&&(u.pooledCacheLanes|=a),u=f),n.memoizedState={parent:s,cache:u},rc(n),ua(n,$e,u)):((t.lanes&a)!==0&&(sc(t,n),ks(n,null,null,a),Ws()),u=t.memoizedState,f=n.memoizedState,u.parent!==s?(u={parent:s,cache:s},n.memoizedState=u,n.lanes===0&&(n.memoizedState=n.updateQueue.baseState=u),ua(n,$e,s)):(s=f.cache,ua(n,$e,s),s!==u.cache&&tc(n,[$e],a,!0))),gn(t,n,n.pendingProps.children,a),n.child;case 29:throw n.pendingProps}throw Error(r(156,n.tag))}function Bi(t){t.flags|=4}function Gc(t,n,a,s,u){if((n=(t.mode&32)!==0)&&(n=!1),n){if(t.flags|=16777216,(u&335544128)===u)if(t.stateNode.complete)t.flags|=8192;else if(gm())t.flags|=8192;else throw Qa=Qo,ac}else t.flags&=-16777217}function Wp(t,n){if(n.type!=="stylesheet"||(n.state.loading&4)!==0)t.flags&=-16777217;else if(t.flags|=16777216,!rg(n))if(gm())t.flags|=8192;else throw Qa=Qo,ac}function pl(t,n){n!==null&&(t.flags|=4),t.flags&16384&&(n=t.tag!==22?Ee():536870912,t.lanes|=n,Hr|=n)}function Qs(t,n){if(!me)switch(t.tailMode){case"hidden":n=t.tail;for(var a=null;n!==null;)n.alternate!==null&&(a=n),n=n.sibling;a===null?t.tail=null:a.sibling=null;break;case"collapsed":a=t.tail;for(var s=null;a!==null;)a.alternate!==null&&(s=a),a=a.sibling;s===null?n||t.tail===null?t.tail=null:t.tail.sibling=null:s.sibling=null}}function Ie(t){var n=t.alternate!==null&&t.alternate.child===t.child,a=0,s=0;if(n)for(var u=t.child;u!==null;)a|=u.lanes|u.childLanes,s|=u.subtreeFlags&65011712,s|=u.flags&65011712,u.return=t,u=u.sibling;else for(u=t.child;u!==null;)a|=u.lanes|u.childLanes,s|=u.subtreeFlags,s|=u.flags,u.return=t,u=u.sibling;return t.subtreeFlags|=s,t.childLanes=a,n}function j0(t,n,a){var s=n.pendingProps;switch(Zu(n),n.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return Ie(n),null;case 1:return Ie(n),null;case 3:return a=n.stateNode,s=null,t!==null&&(s=t.memoizedState.cache),n.memoizedState.cache!==s&&(n.flags|=2048),Ni($e),Nt(),a.pendingContext&&(a.context=a.pendingContext,a.pendingContext=null),(t===null||t.child===null)&&(Rr(n)?Bi(n):t===null||t.memoizedState.isDehydrated&&(n.flags&256)===0||(n.flags|=1024,Qu())),Ie(n),null;case 26:var u=n.type,f=n.memoizedState;return t===null?(Bi(n),f!==null?(Ie(n),Wp(n,f)):(Ie(n),Gc(n,u,null,s,a))):f?f!==t.memoizedState?(Bi(n),Ie(n),Wp(n,f)):(Ie(n),n.flags&=-16777217):(t=t.memoizedProps,t!==s&&Bi(n),Ie(n),Gc(n,u,t,s,a)),null;case 27:if(ue(n),a=xt.current,u=n.type,t!==null&&n.stateNode!=null)t.memoizedProps!==s&&Bi(n);else{if(!s){if(n.stateNode===null)throw Error(r(166));return Ie(n),null}t=K.current,Rr(n)?Ed(n):(t=Qm(u,s,a),n.stateNode=t,Bi(n))}return Ie(n),null;case 5:if(ue(n),u=n.type,t!==null&&n.stateNode!=null)t.memoizedProps!==s&&Bi(n);else{if(!s){if(n.stateNode===null)throw Error(r(166));return Ie(n),null}if(f=K.current,Rr(n))Ed(n);else{var S=wl(xt.current);switch(f){case 1:f=S.createElementNS("http://www.w3.org/2000/svg",u);break;case 2:f=S.createElementNS("http://www.w3.org/1998/Math/MathML",u);break;default:switch(u){case"svg":f=S.createElementNS("http://www.w3.org/2000/svg",u);break;case"math":f=S.createElementNS("http://www.w3.org/1998/Math/MathML",u);break;case"script":f=S.createElement("div"),f.innerHTML="<script><\/script>",f=f.removeChild(f.firstChild);break;case"select":f=typeof s.is=="string"?S.createElement("select",{is:s.is}):S.createElement("select"),s.multiple?f.multiple=!0:s.size&&(f.size=s.size);break;default:f=typeof s.is=="string"?S.createElement(u,{is:s.is}):S.createElement(u)}}f[Ze]=n,f[Sn]=s;t:for(S=n.child;S!==null;){if(S.tag===5||S.tag===6)f.appendChild(S.stateNode);else if(S.tag!==4&&S.tag!==27&&S.child!==null){S.child.return=S,S=S.child;continue}if(S===n)break t;for(;S.sibling===null;){if(S.return===null||S.return===n)break t;S=S.return}S.sibling.return=S.return,S=S.sibling}n.stateNode=f;t:switch(_n(f,u,s),u){case"button":case"input":case"select":case"textarea":s=!!s.autoFocus;break t;case"img":s=!0;break t;default:s=!1}s&&Bi(n)}}return Ie(n),Gc(n,n.type,t===null?null:t.memoizedProps,n.pendingProps,a),null;case 6:if(t&&n.stateNode!=null)t.memoizedProps!==s&&Bi(n);else{if(typeof s!="string"&&n.stateNode===null)throw Error(r(166));if(t=xt.current,Rr(n)){if(t=n.stateNode,a=n.memoizedProps,s=null,u=pn,u!==null)switch(u.tag){case 27:case 5:s=u.memoizedProps}t[Ze]=n,t=!!(t.nodeValue===a||s!==null&&s.suppressHydrationWarning===!0||Hm(t.nodeValue,a)),t||la(n,!0)}else t=wl(t).createTextNode(s),t[Ze]=n,n.stateNode=t}return Ie(n),null;case 31:if(a=n.memoizedState,t===null||t.memoizedState!==null){if(s=Rr(n),a!==null){if(t===null){if(!s)throw Error(r(318));if(t=n.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(r(557));t[Ze]=n}else qa(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;Ie(n),t=!1}else a=Qu(),t!==null&&t.memoizedState!==null&&(t.memoizedState.hydrationErrors=a),t=!0;if(!t)return n.flags&256?(Wn(n),n):(Wn(n),null);if((n.flags&128)!==0)throw Error(r(558))}return Ie(n),null;case 13:if(s=n.memoizedState,t===null||t.memoizedState!==null&&t.memoizedState.dehydrated!==null){if(u=Rr(n),s!==null&&s.dehydrated!==null){if(t===null){if(!u)throw Error(r(318));if(u=n.memoizedState,u=u!==null?u.dehydrated:null,!u)throw Error(r(317));u[Ze]=n}else qa(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;Ie(n),u=!1}else u=Qu(),t!==null&&t.memoizedState!==null&&(t.memoizedState.hydrationErrors=u),u=!0;if(!u)return n.flags&256?(Wn(n),n):(Wn(n),null)}return Wn(n),(n.flags&128)!==0?(n.lanes=a,n):(a=s!==null,t=t!==null&&t.memoizedState!==null,a&&(s=n.child,u=null,s.alternate!==null&&s.alternate.memoizedState!==null&&s.alternate.memoizedState.cachePool!==null&&(u=s.alternate.memoizedState.cachePool.pool),f=null,s.memoizedState!==null&&s.memoizedState.cachePool!==null&&(f=s.memoizedState.cachePool.pool),f!==u&&(s.flags|=2048)),a!==t&&a&&(n.child.flags|=8192),pl(n,n.updateQueue),Ie(n),null);case 4:return Nt(),t===null&&cf(n.stateNode.containerInfo),Ie(n),null;case 10:return Ni(n.type),Ie(n),null;case 19:if(W(Ye),s=n.memoizedState,s===null)return Ie(n),null;if(u=(n.flags&128)!==0,f=s.rendering,f===null)if(u)Qs(s,!1);else{if(ke!==0||t!==null&&(t.flags&128)!==0)for(t=n.child;t!==null;){if(f=el(t),f!==null){for(n.flags|=128,Qs(s,!1),t=f.updateQueue,n.updateQueue=t,pl(n,t),n.subtreeFlags=0,t=a,a=n.child;a!==null;)vd(a,t),a=a.sibling;return G(Ye,Ye.current&1|2),me&&Li(n,s.treeForkCount),n.child}t=t.sibling}s.tail!==null&&gt()>Sl&&(n.flags|=128,u=!0,Qs(s,!1),n.lanes=4194304)}else{if(!u)if(t=el(f),t!==null){if(n.flags|=128,u=!0,t=t.updateQueue,n.updateQueue=t,pl(n,t),Qs(s,!0),s.tail===null&&s.tailMode==="hidden"&&!f.alternate&&!me)return Ie(n),null}else 2*gt()-s.renderingStartTime>Sl&&a!==536870912&&(n.flags|=128,u=!0,Qs(s,!1),n.lanes=4194304);s.isBackwards?(f.sibling=n.child,n.child=f):(t=s.last,t!==null?t.sibling=f:n.child=f,s.last=f)}return s.tail!==null?(t=s.tail,s.rendering=t,s.tail=t.sibling,s.renderingStartTime=gt(),t.sibling=null,a=Ye.current,G(Ye,u?a&1|2:a&1),me&&Li(n,s.treeForkCount),t):(Ie(n),null);case 22:case 23:return Wn(n),cc(),s=n.memoizedState!==null,t!==null?t.memoizedState!==null!==s&&(n.flags|=8192):s&&(n.flags|=8192),s?(a&536870912)!==0&&(n.flags&128)===0&&(Ie(n),n.subtreeFlags&6&&(n.flags|=8192)):Ie(n),a=n.updateQueue,a!==null&&pl(n,a.retryQueue),a=null,t!==null&&t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(a=t.memoizedState.cachePool.pool),s=null,n.memoizedState!==null&&n.memoizedState.cachePool!==null&&(s=n.memoizedState.cachePool.pool),s!==a&&(n.flags|=2048),t!==null&&W(Za),null;case 24:return a=null,t!==null&&(a=t.memoizedState.cache),n.memoizedState.cache!==a&&(n.flags|=2048),Ni($e),Ie(n),null;case 25:return null;case 30:return null}throw Error(r(156,n.tag))}function Z0(t,n){switch(Zu(n),n.tag){case 1:return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 3:return Ni($e),Nt(),t=n.flags,(t&65536)!==0&&(t&128)===0?(n.flags=t&-65537|128,n):null;case 26:case 27:case 5:return ue(n),null;case 31:if(n.memoizedState!==null){if(Wn(n),n.alternate===null)throw Error(r(340));qa()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 13:if(Wn(n),t=n.memoizedState,t!==null&&t.dehydrated!==null){if(n.alternate===null)throw Error(r(340));qa()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 19:return W(Ye),null;case 4:return Nt(),null;case 10:return Ni(n.type),null;case 22:case 23:return Wn(n),cc(),t!==null&&W(Za),t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 24:return Ni($e),null;case 25:return null;default:return null}}function kp(t,n){switch(Zu(n),n.tag){case 3:Ni($e),Nt();break;case 26:case 27:case 5:ue(n);break;case 4:Nt();break;case 31:n.memoizedState!==null&&Wn(n);break;case 13:Wn(n);break;case 19:W(Ye);break;case 10:Ni(n.type);break;case 22:case 23:Wn(n),cc(),t!==null&&W(Za);break;case 24:Ni($e)}}function Js(t,n){try{var a=n.updateQueue,s=a!==null?a.lastEffect:null;if(s!==null){var u=s.next;a=u;do{if((a.tag&t)===t){s=void 0;var f=a.create,S=a.inst;s=f(),S.destroy=s}a=a.next}while(a!==u)}}catch(E){Ae(n,n.return,E)}}function ma(t,n,a){try{var s=n.updateQueue,u=s!==null?s.lastEffect:null;if(u!==null){var f=u.next;s=f;do{if((s.tag&t)===t){var S=s.inst,E=S.destroy;if(E!==void 0){S.destroy=void 0,u=n;var I=a,Q=E;try{Q()}catch(ct){Ae(u,I,ct)}}}s=s.next}while(s!==f)}}catch(ct){Ae(n,n.return,ct)}}function qp(t){var n=t.updateQueue;if(n!==null){var a=t.stateNode;try{Pd(n,a)}catch(s){Ae(t,t.return,s)}}}function Yp(t,n,a){a.props=tr(t.type,t.memoizedProps),a.state=t.memoizedState;try{a.componentWillUnmount()}catch(s){Ae(t,n,s)}}function $s(t,n){try{var a=t.ref;if(a!==null){switch(t.tag){case 26:case 27:case 5:var s=t.stateNode;break;case 30:s=t.stateNode;break;default:s=t.stateNode}typeof a=="function"?t.refCleanup=a(s):a.current=s}}catch(u){Ae(t,n,u)}}function Ei(t,n){var a=t.ref,s=t.refCleanup;if(a!==null)if(typeof s=="function")try{s()}catch(u){Ae(t,n,u)}finally{t.refCleanup=null,t=t.alternate,t!=null&&(t.refCleanup=null)}else if(typeof a=="function")try{a(null)}catch(u){Ae(t,n,u)}else a.current=null}function jp(t){var n=t.type,a=t.memoizedProps,s=t.stateNode;try{t:switch(n){case"button":case"input":case"select":case"textarea":a.autoFocus&&s.focus();break t;case"img":a.src?s.src=a.src:a.srcSet&&(s.srcset=a.srcSet)}}catch(u){Ae(t,t.return,u)}}function Vc(t,n,a){try{var s=t.stateNode;_S(s,t.type,a,n),s[Sn]=n}catch(u){Ae(t,t.return,u)}}function Zp(t){return t.tag===5||t.tag===3||t.tag===26||t.tag===27&&ya(t.type)||t.tag===4}function Xc(t){t:for(;;){for(;t.sibling===null;){if(t.return===null||Zp(t.return))return null;t=t.return}for(t.sibling.return=t.return,t=t.sibling;t.tag!==5&&t.tag!==6&&t.tag!==18;){if(t.tag===27&&ya(t.type)||t.flags&2||t.child===null||t.tag===4)continue t;t.child.return=t,t=t.child}if(!(t.flags&2))return t.stateNode}}function Wc(t,n,a){var s=t.tag;if(s===5||s===6)t=t.stateNode,n?(a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a).insertBefore(t,n):(n=a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a,n.appendChild(t),a=a._reactRootContainer,a!=null||n.onclick!==null||(n.onclick=Ci));else if(s!==4&&(s===27&&ya(t.type)&&(a=t.stateNode,n=null),t=t.child,t!==null))for(Wc(t,n,a),t=t.sibling;t!==null;)Wc(t,n,a),t=t.sibling}function ml(t,n,a){var s=t.tag;if(s===5||s===6)t=t.stateNode,n?a.insertBefore(t,n):a.appendChild(t);else if(s!==4&&(s===27&&ya(t.type)&&(a=t.stateNode),t=t.child,t!==null))for(ml(t,n,a),t=t.sibling;t!==null;)ml(t,n,a),t=t.sibling}function Kp(t){var n=t.stateNode,a=t.memoizedProps;try{for(var s=t.type,u=n.attributes;u.length;)n.removeAttributeNode(u[0]);_n(n,s,a),n[Ze]=t,n[Sn]=a}catch(f){Ae(t,t.return,f)}}var Ii=!1,nn=!1,kc=!1,Qp=typeof WeakSet=="function"?WeakSet:Set,fn=null;function K0(t,n){if(t=t.containerInfo,df=Pl,t=ud(t),Iu(t)){if("selectionStart"in t)var a={start:t.selectionStart,end:t.selectionEnd};else t:{a=(a=t.ownerDocument)&&a.defaultView||window;var s=a.getSelection&&a.getSelection();if(s&&s.rangeCount!==0){a=s.anchorNode;var u=s.anchorOffset,f=s.focusNode;s=s.focusOffset;try{a.nodeType,f.nodeType}catch{a=null;break t}var S=0,E=-1,I=-1,Q=0,ct=0,pt=t,$=null;e:for(;;){for(var ot;pt!==a||u!==0&&pt.nodeType!==3||(E=S+u),pt!==f||s!==0&&pt.nodeType!==3||(I=S+s),pt.nodeType===3&&(S+=pt.nodeValue.length),(ot=pt.firstChild)!==null;)$=pt,pt=ot;for(;;){if(pt===t)break e;if($===a&&++Q===u&&(E=S),$===f&&++ct===s&&(I=S),(ot=pt.nextSibling)!==null)break;pt=$,$=pt.parentNode}pt=ot}a=E===-1||I===-1?null:{start:E,end:I}}else a=null}a=a||{start:0,end:0}}else a=null;for(pf={focusedElem:t,selectionRange:a},Pl=!1,fn=n;fn!==null;)if(n=fn,t=n.child,(n.subtreeFlags&1028)!==0&&t!==null)t.return=n,fn=t;else for(;fn!==null;){switch(n=fn,f=n.alternate,t=n.flags,n.tag){case 0:if((t&4)!==0&&(t=n.updateQueue,t=t!==null?t.events:null,t!==null))for(a=0;a<t.length;a++)u=t[a],u.ref.impl=u.nextImpl;break;case 11:case 15:break;case 1:if((t&1024)!==0&&f!==null){t=void 0,a=n,u=f.memoizedProps,f=f.memoizedState,s=a.stateNode;try{var Lt=tr(a.type,u);t=s.getSnapshotBeforeUpdate(Lt,f),s.__reactInternalSnapshotBeforeUpdate=t}catch(Zt){Ae(a,a.return,Zt)}}break;case 3:if((t&1024)!==0){if(t=n.stateNode.containerInfo,a=t.nodeType,a===9)_f(t);else if(a===1)switch(t.nodeName){case"HEAD":case"HTML":case"BODY":_f(t);break;default:t.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;default:if((t&1024)!==0)throw Error(r(163))}if(t=n.sibling,t!==null){t.return=n.return,fn=t;break}fn=n.return}}function Jp(t,n,a){var s=a.flags;switch(a.tag){case 0:case 11:case 15:Hi(t,a),s&4&&Js(5,a);break;case 1:if(Hi(t,a),s&4)if(t=a.stateNode,n===null)try{t.componentDidMount()}catch(S){Ae(a,a.return,S)}else{var u=tr(a.type,n.memoizedProps);n=n.memoizedState;try{t.componentDidUpdate(u,n,t.__reactInternalSnapshotBeforeUpdate)}catch(S){Ae(a,a.return,S)}}s&64&&qp(a),s&512&&$s(a,a.return);break;case 3:if(Hi(t,a),s&64&&(t=a.updateQueue,t!==null)){if(n=null,a.child!==null)switch(a.child.tag){case 27:case 5:n=a.child.stateNode;break;case 1:n=a.child.stateNode}try{Pd(t,n)}catch(S){Ae(a,a.return,S)}}break;case 27:n===null&&s&4&&Kp(a);case 26:case 5:Hi(t,a),n===null&&s&4&&jp(a),s&512&&$s(a,a.return);break;case 12:Hi(t,a);break;case 31:Hi(t,a),s&4&&em(t,a);break;case 13:Hi(t,a),s&4&&nm(t,a),s&64&&(t=a.memoizedState,t!==null&&(t=t.dehydrated,t!==null&&(a=rS.bind(null,a),bS(t,a))));break;case 22:if(s=a.memoizedState!==null||Ii,!s){n=n!==null&&n.memoizedState!==null||nn,u=Ii;var f=nn;Ii=s,(nn=n)&&!f?Gi(t,a,(a.subtreeFlags&8772)!==0):Hi(t,a),Ii=u,nn=f}break;case 30:break;default:Hi(t,a)}}function $p(t){var n=t.alternate;n!==null&&(t.alternate=null,$p(n)),t.child=null,t.deletions=null,t.sibling=null,t.tag===5&&(n=t.stateNode,n!==null&&nt(n)),t.stateNode=null,t.return=null,t.dependencies=null,t.memoizedProps=null,t.memoizedState=null,t.pendingProps=null,t.stateNode=null,t.updateQueue=null}var Ge=null,Nn=!1;function Fi(t,n,a){for(a=a.child;a!==null;)tm(t,n,a),a=a.sibling}function tm(t,n,a){if(Dt&&typeof Dt.onCommitFiberUnmount=="function")try{Dt.onCommitFiberUnmount(Kt,a)}catch{}switch(a.tag){case 26:nn||Ei(a,n),Fi(t,n,a),a.memoizedState?a.memoizedState.count--:a.stateNode&&(a=a.stateNode,a.parentNode.removeChild(a));break;case 27:nn||Ei(a,n);var s=Ge,u=Nn;ya(a.type)&&(Ge=a.stateNode,Nn=!1),Fi(t,n,a),lo(a.stateNode),Ge=s,Nn=u;break;case 5:nn||Ei(a,n);case 6:if(s=Ge,u=Nn,Ge=null,Fi(t,n,a),Ge=s,Nn=u,Ge!==null)if(Nn)try{(Ge.nodeType===9?Ge.body:Ge.nodeName==="HTML"?Ge.ownerDocument.body:Ge).removeChild(a.stateNode)}catch(f){Ae(a,n,f)}else try{Ge.removeChild(a.stateNode)}catch(f){Ae(a,n,f)}break;case 18:Ge!==null&&(Nn?(t=Ge,qm(t.nodeType===9?t.body:t.nodeName==="HTML"?t.ownerDocument.body:t,a.stateNode),jr(t)):qm(Ge,a.stateNode));break;case 4:s=Ge,u=Nn,Ge=a.stateNode.containerInfo,Nn=!0,Fi(t,n,a),Ge=s,Nn=u;break;case 0:case 11:case 14:case 15:ma(2,a,n),nn||ma(4,a,n),Fi(t,n,a);break;case 1:nn||(Ei(a,n),s=a.stateNode,typeof s.componentWillUnmount=="function"&&Yp(a,n,s)),Fi(t,n,a);break;case 21:Fi(t,n,a);break;case 22:nn=(s=nn)||a.memoizedState!==null,Fi(t,n,a),nn=s;break;default:Fi(t,n,a)}}function em(t,n){if(n.memoizedState===null&&(t=n.alternate,t!==null&&(t=t.memoizedState,t!==null))){t=t.dehydrated;try{jr(t)}catch(a){Ae(n,n.return,a)}}}function nm(t,n){if(n.memoizedState===null&&(t=n.alternate,t!==null&&(t=t.memoizedState,t!==null&&(t=t.dehydrated,t!==null))))try{jr(t)}catch(a){Ae(n,n.return,a)}}function Q0(t){switch(t.tag){case 31:case 13:case 19:var n=t.stateNode;return n===null&&(n=t.stateNode=new Qp),n;case 22:return t=t.stateNode,n=t._retryCache,n===null&&(n=t._retryCache=new Qp),n;default:throw Error(r(435,t.tag))}}function gl(t,n){var a=Q0(t);n.forEach(function(s){if(!a.has(s)){a.add(s);var u=sS.bind(null,t,s);s.then(u,u)}})}function On(t,n){var a=n.deletions;if(a!==null)for(var s=0;s<a.length;s++){var u=a[s],f=t,S=n,E=S;t:for(;E!==null;){switch(E.tag){case 27:if(ya(E.type)){Ge=E.stateNode,Nn=!1;break t}break;case 5:Ge=E.stateNode,Nn=!1;break t;case 3:case 4:Ge=E.stateNode.containerInfo,Nn=!0;break t}E=E.return}if(Ge===null)throw Error(r(160));tm(f,S,u),Ge=null,Nn=!1,f=u.alternate,f!==null&&(f.return=null),u.return=null}if(n.subtreeFlags&13886)for(n=n.child;n!==null;)im(n,t),n=n.sibling}var hi=null;function im(t,n){var a=t.alternate,s=t.flags;switch(t.tag){case 0:case 11:case 14:case 15:On(n,t),zn(t),s&4&&(ma(3,t,t.return),Js(3,t),ma(5,t,t.return));break;case 1:On(n,t),zn(t),s&512&&(nn||a===null||Ei(a,a.return)),s&64&&Ii&&(t=t.updateQueue,t!==null&&(s=t.callbacks,s!==null&&(a=t.shared.hiddenCallbacks,t.shared.hiddenCallbacks=a===null?s:a.concat(s))));break;case 26:var u=hi;if(On(n,t),zn(t),s&512&&(nn||a===null||Ei(a,a.return)),s&4){var f=a!==null?a.memoizedState:null;if(s=t.memoizedState,a===null)if(s===null)if(t.stateNode===null){t:{s=t.type,a=t.memoizedProps,u=u.ownerDocument||u;e:switch(s){case"title":f=u.getElementsByTagName("title")[0],(!f||f[st]||f[Ze]||f.namespaceURI==="http://www.w3.org/2000/svg"||f.hasAttribute("itemprop"))&&(f=u.createElement(s),u.head.insertBefore(f,u.querySelector("head > title"))),_n(f,s,a),f[Ze]=t,Bt(f),s=f;break t;case"link":var S=ig("link","href",u).get(s+(a.href||""));if(S){for(var E=0;E<S.length;E++)if(f=S[E],f.getAttribute("href")===(a.href==null||a.href===""?null:a.href)&&f.getAttribute("rel")===(a.rel==null?null:a.rel)&&f.getAttribute("title")===(a.title==null?null:a.title)&&f.getAttribute("crossorigin")===(a.crossOrigin==null?null:a.crossOrigin)){S.splice(E,1);break e}}f=u.createElement(s),_n(f,s,a),u.head.appendChild(f);break;case"meta":if(S=ig("meta","content",u).get(s+(a.content||""))){for(E=0;E<S.length;E++)if(f=S[E],f.getAttribute("content")===(a.content==null?null:""+a.content)&&f.getAttribute("name")===(a.name==null?null:a.name)&&f.getAttribute("property")===(a.property==null?null:a.property)&&f.getAttribute("http-equiv")===(a.httpEquiv==null?null:a.httpEquiv)&&f.getAttribute("charset")===(a.charSet==null?null:a.charSet)){S.splice(E,1);break e}}f=u.createElement(s),_n(f,s,a),u.head.appendChild(f);break;default:throw Error(r(468,s))}f[Ze]=t,Bt(f),s=f}t.stateNode=s}else ag(u,t.type,t.stateNode);else t.stateNode=ng(u,s,t.memoizedProps);else f!==s?(f===null?a.stateNode!==null&&(a=a.stateNode,a.parentNode.removeChild(a)):f.count--,s===null?ag(u,t.type,t.stateNode):ng(u,s,t.memoizedProps)):s===null&&t.stateNode!==null&&Vc(t,t.memoizedProps,a.memoizedProps)}break;case 27:On(n,t),zn(t),s&512&&(nn||a===null||Ei(a,a.return)),a!==null&&s&4&&Vc(t,t.memoizedProps,a.memoizedProps);break;case 5:if(On(n,t),zn(t),s&512&&(nn||a===null||Ei(a,a.return)),t.flags&32){u=t.stateNode;try{_r(u,"")}catch(Lt){Ae(t,t.return,Lt)}}s&4&&t.stateNode!=null&&(u=t.memoizedProps,Vc(t,u,a!==null?a.memoizedProps:u)),s&1024&&(kc=!0);break;case 6:if(On(n,t),zn(t),s&4){if(t.stateNode===null)throw Error(r(162));s=t.memoizedProps,a=t.stateNode;try{a.nodeValue=s}catch(Lt){Ae(t,t.return,Lt)}}break;case 3:if(Ul=null,u=hi,hi=Dl(n.containerInfo),On(n,t),hi=u,zn(t),s&4&&a!==null&&a.memoizedState.isDehydrated)try{jr(n.containerInfo)}catch(Lt){Ae(t,t.return,Lt)}kc&&(kc=!1,am(t));break;case 4:s=hi,hi=Dl(t.stateNode.containerInfo),On(n,t),zn(t),hi=s;break;case 12:On(n,t),zn(t);break;case 31:On(n,t),zn(t),s&4&&(s=t.updateQueue,s!==null&&(t.updateQueue=null,gl(t,s)));break;case 13:On(n,t),zn(t),t.child.flags&8192&&t.memoizedState!==null!=(a!==null&&a.memoizedState!==null)&&(vl=gt()),s&4&&(s=t.updateQueue,s!==null&&(t.updateQueue=null,gl(t,s)));break;case 22:u=t.memoizedState!==null;var I=a!==null&&a.memoizedState!==null,Q=Ii,ct=nn;if(Ii=Q||u,nn=ct||I,On(n,t),nn=ct,Ii=Q,zn(t),s&8192)t:for(n=t.stateNode,n._visibility=u?n._visibility&-2:n._visibility|1,u&&(a===null||I||Ii||nn||er(t)),a=null,n=t;;){if(n.tag===5||n.tag===26){if(a===null){I=a=n;try{if(f=I.stateNode,u)S=f.style,typeof S.setProperty=="function"?S.setProperty("display","none","important"):S.display="none";else{E=I.stateNode;var pt=I.memoizedProps.style,$=pt!=null&&pt.hasOwnProperty("display")?pt.display:null;E.style.display=$==null||typeof $=="boolean"?"":(""+$).trim()}}catch(Lt){Ae(I,I.return,Lt)}}}else if(n.tag===6){if(a===null){I=n;try{I.stateNode.nodeValue=u?"":I.memoizedProps}catch(Lt){Ae(I,I.return,Lt)}}}else if(n.tag===18){if(a===null){I=n;try{var ot=I.stateNode;u?Ym(ot,!0):Ym(I.stateNode,!1)}catch(Lt){Ae(I,I.return,Lt)}}}else if((n.tag!==22&&n.tag!==23||n.memoizedState===null||n===t)&&n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break t;for(;n.sibling===null;){if(n.return===null||n.return===t)break t;a===n&&(a=null),n=n.return}a===n&&(a=null),n.sibling.return=n.return,n=n.sibling}s&4&&(s=t.updateQueue,s!==null&&(a=s.retryQueue,a!==null&&(s.retryQueue=null,gl(t,a))));break;case 19:On(n,t),zn(t),s&4&&(s=t.updateQueue,s!==null&&(t.updateQueue=null,gl(t,s)));break;case 30:break;case 21:break;default:On(n,t),zn(t)}}function zn(t){var n=t.flags;if(n&2){try{for(var a,s=t.return;s!==null;){if(Zp(s)){a=s;break}s=s.return}if(a==null)throw Error(r(160));switch(a.tag){case 27:var u=a.stateNode,f=Xc(t);ml(t,f,u);break;case 5:var S=a.stateNode;a.flags&32&&(_r(S,""),a.flags&=-33);var E=Xc(t);ml(t,E,S);break;case 3:case 4:var I=a.stateNode.containerInfo,Q=Xc(t);Wc(t,Q,I);break;default:throw Error(r(161))}}catch(ct){Ae(t,t.return,ct)}t.flags&=-3}n&4096&&(t.flags&=-4097)}function am(t){if(t.subtreeFlags&1024)for(t=t.child;t!==null;){var n=t;am(n),n.tag===5&&n.flags&1024&&n.stateNode.reset(),t=t.sibling}}function Hi(t,n){if(n.subtreeFlags&8772)for(n=n.child;n!==null;)Jp(t,n.alternate,n),n=n.sibling}function er(t){for(t=t.child;t!==null;){var n=t;switch(n.tag){case 0:case 11:case 14:case 15:ma(4,n,n.return),er(n);break;case 1:Ei(n,n.return);var a=n.stateNode;typeof a.componentWillUnmount=="function"&&Yp(n,n.return,a),er(n);break;case 27:lo(n.stateNode);case 26:case 5:Ei(n,n.return),er(n);break;case 22:n.memoizedState===null&&er(n);break;case 30:er(n);break;default:er(n)}t=t.sibling}}function Gi(t,n,a){for(a=a&&(n.subtreeFlags&8772)!==0,n=n.child;n!==null;){var s=n.alternate,u=t,f=n,S=f.flags;switch(f.tag){case 0:case 11:case 15:Gi(u,f,a),Js(4,f);break;case 1:if(Gi(u,f,a),s=f,u=s.stateNode,typeof u.componentDidMount=="function")try{u.componentDidMount()}catch(Q){Ae(s,s.return,Q)}if(s=f,u=s.updateQueue,u!==null){var E=s.stateNode;try{var I=u.shared.hiddenCallbacks;if(I!==null)for(u.shared.hiddenCallbacks=null,u=0;u<I.length;u++)zd(I[u],E)}catch(Q){Ae(s,s.return,Q)}}a&&S&64&&qp(f),$s(f,f.return);break;case 27:Kp(f);case 26:case 5:Gi(u,f,a),a&&s===null&&S&4&&jp(f),$s(f,f.return);break;case 12:Gi(u,f,a);break;case 31:Gi(u,f,a),a&&S&4&&em(u,f);break;case 13:Gi(u,f,a),a&&S&4&&nm(u,f);break;case 22:f.memoizedState===null&&Gi(u,f,a),$s(f,f.return);break;case 30:break;default:Gi(u,f,a)}n=n.sibling}}function qc(t,n){var a=null;t!==null&&t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(a=t.memoizedState.cachePool.pool),t=null,n.memoizedState!==null&&n.memoizedState.cachePool!==null&&(t=n.memoizedState.cachePool.pool),t!==a&&(t!=null&&t.refCount++,a!=null&&Fs(a))}function Yc(t,n){t=null,n.alternate!==null&&(t=n.alternate.memoizedState.cache),n=n.memoizedState.cache,n!==t&&(n.refCount++,t!=null&&Fs(t))}function di(t,n,a,s){if(n.subtreeFlags&10256)for(n=n.child;n!==null;)rm(t,n,a,s),n=n.sibling}function rm(t,n,a,s){var u=n.flags;switch(n.tag){case 0:case 11:case 15:di(t,n,a,s),u&2048&&Js(9,n);break;case 1:di(t,n,a,s);break;case 3:di(t,n,a,s),u&2048&&(t=null,n.alternate!==null&&(t=n.alternate.memoizedState.cache),n=n.memoizedState.cache,n!==t&&(n.refCount++,t!=null&&Fs(t)));break;case 12:if(u&2048){di(t,n,a,s),t=n.stateNode;try{var f=n.memoizedProps,S=f.id,E=f.onPostCommit;typeof E=="function"&&E(S,n.alternate===null?"mount":"update",t.passiveEffectDuration,-0)}catch(I){Ae(n,n.return,I)}}else di(t,n,a,s);break;case 31:di(t,n,a,s);break;case 13:di(t,n,a,s);break;case 23:break;case 22:f=n.stateNode,S=n.alternate,n.memoizedState!==null?f._visibility&2?di(t,n,a,s):to(t,n):f._visibility&2?di(t,n,a,s):(f._visibility|=2,Br(t,n,a,s,(n.subtreeFlags&10256)!==0||!1)),u&2048&&qc(S,n);break;case 24:di(t,n,a,s),u&2048&&Yc(n.alternate,n);break;default:di(t,n,a,s)}}function Br(t,n,a,s,u){for(u=u&&((n.subtreeFlags&10256)!==0||!1),n=n.child;n!==null;){var f=t,S=n,E=a,I=s,Q=S.flags;switch(S.tag){case 0:case 11:case 15:Br(f,S,E,I,u),Js(8,S);break;case 23:break;case 22:var ct=S.stateNode;S.memoizedState!==null?ct._visibility&2?Br(f,S,E,I,u):to(f,S):(ct._visibility|=2,Br(f,S,E,I,u)),u&&Q&2048&&qc(S.alternate,S);break;case 24:Br(f,S,E,I,u),u&&Q&2048&&Yc(S.alternate,S);break;default:Br(f,S,E,I,u)}n=n.sibling}}function to(t,n){if(n.subtreeFlags&10256)for(n=n.child;n!==null;){var a=t,s=n,u=s.flags;switch(s.tag){case 22:to(a,s),u&2048&&qc(s.alternate,s);break;case 24:to(a,s),u&2048&&Yc(s.alternate,s);break;default:to(a,s)}n=n.sibling}}var eo=8192;function Ir(t,n,a){if(t.subtreeFlags&eo)for(t=t.child;t!==null;)sm(t,n,a),t=t.sibling}function sm(t,n,a){switch(t.tag){case 26:Ir(t,n,a),t.flags&eo&&t.memoizedState!==null&&BS(a,hi,t.memoizedState,t.memoizedProps);break;case 5:Ir(t,n,a);break;case 3:case 4:var s=hi;hi=Dl(t.stateNode.containerInfo),Ir(t,n,a),hi=s;break;case 22:t.memoizedState===null&&(s=t.alternate,s!==null&&s.memoizedState!==null?(s=eo,eo=16777216,Ir(t,n,a),eo=s):Ir(t,n,a));break;default:Ir(t,n,a)}}function om(t){var n=t.alternate;if(n!==null&&(t=n.child,t!==null)){n.child=null;do n=t.sibling,t.sibling=null,t=n;while(t!==null)}}function no(t){var n=t.deletions;if((t.flags&16)!==0){if(n!==null)for(var a=0;a<n.length;a++){var s=n[a];fn=s,um(s,t)}om(t)}if(t.subtreeFlags&10256)for(t=t.child;t!==null;)lm(t),t=t.sibling}function lm(t){switch(t.tag){case 0:case 11:case 15:no(t),t.flags&2048&&ma(9,t,t.return);break;case 3:no(t);break;case 12:no(t);break;case 22:var n=t.stateNode;t.memoizedState!==null&&n._visibility&2&&(t.return===null||t.return.tag!==13)?(n._visibility&=-3,_l(t)):no(t);break;default:no(t)}}function _l(t){var n=t.deletions;if((t.flags&16)!==0){if(n!==null)for(var a=0;a<n.length;a++){var s=n[a];fn=s,um(s,t)}om(t)}for(t=t.child;t!==null;){switch(n=t,n.tag){case 0:case 11:case 15:ma(8,n,n.return),_l(n);break;case 22:a=n.stateNode,a._visibility&2&&(a._visibility&=-3,_l(n));break;default:_l(n)}t=t.sibling}}function um(t,n){for(;fn!==null;){var a=fn;switch(a.tag){case 0:case 11:case 15:ma(8,a,n);break;case 23:case 22:if(a.memoizedState!==null&&a.memoizedState.cachePool!==null){var s=a.memoizedState.cachePool.pool;s!=null&&s.refCount++}break;case 24:Fs(a.memoizedState.cache)}if(s=a.child,s!==null)s.return=a,fn=s;else t:for(a=t;fn!==null;){s=fn;var u=s.sibling,f=s.return;if($p(s),s===a){fn=null;break t}if(u!==null){u.return=f,fn=u;break t}fn=f}}}var J0={getCacheForType:function(t){var n=mn($e),a=n.data.get(t);return a===void 0&&(a=t(),n.data.set(t,a)),a},cacheSignal:function(){return mn($e).controller.signal}},$0=typeof WeakMap=="function"?WeakMap:Map,xe=0,Oe=null,fe=null,de=0,be=0,kn=null,ga=!1,Fr=!1,jc=!1,Vi=0,ke=0,_a=0,nr=0,Zc=0,qn=0,Hr=0,io=null,Pn=null,Kc=!1,vl=0,cm=0,Sl=1/0,xl=null,va=null,sn=0,Sa=null,Gr=null,Xi=0,Qc=0,Jc=null,fm=null,ao=0,$c=null;function Yn(){return(xe&2)!==0&&de!==0?de&-de:P.T!==null?sf():Es()}function hm(){if(qn===0)if((de&536870912)===0||me){var t=F;F<<=1,(F&3932160)===0&&(F=262144),qn=t}else qn=536870912;return t=Xn.current,t!==null&&(t.flags|=32),qn}function Bn(t,n,a){(t===Oe&&(be===2||be===9)||t.cancelPendingCommit!==null)&&(Vr(t,0),xa(t,de,qn,!1)),qe(t,a),((xe&2)===0||t!==Oe)&&(t===Oe&&((xe&2)===0&&(nr|=a),ke===4&&xa(t,de,qn,!1)),Ti(t))}function dm(t,n,a){if((xe&6)!==0)throw Error(r(327));var s=!a&&(n&127)===0&&(n&t.expiredLanes)===0||Gt(t,n),u=s?nS(t,n):ef(t,n,!0),f=s;do{if(u===0){Fr&&!s&&xa(t,n,0,!1);break}else{if(a=t.current.alternate,f&&!tS(a)){u=ef(t,n,!1),f=!1;continue}if(u===2){if(f=n,t.errorRecoveryDisabledLanes&f)var S=0;else S=t.pendingLanes&-536870913,S=S!==0?S:S&536870912?536870912:0;if(S!==0){n=S;t:{var E=t;u=io;var I=E.current.memoizedState.isDehydrated;if(I&&(Vr(E,S).flags|=256),S=ef(E,S,!1),S!==2){if(jc&&!I){E.errorRecoveryDisabledLanes|=f,nr|=f,u=4;break t}f=Pn,Pn=u,f!==null&&(Pn===null?Pn=f:Pn.push.apply(Pn,f))}u=S}if(f=!1,u!==2)continue}}if(u===1){Vr(t,0),xa(t,n,0,!0);break}t:{switch(s=t,f=u,f){case 0:case 1:throw Error(r(345));case 4:if((n&4194048)!==n)break;case 6:xa(s,n,qn,!ga);break t;case 2:Pn=null;break;case 3:case 5:break;default:throw Error(r(329))}if((n&62914560)===n&&(u=vl+300-gt(),10<u)){if(xa(s,n,qn,!ga),jt(s,0,!0)!==0)break t;Xi=n,s.timeoutHandle=Wm(pm.bind(null,s,a,Pn,xl,Kc,n,qn,nr,Hr,ga,f,"Throttled",-0,0),u);break t}pm(s,a,Pn,xl,Kc,n,qn,nr,Hr,ga,f,null,-0,0)}}break}while(!0);Ti(t)}function pm(t,n,a,s,u,f,S,E,I,Q,ct,pt,$,ot){if(t.timeoutHandle=-1,pt=n.subtreeFlags,pt&8192||(pt&16785408)===16785408){pt={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:Ci},sm(n,f,pt);var Lt=(f&62914560)===f?vl-gt():(f&4194048)===f?cm-gt():0;if(Lt=IS(pt,Lt),Lt!==null){Xi=f,t.cancelPendingCommit=Lt(ym.bind(null,t,n,f,a,s,u,S,E,I,ct,pt,null,$,ot)),xa(t,f,S,!Q);return}}ym(t,n,f,a,s,u,S,E,I)}function tS(t){for(var n=t;;){var a=n.tag;if((a===0||a===11||a===15)&&n.flags&16384&&(a=n.updateQueue,a!==null&&(a=a.stores,a!==null)))for(var s=0;s<a.length;s++){var u=a[s],f=u.getSnapshot;u=u.value;try{if(!Gn(f(),u))return!1}catch{return!1}}if(a=n.child,n.subtreeFlags&16384&&a!==null)a.return=n,n=a;else{if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return!0;n=n.return}n.sibling.return=n.return,n=n.sibling}}return!0}function xa(t,n,a,s){n&=~Zc,n&=~nr,t.suspendedLanes|=n,t.pingedLanes&=~n,s&&(t.warmLanes|=n),s=t.expirationTimes;for(var u=n;0<u;){var f=31-Xt(u),S=1<<f;s[f]=-1,u&=~S}a!==0&&cn(t,a,n)}function Ml(){return(xe&6)===0?(ro(0),!1):!0}function tf(){if(fe!==null){if(be===0)var t=fe.return;else t=fe,Ui=Ya=null,gc(t),Ur=null,Gs=0,t=fe;for(;t!==null;)kp(t.alternate,t),t=t.return;fe=null}}function Vr(t,n){var a=t.timeoutHandle;a!==-1&&(t.timeoutHandle=-1,xS(a)),a=t.cancelPendingCommit,a!==null&&(t.cancelPendingCommit=null,a()),Xi=0,tf(),Oe=t,fe=a=Di(t.current,null),de=n,be=0,kn=null,ga=!1,Fr=Gt(t,n),jc=!1,Hr=qn=Zc=nr=_a=ke=0,Pn=io=null,Kc=!1,(n&8)!==0&&(n|=n&32);var s=t.entangledLanes;if(s!==0)for(t=t.entanglements,s&=n;0<s;){var u=31-Xt(s),f=1<<u;n|=t[u],s&=~f}return Vi=n,Vo(),a}function mm(t,n){ne=null,P.H=Zs,n===Lr||n===Ko?(n=Ld(),be=3):n===ac?(n=Ld(),be=4):be=n===Uc?8:n!==null&&typeof n=="object"&&typeof n.then=="function"?6:1,kn=n,fe===null&&(ke=1,cl(t,$n(n,t.current)))}function gm(){var t=Xn.current;return t===null?!0:(de&4194048)===de?ii===null:(de&62914560)===de||(de&536870912)!==0?t===ii:!1}function _m(){var t=P.H;return P.H=Zs,t===null?Zs:t}function vm(){var t=P.A;return P.A=J0,t}function yl(){ke=4,ga||(de&4194048)!==de&&Xn.current!==null||(Fr=!0),(_a&134217727)===0&&(nr&134217727)===0||Oe===null||xa(Oe,de,qn,!1)}function ef(t,n,a){var s=xe;xe|=2;var u=_m(),f=vm();(Oe!==t||de!==n)&&(xl=null,Vr(t,n)),n=!1;var S=ke;t:do try{if(be!==0&&fe!==null){var E=fe,I=kn;switch(be){case 8:tf(),S=6;break t;case 3:case 2:case 9:case 6:Xn.current===null&&(n=!0);var Q=be;if(be=0,kn=null,Xr(t,E,I,Q),a&&Fr){S=0;break t}break;default:Q=be,be=0,kn=null,Xr(t,E,I,Q)}}eS(),S=ke;break}catch(ct){mm(t,ct)}while(!0);return n&&t.shellSuspendCounter++,Ui=Ya=null,xe=s,P.H=u,P.A=f,fe===null&&(Oe=null,de=0,Vo()),S}function eS(){for(;fe!==null;)Sm(fe)}function nS(t,n){var a=xe;xe|=2;var s=_m(),u=vm();Oe!==t||de!==n?(xl=null,Sl=gt()+500,Vr(t,n)):Fr=Gt(t,n);t:do try{if(be!==0&&fe!==null){n=fe;var f=kn;e:switch(be){case 1:be=0,kn=null,Xr(t,n,f,1);break;case 2:case 9:if(wd(f)){be=0,kn=null,xm(n);break}n=function(){be!==2&&be!==9||Oe!==t||(be=7),Ti(t)},f.then(n,n);break t;case 3:be=7;break t;case 4:be=5;break t;case 7:wd(f)?(be=0,kn=null,xm(n)):(be=0,kn=null,Xr(t,n,f,7));break;case 5:var S=null;switch(fe.tag){case 26:S=fe.memoizedState;case 5:case 27:var E=fe;if(S?rg(S):E.stateNode.complete){be=0,kn=null;var I=E.sibling;if(I!==null)fe=I;else{var Q=E.return;Q!==null?(fe=Q,El(Q)):fe=null}break e}}be=0,kn=null,Xr(t,n,f,5);break;case 6:be=0,kn=null,Xr(t,n,f,6);break;case 8:tf(),ke=6;break t;default:throw Error(r(462))}}iS();break}catch(ct){mm(t,ct)}while(!0);return Ui=Ya=null,P.H=s,P.A=u,xe=a,fe!==null?0:(Oe=null,de=0,Vo(),ke)}function iS(){for(;fe!==null&&!St();)Sm(fe)}function Sm(t){var n=Xp(t.alternate,t,Vi);t.memoizedProps=t.pendingProps,n===null?El(t):fe=n}function xm(t){var n=t,a=n.alternate;switch(n.tag){case 15:case 0:n=Bp(a,n,n.pendingProps,n.type,void 0,de);break;case 11:n=Bp(a,n,n.pendingProps,n.type.render,n.ref,de);break;case 5:gc(n);default:kp(a,n),n=fe=vd(n,Vi),n=Xp(a,n,Vi)}t.memoizedProps=t.pendingProps,n===null?El(t):fe=n}function Xr(t,n,a,s){Ui=Ya=null,gc(n),Ur=null,Gs=0;var u=n.return;try{if(k0(t,u,n,a,de)){ke=1,cl(t,$n(a,t.current)),fe=null;return}}catch(f){if(u!==null)throw fe=u,f;ke=1,cl(t,$n(a,t.current)),fe=null;return}n.flags&32768?(me||s===1?t=!0:Fr||(de&536870912)!==0?t=!1:(ga=t=!0,(s===2||s===9||s===3||s===6)&&(s=Xn.current,s!==null&&s.tag===13&&(s.flags|=16384))),Mm(n,t)):El(n)}function El(t){var n=t;do{if((n.flags&32768)!==0){Mm(n,ga);return}t=n.return;var a=j0(n.alternate,n,Vi);if(a!==null){fe=a;return}if(n=n.sibling,n!==null){fe=n;return}fe=n=t}while(n!==null);ke===0&&(ke=5)}function Mm(t,n){do{var a=Z0(t.alternate,t);if(a!==null){a.flags&=32767,fe=a;return}if(a=t.return,a!==null&&(a.flags|=32768,a.subtreeFlags=0,a.deletions=null),!n&&(t=t.sibling,t!==null)){fe=t;return}fe=t=a}while(t!==null);ke=6,fe=null}function ym(t,n,a,s,u,f,S,E,I){t.cancelPendingCommit=null;do Tl();while(sn!==0);if((xe&6)!==0)throw Error(r(327));if(n!==null){if(n===t.current)throw Error(r(177));if(f=n.lanes|n.childLanes,f|=Xu,Ce(t,a,f,S,E,I),t===Oe&&(fe=Oe=null,de=0),Gr=n,Sa=t,Xi=a,Qc=f,Jc=u,fm=s,(n.subtreeFlags&10256)!==0||(n.flags&10256)!==0?(t.callbackNode=null,t.callbackPriority=0,oS(qt,function(){return Rm(),null})):(t.callbackNode=null,t.callbackPriority=0),s=(n.flags&13878)!==0,(n.subtreeFlags&13878)!==0||s){s=P.T,P.T=null,u=q.p,q.p=2,S=xe,xe|=4;try{K0(t,n,a)}finally{xe=S,q.p=u,P.T=s}}sn=1,Em(),Tm(),bm()}}function Em(){if(sn===1){sn=0;var t=Sa,n=Gr,a=(n.flags&13878)!==0;if((n.subtreeFlags&13878)!==0||a){a=P.T,P.T=null;var s=q.p;q.p=2;var u=xe;xe|=4;try{im(n,t);var f=pf,S=ud(t.containerInfo),E=f.focusedElem,I=f.selectionRange;if(S!==E&&E&&E.ownerDocument&&ld(E.ownerDocument.documentElement,E)){if(I!==null&&Iu(E)){var Q=I.start,ct=I.end;if(ct===void 0&&(ct=Q),"selectionStart"in E)E.selectionStart=Q,E.selectionEnd=Math.min(ct,E.value.length);else{var pt=E.ownerDocument||document,$=pt&&pt.defaultView||window;if($.getSelection){var ot=$.getSelection(),Lt=E.textContent.length,Zt=Math.min(I.start,Lt),Le=I.end===void 0?Zt:Math.min(I.end,Lt);!ot.extend&&Zt>Le&&(S=Le,Le=Zt,Zt=S);var k=od(E,Zt),H=od(E,Le);if(k&&H&&(ot.rangeCount!==1||ot.anchorNode!==k.node||ot.anchorOffset!==k.offset||ot.focusNode!==H.node||ot.focusOffset!==H.offset)){var Z=pt.createRange();Z.setStart(k.node,k.offset),ot.removeAllRanges(),Zt>Le?(ot.addRange(Z),ot.extend(H.node,H.offset)):(Z.setEnd(H.node,H.offset),ot.addRange(Z))}}}}for(pt=[],ot=E;ot=ot.parentNode;)ot.nodeType===1&&pt.push({element:ot,left:ot.scrollLeft,top:ot.scrollTop});for(typeof E.focus=="function"&&E.focus(),E=0;E<pt.length;E++){var ht=pt[E];ht.element.scrollLeft=ht.left,ht.element.scrollTop=ht.top}}Pl=!!df,pf=df=null}finally{xe=u,q.p=s,P.T=a}}t.current=n,sn=2}}function Tm(){if(sn===2){sn=0;var t=Sa,n=Gr,a=(n.flags&8772)!==0;if((n.subtreeFlags&8772)!==0||a){a=P.T,P.T=null;var s=q.p;q.p=2;var u=xe;xe|=4;try{Jp(t,n.alternate,n)}finally{xe=u,q.p=s,P.T=a}}sn=3}}function bm(){if(sn===4||sn===3){sn=0,vt();var t=Sa,n=Gr,a=Xi,s=fm;(n.subtreeFlags&10256)!==0||(n.flags&10256)!==0?sn=5:(sn=0,Gr=Sa=null,Am(t,t.pendingLanes));var u=t.pendingLanes;if(u===0&&(va=null),ta(a),n=n.stateNode,Dt&&typeof Dt.onCommitFiberRoot=="function")try{Dt.onCommitFiberRoot(Kt,n,void 0,(n.current.flags&128)===128)}catch{}if(s!==null){n=P.T,u=q.p,q.p=2,P.T=null;try{for(var f=t.onRecoverableError,S=0;S<s.length;S++){var E=s[S];f(E.value,{componentStack:E.stack})}}finally{P.T=n,q.p=u}}(Xi&3)!==0&&Tl(),Ti(t),u=t.pendingLanes,(a&261930)!==0&&(u&42)!==0?t===$c?ao++:(ao=0,$c=t):ao=0,ro(0)}}function Am(t,n){(t.pooledCacheLanes&=n)===0&&(n=t.pooledCache,n!=null&&(t.pooledCache=null,Fs(n)))}function Tl(){return Em(),Tm(),bm(),Rm()}function Rm(){if(sn!==5)return!1;var t=Sa,n=Qc;Qc=0;var a=ta(Xi),s=P.T,u=q.p;try{q.p=32>a?32:a,P.T=null,a=Jc,Jc=null;var f=Sa,S=Xi;if(sn=0,Gr=Sa=null,Xi=0,(xe&6)!==0)throw Error(r(331));var E=xe;if(xe|=4,lm(f.current),rm(f,f.current,S,a),xe=E,ro(0,!1),Dt&&typeof Dt.onPostCommitFiberRoot=="function")try{Dt.onPostCommitFiberRoot(Kt,f)}catch{}return!0}finally{q.p=u,P.T=s,Am(t,n)}}function Cm(t,n,a){n=$n(a,n),n=Lc(t.stateNode,n,2),t=ha(t,n,2),t!==null&&(qe(t,2),Ti(t))}function Ae(t,n,a){if(t.tag===3)Cm(t,t,a);else for(;n!==null;){if(n.tag===3){Cm(n,t,a);break}else if(n.tag===1){var s=n.stateNode;if(typeof n.type.getDerivedStateFromError=="function"||typeof s.componentDidCatch=="function"&&(va===null||!va.has(s))){t=$n(a,t),a=wp(2),s=ha(n,a,2),s!==null&&(Dp(a,s,n,t),qe(s,2),Ti(s));break}}n=n.return}}function nf(t,n,a){var s=t.pingCache;if(s===null){s=t.pingCache=new $0;var u=new Set;s.set(n,u)}else u=s.get(n),u===void 0&&(u=new Set,s.set(n,u));u.has(a)||(jc=!0,u.add(a),t=aS.bind(null,t,n,a),n.then(t,t))}function aS(t,n,a){var s=t.pingCache;s!==null&&s.delete(n),t.pingedLanes|=t.suspendedLanes&a,t.warmLanes&=~a,Oe===t&&(de&a)===a&&(ke===4||ke===3&&(de&62914560)===de&&300>gt()-vl?(xe&2)===0&&Vr(t,0):Zc|=a,Hr===de&&(Hr=0)),Ti(t)}function wm(t,n){n===0&&(n=Ee()),t=Wa(t,n),t!==null&&(qe(t,n),Ti(t))}function rS(t){var n=t.memoizedState,a=0;n!==null&&(a=n.retryLane),wm(t,a)}function sS(t,n){var a=0;switch(t.tag){case 31:case 13:var s=t.stateNode,u=t.memoizedState;u!==null&&(a=u.retryLane);break;case 19:s=t.stateNode;break;case 22:s=t.stateNode._retryCache;break;default:throw Error(r(314))}s!==null&&s.delete(n),wm(t,a)}function oS(t,n){return R(t,n)}var bl=null,Wr=null,af=!1,Al=!1,rf=!1,Ma=0;function Ti(t){t!==Wr&&t.next===null&&(Wr===null?bl=Wr=t:Wr=Wr.next=t),Al=!0,af||(af=!0,uS())}function ro(t,n){if(!rf&&Al){rf=!0;do for(var a=!1,s=bl;s!==null;){if(t!==0){var u=s.pendingLanes;if(u===0)var f=0;else{var S=s.suspendedLanes,E=s.pingedLanes;f=(1<<31-Xt(42|t)+1)-1,f&=u&~(S&~E),f=f&201326741?f&201326741|1:f?f|2:0}f!==0&&(a=!0,Nm(s,f))}else f=de,f=jt(s,s===Oe?f:0,s.cancelPendingCommit!==null||s.timeoutHandle!==-1),(f&3)===0||Gt(s,f)||(a=!0,Nm(s,f));s=s.next}while(a);rf=!1}}function lS(){Dm()}function Dm(){Al=af=!1;var t=0;Ma!==0&&SS()&&(t=Ma);for(var n=gt(),a=null,s=bl;s!==null;){var u=s.next,f=Lm(s,n);f===0?(s.next=null,a===null?bl=u:a.next=u,u===null&&(Wr=a)):(a=s,(t!==0||(f&3)!==0)&&(Al=!0)),s=u}sn!==0&&sn!==5||ro(t),Ma!==0&&(Ma=0)}function Lm(t,n){for(var a=t.suspendedLanes,s=t.pingedLanes,u=t.expirationTimes,f=t.pendingLanes&-62914561;0<f;){var S=31-Xt(f),E=1<<S,I=u[S];I===-1?((E&a)===0||(E&s)!==0)&&(u[S]=Re(E,n)):I<=n&&(t.expiredLanes|=E),f&=~E}if(n=Oe,a=de,a=jt(t,t===n?a:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),s=t.callbackNode,a===0||t===n&&(be===2||be===9)||t.cancelPendingCommit!==null)return s!==null&&s!==null&&it(s),t.callbackNode=null,t.callbackPriority=0;if((a&3)===0||Gt(t,a)){if(n=a&-a,n===t.callbackPriority)return n;switch(s!==null&&it(s),ta(a)){case 2:case 8:a=Ut;break;case 32:a=qt;break;case 268435456:a=_t;break;default:a=qt}return s=Um.bind(null,t),a=R(a,s),t.callbackPriority=n,t.callbackNode=a,n}return s!==null&&s!==null&&it(s),t.callbackPriority=2,t.callbackNode=null,2}function Um(t,n){if(sn!==0&&sn!==5)return t.callbackNode=null,t.callbackPriority=0,null;var a=t.callbackNode;if(Tl()&&t.callbackNode!==a)return null;var s=de;return s=jt(t,t===Oe?s:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),s===0?null:(dm(t,s,n),Lm(t,gt()),t.callbackNode!=null&&t.callbackNode===a?Um.bind(null,t):null)}function Nm(t,n){if(Tl())return null;dm(t,n,!0)}function uS(){MS(function(){(xe&6)!==0?R(Rt,lS):Dm()})}function sf(){if(Ma===0){var t=wr;t===0&&(t=yt,yt<<=1,(yt&261888)===0&&(yt=256)),Ma=t}return Ma}function Om(t){return t==null||typeof t=="symbol"||typeof t=="boolean"?null:typeof t=="function"?t:Oo(""+t)}function zm(t,n){var a=n.ownerDocument.createElement("input");return a.name=n.name,a.value=n.value,t.id&&a.setAttribute("form",t.id),n.parentNode.insertBefore(a,n),t=new FormData(t),a.parentNode.removeChild(a),t}function cS(t,n,a,s,u){if(n==="submit"&&a&&a.stateNode===u){var f=Om((u[Sn]||null).action),S=s.submitter;S&&(n=(n=S[Sn]||null)?Om(n.formAction):S.getAttribute("formAction"),n!==null&&(f=n,S=null));var E=new Io("action","action",null,s,u);t.push({event:E,listeners:[{instance:null,listener:function(){if(s.defaultPrevented){if(Ma!==0){var I=S?zm(u,S):new FormData(u);bc(a,{pending:!0,data:I,method:u.method,action:f},null,I)}}else typeof f=="function"&&(E.preventDefault(),I=S?zm(u,S):new FormData(u),bc(a,{pending:!0,data:I,method:u.method,action:f},f,I))},currentTarget:u}]})}}for(var of=0;of<Vu.length;of++){var lf=Vu[of],fS=lf.toLowerCase(),hS=lf[0].toUpperCase()+lf.slice(1);fi(fS,"on"+hS)}fi(hd,"onAnimationEnd"),fi(dd,"onAnimationIteration"),fi(pd,"onAnimationStart"),fi("dblclick","onDoubleClick"),fi("focusin","onFocus"),fi("focusout","onBlur"),fi(C0,"onTransitionRun"),fi(w0,"onTransitionStart"),fi(D0,"onTransitionCancel"),fi(md,"onTransitionEnd"),Ke("onMouseEnter",["mouseout","mouseover"]),Ke("onMouseLeave",["mouseout","mouseover"]),Ke("onPointerEnter",["pointerout","pointerover"]),Ke("onPointerLeave",["pointerout","pointerover"]),Te("onChange","change click focusin focusout input keydown keyup selectionchange".split(" ")),Te("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")),Te("onBeforeInput",["compositionend","keypress","textInput","paste"]),Te("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" ")),Te("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" ")),Te("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var so="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),dS=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(so));function Pm(t,n){n=(n&4)!==0;for(var a=0;a<t.length;a++){var s=t[a],u=s.event;s=s.listeners;t:{var f=void 0;if(n)for(var S=s.length-1;0<=S;S--){var E=s[S],I=E.instance,Q=E.currentTarget;if(E=E.listener,I!==f&&u.isPropagationStopped())break t;f=E,u.currentTarget=Q;try{f(u)}catch(ct){Go(ct)}u.currentTarget=null,f=I}else for(S=0;S<s.length;S++){if(E=s[S],I=E.instance,Q=E.currentTarget,E=E.listener,I!==f&&u.isPropagationStopped())break t;f=E,u.currentTarget=Q;try{f(u)}catch(ct){Go(ct)}u.currentTarget=null,f=I}}}}function he(t,n){var a=n[Ts];a===void 0&&(a=n[Ts]=new Set);var s=t+"__bubble";a.has(s)||(Bm(n,t,2,!1),a.add(s))}function uf(t,n,a){var s=0;n&&(s|=4),Bm(a,t,s,n)}var Rl="_reactListening"+Math.random().toString(36).slice(2);function cf(t){if(!t[Rl]){t[Rl]=!0,Jt.forEach(function(a){a!=="selectionchange"&&(dS.has(a)||uf(a,!1,t),uf(a,!0,t))});var n=t.nodeType===9?t:t.ownerDocument;n===null||n[Rl]||(n[Rl]=!0,uf("selectionchange",!1,n))}}function Bm(t,n,a,s){switch(hg(n)){case 2:var u=GS;break;case 8:u=VS;break;default:u=bf}a=u.bind(null,n,a,t),u=void 0,!wu||n!=="touchstart"&&n!=="touchmove"&&n!=="wheel"||(u=!0),s?u!==void 0?t.addEventListener(n,a,{capture:!0,passive:u}):t.addEventListener(n,a,!0):u!==void 0?t.addEventListener(n,a,{passive:u}):t.addEventListener(n,a,!1)}function ff(t,n,a,s,u){var f=s;if((n&1)===0&&(n&2)===0&&s!==null)t:for(;;){if(s===null)return;var S=s.tag;if(S===3||S===4){var E=s.stateNode.containerInfo;if(E===u)break;if(S===4)for(S=s.return;S!==null;){var I=S.tag;if((I===3||I===4)&&S.stateNode.containerInfo===u)return;S=S.return}for(;E!==null;){if(S=Ct(E),S===null)return;if(I=S.tag,I===5||I===6||I===26||I===27){s=f=S;continue t}E=E.parentNode}}s=s.return}Vh(function(){var Q=f,ct=Ru(a),pt=[];t:{var $=gd.get(t);if($!==void 0){var ot=Io,Lt=t;switch(t){case"keypress":if(Po(a)===0)break t;case"keydown":case"keyup":ot=s0;break;case"focusin":Lt="focus",ot=Nu;break;case"focusout":Lt="blur",ot=Nu;break;case"beforeblur":case"afterblur":ot=Nu;break;case"click":if(a.button===2)break t;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":ot=kh;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":ot=jv;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":ot=u0;break;case hd:case dd:case pd:ot=Qv;break;case md:ot=f0;break;case"scroll":case"scrollend":ot=qv;break;case"wheel":ot=d0;break;case"copy":case"cut":case"paste":ot=$v;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":ot=Yh;break;case"toggle":case"beforetoggle":ot=m0}var Zt=(n&4)!==0,Le=!Zt&&(t==="scroll"||t==="scrollend"),k=Zt?$!==null?$+"Capture":null:$;Zt=[];for(var H=Q,Z;H!==null;){var ht=H;if(Z=ht.stateNode,ht=ht.tag,ht!==5&&ht!==26&&ht!==27||Z===null||k===null||(ht=Cs(H,k),ht!=null&&Zt.push(oo(H,ht,Z))),Le)break;H=H.return}0<Zt.length&&($=new ot($,Lt,null,a,ct),pt.push({event:$,listeners:Zt}))}}if((n&7)===0){t:{if($=t==="mouseover"||t==="pointerover",ot=t==="mouseout"||t==="pointerout",$&&a!==Au&&(Lt=a.relatedTarget||a.fromElement)&&(Ct(Lt)||Lt[ea]))break t;if((ot||$)&&($=ct.window===ct?ct:($=ct.ownerDocument)?$.defaultView||$.parentWindow:window,ot?(Lt=a.relatedTarget||a.toElement,ot=Q,Lt=Lt?Ct(Lt):null,Lt!==null&&(Le=c(Lt),Zt=Lt.tag,Lt!==Le||Zt!==5&&Zt!==27&&Zt!==6)&&(Lt=null)):(ot=null,Lt=Q),ot!==Lt)){if(Zt=kh,ht="onMouseLeave",k="onMouseEnter",H="mouse",(t==="pointerout"||t==="pointerover")&&(Zt=Yh,ht="onPointerLeave",k="onPointerEnter",H="pointer"),Le=ot==null?$:Wt(ot),Z=Lt==null?$:Wt(Lt),$=new Zt(ht,H+"leave",ot,a,ct),$.target=Le,$.relatedTarget=Z,ht=null,Ct(ct)===Q&&(Zt=new Zt(k,H+"enter",Lt,a,ct),Zt.target=Z,Zt.relatedTarget=Le,ht=Zt),Le=ht,ot&&Lt)e:{for(Zt=pS,k=ot,H=Lt,Z=0,ht=k;ht;ht=Zt(ht))Z++;ht=0;for(var Vt=H;Vt;Vt=Zt(Vt))ht++;for(;0<Z-ht;)k=Zt(k),Z--;for(;0<ht-Z;)H=Zt(H),ht--;for(;Z--;){if(k===H||H!==null&&k===H.alternate){Zt=k;break e}k=Zt(k),H=Zt(H)}Zt=null}else Zt=null;ot!==null&&Im(pt,$,ot,Zt,!1),Lt!==null&&Le!==null&&Im(pt,Le,Lt,Zt,!0)}}t:{if($=Q?Wt(Q):window,ot=$.nodeName&&$.nodeName.toLowerCase(),ot==="select"||ot==="input"&&$.type==="file")var _e=ed;else if($h($))if(nd)_e=b0;else{_e=E0;var zt=y0}else ot=$.nodeName,!ot||ot.toLowerCase()!=="input"||$.type!=="checkbox"&&$.type!=="radio"?Q&&bu(Q.elementType)&&(_e=ed):_e=T0;if(_e&&(_e=_e(t,Q))){td(pt,_e,a,ct);break t}zt&&zt(t,$,Q),t==="focusout"&&Q&&$.type==="number"&&Q.memoizedProps.value!=null&&Tu($,"number",$.value)}switch(zt=Q?Wt(Q):window,t){case"focusin":($h(zt)||zt.contentEditable==="true")&&(Mr=zt,Fu=Q,Ps=null);break;case"focusout":Ps=Fu=Mr=null;break;case"mousedown":Hu=!0;break;case"contextmenu":case"mouseup":case"dragend":Hu=!1,cd(pt,a,ct);break;case"selectionchange":if(R0)break;case"keydown":case"keyup":cd(pt,a,ct)}var ae;if(zu)t:{switch(t){case"compositionstart":var pe="onCompositionStart";break t;case"compositionend":pe="onCompositionEnd";break t;case"compositionupdate":pe="onCompositionUpdate";break t}pe=void 0}else xr?Qh(t,a)&&(pe="onCompositionEnd"):t==="keydown"&&a.keyCode===229&&(pe="onCompositionStart");pe&&(jh&&a.locale!=="ko"&&(xr||pe!=="onCompositionStart"?pe==="onCompositionEnd"&&xr&&(ae=Xh()):(ra=ct,Du="value"in ra?ra.value:ra.textContent,xr=!0)),zt=Cl(Q,pe),0<zt.length&&(pe=new qh(pe,t,null,a,ct),pt.push({event:pe,listeners:zt}),ae?pe.data=ae:(ae=Jh(a),ae!==null&&(pe.data=ae)))),(ae=_0?v0(t,a):S0(t,a))&&(pe=Cl(Q,"onBeforeInput"),0<pe.length&&(zt=new qh("onBeforeInput","beforeinput",null,a,ct),pt.push({event:zt,listeners:pe}),zt.data=ae)),cS(pt,t,Q,a,ct)}Pm(pt,n)})}function oo(t,n,a){return{instance:t,listener:n,currentTarget:a}}function Cl(t,n){for(var a=n+"Capture",s=[];t!==null;){var u=t,f=u.stateNode;if(u=u.tag,u!==5&&u!==26&&u!==27||f===null||(u=Cs(t,a),u!=null&&s.unshift(oo(t,u,f)),u=Cs(t,n),u!=null&&s.push(oo(t,u,f))),t.tag===3)return s;t=t.return}return[]}function pS(t){if(t===null)return null;do t=t.return;while(t&&t.tag!==5&&t.tag!==27);return t||null}function Im(t,n,a,s,u){for(var f=n._reactName,S=[];a!==null&&a!==s;){var E=a,I=E.alternate,Q=E.stateNode;if(E=E.tag,I!==null&&I===s)break;E!==5&&E!==26&&E!==27||Q===null||(I=Q,u?(Q=Cs(a,f),Q!=null&&S.unshift(oo(a,Q,I))):u||(Q=Cs(a,f),Q!=null&&S.push(oo(a,Q,I)))),a=a.return}S.length!==0&&t.push({event:n,listeners:S})}var mS=/\r\n?/g,gS=/\u0000|\uFFFD/g;function Fm(t){return(typeof t=="string"?t:""+t).replace(mS,`
`).replace(gS,"")}function Hm(t,n){return n=Fm(n),Fm(t)===n}function De(t,n,a,s,u,f){switch(a){case"children":typeof s=="string"?n==="body"||n==="textarea"&&s===""||_r(t,s):(typeof s=="number"||typeof s=="bigint")&&n!=="body"&&_r(t,""+s);break;case"className":Ne(t,"class",s);break;case"tabIndex":Ne(t,"tabindex",s);break;case"dir":case"role":case"viewBox":case"width":case"height":Ne(t,a,s);break;case"style":Hh(t,s,f);break;case"data":if(n!=="object"){Ne(t,"data",s);break}case"src":case"href":if(s===""&&(n!=="a"||a!=="href")){t.removeAttribute(a);break}if(s==null||typeof s=="function"||typeof s=="symbol"||typeof s=="boolean"){t.removeAttribute(a);break}s=Oo(""+s),t.setAttribute(a,s);break;case"action":case"formAction":if(typeof s=="function"){t.setAttribute(a,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}else typeof f=="function"&&(a==="formAction"?(n!=="input"&&De(t,n,"name",u.name,u,null),De(t,n,"formEncType",u.formEncType,u,null),De(t,n,"formMethod",u.formMethod,u,null),De(t,n,"formTarget",u.formTarget,u,null)):(De(t,n,"encType",u.encType,u,null),De(t,n,"method",u.method,u,null),De(t,n,"target",u.target,u,null)));if(s==null||typeof s=="symbol"||typeof s=="boolean"){t.removeAttribute(a);break}s=Oo(""+s),t.setAttribute(a,s);break;case"onClick":s!=null&&(t.onclick=Ci);break;case"onScroll":s!=null&&he("scroll",t);break;case"onScrollEnd":s!=null&&he("scrollend",t);break;case"dangerouslySetInnerHTML":if(s!=null){if(typeof s!="object"||!("__html"in s))throw Error(r(61));if(a=s.__html,a!=null){if(u.children!=null)throw Error(r(60));t.innerHTML=a}}break;case"multiple":t.multiple=s&&typeof s!="function"&&typeof s!="symbol";break;case"muted":t.muted=s&&typeof s!="function"&&typeof s!="symbol";break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":break;case"autoFocus":break;case"xlinkHref":if(s==null||typeof s=="function"||typeof s=="boolean"||typeof s=="symbol"){t.removeAttribute("xlink:href");break}a=Oo(""+s),t.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",a);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":s!=null&&typeof s!="function"&&typeof s!="symbol"?t.setAttribute(a,""+s):t.removeAttribute(a);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":s&&typeof s!="function"&&typeof s!="symbol"?t.setAttribute(a,""):t.removeAttribute(a);break;case"capture":case"download":s===!0?t.setAttribute(a,""):s!==!1&&s!=null&&typeof s!="function"&&typeof s!="symbol"?t.setAttribute(a,s):t.removeAttribute(a);break;case"cols":case"rows":case"size":case"span":s!=null&&typeof s!="function"&&typeof s!="symbol"&&!isNaN(s)&&1<=s?t.setAttribute(a,s):t.removeAttribute(a);break;case"rowSpan":case"start":s==null||typeof s=="function"||typeof s=="symbol"||isNaN(s)?t.removeAttribute(a):t.setAttribute(a,s);break;case"popover":he("beforetoggle",t),he("toggle",t),na(t,"popover",s);break;case"xlinkActuate":dn(t,"http://www.w3.org/1999/xlink","xlink:actuate",s);break;case"xlinkArcrole":dn(t,"http://www.w3.org/1999/xlink","xlink:arcrole",s);break;case"xlinkRole":dn(t,"http://www.w3.org/1999/xlink","xlink:role",s);break;case"xlinkShow":dn(t,"http://www.w3.org/1999/xlink","xlink:show",s);break;case"xlinkTitle":dn(t,"http://www.w3.org/1999/xlink","xlink:title",s);break;case"xlinkType":dn(t,"http://www.w3.org/1999/xlink","xlink:type",s);break;case"xmlBase":dn(t,"http://www.w3.org/XML/1998/namespace","xml:base",s);break;case"xmlLang":dn(t,"http://www.w3.org/XML/1998/namespace","xml:lang",s);break;case"xmlSpace":dn(t,"http://www.w3.org/XML/1998/namespace","xml:space",s);break;case"is":na(t,"is",s);break;case"innerText":case"textContent":break;default:(!(2<a.length)||a[0]!=="o"&&a[0]!=="O"||a[1]!=="n"&&a[1]!=="N")&&(a=Wv.get(a)||a,na(t,a,s))}}function hf(t,n,a,s,u,f){switch(a){case"style":Hh(t,s,f);break;case"dangerouslySetInnerHTML":if(s!=null){if(typeof s!="object"||!("__html"in s))throw Error(r(61));if(a=s.__html,a!=null){if(u.children!=null)throw Error(r(60));t.innerHTML=a}}break;case"children":typeof s=="string"?_r(t,s):(typeof s=="number"||typeof s=="bigint")&&_r(t,""+s);break;case"onScroll":s!=null&&he("scroll",t);break;case"onScrollEnd":s!=null&&he("scrollend",t);break;case"onClick":s!=null&&(t.onclick=Ci);break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":break;case"innerText":case"textContent":break;default:if(!$t.hasOwnProperty(a))t:{if(a[0]==="o"&&a[1]==="n"&&(u=a.endsWith("Capture"),n=a.slice(2,u?a.length-7:void 0),f=t[Sn]||null,f=f!=null?f[a]:null,typeof f=="function"&&t.removeEventListener(n,f,u),typeof s=="function")){typeof f!="function"&&f!==null&&(a in t?t[a]=null:t.hasAttribute(a)&&t.removeAttribute(a)),t.addEventListener(n,s,u);break t}a in t?t[a]=s:s===!0?t.setAttribute(a,""):na(t,a,s)}}}function _n(t,n,a){switch(n){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":he("error",t),he("load",t);var s=!1,u=!1,f;for(f in a)if(a.hasOwnProperty(f)){var S=a[f];if(S!=null)switch(f){case"src":s=!0;break;case"srcSet":u=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(r(137,n));default:De(t,n,f,S,a,null)}}u&&De(t,n,"srcSet",a.srcSet,a,null),s&&De(t,n,"src",a.src,a,null);return;case"input":he("invalid",t);var E=f=S=u=null,I=null,Q=null;for(s in a)if(a.hasOwnProperty(s)){var ct=a[s];if(ct!=null)switch(s){case"name":u=ct;break;case"type":S=ct;break;case"checked":I=ct;break;case"defaultChecked":Q=ct;break;case"value":f=ct;break;case"defaultValue":E=ct;break;case"children":case"dangerouslySetInnerHTML":if(ct!=null)throw Error(r(137,n));break;default:De(t,n,s,ct,a,null)}}Rs(t,f,E,I,Q,S,u,!1);return;case"select":he("invalid",t),s=S=f=null;for(u in a)if(a.hasOwnProperty(u)&&(E=a[u],E!=null))switch(u){case"value":f=E;break;case"defaultValue":S=E;break;case"multiple":s=E;default:De(t,n,u,E,a,null)}n=f,a=S,t.multiple=!!s,n!=null?gr(t,!!s,n,!1):a!=null&&gr(t,!!s,a,!0);return;case"textarea":he("invalid",t),f=u=s=null;for(S in a)if(a.hasOwnProperty(S)&&(E=a[S],E!=null))switch(S){case"value":s=E;break;case"defaultValue":u=E;break;case"children":f=E;break;case"dangerouslySetInnerHTML":if(E!=null)throw Error(r(91));break;default:De(t,n,S,E,a,null)}Ih(t,s,u,f);return;case"option":for(I in a)a.hasOwnProperty(I)&&(s=a[I],s!=null)&&(I==="selected"?t.selected=s&&typeof s!="function"&&typeof s!="symbol":De(t,n,I,s,a,null));return;case"dialog":he("beforetoggle",t),he("toggle",t),he("cancel",t),he("close",t);break;case"iframe":case"object":he("load",t);break;case"video":case"audio":for(s=0;s<so.length;s++)he(so[s],t);break;case"image":he("error",t),he("load",t);break;case"details":he("toggle",t);break;case"embed":case"source":case"link":he("error",t),he("load",t);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(Q in a)if(a.hasOwnProperty(Q)&&(s=a[Q],s!=null))switch(Q){case"children":case"dangerouslySetInnerHTML":throw Error(r(137,n));default:De(t,n,Q,s,a,null)}return;default:if(bu(n)){for(ct in a)a.hasOwnProperty(ct)&&(s=a[ct],s!==void 0&&hf(t,n,ct,s,a,void 0));return}}for(E in a)a.hasOwnProperty(E)&&(s=a[E],s!=null&&De(t,n,E,s,a,null))}function _S(t,n,a,s){switch(n){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var u=null,f=null,S=null,E=null,I=null,Q=null,ct=null;for(ot in a){var pt=a[ot];if(a.hasOwnProperty(ot)&&pt!=null)switch(ot){case"checked":break;case"value":break;case"defaultValue":I=pt;default:s.hasOwnProperty(ot)||De(t,n,ot,null,s,pt)}}for(var $ in s){var ot=s[$];if(pt=a[$],s.hasOwnProperty($)&&(ot!=null||pt!=null))switch($){case"type":f=ot;break;case"name":u=ot;break;case"checked":Q=ot;break;case"defaultChecked":ct=ot;break;case"value":S=ot;break;case"defaultValue":E=ot;break;case"children":case"dangerouslySetInnerHTML":if(ot!=null)throw Error(r(137,n));break;default:ot!==pt&&De(t,n,$,ot,s,pt)}}As(t,S,E,I,Q,ct,f,u);return;case"select":ot=S=E=$=null;for(f in a)if(I=a[f],a.hasOwnProperty(f)&&I!=null)switch(f){case"value":break;case"multiple":ot=I;default:s.hasOwnProperty(f)||De(t,n,f,null,s,I)}for(u in s)if(f=s[u],I=a[u],s.hasOwnProperty(u)&&(f!=null||I!=null))switch(u){case"value":$=f;break;case"defaultValue":E=f;break;case"multiple":S=f;default:f!==I&&De(t,n,u,f,s,I)}n=E,a=S,s=ot,$!=null?gr(t,!!a,$,!1):!!s!=!!a&&(n!=null?gr(t,!!a,n,!0):gr(t,!!a,a?[]:"",!1));return;case"textarea":ot=$=null;for(E in a)if(u=a[E],a.hasOwnProperty(E)&&u!=null&&!s.hasOwnProperty(E))switch(E){case"value":break;case"children":break;default:De(t,n,E,null,s,u)}for(S in s)if(u=s[S],f=a[S],s.hasOwnProperty(S)&&(u!=null||f!=null))switch(S){case"value":$=u;break;case"defaultValue":ot=u;break;case"children":break;case"dangerouslySetInnerHTML":if(u!=null)throw Error(r(91));break;default:u!==f&&De(t,n,S,u,s,f)}Bh(t,$,ot);return;case"option":for(var Lt in a)$=a[Lt],a.hasOwnProperty(Lt)&&$!=null&&!s.hasOwnProperty(Lt)&&(Lt==="selected"?t.selected=!1:De(t,n,Lt,null,s,$));for(I in s)$=s[I],ot=a[I],s.hasOwnProperty(I)&&$!==ot&&($!=null||ot!=null)&&(I==="selected"?t.selected=$&&typeof $!="function"&&typeof $!="symbol":De(t,n,I,$,s,ot));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var Zt in a)$=a[Zt],a.hasOwnProperty(Zt)&&$!=null&&!s.hasOwnProperty(Zt)&&De(t,n,Zt,null,s,$);for(Q in s)if($=s[Q],ot=a[Q],s.hasOwnProperty(Q)&&$!==ot&&($!=null||ot!=null))switch(Q){case"children":case"dangerouslySetInnerHTML":if($!=null)throw Error(r(137,n));break;default:De(t,n,Q,$,s,ot)}return;default:if(bu(n)){for(var Le in a)$=a[Le],a.hasOwnProperty(Le)&&$!==void 0&&!s.hasOwnProperty(Le)&&hf(t,n,Le,void 0,s,$);for(ct in s)$=s[ct],ot=a[ct],!s.hasOwnProperty(ct)||$===ot||$===void 0&&ot===void 0||hf(t,n,ct,$,s,ot);return}}for(var k in a)$=a[k],a.hasOwnProperty(k)&&$!=null&&!s.hasOwnProperty(k)&&De(t,n,k,null,s,$);for(pt in s)$=s[pt],ot=a[pt],!s.hasOwnProperty(pt)||$===ot||$==null&&ot==null||De(t,n,pt,$,s,ot)}function Gm(t){switch(t){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}function vS(){if(typeof performance.getEntriesByType=="function"){for(var t=0,n=0,a=performance.getEntriesByType("resource"),s=0;s<a.length;s++){var u=a[s],f=u.transferSize,S=u.initiatorType,E=u.duration;if(f&&E&&Gm(S)){for(S=0,E=u.responseEnd,s+=1;s<a.length;s++){var I=a[s],Q=I.startTime;if(Q>E)break;var ct=I.transferSize,pt=I.initiatorType;ct&&Gm(pt)&&(I=I.responseEnd,S+=ct*(I<E?1:(E-Q)/(I-Q)))}if(--s,n+=8*(f+S)/(u.duration/1e3),t++,10<t)break}}if(0<t)return n/t/1e6}return navigator.connection&&(t=navigator.connection.downlink,typeof t=="number")?t:5}var df=null,pf=null;function wl(t){return t.nodeType===9?t:t.ownerDocument}function Vm(t){switch(t){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function Xm(t,n){if(t===0)switch(n){case"svg":return 1;case"math":return 2;default:return 0}return t===1&&n==="foreignObject"?0:t}function mf(t,n){return t==="textarea"||t==="noscript"||typeof n.children=="string"||typeof n.children=="number"||typeof n.children=="bigint"||typeof n.dangerouslySetInnerHTML=="object"&&n.dangerouslySetInnerHTML!==null&&n.dangerouslySetInnerHTML.__html!=null}var gf=null;function SS(){var t=window.event;return t&&t.type==="popstate"?t===gf?!1:(gf=t,!0):(gf=null,!1)}var Wm=typeof setTimeout=="function"?setTimeout:void 0,xS=typeof clearTimeout=="function"?clearTimeout:void 0,km=typeof Promise=="function"?Promise:void 0,MS=typeof queueMicrotask=="function"?queueMicrotask:typeof km<"u"?function(t){return km.resolve(null).then(t).catch(yS)}:Wm;function yS(t){setTimeout(function(){throw t})}function ya(t){return t==="head"}function qm(t,n){var a=n,s=0;do{var u=a.nextSibling;if(t.removeChild(a),u&&u.nodeType===8)if(a=u.data,a==="/$"||a==="/&"){if(s===0){t.removeChild(u),jr(n);return}s--}else if(a==="$"||a==="$?"||a==="$~"||a==="$!"||a==="&")s++;else if(a==="html")lo(t.ownerDocument.documentElement);else if(a==="head"){a=t.ownerDocument.head,lo(a);for(var f=a.firstChild;f;){var S=f.nextSibling,E=f.nodeName;f[st]||E==="SCRIPT"||E==="STYLE"||E==="LINK"&&f.rel.toLowerCase()==="stylesheet"||a.removeChild(f),f=S}}else a==="body"&&lo(t.ownerDocument.body);a=u}while(a);jr(n)}function Ym(t,n){var a=t;t=0;do{var s=a.nextSibling;if(a.nodeType===1?n?(a._stashedDisplay=a.style.display,a.style.display="none"):(a.style.display=a._stashedDisplay||"",a.getAttribute("style")===""&&a.removeAttribute("style")):a.nodeType===3&&(n?(a._stashedText=a.nodeValue,a.nodeValue=""):a.nodeValue=a._stashedText||""),s&&s.nodeType===8)if(a=s.data,a==="/$"){if(t===0)break;t--}else a!=="$"&&a!=="$?"&&a!=="$~"&&a!=="$!"||t++;a=s}while(a)}function _f(t){var n=t.firstChild;for(n&&n.nodeType===10&&(n=n.nextSibling);n;){var a=n;switch(n=n.nextSibling,a.nodeName){case"HTML":case"HEAD":case"BODY":_f(a),nt(a);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if(a.rel.toLowerCase()==="stylesheet")continue}t.removeChild(a)}}function ES(t,n,a,s){for(;t.nodeType===1;){var u=a;if(t.nodeName.toLowerCase()!==n.toLowerCase()){if(!s&&(t.nodeName!=="INPUT"||t.type!=="hidden"))break}else if(s){if(!t[st])switch(n){case"meta":if(!t.hasAttribute("itemprop"))break;return t;case"link":if(f=t.getAttribute("rel"),f==="stylesheet"&&t.hasAttribute("data-precedence"))break;if(f!==u.rel||t.getAttribute("href")!==(u.href==null||u.href===""?null:u.href)||t.getAttribute("crossorigin")!==(u.crossOrigin==null?null:u.crossOrigin)||t.getAttribute("title")!==(u.title==null?null:u.title))break;return t;case"style":if(t.hasAttribute("data-precedence"))break;return t;case"script":if(f=t.getAttribute("src"),(f!==(u.src==null?null:u.src)||t.getAttribute("type")!==(u.type==null?null:u.type)||t.getAttribute("crossorigin")!==(u.crossOrigin==null?null:u.crossOrigin))&&f&&t.hasAttribute("async")&&!t.hasAttribute("itemprop"))break;return t;default:return t}}else if(n==="input"&&t.type==="hidden"){var f=u.name==null?null:""+u.name;if(u.type==="hidden"&&t.getAttribute("name")===f)return t}else return t;if(t=ai(t.nextSibling),t===null)break}return null}function TS(t,n,a){if(n==="")return null;for(;t.nodeType!==3;)if((t.nodeType!==1||t.nodeName!=="INPUT"||t.type!=="hidden")&&!a||(t=ai(t.nextSibling),t===null))return null;return t}function jm(t,n){for(;t.nodeType!==8;)if((t.nodeType!==1||t.nodeName!=="INPUT"||t.type!=="hidden")&&!n||(t=ai(t.nextSibling),t===null))return null;return t}function vf(t){return t.data==="$?"||t.data==="$~"}function Sf(t){return t.data==="$!"||t.data==="$?"&&t.ownerDocument.readyState!=="loading"}function bS(t,n){var a=t.ownerDocument;if(t.data==="$~")t._reactRetry=n;else if(t.data!=="$?"||a.readyState!=="loading")n();else{var s=function(){n(),a.removeEventListener("DOMContentLoaded",s)};a.addEventListener("DOMContentLoaded",s),t._reactRetry=s}}function ai(t){for(;t!=null;t=t.nextSibling){var n=t.nodeType;if(n===1||n===3)break;if(n===8){if(n=t.data,n==="$"||n==="$!"||n==="$?"||n==="$~"||n==="&"||n==="F!"||n==="F")break;if(n==="/$"||n==="/&")return null}}return t}var xf=null;function Zm(t){t=t.nextSibling;for(var n=0;t;){if(t.nodeType===8){var a=t.data;if(a==="/$"||a==="/&"){if(n===0)return ai(t.nextSibling);n--}else a!=="$"&&a!=="$!"&&a!=="$?"&&a!=="$~"&&a!=="&"||n++}t=t.nextSibling}return null}function Km(t){t=t.previousSibling;for(var n=0;t;){if(t.nodeType===8){var a=t.data;if(a==="$"||a==="$!"||a==="$?"||a==="$~"||a==="&"){if(n===0)return t;n--}else a!=="/$"&&a!=="/&"||n++}t=t.previousSibling}return null}function Qm(t,n,a){switch(n=wl(a),t){case"html":if(t=n.documentElement,!t)throw Error(r(452));return t;case"head":if(t=n.head,!t)throw Error(r(453));return t;case"body":if(t=n.body,!t)throw Error(r(454));return t;default:throw Error(r(451))}}function lo(t){for(var n=t.attributes;n.length;)t.removeAttributeNode(n[0]);nt(t)}var ri=new Map,Jm=new Set;function Dl(t){return typeof t.getRootNode=="function"?t.getRootNode():t.nodeType===9?t:t.ownerDocument}var Wi=q.d;q.d={f:AS,r:RS,D:CS,C:wS,L:DS,m:LS,X:NS,S:US,M:OS};function AS(){var t=Wi.f(),n=Ml();return t||n}function RS(t){var n=Ot(t);n!==null&&n.tag===5&&n.type==="form"?mp(n):Wi.r(t)}var kr=typeof document>"u"?null:document;function $m(t,n,a){var s=kr;if(s&&typeof n=="string"&&n){var u=xn(n);u='link[rel="'+t+'"][href="'+u+'"]',typeof a=="string"&&(u+='[crossorigin="'+a+'"]'),Jm.has(u)||(Jm.add(u),t={rel:t,crossOrigin:a,href:n},s.querySelector(u)===null&&(n=s.createElement("link"),_n(n,"link",t),Bt(n),s.head.appendChild(n)))}}function CS(t){Wi.D(t),$m("dns-prefetch",t,null)}function wS(t,n){Wi.C(t,n),$m("preconnect",t,n)}function DS(t,n,a){Wi.L(t,n,a);var s=kr;if(s&&t&&n){var u='link[rel="preload"][as="'+xn(n)+'"]';n==="image"&&a&&a.imageSrcSet?(u+='[imagesrcset="'+xn(a.imageSrcSet)+'"]',typeof a.imageSizes=="string"&&(u+='[imagesizes="'+xn(a.imageSizes)+'"]')):u+='[href="'+xn(t)+'"]';var f=u;switch(n){case"style":f=qr(t);break;case"script":f=Yr(t)}ri.has(f)||(t=_({rel:"preload",href:n==="image"&&a&&a.imageSrcSet?void 0:t,as:n},a),ri.set(f,t),s.querySelector(u)!==null||n==="style"&&s.querySelector(uo(f))||n==="script"&&s.querySelector(co(f))||(n=s.createElement("link"),_n(n,"link",t),Bt(n),s.head.appendChild(n)))}}function LS(t,n){Wi.m(t,n);var a=kr;if(a&&t){var s=n&&typeof n.as=="string"?n.as:"script",u='link[rel="modulepreload"][as="'+xn(s)+'"][href="'+xn(t)+'"]',f=u;switch(s){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":f=Yr(t)}if(!ri.has(f)&&(t=_({rel:"modulepreload",href:t},n),ri.set(f,t),a.querySelector(u)===null)){switch(s){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(a.querySelector(co(f)))return}s=a.createElement("link"),_n(s,"link",t),Bt(s),a.head.appendChild(s)}}}function US(t,n,a){Wi.S(t,n,a);var s=kr;if(s&&t){var u=Yt(s).hoistableStyles,f=qr(t);n=n||"default";var S=u.get(f);if(!S){var E={loading:0,preload:null};if(S=s.querySelector(uo(f)))E.loading=5;else{t=_({rel:"stylesheet",href:t,"data-precedence":n},a),(a=ri.get(f))&&Mf(t,a);var I=S=s.createElement("link");Bt(I),_n(I,"link",t),I._p=new Promise(function(Q,ct){I.onload=Q,I.onerror=ct}),I.addEventListener("load",function(){E.loading|=1}),I.addEventListener("error",function(){E.loading|=2}),E.loading|=4,Ll(S,n,s)}S={type:"stylesheet",instance:S,count:1,state:E},u.set(f,S)}}}function NS(t,n){Wi.X(t,n);var a=kr;if(a&&t){var s=Yt(a).hoistableScripts,u=Yr(t),f=s.get(u);f||(f=a.querySelector(co(u)),f||(t=_({src:t,async:!0},n),(n=ri.get(u))&&yf(t,n),f=a.createElement("script"),Bt(f),_n(f,"link",t),a.head.appendChild(f)),f={type:"script",instance:f,count:1,state:null},s.set(u,f))}}function OS(t,n){Wi.M(t,n);var a=kr;if(a&&t){var s=Yt(a).hoistableScripts,u=Yr(t),f=s.get(u);f||(f=a.querySelector(co(u)),f||(t=_({src:t,async:!0,type:"module"},n),(n=ri.get(u))&&yf(t,n),f=a.createElement("script"),Bt(f),_n(f,"link",t),a.head.appendChild(f)),f={type:"script",instance:f,count:1,state:null},s.set(u,f))}}function tg(t,n,a,s){var u=(u=xt.current)?Dl(u):null;if(!u)throw Error(r(446));switch(t){case"meta":case"title":return null;case"style":return typeof a.precedence=="string"&&typeof a.href=="string"?(n=qr(a.href),a=Yt(u).hoistableStyles,s=a.get(n),s||(s={type:"style",instance:null,count:0,state:null},a.set(n,s)),s):{type:"void",instance:null,count:0,state:null};case"link":if(a.rel==="stylesheet"&&typeof a.href=="string"&&typeof a.precedence=="string"){t=qr(a.href);var f=Yt(u).hoistableStyles,S=f.get(t);if(S||(u=u.ownerDocument||u,S={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},f.set(t,S),(f=u.querySelector(uo(t)))&&!f._p&&(S.instance=f,S.state.loading=5),ri.has(t)||(a={rel:"preload",as:"style",href:a.href,crossOrigin:a.crossOrigin,integrity:a.integrity,media:a.media,hrefLang:a.hrefLang,referrerPolicy:a.referrerPolicy},ri.set(t,a),f||zS(u,t,a,S.state))),n&&s===null)throw Error(r(528,""));return S}if(n&&s!==null)throw Error(r(529,""));return null;case"script":return n=a.async,a=a.src,typeof a=="string"&&n&&typeof n!="function"&&typeof n!="symbol"?(n=Yr(a),a=Yt(u).hoistableScripts,s=a.get(n),s||(s={type:"script",instance:null,count:0,state:null},a.set(n,s)),s):{type:"void",instance:null,count:0,state:null};default:throw Error(r(444,t))}}function qr(t){return'href="'+xn(t)+'"'}function uo(t){return'link[rel="stylesheet"]['+t+"]"}function eg(t){return _({},t,{"data-precedence":t.precedence,precedence:null})}function zS(t,n,a,s){t.querySelector('link[rel="preload"][as="style"]['+n+"]")?s.loading=1:(n=t.createElement("link"),s.preload=n,n.addEventListener("load",function(){return s.loading|=1}),n.addEventListener("error",function(){return s.loading|=2}),_n(n,"link",a),Bt(n),t.head.appendChild(n))}function Yr(t){return'[src="'+xn(t)+'"]'}function co(t){return"script[async]"+t}function ng(t,n,a){if(n.count++,n.instance===null)switch(n.type){case"style":var s=t.querySelector('style[data-href~="'+xn(a.href)+'"]');if(s)return n.instance=s,Bt(s),s;var u=_({},a,{"data-href":a.href,"data-precedence":a.precedence,href:null,precedence:null});return s=(t.ownerDocument||t).createElement("style"),Bt(s),_n(s,"style",u),Ll(s,a.precedence,t),n.instance=s;case"stylesheet":u=qr(a.href);var f=t.querySelector(uo(u));if(f)return n.state.loading|=4,n.instance=f,Bt(f),f;s=eg(a),(u=ri.get(u))&&Mf(s,u),f=(t.ownerDocument||t).createElement("link"),Bt(f);var S=f;return S._p=new Promise(function(E,I){S.onload=E,S.onerror=I}),_n(f,"link",s),n.state.loading|=4,Ll(f,a.precedence,t),n.instance=f;case"script":return f=Yr(a.src),(u=t.querySelector(co(f)))?(n.instance=u,Bt(u),u):(s=a,(u=ri.get(f))&&(s=_({},a),yf(s,u)),t=t.ownerDocument||t,u=t.createElement("script"),Bt(u),_n(u,"link",s),t.head.appendChild(u),n.instance=u);case"void":return null;default:throw Error(r(443,n.type))}else n.type==="stylesheet"&&(n.state.loading&4)===0&&(s=n.instance,n.state.loading|=4,Ll(s,a.precedence,t));return n.instance}function Ll(t,n,a){for(var s=a.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),u=s.length?s[s.length-1]:null,f=u,S=0;S<s.length;S++){var E=s[S];if(E.dataset.precedence===n)f=E;else if(f!==u)break}f?f.parentNode.insertBefore(t,f.nextSibling):(n=a.nodeType===9?a.head:a,n.insertBefore(t,n.firstChild))}function Mf(t,n){t.crossOrigin==null&&(t.crossOrigin=n.crossOrigin),t.referrerPolicy==null&&(t.referrerPolicy=n.referrerPolicy),t.title==null&&(t.title=n.title)}function yf(t,n){t.crossOrigin==null&&(t.crossOrigin=n.crossOrigin),t.referrerPolicy==null&&(t.referrerPolicy=n.referrerPolicy),t.integrity==null&&(t.integrity=n.integrity)}var Ul=null;function ig(t,n,a){if(Ul===null){var s=new Map,u=Ul=new Map;u.set(a,s)}else u=Ul,s=u.get(a),s||(s=new Map,u.set(a,s));if(s.has(t))return s;for(s.set(t,null),a=a.getElementsByTagName(t),u=0;u<a.length;u++){var f=a[u];if(!(f[st]||f[Ze]||t==="link"&&f.getAttribute("rel")==="stylesheet")&&f.namespaceURI!=="http://www.w3.org/2000/svg"){var S=f.getAttribute(n)||"";S=t+S;var E=s.get(S);E?E.push(f):s.set(S,[f])}}return s}function ag(t,n,a){t=t.ownerDocument||t,t.head.insertBefore(a,n==="title"?t.querySelector("head > title"):null)}function PS(t,n,a){if(a===1||n.itemProp!=null)return!1;switch(t){case"meta":case"title":return!0;case"style":if(typeof n.precedence!="string"||typeof n.href!="string"||n.href==="")break;return!0;case"link":if(typeof n.rel!="string"||typeof n.href!="string"||n.href===""||n.onLoad||n.onError)break;return n.rel==="stylesheet"?(t=n.disabled,typeof n.precedence=="string"&&t==null):!0;case"script":if(n.async&&typeof n.async!="function"&&typeof n.async!="symbol"&&!n.onLoad&&!n.onError&&n.src&&typeof n.src=="string")return!0}return!1}function rg(t){return!(t.type==="stylesheet"&&(t.state.loading&3)===0)}function BS(t,n,a,s){if(a.type==="stylesheet"&&(typeof s.media!="string"||matchMedia(s.media).matches!==!1)&&(a.state.loading&4)===0){if(a.instance===null){var u=qr(s.href),f=n.querySelector(uo(u));if(f){n=f._p,n!==null&&typeof n=="object"&&typeof n.then=="function"&&(t.count++,t=Nl.bind(t),n.then(t,t)),a.state.loading|=4,a.instance=f,Bt(f);return}f=n.ownerDocument||n,s=eg(s),(u=ri.get(u))&&Mf(s,u),f=f.createElement("link"),Bt(f);var S=f;S._p=new Promise(function(E,I){S.onload=E,S.onerror=I}),_n(f,"link",s),a.instance=f}t.stylesheets===null&&(t.stylesheets=new Map),t.stylesheets.set(a,n),(n=a.state.preload)&&(a.state.loading&3)===0&&(t.count++,a=Nl.bind(t),n.addEventListener("load",a),n.addEventListener("error",a))}}var Ef=0;function IS(t,n){return t.stylesheets&&t.count===0&&zl(t,t.stylesheets),0<t.count||0<t.imgCount?function(a){var s=setTimeout(function(){if(t.stylesheets&&zl(t,t.stylesheets),t.unsuspend){var f=t.unsuspend;t.unsuspend=null,f()}},6e4+n);0<t.imgBytes&&Ef===0&&(Ef=62500*vS());var u=setTimeout(function(){if(t.waitingForImages=!1,t.count===0&&(t.stylesheets&&zl(t,t.stylesheets),t.unsuspend)){var f=t.unsuspend;t.unsuspend=null,f()}},(t.imgBytes>Ef?50:800)+n);return t.unsuspend=a,function(){t.unsuspend=null,clearTimeout(s),clearTimeout(u)}}:null}function Nl(){if(this.count--,this.count===0&&(this.imgCount===0||!this.waitingForImages)){if(this.stylesheets)zl(this,this.stylesheets);else if(this.unsuspend){var t=this.unsuspend;this.unsuspend=null,t()}}}var Ol=null;function zl(t,n){t.stylesheets=null,t.unsuspend!==null&&(t.count++,Ol=new Map,n.forEach(FS,t),Ol=null,Nl.call(t))}function FS(t,n){if(!(n.state.loading&4)){var a=Ol.get(t);if(a)var s=a.get(null);else{a=new Map,Ol.set(t,a);for(var u=t.querySelectorAll("link[data-precedence],style[data-precedence]"),f=0;f<u.length;f++){var S=u[f];(S.nodeName==="LINK"||S.getAttribute("media")!=="not all")&&(a.set(S.dataset.precedence,S),s=S)}s&&a.set(null,s)}u=n.instance,S=u.getAttribute("data-precedence"),f=a.get(S)||s,f===s&&a.set(null,u),a.set(S,u),this.count++,s=Nl.bind(this),u.addEventListener("load",s),u.addEventListener("error",s),f?f.parentNode.insertBefore(u,f.nextSibling):(t=t.nodeType===9?t.head:t,t.insertBefore(u,t.firstChild)),n.state.loading|=4}}var fo={$$typeof:T,Provider:null,Consumer:null,_currentValue:J,_currentValue2:J,_threadCount:0};function HS(t,n,a,s,u,f,S,E,I){this.tag=1,this.containerInfo=t,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=Xe(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Xe(0),this.hiddenUpdates=Xe(null),this.identifierPrefix=s,this.onUncaughtError=u,this.onCaughtError=f,this.onRecoverableError=S,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=I,this.incompleteTransitions=new Map}function sg(t,n,a,s,u,f,S,E,I,Q,ct,pt){return t=new HS(t,n,a,S,I,Q,ct,pt,E),n=1,f===!0&&(n|=24),f=Vn(3,null,null,n),t.current=f,f.stateNode=t,n=ec(),n.refCount++,t.pooledCache=n,n.refCount++,f.memoizedState={element:s,isDehydrated:a,cache:n},rc(f),t}function og(t){return t?(t=Tr,t):Tr}function lg(t,n,a,s,u,f){u=og(u),s.context===null?s.context=u:s.pendingContext=u,s=fa(n),s.payload={element:a},f=f===void 0?null:f,f!==null&&(s.callback=f),a=ha(t,s,n),a!==null&&(Bn(a,t,n),Xs(a,t,n))}function ug(t,n){if(t=t.memoizedState,t!==null&&t.dehydrated!==null){var a=t.retryLane;t.retryLane=a!==0&&a<n?a:n}}function Tf(t,n){ug(t,n),(t=t.alternate)&&ug(t,n)}function cg(t){if(t.tag===13||t.tag===31){var n=Wa(t,67108864);n!==null&&Bn(n,t,67108864),Tf(t,67108864)}}function fg(t){if(t.tag===13||t.tag===31){var n=Yn();n=ys(n);var a=Wa(t,n);a!==null&&Bn(a,t,n),Tf(t,n)}}var Pl=!0;function GS(t,n,a,s){var u=P.T;P.T=null;var f=q.p;try{q.p=2,bf(t,n,a,s)}finally{q.p=f,P.T=u}}function VS(t,n,a,s){var u=P.T;P.T=null;var f=q.p;try{q.p=8,bf(t,n,a,s)}finally{q.p=f,P.T=u}}function bf(t,n,a,s){if(Pl){var u=Af(s);if(u===null)ff(t,n,s,Bl,a),dg(t,s);else if(WS(u,t,n,a,s))s.stopPropagation();else if(dg(t,s),n&4&&-1<XS.indexOf(t)){for(;u!==null;){var f=Ot(u);if(f!==null)switch(f.tag){case 3:if(f=f.stateNode,f.current.memoizedState.isDehydrated){var S=Tt(f.pendingLanes);if(S!==0){var E=f;for(E.pendingLanes|=2,E.entangledLanes|=2;S;){var I=1<<31-Xt(S);E.entanglements[1]|=I,S&=~I}Ti(f),(xe&6)===0&&(Sl=gt()+500,ro(0))}}break;case 31:case 13:E=Wa(f,2),E!==null&&Bn(E,f,2),Ml(),Tf(f,2)}if(f=Af(s),f===null&&ff(t,n,s,Bl,a),f===u)break;u=f}u!==null&&s.stopPropagation()}else ff(t,n,s,null,a)}}function Af(t){return t=Ru(t),Rf(t)}var Bl=null;function Rf(t){if(Bl=null,t=Ct(t),t!==null){var n=c(t);if(n===null)t=null;else{var a=n.tag;if(a===13){if(t=d(n),t!==null)return t;t=null}else if(a===31){if(t=h(n),t!==null)return t;t=null}else if(a===3){if(n.stateNode.current.memoizedState.isDehydrated)return n.tag===3?n.stateNode.containerInfo:null;t=null}else n!==t&&(t=null)}}return Bl=t,null}function hg(t){switch(t){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(Ht()){case Rt:return 2;case Ut:return 8;case qt:case ie:return 32;case _t:return 268435456;default:return 32}default:return 32}}var Cf=!1,Ea=null,Ta=null,ba=null,ho=new Map,po=new Map,Aa=[],XS="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function dg(t,n){switch(t){case"focusin":case"focusout":Ea=null;break;case"dragenter":case"dragleave":Ta=null;break;case"mouseover":case"mouseout":ba=null;break;case"pointerover":case"pointerout":ho.delete(n.pointerId);break;case"gotpointercapture":case"lostpointercapture":po.delete(n.pointerId)}}function mo(t,n,a,s,u,f){return t===null||t.nativeEvent!==f?(t={blockedOn:n,domEventName:a,eventSystemFlags:s,nativeEvent:f,targetContainers:[u]},n!==null&&(n=Ot(n),n!==null&&cg(n)),t):(t.eventSystemFlags|=s,n=t.targetContainers,u!==null&&n.indexOf(u)===-1&&n.push(u),t)}function WS(t,n,a,s,u){switch(n){case"focusin":return Ea=mo(Ea,t,n,a,s,u),!0;case"dragenter":return Ta=mo(Ta,t,n,a,s,u),!0;case"mouseover":return ba=mo(ba,t,n,a,s,u),!0;case"pointerover":var f=u.pointerId;return ho.set(f,mo(ho.get(f)||null,t,n,a,s,u)),!0;case"gotpointercapture":return f=u.pointerId,po.set(f,mo(po.get(f)||null,t,n,a,s,u)),!0}return!1}function pg(t){var n=Ct(t.target);if(n!==null){var a=c(n);if(a!==null){if(n=a.tag,n===13){if(n=d(a),n!==null){t.blockedOn=n,Ha(t.priority,function(){fg(a)});return}}else if(n===31){if(n=h(a),n!==null){t.blockedOn=n,Ha(t.priority,function(){fg(a)});return}}else if(n===3&&a.stateNode.current.memoizedState.isDehydrated){t.blockedOn=a.tag===3?a.stateNode.containerInfo:null;return}}}t.blockedOn=null}function Il(t){if(t.blockedOn!==null)return!1;for(var n=t.targetContainers;0<n.length;){var a=Af(t.nativeEvent);if(a===null){a=t.nativeEvent;var s=new a.constructor(a.type,a);Au=s,a.target.dispatchEvent(s),Au=null}else return n=Ot(a),n!==null&&cg(n),t.blockedOn=a,!1;n.shift()}return!0}function mg(t,n,a){Il(t)&&a.delete(n)}function kS(){Cf=!1,Ea!==null&&Il(Ea)&&(Ea=null),Ta!==null&&Il(Ta)&&(Ta=null),ba!==null&&Il(ba)&&(ba=null),ho.forEach(mg),po.forEach(mg)}function Fl(t,n){t.blockedOn===n&&(t.blockedOn=null,Cf||(Cf=!0,o.unstable_scheduleCallback(o.unstable_NormalPriority,kS)))}var Hl=null;function gg(t){Hl!==t&&(Hl=t,o.unstable_scheduleCallback(o.unstable_NormalPriority,function(){Hl===t&&(Hl=null);for(var n=0;n<t.length;n+=3){var a=t[n],s=t[n+1],u=t[n+2];if(typeof s!="function"){if(Rf(s||a)===null)continue;break}var f=Ot(a);f!==null&&(t.splice(n,3),n-=3,bc(f,{pending:!0,data:u,method:a.method,action:s},s,u))}}))}function jr(t){function n(I){return Fl(I,t)}Ea!==null&&Fl(Ea,t),Ta!==null&&Fl(Ta,t),ba!==null&&Fl(ba,t),ho.forEach(n),po.forEach(n);for(var a=0;a<Aa.length;a++){var s=Aa[a];s.blockedOn===t&&(s.blockedOn=null)}for(;0<Aa.length&&(a=Aa[0],a.blockedOn===null);)pg(a),a.blockedOn===null&&Aa.shift();if(a=(t.ownerDocument||t).$$reactFormReplay,a!=null)for(s=0;s<a.length;s+=3){var u=a[s],f=a[s+1],S=u[Sn]||null;if(typeof f=="function")S||gg(a);else if(S){var E=null;if(f&&f.hasAttribute("formAction")){if(u=f,S=f[Sn]||null)E=S.formAction;else if(Rf(u)!==null)continue}else E=S.action;typeof E=="function"?a[s+1]=E:(a.splice(s,3),s-=3),gg(a)}}}function _g(){function t(f){f.canIntercept&&f.info==="react-transition"&&f.intercept({handler:function(){return new Promise(function(S){return u=S})},focusReset:"manual",scroll:"manual"})}function n(){u!==null&&(u(),u=null),s||setTimeout(a,20)}function a(){if(!s&&!navigation.transition){var f=navigation.currentEntry;f&&f.url!=null&&navigation.navigate(f.url,{state:f.getState(),info:"react-transition",history:"replace"})}}if(typeof navigation=="object"){var s=!1,u=null;return navigation.addEventListener("navigate",t),navigation.addEventListener("navigatesuccess",n),navigation.addEventListener("navigateerror",n),setTimeout(a,100),function(){s=!0,navigation.removeEventListener("navigate",t),navigation.removeEventListener("navigatesuccess",n),navigation.removeEventListener("navigateerror",n),u!==null&&(u(),u=null)}}}function wf(t){this._internalRoot=t}Gl.prototype.render=wf.prototype.render=function(t){var n=this._internalRoot;if(n===null)throw Error(r(409));var a=n.current,s=Yn();lg(a,s,t,n,null,null)},Gl.prototype.unmount=wf.prototype.unmount=function(){var t=this._internalRoot;if(t!==null){this._internalRoot=null;var n=t.containerInfo;lg(t.current,2,null,t,null,null),Ml(),n[ea]=null}};function Gl(t){this._internalRoot=t}Gl.prototype.unstable_scheduleHydration=function(t){if(t){var n=Es();t={blockedOn:null,target:t,priority:n};for(var a=0;a<Aa.length&&n!==0&&n<Aa[a].priority;a++);Aa.splice(a,0,t),a===0&&pg(t)}};var vg=e.version;if(vg!=="19.2.3")throw Error(r(527,vg,"19.2.3"));q.findDOMNode=function(t){var n=t._reactInternals;if(n===void 0)throw typeof t.render=="function"?Error(r(188)):(t=Object.keys(t).join(","),Error(r(268,t)));return t=p(n),t=t!==null?g(t):null,t=t===null?null:t.stateNode,t};var qS={bundleType:0,version:"19.2.3",rendererPackageName:"react-dom",currentDispatcherRef:P,reconcilerVersion:"19.2.3"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var Vl=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!Vl.isDisabled&&Vl.supportsFiber)try{Kt=Vl.inject(qS),Dt=Vl}catch{}}return _o.createRoot=function(t,n){if(!l(t))throw Error(r(299));var a=!1,s="",u=bp,f=Ap,S=Rp;return n!=null&&(n.unstable_strictMode===!0&&(a=!0),n.identifierPrefix!==void 0&&(s=n.identifierPrefix),n.onUncaughtError!==void 0&&(u=n.onUncaughtError),n.onCaughtError!==void 0&&(f=n.onCaughtError),n.onRecoverableError!==void 0&&(S=n.onRecoverableError)),n=sg(t,1,!1,null,null,a,s,null,u,f,S,_g),t[ea]=n.current,cf(t),new wf(n)},_o.hydrateRoot=function(t,n,a){if(!l(t))throw Error(r(299));var s=!1,u="",f=bp,S=Ap,E=Rp,I=null;return a!=null&&(a.unstable_strictMode===!0&&(s=!0),a.identifierPrefix!==void 0&&(u=a.identifierPrefix),a.onUncaughtError!==void 0&&(f=a.onUncaughtError),a.onCaughtError!==void 0&&(S=a.onCaughtError),a.onRecoverableError!==void 0&&(E=a.onRecoverableError),a.formState!==void 0&&(I=a.formState)),n=sg(t,1,!0,n,a??null,s,u,I,f,S,E,_g),n.context=og(null),a=n.current,s=Yn(),s=ys(s),u=fa(s),u.callback=null,ha(a,u,s),a=s,n.current.lanes=a,qe(n,a),Ti(n),t[ea]=n.current,cf(t),new Gl(n)},_o.version="19.2.3",_o}var Cg;function ax(){if(Cg)return Uf.exports;Cg=1;function o(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(o)}catch(e){console.error(e)}}return o(),Uf.exports=ix(),Uf.exports}var AA=ax();const rx="modulepreload",sx=function(o){return"/"+o},wg={},RA=function(e,i,r){let l=Promise.resolve();if(i&&i.length>0){let m=function(p){return Promise.all(p.map(g=>Promise.resolve(g).then(_=>({status:"fulfilled",value:_}),_=>({status:"rejected",reason:_}))))};document.getElementsByTagName("link");const d=document.querySelector("meta[property=csp-nonce]"),h=d?.nonce||d?.getAttribute("nonce");l=m(i.map(p=>{if(p=sx(p),p in wg)return;wg[p]=!0;const g=p.endsWith(".css"),_=g?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${p}"]${_}`))return;const x=document.createElement("link");if(x.rel=g?"stylesheet":rx,g||(x.as="script"),x.crossOrigin="",x.href=p,h&&x.setAttribute("nonce",h),document.head.appendChild(x),g)return new Promise((y,b)=>{x.addEventListener("load",y),x.addEventListener("error",()=>b(new Error(`Unable to preload CSS for ${p}`)))})}))}function c(d){const h=new Event("vite:preloadError",{cancelable:!0});if(h.payload=d,window.dispatchEvent(h),!h.defaultPrevented)throw d}return l.then(d=>{for(const h of d||[])h.status==="rejected"&&c(h.reason);return e().catch(c)})},Dg=o=>{let e;const i=new Set,r=(p,g)=>{const _=typeof p=="function"?p(e):p;if(!Object.is(_,e)){const x=e;e=g??(typeof _!="object"||_===null)?_:Object.assign({},e,_),i.forEach(y=>y(e,x))}},l=()=>e,h={setState:r,getState:l,getInitialState:()=>m,subscribe:p=>(i.add(p),()=>i.delete(p))},m=e=o(r,l,h);return h},ox=(o=>o?Dg(o):Dg),lx=o=>o;function ux(o,e=lx){const i=To.useSyncExternalStore(o.subscribe,To.useCallback(()=>e(o.getState()),[o,e]),To.useCallback(()=>e(o.getInitialState()),[o,e]));return To.useDebugValue(i),i}const Lg=o=>{const e=ox(o),i=r=>ux(e,r);return Object.assign(i,e),i},CA=(o=>o?Lg(o):Lg);const Ch="160",wA={ROTATE:0,DOLLY:1,PAN:2},DA={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},cx=0,Ug=1,fx=2,sv=1,hx=2,Ki=3,Fa=0,Fn=1,Qi=2,Pa=0,ds=1,Ng=2,Og=3,zg=4,dx=5,ur=100,px=101,mx=102,Pg=103,Bg=104,gx=200,_x=201,vx=202,Sx=203,vh=204,Sh=205,xx=206,Mx=207,yx=208,Ex=209,Tx=210,bx=211,Ax=212,Rx=213,Cx=214,wx=0,Dx=1,Lx=2,pu=3,Ux=4,Nx=5,Ox=6,zx=7,ov=0,Px=1,Bx=2,Ba=0,Ix=1,Fx=2,Hx=3,Gx=4,Vx=5,Xx=6,lv=300,ms=301,gs=302,xh=303,Mh=304,xu=306,yh=1e3,vi=1001,Eh=1002,wn=1003,Ig=1004,Pf=1005,oi=1006,Wx=1007,Ao=1008,Ia=1009,kx=1010,qx=1011,wh=1012,uv=1013,Na=1014,Oa=1015,Ro=1016,cv=1017,fv=1018,fr=1020,Yx=1021,Si=1023,jx=1024,Zx=1025,hr=1026,_s=1027,Kx=1028,hv=1029,Qx=1030,dv=1031,pv=1033,Bf=33776,If=33777,Ff=33778,Hf=33779,Fg=35840,Hg=35841,Gg=35842,Vg=35843,mv=36196,Xg=37492,Wg=37496,kg=37808,qg=37809,Yg=37810,jg=37811,Zg=37812,Kg=37813,Qg=37814,Jg=37815,$g=37816,t_=37817,e_=37818,n_=37819,i_=37820,a_=37821,Gf=36492,r_=36494,s_=36495,Jx=36283,o_=36284,l_=36285,u_=36286,gv=3e3,dr=3001,$x=3200,tM=3201,_v=0,eM=1,ui="",vn="srgb",$i="srgb-linear",Dh="display-p3",Mu="display-p3-linear",mu="linear",Fe="srgb",gu="rec709",_u="p3",Zr=7680,c_=519,nM=512,iM=513,aM=514,vv=515,rM=516,sM=517,oM=518,lM=519,f_=35044,h_="300 es",Th=1035,Ji=2e3,vu=2001;class Ss{addEventListener(e,i){this._listeners===void 0&&(this._listeners={});const r=this._listeners;r[e]===void 0&&(r[e]=[]),r[e].indexOf(i)===-1&&r[e].push(i)}hasEventListener(e,i){if(this._listeners===void 0)return!1;const r=this._listeners;return r[e]!==void 0&&r[e].indexOf(i)!==-1}removeEventListener(e,i){if(this._listeners===void 0)return;const l=this._listeners[e];if(l!==void 0){const c=l.indexOf(i);c!==-1&&l.splice(c,1)}}dispatchEvent(e){if(this._listeners===void 0)return;const r=this._listeners[e.type];if(r!==void 0){e.target=this;const l=r.slice(0);for(let c=0,d=l.length;c<d;c++)l[c].call(this,e);e.target=null}}}const yn=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],hu=Math.PI/180,bh=180/Math.PI;function wo(){const o=Math.random()*4294967295|0,e=Math.random()*4294967295|0,i=Math.random()*4294967295|0,r=Math.random()*4294967295|0;return(yn[o&255]+yn[o>>8&255]+yn[o>>16&255]+yn[o>>24&255]+"-"+yn[e&255]+yn[e>>8&255]+"-"+yn[e>>16&15|64]+yn[e>>24&255]+"-"+yn[i&63|128]+yn[i>>8&255]+"-"+yn[i>>16&255]+yn[i>>24&255]+yn[r&255]+yn[r>>8&255]+yn[r>>16&255]+yn[r>>24&255]).toLowerCase()}function Dn(o,e,i){return Math.max(e,Math.min(i,o))}function uM(o,e){return(o%e+e)%e}function Vf(o,e,i){return(1-i)*o+i*e}function d_(o){return(o&o-1)===0&&o!==0}function Ah(o){return Math.pow(2,Math.floor(Math.log(o)/Math.LN2))}function vo(o,e){switch(e.constructor){case Float32Array:return o;case Uint32Array:return o/4294967295;case Uint16Array:return o/65535;case Uint8Array:return o/255;case Int32Array:return Math.max(o/2147483647,-1);case Int16Array:return Math.max(o/32767,-1);case Int8Array:return Math.max(o/127,-1);default:throw new Error("Invalid component type.")}}function In(o,e){switch(e.constructor){case Float32Array:return o;case Uint32Array:return Math.round(o*4294967295);case Uint16Array:return Math.round(o*65535);case Uint8Array:return Math.round(o*255);case Int32Array:return Math.round(o*2147483647);case Int16Array:return Math.round(o*32767);case Int8Array:return Math.round(o*127);default:throw new Error("Invalid component type.")}}const LA={DEG2RAD:hu};class ge{constructor(e=0,i=0){ge.prototype.isVector2=!0,this.x=e,this.y=i}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,i){return this.x=e,this.y=i,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const i=this.x,r=this.y,l=e.elements;return this.x=l[0]*i+l[3]*r+l[6],this.y=l[1]*i+l[4]*r+l[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,i){return this.x=Math.max(e.x,Math.min(i.x,this.x)),this.y=Math.max(e.y,Math.min(i.y,this.y)),this}clampScalar(e,i){return this.x=Math.max(e,Math.min(i,this.x)),this.y=Math.max(e,Math.min(i,this.y)),this}clampLength(e,i){const r=this.length();return this.divideScalar(r||1).multiplyScalar(Math.max(e,Math.min(i,r)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const i=Math.sqrt(this.lengthSq()*e.lengthSq());if(i===0)return Math.PI/2;const r=this.dot(e)/i;return Math.acos(Dn(r,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const i=this.x-e.x,r=this.y-e.y;return i*i+r*r}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this}lerpVectors(e,i,r){return this.x=e.x+(i.x-e.x)*r,this.y=e.y+(i.y-e.y)*r,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this}rotateAround(e,i){const r=Math.cos(i),l=Math.sin(i),c=this.x-e.x,d=this.y-e.y;return this.x=c*r-d*l+e.x,this.y=c*l+d*r+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class ce{constructor(e,i,r,l,c,d,h,m,p){ce.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,i,r,l,c,d,h,m,p)}set(e,i,r,l,c,d,h,m,p){const g=this.elements;return g[0]=e,g[1]=l,g[2]=h,g[3]=i,g[4]=c,g[5]=m,g[6]=r,g[7]=d,g[8]=p,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const i=this.elements,r=e.elements;return i[0]=r[0],i[1]=r[1],i[2]=r[2],i[3]=r[3],i[4]=r[4],i[5]=r[5],i[6]=r[6],i[7]=r[7],i[8]=r[8],this}extractBasis(e,i,r){return e.setFromMatrix3Column(this,0),i.setFromMatrix3Column(this,1),r.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const i=e.elements;return this.set(i[0],i[4],i[8],i[1],i[5],i[9],i[2],i[6],i[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,i){const r=e.elements,l=i.elements,c=this.elements,d=r[0],h=r[3],m=r[6],p=r[1],g=r[4],_=r[7],x=r[2],y=r[5],b=r[8],A=l[0],M=l[3],v=l[6],D=l[1],T=l[4],z=l[7],V=l[2],B=l[5],O=l[8];return c[0]=d*A+h*D+m*V,c[3]=d*M+h*T+m*B,c[6]=d*v+h*z+m*O,c[1]=p*A+g*D+_*V,c[4]=p*M+g*T+_*B,c[7]=p*v+g*z+_*O,c[2]=x*A+y*D+b*V,c[5]=x*M+y*T+b*B,c[8]=x*v+y*z+b*O,this}multiplyScalar(e){const i=this.elements;return i[0]*=e,i[3]*=e,i[6]*=e,i[1]*=e,i[4]*=e,i[7]*=e,i[2]*=e,i[5]*=e,i[8]*=e,this}determinant(){const e=this.elements,i=e[0],r=e[1],l=e[2],c=e[3],d=e[4],h=e[5],m=e[6],p=e[7],g=e[8];return i*d*g-i*h*p-r*c*g+r*h*m+l*c*p-l*d*m}invert(){const e=this.elements,i=e[0],r=e[1],l=e[2],c=e[3],d=e[4],h=e[5],m=e[6],p=e[7],g=e[8],_=g*d-h*p,x=h*m-g*c,y=p*c-d*m,b=i*_+r*x+l*y;if(b===0)return this.set(0,0,0,0,0,0,0,0,0);const A=1/b;return e[0]=_*A,e[1]=(l*p-g*r)*A,e[2]=(h*r-l*d)*A,e[3]=x*A,e[4]=(g*i-l*m)*A,e[5]=(l*c-h*i)*A,e[6]=y*A,e[7]=(r*m-p*i)*A,e[8]=(d*i-r*c)*A,this}transpose(){let e;const i=this.elements;return e=i[1],i[1]=i[3],i[3]=e,e=i[2],i[2]=i[6],i[6]=e,e=i[5],i[5]=i[7],i[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const i=this.elements;return e[0]=i[0],e[1]=i[3],e[2]=i[6],e[3]=i[1],e[4]=i[4],e[5]=i[7],e[6]=i[2],e[7]=i[5],e[8]=i[8],this}setUvTransform(e,i,r,l,c,d,h){const m=Math.cos(c),p=Math.sin(c);return this.set(r*m,r*p,-r*(m*d+p*h)+d+e,-l*p,l*m,-l*(-p*d+m*h)+h+i,0,0,1),this}scale(e,i){return this.premultiply(Xf.makeScale(e,i)),this}rotate(e){return this.premultiply(Xf.makeRotation(-e)),this}translate(e,i){return this.premultiply(Xf.makeTranslation(e,i)),this}makeTranslation(e,i){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,i,0,0,1),this}makeRotation(e){const i=Math.cos(e),r=Math.sin(e);return this.set(i,-r,0,r,i,0,0,0,1),this}makeScale(e,i){return this.set(e,0,0,0,i,0,0,0,1),this}equals(e){const i=this.elements,r=e.elements;for(let l=0;l<9;l++)if(i[l]!==r[l])return!1;return!0}fromArray(e,i=0){for(let r=0;r<9;r++)this.elements[r]=e[r+i];return this}toArray(e=[],i=0){const r=this.elements;return e[i]=r[0],e[i+1]=r[1],e[i+2]=r[2],e[i+3]=r[3],e[i+4]=r[4],e[i+5]=r[5],e[i+6]=r[6],e[i+7]=r[7],e[i+8]=r[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const Xf=new ce;function Sv(o){for(let e=o.length-1;e>=0;--e)if(o[e]>=65535)return!0;return!1}function Su(o){return document.createElementNS("http://www.w3.org/1999/xhtml",o)}function cM(){const o=Su("canvas");return o.style.display="block",o}const p_={};function bo(o){o in p_||(p_[o]=!0,console.warn(o))}const m_=new ce().set(.8224621,.177538,0,.0331941,.9668058,0,.0170827,.0723974,.9105199),g_=new ce().set(1.2249401,-.2249404,0,-.0420569,1.0420571,0,-.0196376,-.0786361,1.0982735),Xl={[$i]:{transfer:mu,primaries:gu,toReference:o=>o,fromReference:o=>o},[vn]:{transfer:Fe,primaries:gu,toReference:o=>o.convertSRGBToLinear(),fromReference:o=>o.convertLinearToSRGB()},[Mu]:{transfer:mu,primaries:_u,toReference:o=>o.applyMatrix3(g_),fromReference:o=>o.applyMatrix3(m_)},[Dh]:{transfer:Fe,primaries:_u,toReference:o=>o.convertSRGBToLinear().applyMatrix3(g_),fromReference:o=>o.applyMatrix3(m_).convertLinearToSRGB()}},fM=new Set([$i,Mu]),Ue={enabled:!0,_workingColorSpace:$i,get workingColorSpace(){return this._workingColorSpace},set workingColorSpace(o){if(!fM.has(o))throw new Error(`Unsupported working color space, "${o}".`);this._workingColorSpace=o},convert:function(o,e,i){if(this.enabled===!1||e===i||!e||!i)return o;const r=Xl[e].toReference,l=Xl[i].fromReference;return l(r(o))},fromWorkingColorSpace:function(o,e){return this.convert(o,this._workingColorSpace,e)},toWorkingColorSpace:function(o,e){return this.convert(o,e,this._workingColorSpace)},getPrimaries:function(o){return Xl[o].primaries},getTransfer:function(o){return o===ui?mu:Xl[o].transfer}};function ps(o){return o<.04045?o*.0773993808:Math.pow(o*.9478672986+.0521327014,2.4)}function Wf(o){return o<.0031308?o*12.92:1.055*Math.pow(o,.41666)-.055}let Kr;class xv{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let i;if(e instanceof HTMLCanvasElement)i=e;else{Kr===void 0&&(Kr=Su("canvas")),Kr.width=e.width,Kr.height=e.height;const r=Kr.getContext("2d");e instanceof ImageData?r.putImageData(e,0,0):r.drawImage(e,0,0,e.width,e.height),i=Kr}return i.width>2048||i.height>2048?(console.warn("THREE.ImageUtils.getDataURL: Image converted to jpg for performance reasons",e),i.toDataURL("image/jpeg",.6)):i.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const i=Su("canvas");i.width=e.width,i.height=e.height;const r=i.getContext("2d");r.drawImage(e,0,0,e.width,e.height);const l=r.getImageData(0,0,e.width,e.height),c=l.data;for(let d=0;d<c.length;d++)c[d]=ps(c[d]/255)*255;return r.putImageData(l,0,0),i}else if(e.data){const i=e.data.slice(0);for(let r=0;r<i.length;r++)i instanceof Uint8Array||i instanceof Uint8ClampedArray?i[r]=Math.floor(ps(i[r]/255)*255):i[r]=ps(i[r]);return{data:i,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let hM=0;class Mv{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:hM++}),this.uuid=wo(),this.data=e,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const i=e===void 0||typeof e=="string";if(!i&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const r={uuid:this.uuid,url:""},l=this.data;if(l!==null){let c;if(Array.isArray(l)){c=[];for(let d=0,h=l.length;d<h;d++)l[d].isDataTexture?c.push(kf(l[d].image)):c.push(kf(l[d]))}else c=kf(l);r.url=c}return i||(e.images[this.uuid]=r),r}}function kf(o){return typeof HTMLImageElement<"u"&&o instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&o instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&o instanceof ImageBitmap?xv.getDataURL(o):o.data?{data:Array.from(o.data),width:o.width,height:o.height,type:o.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let dM=0;class Kn extends Ss{constructor(e=Kn.DEFAULT_IMAGE,i=Kn.DEFAULT_MAPPING,r=vi,l=vi,c=oi,d=Ao,h=Si,m=Ia,p=Kn.DEFAULT_ANISOTROPY,g=ui){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:dM++}),this.uuid=wo(),this.name="",this.source=new Mv(e),this.mipmaps=[],this.mapping=i,this.channel=0,this.wrapS=r,this.wrapT=l,this.magFilter=c,this.minFilter=d,this.anisotropy=p,this.format=h,this.internalFormat=null,this.type=m,this.offset=new ge(0,0),this.repeat=new ge(1,1),this.center=new ge(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new ce,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,typeof g=="string"?this.colorSpace=g:(bo("THREE.Texture: Property .encoding has been replaced by .colorSpace."),this.colorSpace=g===dr?vn:ui),this.userData={},this.version=0,this.onUpdate=null,this.isRenderTargetTexture=!1,this.needsPMREMUpdate=!1}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const i=e===void 0||typeof e=="string";if(!i&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const r={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(r.userData=this.userData),i||(e.textures[this.uuid]=r),r}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==lv)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case yh:e.x=e.x-Math.floor(e.x);break;case vi:e.x=e.x<0?0:1;break;case Eh:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case yh:e.y=e.y-Math.floor(e.y);break;case vi:e.y=e.y<0?0:1;break;case Eh:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}get encoding(){return bo("THREE.Texture: Property .encoding has been replaced by .colorSpace."),this.colorSpace===vn?dr:gv}set encoding(e){bo("THREE.Texture: Property .encoding has been replaced by .colorSpace."),this.colorSpace=e===dr?vn:ui}}Kn.DEFAULT_IMAGE=null;Kn.DEFAULT_MAPPING=lv;Kn.DEFAULT_ANISOTROPY=1;class Ve{constructor(e=0,i=0,r=0,l=1){Ve.prototype.isVector4=!0,this.x=e,this.y=i,this.z=r,this.w=l}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,i,r,l){return this.x=e,this.y=i,this.z=r,this.w=l,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;case 2:this.z=i;break;case 3:this.w=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this.z=e.z+i.z,this.w=e.w+i.w,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this.z+=e.z*i,this.w+=e.w*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this.z=e.z-i.z,this.w=e.w-i.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const i=this.x,r=this.y,l=this.z,c=this.w,d=e.elements;return this.x=d[0]*i+d[4]*r+d[8]*l+d[12]*c,this.y=d[1]*i+d[5]*r+d[9]*l+d[13]*c,this.z=d[2]*i+d[6]*r+d[10]*l+d[14]*c,this.w=d[3]*i+d[7]*r+d[11]*l+d[15]*c,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const i=Math.sqrt(1-e.w*e.w);return i<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/i,this.y=e.y/i,this.z=e.z/i),this}setAxisAngleFromRotationMatrix(e){let i,r,l,c;const m=e.elements,p=m[0],g=m[4],_=m[8],x=m[1],y=m[5],b=m[9],A=m[2],M=m[6],v=m[10];if(Math.abs(g-x)<.01&&Math.abs(_-A)<.01&&Math.abs(b-M)<.01){if(Math.abs(g+x)<.1&&Math.abs(_+A)<.1&&Math.abs(b+M)<.1&&Math.abs(p+y+v-3)<.1)return this.set(1,0,0,0),this;i=Math.PI;const T=(p+1)/2,z=(y+1)/2,V=(v+1)/2,B=(g+x)/4,O=(_+A)/4,ut=(b+M)/4;return T>z&&T>V?T<.01?(r=0,l=.707106781,c=.707106781):(r=Math.sqrt(T),l=B/r,c=O/r):z>V?z<.01?(r=.707106781,l=0,c=.707106781):(l=Math.sqrt(z),r=B/l,c=ut/l):V<.01?(r=.707106781,l=.707106781,c=0):(c=Math.sqrt(V),r=O/c,l=ut/c),this.set(r,l,c,i),this}let D=Math.sqrt((M-b)*(M-b)+(_-A)*(_-A)+(x-g)*(x-g));return Math.abs(D)<.001&&(D=1),this.x=(M-b)/D,this.y=(_-A)/D,this.z=(x-g)/D,this.w=Math.acos((p+y+v-1)/2),this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,i){return this.x=Math.max(e.x,Math.min(i.x,this.x)),this.y=Math.max(e.y,Math.min(i.y,this.y)),this.z=Math.max(e.z,Math.min(i.z,this.z)),this.w=Math.max(e.w,Math.min(i.w,this.w)),this}clampScalar(e,i){return this.x=Math.max(e,Math.min(i,this.x)),this.y=Math.max(e,Math.min(i,this.y)),this.z=Math.max(e,Math.min(i,this.z)),this.w=Math.max(e,Math.min(i,this.w)),this}clampLength(e,i){const r=this.length();return this.divideScalar(r||1).multiplyScalar(Math.max(e,Math.min(i,r)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this.z+=(e.z-this.z)*i,this.w+=(e.w-this.w)*i,this}lerpVectors(e,i,r){return this.x=e.x+(i.x-e.x)*r,this.y=e.y+(i.y-e.y)*r,this.z=e.z+(i.z-e.z)*r,this.w=e.w+(i.w-e.w)*r,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this.z=e[i+2],this.w=e[i+3],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e[i+2]=this.z,e[i+3]=this.w,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this.z=e.getZ(i),this.w=e.getW(i),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class pM extends Ss{constructor(e=1,i=1,r={}){super(),this.isRenderTarget=!0,this.width=e,this.height=i,this.depth=1,this.scissor=new Ve(0,0,e,i),this.scissorTest=!1,this.viewport=new Ve(0,0,e,i);const l={width:e,height:i,depth:1};r.encoding!==void 0&&(bo("THREE.WebGLRenderTarget: option.encoding has been replaced by option.colorSpace."),r.colorSpace=r.encoding===dr?vn:ui),r=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:oi,depthBuffer:!0,stencilBuffer:!1,depthTexture:null,samples:0},r),this.texture=new Kn(l,r.mapping,r.wrapS,r.wrapT,r.magFilter,r.minFilter,r.format,r.type,r.anisotropy,r.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.flipY=!1,this.texture.generateMipmaps=r.generateMipmaps,this.texture.internalFormat=r.internalFormat,this.depthBuffer=r.depthBuffer,this.stencilBuffer=r.stencilBuffer,this.depthTexture=r.depthTexture,this.samples=r.samples}setSize(e,i,r=1){(this.width!==e||this.height!==i||this.depth!==r)&&(this.width=e,this.height=i,this.depth=r,this.texture.image.width=e,this.texture.image.height=i,this.texture.image.depth=r,this.dispose()),this.viewport.set(0,0,e,i),this.scissor.set(0,0,e,i)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.texture=e.texture.clone(),this.texture.isRenderTargetTexture=!0;const i=Object.assign({},e.texture.image);return this.texture.source=new Mv(i),this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class pr extends pM{constructor(e=1,i=1,r={}){super(e,i,r),this.isWebGLRenderTarget=!0}}class yv extends Kn{constructor(e=null,i=1,r=1,l=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:i,height:r,depth:l},this.magFilter=wn,this.minFilter=wn,this.wrapR=vi,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class mM extends Kn{constructor(e=null,i=1,r=1,l=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:i,height:r,depth:l},this.magFilter=wn,this.minFilter=wn,this.wrapR=vi,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class Do{constructor(e=0,i=0,r=0,l=1){this.isQuaternion=!0,this._x=e,this._y=i,this._z=r,this._w=l}static slerpFlat(e,i,r,l,c,d,h){let m=r[l+0],p=r[l+1],g=r[l+2],_=r[l+3];const x=c[d+0],y=c[d+1],b=c[d+2],A=c[d+3];if(h===0){e[i+0]=m,e[i+1]=p,e[i+2]=g,e[i+3]=_;return}if(h===1){e[i+0]=x,e[i+1]=y,e[i+2]=b,e[i+3]=A;return}if(_!==A||m!==x||p!==y||g!==b){let M=1-h;const v=m*x+p*y+g*b+_*A,D=v>=0?1:-1,T=1-v*v;if(T>Number.EPSILON){const V=Math.sqrt(T),B=Math.atan2(V,v*D);M=Math.sin(M*B)/V,h=Math.sin(h*B)/V}const z=h*D;if(m=m*M+x*z,p=p*M+y*z,g=g*M+b*z,_=_*M+A*z,M===1-h){const V=1/Math.sqrt(m*m+p*p+g*g+_*_);m*=V,p*=V,g*=V,_*=V}}e[i]=m,e[i+1]=p,e[i+2]=g,e[i+3]=_}static multiplyQuaternionsFlat(e,i,r,l,c,d){const h=r[l],m=r[l+1],p=r[l+2],g=r[l+3],_=c[d],x=c[d+1],y=c[d+2],b=c[d+3];return e[i]=h*b+g*_+m*y-p*x,e[i+1]=m*b+g*x+p*_-h*y,e[i+2]=p*b+g*y+h*x-m*_,e[i+3]=g*b-h*_-m*x-p*y,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,i,r,l){return this._x=e,this._y=i,this._z=r,this._w=l,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,i=!0){const r=e._x,l=e._y,c=e._z,d=e._order,h=Math.cos,m=Math.sin,p=h(r/2),g=h(l/2),_=h(c/2),x=m(r/2),y=m(l/2),b=m(c/2);switch(d){case"XYZ":this._x=x*g*_+p*y*b,this._y=p*y*_-x*g*b,this._z=p*g*b+x*y*_,this._w=p*g*_-x*y*b;break;case"YXZ":this._x=x*g*_+p*y*b,this._y=p*y*_-x*g*b,this._z=p*g*b-x*y*_,this._w=p*g*_+x*y*b;break;case"ZXY":this._x=x*g*_-p*y*b,this._y=p*y*_+x*g*b,this._z=p*g*b+x*y*_,this._w=p*g*_-x*y*b;break;case"ZYX":this._x=x*g*_-p*y*b,this._y=p*y*_+x*g*b,this._z=p*g*b-x*y*_,this._w=p*g*_+x*y*b;break;case"YZX":this._x=x*g*_+p*y*b,this._y=p*y*_+x*g*b,this._z=p*g*b-x*y*_,this._w=p*g*_-x*y*b;break;case"XZY":this._x=x*g*_-p*y*b,this._y=p*y*_-x*g*b,this._z=p*g*b+x*y*_,this._w=p*g*_+x*y*b;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+d)}return i===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,i){const r=i/2,l=Math.sin(r);return this._x=e.x*l,this._y=e.y*l,this._z=e.z*l,this._w=Math.cos(r),this._onChangeCallback(),this}setFromRotationMatrix(e){const i=e.elements,r=i[0],l=i[4],c=i[8],d=i[1],h=i[5],m=i[9],p=i[2],g=i[6],_=i[10],x=r+h+_;if(x>0){const y=.5/Math.sqrt(x+1);this._w=.25/y,this._x=(g-m)*y,this._y=(c-p)*y,this._z=(d-l)*y}else if(r>h&&r>_){const y=2*Math.sqrt(1+r-h-_);this._w=(g-m)/y,this._x=.25*y,this._y=(l+d)/y,this._z=(c+p)/y}else if(h>_){const y=2*Math.sqrt(1+h-r-_);this._w=(c-p)/y,this._x=(l+d)/y,this._y=.25*y,this._z=(m+g)/y}else{const y=2*Math.sqrt(1+_-r-h);this._w=(d-l)/y,this._x=(c+p)/y,this._y=(m+g)/y,this._z=.25*y}return this._onChangeCallback(),this}setFromUnitVectors(e,i){let r=e.dot(i)+1;return r<Number.EPSILON?(r=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=r):(this._x=0,this._y=-e.z,this._z=e.y,this._w=r)):(this._x=e.y*i.z-e.z*i.y,this._y=e.z*i.x-e.x*i.z,this._z=e.x*i.y-e.y*i.x,this._w=r),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(Dn(this.dot(e),-1,1)))}rotateTowards(e,i){const r=this.angleTo(e);if(r===0)return this;const l=Math.min(1,i/r);return this.slerp(e,l),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,i){const r=e._x,l=e._y,c=e._z,d=e._w,h=i._x,m=i._y,p=i._z,g=i._w;return this._x=r*g+d*h+l*p-c*m,this._y=l*g+d*m+c*h-r*p,this._z=c*g+d*p+r*m-l*h,this._w=d*g-r*h-l*m-c*p,this._onChangeCallback(),this}slerp(e,i){if(i===0)return this;if(i===1)return this.copy(e);const r=this._x,l=this._y,c=this._z,d=this._w;let h=d*e._w+r*e._x+l*e._y+c*e._z;if(h<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,h=-h):this.copy(e),h>=1)return this._w=d,this._x=r,this._y=l,this._z=c,this;const m=1-h*h;if(m<=Number.EPSILON){const y=1-i;return this._w=y*d+i*this._w,this._x=y*r+i*this._x,this._y=y*l+i*this._y,this._z=y*c+i*this._z,this.normalize(),this}const p=Math.sqrt(m),g=Math.atan2(p,h),_=Math.sin((1-i)*g)/p,x=Math.sin(i*g)/p;return this._w=d*_+this._w*x,this._x=r*_+this._x*x,this._y=l*_+this._y*x,this._z=c*_+this._z*x,this._onChangeCallback(),this}slerpQuaternions(e,i,r){return this.copy(e).slerp(i,r)}random(){const e=Math.random(),i=Math.sqrt(1-e),r=Math.sqrt(e),l=2*Math.PI*Math.random(),c=2*Math.PI*Math.random();return this.set(i*Math.cos(l),r*Math.sin(c),r*Math.cos(c),i*Math.sin(l))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,i=0){return this._x=e[i],this._y=e[i+1],this._z=e[i+2],this._w=e[i+3],this._onChangeCallback(),this}toArray(e=[],i=0){return e[i]=this._x,e[i+1]=this._y,e[i+2]=this._z,e[i+3]=this._w,e}fromBufferAttribute(e,i){return this._x=e.getX(i),this._y=e.getY(i),this._z=e.getZ(i),this._w=e.getW(i),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class Y{constructor(e=0,i=0,r=0){Y.prototype.isVector3=!0,this.x=e,this.y=i,this.z=r}set(e,i,r){return r===void 0&&(r=this.z),this.x=e,this.y=i,this.z=r,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;case 2:this.z=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this.z=e.z+i.z,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this.z+=e.z*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this.z=e.z-i.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,i){return this.x=e.x*i.x,this.y=e.y*i.y,this.z=e.z*i.z,this}applyEuler(e){return this.applyQuaternion(__.setFromEuler(e))}applyAxisAngle(e,i){return this.applyQuaternion(__.setFromAxisAngle(e,i))}applyMatrix3(e){const i=this.x,r=this.y,l=this.z,c=e.elements;return this.x=c[0]*i+c[3]*r+c[6]*l,this.y=c[1]*i+c[4]*r+c[7]*l,this.z=c[2]*i+c[5]*r+c[8]*l,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const i=this.x,r=this.y,l=this.z,c=e.elements,d=1/(c[3]*i+c[7]*r+c[11]*l+c[15]);return this.x=(c[0]*i+c[4]*r+c[8]*l+c[12])*d,this.y=(c[1]*i+c[5]*r+c[9]*l+c[13])*d,this.z=(c[2]*i+c[6]*r+c[10]*l+c[14])*d,this}applyQuaternion(e){const i=this.x,r=this.y,l=this.z,c=e.x,d=e.y,h=e.z,m=e.w,p=2*(d*l-h*r),g=2*(h*i-c*l),_=2*(c*r-d*i);return this.x=i+m*p+d*_-h*g,this.y=r+m*g+h*p-c*_,this.z=l+m*_+c*g-d*p,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const i=this.x,r=this.y,l=this.z,c=e.elements;return this.x=c[0]*i+c[4]*r+c[8]*l,this.y=c[1]*i+c[5]*r+c[9]*l,this.z=c[2]*i+c[6]*r+c[10]*l,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,i){return this.x=Math.max(e.x,Math.min(i.x,this.x)),this.y=Math.max(e.y,Math.min(i.y,this.y)),this.z=Math.max(e.z,Math.min(i.z,this.z)),this}clampScalar(e,i){return this.x=Math.max(e,Math.min(i,this.x)),this.y=Math.max(e,Math.min(i,this.y)),this.z=Math.max(e,Math.min(i,this.z)),this}clampLength(e,i){const r=this.length();return this.divideScalar(r||1).multiplyScalar(Math.max(e,Math.min(i,r)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this.z+=(e.z-this.z)*i,this}lerpVectors(e,i,r){return this.x=e.x+(i.x-e.x)*r,this.y=e.y+(i.y-e.y)*r,this.z=e.z+(i.z-e.z)*r,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,i){const r=e.x,l=e.y,c=e.z,d=i.x,h=i.y,m=i.z;return this.x=l*m-c*h,this.y=c*d-r*m,this.z=r*h-l*d,this}projectOnVector(e){const i=e.lengthSq();if(i===0)return this.set(0,0,0);const r=e.dot(this)/i;return this.copy(e).multiplyScalar(r)}projectOnPlane(e){return qf.copy(this).projectOnVector(e),this.sub(qf)}reflect(e){return this.sub(qf.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const i=Math.sqrt(this.lengthSq()*e.lengthSq());if(i===0)return Math.PI/2;const r=this.dot(e)/i;return Math.acos(Dn(r,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const i=this.x-e.x,r=this.y-e.y,l=this.z-e.z;return i*i+r*r+l*l}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,i,r){const l=Math.sin(i)*e;return this.x=l*Math.sin(r),this.y=Math.cos(i)*e,this.z=l*Math.cos(r),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,i,r){return this.x=e*Math.sin(i),this.y=r,this.z=e*Math.cos(i),this}setFromMatrixPosition(e){const i=e.elements;return this.x=i[12],this.y=i[13],this.z=i[14],this}setFromMatrixScale(e){const i=this.setFromMatrixColumn(e,0).length(),r=this.setFromMatrixColumn(e,1).length(),l=this.setFromMatrixColumn(e,2).length();return this.x=i,this.y=r,this.z=l,this}setFromMatrixColumn(e,i){return this.fromArray(e.elements,i*4)}setFromMatrix3Column(e,i){return this.fromArray(e.elements,i*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this.z=e[i+2],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e[i+2]=this.z,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this.z=e.getZ(i),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=(Math.random()-.5)*2,i=Math.random()*Math.PI*2,r=Math.sqrt(1-e**2);return this.x=r*Math.cos(i),this.y=r*Math.sin(i),this.z=e,this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const qf=new Y,__=new Do;class Lo{constructor(e=new Y(1/0,1/0,1/0),i=new Y(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=i}set(e,i){return this.min.copy(e),this.max.copy(i),this}setFromArray(e){this.makeEmpty();for(let i=0,r=e.length;i<r;i+=3)this.expandByPoint(pi.fromArray(e,i));return this}setFromBufferAttribute(e){this.makeEmpty();for(let i=0,r=e.count;i<r;i++)this.expandByPoint(pi.fromBufferAttribute(e,i));return this}setFromPoints(e){this.makeEmpty();for(let i=0,r=e.length;i<r;i++)this.expandByPoint(e[i]);return this}setFromCenterAndSize(e,i){const r=pi.copy(i).multiplyScalar(.5);return this.min.copy(e).sub(r),this.max.copy(e).add(r),this}setFromObject(e,i=!1){return this.makeEmpty(),this.expandByObject(e,i)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,i=!1){e.updateWorldMatrix(!1,!1);const r=e.geometry;if(r!==void 0){const c=r.getAttribute("position");if(i===!0&&c!==void 0&&e.isInstancedMesh!==!0)for(let d=0,h=c.count;d<h;d++)e.isMesh===!0?e.getVertexPosition(d,pi):pi.fromBufferAttribute(c,d),pi.applyMatrix4(e.matrixWorld),this.expandByPoint(pi);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),Wl.copy(e.boundingBox)):(r.boundingBox===null&&r.computeBoundingBox(),Wl.copy(r.boundingBox)),Wl.applyMatrix4(e.matrixWorld),this.union(Wl)}const l=e.children;for(let c=0,d=l.length;c<d;c++)this.expandByObject(l[c],i);return this}containsPoint(e){return!(e.x<this.min.x||e.x>this.max.x||e.y<this.min.y||e.y>this.max.y||e.z<this.min.z||e.z>this.max.z)}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,i){return i.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return!(e.max.x<this.min.x||e.min.x>this.max.x||e.max.y<this.min.y||e.min.y>this.max.y||e.max.z<this.min.z||e.min.z>this.max.z)}intersectsSphere(e){return this.clampPoint(e.center,pi),pi.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let i,r;return e.normal.x>0?(i=e.normal.x*this.min.x,r=e.normal.x*this.max.x):(i=e.normal.x*this.max.x,r=e.normal.x*this.min.x),e.normal.y>0?(i+=e.normal.y*this.min.y,r+=e.normal.y*this.max.y):(i+=e.normal.y*this.max.y,r+=e.normal.y*this.min.y),e.normal.z>0?(i+=e.normal.z*this.min.z,r+=e.normal.z*this.max.z):(i+=e.normal.z*this.max.z,r+=e.normal.z*this.min.z),i<=-e.constant&&r>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(So),kl.subVectors(this.max,So),Qr.subVectors(e.a,So),Jr.subVectors(e.b,So),$r.subVectors(e.c,So),Ca.subVectors(Jr,Qr),wa.subVectors($r,Jr),ir.subVectors(Qr,$r);let i=[0,-Ca.z,Ca.y,0,-wa.z,wa.y,0,-ir.z,ir.y,Ca.z,0,-Ca.x,wa.z,0,-wa.x,ir.z,0,-ir.x,-Ca.y,Ca.x,0,-wa.y,wa.x,0,-ir.y,ir.x,0];return!Yf(i,Qr,Jr,$r,kl)||(i=[1,0,0,0,1,0,0,0,1],!Yf(i,Qr,Jr,$r,kl))?!1:(ql.crossVectors(Ca,wa),i=[ql.x,ql.y,ql.z],Yf(i,Qr,Jr,$r,kl))}clampPoint(e,i){return i.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,pi).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(pi).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(ki[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),ki[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),ki[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),ki[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),ki[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),ki[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),ki[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),ki[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(ki),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const ki=[new Y,new Y,new Y,new Y,new Y,new Y,new Y,new Y],pi=new Y,Wl=new Lo,Qr=new Y,Jr=new Y,$r=new Y,Ca=new Y,wa=new Y,ir=new Y,So=new Y,kl=new Y,ql=new Y,ar=new Y;function Yf(o,e,i,r,l){for(let c=0,d=o.length-3;c<=d;c+=3){ar.fromArray(o,c);const h=l.x*Math.abs(ar.x)+l.y*Math.abs(ar.y)+l.z*Math.abs(ar.z),m=e.dot(ar),p=i.dot(ar),g=r.dot(ar);if(Math.max(-Math.max(m,p,g),Math.min(m,p,g))>h)return!1}return!0}const gM=new Lo,xo=new Y,jf=new Y;class Lh{constructor(e=new Y,i=-1){this.isSphere=!0,this.center=e,this.radius=i}set(e,i){return this.center.copy(e),this.radius=i,this}setFromPoints(e,i){const r=this.center;i!==void 0?r.copy(i):gM.setFromPoints(e).getCenter(r);let l=0;for(let c=0,d=e.length;c<d;c++)l=Math.max(l,r.distanceToSquared(e[c]));return this.radius=Math.sqrt(l),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const i=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=i*i}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,i){const r=this.center.distanceToSquared(e);return i.copy(e),r>this.radius*this.radius&&(i.sub(this.center).normalize(),i.multiplyScalar(this.radius).add(this.center)),i}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;xo.subVectors(e,this.center);const i=xo.lengthSq();if(i>this.radius*this.radius){const r=Math.sqrt(i),l=(r-this.radius)*.5;this.center.addScaledVector(xo,l/r),this.radius+=l}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(jf.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(xo.copy(e.center).add(jf)),this.expandByPoint(xo.copy(e.center).sub(jf))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const qi=new Y,Zf=new Y,Yl=new Y,Da=new Y,Kf=new Y,jl=new Y,Qf=new Y;class _M{constructor(e=new Y,i=new Y(0,0,-1)){this.origin=e,this.direction=i}set(e,i){return this.origin.copy(e),this.direction.copy(i),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,i){return i.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,qi)),this}closestPointToPoint(e,i){i.subVectors(e,this.origin);const r=i.dot(this.direction);return r<0?i.copy(this.origin):i.copy(this.origin).addScaledVector(this.direction,r)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const i=qi.subVectors(e,this.origin).dot(this.direction);return i<0?this.origin.distanceToSquared(e):(qi.copy(this.origin).addScaledVector(this.direction,i),qi.distanceToSquared(e))}distanceSqToSegment(e,i,r,l){Zf.copy(e).add(i).multiplyScalar(.5),Yl.copy(i).sub(e).normalize(),Da.copy(this.origin).sub(Zf);const c=e.distanceTo(i)*.5,d=-this.direction.dot(Yl),h=Da.dot(this.direction),m=-Da.dot(Yl),p=Da.lengthSq(),g=Math.abs(1-d*d);let _,x,y,b;if(g>0)if(_=d*m-h,x=d*h-m,b=c*g,_>=0)if(x>=-b)if(x<=b){const A=1/g;_*=A,x*=A,y=_*(_+d*x+2*h)+x*(d*_+x+2*m)+p}else x=c,_=Math.max(0,-(d*x+h)),y=-_*_+x*(x+2*m)+p;else x=-c,_=Math.max(0,-(d*x+h)),y=-_*_+x*(x+2*m)+p;else x<=-b?(_=Math.max(0,-(-d*c+h)),x=_>0?-c:Math.min(Math.max(-c,-m),c),y=-_*_+x*(x+2*m)+p):x<=b?(_=0,x=Math.min(Math.max(-c,-m),c),y=x*(x+2*m)+p):(_=Math.max(0,-(d*c+h)),x=_>0?c:Math.min(Math.max(-c,-m),c),y=-_*_+x*(x+2*m)+p);else x=d>0?-c:c,_=Math.max(0,-(d*x+h)),y=-_*_+x*(x+2*m)+p;return r&&r.copy(this.origin).addScaledVector(this.direction,_),l&&l.copy(Zf).addScaledVector(Yl,x),y}intersectSphere(e,i){qi.subVectors(e.center,this.origin);const r=qi.dot(this.direction),l=qi.dot(qi)-r*r,c=e.radius*e.radius;if(l>c)return null;const d=Math.sqrt(c-l),h=r-d,m=r+d;return m<0?null:h<0?this.at(m,i):this.at(h,i)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const i=e.normal.dot(this.direction);if(i===0)return e.distanceToPoint(this.origin)===0?0:null;const r=-(this.origin.dot(e.normal)+e.constant)/i;return r>=0?r:null}intersectPlane(e,i){const r=this.distanceToPlane(e);return r===null?null:this.at(r,i)}intersectsPlane(e){const i=e.distanceToPoint(this.origin);return i===0||e.normal.dot(this.direction)*i<0}intersectBox(e,i){let r,l,c,d,h,m;const p=1/this.direction.x,g=1/this.direction.y,_=1/this.direction.z,x=this.origin;return p>=0?(r=(e.min.x-x.x)*p,l=(e.max.x-x.x)*p):(r=(e.max.x-x.x)*p,l=(e.min.x-x.x)*p),g>=0?(c=(e.min.y-x.y)*g,d=(e.max.y-x.y)*g):(c=(e.max.y-x.y)*g,d=(e.min.y-x.y)*g),r>d||c>l||((c>r||isNaN(r))&&(r=c),(d<l||isNaN(l))&&(l=d),_>=0?(h=(e.min.z-x.z)*_,m=(e.max.z-x.z)*_):(h=(e.max.z-x.z)*_,m=(e.min.z-x.z)*_),r>m||h>l)||((h>r||r!==r)&&(r=h),(m<l||l!==l)&&(l=m),l<0)?null:this.at(r>=0?r:l,i)}intersectsBox(e){return this.intersectBox(e,qi)!==null}intersectTriangle(e,i,r,l,c){Kf.subVectors(i,e),jl.subVectors(r,e),Qf.crossVectors(Kf,jl);let d=this.direction.dot(Qf),h;if(d>0){if(l)return null;h=1}else if(d<0)h=-1,d=-d;else return null;Da.subVectors(this.origin,e);const m=h*this.direction.dot(jl.crossVectors(Da,jl));if(m<0)return null;const p=h*this.direction.dot(Kf.cross(Da));if(p<0||m+p>d)return null;const g=-h*Da.dot(Qf);return g<0?null:this.at(g/d,c)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class rn{constructor(e,i,r,l,c,d,h,m,p,g,_,x,y,b,A,M){rn.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,i,r,l,c,d,h,m,p,g,_,x,y,b,A,M)}set(e,i,r,l,c,d,h,m,p,g,_,x,y,b,A,M){const v=this.elements;return v[0]=e,v[4]=i,v[8]=r,v[12]=l,v[1]=c,v[5]=d,v[9]=h,v[13]=m,v[2]=p,v[6]=g,v[10]=_,v[14]=x,v[3]=y,v[7]=b,v[11]=A,v[15]=M,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new rn().fromArray(this.elements)}copy(e){const i=this.elements,r=e.elements;return i[0]=r[0],i[1]=r[1],i[2]=r[2],i[3]=r[3],i[4]=r[4],i[5]=r[5],i[6]=r[6],i[7]=r[7],i[8]=r[8],i[9]=r[9],i[10]=r[10],i[11]=r[11],i[12]=r[12],i[13]=r[13],i[14]=r[14],i[15]=r[15],this}copyPosition(e){const i=this.elements,r=e.elements;return i[12]=r[12],i[13]=r[13],i[14]=r[14],this}setFromMatrix3(e){const i=e.elements;return this.set(i[0],i[3],i[6],0,i[1],i[4],i[7],0,i[2],i[5],i[8],0,0,0,0,1),this}extractBasis(e,i,r){return e.setFromMatrixColumn(this,0),i.setFromMatrixColumn(this,1),r.setFromMatrixColumn(this,2),this}makeBasis(e,i,r){return this.set(e.x,i.x,r.x,0,e.y,i.y,r.y,0,e.z,i.z,r.z,0,0,0,0,1),this}extractRotation(e){const i=this.elements,r=e.elements,l=1/ts.setFromMatrixColumn(e,0).length(),c=1/ts.setFromMatrixColumn(e,1).length(),d=1/ts.setFromMatrixColumn(e,2).length();return i[0]=r[0]*l,i[1]=r[1]*l,i[2]=r[2]*l,i[3]=0,i[4]=r[4]*c,i[5]=r[5]*c,i[6]=r[6]*c,i[7]=0,i[8]=r[8]*d,i[9]=r[9]*d,i[10]=r[10]*d,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,this}makeRotationFromEuler(e){const i=this.elements,r=e.x,l=e.y,c=e.z,d=Math.cos(r),h=Math.sin(r),m=Math.cos(l),p=Math.sin(l),g=Math.cos(c),_=Math.sin(c);if(e.order==="XYZ"){const x=d*g,y=d*_,b=h*g,A=h*_;i[0]=m*g,i[4]=-m*_,i[8]=p,i[1]=y+b*p,i[5]=x-A*p,i[9]=-h*m,i[2]=A-x*p,i[6]=b+y*p,i[10]=d*m}else if(e.order==="YXZ"){const x=m*g,y=m*_,b=p*g,A=p*_;i[0]=x+A*h,i[4]=b*h-y,i[8]=d*p,i[1]=d*_,i[5]=d*g,i[9]=-h,i[2]=y*h-b,i[6]=A+x*h,i[10]=d*m}else if(e.order==="ZXY"){const x=m*g,y=m*_,b=p*g,A=p*_;i[0]=x-A*h,i[4]=-d*_,i[8]=b+y*h,i[1]=y+b*h,i[5]=d*g,i[9]=A-x*h,i[2]=-d*p,i[6]=h,i[10]=d*m}else if(e.order==="ZYX"){const x=d*g,y=d*_,b=h*g,A=h*_;i[0]=m*g,i[4]=b*p-y,i[8]=x*p+A,i[1]=m*_,i[5]=A*p+x,i[9]=y*p-b,i[2]=-p,i[6]=h*m,i[10]=d*m}else if(e.order==="YZX"){const x=d*m,y=d*p,b=h*m,A=h*p;i[0]=m*g,i[4]=A-x*_,i[8]=b*_+y,i[1]=_,i[5]=d*g,i[9]=-h*g,i[2]=-p*g,i[6]=y*_+b,i[10]=x-A*_}else if(e.order==="XZY"){const x=d*m,y=d*p,b=h*m,A=h*p;i[0]=m*g,i[4]=-_,i[8]=p*g,i[1]=x*_+A,i[5]=d*g,i[9]=y*_-b,i[2]=b*_-y,i[6]=h*g,i[10]=A*_+x}return i[3]=0,i[7]=0,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,this}makeRotationFromQuaternion(e){return this.compose(vM,e,SM)}lookAt(e,i,r){const l=this.elements;return jn.subVectors(e,i),jn.lengthSq()===0&&(jn.z=1),jn.normalize(),La.crossVectors(r,jn),La.lengthSq()===0&&(Math.abs(r.z)===1?jn.x+=1e-4:jn.z+=1e-4,jn.normalize(),La.crossVectors(r,jn)),La.normalize(),Zl.crossVectors(jn,La),l[0]=La.x,l[4]=Zl.x,l[8]=jn.x,l[1]=La.y,l[5]=Zl.y,l[9]=jn.y,l[2]=La.z,l[6]=Zl.z,l[10]=jn.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,i){const r=e.elements,l=i.elements,c=this.elements,d=r[0],h=r[4],m=r[8],p=r[12],g=r[1],_=r[5],x=r[9],y=r[13],b=r[2],A=r[6],M=r[10],v=r[14],D=r[3],T=r[7],z=r[11],V=r[15],B=l[0],O=l[4],ut=l[8],C=l[12],N=l[1],rt=l[5],dt=l[9],Et=l[13],X=l[2],tt=l[6],P=l[10],q=l[14],J=l[3],lt=l[7],ft=l[11],L=l[15];return c[0]=d*B+h*N+m*X+p*J,c[4]=d*O+h*rt+m*tt+p*lt,c[8]=d*ut+h*dt+m*P+p*ft,c[12]=d*C+h*Et+m*q+p*L,c[1]=g*B+_*N+x*X+y*J,c[5]=g*O+_*rt+x*tt+y*lt,c[9]=g*ut+_*dt+x*P+y*ft,c[13]=g*C+_*Et+x*q+y*L,c[2]=b*B+A*N+M*X+v*J,c[6]=b*O+A*rt+M*tt+v*lt,c[10]=b*ut+A*dt+M*P+v*ft,c[14]=b*C+A*Et+M*q+v*L,c[3]=D*B+T*N+z*X+V*J,c[7]=D*O+T*rt+z*tt+V*lt,c[11]=D*ut+T*dt+z*P+V*ft,c[15]=D*C+T*Et+z*q+V*L,this}multiplyScalar(e){const i=this.elements;return i[0]*=e,i[4]*=e,i[8]*=e,i[12]*=e,i[1]*=e,i[5]*=e,i[9]*=e,i[13]*=e,i[2]*=e,i[6]*=e,i[10]*=e,i[14]*=e,i[3]*=e,i[7]*=e,i[11]*=e,i[15]*=e,this}determinant(){const e=this.elements,i=e[0],r=e[4],l=e[8],c=e[12],d=e[1],h=e[5],m=e[9],p=e[13],g=e[2],_=e[6],x=e[10],y=e[14],b=e[3],A=e[7],M=e[11],v=e[15];return b*(+c*m*_-l*p*_-c*h*x+r*p*x+l*h*y-r*m*y)+A*(+i*m*y-i*p*x+c*d*x-l*d*y+l*p*g-c*m*g)+M*(+i*p*_-i*h*y-c*d*_+r*d*y+c*h*g-r*p*g)+v*(-l*h*g-i*m*_+i*h*x+l*d*_-r*d*x+r*m*g)}transpose(){const e=this.elements;let i;return i=e[1],e[1]=e[4],e[4]=i,i=e[2],e[2]=e[8],e[8]=i,i=e[6],e[6]=e[9],e[9]=i,i=e[3],e[3]=e[12],e[12]=i,i=e[7],e[7]=e[13],e[13]=i,i=e[11],e[11]=e[14],e[14]=i,this}setPosition(e,i,r){const l=this.elements;return e.isVector3?(l[12]=e.x,l[13]=e.y,l[14]=e.z):(l[12]=e,l[13]=i,l[14]=r),this}invert(){const e=this.elements,i=e[0],r=e[1],l=e[2],c=e[3],d=e[4],h=e[5],m=e[6],p=e[7],g=e[8],_=e[9],x=e[10],y=e[11],b=e[12],A=e[13],M=e[14],v=e[15],D=_*M*p-A*x*p+A*m*y-h*M*y-_*m*v+h*x*v,T=b*x*p-g*M*p-b*m*y+d*M*y+g*m*v-d*x*v,z=g*A*p-b*_*p+b*h*y-d*A*y-g*h*v+d*_*v,V=b*_*m-g*A*m-b*h*x+d*A*x+g*h*M-d*_*M,B=i*D+r*T+l*z+c*V;if(B===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const O=1/B;return e[0]=D*O,e[1]=(A*x*c-_*M*c-A*l*y+r*M*y+_*l*v-r*x*v)*O,e[2]=(h*M*c-A*m*c+A*l*p-r*M*p-h*l*v+r*m*v)*O,e[3]=(_*m*c-h*x*c-_*l*p+r*x*p+h*l*y-r*m*y)*O,e[4]=T*O,e[5]=(g*M*c-b*x*c+b*l*y-i*M*y-g*l*v+i*x*v)*O,e[6]=(b*m*c-d*M*c-b*l*p+i*M*p+d*l*v-i*m*v)*O,e[7]=(d*x*c-g*m*c+g*l*p-i*x*p-d*l*y+i*m*y)*O,e[8]=z*O,e[9]=(b*_*c-g*A*c-b*r*y+i*A*y+g*r*v-i*_*v)*O,e[10]=(d*A*c-b*h*c+b*r*p-i*A*p-d*r*v+i*h*v)*O,e[11]=(g*h*c-d*_*c-g*r*p+i*_*p+d*r*y-i*h*y)*O,e[12]=V*O,e[13]=(g*A*l-b*_*l+b*r*x-i*A*x-g*r*M+i*_*M)*O,e[14]=(b*h*l-d*A*l-b*r*m+i*A*m+d*r*M-i*h*M)*O,e[15]=(d*_*l-g*h*l+g*r*m-i*_*m-d*r*x+i*h*x)*O,this}scale(e){const i=this.elements,r=e.x,l=e.y,c=e.z;return i[0]*=r,i[4]*=l,i[8]*=c,i[1]*=r,i[5]*=l,i[9]*=c,i[2]*=r,i[6]*=l,i[10]*=c,i[3]*=r,i[7]*=l,i[11]*=c,this}getMaxScaleOnAxis(){const e=this.elements,i=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],r=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],l=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(i,r,l))}makeTranslation(e,i,r){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,i,0,0,1,r,0,0,0,1),this}makeRotationX(e){const i=Math.cos(e),r=Math.sin(e);return this.set(1,0,0,0,0,i,-r,0,0,r,i,0,0,0,0,1),this}makeRotationY(e){const i=Math.cos(e),r=Math.sin(e);return this.set(i,0,r,0,0,1,0,0,-r,0,i,0,0,0,0,1),this}makeRotationZ(e){const i=Math.cos(e),r=Math.sin(e);return this.set(i,-r,0,0,r,i,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,i){const r=Math.cos(i),l=Math.sin(i),c=1-r,d=e.x,h=e.y,m=e.z,p=c*d,g=c*h;return this.set(p*d+r,p*h-l*m,p*m+l*h,0,p*h+l*m,g*h+r,g*m-l*d,0,p*m-l*h,g*m+l*d,c*m*m+r,0,0,0,0,1),this}makeScale(e,i,r){return this.set(e,0,0,0,0,i,0,0,0,0,r,0,0,0,0,1),this}makeShear(e,i,r,l,c,d){return this.set(1,r,c,0,e,1,d,0,i,l,1,0,0,0,0,1),this}compose(e,i,r){const l=this.elements,c=i._x,d=i._y,h=i._z,m=i._w,p=c+c,g=d+d,_=h+h,x=c*p,y=c*g,b=c*_,A=d*g,M=d*_,v=h*_,D=m*p,T=m*g,z=m*_,V=r.x,B=r.y,O=r.z;return l[0]=(1-(A+v))*V,l[1]=(y+z)*V,l[2]=(b-T)*V,l[3]=0,l[4]=(y-z)*B,l[5]=(1-(x+v))*B,l[6]=(M+D)*B,l[7]=0,l[8]=(b+T)*O,l[9]=(M-D)*O,l[10]=(1-(x+A))*O,l[11]=0,l[12]=e.x,l[13]=e.y,l[14]=e.z,l[15]=1,this}decompose(e,i,r){const l=this.elements;let c=ts.set(l[0],l[1],l[2]).length();const d=ts.set(l[4],l[5],l[6]).length(),h=ts.set(l[8],l[9],l[10]).length();this.determinant()<0&&(c=-c),e.x=l[12],e.y=l[13],e.z=l[14],mi.copy(this);const p=1/c,g=1/d,_=1/h;return mi.elements[0]*=p,mi.elements[1]*=p,mi.elements[2]*=p,mi.elements[4]*=g,mi.elements[5]*=g,mi.elements[6]*=g,mi.elements[8]*=_,mi.elements[9]*=_,mi.elements[10]*=_,i.setFromRotationMatrix(mi),r.x=c,r.y=d,r.z=h,this}makePerspective(e,i,r,l,c,d,h=Ji){const m=this.elements,p=2*c/(i-e),g=2*c/(r-l),_=(i+e)/(i-e),x=(r+l)/(r-l);let y,b;if(h===Ji)y=-(d+c)/(d-c),b=-2*d*c/(d-c);else if(h===vu)y=-d/(d-c),b=-d*c/(d-c);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+h);return m[0]=p,m[4]=0,m[8]=_,m[12]=0,m[1]=0,m[5]=g,m[9]=x,m[13]=0,m[2]=0,m[6]=0,m[10]=y,m[14]=b,m[3]=0,m[7]=0,m[11]=-1,m[15]=0,this}makeOrthographic(e,i,r,l,c,d,h=Ji){const m=this.elements,p=1/(i-e),g=1/(r-l),_=1/(d-c),x=(i+e)*p,y=(r+l)*g;let b,A;if(h===Ji)b=(d+c)*_,A=-2*_;else if(h===vu)b=c*_,A=-1*_;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+h);return m[0]=2*p,m[4]=0,m[8]=0,m[12]=-x,m[1]=0,m[5]=2*g,m[9]=0,m[13]=-y,m[2]=0,m[6]=0,m[10]=A,m[14]=-b,m[3]=0,m[7]=0,m[11]=0,m[15]=1,this}equals(e){const i=this.elements,r=e.elements;for(let l=0;l<16;l++)if(i[l]!==r[l])return!1;return!0}fromArray(e,i=0){for(let r=0;r<16;r++)this.elements[r]=e[r+i];return this}toArray(e=[],i=0){const r=this.elements;return e[i]=r[0],e[i+1]=r[1],e[i+2]=r[2],e[i+3]=r[3],e[i+4]=r[4],e[i+5]=r[5],e[i+6]=r[6],e[i+7]=r[7],e[i+8]=r[8],e[i+9]=r[9],e[i+10]=r[10],e[i+11]=r[11],e[i+12]=r[12],e[i+13]=r[13],e[i+14]=r[14],e[i+15]=r[15],e}}const ts=new Y,mi=new rn,vM=new Y(0,0,0),SM=new Y(1,1,1),La=new Y,Zl=new Y,jn=new Y,v_=new rn,S_=new Do;class yu{constructor(e=0,i=0,r=0,l=yu.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=i,this._z=r,this._order=l}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,i,r,l=this._order){return this._x=e,this._y=i,this._z=r,this._order=l,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,i=this._order,r=!0){const l=e.elements,c=l[0],d=l[4],h=l[8],m=l[1],p=l[5],g=l[9],_=l[2],x=l[6],y=l[10];switch(i){case"XYZ":this._y=Math.asin(Dn(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(-g,y),this._z=Math.atan2(-d,c)):(this._x=Math.atan2(x,p),this._z=0);break;case"YXZ":this._x=Math.asin(-Dn(g,-1,1)),Math.abs(g)<.9999999?(this._y=Math.atan2(h,y),this._z=Math.atan2(m,p)):(this._y=Math.atan2(-_,c),this._z=0);break;case"ZXY":this._x=Math.asin(Dn(x,-1,1)),Math.abs(x)<.9999999?(this._y=Math.atan2(-_,y),this._z=Math.atan2(-d,p)):(this._y=0,this._z=Math.atan2(m,c));break;case"ZYX":this._y=Math.asin(-Dn(_,-1,1)),Math.abs(_)<.9999999?(this._x=Math.atan2(x,y),this._z=Math.atan2(m,c)):(this._x=0,this._z=Math.atan2(-d,p));break;case"YZX":this._z=Math.asin(Dn(m,-1,1)),Math.abs(m)<.9999999?(this._x=Math.atan2(-g,p),this._y=Math.atan2(-_,c)):(this._x=0,this._y=Math.atan2(h,y));break;case"XZY":this._z=Math.asin(-Dn(d,-1,1)),Math.abs(d)<.9999999?(this._x=Math.atan2(x,p),this._y=Math.atan2(h,c)):(this._x=Math.atan2(-g,y),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+i)}return this._order=i,r===!0&&this._onChangeCallback(),this}setFromQuaternion(e,i,r){return v_.makeRotationFromQuaternion(e),this.setFromRotationMatrix(v_,i,r)}setFromVector3(e,i=this._order){return this.set(e.x,e.y,e.z,i)}reorder(e){return S_.setFromEuler(this),this.setFromQuaternion(S_,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],i=0){return e[i]=this._x,e[i+1]=this._y,e[i+2]=this._z,e[i+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}yu.DEFAULT_ORDER="XYZ";class Ev{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let xM=0;const x_=new Y,es=new Do,Yi=new rn,Kl=new Y,Mo=new Y,MM=new Y,yM=new Do,M_=new Y(1,0,0),y_=new Y(0,1,0),E_=new Y(0,0,1),EM={type:"added"},TM={type:"removed"};class Tn extends Ss{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:xM++}),this.uuid=wo(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Tn.DEFAULT_UP.clone();const e=new Y,i=new yu,r=new Do,l=new Y(1,1,1);function c(){r.setFromEuler(i,!1)}function d(){i.setFromQuaternion(r,void 0,!1)}i._onChange(c),r._onChange(d),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:i},quaternion:{configurable:!0,enumerable:!0,value:r},scale:{configurable:!0,enumerable:!0,value:l},modelViewMatrix:{value:new rn},normalMatrix:{value:new ce}}),this.matrix=new rn,this.matrixWorld=new rn,this.matrixAutoUpdate=Tn.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Tn.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Ev,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,i){this.quaternion.setFromAxisAngle(e,i)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,i){return es.setFromAxisAngle(e,i),this.quaternion.multiply(es),this}rotateOnWorldAxis(e,i){return es.setFromAxisAngle(e,i),this.quaternion.premultiply(es),this}rotateX(e){return this.rotateOnAxis(M_,e)}rotateY(e){return this.rotateOnAxis(y_,e)}rotateZ(e){return this.rotateOnAxis(E_,e)}translateOnAxis(e,i){return x_.copy(e).applyQuaternion(this.quaternion),this.position.add(x_.multiplyScalar(i)),this}translateX(e){return this.translateOnAxis(M_,e)}translateY(e){return this.translateOnAxis(y_,e)}translateZ(e){return this.translateOnAxis(E_,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(Yi.copy(this.matrixWorld).invert())}lookAt(e,i,r){e.isVector3?Kl.copy(e):Kl.set(e,i,r);const l=this.parent;this.updateWorldMatrix(!0,!1),Mo.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?Yi.lookAt(Mo,Kl,this.up):Yi.lookAt(Kl,Mo,this.up),this.quaternion.setFromRotationMatrix(Yi),l&&(Yi.extractRotation(l.matrixWorld),es.setFromRotationMatrix(Yi),this.quaternion.premultiply(es.invert()))}add(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.add(arguments[i]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.parent!==null&&e.parent.remove(e),e.parent=this,this.children.push(e),e.dispatchEvent(EM)):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let r=0;r<arguments.length;r++)this.remove(arguments[r]);return this}const i=this.children.indexOf(e);return i!==-1&&(e.parent=null,this.children.splice(i,1),e.dispatchEvent(TM)),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),Yi.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),Yi.multiply(e.parent.matrixWorld)),e.applyMatrix4(Yi),this.add(e),e.updateWorldMatrix(!1,!0),this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,i){if(this[e]===i)return this;for(let r=0,l=this.children.length;r<l;r++){const d=this.children[r].getObjectByProperty(e,i);if(d!==void 0)return d}}getObjectsByProperty(e,i,r=[]){this[e]===i&&r.push(this);const l=this.children;for(let c=0,d=l.length;c<d;c++)l[c].getObjectsByProperty(e,i,r);return r}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Mo,e,MM),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Mo,yM,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const i=this.matrixWorld.elements;return e.set(i[8],i[9],i[10]).normalize()}raycast(){}traverse(e){e(this);const i=this.children;for(let r=0,l=i.length;r<l;r++)i[r].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const i=this.children;for(let r=0,l=i.length;r<l;r++)i[r].traverseVisible(e)}traverseAncestors(e){const i=this.parent;i!==null&&(e(i),i.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix),this.matrixWorldNeedsUpdate=!1,e=!0);const i=this.children;for(let r=0,l=i.length;r<l;r++){const c=i[r];(c.matrixWorldAutoUpdate===!0||e===!0)&&c.updateMatrixWorld(e)}}updateWorldMatrix(e,i){const r=this.parent;if(e===!0&&r!==null&&r.matrixWorldAutoUpdate===!0&&r.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix),i===!0){const l=this.children;for(let c=0,d=l.length;c<d;c++){const h=l[c];h.matrixWorldAutoUpdate===!0&&h.updateWorldMatrix(!1,!0)}}}toJSON(e){const i=e===void 0||typeof e=="string",r={};i&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},r.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const l={};l.uuid=this.uuid,l.type=this.type,this.name!==""&&(l.name=this.name),this.castShadow===!0&&(l.castShadow=!0),this.receiveShadow===!0&&(l.receiveShadow=!0),this.visible===!1&&(l.visible=!1),this.frustumCulled===!1&&(l.frustumCulled=!1),this.renderOrder!==0&&(l.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(l.userData=this.userData),l.layers=this.layers.mask,l.matrix=this.matrix.toArray(),l.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(l.matrixAutoUpdate=!1),this.isInstancedMesh&&(l.type="InstancedMesh",l.count=this.count,l.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(l.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(l.type="BatchedMesh",l.perObjectFrustumCulled=this.perObjectFrustumCulled,l.sortObjects=this.sortObjects,l.drawRanges=this._drawRanges,l.reservedRanges=this._reservedRanges,l.visibility=this._visibility,l.active=this._active,l.bounds=this._bounds.map(h=>({boxInitialized:h.boxInitialized,boxMin:h.box.min.toArray(),boxMax:h.box.max.toArray(),sphereInitialized:h.sphereInitialized,sphereRadius:h.sphere.radius,sphereCenter:h.sphere.center.toArray()})),l.maxGeometryCount=this._maxGeometryCount,l.maxVertexCount=this._maxVertexCount,l.maxIndexCount=this._maxIndexCount,l.geometryInitialized=this._geometryInitialized,l.geometryCount=this._geometryCount,l.matricesTexture=this._matricesTexture.toJSON(e),this.boundingSphere!==null&&(l.boundingSphere={center:l.boundingSphere.center.toArray(),radius:l.boundingSphere.radius}),this.boundingBox!==null&&(l.boundingBox={min:l.boundingBox.min.toArray(),max:l.boundingBox.max.toArray()}));function c(h,m){return h[m.uuid]===void 0&&(h[m.uuid]=m.toJSON(e)),m.uuid}if(this.isScene)this.background&&(this.background.isColor?l.background=this.background.toJSON():this.background.isTexture&&(l.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(l.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){l.geometry=c(e.geometries,this.geometry);const h=this.geometry.parameters;if(h!==void 0&&h.shapes!==void 0){const m=h.shapes;if(Array.isArray(m))for(let p=0,g=m.length;p<g;p++){const _=m[p];c(e.shapes,_)}else c(e.shapes,m)}}if(this.isSkinnedMesh&&(l.bindMode=this.bindMode,l.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(c(e.skeletons,this.skeleton),l.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const h=[];for(let m=0,p=this.material.length;m<p;m++)h.push(c(e.materials,this.material[m]));l.material=h}else l.material=c(e.materials,this.material);if(this.children.length>0){l.children=[];for(let h=0;h<this.children.length;h++)l.children.push(this.children[h].toJSON(e).object)}if(this.animations.length>0){l.animations=[];for(let h=0;h<this.animations.length;h++){const m=this.animations[h];l.animations.push(c(e.animations,m))}}if(i){const h=d(e.geometries),m=d(e.materials),p=d(e.textures),g=d(e.images),_=d(e.shapes),x=d(e.skeletons),y=d(e.animations),b=d(e.nodes);h.length>0&&(r.geometries=h),m.length>0&&(r.materials=m),p.length>0&&(r.textures=p),g.length>0&&(r.images=g),_.length>0&&(r.shapes=_),x.length>0&&(r.skeletons=x),y.length>0&&(r.animations=y),b.length>0&&(r.nodes=b)}return r.object=l,r;function d(h){const m=[];for(const p in h){const g=h[p];delete g.metadata,m.push(g)}return m}}clone(e){return new this.constructor().copy(this,e)}copy(e,i=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),i===!0)for(let r=0;r<e.children.length;r++){const l=e.children[r];this.add(l.clone())}return this}}Tn.DEFAULT_UP=new Y(0,1,0);Tn.DEFAULT_MATRIX_AUTO_UPDATE=!0;Tn.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const gi=new Y,ji=new Y,Jf=new Y,Zi=new Y,ns=new Y,is=new Y,T_=new Y,$f=new Y,th=new Y,eh=new Y;let Ql=!1;class _i{constructor(e=new Y,i=new Y,r=new Y){this.a=e,this.b=i,this.c=r}static getNormal(e,i,r,l){l.subVectors(r,i),gi.subVectors(e,i),l.cross(gi);const c=l.lengthSq();return c>0?l.multiplyScalar(1/Math.sqrt(c)):l.set(0,0,0)}static getBarycoord(e,i,r,l,c){gi.subVectors(l,i),ji.subVectors(r,i),Jf.subVectors(e,i);const d=gi.dot(gi),h=gi.dot(ji),m=gi.dot(Jf),p=ji.dot(ji),g=ji.dot(Jf),_=d*p-h*h;if(_===0)return c.set(0,0,0),null;const x=1/_,y=(p*m-h*g)*x,b=(d*g-h*m)*x;return c.set(1-y-b,b,y)}static containsPoint(e,i,r,l){return this.getBarycoord(e,i,r,l,Zi)===null?!1:Zi.x>=0&&Zi.y>=0&&Zi.x+Zi.y<=1}static getUV(e,i,r,l,c,d,h,m){return Ql===!1&&(console.warn("THREE.Triangle.getUV() has been renamed to THREE.Triangle.getInterpolation()."),Ql=!0),this.getInterpolation(e,i,r,l,c,d,h,m)}static getInterpolation(e,i,r,l,c,d,h,m){return this.getBarycoord(e,i,r,l,Zi)===null?(m.x=0,m.y=0,"z"in m&&(m.z=0),"w"in m&&(m.w=0),null):(m.setScalar(0),m.addScaledVector(c,Zi.x),m.addScaledVector(d,Zi.y),m.addScaledVector(h,Zi.z),m)}static isFrontFacing(e,i,r,l){return gi.subVectors(r,i),ji.subVectors(e,i),gi.cross(ji).dot(l)<0}set(e,i,r){return this.a.copy(e),this.b.copy(i),this.c.copy(r),this}setFromPointsAndIndices(e,i,r,l){return this.a.copy(e[i]),this.b.copy(e[r]),this.c.copy(e[l]),this}setFromAttributeAndIndices(e,i,r,l){return this.a.fromBufferAttribute(e,i),this.b.fromBufferAttribute(e,r),this.c.fromBufferAttribute(e,l),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return gi.subVectors(this.c,this.b),ji.subVectors(this.a,this.b),gi.cross(ji).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return _i.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,i){return _i.getBarycoord(e,this.a,this.b,this.c,i)}getUV(e,i,r,l,c){return Ql===!1&&(console.warn("THREE.Triangle.getUV() has been renamed to THREE.Triangle.getInterpolation()."),Ql=!0),_i.getInterpolation(e,this.a,this.b,this.c,i,r,l,c)}getInterpolation(e,i,r,l,c){return _i.getInterpolation(e,this.a,this.b,this.c,i,r,l,c)}containsPoint(e){return _i.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return _i.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,i){const r=this.a,l=this.b,c=this.c;let d,h;ns.subVectors(l,r),is.subVectors(c,r),$f.subVectors(e,r);const m=ns.dot($f),p=is.dot($f);if(m<=0&&p<=0)return i.copy(r);th.subVectors(e,l);const g=ns.dot(th),_=is.dot(th);if(g>=0&&_<=g)return i.copy(l);const x=m*_-g*p;if(x<=0&&m>=0&&g<=0)return d=m/(m-g),i.copy(r).addScaledVector(ns,d);eh.subVectors(e,c);const y=ns.dot(eh),b=is.dot(eh);if(b>=0&&y<=b)return i.copy(c);const A=y*p-m*b;if(A<=0&&p>=0&&b<=0)return h=p/(p-b),i.copy(r).addScaledVector(is,h);const M=g*b-y*_;if(M<=0&&_-g>=0&&y-b>=0)return T_.subVectors(c,l),h=(_-g)/(_-g+(y-b)),i.copy(l).addScaledVector(T_,h);const v=1/(M+A+x);return d=A*v,h=x*v,i.copy(r).addScaledVector(ns,d).addScaledVector(is,h)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Tv={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Ua={h:0,s:0,l:0},Jl={h:0,s:0,l:0};function nh(o,e,i){return i<0&&(i+=1),i>1&&(i-=1),i<1/6?o+(e-o)*6*i:i<1/2?e:i<2/3?o+(e-o)*6*(2/3-i):o}class Me{constructor(e,i,r){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,i,r)}set(e,i,r){if(i===void 0&&r===void 0){const l=e;l&&l.isColor?this.copy(l):typeof l=="number"?this.setHex(l):typeof l=="string"&&this.setStyle(l)}else this.setRGB(e,i,r);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,i=vn){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Ue.toWorkingColorSpace(this,i),this}setRGB(e,i,r,l=Ue.workingColorSpace){return this.r=e,this.g=i,this.b=r,Ue.toWorkingColorSpace(this,l),this}setHSL(e,i,r,l=Ue.workingColorSpace){if(e=uM(e,1),i=Dn(i,0,1),r=Dn(r,0,1),i===0)this.r=this.g=this.b=r;else{const c=r<=.5?r*(1+i):r+i-r*i,d=2*r-c;this.r=nh(d,c,e+1/3),this.g=nh(d,c,e),this.b=nh(d,c,e-1/3)}return Ue.toWorkingColorSpace(this,l),this}setStyle(e,i=vn){function r(c){c!==void 0&&parseFloat(c)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let l;if(l=/^(\w+)\(([^\)]*)\)/.exec(e)){let c;const d=l[1],h=l[2];switch(d){case"rgb":case"rgba":if(c=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return r(c[4]),this.setRGB(Math.min(255,parseInt(c[1],10))/255,Math.min(255,parseInt(c[2],10))/255,Math.min(255,parseInt(c[3],10))/255,i);if(c=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return r(c[4]),this.setRGB(Math.min(100,parseInt(c[1],10))/100,Math.min(100,parseInt(c[2],10))/100,Math.min(100,parseInt(c[3],10))/100,i);break;case"hsl":case"hsla":if(c=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return r(c[4]),this.setHSL(parseFloat(c[1])/360,parseFloat(c[2])/100,parseFloat(c[3])/100,i);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(l=/^\#([A-Fa-f\d]+)$/.exec(e)){const c=l[1],d=c.length;if(d===3)return this.setRGB(parseInt(c.charAt(0),16)/15,parseInt(c.charAt(1),16)/15,parseInt(c.charAt(2),16)/15,i);if(d===6)return this.setHex(parseInt(c,16),i);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,i);return this}setColorName(e,i=vn){const r=Tv[e.toLowerCase()];return r!==void 0?this.setHex(r,i):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=ps(e.r),this.g=ps(e.g),this.b=ps(e.b),this}copyLinearToSRGB(e){return this.r=Wf(e.r),this.g=Wf(e.g),this.b=Wf(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=vn){return Ue.fromWorkingColorSpace(En.copy(this),e),Math.round(Dn(En.r*255,0,255))*65536+Math.round(Dn(En.g*255,0,255))*256+Math.round(Dn(En.b*255,0,255))}getHexString(e=vn){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,i=Ue.workingColorSpace){Ue.fromWorkingColorSpace(En.copy(this),i);const r=En.r,l=En.g,c=En.b,d=Math.max(r,l,c),h=Math.min(r,l,c);let m,p;const g=(h+d)/2;if(h===d)m=0,p=0;else{const _=d-h;switch(p=g<=.5?_/(d+h):_/(2-d-h),d){case r:m=(l-c)/_+(l<c?6:0);break;case l:m=(c-r)/_+2;break;case c:m=(r-l)/_+4;break}m/=6}return e.h=m,e.s=p,e.l=g,e}getRGB(e,i=Ue.workingColorSpace){return Ue.fromWorkingColorSpace(En.copy(this),i),e.r=En.r,e.g=En.g,e.b=En.b,e}getStyle(e=vn){Ue.fromWorkingColorSpace(En.copy(this),e);const i=En.r,r=En.g,l=En.b;return e!==vn?`color(${e} ${i.toFixed(3)} ${r.toFixed(3)} ${l.toFixed(3)})`:`rgb(${Math.round(i*255)},${Math.round(r*255)},${Math.round(l*255)})`}offsetHSL(e,i,r){return this.getHSL(Ua),this.setHSL(Ua.h+e,Ua.s+i,Ua.l+r)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,i){return this.r=e.r+i.r,this.g=e.g+i.g,this.b=e.b+i.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,i){return this.r+=(e.r-this.r)*i,this.g+=(e.g-this.g)*i,this.b+=(e.b-this.b)*i,this}lerpColors(e,i,r){return this.r=e.r+(i.r-e.r)*r,this.g=e.g+(i.g-e.g)*r,this.b=e.b+(i.b-e.b)*r,this}lerpHSL(e,i){this.getHSL(Ua),e.getHSL(Jl);const r=Vf(Ua.h,Jl.h,i),l=Vf(Ua.s,Jl.s,i),c=Vf(Ua.l,Jl.l,i);return this.setHSL(r,l,c),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const i=this.r,r=this.g,l=this.b,c=e.elements;return this.r=c[0]*i+c[3]*r+c[6]*l,this.g=c[1]*i+c[4]*r+c[7]*l,this.b=c[2]*i+c[5]*r+c[8]*l,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,i=0){return this.r=e[i],this.g=e[i+1],this.b=e[i+2],this}toArray(e=[],i=0){return e[i]=this.r,e[i+1]=this.g,e[i+2]=this.b,e}fromBufferAttribute(e,i){return this.r=e.getX(i),this.g=e.getY(i),this.b=e.getZ(i),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const En=new Me;Me.NAMES=Tv;let bM=0;class Uo extends Ss{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:bM++}),this.uuid=wo(),this.name="",this.type="Material",this.blending=ds,this.side=Fa,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=vh,this.blendDst=Sh,this.blendEquation=ur,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new Me(0,0,0),this.blendAlpha=0,this.depthFunc=pu,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=c_,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=Zr,this.stencilZFail=Zr,this.stencilZPass=Zr,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBuild(){}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const i in e){const r=e[i];if(r===void 0){console.warn(`THREE.Material: parameter '${i}' has value of undefined.`);continue}const l=this[i];if(l===void 0){console.warn(`THREE.Material: '${i}' is not a property of THREE.${this.type}.`);continue}l&&l.isColor?l.set(r):l&&l.isVector3&&r&&r.isVector3?l.copy(r):this[i]=r}}toJSON(e){const i=e===void 0||typeof e=="string";i&&(e={textures:{},images:{}});const r={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};r.uuid=this.uuid,r.type=this.type,this.name!==""&&(r.name=this.name),this.color&&this.color.isColor&&(r.color=this.color.getHex()),this.roughness!==void 0&&(r.roughness=this.roughness),this.metalness!==void 0&&(r.metalness=this.metalness),this.sheen!==void 0&&(r.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(r.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(r.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(r.emissive=this.emissive.getHex()),this.emissiveIntensity&&this.emissiveIntensity!==1&&(r.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(r.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(r.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(r.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(r.shininess=this.shininess),this.clearcoat!==void 0&&(r.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(r.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(r.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(r.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(r.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,r.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.iridescence!==void 0&&(r.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(r.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(r.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(r.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(r.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(r.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(r.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(r.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(r.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(r.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(r.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(r.lightMap=this.lightMap.toJSON(e).uuid,r.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(r.aoMap=this.aoMap.toJSON(e).uuid,r.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(r.bumpMap=this.bumpMap.toJSON(e).uuid,r.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(r.normalMap=this.normalMap.toJSON(e).uuid,r.normalMapType=this.normalMapType,r.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(r.displacementMap=this.displacementMap.toJSON(e).uuid,r.displacementScale=this.displacementScale,r.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(r.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(r.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(r.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(r.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(r.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(r.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(r.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(r.combine=this.combine)),this.envMapIntensity!==void 0&&(r.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(r.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(r.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(r.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(r.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(r.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(r.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(r.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(r.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(r.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(r.size=this.size),this.shadowSide!==null&&(r.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(r.sizeAttenuation=this.sizeAttenuation),this.blending!==ds&&(r.blending=this.blending),this.side!==Fa&&(r.side=this.side),this.vertexColors===!0&&(r.vertexColors=!0),this.opacity<1&&(r.opacity=this.opacity),this.transparent===!0&&(r.transparent=!0),this.blendSrc!==vh&&(r.blendSrc=this.blendSrc),this.blendDst!==Sh&&(r.blendDst=this.blendDst),this.blendEquation!==ur&&(r.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(r.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(r.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(r.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(r.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(r.blendAlpha=this.blendAlpha),this.depthFunc!==pu&&(r.depthFunc=this.depthFunc),this.depthTest===!1&&(r.depthTest=this.depthTest),this.depthWrite===!1&&(r.depthWrite=this.depthWrite),this.colorWrite===!1&&(r.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(r.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==c_&&(r.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(r.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(r.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==Zr&&(r.stencilFail=this.stencilFail),this.stencilZFail!==Zr&&(r.stencilZFail=this.stencilZFail),this.stencilZPass!==Zr&&(r.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(r.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(r.rotation=this.rotation),this.polygonOffset===!0&&(r.polygonOffset=!0),this.polygonOffsetFactor!==0&&(r.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(r.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(r.linewidth=this.linewidth),this.dashSize!==void 0&&(r.dashSize=this.dashSize),this.gapSize!==void 0&&(r.gapSize=this.gapSize),this.scale!==void 0&&(r.scale=this.scale),this.dithering===!0&&(r.dithering=!0),this.alphaTest>0&&(r.alphaTest=this.alphaTest),this.alphaHash===!0&&(r.alphaHash=!0),this.alphaToCoverage===!0&&(r.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(r.premultipliedAlpha=!0),this.forceSinglePass===!0&&(r.forceSinglePass=!0),this.wireframe===!0&&(r.wireframe=!0),this.wireframeLinewidth>1&&(r.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(r.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(r.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(r.flatShading=!0),this.visible===!1&&(r.visible=!1),this.toneMapped===!1&&(r.toneMapped=!1),this.fog===!1&&(r.fog=!1),Object.keys(this.userData).length>0&&(r.userData=this.userData);function l(c){const d=[];for(const h in c){const m=c[h];delete m.metadata,d.push(m)}return d}if(i){const c=l(e.textures),d=l(e.images);c.length>0&&(r.textures=c),d.length>0&&(r.images=d)}return r}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const i=e.clippingPlanes;let r=null;if(i!==null){const l=i.length;r=new Array(l);for(let c=0;c!==l;++c)r[c]=i[c].clone()}return this.clippingPlanes=r,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}}class bv extends Uo{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new Me(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.combine=ov,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const an=new Y,$l=new ge;class Ai{constructor(e,i,r=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,this.name="",this.array=e,this.itemSize=i,this.count=e!==void 0?e.length/i:0,this.normalized=r,this.usage=f_,this._updateRange={offset:0,count:-1},this.updateRanges=[],this.gpuType=Oa,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}get updateRange(){return console.warn("THREE.BufferAttribute: updateRange() is deprecated and will be removed in r169. Use addUpdateRange() instead."),this._updateRange}setUsage(e){return this.usage=e,this}addUpdateRange(e,i){this.updateRanges.push({start:e,count:i})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,i,r){e*=this.itemSize,r*=i.itemSize;for(let l=0,c=this.itemSize;l<c;l++)this.array[e+l]=i.array[r+l];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let i=0,r=this.count;i<r;i++)$l.fromBufferAttribute(this,i),$l.applyMatrix3(e),this.setXY(i,$l.x,$l.y);else if(this.itemSize===3)for(let i=0,r=this.count;i<r;i++)an.fromBufferAttribute(this,i),an.applyMatrix3(e),this.setXYZ(i,an.x,an.y,an.z);return this}applyMatrix4(e){for(let i=0,r=this.count;i<r;i++)an.fromBufferAttribute(this,i),an.applyMatrix4(e),this.setXYZ(i,an.x,an.y,an.z);return this}applyNormalMatrix(e){for(let i=0,r=this.count;i<r;i++)an.fromBufferAttribute(this,i),an.applyNormalMatrix(e),this.setXYZ(i,an.x,an.y,an.z);return this}transformDirection(e){for(let i=0,r=this.count;i<r;i++)an.fromBufferAttribute(this,i),an.transformDirection(e),this.setXYZ(i,an.x,an.y,an.z);return this}set(e,i=0){return this.array.set(e,i),this}getComponent(e,i){let r=this.array[e*this.itemSize+i];return this.normalized&&(r=vo(r,this.array)),r}setComponent(e,i,r){return this.normalized&&(r=In(r,this.array)),this.array[e*this.itemSize+i]=r,this}getX(e){let i=this.array[e*this.itemSize];return this.normalized&&(i=vo(i,this.array)),i}setX(e,i){return this.normalized&&(i=In(i,this.array)),this.array[e*this.itemSize]=i,this}getY(e){let i=this.array[e*this.itemSize+1];return this.normalized&&(i=vo(i,this.array)),i}setY(e,i){return this.normalized&&(i=In(i,this.array)),this.array[e*this.itemSize+1]=i,this}getZ(e){let i=this.array[e*this.itemSize+2];return this.normalized&&(i=vo(i,this.array)),i}setZ(e,i){return this.normalized&&(i=In(i,this.array)),this.array[e*this.itemSize+2]=i,this}getW(e){let i=this.array[e*this.itemSize+3];return this.normalized&&(i=vo(i,this.array)),i}setW(e,i){return this.normalized&&(i=In(i,this.array)),this.array[e*this.itemSize+3]=i,this}setXY(e,i,r){return e*=this.itemSize,this.normalized&&(i=In(i,this.array),r=In(r,this.array)),this.array[e+0]=i,this.array[e+1]=r,this}setXYZ(e,i,r,l){return e*=this.itemSize,this.normalized&&(i=In(i,this.array),r=In(r,this.array),l=In(l,this.array)),this.array[e+0]=i,this.array[e+1]=r,this.array[e+2]=l,this}setXYZW(e,i,r,l,c){return e*=this.itemSize,this.normalized&&(i=In(i,this.array),r=In(r,this.array),l=In(l,this.array),c=In(c,this.array)),this.array[e+0]=i,this.array[e+1]=r,this.array[e+2]=l,this.array[e+3]=c,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==f_&&(e.usage=this.usage),e}}class Av extends Ai{constructor(e,i,r){super(new Uint16Array(e),i,r)}}class Rv extends Ai{constructor(e,i,r){super(new Uint32Array(e),i,r)}}class bn extends Ai{constructor(e,i,r){super(new Float32Array(e),i,r)}}let AM=0;const si=new rn,ih=new Tn,as=new Y,Zn=new Lo,yo=new Lo,hn=new Y;class Ri extends Ss{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:AM++}),this.uuid=wo(),this.name="",this.type="BufferGeometry",this.index=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Sv(e)?Rv:Av)(e,1):this.index=e,this}getAttribute(e){return this.attributes[e]}setAttribute(e,i){return this.attributes[e]=i,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,i,r=0){this.groups.push({start:e,count:i,materialIndex:r})}clearGroups(){this.groups=[]}setDrawRange(e,i){this.drawRange.start=e,this.drawRange.count=i}applyMatrix4(e){const i=this.attributes.position;i!==void 0&&(i.applyMatrix4(e),i.needsUpdate=!0);const r=this.attributes.normal;if(r!==void 0){const c=new ce().getNormalMatrix(e);r.applyNormalMatrix(c),r.needsUpdate=!0}const l=this.attributes.tangent;return l!==void 0&&(l.transformDirection(e),l.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return si.makeRotationFromQuaternion(e),this.applyMatrix4(si),this}rotateX(e){return si.makeRotationX(e),this.applyMatrix4(si),this}rotateY(e){return si.makeRotationY(e),this.applyMatrix4(si),this}rotateZ(e){return si.makeRotationZ(e),this.applyMatrix4(si),this}translate(e,i,r){return si.makeTranslation(e,i,r),this.applyMatrix4(si),this}scale(e,i,r){return si.makeScale(e,i,r),this.applyMatrix4(si),this}lookAt(e){return ih.lookAt(e),ih.updateMatrix(),this.applyMatrix4(ih.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(as).negate(),this.translate(as.x,as.y,as.z),this}setFromPoints(e){const i=[];for(let r=0,l=e.length;r<l;r++){const c=e[r];i.push(c.x,c.y,c.z||0)}return this.setAttribute("position",new bn(i,3)),this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Lo);const e=this.attributes.position,i=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error('THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box. Alternatively set "mesh.frustumCulled" to "false".',this),this.boundingBox.set(new Y(-1/0,-1/0,-1/0),new Y(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),i)for(let r=0,l=i.length;r<l;r++){const c=i[r];Zn.setFromBufferAttribute(c),this.morphTargetsRelative?(hn.addVectors(this.boundingBox.min,Zn.min),this.boundingBox.expandByPoint(hn),hn.addVectors(this.boundingBox.max,Zn.max),this.boundingBox.expandByPoint(hn)):(this.boundingBox.expandByPoint(Zn.min),this.boundingBox.expandByPoint(Zn.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Lh);const e=this.attributes.position,i=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error('THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere. Alternatively set "mesh.frustumCulled" to "false".',this),this.boundingSphere.set(new Y,1/0);return}if(e){const r=this.boundingSphere.center;if(Zn.setFromBufferAttribute(e),i)for(let c=0,d=i.length;c<d;c++){const h=i[c];yo.setFromBufferAttribute(h),this.morphTargetsRelative?(hn.addVectors(Zn.min,yo.min),Zn.expandByPoint(hn),hn.addVectors(Zn.max,yo.max),Zn.expandByPoint(hn)):(Zn.expandByPoint(yo.min),Zn.expandByPoint(yo.max))}Zn.getCenter(r);let l=0;for(let c=0,d=e.count;c<d;c++)hn.fromBufferAttribute(e,c),l=Math.max(l,r.distanceToSquared(hn));if(i)for(let c=0,d=i.length;c<d;c++){const h=i[c],m=this.morphTargetsRelative;for(let p=0,g=h.count;p<g;p++)hn.fromBufferAttribute(h,p),m&&(as.fromBufferAttribute(e,p),hn.add(as)),l=Math.max(l,r.distanceToSquared(hn))}this.boundingSphere.radius=Math.sqrt(l),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,i=this.attributes;if(e===null||i.position===void 0||i.normal===void 0||i.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const r=e.array,l=i.position.array,c=i.normal.array,d=i.uv.array,h=l.length/3;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Ai(new Float32Array(4*h),4));const m=this.getAttribute("tangent").array,p=[],g=[];for(let N=0;N<h;N++)p[N]=new Y,g[N]=new Y;const _=new Y,x=new Y,y=new Y,b=new ge,A=new ge,M=new ge,v=new Y,D=new Y;function T(N,rt,dt){_.fromArray(l,N*3),x.fromArray(l,rt*3),y.fromArray(l,dt*3),b.fromArray(d,N*2),A.fromArray(d,rt*2),M.fromArray(d,dt*2),x.sub(_),y.sub(_),A.sub(b),M.sub(b);const Et=1/(A.x*M.y-M.x*A.y);isFinite(Et)&&(v.copy(x).multiplyScalar(M.y).addScaledVector(y,-A.y).multiplyScalar(Et),D.copy(y).multiplyScalar(A.x).addScaledVector(x,-M.x).multiplyScalar(Et),p[N].add(v),p[rt].add(v),p[dt].add(v),g[N].add(D),g[rt].add(D),g[dt].add(D))}let z=this.groups;z.length===0&&(z=[{start:0,count:r.length}]);for(let N=0,rt=z.length;N<rt;++N){const dt=z[N],Et=dt.start,X=dt.count;for(let tt=Et,P=Et+X;tt<P;tt+=3)T(r[tt+0],r[tt+1],r[tt+2])}const V=new Y,B=new Y,O=new Y,ut=new Y;function C(N){O.fromArray(c,N*3),ut.copy(O);const rt=p[N];V.copy(rt),V.sub(O.multiplyScalar(O.dot(rt))).normalize(),B.crossVectors(ut,rt);const Et=B.dot(g[N])<0?-1:1;m[N*4]=V.x,m[N*4+1]=V.y,m[N*4+2]=V.z,m[N*4+3]=Et}for(let N=0,rt=z.length;N<rt;++N){const dt=z[N],Et=dt.start,X=dt.count;for(let tt=Et,P=Et+X;tt<P;tt+=3)C(r[tt+0]),C(r[tt+1]),C(r[tt+2])}}computeVertexNormals(){const e=this.index,i=this.getAttribute("position");if(i!==void 0){let r=this.getAttribute("normal");if(r===void 0)r=new Ai(new Float32Array(i.count*3),3),this.setAttribute("normal",r);else for(let x=0,y=r.count;x<y;x++)r.setXYZ(x,0,0,0);const l=new Y,c=new Y,d=new Y,h=new Y,m=new Y,p=new Y,g=new Y,_=new Y;if(e)for(let x=0,y=e.count;x<y;x+=3){const b=e.getX(x+0),A=e.getX(x+1),M=e.getX(x+2);l.fromBufferAttribute(i,b),c.fromBufferAttribute(i,A),d.fromBufferAttribute(i,M),g.subVectors(d,c),_.subVectors(l,c),g.cross(_),h.fromBufferAttribute(r,b),m.fromBufferAttribute(r,A),p.fromBufferAttribute(r,M),h.add(g),m.add(g),p.add(g),r.setXYZ(b,h.x,h.y,h.z),r.setXYZ(A,m.x,m.y,m.z),r.setXYZ(M,p.x,p.y,p.z)}else for(let x=0,y=i.count;x<y;x+=3)l.fromBufferAttribute(i,x+0),c.fromBufferAttribute(i,x+1),d.fromBufferAttribute(i,x+2),g.subVectors(d,c),_.subVectors(l,c),g.cross(_),r.setXYZ(x+0,g.x,g.y,g.z),r.setXYZ(x+1,g.x,g.y,g.z),r.setXYZ(x+2,g.x,g.y,g.z);this.normalizeNormals(),r.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let i=0,r=e.count;i<r;i++)hn.fromBufferAttribute(e,i),hn.normalize(),e.setXYZ(i,hn.x,hn.y,hn.z)}toNonIndexed(){function e(h,m){const p=h.array,g=h.itemSize,_=h.normalized,x=new p.constructor(m.length*g);let y=0,b=0;for(let A=0,M=m.length;A<M;A++){h.isInterleavedBufferAttribute?y=m[A]*h.data.stride+h.offset:y=m[A]*g;for(let v=0;v<g;v++)x[b++]=p[y++]}return new Ai(x,g,_)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const i=new Ri,r=this.index.array,l=this.attributes;for(const h in l){const m=l[h],p=e(m,r);i.setAttribute(h,p)}const c=this.morphAttributes;for(const h in c){const m=[],p=c[h];for(let g=0,_=p.length;g<_;g++){const x=p[g],y=e(x,r);m.push(y)}i.morphAttributes[h]=m}i.morphTargetsRelative=this.morphTargetsRelative;const d=this.groups;for(let h=0,m=d.length;h<m;h++){const p=d[h];i.addGroup(p.start,p.count,p.materialIndex)}return i}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const m=this.parameters;for(const p in m)m[p]!==void 0&&(e[p]=m[p]);return e}e.data={attributes:{}};const i=this.index;i!==null&&(e.data.index={type:i.array.constructor.name,array:Array.prototype.slice.call(i.array)});const r=this.attributes;for(const m in r){const p=r[m];e.data.attributes[m]=p.toJSON(e.data)}const l={};let c=!1;for(const m in this.morphAttributes){const p=this.morphAttributes[m],g=[];for(let _=0,x=p.length;_<x;_++){const y=p[_];g.push(y.toJSON(e.data))}g.length>0&&(l[m]=g,c=!0)}c&&(e.data.morphAttributes=l,e.data.morphTargetsRelative=this.morphTargetsRelative);const d=this.groups;d.length>0&&(e.data.groups=JSON.parse(JSON.stringify(d)));const h=this.boundingSphere;return h!==null&&(e.data.boundingSphere={center:h.center.toArray(),radius:h.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const i={};this.name=e.name;const r=e.index;r!==null&&this.setIndex(r.clone(i));const l=e.attributes;for(const p in l){const g=l[p];this.setAttribute(p,g.clone(i))}const c=e.morphAttributes;for(const p in c){const g=[],_=c[p];for(let x=0,y=_.length;x<y;x++)g.push(_[x].clone(i));this.morphAttributes[p]=g}this.morphTargetsRelative=e.morphTargetsRelative;const d=e.groups;for(let p=0,g=d.length;p<g;p++){const _=d[p];this.addGroup(_.start,_.count,_.materialIndex)}const h=e.boundingBox;h!==null&&(this.boundingBox=h.clone());const m=e.boundingSphere;return m!==null&&(this.boundingSphere=m.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const b_=new rn,rr=new _M,tu=new Lh,A_=new Y,rs=new Y,ss=new Y,os=new Y,ah=new Y,eu=new Y,nu=new ge,iu=new ge,au=new ge,R_=new Y,C_=new Y,w_=new Y,ru=new Y,su=new Y;class za extends Tn{constructor(e=new Ri,i=new bv){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=i,this.updateMorphTargets()}copy(e,i){return super.copy(e,i),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const i=this.geometry.morphAttributes,r=Object.keys(i);if(r.length>0){const l=i[r[0]];if(l!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let c=0,d=l.length;c<d;c++){const h=l[c].name||String(c);this.morphTargetInfluences.push(0),this.morphTargetDictionary[h]=c}}}}getVertexPosition(e,i){const r=this.geometry,l=r.attributes.position,c=r.morphAttributes.position,d=r.morphTargetsRelative;i.fromBufferAttribute(l,e);const h=this.morphTargetInfluences;if(c&&h){eu.set(0,0,0);for(let m=0,p=c.length;m<p;m++){const g=h[m],_=c[m];g!==0&&(ah.fromBufferAttribute(_,e),d?eu.addScaledVector(ah,g):eu.addScaledVector(ah.sub(i),g))}i.add(eu)}return i}raycast(e,i){const r=this.geometry,l=this.material,c=this.matrixWorld;l!==void 0&&(r.boundingSphere===null&&r.computeBoundingSphere(),tu.copy(r.boundingSphere),tu.applyMatrix4(c),rr.copy(e.ray).recast(e.near),!(tu.containsPoint(rr.origin)===!1&&(rr.intersectSphere(tu,A_)===null||rr.origin.distanceToSquared(A_)>(e.far-e.near)**2))&&(b_.copy(c).invert(),rr.copy(e.ray).applyMatrix4(b_),!(r.boundingBox!==null&&rr.intersectsBox(r.boundingBox)===!1)&&this._computeIntersections(e,i,rr)))}_computeIntersections(e,i,r){let l;const c=this.geometry,d=this.material,h=c.index,m=c.attributes.position,p=c.attributes.uv,g=c.attributes.uv1,_=c.attributes.normal,x=c.groups,y=c.drawRange;if(h!==null)if(Array.isArray(d))for(let b=0,A=x.length;b<A;b++){const M=x[b],v=d[M.materialIndex],D=Math.max(M.start,y.start),T=Math.min(h.count,Math.min(M.start+M.count,y.start+y.count));for(let z=D,V=T;z<V;z+=3){const B=h.getX(z),O=h.getX(z+1),ut=h.getX(z+2);l=ou(this,v,e,r,p,g,_,B,O,ut),l&&(l.faceIndex=Math.floor(z/3),l.face.materialIndex=M.materialIndex,i.push(l))}}else{const b=Math.max(0,y.start),A=Math.min(h.count,y.start+y.count);for(let M=b,v=A;M<v;M+=3){const D=h.getX(M),T=h.getX(M+1),z=h.getX(M+2);l=ou(this,d,e,r,p,g,_,D,T,z),l&&(l.faceIndex=Math.floor(M/3),i.push(l))}}else if(m!==void 0)if(Array.isArray(d))for(let b=0,A=x.length;b<A;b++){const M=x[b],v=d[M.materialIndex],D=Math.max(M.start,y.start),T=Math.min(m.count,Math.min(M.start+M.count,y.start+y.count));for(let z=D,V=T;z<V;z+=3){const B=z,O=z+1,ut=z+2;l=ou(this,v,e,r,p,g,_,B,O,ut),l&&(l.faceIndex=Math.floor(z/3),l.face.materialIndex=M.materialIndex,i.push(l))}}else{const b=Math.max(0,y.start),A=Math.min(m.count,y.start+y.count);for(let M=b,v=A;M<v;M+=3){const D=M,T=M+1,z=M+2;l=ou(this,d,e,r,p,g,_,D,T,z),l&&(l.faceIndex=Math.floor(M/3),i.push(l))}}}}function RM(o,e,i,r,l,c,d,h){let m;if(e.side===Fn?m=r.intersectTriangle(d,c,l,!0,h):m=r.intersectTriangle(l,c,d,e.side===Fa,h),m===null)return null;su.copy(h),su.applyMatrix4(o.matrixWorld);const p=i.ray.origin.distanceTo(su);return p<i.near||p>i.far?null:{distance:p,point:su.clone(),object:o}}function ou(o,e,i,r,l,c,d,h,m,p){o.getVertexPosition(h,rs),o.getVertexPosition(m,ss),o.getVertexPosition(p,os);const g=RM(o,e,i,r,rs,ss,os,ru);if(g){l&&(nu.fromBufferAttribute(l,h),iu.fromBufferAttribute(l,m),au.fromBufferAttribute(l,p),g.uv=_i.getInterpolation(ru,rs,ss,os,nu,iu,au,new ge)),c&&(nu.fromBufferAttribute(c,h),iu.fromBufferAttribute(c,m),au.fromBufferAttribute(c,p),g.uv1=_i.getInterpolation(ru,rs,ss,os,nu,iu,au,new ge),g.uv2=g.uv1),d&&(R_.fromBufferAttribute(d,h),C_.fromBufferAttribute(d,m),w_.fromBufferAttribute(d,p),g.normal=_i.getInterpolation(ru,rs,ss,os,R_,C_,w_,new Y),g.normal.dot(r.direction)>0&&g.normal.multiplyScalar(-1));const _={a:h,b:m,c:p,normal:new Y,materialIndex:0};_i.getNormal(rs,ss,os,_.normal),g.face=_}return g}class No extends Ri{constructor(e=1,i=1,r=1,l=1,c=1,d=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:i,depth:r,widthSegments:l,heightSegments:c,depthSegments:d};const h=this;l=Math.floor(l),c=Math.floor(c),d=Math.floor(d);const m=[],p=[],g=[],_=[];let x=0,y=0;b("z","y","x",-1,-1,r,i,e,d,c,0),b("z","y","x",1,-1,r,i,-e,d,c,1),b("x","z","y",1,1,e,r,i,l,d,2),b("x","z","y",1,-1,e,r,-i,l,d,3),b("x","y","z",1,-1,e,i,r,l,c,4),b("x","y","z",-1,-1,e,i,-r,l,c,5),this.setIndex(m),this.setAttribute("position",new bn(p,3)),this.setAttribute("normal",new bn(g,3)),this.setAttribute("uv",new bn(_,2));function b(A,M,v,D,T,z,V,B,O,ut,C){const N=z/O,rt=V/ut,dt=z/2,Et=V/2,X=B/2,tt=O+1,P=ut+1;let q=0,J=0;const lt=new Y;for(let ft=0;ft<P;ft++){const L=ft*rt-Et;for(let W=0;W<tt;W++){const G=W*N-dt;lt[A]=G*D,lt[M]=L*T,lt[v]=X,p.push(lt.x,lt.y,lt.z),lt[A]=0,lt[M]=0,lt[v]=B>0?1:-1,g.push(lt.x,lt.y,lt.z),_.push(W/O),_.push(1-ft/ut),q+=1}}for(let ft=0;ft<ut;ft++)for(let L=0;L<O;L++){const W=x+L+tt*ft,G=x+L+tt*(ft+1),K=x+(L+1)+tt*(ft+1),mt=x+(L+1)+tt*ft;m.push(W,G,mt),m.push(G,K,mt),J+=6}h.addGroup(y,J,C),y+=J,x+=q}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new No(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function vs(o){const e={};for(const i in o){e[i]={};for(const r in o[i]){const l=o[i][r];l&&(l.isColor||l.isMatrix3||l.isMatrix4||l.isVector2||l.isVector3||l.isVector4||l.isTexture||l.isQuaternion)?l.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[i][r]=null):e[i][r]=l.clone():Array.isArray(l)?e[i][r]=l.slice():e[i][r]=l}}return e}function Cn(o){const e={};for(let i=0;i<o.length;i++){const r=vs(o[i]);for(const l in r)e[l]=r[l]}return e}function CM(o){const e=[];for(let i=0;i<o.length;i++)e.push(o[i].clone());return e}function Cv(o){return o.getRenderTarget()===null?o.outputColorSpace:Ue.workingColorSpace}const wM={clone:vs,merge:Cn};var DM=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,LM=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class mr extends Uo{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=DM,this.fragmentShader=LM,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={derivatives:!1,fragDepth:!1,drawBuffers:!1,shaderTextureLOD:!1,clipCullDistance:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=vs(e.uniforms),this.uniformsGroups=CM(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const i=super.toJSON(e);i.glslVersion=this.glslVersion,i.uniforms={};for(const l in this.uniforms){const d=this.uniforms[l].value;d&&d.isTexture?i.uniforms[l]={type:"t",value:d.toJSON(e).uuid}:d&&d.isColor?i.uniforms[l]={type:"c",value:d.getHex()}:d&&d.isVector2?i.uniforms[l]={type:"v2",value:d.toArray()}:d&&d.isVector3?i.uniforms[l]={type:"v3",value:d.toArray()}:d&&d.isVector4?i.uniforms[l]={type:"v4",value:d.toArray()}:d&&d.isMatrix3?i.uniforms[l]={type:"m3",value:d.toArray()}:d&&d.isMatrix4?i.uniforms[l]={type:"m4",value:d.toArray()}:i.uniforms[l]={value:d}}Object.keys(this.defines).length>0&&(i.defines=this.defines),i.vertexShader=this.vertexShader,i.fragmentShader=this.fragmentShader,i.lights=this.lights,i.clipping=this.clipping;const r={};for(const l in this.extensions)this.extensions[l]===!0&&(r[l]=!0);return Object.keys(r).length>0&&(i.extensions=r),i}}class wv extends Tn{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new rn,this.projectionMatrix=new rn,this.projectionMatrixInverse=new rn,this.coordinateSystem=Ji}copy(e,i){return super.copy(e,i),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,i){super.updateWorldMatrix(e,i),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}class li extends wv{constructor(e=50,i=1,r=.1,l=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=r,this.far=l,this.focus=10,this.aspect=i,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,i){return super.copy(e,i),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const i=.5*this.getFilmHeight()/e;this.fov=bh*2*Math.atan(i),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(hu*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return bh*2*Math.atan(Math.tan(hu*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}setViewOffset(e,i,r,l,c,d){this.aspect=e/i,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=i,this.view.offsetX=r,this.view.offsetY=l,this.view.width=c,this.view.height=d,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let i=e*Math.tan(hu*.5*this.fov)/this.zoom,r=2*i,l=this.aspect*r,c=-.5*l;const d=this.view;if(this.view!==null&&this.view.enabled){const m=d.fullWidth,p=d.fullHeight;c+=d.offsetX*l/m,i-=d.offsetY*r/p,l*=d.width/m,r*=d.height/p}const h=this.filmOffset;h!==0&&(c+=e*h/this.getFilmWidth()),this.projectionMatrix.makePerspective(c,c+l,i,i-r,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const i=super.toJSON(e);return i.object.fov=this.fov,i.object.zoom=this.zoom,i.object.near=this.near,i.object.far=this.far,i.object.focus=this.focus,i.object.aspect=this.aspect,this.view!==null&&(i.object.view=Object.assign({},this.view)),i.object.filmGauge=this.filmGauge,i.object.filmOffset=this.filmOffset,i}}const ls=-90,us=1;class UM extends Tn{constructor(e,i,r){super(),this.type="CubeCamera",this.renderTarget=r,this.coordinateSystem=null,this.activeMipmapLevel=0;const l=new li(ls,us,e,i);l.layers=this.layers,this.add(l);const c=new li(ls,us,e,i);c.layers=this.layers,this.add(c);const d=new li(ls,us,e,i);d.layers=this.layers,this.add(d);const h=new li(ls,us,e,i);h.layers=this.layers,this.add(h);const m=new li(ls,us,e,i);m.layers=this.layers,this.add(m);const p=new li(ls,us,e,i);p.layers=this.layers,this.add(p)}updateCoordinateSystem(){const e=this.coordinateSystem,i=this.children.concat(),[r,l,c,d,h,m]=i;for(const p of i)this.remove(p);if(e===Ji)r.up.set(0,1,0),r.lookAt(1,0,0),l.up.set(0,1,0),l.lookAt(-1,0,0),c.up.set(0,0,-1),c.lookAt(0,1,0),d.up.set(0,0,1),d.lookAt(0,-1,0),h.up.set(0,1,0),h.lookAt(0,0,1),m.up.set(0,1,0),m.lookAt(0,0,-1);else if(e===vu)r.up.set(0,-1,0),r.lookAt(-1,0,0),l.up.set(0,-1,0),l.lookAt(1,0,0),c.up.set(0,0,1),c.lookAt(0,1,0),d.up.set(0,0,-1),d.lookAt(0,-1,0),h.up.set(0,-1,0),h.lookAt(0,0,1),m.up.set(0,-1,0),m.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const p of i)this.add(p),p.updateMatrixWorld()}update(e,i){this.parent===null&&this.updateMatrixWorld();const{renderTarget:r,activeMipmapLevel:l}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[c,d,h,m,p,g]=this.children,_=e.getRenderTarget(),x=e.getActiveCubeFace(),y=e.getActiveMipmapLevel(),b=e.xr.enabled;e.xr.enabled=!1;const A=r.texture.generateMipmaps;r.texture.generateMipmaps=!1,e.setRenderTarget(r,0,l),e.render(i,c),e.setRenderTarget(r,1,l),e.render(i,d),e.setRenderTarget(r,2,l),e.render(i,h),e.setRenderTarget(r,3,l),e.render(i,m),e.setRenderTarget(r,4,l),e.render(i,p),r.texture.generateMipmaps=A,e.setRenderTarget(r,5,l),e.render(i,g),e.setRenderTarget(_,x,y),e.xr.enabled=b,r.texture.needsPMREMUpdate=!0}}class Dv extends Kn{constructor(e,i,r,l,c,d,h,m,p,g){e=e!==void 0?e:[],i=i!==void 0?i:ms,super(e,i,r,l,c,d,h,m,p,g),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class NM extends pr{constructor(e=1,i={}){super(e,e,i),this.isWebGLCubeRenderTarget=!0;const r={width:e,height:e,depth:1},l=[r,r,r,r,r,r];i.encoding!==void 0&&(bo("THREE.WebGLCubeRenderTarget: option.encoding has been replaced by option.colorSpace."),i.colorSpace=i.encoding===dr?vn:ui),this.texture=new Dv(l,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=i.generateMipmaps!==void 0?i.generateMipmaps:!1,this.texture.minFilter=i.minFilter!==void 0?i.minFilter:oi}fromEquirectangularTexture(e,i){this.texture.type=i.type,this.texture.colorSpace=i.colorSpace,this.texture.generateMipmaps=i.generateMipmaps,this.texture.minFilter=i.minFilter,this.texture.magFilter=i.magFilter;const r={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},l=new No(5,5,5),c=new mr({name:"CubemapFromEquirect",uniforms:vs(r.uniforms),vertexShader:r.vertexShader,fragmentShader:r.fragmentShader,side:Fn,blending:Pa});c.uniforms.tEquirect.value=i;const d=new za(l,c),h=i.minFilter;return i.minFilter===Ao&&(i.minFilter=oi),new UM(1,10,this).update(e,d),i.minFilter=h,d.geometry.dispose(),d.material.dispose(),this}clear(e,i,r,l){const c=e.getRenderTarget();for(let d=0;d<6;d++)e.setRenderTarget(this,d),e.clear(i,r,l);e.setRenderTarget(c)}}const rh=new Y,OM=new Y,zM=new ce;class or{constructor(e=new Y(1,0,0),i=0){this.isPlane=!0,this.normal=e,this.constant=i}set(e,i){return this.normal.copy(e),this.constant=i,this}setComponents(e,i,r,l){return this.normal.set(e,i,r),this.constant=l,this}setFromNormalAndCoplanarPoint(e,i){return this.normal.copy(e),this.constant=-i.dot(this.normal),this}setFromCoplanarPoints(e,i,r){const l=rh.subVectors(r,i).cross(OM.subVectors(e,i)).normalize();return this.setFromNormalAndCoplanarPoint(l,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,i){return i.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,i){const r=e.delta(rh),l=this.normal.dot(r);if(l===0)return this.distanceToPoint(e.start)===0?i.copy(e.start):null;const c=-(e.start.dot(this.normal)+this.constant)/l;return c<0||c>1?null:i.copy(e.start).addScaledVector(r,c)}intersectsLine(e){const i=this.distanceToPoint(e.start),r=this.distanceToPoint(e.end);return i<0&&r>0||r<0&&i>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,i){const r=i||zM.getNormalMatrix(e),l=this.coplanarPoint(rh).applyMatrix4(e),c=this.normal.applyMatrix3(r).normalize();return this.constant=-l.dot(c),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const sr=new Lh,lu=new Y;class Uh{constructor(e=new or,i=new or,r=new or,l=new or,c=new or,d=new or){this.planes=[e,i,r,l,c,d]}set(e,i,r,l,c,d){const h=this.planes;return h[0].copy(e),h[1].copy(i),h[2].copy(r),h[3].copy(l),h[4].copy(c),h[5].copy(d),this}copy(e){const i=this.planes;for(let r=0;r<6;r++)i[r].copy(e.planes[r]);return this}setFromProjectionMatrix(e,i=Ji){const r=this.planes,l=e.elements,c=l[0],d=l[1],h=l[2],m=l[3],p=l[4],g=l[5],_=l[6],x=l[7],y=l[8],b=l[9],A=l[10],M=l[11],v=l[12],D=l[13],T=l[14],z=l[15];if(r[0].setComponents(m-c,x-p,M-y,z-v).normalize(),r[1].setComponents(m+c,x+p,M+y,z+v).normalize(),r[2].setComponents(m+d,x+g,M+b,z+D).normalize(),r[3].setComponents(m-d,x-g,M-b,z-D).normalize(),r[4].setComponents(m-h,x-_,M-A,z-T).normalize(),i===Ji)r[5].setComponents(m+h,x+_,M+A,z+T).normalize();else if(i===vu)r[5].setComponents(h,_,A,T).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+i);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),sr.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const i=e.geometry;i.boundingSphere===null&&i.computeBoundingSphere(),sr.copy(i.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(sr)}intersectsSprite(e){return sr.center.set(0,0,0),sr.radius=.7071067811865476,sr.applyMatrix4(e.matrixWorld),this.intersectsSphere(sr)}intersectsSphere(e){const i=this.planes,r=e.center,l=-e.radius;for(let c=0;c<6;c++)if(i[c].distanceToPoint(r)<l)return!1;return!0}intersectsBox(e){const i=this.planes;for(let r=0;r<6;r++){const l=i[r];if(lu.x=l.normal.x>0?e.max.x:e.min.x,lu.y=l.normal.y>0?e.max.y:e.min.y,lu.z=l.normal.z>0?e.max.z:e.min.z,l.distanceToPoint(lu)<0)return!1}return!0}containsPoint(e){const i=this.planes;for(let r=0;r<6;r++)if(i[r].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}function Lv(){let o=null,e=!1,i=null,r=null;function l(c,d){i(c,d),r=o.requestAnimationFrame(l)}return{start:function(){e!==!0&&i!==null&&(r=o.requestAnimationFrame(l),e=!0)},stop:function(){o.cancelAnimationFrame(r),e=!1},setAnimationLoop:function(c){i=c},setContext:function(c){o=c}}}function PM(o,e){const i=e.isWebGL2,r=new WeakMap;function l(p,g){const _=p.array,x=p.usage,y=_.byteLength,b=o.createBuffer();o.bindBuffer(g,b),o.bufferData(g,_,x),p.onUploadCallback();let A;if(_ instanceof Float32Array)A=o.FLOAT;else if(_ instanceof Uint16Array)if(p.isFloat16BufferAttribute)if(i)A=o.HALF_FLOAT;else throw new Error("THREE.WebGLAttributes: Usage of Float16BufferAttribute requires WebGL2.");else A=o.UNSIGNED_SHORT;else if(_ instanceof Int16Array)A=o.SHORT;else if(_ instanceof Uint32Array)A=o.UNSIGNED_INT;else if(_ instanceof Int32Array)A=o.INT;else if(_ instanceof Int8Array)A=o.BYTE;else if(_ instanceof Uint8Array)A=o.UNSIGNED_BYTE;else if(_ instanceof Uint8ClampedArray)A=o.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+_);return{buffer:b,type:A,bytesPerElement:_.BYTES_PER_ELEMENT,version:p.version,size:y}}function c(p,g,_){const x=g.array,y=g._updateRange,b=g.updateRanges;if(o.bindBuffer(_,p),y.count===-1&&b.length===0&&o.bufferSubData(_,0,x),b.length!==0){for(let A=0,M=b.length;A<M;A++){const v=b[A];i?o.bufferSubData(_,v.start*x.BYTES_PER_ELEMENT,x,v.start,v.count):o.bufferSubData(_,v.start*x.BYTES_PER_ELEMENT,x.subarray(v.start,v.start+v.count))}g.clearUpdateRanges()}y.count!==-1&&(i?o.bufferSubData(_,y.offset*x.BYTES_PER_ELEMENT,x,y.offset,y.count):o.bufferSubData(_,y.offset*x.BYTES_PER_ELEMENT,x.subarray(y.offset,y.offset+y.count)),y.count=-1),g.onUploadCallback()}function d(p){return p.isInterleavedBufferAttribute&&(p=p.data),r.get(p)}function h(p){p.isInterleavedBufferAttribute&&(p=p.data);const g=r.get(p);g&&(o.deleteBuffer(g.buffer),r.delete(p))}function m(p,g){if(p.isGLBufferAttribute){const x=r.get(p);(!x||x.version<p.version)&&r.set(p,{buffer:p.buffer,type:p.type,bytesPerElement:p.elementSize,version:p.version});return}p.isInterleavedBufferAttribute&&(p=p.data);const _=r.get(p);if(_===void 0)r.set(p,l(p,g));else if(_.version<p.version){if(_.size!==p.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");c(_.buffer,p,g),_.version=p.version}}return{get:d,remove:h,update:m}}class Nh extends Ri{constructor(e=1,i=1,r=1,l=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:i,widthSegments:r,heightSegments:l};const c=e/2,d=i/2,h=Math.floor(r),m=Math.floor(l),p=h+1,g=m+1,_=e/h,x=i/m,y=[],b=[],A=[],M=[];for(let v=0;v<g;v++){const D=v*x-d;for(let T=0;T<p;T++){const z=T*_-c;b.push(z,-D,0),A.push(0,0,1),M.push(T/h),M.push(1-v/m)}}for(let v=0;v<m;v++)for(let D=0;D<h;D++){const T=D+p*v,z=D+p*(v+1),V=D+1+p*(v+1),B=D+1+p*v;y.push(T,z,B),y.push(z,V,B)}this.setIndex(y),this.setAttribute("position",new bn(b,3)),this.setAttribute("normal",new bn(A,3)),this.setAttribute("uv",new bn(M,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Nh(e.width,e.height,e.widthSegments,e.heightSegments)}}var BM=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,IM=`#ifdef USE_ALPHAHASH
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
#endif`,FM=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,HM=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,GM=`#ifdef USE_ALPHATEST
	if ( diffuseColor.a < alphaTest ) discard;
#endif`,VM=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,XM=`#ifdef USE_AOMAP
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
#endif`,WM=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,kM=`#ifdef USE_BATCHING
	attribute float batchId;
	uniform highp sampler2D batchingTexture;
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
#endif`,qM=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( batchId );
#endif`,YM=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,jM=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,ZM=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,KM=`#ifdef USE_IRIDESCENCE
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
#endif`,QM=`#ifdef USE_BUMPMAP
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
#endif`,JM=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
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
#endif`,$M=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,ty=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,ey=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,ny=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,iy=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,ay=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR )
	varying vec3 vColor;
#endif`,ry=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif`,sy=`#define PI 3.141592653589793
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
mat3 transposeMat3( const in mat3 m ) {
	mat3 tmp;
	tmp[ 0 ] = vec3( m[ 0 ].x, m[ 1 ].x, m[ 2 ].x );
	tmp[ 1 ] = vec3( m[ 0 ].y, m[ 1 ].y, m[ 2 ].y );
	tmp[ 2 ] = vec3( m[ 0 ].z, m[ 1 ].z, m[ 2 ].z );
	return tmp;
}
float luminance( const in vec3 rgb ) {
	const vec3 weights = vec3( 0.2126729, 0.7151522, 0.0721750 );
	return dot( weights, rgb );
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
} // validated`,oy=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,ly=`vec3 transformedNormal = objectNormal;
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
#endif`,uy=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,cy=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,fy=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,hy=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,dy="gl_FragColor = linearToOutputTexel( gl_FragColor );",py=`
const mat3 LINEAR_SRGB_TO_LINEAR_DISPLAY_P3 = mat3(
	vec3( 0.8224621, 0.177538, 0.0 ),
	vec3( 0.0331941, 0.9668058, 0.0 ),
	vec3( 0.0170827, 0.0723974, 0.9105199 )
);
const mat3 LINEAR_DISPLAY_P3_TO_LINEAR_SRGB = mat3(
	vec3( 1.2249401, - 0.2249404, 0.0 ),
	vec3( - 0.0420569, 1.0420571, 0.0 ),
	vec3( - 0.0196376, - 0.0786361, 1.0982735 )
);
vec4 LinearSRGBToLinearDisplayP3( in vec4 value ) {
	return vec4( value.rgb * LINEAR_SRGB_TO_LINEAR_DISPLAY_P3, value.a );
}
vec4 LinearDisplayP3ToLinearSRGB( in vec4 value ) {
	return vec4( value.rgb * LINEAR_DISPLAY_P3_TO_LINEAR_SRGB, value.a );
}
vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}
vec4 LinearToLinear( in vec4 value ) {
	return value;
}
vec4 LinearTosRGB( in vec4 value ) {
	return sRGBTransferOETF( value );
}`,my=`#ifdef USE_ENVMAP
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
		vec4 envColor = textureCube( envMap, vec3( flipEnvMap * reflectVec.x, reflectVec.yz ) );
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
#endif`,gy=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,_y=`#ifdef USE_ENVMAP
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
#endif`,vy=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Sy=`#ifdef USE_ENVMAP
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
#endif`,xy=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,My=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,yy=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Ey=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,Ty=`#ifdef USE_GRADIENTMAP
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
}`,by=`#ifdef USE_LIGHTMAP
	vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
	vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
	reflectedLight.indirectDiffuse += lightMapIrradiance;
#endif`,Ay=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,Ry=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Cy=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,wy=`uniform bool receiveShadow;
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
	#if defined ( LEGACY_LIGHTS )
		if ( cutoffDistance > 0.0 && decayExponent > 0.0 ) {
			return pow( saturate( - lightDistance / cutoffDistance + 1.0 ), decayExponent );
		}
		return 1.0;
	#else
		float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
		if ( cutoffDistance > 0.0 ) {
			distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
		}
		return distanceFalloff;
	#endif
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
#endif`,Dy=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, roughness * roughness) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, reflectVec, roughness );
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
#endif`,Ly=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,Uy=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Ny=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Oy=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,zy=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb * ( 1.0 - metalnessFactor );
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
	material.specularColor = mix( min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = mix( vec3( 0.04 ), diffuseColor.rgb, metalnessFactor );
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
	material.sheenRoughness = clamp( sheenRoughness, 0.07, 1.0 );
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
#endif`,Py=`struct PhysicalMaterial {
	vec3 diffuseColor;
	float roughness;
	vec3 specularColor;
	float specularF90;
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
		return saturate(v);
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
	vec3 f0 = material.specularColor;
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
	mat3 mat = mInv * transposeMat3( mat3( T1, T2, N ) );
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
	float a = roughness < 0.25 ? -339.2 * r2 + 161.4 * roughness - 25.9 : -8.48 * r2 + 14.3 * roughness - 9.95;
	float b = roughness < 0.25 ? 44.0 * r2 - 23.7 * roughness + 3.26 : 1.97 * r2 - 3.27 * roughness + 0.72;
	float DG = exp( a * dotNV + b ) + ( roughness < 0.25 ? 0.0 : 0.1 * ( roughness - 0.25 ) );
	return saturate( DG * RECIPROCAL_PI );
}
vec2 DFGApprox( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	const vec4 c0 = vec4( - 1, - 0.0275, - 0.572, 0.022 );
	const vec4 c1 = vec4( 1, 0.0425, 1.04, - 0.04 );
	vec4 r = roughness * c0 + c1;
	float a004 = min( r.x * r.x, exp2( - 9.28 * dotNV ) ) * r.x + r.y;
	vec2 fab = vec2( - 1.04, 1.04 ) * a004 + r.zw;
	return fab;
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	vec2 fab = DFGApprox( normal, viewDir, roughness );
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	vec2 fab = DFGApprox( normal, viewDir, roughness );
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
		vec3 fresnel = ( material.specularColor * t2.x + ( vec3( 1.0 ) - material.specularColor ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseColor * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
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
	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
	#endif
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnel, material.roughness, singleScattering, multiScattering );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScattering, multiScattering );
	#endif
	vec3 totalScattering = singleScattering + multiScattering;
	vec3 diffuse = material.diffuseColor * ( 1.0 - max( max( totalScattering.r, totalScattering.g ), totalScattering.b ) );
	reflectedLight.indirectSpecular += radiance * singleScattering;
	reflectedLight.indirectSpecular += multiScattering * cosineWeightedIrradiance;
	reflectedLight.indirectDiffuse += diffuse * cosineWeightedIrradiance;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,By=`
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
		material.iridescenceFresnel = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
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
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
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
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
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
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
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
#endif`,Iy=`#if defined( RE_IndirectDiffuse )
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
#endif`,Fy=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Hy=`#if defined( USE_LOGDEPTHBUF ) && defined( USE_LOGDEPTHBUF_EXT )
	gl_FragDepthEXT = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Gy=`#if defined( USE_LOGDEPTHBUF ) && defined( USE_LOGDEPTHBUF_EXT )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,Vy=`#ifdef USE_LOGDEPTHBUF
	#ifdef USE_LOGDEPTHBUF_EXT
		varying float vFragDepth;
		varying float vIsPerspective;
	#else
		uniform float logDepthBufFC;
	#endif
#endif`,Xy=`#ifdef USE_LOGDEPTHBUF
	#ifdef USE_LOGDEPTHBUF_EXT
		vFragDepth = 1.0 + gl_Position.w;
		vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
	#else
		if ( isPerspectiveMatrix( projectionMatrix ) ) {
			gl_Position.z = log2( max( EPSILON, gl_Position.w + 1.0 ) ) * logDepthBufFC - 1.0;
			gl_Position.z *= gl_Position.w;
		}
	#endif
#endif`,Wy=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = vec4( mix( pow( sampledDiffuseColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), sampledDiffuseColor.rgb * 0.0773993808, vec3( lessThanEqual( sampledDiffuseColor.rgb, vec3( 0.04045 ) ) ) ), sampledDiffuseColor.w );
	
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,ky=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,qy=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,Yy=`#if defined( USE_POINTS_UV )
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
#endif`,jy=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Zy=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,Ky=`#if defined( USE_MORPHCOLORS ) && defined( MORPHTARGETS_TEXTURE )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Qy=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	#ifdef MORPHTARGETS_TEXTURE
		for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
			if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
		}
	#else
		objectNormal += morphNormal0 * morphTargetInfluences[ 0 ];
		objectNormal += morphNormal1 * morphTargetInfluences[ 1 ];
		objectNormal += morphNormal2 * morphTargetInfluences[ 2 ];
		objectNormal += morphNormal3 * morphTargetInfluences[ 3 ];
	#endif
#endif`,Jy=`#ifdef USE_MORPHTARGETS
	uniform float morphTargetBaseInfluence;
	#ifdef MORPHTARGETS_TEXTURE
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
		uniform sampler2DArray morphTargetsTexture;
		uniform ivec2 morphTargetsTextureSize;
		vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
			int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
			int y = texelIndex / morphTargetsTextureSize.x;
			int x = texelIndex - y * morphTargetsTextureSize.x;
			ivec3 morphUV = ivec3( x, y, morphTargetIndex );
			return texelFetch( morphTargetsTexture, morphUV, 0 );
		}
	#else
		#ifndef USE_MORPHNORMALS
			uniform float morphTargetInfluences[ 8 ];
		#else
			uniform float morphTargetInfluences[ 4 ];
		#endif
	#endif
#endif`,$y=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	#ifdef MORPHTARGETS_TEXTURE
		for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
			if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
		}
	#else
		transformed += morphTarget0 * morphTargetInfluences[ 0 ];
		transformed += morphTarget1 * morphTargetInfluences[ 1 ];
		transformed += morphTarget2 * morphTargetInfluences[ 2 ];
		transformed += morphTarget3 * morphTargetInfluences[ 3 ];
		#ifndef USE_MORPHNORMALS
			transformed += morphTarget4 * morphTargetInfluences[ 4 ];
			transformed += morphTarget5 * morphTargetInfluences[ 5 ];
			transformed += morphTarget6 * morphTargetInfluences[ 6 ];
			transformed += morphTarget7 * morphTargetInfluences[ 7 ];
		#endif
	#endif
#endif`,tE=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,eE=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,nE=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,iE=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,aE=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,rE=`#ifdef USE_NORMALMAP
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
#endif`,sE=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,oE=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,lE=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,uE=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,cE=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,fE=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;
const vec3 PackFactors = vec3( 256. * 256. * 256., 256. * 256., 256. );
const vec4 UnpackFactors = UnpackDownscale / vec4( PackFactors, 1. );
const float ShiftRight8 = 1. / 256.;
vec4 packDepthToRGBA( const in float v ) {
	vec4 r = vec4( fract( v * PackFactors ), v );
	r.yzw -= r.xyz * ShiftRight8;	return r * PackUpscale;
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors );
}
vec2 packDepthToRG( in highp float v ) {
	return packDepthToRGBA( v ).yx;
}
float unpackRGToDepth( const in highp vec2 v ) {
	return unpackRGBAToDepth( vec4( v.xy, 0.0, 0.0 ) );
}
vec4 pack2HalfToRGBA( vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( vec4 v ) {
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
}`,hE=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,dE=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,pE=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,mE=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,gE=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,_E=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,vE=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		struct SpotLightShadow {
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform sampler2D pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	float texture2DCompare( sampler2D depths, vec2 uv, float compare ) {
		return step( compare, unpackRGBAToDepth( texture2D( depths, uv ) ) );
	}
	vec2 texture2DDistribution( sampler2D shadow, vec2 uv ) {
		return unpackRGBATo2Half( texture2D( shadow, uv ) );
	}
	float VSMShadow (sampler2D shadow, vec2 uv, float compare ){
		float occlusion = 1.0;
		vec2 distribution = texture2DDistribution( shadow, uv );
		float hard_shadow = step( compare , distribution.x );
		if (hard_shadow != 1.0 ) {
			float distance = compare - distribution.x ;
			float variance = max( 0.00000, distribution.y * distribution.y );
			float softness_probability = variance / (variance + distance * distance );			softness_probability = clamp( ( softness_probability - 0.3 ) / ( 0.95 - 0.3 ), 0.0, 1.0 );			occlusion = clamp( max( hard_shadow, softness_probability ), 0.0, 1.0 );
		}
		return occlusion;
	}
	float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
		float shadow = 1.0;
		shadowCoord.xyz /= shadowCoord.w;
		shadowCoord.z += shadowBias;
		bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
		bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
		if ( frustumTest ) {
		#if defined( SHADOWMAP_TYPE_PCF )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx0 = - texelSize.x * shadowRadius;
			float dy0 = - texelSize.y * shadowRadius;
			float dx1 = + texelSize.x * shadowRadius;
			float dy1 = + texelSize.y * shadowRadius;
			float dx2 = dx0 / 2.0;
			float dy2 = dy0 / 2.0;
			float dx3 = dx1 / 2.0;
			float dy3 = dy1 / 2.0;
			shadow = (
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy2 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx2, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx3, dy3 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( 0.0, dy1 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, shadowCoord.xy + vec2( dx1, dy1 ), shadowCoord.z )
			) * ( 1.0 / 17.0 );
		#elif defined( SHADOWMAP_TYPE_PCF_SOFT )
			vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
			float dx = texelSize.x;
			float dy = texelSize.y;
			vec2 uv = shadowCoord.xy;
			vec2 f = fract( uv * shadowMapSize + 0.5 );
			uv -= f * texelSize;
			shadow = (
				texture2DCompare( shadowMap, uv, shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( dx, 0.0 ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + vec2( 0.0, dy ), shadowCoord.z ) +
				texture2DCompare( shadowMap, uv + texelSize, shadowCoord.z ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, 0.0 ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 0.0 ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( -dx, dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, dy ), shadowCoord.z ),
					 f.x ) +
				mix( texture2DCompare( shadowMap, uv + vec2( 0.0, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( 0.0, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( texture2DCompare( shadowMap, uv + vec2( dx, -dy ), shadowCoord.z ),
					 texture2DCompare( shadowMap, uv + vec2( dx, 2.0 * dy ), shadowCoord.z ),
					 f.y ) +
				mix( mix( texture2DCompare( shadowMap, uv + vec2( -dx, -dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, -dy ), shadowCoord.z ),
						  f.x ),
					 mix( texture2DCompare( shadowMap, uv + vec2( -dx, 2.0 * dy ), shadowCoord.z ),
						  texture2DCompare( shadowMap, uv + vec2( 2.0 * dx, 2.0 * dy ), shadowCoord.z ),
						  f.x ),
					 f.y )
			) * ( 1.0 / 9.0 );
		#elif defined( SHADOWMAP_TYPE_VSM )
			shadow = VSMShadow( shadowMap, shadowCoord.xy, shadowCoord.z );
		#else
			shadow = texture2DCompare( shadowMap, shadowCoord.xy, shadowCoord.z );
		#endif
		}
		return shadow;
	}
	vec2 cubeToUV( vec3 v, float texelSizeY ) {
		vec3 absV = abs( v );
		float scaleToCube = 1.0 / max( absV.x, max( absV.y, absV.z ) );
		absV *= scaleToCube;
		v *= scaleToCube * ( 1.0 - 2.0 * texelSizeY );
		vec2 planar = v.xy;
		float almostATexel = 1.5 * texelSizeY;
		float almostOne = 1.0 - almostATexel;
		if ( absV.z >= almostOne ) {
			if ( v.z > 0.0 )
				planar.x = 4.0 - v.x;
		} else if ( absV.x >= almostOne ) {
			float signX = sign( v.x );
			planar.x = v.z * signX + 2.0 * signX;
		} else if ( absV.y >= almostOne ) {
			float signY = sign( v.y );
			planar.x = v.x + 2.0 * signY + 2.0;
			planar.y = v.z * signY - 2.0;
		}
		return vec2( 0.125, 0.25 ) * planar + vec2( 0.375, 0.75 );
	}
	float getPointShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		vec2 texelSize = vec2( 1.0 ) / ( shadowMapSize * vec2( 4.0, 2.0 ) );
		vec3 lightToPosition = shadowCoord.xyz;
		float dp = ( length( lightToPosition ) - shadowCameraNear ) / ( shadowCameraFar - shadowCameraNear );		dp += shadowBias;
		vec3 bd3D = normalize( lightToPosition );
		#if defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_PCF_SOFT ) || defined( SHADOWMAP_TYPE_VSM )
			vec2 offset = vec2( - 1, 1 ) * shadowRadius * texelSize.y;
			return (
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyy, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyy, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xyx, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yyx, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxy, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxy, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.xxx, texelSize.y ), dp ) +
				texture2DCompare( shadowMap, cubeToUV( bd3D + offset.yxx, texelSize.y ), dp )
			) * ( 1.0 / 9.0 );
		#else
			return texture2DCompare( shadowMap, cubeToUV( bd3D, texelSize.y ), dp );
		#endif
	}
#endif`,SE=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
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
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,xE=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,ME=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,yE=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,EE=`#ifdef USE_SKINNING
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
#endif`,TE=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,bE=`#ifdef USE_SKINNING
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
#endif`,AE=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,RE=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,CE=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,wE=`#ifndef saturate
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
vec3 OptimizedCineonToneMapping( vec3 color ) {
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
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color *= toneMappingExposure;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	return color;
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,DE=`#ifdef USE_TRANSMISSION
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
		n, v, material.roughness, material.diffuseColor, material.specularColor, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,LE=`#ifdef USE_TRANSMISSION
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
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
		vec3 refractedRayExit = position + transmissionRay;
		vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
		vec2 refractionCoords = ndcPos.xy / ndcPos.w;
		refractionCoords += 1.0;
		refractionCoords /= 2.0;
		vec4 transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
		vec3 transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,UE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,NE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,OE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,zE=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const PE=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,BE=`uniform sampler2D t2D;
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
}`,IE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,FE=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float flipEnvMap;
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, vec3( flipEnvMap * vWorldDirection.x, vWorldDirection.yz ) );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,HE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,GE=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,VE=`#include <common>
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
}`,XE=`#if DEPTH_PACKING == 3200
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( 1.0 );
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	float fragCoordZ = 0.5 * vHighPrecisionZW[0] / vHighPrecisionZW[1] + 0.5;
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#endif
}`,WE=`#define DISTANCE
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
}`,kE=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( 1.0 );
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = packDepthToRGBA( dist );
}`,qE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,YE=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,jE=`uniform float scale;
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
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,ZE=`uniform vec3 diffuse;
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
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,KE=`#include <common>
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
}`,QE=`uniform vec3 diffuse;
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,JE=`#define LAMBERT
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
}`,$E=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,tT=`#define MATCAP
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
}`,eT=`#define MATCAP
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,nT=`#define NORMAL
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
}`,iT=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <packing>
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( packNormalToRGB( normal ), opacity );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,aT=`#define PHONG
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
}`,rT=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <packing>
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,sT=`#define STANDARD
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
}`,oT=`#define STANDARD
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
#include <packing>
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( diffuse, opacity );
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
		float sheenEnergyComp = 1.0 - 0.157 * max3( material.sheenColor );
		outgoingLight = outgoingLight * sheenEnergyComp + sheenSpecularDirect + sheenSpecularIndirect;
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
}`,lT=`#define TOON
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
}`,uT=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <packing>
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
	#include <clipping_planes_fragment>
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,cT=`uniform float size;
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
}`,fT=`uniform vec3 diffuse;
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
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,hT=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
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
}`,dT=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <packing>
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
}`,pT=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix * vec4( 0.0, 0.0, 0.0, 1.0 );
	vec2 scale;
	scale.x = length( vec3( modelMatrix[ 0 ].x, modelMatrix[ 0 ].y, modelMatrix[ 0 ].z ) );
	scale.y = length( vec3( modelMatrix[ 1 ].x, modelMatrix[ 1 ].y, modelMatrix[ 1 ].z ) );
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
}`,mT=`uniform vec3 diffuse;
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
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	vec4 diffuseColor = vec4( diffuse, opacity );
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
}`,oe={alphahash_fragment:BM,alphahash_pars_fragment:IM,alphamap_fragment:FM,alphamap_pars_fragment:HM,alphatest_fragment:GM,alphatest_pars_fragment:VM,aomap_fragment:XM,aomap_pars_fragment:WM,batching_pars_vertex:kM,batching_vertex:qM,begin_vertex:YM,beginnormal_vertex:jM,bsdfs:ZM,iridescence_fragment:KM,bumpmap_pars_fragment:QM,clipping_planes_fragment:JM,clipping_planes_pars_fragment:$M,clipping_planes_pars_vertex:ty,clipping_planes_vertex:ey,color_fragment:ny,color_pars_fragment:iy,color_pars_vertex:ay,color_vertex:ry,common:sy,cube_uv_reflection_fragment:oy,defaultnormal_vertex:ly,displacementmap_pars_vertex:uy,displacementmap_vertex:cy,emissivemap_fragment:fy,emissivemap_pars_fragment:hy,colorspace_fragment:dy,colorspace_pars_fragment:py,envmap_fragment:my,envmap_common_pars_fragment:gy,envmap_pars_fragment:_y,envmap_pars_vertex:vy,envmap_physical_pars_fragment:Dy,envmap_vertex:Sy,fog_vertex:xy,fog_pars_vertex:My,fog_fragment:yy,fog_pars_fragment:Ey,gradientmap_pars_fragment:Ty,lightmap_fragment:by,lightmap_pars_fragment:Ay,lights_lambert_fragment:Ry,lights_lambert_pars_fragment:Cy,lights_pars_begin:wy,lights_toon_fragment:Ly,lights_toon_pars_fragment:Uy,lights_phong_fragment:Ny,lights_phong_pars_fragment:Oy,lights_physical_fragment:zy,lights_physical_pars_fragment:Py,lights_fragment_begin:By,lights_fragment_maps:Iy,lights_fragment_end:Fy,logdepthbuf_fragment:Hy,logdepthbuf_pars_fragment:Gy,logdepthbuf_pars_vertex:Vy,logdepthbuf_vertex:Xy,map_fragment:Wy,map_pars_fragment:ky,map_particle_fragment:qy,map_particle_pars_fragment:Yy,metalnessmap_fragment:jy,metalnessmap_pars_fragment:Zy,morphcolor_vertex:Ky,morphnormal_vertex:Qy,morphtarget_pars_vertex:Jy,morphtarget_vertex:$y,normal_fragment_begin:tE,normal_fragment_maps:eE,normal_pars_fragment:nE,normal_pars_vertex:iE,normal_vertex:aE,normalmap_pars_fragment:rE,clearcoat_normal_fragment_begin:sE,clearcoat_normal_fragment_maps:oE,clearcoat_pars_fragment:lE,iridescence_pars_fragment:uE,opaque_fragment:cE,packing:fE,premultiplied_alpha_fragment:hE,project_vertex:dE,dithering_fragment:pE,dithering_pars_fragment:mE,roughnessmap_fragment:gE,roughnessmap_pars_fragment:_E,shadowmap_pars_fragment:vE,shadowmap_pars_vertex:SE,shadowmap_vertex:xE,shadowmask_pars_fragment:ME,skinbase_vertex:yE,skinning_pars_vertex:EE,skinning_vertex:TE,skinnormal_vertex:bE,specularmap_fragment:AE,specularmap_pars_fragment:RE,tonemapping_fragment:CE,tonemapping_pars_fragment:wE,transmission_fragment:DE,transmission_pars_fragment:LE,uv_pars_fragment:UE,uv_pars_vertex:NE,uv_vertex:OE,worldpos_vertex:zE,background_vert:PE,background_frag:BE,backgroundCube_vert:IE,backgroundCube_frag:FE,cube_vert:HE,cube_frag:GE,depth_vert:VE,depth_frag:XE,distanceRGBA_vert:WE,distanceRGBA_frag:kE,equirect_vert:qE,equirect_frag:YE,linedashed_vert:jE,linedashed_frag:ZE,meshbasic_vert:KE,meshbasic_frag:QE,meshlambert_vert:JE,meshlambert_frag:$E,meshmatcap_vert:tT,meshmatcap_frag:eT,meshnormal_vert:nT,meshnormal_frag:iT,meshphong_vert:aT,meshphong_frag:rT,meshphysical_vert:sT,meshphysical_frag:oT,meshtoon_vert:lT,meshtoon_frag:uT,points_vert:cT,points_frag:fT,shadow_vert:hT,shadow_frag:dT,sprite_vert:pT,sprite_frag:mT},bt={common:{diffuse:{value:new Me(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new ce},alphaMap:{value:null},alphaMapTransform:{value:new ce},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new ce}},envmap:{envMap:{value:null},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new ce}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new ce}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new ce},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new ce},normalScale:{value:new ge(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new ce},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new ce}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new ce}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new ce}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new Me(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new Me(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new ce},alphaTest:{value:0},uvTransform:{value:new ce}},sprite:{diffuse:{value:new Me(16777215)},opacity:{value:1},center:{value:new ge(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new ce},alphaMap:{value:null},alphaMapTransform:{value:new ce},alphaTest:{value:0}}},bi={basic:{uniforms:Cn([bt.common,bt.specularmap,bt.envmap,bt.aomap,bt.lightmap,bt.fog]),vertexShader:oe.meshbasic_vert,fragmentShader:oe.meshbasic_frag},lambert:{uniforms:Cn([bt.common,bt.specularmap,bt.envmap,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.fog,bt.lights,{emissive:{value:new Me(0)}}]),vertexShader:oe.meshlambert_vert,fragmentShader:oe.meshlambert_frag},phong:{uniforms:Cn([bt.common,bt.specularmap,bt.envmap,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.fog,bt.lights,{emissive:{value:new Me(0)},specular:{value:new Me(1118481)},shininess:{value:30}}]),vertexShader:oe.meshphong_vert,fragmentShader:oe.meshphong_frag},standard:{uniforms:Cn([bt.common,bt.envmap,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.roughnessmap,bt.metalnessmap,bt.fog,bt.lights,{emissive:{value:new Me(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:oe.meshphysical_vert,fragmentShader:oe.meshphysical_frag},toon:{uniforms:Cn([bt.common,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.gradientmap,bt.fog,bt.lights,{emissive:{value:new Me(0)}}]),vertexShader:oe.meshtoon_vert,fragmentShader:oe.meshtoon_frag},matcap:{uniforms:Cn([bt.common,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.fog,{matcap:{value:null}}]),vertexShader:oe.meshmatcap_vert,fragmentShader:oe.meshmatcap_frag},points:{uniforms:Cn([bt.points,bt.fog]),vertexShader:oe.points_vert,fragmentShader:oe.points_frag},dashed:{uniforms:Cn([bt.common,bt.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:oe.linedashed_vert,fragmentShader:oe.linedashed_frag},depth:{uniforms:Cn([bt.common,bt.displacementmap]),vertexShader:oe.depth_vert,fragmentShader:oe.depth_frag},normal:{uniforms:Cn([bt.common,bt.bumpmap,bt.normalmap,bt.displacementmap,{opacity:{value:1}}]),vertexShader:oe.meshnormal_vert,fragmentShader:oe.meshnormal_frag},sprite:{uniforms:Cn([bt.sprite,bt.fog]),vertexShader:oe.sprite_vert,fragmentShader:oe.sprite_frag},background:{uniforms:{uvTransform:{value:new ce},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:oe.background_vert,fragmentShader:oe.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1}},vertexShader:oe.backgroundCube_vert,fragmentShader:oe.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:oe.cube_vert,fragmentShader:oe.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:oe.equirect_vert,fragmentShader:oe.equirect_frag},distanceRGBA:{uniforms:Cn([bt.common,bt.displacementmap,{referencePosition:{value:new Y},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:oe.distanceRGBA_vert,fragmentShader:oe.distanceRGBA_frag},shadow:{uniforms:Cn([bt.lights,bt.fog,{color:{value:new Me(0)},opacity:{value:1}}]),vertexShader:oe.shadow_vert,fragmentShader:oe.shadow_frag}};bi.physical={uniforms:Cn([bi.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new ce},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new ce},clearcoatNormalScale:{value:new ge(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new ce},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new ce},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new ce},sheen:{value:0},sheenColor:{value:new Me(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new ce},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new ce},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new ce},transmissionSamplerSize:{value:new ge},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new ce},attenuationDistance:{value:0},attenuationColor:{value:new Me(0)},specularColor:{value:new Me(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new ce},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new ce},anisotropyVector:{value:new ge},anisotropyMap:{value:null},anisotropyMapTransform:{value:new ce}}]),vertexShader:oe.meshphysical_vert,fragmentShader:oe.meshphysical_frag};const uu={r:0,b:0,g:0};function gT(o,e,i,r,l,c,d){const h=new Me(0);let m=c===!0?0:1,p,g,_=null,x=0,y=null;function b(M,v){let D=!1,T=v.isScene===!0?v.background:null;T&&T.isTexture&&(T=(v.backgroundBlurriness>0?i:e).get(T)),T===null?A(h,m):T&&T.isColor&&(A(T,1),D=!0);const z=o.xr.getEnvironmentBlendMode();z==="additive"?r.buffers.color.setClear(0,0,0,1,d):z==="alpha-blend"&&r.buffers.color.setClear(0,0,0,0,d),(o.autoClear||D)&&o.clear(o.autoClearColor,o.autoClearDepth,o.autoClearStencil),T&&(T.isCubeTexture||T.mapping===xu)?(g===void 0&&(g=new za(new No(1,1,1),new mr({name:"BackgroundCubeMaterial",uniforms:vs(bi.backgroundCube.uniforms),vertexShader:bi.backgroundCube.vertexShader,fragmentShader:bi.backgroundCube.fragmentShader,side:Fn,depthTest:!1,depthWrite:!1,fog:!1})),g.geometry.deleteAttribute("normal"),g.geometry.deleteAttribute("uv"),g.onBeforeRender=function(V,B,O){this.matrixWorld.copyPosition(O.matrixWorld)},Object.defineProperty(g.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),l.update(g)),g.material.uniforms.envMap.value=T,g.material.uniforms.flipEnvMap.value=T.isCubeTexture&&T.isRenderTargetTexture===!1?-1:1,g.material.uniforms.backgroundBlurriness.value=v.backgroundBlurriness,g.material.uniforms.backgroundIntensity.value=v.backgroundIntensity,g.material.toneMapped=Ue.getTransfer(T.colorSpace)!==Fe,(_!==T||x!==T.version||y!==o.toneMapping)&&(g.material.needsUpdate=!0,_=T,x=T.version,y=o.toneMapping),g.layers.enableAll(),M.unshift(g,g.geometry,g.material,0,0,null)):T&&T.isTexture&&(p===void 0&&(p=new za(new Nh(2,2),new mr({name:"BackgroundMaterial",uniforms:vs(bi.background.uniforms),vertexShader:bi.background.vertexShader,fragmentShader:bi.background.fragmentShader,side:Fa,depthTest:!1,depthWrite:!1,fog:!1})),p.geometry.deleteAttribute("normal"),Object.defineProperty(p.material,"map",{get:function(){return this.uniforms.t2D.value}}),l.update(p)),p.material.uniforms.t2D.value=T,p.material.uniforms.backgroundIntensity.value=v.backgroundIntensity,p.material.toneMapped=Ue.getTransfer(T.colorSpace)!==Fe,T.matrixAutoUpdate===!0&&T.updateMatrix(),p.material.uniforms.uvTransform.value.copy(T.matrix),(_!==T||x!==T.version||y!==o.toneMapping)&&(p.material.needsUpdate=!0,_=T,x=T.version,y=o.toneMapping),p.layers.enableAll(),M.unshift(p,p.geometry,p.material,0,0,null))}function A(M,v){M.getRGB(uu,Cv(o)),r.buffers.color.setClear(uu.r,uu.g,uu.b,v,d)}return{getClearColor:function(){return h},setClearColor:function(M,v=1){h.set(M),m=v,A(h,m)},getClearAlpha:function(){return m},setClearAlpha:function(M){m=M,A(h,m)},render:b}}function _T(o,e,i,r){const l=o.getParameter(o.MAX_VERTEX_ATTRIBS),c=r.isWebGL2?null:e.get("OES_vertex_array_object"),d=r.isWebGL2||c!==null,h={},m=M(null);let p=m,g=!1;function _(X,tt,P,q,J){let lt=!1;if(d){const ft=A(q,P,tt);p!==ft&&(p=ft,y(p.object)),lt=v(X,q,P,J),lt&&D(X,q,P,J)}else{const ft=tt.wireframe===!0;(p.geometry!==q.id||p.program!==P.id||p.wireframe!==ft)&&(p.geometry=q.id,p.program=P.id,p.wireframe=ft,lt=!0)}J!==null&&i.update(J,o.ELEMENT_ARRAY_BUFFER),(lt||g)&&(g=!1,ut(X,tt,P,q),J!==null&&o.bindBuffer(o.ELEMENT_ARRAY_BUFFER,i.get(J).buffer))}function x(){return r.isWebGL2?o.createVertexArray():c.createVertexArrayOES()}function y(X){return r.isWebGL2?o.bindVertexArray(X):c.bindVertexArrayOES(X)}function b(X){return r.isWebGL2?o.deleteVertexArray(X):c.deleteVertexArrayOES(X)}function A(X,tt,P){const q=P.wireframe===!0;let J=h[X.id];J===void 0&&(J={},h[X.id]=J);let lt=J[tt.id];lt===void 0&&(lt={},J[tt.id]=lt);let ft=lt[q];return ft===void 0&&(ft=M(x()),lt[q]=ft),ft}function M(X){const tt=[],P=[],q=[];for(let J=0;J<l;J++)tt[J]=0,P[J]=0,q[J]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:tt,enabledAttributes:P,attributeDivisors:q,object:X,attributes:{},index:null}}function v(X,tt,P,q){const J=p.attributes,lt=tt.attributes;let ft=0;const L=P.getAttributes();for(const W in L)if(L[W].location>=0){const K=J[W];let mt=lt[W];if(mt===void 0&&(W==="instanceMatrix"&&X.instanceMatrix&&(mt=X.instanceMatrix),W==="instanceColor"&&X.instanceColor&&(mt=X.instanceColor)),K===void 0||K.attribute!==mt||mt&&K.data!==mt.data)return!0;ft++}return p.attributesNum!==ft||p.index!==q}function D(X,tt,P,q){const J={},lt=tt.attributes;let ft=0;const L=P.getAttributes();for(const W in L)if(L[W].location>=0){let K=lt[W];K===void 0&&(W==="instanceMatrix"&&X.instanceMatrix&&(K=X.instanceMatrix),W==="instanceColor"&&X.instanceColor&&(K=X.instanceColor));const mt={};mt.attribute=K,K&&K.data&&(mt.data=K.data),J[W]=mt,ft++}p.attributes=J,p.attributesNum=ft,p.index=q}function T(){const X=p.newAttributes;for(let tt=0,P=X.length;tt<P;tt++)X[tt]=0}function z(X){V(X,0)}function V(X,tt){const P=p.newAttributes,q=p.enabledAttributes,J=p.attributeDivisors;P[X]=1,q[X]===0&&(o.enableVertexAttribArray(X),q[X]=1),J[X]!==tt&&((r.isWebGL2?o:e.get("ANGLE_instanced_arrays"))[r.isWebGL2?"vertexAttribDivisor":"vertexAttribDivisorANGLE"](X,tt),J[X]=tt)}function B(){const X=p.newAttributes,tt=p.enabledAttributes;for(let P=0,q=tt.length;P<q;P++)tt[P]!==X[P]&&(o.disableVertexAttribArray(P),tt[P]=0)}function O(X,tt,P,q,J,lt,ft){ft===!0?o.vertexAttribIPointer(X,tt,P,J,lt):o.vertexAttribPointer(X,tt,P,q,J,lt)}function ut(X,tt,P,q){if(r.isWebGL2===!1&&(X.isInstancedMesh||q.isInstancedBufferGeometry)&&e.get("ANGLE_instanced_arrays")===null)return;T();const J=q.attributes,lt=P.getAttributes(),ft=tt.defaultAttributeValues;for(const L in lt){const W=lt[L];if(W.location>=0){let G=J[L];if(G===void 0&&(L==="instanceMatrix"&&X.instanceMatrix&&(G=X.instanceMatrix),L==="instanceColor"&&X.instanceColor&&(G=X.instanceColor)),G!==void 0){const K=G.normalized,mt=G.itemSize,xt=i.get(G);if(xt===void 0)continue;const Mt=xt.buffer,It=xt.type,Nt=xt.bytesPerElement,kt=r.isWebGL2===!0&&(It===o.INT||It===o.UNSIGNED_INT||G.gpuType===uv);if(G.isInterleavedBufferAttribute){const ue=G.data,et=ue.stride,un=G.offset;if(ue.isInstancedInterleavedBuffer){for(let Ft=0;Ft<W.locationSize;Ft++)V(W.location+Ft,ue.meshPerAttribute);X.isInstancedMesh!==!0&&q._maxInstanceCount===void 0&&(q._maxInstanceCount=ue.meshPerAttribute*ue.count)}else for(let Ft=0;Ft<W.locationSize;Ft++)z(W.location+Ft);o.bindBuffer(o.ARRAY_BUFFER,Mt);for(let Ft=0;Ft<W.locationSize;Ft++)O(W.location+Ft,mt/W.locationSize,It,K,et*Nt,(un+mt/W.locationSize*Ft)*Nt,kt)}else{if(G.isInstancedBufferAttribute){for(let ue=0;ue<W.locationSize;ue++)V(W.location+ue,G.meshPerAttribute);X.isInstancedMesh!==!0&&q._maxInstanceCount===void 0&&(q._maxInstanceCount=G.meshPerAttribute*G.count)}else for(let ue=0;ue<W.locationSize;ue++)z(W.location+ue);o.bindBuffer(o.ARRAY_BUFFER,Mt);for(let ue=0;ue<W.locationSize;ue++)O(W.location+ue,mt/W.locationSize,It,K,mt*Nt,mt/W.locationSize*ue*Nt,kt)}}else if(ft!==void 0){const K=ft[L];if(K!==void 0)switch(K.length){case 2:o.vertexAttrib2fv(W.location,K);break;case 3:o.vertexAttrib3fv(W.location,K);break;case 4:o.vertexAttrib4fv(W.location,K);break;default:o.vertexAttrib1fv(W.location,K)}}}}B()}function C(){dt();for(const X in h){const tt=h[X];for(const P in tt){const q=tt[P];for(const J in q)b(q[J].object),delete q[J];delete tt[P]}delete h[X]}}function N(X){if(h[X.id]===void 0)return;const tt=h[X.id];for(const P in tt){const q=tt[P];for(const J in q)b(q[J].object),delete q[J];delete tt[P]}delete h[X.id]}function rt(X){for(const tt in h){const P=h[tt];if(P[X.id]===void 0)continue;const q=P[X.id];for(const J in q)b(q[J].object),delete q[J];delete P[X.id]}}function dt(){Et(),g=!0,p!==m&&(p=m,y(p.object))}function Et(){m.geometry=null,m.program=null,m.wireframe=!1}return{setup:_,reset:dt,resetDefaultState:Et,dispose:C,releaseStatesOfGeometry:N,releaseStatesOfProgram:rt,initAttributes:T,enableAttribute:z,disableUnusedAttributes:B}}function vT(o,e,i,r){const l=r.isWebGL2;let c;function d(g){c=g}function h(g,_){o.drawArrays(c,g,_),i.update(_,c,1)}function m(g,_,x){if(x===0)return;let y,b;if(l)y=o,b="drawArraysInstanced";else if(y=e.get("ANGLE_instanced_arrays"),b="drawArraysInstancedANGLE",y===null){console.error("THREE.WebGLBufferRenderer: using THREE.InstancedBufferGeometry but hardware does not support extension ANGLE_instanced_arrays.");return}y[b](c,g,_,x),i.update(_,c,x)}function p(g,_,x){if(x===0)return;const y=e.get("WEBGL_multi_draw");if(y===null)for(let b=0;b<x;b++)this.render(g[b],_[b]);else{y.multiDrawArraysWEBGL(c,g,0,_,0,x);let b=0;for(let A=0;A<x;A++)b+=_[A];i.update(b,c,1)}}this.setMode=d,this.render=h,this.renderInstances=m,this.renderMultiDraw=p}function ST(o,e,i){let r;function l(){if(r!==void 0)return r;if(e.has("EXT_texture_filter_anisotropic")===!0){const O=e.get("EXT_texture_filter_anisotropic");r=o.getParameter(O.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else r=0;return r}function c(O){if(O==="highp"){if(o.getShaderPrecisionFormat(o.VERTEX_SHADER,o.HIGH_FLOAT).precision>0&&o.getShaderPrecisionFormat(o.FRAGMENT_SHADER,o.HIGH_FLOAT).precision>0)return"highp";O="mediump"}return O==="mediump"&&o.getShaderPrecisionFormat(o.VERTEX_SHADER,o.MEDIUM_FLOAT).precision>0&&o.getShaderPrecisionFormat(o.FRAGMENT_SHADER,o.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}const d=typeof WebGL2RenderingContext<"u"&&o.constructor.name==="WebGL2RenderingContext";let h=i.precision!==void 0?i.precision:"highp";const m=c(h);m!==h&&(console.warn("THREE.WebGLRenderer:",h,"not supported, using",m,"instead."),h=m);const p=d||e.has("WEBGL_draw_buffers"),g=i.logarithmicDepthBuffer===!0,_=o.getParameter(o.MAX_TEXTURE_IMAGE_UNITS),x=o.getParameter(o.MAX_VERTEX_TEXTURE_IMAGE_UNITS),y=o.getParameter(o.MAX_TEXTURE_SIZE),b=o.getParameter(o.MAX_CUBE_MAP_TEXTURE_SIZE),A=o.getParameter(o.MAX_VERTEX_ATTRIBS),M=o.getParameter(o.MAX_VERTEX_UNIFORM_VECTORS),v=o.getParameter(o.MAX_VARYING_VECTORS),D=o.getParameter(o.MAX_FRAGMENT_UNIFORM_VECTORS),T=x>0,z=d||e.has("OES_texture_float"),V=T&&z,B=d?o.getParameter(o.MAX_SAMPLES):0;return{isWebGL2:d,drawBuffers:p,getMaxAnisotropy:l,getMaxPrecision:c,precision:h,logarithmicDepthBuffer:g,maxTextures:_,maxVertexTextures:x,maxTextureSize:y,maxCubemapSize:b,maxAttributes:A,maxVertexUniforms:M,maxVaryings:v,maxFragmentUniforms:D,vertexTextures:T,floatFragmentTextures:z,floatVertexTextures:V,maxSamples:B}}function xT(o){const e=this;let i=null,r=0,l=!1,c=!1;const d=new or,h=new ce,m={value:null,needsUpdate:!1};this.uniform=m,this.numPlanes=0,this.numIntersection=0,this.init=function(_,x){const y=_.length!==0||x||r!==0||l;return l=x,r=_.length,y},this.beginShadows=function(){c=!0,g(null)},this.endShadows=function(){c=!1},this.setGlobalState=function(_,x){i=g(_,x,0)},this.setState=function(_,x,y){const b=_.clippingPlanes,A=_.clipIntersection,M=_.clipShadows,v=o.get(_);if(!l||b===null||b.length===0||c&&!M)c?g(null):p();else{const D=c?0:r,T=D*4;let z=v.clippingState||null;m.value=z,z=g(b,x,T,y);for(let V=0;V!==T;++V)z[V]=i[V];v.clippingState=z,this.numIntersection=A?this.numPlanes:0,this.numPlanes+=D}};function p(){m.value!==i&&(m.value=i,m.needsUpdate=r>0),e.numPlanes=r,e.numIntersection=0}function g(_,x,y,b){const A=_!==null?_.length:0;let M=null;if(A!==0){if(M=m.value,b!==!0||M===null){const v=y+A*4,D=x.matrixWorldInverse;h.getNormalMatrix(D),(M===null||M.length<v)&&(M=new Float32Array(v));for(let T=0,z=y;T!==A;++T,z+=4)d.copy(_[T]).applyMatrix4(D,h),d.normal.toArray(M,z),M[z+3]=d.constant}m.value=M,m.needsUpdate=!0}return e.numPlanes=A,e.numIntersection=0,M}}function MT(o){let e=new WeakMap;function i(d,h){return h===xh?d.mapping=ms:h===Mh&&(d.mapping=gs),d}function r(d){if(d&&d.isTexture){const h=d.mapping;if(h===xh||h===Mh)if(e.has(d)){const m=e.get(d).texture;return i(m,d.mapping)}else{const m=d.image;if(m&&m.height>0){const p=new NM(m.height/2);return p.fromEquirectangularTexture(o,d),e.set(d,p),d.addEventListener("dispose",l),i(p.texture,d.mapping)}else return null}}return d}function l(d){const h=d.target;h.removeEventListener("dispose",l);const m=e.get(h);m!==void 0&&(e.delete(h),m.dispose())}function c(){e=new WeakMap}return{get:r,dispose:c}}class Uv extends wv{constructor(e=-1,i=1,r=1,l=-1,c=.1,d=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=i,this.top=r,this.bottom=l,this.near=c,this.far=d,this.updateProjectionMatrix()}copy(e,i){return super.copy(e,i),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,i,r,l,c,d){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=i,this.view.offsetX=r,this.view.offsetY=l,this.view.width=c,this.view.height=d,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),i=(this.top-this.bottom)/(2*this.zoom),r=(this.right+this.left)/2,l=(this.top+this.bottom)/2;let c=r-e,d=r+e,h=l+i,m=l-i;if(this.view!==null&&this.view.enabled){const p=(this.right-this.left)/this.view.fullWidth/this.zoom,g=(this.top-this.bottom)/this.view.fullHeight/this.zoom;c+=p*this.view.offsetX,d=c+p*this.view.width,h-=g*this.view.offsetY,m=h-g*this.view.height}this.projectionMatrix.makeOrthographic(c,d,h,m,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const i=super.toJSON(e);return i.object.zoom=this.zoom,i.object.left=this.left,i.object.right=this.right,i.object.top=this.top,i.object.bottom=this.bottom,i.object.near=this.near,i.object.far=this.far,this.view!==null&&(i.object.view=Object.assign({},this.view)),i}}const fs=4,D_=[.125,.215,.35,.446,.526,.582],cr=20,sh=new Uv,L_=new Me;let oh=null,lh=0,uh=0;const lr=(1+Math.sqrt(5))/2,cs=1/lr,U_=[new Y(1,1,1),new Y(-1,1,1),new Y(1,1,-1),new Y(-1,1,-1),new Y(0,lr,cs),new Y(0,lr,-cs),new Y(cs,0,lr),new Y(-cs,0,lr),new Y(lr,cs,0),new Y(-lr,cs,0)];class N_{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,i=0,r=.1,l=100){oh=this._renderer.getRenderTarget(),lh=this._renderer.getActiveCubeFace(),uh=this._renderer.getActiveMipmapLevel(),this._setSize(256);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,r,l,c),i>0&&this._blur(c,0,0,i),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,i=null){return this._fromTexture(e,i)}fromCubemap(e,i=null){return this._fromTexture(e,i)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=P_(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=z_(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(oh,lh,uh),e.scissorTest=!1,cu(e,0,0,e.width,e.height)}_fromTexture(e,i){e.mapping===ms||e.mapping===gs?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),oh=this._renderer.getRenderTarget(),lh=this._renderer.getActiveCubeFace(),uh=this._renderer.getActiveMipmapLevel();const r=i||this._allocateTargets();return this._textureToCubeUV(e,r),this._applyPMREM(r),this._cleanup(r),r}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),i=4*this._cubeSize,r={magFilter:oi,minFilter:oi,generateMipmaps:!1,type:Ro,format:Si,colorSpace:$i,depthBuffer:!1},l=O_(e,i,r);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==i){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=O_(e,i,r);const{_lodMax:c}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=yT(c)),this._blurMaterial=ET(c,e,i)}return l}_compileMaterial(e){const i=new za(this._lodPlanes[0],e);this._renderer.compile(i,sh)}_sceneToCubeUV(e,i,r,l){const h=new li(90,1,i,r),m=[1,-1,1,1,1,1],p=[1,1,1,-1,-1,-1],g=this._renderer,_=g.autoClear,x=g.toneMapping;g.getClearColor(L_),g.toneMapping=Ba,g.autoClear=!1;const y=new bv({name:"PMREM.Background",side:Fn,depthWrite:!1,depthTest:!1}),b=new za(new No,y);let A=!1;const M=e.background;M?M.isColor&&(y.color.copy(M),e.background=null,A=!0):(y.color.copy(L_),A=!0);for(let v=0;v<6;v++){const D=v%3;D===0?(h.up.set(0,m[v],0),h.lookAt(p[v],0,0)):D===1?(h.up.set(0,0,m[v]),h.lookAt(0,p[v],0)):(h.up.set(0,m[v],0),h.lookAt(0,0,p[v]));const T=this._cubeSize;cu(l,D*T,v>2?T:0,T,T),g.setRenderTarget(l),A&&g.render(b,h),g.render(e,h)}b.geometry.dispose(),b.material.dispose(),g.toneMapping=x,g.autoClear=_,e.background=M}_textureToCubeUV(e,i){const r=this._renderer,l=e.mapping===ms||e.mapping===gs;l?(this._cubemapMaterial===null&&(this._cubemapMaterial=P_()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=z_());const c=l?this._cubemapMaterial:this._equirectMaterial,d=new za(this._lodPlanes[0],c),h=c.uniforms;h.envMap.value=e;const m=this._cubeSize;cu(i,0,0,3*m,2*m),r.setRenderTarget(i),r.render(d,sh)}_applyPMREM(e){const i=this._renderer,r=i.autoClear;i.autoClear=!1;for(let l=1;l<this._lodPlanes.length;l++){const c=Math.sqrt(this._sigmas[l]*this._sigmas[l]-this._sigmas[l-1]*this._sigmas[l-1]),d=U_[(l-1)%U_.length];this._blur(e,l-1,l,c,d)}i.autoClear=r}_blur(e,i,r,l,c){const d=this._pingPongRenderTarget;this._halfBlur(e,d,i,r,l,"latitudinal",c),this._halfBlur(d,e,r,r,l,"longitudinal",c)}_halfBlur(e,i,r,l,c,d,h){const m=this._renderer,p=this._blurMaterial;d!=="latitudinal"&&d!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const g=3,_=new za(this._lodPlanes[l],p),x=p.uniforms,y=this._sizeLods[r]-1,b=isFinite(c)?Math.PI/(2*y):2*Math.PI/(2*cr-1),A=c/b,M=isFinite(c)?1+Math.floor(g*A):cr;M>cr&&console.warn(`sigmaRadians, ${c}, is too large and will clip, as it requested ${M} samples when the maximum is set to ${cr}`);const v=[];let D=0;for(let O=0;O<cr;++O){const ut=O/A,C=Math.exp(-ut*ut/2);v.push(C),O===0?D+=C:O<M&&(D+=2*C)}for(let O=0;O<v.length;O++)v[O]=v[O]/D;x.envMap.value=e.texture,x.samples.value=M,x.weights.value=v,x.latitudinal.value=d==="latitudinal",h&&(x.poleAxis.value=h);const{_lodMax:T}=this;x.dTheta.value=b,x.mipInt.value=T-r;const z=this._sizeLods[l],V=3*z*(l>T-fs?l-T+fs:0),B=4*(this._cubeSize-z);cu(i,V,B,3*z,2*z),m.setRenderTarget(i),m.render(_,sh)}}function yT(o){const e=[],i=[],r=[];let l=o;const c=o-fs+1+D_.length;for(let d=0;d<c;d++){const h=Math.pow(2,l);i.push(h);let m=1/h;d>o-fs?m=D_[d-o+fs-1]:d===0&&(m=0),r.push(m);const p=1/(h-2),g=-p,_=1+p,x=[g,g,_,g,_,_,g,g,_,_,g,_],y=6,b=6,A=3,M=2,v=1,D=new Float32Array(A*b*y),T=new Float32Array(M*b*y),z=new Float32Array(v*b*y);for(let B=0;B<y;B++){const O=B%3*2/3-1,ut=B>2?0:-1,C=[O,ut,0,O+2/3,ut,0,O+2/3,ut+1,0,O,ut,0,O+2/3,ut+1,0,O,ut+1,0];D.set(C,A*b*B),T.set(x,M*b*B);const N=[B,B,B,B,B,B];z.set(N,v*b*B)}const V=new Ri;V.setAttribute("position",new Ai(D,A)),V.setAttribute("uv",new Ai(T,M)),V.setAttribute("faceIndex",new Ai(z,v)),e.push(V),l>fs&&l--}return{lodPlanes:e,sizeLods:i,sigmas:r}}function O_(o,e,i){const r=new pr(o,e,i);return r.texture.mapping=xu,r.texture.name="PMREM.cubeUv",r.scissorTest=!0,r}function cu(o,e,i,r,l){o.viewport.set(e,i,r,l),o.scissor.set(e,i,r,l)}function ET(o,e,i){const r=new Float32Array(cr),l=new Y(0,1,0);return new mr({name:"SphericalGaussianBlur",defines:{n:cr,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/i,CUBEUV_MAX_MIP:`${o}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:r},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:l}},vertexShader:Oh(),fragmentShader:`

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
		`,blending:Pa,depthTest:!1,depthWrite:!1})}function z_(){return new mr({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:Oh(),fragmentShader:`

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
		`,blending:Pa,depthTest:!1,depthWrite:!1})}function P_(){return new mr({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:Oh(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:Pa,depthTest:!1,depthWrite:!1})}function Oh(){return`

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
	`}function TT(o){let e=new WeakMap,i=null;function r(h){if(h&&h.isTexture){const m=h.mapping,p=m===xh||m===Mh,g=m===ms||m===gs;if(p||g)if(h.isRenderTargetTexture&&h.needsPMREMUpdate===!0){h.needsPMREMUpdate=!1;let _=e.get(h);return i===null&&(i=new N_(o)),_=p?i.fromEquirectangular(h,_):i.fromCubemap(h,_),e.set(h,_),_.texture}else{if(e.has(h))return e.get(h).texture;{const _=h.image;if(p&&_&&_.height>0||g&&_&&l(_)){i===null&&(i=new N_(o));const x=p?i.fromEquirectangular(h):i.fromCubemap(h);return e.set(h,x),h.addEventListener("dispose",c),x.texture}else return null}}}return h}function l(h){let m=0;const p=6;for(let g=0;g<p;g++)h[g]!==void 0&&m++;return m===p}function c(h){const m=h.target;m.removeEventListener("dispose",c);const p=e.get(m);p!==void 0&&(e.delete(m),p.dispose())}function d(){e=new WeakMap,i!==null&&(i.dispose(),i=null)}return{get:r,dispose:d}}function bT(o){const e={};function i(r){if(e[r]!==void 0)return e[r];let l;switch(r){case"WEBGL_depth_texture":l=o.getExtension("WEBGL_depth_texture")||o.getExtension("MOZ_WEBGL_depth_texture")||o.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":l=o.getExtension("EXT_texture_filter_anisotropic")||o.getExtension("MOZ_EXT_texture_filter_anisotropic")||o.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":l=o.getExtension("WEBGL_compressed_texture_s3tc")||o.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||o.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":l=o.getExtension("WEBGL_compressed_texture_pvrtc")||o.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:l=o.getExtension(r)}return e[r]=l,l}return{has:function(r){return i(r)!==null},init:function(r){r.isWebGL2?(i("EXT_color_buffer_float"),i("WEBGL_clip_cull_distance")):(i("WEBGL_depth_texture"),i("OES_texture_float"),i("OES_texture_half_float"),i("OES_texture_half_float_linear"),i("OES_standard_derivatives"),i("OES_element_index_uint"),i("OES_vertex_array_object"),i("ANGLE_instanced_arrays")),i("OES_texture_float_linear"),i("EXT_color_buffer_half_float"),i("WEBGL_multisampled_render_to_texture")},get:function(r){const l=i(r);return l===null&&console.warn("THREE.WebGLRenderer: "+r+" extension not supported."),l}}}function AT(o,e,i,r){const l={},c=new WeakMap;function d(_){const x=_.target;x.index!==null&&e.remove(x.index);for(const b in x.attributes)e.remove(x.attributes[b]);for(const b in x.morphAttributes){const A=x.morphAttributes[b];for(let M=0,v=A.length;M<v;M++)e.remove(A[M])}x.removeEventListener("dispose",d),delete l[x.id];const y=c.get(x);y&&(e.remove(y),c.delete(x)),r.releaseStatesOfGeometry(x),x.isInstancedBufferGeometry===!0&&delete x._maxInstanceCount,i.memory.geometries--}function h(_,x){return l[x.id]===!0||(x.addEventListener("dispose",d),l[x.id]=!0,i.memory.geometries++),x}function m(_){const x=_.attributes;for(const b in x)e.update(x[b],o.ARRAY_BUFFER);const y=_.morphAttributes;for(const b in y){const A=y[b];for(let M=0,v=A.length;M<v;M++)e.update(A[M],o.ARRAY_BUFFER)}}function p(_){const x=[],y=_.index,b=_.attributes.position;let A=0;if(y!==null){const D=y.array;A=y.version;for(let T=0,z=D.length;T<z;T+=3){const V=D[T+0],B=D[T+1],O=D[T+2];x.push(V,B,B,O,O,V)}}else if(b!==void 0){const D=b.array;A=b.version;for(let T=0,z=D.length/3-1;T<z;T+=3){const V=T+0,B=T+1,O=T+2;x.push(V,B,B,O,O,V)}}else return;const M=new(Sv(x)?Rv:Av)(x,1);M.version=A;const v=c.get(_);v&&e.remove(v),c.set(_,M)}function g(_){const x=c.get(_);if(x){const y=_.index;y!==null&&x.version<y.version&&p(_)}else p(_);return c.get(_)}return{get:h,update:m,getWireframeAttribute:g}}function RT(o,e,i,r){const l=r.isWebGL2;let c;function d(y){c=y}let h,m;function p(y){h=y.type,m=y.bytesPerElement}function g(y,b){o.drawElements(c,b,h,y*m),i.update(b,c,1)}function _(y,b,A){if(A===0)return;let M,v;if(l)M=o,v="drawElementsInstanced";else if(M=e.get("ANGLE_instanced_arrays"),v="drawElementsInstancedANGLE",M===null){console.error("THREE.WebGLIndexedBufferRenderer: using THREE.InstancedBufferGeometry but hardware does not support extension ANGLE_instanced_arrays.");return}M[v](c,b,h,y*m,A),i.update(b,c,A)}function x(y,b,A){if(A===0)return;const M=e.get("WEBGL_multi_draw");if(M===null)for(let v=0;v<A;v++)this.render(y[v]/m,b[v]);else{M.multiDrawElementsWEBGL(c,b,0,h,y,0,A);let v=0;for(let D=0;D<A;D++)v+=b[D];i.update(v,c,1)}}this.setMode=d,this.setIndex=p,this.render=g,this.renderInstances=_,this.renderMultiDraw=x}function CT(o){const e={geometries:0,textures:0},i={frame:0,calls:0,triangles:0,points:0,lines:0};function r(c,d,h){switch(i.calls++,d){case o.TRIANGLES:i.triangles+=h*(c/3);break;case o.LINES:i.lines+=h*(c/2);break;case o.LINE_STRIP:i.lines+=h*(c-1);break;case o.LINE_LOOP:i.lines+=h*c;break;case o.POINTS:i.points+=h*c;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",d);break}}function l(){i.calls=0,i.triangles=0,i.points=0,i.lines=0}return{memory:e,render:i,programs:null,autoReset:!0,reset:l,update:r}}function wT(o,e){return o[0]-e[0]}function DT(o,e){return Math.abs(e[1])-Math.abs(o[1])}function LT(o,e,i){const r={},l=new Float32Array(8),c=new WeakMap,d=new Ve,h=[];for(let p=0;p<8;p++)h[p]=[p,0];function m(p,g,_){const x=p.morphTargetInfluences;if(e.isWebGL2===!0){const y=g.morphAttributes.position||g.morphAttributes.normal||g.morphAttributes.color,b=y!==void 0?y.length:0;let A=c.get(g);if(A===void 0||A.count!==b){let X=function(){dt.dispose(),c.delete(g),g.removeEventListener("dispose",X)};A!==void 0&&A.texture.dispose();const D=g.morphAttributes.position!==void 0,T=g.morphAttributes.normal!==void 0,z=g.morphAttributes.color!==void 0,V=g.morphAttributes.position||[],B=g.morphAttributes.normal||[],O=g.morphAttributes.color||[];let ut=0;D===!0&&(ut=1),T===!0&&(ut=2),z===!0&&(ut=3);let C=g.attributes.position.count*ut,N=1;C>e.maxTextureSize&&(N=Math.ceil(C/e.maxTextureSize),C=e.maxTextureSize);const rt=new Float32Array(C*N*4*b),dt=new yv(rt,C,N,b);dt.type=Oa,dt.needsUpdate=!0;const Et=ut*4;for(let tt=0;tt<b;tt++){const P=V[tt],q=B[tt],J=O[tt],lt=C*N*4*tt;for(let ft=0;ft<P.count;ft++){const L=ft*Et;D===!0&&(d.fromBufferAttribute(P,ft),rt[lt+L+0]=d.x,rt[lt+L+1]=d.y,rt[lt+L+2]=d.z,rt[lt+L+3]=0),T===!0&&(d.fromBufferAttribute(q,ft),rt[lt+L+4]=d.x,rt[lt+L+5]=d.y,rt[lt+L+6]=d.z,rt[lt+L+7]=0),z===!0&&(d.fromBufferAttribute(J,ft),rt[lt+L+8]=d.x,rt[lt+L+9]=d.y,rt[lt+L+10]=d.z,rt[lt+L+11]=J.itemSize===4?d.w:1)}}A={count:b,texture:dt,size:new ge(C,N)},c.set(g,A),g.addEventListener("dispose",X)}let M=0;for(let D=0;D<x.length;D++)M+=x[D];const v=g.morphTargetsRelative?1:1-M;_.getUniforms().setValue(o,"morphTargetBaseInfluence",v),_.getUniforms().setValue(o,"morphTargetInfluences",x),_.getUniforms().setValue(o,"morphTargetsTexture",A.texture,i),_.getUniforms().setValue(o,"morphTargetsTextureSize",A.size)}else{const y=x===void 0?0:x.length;let b=r[g.id];if(b===void 0||b.length!==y){b=[];for(let T=0;T<y;T++)b[T]=[T,0];r[g.id]=b}for(let T=0;T<y;T++){const z=b[T];z[0]=T,z[1]=x[T]}b.sort(DT);for(let T=0;T<8;T++)T<y&&b[T][1]?(h[T][0]=b[T][0],h[T][1]=b[T][1]):(h[T][0]=Number.MAX_SAFE_INTEGER,h[T][1]=0);h.sort(wT);const A=g.morphAttributes.position,M=g.morphAttributes.normal;let v=0;for(let T=0;T<8;T++){const z=h[T],V=z[0],B=z[1];V!==Number.MAX_SAFE_INTEGER&&B?(A&&g.getAttribute("morphTarget"+T)!==A[V]&&g.setAttribute("morphTarget"+T,A[V]),M&&g.getAttribute("morphNormal"+T)!==M[V]&&g.setAttribute("morphNormal"+T,M[V]),l[T]=B,v+=B):(A&&g.hasAttribute("morphTarget"+T)===!0&&g.deleteAttribute("morphTarget"+T),M&&g.hasAttribute("morphNormal"+T)===!0&&g.deleteAttribute("morphNormal"+T),l[T]=0)}const D=g.morphTargetsRelative?1:1-v;_.getUniforms().setValue(o,"morphTargetBaseInfluence",D),_.getUniforms().setValue(o,"morphTargetInfluences",l)}}return{update:m}}function UT(o,e,i,r){let l=new WeakMap;function c(m){const p=r.render.frame,g=m.geometry,_=e.get(m,g);if(l.get(_)!==p&&(e.update(_),l.set(_,p)),m.isInstancedMesh&&(m.hasEventListener("dispose",h)===!1&&m.addEventListener("dispose",h),l.get(m)!==p&&(i.update(m.instanceMatrix,o.ARRAY_BUFFER),m.instanceColor!==null&&i.update(m.instanceColor,o.ARRAY_BUFFER),l.set(m,p))),m.isSkinnedMesh){const x=m.skeleton;l.get(x)!==p&&(x.update(),l.set(x,p))}return _}function d(){l=new WeakMap}function h(m){const p=m.target;p.removeEventListener("dispose",h),i.remove(p.instanceMatrix),p.instanceColor!==null&&i.remove(p.instanceColor)}return{update:c,dispose:d}}class Nv extends Kn{constructor(e,i,r,l,c,d,h,m,p,g){if(g=g!==void 0?g:hr,g!==hr&&g!==_s)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");r===void 0&&g===hr&&(r=Na),r===void 0&&g===_s&&(r=fr),super(null,l,c,d,h,m,g,r,p),this.isDepthTexture=!0,this.image={width:e,height:i},this.magFilter=h!==void 0?h:wn,this.minFilter=m!==void 0?m:wn,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.compareFunction=e.compareFunction,this}toJSON(e){const i=super.toJSON(e);return this.compareFunction!==null&&(i.compareFunction=this.compareFunction),i}}const Ov=new Kn,zv=new Nv(1,1);zv.compareFunction=vv;const Pv=new yv,Bv=new mM,Iv=new Dv,B_=[],I_=[],F_=new Float32Array(16),H_=new Float32Array(9),G_=new Float32Array(4);function xs(o,e,i){const r=o[0];if(r<=0||r>0)return o;const l=e*i;let c=B_[l];if(c===void 0&&(c=new Float32Array(l),B_[l]=c),e!==0){r.toArray(c,0);for(let d=1,h=0;d!==e;++d)h+=i,o[d].toArray(c,h)}return c}function on(o,e){if(o.length!==e.length)return!1;for(let i=0,r=o.length;i<r;i++)if(o[i]!==e[i])return!1;return!0}function ln(o,e){for(let i=0,r=e.length;i<r;i++)o[i]=e[i]}function Eu(o,e){let i=I_[e];i===void 0&&(i=new Int32Array(e),I_[e]=i);for(let r=0;r!==e;++r)i[r]=o.allocateTextureUnit();return i}function NT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1f(this.addr,e),i[0]=e)}function OT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2f(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(on(i,e))return;o.uniform2fv(this.addr,e),ln(i,e)}}function zT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3f(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else if(e.r!==void 0)(i[0]!==e.r||i[1]!==e.g||i[2]!==e.b)&&(o.uniform3f(this.addr,e.r,e.g,e.b),i[0]=e.r,i[1]=e.g,i[2]=e.b);else{if(on(i,e))return;o.uniform3fv(this.addr,e),ln(i,e)}}function PT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4f(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(on(i,e))return;o.uniform4fv(this.addr,e),ln(i,e)}}function BT(o,e){const i=this.cache,r=e.elements;if(r===void 0){if(on(i,e))return;o.uniformMatrix2fv(this.addr,!1,e),ln(i,e)}else{if(on(i,r))return;G_.set(r),o.uniformMatrix2fv(this.addr,!1,G_),ln(i,r)}}function IT(o,e){const i=this.cache,r=e.elements;if(r===void 0){if(on(i,e))return;o.uniformMatrix3fv(this.addr,!1,e),ln(i,e)}else{if(on(i,r))return;H_.set(r),o.uniformMatrix3fv(this.addr,!1,H_),ln(i,r)}}function FT(o,e){const i=this.cache,r=e.elements;if(r===void 0){if(on(i,e))return;o.uniformMatrix4fv(this.addr,!1,e),ln(i,e)}else{if(on(i,r))return;F_.set(r),o.uniformMatrix4fv(this.addr,!1,F_),ln(i,r)}}function HT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1i(this.addr,e),i[0]=e)}function GT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2i(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(on(i,e))return;o.uniform2iv(this.addr,e),ln(i,e)}}function VT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3i(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else{if(on(i,e))return;o.uniform3iv(this.addr,e),ln(i,e)}}function XT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4i(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(on(i,e))return;o.uniform4iv(this.addr,e),ln(i,e)}}function WT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1ui(this.addr,e),i[0]=e)}function kT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2ui(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(on(i,e))return;o.uniform2uiv(this.addr,e),ln(i,e)}}function qT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3ui(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else{if(on(i,e))return;o.uniform3uiv(this.addr,e),ln(i,e)}}function YT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4ui(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(on(i,e))return;o.uniform4uiv(this.addr,e),ln(i,e)}}function jT(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l);const c=this.type===o.SAMPLER_2D_SHADOW?zv:Ov;i.setTexture2D(e||c,l)}function ZT(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l),i.setTexture3D(e||Bv,l)}function KT(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l),i.setTextureCube(e||Iv,l)}function QT(o,e,i){const r=this.cache,l=i.allocateTextureUnit();r[0]!==l&&(o.uniform1i(this.addr,l),r[0]=l),i.setTexture2DArray(e||Pv,l)}function JT(o){switch(o){case 5126:return NT;case 35664:return OT;case 35665:return zT;case 35666:return PT;case 35674:return BT;case 35675:return IT;case 35676:return FT;case 5124:case 35670:return HT;case 35667:case 35671:return GT;case 35668:case 35672:return VT;case 35669:case 35673:return XT;case 5125:return WT;case 36294:return kT;case 36295:return qT;case 36296:return YT;case 35678:case 36198:case 36298:case 36306:case 35682:return jT;case 35679:case 36299:case 36307:return ZT;case 35680:case 36300:case 36308:case 36293:return KT;case 36289:case 36303:case 36311:case 36292:return QT}}function $T(o,e){o.uniform1fv(this.addr,e)}function tb(o,e){const i=xs(e,this.size,2);o.uniform2fv(this.addr,i)}function eb(o,e){const i=xs(e,this.size,3);o.uniform3fv(this.addr,i)}function nb(o,e){const i=xs(e,this.size,4);o.uniform4fv(this.addr,i)}function ib(o,e){const i=xs(e,this.size,4);o.uniformMatrix2fv(this.addr,!1,i)}function ab(o,e){const i=xs(e,this.size,9);o.uniformMatrix3fv(this.addr,!1,i)}function rb(o,e){const i=xs(e,this.size,16);o.uniformMatrix4fv(this.addr,!1,i)}function sb(o,e){o.uniform1iv(this.addr,e)}function ob(o,e){o.uniform2iv(this.addr,e)}function lb(o,e){o.uniform3iv(this.addr,e)}function ub(o,e){o.uniform4iv(this.addr,e)}function cb(o,e){o.uniform1uiv(this.addr,e)}function fb(o,e){o.uniform2uiv(this.addr,e)}function hb(o,e){o.uniform3uiv(this.addr,e)}function db(o,e){o.uniform4uiv(this.addr,e)}function pb(o,e,i){const r=this.cache,l=e.length,c=Eu(i,l);on(r,c)||(o.uniform1iv(this.addr,c),ln(r,c));for(let d=0;d!==l;++d)i.setTexture2D(e[d]||Ov,c[d])}function mb(o,e,i){const r=this.cache,l=e.length,c=Eu(i,l);on(r,c)||(o.uniform1iv(this.addr,c),ln(r,c));for(let d=0;d!==l;++d)i.setTexture3D(e[d]||Bv,c[d])}function gb(o,e,i){const r=this.cache,l=e.length,c=Eu(i,l);on(r,c)||(o.uniform1iv(this.addr,c),ln(r,c));for(let d=0;d!==l;++d)i.setTextureCube(e[d]||Iv,c[d])}function _b(o,e,i){const r=this.cache,l=e.length,c=Eu(i,l);on(r,c)||(o.uniform1iv(this.addr,c),ln(r,c));for(let d=0;d!==l;++d)i.setTexture2DArray(e[d]||Pv,c[d])}function vb(o){switch(o){case 5126:return $T;case 35664:return tb;case 35665:return eb;case 35666:return nb;case 35674:return ib;case 35675:return ab;case 35676:return rb;case 5124:case 35670:return sb;case 35667:case 35671:return ob;case 35668:case 35672:return lb;case 35669:case 35673:return ub;case 5125:return cb;case 36294:return fb;case 36295:return hb;case 36296:return db;case 35678:case 36198:case 36298:case 36306:case 35682:return pb;case 35679:case 36299:case 36307:return mb;case 35680:case 36300:case 36308:case 36293:return gb;case 36289:case 36303:case 36311:case 36292:return _b}}class Sb{constructor(e,i,r){this.id=e,this.addr=r,this.cache=[],this.type=i.type,this.setValue=JT(i.type)}}class xb{constructor(e,i,r){this.id=e,this.addr=r,this.cache=[],this.type=i.type,this.size=i.size,this.setValue=vb(i.type)}}class Mb{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,i,r){const l=this.seq;for(let c=0,d=l.length;c!==d;++c){const h=l[c];h.setValue(e,i[h.id],r)}}}const ch=/(\w+)(\])?(\[|\.)?/g;function V_(o,e){o.seq.push(e),o.map[e.id]=e}function yb(o,e,i){const r=o.name,l=r.length;for(ch.lastIndex=0;;){const c=ch.exec(r),d=ch.lastIndex;let h=c[1];const m=c[2]==="]",p=c[3];if(m&&(h=h|0),p===void 0||p==="["&&d+2===l){V_(i,p===void 0?new Sb(h,o,e):new xb(h,o,e));break}else{let _=i.map[h];_===void 0&&(_=new Mb(h),V_(i,_)),i=_}}}class du{constructor(e,i){this.seq=[],this.map={};const r=e.getProgramParameter(i,e.ACTIVE_UNIFORMS);for(let l=0;l<r;++l){const c=e.getActiveUniform(i,l),d=e.getUniformLocation(i,c.name);yb(c,d,this)}}setValue(e,i,r,l){const c=this.map[i];c!==void 0&&c.setValue(e,r,l)}setOptional(e,i,r){const l=i[r];l!==void 0&&this.setValue(e,r,l)}static upload(e,i,r,l){for(let c=0,d=i.length;c!==d;++c){const h=i[c],m=r[h.id];m.needsUpdate!==!1&&h.setValue(e,m.value,l)}}static seqWithValue(e,i){const r=[];for(let l=0,c=e.length;l!==c;++l){const d=e[l];d.id in i&&r.push(d)}return r}}function X_(o,e,i){const r=o.createShader(e);return o.shaderSource(r,i),o.compileShader(r),r}const Eb=37297;let Tb=0;function bb(o,e){const i=o.split(`
`),r=[],l=Math.max(e-6,0),c=Math.min(e+6,i.length);for(let d=l;d<c;d++){const h=d+1;r.push(`${h===e?">":" "} ${h}: ${i[d]}`)}return r.join(`
`)}function Ab(o){const e=Ue.getPrimaries(Ue.workingColorSpace),i=Ue.getPrimaries(o);let r;switch(e===i?r="":e===_u&&i===gu?r="LinearDisplayP3ToLinearSRGB":e===gu&&i===_u&&(r="LinearSRGBToLinearDisplayP3"),o){case $i:case Mu:return[r,"LinearTransferOETF"];case vn:case Dh:return[r,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space:",o),[r,"LinearTransferOETF"]}}function W_(o,e,i){const r=o.getShaderParameter(e,o.COMPILE_STATUS),l=o.getShaderInfoLog(e).trim();if(r&&l==="")return"";const c=/ERROR: 0:(\d+)/.exec(l);if(c){const d=parseInt(c[1]);return i.toUpperCase()+`

`+l+`

`+bb(o.getShaderSource(e),d)}else return l}function Rb(o,e){const i=Ab(e);return`vec4 ${o}( vec4 value ) { return ${i[0]}( ${i[1]}( value ) ); }`}function Cb(o,e){let i;switch(e){case Ix:i="Linear";break;case Fx:i="Reinhard";break;case Hx:i="OptimizedCineon";break;case Gx:i="ACESFilmic";break;case Xx:i="AgX";break;case Vx:i="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),i="Linear"}return"vec3 "+o+"( vec3 color ) { return "+i+"ToneMapping( color ); }"}function wb(o){return[o.extensionDerivatives||o.envMapCubeUVHeight||o.bumpMap||o.normalMapTangentSpace||o.clearcoatNormalMap||o.flatShading||o.shaderID==="physical"?"#extension GL_OES_standard_derivatives : enable":"",(o.extensionFragDepth||o.logarithmicDepthBuffer)&&o.rendererExtensionFragDepth?"#extension GL_EXT_frag_depth : enable":"",o.extensionDrawBuffers&&o.rendererExtensionDrawBuffers?"#extension GL_EXT_draw_buffers : require":"",(o.extensionShaderTextureLOD||o.envMap||o.transmission)&&o.rendererExtensionShaderTextureLod?"#extension GL_EXT_shader_texture_lod : enable":""].filter(hs).join(`
`)}function Db(o){return[o.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":""].filter(hs).join(`
`)}function Lb(o){const e=[];for(const i in o){const r=o[i];r!==!1&&e.push("#define "+i+" "+r)}return e.join(`
`)}function Ub(o,e){const i={},r=o.getProgramParameter(e,o.ACTIVE_ATTRIBUTES);for(let l=0;l<r;l++){const c=o.getActiveAttrib(e,l),d=c.name;let h=1;c.type===o.FLOAT_MAT2&&(h=2),c.type===o.FLOAT_MAT3&&(h=3),c.type===o.FLOAT_MAT4&&(h=4),i[d]={type:c.type,location:o.getAttribLocation(e,d),locationSize:h}}return i}function hs(o){return o!==""}function k_(o,e){const i=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return o.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,i).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function q_(o,e){return o.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Nb=/^[ \t]*#include +<([\w\d./]+)>/gm;function Rh(o){return o.replace(Nb,zb)}const Ob=new Map([["encodings_fragment","colorspace_fragment"],["encodings_pars_fragment","colorspace_pars_fragment"],["output_fragment","opaque_fragment"]]);function zb(o,e){let i=oe[e];if(i===void 0){const r=Ob.get(e);if(r!==void 0)i=oe[r],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,r);else throw new Error("Can not resolve #include <"+e+">")}return Rh(i)}const Pb=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function Y_(o){return o.replace(Pb,Bb)}function Bb(o,e,i,r){let l="";for(let c=parseInt(e);c<parseInt(i);c++)l+=r.replace(/\[\s*i\s*\]/g,"[ "+c+" ]").replace(/UNROLLED_LOOP_INDEX/g,c);return l}function j_(o){let e="precision "+o.precision+` float;
precision `+o.precision+" int;";return o.precision==="highp"?e+=`
#define HIGH_PRECISION`:o.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:o.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}function Ib(o){let e="SHADOWMAP_TYPE_BASIC";return o.shadowMapType===sv?e="SHADOWMAP_TYPE_PCF":o.shadowMapType===hx?e="SHADOWMAP_TYPE_PCF_SOFT":o.shadowMapType===Ki&&(e="SHADOWMAP_TYPE_VSM"),e}function Fb(o){let e="ENVMAP_TYPE_CUBE";if(o.envMap)switch(o.envMapMode){case ms:case gs:e="ENVMAP_TYPE_CUBE";break;case xu:e="ENVMAP_TYPE_CUBE_UV";break}return e}function Hb(o){let e="ENVMAP_MODE_REFLECTION";return o.envMap&&o.envMapMode===gs&&(e="ENVMAP_MODE_REFRACTION"),e}function Gb(o){let e="ENVMAP_BLENDING_NONE";if(o.envMap)switch(o.combine){case ov:e="ENVMAP_BLENDING_MULTIPLY";break;case Px:e="ENVMAP_BLENDING_MIX";break;case Bx:e="ENVMAP_BLENDING_ADD";break}return e}function Vb(o){const e=o.envMapCubeUVHeight;if(e===null)return null;const i=Math.log2(e)-2,r=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,i),112)),texelHeight:r,maxMip:i}}function Xb(o,e,i,r){const l=o.getContext(),c=i.defines;let d=i.vertexShader,h=i.fragmentShader;const m=Ib(i),p=Fb(i),g=Hb(i),_=Gb(i),x=Vb(i),y=i.isWebGL2?"":wb(i),b=Db(i),A=Lb(c),M=l.createProgram();let v,D,T=i.glslVersion?"#version "+i.glslVersion+`
`:"";i.isRawShaderMaterial?(v=["#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A].filter(hs).join(`
`),v.length>0&&(v+=`
`),D=[y,"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A].filter(hs).join(`
`),D.length>0&&(D+=`
`)):(v=[j_(i),"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A,i.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",i.batching?"#define USE_BATCHING":"",i.instancing?"#define USE_INSTANCING":"",i.instancingColor?"#define USE_INSTANCING_COLOR":"",i.useFog&&i.fog?"#define USE_FOG":"",i.useFog&&i.fogExp2?"#define FOG_EXP2":"",i.map?"#define USE_MAP":"",i.envMap?"#define USE_ENVMAP":"",i.envMap?"#define "+g:"",i.lightMap?"#define USE_LIGHTMAP":"",i.aoMap?"#define USE_AOMAP":"",i.bumpMap?"#define USE_BUMPMAP":"",i.normalMap?"#define USE_NORMALMAP":"",i.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",i.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",i.displacementMap?"#define USE_DISPLACEMENTMAP":"",i.emissiveMap?"#define USE_EMISSIVEMAP":"",i.anisotropy?"#define USE_ANISOTROPY":"",i.anisotropyMap?"#define USE_ANISOTROPYMAP":"",i.clearcoatMap?"#define USE_CLEARCOATMAP":"",i.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",i.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",i.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",i.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",i.specularMap?"#define USE_SPECULARMAP":"",i.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",i.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",i.roughnessMap?"#define USE_ROUGHNESSMAP":"",i.metalnessMap?"#define USE_METALNESSMAP":"",i.alphaMap?"#define USE_ALPHAMAP":"",i.alphaHash?"#define USE_ALPHAHASH":"",i.transmission?"#define USE_TRANSMISSION":"",i.transmissionMap?"#define USE_TRANSMISSIONMAP":"",i.thicknessMap?"#define USE_THICKNESSMAP":"",i.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",i.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",i.mapUv?"#define MAP_UV "+i.mapUv:"",i.alphaMapUv?"#define ALPHAMAP_UV "+i.alphaMapUv:"",i.lightMapUv?"#define LIGHTMAP_UV "+i.lightMapUv:"",i.aoMapUv?"#define AOMAP_UV "+i.aoMapUv:"",i.emissiveMapUv?"#define EMISSIVEMAP_UV "+i.emissiveMapUv:"",i.bumpMapUv?"#define BUMPMAP_UV "+i.bumpMapUv:"",i.normalMapUv?"#define NORMALMAP_UV "+i.normalMapUv:"",i.displacementMapUv?"#define DISPLACEMENTMAP_UV "+i.displacementMapUv:"",i.metalnessMapUv?"#define METALNESSMAP_UV "+i.metalnessMapUv:"",i.roughnessMapUv?"#define ROUGHNESSMAP_UV "+i.roughnessMapUv:"",i.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+i.anisotropyMapUv:"",i.clearcoatMapUv?"#define CLEARCOATMAP_UV "+i.clearcoatMapUv:"",i.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+i.clearcoatNormalMapUv:"",i.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+i.clearcoatRoughnessMapUv:"",i.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+i.iridescenceMapUv:"",i.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+i.iridescenceThicknessMapUv:"",i.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+i.sheenColorMapUv:"",i.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+i.sheenRoughnessMapUv:"",i.specularMapUv?"#define SPECULARMAP_UV "+i.specularMapUv:"",i.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+i.specularColorMapUv:"",i.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+i.specularIntensityMapUv:"",i.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+i.transmissionMapUv:"",i.thicknessMapUv?"#define THICKNESSMAP_UV "+i.thicknessMapUv:"",i.vertexTangents&&i.flatShading===!1?"#define USE_TANGENT":"",i.vertexColors?"#define USE_COLOR":"",i.vertexAlphas?"#define USE_COLOR_ALPHA":"",i.vertexUv1s?"#define USE_UV1":"",i.vertexUv2s?"#define USE_UV2":"",i.vertexUv3s?"#define USE_UV3":"",i.pointsUvs?"#define USE_POINTS_UV":"",i.flatShading?"#define FLAT_SHADED":"",i.skinning?"#define USE_SKINNING":"",i.morphTargets?"#define USE_MORPHTARGETS":"",i.morphNormals&&i.flatShading===!1?"#define USE_MORPHNORMALS":"",i.morphColors&&i.isWebGL2?"#define USE_MORPHCOLORS":"",i.morphTargetsCount>0&&i.isWebGL2?"#define MORPHTARGETS_TEXTURE":"",i.morphTargetsCount>0&&i.isWebGL2?"#define MORPHTARGETS_TEXTURE_STRIDE "+i.morphTextureStride:"",i.morphTargetsCount>0&&i.isWebGL2?"#define MORPHTARGETS_COUNT "+i.morphTargetsCount:"",i.doubleSided?"#define DOUBLE_SIDED":"",i.flipSided?"#define FLIP_SIDED":"",i.shadowMapEnabled?"#define USE_SHADOWMAP":"",i.shadowMapEnabled?"#define "+m:"",i.sizeAttenuation?"#define USE_SIZEATTENUATION":"",i.numLightProbes>0?"#define USE_LIGHT_PROBES":"",i.useLegacyLights?"#define LEGACY_LIGHTS":"",i.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",i.logarithmicDepthBuffer&&i.rendererExtensionFragDepth?"#define USE_LOGDEPTHBUF_EXT":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#if ( defined( USE_MORPHTARGETS ) && ! defined( MORPHTARGETS_TEXTURE ) )","	attribute vec3 morphTarget0;","	attribute vec3 morphTarget1;","	attribute vec3 morphTarget2;","	attribute vec3 morphTarget3;","	#ifdef USE_MORPHNORMALS","		attribute vec3 morphNormal0;","		attribute vec3 morphNormal1;","		attribute vec3 morphNormal2;","		attribute vec3 morphNormal3;","	#else","		attribute vec3 morphTarget4;","		attribute vec3 morphTarget5;","		attribute vec3 morphTarget6;","		attribute vec3 morphTarget7;","	#endif","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(hs).join(`
`),D=[y,j_(i),"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,A,i.useFog&&i.fog?"#define USE_FOG":"",i.useFog&&i.fogExp2?"#define FOG_EXP2":"",i.map?"#define USE_MAP":"",i.matcap?"#define USE_MATCAP":"",i.envMap?"#define USE_ENVMAP":"",i.envMap?"#define "+p:"",i.envMap?"#define "+g:"",i.envMap?"#define "+_:"",x?"#define CUBEUV_TEXEL_WIDTH "+x.texelWidth:"",x?"#define CUBEUV_TEXEL_HEIGHT "+x.texelHeight:"",x?"#define CUBEUV_MAX_MIP "+x.maxMip+".0":"",i.lightMap?"#define USE_LIGHTMAP":"",i.aoMap?"#define USE_AOMAP":"",i.bumpMap?"#define USE_BUMPMAP":"",i.normalMap?"#define USE_NORMALMAP":"",i.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",i.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",i.emissiveMap?"#define USE_EMISSIVEMAP":"",i.anisotropy?"#define USE_ANISOTROPY":"",i.anisotropyMap?"#define USE_ANISOTROPYMAP":"",i.clearcoat?"#define USE_CLEARCOAT":"",i.clearcoatMap?"#define USE_CLEARCOATMAP":"",i.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",i.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",i.iridescence?"#define USE_IRIDESCENCE":"",i.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",i.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",i.specularMap?"#define USE_SPECULARMAP":"",i.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",i.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",i.roughnessMap?"#define USE_ROUGHNESSMAP":"",i.metalnessMap?"#define USE_METALNESSMAP":"",i.alphaMap?"#define USE_ALPHAMAP":"",i.alphaTest?"#define USE_ALPHATEST":"",i.alphaHash?"#define USE_ALPHAHASH":"",i.sheen?"#define USE_SHEEN":"",i.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",i.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",i.transmission?"#define USE_TRANSMISSION":"",i.transmissionMap?"#define USE_TRANSMISSIONMAP":"",i.thicknessMap?"#define USE_THICKNESSMAP":"",i.vertexTangents&&i.flatShading===!1?"#define USE_TANGENT":"",i.vertexColors||i.instancingColor?"#define USE_COLOR":"",i.vertexAlphas?"#define USE_COLOR_ALPHA":"",i.vertexUv1s?"#define USE_UV1":"",i.vertexUv2s?"#define USE_UV2":"",i.vertexUv3s?"#define USE_UV3":"",i.pointsUvs?"#define USE_POINTS_UV":"",i.gradientMap?"#define USE_GRADIENTMAP":"",i.flatShading?"#define FLAT_SHADED":"",i.doubleSided?"#define DOUBLE_SIDED":"",i.flipSided?"#define FLIP_SIDED":"",i.shadowMapEnabled?"#define USE_SHADOWMAP":"",i.shadowMapEnabled?"#define "+m:"",i.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",i.numLightProbes>0?"#define USE_LIGHT_PROBES":"",i.useLegacyLights?"#define LEGACY_LIGHTS":"",i.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",i.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",i.logarithmicDepthBuffer&&i.rendererExtensionFragDepth?"#define USE_LOGDEPTHBUF_EXT":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",i.toneMapping!==Ba?"#define TONE_MAPPING":"",i.toneMapping!==Ba?oe.tonemapping_pars_fragment:"",i.toneMapping!==Ba?Cb("toneMapping",i.toneMapping):"",i.dithering?"#define DITHERING":"",i.opaque?"#define OPAQUE":"",oe.colorspace_pars_fragment,Rb("linearToOutputTexel",i.outputColorSpace),i.useDepthPacking?"#define DEPTH_PACKING "+i.depthPacking:"",`
`].filter(hs).join(`
`)),d=Rh(d),d=k_(d,i),d=q_(d,i),h=Rh(h),h=k_(h,i),h=q_(h,i),d=Y_(d),h=Y_(h),i.isWebGL2&&i.isRawShaderMaterial!==!0&&(T=`#version 300 es
`,v=[b,"precision mediump sampler2DArray;","#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+v,D=["precision mediump sampler2DArray;","#define varying in",i.glslVersion===h_?"":"layout(location = 0) out highp vec4 pc_fragColor;",i.glslVersion===h_?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+D);const z=T+v+d,V=T+D+h,B=X_(l,l.VERTEX_SHADER,z),O=X_(l,l.FRAGMENT_SHADER,V);l.attachShader(M,B),l.attachShader(M,O),i.index0AttributeName!==void 0?l.bindAttribLocation(M,0,i.index0AttributeName):i.morphTargets===!0&&l.bindAttribLocation(M,0,"position"),l.linkProgram(M);function ut(dt){if(o.debug.checkShaderErrors){const Et=l.getProgramInfoLog(M).trim(),X=l.getShaderInfoLog(B).trim(),tt=l.getShaderInfoLog(O).trim();let P=!0,q=!0;if(l.getProgramParameter(M,l.LINK_STATUS)===!1)if(P=!1,typeof o.debug.onShaderError=="function")o.debug.onShaderError(l,M,B,O);else{const J=W_(l,B,"vertex"),lt=W_(l,O,"fragment");console.error("THREE.WebGLProgram: Shader Error "+l.getError()+" - VALIDATE_STATUS "+l.getProgramParameter(M,l.VALIDATE_STATUS)+`

Program Info Log: `+Et+`
`+J+`
`+lt)}else Et!==""?console.warn("THREE.WebGLProgram: Program Info Log:",Et):(X===""||tt==="")&&(q=!1);q&&(dt.diagnostics={runnable:P,programLog:Et,vertexShader:{log:X,prefix:v},fragmentShader:{log:tt,prefix:D}})}l.deleteShader(B),l.deleteShader(O),C=new du(l,M),N=Ub(l,M)}let C;this.getUniforms=function(){return C===void 0&&ut(this),C};let N;this.getAttributes=function(){return N===void 0&&ut(this),N};let rt=i.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return rt===!1&&(rt=l.getProgramParameter(M,Eb)),rt},this.destroy=function(){r.releaseStatesOfProgram(this),l.deleteProgram(M),this.program=void 0},this.type=i.shaderType,this.name=i.shaderName,this.id=Tb++,this.cacheKey=e,this.usedTimes=1,this.program=M,this.vertexShader=B,this.fragmentShader=O,this}let Wb=0;class kb{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const i=e.vertexShader,r=e.fragmentShader,l=this._getShaderStage(i),c=this._getShaderStage(r),d=this._getShaderCacheForMaterial(e);return d.has(l)===!1&&(d.add(l),l.usedTimes++),d.has(c)===!1&&(d.add(c),c.usedTimes++),this}remove(e){const i=this.materialCache.get(e);for(const r of i)r.usedTimes--,r.usedTimes===0&&this.shaderCache.delete(r.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const i=this.materialCache;let r=i.get(e);return r===void 0&&(r=new Set,i.set(e,r)),r}_getShaderStage(e){const i=this.shaderCache;let r=i.get(e);return r===void 0&&(r=new qb(e),i.set(e,r)),r}}class qb{constructor(e){this.id=Wb++,this.code=e,this.usedTimes=0}}function Yb(o,e,i,r,l,c,d){const h=new Ev,m=new kb,p=[],g=l.isWebGL2,_=l.logarithmicDepthBuffer,x=l.vertexTextures;let y=l.precision;const b={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function A(C){return C===0?"uv":`uv${C}`}function M(C,N,rt,dt,Et){const X=dt.fog,tt=Et.geometry,P=C.isMeshStandardMaterial?dt.environment:null,q=(C.isMeshStandardMaterial?i:e).get(C.envMap||P),J=q&&q.mapping===xu?q.image.height:null,lt=b[C.type];C.precision!==null&&(y=l.getMaxPrecision(C.precision),y!==C.precision&&console.warn("THREE.WebGLProgram.getParameters:",C.precision,"not supported, using",y,"instead."));const ft=tt.morphAttributes.position||tt.morphAttributes.normal||tt.morphAttributes.color,L=ft!==void 0?ft.length:0;let W=0;tt.morphAttributes.position!==void 0&&(W=1),tt.morphAttributes.normal!==void 0&&(W=2),tt.morphAttributes.color!==void 0&&(W=3);let G,K,mt,xt;if(lt){const qe=bi[lt];G=qe.vertexShader,K=qe.fragmentShader}else G=C.vertexShader,K=C.fragmentShader,m.update(C),mt=m.getVertexShaderID(C),xt=m.getFragmentShaderID(C);const Mt=o.getRenderTarget(),It=Et.isInstancedMesh===!0,Nt=Et.isBatchedMesh===!0,kt=!!C.map,ue=!!C.matcap,et=!!q,un=!!C.aoMap,Ft=!!C.lightMap,Qt=!!C.bumpMap,Pt=!!C.normalMap,Pe=!!C.displacementMap,ee=!!C.emissiveMap,U=!!C.metalnessMap,R=!!C.roughnessMap,it=C.anisotropy>0,St=C.clearcoat>0,vt=C.iridescence>0,gt=C.sheen>0,Ht=C.transmission>0,Rt=it&&!!C.anisotropyMap,Ut=St&&!!C.clearcoatMap,qt=St&&!!C.clearcoatNormalMap,ie=St&&!!C.clearcoatRoughnessMap,_t=vt&&!!C.iridescenceMap,ye=vt&&!!C.iridescenceThicknessMap,le=gt&&!!C.sheenColorMap,Kt=gt&&!!C.sheenRoughnessMap,Dt=!!C.specularMap,wt=!!C.specularColorMap,Xt=!!C.specularIntensityMap,Se=Ht&&!!C.transmissionMap,He=Ht&&!!C.thicknessMap,re=!!C.gradientMap,yt=!!C.alphaMap,F=C.alphaTest>0,At=!!C.alphaHash,Tt=!!C.extensions,jt=!!tt.attributes.uv1,Gt=!!tt.attributes.uv2,Re=!!tt.attributes.uv3;let Ee=Ba;return C.toneMapped&&(Mt===null||Mt.isXRRenderTarget===!0)&&(Ee=o.toneMapping),{isWebGL2:g,shaderID:lt,shaderType:C.type,shaderName:C.name,vertexShader:G,fragmentShader:K,defines:C.defines,customVertexShaderID:mt,customFragmentShaderID:xt,isRawShaderMaterial:C.isRawShaderMaterial===!0,glslVersion:C.glslVersion,precision:y,batching:Nt,instancing:It,instancingColor:It&&Et.instanceColor!==null,supportsVertexTextures:x,outputColorSpace:Mt===null?o.outputColorSpace:Mt.isXRRenderTarget===!0?Mt.texture.colorSpace:$i,map:kt,matcap:ue,envMap:et,envMapMode:et&&q.mapping,envMapCubeUVHeight:J,aoMap:un,lightMap:Ft,bumpMap:Qt,normalMap:Pt,displacementMap:x&&Pe,emissiveMap:ee,normalMapObjectSpace:Pt&&C.normalMapType===eM,normalMapTangentSpace:Pt&&C.normalMapType===_v,metalnessMap:U,roughnessMap:R,anisotropy:it,anisotropyMap:Rt,clearcoat:St,clearcoatMap:Ut,clearcoatNormalMap:qt,clearcoatRoughnessMap:ie,iridescence:vt,iridescenceMap:_t,iridescenceThicknessMap:ye,sheen:gt,sheenColorMap:le,sheenRoughnessMap:Kt,specularMap:Dt,specularColorMap:wt,specularIntensityMap:Xt,transmission:Ht,transmissionMap:Se,thicknessMap:He,gradientMap:re,opaque:C.transparent===!1&&C.blending===ds,alphaMap:yt,alphaTest:F,alphaHash:At,combine:C.combine,mapUv:kt&&A(C.map.channel),aoMapUv:un&&A(C.aoMap.channel),lightMapUv:Ft&&A(C.lightMap.channel),bumpMapUv:Qt&&A(C.bumpMap.channel),normalMapUv:Pt&&A(C.normalMap.channel),displacementMapUv:Pe&&A(C.displacementMap.channel),emissiveMapUv:ee&&A(C.emissiveMap.channel),metalnessMapUv:U&&A(C.metalnessMap.channel),roughnessMapUv:R&&A(C.roughnessMap.channel),anisotropyMapUv:Rt&&A(C.anisotropyMap.channel),clearcoatMapUv:Ut&&A(C.clearcoatMap.channel),clearcoatNormalMapUv:qt&&A(C.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:ie&&A(C.clearcoatRoughnessMap.channel),iridescenceMapUv:_t&&A(C.iridescenceMap.channel),iridescenceThicknessMapUv:ye&&A(C.iridescenceThicknessMap.channel),sheenColorMapUv:le&&A(C.sheenColorMap.channel),sheenRoughnessMapUv:Kt&&A(C.sheenRoughnessMap.channel),specularMapUv:Dt&&A(C.specularMap.channel),specularColorMapUv:wt&&A(C.specularColorMap.channel),specularIntensityMapUv:Xt&&A(C.specularIntensityMap.channel),transmissionMapUv:Se&&A(C.transmissionMap.channel),thicknessMapUv:He&&A(C.thicknessMap.channel),alphaMapUv:yt&&A(C.alphaMap.channel),vertexTangents:!!tt.attributes.tangent&&(Pt||it),vertexColors:C.vertexColors,vertexAlphas:C.vertexColors===!0&&!!tt.attributes.color&&tt.attributes.color.itemSize===4,vertexUv1s:jt,vertexUv2s:Gt,vertexUv3s:Re,pointsUvs:Et.isPoints===!0&&!!tt.attributes.uv&&(kt||yt),fog:!!X,useFog:C.fog===!0,fogExp2:X&&X.isFogExp2,flatShading:C.flatShading===!0,sizeAttenuation:C.sizeAttenuation===!0,logarithmicDepthBuffer:_,skinning:Et.isSkinnedMesh===!0,morphTargets:tt.morphAttributes.position!==void 0,morphNormals:tt.morphAttributes.normal!==void 0,morphColors:tt.morphAttributes.color!==void 0,morphTargetsCount:L,morphTextureStride:W,numDirLights:N.directional.length,numPointLights:N.point.length,numSpotLights:N.spot.length,numSpotLightMaps:N.spotLightMap.length,numRectAreaLights:N.rectArea.length,numHemiLights:N.hemi.length,numDirLightShadows:N.directionalShadowMap.length,numPointLightShadows:N.pointShadowMap.length,numSpotLightShadows:N.spotShadowMap.length,numSpotLightShadowsWithMaps:N.numSpotLightShadowsWithMaps,numLightProbes:N.numLightProbes,numClippingPlanes:d.numPlanes,numClipIntersection:d.numIntersection,dithering:C.dithering,shadowMapEnabled:o.shadowMap.enabled&&rt.length>0,shadowMapType:o.shadowMap.type,toneMapping:Ee,useLegacyLights:o._useLegacyLights,decodeVideoTexture:kt&&C.map.isVideoTexture===!0&&Ue.getTransfer(C.map.colorSpace)===Fe,premultipliedAlpha:C.premultipliedAlpha,doubleSided:C.side===Qi,flipSided:C.side===Fn,useDepthPacking:C.depthPacking>=0,depthPacking:C.depthPacking||0,index0AttributeName:C.index0AttributeName,extensionDerivatives:Tt&&C.extensions.derivatives===!0,extensionFragDepth:Tt&&C.extensions.fragDepth===!0,extensionDrawBuffers:Tt&&C.extensions.drawBuffers===!0,extensionShaderTextureLOD:Tt&&C.extensions.shaderTextureLOD===!0,extensionClipCullDistance:Tt&&C.extensions.clipCullDistance&&r.has("WEBGL_clip_cull_distance"),rendererExtensionFragDepth:g||r.has("EXT_frag_depth"),rendererExtensionDrawBuffers:g||r.has("WEBGL_draw_buffers"),rendererExtensionShaderTextureLod:g||r.has("EXT_shader_texture_lod"),rendererExtensionParallelShaderCompile:r.has("KHR_parallel_shader_compile"),customProgramCacheKey:C.customProgramCacheKey()}}function v(C){const N=[];if(C.shaderID?N.push(C.shaderID):(N.push(C.customVertexShaderID),N.push(C.customFragmentShaderID)),C.defines!==void 0)for(const rt in C.defines)N.push(rt),N.push(C.defines[rt]);return C.isRawShaderMaterial===!1&&(D(N,C),T(N,C),N.push(o.outputColorSpace)),N.push(C.customProgramCacheKey),N.join()}function D(C,N){C.push(N.precision),C.push(N.outputColorSpace),C.push(N.envMapMode),C.push(N.envMapCubeUVHeight),C.push(N.mapUv),C.push(N.alphaMapUv),C.push(N.lightMapUv),C.push(N.aoMapUv),C.push(N.bumpMapUv),C.push(N.normalMapUv),C.push(N.displacementMapUv),C.push(N.emissiveMapUv),C.push(N.metalnessMapUv),C.push(N.roughnessMapUv),C.push(N.anisotropyMapUv),C.push(N.clearcoatMapUv),C.push(N.clearcoatNormalMapUv),C.push(N.clearcoatRoughnessMapUv),C.push(N.iridescenceMapUv),C.push(N.iridescenceThicknessMapUv),C.push(N.sheenColorMapUv),C.push(N.sheenRoughnessMapUv),C.push(N.specularMapUv),C.push(N.specularColorMapUv),C.push(N.specularIntensityMapUv),C.push(N.transmissionMapUv),C.push(N.thicknessMapUv),C.push(N.combine),C.push(N.fogExp2),C.push(N.sizeAttenuation),C.push(N.morphTargetsCount),C.push(N.morphAttributeCount),C.push(N.numDirLights),C.push(N.numPointLights),C.push(N.numSpotLights),C.push(N.numSpotLightMaps),C.push(N.numHemiLights),C.push(N.numRectAreaLights),C.push(N.numDirLightShadows),C.push(N.numPointLightShadows),C.push(N.numSpotLightShadows),C.push(N.numSpotLightShadowsWithMaps),C.push(N.numLightProbes),C.push(N.shadowMapType),C.push(N.toneMapping),C.push(N.numClippingPlanes),C.push(N.numClipIntersection),C.push(N.depthPacking)}function T(C,N){h.disableAll(),N.isWebGL2&&h.enable(0),N.supportsVertexTextures&&h.enable(1),N.instancing&&h.enable(2),N.instancingColor&&h.enable(3),N.matcap&&h.enable(4),N.envMap&&h.enable(5),N.normalMapObjectSpace&&h.enable(6),N.normalMapTangentSpace&&h.enable(7),N.clearcoat&&h.enable(8),N.iridescence&&h.enable(9),N.alphaTest&&h.enable(10),N.vertexColors&&h.enable(11),N.vertexAlphas&&h.enable(12),N.vertexUv1s&&h.enable(13),N.vertexUv2s&&h.enable(14),N.vertexUv3s&&h.enable(15),N.vertexTangents&&h.enable(16),N.anisotropy&&h.enable(17),N.alphaHash&&h.enable(18),N.batching&&h.enable(19),C.push(h.mask),h.disableAll(),N.fog&&h.enable(0),N.useFog&&h.enable(1),N.flatShading&&h.enable(2),N.logarithmicDepthBuffer&&h.enable(3),N.skinning&&h.enable(4),N.morphTargets&&h.enable(5),N.morphNormals&&h.enable(6),N.morphColors&&h.enable(7),N.premultipliedAlpha&&h.enable(8),N.shadowMapEnabled&&h.enable(9),N.useLegacyLights&&h.enable(10),N.doubleSided&&h.enable(11),N.flipSided&&h.enable(12),N.useDepthPacking&&h.enable(13),N.dithering&&h.enable(14),N.transmission&&h.enable(15),N.sheen&&h.enable(16),N.opaque&&h.enable(17),N.pointsUvs&&h.enable(18),N.decodeVideoTexture&&h.enable(19),C.push(h.mask)}function z(C){const N=b[C.type];let rt;if(N){const dt=bi[N];rt=wM.clone(dt.uniforms)}else rt=C.uniforms;return rt}function V(C,N){let rt;for(let dt=0,Et=p.length;dt<Et;dt++){const X=p[dt];if(X.cacheKey===N){rt=X,++rt.usedTimes;break}}return rt===void 0&&(rt=new Xb(o,N,C,c),p.push(rt)),rt}function B(C){if(--C.usedTimes===0){const N=p.indexOf(C);p[N]=p[p.length-1],p.pop(),C.destroy()}}function O(C){m.remove(C)}function ut(){m.dispose()}return{getParameters:M,getProgramCacheKey:v,getUniforms:z,acquireProgram:V,releaseProgram:B,releaseShaderCache:O,programs:p,dispose:ut}}function jb(){let o=new WeakMap;function e(c){let d=o.get(c);return d===void 0&&(d={},o.set(c,d)),d}function i(c){o.delete(c)}function r(c,d,h){o.get(c)[d]=h}function l(){o=new WeakMap}return{get:e,remove:i,update:r,dispose:l}}function Zb(o,e){return o.groupOrder!==e.groupOrder?o.groupOrder-e.groupOrder:o.renderOrder!==e.renderOrder?o.renderOrder-e.renderOrder:o.material.id!==e.material.id?o.material.id-e.material.id:o.z!==e.z?o.z-e.z:o.id-e.id}function Z_(o,e){return o.groupOrder!==e.groupOrder?o.groupOrder-e.groupOrder:o.renderOrder!==e.renderOrder?o.renderOrder-e.renderOrder:o.z!==e.z?e.z-o.z:o.id-e.id}function K_(){const o=[];let e=0;const i=[],r=[],l=[];function c(){e=0,i.length=0,r.length=0,l.length=0}function d(_,x,y,b,A,M){let v=o[e];return v===void 0?(v={id:_.id,object:_,geometry:x,material:y,groupOrder:b,renderOrder:_.renderOrder,z:A,group:M},o[e]=v):(v.id=_.id,v.object=_,v.geometry=x,v.material=y,v.groupOrder=b,v.renderOrder=_.renderOrder,v.z=A,v.group=M),e++,v}function h(_,x,y,b,A,M){const v=d(_,x,y,b,A,M);y.transmission>0?r.push(v):y.transparent===!0?l.push(v):i.push(v)}function m(_,x,y,b,A,M){const v=d(_,x,y,b,A,M);y.transmission>0?r.unshift(v):y.transparent===!0?l.unshift(v):i.unshift(v)}function p(_,x){i.length>1&&i.sort(_||Zb),r.length>1&&r.sort(x||Z_),l.length>1&&l.sort(x||Z_)}function g(){for(let _=e,x=o.length;_<x;_++){const y=o[_];if(y.id===null)break;y.id=null,y.object=null,y.geometry=null,y.material=null,y.group=null}}return{opaque:i,transmissive:r,transparent:l,init:c,push:h,unshift:m,finish:g,sort:p}}function Kb(){let o=new WeakMap;function e(r,l){const c=o.get(r);let d;return c===void 0?(d=new K_,o.set(r,[d])):l>=c.length?(d=new K_,c.push(d)):d=c[l],d}function i(){o=new WeakMap}return{get:e,dispose:i}}function Qb(){const o={};return{get:function(e){if(o[e.id]!==void 0)return o[e.id];let i;switch(e.type){case"DirectionalLight":i={direction:new Y,color:new Me};break;case"SpotLight":i={position:new Y,direction:new Y,color:new Me,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":i={position:new Y,color:new Me,distance:0,decay:0};break;case"HemisphereLight":i={direction:new Y,skyColor:new Me,groundColor:new Me};break;case"RectAreaLight":i={color:new Me,position:new Y,halfWidth:new Y,halfHeight:new Y};break}return o[e.id]=i,i}}}function Jb(){const o={};return{get:function(e){if(o[e.id]!==void 0)return o[e.id];let i;switch(e.type){case"DirectionalLight":i={shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ge};break;case"SpotLight":i={shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ge};break;case"PointLight":i={shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new ge,shadowCameraNear:1,shadowCameraFar:1e3};break}return o[e.id]=i,i}}}let $b=0;function tA(o,e){return(e.castShadow?2:0)-(o.castShadow?2:0)+(e.map?1:0)-(o.map?1:0)}function eA(o,e){const i=new Qb,r=Jb(),l={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let g=0;g<9;g++)l.probe.push(new Y);const c=new Y,d=new rn,h=new rn;function m(g,_){let x=0,y=0,b=0;for(let dt=0;dt<9;dt++)l.probe[dt].set(0,0,0);let A=0,M=0,v=0,D=0,T=0,z=0,V=0,B=0,O=0,ut=0,C=0;g.sort(tA);const N=_===!0?Math.PI:1;for(let dt=0,Et=g.length;dt<Et;dt++){const X=g[dt],tt=X.color,P=X.intensity,q=X.distance,J=X.shadow&&X.shadow.map?X.shadow.map.texture:null;if(X.isAmbientLight)x+=tt.r*P*N,y+=tt.g*P*N,b+=tt.b*P*N;else if(X.isLightProbe){for(let lt=0;lt<9;lt++)l.probe[lt].addScaledVector(X.sh.coefficients[lt],P);C++}else if(X.isDirectionalLight){const lt=i.get(X);if(lt.color.copy(X.color).multiplyScalar(X.intensity*N),X.castShadow){const ft=X.shadow,L=r.get(X);L.shadowBias=ft.bias,L.shadowNormalBias=ft.normalBias,L.shadowRadius=ft.radius,L.shadowMapSize=ft.mapSize,l.directionalShadow[A]=L,l.directionalShadowMap[A]=J,l.directionalShadowMatrix[A]=X.shadow.matrix,z++}l.directional[A]=lt,A++}else if(X.isSpotLight){const lt=i.get(X);lt.position.setFromMatrixPosition(X.matrixWorld),lt.color.copy(tt).multiplyScalar(P*N),lt.distance=q,lt.coneCos=Math.cos(X.angle),lt.penumbraCos=Math.cos(X.angle*(1-X.penumbra)),lt.decay=X.decay,l.spot[v]=lt;const ft=X.shadow;if(X.map&&(l.spotLightMap[O]=X.map,O++,ft.updateMatrices(X),X.castShadow&&ut++),l.spotLightMatrix[v]=ft.matrix,X.castShadow){const L=r.get(X);L.shadowBias=ft.bias,L.shadowNormalBias=ft.normalBias,L.shadowRadius=ft.radius,L.shadowMapSize=ft.mapSize,l.spotShadow[v]=L,l.spotShadowMap[v]=J,B++}v++}else if(X.isRectAreaLight){const lt=i.get(X);lt.color.copy(tt).multiplyScalar(P),lt.halfWidth.set(X.width*.5,0,0),lt.halfHeight.set(0,X.height*.5,0),l.rectArea[D]=lt,D++}else if(X.isPointLight){const lt=i.get(X);if(lt.color.copy(X.color).multiplyScalar(X.intensity*N),lt.distance=X.distance,lt.decay=X.decay,X.castShadow){const ft=X.shadow,L=r.get(X);L.shadowBias=ft.bias,L.shadowNormalBias=ft.normalBias,L.shadowRadius=ft.radius,L.shadowMapSize=ft.mapSize,L.shadowCameraNear=ft.camera.near,L.shadowCameraFar=ft.camera.far,l.pointShadow[M]=L,l.pointShadowMap[M]=J,l.pointShadowMatrix[M]=X.shadow.matrix,V++}l.point[M]=lt,M++}else if(X.isHemisphereLight){const lt=i.get(X);lt.skyColor.copy(X.color).multiplyScalar(P*N),lt.groundColor.copy(X.groundColor).multiplyScalar(P*N),l.hemi[T]=lt,T++}}D>0&&(e.isWebGL2?o.has("OES_texture_float_linear")===!0?(l.rectAreaLTC1=bt.LTC_FLOAT_1,l.rectAreaLTC2=bt.LTC_FLOAT_2):(l.rectAreaLTC1=bt.LTC_HALF_1,l.rectAreaLTC2=bt.LTC_HALF_2):o.has("OES_texture_float_linear")===!0?(l.rectAreaLTC1=bt.LTC_FLOAT_1,l.rectAreaLTC2=bt.LTC_FLOAT_2):o.has("OES_texture_half_float_linear")===!0?(l.rectAreaLTC1=bt.LTC_HALF_1,l.rectAreaLTC2=bt.LTC_HALF_2):console.error("THREE.WebGLRenderer: Unable to use RectAreaLight. Missing WebGL extensions.")),l.ambient[0]=x,l.ambient[1]=y,l.ambient[2]=b;const rt=l.hash;(rt.directionalLength!==A||rt.pointLength!==M||rt.spotLength!==v||rt.rectAreaLength!==D||rt.hemiLength!==T||rt.numDirectionalShadows!==z||rt.numPointShadows!==V||rt.numSpotShadows!==B||rt.numSpotMaps!==O||rt.numLightProbes!==C)&&(l.directional.length=A,l.spot.length=v,l.rectArea.length=D,l.point.length=M,l.hemi.length=T,l.directionalShadow.length=z,l.directionalShadowMap.length=z,l.pointShadow.length=V,l.pointShadowMap.length=V,l.spotShadow.length=B,l.spotShadowMap.length=B,l.directionalShadowMatrix.length=z,l.pointShadowMatrix.length=V,l.spotLightMatrix.length=B+O-ut,l.spotLightMap.length=O,l.numSpotLightShadowsWithMaps=ut,l.numLightProbes=C,rt.directionalLength=A,rt.pointLength=M,rt.spotLength=v,rt.rectAreaLength=D,rt.hemiLength=T,rt.numDirectionalShadows=z,rt.numPointShadows=V,rt.numSpotShadows=B,rt.numSpotMaps=O,rt.numLightProbes=C,l.version=$b++)}function p(g,_){let x=0,y=0,b=0,A=0,M=0;const v=_.matrixWorldInverse;for(let D=0,T=g.length;D<T;D++){const z=g[D];if(z.isDirectionalLight){const V=l.directional[x];V.direction.setFromMatrixPosition(z.matrixWorld),c.setFromMatrixPosition(z.target.matrixWorld),V.direction.sub(c),V.direction.transformDirection(v),x++}else if(z.isSpotLight){const V=l.spot[b];V.position.setFromMatrixPosition(z.matrixWorld),V.position.applyMatrix4(v),V.direction.setFromMatrixPosition(z.matrixWorld),c.setFromMatrixPosition(z.target.matrixWorld),V.direction.sub(c),V.direction.transformDirection(v),b++}else if(z.isRectAreaLight){const V=l.rectArea[A];V.position.setFromMatrixPosition(z.matrixWorld),V.position.applyMatrix4(v),h.identity(),d.copy(z.matrixWorld),d.premultiply(v),h.extractRotation(d),V.halfWidth.set(z.width*.5,0,0),V.halfHeight.set(0,z.height*.5,0),V.halfWidth.applyMatrix4(h),V.halfHeight.applyMatrix4(h),A++}else if(z.isPointLight){const V=l.point[y];V.position.setFromMatrixPosition(z.matrixWorld),V.position.applyMatrix4(v),y++}else if(z.isHemisphereLight){const V=l.hemi[M];V.direction.setFromMatrixPosition(z.matrixWorld),V.direction.transformDirection(v),M++}}}return{setup:m,setupView:p,state:l}}function Q_(o,e){const i=new eA(o,e),r=[],l=[];function c(){r.length=0,l.length=0}function d(_){r.push(_)}function h(_){l.push(_)}function m(_){i.setup(r,_)}function p(_){i.setupView(r,_)}return{init:c,state:{lightsArray:r,shadowsArray:l,lights:i},setupLights:m,setupLightsView:p,pushLight:d,pushShadow:h}}function nA(o,e){let i=new WeakMap;function r(c,d=0){const h=i.get(c);let m;return h===void 0?(m=new Q_(o,e),i.set(c,[m])):d>=h.length?(m=new Q_(o,e),h.push(m)):m=h[d],m}function l(){i=new WeakMap}return{get:r,dispose:l}}class iA extends Uo{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=$x,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class aA extends Uo{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}const rA=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,sA=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
#include <packing>
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = unpackRGBATo2Half( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ) );
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = unpackRGBAToDepth( texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ) );
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( squared_mean - mean * mean );
	gl_FragColor = pack2HalfToRGBA( vec2( mean, std_dev ) );
}`;function oA(o,e,i){let r=new Uh;const l=new ge,c=new ge,d=new Ve,h=new iA({depthPacking:tM}),m=new aA,p={},g=i.maxTextureSize,_={[Fa]:Fn,[Fn]:Fa,[Qi]:Qi},x=new mr({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new ge},radius:{value:4}},vertexShader:rA,fragmentShader:sA}),y=x.clone();y.defines.HORIZONTAL_PASS=1;const b=new Ri;b.setAttribute("position",new Ai(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const A=new za(b,x),M=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=sv;let v=this.type;this.render=function(B,O,ut){if(M.enabled===!1||M.autoUpdate===!1&&M.needsUpdate===!1||B.length===0)return;const C=o.getRenderTarget(),N=o.getActiveCubeFace(),rt=o.getActiveMipmapLevel(),dt=o.state;dt.setBlending(Pa),dt.buffers.color.setClear(1,1,1,1),dt.buffers.depth.setTest(!0),dt.setScissorTest(!1);const Et=v!==Ki&&this.type===Ki,X=v===Ki&&this.type!==Ki;for(let tt=0,P=B.length;tt<P;tt++){const q=B[tt],J=q.shadow;if(J===void 0){console.warn("THREE.WebGLShadowMap:",q,"has no shadow.");continue}if(J.autoUpdate===!1&&J.needsUpdate===!1)continue;l.copy(J.mapSize);const lt=J.getFrameExtents();if(l.multiply(lt),c.copy(J.mapSize),(l.x>g||l.y>g)&&(l.x>g&&(c.x=Math.floor(g/lt.x),l.x=c.x*lt.x,J.mapSize.x=c.x),l.y>g&&(c.y=Math.floor(g/lt.y),l.y=c.y*lt.y,J.mapSize.y=c.y)),J.map===null||Et===!0||X===!0){const L=this.type!==Ki?{minFilter:wn,magFilter:wn}:{};J.map!==null&&J.map.dispose(),J.map=new pr(l.x,l.y,L),J.map.texture.name=q.name+".shadowMap",J.camera.updateProjectionMatrix()}o.setRenderTarget(J.map),o.clear();const ft=J.getViewportCount();for(let L=0;L<ft;L++){const W=J.getViewport(L);d.set(c.x*W.x,c.y*W.y,c.x*W.z,c.y*W.w),dt.viewport(d),J.updateMatrices(q,L),r=J.getFrustum(),z(O,ut,J.camera,q,this.type)}J.isPointLightShadow!==!0&&this.type===Ki&&D(J,ut),J.needsUpdate=!1}v=this.type,M.needsUpdate=!1,o.setRenderTarget(C,N,rt)};function D(B,O){const ut=e.update(A);x.defines.VSM_SAMPLES!==B.blurSamples&&(x.defines.VSM_SAMPLES=B.blurSamples,y.defines.VSM_SAMPLES=B.blurSamples,x.needsUpdate=!0,y.needsUpdate=!0),B.mapPass===null&&(B.mapPass=new pr(l.x,l.y)),x.uniforms.shadow_pass.value=B.map.texture,x.uniforms.resolution.value=B.mapSize,x.uniforms.radius.value=B.radius,o.setRenderTarget(B.mapPass),o.clear(),o.renderBufferDirect(O,null,ut,x,A,null),y.uniforms.shadow_pass.value=B.mapPass.texture,y.uniforms.resolution.value=B.mapSize,y.uniforms.radius.value=B.radius,o.setRenderTarget(B.map),o.clear(),o.renderBufferDirect(O,null,ut,y,A,null)}function T(B,O,ut,C){let N=null;const rt=ut.isPointLight===!0?B.customDistanceMaterial:B.customDepthMaterial;if(rt!==void 0)N=rt;else if(N=ut.isPointLight===!0?m:h,o.localClippingEnabled&&O.clipShadows===!0&&Array.isArray(O.clippingPlanes)&&O.clippingPlanes.length!==0||O.displacementMap&&O.displacementScale!==0||O.alphaMap&&O.alphaTest>0||O.map&&O.alphaTest>0){const dt=N.uuid,Et=O.uuid;let X=p[dt];X===void 0&&(X={},p[dt]=X);let tt=X[Et];tt===void 0&&(tt=N.clone(),X[Et]=tt,O.addEventListener("dispose",V)),N=tt}if(N.visible=O.visible,N.wireframe=O.wireframe,C===Ki?N.side=O.shadowSide!==null?O.shadowSide:O.side:N.side=O.shadowSide!==null?O.shadowSide:_[O.side],N.alphaMap=O.alphaMap,N.alphaTest=O.alphaTest,N.map=O.map,N.clipShadows=O.clipShadows,N.clippingPlanes=O.clippingPlanes,N.clipIntersection=O.clipIntersection,N.displacementMap=O.displacementMap,N.displacementScale=O.displacementScale,N.displacementBias=O.displacementBias,N.wireframeLinewidth=O.wireframeLinewidth,N.linewidth=O.linewidth,ut.isPointLight===!0&&N.isMeshDistanceMaterial===!0){const dt=o.properties.get(N);dt.light=ut}return N}function z(B,O,ut,C,N){if(B.visible===!1)return;if(B.layers.test(O.layers)&&(B.isMesh||B.isLine||B.isPoints)&&(B.castShadow||B.receiveShadow&&N===Ki)&&(!B.frustumCulled||r.intersectsObject(B))){B.modelViewMatrix.multiplyMatrices(ut.matrixWorldInverse,B.matrixWorld);const Et=e.update(B),X=B.material;if(Array.isArray(X)){const tt=Et.groups;for(let P=0,q=tt.length;P<q;P++){const J=tt[P],lt=X[J.materialIndex];if(lt&&lt.visible){const ft=T(B,lt,C,N);B.onBeforeShadow(o,B,O,ut,Et,ft,J),o.renderBufferDirect(ut,null,Et,ft,B,J),B.onAfterShadow(o,B,O,ut,Et,ft,J)}}}else if(X.visible){const tt=T(B,X,C,N);B.onBeforeShadow(o,B,O,ut,Et,tt,null),o.renderBufferDirect(ut,null,Et,tt,B,null),B.onAfterShadow(o,B,O,ut,Et,tt,null)}}const dt=B.children;for(let Et=0,X=dt.length;Et<X;Et++)z(dt[Et],O,ut,C,N)}function V(B){B.target.removeEventListener("dispose",V);for(const ut in p){const C=p[ut],N=B.target.uuid;N in C&&(C[N].dispose(),delete C[N])}}}function lA(o,e,i){const r=i.isWebGL2;function l(){let F=!1;const At=new Ve;let Tt=null;const jt=new Ve(0,0,0,0);return{setMask:function(Gt){Tt!==Gt&&!F&&(o.colorMask(Gt,Gt,Gt,Gt),Tt=Gt)},setLocked:function(Gt){F=Gt},setClear:function(Gt,Re,Ee,Xe,qe){qe===!0&&(Gt*=Xe,Re*=Xe,Ee*=Xe),At.set(Gt,Re,Ee,Xe),jt.equals(At)===!1&&(o.clearColor(Gt,Re,Ee,Xe),jt.copy(At))},reset:function(){F=!1,Tt=null,jt.set(-1,0,0,0)}}}function c(){let F=!1,At=null,Tt=null,jt=null;return{setTest:function(Gt){Gt?Nt(o.DEPTH_TEST):kt(o.DEPTH_TEST)},setMask:function(Gt){At!==Gt&&!F&&(o.depthMask(Gt),At=Gt)},setFunc:function(Gt){if(Tt!==Gt){switch(Gt){case wx:o.depthFunc(o.NEVER);break;case Dx:o.depthFunc(o.ALWAYS);break;case Lx:o.depthFunc(o.LESS);break;case pu:o.depthFunc(o.LEQUAL);break;case Ux:o.depthFunc(o.EQUAL);break;case Nx:o.depthFunc(o.GEQUAL);break;case Ox:o.depthFunc(o.GREATER);break;case zx:o.depthFunc(o.NOTEQUAL);break;default:o.depthFunc(o.LEQUAL)}Tt=Gt}},setLocked:function(Gt){F=Gt},setClear:function(Gt){jt!==Gt&&(o.clearDepth(Gt),jt=Gt)},reset:function(){F=!1,At=null,Tt=null,jt=null}}}function d(){let F=!1,At=null,Tt=null,jt=null,Gt=null,Re=null,Ee=null,Xe=null,qe=null;return{setTest:function(Ce){F||(Ce?Nt(o.STENCIL_TEST):kt(o.STENCIL_TEST))},setMask:function(Ce){At!==Ce&&!F&&(o.stencilMask(Ce),At=Ce)},setFunc:function(Ce,cn,Hn){(Tt!==Ce||jt!==cn||Gt!==Hn)&&(o.stencilFunc(Ce,cn,Hn),Tt=Ce,jt=cn,Gt=Hn)},setOp:function(Ce,cn,Hn){(Re!==Ce||Ee!==cn||Xe!==Hn)&&(o.stencilOp(Ce,cn,Hn),Re=Ce,Ee=cn,Xe=Hn)},setLocked:function(Ce){F=Ce},setClear:function(Ce){qe!==Ce&&(o.clearStencil(Ce),qe=Ce)},reset:function(){F=!1,At=null,Tt=null,jt=null,Gt=null,Re=null,Ee=null,Xe=null,qe=null}}}const h=new l,m=new c,p=new d,g=new WeakMap,_=new WeakMap;let x={},y={},b=new WeakMap,A=[],M=null,v=!1,D=null,T=null,z=null,V=null,B=null,O=null,ut=null,C=new Me(0,0,0),N=0,rt=!1,dt=null,Et=null,X=null,tt=null,P=null;const q=o.getParameter(o.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let J=!1,lt=0;const ft=o.getParameter(o.VERSION);ft.indexOf("WebGL")!==-1?(lt=parseFloat(/^WebGL (\d)/.exec(ft)[1]),J=lt>=1):ft.indexOf("OpenGL ES")!==-1&&(lt=parseFloat(/^OpenGL ES (\d)/.exec(ft)[1]),J=lt>=2);let L=null,W={};const G=o.getParameter(o.SCISSOR_BOX),K=o.getParameter(o.VIEWPORT),mt=new Ve().fromArray(G),xt=new Ve().fromArray(K);function Mt(F,At,Tt,jt){const Gt=new Uint8Array(4),Re=o.createTexture();o.bindTexture(F,Re),o.texParameteri(F,o.TEXTURE_MIN_FILTER,o.NEAREST),o.texParameteri(F,o.TEXTURE_MAG_FILTER,o.NEAREST);for(let Ee=0;Ee<Tt;Ee++)r&&(F===o.TEXTURE_3D||F===o.TEXTURE_2D_ARRAY)?o.texImage3D(At,0,o.RGBA,1,1,jt,0,o.RGBA,o.UNSIGNED_BYTE,Gt):o.texImage2D(At+Ee,0,o.RGBA,1,1,0,o.RGBA,o.UNSIGNED_BYTE,Gt);return Re}const It={};It[o.TEXTURE_2D]=Mt(o.TEXTURE_2D,o.TEXTURE_2D,1),It[o.TEXTURE_CUBE_MAP]=Mt(o.TEXTURE_CUBE_MAP,o.TEXTURE_CUBE_MAP_POSITIVE_X,6),r&&(It[o.TEXTURE_2D_ARRAY]=Mt(o.TEXTURE_2D_ARRAY,o.TEXTURE_2D_ARRAY,1,1),It[o.TEXTURE_3D]=Mt(o.TEXTURE_3D,o.TEXTURE_3D,1,1)),h.setClear(0,0,0,1),m.setClear(1),p.setClear(0),Nt(o.DEPTH_TEST),m.setFunc(pu),ee(!1),U(Ug),Nt(o.CULL_FACE),Pt(Pa);function Nt(F){x[F]!==!0&&(o.enable(F),x[F]=!0)}function kt(F){x[F]!==!1&&(o.disable(F),x[F]=!1)}function ue(F,At){return y[F]!==At?(o.bindFramebuffer(F,At),y[F]=At,r&&(F===o.DRAW_FRAMEBUFFER&&(y[o.FRAMEBUFFER]=At),F===o.FRAMEBUFFER&&(y[o.DRAW_FRAMEBUFFER]=At)),!0):!1}function et(F,At){let Tt=A,jt=!1;if(F)if(Tt=b.get(At),Tt===void 0&&(Tt=[],b.set(At,Tt)),F.isWebGLMultipleRenderTargets){const Gt=F.texture;if(Tt.length!==Gt.length||Tt[0]!==o.COLOR_ATTACHMENT0){for(let Re=0,Ee=Gt.length;Re<Ee;Re++)Tt[Re]=o.COLOR_ATTACHMENT0+Re;Tt.length=Gt.length,jt=!0}}else Tt[0]!==o.COLOR_ATTACHMENT0&&(Tt[0]=o.COLOR_ATTACHMENT0,jt=!0);else Tt[0]!==o.BACK&&(Tt[0]=o.BACK,jt=!0);jt&&(i.isWebGL2?o.drawBuffers(Tt):e.get("WEBGL_draw_buffers").drawBuffersWEBGL(Tt))}function un(F){return M!==F?(o.useProgram(F),M=F,!0):!1}const Ft={[ur]:o.FUNC_ADD,[px]:o.FUNC_SUBTRACT,[mx]:o.FUNC_REVERSE_SUBTRACT};if(r)Ft[Pg]=o.MIN,Ft[Bg]=o.MAX;else{const F=e.get("EXT_blend_minmax");F!==null&&(Ft[Pg]=F.MIN_EXT,Ft[Bg]=F.MAX_EXT)}const Qt={[gx]:o.ZERO,[_x]:o.ONE,[vx]:o.SRC_COLOR,[vh]:o.SRC_ALPHA,[Tx]:o.SRC_ALPHA_SATURATE,[yx]:o.DST_COLOR,[xx]:o.DST_ALPHA,[Sx]:o.ONE_MINUS_SRC_COLOR,[Sh]:o.ONE_MINUS_SRC_ALPHA,[Ex]:o.ONE_MINUS_DST_COLOR,[Mx]:o.ONE_MINUS_DST_ALPHA,[bx]:o.CONSTANT_COLOR,[Ax]:o.ONE_MINUS_CONSTANT_COLOR,[Rx]:o.CONSTANT_ALPHA,[Cx]:o.ONE_MINUS_CONSTANT_ALPHA};function Pt(F,At,Tt,jt,Gt,Re,Ee,Xe,qe,Ce){if(F===Pa){v===!0&&(kt(o.BLEND),v=!1);return}if(v===!1&&(Nt(o.BLEND),v=!0),F!==dx){if(F!==D||Ce!==rt){if((T!==ur||B!==ur)&&(o.blendEquation(o.FUNC_ADD),T=ur,B=ur),Ce)switch(F){case ds:o.blendFuncSeparate(o.ONE,o.ONE_MINUS_SRC_ALPHA,o.ONE,o.ONE_MINUS_SRC_ALPHA);break;case Ng:o.blendFunc(o.ONE,o.ONE);break;case Og:o.blendFuncSeparate(o.ZERO,o.ONE_MINUS_SRC_COLOR,o.ZERO,o.ONE);break;case zg:o.blendFuncSeparate(o.ZERO,o.SRC_COLOR,o.ZERO,o.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",F);break}else switch(F){case ds:o.blendFuncSeparate(o.SRC_ALPHA,o.ONE_MINUS_SRC_ALPHA,o.ONE,o.ONE_MINUS_SRC_ALPHA);break;case Ng:o.blendFunc(o.SRC_ALPHA,o.ONE);break;case Og:o.blendFuncSeparate(o.ZERO,o.ONE_MINUS_SRC_COLOR,o.ZERO,o.ONE);break;case zg:o.blendFunc(o.ZERO,o.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",F);break}z=null,V=null,O=null,ut=null,C.set(0,0,0),N=0,D=F,rt=Ce}return}Gt=Gt||At,Re=Re||Tt,Ee=Ee||jt,(At!==T||Gt!==B)&&(o.blendEquationSeparate(Ft[At],Ft[Gt]),T=At,B=Gt),(Tt!==z||jt!==V||Re!==O||Ee!==ut)&&(o.blendFuncSeparate(Qt[Tt],Qt[jt],Qt[Re],Qt[Ee]),z=Tt,V=jt,O=Re,ut=Ee),(Xe.equals(C)===!1||qe!==N)&&(o.blendColor(Xe.r,Xe.g,Xe.b,qe),C.copy(Xe),N=qe),D=F,rt=!1}function Pe(F,At){F.side===Qi?kt(o.CULL_FACE):Nt(o.CULL_FACE);let Tt=F.side===Fn;At&&(Tt=!Tt),ee(Tt),F.blending===ds&&F.transparent===!1?Pt(Pa):Pt(F.blending,F.blendEquation,F.blendSrc,F.blendDst,F.blendEquationAlpha,F.blendSrcAlpha,F.blendDstAlpha,F.blendColor,F.blendAlpha,F.premultipliedAlpha),m.setFunc(F.depthFunc),m.setTest(F.depthTest),m.setMask(F.depthWrite),h.setMask(F.colorWrite);const jt=F.stencilWrite;p.setTest(jt),jt&&(p.setMask(F.stencilWriteMask),p.setFunc(F.stencilFunc,F.stencilRef,F.stencilFuncMask),p.setOp(F.stencilFail,F.stencilZFail,F.stencilZPass)),it(F.polygonOffset,F.polygonOffsetFactor,F.polygonOffsetUnits),F.alphaToCoverage===!0?Nt(o.SAMPLE_ALPHA_TO_COVERAGE):kt(o.SAMPLE_ALPHA_TO_COVERAGE)}function ee(F){dt!==F&&(F?o.frontFace(o.CW):o.frontFace(o.CCW),dt=F)}function U(F){F!==cx?(Nt(o.CULL_FACE),F!==Et&&(F===Ug?o.cullFace(o.BACK):F===fx?o.cullFace(o.FRONT):o.cullFace(o.FRONT_AND_BACK))):kt(o.CULL_FACE),Et=F}function R(F){F!==X&&(J&&o.lineWidth(F),X=F)}function it(F,At,Tt){F?(Nt(o.POLYGON_OFFSET_FILL),(tt!==At||P!==Tt)&&(o.polygonOffset(At,Tt),tt=At,P=Tt)):kt(o.POLYGON_OFFSET_FILL)}function St(F){F?Nt(o.SCISSOR_TEST):kt(o.SCISSOR_TEST)}function vt(F){F===void 0&&(F=o.TEXTURE0+q-1),L!==F&&(o.activeTexture(F),L=F)}function gt(F,At,Tt){Tt===void 0&&(L===null?Tt=o.TEXTURE0+q-1:Tt=L);let jt=W[Tt];jt===void 0&&(jt={type:void 0,texture:void 0},W[Tt]=jt),(jt.type!==F||jt.texture!==At)&&(L!==Tt&&(o.activeTexture(Tt),L=Tt),o.bindTexture(F,At||It[F]),jt.type=F,jt.texture=At)}function Ht(){const F=W[L];F!==void 0&&F.type!==void 0&&(o.bindTexture(F.type,null),F.type=void 0,F.texture=void 0)}function Rt(){try{o.compressedTexImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Ut(){try{o.compressedTexImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function qt(){try{o.texSubImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function ie(){try{o.texSubImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function _t(){try{o.compressedTexSubImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function ye(){try{o.compressedTexSubImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function le(){try{o.texStorage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Kt(){try{o.texStorage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Dt(){try{o.texImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function wt(){try{o.texImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Xt(F){mt.equals(F)===!1&&(o.scissor(F.x,F.y,F.z,F.w),mt.copy(F))}function Se(F){xt.equals(F)===!1&&(o.viewport(F.x,F.y,F.z,F.w),xt.copy(F))}function He(F,At){let Tt=_.get(At);Tt===void 0&&(Tt=new WeakMap,_.set(At,Tt));let jt=Tt.get(F);jt===void 0&&(jt=o.getUniformBlockIndex(At,F.name),Tt.set(F,jt))}function re(F,At){const jt=_.get(At).get(F);g.get(At)!==jt&&(o.uniformBlockBinding(At,jt,F.__bindingPointIndex),g.set(At,jt))}function yt(){o.disable(o.BLEND),o.disable(o.CULL_FACE),o.disable(o.DEPTH_TEST),o.disable(o.POLYGON_OFFSET_FILL),o.disable(o.SCISSOR_TEST),o.disable(o.STENCIL_TEST),o.disable(o.SAMPLE_ALPHA_TO_COVERAGE),o.blendEquation(o.FUNC_ADD),o.blendFunc(o.ONE,o.ZERO),o.blendFuncSeparate(o.ONE,o.ZERO,o.ONE,o.ZERO),o.blendColor(0,0,0,0),o.colorMask(!0,!0,!0,!0),o.clearColor(0,0,0,0),o.depthMask(!0),o.depthFunc(o.LESS),o.clearDepth(1),o.stencilMask(4294967295),o.stencilFunc(o.ALWAYS,0,4294967295),o.stencilOp(o.KEEP,o.KEEP,o.KEEP),o.clearStencil(0),o.cullFace(o.BACK),o.frontFace(o.CCW),o.polygonOffset(0,0),o.activeTexture(o.TEXTURE0),o.bindFramebuffer(o.FRAMEBUFFER,null),r===!0&&(o.bindFramebuffer(o.DRAW_FRAMEBUFFER,null),o.bindFramebuffer(o.READ_FRAMEBUFFER,null)),o.useProgram(null),o.lineWidth(1),o.scissor(0,0,o.canvas.width,o.canvas.height),o.viewport(0,0,o.canvas.width,o.canvas.height),x={},L=null,W={},y={},b=new WeakMap,A=[],M=null,v=!1,D=null,T=null,z=null,V=null,B=null,O=null,ut=null,C=new Me(0,0,0),N=0,rt=!1,dt=null,Et=null,X=null,tt=null,P=null,mt.set(0,0,o.canvas.width,o.canvas.height),xt.set(0,0,o.canvas.width,o.canvas.height),h.reset(),m.reset(),p.reset()}return{buffers:{color:h,depth:m,stencil:p},enable:Nt,disable:kt,bindFramebuffer:ue,drawBuffers:et,useProgram:un,setBlending:Pt,setMaterial:Pe,setFlipSided:ee,setCullFace:U,setLineWidth:R,setPolygonOffset:it,setScissorTest:St,activeTexture:vt,bindTexture:gt,unbindTexture:Ht,compressedTexImage2D:Rt,compressedTexImage3D:Ut,texImage2D:Dt,texImage3D:wt,updateUBOMapping:He,uniformBlockBinding:re,texStorage2D:le,texStorage3D:Kt,texSubImage2D:qt,texSubImage3D:ie,compressedTexSubImage2D:_t,compressedTexSubImage3D:ye,scissor:Xt,viewport:Se,reset:yt}}function uA(o,e,i,r,l,c,d){const h=l.isWebGL2,m=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,p=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),g=new WeakMap;let _;const x=new WeakMap;let y=!1;try{y=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function b(U,R){return y?new OffscreenCanvas(U,R):Su("canvas")}function A(U,R,it,St){let vt=1;if((U.width>St||U.height>St)&&(vt=St/Math.max(U.width,U.height)),vt<1||R===!0)if(typeof HTMLImageElement<"u"&&U instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&U instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&U instanceof ImageBitmap){const gt=R?Ah:Math.floor,Ht=gt(vt*U.width),Rt=gt(vt*U.height);_===void 0&&(_=b(Ht,Rt));const Ut=it?b(Ht,Rt):_;return Ut.width=Ht,Ut.height=Rt,Ut.getContext("2d").drawImage(U,0,0,Ht,Rt),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+U.width+"x"+U.height+") to ("+Ht+"x"+Rt+")."),Ut}else return"data"in U&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+U.width+"x"+U.height+")."),U;return U}function M(U){return d_(U.width)&&d_(U.height)}function v(U){return h?!1:U.wrapS!==vi||U.wrapT!==vi||U.minFilter!==wn&&U.minFilter!==oi}function D(U,R){return U.generateMipmaps&&R&&U.minFilter!==wn&&U.minFilter!==oi}function T(U){o.generateMipmap(U)}function z(U,R,it,St,vt=!1){if(h===!1)return R;if(U!==null){if(o[U]!==void 0)return o[U];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+U+"'")}let gt=R;if(R===o.RED&&(it===o.FLOAT&&(gt=o.R32F),it===o.HALF_FLOAT&&(gt=o.R16F),it===o.UNSIGNED_BYTE&&(gt=o.R8)),R===o.RED_INTEGER&&(it===o.UNSIGNED_BYTE&&(gt=o.R8UI),it===o.UNSIGNED_SHORT&&(gt=o.R16UI),it===o.UNSIGNED_INT&&(gt=o.R32UI),it===o.BYTE&&(gt=o.R8I),it===o.SHORT&&(gt=o.R16I),it===o.INT&&(gt=o.R32I)),R===o.RG&&(it===o.FLOAT&&(gt=o.RG32F),it===o.HALF_FLOAT&&(gt=o.RG16F),it===o.UNSIGNED_BYTE&&(gt=o.RG8)),R===o.RGBA){const Ht=vt?mu:Ue.getTransfer(St);it===o.FLOAT&&(gt=o.RGBA32F),it===o.HALF_FLOAT&&(gt=o.RGBA16F),it===o.UNSIGNED_BYTE&&(gt=Ht===Fe?o.SRGB8_ALPHA8:o.RGBA8),it===o.UNSIGNED_SHORT_4_4_4_4&&(gt=o.RGBA4),it===o.UNSIGNED_SHORT_5_5_5_1&&(gt=o.RGB5_A1)}return(gt===o.R16F||gt===o.R32F||gt===o.RG16F||gt===o.RG32F||gt===o.RGBA16F||gt===o.RGBA32F)&&e.get("EXT_color_buffer_float"),gt}function V(U,R,it){return D(U,it)===!0||U.isFramebufferTexture&&U.minFilter!==wn&&U.minFilter!==oi?Math.log2(Math.max(R.width,R.height))+1:U.mipmaps!==void 0&&U.mipmaps.length>0?U.mipmaps.length:U.isCompressedTexture&&Array.isArray(U.image)?R.mipmaps.length:1}function B(U){return U===wn||U===Ig||U===Pf?o.NEAREST:o.LINEAR}function O(U){const R=U.target;R.removeEventListener("dispose",O),C(R),R.isVideoTexture&&g.delete(R)}function ut(U){const R=U.target;R.removeEventListener("dispose",ut),rt(R)}function C(U){const R=r.get(U);if(R.__webglInit===void 0)return;const it=U.source,St=x.get(it);if(St){const vt=St[R.__cacheKey];vt.usedTimes--,vt.usedTimes===0&&N(U),Object.keys(St).length===0&&x.delete(it)}r.remove(U)}function N(U){const R=r.get(U);o.deleteTexture(R.__webglTexture);const it=U.source,St=x.get(it);delete St[R.__cacheKey],d.memory.textures--}function rt(U){const R=U.texture,it=r.get(U),St=r.get(R);if(St.__webglTexture!==void 0&&(o.deleteTexture(St.__webglTexture),d.memory.textures--),U.depthTexture&&U.depthTexture.dispose(),U.isWebGLCubeRenderTarget)for(let vt=0;vt<6;vt++){if(Array.isArray(it.__webglFramebuffer[vt]))for(let gt=0;gt<it.__webglFramebuffer[vt].length;gt++)o.deleteFramebuffer(it.__webglFramebuffer[vt][gt]);else o.deleteFramebuffer(it.__webglFramebuffer[vt]);it.__webglDepthbuffer&&o.deleteRenderbuffer(it.__webglDepthbuffer[vt])}else{if(Array.isArray(it.__webglFramebuffer))for(let vt=0;vt<it.__webglFramebuffer.length;vt++)o.deleteFramebuffer(it.__webglFramebuffer[vt]);else o.deleteFramebuffer(it.__webglFramebuffer);if(it.__webglDepthbuffer&&o.deleteRenderbuffer(it.__webglDepthbuffer),it.__webglMultisampledFramebuffer&&o.deleteFramebuffer(it.__webglMultisampledFramebuffer),it.__webglColorRenderbuffer)for(let vt=0;vt<it.__webglColorRenderbuffer.length;vt++)it.__webglColorRenderbuffer[vt]&&o.deleteRenderbuffer(it.__webglColorRenderbuffer[vt]);it.__webglDepthRenderbuffer&&o.deleteRenderbuffer(it.__webglDepthRenderbuffer)}if(U.isWebGLMultipleRenderTargets)for(let vt=0,gt=R.length;vt<gt;vt++){const Ht=r.get(R[vt]);Ht.__webglTexture&&(o.deleteTexture(Ht.__webglTexture),d.memory.textures--),r.remove(R[vt])}r.remove(R),r.remove(U)}let dt=0;function Et(){dt=0}function X(){const U=dt;return U>=l.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+U+" texture units while this GPU supports only "+l.maxTextures),dt+=1,U}function tt(U){const R=[];return R.push(U.wrapS),R.push(U.wrapT),R.push(U.wrapR||0),R.push(U.magFilter),R.push(U.minFilter),R.push(U.anisotropy),R.push(U.internalFormat),R.push(U.format),R.push(U.type),R.push(U.generateMipmaps),R.push(U.premultiplyAlpha),R.push(U.flipY),R.push(U.unpackAlignment),R.push(U.colorSpace),R.join()}function P(U,R){const it=r.get(U);if(U.isVideoTexture&&Pe(U),U.isRenderTargetTexture===!1&&U.version>0&&it.__version!==U.version){const St=U.image;if(St===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(St.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{mt(it,U,R);return}}i.bindTexture(o.TEXTURE_2D,it.__webglTexture,o.TEXTURE0+R)}function q(U,R){const it=r.get(U);if(U.version>0&&it.__version!==U.version){mt(it,U,R);return}i.bindTexture(o.TEXTURE_2D_ARRAY,it.__webglTexture,o.TEXTURE0+R)}function J(U,R){const it=r.get(U);if(U.version>0&&it.__version!==U.version){mt(it,U,R);return}i.bindTexture(o.TEXTURE_3D,it.__webglTexture,o.TEXTURE0+R)}function lt(U,R){const it=r.get(U);if(U.version>0&&it.__version!==U.version){xt(it,U,R);return}i.bindTexture(o.TEXTURE_CUBE_MAP,it.__webglTexture,o.TEXTURE0+R)}const ft={[yh]:o.REPEAT,[vi]:o.CLAMP_TO_EDGE,[Eh]:o.MIRRORED_REPEAT},L={[wn]:o.NEAREST,[Ig]:o.NEAREST_MIPMAP_NEAREST,[Pf]:o.NEAREST_MIPMAP_LINEAR,[oi]:o.LINEAR,[Wx]:o.LINEAR_MIPMAP_NEAREST,[Ao]:o.LINEAR_MIPMAP_LINEAR},W={[nM]:o.NEVER,[lM]:o.ALWAYS,[iM]:o.LESS,[vv]:o.LEQUAL,[aM]:o.EQUAL,[oM]:o.GEQUAL,[rM]:o.GREATER,[sM]:o.NOTEQUAL};function G(U,R,it){if(it?(o.texParameteri(U,o.TEXTURE_WRAP_S,ft[R.wrapS]),o.texParameteri(U,o.TEXTURE_WRAP_T,ft[R.wrapT]),(U===o.TEXTURE_3D||U===o.TEXTURE_2D_ARRAY)&&o.texParameteri(U,o.TEXTURE_WRAP_R,ft[R.wrapR]),o.texParameteri(U,o.TEXTURE_MAG_FILTER,L[R.magFilter]),o.texParameteri(U,o.TEXTURE_MIN_FILTER,L[R.minFilter])):(o.texParameteri(U,o.TEXTURE_WRAP_S,o.CLAMP_TO_EDGE),o.texParameteri(U,o.TEXTURE_WRAP_T,o.CLAMP_TO_EDGE),(U===o.TEXTURE_3D||U===o.TEXTURE_2D_ARRAY)&&o.texParameteri(U,o.TEXTURE_WRAP_R,o.CLAMP_TO_EDGE),(R.wrapS!==vi||R.wrapT!==vi)&&console.warn("THREE.WebGLRenderer: Texture is not power of two. Texture.wrapS and Texture.wrapT should be set to THREE.ClampToEdgeWrapping."),o.texParameteri(U,o.TEXTURE_MAG_FILTER,B(R.magFilter)),o.texParameteri(U,o.TEXTURE_MIN_FILTER,B(R.minFilter)),R.minFilter!==wn&&R.minFilter!==oi&&console.warn("THREE.WebGLRenderer: Texture is not power of two. Texture.minFilter should be set to THREE.NearestFilter or THREE.LinearFilter.")),R.compareFunction&&(o.texParameteri(U,o.TEXTURE_COMPARE_MODE,o.COMPARE_REF_TO_TEXTURE),o.texParameteri(U,o.TEXTURE_COMPARE_FUNC,W[R.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){const St=e.get("EXT_texture_filter_anisotropic");if(R.magFilter===wn||R.minFilter!==Pf&&R.minFilter!==Ao||R.type===Oa&&e.has("OES_texture_float_linear")===!1||h===!1&&R.type===Ro&&e.has("OES_texture_half_float_linear")===!1)return;(R.anisotropy>1||r.get(R).__currentAnisotropy)&&(o.texParameterf(U,St.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(R.anisotropy,l.getMaxAnisotropy())),r.get(R).__currentAnisotropy=R.anisotropy)}}function K(U,R){let it=!1;U.__webglInit===void 0&&(U.__webglInit=!0,R.addEventListener("dispose",O));const St=R.source;let vt=x.get(St);vt===void 0&&(vt={},x.set(St,vt));const gt=tt(R);if(gt!==U.__cacheKey){vt[gt]===void 0&&(vt[gt]={texture:o.createTexture(),usedTimes:0},d.memory.textures++,it=!0),vt[gt].usedTimes++;const Ht=vt[U.__cacheKey];Ht!==void 0&&(vt[U.__cacheKey].usedTimes--,Ht.usedTimes===0&&N(R)),U.__cacheKey=gt,U.__webglTexture=vt[gt].texture}return it}function mt(U,R,it){let St=o.TEXTURE_2D;(R.isDataArrayTexture||R.isCompressedArrayTexture)&&(St=o.TEXTURE_2D_ARRAY),R.isData3DTexture&&(St=o.TEXTURE_3D);const vt=K(U,R),gt=R.source;i.bindTexture(St,U.__webglTexture,o.TEXTURE0+it);const Ht=r.get(gt);if(gt.version!==Ht.__version||vt===!0){i.activeTexture(o.TEXTURE0+it);const Rt=Ue.getPrimaries(Ue.workingColorSpace),Ut=R.colorSpace===ui?null:Ue.getPrimaries(R.colorSpace),qt=R.colorSpace===ui||Rt===Ut?o.NONE:o.BROWSER_DEFAULT_WEBGL;o.pixelStorei(o.UNPACK_FLIP_Y_WEBGL,R.flipY),o.pixelStorei(o.UNPACK_PREMULTIPLY_ALPHA_WEBGL,R.premultiplyAlpha),o.pixelStorei(o.UNPACK_ALIGNMENT,R.unpackAlignment),o.pixelStorei(o.UNPACK_COLORSPACE_CONVERSION_WEBGL,qt);const ie=v(R)&&M(R.image)===!1;let _t=A(R.image,ie,!1,l.maxTextureSize);_t=ee(R,_t);const ye=M(_t)||h,le=c.convert(R.format,R.colorSpace);let Kt=c.convert(R.type),Dt=z(R.internalFormat,le,Kt,R.colorSpace,R.isVideoTexture);G(St,R,ye);let wt;const Xt=R.mipmaps,Se=h&&R.isVideoTexture!==!0&&Dt!==mv,He=Ht.__version===void 0||vt===!0,re=V(R,_t,ye);if(R.isDepthTexture)Dt=o.DEPTH_COMPONENT,h?R.type===Oa?Dt=o.DEPTH_COMPONENT32F:R.type===Na?Dt=o.DEPTH_COMPONENT24:R.type===fr?Dt=o.DEPTH24_STENCIL8:Dt=o.DEPTH_COMPONENT16:R.type===Oa&&console.error("WebGLRenderer: Floating point depth texture requires WebGL2."),R.format===hr&&Dt===o.DEPTH_COMPONENT&&R.type!==wh&&R.type!==Na&&(console.warn("THREE.WebGLRenderer: Use UnsignedShortType or UnsignedIntType for DepthFormat DepthTexture."),R.type=Na,Kt=c.convert(R.type)),R.format===_s&&Dt===o.DEPTH_COMPONENT&&(Dt=o.DEPTH_STENCIL,R.type!==fr&&(console.warn("THREE.WebGLRenderer: Use UnsignedInt248Type for DepthStencilFormat DepthTexture."),R.type=fr,Kt=c.convert(R.type))),He&&(Se?i.texStorage2D(o.TEXTURE_2D,1,Dt,_t.width,_t.height):i.texImage2D(o.TEXTURE_2D,0,Dt,_t.width,_t.height,0,le,Kt,null));else if(R.isDataTexture)if(Xt.length>0&&ye){Se&&He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,Xt[0].width,Xt[0].height);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],Se?i.texSubImage2D(o.TEXTURE_2D,yt,0,0,wt.width,wt.height,le,Kt,wt.data):i.texImage2D(o.TEXTURE_2D,yt,Dt,wt.width,wt.height,0,le,Kt,wt.data);R.generateMipmaps=!1}else Se?(He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,_t.width,_t.height),i.texSubImage2D(o.TEXTURE_2D,0,0,0,_t.width,_t.height,le,Kt,_t.data)):i.texImage2D(o.TEXTURE_2D,0,Dt,_t.width,_t.height,0,le,Kt,_t.data);else if(R.isCompressedTexture)if(R.isCompressedArrayTexture){Se&&He&&i.texStorage3D(o.TEXTURE_2D_ARRAY,re,Dt,Xt[0].width,Xt[0].height,_t.depth);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],R.format!==Si?le!==null?Se?i.compressedTexSubImage3D(o.TEXTURE_2D_ARRAY,yt,0,0,0,wt.width,wt.height,_t.depth,le,wt.data,0,0):i.compressedTexImage3D(o.TEXTURE_2D_ARRAY,yt,Dt,wt.width,wt.height,_t.depth,0,wt.data,0,0):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):Se?i.texSubImage3D(o.TEXTURE_2D_ARRAY,yt,0,0,0,wt.width,wt.height,_t.depth,le,Kt,wt.data):i.texImage3D(o.TEXTURE_2D_ARRAY,yt,Dt,wt.width,wt.height,_t.depth,0,le,Kt,wt.data)}else{Se&&He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,Xt[0].width,Xt[0].height);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],R.format!==Si?le!==null?Se?i.compressedTexSubImage2D(o.TEXTURE_2D,yt,0,0,wt.width,wt.height,le,wt.data):i.compressedTexImage2D(o.TEXTURE_2D,yt,Dt,wt.width,wt.height,0,wt.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):Se?i.texSubImage2D(o.TEXTURE_2D,yt,0,0,wt.width,wt.height,le,Kt,wt.data):i.texImage2D(o.TEXTURE_2D,yt,Dt,wt.width,wt.height,0,le,Kt,wt.data)}else if(R.isDataArrayTexture)Se?(He&&i.texStorage3D(o.TEXTURE_2D_ARRAY,re,Dt,_t.width,_t.height,_t.depth),i.texSubImage3D(o.TEXTURE_2D_ARRAY,0,0,0,0,_t.width,_t.height,_t.depth,le,Kt,_t.data)):i.texImage3D(o.TEXTURE_2D_ARRAY,0,Dt,_t.width,_t.height,_t.depth,0,le,Kt,_t.data);else if(R.isData3DTexture)Se?(He&&i.texStorage3D(o.TEXTURE_3D,re,Dt,_t.width,_t.height,_t.depth),i.texSubImage3D(o.TEXTURE_3D,0,0,0,0,_t.width,_t.height,_t.depth,le,Kt,_t.data)):i.texImage3D(o.TEXTURE_3D,0,Dt,_t.width,_t.height,_t.depth,0,le,Kt,_t.data);else if(R.isFramebufferTexture){if(He)if(Se)i.texStorage2D(o.TEXTURE_2D,re,Dt,_t.width,_t.height);else{let yt=_t.width,F=_t.height;for(let At=0;At<re;At++)i.texImage2D(o.TEXTURE_2D,At,Dt,yt,F,0,le,Kt,null),yt>>=1,F>>=1}}else if(Xt.length>0&&ye){Se&&He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,Xt[0].width,Xt[0].height);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],Se?i.texSubImage2D(o.TEXTURE_2D,yt,0,0,le,Kt,wt):i.texImage2D(o.TEXTURE_2D,yt,Dt,le,Kt,wt);R.generateMipmaps=!1}else Se?(He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,_t.width,_t.height),i.texSubImage2D(o.TEXTURE_2D,0,0,0,le,Kt,_t)):i.texImage2D(o.TEXTURE_2D,0,Dt,le,Kt,_t);D(R,ye)&&T(St),Ht.__version=gt.version,R.onUpdate&&R.onUpdate(R)}U.__version=R.version}function xt(U,R,it){if(R.image.length!==6)return;const St=K(U,R),vt=R.source;i.bindTexture(o.TEXTURE_CUBE_MAP,U.__webglTexture,o.TEXTURE0+it);const gt=r.get(vt);if(vt.version!==gt.__version||St===!0){i.activeTexture(o.TEXTURE0+it);const Ht=Ue.getPrimaries(Ue.workingColorSpace),Rt=R.colorSpace===ui?null:Ue.getPrimaries(R.colorSpace),Ut=R.colorSpace===ui||Ht===Rt?o.NONE:o.BROWSER_DEFAULT_WEBGL;o.pixelStorei(o.UNPACK_FLIP_Y_WEBGL,R.flipY),o.pixelStorei(o.UNPACK_PREMULTIPLY_ALPHA_WEBGL,R.premultiplyAlpha),o.pixelStorei(o.UNPACK_ALIGNMENT,R.unpackAlignment),o.pixelStorei(o.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ut);const qt=R.isCompressedTexture||R.image[0].isCompressedTexture,ie=R.image[0]&&R.image[0].isDataTexture,_t=[];for(let yt=0;yt<6;yt++)!qt&&!ie?_t[yt]=A(R.image[yt],!1,!0,l.maxCubemapSize):_t[yt]=ie?R.image[yt].image:R.image[yt],_t[yt]=ee(R,_t[yt]);const ye=_t[0],le=M(ye)||h,Kt=c.convert(R.format,R.colorSpace),Dt=c.convert(R.type),wt=z(R.internalFormat,Kt,Dt,R.colorSpace),Xt=h&&R.isVideoTexture!==!0,Se=gt.__version===void 0||St===!0;let He=V(R,ye,le);G(o.TEXTURE_CUBE_MAP,R,le);let re;if(qt){Xt&&Se&&i.texStorage2D(o.TEXTURE_CUBE_MAP,He,wt,ye.width,ye.height);for(let yt=0;yt<6;yt++){re=_t[yt].mipmaps;for(let F=0;F<re.length;F++){const At=re[F];R.format!==Si?Kt!==null?Xt?i.compressedTexSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,0,0,At.width,At.height,Kt,At.data):i.compressedTexImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,wt,At.width,At.height,0,At.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,0,0,At.width,At.height,Kt,Dt,At.data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,wt,At.width,At.height,0,Kt,Dt,At.data)}}}else{re=R.mipmaps,Xt&&Se&&(re.length>0&&He++,i.texStorage2D(o.TEXTURE_CUBE_MAP,He,wt,_t[0].width,_t[0].height));for(let yt=0;yt<6;yt++)if(ie){Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,0,0,_t[yt].width,_t[yt].height,Kt,Dt,_t[yt].data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,wt,_t[yt].width,_t[yt].height,0,Kt,Dt,_t[yt].data);for(let F=0;F<re.length;F++){const Tt=re[F].image[yt].image;Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,0,0,Tt.width,Tt.height,Kt,Dt,Tt.data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,wt,Tt.width,Tt.height,0,Kt,Dt,Tt.data)}}else{Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,0,0,Kt,Dt,_t[yt]):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,wt,Kt,Dt,_t[yt]);for(let F=0;F<re.length;F++){const At=re[F];Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,0,0,Kt,Dt,At.image[yt]):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,wt,Kt,Dt,At.image[yt])}}}D(R,le)&&T(o.TEXTURE_CUBE_MAP),gt.__version=vt.version,R.onUpdate&&R.onUpdate(R)}U.__version=R.version}function Mt(U,R,it,St,vt,gt){const Ht=c.convert(it.format,it.colorSpace),Rt=c.convert(it.type),Ut=z(it.internalFormat,Ht,Rt,it.colorSpace);if(!r.get(R).__hasExternalTextures){const ie=Math.max(1,R.width>>gt),_t=Math.max(1,R.height>>gt);vt===o.TEXTURE_3D||vt===o.TEXTURE_2D_ARRAY?i.texImage3D(vt,gt,Ut,ie,_t,R.depth,0,Ht,Rt,null):i.texImage2D(vt,gt,Ut,ie,_t,0,Ht,Rt,null)}i.bindFramebuffer(o.FRAMEBUFFER,U),Pt(R)?m.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,St,vt,r.get(it).__webglTexture,0,Qt(R)):(vt===o.TEXTURE_2D||vt>=o.TEXTURE_CUBE_MAP_POSITIVE_X&&vt<=o.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&o.framebufferTexture2D(o.FRAMEBUFFER,St,vt,r.get(it).__webglTexture,gt),i.bindFramebuffer(o.FRAMEBUFFER,null)}function It(U,R,it){if(o.bindRenderbuffer(o.RENDERBUFFER,U),R.depthBuffer&&!R.stencilBuffer){let St=h===!0?o.DEPTH_COMPONENT24:o.DEPTH_COMPONENT16;if(it||Pt(R)){const vt=R.depthTexture;vt&&vt.isDepthTexture&&(vt.type===Oa?St=o.DEPTH_COMPONENT32F:vt.type===Na&&(St=o.DEPTH_COMPONENT24));const gt=Qt(R);Pt(R)?m.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,gt,St,R.width,R.height):o.renderbufferStorageMultisample(o.RENDERBUFFER,gt,St,R.width,R.height)}else o.renderbufferStorage(o.RENDERBUFFER,St,R.width,R.height);o.framebufferRenderbuffer(o.FRAMEBUFFER,o.DEPTH_ATTACHMENT,o.RENDERBUFFER,U)}else if(R.depthBuffer&&R.stencilBuffer){const St=Qt(R);it&&Pt(R)===!1?o.renderbufferStorageMultisample(o.RENDERBUFFER,St,o.DEPTH24_STENCIL8,R.width,R.height):Pt(R)?m.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,St,o.DEPTH24_STENCIL8,R.width,R.height):o.renderbufferStorage(o.RENDERBUFFER,o.DEPTH_STENCIL,R.width,R.height),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.DEPTH_STENCIL_ATTACHMENT,o.RENDERBUFFER,U)}else{const St=R.isWebGLMultipleRenderTargets===!0?R.texture:[R.texture];for(let vt=0;vt<St.length;vt++){const gt=St[vt],Ht=c.convert(gt.format,gt.colorSpace),Rt=c.convert(gt.type),Ut=z(gt.internalFormat,Ht,Rt,gt.colorSpace),qt=Qt(R);it&&Pt(R)===!1?o.renderbufferStorageMultisample(o.RENDERBUFFER,qt,Ut,R.width,R.height):Pt(R)?m.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,qt,Ut,R.width,R.height):o.renderbufferStorage(o.RENDERBUFFER,Ut,R.width,R.height)}}o.bindRenderbuffer(o.RENDERBUFFER,null)}function Nt(U,R){if(R&&R.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(i.bindFramebuffer(o.FRAMEBUFFER,U),!(R.depthTexture&&R.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");(!r.get(R.depthTexture).__webglTexture||R.depthTexture.image.width!==R.width||R.depthTexture.image.height!==R.height)&&(R.depthTexture.image.width=R.width,R.depthTexture.image.height=R.height,R.depthTexture.needsUpdate=!0),P(R.depthTexture,0);const St=r.get(R.depthTexture).__webglTexture,vt=Qt(R);if(R.depthTexture.format===hr)Pt(R)?m.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,o.DEPTH_ATTACHMENT,o.TEXTURE_2D,St,0,vt):o.framebufferTexture2D(o.FRAMEBUFFER,o.DEPTH_ATTACHMENT,o.TEXTURE_2D,St,0);else if(R.depthTexture.format===_s)Pt(R)?m.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,o.DEPTH_STENCIL_ATTACHMENT,o.TEXTURE_2D,St,0,vt):o.framebufferTexture2D(o.FRAMEBUFFER,o.DEPTH_STENCIL_ATTACHMENT,o.TEXTURE_2D,St,0);else throw new Error("Unknown depthTexture format")}function kt(U){const R=r.get(U),it=U.isWebGLCubeRenderTarget===!0;if(U.depthTexture&&!R.__autoAllocateDepthBuffer){if(it)throw new Error("target.depthTexture not supported in Cube render targets");Nt(R.__webglFramebuffer,U)}else if(it){R.__webglDepthbuffer=[];for(let St=0;St<6;St++)i.bindFramebuffer(o.FRAMEBUFFER,R.__webglFramebuffer[St]),R.__webglDepthbuffer[St]=o.createRenderbuffer(),It(R.__webglDepthbuffer[St],U,!1)}else i.bindFramebuffer(o.FRAMEBUFFER,R.__webglFramebuffer),R.__webglDepthbuffer=o.createRenderbuffer(),It(R.__webglDepthbuffer,U,!1);i.bindFramebuffer(o.FRAMEBUFFER,null)}function ue(U,R,it){const St=r.get(U);R!==void 0&&Mt(St.__webglFramebuffer,U,U.texture,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,0),it!==void 0&&kt(U)}function et(U){const R=U.texture,it=r.get(U),St=r.get(R);U.addEventListener("dispose",ut),U.isWebGLMultipleRenderTargets!==!0&&(St.__webglTexture===void 0&&(St.__webglTexture=o.createTexture()),St.__version=R.version,d.memory.textures++);const vt=U.isWebGLCubeRenderTarget===!0,gt=U.isWebGLMultipleRenderTargets===!0,Ht=M(U)||h;if(vt){it.__webglFramebuffer=[];for(let Rt=0;Rt<6;Rt++)if(h&&R.mipmaps&&R.mipmaps.length>0){it.__webglFramebuffer[Rt]=[];for(let Ut=0;Ut<R.mipmaps.length;Ut++)it.__webglFramebuffer[Rt][Ut]=o.createFramebuffer()}else it.__webglFramebuffer[Rt]=o.createFramebuffer()}else{if(h&&R.mipmaps&&R.mipmaps.length>0){it.__webglFramebuffer=[];for(let Rt=0;Rt<R.mipmaps.length;Rt++)it.__webglFramebuffer[Rt]=o.createFramebuffer()}else it.__webglFramebuffer=o.createFramebuffer();if(gt)if(l.drawBuffers){const Rt=U.texture;for(let Ut=0,qt=Rt.length;Ut<qt;Ut++){const ie=r.get(Rt[Ut]);ie.__webglTexture===void 0&&(ie.__webglTexture=o.createTexture(),d.memory.textures++)}}else console.warn("THREE.WebGLRenderer: WebGLMultipleRenderTargets can only be used with WebGL2 or WEBGL_draw_buffers extension.");if(h&&U.samples>0&&Pt(U)===!1){const Rt=gt?R:[R];it.__webglMultisampledFramebuffer=o.createFramebuffer(),it.__webglColorRenderbuffer=[],i.bindFramebuffer(o.FRAMEBUFFER,it.__webglMultisampledFramebuffer);for(let Ut=0;Ut<Rt.length;Ut++){const qt=Rt[Ut];it.__webglColorRenderbuffer[Ut]=o.createRenderbuffer(),o.bindRenderbuffer(o.RENDERBUFFER,it.__webglColorRenderbuffer[Ut]);const ie=c.convert(qt.format,qt.colorSpace),_t=c.convert(qt.type),ye=z(qt.internalFormat,ie,_t,qt.colorSpace,U.isXRRenderTarget===!0),le=Qt(U);o.renderbufferStorageMultisample(o.RENDERBUFFER,le,ye,U.width,U.height),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+Ut,o.RENDERBUFFER,it.__webglColorRenderbuffer[Ut])}o.bindRenderbuffer(o.RENDERBUFFER,null),U.depthBuffer&&(it.__webglDepthRenderbuffer=o.createRenderbuffer(),It(it.__webglDepthRenderbuffer,U,!0)),i.bindFramebuffer(o.FRAMEBUFFER,null)}}if(vt){i.bindTexture(o.TEXTURE_CUBE_MAP,St.__webglTexture),G(o.TEXTURE_CUBE_MAP,R,Ht);for(let Rt=0;Rt<6;Rt++)if(h&&R.mipmaps&&R.mipmaps.length>0)for(let Ut=0;Ut<R.mipmaps.length;Ut++)Mt(it.__webglFramebuffer[Rt][Ut],U,R,o.COLOR_ATTACHMENT0,o.TEXTURE_CUBE_MAP_POSITIVE_X+Rt,Ut);else Mt(it.__webglFramebuffer[Rt],U,R,o.COLOR_ATTACHMENT0,o.TEXTURE_CUBE_MAP_POSITIVE_X+Rt,0);D(R,Ht)&&T(o.TEXTURE_CUBE_MAP),i.unbindTexture()}else if(gt){const Rt=U.texture;for(let Ut=0,qt=Rt.length;Ut<qt;Ut++){const ie=Rt[Ut],_t=r.get(ie);i.bindTexture(o.TEXTURE_2D,_t.__webglTexture),G(o.TEXTURE_2D,ie,Ht),Mt(it.__webglFramebuffer,U,ie,o.COLOR_ATTACHMENT0+Ut,o.TEXTURE_2D,0),D(ie,Ht)&&T(o.TEXTURE_2D)}i.unbindTexture()}else{let Rt=o.TEXTURE_2D;if((U.isWebGL3DRenderTarget||U.isWebGLArrayRenderTarget)&&(h?Rt=U.isWebGL3DRenderTarget?o.TEXTURE_3D:o.TEXTURE_2D_ARRAY:console.error("THREE.WebGLTextures: THREE.Data3DTexture and THREE.DataArrayTexture only supported with WebGL2.")),i.bindTexture(Rt,St.__webglTexture),G(Rt,R,Ht),h&&R.mipmaps&&R.mipmaps.length>0)for(let Ut=0;Ut<R.mipmaps.length;Ut++)Mt(it.__webglFramebuffer[Ut],U,R,o.COLOR_ATTACHMENT0,Rt,Ut);else Mt(it.__webglFramebuffer,U,R,o.COLOR_ATTACHMENT0,Rt,0);D(R,Ht)&&T(Rt),i.unbindTexture()}U.depthBuffer&&kt(U)}function un(U){const R=M(U)||h,it=U.isWebGLMultipleRenderTargets===!0?U.texture:[U.texture];for(let St=0,vt=it.length;St<vt;St++){const gt=it[St];if(D(gt,R)){const Ht=U.isWebGLCubeRenderTarget?o.TEXTURE_CUBE_MAP:o.TEXTURE_2D,Rt=r.get(gt).__webglTexture;i.bindTexture(Ht,Rt),T(Ht),i.unbindTexture()}}}function Ft(U){if(h&&U.samples>0&&Pt(U)===!1){const R=U.isWebGLMultipleRenderTargets?U.texture:[U.texture],it=U.width,St=U.height;let vt=o.COLOR_BUFFER_BIT;const gt=[],Ht=U.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT,Rt=r.get(U),Ut=U.isWebGLMultipleRenderTargets===!0;if(Ut)for(let qt=0;qt<R.length;qt++)i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglMultisampledFramebuffer),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.RENDERBUFFER,null),i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglFramebuffer),o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.TEXTURE_2D,null,0);i.bindFramebuffer(o.READ_FRAMEBUFFER,Rt.__webglMultisampledFramebuffer),i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Rt.__webglFramebuffer);for(let qt=0;qt<R.length;qt++){gt.push(o.COLOR_ATTACHMENT0+qt),U.depthBuffer&&gt.push(Ht);const ie=Rt.__ignoreDepthValues!==void 0?Rt.__ignoreDepthValues:!1;if(ie===!1&&(U.depthBuffer&&(vt|=o.DEPTH_BUFFER_BIT),U.stencilBuffer&&(vt|=o.STENCIL_BUFFER_BIT)),Ut&&o.framebufferRenderbuffer(o.READ_FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.RENDERBUFFER,Rt.__webglColorRenderbuffer[qt]),ie===!0&&(o.invalidateFramebuffer(o.READ_FRAMEBUFFER,[Ht]),o.invalidateFramebuffer(o.DRAW_FRAMEBUFFER,[Ht])),Ut){const _t=r.get(R[qt]).__webglTexture;o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,_t,0)}o.blitFramebuffer(0,0,it,St,0,0,it,St,vt,o.NEAREST),p&&o.invalidateFramebuffer(o.READ_FRAMEBUFFER,gt)}if(i.bindFramebuffer(o.READ_FRAMEBUFFER,null),i.bindFramebuffer(o.DRAW_FRAMEBUFFER,null),Ut)for(let qt=0;qt<R.length;qt++){i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglMultisampledFramebuffer),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.RENDERBUFFER,Rt.__webglColorRenderbuffer[qt]);const ie=r.get(R[qt]).__webglTexture;i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglFramebuffer),o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.TEXTURE_2D,ie,0)}i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Rt.__webglMultisampledFramebuffer)}}function Qt(U){return Math.min(l.maxSamples,U.samples)}function Pt(U){const R=r.get(U);return h&&U.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&R.__useRenderToTexture!==!1}function Pe(U){const R=d.render.frame;g.get(U)!==R&&(g.set(U,R),U.update())}function ee(U,R){const it=U.colorSpace,St=U.format,vt=U.type;return U.isCompressedTexture===!0||U.isVideoTexture===!0||U.format===Th||it!==$i&&it!==ui&&(Ue.getTransfer(it)===Fe?h===!1?e.has("EXT_sRGB")===!0&&St===Si?(U.format=Th,U.minFilter=oi,U.generateMipmaps=!1):R=xv.sRGBToLinear(R):(St!==Si||vt!==Ia)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",it)),R}this.allocateTextureUnit=X,this.resetTextureUnits=Et,this.setTexture2D=P,this.setTexture2DArray=q,this.setTexture3D=J,this.setTextureCube=lt,this.rebindTextures=ue,this.setupRenderTarget=et,this.updateRenderTargetMipmap=un,this.updateMultisampleRenderTarget=Ft,this.setupDepthRenderbuffer=kt,this.setupFrameBufferTexture=Mt,this.useMultisampledRTT=Pt}function cA(o,e,i){const r=i.isWebGL2;function l(c,d=ui){let h;const m=Ue.getTransfer(d);if(c===Ia)return o.UNSIGNED_BYTE;if(c===cv)return o.UNSIGNED_SHORT_4_4_4_4;if(c===fv)return o.UNSIGNED_SHORT_5_5_5_1;if(c===kx)return o.BYTE;if(c===qx)return o.SHORT;if(c===wh)return o.UNSIGNED_SHORT;if(c===uv)return o.INT;if(c===Na)return o.UNSIGNED_INT;if(c===Oa)return o.FLOAT;if(c===Ro)return r?o.HALF_FLOAT:(h=e.get("OES_texture_half_float"),h!==null?h.HALF_FLOAT_OES:null);if(c===Yx)return o.ALPHA;if(c===Si)return o.RGBA;if(c===jx)return o.LUMINANCE;if(c===Zx)return o.LUMINANCE_ALPHA;if(c===hr)return o.DEPTH_COMPONENT;if(c===_s)return o.DEPTH_STENCIL;if(c===Th)return h=e.get("EXT_sRGB"),h!==null?h.SRGB_ALPHA_EXT:null;if(c===Kx)return o.RED;if(c===hv)return o.RED_INTEGER;if(c===Qx)return o.RG;if(c===dv)return o.RG_INTEGER;if(c===pv)return o.RGBA_INTEGER;if(c===Bf||c===If||c===Ff||c===Hf)if(m===Fe)if(h=e.get("WEBGL_compressed_texture_s3tc_srgb"),h!==null){if(c===Bf)return h.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(c===If)return h.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(c===Ff)return h.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(c===Hf)return h.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(h=e.get("WEBGL_compressed_texture_s3tc"),h!==null){if(c===Bf)return h.COMPRESSED_RGB_S3TC_DXT1_EXT;if(c===If)return h.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(c===Ff)return h.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(c===Hf)return h.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(c===Fg||c===Hg||c===Gg||c===Vg)if(h=e.get("WEBGL_compressed_texture_pvrtc"),h!==null){if(c===Fg)return h.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(c===Hg)return h.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(c===Gg)return h.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(c===Vg)return h.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(c===mv)return h=e.get("WEBGL_compressed_texture_etc1"),h!==null?h.COMPRESSED_RGB_ETC1_WEBGL:null;if(c===Xg||c===Wg)if(h=e.get("WEBGL_compressed_texture_etc"),h!==null){if(c===Xg)return m===Fe?h.COMPRESSED_SRGB8_ETC2:h.COMPRESSED_RGB8_ETC2;if(c===Wg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:h.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(c===kg||c===qg||c===Yg||c===jg||c===Zg||c===Kg||c===Qg||c===Jg||c===$g||c===t_||c===e_||c===n_||c===i_||c===a_)if(h=e.get("WEBGL_compressed_texture_astc"),h!==null){if(c===kg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:h.COMPRESSED_RGBA_ASTC_4x4_KHR;if(c===qg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:h.COMPRESSED_RGBA_ASTC_5x4_KHR;if(c===Yg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:h.COMPRESSED_RGBA_ASTC_5x5_KHR;if(c===jg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:h.COMPRESSED_RGBA_ASTC_6x5_KHR;if(c===Zg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:h.COMPRESSED_RGBA_ASTC_6x6_KHR;if(c===Kg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:h.COMPRESSED_RGBA_ASTC_8x5_KHR;if(c===Qg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:h.COMPRESSED_RGBA_ASTC_8x6_KHR;if(c===Jg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:h.COMPRESSED_RGBA_ASTC_8x8_KHR;if(c===$g)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:h.COMPRESSED_RGBA_ASTC_10x5_KHR;if(c===t_)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:h.COMPRESSED_RGBA_ASTC_10x6_KHR;if(c===e_)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:h.COMPRESSED_RGBA_ASTC_10x8_KHR;if(c===n_)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:h.COMPRESSED_RGBA_ASTC_10x10_KHR;if(c===i_)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:h.COMPRESSED_RGBA_ASTC_12x10_KHR;if(c===a_)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:h.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(c===Gf||c===r_||c===s_)if(h=e.get("EXT_texture_compression_bptc"),h!==null){if(c===Gf)return m===Fe?h.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:h.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(c===r_)return h.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(c===s_)return h.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(c===Jx||c===o_||c===l_||c===u_)if(h=e.get("EXT_texture_compression_rgtc"),h!==null){if(c===Gf)return h.COMPRESSED_RED_RGTC1_EXT;if(c===o_)return h.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(c===l_)return h.COMPRESSED_RED_GREEN_RGTC2_EXT;if(c===u_)return h.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return c===fr?r?o.UNSIGNED_INT_24_8:(h=e.get("WEBGL_depth_texture"),h!==null?h.UNSIGNED_INT_24_8_WEBGL:null):o[c]!==void 0?o[c]:null}return{convert:l}}class fA extends li{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e}}class fu extends Tn{constructor(){super(),this.isGroup=!0,this.type="Group"}}const hA={type:"move"};class fh{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new fu,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new fu,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new Y,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new Y),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new fu,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new Y,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new Y),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const i=this._hand;if(i)for(const r of e.hand.values())this._getHandJoint(i,r)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,i,r){let l=null,c=null,d=null;const h=this._targetRay,m=this._grip,p=this._hand;if(e&&i.session.visibilityState!=="visible-blurred"){if(p&&e.hand){d=!0;for(const A of e.hand.values()){const M=i.getJointPose(A,r),v=this._getHandJoint(p,A);M!==null&&(v.matrix.fromArray(M.transform.matrix),v.matrix.decompose(v.position,v.rotation,v.scale),v.matrixWorldNeedsUpdate=!0,v.jointRadius=M.radius),v.visible=M!==null}const g=p.joints["index-finger-tip"],_=p.joints["thumb-tip"],x=g.position.distanceTo(_.position),y=.02,b=.005;p.inputState.pinching&&x>y+b?(p.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!p.inputState.pinching&&x<=y-b&&(p.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else m!==null&&e.gripSpace&&(c=i.getPose(e.gripSpace,r),c!==null&&(m.matrix.fromArray(c.transform.matrix),m.matrix.decompose(m.position,m.rotation,m.scale),m.matrixWorldNeedsUpdate=!0,c.linearVelocity?(m.hasLinearVelocity=!0,m.linearVelocity.copy(c.linearVelocity)):m.hasLinearVelocity=!1,c.angularVelocity?(m.hasAngularVelocity=!0,m.angularVelocity.copy(c.angularVelocity)):m.hasAngularVelocity=!1));h!==null&&(l=i.getPose(e.targetRaySpace,r),l===null&&c!==null&&(l=c),l!==null&&(h.matrix.fromArray(l.transform.matrix),h.matrix.decompose(h.position,h.rotation,h.scale),h.matrixWorldNeedsUpdate=!0,l.linearVelocity?(h.hasLinearVelocity=!0,h.linearVelocity.copy(l.linearVelocity)):h.hasLinearVelocity=!1,l.angularVelocity?(h.hasAngularVelocity=!0,h.angularVelocity.copy(l.angularVelocity)):h.hasAngularVelocity=!1,this.dispatchEvent(hA)))}return h!==null&&(h.visible=l!==null),m!==null&&(m.visible=c!==null),p!==null&&(p.visible=d!==null),this}_getHandJoint(e,i){if(e.joints[i.jointName]===void 0){const r=new fu;r.matrixAutoUpdate=!1,r.visible=!1,e.joints[i.jointName]=r,e.add(r)}return e.joints[i.jointName]}}class dA extends Ss{constructor(e,i){super();const r=this;let l=null,c=1,d=null,h="local-floor",m=1,p=null,g=null,_=null,x=null,y=null,b=null;const A=i.getContextAttributes();let M=null,v=null;const D=[],T=[],z=new ge;let V=null;const B=new li;B.layers.enable(1),B.viewport=new Ve;const O=new li;O.layers.enable(2),O.viewport=new Ve;const ut=[B,O],C=new fA;C.layers.enable(1),C.layers.enable(2);let N=null,rt=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(G){let K=D[G];return K===void 0&&(K=new fh,D[G]=K),K.getTargetRaySpace()},this.getControllerGrip=function(G){let K=D[G];return K===void 0&&(K=new fh,D[G]=K),K.getGripSpace()},this.getHand=function(G){let K=D[G];return K===void 0&&(K=new fh,D[G]=K),K.getHandSpace()};function dt(G){const K=T.indexOf(G.inputSource);if(K===-1)return;const mt=D[K];mt!==void 0&&(mt.update(G.inputSource,G.frame,p||d),mt.dispatchEvent({type:G.type,data:G.inputSource}))}function Et(){l.removeEventListener("select",dt),l.removeEventListener("selectstart",dt),l.removeEventListener("selectend",dt),l.removeEventListener("squeeze",dt),l.removeEventListener("squeezestart",dt),l.removeEventListener("squeezeend",dt),l.removeEventListener("end",Et),l.removeEventListener("inputsourceschange",X);for(let G=0;G<D.length;G++){const K=T[G];K!==null&&(T[G]=null,D[G].disconnect(K))}N=null,rt=null,e.setRenderTarget(M),y=null,x=null,_=null,l=null,v=null,W.stop(),r.isPresenting=!1,e.setPixelRatio(V),e.setSize(z.width,z.height,!1),r.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(G){c=G,r.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(G){h=G,r.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return p||d},this.setReferenceSpace=function(G){p=G},this.getBaseLayer=function(){return x!==null?x:y},this.getBinding=function(){return _},this.getFrame=function(){return b},this.getSession=function(){return l},this.setSession=async function(G){if(l=G,l!==null){if(M=e.getRenderTarget(),l.addEventListener("select",dt),l.addEventListener("selectstart",dt),l.addEventListener("selectend",dt),l.addEventListener("squeeze",dt),l.addEventListener("squeezestart",dt),l.addEventListener("squeezeend",dt),l.addEventListener("end",Et),l.addEventListener("inputsourceschange",X),A.xrCompatible!==!0&&await i.makeXRCompatible(),V=e.getPixelRatio(),e.getSize(z),l.renderState.layers===void 0||e.capabilities.isWebGL2===!1){const K={antialias:l.renderState.layers===void 0?A.antialias:!0,alpha:!0,depth:A.depth,stencil:A.stencil,framebufferScaleFactor:c};y=new XRWebGLLayer(l,i,K),l.updateRenderState({baseLayer:y}),e.setPixelRatio(1),e.setSize(y.framebufferWidth,y.framebufferHeight,!1),v=new pr(y.framebufferWidth,y.framebufferHeight,{format:Si,type:Ia,colorSpace:e.outputColorSpace,stencilBuffer:A.stencil})}else{let K=null,mt=null,xt=null;A.depth&&(xt=A.stencil?i.DEPTH24_STENCIL8:i.DEPTH_COMPONENT24,K=A.stencil?_s:hr,mt=A.stencil?fr:Na);const Mt={colorFormat:i.RGBA8,depthFormat:xt,scaleFactor:c};_=new XRWebGLBinding(l,i),x=_.createProjectionLayer(Mt),l.updateRenderState({layers:[x]}),e.setPixelRatio(1),e.setSize(x.textureWidth,x.textureHeight,!1),v=new pr(x.textureWidth,x.textureHeight,{format:Si,type:Ia,depthTexture:new Nv(x.textureWidth,x.textureHeight,mt,void 0,void 0,void 0,void 0,void 0,void 0,K),stencilBuffer:A.stencil,colorSpace:e.outputColorSpace,samples:A.antialias?4:0});const It=e.properties.get(v);It.__ignoreDepthValues=x.ignoreDepthValues}v.isXRRenderTarget=!0,this.setFoveation(m),p=null,d=await l.requestReferenceSpace(h),W.setContext(l),W.start(),r.isPresenting=!0,r.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(l!==null)return l.environmentBlendMode};function X(G){for(let K=0;K<G.removed.length;K++){const mt=G.removed[K],xt=T.indexOf(mt);xt>=0&&(T[xt]=null,D[xt].disconnect(mt))}for(let K=0;K<G.added.length;K++){const mt=G.added[K];let xt=T.indexOf(mt);if(xt===-1){for(let It=0;It<D.length;It++)if(It>=T.length){T.push(mt),xt=It;break}else if(T[It]===null){T[It]=mt,xt=It;break}if(xt===-1)break}const Mt=D[xt];Mt&&Mt.connect(mt)}}const tt=new Y,P=new Y;function q(G,K,mt){tt.setFromMatrixPosition(K.matrixWorld),P.setFromMatrixPosition(mt.matrixWorld);const xt=tt.distanceTo(P),Mt=K.projectionMatrix.elements,It=mt.projectionMatrix.elements,Nt=Mt[14]/(Mt[10]-1),kt=Mt[14]/(Mt[10]+1),ue=(Mt[9]+1)/Mt[5],et=(Mt[9]-1)/Mt[5],un=(Mt[8]-1)/Mt[0],Ft=(It[8]+1)/It[0],Qt=Nt*un,Pt=Nt*Ft,Pe=xt/(-un+Ft),ee=Pe*-un;K.matrixWorld.decompose(G.position,G.quaternion,G.scale),G.translateX(ee),G.translateZ(Pe),G.matrixWorld.compose(G.position,G.quaternion,G.scale),G.matrixWorldInverse.copy(G.matrixWorld).invert();const U=Nt+Pe,R=kt+Pe,it=Qt-ee,St=Pt+(xt-ee),vt=ue*kt/R*U,gt=et*kt/R*U;G.projectionMatrix.makePerspective(it,St,vt,gt,U,R),G.projectionMatrixInverse.copy(G.projectionMatrix).invert()}function J(G,K){K===null?G.matrixWorld.copy(G.matrix):G.matrixWorld.multiplyMatrices(K.matrixWorld,G.matrix),G.matrixWorldInverse.copy(G.matrixWorld).invert()}this.updateCamera=function(G){if(l===null)return;C.near=O.near=B.near=G.near,C.far=O.far=B.far=G.far,(N!==C.near||rt!==C.far)&&(l.updateRenderState({depthNear:C.near,depthFar:C.far}),N=C.near,rt=C.far);const K=G.parent,mt=C.cameras;J(C,K);for(let xt=0;xt<mt.length;xt++)J(mt[xt],K);mt.length===2?q(C,B,O):C.projectionMatrix.copy(B.projectionMatrix),lt(G,C,K)};function lt(G,K,mt){mt===null?G.matrix.copy(K.matrixWorld):(G.matrix.copy(mt.matrixWorld),G.matrix.invert(),G.matrix.multiply(K.matrixWorld)),G.matrix.decompose(G.position,G.quaternion,G.scale),G.updateMatrixWorld(!0),G.projectionMatrix.copy(K.projectionMatrix),G.projectionMatrixInverse.copy(K.projectionMatrixInverse),G.isPerspectiveCamera&&(G.fov=bh*2*Math.atan(1/G.projectionMatrix.elements[5]),G.zoom=1)}this.getCamera=function(){return C},this.getFoveation=function(){if(!(x===null&&y===null))return m},this.setFoveation=function(G){m=G,x!==null&&(x.fixedFoveation=G),y!==null&&y.fixedFoveation!==void 0&&(y.fixedFoveation=G)};let ft=null;function L(G,K){if(g=K.getViewerPose(p||d),b=K,g!==null){const mt=g.views;y!==null&&(e.setRenderTargetFramebuffer(v,y.framebuffer),e.setRenderTarget(v));let xt=!1;mt.length!==C.cameras.length&&(C.cameras.length=0,xt=!0);for(let Mt=0;Mt<mt.length;Mt++){const It=mt[Mt];let Nt=null;if(y!==null)Nt=y.getViewport(It);else{const ue=_.getViewSubImage(x,It);Nt=ue.viewport,Mt===0&&(e.setRenderTargetTextures(v,ue.colorTexture,x.ignoreDepthValues?void 0:ue.depthStencilTexture),e.setRenderTarget(v))}let kt=ut[Mt];kt===void 0&&(kt=new li,kt.layers.enable(Mt),kt.viewport=new Ve,ut[Mt]=kt),kt.matrix.fromArray(It.transform.matrix),kt.matrix.decompose(kt.position,kt.quaternion,kt.scale),kt.projectionMatrix.fromArray(It.projectionMatrix),kt.projectionMatrixInverse.copy(kt.projectionMatrix).invert(),kt.viewport.set(Nt.x,Nt.y,Nt.width,Nt.height),Mt===0&&(C.matrix.copy(kt.matrix),C.matrix.decompose(C.position,C.quaternion,C.scale)),xt===!0&&C.cameras.push(kt)}}for(let mt=0;mt<D.length;mt++){const xt=T[mt],Mt=D[mt];xt!==null&&Mt!==void 0&&Mt.update(xt,K,p||d)}ft&&ft(G,K),K.detectedPlanes&&r.dispatchEvent({type:"planesdetected",data:K}),b=null}const W=new Lv;W.setAnimationLoop(L),this.setAnimationLoop=function(G){ft=G},this.dispose=function(){}}}function pA(o,e){function i(M,v){M.matrixAutoUpdate===!0&&M.updateMatrix(),v.value.copy(M.matrix)}function r(M,v){v.color.getRGB(M.fogColor.value,Cv(o)),v.isFog?(M.fogNear.value=v.near,M.fogFar.value=v.far):v.isFogExp2&&(M.fogDensity.value=v.density)}function l(M,v,D,T,z){v.isMeshBasicMaterial||v.isMeshLambertMaterial?c(M,v):v.isMeshToonMaterial?(c(M,v),_(M,v)):v.isMeshPhongMaterial?(c(M,v),g(M,v)):v.isMeshStandardMaterial?(c(M,v),x(M,v),v.isMeshPhysicalMaterial&&y(M,v,z)):v.isMeshMatcapMaterial?(c(M,v),b(M,v)):v.isMeshDepthMaterial?c(M,v):v.isMeshDistanceMaterial?(c(M,v),A(M,v)):v.isMeshNormalMaterial?c(M,v):v.isLineBasicMaterial?(d(M,v),v.isLineDashedMaterial&&h(M,v)):v.isPointsMaterial?m(M,v,D,T):v.isSpriteMaterial?p(M,v):v.isShadowMaterial?(M.color.value.copy(v.color),M.opacity.value=v.opacity):v.isShaderMaterial&&(v.uniformsNeedUpdate=!1)}function c(M,v){M.opacity.value=v.opacity,v.color&&M.diffuse.value.copy(v.color),v.emissive&&M.emissive.value.copy(v.emissive).multiplyScalar(v.emissiveIntensity),v.map&&(M.map.value=v.map,i(v.map,M.mapTransform)),v.alphaMap&&(M.alphaMap.value=v.alphaMap,i(v.alphaMap,M.alphaMapTransform)),v.bumpMap&&(M.bumpMap.value=v.bumpMap,i(v.bumpMap,M.bumpMapTransform),M.bumpScale.value=v.bumpScale,v.side===Fn&&(M.bumpScale.value*=-1)),v.normalMap&&(M.normalMap.value=v.normalMap,i(v.normalMap,M.normalMapTransform),M.normalScale.value.copy(v.normalScale),v.side===Fn&&M.normalScale.value.negate()),v.displacementMap&&(M.displacementMap.value=v.displacementMap,i(v.displacementMap,M.displacementMapTransform),M.displacementScale.value=v.displacementScale,M.displacementBias.value=v.displacementBias),v.emissiveMap&&(M.emissiveMap.value=v.emissiveMap,i(v.emissiveMap,M.emissiveMapTransform)),v.specularMap&&(M.specularMap.value=v.specularMap,i(v.specularMap,M.specularMapTransform)),v.alphaTest>0&&(M.alphaTest.value=v.alphaTest);const D=e.get(v).envMap;if(D&&(M.envMap.value=D,M.flipEnvMap.value=D.isCubeTexture&&D.isRenderTargetTexture===!1?-1:1,M.reflectivity.value=v.reflectivity,M.ior.value=v.ior,M.refractionRatio.value=v.refractionRatio),v.lightMap){M.lightMap.value=v.lightMap;const T=o._useLegacyLights===!0?Math.PI:1;M.lightMapIntensity.value=v.lightMapIntensity*T,i(v.lightMap,M.lightMapTransform)}v.aoMap&&(M.aoMap.value=v.aoMap,M.aoMapIntensity.value=v.aoMapIntensity,i(v.aoMap,M.aoMapTransform))}function d(M,v){M.diffuse.value.copy(v.color),M.opacity.value=v.opacity,v.map&&(M.map.value=v.map,i(v.map,M.mapTransform))}function h(M,v){M.dashSize.value=v.dashSize,M.totalSize.value=v.dashSize+v.gapSize,M.scale.value=v.scale}function m(M,v,D,T){M.diffuse.value.copy(v.color),M.opacity.value=v.opacity,M.size.value=v.size*D,M.scale.value=T*.5,v.map&&(M.map.value=v.map,i(v.map,M.uvTransform)),v.alphaMap&&(M.alphaMap.value=v.alphaMap,i(v.alphaMap,M.alphaMapTransform)),v.alphaTest>0&&(M.alphaTest.value=v.alphaTest)}function p(M,v){M.diffuse.value.copy(v.color),M.opacity.value=v.opacity,M.rotation.value=v.rotation,v.map&&(M.map.value=v.map,i(v.map,M.mapTransform)),v.alphaMap&&(M.alphaMap.value=v.alphaMap,i(v.alphaMap,M.alphaMapTransform)),v.alphaTest>0&&(M.alphaTest.value=v.alphaTest)}function g(M,v){M.specular.value.copy(v.specular),M.shininess.value=Math.max(v.shininess,1e-4)}function _(M,v){v.gradientMap&&(M.gradientMap.value=v.gradientMap)}function x(M,v){M.metalness.value=v.metalness,v.metalnessMap&&(M.metalnessMap.value=v.metalnessMap,i(v.metalnessMap,M.metalnessMapTransform)),M.roughness.value=v.roughness,v.roughnessMap&&(M.roughnessMap.value=v.roughnessMap,i(v.roughnessMap,M.roughnessMapTransform)),e.get(v).envMap&&(M.envMapIntensity.value=v.envMapIntensity)}function y(M,v,D){M.ior.value=v.ior,v.sheen>0&&(M.sheenColor.value.copy(v.sheenColor).multiplyScalar(v.sheen),M.sheenRoughness.value=v.sheenRoughness,v.sheenColorMap&&(M.sheenColorMap.value=v.sheenColorMap,i(v.sheenColorMap,M.sheenColorMapTransform)),v.sheenRoughnessMap&&(M.sheenRoughnessMap.value=v.sheenRoughnessMap,i(v.sheenRoughnessMap,M.sheenRoughnessMapTransform))),v.clearcoat>0&&(M.clearcoat.value=v.clearcoat,M.clearcoatRoughness.value=v.clearcoatRoughness,v.clearcoatMap&&(M.clearcoatMap.value=v.clearcoatMap,i(v.clearcoatMap,M.clearcoatMapTransform)),v.clearcoatRoughnessMap&&(M.clearcoatRoughnessMap.value=v.clearcoatRoughnessMap,i(v.clearcoatRoughnessMap,M.clearcoatRoughnessMapTransform)),v.clearcoatNormalMap&&(M.clearcoatNormalMap.value=v.clearcoatNormalMap,i(v.clearcoatNormalMap,M.clearcoatNormalMapTransform),M.clearcoatNormalScale.value.copy(v.clearcoatNormalScale),v.side===Fn&&M.clearcoatNormalScale.value.negate())),v.iridescence>0&&(M.iridescence.value=v.iridescence,M.iridescenceIOR.value=v.iridescenceIOR,M.iridescenceThicknessMinimum.value=v.iridescenceThicknessRange[0],M.iridescenceThicknessMaximum.value=v.iridescenceThicknessRange[1],v.iridescenceMap&&(M.iridescenceMap.value=v.iridescenceMap,i(v.iridescenceMap,M.iridescenceMapTransform)),v.iridescenceThicknessMap&&(M.iridescenceThicknessMap.value=v.iridescenceThicknessMap,i(v.iridescenceThicknessMap,M.iridescenceThicknessMapTransform))),v.transmission>0&&(M.transmission.value=v.transmission,M.transmissionSamplerMap.value=D.texture,M.transmissionSamplerSize.value.set(D.width,D.height),v.transmissionMap&&(M.transmissionMap.value=v.transmissionMap,i(v.transmissionMap,M.transmissionMapTransform)),M.thickness.value=v.thickness,v.thicknessMap&&(M.thicknessMap.value=v.thicknessMap,i(v.thicknessMap,M.thicknessMapTransform)),M.attenuationDistance.value=v.attenuationDistance,M.attenuationColor.value.copy(v.attenuationColor)),v.anisotropy>0&&(M.anisotropyVector.value.set(v.anisotropy*Math.cos(v.anisotropyRotation),v.anisotropy*Math.sin(v.anisotropyRotation)),v.anisotropyMap&&(M.anisotropyMap.value=v.anisotropyMap,i(v.anisotropyMap,M.anisotropyMapTransform))),M.specularIntensity.value=v.specularIntensity,M.specularColor.value.copy(v.specularColor),v.specularColorMap&&(M.specularColorMap.value=v.specularColorMap,i(v.specularColorMap,M.specularColorMapTransform)),v.specularIntensityMap&&(M.specularIntensityMap.value=v.specularIntensityMap,i(v.specularIntensityMap,M.specularIntensityMapTransform))}function b(M,v){v.matcap&&(M.matcap.value=v.matcap)}function A(M,v){const D=e.get(v).light;M.referencePosition.value.setFromMatrixPosition(D.matrixWorld),M.nearDistance.value=D.shadow.camera.near,M.farDistance.value=D.shadow.camera.far}return{refreshFogUniforms:r,refreshMaterialUniforms:l}}function mA(o,e,i,r){let l={},c={},d=[];const h=i.isWebGL2?o.getParameter(o.MAX_UNIFORM_BUFFER_BINDINGS):0;function m(D,T){const z=T.program;r.uniformBlockBinding(D,z)}function p(D,T){let z=l[D.id];z===void 0&&(b(D),z=g(D),l[D.id]=z,D.addEventListener("dispose",M));const V=T.program;r.updateUBOMapping(D,V);const B=e.render.frame;c[D.id]!==B&&(x(D),c[D.id]=B)}function g(D){const T=_();D.__bindingPointIndex=T;const z=o.createBuffer(),V=D.__size,B=D.usage;return o.bindBuffer(o.UNIFORM_BUFFER,z),o.bufferData(o.UNIFORM_BUFFER,V,B),o.bindBuffer(o.UNIFORM_BUFFER,null),o.bindBufferBase(o.UNIFORM_BUFFER,T,z),z}function _(){for(let D=0;D<h;D++)if(d.indexOf(D)===-1)return d.push(D),D;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function x(D){const T=l[D.id],z=D.uniforms,V=D.__cache;o.bindBuffer(o.UNIFORM_BUFFER,T);for(let B=0,O=z.length;B<O;B++){const ut=Array.isArray(z[B])?z[B]:[z[B]];for(let C=0,N=ut.length;C<N;C++){const rt=ut[C];if(y(rt,B,C,V)===!0){const dt=rt.__offset,Et=Array.isArray(rt.value)?rt.value:[rt.value];let X=0;for(let tt=0;tt<Et.length;tt++){const P=Et[tt],q=A(P);typeof P=="number"||typeof P=="boolean"?(rt.__data[0]=P,o.bufferSubData(o.UNIFORM_BUFFER,dt+X,rt.__data)):P.isMatrix3?(rt.__data[0]=P.elements[0],rt.__data[1]=P.elements[1],rt.__data[2]=P.elements[2],rt.__data[3]=0,rt.__data[4]=P.elements[3],rt.__data[5]=P.elements[4],rt.__data[6]=P.elements[5],rt.__data[7]=0,rt.__data[8]=P.elements[6],rt.__data[9]=P.elements[7],rt.__data[10]=P.elements[8],rt.__data[11]=0):(P.toArray(rt.__data,X),X+=q.storage/Float32Array.BYTES_PER_ELEMENT)}o.bufferSubData(o.UNIFORM_BUFFER,dt,rt.__data)}}}o.bindBuffer(o.UNIFORM_BUFFER,null)}function y(D,T,z,V){const B=D.value,O=T+"_"+z;if(V[O]===void 0)return typeof B=="number"||typeof B=="boolean"?V[O]=B:V[O]=B.clone(),!0;{const ut=V[O];if(typeof B=="number"||typeof B=="boolean"){if(ut!==B)return V[O]=B,!0}else if(ut.equals(B)===!1)return ut.copy(B),!0}return!1}function b(D){const T=D.uniforms;let z=0;const V=16;for(let O=0,ut=T.length;O<ut;O++){const C=Array.isArray(T[O])?T[O]:[T[O]];for(let N=0,rt=C.length;N<rt;N++){const dt=C[N],Et=Array.isArray(dt.value)?dt.value:[dt.value];for(let X=0,tt=Et.length;X<tt;X++){const P=Et[X],q=A(P),J=z%V;J!==0&&V-J<q.boundary&&(z+=V-J),dt.__data=new Float32Array(q.storage/Float32Array.BYTES_PER_ELEMENT),dt.__offset=z,z+=q.storage}}}const B=z%V;return B>0&&(z+=V-B),D.__size=z,D.__cache={},this}function A(D){const T={boundary:0,storage:0};return typeof D=="number"||typeof D=="boolean"?(T.boundary=4,T.storage=4):D.isVector2?(T.boundary=8,T.storage=8):D.isVector3||D.isColor?(T.boundary=16,T.storage=12):D.isVector4?(T.boundary=16,T.storage=16):D.isMatrix3?(T.boundary=48,T.storage=48):D.isMatrix4?(T.boundary=64,T.storage=64):D.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",D),T}function M(D){const T=D.target;T.removeEventListener("dispose",M);const z=d.indexOf(T.__bindingPointIndex);d.splice(z,1),o.deleteBuffer(l[T.id]),delete l[T.id],delete c[T.id]}function v(){for(const D in l)o.deleteBuffer(l[D]);d=[],l={},c={}}return{bind:m,update:p,dispose:v}}class gA{constructor(e={}){const{canvas:i=cM(),context:r=null,depth:l=!0,stencil:c=!0,alpha:d=!1,antialias:h=!1,premultipliedAlpha:m=!0,preserveDrawingBuffer:p=!1,powerPreference:g="default",failIfMajorPerformanceCaveat:_=!1}=e;this.isWebGLRenderer=!0;let x;r!==null?x=r.getContextAttributes().alpha:x=d;const y=new Uint32Array(4),b=new Int32Array(4);let A=null,M=null;const v=[],D=[];this.domElement=i,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=vn,this._useLegacyLights=!1,this.toneMapping=Ba,this.toneMappingExposure=1;const T=this;let z=!1,V=0,B=0,O=null,ut=-1,C=null;const N=new Ve,rt=new Ve;let dt=null;const Et=new Me(0);let X=0,tt=i.width,P=i.height,q=1,J=null,lt=null;const ft=new Ve(0,0,tt,P),L=new Ve(0,0,tt,P);let W=!1;const G=new Uh;let K=!1,mt=!1,xt=null;const Mt=new rn,It=new ge,Nt=new Y,kt={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};function ue(){return O===null?q:1}let et=r;function un(w,j){for(let at=0;at<w.length;at++){const st=w[at],nt=i.getContext(st,j);if(nt!==null)return nt}return null}try{const w={alpha:!0,depth:l,stencil:c,antialias:h,premultipliedAlpha:m,preserveDrawingBuffer:p,powerPreference:g,failIfMajorPerformanceCaveat:_};if("setAttribute"in i&&i.setAttribute("data-engine",`three.js r${Ch}`),i.addEventListener("webglcontextlost",yt,!1),i.addEventListener("webglcontextrestored",F,!1),i.addEventListener("webglcontextcreationerror",At,!1),et===null){const j=["webgl2","webgl","experimental-webgl"];if(T.isWebGL1Renderer===!0&&j.shift(),et=un(j,w),et===null)throw un(j)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}typeof WebGLRenderingContext<"u"&&et instanceof WebGLRenderingContext&&console.warn("THREE.WebGLRenderer: WebGL 1 support was deprecated in r153 and will be removed in r163."),et.getShaderPrecisionFormat===void 0&&(et.getShaderPrecisionFormat=function(){return{rangeMin:1,rangeMax:1,precision:1}})}catch(w){throw console.error("THREE.WebGLRenderer: "+w.message),w}let Ft,Qt,Pt,Pe,ee,U,R,it,St,vt,gt,Ht,Rt,Ut,qt,ie,_t,ye,le,Kt,Dt,wt,Xt,Se;function He(){Ft=new bT(et),Qt=new ST(et,Ft,e),Ft.init(Qt),wt=new cA(et,Ft,Qt),Pt=new lA(et,Ft,Qt),Pe=new CT(et),ee=new jb,U=new uA(et,Ft,Pt,ee,Qt,wt,Pe),R=new MT(T),it=new TT(T),St=new PM(et,Qt),Xt=new _T(et,Ft,St,Qt),vt=new AT(et,St,Pe,Xt),gt=new UT(et,vt,St,Pe),le=new LT(et,Qt,U),ie=new xT(ee),Ht=new Yb(T,R,it,Ft,Qt,Xt,ie),Rt=new pA(T,ee),Ut=new Kb,qt=new nA(Ft,Qt),ye=new gT(T,R,it,Pt,gt,x,m),_t=new oA(T,gt,Qt),Se=new mA(et,Pe,Qt,Pt),Kt=new vT(et,Ft,Pe,Qt),Dt=new RT(et,Ft,Pe,Qt),Pe.programs=Ht.programs,T.capabilities=Qt,T.extensions=Ft,T.properties=ee,T.renderLists=Ut,T.shadowMap=_t,T.state=Pt,T.info=Pe}He();const re=new dA(T,et);this.xr=re,this.getContext=function(){return et},this.getContextAttributes=function(){return et.getContextAttributes()},this.forceContextLoss=function(){const w=Ft.get("WEBGL_lose_context");w&&w.loseContext()},this.forceContextRestore=function(){const w=Ft.get("WEBGL_lose_context");w&&w.restoreContext()},this.getPixelRatio=function(){return q},this.setPixelRatio=function(w){w!==void 0&&(q=w,this.setSize(tt,P,!1))},this.getSize=function(w){return w.set(tt,P)},this.setSize=function(w,j,at=!0){if(re.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}tt=w,P=j,i.width=Math.floor(w*q),i.height=Math.floor(j*q),at===!0&&(i.style.width=w+"px",i.style.height=j+"px"),this.setViewport(0,0,w,j)},this.getDrawingBufferSize=function(w){return w.set(tt*q,P*q).floor()},this.setDrawingBufferSize=function(w,j,at){tt=w,P=j,q=at,i.width=Math.floor(w*at),i.height=Math.floor(j*at),this.setViewport(0,0,w,j)},this.getCurrentViewport=function(w){return w.copy(N)},this.getViewport=function(w){return w.copy(ft)},this.setViewport=function(w,j,at,st){w.isVector4?ft.set(w.x,w.y,w.z,w.w):ft.set(w,j,at,st),Pt.viewport(N.copy(ft).multiplyScalar(q).floor())},this.getScissor=function(w){return w.copy(L)},this.setScissor=function(w,j,at,st){w.isVector4?L.set(w.x,w.y,w.z,w.w):L.set(w,j,at,st),Pt.scissor(rt.copy(L).multiplyScalar(q).floor())},this.getScissorTest=function(){return W},this.setScissorTest=function(w){Pt.setScissorTest(W=w)},this.setOpaqueSort=function(w){J=w},this.setTransparentSort=function(w){lt=w},this.getClearColor=function(w){return w.copy(ye.getClearColor())},this.setClearColor=function(){ye.setClearColor.apply(ye,arguments)},this.getClearAlpha=function(){return ye.getClearAlpha()},this.setClearAlpha=function(){ye.setClearAlpha.apply(ye,arguments)},this.clear=function(w=!0,j=!0,at=!0){let st=0;if(w){let nt=!1;if(O!==null){const Ct=O.texture.format;nt=Ct===pv||Ct===dv||Ct===hv}if(nt){const Ct=O.texture.type,Ot=Ct===Ia||Ct===Na||Ct===wh||Ct===fr||Ct===cv||Ct===fv,Wt=ye.getClearColor(),Yt=ye.getClearAlpha(),Bt=Wt.r,Jt=Wt.g,$t=Wt.b;Ot?(y[0]=Bt,y[1]=Jt,y[2]=$t,y[3]=Yt,et.clearBufferuiv(et.COLOR,0,y)):(b[0]=Bt,b[1]=Jt,b[2]=$t,b[3]=Yt,et.clearBufferiv(et.COLOR,0,b))}else st|=et.COLOR_BUFFER_BIT}j&&(st|=et.DEPTH_BUFFER_BIT),at&&(st|=et.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),et.clear(st)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){i.removeEventListener("webglcontextlost",yt,!1),i.removeEventListener("webglcontextrestored",F,!1),i.removeEventListener("webglcontextcreationerror",At,!1),Ut.dispose(),qt.dispose(),ee.dispose(),R.dispose(),it.dispose(),gt.dispose(),Xt.dispose(),Se.dispose(),Ht.dispose(),re.dispose(),re.removeEventListener("sessionstart",qe),re.removeEventListener("sessionend",Ce),xt&&(xt.dispose(),xt=null),cn.stop()};function yt(w){w.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),z=!0}function F(){console.log("THREE.WebGLRenderer: Context Restored."),z=!1;const w=Pe.autoReset,j=_t.enabled,at=_t.autoUpdate,st=_t.needsUpdate,nt=_t.type;He(),Pe.autoReset=w,_t.enabled=j,_t.autoUpdate=at,_t.needsUpdate=st,_t.type=nt}function At(w){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",w.statusMessage)}function Tt(w){const j=w.target;j.removeEventListener("dispose",Tt),jt(j)}function jt(w){Gt(w),ee.remove(w)}function Gt(w){const j=ee.get(w).programs;j!==void 0&&(j.forEach(function(at){Ht.releaseProgram(at)}),w.isShaderMaterial&&Ht.releaseShaderCache(w))}this.renderBufferDirect=function(w,j,at,st,nt,Ct){j===null&&(j=kt);const Ot=nt.isMesh&&nt.matrixWorld.determinant()<0,Wt=Sn(w,j,at,st,nt);Pt.setMaterial(st,Ot);let Yt=at.index,Bt=1;if(st.wireframe===!0){if(Yt=vt.getWireframeAttribute(at),Yt===void 0)return;Bt=2}const Jt=at.drawRange,$t=at.attributes.position;let Te=Jt.start*Bt,Ke=(Jt.start+Jt.count)*Bt;Ct!==null&&(Te=Math.max(Te,Ct.start*Bt),Ke=Math.min(Ke,(Ct.start+Ct.count)*Bt)),Yt!==null?(Te=Math.max(Te,0),Ke=Math.min(Ke,Yt.count)):$t!=null&&(Te=Math.max(Te,0),Ke=Math.min(Ke,$t.count));const Qe=Ke-Te;if(Qe<0||Qe===1/0)return;Xt.setup(nt,st,Wt,at,Yt);let Qn,ze=Kt;if(Yt!==null&&(Qn=St.get(Yt),ze=Dt,ze.setIndex(Qn)),nt.isMesh)st.wireframe===!0?(Pt.setLineWidth(st.wireframeLinewidth*ue()),ze.setMode(et.LINES)):ze.setMode(et.TRIANGLES);else if(nt.isLine){let se=st.linewidth;se===void 0&&(se=1),Pt.setLineWidth(se*ue()),nt.isLineSegments?ze.setMode(et.LINES):nt.isLineLoop?ze.setMode(et.LINE_LOOP):ze.setMode(et.LINE_STRIP)}else nt.isPoints?ze.setMode(et.POINTS):nt.isSprite&&ze.setMode(et.TRIANGLES);if(nt.isBatchedMesh)ze.renderMultiDraw(nt._multiDrawStarts,nt._multiDrawCounts,nt._multiDrawCount);else if(nt.isInstancedMesh)ze.renderInstances(Te,Qe,nt.count);else if(at.isInstancedBufferGeometry){const se=at._maxInstanceCount!==void 0?at._maxInstanceCount:1/0,na=Math.min(at.instanceCount,se);ze.renderInstances(Te,Qe,na)}else ze.render(Te,Qe)};function Re(w,j,at){w.transparent===!0&&w.side===Qi&&w.forceSinglePass===!1?(w.side=Fn,w.needsUpdate=!0,Ha(w,j,at),w.side=Fa,w.needsUpdate=!0,Ha(w,j,at),w.side=Qi):Ha(w,j,at)}this.compile=function(w,j,at=null){at===null&&(at=w),M=qt.get(at),M.init(),D.push(M),at.traverseVisible(function(nt){nt.isLight&&nt.layers.test(j.layers)&&(M.pushLight(nt),nt.castShadow&&M.pushShadow(nt))}),w!==at&&w.traverseVisible(function(nt){nt.isLight&&nt.layers.test(j.layers)&&(M.pushLight(nt),nt.castShadow&&M.pushShadow(nt))}),M.setupLights(T._useLegacyLights);const st=new Set;return w.traverse(function(nt){const Ct=nt.material;if(Ct)if(Array.isArray(Ct))for(let Ot=0;Ot<Ct.length;Ot++){const Wt=Ct[Ot];Re(Wt,at,nt),st.add(Wt)}else Re(Ct,at,nt),st.add(Ct)}),D.pop(),M=null,st},this.compileAsync=function(w,j,at=null){const st=this.compile(w,j,at);return new Promise(nt=>{function Ct(){if(st.forEach(function(Ot){ee.get(Ot).currentProgram.isReady()&&st.delete(Ot)}),st.size===0){nt(w);return}setTimeout(Ct,10)}Ft.get("KHR_parallel_shader_compile")!==null?Ct():setTimeout(Ct,10)})};let Ee=null;function Xe(w){Ee&&Ee(w)}function qe(){cn.stop()}function Ce(){cn.start()}const cn=new Lv;cn.setAnimationLoop(Xe),typeof self<"u"&&cn.setContext(self),this.setAnimationLoop=function(w){Ee=w,re.setAnimationLoop(w),w===null?cn.stop():cn.start()},re.addEventListener("sessionstart",qe),re.addEventListener("sessionend",Ce),this.render=function(w,j){if(j!==void 0&&j.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(z===!0)return;w.matrixWorldAutoUpdate===!0&&w.updateMatrixWorld(),j.parent===null&&j.matrixWorldAutoUpdate===!0&&j.updateMatrixWorld(),re.enabled===!0&&re.isPresenting===!0&&(re.cameraAutoUpdate===!0&&re.updateCamera(j),j=re.getCamera()),w.isScene===!0&&w.onBeforeRender(T,w,j,O),M=qt.get(w,D.length),M.init(),D.push(M),Mt.multiplyMatrices(j.projectionMatrix,j.matrixWorldInverse),G.setFromProjectionMatrix(Mt),mt=this.localClippingEnabled,K=ie.init(this.clippingPlanes,mt),A=Ut.get(w,v.length),A.init(),v.push(A),Hn(w,j,0,T.sortObjects),A.finish(),T.sortObjects===!0&&A.sort(J,lt),this.info.render.frame++,K===!0&&ie.beginShadows();const at=M.state.shadowsArray;if(_t.render(at,w,j),K===!0&&ie.endShadows(),this.info.autoReset===!0&&this.info.reset(),ye.render(A,w),M.setupLights(T._useLegacyLights),j.isArrayCamera){const st=j.cameras;for(let nt=0,Ct=st.length;nt<Ct;nt++){const Ot=st[nt];Ms(A,w,Ot,Ot.viewport)}}else Ms(A,w,j);O!==null&&(U.updateMultisampleRenderTarget(O),U.updateRenderTargetMipmap(O)),w.isScene===!0&&w.onAfterRender(T,w,j),Xt.resetDefaultState(),ut=-1,C=null,D.pop(),D.length>0?M=D[D.length-1]:M=null,v.pop(),v.length>0?A=v[v.length-1]:A=null};function Hn(w,j,at,st){if(w.visible===!1)return;if(w.layers.test(j.layers)){if(w.isGroup)at=w.renderOrder;else if(w.isLOD)w.autoUpdate===!0&&w.update(j);else if(w.isLight)M.pushLight(w),w.castShadow&&M.pushShadow(w);else if(w.isSprite){if(!w.frustumCulled||G.intersectsSprite(w)){st&&Nt.setFromMatrixPosition(w.matrixWorld).applyMatrix4(Mt);const Ot=gt.update(w),Wt=w.material;Wt.visible&&A.push(w,Ot,Wt,at,Nt.z,null)}}else if((w.isMesh||w.isLine||w.isPoints)&&(!w.frustumCulled||G.intersectsObject(w))){const Ot=gt.update(w),Wt=w.material;if(st&&(w.boundingSphere!==void 0?(w.boundingSphere===null&&w.computeBoundingSphere(),Nt.copy(w.boundingSphere.center)):(Ot.boundingSphere===null&&Ot.computeBoundingSphere(),Nt.copy(Ot.boundingSphere.center)),Nt.applyMatrix4(w.matrixWorld).applyMatrix4(Mt)),Array.isArray(Wt)){const Yt=Ot.groups;for(let Bt=0,Jt=Yt.length;Bt<Jt;Bt++){const $t=Yt[Bt],Te=Wt[$t.materialIndex];Te&&Te.visible&&A.push(w,Ot,Te,at,Nt.z,$t)}}else Wt.visible&&A.push(w,Ot,Wt,at,Nt.z,null)}}const Ct=w.children;for(let Ot=0,Wt=Ct.length;Ot<Wt;Ot++)Hn(Ct[Ot],j,at,st)}function Ms(w,j,at,st){const nt=w.opaque,Ct=w.transmissive,Ot=w.transparent;M.setupLightsView(at),K===!0&&ie.setGlobalState(T.clippingPlanes,at),Ct.length>0&&ys(nt,Ct,j,at),st&&Pt.viewport(N.copy(st)),nt.length>0&&ta(nt,j,at),Ct.length>0&&ta(Ct,j,at),Ot.length>0&&ta(Ot,j,at),Pt.buffers.depth.setTest(!0),Pt.buffers.depth.setMask(!0),Pt.buffers.color.setMask(!0),Pt.setPolygonOffset(!1)}function ys(w,j,at,st){if((at.isScene===!0?at.overrideMaterial:null)!==null)return;const Ct=Qt.isWebGL2;xt===null&&(xt=new pr(1,1,{generateMipmaps:!0,type:Ft.has("EXT_color_buffer_half_float")?Ro:Ia,minFilter:Ao,samples:Ct?4:0})),T.getDrawingBufferSize(It),Ct?xt.setSize(It.x,It.y):xt.setSize(Ah(It.x),Ah(It.y));const Ot=T.getRenderTarget();T.setRenderTarget(xt),T.getClearColor(Et),X=T.getClearAlpha(),X<1&&T.setClearColor(16777215,.5),T.clear();const Wt=T.toneMapping;T.toneMapping=Ba,ta(w,at,st),U.updateMultisampleRenderTarget(xt),U.updateRenderTargetMipmap(xt);let Yt=!1;for(let Bt=0,Jt=j.length;Bt<Jt;Bt++){const $t=j[Bt],Te=$t.object,Ke=$t.geometry,Qe=$t.material,Qn=$t.group;if(Qe.side===Qi&&Te.layers.test(st.layers)){const ze=Qe.side;Qe.side=Fn,Qe.needsUpdate=!0,Es(Te,at,st,Ke,Qe,Qn),Qe.side=ze,Qe.needsUpdate=!0,Yt=!0}}Yt===!0&&(U.updateMultisampleRenderTarget(xt),U.updateRenderTargetMipmap(xt)),T.setRenderTarget(Ot),T.setClearColor(Et,X),T.toneMapping=Wt}function ta(w,j,at){const st=j.isScene===!0?j.overrideMaterial:null;for(let nt=0,Ct=w.length;nt<Ct;nt++){const Ot=w[nt],Wt=Ot.object,Yt=Ot.geometry,Bt=st===null?Ot.material:st,Jt=Ot.group;Wt.layers.test(at.layers)&&Es(Wt,j,at,Yt,Bt,Jt)}}function Es(w,j,at,st,nt,Ct){w.onBeforeRender(T,j,at,st,nt,Ct),w.modelViewMatrix.multiplyMatrices(at.matrixWorldInverse,w.matrixWorld),w.normalMatrix.getNormalMatrix(w.modelViewMatrix),nt.onBeforeRender(T,j,at,st,w,Ct),nt.transparent===!0&&nt.side===Qi&&nt.forceSinglePass===!1?(nt.side=Fn,nt.needsUpdate=!0,T.renderBufferDirect(at,j,st,nt,w,Ct),nt.side=Fa,nt.needsUpdate=!0,T.renderBufferDirect(at,j,st,nt,w,Ct),nt.side=Qi):T.renderBufferDirect(at,j,st,nt,w,Ct),w.onAfterRender(T,j,at,st,nt,Ct)}function Ha(w,j,at){j.isScene!==!0&&(j=kt);const st=ee.get(w),nt=M.state.lights,Ct=M.state.shadowsArray,Ot=nt.state.version,Wt=Ht.getParameters(w,nt.state,Ct,j,at),Yt=Ht.getProgramCacheKey(Wt);let Bt=st.programs;st.environment=w.isMeshStandardMaterial?j.environment:null,st.fog=j.fog,st.envMap=(w.isMeshStandardMaterial?it:R).get(w.envMap||st.environment),Bt===void 0&&(w.addEventListener("dispose",Tt),Bt=new Map,st.programs=Bt);let Jt=Bt.get(Yt);if(Jt!==void 0){if(st.currentProgram===Jt&&st.lightsStateVersion===Ot)return Ze(w,Wt),Jt}else Wt.uniforms=Ht.getUniforms(w),w.onBuild(at,Wt,T),w.onBeforeCompile(Wt,T),Jt=Ht.acquireProgram(Wt,Yt),Bt.set(Yt,Jt),st.uniforms=Wt.uniforms;const $t=st.uniforms;return(!w.isShaderMaterial&&!w.isRawShaderMaterial||w.clipping===!0)&&($t.clippingPlanes=ie.uniform),Ze(w,Wt),st.needsLights=Ts(w),st.lightsStateVersion=Ot,st.needsLights&&($t.ambientLightColor.value=nt.state.ambient,$t.lightProbe.value=nt.state.probe,$t.directionalLights.value=nt.state.directional,$t.directionalLightShadows.value=nt.state.directionalShadow,$t.spotLights.value=nt.state.spot,$t.spotLightShadows.value=nt.state.spotShadow,$t.rectAreaLights.value=nt.state.rectArea,$t.ltc_1.value=nt.state.rectAreaLTC1,$t.ltc_2.value=nt.state.rectAreaLTC2,$t.pointLights.value=nt.state.point,$t.pointLightShadows.value=nt.state.pointShadow,$t.hemisphereLights.value=nt.state.hemi,$t.directionalShadowMap.value=nt.state.directionalShadowMap,$t.directionalShadowMatrix.value=nt.state.directionalShadowMatrix,$t.spotShadowMap.value=nt.state.spotShadowMap,$t.spotLightMatrix.value=nt.state.spotLightMatrix,$t.spotLightMap.value=nt.state.spotLightMap,$t.pointShadowMap.value=nt.state.pointShadowMap,$t.pointShadowMatrix.value=nt.state.pointShadowMatrix),st.currentProgram=Jt,st.uniformsList=null,Jt}function ci(w){if(w.uniformsList===null){const j=w.currentProgram.getUniforms();w.uniformsList=du.seqWithValue(j.seq,w.uniforms)}return w.uniformsList}function Ze(w,j){const at=ee.get(w);at.outputColorSpace=j.outputColorSpace,at.batching=j.batching,at.instancing=j.instancing,at.instancingColor=j.instancingColor,at.skinning=j.skinning,at.morphTargets=j.morphTargets,at.morphNormals=j.morphNormals,at.morphColors=j.morphColors,at.morphTargetsCount=j.morphTargetsCount,at.numClippingPlanes=j.numClippingPlanes,at.numIntersection=j.numClipIntersection,at.vertexAlphas=j.vertexAlphas,at.vertexTangents=j.vertexTangents,at.toneMapping=j.toneMapping}function Sn(w,j,at,st,nt){j.isScene!==!0&&(j=kt),U.resetTextureUnits();const Ct=j.fog,Ot=st.isMeshStandardMaterial?j.environment:null,Wt=O===null?T.outputColorSpace:O.isXRRenderTarget===!0?O.texture.colorSpace:$i,Yt=(st.isMeshStandardMaterial?it:R).get(st.envMap||Ot),Bt=st.vertexColors===!0&&!!at.attributes.color&&at.attributes.color.itemSize===4,Jt=!!at.attributes.tangent&&(!!st.normalMap||st.anisotropy>0),$t=!!at.morphAttributes.position,Te=!!at.morphAttributes.normal,Ke=!!at.morphAttributes.color;let Qe=Ba;st.toneMapped&&(O===null||O.isXRRenderTarget===!0)&&(Qe=T.toneMapping);const Qn=at.morphAttributes.position||at.morphAttributes.normal||at.morphAttributes.color,ze=Qn!==void 0?Qn.length:0,se=ee.get(st),na=M.state.lights;if(K===!0&&(mt===!0||w!==C)){const Ln=w===C&&st.id===ut;ie.setState(st,w,Ln)}let Ne=!1;st.version===se.__version?(se.needsLights&&se.lightsStateVersion!==na.state.version||se.outputColorSpace!==Wt||nt.isBatchedMesh&&se.batching===!1||!nt.isBatchedMesh&&se.batching===!0||nt.isInstancedMesh&&se.instancing===!1||!nt.isInstancedMesh&&se.instancing===!0||nt.isSkinnedMesh&&se.skinning===!1||!nt.isSkinnedMesh&&se.skinning===!0||nt.isInstancedMesh&&se.instancingColor===!0&&nt.instanceColor===null||nt.isInstancedMesh&&se.instancingColor===!1&&nt.instanceColor!==null||se.envMap!==Yt||st.fog===!0&&se.fog!==Ct||se.numClippingPlanes!==void 0&&(se.numClippingPlanes!==ie.numPlanes||se.numIntersection!==ie.numIntersection)||se.vertexAlphas!==Bt||se.vertexTangents!==Jt||se.morphTargets!==$t||se.morphNormals!==Te||se.morphColors!==Ke||se.toneMapping!==Qe||Qt.isWebGL2===!0&&se.morphTargetsCount!==ze)&&(Ne=!0):(Ne=!0,se.__version=st.version);let dn=se.currentProgram;Ne===!0&&(dn=Ha(st,j,nt));let An=!1,ia=!1,bs=!1;const Je=dn.getUniforms(),xi=se.uniforms;if(Pt.useProgram(dn.program)&&(An=!0,ia=!0,bs=!0),st.id!==ut&&(ut=st.id,ia=!0),An||C!==w){Je.setValue(et,"projectionMatrix",w.projectionMatrix),Je.setValue(et,"viewMatrix",w.matrixWorldInverse);const Ln=Je.map.cameraPosition;Ln!==void 0&&Ln.setValue(et,Nt.setFromMatrixPosition(w.matrixWorld)),Qt.logarithmicDepthBuffer&&Je.setValue(et,"logDepthBufFC",2/(Math.log(w.far+1)/Math.LN2)),(st.isMeshPhongMaterial||st.isMeshToonMaterial||st.isMeshLambertMaterial||st.isMeshBasicMaterial||st.isMeshStandardMaterial||st.isShaderMaterial)&&Je.setValue(et,"isOrthographic",w.isOrthographicCamera===!0),C!==w&&(C=w,ia=!0,bs=!0)}if(nt.isSkinnedMesh){Je.setOptional(et,nt,"bindMatrix"),Je.setOptional(et,nt,"bindMatrixInverse");const Ln=nt.skeleton;Ln&&(Qt.floatVertexTextures?(Ln.boneTexture===null&&Ln.computeBoneTexture(),Je.setValue(et,"boneTexture",Ln.boneTexture,U)):console.warn("THREE.WebGLRenderer: SkinnedMesh can only be used with WebGL 2. With WebGL 1 OES_texture_float and vertex textures support is required."))}nt.isBatchedMesh&&(Je.setOptional(et,nt,"batchingTexture"),Je.setValue(et,"batchingTexture",nt._matricesTexture,U));const aa=at.morphAttributes;if((aa.position!==void 0||aa.normal!==void 0||aa.color!==void 0&&Qt.isWebGL2===!0)&&le.update(nt,at,dn),(ia||se.receiveShadow!==nt.receiveShadow)&&(se.receiveShadow=nt.receiveShadow,Je.setValue(et,"receiveShadow",nt.receiveShadow)),st.isMeshGouraudMaterial&&st.envMap!==null&&(xi.envMap.value=Yt,xi.flipEnvMap.value=Yt.isCubeTexture&&Yt.isRenderTargetTexture===!1?-1:1),ia&&(Je.setValue(et,"toneMappingExposure",T.toneMappingExposure),se.needsLights&&ea(xi,bs),Ct&&st.fog===!0&&Rt.refreshFogUniforms(xi,Ct),Rt.refreshMaterialUniforms(xi,st,q,P,xt),du.upload(et,ci(se),xi,U)),st.isShaderMaterial&&st.uniformsNeedUpdate===!0&&(du.upload(et,ci(se),xi,U),st.uniformsNeedUpdate=!1),st.isSpriteMaterial&&Je.setValue(et,"center",nt.center),Je.setValue(et,"modelViewMatrix",nt.modelViewMatrix),Je.setValue(et,"normalMatrix",nt.normalMatrix),Je.setValue(et,"modelMatrix",nt.matrixWorld),st.isShaderMaterial||st.isRawShaderMaterial){const Ln=st.uniformsGroups;for(let xn=0,As=Ln.length;xn<As;xn++)if(Qt.isWebGL2){const Rs=Ln[xn];Se.update(Rs,dn),Se.bind(Rs,dn)}else console.warn("THREE.WebGLRenderer: Uniform Buffer Objects can only be used with WebGL 2.")}return dn}function ea(w,j){w.ambientLightColor.needsUpdate=j,w.lightProbe.needsUpdate=j,w.directionalLights.needsUpdate=j,w.directionalLightShadows.needsUpdate=j,w.pointLights.needsUpdate=j,w.pointLightShadows.needsUpdate=j,w.spotLights.needsUpdate=j,w.spotLightShadows.needsUpdate=j,w.rectAreaLights.needsUpdate=j,w.hemisphereLights.needsUpdate=j}function Ts(w){return w.isMeshLambertMaterial||w.isMeshToonMaterial||w.isMeshPhongMaterial||w.isMeshStandardMaterial||w.isShadowMaterial||w.isShaderMaterial&&w.lights===!0}this.getActiveCubeFace=function(){return V},this.getActiveMipmapLevel=function(){return B},this.getRenderTarget=function(){return O},this.setRenderTargetTextures=function(w,j,at){ee.get(w.texture).__webglTexture=j,ee.get(w.depthTexture).__webglTexture=at;const st=ee.get(w);st.__hasExternalTextures=!0,st.__hasExternalTextures&&(st.__autoAllocateDepthBuffer=at===void 0,st.__autoAllocateDepthBuffer||Ft.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),st.__useRenderToTexture=!1))},this.setRenderTargetFramebuffer=function(w,j){const at=ee.get(w);at.__webglFramebuffer=j,at.__useDefaultFramebuffer=j===void 0},this.setRenderTarget=function(w,j=0,at=0){O=w,V=j,B=at;let st=!0,nt=null,Ct=!1,Ot=!1;if(w){const Yt=ee.get(w);Yt.__useDefaultFramebuffer!==void 0?(Pt.bindFramebuffer(et.FRAMEBUFFER,null),st=!1):Yt.__webglFramebuffer===void 0?U.setupRenderTarget(w):Yt.__hasExternalTextures&&U.rebindTextures(w,ee.get(w.texture).__webglTexture,ee.get(w.depthTexture).__webglTexture);const Bt=w.texture;(Bt.isData3DTexture||Bt.isDataArrayTexture||Bt.isCompressedArrayTexture)&&(Ot=!0);const Jt=ee.get(w).__webglFramebuffer;w.isWebGLCubeRenderTarget?(Array.isArray(Jt[j])?nt=Jt[j][at]:nt=Jt[j],Ct=!0):Qt.isWebGL2&&w.samples>0&&U.useMultisampledRTT(w)===!1?nt=ee.get(w).__webglMultisampledFramebuffer:Array.isArray(Jt)?nt=Jt[at]:nt=Jt,N.copy(w.viewport),rt.copy(w.scissor),dt=w.scissorTest}else N.copy(ft).multiplyScalar(q).floor(),rt.copy(L).multiplyScalar(q).floor(),dt=W;if(Pt.bindFramebuffer(et.FRAMEBUFFER,nt)&&Qt.drawBuffers&&st&&Pt.drawBuffers(w,nt),Pt.viewport(N),Pt.scissor(rt),Pt.setScissorTest(dt),Ct){const Yt=ee.get(w.texture);et.framebufferTexture2D(et.FRAMEBUFFER,et.COLOR_ATTACHMENT0,et.TEXTURE_CUBE_MAP_POSITIVE_X+j,Yt.__webglTexture,at)}else if(Ot){const Yt=ee.get(w.texture),Bt=j||0;et.framebufferTextureLayer(et.FRAMEBUFFER,et.COLOR_ATTACHMENT0,Yt.__webglTexture,at||0,Bt)}ut=-1},this.readRenderTargetPixels=function(w,j,at,st,nt,Ct,Ot){if(!(w&&w.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Wt=ee.get(w).__webglFramebuffer;if(w.isWebGLCubeRenderTarget&&Ot!==void 0&&(Wt=Wt[Ot]),Wt){Pt.bindFramebuffer(et.FRAMEBUFFER,Wt);try{const Yt=w.texture,Bt=Yt.format,Jt=Yt.type;if(Bt!==Si&&wt.convert(Bt)!==et.getParameter(et.IMPLEMENTATION_COLOR_READ_FORMAT)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}const $t=Jt===Ro&&(Ft.has("EXT_color_buffer_half_float")||Qt.isWebGL2&&Ft.has("EXT_color_buffer_float"));if(Jt!==Ia&&wt.convert(Jt)!==et.getParameter(et.IMPLEMENTATION_COLOR_READ_TYPE)&&!(Jt===Oa&&(Qt.isWebGL2||Ft.has("OES_texture_float")||Ft.has("WEBGL_color_buffer_float")))&&!$t){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}j>=0&&j<=w.width-st&&at>=0&&at<=w.height-nt&&et.readPixels(j,at,st,nt,wt.convert(Bt),wt.convert(Jt),Ct)}finally{const Yt=O!==null?ee.get(O).__webglFramebuffer:null;Pt.bindFramebuffer(et.FRAMEBUFFER,Yt)}}},this.copyFramebufferToTexture=function(w,j,at=0){const st=Math.pow(2,-at),nt=Math.floor(j.image.width*st),Ct=Math.floor(j.image.height*st);U.setTexture2D(j,0),et.copyTexSubImage2D(et.TEXTURE_2D,at,0,0,w.x,w.y,nt,Ct),Pt.unbindTexture()},this.copyTextureToTexture=function(w,j,at,st=0){const nt=j.image.width,Ct=j.image.height,Ot=wt.convert(at.format),Wt=wt.convert(at.type);U.setTexture2D(at,0),et.pixelStorei(et.UNPACK_FLIP_Y_WEBGL,at.flipY),et.pixelStorei(et.UNPACK_PREMULTIPLY_ALPHA_WEBGL,at.premultiplyAlpha),et.pixelStorei(et.UNPACK_ALIGNMENT,at.unpackAlignment),j.isDataTexture?et.texSubImage2D(et.TEXTURE_2D,st,w.x,w.y,nt,Ct,Ot,Wt,j.image.data):j.isCompressedTexture?et.compressedTexSubImage2D(et.TEXTURE_2D,st,w.x,w.y,j.mipmaps[0].width,j.mipmaps[0].height,Ot,j.mipmaps[0].data):et.texSubImage2D(et.TEXTURE_2D,st,w.x,w.y,Ot,Wt,j.image),st===0&&at.generateMipmaps&&et.generateMipmap(et.TEXTURE_2D),Pt.unbindTexture()},this.copyTextureToTexture3D=function(w,j,at,st,nt=0){if(T.isWebGL1Renderer){console.warn("THREE.WebGLRenderer.copyTextureToTexture3D: can only be used with WebGL2.");return}const Ct=w.max.x-w.min.x+1,Ot=w.max.y-w.min.y+1,Wt=w.max.z-w.min.z+1,Yt=wt.convert(st.format),Bt=wt.convert(st.type);let Jt;if(st.isData3DTexture)U.setTexture3D(st,0),Jt=et.TEXTURE_3D;else if(st.isDataArrayTexture||st.isCompressedArrayTexture)U.setTexture2DArray(st,0),Jt=et.TEXTURE_2D_ARRAY;else{console.warn("THREE.WebGLRenderer.copyTextureToTexture3D: only supports THREE.DataTexture3D and THREE.DataTexture2DArray.");return}et.pixelStorei(et.UNPACK_FLIP_Y_WEBGL,st.flipY),et.pixelStorei(et.UNPACK_PREMULTIPLY_ALPHA_WEBGL,st.premultiplyAlpha),et.pixelStorei(et.UNPACK_ALIGNMENT,st.unpackAlignment);const $t=et.getParameter(et.UNPACK_ROW_LENGTH),Te=et.getParameter(et.UNPACK_IMAGE_HEIGHT),Ke=et.getParameter(et.UNPACK_SKIP_PIXELS),Qe=et.getParameter(et.UNPACK_SKIP_ROWS),Qn=et.getParameter(et.UNPACK_SKIP_IMAGES),ze=at.isCompressedTexture?at.mipmaps[nt]:at.image;et.pixelStorei(et.UNPACK_ROW_LENGTH,ze.width),et.pixelStorei(et.UNPACK_IMAGE_HEIGHT,ze.height),et.pixelStorei(et.UNPACK_SKIP_PIXELS,w.min.x),et.pixelStorei(et.UNPACK_SKIP_ROWS,w.min.y),et.pixelStorei(et.UNPACK_SKIP_IMAGES,w.min.z),at.isDataTexture||at.isData3DTexture?et.texSubImage3D(Jt,nt,j.x,j.y,j.z,Ct,Ot,Wt,Yt,Bt,ze.data):at.isCompressedArrayTexture?(console.warn("THREE.WebGLRenderer.copyTextureToTexture3D: untested support for compressed srcTexture."),et.compressedTexSubImage3D(Jt,nt,j.x,j.y,j.z,Ct,Ot,Wt,Yt,ze.data)):et.texSubImage3D(Jt,nt,j.x,j.y,j.z,Ct,Ot,Wt,Yt,Bt,ze),et.pixelStorei(et.UNPACK_ROW_LENGTH,$t),et.pixelStorei(et.UNPACK_IMAGE_HEIGHT,Te),et.pixelStorei(et.UNPACK_SKIP_PIXELS,Ke),et.pixelStorei(et.UNPACK_SKIP_ROWS,Qe),et.pixelStorei(et.UNPACK_SKIP_IMAGES,Qn),nt===0&&st.generateMipmaps&&et.generateMipmap(Jt),Pt.unbindTexture()},this.initTexture=function(w){w.isCubeTexture?U.setTextureCube(w,0):w.isData3DTexture?U.setTexture3D(w,0):w.isDataArrayTexture||w.isCompressedArrayTexture?U.setTexture2DArray(w,0):U.setTexture2D(w,0),Pt.unbindTexture()},this.resetState=function(){V=0,B=0,O=null,Pt.reset(),Xt.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return Ji}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const i=this.getContext();i.drawingBufferColorSpace=e===Dh?"display-p3":"srgb",i.unpackColorSpace=Ue.workingColorSpace===Mu?"display-p3":"srgb"}get outputEncoding(){return console.warn("THREE.WebGLRenderer: Property .outputEncoding has been removed. Use .outputColorSpace instead."),this.outputColorSpace===vn?dr:gv}set outputEncoding(e){console.warn("THREE.WebGLRenderer: Property .outputEncoding has been removed. Use .outputColorSpace instead."),this.outputColorSpace=e===dr?vn:$i}get useLegacyLights(){return console.warn("THREE.WebGLRenderer: The property .useLegacyLights has been deprecated. Migrate your lighting according to the following guide: https://discourse.threejs.org/t/updates-to-lighting-in-three-js-r155/53733."),this._useLegacyLights}set useLegacyLights(e){console.warn("THREE.WebGLRenderer: The property .useLegacyLights has been deprecated. Migrate your lighting according to the following guide: https://discourse.threejs.org/t/updates-to-lighting-in-three-js-r155/53733."),this._useLegacyLights=e}}class _A extends gA{}_A.prototype.isWebGL1Renderer=!0;class UA extends Tn{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,i){return super.copy(e,i),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const i=super.toJSON(e);return this.fog!==null&&(i.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(i.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(i.object.backgroundIntensity=this.backgroundIntensity),i}}class zh extends Ri{constructor(e=[],i=[],r=1,l=0){super(),this.type="PolyhedronGeometry",this.parameters={vertices:e,indices:i,radius:r,detail:l};const c=[],d=[];h(l),p(r),g(),this.setAttribute("position",new bn(c,3)),this.setAttribute("normal",new bn(c.slice(),3)),this.setAttribute("uv",new bn(d,2)),l===0?this.computeVertexNormals():this.normalizeNormals();function h(D){const T=new Y,z=new Y,V=new Y;for(let B=0;B<i.length;B+=3)y(i[B+0],T),y(i[B+1],z),y(i[B+2],V),m(T,z,V,D)}function m(D,T,z,V){const B=V+1,O=[];for(let ut=0;ut<=B;ut++){O[ut]=[];const C=D.clone().lerp(z,ut/B),N=T.clone().lerp(z,ut/B),rt=B-ut;for(let dt=0;dt<=rt;dt++)dt===0&&ut===B?O[ut][dt]=C:O[ut][dt]=C.clone().lerp(N,dt/rt)}for(let ut=0;ut<B;ut++)for(let C=0;C<2*(B-ut)-1;C++){const N=Math.floor(C/2);C%2===0?(x(O[ut][N+1]),x(O[ut+1][N]),x(O[ut][N])):(x(O[ut][N+1]),x(O[ut+1][N+1]),x(O[ut+1][N]))}}function p(D){const T=new Y;for(let z=0;z<c.length;z+=3)T.x=c[z+0],T.y=c[z+1],T.z=c[z+2],T.normalize().multiplyScalar(D),c[z+0]=T.x,c[z+1]=T.y,c[z+2]=T.z}function g(){const D=new Y;for(let T=0;T<c.length;T+=3){D.x=c[T+0],D.y=c[T+1],D.z=c[T+2];const z=M(D)/2/Math.PI+.5,V=v(D)/Math.PI+.5;d.push(z,1-V)}b(),_()}function _(){for(let D=0;D<d.length;D+=6){const T=d[D+0],z=d[D+2],V=d[D+4],B=Math.max(T,z,V),O=Math.min(T,z,V);B>.9&&O<.1&&(T<.2&&(d[D+0]+=1),z<.2&&(d[D+2]+=1),V<.2&&(d[D+4]+=1))}}function x(D){c.push(D.x,D.y,D.z)}function y(D,T){const z=D*3;T.x=e[z+0],T.y=e[z+1],T.z=e[z+2]}function b(){const D=new Y,T=new Y,z=new Y,V=new Y,B=new ge,O=new ge,ut=new ge;for(let C=0,N=0;C<c.length;C+=9,N+=6){D.set(c[C+0],c[C+1],c[C+2]),T.set(c[C+3],c[C+4],c[C+5]),z.set(c[C+6],c[C+7],c[C+8]),B.set(d[N+0],d[N+1]),O.set(d[N+2],d[N+3]),ut.set(d[N+4],d[N+5]),V.copy(D).add(T).add(z).divideScalar(3);const rt=M(V);A(B,N+0,D,rt),A(O,N+2,T,rt),A(ut,N+4,z,rt)}}function A(D,T,z,V){V<0&&D.x===1&&(d[T]=D.x-1),z.x===0&&z.z===0&&(d[T]=V/2/Math.PI+.5)}function M(D){return Math.atan2(D.z,-D.x)}function v(D){return Math.atan2(-D.y,Math.sqrt(D.x*D.x+D.z*D.z))}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new zh(e.vertices,e.indices,e.radius,e.details)}}class Fv extends zh{constructor(e=1,i=0){const r=(1+Math.sqrt(5))/2,l=[-1,r,0,1,r,0,-1,-r,0,1,-r,0,0,-1,r,0,1,r,0,-1,-r,0,1,-r,r,0,-1,r,0,1,-r,0,-1,-r,0,1],c=[0,11,5,0,5,1,0,1,7,0,7,10,0,10,11,1,5,9,5,11,4,11,10,2,10,7,6,7,1,8,3,9,4,3,4,2,3,2,6,3,6,8,3,8,9,4,9,5,2,4,11,6,2,10,8,6,7,9,8,1];super(l,c,e,i),this.type="IcosahedronGeometry",this.parameters={radius:e,detail:i}}static fromJSON(e){return new Fv(e.radius,e.detail)}}class Hv extends Ri{constructor(e=1,i=32,r=16,l=0,c=Math.PI*2,d=0,h=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:i,heightSegments:r,phiStart:l,phiLength:c,thetaStart:d,thetaLength:h},i=Math.max(3,Math.floor(i)),r=Math.max(2,Math.floor(r));const m=Math.min(d+h,Math.PI);let p=0;const g=[],_=new Y,x=new Y,y=[],b=[],A=[],M=[];for(let v=0;v<=r;v++){const D=[],T=v/r;let z=0;v===0&&d===0?z=.5/i:v===r&&m===Math.PI&&(z=-.5/i);for(let V=0;V<=i;V++){const B=V/i;_.x=-e*Math.cos(l+B*c)*Math.sin(d+T*h),_.y=e*Math.cos(d+T*h),_.z=e*Math.sin(l+B*c)*Math.sin(d+T*h),b.push(_.x,_.y,_.z),x.copy(_).normalize(),A.push(x.x,x.y,x.z),M.push(B+z,1-T),D.push(p++)}g.push(D)}for(let v=0;v<r;v++)for(let D=0;D<i;D++){const T=g[v][D+1],z=g[v][D],V=g[v+1][D],B=g[v+1][D+1];(v!==0||d>0)&&y.push(T,z,B),(v!==r-1||m<Math.PI)&&y.push(z,V,B)}this.setIndex(y),this.setAttribute("position",new bn(b,3)),this.setAttribute("normal",new bn(A,3)),this.setAttribute("uv",new bn(M,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Hv(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class Gv extends Ri{constructor(e=1,i=.4,r=12,l=48,c=Math.PI*2){super(),this.type="TorusGeometry",this.parameters={radius:e,tube:i,radialSegments:r,tubularSegments:l,arc:c},r=Math.floor(r),l=Math.floor(l);const d=[],h=[],m=[],p=[],g=new Y,_=new Y,x=new Y;for(let y=0;y<=r;y++)for(let b=0;b<=l;b++){const A=b/l*c,M=y/r*Math.PI*2;_.x=(e+i*Math.cos(M))*Math.cos(A),_.y=(e+i*Math.cos(M))*Math.sin(A),_.z=i*Math.sin(M),h.push(_.x,_.y,_.z),g.x=e*Math.cos(A),g.y=e*Math.sin(A),x.subVectors(_,g).normalize(),m.push(x.x,x.y,x.z),p.push(b/l),p.push(y/r)}for(let y=1;y<=r;y++)for(let b=1;b<=l;b++){const A=(l+1)*y+b-1,M=(l+1)*(y-1)+b-1,v=(l+1)*(y-1)+b,D=(l+1)*y+b;d.push(A,M,D),d.push(M,v,D)}this.setIndex(d),this.setAttribute("position",new bn(h,3)),this.setAttribute("normal",new bn(m,3)),this.setAttribute("uv",new bn(p,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Gv(e.radius,e.tube,e.radialSegments,e.tubularSegments,e.arc)}}class NA extends Uo{constructor(e){super(),this.isMeshStandardMaterial=!0,this.defines={STANDARD:""},this.type="MeshStandardMaterial",this.color=new Me(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new Me(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=_v,this.normalScale=new ge(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class Ph extends Tn{constructor(e,i=1){super(),this.isLight=!0,this.type="Light",this.color=new Me(e),this.intensity=i}dispose(){}copy(e,i){return super.copy(e,i),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const i=super.toJSON(e);return i.object.color=this.color.getHex(),i.object.intensity=this.intensity,this.groundColor!==void 0&&(i.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(i.object.distance=this.distance),this.angle!==void 0&&(i.object.angle=this.angle),this.decay!==void 0&&(i.object.decay=this.decay),this.penumbra!==void 0&&(i.object.penumbra=this.penumbra),this.shadow!==void 0&&(i.object.shadow=this.shadow.toJSON()),i}}const hh=new rn,J_=new Y,$_=new Y;class Vv{constructor(e){this.camera=e,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new ge(512,512),this.map=null,this.mapPass=null,this.matrix=new rn,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Uh,this._frameExtents=new ge(1,1),this._viewportCount=1,this._viewports=[new Ve(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const i=this.camera,r=this.matrix;J_.setFromMatrixPosition(e.matrixWorld),i.position.copy(J_),$_.setFromMatrixPosition(e.target.matrixWorld),i.lookAt($_),i.updateMatrixWorld(),hh.multiplyMatrices(i.projectionMatrix,i.matrixWorldInverse),this._frustum.setFromProjectionMatrix(hh),r.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),r.multiply(hh)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}const tv=new rn,Eo=new Y,dh=new Y;class vA extends Vv{constructor(){super(new li(90,1,.5,500)),this.isPointLightShadow=!0,this._frameExtents=new ge(4,2),this._viewportCount=6,this._viewports=[new Ve(2,1,1,1),new Ve(0,1,1,1),new Ve(3,1,1,1),new Ve(1,1,1,1),new Ve(3,0,1,1),new Ve(1,0,1,1)],this._cubeDirections=[new Y(1,0,0),new Y(-1,0,0),new Y(0,0,1),new Y(0,0,-1),new Y(0,1,0),new Y(0,-1,0)],this._cubeUps=[new Y(0,1,0),new Y(0,1,0),new Y(0,1,0),new Y(0,1,0),new Y(0,0,1),new Y(0,0,-1)]}updateMatrices(e,i=0){const r=this.camera,l=this.matrix,c=e.distance||r.far;c!==r.far&&(r.far=c,r.updateProjectionMatrix()),Eo.setFromMatrixPosition(e.matrixWorld),r.position.copy(Eo),dh.copy(r.position),dh.add(this._cubeDirections[i]),r.up.copy(this._cubeUps[i]),r.lookAt(dh),r.updateMatrixWorld(),l.makeTranslation(-Eo.x,-Eo.y,-Eo.z),tv.multiplyMatrices(r.projectionMatrix,r.matrixWorldInverse),this._frustum.setFromProjectionMatrix(tv)}}class OA extends Ph{constructor(e,i,r=0,l=2){super(e,i),this.isPointLight=!0,this.type="PointLight",this.distance=r,this.decay=l,this.shadow=new vA}get power(){return this.intensity*4*Math.PI}set power(e){this.intensity=e/(4*Math.PI)}dispose(){this.shadow.dispose()}copy(e,i){return super.copy(e,i),this.distance=e.distance,this.decay=e.decay,this.shadow=e.shadow.clone(),this}}class SA extends Vv{constructor(){super(new Uv(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class zA extends Ph{constructor(e,i){super(e,i),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Tn.DEFAULT_UP),this.updateMatrix(),this.target=new Tn,this.shadow=new SA}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class PA extends Ph{constructor(e,i){super(e,i),this.isAmbientLight=!0,this.type="AmbientLight"}}class BA{constructor(e=1,i=0,r=0){return this.radius=e,this.phi=i,this.theta=r,this}set(e,i,r){return this.radius=e,this.phi=i,this.theta=r,this}copy(e){return this.radius=e.radius,this.phi=e.phi,this.theta=e.theta,this}makeSafe(){return this.phi=Math.max(1e-6,Math.min(Math.PI-1e-6,this.phi)),this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,i,r){return this.radius=Math.sqrt(e*e+i*i+r*r),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(e,r),this.phi=Math.acos(Dn(i/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:Ch}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=Ch);var ph={exports:{}},mh={},gh={exports:{}},_h={};var ev;function xA(){if(ev)return _h;ev=1;var o=Co();function e(_,x){return _===x&&(_!==0||1/_===1/x)||_!==_&&x!==x}var i=typeof Object.is=="function"?Object.is:e,r=o.useState,l=o.useEffect,c=o.useLayoutEffect,d=o.useDebugValue;function h(_,x){var y=x(),b=r({inst:{value:y,getSnapshot:x}}),A=b[0].inst,M=b[1];return c(function(){A.value=y,A.getSnapshot=x,m(A)&&M({inst:A})},[_,y,x]),l(function(){return m(A)&&M({inst:A}),_(function(){m(A)&&M({inst:A})})},[_]),d(y),y}function m(_){var x=_.getSnapshot;_=_.value;try{var y=x();return!i(_,y)}catch{return!0}}function p(_,x){return x()}var g=typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"?p:h;return _h.useSyncExternalStore=o.useSyncExternalStore!==void 0?o.useSyncExternalStore:g,_h}var nv;function MA(){return nv||(nv=1,gh.exports=xA()),gh.exports}var iv;function yA(){if(iv)return mh;iv=1;var o=Co(),e=MA();function i(p,g){return p===g&&(p!==0||1/p===1/g)||p!==p&&g!==g}var r=typeof Object.is=="function"?Object.is:i,l=e.useSyncExternalStore,c=o.useRef,d=o.useEffect,h=o.useMemo,m=o.useDebugValue;return mh.useSyncExternalStoreWithSelector=function(p,g,_,x,y){var b=c(null);if(b.current===null){var A={hasValue:!1,value:null};b.current=A}else A=b.current;b=h(function(){function v(B){if(!D){if(D=!0,T=B,B=x(B),y!==void 0&&A.hasValue){var O=A.value;if(y(O,B))return z=O}return z=B}if(O=z,r(T,B))return O;var ut=x(B);return y!==void 0&&y(O,ut)?(T=B,O):(T=B,z=ut)}var D=!1,T,z,V=_===void 0?null:_;return[function(){return v(g())},V===null?void 0:function(){return v(V())}]},[g,_,x,y]);var M=l(p,b[0],b[1]);return d(function(){A.hasValue=!0,A.value=M},[M]),m(M),M},mh}var av;function EA(){return av||(av=1,ph.exports=yA()),ph.exports}var IA=EA();export{PA as A,Me as C,zA as D,Ss as E,fu as G,Fv as I,wA as M,or as P,Do as Q,bA as R,BA as S,DA as T,Y as V,gA as W,RA as _,rv as a,Co as b,CA as c,AA as d,ge as e,_M as f,ZS as g,LA as h,UA as i,TA as j,li as k,hx as l,NA as m,za as n,bv as o,Gv as p,Hv as q,nx as r,OA as s,IA as w};
