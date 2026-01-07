function GS(o,e){for(var i=0;i<e.length;i++){const s=e[i];if(typeof s!="string"&&!Array.isArray(s)){for(const l in s)if(l!=="default"&&!(l in o)){const c=Object.getOwnPropertyDescriptor(s,l);c&&Object.defineProperty(o,l,c.get?c:{enumerable:!0,get:()=>s[l]})}}}return Object.freeze(Object.defineProperty(o,Symbol.toStringTag,{value:"Module"}))}function VS(o){return o&&o.__esModule&&Object.prototype.hasOwnProperty.call(o,"default")?o.default:o}var wf={exports:{}},go={};var mg;function XS(){if(mg)return go;mg=1;var o=Symbol.for("react.transitional.element"),e=Symbol.for("react.fragment");function i(s,l,c){var d=null;if(c!==void 0&&(d=""+c),l.key!==void 0&&(d=""+l.key),"key"in l){c={};for(var h in l)h!=="key"&&(c[h]=l[h])}else c=l;return l=c.ref,{$$typeof:o,type:s,key:d,ref:l!==void 0?l:null,props:c}}return go.Fragment=e,go.jsx=i,go.jsxs=i,go}var gg;function WS(){return gg||(gg=1,wf.exports=XS()),wf.exports}var _A=WS(),Df={exports:{}},te={};var _g;function kS(){if(_g)return te;_g=1;var o=Symbol.for("react.transitional.element"),e=Symbol.for("react.portal"),i=Symbol.for("react.fragment"),s=Symbol.for("react.strict_mode"),l=Symbol.for("react.profiler"),c=Symbol.for("react.consumer"),d=Symbol.for("react.context"),h=Symbol.for("react.forward_ref"),m=Symbol.for("react.suspense"),p=Symbol.for("react.memo"),g=Symbol.for("react.lazy"),_=Symbol.for("react.activity"),M=Symbol.iterator;function y(D){return D===null||typeof D!="object"?null:(D=M&&D[M]||D["@@iterator"],typeof D=="function"?D:null)}var b={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},T=Object.assign,x={};function v(D,X,G){this.props=D,this.context=X,this.refs=x,this.updater=G||b}v.prototype.isReactComponent={},v.prototype.setState=function(D,X){if(typeof D!="object"&&typeof D!="function"&&D!=null)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,D,X,"setState")},v.prototype.forceUpdate=function(D){this.updater.enqueueForceUpdate(this,D,"forceUpdate")};function N(){}N.prototype=v.prototype;function R(D,X,G){this.props=D,this.context=X,this.refs=x,this.updater=G||b}var I=R.prototype=new N;I.constructor=R,T(I,v.prototype),I.isPureReactComponent=!0;var q=Array.isArray;function B(){}var z={H:null,A:null,T:null,S:null},dt=Object.prototype.hasOwnProperty;function w(D,X,G){var Z=G.ref;return{$$typeof:o,type:D,key:X,ref:Z!==void 0?Z:null,props:G}}function U(D,X){return w(D.type,X,D.props)}function lt(D){return typeof D=="object"&&D!==null&&D.$$typeof===o}function mt(D){var X={"=":"=0",":":"=2"};return"$"+D.replace(/[=:]/g,function(G){return X[G]})}var Et=/\/+/g;function V(D,X){return typeof D=="object"&&D!==null&&D.key!=null?mt(""+D.key):X.toString(36)}function $(D){switch(D.status){case"fulfilled":return D.value;case"rejected":throw D.reason;default:switch(typeof D.status=="string"?D.then(B,B):(D.status="pending",D.then(function(X){D.status==="pending"&&(D.status="fulfilled",D.value=X)},function(X){D.status==="pending"&&(D.status="rejected",D.reason=X)})),D.status){case"fulfilled":return D.value;case"rejected":throw D.reason}}throw D}function O(D,X,G,Z,pt){var Mt=typeof D;(Mt==="undefined"||Mt==="boolean")&&(D=null);var xt=!1;if(D===null)xt=!0;else switch(Mt){case"bigint":case"string":case"number":xt=!0;break;case"object":switch(D.$$typeof){case o:case e:xt=!0;break;case g:return xt=D._init,O(xt(D._payload),X,G,Z,pt)}}if(xt)return pt=pt(D),xt=Z===""?"."+V(D,0):Z,q(pt)?(G="",xt!=null&&(G=xt.replace(Et,"$&/")+"/"),O(pt,X,G,"",function(kt){return kt})):pt!=null&&(lt(pt)&&(pt=U(pt,G+(pt.key==null||D&&D.key===pt.key?"":(""+pt.key).replace(Et,"$&/")+"/")+xt)),X.push(pt)),1;xt=0;var It=Z===""?".":Z+":";if(q(D))for(var Nt=0;Nt<D.length;Nt++)Z=D[Nt],Mt=It+V(Z,Nt),xt+=O(Z,X,G,Mt,pt);else if(Nt=y(D),typeof Nt=="function")for(D=Nt.call(D),Nt=0;!(Z=D.next()).done;)Z=Z.value,Mt=It+V(Z,Nt++),xt+=O(Z,X,G,Mt,pt);else if(Mt==="object"){if(typeof D.then=="function")return O($(D),X,G,Z,pt);throw X=String(D),Error("Objects are not valid as a React child (found: "+(X==="[object Object]"?"object with keys {"+Object.keys(D).join(", ")+"}":X)+"). If you meant to render a collection of children, use an array instead.")}return xt}function k(D,X,G){if(D==null)return D;var Z=[],pt=0;return O(D,Z,"","",function(Mt){return X.call(G,Mt,pt++)}),Z}function Q(D){if(D._status===-1){var X=D._result;X=X(),X.then(function(G){(D._status===0||D._status===-1)&&(D._status=1,D._result=G)},function(G){(D._status===0||D._status===-1)&&(D._status=2,D._result=G)}),D._status===-1&&(D._status=0,D._result=X)}if(D._status===1)return D._result.default;throw D._result}var ot=typeof reportError=="function"?reportError:function(D){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var X=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof D=="object"&&D!==null&&typeof D.message=="string"?String(D.message):String(D),error:D});if(!window.dispatchEvent(X))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",D);return}console.error(D)},ct={map:k,forEach:function(D,X,G){k(D,function(){X.apply(this,arguments)},G)},count:function(D){var X=0;return k(D,function(){X++}),X},toArray:function(D){return k(D,function(X){return X})||[]},only:function(D){if(!lt(D))throw Error("React.Children.only expected to receive a single React element child.");return D}};return te.Activity=_,te.Children=ct,te.Component=v,te.Fragment=i,te.Profiler=l,te.PureComponent=R,te.StrictMode=s,te.Suspense=m,te.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=z,te.__COMPILER_RUNTIME={__proto__:null,c:function(D){return z.H.useMemoCache(D)}},te.cache=function(D){return function(){return D.apply(null,arguments)}},te.cacheSignal=function(){return null},te.cloneElement=function(D,X,G){if(D==null)throw Error("The argument must be a React element, but you passed "+D+".");var Z=T({},D.props),pt=D.key;if(X!=null)for(Mt in X.key!==void 0&&(pt=""+X.key),X)!dt.call(X,Mt)||Mt==="key"||Mt==="__self"||Mt==="__source"||Mt==="ref"&&X.ref===void 0||(Z[Mt]=X[Mt]);var Mt=arguments.length-2;if(Mt===1)Z.children=G;else if(1<Mt){for(var xt=Array(Mt),It=0;It<Mt;It++)xt[It]=arguments[It+2];Z.children=xt}return w(D.type,pt,Z)},te.createContext=function(D){return D={$$typeof:d,_currentValue:D,_currentValue2:D,_threadCount:0,Provider:null,Consumer:null},D.Provider=D,D.Consumer={$$typeof:c,_context:D},D},te.createElement=function(D,X,G){var Z,pt={},Mt=null;if(X!=null)for(Z in X.key!==void 0&&(Mt=""+X.key),X)dt.call(X,Z)&&Z!=="key"&&Z!=="__self"&&Z!=="__source"&&(pt[Z]=X[Z]);var xt=arguments.length-2;if(xt===1)pt.children=G;else if(1<xt){for(var It=Array(xt),Nt=0;Nt<xt;Nt++)It[Nt]=arguments[Nt+2];pt.children=It}if(D&&D.defaultProps)for(Z in xt=D.defaultProps,xt)pt[Z]===void 0&&(pt[Z]=xt[Z]);return w(D,Mt,pt)},te.createRef=function(){return{current:null}},te.forwardRef=function(D){return{$$typeof:h,render:D}},te.isValidElement=lt,te.lazy=function(D){return{$$typeof:g,_payload:{_status:-1,_result:D},_init:Q}},te.memo=function(D,X){return{$$typeof:p,type:D,compare:X===void 0?null:X}},te.startTransition=function(D){var X=z.T,G={};z.T=G;try{var Z=D(),pt=z.S;pt!==null&&pt(G,Z),typeof Z=="object"&&Z!==null&&typeof Z.then=="function"&&Z.then(B,ot)}catch(Mt){ot(Mt)}finally{X!==null&&G.types!==null&&(X.types=G.types),z.T=X}},te.unstable_useCacheRefresh=function(){return z.H.useCacheRefresh()},te.use=function(D){return z.H.use(D)},te.useActionState=function(D,X,G){return z.H.useActionState(D,X,G)},te.useCallback=function(D,X){return z.H.useCallback(D,X)},te.useContext=function(D){return z.H.useContext(D)},te.useDebugValue=function(){},te.useDeferredValue=function(D,X){return z.H.useDeferredValue(D,X)},te.useEffect=function(D,X){return z.H.useEffect(D,X)},te.useEffectEvent=function(D){return z.H.useEffectEvent(D)},te.useId=function(){return z.H.useId()},te.useImperativeHandle=function(D,X,G){return z.H.useImperativeHandle(D,X,G)},te.useInsertionEffect=function(D,X){return z.H.useInsertionEffect(D,X)},te.useLayoutEffect=function(D,X){return z.H.useLayoutEffect(D,X)},te.useMemo=function(D,X){return z.H.useMemo(D,X)},te.useOptimistic=function(D,X){return z.H.useOptimistic(D,X)},te.useReducer=function(D,X,G){return z.H.useReducer(D,X,G)},te.useRef=function(D){return z.H.useRef(D)},te.useState=function(D){return z.H.useState(D)},te.useSyncExternalStore=function(D,X,G){return z.H.useSyncExternalStore(D,X,G)},te.useTransition=function(){return z.H.useTransition()},te.version="19.2.3",te}var vg;function Ro(){return vg||(vg=1,Df.exports=kS()),Df.exports}var tv=Ro();const Eo=VS(tv),vA=GS({__proto__:null,default:Eo},[tv]);var Lf={exports:{}},_o={},Uf={exports:{}},Nf={};var Sg;function qS(){return Sg||(Sg=1,(function(o){function e(O,k){var Q=O.length;O.push(k);t:for(;0<Q;){var ot=Q-1>>>1,ct=O[ot];if(0<l(ct,k))O[ot]=k,O[Q]=ct,Q=ot;else break t}}function i(O){return O.length===0?null:O[0]}function s(O){if(O.length===0)return null;var k=O[0],Q=O.pop();if(Q!==k){O[0]=Q;t:for(var ot=0,ct=O.length,D=ct>>>1;ot<D;){var X=2*(ot+1)-1,G=O[X],Z=X+1,pt=O[Z];if(0>l(G,Q))Z<ct&&0>l(pt,G)?(O[ot]=pt,O[Z]=Q,ot=Z):(O[ot]=G,O[X]=Q,ot=X);else if(Z<ct&&0>l(pt,Q))O[ot]=pt,O[Z]=Q,ot=Z;else break t}}return k}function l(O,k){var Q=O.sortIndex-k.sortIndex;return Q!==0?Q:O.id-k.id}if(o.unstable_now=void 0,typeof performance=="object"&&typeof performance.now=="function"){var c=performance;o.unstable_now=function(){return c.now()}}else{var d=Date,h=d.now();o.unstable_now=function(){return d.now()-h}}var m=[],p=[],g=1,_=null,M=3,y=!1,b=!1,T=!1,x=!1,v=typeof setTimeout=="function"?setTimeout:null,N=typeof clearTimeout=="function"?clearTimeout:null,R=typeof setImmediate<"u"?setImmediate:null;function I(O){for(var k=i(p);k!==null;){if(k.callback===null)s(p);else if(k.startTime<=O)s(p),k.sortIndex=k.expirationTime,e(m,k);else break;k=i(p)}}function q(O){if(T=!1,I(O),!b)if(i(m)!==null)b=!0,B||(B=!0,mt());else{var k=i(p);k!==null&&$(q,k.startTime-O)}}var B=!1,z=-1,dt=5,w=-1;function U(){return x?!0:!(o.unstable_now()-w<dt)}function lt(){if(x=!1,B){var O=o.unstable_now();w=O;var k=!0;try{t:{b=!1,T&&(T=!1,N(z),z=-1),y=!0;var Q=M;try{e:{for(I(O),_=i(m);_!==null&&!(_.expirationTime>O&&U());){var ot=_.callback;if(typeof ot=="function"){_.callback=null,M=_.priorityLevel;var ct=ot(_.expirationTime<=O);if(O=o.unstable_now(),typeof ct=="function"){_.callback=ct,I(O),k=!0;break e}_===i(m)&&s(m),I(O)}else s(m);_=i(m)}if(_!==null)k=!0;else{var D=i(p);D!==null&&$(q,D.startTime-O),k=!1}}break t}finally{_=null,M=Q,y=!1}k=void 0}}finally{k?mt():B=!1}}}var mt;if(typeof R=="function")mt=function(){R(lt)};else if(typeof MessageChannel<"u"){var Et=new MessageChannel,V=Et.port2;Et.port1.onmessage=lt,mt=function(){V.postMessage(null)}}else mt=function(){v(lt,0)};function $(O,k){z=v(function(){O(o.unstable_now())},k)}o.unstable_IdlePriority=5,o.unstable_ImmediatePriority=1,o.unstable_LowPriority=4,o.unstable_NormalPriority=3,o.unstable_Profiling=null,o.unstable_UserBlockingPriority=2,o.unstable_cancelCallback=function(O){O.callback=null},o.unstable_forceFrameRate=function(O){0>O||125<O?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):dt=0<O?Math.floor(1e3/O):5},o.unstable_getCurrentPriorityLevel=function(){return M},o.unstable_next=function(O){switch(M){case 1:case 2:case 3:var k=3;break;default:k=M}var Q=M;M=k;try{return O()}finally{M=Q}},o.unstable_requestPaint=function(){x=!0},o.unstable_runWithPriority=function(O,k){switch(O){case 1:case 2:case 3:case 4:case 5:break;default:O=3}var Q=M;M=O;try{return k()}finally{M=Q}},o.unstable_scheduleCallback=function(O,k,Q){var ot=o.unstable_now();switch(typeof Q=="object"&&Q!==null?(Q=Q.delay,Q=typeof Q=="number"&&0<Q?ot+Q:ot):Q=ot,O){case 1:var ct=-1;break;case 2:ct=250;break;case 5:ct=1073741823;break;case 4:ct=1e4;break;default:ct=5e3}return ct=Q+ct,O={id:g++,callback:k,priorityLevel:O,startTime:Q,expirationTime:ct,sortIndex:-1},Q>ot?(O.sortIndex=Q,e(p,O),i(m)===null&&O===i(p)&&(T?(N(z),z=-1):T=!0,$(q,Q-ot))):(O.sortIndex=ct,e(m,O),b||y||(b=!0,B||(B=!0,mt()))),O},o.unstable_shouldYield=U,o.unstable_wrapCallback=function(O){var k=M;return function(){var Q=M;M=k;try{return O.apply(this,arguments)}finally{M=Q}}}})(Nf)),Nf}var Mg;function YS(){return Mg||(Mg=1,Uf.exports=qS()),Uf.exports}var Of={exports:{}},xn={};var xg;function jS(){if(xg)return xn;xg=1;var o=Ro();function e(m){var p="https://react.dev/errors/"+m;if(1<arguments.length){p+="?args[]="+encodeURIComponent(arguments[1]);for(var g=2;g<arguments.length;g++)p+="&args[]="+encodeURIComponent(arguments[g])}return"Minified React error #"+m+"; visit "+p+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function i(){}var s={d:{f:i,r:function(){throw Error(e(522))},D:i,C:i,L:i,m:i,X:i,S:i,M:i},p:0,findDOMNode:null},l=Symbol.for("react.portal");function c(m,p,g){var _=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:l,key:_==null?null:""+_,children:m,containerInfo:p,implementation:g}}var d=o.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function h(m,p){if(m==="font")return"";if(typeof p=="string")return p==="use-credentials"?p:""}return xn.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=s,xn.createPortal=function(m,p){var g=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!p||p.nodeType!==1&&p.nodeType!==9&&p.nodeType!==11)throw Error(e(299));return c(m,p,null,g)},xn.flushSync=function(m){var p=d.T,g=s.p;try{if(d.T=null,s.p=2,m)return m()}finally{d.T=p,s.p=g,s.d.f()}},xn.preconnect=function(m,p){typeof m=="string"&&(p?(p=p.crossOrigin,p=typeof p=="string"?p==="use-credentials"?p:"":void 0):p=null,s.d.C(m,p))},xn.prefetchDNS=function(m){typeof m=="string"&&s.d.D(m)},xn.preinit=function(m,p){if(typeof m=="string"&&p&&typeof p.as=="string"){var g=p.as,_=h(g,p.crossOrigin),M=typeof p.integrity=="string"?p.integrity:void 0,y=typeof p.fetchPriority=="string"?p.fetchPriority:void 0;g==="style"?s.d.S(m,typeof p.precedence=="string"?p.precedence:void 0,{crossOrigin:_,integrity:M,fetchPriority:y}):g==="script"&&s.d.X(m,{crossOrigin:_,integrity:M,fetchPriority:y,nonce:typeof p.nonce=="string"?p.nonce:void 0})}},xn.preinitModule=function(m,p){if(typeof m=="string")if(typeof p=="object"&&p!==null){if(p.as==null||p.as==="script"){var g=h(p.as,p.crossOrigin);s.d.M(m,{crossOrigin:g,integrity:typeof p.integrity=="string"?p.integrity:void 0,nonce:typeof p.nonce=="string"?p.nonce:void 0})}}else p==null&&s.d.M(m)},xn.preload=function(m,p){if(typeof m=="string"&&typeof p=="object"&&p!==null&&typeof p.as=="string"){var g=p.as,_=h(g,p.crossOrigin);s.d.L(m,g,{crossOrigin:_,integrity:typeof p.integrity=="string"?p.integrity:void 0,nonce:typeof p.nonce=="string"?p.nonce:void 0,type:typeof p.type=="string"?p.type:void 0,fetchPriority:typeof p.fetchPriority=="string"?p.fetchPriority:void 0,referrerPolicy:typeof p.referrerPolicy=="string"?p.referrerPolicy:void 0,imageSrcSet:typeof p.imageSrcSet=="string"?p.imageSrcSet:void 0,imageSizes:typeof p.imageSizes=="string"?p.imageSizes:void 0,media:typeof p.media=="string"?p.media:void 0})}},xn.preloadModule=function(m,p){if(typeof m=="string")if(p){var g=h(p.as,p.crossOrigin);s.d.m(m,{as:typeof p.as=="string"&&p.as!=="script"?p.as:void 0,crossOrigin:g,integrity:typeof p.integrity=="string"?p.integrity:void 0})}else s.d.m(m)},xn.requestFormReset=function(m){s.d.r(m)},xn.unstable_batchedUpdates=function(m,p){return m(p)},xn.useFormState=function(m,p,g){return d.H.useFormState(m,p,g)},xn.useFormStatus=function(){return d.H.useHostTransitionStatus()},xn.version="19.2.3",xn}var yg;function ZS(){if(yg)return Of.exports;yg=1;function o(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(o)}catch(e){console.error(e)}}return o(),Of.exports=jS(),Of.exports}var Eg;function KS(){if(Eg)return _o;Eg=1;var o=YS(),e=Ro(),i=ZS();function s(t){var n="https://react.dev/errors/"+t;if(1<arguments.length){n+="?args[]="+encodeURIComponent(arguments[1]);for(var a=2;a<arguments.length;a++)n+="&args[]="+encodeURIComponent(arguments[a])}return"Minified React error #"+t+"; visit "+n+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function l(t){return!(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11)}function c(t){var n=t,a=t;if(t.alternate)for(;n.return;)n=n.return;else{t=n;do n=t,(n.flags&4098)!==0&&(a=n.return),t=n.return;while(t)}return n.tag===3?a:null}function d(t){if(t.tag===13){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function h(t){if(t.tag===31){var n=t.memoizedState;if(n===null&&(t=t.alternate,t!==null&&(n=t.memoizedState)),n!==null)return n.dehydrated}return null}function m(t){if(c(t)!==t)throw Error(s(188))}function p(t){var n=t.alternate;if(!n){if(n=c(t),n===null)throw Error(s(188));return n!==t?null:t}for(var a=t,r=n;;){var u=a.return;if(u===null)break;var f=u.alternate;if(f===null){if(r=u.return,r!==null){a=r;continue}break}if(u.child===f.child){for(f=u.child;f;){if(f===a)return m(u),t;if(f===r)return m(u),n;f=f.sibling}throw Error(s(188))}if(a.return!==r.return)a=u,r=f;else{for(var S=!1,E=u.child;E;){if(E===a){S=!0,a=u,r=f;break}if(E===r){S=!0,r=u,a=f;break}E=E.sibling}if(!S){for(E=f.child;E;){if(E===a){S=!0,a=f,r=u;break}if(E===r){S=!0,r=f,a=u;break}E=E.sibling}if(!S)throw Error(s(189))}}if(a.alternate!==r)throw Error(s(190))}if(a.tag!==3)throw Error(s(188));return a.stateNode.current===a?t:n}function g(t){var n=t.tag;if(n===5||n===26||n===27||n===6)return t;for(t=t.child;t!==null;){if(n=g(t),n!==null)return n;t=t.sibling}return null}var _=Object.assign,M=Symbol.for("react.element"),y=Symbol.for("react.transitional.element"),b=Symbol.for("react.portal"),T=Symbol.for("react.fragment"),x=Symbol.for("react.strict_mode"),v=Symbol.for("react.profiler"),N=Symbol.for("react.consumer"),R=Symbol.for("react.context"),I=Symbol.for("react.forward_ref"),q=Symbol.for("react.suspense"),B=Symbol.for("react.suspense_list"),z=Symbol.for("react.memo"),dt=Symbol.for("react.lazy"),w=Symbol.for("react.activity"),U=Symbol.for("react.memo_cache_sentinel"),lt=Symbol.iterator;function mt(t){return t===null||typeof t!="object"?null:(t=lt&&t[lt]||t["@@iterator"],typeof t=="function"?t:null)}var Et=Symbol.for("react.client.reference");function V(t){if(t==null)return null;if(typeof t=="function")return t.$$typeof===Et?null:t.displayName||t.name||null;if(typeof t=="string")return t;switch(t){case T:return"Fragment";case v:return"Profiler";case x:return"StrictMode";case q:return"Suspense";case B:return"SuspenseList";case w:return"Activity"}if(typeof t=="object")switch(t.$$typeof){case b:return"Portal";case R:return t.displayName||"Context";case N:return(t._context.displayName||"Context")+".Consumer";case I:var n=t.render;return t=t.displayName,t||(t=n.displayName||n.name||"",t=t!==""?"ForwardRef("+t+")":"ForwardRef"),t;case z:return n=t.displayName||null,n!==null?n:V(t.type)||"Memo";case dt:n=t._payload,t=t._init;try{return V(t(n))}catch{}}return null}var $=Array.isArray,O=e.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,k=i.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,Q={pending:!1,data:null,method:null,action:null},ot=[],ct=-1;function D(t){return{current:t}}function X(t){0>ct||(t.current=ot[ct],ot[ct]=null,ct--)}function G(t,n){ct++,ot[ct]=t.current,t.current=n}var Z=D(null),pt=D(null),Mt=D(null),xt=D(null);function It(t,n){switch(G(Mt,n),G(pt,t),G(Z,null),n.nodeType){case 9:case 11:t=(t=n.documentElement)&&(t=t.namespaceURI)?Im(t):0;break;default:if(t=n.tagName,n=n.namespaceURI)n=Im(n),t=Fm(n,t);else switch(t){case"svg":t=1;break;case"math":t=2;break;default:t=0}}X(Z),G(Z,t)}function Nt(){X(Z),X(pt),X(Mt)}function kt(t){t.memoizedState!==null&&G(xt,t);var n=Z.current,a=Fm(n,t.type);n!==a&&(G(pt,t),G(Z,a))}function ue(t){pt.current===t&&(X(Z),X(pt)),xt.current===t&&(X(xt),fo._currentValue=Q)}var tt,ln;function Ft(t){if(tt===void 0)try{throw Error()}catch(a){var n=a.stack.trim().match(/\n( *(at )?)/);tt=n&&n[1]||"",ln=-1<a.stack.indexOf(`
    at`)?" (<anonymous>)":-1<a.stack.indexOf("@")?"@unknown:0:0":""}return`
`+tt+t+ln}var Qt=!1;function Pt(t,n){if(!t||Qt)return"";Qt=!0;var a=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var r={DetermineComponentFrameRoot:function(){try{if(n){var ht=function(){throw Error()};if(Object.defineProperty(ht.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(ht,[])}catch(st){var J=st}Reflect.construct(t,[],ht)}else{try{ht.call()}catch(st){J=st}t.call(ht.prototype)}}else{try{throw Error()}catch(st){J=st}(ht=t())&&typeof ht.catch=="function"&&ht.catch(function(){})}}catch(st){if(st&&J&&typeof st.stack=="string")return[st.stack,J.stack]}return[null,null]}};r.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var u=Object.getOwnPropertyDescriptor(r.DetermineComponentFrameRoot,"name");u&&u.configurable&&Object.defineProperty(r.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var f=r.DetermineComponentFrameRoot(),S=f[0],E=f[1];if(S&&E){var P=S.split(`
`),K=E.split(`
`);for(u=r=0;r<P.length&&!P[r].includes("DetermineComponentFrameRoot");)r++;for(;u<K.length&&!K[u].includes("DetermineComponentFrameRoot");)u++;if(r===P.length||u===K.length)for(r=P.length-1,u=K.length-1;1<=r&&0<=u&&P[r]!==K[u];)u--;for(;1<=r&&0<=u;r--,u--)if(P[r]!==K[u]){if(r!==1||u!==1)do if(r--,u--,0>u||P[r]!==K[u]){var ut=`
`+P[r].replace(" at new "," at ");return t.displayName&&ut.includes("<anonymous>")&&(ut=ut.replace("<anonymous>",t.displayName)),ut}while(1<=r&&0<=u);break}}}finally{Qt=!1,Error.prepareStackTrace=a}return(a=t?t.displayName||t.name:"")?Ft(a):""}function Pe(t,n){switch(t.tag){case 26:case 27:case 5:return Ft(t.type);case 16:return Ft("Lazy");case 13:return t.child!==n&&n!==null?Ft("Suspense Fallback"):Ft("Suspense");case 19:return Ft("SuspenseList");case 0:case 15:return Pt(t.type,!1);case 11:return Pt(t.type.render,!1);case 1:return Pt(t.type,!0);case 31:return Ft("Activity");default:return""}}function ee(t){try{var n="",a=null;do n+=Pe(t,a),a=t,t=t.return;while(t);return n}catch(r){return`
Error generating stack: `+r.message+`
`+r.stack}}var L=Object.prototype.hasOwnProperty,A=o.unstable_scheduleCallback,nt=o.unstable_cancelCallback,St=o.unstable_shouldYield,vt=o.unstable_requestPaint,gt=o.unstable_now,Ht=o.unstable_getCurrentPriorityLevel,Rt=o.unstable_ImmediatePriority,Ut=o.unstable_UserBlockingPriority,qt=o.unstable_NormalPriority,ie=o.unstable_LowPriority,_t=o.unstable_IdlePriority,ye=o.log,le=o.unstable_setDisableYieldValue,Kt=null,Dt=null;function wt(t){if(typeof ye=="function"&&le(t),Dt&&typeof Dt.setStrictMode=="function")try{Dt.setStrictMode(Kt,t)}catch{}}var Xt=Math.clz32?Math.clz32:re,ve=Math.log,He=Math.LN2;function re(t){return t>>>=0,t===0?32:31-(ve(t)/He|0)|0}var yt=256,F=262144,At=4194304;function Tt(t){var n=t&42;if(n!==0)return n;switch(t&-t){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return t&261888;case 262144:case 524288:case 1048576:case 2097152:return t&3932160;case 4194304:case 8388608:case 16777216:case 33554432:return t&62914560;case 67108864:return 67108864;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 0;default:return t}}function jt(t,n,a){var r=t.pendingLanes;if(r===0)return 0;var u=0,f=t.suspendedLanes,S=t.pingedLanes;t=t.warmLanes;var E=r&134217727;return E!==0?(r=E&~f,r!==0?u=Tt(r):(S&=E,S!==0?u=Tt(S):a||(a=E&~t,a!==0&&(u=Tt(a))))):(E=r&~f,E!==0?u=Tt(E):S!==0?u=Tt(S):a||(a=r&~t,a!==0&&(u=Tt(a)))),u===0?0:n!==0&&n!==u&&(n&f)===0&&(f=u&-u,a=n&-n,f>=a||f===32&&(a&4194048)!==0)?n:u}function Gt(t,n){return(t.pendingLanes&~(t.suspendedLanes&~t.pingedLanes)&n)===0}function Re(t,n){switch(t){case 1:case 2:case 4:case 8:case 64:return n+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return n+5e3;case 4194304:case 8388608:case 16777216:case 33554432:return-1;case 67108864:case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function Ee(){var t=At;return At<<=1,(At&62914560)===0&&(At=4194304),t}function Ve(t){for(var n=[],a=0;31>a;a++)n.push(t);return n}function ke(t,n){t.pendingLanes|=n,n!==268435456&&(t.suspendedLanes=0,t.pingedLanes=0,t.warmLanes=0)}function Ce(t,n,a,r,u,f){var S=t.pendingLanes;t.pendingLanes=a,t.suspendedLanes=0,t.pingedLanes=0,t.warmLanes=0,t.expiredLanes&=a,t.entangledLanes&=a,t.errorRecoveryDisabledLanes&=a,t.shellSuspendCounter=0;var E=t.entanglements,P=t.expirationTimes,K=t.hiddenUpdates;for(a=S&~a;0<a;){var ut=31-Xt(a),ht=1<<ut;E[ut]=0,P[ut]=-1;var J=K[ut];if(J!==null)for(K[ut]=null,ut=0;ut<J.length;ut++){var st=J[ut];st!==null&&(st.lane&=-536870913)}a&=~ht}r!==0&&un(t,r,0),f!==0&&u===0&&t.tag!==0&&(t.suspendedLanes|=f&~(S&~n))}function un(t,n,a){t.pendingLanes|=n,t.suspendedLanes&=~n;var r=31-Xt(n);t.entangledLanes|=n,t.entanglements[r]=t.entanglements[r]|1073741824|a&261930}function Fn(t,n){var a=t.entangledLanes|=n;for(t=t.entanglements;a;){var r=31-Xt(a),u=1<<r;u&n|t[r]&n&&(t[r]|=n),a&=~u}}function xs(t,n){var a=n&-n;return a=(a&42)!==0?1:ys(a),(a&(t.suspendedLanes|n))!==0?0:a}function ys(t){switch(t){case 2:t=1;break;case 8:t=4;break;case 32:t=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:t=128;break;case 268435456:t=134217728;break;default:t=0}return t}function $i(t){return t&=-t,2<t?8<t?(t&134217727)!==0?32:268435456:8:2}function Es(){var t=k.p;return t!==0?t:(t=window.event,t===void 0?32:lg(t.type))}function Ha(t,n){var a=k.p;try{return k.p=t,n()}finally{k.p=a}}var li=Math.random().toString(36).slice(2),je="__reactFiber$"+li,Sn="__reactProps$"+li,ta="__reactContainer$"+li,Ts="__reactEvents$"+li,C="__reactListeners$"+li,Y="__reactHandles$"+li,it="__reactResources$"+li,rt="__reactMarker$"+li;function et(t){delete t[je],delete t[Sn],delete t[Ts],delete t[C],delete t[Y]}function Ct(t){var n=t[je];if(n)return n;for(var a=t.parentNode;a;){if(n=a[ta]||a[je]){if(a=n.alternate,n.child!==null||a!==null&&a.child!==null)for(t=qm(t);t!==null;){if(a=t[je])return a;t=qm(t)}return n}t=a,a=t.parentNode}return null}function Ot(t){if(t=t[je]||t[ta]){var n=t.tag;if(n===5||n===6||n===13||n===31||n===26||n===27||n===3)return t}return null}function Wt(t){var n=t.tag;if(n===5||n===26||n===27||n===6)return t.stateNode;throw Error(s(33))}function Yt(t){var n=t[it];return n||(n=t[it]={hoistableStyles:new Map,hoistableScripts:new Map}),n}function Bt(t){t[rt]=!0}var Jt=new Set,$t={};function Te(t,n){Ze(t,n),Ze(t+"Capture",n)}function Ze(t,n){for($t[t]=n,t=0;t<n.length;t++)Jt.add(n[t])}var Ke=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),Kn={},ze={};function se(t){return L.call(ze,t)?!0:L.call(Kn,t)?!1:Ke.test(t)?ze[t]=!0:(Kn[t]=!0,!1)}function ea(t,n,a){if(se(n))if(a===null)t.removeAttribute(n);else{switch(typeof a){case"undefined":case"function":case"symbol":t.removeAttribute(n);return;case"boolean":var r=n.toLowerCase().slice(0,5);if(r!=="data-"&&r!=="aria-"){t.removeAttribute(n);return}}t.setAttribute(n,""+a)}}function Ne(t,n,a){if(a===null)t.removeAttribute(n);else{switch(typeof a){case"undefined":case"function":case"symbol":case"boolean":t.removeAttribute(n);return}t.setAttribute(n,""+a)}}function dn(t,n,a,r){if(r===null)t.removeAttribute(a);else{switch(typeof r){case"undefined":case"function":case"symbol":case"boolean":t.removeAttribute(a);return}t.setAttributeNS(n,a,""+r)}}function bn(t){switch(typeof t){case"bigint":case"boolean":case"number":case"string":case"undefined":return t;case"object":return t;default:return""}}function na(t){var n=t.type;return(t=t.nodeName)&&t.toLowerCase()==="input"&&(n==="checkbox"||n==="radio")}function bs(t,n,a){var r=Object.getOwnPropertyDescriptor(t.constructor.prototype,n);if(!t.hasOwnProperty(n)&&typeof r<"u"&&typeof r.get=="function"&&typeof r.set=="function"){var u=r.get,f=r.set;return Object.defineProperty(t,n,{configurable:!0,get:function(){return u.call(this)},set:function(S){a=""+S,f.call(this,S)}}),Object.defineProperty(t,n,{enumerable:r.enumerable}),{getValue:function(){return a},setValue:function(S){a=""+S},stopTracking:function(){t._valueTracker=null,delete t[n]}}}}function Qe(t){if(!t._valueTracker){var n=na(t)?"checked":"value";t._valueTracker=bs(t,n,""+t[n])}}function Si(t){if(!t)return!1;var n=t._valueTracker;if(!n)return!0;var a=n.getValue(),r="";return t&&(r=na(t)?t.checked?"true":"false":t.value),t=r,t!==a?(n.setValue(t),!0):!1}function ia(t){if(t=t||(typeof document<"u"?document:void 0),typeof t>"u")return null;try{return t.activeElement||t.body}catch{return t.body}}var Dn=/[\n"\\]/g;function Mn(t){return t.replace(Dn,function(n){return"\\"+n.charCodeAt(0).toString(16)+" "})}function As(t,n,a,r,u,f,S,E){t.name="",S!=null&&typeof S!="function"&&typeof S!="symbol"&&typeof S!="boolean"?t.type=S:t.removeAttribute("type"),n!=null?S==="number"?(n===0&&t.value===""||t.value!=n)&&(t.value=""+bn(n)):t.value!==""+bn(n)&&(t.value=""+bn(n)):S!=="submit"&&S!=="reset"||t.removeAttribute("value"),n!=null?Eu(t,S,bn(n)):a!=null?Eu(t,S,bn(a)):r!=null&&t.removeAttribute("value"),u==null&&f!=null&&(t.defaultChecked=!!f),u!=null&&(t.checked=u&&typeof u!="function"&&typeof u!="symbol"),E!=null&&typeof E!="function"&&typeof E!="symbol"&&typeof E!="boolean"?t.name=""+bn(E):t.removeAttribute("name")}function Rs(t,n,a,r,u,f,S,E){if(f!=null&&typeof f!="function"&&typeof f!="symbol"&&typeof f!="boolean"&&(t.type=f),n!=null||a!=null){if(!(f!=="submit"&&f!=="reset"||n!=null)){Qe(t);return}a=a!=null?""+bn(a):"",n=n!=null?""+bn(n):a,E||n===t.value||(t.value=n),t.defaultValue=n}r=r??u,r=typeof r!="function"&&typeof r!="symbol"&&!!r,t.checked=E?t.checked:!!r,t.defaultChecked=!!r,S!=null&&typeof S!="function"&&typeof S!="symbol"&&typeof S!="boolean"&&(t.name=S),Qe(t)}function Eu(t,n,a){n==="number"&&ia(t.ownerDocument)===t||t.defaultValue===""+a||(t.defaultValue=""+a)}function gr(t,n,a,r){if(t=t.options,n){n={};for(var u=0;u<a.length;u++)n["$"+a[u]]=!0;for(a=0;a<t.length;a++)u=n.hasOwnProperty("$"+t[a].value),t[a].selected!==u&&(t[a].selected=u),u&&r&&(t[a].defaultSelected=!0)}else{for(a=""+bn(a),n=null,u=0;u<t.length;u++){if(t[u].value===a){t[u].selected=!0,r&&(t[u].defaultSelected=!0);return}n!==null||t[u].disabled||(n=t[u])}n!==null&&(n.selected=!0)}}function Nh(t,n,a){if(n!=null&&(n=""+bn(n),n!==t.value&&(t.value=n),a==null)){t.defaultValue!==n&&(t.defaultValue=n);return}t.defaultValue=a!=null?""+bn(a):""}function Oh(t,n,a,r){if(n==null){if(r!=null){if(a!=null)throw Error(s(92));if($(r)){if(1<r.length)throw Error(s(93));r=r[0]}a=r}a==null&&(a=""),n=a}a=bn(n),t.defaultValue=a,r=t.textContent,r===a&&r!==""&&r!==null&&(t.value=r),Qe(t)}function _r(t,n){if(n){var a=t.firstChild;if(a&&a===t.lastChild&&a.nodeType===3){a.nodeValue=n;return}}t.textContent=n}var Pv=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function zh(t,n,a){var r=n.indexOf("--")===0;a==null||typeof a=="boolean"||a===""?r?t.setProperty(n,""):n==="float"?t.cssFloat="":t[n]="":r?t.setProperty(n,a):typeof a!="number"||a===0||Pv.has(n)?n==="float"?t.cssFloat=a:t[n]=(""+a).trim():t[n]=a+"px"}function Ph(t,n,a){if(n!=null&&typeof n!="object")throw Error(s(62));if(t=t.style,a!=null){for(var r in a)!a.hasOwnProperty(r)||n!=null&&n.hasOwnProperty(r)||(r.indexOf("--")===0?t.setProperty(r,""):r==="float"?t.cssFloat="":t[r]="");for(var u in n)r=n[u],n.hasOwnProperty(u)&&a[u]!==r&&zh(t,u,r)}else for(var f in n)n.hasOwnProperty(f)&&zh(t,f,n[f])}function Tu(t){if(t.indexOf("-")===-1)return!1;switch(t){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var Bv=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),Iv=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function No(t){return Iv.test(""+t)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":t}function Ri(){}var bu=null;function Au(t){return t=t.target||t.srcElement||window,t.correspondingUseElement&&(t=t.correspondingUseElement),t.nodeType===3?t.parentNode:t}var vr=null,Sr=null;function Bh(t){var n=Ot(t);if(n&&(t=n.stateNode)){var a=t[Sn]||null;t:switch(t=n.stateNode,n.type){case"input":if(As(t,a.value,a.defaultValue,a.defaultValue,a.checked,a.defaultChecked,a.type,a.name),n=a.name,a.type==="radio"&&n!=null){for(a=t;a.parentNode;)a=a.parentNode;for(a=a.querySelectorAll('input[name="'+Mn(""+n)+'"][type="radio"]'),n=0;n<a.length;n++){var r=a[n];if(r!==t&&r.form===t.form){var u=r[Sn]||null;if(!u)throw Error(s(90));As(r,u.value,u.defaultValue,u.defaultValue,u.checked,u.defaultChecked,u.type,u.name)}}for(n=0;n<a.length;n++)r=a[n],r.form===t.form&&Si(r)}break t;case"textarea":Nh(t,a.value,a.defaultValue);break t;case"select":n=a.value,n!=null&&gr(t,!!a.multiple,n,!1)}}}var Ru=!1;function Ih(t,n,a){if(Ru)return t(n,a);Ru=!0;try{var r=t(n);return r}finally{if(Ru=!1,(vr!==null||Sr!==null)&&(Ml(),vr&&(n=vr,t=Sr,Sr=vr=null,Bh(n),t)))for(n=0;n<t.length;n++)Bh(t[n])}}function Cs(t,n){var a=t.stateNode;if(a===null)return null;var r=a[Sn]||null;if(r===null)return null;a=r[n];t:switch(n){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(r=!r.disabled)||(t=t.type,r=!(t==="button"||t==="input"||t==="select"||t==="textarea")),t=!r;break t;default:t=!1}if(t)return null;if(a&&typeof a!="function")throw Error(s(231,n,typeof a));return a}var Ci=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),Cu=!1;if(Ci)try{var ws={};Object.defineProperty(ws,"passive",{get:function(){Cu=!0}}),window.addEventListener("test",ws,ws),window.removeEventListener("test",ws,ws)}catch{Cu=!1}var aa=null,wu=null,Oo=null;function Fh(){if(Oo)return Oo;var t,n=wu,a=n.length,r,u="value"in aa?aa.value:aa.textContent,f=u.length;for(t=0;t<a&&n[t]===u[t];t++);var S=a-t;for(r=1;r<=S&&n[a-r]===u[f-r];r++);return Oo=u.slice(t,1<r?1-r:void 0)}function zo(t){var n=t.keyCode;return"charCode"in t?(t=t.charCode,t===0&&n===13&&(t=13)):t=n,t===10&&(t=13),32<=t||t===13?t:0}function Po(){return!0}function Hh(){return!1}function Ln(t){function n(a,r,u,f,S){this._reactName=a,this._targetInst=u,this.type=r,this.nativeEvent=f,this.target=S,this.currentTarget=null;for(var E in t)t.hasOwnProperty(E)&&(a=t[E],this[E]=a?a(f):f[E]);return this.isDefaultPrevented=(f.defaultPrevented!=null?f.defaultPrevented:f.returnValue===!1)?Po:Hh,this.isPropagationStopped=Hh,this}return _(n.prototype,{preventDefault:function(){this.defaultPrevented=!0;var a=this.nativeEvent;a&&(a.preventDefault?a.preventDefault():typeof a.returnValue!="unknown"&&(a.returnValue=!1),this.isDefaultPrevented=Po)},stopPropagation:function(){var a=this.nativeEvent;a&&(a.stopPropagation?a.stopPropagation():typeof a.cancelBubble!="unknown"&&(a.cancelBubble=!0),this.isPropagationStopped=Po)},persist:function(){},isPersistent:Po}),n}var Ga={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(t){return t.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},Bo=Ln(Ga),Ds=_({},Ga,{view:0,detail:0}),Fv=Ln(Ds),Du,Lu,Ls,Io=_({},Ds,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:Nu,button:0,buttons:0,relatedTarget:function(t){return t.relatedTarget===void 0?t.fromElement===t.srcElement?t.toElement:t.fromElement:t.relatedTarget},movementX:function(t){return"movementX"in t?t.movementX:(t!==Ls&&(Ls&&t.type==="mousemove"?(Du=t.screenX-Ls.screenX,Lu=t.screenY-Ls.screenY):Lu=Du=0,Ls=t),Du)},movementY:function(t){return"movementY"in t?t.movementY:Lu}}),Gh=Ln(Io),Hv=_({},Io,{dataTransfer:0}),Gv=Ln(Hv),Vv=_({},Ds,{relatedTarget:0}),Uu=Ln(Vv),Xv=_({},Ga,{animationName:0,elapsedTime:0,pseudoElement:0}),Wv=Ln(Xv),kv=_({},Ga,{clipboardData:function(t){return"clipboardData"in t?t.clipboardData:window.clipboardData}}),qv=Ln(kv),Yv=_({},Ga,{data:0}),Vh=Ln(Yv),jv={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},Zv={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},Kv={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function Qv(t){var n=this.nativeEvent;return n.getModifierState?n.getModifierState(t):(t=Kv[t])?!!n[t]:!1}function Nu(){return Qv}var Jv=_({},Ds,{key:function(t){if(t.key){var n=jv[t.key]||t.key;if(n!=="Unidentified")return n}return t.type==="keypress"?(t=zo(t),t===13?"Enter":String.fromCharCode(t)):t.type==="keydown"||t.type==="keyup"?Zv[t.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:Nu,charCode:function(t){return t.type==="keypress"?zo(t):0},keyCode:function(t){return t.type==="keydown"||t.type==="keyup"?t.keyCode:0},which:function(t){return t.type==="keypress"?zo(t):t.type==="keydown"||t.type==="keyup"?t.keyCode:0}}),$v=Ln(Jv),t0=_({},Io,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),Xh=Ln(t0),e0=_({},Ds,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:Nu}),n0=Ln(e0),i0=_({},Ga,{propertyName:0,elapsedTime:0,pseudoElement:0}),a0=Ln(i0),r0=_({},Io,{deltaX:function(t){return"deltaX"in t?t.deltaX:"wheelDeltaX"in t?-t.wheelDeltaX:0},deltaY:function(t){return"deltaY"in t?t.deltaY:"wheelDeltaY"in t?-t.wheelDeltaY:"wheelDelta"in t?-t.wheelDelta:0},deltaZ:0,deltaMode:0}),s0=Ln(r0),o0=_({},Ga,{newState:0,oldState:0}),l0=Ln(o0),u0=[9,13,27,32],Ou=Ci&&"CompositionEvent"in window,Us=null;Ci&&"documentMode"in document&&(Us=document.documentMode);var c0=Ci&&"TextEvent"in window&&!Us,Wh=Ci&&(!Ou||Us&&8<Us&&11>=Us),kh=" ",qh=!1;function Yh(t,n){switch(t){case"keyup":return u0.indexOf(n.keyCode)!==-1;case"keydown":return n.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function jh(t){return t=t.detail,typeof t=="object"&&"data"in t?t.data:null}var Mr=!1;function f0(t,n){switch(t){case"compositionend":return jh(n);case"keypress":return n.which!==32?null:(qh=!0,kh);case"textInput":return t=n.data,t===kh&&qh?null:t;default:return null}}function h0(t,n){if(Mr)return t==="compositionend"||!Ou&&Yh(t,n)?(t=Fh(),Oo=wu=aa=null,Mr=!1,t):null;switch(t){case"paste":return null;case"keypress":if(!(n.ctrlKey||n.altKey||n.metaKey)||n.ctrlKey&&n.altKey){if(n.char&&1<n.char.length)return n.char;if(n.which)return String.fromCharCode(n.which)}return null;case"compositionend":return Wh&&n.locale!=="ko"?null:n.data;default:return null}}var d0={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function Zh(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n==="input"?!!d0[t.type]:n==="textarea"}function Kh(t,n,a,r){vr?Sr?Sr.push(r):Sr=[r]:vr=r,n=Rl(n,"onChange"),0<n.length&&(a=new Bo("onChange","change",null,a,r),t.push({event:a,listeners:n}))}var Ns=null,Os=null;function p0(t){Um(t,0)}function Fo(t){var n=Wt(t);if(Si(n))return t}function Qh(t,n){if(t==="change")return n}var Jh=!1;if(Ci){var zu;if(Ci){var Pu="oninput"in document;if(!Pu){var $h=document.createElement("div");$h.setAttribute("oninput","return;"),Pu=typeof $h.oninput=="function"}zu=Pu}else zu=!1;Jh=zu&&(!document.documentMode||9<document.documentMode)}function td(){Ns&&(Ns.detachEvent("onpropertychange",ed),Os=Ns=null)}function ed(t){if(t.propertyName==="value"&&Fo(Os)){var n=[];Kh(n,Os,t,Au(t)),Ih(p0,n)}}function m0(t,n,a){t==="focusin"?(td(),Ns=n,Os=a,Ns.attachEvent("onpropertychange",ed)):t==="focusout"&&td()}function g0(t){if(t==="selectionchange"||t==="keyup"||t==="keydown")return Fo(Os)}function _0(t,n){if(t==="click")return Fo(n)}function v0(t,n){if(t==="input"||t==="change")return Fo(n)}function S0(t,n){return t===n&&(t!==0||1/t===1/n)||t!==t&&n!==n}var Hn=typeof Object.is=="function"?Object.is:S0;function zs(t,n){if(Hn(t,n))return!0;if(typeof t!="object"||t===null||typeof n!="object"||n===null)return!1;var a=Object.keys(t),r=Object.keys(n);if(a.length!==r.length)return!1;for(r=0;r<a.length;r++){var u=a[r];if(!L.call(n,u)||!Hn(t[u],n[u]))return!1}return!0}function nd(t){for(;t&&t.firstChild;)t=t.firstChild;return t}function id(t,n){var a=nd(t);t=0;for(var r;a;){if(a.nodeType===3){if(r=t+a.textContent.length,t<=n&&r>=n)return{node:a,offset:n-t};t=r}t:{for(;a;){if(a.nextSibling){a=a.nextSibling;break t}a=a.parentNode}a=void 0}a=nd(a)}}function ad(t,n){return t&&n?t===n?!0:t&&t.nodeType===3?!1:n&&n.nodeType===3?ad(t,n.parentNode):"contains"in t?t.contains(n):t.compareDocumentPosition?!!(t.compareDocumentPosition(n)&16):!1:!1}function rd(t){t=t!=null&&t.ownerDocument!=null&&t.ownerDocument.defaultView!=null?t.ownerDocument.defaultView:window;for(var n=ia(t.document);n instanceof t.HTMLIFrameElement;){try{var a=typeof n.contentWindow.location.href=="string"}catch{a=!1}if(a)t=n.contentWindow;else break;n=ia(t.document)}return n}function Bu(t){var n=t&&t.nodeName&&t.nodeName.toLowerCase();return n&&(n==="input"&&(t.type==="text"||t.type==="search"||t.type==="tel"||t.type==="url"||t.type==="password")||n==="textarea"||t.contentEditable==="true")}var M0=Ci&&"documentMode"in document&&11>=document.documentMode,xr=null,Iu=null,Ps=null,Fu=!1;function sd(t,n,a){var r=a.window===a?a.document:a.nodeType===9?a:a.ownerDocument;Fu||xr==null||xr!==ia(r)||(r=xr,"selectionStart"in r&&Bu(r)?r={start:r.selectionStart,end:r.selectionEnd}:(r=(r.ownerDocument&&r.ownerDocument.defaultView||window).getSelection(),r={anchorNode:r.anchorNode,anchorOffset:r.anchorOffset,focusNode:r.focusNode,focusOffset:r.focusOffset}),Ps&&zs(Ps,r)||(Ps=r,r=Rl(Iu,"onSelect"),0<r.length&&(n=new Bo("onSelect","select",null,n,a),t.push({event:n,listeners:r}),n.target=xr)))}function Va(t,n){var a={};return a[t.toLowerCase()]=n.toLowerCase(),a["Webkit"+t]="webkit"+n,a["Moz"+t]="moz"+n,a}var yr={animationend:Va("Animation","AnimationEnd"),animationiteration:Va("Animation","AnimationIteration"),animationstart:Va("Animation","AnimationStart"),transitionrun:Va("Transition","TransitionRun"),transitionstart:Va("Transition","TransitionStart"),transitioncancel:Va("Transition","TransitionCancel"),transitionend:Va("Transition","TransitionEnd")},Hu={},od={};Ci&&(od=document.createElement("div").style,"AnimationEvent"in window||(delete yr.animationend.animation,delete yr.animationiteration.animation,delete yr.animationstart.animation),"TransitionEvent"in window||delete yr.transitionend.transition);function Xa(t){if(Hu[t])return Hu[t];if(!yr[t])return t;var n=yr[t],a;for(a in n)if(n.hasOwnProperty(a)&&a in od)return Hu[t]=n[a];return t}var ld=Xa("animationend"),ud=Xa("animationiteration"),cd=Xa("animationstart"),x0=Xa("transitionrun"),y0=Xa("transitionstart"),E0=Xa("transitioncancel"),fd=Xa("transitionend"),hd=new Map,Gu="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");Gu.push("scrollEnd");function ui(t,n){hd.set(t,n),Te(n,[t])}var Ho=typeof reportError=="function"?reportError:function(t){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var n=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof t=="object"&&t!==null&&typeof t.message=="string"?String(t.message):String(t),error:t});if(!window.dispatchEvent(n))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",t);return}console.error(t)},Qn=[],Er=0,Vu=0;function Go(){for(var t=Er,n=Vu=Er=0;n<t;){var a=Qn[n];Qn[n++]=null;var r=Qn[n];Qn[n++]=null;var u=Qn[n];Qn[n++]=null;var f=Qn[n];if(Qn[n++]=null,r!==null&&u!==null){var S=r.pending;S===null?u.next=u:(u.next=S.next,S.next=u),r.pending=u}f!==0&&dd(a,u,f)}}function Vo(t,n,a,r){Qn[Er++]=t,Qn[Er++]=n,Qn[Er++]=a,Qn[Er++]=r,Vu|=r,t.lanes|=r,t=t.alternate,t!==null&&(t.lanes|=r)}function Xu(t,n,a,r){return Vo(t,n,a,r),Xo(t)}function Wa(t,n){return Vo(t,null,null,n),Xo(t)}function dd(t,n,a){t.lanes|=a;var r=t.alternate;r!==null&&(r.lanes|=a);for(var u=!1,f=t.return;f!==null;)f.childLanes|=a,r=f.alternate,r!==null&&(r.childLanes|=a),f.tag===22&&(t=f.stateNode,t===null||t._visibility&1||(u=!0)),t=f,f=f.return;return t.tag===3?(f=t.stateNode,u&&n!==null&&(u=31-Xt(a),t=f.hiddenUpdates,r=t[u],r===null?t[u]=[n]:r.push(n),n.lane=a|536870912),f):null}function Xo(t){if(50<ao)throw ao=0,Jc=null,Error(s(185));for(var n=t.return;n!==null;)t=n,n=t.return;return t.tag===3?t.stateNode:null}var Tr={};function T0(t,n,a,r){this.tag=t,this.key=a,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=n,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=r,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function Gn(t,n,a,r){return new T0(t,n,a,r)}function Wu(t){return t=t.prototype,!(!t||!t.isReactComponent)}function wi(t,n){var a=t.alternate;return a===null?(a=Gn(t.tag,n,t.key,t.mode),a.elementType=t.elementType,a.type=t.type,a.stateNode=t.stateNode,a.alternate=t,t.alternate=a):(a.pendingProps=n,a.type=t.type,a.flags=0,a.subtreeFlags=0,a.deletions=null),a.flags=t.flags&65011712,a.childLanes=t.childLanes,a.lanes=t.lanes,a.child=t.child,a.memoizedProps=t.memoizedProps,a.memoizedState=t.memoizedState,a.updateQueue=t.updateQueue,n=t.dependencies,a.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext},a.sibling=t.sibling,a.index=t.index,a.ref=t.ref,a.refCleanup=t.refCleanup,a}function pd(t,n){t.flags&=65011714;var a=t.alternate;return a===null?(t.childLanes=0,t.lanes=n,t.child=null,t.subtreeFlags=0,t.memoizedProps=null,t.memoizedState=null,t.updateQueue=null,t.dependencies=null,t.stateNode=null):(t.childLanes=a.childLanes,t.lanes=a.lanes,t.child=a.child,t.subtreeFlags=0,t.deletions=null,t.memoizedProps=a.memoizedProps,t.memoizedState=a.memoizedState,t.updateQueue=a.updateQueue,t.type=a.type,n=a.dependencies,t.dependencies=n===null?null:{lanes:n.lanes,firstContext:n.firstContext}),t}function Wo(t,n,a,r,u,f){var S=0;if(r=t,typeof t=="function")Wu(t)&&(S=1);else if(typeof t=="string")S=wS(t,a,Z.current)?26:t==="html"||t==="head"||t==="body"?27:5;else t:switch(t){case w:return t=Gn(31,a,n,u),t.elementType=w,t.lanes=f,t;case T:return ka(a.children,u,f,n);case x:S=8,u|=24;break;case v:return t=Gn(12,a,n,u|2),t.elementType=v,t.lanes=f,t;case q:return t=Gn(13,a,n,u),t.elementType=q,t.lanes=f,t;case B:return t=Gn(19,a,n,u),t.elementType=B,t.lanes=f,t;default:if(typeof t=="object"&&t!==null)switch(t.$$typeof){case R:S=10;break t;case N:S=9;break t;case I:S=11;break t;case z:S=14;break t;case dt:S=16,r=null;break t}S=29,a=Error(s(130,t===null?"null":typeof t,"")),r=null}return n=Gn(S,a,n,u),n.elementType=t,n.type=r,n.lanes=f,n}function ka(t,n,a,r){return t=Gn(7,t,r,n),t.lanes=a,t}function ku(t,n,a){return t=Gn(6,t,null,n),t.lanes=a,t}function md(t){var n=Gn(18,null,null,0);return n.stateNode=t,n}function qu(t,n,a){return n=Gn(4,t.children!==null?t.children:[],t.key,n),n.lanes=a,n.stateNode={containerInfo:t.containerInfo,pendingChildren:null,implementation:t.implementation},n}var gd=new WeakMap;function Jn(t,n){if(typeof t=="object"&&t!==null){var a=gd.get(t);return a!==void 0?a:(n={value:t,source:n,stack:ee(n)},gd.set(t,n),n)}return{value:t,source:n,stack:ee(n)}}var br=[],Ar=0,ko=null,Bs=0,$n=[],ti=0,ra=null,Mi=1,xi="";function Di(t,n){br[Ar++]=Bs,br[Ar++]=ko,ko=t,Bs=n}function _d(t,n,a){$n[ti++]=Mi,$n[ti++]=xi,$n[ti++]=ra,ra=t;var r=Mi;t=xi;var u=32-Xt(r)-1;r&=~(1<<u),a+=1;var f=32-Xt(n)+u;if(30<f){var S=u-u%5;f=(r&(1<<S)-1).toString(32),r>>=S,u-=S,Mi=1<<32-Xt(n)+u|a<<u|r,xi=f+t}else Mi=1<<f|a<<u|r,xi=t}function Yu(t){t.return!==null&&(Di(t,1),_d(t,1,0))}function ju(t){for(;t===ko;)ko=br[--Ar],br[Ar]=null,Bs=br[--Ar],br[Ar]=null;for(;t===ra;)ra=$n[--ti],$n[ti]=null,xi=$n[--ti],$n[ti]=null,Mi=$n[--ti],$n[ti]=null}function vd(t,n){$n[ti++]=Mi,$n[ti++]=xi,$n[ti++]=ra,Mi=n.id,xi=n.overflow,ra=t}var pn=null,Be=null,me=!1,sa=null,ei=!1,Zu=Error(s(519));function oa(t){var n=Error(s(418,1<arguments.length&&arguments[1]!==void 0&&arguments[1]?"text":"HTML",""));throw Is(Jn(n,t)),Zu}function Sd(t){var n=t.stateNode,a=t.type,r=t.memoizedProps;switch(n[je]=t,n[Sn]=r,a){case"dialog":he("cancel",n),he("close",n);break;case"iframe":case"object":case"embed":he("load",n);break;case"video":case"audio":for(a=0;a<so.length;a++)he(so[a],n);break;case"source":he("error",n);break;case"img":case"image":case"link":he("error",n),he("load",n);break;case"details":he("toggle",n);break;case"input":he("invalid",n),Rs(n,r.value,r.defaultValue,r.checked,r.defaultChecked,r.type,r.name,!0);break;case"select":he("invalid",n);break;case"textarea":he("invalid",n),Oh(n,r.value,r.defaultValue,r.children)}a=r.children,typeof a!="string"&&typeof a!="number"&&typeof a!="bigint"||n.textContent===""+a||r.suppressHydrationWarning===!0||Pm(n.textContent,a)?(r.popover!=null&&(he("beforetoggle",n),he("toggle",n)),r.onScroll!=null&&he("scroll",n),r.onScrollEnd!=null&&he("scrollend",n),r.onClick!=null&&(n.onclick=Ri),n=!0):n=!1,n||oa(t,!0)}function Md(t){for(pn=t.return;pn;)switch(pn.tag){case 5:case 31:case 13:ei=!1;return;case 27:case 3:ei=!0;return;default:pn=pn.return}}function Rr(t){if(t!==pn)return!1;if(!me)return Md(t),me=!0,!1;var n=t.tag,a;if((a=n!==3&&n!==27)&&((a=n===5)&&(a=t.type,a=!(a!=="form"&&a!=="button")||pf(t.type,t.memoizedProps)),a=!a),a&&Be&&oa(t),Md(t),n===13){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(s(317));Be=km(t)}else if(n===31){if(t=t.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(s(317));Be=km(t)}else n===27?(n=Be,xa(t.type)?(t=Sf,Sf=null,Be=t):Be=n):Be=pn?ii(t.stateNode.nextSibling):null;return!0}function qa(){Be=pn=null,me=!1}function Ku(){var t=sa;return t!==null&&(zn===null?zn=t:zn.push.apply(zn,t),sa=null),t}function Is(t){sa===null?sa=[t]:sa.push(t)}var Qu=D(null),Ya=null,Li=null;function la(t,n,a){G(Qu,n._currentValue),n._currentValue=a}function Ui(t){t._currentValue=Qu.current,X(Qu)}function Ju(t,n,a){for(;t!==null;){var r=t.alternate;if((t.childLanes&n)!==n?(t.childLanes|=n,r!==null&&(r.childLanes|=n)):r!==null&&(r.childLanes&n)!==n&&(r.childLanes|=n),t===a)break;t=t.return}}function $u(t,n,a,r){var u=t.child;for(u!==null&&(u.return=t);u!==null;){var f=u.dependencies;if(f!==null){var S=u.child;f=f.firstContext;t:for(;f!==null;){var E=f;f=u;for(var P=0;P<n.length;P++)if(E.context===n[P]){f.lanes|=a,E=f.alternate,E!==null&&(E.lanes|=a),Ju(f.return,a,t),r||(S=null);break t}f=E.next}}else if(u.tag===18){if(S=u.return,S===null)throw Error(s(341));S.lanes|=a,f=S.alternate,f!==null&&(f.lanes|=a),Ju(S,a,t),S=null}else S=u.child;if(S!==null)S.return=u;else for(S=u;S!==null;){if(S===t){S=null;break}if(u=S.sibling,u!==null){u.return=S.return,S=u;break}S=S.return}u=S}}function Cr(t,n,a,r){t=null;for(var u=n,f=!1;u!==null;){if(!f){if((u.flags&524288)!==0)f=!0;else if((u.flags&262144)!==0)break}if(u.tag===10){var S=u.alternate;if(S===null)throw Error(s(387));if(S=S.memoizedProps,S!==null){var E=u.type;Hn(u.pendingProps.value,S.value)||(t!==null?t.push(E):t=[E])}}else if(u===xt.current){if(S=u.alternate,S===null)throw Error(s(387));S.memoizedState.memoizedState!==u.memoizedState.memoizedState&&(t!==null?t.push(fo):t=[fo])}u=u.return}t!==null&&$u(n,t,a,r),n.flags|=262144}function qo(t){for(t=t.firstContext;t!==null;){if(!Hn(t.context._currentValue,t.memoizedValue))return!0;t=t.next}return!1}function ja(t){Ya=t,Li=null,t=t.dependencies,t!==null&&(t.firstContext=null)}function mn(t){return xd(Ya,t)}function Yo(t,n){return Ya===null&&ja(t),xd(t,n)}function xd(t,n){var a=n._currentValue;if(n={context:n,memoizedValue:a,next:null},Li===null){if(t===null)throw Error(s(308));Li=n,t.dependencies={lanes:0,firstContext:n},t.flags|=524288}else Li=Li.next=n;return a}var b0=typeof AbortController<"u"?AbortController:function(){var t=[],n=this.signal={aborted:!1,addEventListener:function(a,r){t.push(r)}};this.abort=function(){n.aborted=!0,t.forEach(function(a){return a()})}},A0=o.unstable_scheduleCallback,R0=o.unstable_NormalPriority,Je={$$typeof:R,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function tc(){return{controller:new b0,data:new Map,refCount:0}}function Fs(t){t.refCount--,t.refCount===0&&A0(R0,function(){t.controller.abort()})}var Hs=null,ec=0,wr=0,Dr=null;function C0(t,n){if(Hs===null){var a=Hs=[];ec=0,wr=rf(),Dr={status:"pending",value:void 0,then:function(r){a.push(r)}}}return ec++,n.then(yd,yd),n}function yd(){if(--ec===0&&Hs!==null){Dr!==null&&(Dr.status="fulfilled");var t=Hs;Hs=null,wr=0,Dr=null;for(var n=0;n<t.length;n++)(0,t[n])()}}function w0(t,n){var a=[],r={status:"pending",value:null,reason:null,then:function(u){a.push(u)}};return t.then(function(){r.status="fulfilled",r.value=n;for(var u=0;u<a.length;u++)(0,a[u])(n)},function(u){for(r.status="rejected",r.reason=u,u=0;u<a.length;u++)(0,a[u])(void 0)}),r}var Ed=O.S;O.S=function(t,n){sm=gt(),typeof n=="object"&&n!==null&&typeof n.then=="function"&&C0(t,n),Ed!==null&&Ed(t,n)};var Za=D(null);function nc(){var t=Za.current;return t!==null?t:Oe.pooledCache}function jo(t,n){n===null?G(Za,Za.current):G(Za,n.pool)}function Td(){var t=nc();return t===null?null:{parent:Je._currentValue,pool:t}}var Lr=Error(s(460)),ic=Error(s(474)),Zo=Error(s(542)),Ko={then:function(){}};function bd(t){return t=t.status,t==="fulfilled"||t==="rejected"}function Ad(t,n,a){switch(a=t[a],a===void 0?t.push(n):a!==n&&(n.then(Ri,Ri),n=a),n.status){case"fulfilled":return n.value;case"rejected":throw t=n.reason,Cd(t),t;default:if(typeof n.status=="string")n.then(Ri,Ri);else{if(t=Oe,t!==null&&100<t.shellSuspendCounter)throw Error(s(482));t=n,t.status="pending",t.then(function(r){if(n.status==="pending"){var u=n;u.status="fulfilled",u.value=r}},function(r){if(n.status==="pending"){var u=n;u.status="rejected",u.reason=r}})}switch(n.status){case"fulfilled":return n.value;case"rejected":throw t=n.reason,Cd(t),t}throw Qa=n,Lr}}function Ka(t){try{var n=t._init;return n(t._payload)}catch(a){throw a!==null&&typeof a=="object"&&typeof a.then=="function"?(Qa=a,Lr):a}}var Qa=null;function Rd(){if(Qa===null)throw Error(s(459));var t=Qa;return Qa=null,t}function Cd(t){if(t===Lr||t===Zo)throw Error(s(483))}var Ur=null,Gs=0;function Qo(t){var n=Gs;return Gs+=1,Ur===null&&(Ur=[]),Ad(Ur,t,n)}function Vs(t,n){n=n.props.ref,t.ref=n!==void 0?n:null}function Jo(t,n){throw n.$$typeof===M?Error(s(525)):(t=Object.prototype.toString.call(n),Error(s(31,t==="[object Object]"?"object with keys {"+Object.keys(n).join(", ")+"}":t)))}function wd(t){function n(W,H){if(t){var j=W.deletions;j===null?(W.deletions=[H],W.flags|=16):j.push(H)}}function a(W,H){if(!t)return null;for(;H!==null;)n(W,H),H=H.sibling;return null}function r(W){for(var H=new Map;W!==null;)W.key!==null?H.set(W.key,W):H.set(W.index,W),W=W.sibling;return H}function u(W,H){return W=wi(W,H),W.index=0,W.sibling=null,W}function f(W,H,j){return W.index=j,t?(j=W.alternate,j!==null?(j=j.index,j<H?(W.flags|=67108866,H):j):(W.flags|=67108866,H)):(W.flags|=1048576,H)}function S(W){return t&&W.alternate===null&&(W.flags|=67108866),W}function E(W,H,j,ft){return H===null||H.tag!==6?(H=ku(j,W.mode,ft),H.return=W,H):(H=u(H,j),H.return=W,H)}function P(W,H,j,ft){var Vt=j.type;return Vt===T?ut(W,H,j.props.children,ft,j.key):H!==null&&(H.elementType===Vt||typeof Vt=="object"&&Vt!==null&&Vt.$$typeof===dt&&Ka(Vt)===H.type)?(H=u(H,j.props),Vs(H,j),H.return=W,H):(H=Wo(j.type,j.key,j.props,null,W.mode,ft),Vs(H,j),H.return=W,H)}function K(W,H,j,ft){return H===null||H.tag!==4||H.stateNode.containerInfo!==j.containerInfo||H.stateNode.implementation!==j.implementation?(H=qu(j,W.mode,ft),H.return=W,H):(H=u(H,j.children||[]),H.return=W,H)}function ut(W,H,j,ft,Vt){return H===null||H.tag!==7?(H=ka(j,W.mode,ft,Vt),H.return=W,H):(H=u(H,j),H.return=W,H)}function ht(W,H,j){if(typeof H=="string"&&H!==""||typeof H=="number"||typeof H=="bigint")return H=ku(""+H,W.mode,j),H.return=W,H;if(typeof H=="object"&&H!==null){switch(H.$$typeof){case y:return j=Wo(H.type,H.key,H.props,null,W.mode,j),Vs(j,H),j.return=W,j;case b:return H=qu(H,W.mode,j),H.return=W,H;case dt:return H=Ka(H),ht(W,H,j)}if($(H)||mt(H))return H=ka(H,W.mode,j,null),H.return=W,H;if(typeof H.then=="function")return ht(W,Qo(H),j);if(H.$$typeof===R)return ht(W,Yo(W,H),j);Jo(W,H)}return null}function J(W,H,j,ft){var Vt=H!==null?H.key:null;if(typeof j=="string"&&j!==""||typeof j=="number"||typeof j=="bigint")return Vt!==null?null:E(W,H,""+j,ft);if(typeof j=="object"&&j!==null){switch(j.$$typeof){case y:return j.key===Vt?P(W,H,j,ft):null;case b:return j.key===Vt?K(W,H,j,ft):null;case dt:return j=Ka(j),J(W,H,j,ft)}if($(j)||mt(j))return Vt!==null?null:ut(W,H,j,ft,null);if(typeof j.then=="function")return J(W,H,Qo(j),ft);if(j.$$typeof===R)return J(W,H,Yo(W,j),ft);Jo(W,j)}return null}function st(W,H,j,ft,Vt){if(typeof ft=="string"&&ft!==""||typeof ft=="number"||typeof ft=="bigint")return W=W.get(j)||null,E(H,W,""+ft,Vt);if(typeof ft=="object"&&ft!==null){switch(ft.$$typeof){case y:return W=W.get(ft.key===null?j:ft.key)||null,P(H,W,ft,Vt);case b:return W=W.get(ft.key===null?j:ft.key)||null,K(H,W,ft,Vt);case dt:return ft=Ka(ft),st(W,H,j,ft,Vt)}if($(ft)||mt(ft))return W=W.get(j)||null,ut(H,W,ft,Vt,null);if(typeof ft.then=="function")return st(W,H,j,Qo(ft),Vt);if(ft.$$typeof===R)return st(W,H,j,Yo(H,ft),Vt);Jo(H,ft)}return null}function Lt(W,H,j,ft){for(var Vt=null,ge=null,zt=H,ae=H=0,pe=null;zt!==null&&ae<j.length;ae++){zt.index>ae?(pe=zt,zt=null):pe=zt.sibling;var _e=J(W,zt,j[ae],ft);if(_e===null){zt===null&&(zt=pe);break}t&&zt&&_e.alternate===null&&n(W,zt),H=f(_e,H,ae),ge===null?Vt=_e:ge.sibling=_e,ge=_e,zt=pe}if(ae===j.length)return a(W,zt),me&&Di(W,ae),Vt;if(zt===null){for(;ae<j.length;ae++)zt=ht(W,j[ae],ft),zt!==null&&(H=f(zt,H,ae),ge===null?Vt=zt:ge.sibling=zt,ge=zt);return me&&Di(W,ae),Vt}for(zt=r(zt);ae<j.length;ae++)pe=st(zt,W,ae,j[ae],ft),pe!==null&&(t&&pe.alternate!==null&&zt.delete(pe.key===null?ae:pe.key),H=f(pe,H,ae),ge===null?Vt=pe:ge.sibling=pe,ge=pe);return t&&zt.forEach(function(Aa){return n(W,Aa)}),me&&Di(W,ae),Vt}function Zt(W,H,j,ft){if(j==null)throw Error(s(151));for(var Vt=null,ge=null,zt=H,ae=H=0,pe=null,_e=j.next();zt!==null&&!_e.done;ae++,_e=j.next()){zt.index>ae?(pe=zt,zt=null):pe=zt.sibling;var Aa=J(W,zt,_e.value,ft);if(Aa===null){zt===null&&(zt=pe);break}t&&zt&&Aa.alternate===null&&n(W,zt),H=f(Aa,H,ae),ge===null?Vt=Aa:ge.sibling=Aa,ge=Aa,zt=pe}if(_e.done)return a(W,zt),me&&Di(W,ae),Vt;if(zt===null){for(;!_e.done;ae++,_e=j.next())_e=ht(W,_e.value,ft),_e!==null&&(H=f(_e,H,ae),ge===null?Vt=_e:ge.sibling=_e,ge=_e);return me&&Di(W,ae),Vt}for(zt=r(zt);!_e.done;ae++,_e=j.next())_e=st(zt,W,ae,_e.value,ft),_e!==null&&(t&&_e.alternate!==null&&zt.delete(_e.key===null?ae:_e.key),H=f(_e,H,ae),ge===null?Vt=_e:ge.sibling=_e,ge=_e);return t&&zt.forEach(function(HS){return n(W,HS)}),me&&Di(W,ae),Vt}function Le(W,H,j,ft){if(typeof j=="object"&&j!==null&&j.type===T&&j.key===null&&(j=j.props.children),typeof j=="object"&&j!==null){switch(j.$$typeof){case y:t:{for(var Vt=j.key;H!==null;){if(H.key===Vt){if(Vt=j.type,Vt===T){if(H.tag===7){a(W,H.sibling),ft=u(H,j.props.children),ft.return=W,W=ft;break t}}else if(H.elementType===Vt||typeof Vt=="object"&&Vt!==null&&Vt.$$typeof===dt&&Ka(Vt)===H.type){a(W,H.sibling),ft=u(H,j.props),Vs(ft,j),ft.return=W,W=ft;break t}a(W,H);break}else n(W,H);H=H.sibling}j.type===T?(ft=ka(j.props.children,W.mode,ft,j.key),ft.return=W,W=ft):(ft=Wo(j.type,j.key,j.props,null,W.mode,ft),Vs(ft,j),ft.return=W,W=ft)}return S(W);case b:t:{for(Vt=j.key;H!==null;){if(H.key===Vt)if(H.tag===4&&H.stateNode.containerInfo===j.containerInfo&&H.stateNode.implementation===j.implementation){a(W,H.sibling),ft=u(H,j.children||[]),ft.return=W,W=ft;break t}else{a(W,H);break}else n(W,H);H=H.sibling}ft=qu(j,W.mode,ft),ft.return=W,W=ft}return S(W);case dt:return j=Ka(j),Le(W,H,j,ft)}if($(j))return Lt(W,H,j,ft);if(mt(j)){if(Vt=mt(j),typeof Vt!="function")throw Error(s(150));return j=Vt.call(j),Zt(W,H,j,ft)}if(typeof j.then=="function")return Le(W,H,Qo(j),ft);if(j.$$typeof===R)return Le(W,H,Yo(W,j),ft);Jo(W,j)}return typeof j=="string"&&j!==""||typeof j=="number"||typeof j=="bigint"?(j=""+j,H!==null&&H.tag===6?(a(W,H.sibling),ft=u(H,j),ft.return=W,W=ft):(a(W,H),ft=ku(j,W.mode,ft),ft.return=W,W=ft),S(W)):a(W,H)}return function(W,H,j,ft){try{Gs=0;var Vt=Le(W,H,j,ft);return Ur=null,Vt}catch(zt){if(zt===Lr||zt===Zo)throw zt;var ge=Gn(29,zt,null,W.mode);return ge.lanes=ft,ge.return=W,ge}}}var Ja=wd(!0),Dd=wd(!1),ua=!1;function ac(t){t.updateQueue={baseState:t.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function rc(t,n){t=t.updateQueue,n.updateQueue===t&&(n.updateQueue={baseState:t.baseState,firstBaseUpdate:t.firstBaseUpdate,lastBaseUpdate:t.lastBaseUpdate,shared:t.shared,callbacks:null})}function ca(t){return{lane:t,tag:0,payload:null,callback:null,next:null}}function fa(t,n,a){var r=t.updateQueue;if(r===null)return null;if(r=r.shared,(Se&2)!==0){var u=r.pending;return u===null?n.next=n:(n.next=u.next,u.next=n),r.pending=n,n=Xo(t),dd(t,null,a),n}return Vo(t,r,n,a),Xo(t)}function Xs(t,n,a){if(n=n.updateQueue,n!==null&&(n=n.shared,(a&4194048)!==0)){var r=n.lanes;r&=t.pendingLanes,a|=r,n.lanes=a,Fn(t,a)}}function sc(t,n){var a=t.updateQueue,r=t.alternate;if(r!==null&&(r=r.updateQueue,a===r)){var u=null,f=null;if(a=a.firstBaseUpdate,a!==null){do{var S={lane:a.lane,tag:a.tag,payload:a.payload,callback:null,next:null};f===null?u=f=S:f=f.next=S,a=a.next}while(a!==null);f===null?u=f=n:f=f.next=n}else u=f=n;a={baseState:r.baseState,firstBaseUpdate:u,lastBaseUpdate:f,shared:r.shared,callbacks:r.callbacks},t.updateQueue=a;return}t=a.lastBaseUpdate,t===null?a.firstBaseUpdate=n:t.next=n,a.lastBaseUpdate=n}var oc=!1;function Ws(){if(oc){var t=Dr;if(t!==null)throw t}}function ks(t,n,a,r){oc=!1;var u=t.updateQueue;ua=!1;var f=u.firstBaseUpdate,S=u.lastBaseUpdate,E=u.shared.pending;if(E!==null){u.shared.pending=null;var P=E,K=P.next;P.next=null,S===null?f=K:S.next=K,S=P;var ut=t.alternate;ut!==null&&(ut=ut.updateQueue,E=ut.lastBaseUpdate,E!==S&&(E===null?ut.firstBaseUpdate=K:E.next=K,ut.lastBaseUpdate=P))}if(f!==null){var ht=u.baseState;S=0,ut=K=P=null,E=f;do{var J=E.lane&-536870913,st=J!==E.lane;if(st?(de&J)===J:(r&J)===J){J!==0&&J===wr&&(oc=!0),ut!==null&&(ut=ut.next={lane:0,tag:E.tag,payload:E.payload,callback:null,next:null});t:{var Lt=t,Zt=E;J=n;var Le=a;switch(Zt.tag){case 1:if(Lt=Zt.payload,typeof Lt=="function"){ht=Lt.call(Le,ht,J);break t}ht=Lt;break t;case 3:Lt.flags=Lt.flags&-65537|128;case 0:if(Lt=Zt.payload,J=typeof Lt=="function"?Lt.call(Le,ht,J):Lt,J==null)break t;ht=_({},ht,J);break t;case 2:ua=!0}}J=E.callback,J!==null&&(t.flags|=64,st&&(t.flags|=8192),st=u.callbacks,st===null?u.callbacks=[J]:st.push(J))}else st={lane:J,tag:E.tag,payload:E.payload,callback:E.callback,next:null},ut===null?(K=ut=st,P=ht):ut=ut.next=st,S|=J;if(E=E.next,E===null){if(E=u.shared.pending,E===null)break;st=E,E=st.next,st.next=null,u.lastBaseUpdate=st,u.shared.pending=null}}while(!0);ut===null&&(P=ht),u.baseState=P,u.firstBaseUpdate=K,u.lastBaseUpdate=ut,f===null&&(u.shared.lanes=0),ga|=S,t.lanes=S,t.memoizedState=ht}}function Ld(t,n){if(typeof t!="function")throw Error(s(191,t));t.call(n)}function Ud(t,n){var a=t.callbacks;if(a!==null)for(t.callbacks=null,t=0;t<a.length;t++)Ld(a[t],n)}var Nr=D(null),$o=D(0);function Nd(t,n){t=Gi,G($o,t),G(Nr,n),Gi=t|n.baseLanes}function lc(){G($o,Gi),G(Nr,Nr.current)}function uc(){Gi=$o.current,X(Nr),X($o)}var Vn=D(null),ni=null;function ha(t){var n=t.alternate;G(qe,qe.current&1),G(Vn,t),ni===null&&(n===null||Nr.current!==null||n.memoizedState!==null)&&(ni=t)}function cc(t){G(qe,qe.current),G(Vn,t),ni===null&&(ni=t)}function Od(t){t.tag===22?(G(qe,qe.current),G(Vn,t),ni===null&&(ni=t)):da()}function da(){G(qe,qe.current),G(Vn,Vn.current)}function Xn(t){X(Vn),ni===t&&(ni=null),X(qe)}var qe=D(0);function tl(t){for(var n=t;n!==null;){if(n.tag===13){var a=n.memoizedState;if(a!==null&&(a=a.dehydrated,a===null||_f(a)||vf(a)))return n}else if(n.tag===19&&(n.memoizedProps.revealOrder==="forwards"||n.memoizedProps.revealOrder==="backwards"||n.memoizedProps.revealOrder==="unstable_legacy-backwards"||n.memoizedProps.revealOrder==="together")){if((n.flags&128)!==0)return n}else if(n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return null;n=n.return}n.sibling.return=n.return,n=n.sibling}return null}var Ni=0,ne=null,we=null,$e=null,el=!1,Or=!1,$a=!1,nl=0,qs=0,zr=null,D0=0;function Xe(){throw Error(s(321))}function fc(t,n){if(n===null)return!1;for(var a=0;a<n.length&&a<t.length;a++)if(!Hn(t[a],n[a]))return!1;return!0}function hc(t,n,a,r,u,f){return Ni=f,ne=n,n.memoizedState=null,n.updateQueue=null,n.lanes=0,O.H=t===null||t.memoizedState===null?_p:Rc,$a=!1,f=a(r,u),$a=!1,Or&&(f=Pd(n,a,r,u)),zd(t),f}function zd(t){O.H=Zs;var n=we!==null&&we.next!==null;if(Ni=0,$e=we=ne=null,el=!1,qs=0,zr=null,n)throw Error(s(300));t===null||tn||(t=t.dependencies,t!==null&&qo(t)&&(tn=!0))}function Pd(t,n,a,r){ne=t;var u=0;do{if(Or&&(zr=null),qs=0,Or=!1,25<=u)throw Error(s(301));if(u+=1,$e=we=null,t.updateQueue!=null){var f=t.updateQueue;f.lastEffect=null,f.events=null,f.stores=null,f.memoCache!=null&&(f.memoCache.index=0)}O.H=vp,f=n(a,r)}while(Or);return f}function L0(){var t=O.H,n=t.useState()[0];return n=typeof n.then=="function"?Ys(n):n,t=t.useState()[0],(we!==null?we.memoizedState:null)!==t&&(ne.flags|=1024),n}function dc(){var t=nl!==0;return nl=0,t}function pc(t,n,a){n.updateQueue=t.updateQueue,n.flags&=-2053,t.lanes&=~a}function mc(t){if(el){for(t=t.memoizedState;t!==null;){var n=t.queue;n!==null&&(n.pending=null),t=t.next}el=!1}Ni=0,$e=we=ne=null,Or=!1,qs=nl=0,zr=null}function An(){var t={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return $e===null?ne.memoizedState=$e=t:$e=$e.next=t,$e}function Ye(){if(we===null){var t=ne.alternate;t=t!==null?t.memoizedState:null}else t=we.next;var n=$e===null?ne.memoizedState:$e.next;if(n!==null)$e=n,we=t;else{if(t===null)throw ne.alternate===null?Error(s(467)):Error(s(310));we=t,t={memoizedState:we.memoizedState,baseState:we.baseState,baseQueue:we.baseQueue,queue:we.queue,next:null},$e===null?ne.memoizedState=$e=t:$e=$e.next=t}return $e}function il(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function Ys(t){var n=qs;return qs+=1,zr===null&&(zr=[]),t=Ad(zr,t,n),n=ne,($e===null?n.memoizedState:$e.next)===null&&(n=n.alternate,O.H=n===null||n.memoizedState===null?_p:Rc),t}function al(t){if(t!==null&&typeof t=="object"){if(typeof t.then=="function")return Ys(t);if(t.$$typeof===R)return mn(t)}throw Error(s(438,String(t)))}function gc(t){var n=null,a=ne.updateQueue;if(a!==null&&(n=a.memoCache),n==null){var r=ne.alternate;r!==null&&(r=r.updateQueue,r!==null&&(r=r.memoCache,r!=null&&(n={data:r.data.map(function(u){return u.slice()}),index:0})))}if(n==null&&(n={data:[],index:0}),a===null&&(a=il(),ne.updateQueue=a),a.memoCache=n,a=n.data[n.index],a===void 0)for(a=n.data[n.index]=Array(t),r=0;r<t;r++)a[r]=U;return n.index++,a}function Oi(t,n){return typeof n=="function"?n(t):n}function rl(t){var n=Ye();return _c(n,we,t)}function _c(t,n,a){var r=t.queue;if(r===null)throw Error(s(311));r.lastRenderedReducer=a;var u=t.baseQueue,f=r.pending;if(f!==null){if(u!==null){var S=u.next;u.next=f.next,f.next=S}n.baseQueue=u=f,r.pending=null}if(f=t.baseState,u===null)t.memoizedState=f;else{n=u.next;var E=S=null,P=null,K=n,ut=!1;do{var ht=K.lane&-536870913;if(ht!==K.lane?(de&ht)===ht:(Ni&ht)===ht){var J=K.revertLane;if(J===0)P!==null&&(P=P.next={lane:0,revertLane:0,gesture:null,action:K.action,hasEagerState:K.hasEagerState,eagerState:K.eagerState,next:null}),ht===wr&&(ut=!0);else if((Ni&J)===J){K=K.next,J===wr&&(ut=!0);continue}else ht={lane:0,revertLane:K.revertLane,gesture:null,action:K.action,hasEagerState:K.hasEagerState,eagerState:K.eagerState,next:null},P===null?(E=P=ht,S=f):P=P.next=ht,ne.lanes|=J,ga|=J;ht=K.action,$a&&a(f,ht),f=K.hasEagerState?K.eagerState:a(f,ht)}else J={lane:ht,revertLane:K.revertLane,gesture:K.gesture,action:K.action,hasEagerState:K.hasEagerState,eagerState:K.eagerState,next:null},P===null?(E=P=J,S=f):P=P.next=J,ne.lanes|=ht,ga|=ht;K=K.next}while(K!==null&&K!==n);if(P===null?S=f:P.next=E,!Hn(f,t.memoizedState)&&(tn=!0,ut&&(a=Dr,a!==null)))throw a;t.memoizedState=f,t.baseState=S,t.baseQueue=P,r.lastRenderedState=f}return u===null&&(r.lanes=0),[t.memoizedState,r.dispatch]}function vc(t){var n=Ye(),a=n.queue;if(a===null)throw Error(s(311));a.lastRenderedReducer=t;var r=a.dispatch,u=a.pending,f=n.memoizedState;if(u!==null){a.pending=null;var S=u=u.next;do f=t(f,S.action),S=S.next;while(S!==u);Hn(f,n.memoizedState)||(tn=!0),n.memoizedState=f,n.baseQueue===null&&(n.baseState=f),a.lastRenderedState=f}return[f,r]}function Bd(t,n,a){var r=ne,u=Ye(),f=me;if(f){if(a===void 0)throw Error(s(407));a=a()}else a=n();var S=!Hn((we||u).memoizedState,a);if(S&&(u.memoizedState=a,tn=!0),u=u.queue,xc(Hd.bind(null,r,u,t),[t]),u.getSnapshot!==n||S||$e!==null&&$e.memoizedState.tag&1){if(r.flags|=2048,Pr(9,{destroy:void 0},Fd.bind(null,r,u,a,n),null),Oe===null)throw Error(s(349));f||(Ni&127)!==0||Id(r,n,a)}return a}function Id(t,n,a){t.flags|=16384,t={getSnapshot:n,value:a},n=ne.updateQueue,n===null?(n=il(),ne.updateQueue=n,n.stores=[t]):(a=n.stores,a===null?n.stores=[t]:a.push(t))}function Fd(t,n,a,r){n.value=a,n.getSnapshot=r,Gd(n)&&Vd(t)}function Hd(t,n,a){return a(function(){Gd(n)&&Vd(t)})}function Gd(t){var n=t.getSnapshot;t=t.value;try{var a=n();return!Hn(t,a)}catch{return!0}}function Vd(t){var n=Wa(t,2);n!==null&&Pn(n,t,2)}function Sc(t){var n=An();if(typeof t=="function"){var a=t;if(t=a(),$a){wt(!0);try{a()}finally{wt(!1)}}}return n.memoizedState=n.baseState=t,n.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:Oi,lastRenderedState:t},n}function Xd(t,n,a,r){return t.baseState=a,_c(t,we,typeof r=="function"?r:Oi)}function U0(t,n,a,r,u){if(ll(t))throw Error(s(485));if(t=n.action,t!==null){var f={payload:u,action:t,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(S){f.listeners.push(S)}};O.T!==null?a(!0):f.isTransition=!1,r(f),a=n.pending,a===null?(f.next=n.pending=f,Wd(n,f)):(f.next=a.next,n.pending=a.next=f)}}function Wd(t,n){var a=n.action,r=n.payload,u=t.state;if(n.isTransition){var f=O.T,S={};O.T=S;try{var E=a(u,r),P=O.S;P!==null&&P(S,E),kd(t,n,E)}catch(K){Mc(t,n,K)}finally{f!==null&&S.types!==null&&(f.types=S.types),O.T=f}}else try{f=a(u,r),kd(t,n,f)}catch(K){Mc(t,n,K)}}function kd(t,n,a){a!==null&&typeof a=="object"&&typeof a.then=="function"?a.then(function(r){qd(t,n,r)},function(r){return Mc(t,n,r)}):qd(t,n,a)}function qd(t,n,a){n.status="fulfilled",n.value=a,Yd(n),t.state=a,n=t.pending,n!==null&&(a=n.next,a===n?t.pending=null:(a=a.next,n.next=a,Wd(t,a)))}function Mc(t,n,a){var r=t.pending;if(t.pending=null,r!==null){r=r.next;do n.status="rejected",n.reason=a,Yd(n),n=n.next;while(n!==r)}t.action=null}function Yd(t){t=t.listeners;for(var n=0;n<t.length;n++)(0,t[n])()}function jd(t,n){return n}function Zd(t,n){if(me){var a=Oe.formState;if(a!==null){t:{var r=ne;if(me){if(Be){e:{for(var u=Be,f=ei;u.nodeType!==8;){if(!f){u=null;break e}if(u=ii(u.nextSibling),u===null){u=null;break e}}f=u.data,u=f==="F!"||f==="F"?u:null}if(u){Be=ii(u.nextSibling),r=u.data==="F!";break t}}oa(r)}r=!1}r&&(n=a[0])}}return a=An(),a.memoizedState=a.baseState=n,r={pending:null,lanes:0,dispatch:null,lastRenderedReducer:jd,lastRenderedState:n},a.queue=r,a=pp.bind(null,ne,r),r.dispatch=a,r=Sc(!1),f=Ac.bind(null,ne,!1,r.queue),r=An(),u={state:n,dispatch:null,action:t,pending:null},r.queue=u,a=U0.bind(null,ne,u,f,a),u.dispatch=a,r.memoizedState=t,[n,a,!1]}function Kd(t){var n=Ye();return Qd(n,we,t)}function Qd(t,n,a){if(n=_c(t,n,jd)[0],t=rl(Oi)[0],typeof n=="object"&&n!==null&&typeof n.then=="function")try{var r=Ys(n)}catch(S){throw S===Lr?Zo:S}else r=n;n=Ye();var u=n.queue,f=u.dispatch;return a!==n.memoizedState&&(ne.flags|=2048,Pr(9,{destroy:void 0},N0.bind(null,u,a),null)),[r,f,t]}function N0(t,n){t.action=n}function Jd(t){var n=Ye(),a=we;if(a!==null)return Qd(n,a,t);Ye(),n=n.memoizedState,a=Ye();var r=a.queue.dispatch;return a.memoizedState=t,[n,r,!1]}function Pr(t,n,a,r){return t={tag:t,create:a,deps:r,inst:n,next:null},n=ne.updateQueue,n===null&&(n=il(),ne.updateQueue=n),a=n.lastEffect,a===null?n.lastEffect=t.next=t:(r=a.next,a.next=t,t.next=r,n.lastEffect=t),t}function $d(){return Ye().memoizedState}function sl(t,n,a,r){var u=An();ne.flags|=t,u.memoizedState=Pr(1|n,{destroy:void 0},a,r===void 0?null:r)}function ol(t,n,a,r){var u=Ye();r=r===void 0?null:r;var f=u.memoizedState.inst;we!==null&&r!==null&&fc(r,we.memoizedState.deps)?u.memoizedState=Pr(n,f,a,r):(ne.flags|=t,u.memoizedState=Pr(1|n,f,a,r))}function tp(t,n){sl(8390656,8,t,n)}function xc(t,n){ol(2048,8,t,n)}function O0(t){ne.flags|=4;var n=ne.updateQueue;if(n===null)n=il(),ne.updateQueue=n,n.events=[t];else{var a=n.events;a===null?n.events=[t]:a.push(t)}}function ep(t){var n=Ye().memoizedState;return O0({ref:n,nextImpl:t}),function(){if((Se&2)!==0)throw Error(s(440));return n.impl.apply(void 0,arguments)}}function np(t,n){return ol(4,2,t,n)}function ip(t,n){return ol(4,4,t,n)}function ap(t,n){if(typeof n=="function"){t=t();var a=n(t);return function(){typeof a=="function"?a():n(null)}}if(n!=null)return t=t(),n.current=t,function(){n.current=null}}function rp(t,n,a){a=a!=null?a.concat([t]):null,ol(4,4,ap.bind(null,n,t),a)}function yc(){}function sp(t,n){var a=Ye();n=n===void 0?null:n;var r=a.memoizedState;return n!==null&&fc(n,r[1])?r[0]:(a.memoizedState=[t,n],t)}function op(t,n){var a=Ye();n=n===void 0?null:n;var r=a.memoizedState;if(n!==null&&fc(n,r[1]))return r[0];if(r=t(),$a){wt(!0);try{t()}finally{wt(!1)}}return a.memoizedState=[r,n],r}function Ec(t,n,a){return a===void 0||(Ni&1073741824)!==0&&(de&261930)===0?t.memoizedState=n:(t.memoizedState=a,t=lm(),ne.lanes|=t,ga|=t,a)}function lp(t,n,a,r){return Hn(a,n)?a:Nr.current!==null?(t=Ec(t,a,r),Hn(t,n)||(tn=!0),t):(Ni&42)===0||(Ni&1073741824)!==0&&(de&261930)===0?(tn=!0,t.memoizedState=a):(t=lm(),ne.lanes|=t,ga|=t,n)}function up(t,n,a,r,u){var f=k.p;k.p=f!==0&&8>f?f:8;var S=O.T,E={};O.T=E,Ac(t,!1,n,a);try{var P=u(),K=O.S;if(K!==null&&K(E,P),P!==null&&typeof P=="object"&&typeof P.then=="function"){var ut=w0(P,r);js(t,n,ut,qn(t))}else js(t,n,r,qn(t))}catch(ht){js(t,n,{then:function(){},status:"rejected",reason:ht},qn())}finally{k.p=f,S!==null&&E.types!==null&&(S.types=E.types),O.T=S}}function z0(){}function Tc(t,n,a,r){if(t.tag!==5)throw Error(s(476));var u=cp(t).queue;up(t,u,n,Q,a===null?z0:function(){return fp(t),a(r)})}function cp(t){var n=t.memoizedState;if(n!==null)return n;n={memoizedState:Q,baseState:Q,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:Oi,lastRenderedState:Q},next:null};var a={};return n.next={memoizedState:a,baseState:a,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:Oi,lastRenderedState:a},next:null},t.memoizedState=n,t=t.alternate,t!==null&&(t.memoizedState=n),n}function fp(t){var n=cp(t);n.next===null&&(n=t.alternate.memoizedState),js(t,n.next.queue,{},qn())}function bc(){return mn(fo)}function hp(){return Ye().memoizedState}function dp(){return Ye().memoizedState}function P0(t){for(var n=t.return;n!==null;){switch(n.tag){case 24:case 3:var a=qn();t=ca(a);var r=fa(n,t,a);r!==null&&(Pn(r,n,a),Xs(r,n,a)),n={cache:tc()},t.payload=n;return}n=n.return}}function B0(t,n,a){var r=qn();a={lane:r,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null},ll(t)?mp(n,a):(a=Xu(t,n,a,r),a!==null&&(Pn(a,t,r),gp(a,n,r)))}function pp(t,n,a){var r=qn();js(t,n,a,r)}function js(t,n,a,r){var u={lane:r,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null};if(ll(t))mp(n,u);else{var f=t.alternate;if(t.lanes===0&&(f===null||f.lanes===0)&&(f=n.lastRenderedReducer,f!==null))try{var S=n.lastRenderedState,E=f(S,a);if(u.hasEagerState=!0,u.eagerState=E,Hn(E,S))return Vo(t,n,u,0),Oe===null&&Go(),!1}catch{}if(a=Xu(t,n,u,r),a!==null)return Pn(a,t,r),gp(a,n,r),!0}return!1}function Ac(t,n,a,r){if(r={lane:2,revertLane:rf(),gesture:null,action:r,hasEagerState:!1,eagerState:null,next:null},ll(t)){if(n)throw Error(s(479))}else n=Xu(t,a,r,2),n!==null&&Pn(n,t,2)}function ll(t){var n=t.alternate;return t===ne||n!==null&&n===ne}function mp(t,n){Or=el=!0;var a=t.pending;a===null?n.next=n:(n.next=a.next,a.next=n),t.pending=n}function gp(t,n,a){if((a&4194048)!==0){var r=n.lanes;r&=t.pendingLanes,a|=r,n.lanes=a,Fn(t,a)}}var Zs={readContext:mn,use:al,useCallback:Xe,useContext:Xe,useEffect:Xe,useImperativeHandle:Xe,useLayoutEffect:Xe,useInsertionEffect:Xe,useMemo:Xe,useReducer:Xe,useRef:Xe,useState:Xe,useDebugValue:Xe,useDeferredValue:Xe,useTransition:Xe,useSyncExternalStore:Xe,useId:Xe,useHostTransitionStatus:Xe,useFormState:Xe,useActionState:Xe,useOptimistic:Xe,useMemoCache:Xe,useCacheRefresh:Xe};Zs.useEffectEvent=Xe;var _p={readContext:mn,use:al,useCallback:function(t,n){return An().memoizedState=[t,n===void 0?null:n],t},useContext:mn,useEffect:tp,useImperativeHandle:function(t,n,a){a=a!=null?a.concat([t]):null,sl(4194308,4,ap.bind(null,n,t),a)},useLayoutEffect:function(t,n){return sl(4194308,4,t,n)},useInsertionEffect:function(t,n){sl(4,2,t,n)},useMemo:function(t,n){var a=An();n=n===void 0?null:n;var r=t();if($a){wt(!0);try{t()}finally{wt(!1)}}return a.memoizedState=[r,n],r},useReducer:function(t,n,a){var r=An();if(a!==void 0){var u=a(n);if($a){wt(!0);try{a(n)}finally{wt(!1)}}}else u=n;return r.memoizedState=r.baseState=u,t={pending:null,lanes:0,dispatch:null,lastRenderedReducer:t,lastRenderedState:u},r.queue=t,t=t.dispatch=B0.bind(null,ne,t),[r.memoizedState,t]},useRef:function(t){var n=An();return t={current:t},n.memoizedState=t},useState:function(t){t=Sc(t);var n=t.queue,a=pp.bind(null,ne,n);return n.dispatch=a,[t.memoizedState,a]},useDebugValue:yc,useDeferredValue:function(t,n){var a=An();return Ec(a,t,n)},useTransition:function(){var t=Sc(!1);return t=up.bind(null,ne,t.queue,!0,!1),An().memoizedState=t,[!1,t]},useSyncExternalStore:function(t,n,a){var r=ne,u=An();if(me){if(a===void 0)throw Error(s(407));a=a()}else{if(a=n(),Oe===null)throw Error(s(349));(de&127)!==0||Id(r,n,a)}u.memoizedState=a;var f={value:a,getSnapshot:n};return u.queue=f,tp(Hd.bind(null,r,f,t),[t]),r.flags|=2048,Pr(9,{destroy:void 0},Fd.bind(null,r,f,a,n),null),a},useId:function(){var t=An(),n=Oe.identifierPrefix;if(me){var a=xi,r=Mi;a=(r&~(1<<32-Xt(r)-1)).toString(32)+a,n="_"+n+"R_"+a,a=nl++,0<a&&(n+="H"+a.toString(32)),n+="_"}else a=D0++,n="_"+n+"r_"+a.toString(32)+"_";return t.memoizedState=n},useHostTransitionStatus:bc,useFormState:Zd,useActionState:Zd,useOptimistic:function(t){var n=An();n.memoizedState=n.baseState=t;var a={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return n.queue=a,n=Ac.bind(null,ne,!0,a),a.dispatch=n,[t,n]},useMemoCache:gc,useCacheRefresh:function(){return An().memoizedState=P0.bind(null,ne)},useEffectEvent:function(t){var n=An(),a={impl:t};return n.memoizedState=a,function(){if((Se&2)!==0)throw Error(s(440));return a.impl.apply(void 0,arguments)}}},Rc={readContext:mn,use:al,useCallback:sp,useContext:mn,useEffect:xc,useImperativeHandle:rp,useInsertionEffect:np,useLayoutEffect:ip,useMemo:op,useReducer:rl,useRef:$d,useState:function(){return rl(Oi)},useDebugValue:yc,useDeferredValue:function(t,n){var a=Ye();return lp(a,we.memoizedState,t,n)},useTransition:function(){var t=rl(Oi)[0],n=Ye().memoizedState;return[typeof t=="boolean"?t:Ys(t),n]},useSyncExternalStore:Bd,useId:hp,useHostTransitionStatus:bc,useFormState:Kd,useActionState:Kd,useOptimistic:function(t,n){var a=Ye();return Xd(a,we,t,n)},useMemoCache:gc,useCacheRefresh:dp};Rc.useEffectEvent=ep;var vp={readContext:mn,use:al,useCallback:sp,useContext:mn,useEffect:xc,useImperativeHandle:rp,useInsertionEffect:np,useLayoutEffect:ip,useMemo:op,useReducer:vc,useRef:$d,useState:function(){return vc(Oi)},useDebugValue:yc,useDeferredValue:function(t,n){var a=Ye();return we===null?Ec(a,t,n):lp(a,we.memoizedState,t,n)},useTransition:function(){var t=vc(Oi)[0],n=Ye().memoizedState;return[typeof t=="boolean"?t:Ys(t),n]},useSyncExternalStore:Bd,useId:hp,useHostTransitionStatus:bc,useFormState:Jd,useActionState:Jd,useOptimistic:function(t,n){var a=Ye();return we!==null?Xd(a,we,t,n):(a.baseState=t,[t,a.queue.dispatch])},useMemoCache:gc,useCacheRefresh:dp};vp.useEffectEvent=ep;function Cc(t,n,a,r){n=t.memoizedState,a=a(r,n),a=a==null?n:_({},n,a),t.memoizedState=a,t.lanes===0&&(t.updateQueue.baseState=a)}var wc={enqueueSetState:function(t,n,a){t=t._reactInternals;var r=qn(),u=ca(r);u.payload=n,a!=null&&(u.callback=a),n=fa(t,u,r),n!==null&&(Pn(n,t,r),Xs(n,t,r))},enqueueReplaceState:function(t,n,a){t=t._reactInternals;var r=qn(),u=ca(r);u.tag=1,u.payload=n,a!=null&&(u.callback=a),n=fa(t,u,r),n!==null&&(Pn(n,t,r),Xs(n,t,r))},enqueueForceUpdate:function(t,n){t=t._reactInternals;var a=qn(),r=ca(a);r.tag=2,n!=null&&(r.callback=n),n=fa(t,r,a),n!==null&&(Pn(n,t,a),Xs(n,t,a))}};function Sp(t,n,a,r,u,f,S){return t=t.stateNode,typeof t.shouldComponentUpdate=="function"?t.shouldComponentUpdate(r,f,S):n.prototype&&n.prototype.isPureReactComponent?!zs(a,r)||!zs(u,f):!0}function Mp(t,n,a,r){t=n.state,typeof n.componentWillReceiveProps=="function"&&n.componentWillReceiveProps(a,r),typeof n.UNSAFE_componentWillReceiveProps=="function"&&n.UNSAFE_componentWillReceiveProps(a,r),n.state!==t&&wc.enqueueReplaceState(n,n.state,null)}function tr(t,n){var a=n;if("ref"in n){a={};for(var r in n)r!=="ref"&&(a[r]=n[r])}if(t=t.defaultProps){a===n&&(a=_({},a));for(var u in t)a[u]===void 0&&(a[u]=t[u])}return a}function xp(t){Ho(t)}function yp(t){console.error(t)}function Ep(t){Ho(t)}function ul(t,n){try{var a=t.onUncaughtError;a(n.value,{componentStack:n.stack})}catch(r){setTimeout(function(){throw r})}}function Tp(t,n,a){try{var r=t.onCaughtError;r(a.value,{componentStack:a.stack,errorBoundary:n.tag===1?n.stateNode:null})}catch(u){setTimeout(function(){throw u})}}function Dc(t,n,a){return a=ca(a),a.tag=3,a.payload={element:null},a.callback=function(){ul(t,n)},a}function bp(t){return t=ca(t),t.tag=3,t}function Ap(t,n,a,r){var u=a.type.getDerivedStateFromError;if(typeof u=="function"){var f=r.value;t.payload=function(){return u(f)},t.callback=function(){Tp(n,a,r)}}var S=a.stateNode;S!==null&&typeof S.componentDidCatch=="function"&&(t.callback=function(){Tp(n,a,r),typeof u!="function"&&(_a===null?_a=new Set([this]):_a.add(this));var E=r.stack;this.componentDidCatch(r.value,{componentStack:E!==null?E:""})})}function I0(t,n,a,r,u){if(a.flags|=32768,r!==null&&typeof r=="object"&&typeof r.then=="function"){if(n=a.alternate,n!==null&&Cr(n,a,u,!0),a=Vn.current,a!==null){switch(a.tag){case 31:case 13:return ni===null?xl():a.alternate===null&&We===0&&(We=3),a.flags&=-257,a.flags|=65536,a.lanes=u,r===Ko?a.flags|=16384:(n=a.updateQueue,n===null?a.updateQueue=new Set([r]):n.add(r),ef(t,r,u)),!1;case 22:return a.flags|=65536,r===Ko?a.flags|=16384:(n=a.updateQueue,n===null?(n={transitions:null,markerInstances:null,retryQueue:new Set([r])},a.updateQueue=n):(a=n.retryQueue,a===null?n.retryQueue=new Set([r]):a.add(r)),ef(t,r,u)),!1}throw Error(s(435,a.tag))}return ef(t,r,u),xl(),!1}if(me)return n=Vn.current,n!==null?((n.flags&65536)===0&&(n.flags|=256),n.flags|=65536,n.lanes=u,r!==Zu&&(t=Error(s(422),{cause:r}),Is(Jn(t,a)))):(r!==Zu&&(n=Error(s(423),{cause:r}),Is(Jn(n,a))),t=t.current.alternate,t.flags|=65536,u&=-u,t.lanes|=u,r=Jn(r,a),u=Dc(t.stateNode,r,u),sc(t,u),We!==4&&(We=2)),!1;var f=Error(s(520),{cause:r});if(f=Jn(f,a),io===null?io=[f]:io.push(f),We!==4&&(We=2),n===null)return!0;r=Jn(r,a),a=n;do{switch(a.tag){case 3:return a.flags|=65536,t=u&-u,a.lanes|=t,t=Dc(a.stateNode,r,t),sc(a,t),!1;case 1:if(n=a.type,f=a.stateNode,(a.flags&128)===0&&(typeof n.getDerivedStateFromError=="function"||f!==null&&typeof f.componentDidCatch=="function"&&(_a===null||!_a.has(f))))return a.flags|=65536,u&=-u,a.lanes|=u,u=bp(u),Ap(u,t,a,r),sc(a,u),!1}a=a.return}while(a!==null);return!1}var Lc=Error(s(461)),tn=!1;function gn(t,n,a,r){n.child=t===null?Dd(n,null,a,r):Ja(n,t.child,a,r)}function Rp(t,n,a,r,u){a=a.render;var f=n.ref;if("ref"in r){var S={};for(var E in r)E!=="ref"&&(S[E]=r[E])}else S=r;return ja(n),r=hc(t,n,a,S,f,u),E=dc(),t!==null&&!tn?(pc(t,n,u),zi(t,n,u)):(me&&E&&Yu(n),n.flags|=1,gn(t,n,r,u),n.child)}function Cp(t,n,a,r,u){if(t===null){var f=a.type;return typeof f=="function"&&!Wu(f)&&f.defaultProps===void 0&&a.compare===null?(n.tag=15,n.type=f,wp(t,n,f,r,u)):(t=Wo(a.type,null,r,n,n.mode,u),t.ref=n.ref,t.return=n,n.child=t)}if(f=t.child,!Fc(t,u)){var S=f.memoizedProps;if(a=a.compare,a=a!==null?a:zs,a(S,r)&&t.ref===n.ref)return zi(t,n,u)}return n.flags|=1,t=wi(f,r),t.ref=n.ref,t.return=n,n.child=t}function wp(t,n,a,r,u){if(t!==null){var f=t.memoizedProps;if(zs(f,r)&&t.ref===n.ref)if(tn=!1,n.pendingProps=r=f,Fc(t,u))(t.flags&131072)!==0&&(tn=!0);else return n.lanes=t.lanes,zi(t,n,u)}return Uc(t,n,a,r,u)}function Dp(t,n,a,r){var u=r.children,f=t!==null?t.memoizedState:null;if(t===null&&n.stateNode===null&&(n.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),r.mode==="hidden"){if((n.flags&128)!==0){if(f=f!==null?f.baseLanes|a:a,t!==null){for(r=n.child=t.child,u=0;r!==null;)u=u|r.lanes|r.childLanes,r=r.sibling;r=u&~f}else r=0,n.child=null;return Lp(t,n,f,a,r)}if((a&536870912)!==0)n.memoizedState={baseLanes:0,cachePool:null},t!==null&&jo(n,f!==null?f.cachePool:null),f!==null?Nd(n,f):lc(),Od(n);else return r=n.lanes=536870912,Lp(t,n,f!==null?f.baseLanes|a:a,a,r)}else f!==null?(jo(n,f.cachePool),Nd(n,f),da(),n.memoizedState=null):(t!==null&&jo(n,null),lc(),da());return gn(t,n,u,a),n.child}function Ks(t,n){return t!==null&&t.tag===22||n.stateNode!==null||(n.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),n.sibling}function Lp(t,n,a,r,u){var f=nc();return f=f===null?null:{parent:Je._currentValue,pool:f},n.memoizedState={baseLanes:a,cachePool:f},t!==null&&jo(n,null),lc(),Od(n),t!==null&&Cr(t,n,r,!0),n.childLanes=u,null}function cl(t,n){return n=hl({mode:n.mode,children:n.children},t.mode),n.ref=t.ref,t.child=n,n.return=t,n}function Up(t,n,a){return Ja(n,t.child,null,a),t=cl(n,n.pendingProps),t.flags|=2,Xn(n),n.memoizedState=null,t}function F0(t,n,a){var r=n.pendingProps,u=(n.flags&128)!==0;if(n.flags&=-129,t===null){if(me){if(r.mode==="hidden")return t=cl(n,r),n.lanes=536870912,Ks(null,t);if(cc(n),(t=Be)?(t=Wm(t,ei),t=t!==null&&t.data==="&"?t:null,t!==null&&(n.memoizedState={dehydrated:t,treeContext:ra!==null?{id:Mi,overflow:xi}:null,retryLane:536870912,hydrationErrors:null},a=md(t),a.return=n,n.child=a,pn=n,Be=null)):t=null,t===null)throw oa(n);return n.lanes=536870912,null}return cl(n,r)}var f=t.memoizedState;if(f!==null){var S=f.dehydrated;if(cc(n),u)if(n.flags&256)n.flags&=-257,n=Up(t,n,a);else if(n.memoizedState!==null)n.child=t.child,n.flags|=128,n=null;else throw Error(s(558));else if(tn||Cr(t,n,a,!1),u=(a&t.childLanes)!==0,tn||u){if(r=Oe,r!==null&&(S=xs(r,a),S!==0&&S!==f.retryLane))throw f.retryLane=S,Wa(t,S),Pn(r,t,S),Lc;xl(),n=Up(t,n,a)}else t=f.treeContext,Be=ii(S.nextSibling),pn=n,me=!0,sa=null,ei=!1,t!==null&&vd(n,t),n=cl(n,r),n.flags|=4096;return n}return t=wi(t.child,{mode:r.mode,children:r.children}),t.ref=n.ref,n.child=t,t.return=n,t}function fl(t,n){var a=n.ref;if(a===null)t!==null&&t.ref!==null&&(n.flags|=4194816);else{if(typeof a!="function"&&typeof a!="object")throw Error(s(284));(t===null||t.ref!==a)&&(n.flags|=4194816)}}function Uc(t,n,a,r,u){return ja(n),a=hc(t,n,a,r,void 0,u),r=dc(),t!==null&&!tn?(pc(t,n,u),zi(t,n,u)):(me&&r&&Yu(n),n.flags|=1,gn(t,n,a,u),n.child)}function Np(t,n,a,r,u,f){return ja(n),n.updateQueue=null,a=Pd(n,r,a,u),zd(t),r=dc(),t!==null&&!tn?(pc(t,n,f),zi(t,n,f)):(me&&r&&Yu(n),n.flags|=1,gn(t,n,a,f),n.child)}function Op(t,n,a,r,u){if(ja(n),n.stateNode===null){var f=Tr,S=a.contextType;typeof S=="object"&&S!==null&&(f=mn(S)),f=new a(r,f),n.memoizedState=f.state!==null&&f.state!==void 0?f.state:null,f.updater=wc,n.stateNode=f,f._reactInternals=n,f=n.stateNode,f.props=r,f.state=n.memoizedState,f.refs={},ac(n),S=a.contextType,f.context=typeof S=="object"&&S!==null?mn(S):Tr,f.state=n.memoizedState,S=a.getDerivedStateFromProps,typeof S=="function"&&(Cc(n,a,S,r),f.state=n.memoizedState),typeof a.getDerivedStateFromProps=="function"||typeof f.getSnapshotBeforeUpdate=="function"||typeof f.UNSAFE_componentWillMount!="function"&&typeof f.componentWillMount!="function"||(S=f.state,typeof f.componentWillMount=="function"&&f.componentWillMount(),typeof f.UNSAFE_componentWillMount=="function"&&f.UNSAFE_componentWillMount(),S!==f.state&&wc.enqueueReplaceState(f,f.state,null),ks(n,r,f,u),Ws(),f.state=n.memoizedState),typeof f.componentDidMount=="function"&&(n.flags|=4194308),r=!0}else if(t===null){f=n.stateNode;var E=n.memoizedProps,P=tr(a,E);f.props=P;var K=f.context,ut=a.contextType;S=Tr,typeof ut=="object"&&ut!==null&&(S=mn(ut));var ht=a.getDerivedStateFromProps;ut=typeof ht=="function"||typeof f.getSnapshotBeforeUpdate=="function",E=n.pendingProps!==E,ut||typeof f.UNSAFE_componentWillReceiveProps!="function"&&typeof f.componentWillReceiveProps!="function"||(E||K!==S)&&Mp(n,f,r,S),ua=!1;var J=n.memoizedState;f.state=J,ks(n,r,f,u),Ws(),K=n.memoizedState,E||J!==K||ua?(typeof ht=="function"&&(Cc(n,a,ht,r),K=n.memoizedState),(P=ua||Sp(n,a,P,r,J,K,S))?(ut||typeof f.UNSAFE_componentWillMount!="function"&&typeof f.componentWillMount!="function"||(typeof f.componentWillMount=="function"&&f.componentWillMount(),typeof f.UNSAFE_componentWillMount=="function"&&f.UNSAFE_componentWillMount()),typeof f.componentDidMount=="function"&&(n.flags|=4194308)):(typeof f.componentDidMount=="function"&&(n.flags|=4194308),n.memoizedProps=r,n.memoizedState=K),f.props=r,f.state=K,f.context=S,r=P):(typeof f.componentDidMount=="function"&&(n.flags|=4194308),r=!1)}else{f=n.stateNode,rc(t,n),S=n.memoizedProps,ut=tr(a,S),f.props=ut,ht=n.pendingProps,J=f.context,K=a.contextType,P=Tr,typeof K=="object"&&K!==null&&(P=mn(K)),E=a.getDerivedStateFromProps,(K=typeof E=="function"||typeof f.getSnapshotBeforeUpdate=="function")||typeof f.UNSAFE_componentWillReceiveProps!="function"&&typeof f.componentWillReceiveProps!="function"||(S!==ht||J!==P)&&Mp(n,f,r,P),ua=!1,J=n.memoizedState,f.state=J,ks(n,r,f,u),Ws();var st=n.memoizedState;S!==ht||J!==st||ua||t!==null&&t.dependencies!==null&&qo(t.dependencies)?(typeof E=="function"&&(Cc(n,a,E,r),st=n.memoizedState),(ut=ua||Sp(n,a,ut,r,J,st,P)||t!==null&&t.dependencies!==null&&qo(t.dependencies))?(K||typeof f.UNSAFE_componentWillUpdate!="function"&&typeof f.componentWillUpdate!="function"||(typeof f.componentWillUpdate=="function"&&f.componentWillUpdate(r,st,P),typeof f.UNSAFE_componentWillUpdate=="function"&&f.UNSAFE_componentWillUpdate(r,st,P)),typeof f.componentDidUpdate=="function"&&(n.flags|=4),typeof f.getSnapshotBeforeUpdate=="function"&&(n.flags|=1024)):(typeof f.componentDidUpdate!="function"||S===t.memoizedProps&&J===t.memoizedState||(n.flags|=4),typeof f.getSnapshotBeforeUpdate!="function"||S===t.memoizedProps&&J===t.memoizedState||(n.flags|=1024),n.memoizedProps=r,n.memoizedState=st),f.props=r,f.state=st,f.context=P,r=ut):(typeof f.componentDidUpdate!="function"||S===t.memoizedProps&&J===t.memoizedState||(n.flags|=4),typeof f.getSnapshotBeforeUpdate!="function"||S===t.memoizedProps&&J===t.memoizedState||(n.flags|=1024),r=!1)}return f=r,fl(t,n),r=(n.flags&128)!==0,f||r?(f=n.stateNode,a=r&&typeof a.getDerivedStateFromError!="function"?null:f.render(),n.flags|=1,t!==null&&r?(n.child=Ja(n,t.child,null,u),n.child=Ja(n,null,a,u)):gn(t,n,a,u),n.memoizedState=f.state,t=n.child):t=zi(t,n,u),t}function zp(t,n,a,r){return qa(),n.flags|=256,gn(t,n,a,r),n.child}var Nc={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function Oc(t){return{baseLanes:t,cachePool:Td()}}function zc(t,n,a){return t=t!==null?t.childLanes&~a:0,n&&(t|=kn),t}function Pp(t,n,a){var r=n.pendingProps,u=!1,f=(n.flags&128)!==0,S;if((S=f)||(S=t!==null&&t.memoizedState===null?!1:(qe.current&2)!==0),S&&(u=!0,n.flags&=-129),S=(n.flags&32)!==0,n.flags&=-33,t===null){if(me){if(u?ha(n):da(),(t=Be)?(t=Wm(t,ei),t=t!==null&&t.data!=="&"?t:null,t!==null&&(n.memoizedState={dehydrated:t,treeContext:ra!==null?{id:Mi,overflow:xi}:null,retryLane:536870912,hydrationErrors:null},a=md(t),a.return=n,n.child=a,pn=n,Be=null)):t=null,t===null)throw oa(n);return vf(t)?n.lanes=32:n.lanes=536870912,null}var E=r.children;return r=r.fallback,u?(da(),u=n.mode,E=hl({mode:"hidden",children:E},u),r=ka(r,u,a,null),E.return=n,r.return=n,E.sibling=r,n.child=E,r=n.child,r.memoizedState=Oc(a),r.childLanes=zc(t,S,a),n.memoizedState=Nc,Ks(null,r)):(ha(n),Pc(n,E))}var P=t.memoizedState;if(P!==null&&(E=P.dehydrated,E!==null)){if(f)n.flags&256?(ha(n),n.flags&=-257,n=Bc(t,n,a)):n.memoizedState!==null?(da(),n.child=t.child,n.flags|=128,n=null):(da(),E=r.fallback,u=n.mode,r=hl({mode:"visible",children:r.children},u),E=ka(E,u,a,null),E.flags|=2,r.return=n,E.return=n,r.sibling=E,n.child=r,Ja(n,t.child,null,a),r=n.child,r.memoizedState=Oc(a),r.childLanes=zc(t,S,a),n.memoizedState=Nc,n=Ks(null,r));else if(ha(n),vf(E)){if(S=E.nextSibling&&E.nextSibling.dataset,S)var K=S.dgst;S=K,r=Error(s(419)),r.stack="",r.digest=S,Is({value:r,source:null,stack:null}),n=Bc(t,n,a)}else if(tn||Cr(t,n,a,!1),S=(a&t.childLanes)!==0,tn||S){if(S=Oe,S!==null&&(r=xs(S,a),r!==0&&r!==P.retryLane))throw P.retryLane=r,Wa(t,r),Pn(S,t,r),Lc;_f(E)||xl(),n=Bc(t,n,a)}else _f(E)?(n.flags|=192,n.child=t.child,n=null):(t=P.treeContext,Be=ii(E.nextSibling),pn=n,me=!0,sa=null,ei=!1,t!==null&&vd(n,t),n=Pc(n,r.children),n.flags|=4096);return n}return u?(da(),E=r.fallback,u=n.mode,P=t.child,K=P.sibling,r=wi(P,{mode:"hidden",children:r.children}),r.subtreeFlags=P.subtreeFlags&65011712,K!==null?E=wi(K,E):(E=ka(E,u,a,null),E.flags|=2),E.return=n,r.return=n,r.sibling=E,n.child=r,Ks(null,r),r=n.child,E=t.child.memoizedState,E===null?E=Oc(a):(u=E.cachePool,u!==null?(P=Je._currentValue,u=u.parent!==P?{parent:P,pool:P}:u):u=Td(),E={baseLanes:E.baseLanes|a,cachePool:u}),r.memoizedState=E,r.childLanes=zc(t,S,a),n.memoizedState=Nc,Ks(t.child,r)):(ha(n),a=t.child,t=a.sibling,a=wi(a,{mode:"visible",children:r.children}),a.return=n,a.sibling=null,t!==null&&(S=n.deletions,S===null?(n.deletions=[t],n.flags|=16):S.push(t)),n.child=a,n.memoizedState=null,a)}function Pc(t,n){return n=hl({mode:"visible",children:n},t.mode),n.return=t,t.child=n}function hl(t,n){return t=Gn(22,t,null,n),t.lanes=0,t}function Bc(t,n,a){return Ja(n,t.child,null,a),t=Pc(n,n.pendingProps.children),t.flags|=2,n.memoizedState=null,t}function Bp(t,n,a){t.lanes|=n;var r=t.alternate;r!==null&&(r.lanes|=n),Ju(t.return,n,a)}function Ic(t,n,a,r,u,f){var S=t.memoizedState;S===null?t.memoizedState={isBackwards:n,rendering:null,renderingStartTime:0,last:r,tail:a,tailMode:u,treeForkCount:f}:(S.isBackwards=n,S.rendering=null,S.renderingStartTime=0,S.last=r,S.tail=a,S.tailMode=u,S.treeForkCount=f)}function Ip(t,n,a){var r=n.pendingProps,u=r.revealOrder,f=r.tail;r=r.children;var S=qe.current,E=(S&2)!==0;if(E?(S=S&1|2,n.flags|=128):S&=1,G(qe,S),gn(t,n,r,a),r=me?Bs:0,!E&&t!==null&&(t.flags&128)!==0)t:for(t=n.child;t!==null;){if(t.tag===13)t.memoizedState!==null&&Bp(t,a,n);else if(t.tag===19)Bp(t,a,n);else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===n)break t;for(;t.sibling===null;){if(t.return===null||t.return===n)break t;t=t.return}t.sibling.return=t.return,t=t.sibling}switch(u){case"forwards":for(a=n.child,u=null;a!==null;)t=a.alternate,t!==null&&tl(t)===null&&(u=a),a=a.sibling;a=u,a===null?(u=n.child,n.child=null):(u=a.sibling,a.sibling=null),Ic(n,!1,u,a,f,r);break;case"backwards":case"unstable_legacy-backwards":for(a=null,u=n.child,n.child=null;u!==null;){if(t=u.alternate,t!==null&&tl(t)===null){n.child=u;break}t=u.sibling,u.sibling=a,a=u,u=t}Ic(n,!0,a,null,f,r);break;case"together":Ic(n,!1,null,null,void 0,r);break;default:n.memoizedState=null}return n.child}function zi(t,n,a){if(t!==null&&(n.dependencies=t.dependencies),ga|=n.lanes,(a&n.childLanes)===0)if(t!==null){if(Cr(t,n,a,!1),(a&n.childLanes)===0)return null}else return null;if(t!==null&&n.child!==t.child)throw Error(s(153));if(n.child!==null){for(t=n.child,a=wi(t,t.pendingProps),n.child=a,a.return=n;t.sibling!==null;)t=t.sibling,a=a.sibling=wi(t,t.pendingProps),a.return=n;a.sibling=null}return n.child}function Fc(t,n){return(t.lanes&n)!==0?!0:(t=t.dependencies,!!(t!==null&&qo(t)))}function H0(t,n,a){switch(n.tag){case 3:It(n,n.stateNode.containerInfo),la(n,Je,t.memoizedState.cache),qa();break;case 27:case 5:kt(n);break;case 4:It(n,n.stateNode.containerInfo);break;case 10:la(n,n.type,n.memoizedProps.value);break;case 31:if(n.memoizedState!==null)return n.flags|=128,cc(n),null;break;case 13:var r=n.memoizedState;if(r!==null)return r.dehydrated!==null?(ha(n),n.flags|=128,null):(a&n.child.childLanes)!==0?Pp(t,n,a):(ha(n),t=zi(t,n,a),t!==null?t.sibling:null);ha(n);break;case 19:var u=(t.flags&128)!==0;if(r=(a&n.childLanes)!==0,r||(Cr(t,n,a,!1),r=(a&n.childLanes)!==0),u){if(r)return Ip(t,n,a);n.flags|=128}if(u=n.memoizedState,u!==null&&(u.rendering=null,u.tail=null,u.lastEffect=null),G(qe,qe.current),r)break;return null;case 22:return n.lanes=0,Dp(t,n,a,n.pendingProps);case 24:la(n,Je,t.memoizedState.cache)}return zi(t,n,a)}function Fp(t,n,a){if(t!==null)if(t.memoizedProps!==n.pendingProps)tn=!0;else{if(!Fc(t,a)&&(n.flags&128)===0)return tn=!1,H0(t,n,a);tn=(t.flags&131072)!==0}else tn=!1,me&&(n.flags&1048576)!==0&&_d(n,Bs,n.index);switch(n.lanes=0,n.tag){case 16:t:{var r=n.pendingProps;if(t=Ka(n.elementType),n.type=t,typeof t=="function")Wu(t)?(r=tr(t,r),n.tag=1,n=Op(null,n,t,r,a)):(n.tag=0,n=Uc(null,n,t,r,a));else{if(t!=null){var u=t.$$typeof;if(u===I){n.tag=11,n=Rp(null,n,t,r,a);break t}else if(u===z){n.tag=14,n=Cp(null,n,t,r,a);break t}}throw n=V(t)||t,Error(s(306,n,""))}}return n;case 0:return Uc(t,n,n.type,n.pendingProps,a);case 1:return r=n.type,u=tr(r,n.pendingProps),Op(t,n,r,u,a);case 3:t:{if(It(n,n.stateNode.containerInfo),t===null)throw Error(s(387));r=n.pendingProps;var f=n.memoizedState;u=f.element,rc(t,n),ks(n,r,null,a);var S=n.memoizedState;if(r=S.cache,la(n,Je,r),r!==f.cache&&$u(n,[Je],a,!0),Ws(),r=S.element,f.isDehydrated)if(f={element:r,isDehydrated:!1,cache:S.cache},n.updateQueue.baseState=f,n.memoizedState=f,n.flags&256){n=zp(t,n,r,a);break t}else if(r!==u){u=Jn(Error(s(424)),n),Is(u),n=zp(t,n,r,a);break t}else for(t=n.stateNode.containerInfo,t.nodeType===9?t=t.body:t=t.nodeName==="HTML"?t.ownerDocument.body:t,Be=ii(t.firstChild),pn=n,me=!0,sa=null,ei=!0,a=Dd(n,null,r,a),n.child=a;a;)a.flags=a.flags&-3|4096,a=a.sibling;else{if(qa(),r===u){n=zi(t,n,a);break t}gn(t,n,r,a)}n=n.child}return n;case 26:return fl(t,n),t===null?(a=Km(n.type,null,n.pendingProps,null))?n.memoizedState=a:me||(a=n.type,t=n.pendingProps,r=Cl(Mt.current).createElement(a),r[je]=n,r[Sn]=t,_n(r,a,t),Bt(r),n.stateNode=r):n.memoizedState=Km(n.type,t.memoizedProps,n.pendingProps,t.memoizedState),null;case 27:return kt(n),t===null&&me&&(r=n.stateNode=Ym(n.type,n.pendingProps,Mt.current),pn=n,ei=!0,u=Be,xa(n.type)?(Sf=u,Be=ii(r.firstChild)):Be=u),gn(t,n,n.pendingProps.children,a),fl(t,n),t===null&&(n.flags|=4194304),n.child;case 5:return t===null&&me&&((u=r=Be)&&(r=gS(r,n.type,n.pendingProps,ei),r!==null?(n.stateNode=r,pn=n,Be=ii(r.firstChild),ei=!1,u=!0):u=!1),u||oa(n)),kt(n),u=n.type,f=n.pendingProps,S=t!==null?t.memoizedProps:null,r=f.children,pf(u,f)?r=null:S!==null&&pf(u,S)&&(n.flags|=32),n.memoizedState!==null&&(u=hc(t,n,L0,null,null,a),fo._currentValue=u),fl(t,n),gn(t,n,r,a),n.child;case 6:return t===null&&me&&((t=a=Be)&&(a=_S(a,n.pendingProps,ei),a!==null?(n.stateNode=a,pn=n,Be=null,t=!0):t=!1),t||oa(n)),null;case 13:return Pp(t,n,a);case 4:return It(n,n.stateNode.containerInfo),r=n.pendingProps,t===null?n.child=Ja(n,null,r,a):gn(t,n,r,a),n.child;case 11:return Rp(t,n,n.type,n.pendingProps,a);case 7:return gn(t,n,n.pendingProps,a),n.child;case 8:return gn(t,n,n.pendingProps.children,a),n.child;case 12:return gn(t,n,n.pendingProps.children,a),n.child;case 10:return r=n.pendingProps,la(n,n.type,r.value),gn(t,n,r.children,a),n.child;case 9:return u=n.type._context,r=n.pendingProps.children,ja(n),u=mn(u),r=r(u),n.flags|=1,gn(t,n,r,a),n.child;case 14:return Cp(t,n,n.type,n.pendingProps,a);case 15:return wp(t,n,n.type,n.pendingProps,a);case 19:return Ip(t,n,a);case 31:return F0(t,n,a);case 22:return Dp(t,n,a,n.pendingProps);case 24:return ja(n),r=mn(Je),t===null?(u=nc(),u===null&&(u=Oe,f=tc(),u.pooledCache=f,f.refCount++,f!==null&&(u.pooledCacheLanes|=a),u=f),n.memoizedState={parent:r,cache:u},ac(n),la(n,Je,u)):((t.lanes&a)!==0&&(rc(t,n),ks(n,null,null,a),Ws()),u=t.memoizedState,f=n.memoizedState,u.parent!==r?(u={parent:r,cache:r},n.memoizedState=u,n.lanes===0&&(n.memoizedState=n.updateQueue.baseState=u),la(n,Je,r)):(r=f.cache,la(n,Je,r),r!==u.cache&&$u(n,[Je],a,!0))),gn(t,n,n.pendingProps.children,a),n.child;case 29:throw n.pendingProps}throw Error(s(156,n.tag))}function Pi(t){t.flags|=4}function Hc(t,n,a,r,u){if((n=(t.mode&32)!==0)&&(n=!1),n){if(t.flags|=16777216,(u&335544128)===u)if(t.stateNode.complete)t.flags|=8192;else if(hm())t.flags|=8192;else throw Qa=Ko,ic}else t.flags&=-16777217}function Hp(t,n){if(n.type!=="stylesheet"||(n.state.loading&4)!==0)t.flags&=-16777217;else if(t.flags|=16777216,!eg(n))if(hm())t.flags|=8192;else throw Qa=Ko,ic}function dl(t,n){n!==null&&(t.flags|=4),t.flags&16384&&(n=t.tag!==22?Ee():536870912,t.lanes|=n,Hr|=n)}function Qs(t,n){if(!me)switch(t.tailMode){case"hidden":n=t.tail;for(var a=null;n!==null;)n.alternate!==null&&(a=n),n=n.sibling;a===null?t.tail=null:a.sibling=null;break;case"collapsed":a=t.tail;for(var r=null;a!==null;)a.alternate!==null&&(r=a),a=a.sibling;r===null?n||t.tail===null?t.tail=null:t.tail.sibling=null:r.sibling=null}}function Ie(t){var n=t.alternate!==null&&t.alternate.child===t.child,a=0,r=0;if(n)for(var u=t.child;u!==null;)a|=u.lanes|u.childLanes,r|=u.subtreeFlags&65011712,r|=u.flags&65011712,u.return=t,u=u.sibling;else for(u=t.child;u!==null;)a|=u.lanes|u.childLanes,r|=u.subtreeFlags,r|=u.flags,u.return=t,u=u.sibling;return t.subtreeFlags|=r,t.childLanes=a,n}function G0(t,n,a){var r=n.pendingProps;switch(ju(n),n.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return Ie(n),null;case 1:return Ie(n),null;case 3:return a=n.stateNode,r=null,t!==null&&(r=t.memoizedState.cache),n.memoizedState.cache!==r&&(n.flags|=2048),Ui(Je),Nt(),a.pendingContext&&(a.context=a.pendingContext,a.pendingContext=null),(t===null||t.child===null)&&(Rr(n)?Pi(n):t===null||t.memoizedState.isDehydrated&&(n.flags&256)===0||(n.flags|=1024,Ku())),Ie(n),null;case 26:var u=n.type,f=n.memoizedState;return t===null?(Pi(n),f!==null?(Ie(n),Hp(n,f)):(Ie(n),Hc(n,u,null,r,a))):f?f!==t.memoizedState?(Pi(n),Ie(n),Hp(n,f)):(Ie(n),n.flags&=-16777217):(t=t.memoizedProps,t!==r&&Pi(n),Ie(n),Hc(n,u,t,r,a)),null;case 27:if(ue(n),a=Mt.current,u=n.type,t!==null&&n.stateNode!=null)t.memoizedProps!==r&&Pi(n);else{if(!r){if(n.stateNode===null)throw Error(s(166));return Ie(n),null}t=Z.current,Rr(n)?Sd(n):(t=Ym(u,r,a),n.stateNode=t,Pi(n))}return Ie(n),null;case 5:if(ue(n),u=n.type,t!==null&&n.stateNode!=null)t.memoizedProps!==r&&Pi(n);else{if(!r){if(n.stateNode===null)throw Error(s(166));return Ie(n),null}if(f=Z.current,Rr(n))Sd(n);else{var S=Cl(Mt.current);switch(f){case 1:f=S.createElementNS("http://www.w3.org/2000/svg",u);break;case 2:f=S.createElementNS("http://www.w3.org/1998/Math/MathML",u);break;default:switch(u){case"svg":f=S.createElementNS("http://www.w3.org/2000/svg",u);break;case"math":f=S.createElementNS("http://www.w3.org/1998/Math/MathML",u);break;case"script":f=S.createElement("div"),f.innerHTML="<script><\/script>",f=f.removeChild(f.firstChild);break;case"select":f=typeof r.is=="string"?S.createElement("select",{is:r.is}):S.createElement("select"),r.multiple?f.multiple=!0:r.size&&(f.size=r.size);break;default:f=typeof r.is=="string"?S.createElement(u,{is:r.is}):S.createElement(u)}}f[je]=n,f[Sn]=r;t:for(S=n.child;S!==null;){if(S.tag===5||S.tag===6)f.appendChild(S.stateNode);else if(S.tag!==4&&S.tag!==27&&S.child!==null){S.child.return=S,S=S.child;continue}if(S===n)break t;for(;S.sibling===null;){if(S.return===null||S.return===n)break t;S=S.return}S.sibling.return=S.return,S=S.sibling}n.stateNode=f;t:switch(_n(f,u,r),u){case"button":case"input":case"select":case"textarea":r=!!r.autoFocus;break t;case"img":r=!0;break t;default:r=!1}r&&Pi(n)}}return Ie(n),Hc(n,n.type,t===null?null:t.memoizedProps,n.pendingProps,a),null;case 6:if(t&&n.stateNode!=null)t.memoizedProps!==r&&Pi(n);else{if(typeof r!="string"&&n.stateNode===null)throw Error(s(166));if(t=Mt.current,Rr(n)){if(t=n.stateNode,a=n.memoizedProps,r=null,u=pn,u!==null)switch(u.tag){case 27:case 5:r=u.memoizedProps}t[je]=n,t=!!(t.nodeValue===a||r!==null&&r.suppressHydrationWarning===!0||Pm(t.nodeValue,a)),t||oa(n,!0)}else t=Cl(t).createTextNode(r),t[je]=n,n.stateNode=t}return Ie(n),null;case 31:if(a=n.memoizedState,t===null||t.memoizedState!==null){if(r=Rr(n),a!==null){if(t===null){if(!r)throw Error(s(318));if(t=n.memoizedState,t=t!==null?t.dehydrated:null,!t)throw Error(s(557));t[je]=n}else qa(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;Ie(n),t=!1}else a=Ku(),t!==null&&t.memoizedState!==null&&(t.memoizedState.hydrationErrors=a),t=!0;if(!t)return n.flags&256?(Xn(n),n):(Xn(n),null);if((n.flags&128)!==0)throw Error(s(558))}return Ie(n),null;case 13:if(r=n.memoizedState,t===null||t.memoizedState!==null&&t.memoizedState.dehydrated!==null){if(u=Rr(n),r!==null&&r.dehydrated!==null){if(t===null){if(!u)throw Error(s(318));if(u=n.memoizedState,u=u!==null?u.dehydrated:null,!u)throw Error(s(317));u[je]=n}else qa(),(n.flags&128)===0&&(n.memoizedState=null),n.flags|=4;Ie(n),u=!1}else u=Ku(),t!==null&&t.memoizedState!==null&&(t.memoizedState.hydrationErrors=u),u=!0;if(!u)return n.flags&256?(Xn(n),n):(Xn(n),null)}return Xn(n),(n.flags&128)!==0?(n.lanes=a,n):(a=r!==null,t=t!==null&&t.memoizedState!==null,a&&(r=n.child,u=null,r.alternate!==null&&r.alternate.memoizedState!==null&&r.alternate.memoizedState.cachePool!==null&&(u=r.alternate.memoizedState.cachePool.pool),f=null,r.memoizedState!==null&&r.memoizedState.cachePool!==null&&(f=r.memoizedState.cachePool.pool),f!==u&&(r.flags|=2048)),a!==t&&a&&(n.child.flags|=8192),dl(n,n.updateQueue),Ie(n),null);case 4:return Nt(),t===null&&uf(n.stateNode.containerInfo),Ie(n),null;case 10:return Ui(n.type),Ie(n),null;case 19:if(X(qe),r=n.memoizedState,r===null)return Ie(n),null;if(u=(n.flags&128)!==0,f=r.rendering,f===null)if(u)Qs(r,!1);else{if(We!==0||t!==null&&(t.flags&128)!==0)for(t=n.child;t!==null;){if(f=tl(t),f!==null){for(n.flags|=128,Qs(r,!1),t=f.updateQueue,n.updateQueue=t,dl(n,t),n.subtreeFlags=0,t=a,a=n.child;a!==null;)pd(a,t),a=a.sibling;return G(qe,qe.current&1|2),me&&Di(n,r.treeForkCount),n.child}t=t.sibling}r.tail!==null&&gt()>vl&&(n.flags|=128,u=!0,Qs(r,!1),n.lanes=4194304)}else{if(!u)if(t=tl(f),t!==null){if(n.flags|=128,u=!0,t=t.updateQueue,n.updateQueue=t,dl(n,t),Qs(r,!0),r.tail===null&&r.tailMode==="hidden"&&!f.alternate&&!me)return Ie(n),null}else 2*gt()-r.renderingStartTime>vl&&a!==536870912&&(n.flags|=128,u=!0,Qs(r,!1),n.lanes=4194304);r.isBackwards?(f.sibling=n.child,n.child=f):(t=r.last,t!==null?t.sibling=f:n.child=f,r.last=f)}return r.tail!==null?(t=r.tail,r.rendering=t,r.tail=t.sibling,r.renderingStartTime=gt(),t.sibling=null,a=qe.current,G(qe,u?a&1|2:a&1),me&&Di(n,r.treeForkCount),t):(Ie(n),null);case 22:case 23:return Xn(n),uc(),r=n.memoizedState!==null,t!==null?t.memoizedState!==null!==r&&(n.flags|=8192):r&&(n.flags|=8192),r?(a&536870912)!==0&&(n.flags&128)===0&&(Ie(n),n.subtreeFlags&6&&(n.flags|=8192)):Ie(n),a=n.updateQueue,a!==null&&dl(n,a.retryQueue),a=null,t!==null&&t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(a=t.memoizedState.cachePool.pool),r=null,n.memoizedState!==null&&n.memoizedState.cachePool!==null&&(r=n.memoizedState.cachePool.pool),r!==a&&(n.flags|=2048),t!==null&&X(Za),null;case 24:return a=null,t!==null&&(a=t.memoizedState.cache),n.memoizedState.cache!==a&&(n.flags|=2048),Ui(Je),Ie(n),null;case 25:return null;case 30:return null}throw Error(s(156,n.tag))}function V0(t,n){switch(ju(n),n.tag){case 1:return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 3:return Ui(Je),Nt(),t=n.flags,(t&65536)!==0&&(t&128)===0?(n.flags=t&-65537|128,n):null;case 26:case 27:case 5:return ue(n),null;case 31:if(n.memoizedState!==null){if(Xn(n),n.alternate===null)throw Error(s(340));qa()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 13:if(Xn(n),t=n.memoizedState,t!==null&&t.dehydrated!==null){if(n.alternate===null)throw Error(s(340));qa()}return t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 19:return X(qe),null;case 4:return Nt(),null;case 10:return Ui(n.type),null;case 22:case 23:return Xn(n),uc(),t!==null&&X(Za),t=n.flags,t&65536?(n.flags=t&-65537|128,n):null;case 24:return Ui(Je),null;case 25:return null;default:return null}}function Gp(t,n){switch(ju(n),n.tag){case 3:Ui(Je),Nt();break;case 26:case 27:case 5:ue(n);break;case 4:Nt();break;case 31:n.memoizedState!==null&&Xn(n);break;case 13:Xn(n);break;case 19:X(qe);break;case 10:Ui(n.type);break;case 22:case 23:Xn(n),uc(),t!==null&&X(Za);break;case 24:Ui(Je)}}function Js(t,n){try{var a=n.updateQueue,r=a!==null?a.lastEffect:null;if(r!==null){var u=r.next;a=u;do{if((a.tag&t)===t){r=void 0;var f=a.create,S=a.inst;r=f(),S.destroy=r}a=a.next}while(a!==u)}}catch(E){Ae(n,n.return,E)}}function pa(t,n,a){try{var r=n.updateQueue,u=r!==null?r.lastEffect:null;if(u!==null){var f=u.next;r=f;do{if((r.tag&t)===t){var S=r.inst,E=S.destroy;if(E!==void 0){S.destroy=void 0,u=n;var P=a,K=E;try{K()}catch(ut){Ae(u,P,ut)}}}r=r.next}while(r!==f)}}catch(ut){Ae(n,n.return,ut)}}function Vp(t){var n=t.updateQueue;if(n!==null){var a=t.stateNode;try{Ud(n,a)}catch(r){Ae(t,t.return,r)}}}function Xp(t,n,a){a.props=tr(t.type,t.memoizedProps),a.state=t.memoizedState;try{a.componentWillUnmount()}catch(r){Ae(t,n,r)}}function $s(t,n){try{var a=t.ref;if(a!==null){switch(t.tag){case 26:case 27:case 5:var r=t.stateNode;break;case 30:r=t.stateNode;break;default:r=t.stateNode}typeof a=="function"?t.refCleanup=a(r):a.current=r}}catch(u){Ae(t,n,u)}}function yi(t,n){var a=t.ref,r=t.refCleanup;if(a!==null)if(typeof r=="function")try{r()}catch(u){Ae(t,n,u)}finally{t.refCleanup=null,t=t.alternate,t!=null&&(t.refCleanup=null)}else if(typeof a=="function")try{a(null)}catch(u){Ae(t,n,u)}else a.current=null}function Wp(t){var n=t.type,a=t.memoizedProps,r=t.stateNode;try{t:switch(n){case"button":case"input":case"select":case"textarea":a.autoFocus&&r.focus();break t;case"img":a.src?r.src=a.src:a.srcSet&&(r.srcset=a.srcSet)}}catch(u){Ae(t,t.return,u)}}function Gc(t,n,a){try{var r=t.stateNode;cS(r,t.type,a,n),r[Sn]=n}catch(u){Ae(t,t.return,u)}}function kp(t){return t.tag===5||t.tag===3||t.tag===26||t.tag===27&&xa(t.type)||t.tag===4}function Vc(t){t:for(;;){for(;t.sibling===null;){if(t.return===null||kp(t.return))return null;t=t.return}for(t.sibling.return=t.return,t=t.sibling;t.tag!==5&&t.tag!==6&&t.tag!==18;){if(t.tag===27&&xa(t.type)||t.flags&2||t.child===null||t.tag===4)continue t;t.child.return=t,t=t.child}if(!(t.flags&2))return t.stateNode}}function Xc(t,n,a){var r=t.tag;if(r===5||r===6)t=t.stateNode,n?(a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a).insertBefore(t,n):(n=a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a,n.appendChild(t),a=a._reactRootContainer,a!=null||n.onclick!==null||(n.onclick=Ri));else if(r!==4&&(r===27&&xa(t.type)&&(a=t.stateNode,n=null),t=t.child,t!==null))for(Xc(t,n,a),t=t.sibling;t!==null;)Xc(t,n,a),t=t.sibling}function pl(t,n,a){var r=t.tag;if(r===5||r===6)t=t.stateNode,n?a.insertBefore(t,n):a.appendChild(t);else if(r!==4&&(r===27&&xa(t.type)&&(a=t.stateNode),t=t.child,t!==null))for(pl(t,n,a),t=t.sibling;t!==null;)pl(t,n,a),t=t.sibling}function qp(t){var n=t.stateNode,a=t.memoizedProps;try{for(var r=t.type,u=n.attributes;u.length;)n.removeAttributeNode(u[0]);_n(n,r,a),n[je]=t,n[Sn]=a}catch(f){Ae(t,t.return,f)}}var Bi=!1,en=!1,Wc=!1,Yp=typeof WeakSet=="function"?WeakSet:Set,cn=null;function X0(t,n){if(t=t.containerInfo,hf=zl,t=rd(t),Bu(t)){if("selectionStart"in t)var a={start:t.selectionStart,end:t.selectionEnd};else t:{a=(a=t.ownerDocument)&&a.defaultView||window;var r=a.getSelection&&a.getSelection();if(r&&r.rangeCount!==0){a=r.anchorNode;var u=r.anchorOffset,f=r.focusNode;r=r.focusOffset;try{a.nodeType,f.nodeType}catch{a=null;break t}var S=0,E=-1,P=-1,K=0,ut=0,ht=t,J=null;e:for(;;){for(var st;ht!==a||u!==0&&ht.nodeType!==3||(E=S+u),ht!==f||r!==0&&ht.nodeType!==3||(P=S+r),ht.nodeType===3&&(S+=ht.nodeValue.length),(st=ht.firstChild)!==null;)J=ht,ht=st;for(;;){if(ht===t)break e;if(J===a&&++K===u&&(E=S),J===f&&++ut===r&&(P=S),(st=ht.nextSibling)!==null)break;ht=J,J=ht.parentNode}ht=st}a=E===-1||P===-1?null:{start:E,end:P}}else a=null}a=a||{start:0,end:0}}else a=null;for(df={focusedElem:t,selectionRange:a},zl=!1,cn=n;cn!==null;)if(n=cn,t=n.child,(n.subtreeFlags&1028)!==0&&t!==null)t.return=n,cn=t;else for(;cn!==null;){switch(n=cn,f=n.alternate,t=n.flags,n.tag){case 0:if((t&4)!==0&&(t=n.updateQueue,t=t!==null?t.events:null,t!==null))for(a=0;a<t.length;a++)u=t[a],u.ref.impl=u.nextImpl;break;case 11:case 15:break;case 1:if((t&1024)!==0&&f!==null){t=void 0,a=n,u=f.memoizedProps,f=f.memoizedState,r=a.stateNode;try{var Lt=tr(a.type,u);t=r.getSnapshotBeforeUpdate(Lt,f),r.__reactInternalSnapshotBeforeUpdate=t}catch(Zt){Ae(a,a.return,Zt)}}break;case 3:if((t&1024)!==0){if(t=n.stateNode.containerInfo,a=t.nodeType,a===9)gf(t);else if(a===1)switch(t.nodeName){case"HEAD":case"HTML":case"BODY":gf(t);break;default:t.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;default:if((t&1024)!==0)throw Error(s(163))}if(t=n.sibling,t!==null){t.return=n.return,cn=t;break}cn=n.return}}function jp(t,n,a){var r=a.flags;switch(a.tag){case 0:case 11:case 15:Fi(t,a),r&4&&Js(5,a);break;case 1:if(Fi(t,a),r&4)if(t=a.stateNode,n===null)try{t.componentDidMount()}catch(S){Ae(a,a.return,S)}else{var u=tr(a.type,n.memoizedProps);n=n.memoizedState;try{t.componentDidUpdate(u,n,t.__reactInternalSnapshotBeforeUpdate)}catch(S){Ae(a,a.return,S)}}r&64&&Vp(a),r&512&&$s(a,a.return);break;case 3:if(Fi(t,a),r&64&&(t=a.updateQueue,t!==null)){if(n=null,a.child!==null)switch(a.child.tag){case 27:case 5:n=a.child.stateNode;break;case 1:n=a.child.stateNode}try{Ud(t,n)}catch(S){Ae(a,a.return,S)}}break;case 27:n===null&&r&4&&qp(a);case 26:case 5:Fi(t,a),n===null&&r&4&&Wp(a),r&512&&$s(a,a.return);break;case 12:Fi(t,a);break;case 31:Fi(t,a),r&4&&Qp(t,a);break;case 13:Fi(t,a),r&4&&Jp(t,a),r&64&&(t=a.memoizedState,t!==null&&(t=t.dehydrated,t!==null&&(a=J0.bind(null,a),vS(t,a))));break;case 22:if(r=a.memoizedState!==null||Bi,!r){n=n!==null&&n.memoizedState!==null||en,u=Bi;var f=en;Bi=r,(en=n)&&!f?Hi(t,a,(a.subtreeFlags&8772)!==0):Fi(t,a),Bi=u,en=f}break;case 30:break;default:Fi(t,a)}}function Zp(t){var n=t.alternate;n!==null&&(t.alternate=null,Zp(n)),t.child=null,t.deletions=null,t.sibling=null,t.tag===5&&(n=t.stateNode,n!==null&&et(n)),t.stateNode=null,t.return=null,t.dependencies=null,t.memoizedProps=null,t.memoizedState=null,t.pendingProps=null,t.stateNode=null,t.updateQueue=null}var Ge=null,Un=!1;function Ii(t,n,a){for(a=a.child;a!==null;)Kp(t,n,a),a=a.sibling}function Kp(t,n,a){if(Dt&&typeof Dt.onCommitFiberUnmount=="function")try{Dt.onCommitFiberUnmount(Kt,a)}catch{}switch(a.tag){case 26:en||yi(a,n),Ii(t,n,a),a.memoizedState?a.memoizedState.count--:a.stateNode&&(a=a.stateNode,a.parentNode.removeChild(a));break;case 27:en||yi(a,n);var r=Ge,u=Un;xa(a.type)&&(Ge=a.stateNode,Un=!1),Ii(t,n,a),lo(a.stateNode),Ge=r,Un=u;break;case 5:en||yi(a,n);case 6:if(r=Ge,u=Un,Ge=null,Ii(t,n,a),Ge=r,Un=u,Ge!==null)if(Un)try{(Ge.nodeType===9?Ge.body:Ge.nodeName==="HTML"?Ge.ownerDocument.body:Ge).removeChild(a.stateNode)}catch(f){Ae(a,n,f)}else try{Ge.removeChild(a.stateNode)}catch(f){Ae(a,n,f)}break;case 18:Ge!==null&&(Un?(t=Ge,Vm(t.nodeType===9?t.body:t.nodeName==="HTML"?t.ownerDocument.body:t,a.stateNode),jr(t)):Vm(Ge,a.stateNode));break;case 4:r=Ge,u=Un,Ge=a.stateNode.containerInfo,Un=!0,Ii(t,n,a),Ge=r,Un=u;break;case 0:case 11:case 14:case 15:pa(2,a,n),en||pa(4,a,n),Ii(t,n,a);break;case 1:en||(yi(a,n),r=a.stateNode,typeof r.componentWillUnmount=="function"&&Xp(a,n,r)),Ii(t,n,a);break;case 21:Ii(t,n,a);break;case 22:en=(r=en)||a.memoizedState!==null,Ii(t,n,a),en=r;break;default:Ii(t,n,a)}}function Qp(t,n){if(n.memoizedState===null&&(t=n.alternate,t!==null&&(t=t.memoizedState,t!==null))){t=t.dehydrated;try{jr(t)}catch(a){Ae(n,n.return,a)}}}function Jp(t,n){if(n.memoizedState===null&&(t=n.alternate,t!==null&&(t=t.memoizedState,t!==null&&(t=t.dehydrated,t!==null))))try{jr(t)}catch(a){Ae(n,n.return,a)}}function W0(t){switch(t.tag){case 31:case 13:case 19:var n=t.stateNode;return n===null&&(n=t.stateNode=new Yp),n;case 22:return t=t.stateNode,n=t._retryCache,n===null&&(n=t._retryCache=new Yp),n;default:throw Error(s(435,t.tag))}}function ml(t,n){var a=W0(t);n.forEach(function(r){if(!a.has(r)){a.add(r);var u=$0.bind(null,t,r);r.then(u,u)}})}function Nn(t,n){var a=n.deletions;if(a!==null)for(var r=0;r<a.length;r++){var u=a[r],f=t,S=n,E=S;t:for(;E!==null;){switch(E.tag){case 27:if(xa(E.type)){Ge=E.stateNode,Un=!1;break t}break;case 5:Ge=E.stateNode,Un=!1;break t;case 3:case 4:Ge=E.stateNode.containerInfo,Un=!0;break t}E=E.return}if(Ge===null)throw Error(s(160));Kp(f,S,u),Ge=null,Un=!1,f=u.alternate,f!==null&&(f.return=null),u.return=null}if(n.subtreeFlags&13886)for(n=n.child;n!==null;)$p(n,t),n=n.sibling}var ci=null;function $p(t,n){var a=t.alternate,r=t.flags;switch(t.tag){case 0:case 11:case 14:case 15:Nn(n,t),On(t),r&4&&(pa(3,t,t.return),Js(3,t),pa(5,t,t.return));break;case 1:Nn(n,t),On(t),r&512&&(en||a===null||yi(a,a.return)),r&64&&Bi&&(t=t.updateQueue,t!==null&&(r=t.callbacks,r!==null&&(a=t.shared.hiddenCallbacks,t.shared.hiddenCallbacks=a===null?r:a.concat(r))));break;case 26:var u=ci;if(Nn(n,t),On(t),r&512&&(en||a===null||yi(a,a.return)),r&4){var f=a!==null?a.memoizedState:null;if(r=t.memoizedState,a===null)if(r===null)if(t.stateNode===null){t:{r=t.type,a=t.memoizedProps,u=u.ownerDocument||u;e:switch(r){case"title":f=u.getElementsByTagName("title")[0],(!f||f[rt]||f[je]||f.namespaceURI==="http://www.w3.org/2000/svg"||f.hasAttribute("itemprop"))&&(f=u.createElement(r),u.head.insertBefore(f,u.querySelector("head > title"))),_n(f,r,a),f[je]=t,Bt(f),r=f;break t;case"link":var S=$m("link","href",u).get(r+(a.href||""));if(S){for(var E=0;E<S.length;E++)if(f=S[E],f.getAttribute("href")===(a.href==null||a.href===""?null:a.href)&&f.getAttribute("rel")===(a.rel==null?null:a.rel)&&f.getAttribute("title")===(a.title==null?null:a.title)&&f.getAttribute("crossorigin")===(a.crossOrigin==null?null:a.crossOrigin)){S.splice(E,1);break e}}f=u.createElement(r),_n(f,r,a),u.head.appendChild(f);break;case"meta":if(S=$m("meta","content",u).get(r+(a.content||""))){for(E=0;E<S.length;E++)if(f=S[E],f.getAttribute("content")===(a.content==null?null:""+a.content)&&f.getAttribute("name")===(a.name==null?null:a.name)&&f.getAttribute("property")===(a.property==null?null:a.property)&&f.getAttribute("http-equiv")===(a.httpEquiv==null?null:a.httpEquiv)&&f.getAttribute("charset")===(a.charSet==null?null:a.charSet)){S.splice(E,1);break e}}f=u.createElement(r),_n(f,r,a),u.head.appendChild(f);break;default:throw Error(s(468,r))}f[je]=t,Bt(f),r=f}t.stateNode=r}else tg(u,t.type,t.stateNode);else t.stateNode=Jm(u,r,t.memoizedProps);else f!==r?(f===null?a.stateNode!==null&&(a=a.stateNode,a.parentNode.removeChild(a)):f.count--,r===null?tg(u,t.type,t.stateNode):Jm(u,r,t.memoizedProps)):r===null&&t.stateNode!==null&&Gc(t,t.memoizedProps,a.memoizedProps)}break;case 27:Nn(n,t),On(t),r&512&&(en||a===null||yi(a,a.return)),a!==null&&r&4&&Gc(t,t.memoizedProps,a.memoizedProps);break;case 5:if(Nn(n,t),On(t),r&512&&(en||a===null||yi(a,a.return)),t.flags&32){u=t.stateNode;try{_r(u,"")}catch(Lt){Ae(t,t.return,Lt)}}r&4&&t.stateNode!=null&&(u=t.memoizedProps,Gc(t,u,a!==null?a.memoizedProps:u)),r&1024&&(Wc=!0);break;case 6:if(Nn(n,t),On(t),r&4){if(t.stateNode===null)throw Error(s(162));r=t.memoizedProps,a=t.stateNode;try{a.nodeValue=r}catch(Lt){Ae(t,t.return,Lt)}}break;case 3:if(Ll=null,u=ci,ci=wl(n.containerInfo),Nn(n,t),ci=u,On(t),r&4&&a!==null&&a.memoizedState.isDehydrated)try{jr(n.containerInfo)}catch(Lt){Ae(t,t.return,Lt)}Wc&&(Wc=!1,tm(t));break;case 4:r=ci,ci=wl(t.stateNode.containerInfo),Nn(n,t),On(t),ci=r;break;case 12:Nn(n,t),On(t);break;case 31:Nn(n,t),On(t),r&4&&(r=t.updateQueue,r!==null&&(t.updateQueue=null,ml(t,r)));break;case 13:Nn(n,t),On(t),t.child.flags&8192&&t.memoizedState!==null!=(a!==null&&a.memoizedState!==null)&&(_l=gt()),r&4&&(r=t.updateQueue,r!==null&&(t.updateQueue=null,ml(t,r)));break;case 22:u=t.memoizedState!==null;var P=a!==null&&a.memoizedState!==null,K=Bi,ut=en;if(Bi=K||u,en=ut||P,Nn(n,t),en=ut,Bi=K,On(t),r&8192)t:for(n=t.stateNode,n._visibility=u?n._visibility&-2:n._visibility|1,u&&(a===null||P||Bi||en||er(t)),a=null,n=t;;){if(n.tag===5||n.tag===26){if(a===null){P=a=n;try{if(f=P.stateNode,u)S=f.style,typeof S.setProperty=="function"?S.setProperty("display","none","important"):S.display="none";else{E=P.stateNode;var ht=P.memoizedProps.style,J=ht!=null&&ht.hasOwnProperty("display")?ht.display:null;E.style.display=J==null||typeof J=="boolean"?"":(""+J).trim()}}catch(Lt){Ae(P,P.return,Lt)}}}else if(n.tag===6){if(a===null){P=n;try{P.stateNode.nodeValue=u?"":P.memoizedProps}catch(Lt){Ae(P,P.return,Lt)}}}else if(n.tag===18){if(a===null){P=n;try{var st=P.stateNode;u?Xm(st,!0):Xm(P.stateNode,!1)}catch(Lt){Ae(P,P.return,Lt)}}}else if((n.tag!==22&&n.tag!==23||n.memoizedState===null||n===t)&&n.child!==null){n.child.return=n,n=n.child;continue}if(n===t)break t;for(;n.sibling===null;){if(n.return===null||n.return===t)break t;a===n&&(a=null),n=n.return}a===n&&(a=null),n.sibling.return=n.return,n=n.sibling}r&4&&(r=t.updateQueue,r!==null&&(a=r.retryQueue,a!==null&&(r.retryQueue=null,ml(t,a))));break;case 19:Nn(n,t),On(t),r&4&&(r=t.updateQueue,r!==null&&(t.updateQueue=null,ml(t,r)));break;case 30:break;case 21:break;default:Nn(n,t),On(t)}}function On(t){var n=t.flags;if(n&2){try{for(var a,r=t.return;r!==null;){if(kp(r)){a=r;break}r=r.return}if(a==null)throw Error(s(160));switch(a.tag){case 27:var u=a.stateNode,f=Vc(t);pl(t,f,u);break;case 5:var S=a.stateNode;a.flags&32&&(_r(S,""),a.flags&=-33);var E=Vc(t);pl(t,E,S);break;case 3:case 4:var P=a.stateNode.containerInfo,K=Vc(t);Xc(t,K,P);break;default:throw Error(s(161))}}catch(ut){Ae(t,t.return,ut)}t.flags&=-3}n&4096&&(t.flags&=-4097)}function tm(t){if(t.subtreeFlags&1024)for(t=t.child;t!==null;){var n=t;tm(n),n.tag===5&&n.flags&1024&&n.stateNode.reset(),t=t.sibling}}function Fi(t,n){if(n.subtreeFlags&8772)for(n=n.child;n!==null;)jp(t,n.alternate,n),n=n.sibling}function er(t){for(t=t.child;t!==null;){var n=t;switch(n.tag){case 0:case 11:case 14:case 15:pa(4,n,n.return),er(n);break;case 1:yi(n,n.return);var a=n.stateNode;typeof a.componentWillUnmount=="function"&&Xp(n,n.return,a),er(n);break;case 27:lo(n.stateNode);case 26:case 5:yi(n,n.return),er(n);break;case 22:n.memoizedState===null&&er(n);break;case 30:er(n);break;default:er(n)}t=t.sibling}}function Hi(t,n,a){for(a=a&&(n.subtreeFlags&8772)!==0,n=n.child;n!==null;){var r=n.alternate,u=t,f=n,S=f.flags;switch(f.tag){case 0:case 11:case 15:Hi(u,f,a),Js(4,f);break;case 1:if(Hi(u,f,a),r=f,u=r.stateNode,typeof u.componentDidMount=="function")try{u.componentDidMount()}catch(K){Ae(r,r.return,K)}if(r=f,u=r.updateQueue,u!==null){var E=r.stateNode;try{var P=u.shared.hiddenCallbacks;if(P!==null)for(u.shared.hiddenCallbacks=null,u=0;u<P.length;u++)Ld(P[u],E)}catch(K){Ae(r,r.return,K)}}a&&S&64&&Vp(f),$s(f,f.return);break;case 27:qp(f);case 26:case 5:Hi(u,f,a),a&&r===null&&S&4&&Wp(f),$s(f,f.return);break;case 12:Hi(u,f,a);break;case 31:Hi(u,f,a),a&&S&4&&Qp(u,f);break;case 13:Hi(u,f,a),a&&S&4&&Jp(u,f);break;case 22:f.memoizedState===null&&Hi(u,f,a),$s(f,f.return);break;case 30:break;default:Hi(u,f,a)}n=n.sibling}}function kc(t,n){var a=null;t!==null&&t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(a=t.memoizedState.cachePool.pool),t=null,n.memoizedState!==null&&n.memoizedState.cachePool!==null&&(t=n.memoizedState.cachePool.pool),t!==a&&(t!=null&&t.refCount++,a!=null&&Fs(a))}function qc(t,n){t=null,n.alternate!==null&&(t=n.alternate.memoizedState.cache),n=n.memoizedState.cache,n!==t&&(n.refCount++,t!=null&&Fs(t))}function fi(t,n,a,r){if(n.subtreeFlags&10256)for(n=n.child;n!==null;)em(t,n,a,r),n=n.sibling}function em(t,n,a,r){var u=n.flags;switch(n.tag){case 0:case 11:case 15:fi(t,n,a,r),u&2048&&Js(9,n);break;case 1:fi(t,n,a,r);break;case 3:fi(t,n,a,r),u&2048&&(t=null,n.alternate!==null&&(t=n.alternate.memoizedState.cache),n=n.memoizedState.cache,n!==t&&(n.refCount++,t!=null&&Fs(t)));break;case 12:if(u&2048){fi(t,n,a,r),t=n.stateNode;try{var f=n.memoizedProps,S=f.id,E=f.onPostCommit;typeof E=="function"&&E(S,n.alternate===null?"mount":"update",t.passiveEffectDuration,-0)}catch(P){Ae(n,n.return,P)}}else fi(t,n,a,r);break;case 31:fi(t,n,a,r);break;case 13:fi(t,n,a,r);break;case 23:break;case 22:f=n.stateNode,S=n.alternate,n.memoizedState!==null?f._visibility&2?fi(t,n,a,r):to(t,n):f._visibility&2?fi(t,n,a,r):(f._visibility|=2,Br(t,n,a,r,(n.subtreeFlags&10256)!==0||!1)),u&2048&&kc(S,n);break;case 24:fi(t,n,a,r),u&2048&&qc(n.alternate,n);break;default:fi(t,n,a,r)}}function Br(t,n,a,r,u){for(u=u&&((n.subtreeFlags&10256)!==0||!1),n=n.child;n!==null;){var f=t,S=n,E=a,P=r,K=S.flags;switch(S.tag){case 0:case 11:case 15:Br(f,S,E,P,u),Js(8,S);break;case 23:break;case 22:var ut=S.stateNode;S.memoizedState!==null?ut._visibility&2?Br(f,S,E,P,u):to(f,S):(ut._visibility|=2,Br(f,S,E,P,u)),u&&K&2048&&kc(S.alternate,S);break;case 24:Br(f,S,E,P,u),u&&K&2048&&qc(S.alternate,S);break;default:Br(f,S,E,P,u)}n=n.sibling}}function to(t,n){if(n.subtreeFlags&10256)for(n=n.child;n!==null;){var a=t,r=n,u=r.flags;switch(r.tag){case 22:to(a,r),u&2048&&kc(r.alternate,r);break;case 24:to(a,r),u&2048&&qc(r.alternate,r);break;default:to(a,r)}n=n.sibling}}var eo=8192;function Ir(t,n,a){if(t.subtreeFlags&eo)for(t=t.child;t!==null;)nm(t,n,a),t=t.sibling}function nm(t,n,a){switch(t.tag){case 26:Ir(t,n,a),t.flags&eo&&t.memoizedState!==null&&DS(a,ci,t.memoizedState,t.memoizedProps);break;case 5:Ir(t,n,a);break;case 3:case 4:var r=ci;ci=wl(t.stateNode.containerInfo),Ir(t,n,a),ci=r;break;case 22:t.memoizedState===null&&(r=t.alternate,r!==null&&r.memoizedState!==null?(r=eo,eo=16777216,Ir(t,n,a),eo=r):Ir(t,n,a));break;default:Ir(t,n,a)}}function im(t){var n=t.alternate;if(n!==null&&(t=n.child,t!==null)){n.child=null;do n=t.sibling,t.sibling=null,t=n;while(t!==null)}}function no(t){var n=t.deletions;if((t.flags&16)!==0){if(n!==null)for(var a=0;a<n.length;a++){var r=n[a];cn=r,rm(r,t)}im(t)}if(t.subtreeFlags&10256)for(t=t.child;t!==null;)am(t),t=t.sibling}function am(t){switch(t.tag){case 0:case 11:case 15:no(t),t.flags&2048&&pa(9,t,t.return);break;case 3:no(t);break;case 12:no(t);break;case 22:var n=t.stateNode;t.memoizedState!==null&&n._visibility&2&&(t.return===null||t.return.tag!==13)?(n._visibility&=-3,gl(t)):no(t);break;default:no(t)}}function gl(t){var n=t.deletions;if((t.flags&16)!==0){if(n!==null)for(var a=0;a<n.length;a++){var r=n[a];cn=r,rm(r,t)}im(t)}for(t=t.child;t!==null;){switch(n=t,n.tag){case 0:case 11:case 15:pa(8,n,n.return),gl(n);break;case 22:a=n.stateNode,a._visibility&2&&(a._visibility&=-3,gl(n));break;default:gl(n)}t=t.sibling}}function rm(t,n){for(;cn!==null;){var a=cn;switch(a.tag){case 0:case 11:case 15:pa(8,a,n);break;case 23:case 22:if(a.memoizedState!==null&&a.memoizedState.cachePool!==null){var r=a.memoizedState.cachePool.pool;r!=null&&r.refCount++}break;case 24:Fs(a.memoizedState.cache)}if(r=a.child,r!==null)r.return=a,cn=r;else t:for(a=t;cn!==null;){r=cn;var u=r.sibling,f=r.return;if(Zp(r),r===a){cn=null;break t}if(u!==null){u.return=f,cn=u;break t}cn=f}}}var k0={getCacheForType:function(t){var n=mn(Je),a=n.data.get(t);return a===void 0&&(a=t(),n.data.set(t,a)),a},cacheSignal:function(){return mn(Je).controller.signal}},q0=typeof WeakMap=="function"?WeakMap:Map,Se=0,Oe=null,fe=null,de=0,be=0,Wn=null,ma=!1,Fr=!1,Yc=!1,Gi=0,We=0,ga=0,nr=0,jc=0,kn=0,Hr=0,io=null,zn=null,Zc=!1,_l=0,sm=0,vl=1/0,Sl=null,_a=null,an=0,va=null,Gr=null,Vi=0,Kc=0,Qc=null,om=null,ao=0,Jc=null;function qn(){return(Se&2)!==0&&de!==0?de&-de:O.T!==null?rf():Es()}function lm(){if(kn===0)if((de&536870912)===0||me){var t=F;F<<=1,(F&3932160)===0&&(F=262144),kn=t}else kn=536870912;return t=Vn.current,t!==null&&(t.flags|=32),kn}function Pn(t,n,a){(t===Oe&&(be===2||be===9)||t.cancelPendingCommit!==null)&&(Vr(t,0),Sa(t,de,kn,!1)),ke(t,a),((Se&2)===0||t!==Oe)&&(t===Oe&&((Se&2)===0&&(nr|=a),We===4&&Sa(t,de,kn,!1)),Ei(t))}function um(t,n,a){if((Se&6)!==0)throw Error(s(327));var r=!a&&(n&127)===0&&(n&t.expiredLanes)===0||Gt(t,n),u=r?Z0(t,n):tf(t,n,!0),f=r;do{if(u===0){Fr&&!r&&Sa(t,n,0,!1);break}else{if(a=t.current.alternate,f&&!Y0(a)){u=tf(t,n,!1),f=!1;continue}if(u===2){if(f=n,t.errorRecoveryDisabledLanes&f)var S=0;else S=t.pendingLanes&-536870913,S=S!==0?S:S&536870912?536870912:0;if(S!==0){n=S;t:{var E=t;u=io;var P=E.current.memoizedState.isDehydrated;if(P&&(Vr(E,S).flags|=256),S=tf(E,S,!1),S!==2){if(Yc&&!P){E.errorRecoveryDisabledLanes|=f,nr|=f,u=4;break t}f=zn,zn=u,f!==null&&(zn===null?zn=f:zn.push.apply(zn,f))}u=S}if(f=!1,u!==2)continue}}if(u===1){Vr(t,0),Sa(t,n,0,!0);break}t:{switch(r=t,f=u,f){case 0:case 1:throw Error(s(345));case 4:if((n&4194048)!==n)break;case 6:Sa(r,n,kn,!ma);break t;case 2:zn=null;break;case 3:case 5:break;default:throw Error(s(329))}if((n&62914560)===n&&(u=_l+300-gt(),10<u)){if(Sa(r,n,kn,!ma),jt(r,0,!0)!==0)break t;Vi=n,r.timeoutHandle=Hm(cm.bind(null,r,a,zn,Sl,Zc,n,kn,nr,Hr,ma,f,"Throttled",-0,0),u);break t}cm(r,a,zn,Sl,Zc,n,kn,nr,Hr,ma,f,null,-0,0)}}break}while(!0);Ei(t)}function cm(t,n,a,r,u,f,S,E,P,K,ut,ht,J,st){if(t.timeoutHandle=-1,ht=n.subtreeFlags,ht&8192||(ht&16785408)===16785408){ht={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:Ri},nm(n,f,ht);var Lt=(f&62914560)===f?_l-gt():(f&4194048)===f?sm-gt():0;if(Lt=LS(ht,Lt),Lt!==null){Vi=f,t.cancelPendingCommit=Lt(vm.bind(null,t,n,f,a,r,u,S,E,P,ut,ht,null,J,st)),Sa(t,f,S,!K);return}}vm(t,n,f,a,r,u,S,E,P)}function Y0(t){for(var n=t;;){var a=n.tag;if((a===0||a===11||a===15)&&n.flags&16384&&(a=n.updateQueue,a!==null&&(a=a.stores,a!==null)))for(var r=0;r<a.length;r++){var u=a[r],f=u.getSnapshot;u=u.value;try{if(!Hn(f(),u))return!1}catch{return!1}}if(a=n.child,n.subtreeFlags&16384&&a!==null)a.return=n,n=a;else{if(n===t)break;for(;n.sibling===null;){if(n.return===null||n.return===t)return!0;n=n.return}n.sibling.return=n.return,n=n.sibling}}return!0}function Sa(t,n,a,r){n&=~jc,n&=~nr,t.suspendedLanes|=n,t.pingedLanes&=~n,r&&(t.warmLanes|=n),r=t.expirationTimes;for(var u=n;0<u;){var f=31-Xt(u),S=1<<f;r[f]=-1,u&=~S}a!==0&&un(t,a,n)}function Ml(){return(Se&6)===0?(ro(0),!1):!0}function $c(){if(fe!==null){if(be===0)var t=fe.return;else t=fe,Li=Ya=null,mc(t),Ur=null,Gs=0,t=fe;for(;t!==null;)Gp(t.alternate,t),t=t.return;fe=null}}function Vr(t,n){var a=t.timeoutHandle;a!==-1&&(t.timeoutHandle=-1,dS(a)),a=t.cancelPendingCommit,a!==null&&(t.cancelPendingCommit=null,a()),Vi=0,$c(),Oe=t,fe=a=wi(t.current,null),de=n,be=0,Wn=null,ma=!1,Fr=Gt(t,n),Yc=!1,Hr=kn=jc=nr=ga=We=0,zn=io=null,Zc=!1,(n&8)!==0&&(n|=n&32);var r=t.entangledLanes;if(r!==0)for(t=t.entanglements,r&=n;0<r;){var u=31-Xt(r),f=1<<u;n|=t[u],r&=~f}return Gi=n,Go(),a}function fm(t,n){ne=null,O.H=Zs,n===Lr||n===Zo?(n=Rd(),be=3):n===ic?(n=Rd(),be=4):be=n===Lc?8:n!==null&&typeof n=="object"&&typeof n.then=="function"?6:1,Wn=n,fe===null&&(We=1,ul(t,Jn(n,t.current)))}function hm(){var t=Vn.current;return t===null?!0:(de&4194048)===de?ni===null:(de&62914560)===de||(de&536870912)!==0?t===ni:!1}function dm(){var t=O.H;return O.H=Zs,t===null?Zs:t}function pm(){var t=O.A;return O.A=k0,t}function xl(){We=4,ma||(de&4194048)!==de&&Vn.current!==null||(Fr=!0),(ga&134217727)===0&&(nr&134217727)===0||Oe===null||Sa(Oe,de,kn,!1)}function tf(t,n,a){var r=Se;Se|=2;var u=dm(),f=pm();(Oe!==t||de!==n)&&(Sl=null,Vr(t,n)),n=!1;var S=We;t:do try{if(be!==0&&fe!==null){var E=fe,P=Wn;switch(be){case 8:$c(),S=6;break t;case 3:case 2:case 9:case 6:Vn.current===null&&(n=!0);var K=be;if(be=0,Wn=null,Xr(t,E,P,K),a&&Fr){S=0;break t}break;default:K=be,be=0,Wn=null,Xr(t,E,P,K)}}j0(),S=We;break}catch(ut){fm(t,ut)}while(!0);return n&&t.shellSuspendCounter++,Li=Ya=null,Se=r,O.H=u,O.A=f,fe===null&&(Oe=null,de=0,Go()),S}function j0(){for(;fe!==null;)mm(fe)}function Z0(t,n){var a=Se;Se|=2;var r=dm(),u=pm();Oe!==t||de!==n?(Sl=null,vl=gt()+500,Vr(t,n)):Fr=Gt(t,n);t:do try{if(be!==0&&fe!==null){n=fe;var f=Wn;e:switch(be){case 1:be=0,Wn=null,Xr(t,n,f,1);break;case 2:case 9:if(bd(f)){be=0,Wn=null,gm(n);break}n=function(){be!==2&&be!==9||Oe!==t||(be=7),Ei(t)},f.then(n,n);break t;case 3:be=7;break t;case 4:be=5;break t;case 7:bd(f)?(be=0,Wn=null,gm(n)):(be=0,Wn=null,Xr(t,n,f,7));break;case 5:var S=null;switch(fe.tag){case 26:S=fe.memoizedState;case 5:case 27:var E=fe;if(S?eg(S):E.stateNode.complete){be=0,Wn=null;var P=E.sibling;if(P!==null)fe=P;else{var K=E.return;K!==null?(fe=K,yl(K)):fe=null}break e}}be=0,Wn=null,Xr(t,n,f,5);break;case 6:be=0,Wn=null,Xr(t,n,f,6);break;case 8:$c(),We=6;break t;default:throw Error(s(462))}}K0();break}catch(ut){fm(t,ut)}while(!0);return Li=Ya=null,O.H=r,O.A=u,Se=a,fe!==null?0:(Oe=null,de=0,Go(),We)}function K0(){for(;fe!==null&&!St();)mm(fe)}function mm(t){var n=Fp(t.alternate,t,Gi);t.memoizedProps=t.pendingProps,n===null?yl(t):fe=n}function gm(t){var n=t,a=n.alternate;switch(n.tag){case 15:case 0:n=Np(a,n,n.pendingProps,n.type,void 0,de);break;case 11:n=Np(a,n,n.pendingProps,n.type.render,n.ref,de);break;case 5:mc(n);default:Gp(a,n),n=fe=pd(n,Gi),n=Fp(a,n,Gi)}t.memoizedProps=t.pendingProps,n===null?yl(t):fe=n}function Xr(t,n,a,r){Li=Ya=null,mc(n),Ur=null,Gs=0;var u=n.return;try{if(I0(t,u,n,a,de)){We=1,ul(t,Jn(a,t.current)),fe=null;return}}catch(f){if(u!==null)throw fe=u,f;We=1,ul(t,Jn(a,t.current)),fe=null;return}n.flags&32768?(me||r===1?t=!0:Fr||(de&536870912)!==0?t=!1:(ma=t=!0,(r===2||r===9||r===3||r===6)&&(r=Vn.current,r!==null&&r.tag===13&&(r.flags|=16384))),_m(n,t)):yl(n)}function yl(t){var n=t;do{if((n.flags&32768)!==0){_m(n,ma);return}t=n.return;var a=G0(n.alternate,n,Gi);if(a!==null){fe=a;return}if(n=n.sibling,n!==null){fe=n;return}fe=n=t}while(n!==null);We===0&&(We=5)}function _m(t,n){do{var a=V0(t.alternate,t);if(a!==null){a.flags&=32767,fe=a;return}if(a=t.return,a!==null&&(a.flags|=32768,a.subtreeFlags=0,a.deletions=null),!n&&(t=t.sibling,t!==null)){fe=t;return}fe=t=a}while(t!==null);We=6,fe=null}function vm(t,n,a,r,u,f,S,E,P){t.cancelPendingCommit=null;do El();while(an!==0);if((Se&6)!==0)throw Error(s(327));if(n!==null){if(n===t.current)throw Error(s(177));if(f=n.lanes|n.childLanes,f|=Vu,Ce(t,a,f,S,E,P),t===Oe&&(fe=Oe=null,de=0),Gr=n,va=t,Vi=a,Kc=f,Qc=u,om=r,(n.subtreeFlags&10256)!==0||(n.flags&10256)!==0?(t.callbackNode=null,t.callbackPriority=0,tS(qt,function(){return Em(),null})):(t.callbackNode=null,t.callbackPriority=0),r=(n.flags&13878)!==0,(n.subtreeFlags&13878)!==0||r){r=O.T,O.T=null,u=k.p,k.p=2,S=Se,Se|=4;try{X0(t,n,a)}finally{Se=S,k.p=u,O.T=r}}an=1,Sm(),Mm(),xm()}}function Sm(){if(an===1){an=0;var t=va,n=Gr,a=(n.flags&13878)!==0;if((n.subtreeFlags&13878)!==0||a){a=O.T,O.T=null;var r=k.p;k.p=2;var u=Se;Se|=4;try{$p(n,t);var f=df,S=rd(t.containerInfo),E=f.focusedElem,P=f.selectionRange;if(S!==E&&E&&E.ownerDocument&&ad(E.ownerDocument.documentElement,E)){if(P!==null&&Bu(E)){var K=P.start,ut=P.end;if(ut===void 0&&(ut=K),"selectionStart"in E)E.selectionStart=K,E.selectionEnd=Math.min(ut,E.value.length);else{var ht=E.ownerDocument||document,J=ht&&ht.defaultView||window;if(J.getSelection){var st=J.getSelection(),Lt=E.textContent.length,Zt=Math.min(P.start,Lt),Le=P.end===void 0?Zt:Math.min(P.end,Lt);!st.extend&&Zt>Le&&(S=Le,Le=Zt,Zt=S);var W=id(E,Zt),H=id(E,Le);if(W&&H&&(st.rangeCount!==1||st.anchorNode!==W.node||st.anchorOffset!==W.offset||st.focusNode!==H.node||st.focusOffset!==H.offset)){var j=ht.createRange();j.setStart(W.node,W.offset),st.removeAllRanges(),Zt>Le?(st.addRange(j),st.extend(H.node,H.offset)):(j.setEnd(H.node,H.offset),st.addRange(j))}}}}for(ht=[],st=E;st=st.parentNode;)st.nodeType===1&&ht.push({element:st,left:st.scrollLeft,top:st.scrollTop});for(typeof E.focus=="function"&&E.focus(),E=0;E<ht.length;E++){var ft=ht[E];ft.element.scrollLeft=ft.left,ft.element.scrollTop=ft.top}}zl=!!hf,df=hf=null}finally{Se=u,k.p=r,O.T=a}}t.current=n,an=2}}function Mm(){if(an===2){an=0;var t=va,n=Gr,a=(n.flags&8772)!==0;if((n.subtreeFlags&8772)!==0||a){a=O.T,O.T=null;var r=k.p;k.p=2;var u=Se;Se|=4;try{jp(t,n.alternate,n)}finally{Se=u,k.p=r,O.T=a}}an=3}}function xm(){if(an===4||an===3){an=0,vt();var t=va,n=Gr,a=Vi,r=om;(n.subtreeFlags&10256)!==0||(n.flags&10256)!==0?an=5:(an=0,Gr=va=null,ym(t,t.pendingLanes));var u=t.pendingLanes;if(u===0&&(_a=null),$i(a),n=n.stateNode,Dt&&typeof Dt.onCommitFiberRoot=="function")try{Dt.onCommitFiberRoot(Kt,n,void 0,(n.current.flags&128)===128)}catch{}if(r!==null){n=O.T,u=k.p,k.p=2,O.T=null;try{for(var f=t.onRecoverableError,S=0;S<r.length;S++){var E=r[S];f(E.value,{componentStack:E.stack})}}finally{O.T=n,k.p=u}}(Vi&3)!==0&&El(),Ei(t),u=t.pendingLanes,(a&261930)!==0&&(u&42)!==0?t===Jc?ao++:(ao=0,Jc=t):ao=0,ro(0)}}function ym(t,n){(t.pooledCacheLanes&=n)===0&&(n=t.pooledCache,n!=null&&(t.pooledCache=null,Fs(n)))}function El(){return Sm(),Mm(),xm(),Em()}function Em(){if(an!==5)return!1;var t=va,n=Kc;Kc=0;var a=$i(Vi),r=O.T,u=k.p;try{k.p=32>a?32:a,O.T=null,a=Qc,Qc=null;var f=va,S=Vi;if(an=0,Gr=va=null,Vi=0,(Se&6)!==0)throw Error(s(331));var E=Se;if(Se|=4,am(f.current),em(f,f.current,S,a),Se=E,ro(0,!1),Dt&&typeof Dt.onPostCommitFiberRoot=="function")try{Dt.onPostCommitFiberRoot(Kt,f)}catch{}return!0}finally{k.p=u,O.T=r,ym(t,n)}}function Tm(t,n,a){n=Jn(a,n),n=Dc(t.stateNode,n,2),t=fa(t,n,2),t!==null&&(ke(t,2),Ei(t))}function Ae(t,n,a){if(t.tag===3)Tm(t,t,a);else for(;n!==null;){if(n.tag===3){Tm(n,t,a);break}else if(n.tag===1){var r=n.stateNode;if(typeof n.type.getDerivedStateFromError=="function"||typeof r.componentDidCatch=="function"&&(_a===null||!_a.has(r))){t=Jn(a,t),a=bp(2),r=fa(n,a,2),r!==null&&(Ap(a,r,n,t),ke(r,2),Ei(r));break}}n=n.return}}function ef(t,n,a){var r=t.pingCache;if(r===null){r=t.pingCache=new q0;var u=new Set;r.set(n,u)}else u=r.get(n),u===void 0&&(u=new Set,r.set(n,u));u.has(a)||(Yc=!0,u.add(a),t=Q0.bind(null,t,n,a),n.then(t,t))}function Q0(t,n,a){var r=t.pingCache;r!==null&&r.delete(n),t.pingedLanes|=t.suspendedLanes&a,t.warmLanes&=~a,Oe===t&&(de&a)===a&&(We===4||We===3&&(de&62914560)===de&&300>gt()-_l?(Se&2)===0&&Vr(t,0):jc|=a,Hr===de&&(Hr=0)),Ei(t)}function bm(t,n){n===0&&(n=Ee()),t=Wa(t,n),t!==null&&(ke(t,n),Ei(t))}function J0(t){var n=t.memoizedState,a=0;n!==null&&(a=n.retryLane),bm(t,a)}function $0(t,n){var a=0;switch(t.tag){case 31:case 13:var r=t.stateNode,u=t.memoizedState;u!==null&&(a=u.retryLane);break;case 19:r=t.stateNode;break;case 22:r=t.stateNode._retryCache;break;default:throw Error(s(314))}r!==null&&r.delete(n),bm(t,a)}function tS(t,n){return A(t,n)}var Tl=null,Wr=null,nf=!1,bl=!1,af=!1,Ma=0;function Ei(t){t!==Wr&&t.next===null&&(Wr===null?Tl=Wr=t:Wr=Wr.next=t),bl=!0,nf||(nf=!0,nS())}function ro(t,n){if(!af&&bl){af=!0;do for(var a=!1,r=Tl;r!==null;){if(t!==0){var u=r.pendingLanes;if(u===0)var f=0;else{var S=r.suspendedLanes,E=r.pingedLanes;f=(1<<31-Xt(42|t)+1)-1,f&=u&~(S&~E),f=f&201326741?f&201326741|1:f?f|2:0}f!==0&&(a=!0,wm(r,f))}else f=de,f=jt(r,r===Oe?f:0,r.cancelPendingCommit!==null||r.timeoutHandle!==-1),(f&3)===0||Gt(r,f)||(a=!0,wm(r,f));r=r.next}while(a);af=!1}}function eS(){Am()}function Am(){bl=nf=!1;var t=0;Ma!==0&&hS()&&(t=Ma);for(var n=gt(),a=null,r=Tl;r!==null;){var u=r.next,f=Rm(r,n);f===0?(r.next=null,a===null?Tl=u:a.next=u,u===null&&(Wr=a)):(a=r,(t!==0||(f&3)!==0)&&(bl=!0)),r=u}an!==0&&an!==5||ro(t),Ma!==0&&(Ma=0)}function Rm(t,n){for(var a=t.suspendedLanes,r=t.pingedLanes,u=t.expirationTimes,f=t.pendingLanes&-62914561;0<f;){var S=31-Xt(f),E=1<<S,P=u[S];P===-1?((E&a)===0||(E&r)!==0)&&(u[S]=Re(E,n)):P<=n&&(t.expiredLanes|=E),f&=~E}if(n=Oe,a=de,a=jt(t,t===n?a:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),r=t.callbackNode,a===0||t===n&&(be===2||be===9)||t.cancelPendingCommit!==null)return r!==null&&r!==null&&nt(r),t.callbackNode=null,t.callbackPriority=0;if((a&3)===0||Gt(t,a)){if(n=a&-a,n===t.callbackPriority)return n;switch(r!==null&&nt(r),$i(a)){case 2:case 8:a=Ut;break;case 32:a=qt;break;case 268435456:a=_t;break;default:a=qt}return r=Cm.bind(null,t),a=A(a,r),t.callbackPriority=n,t.callbackNode=a,n}return r!==null&&r!==null&&nt(r),t.callbackPriority=2,t.callbackNode=null,2}function Cm(t,n){if(an!==0&&an!==5)return t.callbackNode=null,t.callbackPriority=0,null;var a=t.callbackNode;if(El()&&t.callbackNode!==a)return null;var r=de;return r=jt(t,t===Oe?r:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),r===0?null:(um(t,r,n),Rm(t,gt()),t.callbackNode!=null&&t.callbackNode===a?Cm.bind(null,t):null)}function wm(t,n){if(El())return null;um(t,n,!0)}function nS(){pS(function(){(Se&6)!==0?A(Rt,eS):Am()})}function rf(){if(Ma===0){var t=wr;t===0&&(t=yt,yt<<=1,(yt&261888)===0&&(yt=256)),Ma=t}return Ma}function Dm(t){return t==null||typeof t=="symbol"||typeof t=="boolean"?null:typeof t=="function"?t:No(""+t)}function Lm(t,n){var a=n.ownerDocument.createElement("input");return a.name=n.name,a.value=n.value,t.id&&a.setAttribute("form",t.id),n.parentNode.insertBefore(a,n),t=new FormData(t),a.parentNode.removeChild(a),t}function iS(t,n,a,r,u){if(n==="submit"&&a&&a.stateNode===u){var f=Dm((u[Sn]||null).action),S=r.submitter;S&&(n=(n=S[Sn]||null)?Dm(n.formAction):S.getAttribute("formAction"),n!==null&&(f=n,S=null));var E=new Bo("action","action",null,r,u);t.push({event:E,listeners:[{instance:null,listener:function(){if(r.defaultPrevented){if(Ma!==0){var P=S?Lm(u,S):new FormData(u);Tc(a,{pending:!0,data:P,method:u.method,action:f},null,P)}}else typeof f=="function"&&(E.preventDefault(),P=S?Lm(u,S):new FormData(u),Tc(a,{pending:!0,data:P,method:u.method,action:f},f,P))},currentTarget:u}]})}}for(var sf=0;sf<Gu.length;sf++){var of=Gu[sf],aS=of.toLowerCase(),rS=of[0].toUpperCase()+of.slice(1);ui(aS,"on"+rS)}ui(ld,"onAnimationEnd"),ui(ud,"onAnimationIteration"),ui(cd,"onAnimationStart"),ui("dblclick","onDoubleClick"),ui("focusin","onFocus"),ui("focusout","onBlur"),ui(x0,"onTransitionRun"),ui(y0,"onTransitionStart"),ui(E0,"onTransitionCancel"),ui(fd,"onTransitionEnd"),Ze("onMouseEnter",["mouseout","mouseover"]),Ze("onMouseLeave",["mouseout","mouseover"]),Ze("onPointerEnter",["pointerout","pointerover"]),Ze("onPointerLeave",["pointerout","pointerover"]),Te("onChange","change click focusin focusout input keydown keyup selectionchange".split(" ")),Te("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")),Te("onBeforeInput",["compositionend","keypress","textInput","paste"]),Te("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" ")),Te("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" ")),Te("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var so="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),sS=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(so));function Um(t,n){n=(n&4)!==0;for(var a=0;a<t.length;a++){var r=t[a],u=r.event;r=r.listeners;t:{var f=void 0;if(n)for(var S=r.length-1;0<=S;S--){var E=r[S],P=E.instance,K=E.currentTarget;if(E=E.listener,P!==f&&u.isPropagationStopped())break t;f=E,u.currentTarget=K;try{f(u)}catch(ut){Ho(ut)}u.currentTarget=null,f=P}else for(S=0;S<r.length;S++){if(E=r[S],P=E.instance,K=E.currentTarget,E=E.listener,P!==f&&u.isPropagationStopped())break t;f=E,u.currentTarget=K;try{f(u)}catch(ut){Ho(ut)}u.currentTarget=null,f=P}}}}function he(t,n){var a=n[Ts];a===void 0&&(a=n[Ts]=new Set);var r=t+"__bubble";a.has(r)||(Nm(n,t,2,!1),a.add(r))}function lf(t,n,a){var r=0;n&&(r|=4),Nm(a,t,r,n)}var Al="_reactListening"+Math.random().toString(36).slice(2);function uf(t){if(!t[Al]){t[Al]=!0,Jt.forEach(function(a){a!=="selectionchange"&&(sS.has(a)||lf(a,!1,t),lf(a,!0,t))});var n=t.nodeType===9?t:t.ownerDocument;n===null||n[Al]||(n[Al]=!0,lf("selectionchange",!1,n))}}function Nm(t,n,a,r){switch(lg(n)){case 2:var u=OS;break;case 8:u=zS;break;default:u=Tf}a=u.bind(null,n,a,t),u=void 0,!Cu||n!=="touchstart"&&n!=="touchmove"&&n!=="wheel"||(u=!0),r?u!==void 0?t.addEventListener(n,a,{capture:!0,passive:u}):t.addEventListener(n,a,!0):u!==void 0?t.addEventListener(n,a,{passive:u}):t.addEventListener(n,a,!1)}function cf(t,n,a,r,u){var f=r;if((n&1)===0&&(n&2)===0&&r!==null)t:for(;;){if(r===null)return;var S=r.tag;if(S===3||S===4){var E=r.stateNode.containerInfo;if(E===u)break;if(S===4)for(S=r.return;S!==null;){var P=S.tag;if((P===3||P===4)&&S.stateNode.containerInfo===u)return;S=S.return}for(;E!==null;){if(S=Ct(E),S===null)return;if(P=S.tag,P===5||P===6||P===26||P===27){r=f=S;continue t}E=E.parentNode}}r=r.return}Ih(function(){var K=f,ut=Au(a),ht=[];t:{var J=hd.get(t);if(J!==void 0){var st=Bo,Lt=t;switch(t){case"keypress":if(zo(a)===0)break t;case"keydown":case"keyup":st=$v;break;case"focusin":Lt="focus",st=Uu;break;case"focusout":Lt="blur",st=Uu;break;case"beforeblur":case"afterblur":st=Uu;break;case"click":if(a.button===2)break t;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":st=Gh;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":st=Gv;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":st=n0;break;case ld:case ud:case cd:st=Wv;break;case fd:st=a0;break;case"scroll":case"scrollend":st=Fv;break;case"wheel":st=s0;break;case"copy":case"cut":case"paste":st=qv;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":st=Xh;break;case"toggle":case"beforetoggle":st=l0}var Zt=(n&4)!==0,Le=!Zt&&(t==="scroll"||t==="scrollend"),W=Zt?J!==null?J+"Capture":null:J;Zt=[];for(var H=K,j;H!==null;){var ft=H;if(j=ft.stateNode,ft=ft.tag,ft!==5&&ft!==26&&ft!==27||j===null||W===null||(ft=Cs(H,W),ft!=null&&Zt.push(oo(H,ft,j))),Le)break;H=H.return}0<Zt.length&&(J=new st(J,Lt,null,a,ut),ht.push({event:J,listeners:Zt}))}}if((n&7)===0){t:{if(J=t==="mouseover"||t==="pointerover",st=t==="mouseout"||t==="pointerout",J&&a!==bu&&(Lt=a.relatedTarget||a.fromElement)&&(Ct(Lt)||Lt[ta]))break t;if((st||J)&&(J=ut.window===ut?ut:(J=ut.ownerDocument)?J.defaultView||J.parentWindow:window,st?(Lt=a.relatedTarget||a.toElement,st=K,Lt=Lt?Ct(Lt):null,Lt!==null&&(Le=c(Lt),Zt=Lt.tag,Lt!==Le||Zt!==5&&Zt!==27&&Zt!==6)&&(Lt=null)):(st=null,Lt=K),st!==Lt)){if(Zt=Gh,ft="onMouseLeave",W="onMouseEnter",H="mouse",(t==="pointerout"||t==="pointerover")&&(Zt=Xh,ft="onPointerLeave",W="onPointerEnter",H="pointer"),Le=st==null?J:Wt(st),j=Lt==null?J:Wt(Lt),J=new Zt(ft,H+"leave",st,a,ut),J.target=Le,J.relatedTarget=j,ft=null,Ct(ut)===K&&(Zt=new Zt(W,H+"enter",Lt,a,ut),Zt.target=j,Zt.relatedTarget=Le,ft=Zt),Le=ft,st&&Lt)e:{for(Zt=oS,W=st,H=Lt,j=0,ft=W;ft;ft=Zt(ft))j++;ft=0;for(var Vt=H;Vt;Vt=Zt(Vt))ft++;for(;0<j-ft;)W=Zt(W),j--;for(;0<ft-j;)H=Zt(H),ft--;for(;j--;){if(W===H||H!==null&&W===H.alternate){Zt=W;break e}W=Zt(W),H=Zt(H)}Zt=null}else Zt=null;st!==null&&Om(ht,J,st,Zt,!1),Lt!==null&&Le!==null&&Om(ht,Le,Lt,Zt,!0)}}t:{if(J=K?Wt(K):window,st=J.nodeName&&J.nodeName.toLowerCase(),st==="select"||st==="input"&&J.type==="file")var ge=Qh;else if(Zh(J))if(Jh)ge=v0;else{ge=g0;var zt=m0}else st=J.nodeName,!st||st.toLowerCase()!=="input"||J.type!=="checkbox"&&J.type!=="radio"?K&&Tu(K.elementType)&&(ge=Qh):ge=_0;if(ge&&(ge=ge(t,K))){Kh(ht,ge,a,ut);break t}zt&&zt(t,J,K),t==="focusout"&&K&&J.type==="number"&&K.memoizedProps.value!=null&&Eu(J,"number",J.value)}switch(zt=K?Wt(K):window,t){case"focusin":(Zh(zt)||zt.contentEditable==="true")&&(xr=zt,Iu=K,Ps=null);break;case"focusout":Ps=Iu=xr=null;break;case"mousedown":Fu=!0;break;case"contextmenu":case"mouseup":case"dragend":Fu=!1,sd(ht,a,ut);break;case"selectionchange":if(M0)break;case"keydown":case"keyup":sd(ht,a,ut)}var ae;if(Ou)t:{switch(t){case"compositionstart":var pe="onCompositionStart";break t;case"compositionend":pe="onCompositionEnd";break t;case"compositionupdate":pe="onCompositionUpdate";break t}pe=void 0}else Mr?Yh(t,a)&&(pe="onCompositionEnd"):t==="keydown"&&a.keyCode===229&&(pe="onCompositionStart");pe&&(Wh&&a.locale!=="ko"&&(Mr||pe!=="onCompositionStart"?pe==="onCompositionEnd"&&Mr&&(ae=Fh()):(aa=ut,wu="value"in aa?aa.value:aa.textContent,Mr=!0)),zt=Rl(K,pe),0<zt.length&&(pe=new Vh(pe,t,null,a,ut),ht.push({event:pe,listeners:zt}),ae?pe.data=ae:(ae=jh(a),ae!==null&&(pe.data=ae)))),(ae=c0?f0(t,a):h0(t,a))&&(pe=Rl(K,"onBeforeInput"),0<pe.length&&(zt=new Vh("onBeforeInput","beforeinput",null,a,ut),ht.push({event:zt,listeners:pe}),zt.data=ae)),iS(ht,t,K,a,ut)}Um(ht,n)})}function oo(t,n,a){return{instance:t,listener:n,currentTarget:a}}function Rl(t,n){for(var a=n+"Capture",r=[];t!==null;){var u=t,f=u.stateNode;if(u=u.tag,u!==5&&u!==26&&u!==27||f===null||(u=Cs(t,a),u!=null&&r.unshift(oo(t,u,f)),u=Cs(t,n),u!=null&&r.push(oo(t,u,f))),t.tag===3)return r;t=t.return}return[]}function oS(t){if(t===null)return null;do t=t.return;while(t&&t.tag!==5&&t.tag!==27);return t||null}function Om(t,n,a,r,u){for(var f=n._reactName,S=[];a!==null&&a!==r;){var E=a,P=E.alternate,K=E.stateNode;if(E=E.tag,P!==null&&P===r)break;E!==5&&E!==26&&E!==27||K===null||(P=K,u?(K=Cs(a,f),K!=null&&S.unshift(oo(a,K,P))):u||(K=Cs(a,f),K!=null&&S.push(oo(a,K,P)))),a=a.return}S.length!==0&&t.push({event:n,listeners:S})}var lS=/\r\n?/g,uS=/\u0000|\uFFFD/g;function zm(t){return(typeof t=="string"?t:""+t).replace(lS,`
`).replace(uS,"")}function Pm(t,n){return n=zm(n),zm(t)===n}function De(t,n,a,r,u,f){switch(a){case"children":typeof r=="string"?n==="body"||n==="textarea"&&r===""||_r(t,r):(typeof r=="number"||typeof r=="bigint")&&n!=="body"&&_r(t,""+r);break;case"className":Ne(t,"class",r);break;case"tabIndex":Ne(t,"tabindex",r);break;case"dir":case"role":case"viewBox":case"width":case"height":Ne(t,a,r);break;case"style":Ph(t,r,f);break;case"data":if(n!=="object"){Ne(t,"data",r);break}case"src":case"href":if(r===""&&(n!=="a"||a!=="href")){t.removeAttribute(a);break}if(r==null||typeof r=="function"||typeof r=="symbol"||typeof r=="boolean"){t.removeAttribute(a);break}r=No(""+r),t.setAttribute(a,r);break;case"action":case"formAction":if(typeof r=="function"){t.setAttribute(a,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}else typeof f=="function"&&(a==="formAction"?(n!=="input"&&De(t,n,"name",u.name,u,null),De(t,n,"formEncType",u.formEncType,u,null),De(t,n,"formMethod",u.formMethod,u,null),De(t,n,"formTarget",u.formTarget,u,null)):(De(t,n,"encType",u.encType,u,null),De(t,n,"method",u.method,u,null),De(t,n,"target",u.target,u,null)));if(r==null||typeof r=="symbol"||typeof r=="boolean"){t.removeAttribute(a);break}r=No(""+r),t.setAttribute(a,r);break;case"onClick":r!=null&&(t.onclick=Ri);break;case"onScroll":r!=null&&he("scroll",t);break;case"onScrollEnd":r!=null&&he("scrollend",t);break;case"dangerouslySetInnerHTML":if(r!=null){if(typeof r!="object"||!("__html"in r))throw Error(s(61));if(a=r.__html,a!=null){if(u.children!=null)throw Error(s(60));t.innerHTML=a}}break;case"multiple":t.multiple=r&&typeof r!="function"&&typeof r!="symbol";break;case"muted":t.muted=r&&typeof r!="function"&&typeof r!="symbol";break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":break;case"autoFocus":break;case"xlinkHref":if(r==null||typeof r=="function"||typeof r=="boolean"||typeof r=="symbol"){t.removeAttribute("xlink:href");break}a=No(""+r),t.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",a);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":r!=null&&typeof r!="function"&&typeof r!="symbol"?t.setAttribute(a,""+r):t.removeAttribute(a);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":r&&typeof r!="function"&&typeof r!="symbol"?t.setAttribute(a,""):t.removeAttribute(a);break;case"capture":case"download":r===!0?t.setAttribute(a,""):r!==!1&&r!=null&&typeof r!="function"&&typeof r!="symbol"?t.setAttribute(a,r):t.removeAttribute(a);break;case"cols":case"rows":case"size":case"span":r!=null&&typeof r!="function"&&typeof r!="symbol"&&!isNaN(r)&&1<=r?t.setAttribute(a,r):t.removeAttribute(a);break;case"rowSpan":case"start":r==null||typeof r=="function"||typeof r=="symbol"||isNaN(r)?t.removeAttribute(a):t.setAttribute(a,r);break;case"popover":he("beforetoggle",t),he("toggle",t),ea(t,"popover",r);break;case"xlinkActuate":dn(t,"http://www.w3.org/1999/xlink","xlink:actuate",r);break;case"xlinkArcrole":dn(t,"http://www.w3.org/1999/xlink","xlink:arcrole",r);break;case"xlinkRole":dn(t,"http://www.w3.org/1999/xlink","xlink:role",r);break;case"xlinkShow":dn(t,"http://www.w3.org/1999/xlink","xlink:show",r);break;case"xlinkTitle":dn(t,"http://www.w3.org/1999/xlink","xlink:title",r);break;case"xlinkType":dn(t,"http://www.w3.org/1999/xlink","xlink:type",r);break;case"xmlBase":dn(t,"http://www.w3.org/XML/1998/namespace","xml:base",r);break;case"xmlLang":dn(t,"http://www.w3.org/XML/1998/namespace","xml:lang",r);break;case"xmlSpace":dn(t,"http://www.w3.org/XML/1998/namespace","xml:space",r);break;case"is":ea(t,"is",r);break;case"innerText":case"textContent":break;default:(!(2<a.length)||a[0]!=="o"&&a[0]!=="O"||a[1]!=="n"&&a[1]!=="N")&&(a=Bv.get(a)||a,ea(t,a,r))}}function ff(t,n,a,r,u,f){switch(a){case"style":Ph(t,r,f);break;case"dangerouslySetInnerHTML":if(r!=null){if(typeof r!="object"||!("__html"in r))throw Error(s(61));if(a=r.__html,a!=null){if(u.children!=null)throw Error(s(60));t.innerHTML=a}}break;case"children":typeof r=="string"?_r(t,r):(typeof r=="number"||typeof r=="bigint")&&_r(t,""+r);break;case"onScroll":r!=null&&he("scroll",t);break;case"onScrollEnd":r!=null&&he("scrollend",t);break;case"onClick":r!=null&&(t.onclick=Ri);break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":break;case"innerText":case"textContent":break;default:if(!$t.hasOwnProperty(a))t:{if(a[0]==="o"&&a[1]==="n"&&(u=a.endsWith("Capture"),n=a.slice(2,u?a.length-7:void 0),f=t[Sn]||null,f=f!=null?f[a]:null,typeof f=="function"&&t.removeEventListener(n,f,u),typeof r=="function")){typeof f!="function"&&f!==null&&(a in t?t[a]=null:t.hasAttribute(a)&&t.removeAttribute(a)),t.addEventListener(n,r,u);break t}a in t?t[a]=r:r===!0?t.setAttribute(a,""):ea(t,a,r)}}}function _n(t,n,a){switch(n){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":he("error",t),he("load",t);var r=!1,u=!1,f;for(f in a)if(a.hasOwnProperty(f)){var S=a[f];if(S!=null)switch(f){case"src":r=!0;break;case"srcSet":u=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(s(137,n));default:De(t,n,f,S,a,null)}}u&&De(t,n,"srcSet",a.srcSet,a,null),r&&De(t,n,"src",a.src,a,null);return;case"input":he("invalid",t);var E=f=S=u=null,P=null,K=null;for(r in a)if(a.hasOwnProperty(r)){var ut=a[r];if(ut!=null)switch(r){case"name":u=ut;break;case"type":S=ut;break;case"checked":P=ut;break;case"defaultChecked":K=ut;break;case"value":f=ut;break;case"defaultValue":E=ut;break;case"children":case"dangerouslySetInnerHTML":if(ut!=null)throw Error(s(137,n));break;default:De(t,n,r,ut,a,null)}}Rs(t,f,E,P,K,S,u,!1);return;case"select":he("invalid",t),r=S=f=null;for(u in a)if(a.hasOwnProperty(u)&&(E=a[u],E!=null))switch(u){case"value":f=E;break;case"defaultValue":S=E;break;case"multiple":r=E;default:De(t,n,u,E,a,null)}n=f,a=S,t.multiple=!!r,n!=null?gr(t,!!r,n,!1):a!=null&&gr(t,!!r,a,!0);return;case"textarea":he("invalid",t),f=u=r=null;for(S in a)if(a.hasOwnProperty(S)&&(E=a[S],E!=null))switch(S){case"value":r=E;break;case"defaultValue":u=E;break;case"children":f=E;break;case"dangerouslySetInnerHTML":if(E!=null)throw Error(s(91));break;default:De(t,n,S,E,a,null)}Oh(t,r,u,f);return;case"option":for(P in a)a.hasOwnProperty(P)&&(r=a[P],r!=null)&&(P==="selected"?t.selected=r&&typeof r!="function"&&typeof r!="symbol":De(t,n,P,r,a,null));return;case"dialog":he("beforetoggle",t),he("toggle",t),he("cancel",t),he("close",t);break;case"iframe":case"object":he("load",t);break;case"video":case"audio":for(r=0;r<so.length;r++)he(so[r],t);break;case"image":he("error",t),he("load",t);break;case"details":he("toggle",t);break;case"embed":case"source":case"link":he("error",t),he("load",t);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(K in a)if(a.hasOwnProperty(K)&&(r=a[K],r!=null))switch(K){case"children":case"dangerouslySetInnerHTML":throw Error(s(137,n));default:De(t,n,K,r,a,null)}return;default:if(Tu(n)){for(ut in a)a.hasOwnProperty(ut)&&(r=a[ut],r!==void 0&&ff(t,n,ut,r,a,void 0));return}}for(E in a)a.hasOwnProperty(E)&&(r=a[E],r!=null&&De(t,n,E,r,a,null))}function cS(t,n,a,r){switch(n){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var u=null,f=null,S=null,E=null,P=null,K=null,ut=null;for(st in a){var ht=a[st];if(a.hasOwnProperty(st)&&ht!=null)switch(st){case"checked":break;case"value":break;case"defaultValue":P=ht;default:r.hasOwnProperty(st)||De(t,n,st,null,r,ht)}}for(var J in r){var st=r[J];if(ht=a[J],r.hasOwnProperty(J)&&(st!=null||ht!=null))switch(J){case"type":f=st;break;case"name":u=st;break;case"checked":K=st;break;case"defaultChecked":ut=st;break;case"value":S=st;break;case"defaultValue":E=st;break;case"children":case"dangerouslySetInnerHTML":if(st!=null)throw Error(s(137,n));break;default:st!==ht&&De(t,n,J,st,r,ht)}}As(t,S,E,P,K,ut,f,u);return;case"select":st=S=E=J=null;for(f in a)if(P=a[f],a.hasOwnProperty(f)&&P!=null)switch(f){case"value":break;case"multiple":st=P;default:r.hasOwnProperty(f)||De(t,n,f,null,r,P)}for(u in r)if(f=r[u],P=a[u],r.hasOwnProperty(u)&&(f!=null||P!=null))switch(u){case"value":J=f;break;case"defaultValue":E=f;break;case"multiple":S=f;default:f!==P&&De(t,n,u,f,r,P)}n=E,a=S,r=st,J!=null?gr(t,!!a,J,!1):!!r!=!!a&&(n!=null?gr(t,!!a,n,!0):gr(t,!!a,a?[]:"",!1));return;case"textarea":st=J=null;for(E in a)if(u=a[E],a.hasOwnProperty(E)&&u!=null&&!r.hasOwnProperty(E))switch(E){case"value":break;case"children":break;default:De(t,n,E,null,r,u)}for(S in r)if(u=r[S],f=a[S],r.hasOwnProperty(S)&&(u!=null||f!=null))switch(S){case"value":J=u;break;case"defaultValue":st=u;break;case"children":break;case"dangerouslySetInnerHTML":if(u!=null)throw Error(s(91));break;default:u!==f&&De(t,n,S,u,r,f)}Nh(t,J,st);return;case"option":for(var Lt in a)J=a[Lt],a.hasOwnProperty(Lt)&&J!=null&&!r.hasOwnProperty(Lt)&&(Lt==="selected"?t.selected=!1:De(t,n,Lt,null,r,J));for(P in r)J=r[P],st=a[P],r.hasOwnProperty(P)&&J!==st&&(J!=null||st!=null)&&(P==="selected"?t.selected=J&&typeof J!="function"&&typeof J!="symbol":De(t,n,P,J,r,st));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var Zt in a)J=a[Zt],a.hasOwnProperty(Zt)&&J!=null&&!r.hasOwnProperty(Zt)&&De(t,n,Zt,null,r,J);for(K in r)if(J=r[K],st=a[K],r.hasOwnProperty(K)&&J!==st&&(J!=null||st!=null))switch(K){case"children":case"dangerouslySetInnerHTML":if(J!=null)throw Error(s(137,n));break;default:De(t,n,K,J,r,st)}return;default:if(Tu(n)){for(var Le in a)J=a[Le],a.hasOwnProperty(Le)&&J!==void 0&&!r.hasOwnProperty(Le)&&ff(t,n,Le,void 0,r,J);for(ut in r)J=r[ut],st=a[ut],!r.hasOwnProperty(ut)||J===st||J===void 0&&st===void 0||ff(t,n,ut,J,r,st);return}}for(var W in a)J=a[W],a.hasOwnProperty(W)&&J!=null&&!r.hasOwnProperty(W)&&De(t,n,W,null,r,J);for(ht in r)J=r[ht],st=a[ht],!r.hasOwnProperty(ht)||J===st||J==null&&st==null||De(t,n,ht,J,r,st)}function Bm(t){switch(t){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}function fS(){if(typeof performance.getEntriesByType=="function"){for(var t=0,n=0,a=performance.getEntriesByType("resource"),r=0;r<a.length;r++){var u=a[r],f=u.transferSize,S=u.initiatorType,E=u.duration;if(f&&E&&Bm(S)){for(S=0,E=u.responseEnd,r+=1;r<a.length;r++){var P=a[r],K=P.startTime;if(K>E)break;var ut=P.transferSize,ht=P.initiatorType;ut&&Bm(ht)&&(P=P.responseEnd,S+=ut*(P<E?1:(E-K)/(P-K)))}if(--r,n+=8*(f+S)/(u.duration/1e3),t++,10<t)break}}if(0<t)return n/t/1e6}return navigator.connection&&(t=navigator.connection.downlink,typeof t=="number")?t:5}var hf=null,df=null;function Cl(t){return t.nodeType===9?t:t.ownerDocument}function Im(t){switch(t){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function Fm(t,n){if(t===0)switch(n){case"svg":return 1;case"math":return 2;default:return 0}return t===1&&n==="foreignObject"?0:t}function pf(t,n){return t==="textarea"||t==="noscript"||typeof n.children=="string"||typeof n.children=="number"||typeof n.children=="bigint"||typeof n.dangerouslySetInnerHTML=="object"&&n.dangerouslySetInnerHTML!==null&&n.dangerouslySetInnerHTML.__html!=null}var mf=null;function hS(){var t=window.event;return t&&t.type==="popstate"?t===mf?!1:(mf=t,!0):(mf=null,!1)}var Hm=typeof setTimeout=="function"?setTimeout:void 0,dS=typeof clearTimeout=="function"?clearTimeout:void 0,Gm=typeof Promise=="function"?Promise:void 0,pS=typeof queueMicrotask=="function"?queueMicrotask:typeof Gm<"u"?function(t){return Gm.resolve(null).then(t).catch(mS)}:Hm;function mS(t){setTimeout(function(){throw t})}function xa(t){return t==="head"}function Vm(t,n){var a=n,r=0;do{var u=a.nextSibling;if(t.removeChild(a),u&&u.nodeType===8)if(a=u.data,a==="/$"||a==="/&"){if(r===0){t.removeChild(u),jr(n);return}r--}else if(a==="$"||a==="$?"||a==="$~"||a==="$!"||a==="&")r++;else if(a==="html")lo(t.ownerDocument.documentElement);else if(a==="head"){a=t.ownerDocument.head,lo(a);for(var f=a.firstChild;f;){var S=f.nextSibling,E=f.nodeName;f[rt]||E==="SCRIPT"||E==="STYLE"||E==="LINK"&&f.rel.toLowerCase()==="stylesheet"||a.removeChild(f),f=S}}else a==="body"&&lo(t.ownerDocument.body);a=u}while(a);jr(n)}function Xm(t,n){var a=t;t=0;do{var r=a.nextSibling;if(a.nodeType===1?n?(a._stashedDisplay=a.style.display,a.style.display="none"):(a.style.display=a._stashedDisplay||"",a.getAttribute("style")===""&&a.removeAttribute("style")):a.nodeType===3&&(n?(a._stashedText=a.nodeValue,a.nodeValue=""):a.nodeValue=a._stashedText||""),r&&r.nodeType===8)if(a=r.data,a==="/$"){if(t===0)break;t--}else a!=="$"&&a!=="$?"&&a!=="$~"&&a!=="$!"||t++;a=r}while(a)}function gf(t){var n=t.firstChild;for(n&&n.nodeType===10&&(n=n.nextSibling);n;){var a=n;switch(n=n.nextSibling,a.nodeName){case"HTML":case"HEAD":case"BODY":gf(a),et(a);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if(a.rel.toLowerCase()==="stylesheet")continue}t.removeChild(a)}}function gS(t,n,a,r){for(;t.nodeType===1;){var u=a;if(t.nodeName.toLowerCase()!==n.toLowerCase()){if(!r&&(t.nodeName!=="INPUT"||t.type!=="hidden"))break}else if(r){if(!t[rt])switch(n){case"meta":if(!t.hasAttribute("itemprop"))break;return t;case"link":if(f=t.getAttribute("rel"),f==="stylesheet"&&t.hasAttribute("data-precedence"))break;if(f!==u.rel||t.getAttribute("href")!==(u.href==null||u.href===""?null:u.href)||t.getAttribute("crossorigin")!==(u.crossOrigin==null?null:u.crossOrigin)||t.getAttribute("title")!==(u.title==null?null:u.title))break;return t;case"style":if(t.hasAttribute("data-precedence"))break;return t;case"script":if(f=t.getAttribute("src"),(f!==(u.src==null?null:u.src)||t.getAttribute("type")!==(u.type==null?null:u.type)||t.getAttribute("crossorigin")!==(u.crossOrigin==null?null:u.crossOrigin))&&f&&t.hasAttribute("async")&&!t.hasAttribute("itemprop"))break;return t;default:return t}}else if(n==="input"&&t.type==="hidden"){var f=u.name==null?null:""+u.name;if(u.type==="hidden"&&t.getAttribute("name")===f)return t}else return t;if(t=ii(t.nextSibling),t===null)break}return null}function _S(t,n,a){if(n==="")return null;for(;t.nodeType!==3;)if((t.nodeType!==1||t.nodeName!=="INPUT"||t.type!=="hidden")&&!a||(t=ii(t.nextSibling),t===null))return null;return t}function Wm(t,n){for(;t.nodeType!==8;)if((t.nodeType!==1||t.nodeName!=="INPUT"||t.type!=="hidden")&&!n||(t=ii(t.nextSibling),t===null))return null;return t}function _f(t){return t.data==="$?"||t.data==="$~"}function vf(t){return t.data==="$!"||t.data==="$?"&&t.ownerDocument.readyState!=="loading"}function vS(t,n){var a=t.ownerDocument;if(t.data==="$~")t._reactRetry=n;else if(t.data!=="$?"||a.readyState!=="loading")n();else{var r=function(){n(),a.removeEventListener("DOMContentLoaded",r)};a.addEventListener("DOMContentLoaded",r),t._reactRetry=r}}function ii(t){for(;t!=null;t=t.nextSibling){var n=t.nodeType;if(n===1||n===3)break;if(n===8){if(n=t.data,n==="$"||n==="$!"||n==="$?"||n==="$~"||n==="&"||n==="F!"||n==="F")break;if(n==="/$"||n==="/&")return null}}return t}var Sf=null;function km(t){t=t.nextSibling;for(var n=0;t;){if(t.nodeType===8){var a=t.data;if(a==="/$"||a==="/&"){if(n===0)return ii(t.nextSibling);n--}else a!=="$"&&a!=="$!"&&a!=="$?"&&a!=="$~"&&a!=="&"||n++}t=t.nextSibling}return null}function qm(t){t=t.previousSibling;for(var n=0;t;){if(t.nodeType===8){var a=t.data;if(a==="$"||a==="$!"||a==="$?"||a==="$~"||a==="&"){if(n===0)return t;n--}else a!=="/$"&&a!=="/&"||n++}t=t.previousSibling}return null}function Ym(t,n,a){switch(n=Cl(a),t){case"html":if(t=n.documentElement,!t)throw Error(s(452));return t;case"head":if(t=n.head,!t)throw Error(s(453));return t;case"body":if(t=n.body,!t)throw Error(s(454));return t;default:throw Error(s(451))}}function lo(t){for(var n=t.attributes;n.length;)t.removeAttributeNode(n[0]);et(t)}var ai=new Map,jm=new Set;function wl(t){return typeof t.getRootNode=="function"?t.getRootNode():t.nodeType===9?t:t.ownerDocument}var Xi=k.d;k.d={f:SS,r:MS,D:xS,C:yS,L:ES,m:TS,X:AS,S:bS,M:RS};function SS(){var t=Xi.f(),n=Ml();return t||n}function MS(t){var n=Ot(t);n!==null&&n.tag===5&&n.type==="form"?fp(n):Xi.r(t)}var kr=typeof document>"u"?null:document;function Zm(t,n,a){var r=kr;if(r&&typeof n=="string"&&n){var u=Mn(n);u='link[rel="'+t+'"][href="'+u+'"]',typeof a=="string"&&(u+='[crossorigin="'+a+'"]'),jm.has(u)||(jm.add(u),t={rel:t,crossOrigin:a,href:n},r.querySelector(u)===null&&(n=r.createElement("link"),_n(n,"link",t),Bt(n),r.head.appendChild(n)))}}function xS(t){Xi.D(t),Zm("dns-prefetch",t,null)}function yS(t,n){Xi.C(t,n),Zm("preconnect",t,n)}function ES(t,n,a){Xi.L(t,n,a);var r=kr;if(r&&t&&n){var u='link[rel="preload"][as="'+Mn(n)+'"]';n==="image"&&a&&a.imageSrcSet?(u+='[imagesrcset="'+Mn(a.imageSrcSet)+'"]',typeof a.imageSizes=="string"&&(u+='[imagesizes="'+Mn(a.imageSizes)+'"]')):u+='[href="'+Mn(t)+'"]';var f=u;switch(n){case"style":f=qr(t);break;case"script":f=Yr(t)}ai.has(f)||(t=_({rel:"preload",href:n==="image"&&a&&a.imageSrcSet?void 0:t,as:n},a),ai.set(f,t),r.querySelector(u)!==null||n==="style"&&r.querySelector(uo(f))||n==="script"&&r.querySelector(co(f))||(n=r.createElement("link"),_n(n,"link",t),Bt(n),r.head.appendChild(n)))}}function TS(t,n){Xi.m(t,n);var a=kr;if(a&&t){var r=n&&typeof n.as=="string"?n.as:"script",u='link[rel="modulepreload"][as="'+Mn(r)+'"][href="'+Mn(t)+'"]',f=u;switch(r){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":f=Yr(t)}if(!ai.has(f)&&(t=_({rel:"modulepreload",href:t},n),ai.set(f,t),a.querySelector(u)===null)){switch(r){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(a.querySelector(co(f)))return}r=a.createElement("link"),_n(r,"link",t),Bt(r),a.head.appendChild(r)}}}function bS(t,n,a){Xi.S(t,n,a);var r=kr;if(r&&t){var u=Yt(r).hoistableStyles,f=qr(t);n=n||"default";var S=u.get(f);if(!S){var E={loading:0,preload:null};if(S=r.querySelector(uo(f)))E.loading=5;else{t=_({rel:"stylesheet",href:t,"data-precedence":n},a),(a=ai.get(f))&&Mf(t,a);var P=S=r.createElement("link");Bt(P),_n(P,"link",t),P._p=new Promise(function(K,ut){P.onload=K,P.onerror=ut}),P.addEventListener("load",function(){E.loading|=1}),P.addEventListener("error",function(){E.loading|=2}),E.loading|=4,Dl(S,n,r)}S={type:"stylesheet",instance:S,count:1,state:E},u.set(f,S)}}}function AS(t,n){Xi.X(t,n);var a=kr;if(a&&t){var r=Yt(a).hoistableScripts,u=Yr(t),f=r.get(u);f||(f=a.querySelector(co(u)),f||(t=_({src:t,async:!0},n),(n=ai.get(u))&&xf(t,n),f=a.createElement("script"),Bt(f),_n(f,"link",t),a.head.appendChild(f)),f={type:"script",instance:f,count:1,state:null},r.set(u,f))}}function RS(t,n){Xi.M(t,n);var a=kr;if(a&&t){var r=Yt(a).hoistableScripts,u=Yr(t),f=r.get(u);f||(f=a.querySelector(co(u)),f||(t=_({src:t,async:!0,type:"module"},n),(n=ai.get(u))&&xf(t,n),f=a.createElement("script"),Bt(f),_n(f,"link",t),a.head.appendChild(f)),f={type:"script",instance:f,count:1,state:null},r.set(u,f))}}function Km(t,n,a,r){var u=(u=Mt.current)?wl(u):null;if(!u)throw Error(s(446));switch(t){case"meta":case"title":return null;case"style":return typeof a.precedence=="string"&&typeof a.href=="string"?(n=qr(a.href),a=Yt(u).hoistableStyles,r=a.get(n),r||(r={type:"style",instance:null,count:0,state:null},a.set(n,r)),r):{type:"void",instance:null,count:0,state:null};case"link":if(a.rel==="stylesheet"&&typeof a.href=="string"&&typeof a.precedence=="string"){t=qr(a.href);var f=Yt(u).hoistableStyles,S=f.get(t);if(S||(u=u.ownerDocument||u,S={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},f.set(t,S),(f=u.querySelector(uo(t)))&&!f._p&&(S.instance=f,S.state.loading=5),ai.has(t)||(a={rel:"preload",as:"style",href:a.href,crossOrigin:a.crossOrigin,integrity:a.integrity,media:a.media,hrefLang:a.hrefLang,referrerPolicy:a.referrerPolicy},ai.set(t,a),f||CS(u,t,a,S.state))),n&&r===null)throw Error(s(528,""));return S}if(n&&r!==null)throw Error(s(529,""));return null;case"script":return n=a.async,a=a.src,typeof a=="string"&&n&&typeof n!="function"&&typeof n!="symbol"?(n=Yr(a),a=Yt(u).hoistableScripts,r=a.get(n),r||(r={type:"script",instance:null,count:0,state:null},a.set(n,r)),r):{type:"void",instance:null,count:0,state:null};default:throw Error(s(444,t))}}function qr(t){return'href="'+Mn(t)+'"'}function uo(t){return'link[rel="stylesheet"]['+t+"]"}function Qm(t){return _({},t,{"data-precedence":t.precedence,precedence:null})}function CS(t,n,a,r){t.querySelector('link[rel="preload"][as="style"]['+n+"]")?r.loading=1:(n=t.createElement("link"),r.preload=n,n.addEventListener("load",function(){return r.loading|=1}),n.addEventListener("error",function(){return r.loading|=2}),_n(n,"link",a),Bt(n),t.head.appendChild(n))}function Yr(t){return'[src="'+Mn(t)+'"]'}function co(t){return"script[async]"+t}function Jm(t,n,a){if(n.count++,n.instance===null)switch(n.type){case"style":var r=t.querySelector('style[data-href~="'+Mn(a.href)+'"]');if(r)return n.instance=r,Bt(r),r;var u=_({},a,{"data-href":a.href,"data-precedence":a.precedence,href:null,precedence:null});return r=(t.ownerDocument||t).createElement("style"),Bt(r),_n(r,"style",u),Dl(r,a.precedence,t),n.instance=r;case"stylesheet":u=qr(a.href);var f=t.querySelector(uo(u));if(f)return n.state.loading|=4,n.instance=f,Bt(f),f;r=Qm(a),(u=ai.get(u))&&Mf(r,u),f=(t.ownerDocument||t).createElement("link"),Bt(f);var S=f;return S._p=new Promise(function(E,P){S.onload=E,S.onerror=P}),_n(f,"link",r),n.state.loading|=4,Dl(f,a.precedence,t),n.instance=f;case"script":return f=Yr(a.src),(u=t.querySelector(co(f)))?(n.instance=u,Bt(u),u):(r=a,(u=ai.get(f))&&(r=_({},a),xf(r,u)),t=t.ownerDocument||t,u=t.createElement("script"),Bt(u),_n(u,"link",r),t.head.appendChild(u),n.instance=u);case"void":return null;default:throw Error(s(443,n.type))}else n.type==="stylesheet"&&(n.state.loading&4)===0&&(r=n.instance,n.state.loading|=4,Dl(r,a.precedence,t));return n.instance}function Dl(t,n,a){for(var r=a.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),u=r.length?r[r.length-1]:null,f=u,S=0;S<r.length;S++){var E=r[S];if(E.dataset.precedence===n)f=E;else if(f!==u)break}f?f.parentNode.insertBefore(t,f.nextSibling):(n=a.nodeType===9?a.head:a,n.insertBefore(t,n.firstChild))}function Mf(t,n){t.crossOrigin==null&&(t.crossOrigin=n.crossOrigin),t.referrerPolicy==null&&(t.referrerPolicy=n.referrerPolicy),t.title==null&&(t.title=n.title)}function xf(t,n){t.crossOrigin==null&&(t.crossOrigin=n.crossOrigin),t.referrerPolicy==null&&(t.referrerPolicy=n.referrerPolicy),t.integrity==null&&(t.integrity=n.integrity)}var Ll=null;function $m(t,n,a){if(Ll===null){var r=new Map,u=Ll=new Map;u.set(a,r)}else u=Ll,r=u.get(a),r||(r=new Map,u.set(a,r));if(r.has(t))return r;for(r.set(t,null),a=a.getElementsByTagName(t),u=0;u<a.length;u++){var f=a[u];if(!(f[rt]||f[je]||t==="link"&&f.getAttribute("rel")==="stylesheet")&&f.namespaceURI!=="http://www.w3.org/2000/svg"){var S=f.getAttribute(n)||"";S=t+S;var E=r.get(S);E?E.push(f):r.set(S,[f])}}return r}function tg(t,n,a){t=t.ownerDocument||t,t.head.insertBefore(a,n==="title"?t.querySelector("head > title"):null)}function wS(t,n,a){if(a===1||n.itemProp!=null)return!1;switch(t){case"meta":case"title":return!0;case"style":if(typeof n.precedence!="string"||typeof n.href!="string"||n.href==="")break;return!0;case"link":if(typeof n.rel!="string"||typeof n.href!="string"||n.href===""||n.onLoad||n.onError)break;return n.rel==="stylesheet"?(t=n.disabled,typeof n.precedence=="string"&&t==null):!0;case"script":if(n.async&&typeof n.async!="function"&&typeof n.async!="symbol"&&!n.onLoad&&!n.onError&&n.src&&typeof n.src=="string")return!0}return!1}function eg(t){return!(t.type==="stylesheet"&&(t.state.loading&3)===0)}function DS(t,n,a,r){if(a.type==="stylesheet"&&(typeof r.media!="string"||matchMedia(r.media).matches!==!1)&&(a.state.loading&4)===0){if(a.instance===null){var u=qr(r.href),f=n.querySelector(uo(u));if(f){n=f._p,n!==null&&typeof n=="object"&&typeof n.then=="function"&&(t.count++,t=Ul.bind(t),n.then(t,t)),a.state.loading|=4,a.instance=f,Bt(f);return}f=n.ownerDocument||n,r=Qm(r),(u=ai.get(u))&&Mf(r,u),f=f.createElement("link"),Bt(f);var S=f;S._p=new Promise(function(E,P){S.onload=E,S.onerror=P}),_n(f,"link",r),a.instance=f}t.stylesheets===null&&(t.stylesheets=new Map),t.stylesheets.set(a,n),(n=a.state.preload)&&(a.state.loading&3)===0&&(t.count++,a=Ul.bind(t),n.addEventListener("load",a),n.addEventListener("error",a))}}var yf=0;function LS(t,n){return t.stylesheets&&t.count===0&&Ol(t,t.stylesheets),0<t.count||0<t.imgCount?function(a){var r=setTimeout(function(){if(t.stylesheets&&Ol(t,t.stylesheets),t.unsuspend){var f=t.unsuspend;t.unsuspend=null,f()}},6e4+n);0<t.imgBytes&&yf===0&&(yf=62500*fS());var u=setTimeout(function(){if(t.waitingForImages=!1,t.count===0&&(t.stylesheets&&Ol(t,t.stylesheets),t.unsuspend)){var f=t.unsuspend;t.unsuspend=null,f()}},(t.imgBytes>yf?50:800)+n);return t.unsuspend=a,function(){t.unsuspend=null,clearTimeout(r),clearTimeout(u)}}:null}function Ul(){if(this.count--,this.count===0&&(this.imgCount===0||!this.waitingForImages)){if(this.stylesheets)Ol(this,this.stylesheets);else if(this.unsuspend){var t=this.unsuspend;this.unsuspend=null,t()}}}var Nl=null;function Ol(t,n){t.stylesheets=null,t.unsuspend!==null&&(t.count++,Nl=new Map,n.forEach(US,t),Nl=null,Ul.call(t))}function US(t,n){if(!(n.state.loading&4)){var a=Nl.get(t);if(a)var r=a.get(null);else{a=new Map,Nl.set(t,a);for(var u=t.querySelectorAll("link[data-precedence],style[data-precedence]"),f=0;f<u.length;f++){var S=u[f];(S.nodeName==="LINK"||S.getAttribute("media")!=="not all")&&(a.set(S.dataset.precedence,S),r=S)}r&&a.set(null,r)}u=n.instance,S=u.getAttribute("data-precedence"),f=a.get(S)||r,f===r&&a.set(null,u),a.set(S,u),this.count++,r=Ul.bind(this),u.addEventListener("load",r),u.addEventListener("error",r),f?f.parentNode.insertBefore(u,f.nextSibling):(t=t.nodeType===9?t.head:t,t.insertBefore(u,t.firstChild)),n.state.loading|=4}}var fo={$$typeof:R,Provider:null,Consumer:null,_currentValue:Q,_currentValue2:Q,_threadCount:0};function NS(t,n,a,r,u,f,S,E,P){this.tag=1,this.containerInfo=t,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=Ve(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Ve(0),this.hiddenUpdates=Ve(null),this.identifierPrefix=r,this.onUncaughtError=u,this.onCaughtError=f,this.onRecoverableError=S,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=P,this.incompleteTransitions=new Map}function ng(t,n,a,r,u,f,S,E,P,K,ut,ht){return t=new NS(t,n,a,S,P,K,ut,ht,E),n=1,f===!0&&(n|=24),f=Gn(3,null,null,n),t.current=f,f.stateNode=t,n=tc(),n.refCount++,t.pooledCache=n,n.refCount++,f.memoizedState={element:r,isDehydrated:a,cache:n},ac(f),t}function ig(t){return t?(t=Tr,t):Tr}function ag(t,n,a,r,u,f){u=ig(u),r.context===null?r.context=u:r.pendingContext=u,r=ca(n),r.payload={element:a},f=f===void 0?null:f,f!==null&&(r.callback=f),a=fa(t,r,n),a!==null&&(Pn(a,t,n),Xs(a,t,n))}function rg(t,n){if(t=t.memoizedState,t!==null&&t.dehydrated!==null){var a=t.retryLane;t.retryLane=a!==0&&a<n?a:n}}function Ef(t,n){rg(t,n),(t=t.alternate)&&rg(t,n)}function sg(t){if(t.tag===13||t.tag===31){var n=Wa(t,67108864);n!==null&&Pn(n,t,67108864),Ef(t,67108864)}}function og(t){if(t.tag===13||t.tag===31){var n=qn();n=ys(n);var a=Wa(t,n);a!==null&&Pn(a,t,n),Ef(t,n)}}var zl=!0;function OS(t,n,a,r){var u=O.T;O.T=null;var f=k.p;try{k.p=2,Tf(t,n,a,r)}finally{k.p=f,O.T=u}}function zS(t,n,a,r){var u=O.T;O.T=null;var f=k.p;try{k.p=8,Tf(t,n,a,r)}finally{k.p=f,O.T=u}}function Tf(t,n,a,r){if(zl){var u=bf(r);if(u===null)cf(t,n,r,Pl,a),ug(t,r);else if(BS(u,t,n,a,r))r.stopPropagation();else if(ug(t,r),n&4&&-1<PS.indexOf(t)){for(;u!==null;){var f=Ot(u);if(f!==null)switch(f.tag){case 3:if(f=f.stateNode,f.current.memoizedState.isDehydrated){var S=Tt(f.pendingLanes);if(S!==0){var E=f;for(E.pendingLanes|=2,E.entangledLanes|=2;S;){var P=1<<31-Xt(S);E.entanglements[1]|=P,S&=~P}Ei(f),(Se&6)===0&&(vl=gt()+500,ro(0))}}break;case 31:case 13:E=Wa(f,2),E!==null&&Pn(E,f,2),Ml(),Ef(f,2)}if(f=bf(r),f===null&&cf(t,n,r,Pl,a),f===u)break;u=f}u!==null&&r.stopPropagation()}else cf(t,n,r,null,a)}}function bf(t){return t=Au(t),Af(t)}var Pl=null;function Af(t){if(Pl=null,t=Ct(t),t!==null){var n=c(t);if(n===null)t=null;else{var a=n.tag;if(a===13){if(t=d(n),t!==null)return t;t=null}else if(a===31){if(t=h(n),t!==null)return t;t=null}else if(a===3){if(n.stateNode.current.memoizedState.isDehydrated)return n.tag===3?n.stateNode.containerInfo:null;t=null}else n!==t&&(t=null)}}return Pl=t,null}function lg(t){switch(t){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(Ht()){case Rt:return 2;case Ut:return 8;case qt:case ie:return 32;case _t:return 268435456;default:return 32}default:return 32}}var Rf=!1,ya=null,Ea=null,Ta=null,ho=new Map,po=new Map,ba=[],PS="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function ug(t,n){switch(t){case"focusin":case"focusout":ya=null;break;case"dragenter":case"dragleave":Ea=null;break;case"mouseover":case"mouseout":Ta=null;break;case"pointerover":case"pointerout":ho.delete(n.pointerId);break;case"gotpointercapture":case"lostpointercapture":po.delete(n.pointerId)}}function mo(t,n,a,r,u,f){return t===null||t.nativeEvent!==f?(t={blockedOn:n,domEventName:a,eventSystemFlags:r,nativeEvent:f,targetContainers:[u]},n!==null&&(n=Ot(n),n!==null&&sg(n)),t):(t.eventSystemFlags|=r,n=t.targetContainers,u!==null&&n.indexOf(u)===-1&&n.push(u),t)}function BS(t,n,a,r,u){switch(n){case"focusin":return ya=mo(ya,t,n,a,r,u),!0;case"dragenter":return Ea=mo(Ea,t,n,a,r,u),!0;case"mouseover":return Ta=mo(Ta,t,n,a,r,u),!0;case"pointerover":var f=u.pointerId;return ho.set(f,mo(ho.get(f)||null,t,n,a,r,u)),!0;case"gotpointercapture":return f=u.pointerId,po.set(f,mo(po.get(f)||null,t,n,a,r,u)),!0}return!1}function cg(t){var n=Ct(t.target);if(n!==null){var a=c(n);if(a!==null){if(n=a.tag,n===13){if(n=d(a),n!==null){t.blockedOn=n,Ha(t.priority,function(){og(a)});return}}else if(n===31){if(n=h(a),n!==null){t.blockedOn=n,Ha(t.priority,function(){og(a)});return}}else if(n===3&&a.stateNode.current.memoizedState.isDehydrated){t.blockedOn=a.tag===3?a.stateNode.containerInfo:null;return}}}t.blockedOn=null}function Bl(t){if(t.blockedOn!==null)return!1;for(var n=t.targetContainers;0<n.length;){var a=bf(t.nativeEvent);if(a===null){a=t.nativeEvent;var r=new a.constructor(a.type,a);bu=r,a.target.dispatchEvent(r),bu=null}else return n=Ot(a),n!==null&&sg(n),t.blockedOn=a,!1;n.shift()}return!0}function fg(t,n,a){Bl(t)&&a.delete(n)}function IS(){Rf=!1,ya!==null&&Bl(ya)&&(ya=null),Ea!==null&&Bl(Ea)&&(Ea=null),Ta!==null&&Bl(Ta)&&(Ta=null),ho.forEach(fg),po.forEach(fg)}function Il(t,n){t.blockedOn===n&&(t.blockedOn=null,Rf||(Rf=!0,o.unstable_scheduleCallback(o.unstable_NormalPriority,IS)))}var Fl=null;function hg(t){Fl!==t&&(Fl=t,o.unstable_scheduleCallback(o.unstable_NormalPriority,function(){Fl===t&&(Fl=null);for(var n=0;n<t.length;n+=3){var a=t[n],r=t[n+1],u=t[n+2];if(typeof r!="function"){if(Af(r||a)===null)continue;break}var f=Ot(a);f!==null&&(t.splice(n,3),n-=3,Tc(f,{pending:!0,data:u,method:a.method,action:r},r,u))}}))}function jr(t){function n(P){return Il(P,t)}ya!==null&&Il(ya,t),Ea!==null&&Il(Ea,t),Ta!==null&&Il(Ta,t),ho.forEach(n),po.forEach(n);for(var a=0;a<ba.length;a++){var r=ba[a];r.blockedOn===t&&(r.blockedOn=null)}for(;0<ba.length&&(a=ba[0],a.blockedOn===null);)cg(a),a.blockedOn===null&&ba.shift();if(a=(t.ownerDocument||t).$$reactFormReplay,a!=null)for(r=0;r<a.length;r+=3){var u=a[r],f=a[r+1],S=u[Sn]||null;if(typeof f=="function")S||hg(a);else if(S){var E=null;if(f&&f.hasAttribute("formAction")){if(u=f,S=f[Sn]||null)E=S.formAction;else if(Af(u)!==null)continue}else E=S.action;typeof E=="function"?a[r+1]=E:(a.splice(r,3),r-=3),hg(a)}}}function dg(){function t(f){f.canIntercept&&f.info==="react-transition"&&f.intercept({handler:function(){return new Promise(function(S){return u=S})},focusReset:"manual",scroll:"manual"})}function n(){u!==null&&(u(),u=null),r||setTimeout(a,20)}function a(){if(!r&&!navigation.transition){var f=navigation.currentEntry;f&&f.url!=null&&navigation.navigate(f.url,{state:f.getState(),info:"react-transition",history:"replace"})}}if(typeof navigation=="object"){var r=!1,u=null;return navigation.addEventListener("navigate",t),navigation.addEventListener("navigatesuccess",n),navigation.addEventListener("navigateerror",n),setTimeout(a,100),function(){r=!0,navigation.removeEventListener("navigate",t),navigation.removeEventListener("navigatesuccess",n),navigation.removeEventListener("navigateerror",n),u!==null&&(u(),u=null)}}}function Cf(t){this._internalRoot=t}Hl.prototype.render=Cf.prototype.render=function(t){var n=this._internalRoot;if(n===null)throw Error(s(409));var a=n.current,r=qn();ag(a,r,t,n,null,null)},Hl.prototype.unmount=Cf.prototype.unmount=function(){var t=this._internalRoot;if(t!==null){this._internalRoot=null;var n=t.containerInfo;ag(t.current,2,null,t,null,null),Ml(),n[ta]=null}};function Hl(t){this._internalRoot=t}Hl.prototype.unstable_scheduleHydration=function(t){if(t){var n=Es();t={blockedOn:null,target:t,priority:n};for(var a=0;a<ba.length&&n!==0&&n<ba[a].priority;a++);ba.splice(a,0,t),a===0&&cg(t)}};var pg=e.version;if(pg!=="19.2.3")throw Error(s(527,pg,"19.2.3"));k.findDOMNode=function(t){var n=t._reactInternals;if(n===void 0)throw typeof t.render=="function"?Error(s(188)):(t=Object.keys(t).join(","),Error(s(268,t)));return t=p(n),t=t!==null?g(t):null,t=t===null?null:t.stateNode,t};var FS={bundleType:0,version:"19.2.3",rendererPackageName:"react-dom",currentDispatcherRef:O,reconcilerVersion:"19.2.3"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var Gl=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!Gl.isDisabled&&Gl.supportsFiber)try{Kt=Gl.inject(FS),Dt=Gl}catch{}}return _o.createRoot=function(t,n){if(!l(t))throw Error(s(299));var a=!1,r="",u=xp,f=yp,S=Ep;return n!=null&&(n.unstable_strictMode===!0&&(a=!0),n.identifierPrefix!==void 0&&(r=n.identifierPrefix),n.onUncaughtError!==void 0&&(u=n.onUncaughtError),n.onCaughtError!==void 0&&(f=n.onCaughtError),n.onRecoverableError!==void 0&&(S=n.onRecoverableError)),n=ng(t,1,!1,null,null,a,r,null,u,f,S,dg),t[ta]=n.current,uf(t),new Cf(n)},_o.hydrateRoot=function(t,n,a){if(!l(t))throw Error(s(299));var r=!1,u="",f=xp,S=yp,E=Ep,P=null;return a!=null&&(a.unstable_strictMode===!0&&(r=!0),a.identifierPrefix!==void 0&&(u=a.identifierPrefix),a.onUncaughtError!==void 0&&(f=a.onUncaughtError),a.onCaughtError!==void 0&&(S=a.onCaughtError),a.onRecoverableError!==void 0&&(E=a.onRecoverableError),a.formState!==void 0&&(P=a.formState)),n=ng(t,1,!0,n,a??null,r,u,P,f,S,E,dg),n.context=ig(null),a=n.current,r=qn(),r=ys(r),u=ca(r),u.callback=null,fa(a,u,r),a=r,n.current.lanes=a,ke(n,a),Ei(n),t[ta]=n.current,uf(t),new Hl(n)},_o.version="19.2.3",_o}var Tg;function QS(){if(Tg)return Lf.exports;Tg=1;function o(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(o)}catch(e){console.error(e)}}return o(),Lf.exports=KS(),Lf.exports}var SA=QS();const JS="modulepreload",$S=function(o){return"/"+o},bg={},MA=function(e,i,s){let l=Promise.resolve();if(i&&i.length>0){let m=function(p){return Promise.all(p.map(g=>Promise.resolve(g).then(_=>({status:"fulfilled",value:_}),_=>({status:"rejected",reason:_}))))};document.getElementsByTagName("link");const d=document.querySelector("meta[property=csp-nonce]"),h=d?.nonce||d?.getAttribute("nonce");l=m(i.map(p=>{if(p=$S(p),p in bg)return;bg[p]=!0;const g=p.endsWith(".css"),_=g?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${p}"]${_}`))return;const M=document.createElement("link");if(M.rel=g?"stylesheet":JS,g||(M.as="script"),M.crossOrigin="",M.href=p,h&&M.setAttribute("nonce",h),document.head.appendChild(M),g)return new Promise((y,b)=>{M.addEventListener("load",y),M.addEventListener("error",()=>b(new Error(`Unable to preload CSS for ${p}`)))})}))}function c(d){const h=new Event("vite:preloadError",{cancelable:!0});if(h.payload=d,window.dispatchEvent(h),!h.defaultPrevented)throw d}return l.then(d=>{for(const h of d||[])h.status==="rejected"&&c(h.reason);return e().catch(c)})},Ag=o=>{let e;const i=new Set,s=(p,g)=>{const _=typeof p=="function"?p(e):p;if(!Object.is(_,e)){const M=e;e=g??(typeof _!="object"||_===null)?_:Object.assign({},e,_),i.forEach(y=>y(e,M))}},l=()=>e,h={setState:s,getState:l,getInitialState:()=>m,subscribe:p=>(i.add(p),()=>i.delete(p))},m=e=o(s,l,h);return h},tM=(o=>o?Ag(o):Ag),eM=o=>o;function nM(o,e=eM){const i=Eo.useSyncExternalStore(o.subscribe,Eo.useCallback(()=>e(o.getState()),[o,e]),Eo.useCallback(()=>e(o.getInitialState()),[o,e]));return Eo.useDebugValue(i),i}const Rg=o=>{const e=tM(o),i=s=>nM(e,s);return Object.assign(i,e),i},xA=(o=>o?Rg(o):Rg);const Ah="160",yA={ROTATE:0,DOLLY:1,PAN:2},EA={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},iM=0,Cg=1,aM=2,ev=1,rM=2,Zi=3,Ia=0,In=1,Ki=2,za=0,ds=1,wg=2,Dg=3,Lg=4,sM=5,ur=100,oM=101,lM=102,Ug=103,Ng=104,uM=200,cM=201,fM=202,hM=203,gh=204,_h=205,dM=206,pM=207,mM=208,gM=209,_M=210,vM=211,SM=212,MM=213,xM=214,yM=0,EM=1,TM=2,du=3,bM=4,AM=5,RM=6,CM=7,nv=0,wM=1,DM=2,Pa=0,LM=1,UM=2,NM=3,OM=4,zM=5,PM=6,iv=300,ms=301,gs=302,vh=303,Sh=304,Su=306,Mh=1e3,_i=1001,xh=1002,Cn=1003,Og=1004,zf=1005,si=1006,BM=1007,bo=1008,Ba=1009,IM=1010,FM=1011,Rh=1012,av=1013,Ua=1014,Na=1015,Ao=1016,rv=1017,sv=1018,fr=1020,HM=1021,vi=1023,GM=1024,VM=1025,hr=1026,_s=1027,XM=1028,ov=1029,WM=1030,lv=1031,uv=1033,Pf=33776,Bf=33777,If=33778,Ff=33779,zg=35840,Pg=35841,Bg=35842,Ig=35843,cv=36196,Fg=37492,Hg=37496,Gg=37808,Vg=37809,Xg=37810,Wg=37811,kg=37812,qg=37813,Yg=37814,jg=37815,Zg=37816,Kg=37817,Qg=37818,Jg=37819,$g=37820,t_=37821,Hf=36492,e_=36494,n_=36495,kM=36283,i_=36284,a_=36285,r_=36286,fv=3e3,dr=3001,qM=3200,YM=3201,hv=0,jM=1,oi="",vn="srgb",Ji="srgb-linear",Ch="display-p3",Mu="display-p3-linear",pu="linear",Fe="srgb",mu="rec709",gu="p3",Zr=7680,s_=519,ZM=512,KM=513,QM=514,dv=515,JM=516,$M=517,tx=518,ex=519,o_=35044,l_="300 es",yh=1035,Qi=2e3,_u=2001;class Ss{addEventListener(e,i){this._listeners===void 0&&(this._listeners={});const s=this._listeners;s[e]===void 0&&(s[e]=[]),s[e].indexOf(i)===-1&&s[e].push(i)}hasEventListener(e,i){if(this._listeners===void 0)return!1;const s=this._listeners;return s[e]!==void 0&&s[e].indexOf(i)!==-1}removeEventListener(e,i){if(this._listeners===void 0)return;const l=this._listeners[e];if(l!==void 0){const c=l.indexOf(i);c!==-1&&l.splice(c,1)}}dispatchEvent(e){if(this._listeners===void 0)return;const s=this._listeners[e.type];if(s!==void 0){e.target=this;const l=s.slice(0);for(let c=0,d=l.length;c<d;c++)l[c].call(this,e);e.target=null}}}const yn=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],fu=Math.PI/180,Eh=180/Math.PI;function Co(){const o=Math.random()*4294967295|0,e=Math.random()*4294967295|0,i=Math.random()*4294967295|0,s=Math.random()*4294967295|0;return(yn[o&255]+yn[o>>8&255]+yn[o>>16&255]+yn[o>>24&255]+"-"+yn[e&255]+yn[e>>8&255]+"-"+yn[e>>16&15|64]+yn[e>>24&255]+"-"+yn[i&63|128]+yn[i>>8&255]+"-"+yn[i>>16&255]+yn[i>>24&255]+yn[s&255]+yn[s>>8&255]+yn[s>>16&255]+yn[s>>24&255]).toLowerCase()}function wn(o,e,i){return Math.max(e,Math.min(i,o))}function nx(o,e){return(o%e+e)%e}function Gf(o,e,i){return(1-i)*o+i*e}function u_(o){return(o&o-1)===0&&o!==0}function Th(o){return Math.pow(2,Math.floor(Math.log(o)/Math.LN2))}function vo(o,e){switch(e.constructor){case Float32Array:return o;case Uint32Array:return o/4294967295;case Uint16Array:return o/65535;case Uint8Array:return o/255;case Int32Array:return Math.max(o/2147483647,-1);case Int16Array:return Math.max(o/32767,-1);case Int8Array:return Math.max(o/127,-1);default:throw new Error("Invalid component type.")}}function Bn(o,e){switch(e.constructor){case Float32Array:return o;case Uint32Array:return Math.round(o*4294967295);case Uint16Array:return Math.round(o*65535);case Uint8Array:return Math.round(o*255);case Int32Array:return Math.round(o*2147483647);case Int16Array:return Math.round(o*32767);case Int8Array:return Math.round(o*127);default:throw new Error("Invalid component type.")}}const TA={DEG2RAD:fu};class xe{constructor(e=0,i=0){xe.prototype.isVector2=!0,this.x=e,this.y=i}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,i){return this.x=e,this.y=i,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){const i=this.x,s=this.y,l=e.elements;return this.x=l[0]*i+l[3]*s+l[6],this.y=l[1]*i+l[4]*s+l[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,i){return this.x=Math.max(e.x,Math.min(i.x,this.x)),this.y=Math.max(e.y,Math.min(i.y,this.y)),this}clampScalar(e,i){return this.x=Math.max(e,Math.min(i,this.x)),this.y=Math.max(e,Math.min(i,this.y)),this}clampLength(e,i){const s=this.length();return this.divideScalar(s||1).multiplyScalar(Math.max(e,Math.min(i,s)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){const i=Math.sqrt(this.lengthSq()*e.lengthSq());if(i===0)return Math.PI/2;const s=this.dot(e)/i;return Math.acos(wn(s,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const i=this.x-e.x,s=this.y-e.y;return i*i+s*s}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this}lerpVectors(e,i,s){return this.x=e.x+(i.x-e.x)*s,this.y=e.y+(i.y-e.y)*s,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this}rotateAround(e,i){const s=Math.cos(i),l=Math.sin(i),c=this.x-e.x,d=this.y-e.y;return this.x=c*s-d*l+e.x,this.y=c*l+d*s+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}}class ce{constructor(e,i,s,l,c,d,h,m,p){ce.prototype.isMatrix3=!0,this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,i,s,l,c,d,h,m,p)}set(e,i,s,l,c,d,h,m,p){const g=this.elements;return g[0]=e,g[1]=l,g[2]=h,g[3]=i,g[4]=c,g[5]=m,g[6]=s,g[7]=d,g[8]=p,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){const i=this.elements,s=e.elements;return i[0]=s[0],i[1]=s[1],i[2]=s[2],i[3]=s[3],i[4]=s[4],i[5]=s[5],i[6]=s[6],i[7]=s[7],i[8]=s[8],this}extractBasis(e,i,s){return e.setFromMatrix3Column(this,0),i.setFromMatrix3Column(this,1),s.setFromMatrix3Column(this,2),this}setFromMatrix4(e){const i=e.elements;return this.set(i[0],i[4],i[8],i[1],i[5],i[9],i[2],i[6],i[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,i){const s=e.elements,l=i.elements,c=this.elements,d=s[0],h=s[3],m=s[6],p=s[1],g=s[4],_=s[7],M=s[2],y=s[5],b=s[8],T=l[0],x=l[3],v=l[6],N=l[1],R=l[4],I=l[7],q=l[2],B=l[5],z=l[8];return c[0]=d*T+h*N+m*q,c[3]=d*x+h*R+m*B,c[6]=d*v+h*I+m*z,c[1]=p*T+g*N+_*q,c[4]=p*x+g*R+_*B,c[7]=p*v+g*I+_*z,c[2]=M*T+y*N+b*q,c[5]=M*x+y*R+b*B,c[8]=M*v+y*I+b*z,this}multiplyScalar(e){const i=this.elements;return i[0]*=e,i[3]*=e,i[6]*=e,i[1]*=e,i[4]*=e,i[7]*=e,i[2]*=e,i[5]*=e,i[8]*=e,this}determinant(){const e=this.elements,i=e[0],s=e[1],l=e[2],c=e[3],d=e[4],h=e[5],m=e[6],p=e[7],g=e[8];return i*d*g-i*h*p-s*c*g+s*h*m+l*c*p-l*d*m}invert(){const e=this.elements,i=e[0],s=e[1],l=e[2],c=e[3],d=e[4],h=e[5],m=e[6],p=e[7],g=e[8],_=g*d-h*p,M=h*m-g*c,y=p*c-d*m,b=i*_+s*M+l*y;if(b===0)return this.set(0,0,0,0,0,0,0,0,0);const T=1/b;return e[0]=_*T,e[1]=(l*p-g*s)*T,e[2]=(h*s-l*d)*T,e[3]=M*T,e[4]=(g*i-l*m)*T,e[5]=(l*c-h*i)*T,e[6]=y*T,e[7]=(s*m-p*i)*T,e[8]=(d*i-s*c)*T,this}transpose(){let e;const i=this.elements;return e=i[1],i[1]=i[3],i[3]=e,e=i[2],i[2]=i[6],i[6]=e,e=i[5],i[5]=i[7],i[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){const i=this.elements;return e[0]=i[0],e[1]=i[3],e[2]=i[6],e[3]=i[1],e[4]=i[4],e[5]=i[7],e[6]=i[2],e[7]=i[5],e[8]=i[8],this}setUvTransform(e,i,s,l,c,d,h){const m=Math.cos(c),p=Math.sin(c);return this.set(s*m,s*p,-s*(m*d+p*h)+d+e,-l*p,l*m,-l*(-p*d+m*h)+h+i,0,0,1),this}scale(e,i){return this.premultiply(Vf.makeScale(e,i)),this}rotate(e){return this.premultiply(Vf.makeRotation(-e)),this}translate(e,i){return this.premultiply(Vf.makeTranslation(e,i)),this}makeTranslation(e,i){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,i,0,0,1),this}makeRotation(e){const i=Math.cos(e),s=Math.sin(e);return this.set(i,-s,0,s,i,0,0,0,1),this}makeScale(e,i){return this.set(e,0,0,0,i,0,0,0,1),this}equals(e){const i=this.elements,s=e.elements;for(let l=0;l<9;l++)if(i[l]!==s[l])return!1;return!0}fromArray(e,i=0){for(let s=0;s<9;s++)this.elements[s]=e[s+i];return this}toArray(e=[],i=0){const s=this.elements;return e[i]=s[0],e[i+1]=s[1],e[i+2]=s[2],e[i+3]=s[3],e[i+4]=s[4],e[i+5]=s[5],e[i+6]=s[6],e[i+7]=s[7],e[i+8]=s[8],e}clone(){return new this.constructor().fromArray(this.elements)}}const Vf=new ce;function pv(o){for(let e=o.length-1;e>=0;--e)if(o[e]>=65535)return!0;return!1}function vu(o){return document.createElementNS("http://www.w3.org/1999/xhtml",o)}function ix(){const o=vu("canvas");return o.style.display="block",o}const c_={};function To(o){o in c_||(c_[o]=!0,console.warn(o))}const f_=new ce().set(.8224621,.177538,0,.0331941,.9668058,0,.0170827,.0723974,.9105199),h_=new ce().set(1.2249401,-.2249404,0,-.0420569,1.0420571,0,-.0196376,-.0786361,1.0982735),Vl={[Ji]:{transfer:pu,primaries:mu,toReference:o=>o,fromReference:o=>o},[vn]:{transfer:Fe,primaries:mu,toReference:o=>o.convertSRGBToLinear(),fromReference:o=>o.convertLinearToSRGB()},[Mu]:{transfer:pu,primaries:gu,toReference:o=>o.applyMatrix3(h_),fromReference:o=>o.applyMatrix3(f_)},[Ch]:{transfer:Fe,primaries:gu,toReference:o=>o.convertSRGBToLinear().applyMatrix3(h_),fromReference:o=>o.applyMatrix3(f_).convertLinearToSRGB()}},ax=new Set([Ji,Mu]),Ue={enabled:!0,_workingColorSpace:Ji,get workingColorSpace(){return this._workingColorSpace},set workingColorSpace(o){if(!ax.has(o))throw new Error(`Unsupported working color space, "${o}".`);this._workingColorSpace=o},convert:function(o,e,i){if(this.enabled===!1||e===i||!e||!i)return o;const s=Vl[e].toReference,l=Vl[i].fromReference;return l(s(o))},fromWorkingColorSpace:function(o,e){return this.convert(o,this._workingColorSpace,e)},toWorkingColorSpace:function(o,e){return this.convert(o,e,this._workingColorSpace)},getPrimaries:function(o){return Vl[o].primaries},getTransfer:function(o){return o===oi?pu:Vl[o].transfer}};function ps(o){return o<.04045?o*.0773993808:Math.pow(o*.9478672986+.0521327014,2.4)}function Xf(o){return o<.0031308?o*12.92:1.055*Math.pow(o,.41666)-.055}let Kr;class mv{static getDataURL(e){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let i;if(e instanceof HTMLCanvasElement)i=e;else{Kr===void 0&&(Kr=vu("canvas")),Kr.width=e.width,Kr.height=e.height;const s=Kr.getContext("2d");e instanceof ImageData?s.putImageData(e,0,0):s.drawImage(e,0,0,e.width,e.height),i=Kr}return i.width>2048||i.height>2048?(console.warn("THREE.ImageUtils.getDataURL: Image converted to jpg for performance reasons",e),i.toDataURL("image/jpeg",.6)):i.toDataURL("image/png")}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){const i=vu("canvas");i.width=e.width,i.height=e.height;const s=i.getContext("2d");s.drawImage(e,0,0,e.width,e.height);const l=s.getImageData(0,0,e.width,e.height),c=l.data;for(let d=0;d<c.length;d++)c[d]=ps(c[d]/255)*255;return s.putImageData(l,0,0),i}else if(e.data){const i=e.data.slice(0);for(let s=0;s<i.length;s++)i instanceof Uint8Array||i instanceof Uint8ClampedArray?i[s]=Math.floor(ps(i[s]/255)*255):i[s]=ps(i[s]);return{data:i,width:e.width,height:e.height}}else return console.warn("THREE.ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}}let rx=0;class gv{constructor(e=null){this.isSource=!0,Object.defineProperty(this,"id",{value:rx++}),this.uuid=Co(),this.data=e,this.version=0}set needsUpdate(e){e===!0&&this.version++}toJSON(e){const i=e===void 0||typeof e=="string";if(!i&&e.images[this.uuid]!==void 0)return e.images[this.uuid];const s={uuid:this.uuid,url:""},l=this.data;if(l!==null){let c;if(Array.isArray(l)){c=[];for(let d=0,h=l.length;d<h;d++)l[d].isDataTexture?c.push(Wf(l[d].image)):c.push(Wf(l[d]))}else c=Wf(l);s.url=c}return i||(e.images[this.uuid]=s),s}}function Wf(o){return typeof HTMLImageElement<"u"&&o instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&o instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&o instanceof ImageBitmap?mv.getDataURL(o):o.data?{data:Array.from(o.data),width:o.width,height:o.height,type:o.data.constructor.name}:(console.warn("THREE.Texture: Unable to serialize Texture."),{})}let sx=0;class Zn extends Ss{constructor(e=Zn.DEFAULT_IMAGE,i=Zn.DEFAULT_MAPPING,s=_i,l=_i,c=si,d=bo,h=vi,m=Ba,p=Zn.DEFAULT_ANISOTROPY,g=oi){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:sx++}),this.uuid=Co(),this.name="",this.source=new gv(e),this.mipmaps=[],this.mapping=i,this.channel=0,this.wrapS=s,this.wrapT=l,this.magFilter=c,this.minFilter=d,this.anisotropy=p,this.format=h,this.internalFormat=null,this.type=m,this.offset=new xe(0,0),this.repeat=new xe(1,1),this.center=new xe(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new ce,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,typeof g=="string"?this.colorSpace=g:(To("THREE.Texture: Property .encoding has been replaced by .colorSpace."),this.colorSpace=g===dr?vn:oi),this.userData={},this.version=0,this.onUpdate=null,this.isRenderTargetTexture=!1,this.needsPMREMUpdate=!1}get image(){return this.source.data}set image(e=null){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}toJSON(e){const i=e===void 0||typeof e=="string";if(!i&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];const s={metadata:{version:4.6,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(s.userData=this.userData),i||(e.textures[this.uuid]=s),s}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==iv)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Mh:e.x=e.x-Math.floor(e.x);break;case _i:e.x=e.x<0?0:1;break;case xh:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Mh:e.y=e.y-Math.floor(e.y);break;case _i:e.y=e.y<0?0:1;break;case xh:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}get encoding(){return To("THREE.Texture: Property .encoding has been replaced by .colorSpace."),this.colorSpace===vn?dr:fv}set encoding(e){To("THREE.Texture: Property .encoding has been replaced by .colorSpace."),this.colorSpace=e===dr?vn:oi}}Zn.DEFAULT_IMAGE=null;Zn.DEFAULT_MAPPING=iv;Zn.DEFAULT_ANISOTROPY=1;class hn{constructor(e=0,i=0,s=0,l=1){hn.prototype.isVector4=!0,this.x=e,this.y=i,this.z=s,this.w=l}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,i,s,l){return this.x=e,this.y=i,this.z=s,this.w=l,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;case 2:this.z=i;break;case 3:this.w=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this.z=e.z+i.z,this.w=e.w+i.w,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this.z+=e.z*i,this.w+=e.w*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this.z=e.z-i.z,this.w=e.w-i.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){const i=this.x,s=this.y,l=this.z,c=this.w,d=e.elements;return this.x=d[0]*i+d[4]*s+d[8]*l+d[12]*c,this.y=d[1]*i+d[5]*s+d[9]*l+d[13]*c,this.z=d[2]*i+d[6]*s+d[10]*l+d[14]*c,this.w=d[3]*i+d[7]*s+d[11]*l+d[15]*c,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);const i=Math.sqrt(1-e.w*e.w);return i<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/i,this.y=e.y/i,this.z=e.z/i),this}setAxisAngleFromRotationMatrix(e){let i,s,l,c;const m=e.elements,p=m[0],g=m[4],_=m[8],M=m[1],y=m[5],b=m[9],T=m[2],x=m[6],v=m[10];if(Math.abs(g-M)<.01&&Math.abs(_-T)<.01&&Math.abs(b-x)<.01){if(Math.abs(g+M)<.1&&Math.abs(_+T)<.1&&Math.abs(b+x)<.1&&Math.abs(p+y+v-3)<.1)return this.set(1,0,0,0),this;i=Math.PI;const R=(p+1)/2,I=(y+1)/2,q=(v+1)/2,B=(g+M)/4,z=(_+T)/4,dt=(b+x)/4;return R>I&&R>q?R<.01?(s=0,l=.707106781,c=.707106781):(s=Math.sqrt(R),l=B/s,c=z/s):I>q?I<.01?(s=.707106781,l=0,c=.707106781):(l=Math.sqrt(I),s=B/l,c=dt/l):q<.01?(s=.707106781,l=.707106781,c=0):(c=Math.sqrt(q),s=z/c,l=dt/c),this.set(s,l,c,i),this}let N=Math.sqrt((x-b)*(x-b)+(_-T)*(_-T)+(M-g)*(M-g));return Math.abs(N)<.001&&(N=1),this.x=(x-b)/N,this.y=(_-T)/N,this.z=(M-g)/N,this.w=Math.acos((p+y+v-1)/2),this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,i){return this.x=Math.max(e.x,Math.min(i.x,this.x)),this.y=Math.max(e.y,Math.min(i.y,this.y)),this.z=Math.max(e.z,Math.min(i.z,this.z)),this.w=Math.max(e.w,Math.min(i.w,this.w)),this}clampScalar(e,i){return this.x=Math.max(e,Math.min(i,this.x)),this.y=Math.max(e,Math.min(i,this.y)),this.z=Math.max(e,Math.min(i,this.z)),this.w=Math.max(e,Math.min(i,this.w)),this}clampLength(e,i){const s=this.length();return this.divideScalar(s||1).multiplyScalar(Math.max(e,Math.min(i,s)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this.z+=(e.z-this.z)*i,this.w+=(e.w-this.w)*i,this}lerpVectors(e,i,s){return this.x=e.x+(i.x-e.x)*s,this.y=e.y+(i.y-e.y)*s,this.z=e.z+(i.z-e.z)*s,this.w=e.w+(i.w-e.w)*s,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this.z=e[i+2],this.w=e[i+3],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e[i+2]=this.z,e[i+3]=this.w,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this.z=e.getZ(i),this.w=e.getW(i),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}}class ox extends Ss{constructor(e=1,i=1,s={}){super(),this.isRenderTarget=!0,this.width=e,this.height=i,this.depth=1,this.scissor=new hn(0,0,e,i),this.scissorTest=!1,this.viewport=new hn(0,0,e,i);const l={width:e,height:i,depth:1};s.encoding!==void 0&&(To("THREE.WebGLRenderTarget: option.encoding has been replaced by option.colorSpace."),s.colorSpace=s.encoding===dr?vn:oi),s=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:si,depthBuffer:!0,stencilBuffer:!1,depthTexture:null,samples:0},s),this.texture=new Zn(l,s.mapping,s.wrapS,s.wrapT,s.magFilter,s.minFilter,s.format,s.type,s.anisotropy,s.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.flipY=!1,this.texture.generateMipmaps=s.generateMipmaps,this.texture.internalFormat=s.internalFormat,this.depthBuffer=s.depthBuffer,this.stencilBuffer=s.stencilBuffer,this.depthTexture=s.depthTexture,this.samples=s.samples}setSize(e,i,s=1){(this.width!==e||this.height!==i||this.depth!==s)&&(this.width=e,this.height=i,this.depth=s,this.texture.image.width=e,this.texture.image.height=i,this.texture.image.depth=s,this.dispose()),this.viewport.set(0,0,e,i),this.scissor.set(0,0,e,i)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.texture=e.texture.clone(),this.texture.isRenderTargetTexture=!0;const i=Object.assign({},e.texture.image);return this.texture.source=new gv(i),this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,e.depthTexture!==null&&(this.depthTexture=e.depthTexture.clone()),this.samples=e.samples,this}dispose(){this.dispatchEvent({type:"dispose"})}}class pr extends ox{constructor(e=1,i=1,s={}){super(e,i,s),this.isWebGLRenderTarget=!0}}class _v extends Zn{constructor(e=null,i=1,s=1,l=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:i,height:s,depth:l},this.magFilter=Cn,this.minFilter=Cn,this.wrapR=_i,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class lx extends Zn{constructor(e=null,i=1,s=1,l=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:i,height:s,depth:l},this.magFilter=Cn,this.minFilter=Cn,this.wrapR=_i,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}}class wo{constructor(e=0,i=0,s=0,l=1){this.isQuaternion=!0,this._x=e,this._y=i,this._z=s,this._w=l}static slerpFlat(e,i,s,l,c,d,h){let m=s[l+0],p=s[l+1],g=s[l+2],_=s[l+3];const M=c[d+0],y=c[d+1],b=c[d+2],T=c[d+3];if(h===0){e[i+0]=m,e[i+1]=p,e[i+2]=g,e[i+3]=_;return}if(h===1){e[i+0]=M,e[i+1]=y,e[i+2]=b,e[i+3]=T;return}if(_!==T||m!==M||p!==y||g!==b){let x=1-h;const v=m*M+p*y+g*b+_*T,N=v>=0?1:-1,R=1-v*v;if(R>Number.EPSILON){const q=Math.sqrt(R),B=Math.atan2(q,v*N);x=Math.sin(x*B)/q,h=Math.sin(h*B)/q}const I=h*N;if(m=m*x+M*I,p=p*x+y*I,g=g*x+b*I,_=_*x+T*I,x===1-h){const q=1/Math.sqrt(m*m+p*p+g*g+_*_);m*=q,p*=q,g*=q,_*=q}}e[i]=m,e[i+1]=p,e[i+2]=g,e[i+3]=_}static multiplyQuaternionsFlat(e,i,s,l,c,d){const h=s[l],m=s[l+1],p=s[l+2],g=s[l+3],_=c[d],M=c[d+1],y=c[d+2],b=c[d+3];return e[i]=h*b+g*_+m*y-p*M,e[i+1]=m*b+g*M+p*_-h*y,e[i+2]=p*b+g*y+h*M-m*_,e[i+3]=g*b-h*_-m*M-p*y,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,i,s,l){return this._x=e,this._y=i,this._z=s,this._w=l,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,i=!0){const s=e._x,l=e._y,c=e._z,d=e._order,h=Math.cos,m=Math.sin,p=h(s/2),g=h(l/2),_=h(c/2),M=m(s/2),y=m(l/2),b=m(c/2);switch(d){case"XYZ":this._x=M*g*_+p*y*b,this._y=p*y*_-M*g*b,this._z=p*g*b+M*y*_,this._w=p*g*_-M*y*b;break;case"YXZ":this._x=M*g*_+p*y*b,this._y=p*y*_-M*g*b,this._z=p*g*b-M*y*_,this._w=p*g*_+M*y*b;break;case"ZXY":this._x=M*g*_-p*y*b,this._y=p*y*_+M*g*b,this._z=p*g*b+M*y*_,this._w=p*g*_-M*y*b;break;case"ZYX":this._x=M*g*_-p*y*b,this._y=p*y*_+M*g*b,this._z=p*g*b-M*y*_,this._w=p*g*_+M*y*b;break;case"YZX":this._x=M*g*_+p*y*b,this._y=p*y*_+M*g*b,this._z=p*g*b-M*y*_,this._w=p*g*_-M*y*b;break;case"XZY":this._x=M*g*_-p*y*b,this._y=p*y*_-M*g*b,this._z=p*g*b+M*y*_,this._w=p*g*_+M*y*b;break;default:console.warn("THREE.Quaternion: .setFromEuler() encountered an unknown order: "+d)}return i===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,i){const s=i/2,l=Math.sin(s);return this._x=e.x*l,this._y=e.y*l,this._z=e.z*l,this._w=Math.cos(s),this._onChangeCallback(),this}setFromRotationMatrix(e){const i=e.elements,s=i[0],l=i[4],c=i[8],d=i[1],h=i[5],m=i[9],p=i[2],g=i[6],_=i[10],M=s+h+_;if(M>0){const y=.5/Math.sqrt(M+1);this._w=.25/y,this._x=(g-m)*y,this._y=(c-p)*y,this._z=(d-l)*y}else if(s>h&&s>_){const y=2*Math.sqrt(1+s-h-_);this._w=(g-m)/y,this._x=.25*y,this._y=(l+d)/y,this._z=(c+p)/y}else if(h>_){const y=2*Math.sqrt(1+h-s-_);this._w=(c-p)/y,this._x=(l+d)/y,this._y=.25*y,this._z=(m+g)/y}else{const y=2*Math.sqrt(1+_-s-h);this._w=(d-l)/y,this._x=(c+p)/y,this._y=(m+g)/y,this._z=.25*y}return this._onChangeCallback(),this}setFromUnitVectors(e,i){let s=e.dot(i)+1;return s<Number.EPSILON?(s=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=s):(this._x=0,this._y=-e.z,this._z=e.y,this._w=s)):(this._x=e.y*i.z-e.z*i.y,this._y=e.z*i.x-e.x*i.z,this._z=e.x*i.y-e.y*i.x,this._w=s),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(wn(this.dot(e),-1,1)))}rotateTowards(e,i){const s=this.angleTo(e);if(s===0)return this;const l=Math.min(1,i/s);return this.slerp(e,l),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,i){const s=e._x,l=e._y,c=e._z,d=e._w,h=i._x,m=i._y,p=i._z,g=i._w;return this._x=s*g+d*h+l*p-c*m,this._y=l*g+d*m+c*h-s*p,this._z=c*g+d*p+s*m-l*h,this._w=d*g-s*h-l*m-c*p,this._onChangeCallback(),this}slerp(e,i){if(i===0)return this;if(i===1)return this.copy(e);const s=this._x,l=this._y,c=this._z,d=this._w;let h=d*e._w+s*e._x+l*e._y+c*e._z;if(h<0?(this._w=-e._w,this._x=-e._x,this._y=-e._y,this._z=-e._z,h=-h):this.copy(e),h>=1)return this._w=d,this._x=s,this._y=l,this._z=c,this;const m=1-h*h;if(m<=Number.EPSILON){const y=1-i;return this._w=y*d+i*this._w,this._x=y*s+i*this._x,this._y=y*l+i*this._y,this._z=y*c+i*this._z,this.normalize(),this}const p=Math.sqrt(m),g=Math.atan2(p,h),_=Math.sin((1-i)*g)/p,M=Math.sin(i*g)/p;return this._w=d*_+this._w*M,this._x=s*_+this._x*M,this._y=l*_+this._y*M,this._z=c*_+this._z*M,this._onChangeCallback(),this}slerpQuaternions(e,i,s){return this.copy(e).slerp(i,s)}random(){const e=Math.random(),i=Math.sqrt(1-e),s=Math.sqrt(e),l=2*Math.PI*Math.random(),c=2*Math.PI*Math.random();return this.set(i*Math.cos(l),s*Math.sin(c),s*Math.cos(c),i*Math.sin(l))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,i=0){return this._x=e[i],this._y=e[i+1],this._z=e[i+2],this._w=e[i+3],this._onChangeCallback(),this}toArray(e=[],i=0){return e[i]=this._x,e[i+1]=this._y,e[i+2]=this._z,e[i+3]=this._w,e}fromBufferAttribute(e,i){return this._x=e.getX(i),this._y=e.getY(i),this._z=e.getZ(i),this._w=e.getW(i),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}}class at{constructor(e=0,i=0,s=0){at.prototype.isVector3=!0,this.x=e,this.y=i,this.z=s}set(e,i,s){return s===void 0&&(s=this.z),this.x=e,this.y=i,this.z=s,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,i){switch(e){case 0:this.x=i;break;case 1:this.y=i;break;case 2:this.z=i;break;default:throw new Error("index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,i){return this.x=e.x+i.x,this.y=e.y+i.y,this.z=e.z+i.z,this}addScaledVector(e,i){return this.x+=e.x*i,this.y+=e.y*i,this.z+=e.z*i,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,i){return this.x=e.x-i.x,this.y=e.y-i.y,this.z=e.z-i.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,i){return this.x=e.x*i.x,this.y=e.y*i.y,this.z=e.z*i.z,this}applyEuler(e){return this.applyQuaternion(d_.setFromEuler(e))}applyAxisAngle(e,i){return this.applyQuaternion(d_.setFromAxisAngle(e,i))}applyMatrix3(e){const i=this.x,s=this.y,l=this.z,c=e.elements;return this.x=c[0]*i+c[3]*s+c[6]*l,this.y=c[1]*i+c[4]*s+c[7]*l,this.z=c[2]*i+c[5]*s+c[8]*l,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){const i=this.x,s=this.y,l=this.z,c=e.elements,d=1/(c[3]*i+c[7]*s+c[11]*l+c[15]);return this.x=(c[0]*i+c[4]*s+c[8]*l+c[12])*d,this.y=(c[1]*i+c[5]*s+c[9]*l+c[13])*d,this.z=(c[2]*i+c[6]*s+c[10]*l+c[14])*d,this}applyQuaternion(e){const i=this.x,s=this.y,l=this.z,c=e.x,d=e.y,h=e.z,m=e.w,p=2*(d*l-h*s),g=2*(h*i-c*l),_=2*(c*s-d*i);return this.x=i+m*p+d*_-h*g,this.y=s+m*g+h*p-c*_,this.z=l+m*_+c*g-d*p,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){const i=this.x,s=this.y,l=this.z,c=e.elements;return this.x=c[0]*i+c[4]*s+c[8]*l,this.y=c[1]*i+c[5]*s+c[9]*l,this.z=c[2]*i+c[6]*s+c[10]*l,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,i){return this.x=Math.max(e.x,Math.min(i.x,this.x)),this.y=Math.max(e.y,Math.min(i.y,this.y)),this.z=Math.max(e.z,Math.min(i.z,this.z)),this}clampScalar(e,i){return this.x=Math.max(e,Math.min(i,this.x)),this.y=Math.max(e,Math.min(i,this.y)),this.z=Math.max(e,Math.min(i,this.z)),this}clampLength(e,i){const s=this.length();return this.divideScalar(s||1).multiplyScalar(Math.max(e,Math.min(i,s)))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,i){return this.x+=(e.x-this.x)*i,this.y+=(e.y-this.y)*i,this.z+=(e.z-this.z)*i,this}lerpVectors(e,i,s){return this.x=e.x+(i.x-e.x)*s,this.y=e.y+(i.y-e.y)*s,this.z=e.z+(i.z-e.z)*s,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,i){const s=e.x,l=e.y,c=e.z,d=i.x,h=i.y,m=i.z;return this.x=l*m-c*h,this.y=c*d-s*m,this.z=s*h-l*d,this}projectOnVector(e){const i=e.lengthSq();if(i===0)return this.set(0,0,0);const s=e.dot(this)/i;return this.copy(e).multiplyScalar(s)}projectOnPlane(e){return kf.copy(this).projectOnVector(e),this.sub(kf)}reflect(e){return this.sub(kf.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){const i=Math.sqrt(this.lengthSq()*e.lengthSq());if(i===0)return Math.PI/2;const s=this.dot(e)/i;return Math.acos(wn(s,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){const i=this.x-e.x,s=this.y-e.y,l=this.z-e.z;return i*i+s*s+l*l}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,i,s){const l=Math.sin(i)*e;return this.x=l*Math.sin(s),this.y=Math.cos(i)*e,this.z=l*Math.cos(s),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,i,s){return this.x=e*Math.sin(i),this.y=s,this.z=e*Math.cos(i),this}setFromMatrixPosition(e){const i=e.elements;return this.x=i[12],this.y=i[13],this.z=i[14],this}setFromMatrixScale(e){const i=this.setFromMatrixColumn(e,0).length(),s=this.setFromMatrixColumn(e,1).length(),l=this.setFromMatrixColumn(e,2).length();return this.x=i,this.y=s,this.z=l,this}setFromMatrixColumn(e,i){return this.fromArray(e.elements,i*4)}setFromMatrix3Column(e,i){return this.fromArray(e.elements,i*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,i=0){return this.x=e[i],this.y=e[i+1],this.z=e[i+2],this}toArray(e=[],i=0){return e[i]=this.x,e[i+1]=this.y,e[i+2]=this.z,e}fromBufferAttribute(e,i){return this.x=e.getX(i),this.y=e.getY(i),this.z=e.getZ(i),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){const e=(Math.random()-.5)*2,i=Math.random()*Math.PI*2,s=Math.sqrt(1-e**2);return this.x=s*Math.cos(i),this.y=s*Math.sin(i),this.z=e,this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}}const kf=new at,d_=new wo;class Do{constructor(e=new at(1/0,1/0,1/0),i=new at(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=i}set(e,i){return this.min.copy(e),this.max.copy(i),this}setFromArray(e){this.makeEmpty();for(let i=0,s=e.length;i<s;i+=3)this.expandByPoint(hi.fromArray(e,i));return this}setFromBufferAttribute(e){this.makeEmpty();for(let i=0,s=e.count;i<s;i++)this.expandByPoint(hi.fromBufferAttribute(e,i));return this}setFromPoints(e){this.makeEmpty();for(let i=0,s=e.length;i<s;i++)this.expandByPoint(e[i]);return this}setFromCenterAndSize(e,i){const s=hi.copy(i).multiplyScalar(.5);return this.min.copy(e).sub(s),this.max.copy(e).add(s),this}setFromObject(e,i=!1){return this.makeEmpty(),this.expandByObject(e,i)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,i=!1){e.updateWorldMatrix(!1,!1);const s=e.geometry;if(s!==void 0){const c=s.getAttribute("position");if(i===!0&&c!==void 0&&e.isInstancedMesh!==!0)for(let d=0,h=c.count;d<h;d++)e.isMesh===!0?e.getVertexPosition(d,hi):hi.fromBufferAttribute(c,d),hi.applyMatrix4(e.matrixWorld),this.expandByPoint(hi);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),Xl.copy(e.boundingBox)):(s.boundingBox===null&&s.computeBoundingBox(),Xl.copy(s.boundingBox)),Xl.applyMatrix4(e.matrixWorld),this.union(Xl)}const l=e.children;for(let c=0,d=l.length;c<d;c++)this.expandByObject(l[c],i);return this}containsPoint(e){return!(e.x<this.min.x||e.x>this.max.x||e.y<this.min.y||e.y>this.max.y||e.z<this.min.z||e.z>this.max.z)}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,i){return i.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return!(e.max.x<this.min.x||e.min.x>this.max.x||e.max.y<this.min.y||e.min.y>this.max.y||e.max.z<this.min.z||e.min.z>this.max.z)}intersectsSphere(e){return this.clampPoint(e.center,hi),hi.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let i,s;return e.normal.x>0?(i=e.normal.x*this.min.x,s=e.normal.x*this.max.x):(i=e.normal.x*this.max.x,s=e.normal.x*this.min.x),e.normal.y>0?(i+=e.normal.y*this.min.y,s+=e.normal.y*this.max.y):(i+=e.normal.y*this.max.y,s+=e.normal.y*this.min.y),e.normal.z>0?(i+=e.normal.z*this.min.z,s+=e.normal.z*this.max.z):(i+=e.normal.z*this.max.z,s+=e.normal.z*this.min.z),i<=-e.constant&&s>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(So),Wl.subVectors(this.max,So),Qr.subVectors(e.a,So),Jr.subVectors(e.b,So),$r.subVectors(e.c,So),Ra.subVectors(Jr,Qr),Ca.subVectors($r,Jr),ir.subVectors(Qr,$r);let i=[0,-Ra.z,Ra.y,0,-Ca.z,Ca.y,0,-ir.z,ir.y,Ra.z,0,-Ra.x,Ca.z,0,-Ca.x,ir.z,0,-ir.x,-Ra.y,Ra.x,0,-Ca.y,Ca.x,0,-ir.y,ir.x,0];return!qf(i,Qr,Jr,$r,Wl)||(i=[1,0,0,0,1,0,0,0,1],!qf(i,Qr,Jr,$r,Wl))?!1:(kl.crossVectors(Ra,Ca),i=[kl.x,kl.y,kl.z],qf(i,Qr,Jr,$r,Wl))}clampPoint(e,i){return i.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,hi).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(hi).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(Wi[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),Wi[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),Wi[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),Wi[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),Wi[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),Wi[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),Wi[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),Wi[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(Wi),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}}const Wi=[new at,new at,new at,new at,new at,new at,new at,new at],hi=new at,Xl=new Do,Qr=new at,Jr=new at,$r=new at,Ra=new at,Ca=new at,ir=new at,So=new at,Wl=new at,kl=new at,ar=new at;function qf(o,e,i,s,l){for(let c=0,d=o.length-3;c<=d;c+=3){ar.fromArray(o,c);const h=l.x*Math.abs(ar.x)+l.y*Math.abs(ar.y)+l.z*Math.abs(ar.z),m=e.dot(ar),p=i.dot(ar),g=s.dot(ar);if(Math.max(-Math.max(m,p,g),Math.min(m,p,g))>h)return!1}return!0}const ux=new Do,Mo=new at,Yf=new at;class wh{constructor(e=new at,i=-1){this.isSphere=!0,this.center=e,this.radius=i}set(e,i){return this.center.copy(e),this.radius=i,this}setFromPoints(e,i){const s=this.center;i!==void 0?s.copy(i):ux.setFromPoints(e).getCenter(s);let l=0;for(let c=0,d=e.length;c<d;c++)l=Math.max(l,s.distanceToSquared(e[c]));return this.radius=Math.sqrt(l),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){const i=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=i*i}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,i){const s=this.center.distanceToSquared(e);return i.copy(e),s>this.radius*this.radius&&(i.sub(this.center).normalize(),i.multiplyScalar(this.radius).add(this.center)),i}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;Mo.subVectors(e,this.center);const i=Mo.lengthSq();if(i>this.radius*this.radius){const s=Math.sqrt(i),l=(s-this.radius)*.5;this.center.addScaledVector(Mo,l/s),this.radius+=l}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(Yf.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(Mo.copy(e.center).add(Yf)),this.expandByPoint(Mo.copy(e.center).sub(Yf))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}}const ki=new at,jf=new at,ql=new at,wa=new at,Zf=new at,Yl=new at,Kf=new at;class cx{constructor(e=new at,i=new at(0,0,-1)){this.origin=e,this.direction=i}set(e,i){return this.origin.copy(e),this.direction.copy(i),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,i){return i.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,ki)),this}closestPointToPoint(e,i){i.subVectors(e,this.origin);const s=i.dot(this.direction);return s<0?i.copy(this.origin):i.copy(this.origin).addScaledVector(this.direction,s)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){const i=ki.subVectors(e,this.origin).dot(this.direction);return i<0?this.origin.distanceToSquared(e):(ki.copy(this.origin).addScaledVector(this.direction,i),ki.distanceToSquared(e))}distanceSqToSegment(e,i,s,l){jf.copy(e).add(i).multiplyScalar(.5),ql.copy(i).sub(e).normalize(),wa.copy(this.origin).sub(jf);const c=e.distanceTo(i)*.5,d=-this.direction.dot(ql),h=wa.dot(this.direction),m=-wa.dot(ql),p=wa.lengthSq(),g=Math.abs(1-d*d);let _,M,y,b;if(g>0)if(_=d*m-h,M=d*h-m,b=c*g,_>=0)if(M>=-b)if(M<=b){const T=1/g;_*=T,M*=T,y=_*(_+d*M+2*h)+M*(d*_+M+2*m)+p}else M=c,_=Math.max(0,-(d*M+h)),y=-_*_+M*(M+2*m)+p;else M=-c,_=Math.max(0,-(d*M+h)),y=-_*_+M*(M+2*m)+p;else M<=-b?(_=Math.max(0,-(-d*c+h)),M=_>0?-c:Math.min(Math.max(-c,-m),c),y=-_*_+M*(M+2*m)+p):M<=b?(_=0,M=Math.min(Math.max(-c,-m),c),y=M*(M+2*m)+p):(_=Math.max(0,-(d*c+h)),M=_>0?c:Math.min(Math.max(-c,-m),c),y=-_*_+M*(M+2*m)+p);else M=d>0?-c:c,_=Math.max(0,-(d*M+h)),y=-_*_+M*(M+2*m)+p;return s&&s.copy(this.origin).addScaledVector(this.direction,_),l&&l.copy(jf).addScaledVector(ql,M),y}intersectSphere(e,i){ki.subVectors(e.center,this.origin);const s=ki.dot(this.direction),l=ki.dot(ki)-s*s,c=e.radius*e.radius;if(l>c)return null;const d=Math.sqrt(c-l),h=s-d,m=s+d;return m<0?null:h<0?this.at(m,i):this.at(h,i)}intersectsSphere(e){return this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){const i=e.normal.dot(this.direction);if(i===0)return e.distanceToPoint(this.origin)===0?0:null;const s=-(this.origin.dot(e.normal)+e.constant)/i;return s>=0?s:null}intersectPlane(e,i){const s=this.distanceToPlane(e);return s===null?null:this.at(s,i)}intersectsPlane(e){const i=e.distanceToPoint(this.origin);return i===0||e.normal.dot(this.direction)*i<0}intersectBox(e,i){let s,l,c,d,h,m;const p=1/this.direction.x,g=1/this.direction.y,_=1/this.direction.z,M=this.origin;return p>=0?(s=(e.min.x-M.x)*p,l=(e.max.x-M.x)*p):(s=(e.max.x-M.x)*p,l=(e.min.x-M.x)*p),g>=0?(c=(e.min.y-M.y)*g,d=(e.max.y-M.y)*g):(c=(e.max.y-M.y)*g,d=(e.min.y-M.y)*g),s>d||c>l||((c>s||isNaN(s))&&(s=c),(d<l||isNaN(l))&&(l=d),_>=0?(h=(e.min.z-M.z)*_,m=(e.max.z-M.z)*_):(h=(e.max.z-M.z)*_,m=(e.min.z-M.z)*_),s>m||h>l)||((h>s||s!==s)&&(s=h),(m<l||l!==l)&&(l=m),l<0)?null:this.at(s>=0?s:l,i)}intersectsBox(e){return this.intersectBox(e,ki)!==null}intersectTriangle(e,i,s,l,c){Zf.subVectors(i,e),Yl.subVectors(s,e),Kf.crossVectors(Zf,Yl);let d=this.direction.dot(Kf),h;if(d>0){if(l)return null;h=1}else if(d<0)h=-1,d=-d;else return null;wa.subVectors(this.origin,e);const m=h*this.direction.dot(Yl.crossVectors(wa,Yl));if(m<0)return null;const p=h*this.direction.dot(Zf.cross(wa));if(p<0||m+p>d)return null;const g=-h*wa.dot(Kf);return g<0?null:this.at(g/d,c)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}}class rn{constructor(e,i,s,l,c,d,h,m,p,g,_,M,y,b,T,x){rn.prototype.isMatrix4=!0,this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,i,s,l,c,d,h,m,p,g,_,M,y,b,T,x)}set(e,i,s,l,c,d,h,m,p,g,_,M,y,b,T,x){const v=this.elements;return v[0]=e,v[4]=i,v[8]=s,v[12]=l,v[1]=c,v[5]=d,v[9]=h,v[13]=m,v[2]=p,v[6]=g,v[10]=_,v[14]=M,v[3]=y,v[7]=b,v[11]=T,v[15]=x,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new rn().fromArray(this.elements)}copy(e){const i=this.elements,s=e.elements;return i[0]=s[0],i[1]=s[1],i[2]=s[2],i[3]=s[3],i[4]=s[4],i[5]=s[5],i[6]=s[6],i[7]=s[7],i[8]=s[8],i[9]=s[9],i[10]=s[10],i[11]=s[11],i[12]=s[12],i[13]=s[13],i[14]=s[14],i[15]=s[15],this}copyPosition(e){const i=this.elements,s=e.elements;return i[12]=s[12],i[13]=s[13],i[14]=s[14],this}setFromMatrix3(e){const i=e.elements;return this.set(i[0],i[3],i[6],0,i[1],i[4],i[7],0,i[2],i[5],i[8],0,0,0,0,1),this}extractBasis(e,i,s){return e.setFromMatrixColumn(this,0),i.setFromMatrixColumn(this,1),s.setFromMatrixColumn(this,2),this}makeBasis(e,i,s){return this.set(e.x,i.x,s.x,0,e.y,i.y,s.y,0,e.z,i.z,s.z,0,0,0,0,1),this}extractRotation(e){const i=this.elements,s=e.elements,l=1/ts.setFromMatrixColumn(e,0).length(),c=1/ts.setFromMatrixColumn(e,1).length(),d=1/ts.setFromMatrixColumn(e,2).length();return i[0]=s[0]*l,i[1]=s[1]*l,i[2]=s[2]*l,i[3]=0,i[4]=s[4]*c,i[5]=s[5]*c,i[6]=s[6]*c,i[7]=0,i[8]=s[8]*d,i[9]=s[9]*d,i[10]=s[10]*d,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,this}makeRotationFromEuler(e){const i=this.elements,s=e.x,l=e.y,c=e.z,d=Math.cos(s),h=Math.sin(s),m=Math.cos(l),p=Math.sin(l),g=Math.cos(c),_=Math.sin(c);if(e.order==="XYZ"){const M=d*g,y=d*_,b=h*g,T=h*_;i[0]=m*g,i[4]=-m*_,i[8]=p,i[1]=y+b*p,i[5]=M-T*p,i[9]=-h*m,i[2]=T-M*p,i[6]=b+y*p,i[10]=d*m}else if(e.order==="YXZ"){const M=m*g,y=m*_,b=p*g,T=p*_;i[0]=M+T*h,i[4]=b*h-y,i[8]=d*p,i[1]=d*_,i[5]=d*g,i[9]=-h,i[2]=y*h-b,i[6]=T+M*h,i[10]=d*m}else if(e.order==="ZXY"){const M=m*g,y=m*_,b=p*g,T=p*_;i[0]=M-T*h,i[4]=-d*_,i[8]=b+y*h,i[1]=y+b*h,i[5]=d*g,i[9]=T-M*h,i[2]=-d*p,i[6]=h,i[10]=d*m}else if(e.order==="ZYX"){const M=d*g,y=d*_,b=h*g,T=h*_;i[0]=m*g,i[4]=b*p-y,i[8]=M*p+T,i[1]=m*_,i[5]=T*p+M,i[9]=y*p-b,i[2]=-p,i[6]=h*m,i[10]=d*m}else if(e.order==="YZX"){const M=d*m,y=d*p,b=h*m,T=h*p;i[0]=m*g,i[4]=T-M*_,i[8]=b*_+y,i[1]=_,i[5]=d*g,i[9]=-h*g,i[2]=-p*g,i[6]=y*_+b,i[10]=M-T*_}else if(e.order==="XZY"){const M=d*m,y=d*p,b=h*m,T=h*p;i[0]=m*g,i[4]=-_,i[8]=p*g,i[1]=M*_+T,i[5]=d*g,i[9]=y*_-b,i[2]=b*_-y,i[6]=h*g,i[10]=T*_+M}return i[3]=0,i[7]=0,i[11]=0,i[12]=0,i[13]=0,i[14]=0,i[15]=1,this}makeRotationFromQuaternion(e){return this.compose(fx,e,hx)}lookAt(e,i,s){const l=this.elements;return Yn.subVectors(e,i),Yn.lengthSq()===0&&(Yn.z=1),Yn.normalize(),Da.crossVectors(s,Yn),Da.lengthSq()===0&&(Math.abs(s.z)===1?Yn.x+=1e-4:Yn.z+=1e-4,Yn.normalize(),Da.crossVectors(s,Yn)),Da.normalize(),jl.crossVectors(Yn,Da),l[0]=Da.x,l[4]=jl.x,l[8]=Yn.x,l[1]=Da.y,l[5]=jl.y,l[9]=Yn.y,l[2]=Da.z,l[6]=jl.z,l[10]=Yn.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,i){const s=e.elements,l=i.elements,c=this.elements,d=s[0],h=s[4],m=s[8],p=s[12],g=s[1],_=s[5],M=s[9],y=s[13],b=s[2],T=s[6],x=s[10],v=s[14],N=s[3],R=s[7],I=s[11],q=s[15],B=l[0],z=l[4],dt=l[8],w=l[12],U=l[1],lt=l[5],mt=l[9],Et=l[13],V=l[2],$=l[6],O=l[10],k=l[14],Q=l[3],ot=l[7],ct=l[11],D=l[15];return c[0]=d*B+h*U+m*V+p*Q,c[4]=d*z+h*lt+m*$+p*ot,c[8]=d*dt+h*mt+m*O+p*ct,c[12]=d*w+h*Et+m*k+p*D,c[1]=g*B+_*U+M*V+y*Q,c[5]=g*z+_*lt+M*$+y*ot,c[9]=g*dt+_*mt+M*O+y*ct,c[13]=g*w+_*Et+M*k+y*D,c[2]=b*B+T*U+x*V+v*Q,c[6]=b*z+T*lt+x*$+v*ot,c[10]=b*dt+T*mt+x*O+v*ct,c[14]=b*w+T*Et+x*k+v*D,c[3]=N*B+R*U+I*V+q*Q,c[7]=N*z+R*lt+I*$+q*ot,c[11]=N*dt+R*mt+I*O+q*ct,c[15]=N*w+R*Et+I*k+q*D,this}multiplyScalar(e){const i=this.elements;return i[0]*=e,i[4]*=e,i[8]*=e,i[12]*=e,i[1]*=e,i[5]*=e,i[9]*=e,i[13]*=e,i[2]*=e,i[6]*=e,i[10]*=e,i[14]*=e,i[3]*=e,i[7]*=e,i[11]*=e,i[15]*=e,this}determinant(){const e=this.elements,i=e[0],s=e[4],l=e[8],c=e[12],d=e[1],h=e[5],m=e[9],p=e[13],g=e[2],_=e[6],M=e[10],y=e[14],b=e[3],T=e[7],x=e[11],v=e[15];return b*(+c*m*_-l*p*_-c*h*M+s*p*M+l*h*y-s*m*y)+T*(+i*m*y-i*p*M+c*d*M-l*d*y+l*p*g-c*m*g)+x*(+i*p*_-i*h*y-c*d*_+s*d*y+c*h*g-s*p*g)+v*(-l*h*g-i*m*_+i*h*M+l*d*_-s*d*M+s*m*g)}transpose(){const e=this.elements;let i;return i=e[1],e[1]=e[4],e[4]=i,i=e[2],e[2]=e[8],e[8]=i,i=e[6],e[6]=e[9],e[9]=i,i=e[3],e[3]=e[12],e[12]=i,i=e[7],e[7]=e[13],e[13]=i,i=e[11],e[11]=e[14],e[14]=i,this}setPosition(e,i,s){const l=this.elements;return e.isVector3?(l[12]=e.x,l[13]=e.y,l[14]=e.z):(l[12]=e,l[13]=i,l[14]=s),this}invert(){const e=this.elements,i=e[0],s=e[1],l=e[2],c=e[3],d=e[4],h=e[5],m=e[6],p=e[7],g=e[8],_=e[9],M=e[10],y=e[11],b=e[12],T=e[13],x=e[14],v=e[15],N=_*x*p-T*M*p+T*m*y-h*x*y-_*m*v+h*M*v,R=b*M*p-g*x*p-b*m*y+d*x*y+g*m*v-d*M*v,I=g*T*p-b*_*p+b*h*y-d*T*y-g*h*v+d*_*v,q=b*_*m-g*T*m-b*h*M+d*T*M+g*h*x-d*_*x,B=i*N+s*R+l*I+c*q;if(B===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);const z=1/B;return e[0]=N*z,e[1]=(T*M*c-_*x*c-T*l*y+s*x*y+_*l*v-s*M*v)*z,e[2]=(h*x*c-T*m*c+T*l*p-s*x*p-h*l*v+s*m*v)*z,e[3]=(_*m*c-h*M*c-_*l*p+s*M*p+h*l*y-s*m*y)*z,e[4]=R*z,e[5]=(g*x*c-b*M*c+b*l*y-i*x*y-g*l*v+i*M*v)*z,e[6]=(b*m*c-d*x*c-b*l*p+i*x*p+d*l*v-i*m*v)*z,e[7]=(d*M*c-g*m*c+g*l*p-i*M*p-d*l*y+i*m*y)*z,e[8]=I*z,e[9]=(b*_*c-g*T*c-b*s*y+i*T*y+g*s*v-i*_*v)*z,e[10]=(d*T*c-b*h*c+b*s*p-i*T*p-d*s*v+i*h*v)*z,e[11]=(g*h*c-d*_*c-g*s*p+i*_*p+d*s*y-i*h*y)*z,e[12]=q*z,e[13]=(g*T*l-b*_*l+b*s*M-i*T*M-g*s*x+i*_*x)*z,e[14]=(b*h*l-d*T*l-b*s*m+i*T*m+d*s*x-i*h*x)*z,e[15]=(d*_*l-g*h*l+g*s*m-i*_*m-d*s*M+i*h*M)*z,this}scale(e){const i=this.elements,s=e.x,l=e.y,c=e.z;return i[0]*=s,i[4]*=l,i[8]*=c,i[1]*=s,i[5]*=l,i[9]*=c,i[2]*=s,i[6]*=l,i[10]*=c,i[3]*=s,i[7]*=l,i[11]*=c,this}getMaxScaleOnAxis(){const e=this.elements,i=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],s=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],l=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(i,s,l))}makeTranslation(e,i,s){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,i,0,0,1,s,0,0,0,1),this}makeRotationX(e){const i=Math.cos(e),s=Math.sin(e);return this.set(1,0,0,0,0,i,-s,0,0,s,i,0,0,0,0,1),this}makeRotationY(e){const i=Math.cos(e),s=Math.sin(e);return this.set(i,0,s,0,0,1,0,0,-s,0,i,0,0,0,0,1),this}makeRotationZ(e){const i=Math.cos(e),s=Math.sin(e);return this.set(i,-s,0,0,s,i,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,i){const s=Math.cos(i),l=Math.sin(i),c=1-s,d=e.x,h=e.y,m=e.z,p=c*d,g=c*h;return this.set(p*d+s,p*h-l*m,p*m+l*h,0,p*h+l*m,g*h+s,g*m-l*d,0,p*m-l*h,g*m+l*d,c*m*m+s,0,0,0,0,1),this}makeScale(e,i,s){return this.set(e,0,0,0,0,i,0,0,0,0,s,0,0,0,0,1),this}makeShear(e,i,s,l,c,d){return this.set(1,s,c,0,e,1,d,0,i,l,1,0,0,0,0,1),this}compose(e,i,s){const l=this.elements,c=i._x,d=i._y,h=i._z,m=i._w,p=c+c,g=d+d,_=h+h,M=c*p,y=c*g,b=c*_,T=d*g,x=d*_,v=h*_,N=m*p,R=m*g,I=m*_,q=s.x,B=s.y,z=s.z;return l[0]=(1-(T+v))*q,l[1]=(y+I)*q,l[2]=(b-R)*q,l[3]=0,l[4]=(y-I)*B,l[5]=(1-(M+v))*B,l[6]=(x+N)*B,l[7]=0,l[8]=(b+R)*z,l[9]=(x-N)*z,l[10]=(1-(M+T))*z,l[11]=0,l[12]=e.x,l[13]=e.y,l[14]=e.z,l[15]=1,this}decompose(e,i,s){const l=this.elements;let c=ts.set(l[0],l[1],l[2]).length();const d=ts.set(l[4],l[5],l[6]).length(),h=ts.set(l[8],l[9],l[10]).length();this.determinant()<0&&(c=-c),e.x=l[12],e.y=l[13],e.z=l[14],di.copy(this);const p=1/c,g=1/d,_=1/h;return di.elements[0]*=p,di.elements[1]*=p,di.elements[2]*=p,di.elements[4]*=g,di.elements[5]*=g,di.elements[6]*=g,di.elements[8]*=_,di.elements[9]*=_,di.elements[10]*=_,i.setFromRotationMatrix(di),s.x=c,s.y=d,s.z=h,this}makePerspective(e,i,s,l,c,d,h=Qi){const m=this.elements,p=2*c/(i-e),g=2*c/(s-l),_=(i+e)/(i-e),M=(s+l)/(s-l);let y,b;if(h===Qi)y=-(d+c)/(d-c),b=-2*d*c/(d-c);else if(h===_u)y=-d/(d-c),b=-d*c/(d-c);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+h);return m[0]=p,m[4]=0,m[8]=_,m[12]=0,m[1]=0,m[5]=g,m[9]=M,m[13]=0,m[2]=0,m[6]=0,m[10]=y,m[14]=b,m[3]=0,m[7]=0,m[11]=-1,m[15]=0,this}makeOrthographic(e,i,s,l,c,d,h=Qi){const m=this.elements,p=1/(i-e),g=1/(s-l),_=1/(d-c),M=(i+e)*p,y=(s+l)*g;let b,T;if(h===Qi)b=(d+c)*_,T=-2*_;else if(h===_u)b=c*_,T=-1*_;else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+h);return m[0]=2*p,m[4]=0,m[8]=0,m[12]=-M,m[1]=0,m[5]=2*g,m[9]=0,m[13]=-y,m[2]=0,m[6]=0,m[10]=T,m[14]=-b,m[3]=0,m[7]=0,m[11]=0,m[15]=1,this}equals(e){const i=this.elements,s=e.elements;for(let l=0;l<16;l++)if(i[l]!==s[l])return!1;return!0}fromArray(e,i=0){for(let s=0;s<16;s++)this.elements[s]=e[s+i];return this}toArray(e=[],i=0){const s=this.elements;return e[i]=s[0],e[i+1]=s[1],e[i+2]=s[2],e[i+3]=s[3],e[i+4]=s[4],e[i+5]=s[5],e[i+6]=s[6],e[i+7]=s[7],e[i+8]=s[8],e[i+9]=s[9],e[i+10]=s[10],e[i+11]=s[11],e[i+12]=s[12],e[i+13]=s[13],e[i+14]=s[14],e[i+15]=s[15],e}}const ts=new at,di=new rn,fx=new at(0,0,0),hx=new at(1,1,1),Da=new at,jl=new at,Yn=new at,p_=new rn,m_=new wo;class xu{constructor(e=0,i=0,s=0,l=xu.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=i,this._z=s,this._order=l}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,i,s,l=this._order){return this._x=e,this._y=i,this._z=s,this._order=l,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,i=this._order,s=!0){const l=e.elements,c=l[0],d=l[4],h=l[8],m=l[1],p=l[5],g=l[9],_=l[2],M=l[6],y=l[10];switch(i){case"XYZ":this._y=Math.asin(wn(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(-g,y),this._z=Math.atan2(-d,c)):(this._x=Math.atan2(M,p),this._z=0);break;case"YXZ":this._x=Math.asin(-wn(g,-1,1)),Math.abs(g)<.9999999?(this._y=Math.atan2(h,y),this._z=Math.atan2(m,p)):(this._y=Math.atan2(-_,c),this._z=0);break;case"ZXY":this._x=Math.asin(wn(M,-1,1)),Math.abs(M)<.9999999?(this._y=Math.atan2(-_,y),this._z=Math.atan2(-d,p)):(this._y=0,this._z=Math.atan2(m,c));break;case"ZYX":this._y=Math.asin(-wn(_,-1,1)),Math.abs(_)<.9999999?(this._x=Math.atan2(M,y),this._z=Math.atan2(m,c)):(this._x=0,this._z=Math.atan2(-d,p));break;case"YZX":this._z=Math.asin(wn(m,-1,1)),Math.abs(m)<.9999999?(this._x=Math.atan2(-g,p),this._y=Math.atan2(-_,c)):(this._x=0,this._y=Math.atan2(h,y));break;case"XZY":this._z=Math.asin(-wn(d,-1,1)),Math.abs(d)<.9999999?(this._x=Math.atan2(M,p),this._y=Math.atan2(h,c)):(this._x=Math.atan2(-g,y),this._y=0);break;default:console.warn("THREE.Euler: .setFromRotationMatrix() encountered an unknown order: "+i)}return this._order=i,s===!0&&this._onChangeCallback(),this}setFromQuaternion(e,i,s){return p_.makeRotationFromQuaternion(e),this.setFromRotationMatrix(p_,i,s)}setFromVector3(e,i=this._order){return this.set(e.x,e.y,e.z,i)}reorder(e){return m_.setFromEuler(this),this.setFromQuaternion(m_,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],i=0){return e[i]=this._x,e[i+1]=this._y,e[i+2]=this._z,e[i+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}}xu.DEFAULT_ORDER="XYZ";class vv{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}}let dx=0;const g_=new at,es=new wo,qi=new rn,Zl=new at,xo=new at,px=new at,mx=new wo,__=new at(1,0,0),v_=new at(0,1,0),S_=new at(0,0,1),gx={type:"added"},_x={type:"removed"};class Tn extends Ss{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:dx++}),this.uuid=Co(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=Tn.DEFAULT_UP.clone();const e=new at,i=new xu,s=new wo,l=new at(1,1,1);function c(){s.setFromEuler(i,!1)}function d(){i.setFromQuaternion(s,void 0,!1)}i._onChange(c),s._onChange(d),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:i},quaternion:{configurable:!0,enumerable:!0,value:s},scale:{configurable:!0,enumerable:!0,value:l},modelViewMatrix:{value:new rn},normalMatrix:{value:new ce}}),this.matrix=new rn,this.matrixWorld=new rn,this.matrixAutoUpdate=Tn.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=Tn.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new vv,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.userData={}}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,i){this.quaternion.setFromAxisAngle(e,i)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,i){return es.setFromAxisAngle(e,i),this.quaternion.multiply(es),this}rotateOnWorldAxis(e,i){return es.setFromAxisAngle(e,i),this.quaternion.premultiply(es),this}rotateX(e){return this.rotateOnAxis(__,e)}rotateY(e){return this.rotateOnAxis(v_,e)}rotateZ(e){return this.rotateOnAxis(S_,e)}translateOnAxis(e,i){return g_.copy(e).applyQuaternion(this.quaternion),this.position.add(g_.multiplyScalar(i)),this}translateX(e){return this.translateOnAxis(__,e)}translateY(e){return this.translateOnAxis(v_,e)}translateZ(e){return this.translateOnAxis(S_,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(qi.copy(this.matrixWorld).invert())}lookAt(e,i,s){e.isVector3?Zl.copy(e):Zl.set(e,i,s);const l=this.parent;this.updateWorldMatrix(!0,!1),xo.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?qi.lookAt(xo,Zl,this.up):qi.lookAt(Zl,xo,this.up),this.quaternion.setFromRotationMatrix(qi),l&&(qi.extractRotation(l.matrixWorld),es.setFromRotationMatrix(qi),this.quaternion.premultiply(es.invert()))}add(e){if(arguments.length>1){for(let i=0;i<arguments.length;i++)this.add(arguments[i]);return this}return e===this?(console.error("THREE.Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.parent!==null&&e.parent.remove(e),e.parent=this,this.children.push(e),e.dispatchEvent(gx)):console.error("THREE.Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let s=0;s<arguments.length;s++)this.remove(arguments[s]);return this}const i=this.children.indexOf(e);return i!==-1&&(e.parent=null,this.children.splice(i,1),e.dispatchEvent(_x)),this}removeFromParent(){const e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),qi.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),qi.multiply(e.parent.matrixWorld)),e.applyMatrix4(qi),this.add(e),e.updateWorldMatrix(!1,!0),this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,i){if(this[e]===i)return this;for(let s=0,l=this.children.length;s<l;s++){const d=this.children[s].getObjectByProperty(e,i);if(d!==void 0)return d}}getObjectsByProperty(e,i,s=[]){this[e]===i&&s.push(this);const l=this.children;for(let c=0,d=l.length;c<d;c++)l[c].getObjectsByProperty(e,i,s);return s}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(xo,e,px),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(xo,mx,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);const i=this.matrixWorld.elements;return e.set(i[8],i[9],i[10]).normalize()}raycast(){}traverse(e){e(this);const i=this.children;for(let s=0,l=i.length;s<l;s++)i[s].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);const i=this.children;for(let s=0,l=i.length;s<l;s++)i[s].traverseVisible(e)}traverseAncestors(e){const i=this.parent;i!==null&&(e(i),i.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale),this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix),this.matrixWorldNeedsUpdate=!1,e=!0);const i=this.children;for(let s=0,l=i.length;s<l;s++){const c=i[s];(c.matrixWorldAutoUpdate===!0||e===!0)&&c.updateMatrixWorld(e)}}updateWorldMatrix(e,i){const s=this.parent;if(e===!0&&s!==null&&s.matrixWorldAutoUpdate===!0&&s.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix),i===!0){const l=this.children;for(let c=0,d=l.length;c<d;c++){const h=l[c];h.matrixWorldAutoUpdate===!0&&h.updateWorldMatrix(!1,!0)}}}toJSON(e){const i=e===void 0||typeof e=="string",s={};i&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},s.metadata={version:4.6,type:"Object",generator:"Object3D.toJSON"});const l={};l.uuid=this.uuid,l.type=this.type,this.name!==""&&(l.name=this.name),this.castShadow===!0&&(l.castShadow=!0),this.receiveShadow===!0&&(l.receiveShadow=!0),this.visible===!1&&(l.visible=!1),this.frustumCulled===!1&&(l.frustumCulled=!1),this.renderOrder!==0&&(l.renderOrder=this.renderOrder),Object.keys(this.userData).length>0&&(l.userData=this.userData),l.layers=this.layers.mask,l.matrix=this.matrix.toArray(),l.up=this.up.toArray(),this.matrixAutoUpdate===!1&&(l.matrixAutoUpdate=!1),this.isInstancedMesh&&(l.type="InstancedMesh",l.count=this.count,l.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(l.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(l.type="BatchedMesh",l.perObjectFrustumCulled=this.perObjectFrustumCulled,l.sortObjects=this.sortObjects,l.drawRanges=this._drawRanges,l.reservedRanges=this._reservedRanges,l.visibility=this._visibility,l.active=this._active,l.bounds=this._bounds.map(h=>({boxInitialized:h.boxInitialized,boxMin:h.box.min.toArray(),boxMax:h.box.max.toArray(),sphereInitialized:h.sphereInitialized,sphereRadius:h.sphere.radius,sphereCenter:h.sphere.center.toArray()})),l.maxGeometryCount=this._maxGeometryCount,l.maxVertexCount=this._maxVertexCount,l.maxIndexCount=this._maxIndexCount,l.geometryInitialized=this._geometryInitialized,l.geometryCount=this._geometryCount,l.matricesTexture=this._matricesTexture.toJSON(e),this.boundingSphere!==null&&(l.boundingSphere={center:l.boundingSphere.center.toArray(),radius:l.boundingSphere.radius}),this.boundingBox!==null&&(l.boundingBox={min:l.boundingBox.min.toArray(),max:l.boundingBox.max.toArray()}));function c(h,m){return h[m.uuid]===void 0&&(h[m.uuid]=m.toJSON(e)),m.uuid}if(this.isScene)this.background&&(this.background.isColor?l.background=this.background.toJSON():this.background.isTexture&&(l.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(l.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){l.geometry=c(e.geometries,this.geometry);const h=this.geometry.parameters;if(h!==void 0&&h.shapes!==void 0){const m=h.shapes;if(Array.isArray(m))for(let p=0,g=m.length;p<g;p++){const _=m[p];c(e.shapes,_)}else c(e.shapes,m)}}if(this.isSkinnedMesh&&(l.bindMode=this.bindMode,l.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(c(e.skeletons,this.skeleton),l.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){const h=[];for(let m=0,p=this.material.length;m<p;m++)h.push(c(e.materials,this.material[m]));l.material=h}else l.material=c(e.materials,this.material);if(this.children.length>0){l.children=[];for(let h=0;h<this.children.length;h++)l.children.push(this.children[h].toJSON(e).object)}if(this.animations.length>0){l.animations=[];for(let h=0;h<this.animations.length;h++){const m=this.animations[h];l.animations.push(c(e.animations,m))}}if(i){const h=d(e.geometries),m=d(e.materials),p=d(e.textures),g=d(e.images),_=d(e.shapes),M=d(e.skeletons),y=d(e.animations),b=d(e.nodes);h.length>0&&(s.geometries=h),m.length>0&&(s.materials=m),p.length>0&&(s.textures=p),g.length>0&&(s.images=g),_.length>0&&(s.shapes=_),M.length>0&&(s.skeletons=M),y.length>0&&(s.animations=y),b.length>0&&(s.nodes=b)}return s.object=l,s;function d(h){const m=[];for(const p in h){const g=h[p];delete g.metadata,m.push(g)}return m}}clone(e){return new this.constructor().copy(this,e)}copy(e,i=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),i===!0)for(let s=0;s<e.children.length;s++){const l=e.children[s];this.add(l.clone())}return this}}Tn.DEFAULT_UP=new at(0,1,0);Tn.DEFAULT_MATRIX_AUTO_UPDATE=!0;Tn.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;const pi=new at,Yi=new at,Qf=new at,ji=new at,ns=new at,is=new at,M_=new at,Jf=new at,$f=new at,th=new at;let Kl=!1;class mi{constructor(e=new at,i=new at,s=new at){this.a=e,this.b=i,this.c=s}static getNormal(e,i,s,l){l.subVectors(s,i),pi.subVectors(e,i),l.cross(pi);const c=l.lengthSq();return c>0?l.multiplyScalar(1/Math.sqrt(c)):l.set(0,0,0)}static getBarycoord(e,i,s,l,c){pi.subVectors(l,i),Yi.subVectors(s,i),Qf.subVectors(e,i);const d=pi.dot(pi),h=pi.dot(Yi),m=pi.dot(Qf),p=Yi.dot(Yi),g=Yi.dot(Qf),_=d*p-h*h;if(_===0)return c.set(0,0,0),null;const M=1/_,y=(p*m-h*g)*M,b=(d*g-h*m)*M;return c.set(1-y-b,b,y)}static containsPoint(e,i,s,l){return this.getBarycoord(e,i,s,l,ji)===null?!1:ji.x>=0&&ji.y>=0&&ji.x+ji.y<=1}static getUV(e,i,s,l,c,d,h,m){return Kl===!1&&(console.warn("THREE.Triangle.getUV() has been renamed to THREE.Triangle.getInterpolation()."),Kl=!0),this.getInterpolation(e,i,s,l,c,d,h,m)}static getInterpolation(e,i,s,l,c,d,h,m){return this.getBarycoord(e,i,s,l,ji)===null?(m.x=0,m.y=0,"z"in m&&(m.z=0),"w"in m&&(m.w=0),null):(m.setScalar(0),m.addScaledVector(c,ji.x),m.addScaledVector(d,ji.y),m.addScaledVector(h,ji.z),m)}static isFrontFacing(e,i,s,l){return pi.subVectors(s,i),Yi.subVectors(e,i),pi.cross(Yi).dot(l)<0}set(e,i,s){return this.a.copy(e),this.b.copy(i),this.c.copy(s),this}setFromPointsAndIndices(e,i,s,l){return this.a.copy(e[i]),this.b.copy(e[s]),this.c.copy(e[l]),this}setFromAttributeAndIndices(e,i,s,l){return this.a.fromBufferAttribute(e,i),this.b.fromBufferAttribute(e,s),this.c.fromBufferAttribute(e,l),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return pi.subVectors(this.c,this.b),Yi.subVectors(this.a,this.b),pi.cross(Yi).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return mi.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,i){return mi.getBarycoord(e,this.a,this.b,this.c,i)}getUV(e,i,s,l,c){return Kl===!1&&(console.warn("THREE.Triangle.getUV() has been renamed to THREE.Triangle.getInterpolation()."),Kl=!0),mi.getInterpolation(e,this.a,this.b,this.c,i,s,l,c)}getInterpolation(e,i,s,l,c){return mi.getInterpolation(e,this.a,this.b,this.c,i,s,l,c)}containsPoint(e){return mi.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return mi.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,i){const s=this.a,l=this.b,c=this.c;let d,h;ns.subVectors(l,s),is.subVectors(c,s),Jf.subVectors(e,s);const m=ns.dot(Jf),p=is.dot(Jf);if(m<=0&&p<=0)return i.copy(s);$f.subVectors(e,l);const g=ns.dot($f),_=is.dot($f);if(g>=0&&_<=g)return i.copy(l);const M=m*_-g*p;if(M<=0&&m>=0&&g<=0)return d=m/(m-g),i.copy(s).addScaledVector(ns,d);th.subVectors(e,c);const y=ns.dot(th),b=is.dot(th);if(b>=0&&y<=b)return i.copy(c);const T=y*p-m*b;if(T<=0&&p>=0&&b<=0)return h=p/(p-b),i.copy(s).addScaledVector(is,h);const x=g*b-y*_;if(x<=0&&_-g>=0&&y-b>=0)return M_.subVectors(c,l),h=(_-g)/(_-g+(y-b)),i.copy(l).addScaledVector(M_,h);const v=1/(x+T+M);return d=T*v,h=M*v,i.copy(s).addScaledVector(ns,d).addScaledVector(is,h)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}}const Sv={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},La={h:0,s:0,l:0},Ql={h:0,s:0,l:0};function eh(o,e,i){return i<0&&(i+=1),i>1&&(i-=1),i<1/6?o+(e-o)*6*i:i<1/2?e:i<2/3?o+(e-o)*6*(2/3-i):o}class Me{constructor(e,i,s){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,i,s)}set(e,i,s){if(i===void 0&&s===void 0){const l=e;l&&l.isColor?this.copy(l):typeof l=="number"?this.setHex(l):typeof l=="string"&&this.setStyle(l)}else this.setRGB(e,i,s);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,i=vn){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,Ue.toWorkingColorSpace(this,i),this}setRGB(e,i,s,l=Ue.workingColorSpace){return this.r=e,this.g=i,this.b=s,Ue.toWorkingColorSpace(this,l),this}setHSL(e,i,s,l=Ue.workingColorSpace){if(e=nx(e,1),i=wn(i,0,1),s=wn(s,0,1),i===0)this.r=this.g=this.b=s;else{const c=s<=.5?s*(1+i):s+i-s*i,d=2*s-c;this.r=eh(d,c,e+1/3),this.g=eh(d,c,e),this.b=eh(d,c,e-1/3)}return Ue.toWorkingColorSpace(this,l),this}setStyle(e,i=vn){function s(c){c!==void 0&&parseFloat(c)<1&&console.warn("THREE.Color: Alpha component of "+e+" will be ignored.")}let l;if(l=/^(\w+)\(([^\)]*)\)/.exec(e)){let c;const d=l[1],h=l[2];switch(d){case"rgb":case"rgba":if(c=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return s(c[4]),this.setRGB(Math.min(255,parseInt(c[1],10))/255,Math.min(255,parseInt(c[2],10))/255,Math.min(255,parseInt(c[3],10))/255,i);if(c=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return s(c[4]),this.setRGB(Math.min(100,parseInt(c[1],10))/100,Math.min(100,parseInt(c[2],10))/100,Math.min(100,parseInt(c[3],10))/100,i);break;case"hsl":case"hsla":if(c=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return s(c[4]),this.setHSL(parseFloat(c[1])/360,parseFloat(c[2])/100,parseFloat(c[3])/100,i);break;default:console.warn("THREE.Color: Unknown color model "+e)}}else if(l=/^\#([A-Fa-f\d]+)$/.exec(e)){const c=l[1],d=c.length;if(d===3)return this.setRGB(parseInt(c.charAt(0),16)/15,parseInt(c.charAt(1),16)/15,parseInt(c.charAt(2),16)/15,i);if(d===6)return this.setHex(parseInt(c,16),i);console.warn("THREE.Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,i);return this}setColorName(e,i=vn){const s=Sv[e.toLowerCase()];return s!==void 0?this.setHex(s,i):console.warn("THREE.Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=ps(e.r),this.g=ps(e.g),this.b=ps(e.b),this}copyLinearToSRGB(e){return this.r=Xf(e.r),this.g=Xf(e.g),this.b=Xf(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=vn){return Ue.fromWorkingColorSpace(En.copy(this),e),Math.round(wn(En.r*255,0,255))*65536+Math.round(wn(En.g*255,0,255))*256+Math.round(wn(En.b*255,0,255))}getHexString(e=vn){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,i=Ue.workingColorSpace){Ue.fromWorkingColorSpace(En.copy(this),i);const s=En.r,l=En.g,c=En.b,d=Math.max(s,l,c),h=Math.min(s,l,c);let m,p;const g=(h+d)/2;if(h===d)m=0,p=0;else{const _=d-h;switch(p=g<=.5?_/(d+h):_/(2-d-h),d){case s:m=(l-c)/_+(l<c?6:0);break;case l:m=(c-s)/_+2;break;case c:m=(s-l)/_+4;break}m/=6}return e.h=m,e.s=p,e.l=g,e}getRGB(e,i=Ue.workingColorSpace){return Ue.fromWorkingColorSpace(En.copy(this),i),e.r=En.r,e.g=En.g,e.b=En.b,e}getStyle(e=vn){Ue.fromWorkingColorSpace(En.copy(this),e);const i=En.r,s=En.g,l=En.b;return e!==vn?`color(${e} ${i.toFixed(3)} ${s.toFixed(3)} ${l.toFixed(3)})`:`rgb(${Math.round(i*255)},${Math.round(s*255)},${Math.round(l*255)})`}offsetHSL(e,i,s){return this.getHSL(La),this.setHSL(La.h+e,La.s+i,La.l+s)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,i){return this.r=e.r+i.r,this.g=e.g+i.g,this.b=e.b+i.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,i){return this.r+=(e.r-this.r)*i,this.g+=(e.g-this.g)*i,this.b+=(e.b-this.b)*i,this}lerpColors(e,i,s){return this.r=e.r+(i.r-e.r)*s,this.g=e.g+(i.g-e.g)*s,this.b=e.b+(i.b-e.b)*s,this}lerpHSL(e,i){this.getHSL(La),e.getHSL(Ql);const s=Gf(La.h,Ql.h,i),l=Gf(La.s,Ql.s,i),c=Gf(La.l,Ql.l,i);return this.setHSL(s,l,c),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){const i=this.r,s=this.g,l=this.b,c=e.elements;return this.r=c[0]*i+c[3]*s+c[6]*l,this.g=c[1]*i+c[4]*s+c[7]*l,this.b=c[2]*i+c[5]*s+c[8]*l,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,i=0){return this.r=e[i],this.g=e[i+1],this.b=e[i+2],this}toArray(e=[],i=0){return e[i]=this.r,e[i+1]=this.g,e[i+2]=this.b,e}fromBufferAttribute(e,i){return this.r=e.getX(i),this.g=e.getY(i),this.b=e.getZ(i),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}}const En=new Me;Me.NAMES=Sv;let vx=0;class Lo extends Ss{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:vx++}),this.uuid=Co(),this.name="",this.type="Material",this.blending=ds,this.side=Ia,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=gh,this.blendDst=_h,this.blendEquation=ur,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new Me(0,0,0),this.blendAlpha=0,this.depthFunc=du,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=s_,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=Zr,this.stencilZFail=Zr,this.stencilZPass=Zr,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBuild(){}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(const i in e){const s=e[i];if(s===void 0){console.warn(`THREE.Material: parameter '${i}' has value of undefined.`);continue}const l=this[i];if(l===void 0){console.warn(`THREE.Material: '${i}' is not a property of THREE.${this.type}.`);continue}l&&l.isColor?l.set(s):l&&l.isVector3&&s&&s.isVector3?l.copy(s):this[i]=s}}toJSON(e){const i=e===void 0||typeof e=="string";i&&(e={textures:{},images:{}});const s={metadata:{version:4.6,type:"Material",generator:"Material.toJSON"}};s.uuid=this.uuid,s.type=this.type,this.name!==""&&(s.name=this.name),this.color&&this.color.isColor&&(s.color=this.color.getHex()),this.roughness!==void 0&&(s.roughness=this.roughness),this.metalness!==void 0&&(s.metalness=this.metalness),this.sheen!==void 0&&(s.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(s.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(s.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(s.emissive=this.emissive.getHex()),this.emissiveIntensity&&this.emissiveIntensity!==1&&(s.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(s.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(s.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(s.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(s.shininess=this.shininess),this.clearcoat!==void 0&&(s.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(s.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(s.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(s.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(s.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,s.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.iridescence!==void 0&&(s.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(s.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(s.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(s.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(s.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(s.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(s.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(s.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(s.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(s.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(s.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(s.lightMap=this.lightMap.toJSON(e).uuid,s.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(s.aoMap=this.aoMap.toJSON(e).uuid,s.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(s.bumpMap=this.bumpMap.toJSON(e).uuid,s.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(s.normalMap=this.normalMap.toJSON(e).uuid,s.normalMapType=this.normalMapType,s.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(s.displacementMap=this.displacementMap.toJSON(e).uuid,s.displacementScale=this.displacementScale,s.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(s.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(s.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(s.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(s.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(s.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(s.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(s.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(s.combine=this.combine)),this.envMapIntensity!==void 0&&(s.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(s.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(s.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(s.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(s.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(s.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(s.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(s.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(s.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(s.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(s.size=this.size),this.shadowSide!==null&&(s.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(s.sizeAttenuation=this.sizeAttenuation),this.blending!==ds&&(s.blending=this.blending),this.side!==Ia&&(s.side=this.side),this.vertexColors===!0&&(s.vertexColors=!0),this.opacity<1&&(s.opacity=this.opacity),this.transparent===!0&&(s.transparent=!0),this.blendSrc!==gh&&(s.blendSrc=this.blendSrc),this.blendDst!==_h&&(s.blendDst=this.blendDst),this.blendEquation!==ur&&(s.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(s.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(s.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(s.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(s.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(s.blendAlpha=this.blendAlpha),this.depthFunc!==du&&(s.depthFunc=this.depthFunc),this.depthTest===!1&&(s.depthTest=this.depthTest),this.depthWrite===!1&&(s.depthWrite=this.depthWrite),this.colorWrite===!1&&(s.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(s.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==s_&&(s.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(s.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(s.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==Zr&&(s.stencilFail=this.stencilFail),this.stencilZFail!==Zr&&(s.stencilZFail=this.stencilZFail),this.stencilZPass!==Zr&&(s.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(s.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(s.rotation=this.rotation),this.polygonOffset===!0&&(s.polygonOffset=!0),this.polygonOffsetFactor!==0&&(s.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(s.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(s.linewidth=this.linewidth),this.dashSize!==void 0&&(s.dashSize=this.dashSize),this.gapSize!==void 0&&(s.gapSize=this.gapSize),this.scale!==void 0&&(s.scale=this.scale),this.dithering===!0&&(s.dithering=!0),this.alphaTest>0&&(s.alphaTest=this.alphaTest),this.alphaHash===!0&&(s.alphaHash=!0),this.alphaToCoverage===!0&&(s.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(s.premultipliedAlpha=!0),this.forceSinglePass===!0&&(s.forceSinglePass=!0),this.wireframe===!0&&(s.wireframe=!0),this.wireframeLinewidth>1&&(s.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(s.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(s.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(s.flatShading=!0),this.visible===!1&&(s.visible=!1),this.toneMapped===!1&&(s.toneMapped=!1),this.fog===!1&&(s.fog=!1),Object.keys(this.userData).length>0&&(s.userData=this.userData);function l(c){const d=[];for(const h in c){const m=c[h];delete m.metadata,d.push(m)}return d}if(i){const c=l(e.textures),d=l(e.images);c.length>0&&(s.textures=c),d.length>0&&(s.images=d)}return s}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;const i=e.clippingPlanes;let s=null;if(i!==null){const l=i.length;s=new Array(l);for(let c=0;c!==l;++c)s[c]=i[c].clone()}return this.clippingPlanes=s,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}}class Mv extends Lo{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new Me(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.combine=nv,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}}const nn=new at,Jl=new xe;class bi{constructor(e,i,s=!1){if(Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,this.name="",this.array=e,this.itemSize=i,this.count=e!==void 0?e.length/i:0,this.normalized=s,this.usage=o_,this._updateRange={offset:0,count:-1},this.updateRanges=[],this.gpuType=Na,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}get updateRange(){return console.warn("THREE.BufferAttribute: updateRange() is deprecated and will be removed in r169. Use addUpdateRange() instead."),this._updateRange}setUsage(e){return this.usage=e,this}addUpdateRange(e,i){this.updateRanges.push({start:e,count:i})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,i,s){e*=this.itemSize,s*=i.itemSize;for(let l=0,c=this.itemSize;l<c;l++)this.array[e+l]=i.array[s+l];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let i=0,s=this.count;i<s;i++)Jl.fromBufferAttribute(this,i),Jl.applyMatrix3(e),this.setXY(i,Jl.x,Jl.y);else if(this.itemSize===3)for(let i=0,s=this.count;i<s;i++)nn.fromBufferAttribute(this,i),nn.applyMatrix3(e),this.setXYZ(i,nn.x,nn.y,nn.z);return this}applyMatrix4(e){for(let i=0,s=this.count;i<s;i++)nn.fromBufferAttribute(this,i),nn.applyMatrix4(e),this.setXYZ(i,nn.x,nn.y,nn.z);return this}applyNormalMatrix(e){for(let i=0,s=this.count;i<s;i++)nn.fromBufferAttribute(this,i),nn.applyNormalMatrix(e),this.setXYZ(i,nn.x,nn.y,nn.z);return this}transformDirection(e){for(let i=0,s=this.count;i<s;i++)nn.fromBufferAttribute(this,i),nn.transformDirection(e),this.setXYZ(i,nn.x,nn.y,nn.z);return this}set(e,i=0){return this.array.set(e,i),this}getComponent(e,i){let s=this.array[e*this.itemSize+i];return this.normalized&&(s=vo(s,this.array)),s}setComponent(e,i,s){return this.normalized&&(s=Bn(s,this.array)),this.array[e*this.itemSize+i]=s,this}getX(e){let i=this.array[e*this.itemSize];return this.normalized&&(i=vo(i,this.array)),i}setX(e,i){return this.normalized&&(i=Bn(i,this.array)),this.array[e*this.itemSize]=i,this}getY(e){let i=this.array[e*this.itemSize+1];return this.normalized&&(i=vo(i,this.array)),i}setY(e,i){return this.normalized&&(i=Bn(i,this.array)),this.array[e*this.itemSize+1]=i,this}getZ(e){let i=this.array[e*this.itemSize+2];return this.normalized&&(i=vo(i,this.array)),i}setZ(e,i){return this.normalized&&(i=Bn(i,this.array)),this.array[e*this.itemSize+2]=i,this}getW(e){let i=this.array[e*this.itemSize+3];return this.normalized&&(i=vo(i,this.array)),i}setW(e,i){return this.normalized&&(i=Bn(i,this.array)),this.array[e*this.itemSize+3]=i,this}setXY(e,i,s){return e*=this.itemSize,this.normalized&&(i=Bn(i,this.array),s=Bn(s,this.array)),this.array[e+0]=i,this.array[e+1]=s,this}setXYZ(e,i,s,l){return e*=this.itemSize,this.normalized&&(i=Bn(i,this.array),s=Bn(s,this.array),l=Bn(l,this.array)),this.array[e+0]=i,this.array[e+1]=s,this.array[e+2]=l,this}setXYZW(e,i,s,l,c){return e*=this.itemSize,this.normalized&&(i=Bn(i,this.array),s=Bn(s,this.array),l=Bn(l,this.array),c=Bn(c,this.array)),this.array[e+0]=i,this.array[e+1]=s,this.array[e+2]=l,this.array[e+3]=c,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){const e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(e.name=this.name),this.usage!==o_&&(e.usage=this.usage),e}}class xv extends bi{constructor(e,i,s){super(new Uint16Array(e),i,s)}}class yv extends bi{constructor(e,i,s){super(new Uint32Array(e),i,s)}}class Ai extends bi{constructor(e,i,s){super(new Float32Array(e),i,s)}}let Sx=0;const ri=new rn,nh=new Tn,as=new at,jn=new Do,yo=new Do,fn=new at;class Fa extends Ss{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:Sx++}),this.uuid=Co(),this.name="",this.type="BufferGeometry",this.index=null,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(pv(e)?yv:xv)(e,1):this.index=e,this}getAttribute(e){return this.attributes[e]}setAttribute(e,i){return this.attributes[e]=i,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,i,s=0){this.groups.push({start:e,count:i,materialIndex:s})}clearGroups(){this.groups=[]}setDrawRange(e,i){this.drawRange.start=e,this.drawRange.count=i}applyMatrix4(e){const i=this.attributes.position;i!==void 0&&(i.applyMatrix4(e),i.needsUpdate=!0);const s=this.attributes.normal;if(s!==void 0){const c=new ce().getNormalMatrix(e);s.applyNormalMatrix(c),s.needsUpdate=!0}const l=this.attributes.tangent;return l!==void 0&&(l.transformDirection(e),l.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(e){return ri.makeRotationFromQuaternion(e),this.applyMatrix4(ri),this}rotateX(e){return ri.makeRotationX(e),this.applyMatrix4(ri),this}rotateY(e){return ri.makeRotationY(e),this.applyMatrix4(ri),this}rotateZ(e){return ri.makeRotationZ(e),this.applyMatrix4(ri),this}translate(e,i,s){return ri.makeTranslation(e,i,s),this.applyMatrix4(ri),this}scale(e,i,s){return ri.makeScale(e,i,s),this.applyMatrix4(ri),this}lookAt(e){return nh.lookAt(e),nh.updateMatrix(),this.applyMatrix4(nh.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(as).negate(),this.translate(as.x,as.y,as.z),this}setFromPoints(e){const i=[];for(let s=0,l=e.length;s<l;s++){const c=e[s];i.push(c.x,c.y,c.z||0)}return this.setAttribute("position",new Ai(i,3)),this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Do);const e=this.attributes.position,i=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error('THREE.BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box. Alternatively set "mesh.frustumCulled" to "false".',this),this.boundingBox.set(new at(-1/0,-1/0,-1/0),new at(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),i)for(let s=0,l=i.length;s<l;s++){const c=i[s];jn.setFromBufferAttribute(c),this.morphTargetsRelative?(fn.addVectors(this.boundingBox.min,jn.min),this.boundingBox.expandByPoint(fn),fn.addVectors(this.boundingBox.max,jn.max),this.boundingBox.expandByPoint(fn)):(this.boundingBox.expandByPoint(jn.min),this.boundingBox.expandByPoint(jn.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&console.error('THREE.BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new wh);const e=this.attributes.position,i=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){console.error('THREE.BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere. Alternatively set "mesh.frustumCulled" to "false".',this),this.boundingSphere.set(new at,1/0);return}if(e){const s=this.boundingSphere.center;if(jn.setFromBufferAttribute(e),i)for(let c=0,d=i.length;c<d;c++){const h=i[c];yo.setFromBufferAttribute(h),this.morphTargetsRelative?(fn.addVectors(jn.min,yo.min),jn.expandByPoint(fn),fn.addVectors(jn.max,yo.max),jn.expandByPoint(fn)):(jn.expandByPoint(yo.min),jn.expandByPoint(yo.max))}jn.getCenter(s);let l=0;for(let c=0,d=e.count;c<d;c++)fn.fromBufferAttribute(e,c),l=Math.max(l,s.distanceToSquared(fn));if(i)for(let c=0,d=i.length;c<d;c++){const h=i[c],m=this.morphTargetsRelative;for(let p=0,g=h.count;p<g;p++)fn.fromBufferAttribute(h,p),m&&(as.fromBufferAttribute(e,p),fn.add(as)),l=Math.max(l,s.distanceToSquared(fn))}this.boundingSphere.radius=Math.sqrt(l),isNaN(this.boundingSphere.radius)&&console.error('THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){const e=this.index,i=this.attributes;if(e===null||i.position===void 0||i.normal===void 0||i.uv===void 0){console.error("THREE.BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}const s=e.array,l=i.position.array,c=i.normal.array,d=i.uv.array,h=l.length/3;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new bi(new Float32Array(4*h),4));const m=this.getAttribute("tangent").array,p=[],g=[];for(let U=0;U<h;U++)p[U]=new at,g[U]=new at;const _=new at,M=new at,y=new at,b=new xe,T=new xe,x=new xe,v=new at,N=new at;function R(U,lt,mt){_.fromArray(l,U*3),M.fromArray(l,lt*3),y.fromArray(l,mt*3),b.fromArray(d,U*2),T.fromArray(d,lt*2),x.fromArray(d,mt*2),M.sub(_),y.sub(_),T.sub(b),x.sub(b);const Et=1/(T.x*x.y-x.x*T.y);isFinite(Et)&&(v.copy(M).multiplyScalar(x.y).addScaledVector(y,-T.y).multiplyScalar(Et),N.copy(y).multiplyScalar(T.x).addScaledVector(M,-x.x).multiplyScalar(Et),p[U].add(v),p[lt].add(v),p[mt].add(v),g[U].add(N),g[lt].add(N),g[mt].add(N))}let I=this.groups;I.length===0&&(I=[{start:0,count:s.length}]);for(let U=0,lt=I.length;U<lt;++U){const mt=I[U],Et=mt.start,V=mt.count;for(let $=Et,O=Et+V;$<O;$+=3)R(s[$+0],s[$+1],s[$+2])}const q=new at,B=new at,z=new at,dt=new at;function w(U){z.fromArray(c,U*3),dt.copy(z);const lt=p[U];q.copy(lt),q.sub(z.multiplyScalar(z.dot(lt))).normalize(),B.crossVectors(dt,lt);const Et=B.dot(g[U])<0?-1:1;m[U*4]=q.x,m[U*4+1]=q.y,m[U*4+2]=q.z,m[U*4+3]=Et}for(let U=0,lt=I.length;U<lt;++U){const mt=I[U],Et=mt.start,V=mt.count;for(let $=Et,O=Et+V;$<O;$+=3)w(s[$+0]),w(s[$+1]),w(s[$+2])}}computeVertexNormals(){const e=this.index,i=this.getAttribute("position");if(i!==void 0){let s=this.getAttribute("normal");if(s===void 0)s=new bi(new Float32Array(i.count*3),3),this.setAttribute("normal",s);else for(let M=0,y=s.count;M<y;M++)s.setXYZ(M,0,0,0);const l=new at,c=new at,d=new at,h=new at,m=new at,p=new at,g=new at,_=new at;if(e)for(let M=0,y=e.count;M<y;M+=3){const b=e.getX(M+0),T=e.getX(M+1),x=e.getX(M+2);l.fromBufferAttribute(i,b),c.fromBufferAttribute(i,T),d.fromBufferAttribute(i,x),g.subVectors(d,c),_.subVectors(l,c),g.cross(_),h.fromBufferAttribute(s,b),m.fromBufferAttribute(s,T),p.fromBufferAttribute(s,x),h.add(g),m.add(g),p.add(g),s.setXYZ(b,h.x,h.y,h.z),s.setXYZ(T,m.x,m.y,m.z),s.setXYZ(x,p.x,p.y,p.z)}else for(let M=0,y=i.count;M<y;M+=3)l.fromBufferAttribute(i,M+0),c.fromBufferAttribute(i,M+1),d.fromBufferAttribute(i,M+2),g.subVectors(d,c),_.subVectors(l,c),g.cross(_),s.setXYZ(M+0,g.x,g.y,g.z),s.setXYZ(M+1,g.x,g.y,g.z),s.setXYZ(M+2,g.x,g.y,g.z);this.normalizeNormals(),s.needsUpdate=!0}}normalizeNormals(){const e=this.attributes.normal;for(let i=0,s=e.count;i<s;i++)fn.fromBufferAttribute(e,i),fn.normalize(),e.setXYZ(i,fn.x,fn.y,fn.z)}toNonIndexed(){function e(h,m){const p=h.array,g=h.itemSize,_=h.normalized,M=new p.constructor(m.length*g);let y=0,b=0;for(let T=0,x=m.length;T<x;T++){h.isInterleavedBufferAttribute?y=m[T]*h.data.stride+h.offset:y=m[T]*g;for(let v=0;v<g;v++)M[b++]=p[y++]}return new bi(M,g,_)}if(this.index===null)return console.warn("THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;const i=new Fa,s=this.index.array,l=this.attributes;for(const h in l){const m=l[h],p=e(m,s);i.setAttribute(h,p)}const c=this.morphAttributes;for(const h in c){const m=[],p=c[h];for(let g=0,_=p.length;g<_;g++){const M=p[g],y=e(M,s);m.push(y)}i.morphAttributes[h]=m}i.morphTargetsRelative=this.morphTargetsRelative;const d=this.groups;for(let h=0,m=d.length;h<m;h++){const p=d[h];i.addGroup(p.start,p.count,p.materialIndex)}return i}toJSON(){const e={metadata:{version:4.6,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.type,this.name!==""&&(e.name=this.name),Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0){const m=this.parameters;for(const p in m)m[p]!==void 0&&(e[p]=m[p]);return e}e.data={attributes:{}};const i=this.index;i!==null&&(e.data.index={type:i.array.constructor.name,array:Array.prototype.slice.call(i.array)});const s=this.attributes;for(const m in s){const p=s[m];e.data.attributes[m]=p.toJSON(e.data)}const l={};let c=!1;for(const m in this.morphAttributes){const p=this.morphAttributes[m],g=[];for(let _=0,M=p.length;_<M;_++){const y=p[_];g.push(y.toJSON(e.data))}g.length>0&&(l[m]=g,c=!0)}c&&(e.data.morphAttributes=l,e.data.morphTargetsRelative=this.morphTargetsRelative);const d=this.groups;d.length>0&&(e.data.groups=JSON.parse(JSON.stringify(d)));const h=this.boundingSphere;return h!==null&&(e.data.boundingSphere={center:h.center.toArray(),radius:h.radius}),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;const i={};this.name=e.name;const s=e.index;s!==null&&this.setIndex(s.clone(i));const l=e.attributes;for(const p in l){const g=l[p];this.setAttribute(p,g.clone(i))}const c=e.morphAttributes;for(const p in c){const g=[],_=c[p];for(let M=0,y=_.length;M<y;M++)g.push(_[M].clone(i));this.morphAttributes[p]=g}this.morphTargetsRelative=e.morphTargetsRelative;const d=e.groups;for(let p=0,g=d.length;p<g;p++){const _=d[p];this.addGroup(_.start,_.count,_.materialIndex)}const h=e.boundingBox;h!==null&&(this.boundingBox=h.clone());const m=e.boundingSphere;return m!==null&&(this.boundingSphere=m.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}}const x_=new rn,rr=new cx,$l=new wh,y_=new at,rs=new at,ss=new at,os=new at,ih=new at,tu=new at,eu=new xe,nu=new xe,iu=new xe,E_=new at,T_=new at,b_=new at,au=new at,ru=new at;class Oa extends Tn{constructor(e=new Fa,i=new Mv){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=i,this.updateMorphTargets()}copy(e,i){return super.copy(e,i),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){const i=this.geometry.morphAttributes,s=Object.keys(i);if(s.length>0){const l=i[s[0]];if(l!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let c=0,d=l.length;c<d;c++){const h=l[c].name||String(c);this.morphTargetInfluences.push(0),this.morphTargetDictionary[h]=c}}}}getVertexPosition(e,i){const s=this.geometry,l=s.attributes.position,c=s.morphAttributes.position,d=s.morphTargetsRelative;i.fromBufferAttribute(l,e);const h=this.morphTargetInfluences;if(c&&h){tu.set(0,0,0);for(let m=0,p=c.length;m<p;m++){const g=h[m],_=c[m];g!==0&&(ih.fromBufferAttribute(_,e),d?tu.addScaledVector(ih,g):tu.addScaledVector(ih.sub(i),g))}i.add(tu)}return i}raycast(e,i){const s=this.geometry,l=this.material,c=this.matrixWorld;l!==void 0&&(s.boundingSphere===null&&s.computeBoundingSphere(),$l.copy(s.boundingSphere),$l.applyMatrix4(c),rr.copy(e.ray).recast(e.near),!($l.containsPoint(rr.origin)===!1&&(rr.intersectSphere($l,y_)===null||rr.origin.distanceToSquared(y_)>(e.far-e.near)**2))&&(x_.copy(c).invert(),rr.copy(e.ray).applyMatrix4(x_),!(s.boundingBox!==null&&rr.intersectsBox(s.boundingBox)===!1)&&this._computeIntersections(e,i,rr)))}_computeIntersections(e,i,s){let l;const c=this.geometry,d=this.material,h=c.index,m=c.attributes.position,p=c.attributes.uv,g=c.attributes.uv1,_=c.attributes.normal,M=c.groups,y=c.drawRange;if(h!==null)if(Array.isArray(d))for(let b=0,T=M.length;b<T;b++){const x=M[b],v=d[x.materialIndex],N=Math.max(x.start,y.start),R=Math.min(h.count,Math.min(x.start+x.count,y.start+y.count));for(let I=N,q=R;I<q;I+=3){const B=h.getX(I),z=h.getX(I+1),dt=h.getX(I+2);l=su(this,v,e,s,p,g,_,B,z,dt),l&&(l.faceIndex=Math.floor(I/3),l.face.materialIndex=x.materialIndex,i.push(l))}}else{const b=Math.max(0,y.start),T=Math.min(h.count,y.start+y.count);for(let x=b,v=T;x<v;x+=3){const N=h.getX(x),R=h.getX(x+1),I=h.getX(x+2);l=su(this,d,e,s,p,g,_,N,R,I),l&&(l.faceIndex=Math.floor(x/3),i.push(l))}}else if(m!==void 0)if(Array.isArray(d))for(let b=0,T=M.length;b<T;b++){const x=M[b],v=d[x.materialIndex],N=Math.max(x.start,y.start),R=Math.min(m.count,Math.min(x.start+x.count,y.start+y.count));for(let I=N,q=R;I<q;I+=3){const B=I,z=I+1,dt=I+2;l=su(this,v,e,s,p,g,_,B,z,dt),l&&(l.faceIndex=Math.floor(I/3),l.face.materialIndex=x.materialIndex,i.push(l))}}else{const b=Math.max(0,y.start),T=Math.min(m.count,y.start+y.count);for(let x=b,v=T;x<v;x+=3){const N=x,R=x+1,I=x+2;l=su(this,d,e,s,p,g,_,N,R,I),l&&(l.faceIndex=Math.floor(x/3),i.push(l))}}}}function Mx(o,e,i,s,l,c,d,h){let m;if(e.side===In?m=s.intersectTriangle(d,c,l,!0,h):m=s.intersectTriangle(l,c,d,e.side===Ia,h),m===null)return null;ru.copy(h),ru.applyMatrix4(o.matrixWorld);const p=i.ray.origin.distanceTo(ru);return p<i.near||p>i.far?null:{distance:p,point:ru.clone(),object:o}}function su(o,e,i,s,l,c,d,h,m,p){o.getVertexPosition(h,rs),o.getVertexPosition(m,ss),o.getVertexPosition(p,os);const g=Mx(o,e,i,s,rs,ss,os,au);if(g){l&&(eu.fromBufferAttribute(l,h),nu.fromBufferAttribute(l,m),iu.fromBufferAttribute(l,p),g.uv=mi.getInterpolation(au,rs,ss,os,eu,nu,iu,new xe)),c&&(eu.fromBufferAttribute(c,h),nu.fromBufferAttribute(c,m),iu.fromBufferAttribute(c,p),g.uv1=mi.getInterpolation(au,rs,ss,os,eu,nu,iu,new xe),g.uv2=g.uv1),d&&(E_.fromBufferAttribute(d,h),T_.fromBufferAttribute(d,m),b_.fromBufferAttribute(d,p),g.normal=mi.getInterpolation(au,rs,ss,os,E_,T_,b_,new at),g.normal.dot(s.direction)>0&&g.normal.multiplyScalar(-1));const _={a:h,b:m,c:p,normal:new at,materialIndex:0};mi.getNormal(rs,ss,os,_.normal),g.face=_}return g}class Uo extends Fa{constructor(e=1,i=1,s=1,l=1,c=1,d=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:i,depth:s,widthSegments:l,heightSegments:c,depthSegments:d};const h=this;l=Math.floor(l),c=Math.floor(c),d=Math.floor(d);const m=[],p=[],g=[],_=[];let M=0,y=0;b("z","y","x",-1,-1,s,i,e,d,c,0),b("z","y","x",1,-1,s,i,-e,d,c,1),b("x","z","y",1,1,e,s,i,l,d,2),b("x","z","y",1,-1,e,s,-i,l,d,3),b("x","y","z",1,-1,e,i,s,l,c,4),b("x","y","z",-1,-1,e,i,-s,l,c,5),this.setIndex(m),this.setAttribute("position",new Ai(p,3)),this.setAttribute("normal",new Ai(g,3)),this.setAttribute("uv",new Ai(_,2));function b(T,x,v,N,R,I,q,B,z,dt,w){const U=I/z,lt=q/dt,mt=I/2,Et=q/2,V=B/2,$=z+1,O=dt+1;let k=0,Q=0;const ot=new at;for(let ct=0;ct<O;ct++){const D=ct*lt-Et;for(let X=0;X<$;X++){const G=X*U-mt;ot[T]=G*N,ot[x]=D*R,ot[v]=V,p.push(ot.x,ot.y,ot.z),ot[T]=0,ot[x]=0,ot[v]=B>0?1:-1,g.push(ot.x,ot.y,ot.z),_.push(X/z),_.push(1-ct/dt),k+=1}}for(let ct=0;ct<dt;ct++)for(let D=0;D<z;D++){const X=M+D+$*ct,G=M+D+$*(ct+1),Z=M+(D+1)+$*(ct+1),pt=M+(D+1)+$*ct;m.push(X,G,pt),m.push(G,Z,pt),Q+=6}h.addGroup(y,Q,w),y+=Q,M+=k}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Uo(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}}function vs(o){const e={};for(const i in o){e[i]={};for(const s in o[i]){const l=o[i][s];l&&(l.isColor||l.isMatrix3||l.isMatrix4||l.isVector2||l.isVector3||l.isVector4||l.isTexture||l.isQuaternion)?l.isRenderTargetTexture?(console.warn("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[i][s]=null):e[i][s]=l.clone():Array.isArray(l)?e[i][s]=l.slice():e[i][s]=l}}return e}function Rn(o){const e={};for(let i=0;i<o.length;i++){const s=vs(o[i]);for(const l in s)e[l]=s[l]}return e}function xx(o){const e=[];for(let i=0;i<o.length;i++)e.push(o[i].clone());return e}function Ev(o){return o.getRenderTarget()===null?o.outputColorSpace:Ue.workingColorSpace}const yx={clone:vs,merge:Rn};var Ex=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Tx=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`;class mr extends Lo{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=Ex,this.fragmentShader=Tx,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={derivatives:!1,fragDepth:!1,drawBuffers:!1,shaderTextureLOD:!1,clipCullDistance:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=vs(e.uniforms),this.uniformsGroups=xx(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this}toJSON(e){const i=super.toJSON(e);i.glslVersion=this.glslVersion,i.uniforms={};for(const l in this.uniforms){const d=this.uniforms[l].value;d&&d.isTexture?i.uniforms[l]={type:"t",value:d.toJSON(e).uuid}:d&&d.isColor?i.uniforms[l]={type:"c",value:d.getHex()}:d&&d.isVector2?i.uniforms[l]={type:"v2",value:d.toArray()}:d&&d.isVector3?i.uniforms[l]={type:"v3",value:d.toArray()}:d&&d.isVector4?i.uniforms[l]={type:"v4",value:d.toArray()}:d&&d.isMatrix3?i.uniforms[l]={type:"m3",value:d.toArray()}:d&&d.isMatrix4?i.uniforms[l]={type:"m4",value:d.toArray()}:i.uniforms[l]={value:d}}Object.keys(this.defines).length>0&&(i.defines=this.defines),i.vertexShader=this.vertexShader,i.fragmentShader=this.fragmentShader,i.lights=this.lights,i.clipping=this.clipping;const s={};for(const l in this.extensions)this.extensions[l]===!0&&(s[l]=!0);return Object.keys(s).length>0&&(i.extensions=s),i}}class Tv extends Tn{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new rn,this.projectionMatrix=new rn,this.projectionMatrixInverse=new rn,this.coordinateSystem=Qi}copy(e,i){return super.copy(e,i),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorldInverse.copy(this.matrixWorld).invert()}updateWorldMatrix(e,i){super.updateWorldMatrix(e,i),this.matrixWorldInverse.copy(this.matrixWorld).invert()}clone(){return new this.constructor().copy(this)}}class gi extends Tv{constructor(e=50,i=1,s=.1,l=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=s,this.far=l,this.focus=10,this.aspect=i,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,i){return super.copy(e,i),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){const i=.5*this.getFilmHeight()/e;this.fov=Eh*2*Math.atan(i),this.updateProjectionMatrix()}getFocalLength(){const e=Math.tan(fu*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return Eh*2*Math.atan(Math.tan(fu*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}setViewOffset(e,i,s,l,c,d){this.aspect=e/i,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=i,this.view.offsetX=s,this.view.offsetY=l,this.view.width=c,this.view.height=d,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=this.near;let i=e*Math.tan(fu*.5*this.fov)/this.zoom,s=2*i,l=this.aspect*s,c=-.5*l;const d=this.view;if(this.view!==null&&this.view.enabled){const m=d.fullWidth,p=d.fullHeight;c+=d.offsetX*l/m,i-=d.offsetY*s/p,l*=d.width/m,s*=d.height/p}const h=this.filmOffset;h!==0&&(c+=e*h/this.getFilmWidth()),this.projectionMatrix.makePerspective(c,c+l,i,i-s,e,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const i=super.toJSON(e);return i.object.fov=this.fov,i.object.zoom=this.zoom,i.object.near=this.near,i.object.far=this.far,i.object.focus=this.focus,i.object.aspect=this.aspect,this.view!==null&&(i.object.view=Object.assign({},this.view)),i.object.filmGauge=this.filmGauge,i.object.filmOffset=this.filmOffset,i}}const ls=-90,us=1;class bx extends Tn{constructor(e,i,s){super(),this.type="CubeCamera",this.renderTarget=s,this.coordinateSystem=null,this.activeMipmapLevel=0;const l=new gi(ls,us,e,i);l.layers=this.layers,this.add(l);const c=new gi(ls,us,e,i);c.layers=this.layers,this.add(c);const d=new gi(ls,us,e,i);d.layers=this.layers,this.add(d);const h=new gi(ls,us,e,i);h.layers=this.layers,this.add(h);const m=new gi(ls,us,e,i);m.layers=this.layers,this.add(m);const p=new gi(ls,us,e,i);p.layers=this.layers,this.add(p)}updateCoordinateSystem(){const e=this.coordinateSystem,i=this.children.concat(),[s,l,c,d,h,m]=i;for(const p of i)this.remove(p);if(e===Qi)s.up.set(0,1,0),s.lookAt(1,0,0),l.up.set(0,1,0),l.lookAt(-1,0,0),c.up.set(0,0,-1),c.lookAt(0,1,0),d.up.set(0,0,1),d.lookAt(0,-1,0),h.up.set(0,1,0),h.lookAt(0,0,1),m.up.set(0,1,0),m.lookAt(0,0,-1);else if(e===_u)s.up.set(0,-1,0),s.lookAt(-1,0,0),l.up.set(0,-1,0),l.lookAt(1,0,0),c.up.set(0,0,1),c.lookAt(0,1,0),d.up.set(0,0,-1),d.lookAt(0,-1,0),h.up.set(0,-1,0),h.lookAt(0,0,1),m.up.set(0,-1,0),m.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(const p of i)this.add(p),p.updateMatrixWorld()}update(e,i){this.parent===null&&this.updateMatrixWorld();const{renderTarget:s,activeMipmapLevel:l}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());const[c,d,h,m,p,g]=this.children,_=e.getRenderTarget(),M=e.getActiveCubeFace(),y=e.getActiveMipmapLevel(),b=e.xr.enabled;e.xr.enabled=!1;const T=s.texture.generateMipmaps;s.texture.generateMipmaps=!1,e.setRenderTarget(s,0,l),e.render(i,c),e.setRenderTarget(s,1,l),e.render(i,d),e.setRenderTarget(s,2,l),e.render(i,h),e.setRenderTarget(s,3,l),e.render(i,m),e.setRenderTarget(s,4,l),e.render(i,p),s.texture.generateMipmaps=T,e.setRenderTarget(s,5,l),e.render(i,g),e.setRenderTarget(_,M,y),e.xr.enabled=b,s.texture.needsPMREMUpdate=!0}}class bv extends Zn{constructor(e,i,s,l,c,d,h,m,p,g){e=e!==void 0?e:[],i=i!==void 0?i:ms,super(e,i,s,l,c,d,h,m,p,g),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}}class Ax extends pr{constructor(e=1,i={}){super(e,e,i),this.isWebGLCubeRenderTarget=!0;const s={width:e,height:e,depth:1},l=[s,s,s,s,s,s];i.encoding!==void 0&&(To("THREE.WebGLCubeRenderTarget: option.encoding has been replaced by option.colorSpace."),i.colorSpace=i.encoding===dr?vn:oi),this.texture=new bv(l,i.mapping,i.wrapS,i.wrapT,i.magFilter,i.minFilter,i.format,i.type,i.anisotropy,i.colorSpace),this.texture.isRenderTargetTexture=!0,this.texture.generateMipmaps=i.generateMipmaps!==void 0?i.generateMipmaps:!1,this.texture.minFilter=i.minFilter!==void 0?i.minFilter:si}fromEquirectangularTexture(e,i){this.texture.type=i.type,this.texture.colorSpace=i.colorSpace,this.texture.generateMipmaps=i.generateMipmaps,this.texture.minFilter=i.minFilter,this.texture.magFilter=i.magFilter;const s={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},l=new Uo(5,5,5),c=new mr({name:"CubemapFromEquirect",uniforms:vs(s.uniforms),vertexShader:s.vertexShader,fragmentShader:s.fragmentShader,side:In,blending:za});c.uniforms.tEquirect.value=i;const d=new Oa(l,c),h=i.minFilter;return i.minFilter===bo&&(i.minFilter=si),new bx(1,10,this).update(e,d),i.minFilter=h,d.geometry.dispose(),d.material.dispose(),this}clear(e,i,s,l){const c=e.getRenderTarget();for(let d=0;d<6;d++)e.setRenderTarget(this,d),e.clear(i,s,l);e.setRenderTarget(c)}}const ah=new at,Rx=new at,Cx=new ce;class or{constructor(e=new at(1,0,0),i=0){this.isPlane=!0,this.normal=e,this.constant=i}set(e,i){return this.normal.copy(e),this.constant=i,this}setComponents(e,i,s,l){return this.normal.set(e,i,s),this.constant=l,this}setFromNormalAndCoplanarPoint(e,i){return this.normal.copy(e),this.constant=-i.dot(this.normal),this}setFromCoplanarPoints(e,i,s){const l=ah.subVectors(s,i).cross(Rx.subVectors(e,i)).normalize();return this.setFromNormalAndCoplanarPoint(l,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){const e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,i){return i.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,i){const s=e.delta(ah),l=this.normal.dot(s);if(l===0)return this.distanceToPoint(e.start)===0?i.copy(e.start):null;const c=-(e.start.dot(this.normal)+this.constant)/l;return c<0||c>1?null:i.copy(e.start).addScaledVector(s,c)}intersectsLine(e){const i=this.distanceToPoint(e.start),s=this.distanceToPoint(e.end);return i<0&&s>0||s<0&&i>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,i){const s=i||Cx.getNormalMatrix(e),l=this.coplanarPoint(ah).applyMatrix4(e),c=this.normal.applyMatrix3(s).normalize();return this.constant=-l.dot(c),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}}const sr=new wh,ou=new at;class Dh{constructor(e=new or,i=new or,s=new or,l=new or,c=new or,d=new or){this.planes=[e,i,s,l,c,d]}set(e,i,s,l,c,d){const h=this.planes;return h[0].copy(e),h[1].copy(i),h[2].copy(s),h[3].copy(l),h[4].copy(c),h[5].copy(d),this}copy(e){const i=this.planes;for(let s=0;s<6;s++)i[s].copy(e.planes[s]);return this}setFromProjectionMatrix(e,i=Qi){const s=this.planes,l=e.elements,c=l[0],d=l[1],h=l[2],m=l[3],p=l[4],g=l[5],_=l[6],M=l[7],y=l[8],b=l[9],T=l[10],x=l[11],v=l[12],N=l[13],R=l[14],I=l[15];if(s[0].setComponents(m-c,M-p,x-y,I-v).normalize(),s[1].setComponents(m+c,M+p,x+y,I+v).normalize(),s[2].setComponents(m+d,M+g,x+b,I+N).normalize(),s[3].setComponents(m-d,M-g,x-b,I-N).normalize(),s[4].setComponents(m-h,M-_,x-T,I-R).normalize(),i===Qi)s[5].setComponents(m+h,M+_,x+T,I+R).normalize();else if(i===_u)s[5].setComponents(h,_,T,R).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+i);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),sr.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{const i=e.geometry;i.boundingSphere===null&&i.computeBoundingSphere(),sr.copy(i.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(sr)}intersectsSprite(e){return sr.center.set(0,0,0),sr.radius=.7071067811865476,sr.applyMatrix4(e.matrixWorld),this.intersectsSphere(sr)}intersectsSphere(e){const i=this.planes,s=e.center,l=-e.radius;for(let c=0;c<6;c++)if(i[c].distanceToPoint(s)<l)return!1;return!0}intersectsBox(e){const i=this.planes;for(let s=0;s<6;s++){const l=i[s];if(ou.x=l.normal.x>0?e.max.x:e.min.x,ou.y=l.normal.y>0?e.max.y:e.min.y,ou.z=l.normal.z>0?e.max.z:e.min.z,l.distanceToPoint(ou)<0)return!1}return!0}containsPoint(e){const i=this.planes;for(let s=0;s<6;s++)if(i[s].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}}function Av(){let o=null,e=!1,i=null,s=null;function l(c,d){i(c,d),s=o.requestAnimationFrame(l)}return{start:function(){e!==!0&&i!==null&&(s=o.requestAnimationFrame(l),e=!0)},stop:function(){o.cancelAnimationFrame(s),e=!1},setAnimationLoop:function(c){i=c},setContext:function(c){o=c}}}function wx(o,e){const i=e.isWebGL2,s=new WeakMap;function l(p,g){const _=p.array,M=p.usage,y=_.byteLength,b=o.createBuffer();o.bindBuffer(g,b),o.bufferData(g,_,M),p.onUploadCallback();let T;if(_ instanceof Float32Array)T=o.FLOAT;else if(_ instanceof Uint16Array)if(p.isFloat16BufferAttribute)if(i)T=o.HALF_FLOAT;else throw new Error("THREE.WebGLAttributes: Usage of Float16BufferAttribute requires WebGL2.");else T=o.UNSIGNED_SHORT;else if(_ instanceof Int16Array)T=o.SHORT;else if(_ instanceof Uint32Array)T=o.UNSIGNED_INT;else if(_ instanceof Int32Array)T=o.INT;else if(_ instanceof Int8Array)T=o.BYTE;else if(_ instanceof Uint8Array)T=o.UNSIGNED_BYTE;else if(_ instanceof Uint8ClampedArray)T=o.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+_);return{buffer:b,type:T,bytesPerElement:_.BYTES_PER_ELEMENT,version:p.version,size:y}}function c(p,g,_){const M=g.array,y=g._updateRange,b=g.updateRanges;if(o.bindBuffer(_,p),y.count===-1&&b.length===0&&o.bufferSubData(_,0,M),b.length!==0){for(let T=0,x=b.length;T<x;T++){const v=b[T];i?o.bufferSubData(_,v.start*M.BYTES_PER_ELEMENT,M,v.start,v.count):o.bufferSubData(_,v.start*M.BYTES_PER_ELEMENT,M.subarray(v.start,v.start+v.count))}g.clearUpdateRanges()}y.count!==-1&&(i?o.bufferSubData(_,y.offset*M.BYTES_PER_ELEMENT,M,y.offset,y.count):o.bufferSubData(_,y.offset*M.BYTES_PER_ELEMENT,M.subarray(y.offset,y.offset+y.count)),y.count=-1),g.onUploadCallback()}function d(p){return p.isInterleavedBufferAttribute&&(p=p.data),s.get(p)}function h(p){p.isInterleavedBufferAttribute&&(p=p.data);const g=s.get(p);g&&(o.deleteBuffer(g.buffer),s.delete(p))}function m(p,g){if(p.isGLBufferAttribute){const M=s.get(p);(!M||M.version<p.version)&&s.set(p,{buffer:p.buffer,type:p.type,bytesPerElement:p.elementSize,version:p.version});return}p.isInterleavedBufferAttribute&&(p=p.data);const _=s.get(p);if(_===void 0)s.set(p,l(p,g));else if(_.version<p.version){if(_.size!==p.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");c(_.buffer,p,g),_.version=p.version}}return{get:d,remove:h,update:m}}class Lh extends Fa{constructor(e=1,i=1,s=1,l=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:i,widthSegments:s,heightSegments:l};const c=e/2,d=i/2,h=Math.floor(s),m=Math.floor(l),p=h+1,g=m+1,_=e/h,M=i/m,y=[],b=[],T=[],x=[];for(let v=0;v<g;v++){const N=v*M-d;for(let R=0;R<p;R++){const I=R*_-c;b.push(I,-N,0),T.push(0,0,1),x.push(R/h),x.push(1-v/m)}}for(let v=0;v<m;v++)for(let N=0;N<h;N++){const R=N+p*v,I=N+p*(v+1),q=N+1+p*(v+1),B=N+1+p*v;y.push(R,I,B),y.push(I,q,B)}this.setIndex(y),this.setAttribute("position",new Ai(b,3)),this.setAttribute("normal",new Ai(T,3)),this.setAttribute("uv",new Ai(x,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Lh(e.width,e.height,e.widthSegments,e.heightSegments)}}var Dx=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,Lx=`#ifdef USE_ALPHAHASH
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
#endif`,Ux=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Nx=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Ox=`#ifdef USE_ALPHATEST
	if ( diffuseColor.a < alphaTest ) discard;
#endif`,zx=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,Px=`#ifdef USE_AOMAP
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
#endif`,Bx=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,Ix=`#ifdef USE_BATCHING
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
#endif`,Fx=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( batchId );
#endif`,Hx=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,Gx=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Vx=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,Xx=`#ifdef USE_IRIDESCENCE
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
#endif`,Wx=`#ifdef USE_BUMPMAP
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
#endif`,kx=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,qx=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Yx=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,jx=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,Zx=`#if defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#elif defined( USE_COLOR )
	diffuseColor.rgb *= vColor;
#endif`,Kx=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR )
	varying vec3 vColor;
#endif`,Qx=`#if defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR )
	varying vec3 vColor;
#endif`,Jx=`#if defined( USE_COLOR_ALPHA )
	vColor = vec4( 1.0 );
#elif defined( USE_COLOR ) || defined( USE_INSTANCING_COLOR )
	vColor = vec3( 1.0 );
#endif
#ifdef USE_COLOR
	vColor *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.xyz *= instanceColor.xyz;
#endif`,$x=`#define PI 3.141592653589793
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
} // validated`,ty=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,ey=`vec3 transformedNormal = objectNormal;
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
#endif`,ny=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,iy=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,ay=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,ry=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,sy="gl_FragColor = linearToOutputTexel( gl_FragColor );",oy=`
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
}`,ly=`#ifdef USE_ENVMAP
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
#endif`,uy=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform float flipEnvMap;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
	
#endif`,cy=`#ifdef USE_ENVMAP
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
#endif`,fy=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,hy=`#ifdef USE_ENVMAP
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
#endif`,dy=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,py=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,my=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,gy=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,_y=`#ifdef USE_GRADIENTMAP
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
}`,vy=`#ifdef USE_LIGHTMAP
	vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
	vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
	reflectedLight.indirectDiffuse += lightMapIrradiance;
#endif`,Sy=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,My=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,xy=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,yy=`uniform bool receiveShadow;
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
#endif`,Ey=`#ifdef USE_ENVMAP
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
#endif`,Ty=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,by=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,Ay=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,Ry=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,Cy=`PhysicalMaterial material;
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
#endif`,wy=`struct PhysicalMaterial {
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
}`,Dy=`
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
#endif`,Ly=`#if defined( RE_IndirectDiffuse )
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
#endif`,Uy=`#if defined( RE_IndirectDiffuse )
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Ny=`#if defined( USE_LOGDEPTHBUF ) && defined( USE_LOGDEPTHBUF_EXT )
	gl_FragDepthEXT = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,Oy=`#if defined( USE_LOGDEPTHBUF ) && defined( USE_LOGDEPTHBUF_EXT )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,zy=`#ifdef USE_LOGDEPTHBUF
	#ifdef USE_LOGDEPTHBUF_EXT
		varying float vFragDepth;
		varying float vIsPerspective;
	#else
		uniform float logDepthBufFC;
	#endif
#endif`,Py=`#ifdef USE_LOGDEPTHBUF
	#ifdef USE_LOGDEPTHBUF_EXT
		vFragDepth = 1.0 + gl_Position.w;
		vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
	#else
		if ( isPerspectiveMatrix( projectionMatrix ) ) {
			gl_Position.z = log2( max( EPSILON, gl_Position.w + 1.0 ) ) * logDepthBufFC - 1.0;
			gl_Position.z *= gl_Position.w;
		}
	#endif
#endif`,By=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = vec4( mix( pow( sampledDiffuseColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), sampledDiffuseColor.rgb * 0.0773993808, vec3( lessThanEqual( sampledDiffuseColor.rgb, vec3( 0.04045 ) ) ) ), sampledDiffuseColor.w );
	
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,Iy=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,Fy=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,Hy=`#if defined( USE_POINTS_UV )
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
#endif`,Gy=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,Vy=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,Xy=`#if defined( USE_MORPHCOLORS ) && defined( MORPHTARGETS_TEXTURE )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Wy=`#ifdef USE_MORPHNORMALS
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
#endif`,ky=`#ifdef USE_MORPHTARGETS
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
#endif`,qy=`#ifdef USE_MORPHTARGETS
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
#endif`,Yy=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,jy=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,Zy=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Ky=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Qy=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,Jy=`#ifdef USE_NORMALMAP
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
#endif`,$y=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,tE=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,eE=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,nE=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,iE=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,aE=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,rE=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,sE=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,oE=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,lE=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,uE=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,cE=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,fE=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,hE=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,dE=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,pE=`float getShadowMask() {
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
}`,mE=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,gE=`#ifdef USE_SKINNING
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
#endif`,_E=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,vE=`#ifdef USE_SKINNING
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
#endif`,SE=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,ME=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,xE=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,yE=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,EE=`#ifdef USE_TRANSMISSION
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
#endif`,TE=`#ifdef USE_TRANSMISSION
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
#endif`,bE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,AE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,RE=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,CE=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`;const wE=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,DE=`uniform sampler2D t2D;
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
}`,LE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,UE=`#ifdef ENVMAP_TYPE_CUBE
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
}`,NE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,OE=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,zE=`#include <common>
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
}`,PE=`#if DEPTH_PACKING == 3200
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
}`,BE=`#define DISTANCE
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
}`,IE=`#define DISTANCE
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
}`,FE=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,HE=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,GE=`uniform float scale;
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
}`,VE=`uniform vec3 diffuse;
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
}`,XE=`#include <common>
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
}`,WE=`uniform vec3 diffuse;
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
}`,kE=`#define LAMBERT
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
}`,qE=`#define LAMBERT
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
}`,YE=`#define MATCAP
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
}`,jE=`#define MATCAP
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
}`,ZE=`#define NORMAL
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
}`,KE=`#define NORMAL
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
}`,QE=`#define PHONG
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
}`,JE=`#define PHONG
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
}`,$E=`#define STANDARD
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
}`,tT=`#define STANDARD
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
}`,eT=`#define TOON
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
}`,nT=`#define TOON
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
}`,iT=`uniform float size;
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
}`,aT=`uniform vec3 diffuse;
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
}`,rT=`#include <common>
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
}`,sT=`uniform vec3 color;
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
}`,oT=`uniform float rotation;
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
}`,lT=`uniform vec3 diffuse;
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
}`,oe={alphahash_fragment:Dx,alphahash_pars_fragment:Lx,alphamap_fragment:Ux,alphamap_pars_fragment:Nx,alphatest_fragment:Ox,alphatest_pars_fragment:zx,aomap_fragment:Px,aomap_pars_fragment:Bx,batching_pars_vertex:Ix,batching_vertex:Fx,begin_vertex:Hx,beginnormal_vertex:Gx,bsdfs:Vx,iridescence_fragment:Xx,bumpmap_pars_fragment:Wx,clipping_planes_fragment:kx,clipping_planes_pars_fragment:qx,clipping_planes_pars_vertex:Yx,clipping_planes_vertex:jx,color_fragment:Zx,color_pars_fragment:Kx,color_pars_vertex:Qx,color_vertex:Jx,common:$x,cube_uv_reflection_fragment:ty,defaultnormal_vertex:ey,displacementmap_pars_vertex:ny,displacementmap_vertex:iy,emissivemap_fragment:ay,emissivemap_pars_fragment:ry,colorspace_fragment:sy,colorspace_pars_fragment:oy,envmap_fragment:ly,envmap_common_pars_fragment:uy,envmap_pars_fragment:cy,envmap_pars_vertex:fy,envmap_physical_pars_fragment:Ey,envmap_vertex:hy,fog_vertex:dy,fog_pars_vertex:py,fog_fragment:my,fog_pars_fragment:gy,gradientmap_pars_fragment:_y,lightmap_fragment:vy,lightmap_pars_fragment:Sy,lights_lambert_fragment:My,lights_lambert_pars_fragment:xy,lights_pars_begin:yy,lights_toon_fragment:Ty,lights_toon_pars_fragment:by,lights_phong_fragment:Ay,lights_phong_pars_fragment:Ry,lights_physical_fragment:Cy,lights_physical_pars_fragment:wy,lights_fragment_begin:Dy,lights_fragment_maps:Ly,lights_fragment_end:Uy,logdepthbuf_fragment:Ny,logdepthbuf_pars_fragment:Oy,logdepthbuf_pars_vertex:zy,logdepthbuf_vertex:Py,map_fragment:By,map_pars_fragment:Iy,map_particle_fragment:Fy,map_particle_pars_fragment:Hy,metalnessmap_fragment:Gy,metalnessmap_pars_fragment:Vy,morphcolor_vertex:Xy,morphnormal_vertex:Wy,morphtarget_pars_vertex:ky,morphtarget_vertex:qy,normal_fragment_begin:Yy,normal_fragment_maps:jy,normal_pars_fragment:Zy,normal_pars_vertex:Ky,normal_vertex:Qy,normalmap_pars_fragment:Jy,clearcoat_normal_fragment_begin:$y,clearcoat_normal_fragment_maps:tE,clearcoat_pars_fragment:eE,iridescence_pars_fragment:nE,opaque_fragment:iE,packing:aE,premultiplied_alpha_fragment:rE,project_vertex:sE,dithering_fragment:oE,dithering_pars_fragment:lE,roughnessmap_fragment:uE,roughnessmap_pars_fragment:cE,shadowmap_pars_fragment:fE,shadowmap_pars_vertex:hE,shadowmap_vertex:dE,shadowmask_pars_fragment:pE,skinbase_vertex:mE,skinning_pars_vertex:gE,skinning_vertex:_E,skinnormal_vertex:vE,specularmap_fragment:SE,specularmap_pars_fragment:ME,tonemapping_fragment:xE,tonemapping_pars_fragment:yE,transmission_fragment:EE,transmission_pars_fragment:TE,uv_pars_fragment:bE,uv_pars_vertex:AE,uv_vertex:RE,worldpos_vertex:CE,background_vert:wE,background_frag:DE,backgroundCube_vert:LE,backgroundCube_frag:UE,cube_vert:NE,cube_frag:OE,depth_vert:zE,depth_frag:PE,distanceRGBA_vert:BE,distanceRGBA_frag:IE,equirect_vert:FE,equirect_frag:HE,linedashed_vert:GE,linedashed_frag:VE,meshbasic_vert:XE,meshbasic_frag:WE,meshlambert_vert:kE,meshlambert_frag:qE,meshmatcap_vert:YE,meshmatcap_frag:jE,meshnormal_vert:ZE,meshnormal_frag:KE,meshphong_vert:QE,meshphong_frag:JE,meshphysical_vert:$E,meshphysical_frag:tT,meshtoon_vert:eT,meshtoon_frag:nT,points_vert:iT,points_frag:aT,shadow_vert:rT,shadow_frag:sT,sprite_vert:oT,sprite_frag:lT},bt={common:{diffuse:{value:new Me(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new ce},alphaMap:{value:null},alphaMapTransform:{value:new ce},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new ce}},envmap:{envMap:{value:null},flipEnvMap:{value:-1},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new ce}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new ce}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new ce},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new ce},normalScale:{value:new xe(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new ce},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new ce}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new ce}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new ce}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new Me(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMap:{value:[]},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotShadowMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMap:{value:[]},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null}},points:{diffuse:{value:new Me(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new ce},alphaTest:{value:0},uvTransform:{value:new ce}},sprite:{diffuse:{value:new Me(16777215)},opacity:{value:1},center:{value:new xe(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new ce},alphaMap:{value:null},alphaMapTransform:{value:new ce},alphaTest:{value:0}}},Ti={basic:{uniforms:Rn([bt.common,bt.specularmap,bt.envmap,bt.aomap,bt.lightmap,bt.fog]),vertexShader:oe.meshbasic_vert,fragmentShader:oe.meshbasic_frag},lambert:{uniforms:Rn([bt.common,bt.specularmap,bt.envmap,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.fog,bt.lights,{emissive:{value:new Me(0)}}]),vertexShader:oe.meshlambert_vert,fragmentShader:oe.meshlambert_frag},phong:{uniforms:Rn([bt.common,bt.specularmap,bt.envmap,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.fog,bt.lights,{emissive:{value:new Me(0)},specular:{value:new Me(1118481)},shininess:{value:30}}]),vertexShader:oe.meshphong_vert,fragmentShader:oe.meshphong_frag},standard:{uniforms:Rn([bt.common,bt.envmap,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.roughnessmap,bt.metalnessmap,bt.fog,bt.lights,{emissive:{value:new Me(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:oe.meshphysical_vert,fragmentShader:oe.meshphysical_frag},toon:{uniforms:Rn([bt.common,bt.aomap,bt.lightmap,bt.emissivemap,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.gradientmap,bt.fog,bt.lights,{emissive:{value:new Me(0)}}]),vertexShader:oe.meshtoon_vert,fragmentShader:oe.meshtoon_frag},matcap:{uniforms:Rn([bt.common,bt.bumpmap,bt.normalmap,bt.displacementmap,bt.fog,{matcap:{value:null}}]),vertexShader:oe.meshmatcap_vert,fragmentShader:oe.meshmatcap_frag},points:{uniforms:Rn([bt.points,bt.fog]),vertexShader:oe.points_vert,fragmentShader:oe.points_frag},dashed:{uniforms:Rn([bt.common,bt.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:oe.linedashed_vert,fragmentShader:oe.linedashed_frag},depth:{uniforms:Rn([bt.common,bt.displacementmap]),vertexShader:oe.depth_vert,fragmentShader:oe.depth_frag},normal:{uniforms:Rn([bt.common,bt.bumpmap,bt.normalmap,bt.displacementmap,{opacity:{value:1}}]),vertexShader:oe.meshnormal_vert,fragmentShader:oe.meshnormal_frag},sprite:{uniforms:Rn([bt.sprite,bt.fog]),vertexShader:oe.sprite_vert,fragmentShader:oe.sprite_frag},background:{uniforms:{uvTransform:{value:new ce},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:oe.background_vert,fragmentShader:oe.background_frag},backgroundCube:{uniforms:{envMap:{value:null},flipEnvMap:{value:-1},backgroundBlurriness:{value:0},backgroundIntensity:{value:1}},vertexShader:oe.backgroundCube_vert,fragmentShader:oe.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:oe.cube_vert,fragmentShader:oe.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:oe.equirect_vert,fragmentShader:oe.equirect_frag},distanceRGBA:{uniforms:Rn([bt.common,bt.displacementmap,{referencePosition:{value:new at},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:oe.distanceRGBA_vert,fragmentShader:oe.distanceRGBA_frag},shadow:{uniforms:Rn([bt.lights,bt.fog,{color:{value:new Me(0)},opacity:{value:1}}]),vertexShader:oe.shadow_vert,fragmentShader:oe.shadow_frag}};Ti.physical={uniforms:Rn([Ti.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new ce},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new ce},clearcoatNormalScale:{value:new xe(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new ce},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new ce},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new ce},sheen:{value:0},sheenColor:{value:new Me(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new ce},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new ce},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new ce},transmissionSamplerSize:{value:new xe},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new ce},attenuationDistance:{value:0},attenuationColor:{value:new Me(0)},specularColor:{value:new Me(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new ce},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new ce},anisotropyVector:{value:new xe},anisotropyMap:{value:null},anisotropyMapTransform:{value:new ce}}]),vertexShader:oe.meshphysical_vert,fragmentShader:oe.meshphysical_frag};const lu={r:0,b:0,g:0};function uT(o,e,i,s,l,c,d){const h=new Me(0);let m=c===!0?0:1,p,g,_=null,M=0,y=null;function b(x,v){let N=!1,R=v.isScene===!0?v.background:null;R&&R.isTexture&&(R=(v.backgroundBlurriness>0?i:e).get(R)),R===null?T(h,m):R&&R.isColor&&(T(R,1),N=!0);const I=o.xr.getEnvironmentBlendMode();I==="additive"?s.buffers.color.setClear(0,0,0,1,d):I==="alpha-blend"&&s.buffers.color.setClear(0,0,0,0,d),(o.autoClear||N)&&o.clear(o.autoClearColor,o.autoClearDepth,o.autoClearStencil),R&&(R.isCubeTexture||R.mapping===Su)?(g===void 0&&(g=new Oa(new Uo(1,1,1),new mr({name:"BackgroundCubeMaterial",uniforms:vs(Ti.backgroundCube.uniforms),vertexShader:Ti.backgroundCube.vertexShader,fragmentShader:Ti.backgroundCube.fragmentShader,side:In,depthTest:!1,depthWrite:!1,fog:!1})),g.geometry.deleteAttribute("normal"),g.geometry.deleteAttribute("uv"),g.onBeforeRender=function(q,B,z){this.matrixWorld.copyPosition(z.matrixWorld)},Object.defineProperty(g.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),l.update(g)),g.material.uniforms.envMap.value=R,g.material.uniforms.flipEnvMap.value=R.isCubeTexture&&R.isRenderTargetTexture===!1?-1:1,g.material.uniforms.backgroundBlurriness.value=v.backgroundBlurriness,g.material.uniforms.backgroundIntensity.value=v.backgroundIntensity,g.material.toneMapped=Ue.getTransfer(R.colorSpace)!==Fe,(_!==R||M!==R.version||y!==o.toneMapping)&&(g.material.needsUpdate=!0,_=R,M=R.version,y=o.toneMapping),g.layers.enableAll(),x.unshift(g,g.geometry,g.material,0,0,null)):R&&R.isTexture&&(p===void 0&&(p=new Oa(new Lh(2,2),new mr({name:"BackgroundMaterial",uniforms:vs(Ti.background.uniforms),vertexShader:Ti.background.vertexShader,fragmentShader:Ti.background.fragmentShader,side:Ia,depthTest:!1,depthWrite:!1,fog:!1})),p.geometry.deleteAttribute("normal"),Object.defineProperty(p.material,"map",{get:function(){return this.uniforms.t2D.value}}),l.update(p)),p.material.uniforms.t2D.value=R,p.material.uniforms.backgroundIntensity.value=v.backgroundIntensity,p.material.toneMapped=Ue.getTransfer(R.colorSpace)!==Fe,R.matrixAutoUpdate===!0&&R.updateMatrix(),p.material.uniforms.uvTransform.value.copy(R.matrix),(_!==R||M!==R.version||y!==o.toneMapping)&&(p.material.needsUpdate=!0,_=R,M=R.version,y=o.toneMapping),p.layers.enableAll(),x.unshift(p,p.geometry,p.material,0,0,null))}function T(x,v){x.getRGB(lu,Ev(o)),s.buffers.color.setClear(lu.r,lu.g,lu.b,v,d)}return{getClearColor:function(){return h},setClearColor:function(x,v=1){h.set(x),m=v,T(h,m)},getClearAlpha:function(){return m},setClearAlpha:function(x){m=x,T(h,m)},render:b}}function cT(o,e,i,s){const l=o.getParameter(o.MAX_VERTEX_ATTRIBS),c=s.isWebGL2?null:e.get("OES_vertex_array_object"),d=s.isWebGL2||c!==null,h={},m=x(null);let p=m,g=!1;function _(V,$,O,k,Q){let ot=!1;if(d){const ct=T(k,O,$);p!==ct&&(p=ct,y(p.object)),ot=v(V,k,O,Q),ot&&N(V,k,O,Q)}else{const ct=$.wireframe===!0;(p.geometry!==k.id||p.program!==O.id||p.wireframe!==ct)&&(p.geometry=k.id,p.program=O.id,p.wireframe=ct,ot=!0)}Q!==null&&i.update(Q,o.ELEMENT_ARRAY_BUFFER),(ot||g)&&(g=!1,dt(V,$,O,k),Q!==null&&o.bindBuffer(o.ELEMENT_ARRAY_BUFFER,i.get(Q).buffer))}function M(){return s.isWebGL2?o.createVertexArray():c.createVertexArrayOES()}function y(V){return s.isWebGL2?o.bindVertexArray(V):c.bindVertexArrayOES(V)}function b(V){return s.isWebGL2?o.deleteVertexArray(V):c.deleteVertexArrayOES(V)}function T(V,$,O){const k=O.wireframe===!0;let Q=h[V.id];Q===void 0&&(Q={},h[V.id]=Q);let ot=Q[$.id];ot===void 0&&(ot={},Q[$.id]=ot);let ct=ot[k];return ct===void 0&&(ct=x(M()),ot[k]=ct),ct}function x(V){const $=[],O=[],k=[];for(let Q=0;Q<l;Q++)$[Q]=0,O[Q]=0,k[Q]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:$,enabledAttributes:O,attributeDivisors:k,object:V,attributes:{},index:null}}function v(V,$,O,k){const Q=p.attributes,ot=$.attributes;let ct=0;const D=O.getAttributes();for(const X in D)if(D[X].location>=0){const Z=Q[X];let pt=ot[X];if(pt===void 0&&(X==="instanceMatrix"&&V.instanceMatrix&&(pt=V.instanceMatrix),X==="instanceColor"&&V.instanceColor&&(pt=V.instanceColor)),Z===void 0||Z.attribute!==pt||pt&&Z.data!==pt.data)return!0;ct++}return p.attributesNum!==ct||p.index!==k}function N(V,$,O,k){const Q={},ot=$.attributes;let ct=0;const D=O.getAttributes();for(const X in D)if(D[X].location>=0){let Z=ot[X];Z===void 0&&(X==="instanceMatrix"&&V.instanceMatrix&&(Z=V.instanceMatrix),X==="instanceColor"&&V.instanceColor&&(Z=V.instanceColor));const pt={};pt.attribute=Z,Z&&Z.data&&(pt.data=Z.data),Q[X]=pt,ct++}p.attributes=Q,p.attributesNum=ct,p.index=k}function R(){const V=p.newAttributes;for(let $=0,O=V.length;$<O;$++)V[$]=0}function I(V){q(V,0)}function q(V,$){const O=p.newAttributes,k=p.enabledAttributes,Q=p.attributeDivisors;O[V]=1,k[V]===0&&(o.enableVertexAttribArray(V),k[V]=1),Q[V]!==$&&((s.isWebGL2?o:e.get("ANGLE_instanced_arrays"))[s.isWebGL2?"vertexAttribDivisor":"vertexAttribDivisorANGLE"](V,$),Q[V]=$)}function B(){const V=p.newAttributes,$=p.enabledAttributes;for(let O=0,k=$.length;O<k;O++)$[O]!==V[O]&&(o.disableVertexAttribArray(O),$[O]=0)}function z(V,$,O,k,Q,ot,ct){ct===!0?o.vertexAttribIPointer(V,$,O,Q,ot):o.vertexAttribPointer(V,$,O,k,Q,ot)}function dt(V,$,O,k){if(s.isWebGL2===!1&&(V.isInstancedMesh||k.isInstancedBufferGeometry)&&e.get("ANGLE_instanced_arrays")===null)return;R();const Q=k.attributes,ot=O.getAttributes(),ct=$.defaultAttributeValues;for(const D in ot){const X=ot[D];if(X.location>=0){let G=Q[D];if(G===void 0&&(D==="instanceMatrix"&&V.instanceMatrix&&(G=V.instanceMatrix),D==="instanceColor"&&V.instanceColor&&(G=V.instanceColor)),G!==void 0){const Z=G.normalized,pt=G.itemSize,Mt=i.get(G);if(Mt===void 0)continue;const xt=Mt.buffer,It=Mt.type,Nt=Mt.bytesPerElement,kt=s.isWebGL2===!0&&(It===o.INT||It===o.UNSIGNED_INT||G.gpuType===av);if(G.isInterleavedBufferAttribute){const ue=G.data,tt=ue.stride,ln=G.offset;if(ue.isInstancedInterleavedBuffer){for(let Ft=0;Ft<X.locationSize;Ft++)q(X.location+Ft,ue.meshPerAttribute);V.isInstancedMesh!==!0&&k._maxInstanceCount===void 0&&(k._maxInstanceCount=ue.meshPerAttribute*ue.count)}else for(let Ft=0;Ft<X.locationSize;Ft++)I(X.location+Ft);o.bindBuffer(o.ARRAY_BUFFER,xt);for(let Ft=0;Ft<X.locationSize;Ft++)z(X.location+Ft,pt/X.locationSize,It,Z,tt*Nt,(ln+pt/X.locationSize*Ft)*Nt,kt)}else{if(G.isInstancedBufferAttribute){for(let ue=0;ue<X.locationSize;ue++)q(X.location+ue,G.meshPerAttribute);V.isInstancedMesh!==!0&&k._maxInstanceCount===void 0&&(k._maxInstanceCount=G.meshPerAttribute*G.count)}else for(let ue=0;ue<X.locationSize;ue++)I(X.location+ue);o.bindBuffer(o.ARRAY_BUFFER,xt);for(let ue=0;ue<X.locationSize;ue++)z(X.location+ue,pt/X.locationSize,It,Z,pt*Nt,pt/X.locationSize*ue*Nt,kt)}}else if(ct!==void 0){const Z=ct[D];if(Z!==void 0)switch(Z.length){case 2:o.vertexAttrib2fv(X.location,Z);break;case 3:o.vertexAttrib3fv(X.location,Z);break;case 4:o.vertexAttrib4fv(X.location,Z);break;default:o.vertexAttrib1fv(X.location,Z)}}}}B()}function w(){mt();for(const V in h){const $=h[V];for(const O in $){const k=$[O];for(const Q in k)b(k[Q].object),delete k[Q];delete $[O]}delete h[V]}}function U(V){if(h[V.id]===void 0)return;const $=h[V.id];for(const O in $){const k=$[O];for(const Q in k)b(k[Q].object),delete k[Q];delete $[O]}delete h[V.id]}function lt(V){for(const $ in h){const O=h[$];if(O[V.id]===void 0)continue;const k=O[V.id];for(const Q in k)b(k[Q].object),delete k[Q];delete O[V.id]}}function mt(){Et(),g=!0,p!==m&&(p=m,y(p.object))}function Et(){m.geometry=null,m.program=null,m.wireframe=!1}return{setup:_,reset:mt,resetDefaultState:Et,dispose:w,releaseStatesOfGeometry:U,releaseStatesOfProgram:lt,initAttributes:R,enableAttribute:I,disableUnusedAttributes:B}}function fT(o,e,i,s){const l=s.isWebGL2;let c;function d(g){c=g}function h(g,_){o.drawArrays(c,g,_),i.update(_,c,1)}function m(g,_,M){if(M===0)return;let y,b;if(l)y=o,b="drawArraysInstanced";else if(y=e.get("ANGLE_instanced_arrays"),b="drawArraysInstancedANGLE",y===null){console.error("THREE.WebGLBufferRenderer: using THREE.InstancedBufferGeometry but hardware does not support extension ANGLE_instanced_arrays.");return}y[b](c,g,_,M),i.update(_,c,M)}function p(g,_,M){if(M===0)return;const y=e.get("WEBGL_multi_draw");if(y===null)for(let b=0;b<M;b++)this.render(g[b],_[b]);else{y.multiDrawArraysWEBGL(c,g,0,_,0,M);let b=0;for(let T=0;T<M;T++)b+=_[T];i.update(b,c,1)}}this.setMode=d,this.render=h,this.renderInstances=m,this.renderMultiDraw=p}function hT(o,e,i){let s;function l(){if(s!==void 0)return s;if(e.has("EXT_texture_filter_anisotropic")===!0){const z=e.get("EXT_texture_filter_anisotropic");s=o.getParameter(z.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else s=0;return s}function c(z){if(z==="highp"){if(o.getShaderPrecisionFormat(o.VERTEX_SHADER,o.HIGH_FLOAT).precision>0&&o.getShaderPrecisionFormat(o.FRAGMENT_SHADER,o.HIGH_FLOAT).precision>0)return"highp";z="mediump"}return z==="mediump"&&o.getShaderPrecisionFormat(o.VERTEX_SHADER,o.MEDIUM_FLOAT).precision>0&&o.getShaderPrecisionFormat(o.FRAGMENT_SHADER,o.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}const d=typeof WebGL2RenderingContext<"u"&&o.constructor.name==="WebGL2RenderingContext";let h=i.precision!==void 0?i.precision:"highp";const m=c(h);m!==h&&(console.warn("THREE.WebGLRenderer:",h,"not supported, using",m,"instead."),h=m);const p=d||e.has("WEBGL_draw_buffers"),g=i.logarithmicDepthBuffer===!0,_=o.getParameter(o.MAX_TEXTURE_IMAGE_UNITS),M=o.getParameter(o.MAX_VERTEX_TEXTURE_IMAGE_UNITS),y=o.getParameter(o.MAX_TEXTURE_SIZE),b=o.getParameter(o.MAX_CUBE_MAP_TEXTURE_SIZE),T=o.getParameter(o.MAX_VERTEX_ATTRIBS),x=o.getParameter(o.MAX_VERTEX_UNIFORM_VECTORS),v=o.getParameter(o.MAX_VARYING_VECTORS),N=o.getParameter(o.MAX_FRAGMENT_UNIFORM_VECTORS),R=M>0,I=d||e.has("OES_texture_float"),q=R&&I,B=d?o.getParameter(o.MAX_SAMPLES):0;return{isWebGL2:d,drawBuffers:p,getMaxAnisotropy:l,getMaxPrecision:c,precision:h,logarithmicDepthBuffer:g,maxTextures:_,maxVertexTextures:M,maxTextureSize:y,maxCubemapSize:b,maxAttributes:T,maxVertexUniforms:x,maxVaryings:v,maxFragmentUniforms:N,vertexTextures:R,floatFragmentTextures:I,floatVertexTextures:q,maxSamples:B}}function dT(o){const e=this;let i=null,s=0,l=!1,c=!1;const d=new or,h=new ce,m={value:null,needsUpdate:!1};this.uniform=m,this.numPlanes=0,this.numIntersection=0,this.init=function(_,M){const y=_.length!==0||M||s!==0||l;return l=M,s=_.length,y},this.beginShadows=function(){c=!0,g(null)},this.endShadows=function(){c=!1},this.setGlobalState=function(_,M){i=g(_,M,0)},this.setState=function(_,M,y){const b=_.clippingPlanes,T=_.clipIntersection,x=_.clipShadows,v=o.get(_);if(!l||b===null||b.length===0||c&&!x)c?g(null):p();else{const N=c?0:s,R=N*4;let I=v.clippingState||null;m.value=I,I=g(b,M,R,y);for(let q=0;q!==R;++q)I[q]=i[q];v.clippingState=I,this.numIntersection=T?this.numPlanes:0,this.numPlanes+=N}};function p(){m.value!==i&&(m.value=i,m.needsUpdate=s>0),e.numPlanes=s,e.numIntersection=0}function g(_,M,y,b){const T=_!==null?_.length:0;let x=null;if(T!==0){if(x=m.value,b!==!0||x===null){const v=y+T*4,N=M.matrixWorldInverse;h.getNormalMatrix(N),(x===null||x.length<v)&&(x=new Float32Array(v));for(let R=0,I=y;R!==T;++R,I+=4)d.copy(_[R]).applyMatrix4(N,h),d.normal.toArray(x,I),x[I+3]=d.constant}m.value=x,m.needsUpdate=!0}return e.numPlanes=T,e.numIntersection=0,x}}function pT(o){let e=new WeakMap;function i(d,h){return h===vh?d.mapping=ms:h===Sh&&(d.mapping=gs),d}function s(d){if(d&&d.isTexture){const h=d.mapping;if(h===vh||h===Sh)if(e.has(d)){const m=e.get(d).texture;return i(m,d.mapping)}else{const m=d.image;if(m&&m.height>0){const p=new Ax(m.height/2);return p.fromEquirectangularTexture(o,d),e.set(d,p),d.addEventListener("dispose",l),i(p.texture,d.mapping)}else return null}}return d}function l(d){const h=d.target;h.removeEventListener("dispose",l);const m=e.get(h);m!==void 0&&(e.delete(h),m.dispose())}function c(){e=new WeakMap}return{get:s,dispose:c}}class Rv extends Tv{constructor(e=-1,i=1,s=1,l=-1,c=.1,d=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=i,this.top=s,this.bottom=l,this.near=c,this.far=d,this.updateProjectionMatrix()}copy(e,i){return super.copy(e,i),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,i,s,l,c,d){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=i,this.view.offsetX=s,this.view.offsetY=l,this.view.width=c,this.view.height=d,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){const e=(this.right-this.left)/(2*this.zoom),i=(this.top-this.bottom)/(2*this.zoom),s=(this.right+this.left)/2,l=(this.top+this.bottom)/2;let c=s-e,d=s+e,h=l+i,m=l-i;if(this.view!==null&&this.view.enabled){const p=(this.right-this.left)/this.view.fullWidth/this.zoom,g=(this.top-this.bottom)/this.view.fullHeight/this.zoom;c+=p*this.view.offsetX,d=c+p*this.view.width,h-=g*this.view.offsetY,m=h-g*this.view.height}this.projectionMatrix.makeOrthographic(c,d,h,m,this.near,this.far,this.coordinateSystem),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){const i=super.toJSON(e);return i.object.zoom=this.zoom,i.object.left=this.left,i.object.right=this.right,i.object.top=this.top,i.object.bottom=this.bottom,i.object.near=this.near,i.object.far=this.far,this.view!==null&&(i.object.view=Object.assign({},this.view)),i}}const fs=4,A_=[.125,.215,.35,.446,.526,.582],cr=20,rh=new Rv,R_=new Me;let sh=null,oh=0,lh=0;const lr=(1+Math.sqrt(5))/2,cs=1/lr,C_=[new at(1,1,1),new at(-1,1,1),new at(1,1,-1),new at(-1,1,-1),new at(0,lr,cs),new at(0,lr,-cs),new at(cs,0,lr),new at(-cs,0,lr),new at(lr,cs,0),new at(-lr,cs,0)];class w_{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._lodPlanes=[],this._sizeLods=[],this._sigmas=[],this._blurMaterial=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._compileMaterial(this._blurMaterial)}fromScene(e,i=0,s=.1,l=100){sh=this._renderer.getRenderTarget(),oh=this._renderer.getActiveCubeFace(),lh=this._renderer.getActiveMipmapLevel(),this._setSize(256);const c=this._allocateTargets();return c.depthBuffer=!0,this._sceneToCubeUV(e,s,l,c),i>0&&this._blur(c,0,0,i),this._applyPMREM(c),this._cleanup(c),c}fromEquirectangular(e,i=null){return this._fromTexture(e,i)}fromCubemap(e,i=null){return this._fromTexture(e,i)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=U_(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=L_(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose()}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodPlanes.length;e++)this._lodPlanes[e].dispose()}_cleanup(e){this._renderer.setRenderTarget(sh,oh,lh),e.scissorTest=!1,uu(e,0,0,e.width,e.height)}_fromTexture(e,i){e.mapping===ms||e.mapping===gs?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),sh=this._renderer.getRenderTarget(),oh=this._renderer.getActiveCubeFace(),lh=this._renderer.getActiveMipmapLevel();const s=i||this._allocateTargets();return this._textureToCubeUV(e,s),this._applyPMREM(s),this._cleanup(s),s}_allocateTargets(){const e=3*Math.max(this._cubeSize,112),i=4*this._cubeSize,s={magFilter:si,minFilter:si,generateMipmaps:!1,type:Ao,format:vi,colorSpace:Ji,depthBuffer:!1},l=D_(e,i,s);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==i){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=D_(e,i,s);const{_lodMax:c}=this;({sizeLods:this._sizeLods,lodPlanes:this._lodPlanes,sigmas:this._sigmas}=mT(c)),this._blurMaterial=gT(c,e,i)}return l}_compileMaterial(e){const i=new Oa(this._lodPlanes[0],e);this._renderer.compile(i,rh)}_sceneToCubeUV(e,i,s,l){const h=new gi(90,1,i,s),m=[1,-1,1,1,1,1],p=[1,1,1,-1,-1,-1],g=this._renderer,_=g.autoClear,M=g.toneMapping;g.getClearColor(R_),g.toneMapping=Pa,g.autoClear=!1;const y=new Mv({name:"PMREM.Background",side:In,depthWrite:!1,depthTest:!1}),b=new Oa(new Uo,y);let T=!1;const x=e.background;x?x.isColor&&(y.color.copy(x),e.background=null,T=!0):(y.color.copy(R_),T=!0);for(let v=0;v<6;v++){const N=v%3;N===0?(h.up.set(0,m[v],0),h.lookAt(p[v],0,0)):N===1?(h.up.set(0,0,m[v]),h.lookAt(0,p[v],0)):(h.up.set(0,m[v],0),h.lookAt(0,0,p[v]));const R=this._cubeSize;uu(l,N*R,v>2?R:0,R,R),g.setRenderTarget(l),T&&g.render(b,h),g.render(e,h)}b.geometry.dispose(),b.material.dispose(),g.toneMapping=M,g.autoClear=_,e.background=x}_textureToCubeUV(e,i){const s=this._renderer,l=e.mapping===ms||e.mapping===gs;l?(this._cubemapMaterial===null&&(this._cubemapMaterial=U_()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=L_());const c=l?this._cubemapMaterial:this._equirectMaterial,d=new Oa(this._lodPlanes[0],c),h=c.uniforms;h.envMap.value=e;const m=this._cubeSize;uu(i,0,0,3*m,2*m),s.setRenderTarget(i),s.render(d,rh)}_applyPMREM(e){const i=this._renderer,s=i.autoClear;i.autoClear=!1;for(let l=1;l<this._lodPlanes.length;l++){const c=Math.sqrt(this._sigmas[l]*this._sigmas[l]-this._sigmas[l-1]*this._sigmas[l-1]),d=C_[(l-1)%C_.length];this._blur(e,l-1,l,c,d)}i.autoClear=s}_blur(e,i,s,l,c){const d=this._pingPongRenderTarget;this._halfBlur(e,d,i,s,l,"latitudinal",c),this._halfBlur(d,e,s,s,l,"longitudinal",c)}_halfBlur(e,i,s,l,c,d,h){const m=this._renderer,p=this._blurMaterial;d!=="latitudinal"&&d!=="longitudinal"&&console.error("blur direction must be either latitudinal or longitudinal!");const g=3,_=new Oa(this._lodPlanes[l],p),M=p.uniforms,y=this._sizeLods[s]-1,b=isFinite(c)?Math.PI/(2*y):2*Math.PI/(2*cr-1),T=c/b,x=isFinite(c)?1+Math.floor(g*T):cr;x>cr&&console.warn(`sigmaRadians, ${c}, is too large and will clip, as it requested ${x} samples when the maximum is set to ${cr}`);const v=[];let N=0;for(let z=0;z<cr;++z){const dt=z/T,w=Math.exp(-dt*dt/2);v.push(w),z===0?N+=w:z<x&&(N+=2*w)}for(let z=0;z<v.length;z++)v[z]=v[z]/N;M.envMap.value=e.texture,M.samples.value=x,M.weights.value=v,M.latitudinal.value=d==="latitudinal",h&&(M.poleAxis.value=h);const{_lodMax:R}=this;M.dTheta.value=b,M.mipInt.value=R-s;const I=this._sizeLods[l],q=3*I*(l>R-fs?l-R+fs:0),B=4*(this._cubeSize-I);uu(i,q,B,3*I,2*I),m.setRenderTarget(i),m.render(_,rh)}}function mT(o){const e=[],i=[],s=[];let l=o;const c=o-fs+1+A_.length;for(let d=0;d<c;d++){const h=Math.pow(2,l);i.push(h);let m=1/h;d>o-fs?m=A_[d-o+fs-1]:d===0&&(m=0),s.push(m);const p=1/(h-2),g=-p,_=1+p,M=[g,g,_,g,_,_,g,g,_,_,g,_],y=6,b=6,T=3,x=2,v=1,N=new Float32Array(T*b*y),R=new Float32Array(x*b*y),I=new Float32Array(v*b*y);for(let B=0;B<y;B++){const z=B%3*2/3-1,dt=B>2?0:-1,w=[z,dt,0,z+2/3,dt,0,z+2/3,dt+1,0,z,dt,0,z+2/3,dt+1,0,z,dt+1,0];N.set(w,T*b*B),R.set(M,x*b*B);const U=[B,B,B,B,B,B];I.set(U,v*b*B)}const q=new Fa;q.setAttribute("position",new bi(N,T)),q.setAttribute("uv",new bi(R,x)),q.setAttribute("faceIndex",new bi(I,v)),e.push(q),l>fs&&l--}return{lodPlanes:e,sizeLods:i,sigmas:s}}function D_(o,e,i){const s=new pr(o,e,i);return s.texture.mapping=Su,s.texture.name="PMREM.cubeUv",s.scissorTest=!0,s}function uu(o,e,i,s,l){o.viewport.set(e,i,s,l),o.scissor.set(e,i,s,l)}function gT(o,e,i){const s=new Float32Array(cr),l=new at(0,1,0);return new mr({name:"SphericalGaussianBlur",defines:{n:cr,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/i,CUBEUV_MAX_MIP:`${o}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:s},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:l}},vertexShader:Uh(),fragmentShader:`

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
		`,blending:za,depthTest:!1,depthWrite:!1})}function L_(){return new mr({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:Uh(),fragmentShader:`

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
		`,blending:za,depthTest:!1,depthWrite:!1})}function U_(){return new mr({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:Uh(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:za,depthTest:!1,depthWrite:!1})}function Uh(){return`

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
	`}function _T(o){let e=new WeakMap,i=null;function s(h){if(h&&h.isTexture){const m=h.mapping,p=m===vh||m===Sh,g=m===ms||m===gs;if(p||g)if(h.isRenderTargetTexture&&h.needsPMREMUpdate===!0){h.needsPMREMUpdate=!1;let _=e.get(h);return i===null&&(i=new w_(o)),_=p?i.fromEquirectangular(h,_):i.fromCubemap(h,_),e.set(h,_),_.texture}else{if(e.has(h))return e.get(h).texture;{const _=h.image;if(p&&_&&_.height>0||g&&_&&l(_)){i===null&&(i=new w_(o));const M=p?i.fromEquirectangular(h):i.fromCubemap(h);return e.set(h,M),h.addEventListener("dispose",c),M.texture}else return null}}}return h}function l(h){let m=0;const p=6;for(let g=0;g<p;g++)h[g]!==void 0&&m++;return m===p}function c(h){const m=h.target;m.removeEventListener("dispose",c);const p=e.get(m);p!==void 0&&(e.delete(m),p.dispose())}function d(){e=new WeakMap,i!==null&&(i.dispose(),i=null)}return{get:s,dispose:d}}function vT(o){const e={};function i(s){if(e[s]!==void 0)return e[s];let l;switch(s){case"WEBGL_depth_texture":l=o.getExtension("WEBGL_depth_texture")||o.getExtension("MOZ_WEBGL_depth_texture")||o.getExtension("WEBKIT_WEBGL_depth_texture");break;case"EXT_texture_filter_anisotropic":l=o.getExtension("EXT_texture_filter_anisotropic")||o.getExtension("MOZ_EXT_texture_filter_anisotropic")||o.getExtension("WEBKIT_EXT_texture_filter_anisotropic");break;case"WEBGL_compressed_texture_s3tc":l=o.getExtension("WEBGL_compressed_texture_s3tc")||o.getExtension("MOZ_WEBGL_compressed_texture_s3tc")||o.getExtension("WEBKIT_WEBGL_compressed_texture_s3tc");break;case"WEBGL_compressed_texture_pvrtc":l=o.getExtension("WEBGL_compressed_texture_pvrtc")||o.getExtension("WEBKIT_WEBGL_compressed_texture_pvrtc");break;default:l=o.getExtension(s)}return e[s]=l,l}return{has:function(s){return i(s)!==null},init:function(s){s.isWebGL2?(i("EXT_color_buffer_float"),i("WEBGL_clip_cull_distance")):(i("WEBGL_depth_texture"),i("OES_texture_float"),i("OES_texture_half_float"),i("OES_texture_half_float_linear"),i("OES_standard_derivatives"),i("OES_element_index_uint"),i("OES_vertex_array_object"),i("ANGLE_instanced_arrays")),i("OES_texture_float_linear"),i("EXT_color_buffer_half_float"),i("WEBGL_multisampled_render_to_texture")},get:function(s){const l=i(s);return l===null&&console.warn("THREE.WebGLRenderer: "+s+" extension not supported."),l}}}function ST(o,e,i,s){const l={},c=new WeakMap;function d(_){const M=_.target;M.index!==null&&e.remove(M.index);for(const b in M.attributes)e.remove(M.attributes[b]);for(const b in M.morphAttributes){const T=M.morphAttributes[b];for(let x=0,v=T.length;x<v;x++)e.remove(T[x])}M.removeEventListener("dispose",d),delete l[M.id];const y=c.get(M);y&&(e.remove(y),c.delete(M)),s.releaseStatesOfGeometry(M),M.isInstancedBufferGeometry===!0&&delete M._maxInstanceCount,i.memory.geometries--}function h(_,M){return l[M.id]===!0||(M.addEventListener("dispose",d),l[M.id]=!0,i.memory.geometries++),M}function m(_){const M=_.attributes;for(const b in M)e.update(M[b],o.ARRAY_BUFFER);const y=_.morphAttributes;for(const b in y){const T=y[b];for(let x=0,v=T.length;x<v;x++)e.update(T[x],o.ARRAY_BUFFER)}}function p(_){const M=[],y=_.index,b=_.attributes.position;let T=0;if(y!==null){const N=y.array;T=y.version;for(let R=0,I=N.length;R<I;R+=3){const q=N[R+0],B=N[R+1],z=N[R+2];M.push(q,B,B,z,z,q)}}else if(b!==void 0){const N=b.array;T=b.version;for(let R=0,I=N.length/3-1;R<I;R+=3){const q=R+0,B=R+1,z=R+2;M.push(q,B,B,z,z,q)}}else return;const x=new(pv(M)?yv:xv)(M,1);x.version=T;const v=c.get(_);v&&e.remove(v),c.set(_,x)}function g(_){const M=c.get(_);if(M){const y=_.index;y!==null&&M.version<y.version&&p(_)}else p(_);return c.get(_)}return{get:h,update:m,getWireframeAttribute:g}}function MT(o,e,i,s){const l=s.isWebGL2;let c;function d(y){c=y}let h,m;function p(y){h=y.type,m=y.bytesPerElement}function g(y,b){o.drawElements(c,b,h,y*m),i.update(b,c,1)}function _(y,b,T){if(T===0)return;let x,v;if(l)x=o,v="drawElementsInstanced";else if(x=e.get("ANGLE_instanced_arrays"),v="drawElementsInstancedANGLE",x===null){console.error("THREE.WebGLIndexedBufferRenderer: using THREE.InstancedBufferGeometry but hardware does not support extension ANGLE_instanced_arrays.");return}x[v](c,b,h,y*m,T),i.update(b,c,T)}function M(y,b,T){if(T===0)return;const x=e.get("WEBGL_multi_draw");if(x===null)for(let v=0;v<T;v++)this.render(y[v]/m,b[v]);else{x.multiDrawElementsWEBGL(c,b,0,h,y,0,T);let v=0;for(let N=0;N<T;N++)v+=b[N];i.update(v,c,1)}}this.setMode=d,this.setIndex=p,this.render=g,this.renderInstances=_,this.renderMultiDraw=M}function xT(o){const e={geometries:0,textures:0},i={frame:0,calls:0,triangles:0,points:0,lines:0};function s(c,d,h){switch(i.calls++,d){case o.TRIANGLES:i.triangles+=h*(c/3);break;case o.LINES:i.lines+=h*(c/2);break;case o.LINE_STRIP:i.lines+=h*(c-1);break;case o.LINE_LOOP:i.lines+=h*c;break;case o.POINTS:i.points+=h*c;break;default:console.error("THREE.WebGLInfo: Unknown draw mode:",d);break}}function l(){i.calls=0,i.triangles=0,i.points=0,i.lines=0}return{memory:e,render:i,programs:null,autoReset:!0,reset:l,update:s}}function yT(o,e){return o[0]-e[0]}function ET(o,e){return Math.abs(e[1])-Math.abs(o[1])}function TT(o,e,i){const s={},l=new Float32Array(8),c=new WeakMap,d=new hn,h=[];for(let p=0;p<8;p++)h[p]=[p,0];function m(p,g,_){const M=p.morphTargetInfluences;if(e.isWebGL2===!0){const y=g.morphAttributes.position||g.morphAttributes.normal||g.morphAttributes.color,b=y!==void 0?y.length:0;let T=c.get(g);if(T===void 0||T.count!==b){let V=function(){mt.dispose(),c.delete(g),g.removeEventListener("dispose",V)};T!==void 0&&T.texture.dispose();const N=g.morphAttributes.position!==void 0,R=g.morphAttributes.normal!==void 0,I=g.morphAttributes.color!==void 0,q=g.morphAttributes.position||[],B=g.morphAttributes.normal||[],z=g.morphAttributes.color||[];let dt=0;N===!0&&(dt=1),R===!0&&(dt=2),I===!0&&(dt=3);let w=g.attributes.position.count*dt,U=1;w>e.maxTextureSize&&(U=Math.ceil(w/e.maxTextureSize),w=e.maxTextureSize);const lt=new Float32Array(w*U*4*b),mt=new _v(lt,w,U,b);mt.type=Na,mt.needsUpdate=!0;const Et=dt*4;for(let $=0;$<b;$++){const O=q[$],k=B[$],Q=z[$],ot=w*U*4*$;for(let ct=0;ct<O.count;ct++){const D=ct*Et;N===!0&&(d.fromBufferAttribute(O,ct),lt[ot+D+0]=d.x,lt[ot+D+1]=d.y,lt[ot+D+2]=d.z,lt[ot+D+3]=0),R===!0&&(d.fromBufferAttribute(k,ct),lt[ot+D+4]=d.x,lt[ot+D+5]=d.y,lt[ot+D+6]=d.z,lt[ot+D+7]=0),I===!0&&(d.fromBufferAttribute(Q,ct),lt[ot+D+8]=d.x,lt[ot+D+9]=d.y,lt[ot+D+10]=d.z,lt[ot+D+11]=Q.itemSize===4?d.w:1)}}T={count:b,texture:mt,size:new xe(w,U)},c.set(g,T),g.addEventListener("dispose",V)}let x=0;for(let N=0;N<M.length;N++)x+=M[N];const v=g.morphTargetsRelative?1:1-x;_.getUniforms().setValue(o,"morphTargetBaseInfluence",v),_.getUniforms().setValue(o,"morphTargetInfluences",M),_.getUniforms().setValue(o,"morphTargetsTexture",T.texture,i),_.getUniforms().setValue(o,"morphTargetsTextureSize",T.size)}else{const y=M===void 0?0:M.length;let b=s[g.id];if(b===void 0||b.length!==y){b=[];for(let R=0;R<y;R++)b[R]=[R,0];s[g.id]=b}for(let R=0;R<y;R++){const I=b[R];I[0]=R,I[1]=M[R]}b.sort(ET);for(let R=0;R<8;R++)R<y&&b[R][1]?(h[R][0]=b[R][0],h[R][1]=b[R][1]):(h[R][0]=Number.MAX_SAFE_INTEGER,h[R][1]=0);h.sort(yT);const T=g.morphAttributes.position,x=g.morphAttributes.normal;let v=0;for(let R=0;R<8;R++){const I=h[R],q=I[0],B=I[1];q!==Number.MAX_SAFE_INTEGER&&B?(T&&g.getAttribute("morphTarget"+R)!==T[q]&&g.setAttribute("morphTarget"+R,T[q]),x&&g.getAttribute("morphNormal"+R)!==x[q]&&g.setAttribute("morphNormal"+R,x[q]),l[R]=B,v+=B):(T&&g.hasAttribute("morphTarget"+R)===!0&&g.deleteAttribute("morphTarget"+R),x&&g.hasAttribute("morphNormal"+R)===!0&&g.deleteAttribute("morphNormal"+R),l[R]=0)}const N=g.morphTargetsRelative?1:1-v;_.getUniforms().setValue(o,"morphTargetBaseInfluence",N),_.getUniforms().setValue(o,"morphTargetInfluences",l)}}return{update:m}}function bT(o,e,i,s){let l=new WeakMap;function c(m){const p=s.render.frame,g=m.geometry,_=e.get(m,g);if(l.get(_)!==p&&(e.update(_),l.set(_,p)),m.isInstancedMesh&&(m.hasEventListener("dispose",h)===!1&&m.addEventListener("dispose",h),l.get(m)!==p&&(i.update(m.instanceMatrix,o.ARRAY_BUFFER),m.instanceColor!==null&&i.update(m.instanceColor,o.ARRAY_BUFFER),l.set(m,p))),m.isSkinnedMesh){const M=m.skeleton;l.get(M)!==p&&(M.update(),l.set(M,p))}return _}function d(){l=new WeakMap}function h(m){const p=m.target;p.removeEventListener("dispose",h),i.remove(p.instanceMatrix),p.instanceColor!==null&&i.remove(p.instanceColor)}return{update:c,dispose:d}}class Cv extends Zn{constructor(e,i,s,l,c,d,h,m,p,g){if(g=g!==void 0?g:hr,g!==hr&&g!==_s)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");s===void 0&&g===hr&&(s=Ua),s===void 0&&g===_s&&(s=fr),super(null,l,c,d,h,m,g,s,p),this.isDepthTexture=!0,this.image={width:e,height:i},this.magFilter=h!==void 0?h:Cn,this.minFilter=m!==void 0?m:Cn,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.compareFunction=e.compareFunction,this}toJSON(e){const i=super.toJSON(e);return this.compareFunction!==null&&(i.compareFunction=this.compareFunction),i}}const wv=new Zn,Dv=new Cv(1,1);Dv.compareFunction=dv;const Lv=new _v,Uv=new lx,Nv=new bv,N_=[],O_=[],z_=new Float32Array(16),P_=new Float32Array(9),B_=new Float32Array(4);function Ms(o,e,i){const s=o[0];if(s<=0||s>0)return o;const l=e*i;let c=N_[l];if(c===void 0&&(c=new Float32Array(l),N_[l]=c),e!==0){s.toArray(c,0);for(let d=1,h=0;d!==e;++d)h+=i,o[d].toArray(c,h)}return c}function sn(o,e){if(o.length!==e.length)return!1;for(let i=0,s=o.length;i<s;i++)if(o[i]!==e[i])return!1;return!0}function on(o,e){for(let i=0,s=e.length;i<s;i++)o[i]=e[i]}function yu(o,e){let i=O_[e];i===void 0&&(i=new Int32Array(e),O_[e]=i);for(let s=0;s!==e;++s)i[s]=o.allocateTextureUnit();return i}function AT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1f(this.addr,e),i[0]=e)}function RT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2f(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(sn(i,e))return;o.uniform2fv(this.addr,e),on(i,e)}}function CT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3f(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else if(e.r!==void 0)(i[0]!==e.r||i[1]!==e.g||i[2]!==e.b)&&(o.uniform3f(this.addr,e.r,e.g,e.b),i[0]=e.r,i[1]=e.g,i[2]=e.b);else{if(sn(i,e))return;o.uniform3fv(this.addr,e),on(i,e)}}function wT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4f(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(sn(i,e))return;o.uniform4fv(this.addr,e),on(i,e)}}function DT(o,e){const i=this.cache,s=e.elements;if(s===void 0){if(sn(i,e))return;o.uniformMatrix2fv(this.addr,!1,e),on(i,e)}else{if(sn(i,s))return;B_.set(s),o.uniformMatrix2fv(this.addr,!1,B_),on(i,s)}}function LT(o,e){const i=this.cache,s=e.elements;if(s===void 0){if(sn(i,e))return;o.uniformMatrix3fv(this.addr,!1,e),on(i,e)}else{if(sn(i,s))return;P_.set(s),o.uniformMatrix3fv(this.addr,!1,P_),on(i,s)}}function UT(o,e){const i=this.cache,s=e.elements;if(s===void 0){if(sn(i,e))return;o.uniformMatrix4fv(this.addr,!1,e),on(i,e)}else{if(sn(i,s))return;z_.set(s),o.uniformMatrix4fv(this.addr,!1,z_),on(i,s)}}function NT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1i(this.addr,e),i[0]=e)}function OT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2i(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(sn(i,e))return;o.uniform2iv(this.addr,e),on(i,e)}}function zT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3i(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else{if(sn(i,e))return;o.uniform3iv(this.addr,e),on(i,e)}}function PT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4i(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(sn(i,e))return;o.uniform4iv(this.addr,e),on(i,e)}}function BT(o,e){const i=this.cache;i[0]!==e&&(o.uniform1ui(this.addr,e),i[0]=e)}function IT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y)&&(o.uniform2ui(this.addr,e.x,e.y),i[0]=e.x,i[1]=e.y);else{if(sn(i,e))return;o.uniform2uiv(this.addr,e),on(i,e)}}function FT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z)&&(o.uniform3ui(this.addr,e.x,e.y,e.z),i[0]=e.x,i[1]=e.y,i[2]=e.z);else{if(sn(i,e))return;o.uniform3uiv(this.addr,e),on(i,e)}}function HT(o,e){const i=this.cache;if(e.x!==void 0)(i[0]!==e.x||i[1]!==e.y||i[2]!==e.z||i[3]!==e.w)&&(o.uniform4ui(this.addr,e.x,e.y,e.z,e.w),i[0]=e.x,i[1]=e.y,i[2]=e.z,i[3]=e.w);else{if(sn(i,e))return;o.uniform4uiv(this.addr,e),on(i,e)}}function GT(o,e,i){const s=this.cache,l=i.allocateTextureUnit();s[0]!==l&&(o.uniform1i(this.addr,l),s[0]=l);const c=this.type===o.SAMPLER_2D_SHADOW?Dv:wv;i.setTexture2D(e||c,l)}function VT(o,e,i){const s=this.cache,l=i.allocateTextureUnit();s[0]!==l&&(o.uniform1i(this.addr,l),s[0]=l),i.setTexture3D(e||Uv,l)}function XT(o,e,i){const s=this.cache,l=i.allocateTextureUnit();s[0]!==l&&(o.uniform1i(this.addr,l),s[0]=l),i.setTextureCube(e||Nv,l)}function WT(o,e,i){const s=this.cache,l=i.allocateTextureUnit();s[0]!==l&&(o.uniform1i(this.addr,l),s[0]=l),i.setTexture2DArray(e||Lv,l)}function kT(o){switch(o){case 5126:return AT;case 35664:return RT;case 35665:return CT;case 35666:return wT;case 35674:return DT;case 35675:return LT;case 35676:return UT;case 5124:case 35670:return NT;case 35667:case 35671:return OT;case 35668:case 35672:return zT;case 35669:case 35673:return PT;case 5125:return BT;case 36294:return IT;case 36295:return FT;case 36296:return HT;case 35678:case 36198:case 36298:case 36306:case 35682:return GT;case 35679:case 36299:case 36307:return VT;case 35680:case 36300:case 36308:case 36293:return XT;case 36289:case 36303:case 36311:case 36292:return WT}}function qT(o,e){o.uniform1fv(this.addr,e)}function YT(o,e){const i=Ms(e,this.size,2);o.uniform2fv(this.addr,i)}function jT(o,e){const i=Ms(e,this.size,3);o.uniform3fv(this.addr,i)}function ZT(o,e){const i=Ms(e,this.size,4);o.uniform4fv(this.addr,i)}function KT(o,e){const i=Ms(e,this.size,4);o.uniformMatrix2fv(this.addr,!1,i)}function QT(o,e){const i=Ms(e,this.size,9);o.uniformMatrix3fv(this.addr,!1,i)}function JT(o,e){const i=Ms(e,this.size,16);o.uniformMatrix4fv(this.addr,!1,i)}function $T(o,e){o.uniform1iv(this.addr,e)}function tb(o,e){o.uniform2iv(this.addr,e)}function eb(o,e){o.uniform3iv(this.addr,e)}function nb(o,e){o.uniform4iv(this.addr,e)}function ib(o,e){o.uniform1uiv(this.addr,e)}function ab(o,e){o.uniform2uiv(this.addr,e)}function rb(o,e){o.uniform3uiv(this.addr,e)}function sb(o,e){o.uniform4uiv(this.addr,e)}function ob(o,e,i){const s=this.cache,l=e.length,c=yu(i,l);sn(s,c)||(o.uniform1iv(this.addr,c),on(s,c));for(let d=0;d!==l;++d)i.setTexture2D(e[d]||wv,c[d])}function lb(o,e,i){const s=this.cache,l=e.length,c=yu(i,l);sn(s,c)||(o.uniform1iv(this.addr,c),on(s,c));for(let d=0;d!==l;++d)i.setTexture3D(e[d]||Uv,c[d])}function ub(o,e,i){const s=this.cache,l=e.length,c=yu(i,l);sn(s,c)||(o.uniform1iv(this.addr,c),on(s,c));for(let d=0;d!==l;++d)i.setTextureCube(e[d]||Nv,c[d])}function cb(o,e,i){const s=this.cache,l=e.length,c=yu(i,l);sn(s,c)||(o.uniform1iv(this.addr,c),on(s,c));for(let d=0;d!==l;++d)i.setTexture2DArray(e[d]||Lv,c[d])}function fb(o){switch(o){case 5126:return qT;case 35664:return YT;case 35665:return jT;case 35666:return ZT;case 35674:return KT;case 35675:return QT;case 35676:return JT;case 5124:case 35670:return $T;case 35667:case 35671:return tb;case 35668:case 35672:return eb;case 35669:case 35673:return nb;case 5125:return ib;case 36294:return ab;case 36295:return rb;case 36296:return sb;case 35678:case 36198:case 36298:case 36306:case 35682:return ob;case 35679:case 36299:case 36307:return lb;case 35680:case 36300:case 36308:case 36293:return ub;case 36289:case 36303:case 36311:case 36292:return cb}}class hb{constructor(e,i,s){this.id=e,this.addr=s,this.cache=[],this.type=i.type,this.setValue=kT(i.type)}}class db{constructor(e,i,s){this.id=e,this.addr=s,this.cache=[],this.type=i.type,this.size=i.size,this.setValue=fb(i.type)}}class pb{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,i,s){const l=this.seq;for(let c=0,d=l.length;c!==d;++c){const h=l[c];h.setValue(e,i[h.id],s)}}}const uh=/(\w+)(\])?(\[|\.)?/g;function I_(o,e){o.seq.push(e),o.map[e.id]=e}function mb(o,e,i){const s=o.name,l=s.length;for(uh.lastIndex=0;;){const c=uh.exec(s),d=uh.lastIndex;let h=c[1];const m=c[2]==="]",p=c[3];if(m&&(h=h|0),p===void 0||p==="["&&d+2===l){I_(i,p===void 0?new hb(h,o,e):new db(h,o,e));break}else{let _=i.map[h];_===void 0&&(_=new pb(h),I_(i,_)),i=_}}}class hu{constructor(e,i){this.seq=[],this.map={};const s=e.getProgramParameter(i,e.ACTIVE_UNIFORMS);for(let l=0;l<s;++l){const c=e.getActiveUniform(i,l),d=e.getUniformLocation(i,c.name);mb(c,d,this)}}setValue(e,i,s,l){const c=this.map[i];c!==void 0&&c.setValue(e,s,l)}setOptional(e,i,s){const l=i[s];l!==void 0&&this.setValue(e,s,l)}static upload(e,i,s,l){for(let c=0,d=i.length;c!==d;++c){const h=i[c],m=s[h.id];m.needsUpdate!==!1&&h.setValue(e,m.value,l)}}static seqWithValue(e,i){const s=[];for(let l=0,c=e.length;l!==c;++l){const d=e[l];d.id in i&&s.push(d)}return s}}function F_(o,e,i){const s=o.createShader(e);return o.shaderSource(s,i),o.compileShader(s),s}const gb=37297;let _b=0;function vb(o,e){const i=o.split(`
`),s=[],l=Math.max(e-6,0),c=Math.min(e+6,i.length);for(let d=l;d<c;d++){const h=d+1;s.push(`${h===e?">":" "} ${h}: ${i[d]}`)}return s.join(`
`)}function Sb(o){const e=Ue.getPrimaries(Ue.workingColorSpace),i=Ue.getPrimaries(o);let s;switch(e===i?s="":e===gu&&i===mu?s="LinearDisplayP3ToLinearSRGB":e===mu&&i===gu&&(s="LinearSRGBToLinearDisplayP3"),o){case Ji:case Mu:return[s,"LinearTransferOETF"];case vn:case Ch:return[s,"sRGBTransferOETF"];default:return console.warn("THREE.WebGLProgram: Unsupported color space:",o),[s,"LinearTransferOETF"]}}function H_(o,e,i){const s=o.getShaderParameter(e,o.COMPILE_STATUS),l=o.getShaderInfoLog(e).trim();if(s&&l==="")return"";const c=/ERROR: 0:(\d+)/.exec(l);if(c){const d=parseInt(c[1]);return i.toUpperCase()+`

`+l+`

`+vb(o.getShaderSource(e),d)}else return l}function Mb(o,e){const i=Sb(e);return`vec4 ${o}( vec4 value ) { return ${i[0]}( ${i[1]}( value ) ); }`}function xb(o,e){let i;switch(e){case LM:i="Linear";break;case UM:i="Reinhard";break;case NM:i="OptimizedCineon";break;case OM:i="ACESFilmic";break;case PM:i="AgX";break;case zM:i="Custom";break;default:console.warn("THREE.WebGLProgram: Unsupported toneMapping:",e),i="Linear"}return"vec3 "+o+"( vec3 color ) { return "+i+"ToneMapping( color ); }"}function yb(o){return[o.extensionDerivatives||o.envMapCubeUVHeight||o.bumpMap||o.normalMapTangentSpace||o.clearcoatNormalMap||o.flatShading||o.shaderID==="physical"?"#extension GL_OES_standard_derivatives : enable":"",(o.extensionFragDepth||o.logarithmicDepthBuffer)&&o.rendererExtensionFragDepth?"#extension GL_EXT_frag_depth : enable":"",o.extensionDrawBuffers&&o.rendererExtensionDrawBuffers?"#extension GL_EXT_draw_buffers : require":"",(o.extensionShaderTextureLOD||o.envMap||o.transmission)&&o.rendererExtensionShaderTextureLod?"#extension GL_EXT_shader_texture_lod : enable":""].filter(hs).join(`
`)}function Eb(o){return[o.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":""].filter(hs).join(`
`)}function Tb(o){const e=[];for(const i in o){const s=o[i];s!==!1&&e.push("#define "+i+" "+s)}return e.join(`
`)}function bb(o,e){const i={},s=o.getProgramParameter(e,o.ACTIVE_ATTRIBUTES);for(let l=0;l<s;l++){const c=o.getActiveAttrib(e,l),d=c.name;let h=1;c.type===o.FLOAT_MAT2&&(h=2),c.type===o.FLOAT_MAT3&&(h=3),c.type===o.FLOAT_MAT4&&(h=4),i[d]={type:c.type,location:o.getAttribLocation(e,d),locationSize:h}}return i}function hs(o){return o!==""}function G_(o,e){const i=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return o.replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,i).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function V_(o,e){return o.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}const Ab=/^[ \t]*#include +<([\w\d./]+)>/gm;function bh(o){return o.replace(Ab,Cb)}const Rb=new Map([["encodings_fragment","colorspace_fragment"],["encodings_pars_fragment","colorspace_pars_fragment"],["output_fragment","opaque_fragment"]]);function Cb(o,e){let i=oe[e];if(i===void 0){const s=Rb.get(e);if(s!==void 0)i=oe[s],console.warn('THREE.WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,s);else throw new Error("Can not resolve #include <"+e+">")}return bh(i)}const wb=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function X_(o){return o.replace(wb,Db)}function Db(o,e,i,s){let l="";for(let c=parseInt(e);c<parseInt(i);c++)l+=s.replace(/\[\s*i\s*\]/g,"[ "+c+" ]").replace(/UNROLLED_LOOP_INDEX/g,c);return l}function W_(o){let e="precision "+o.precision+` float;
precision `+o.precision+" int;";return o.precision==="highp"?e+=`
#define HIGH_PRECISION`:o.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:o.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}function Lb(o){let e="SHADOWMAP_TYPE_BASIC";return o.shadowMapType===ev?e="SHADOWMAP_TYPE_PCF":o.shadowMapType===rM?e="SHADOWMAP_TYPE_PCF_SOFT":o.shadowMapType===Zi&&(e="SHADOWMAP_TYPE_VSM"),e}function Ub(o){let e="ENVMAP_TYPE_CUBE";if(o.envMap)switch(o.envMapMode){case ms:case gs:e="ENVMAP_TYPE_CUBE";break;case Su:e="ENVMAP_TYPE_CUBE_UV";break}return e}function Nb(o){let e="ENVMAP_MODE_REFLECTION";return o.envMap&&o.envMapMode===gs&&(e="ENVMAP_MODE_REFRACTION"),e}function Ob(o){let e="ENVMAP_BLENDING_NONE";if(o.envMap)switch(o.combine){case nv:e="ENVMAP_BLENDING_MULTIPLY";break;case wM:e="ENVMAP_BLENDING_MIX";break;case DM:e="ENVMAP_BLENDING_ADD";break}return e}function zb(o){const e=o.envMapCubeUVHeight;if(e===null)return null;const i=Math.log2(e)-2,s=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,i),112)),texelHeight:s,maxMip:i}}function Pb(o,e,i,s){const l=o.getContext(),c=i.defines;let d=i.vertexShader,h=i.fragmentShader;const m=Lb(i),p=Ub(i),g=Nb(i),_=Ob(i),M=zb(i),y=i.isWebGL2?"":yb(i),b=Eb(i),T=Tb(c),x=l.createProgram();let v,N,R=i.glslVersion?"#version "+i.glslVersion+`
`:"";i.isRawShaderMaterial?(v=["#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,T].filter(hs).join(`
`),v.length>0&&(v+=`
`),N=[y,"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,T].filter(hs).join(`
`),N.length>0&&(N+=`
`)):(v=[W_(i),"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,T,i.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",i.batching?"#define USE_BATCHING":"",i.instancing?"#define USE_INSTANCING":"",i.instancingColor?"#define USE_INSTANCING_COLOR":"",i.useFog&&i.fog?"#define USE_FOG":"",i.useFog&&i.fogExp2?"#define FOG_EXP2":"",i.map?"#define USE_MAP":"",i.envMap?"#define USE_ENVMAP":"",i.envMap?"#define "+g:"",i.lightMap?"#define USE_LIGHTMAP":"",i.aoMap?"#define USE_AOMAP":"",i.bumpMap?"#define USE_BUMPMAP":"",i.normalMap?"#define USE_NORMALMAP":"",i.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",i.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",i.displacementMap?"#define USE_DISPLACEMENTMAP":"",i.emissiveMap?"#define USE_EMISSIVEMAP":"",i.anisotropy?"#define USE_ANISOTROPY":"",i.anisotropyMap?"#define USE_ANISOTROPYMAP":"",i.clearcoatMap?"#define USE_CLEARCOATMAP":"",i.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",i.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",i.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",i.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",i.specularMap?"#define USE_SPECULARMAP":"",i.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",i.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",i.roughnessMap?"#define USE_ROUGHNESSMAP":"",i.metalnessMap?"#define USE_METALNESSMAP":"",i.alphaMap?"#define USE_ALPHAMAP":"",i.alphaHash?"#define USE_ALPHAHASH":"",i.transmission?"#define USE_TRANSMISSION":"",i.transmissionMap?"#define USE_TRANSMISSIONMAP":"",i.thicknessMap?"#define USE_THICKNESSMAP":"",i.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",i.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",i.mapUv?"#define MAP_UV "+i.mapUv:"",i.alphaMapUv?"#define ALPHAMAP_UV "+i.alphaMapUv:"",i.lightMapUv?"#define LIGHTMAP_UV "+i.lightMapUv:"",i.aoMapUv?"#define AOMAP_UV "+i.aoMapUv:"",i.emissiveMapUv?"#define EMISSIVEMAP_UV "+i.emissiveMapUv:"",i.bumpMapUv?"#define BUMPMAP_UV "+i.bumpMapUv:"",i.normalMapUv?"#define NORMALMAP_UV "+i.normalMapUv:"",i.displacementMapUv?"#define DISPLACEMENTMAP_UV "+i.displacementMapUv:"",i.metalnessMapUv?"#define METALNESSMAP_UV "+i.metalnessMapUv:"",i.roughnessMapUv?"#define ROUGHNESSMAP_UV "+i.roughnessMapUv:"",i.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+i.anisotropyMapUv:"",i.clearcoatMapUv?"#define CLEARCOATMAP_UV "+i.clearcoatMapUv:"",i.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+i.clearcoatNormalMapUv:"",i.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+i.clearcoatRoughnessMapUv:"",i.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+i.iridescenceMapUv:"",i.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+i.iridescenceThicknessMapUv:"",i.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+i.sheenColorMapUv:"",i.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+i.sheenRoughnessMapUv:"",i.specularMapUv?"#define SPECULARMAP_UV "+i.specularMapUv:"",i.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+i.specularColorMapUv:"",i.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+i.specularIntensityMapUv:"",i.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+i.transmissionMapUv:"",i.thicknessMapUv?"#define THICKNESSMAP_UV "+i.thicknessMapUv:"",i.vertexTangents&&i.flatShading===!1?"#define USE_TANGENT":"",i.vertexColors?"#define USE_COLOR":"",i.vertexAlphas?"#define USE_COLOR_ALPHA":"",i.vertexUv1s?"#define USE_UV1":"",i.vertexUv2s?"#define USE_UV2":"",i.vertexUv3s?"#define USE_UV3":"",i.pointsUvs?"#define USE_POINTS_UV":"",i.flatShading?"#define FLAT_SHADED":"",i.skinning?"#define USE_SKINNING":"",i.morphTargets?"#define USE_MORPHTARGETS":"",i.morphNormals&&i.flatShading===!1?"#define USE_MORPHNORMALS":"",i.morphColors&&i.isWebGL2?"#define USE_MORPHCOLORS":"",i.morphTargetsCount>0&&i.isWebGL2?"#define MORPHTARGETS_TEXTURE":"",i.morphTargetsCount>0&&i.isWebGL2?"#define MORPHTARGETS_TEXTURE_STRIDE "+i.morphTextureStride:"",i.morphTargetsCount>0&&i.isWebGL2?"#define MORPHTARGETS_COUNT "+i.morphTargetsCount:"",i.doubleSided?"#define DOUBLE_SIDED":"",i.flipSided?"#define FLIP_SIDED":"",i.shadowMapEnabled?"#define USE_SHADOWMAP":"",i.shadowMapEnabled?"#define "+m:"",i.sizeAttenuation?"#define USE_SIZEATTENUATION":"",i.numLightProbes>0?"#define USE_LIGHT_PROBES":"",i.useLegacyLights?"#define LEGACY_LIGHTS":"",i.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",i.logarithmicDepthBuffer&&i.rendererExtensionFragDepth?"#define USE_LOGDEPTHBUF_EXT":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#if ( defined( USE_MORPHTARGETS ) && ! defined( MORPHTARGETS_TEXTURE ) )","	attribute vec3 morphTarget0;","	attribute vec3 morphTarget1;","	attribute vec3 morphTarget2;","	attribute vec3 morphTarget3;","	#ifdef USE_MORPHNORMALS","		attribute vec3 morphNormal0;","		attribute vec3 morphNormal1;","		attribute vec3 morphNormal2;","		attribute vec3 morphNormal3;","	#else","		attribute vec3 morphTarget4;","		attribute vec3 morphTarget5;","		attribute vec3 morphTarget6;","		attribute vec3 morphTarget7;","	#endif","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(hs).join(`
`),N=[y,W_(i),"#define SHADER_TYPE "+i.shaderType,"#define SHADER_NAME "+i.shaderName,T,i.useFog&&i.fog?"#define USE_FOG":"",i.useFog&&i.fogExp2?"#define FOG_EXP2":"",i.map?"#define USE_MAP":"",i.matcap?"#define USE_MATCAP":"",i.envMap?"#define USE_ENVMAP":"",i.envMap?"#define "+p:"",i.envMap?"#define "+g:"",i.envMap?"#define "+_:"",M?"#define CUBEUV_TEXEL_WIDTH "+M.texelWidth:"",M?"#define CUBEUV_TEXEL_HEIGHT "+M.texelHeight:"",M?"#define CUBEUV_MAX_MIP "+M.maxMip+".0":"",i.lightMap?"#define USE_LIGHTMAP":"",i.aoMap?"#define USE_AOMAP":"",i.bumpMap?"#define USE_BUMPMAP":"",i.normalMap?"#define USE_NORMALMAP":"",i.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",i.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",i.emissiveMap?"#define USE_EMISSIVEMAP":"",i.anisotropy?"#define USE_ANISOTROPY":"",i.anisotropyMap?"#define USE_ANISOTROPYMAP":"",i.clearcoat?"#define USE_CLEARCOAT":"",i.clearcoatMap?"#define USE_CLEARCOATMAP":"",i.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",i.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",i.iridescence?"#define USE_IRIDESCENCE":"",i.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",i.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",i.specularMap?"#define USE_SPECULARMAP":"",i.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",i.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",i.roughnessMap?"#define USE_ROUGHNESSMAP":"",i.metalnessMap?"#define USE_METALNESSMAP":"",i.alphaMap?"#define USE_ALPHAMAP":"",i.alphaTest?"#define USE_ALPHATEST":"",i.alphaHash?"#define USE_ALPHAHASH":"",i.sheen?"#define USE_SHEEN":"",i.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",i.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",i.transmission?"#define USE_TRANSMISSION":"",i.transmissionMap?"#define USE_TRANSMISSIONMAP":"",i.thicknessMap?"#define USE_THICKNESSMAP":"",i.vertexTangents&&i.flatShading===!1?"#define USE_TANGENT":"",i.vertexColors||i.instancingColor?"#define USE_COLOR":"",i.vertexAlphas?"#define USE_COLOR_ALPHA":"",i.vertexUv1s?"#define USE_UV1":"",i.vertexUv2s?"#define USE_UV2":"",i.vertexUv3s?"#define USE_UV3":"",i.pointsUvs?"#define USE_POINTS_UV":"",i.gradientMap?"#define USE_GRADIENTMAP":"",i.flatShading?"#define FLAT_SHADED":"",i.doubleSided?"#define DOUBLE_SIDED":"",i.flipSided?"#define FLIP_SIDED":"",i.shadowMapEnabled?"#define USE_SHADOWMAP":"",i.shadowMapEnabled?"#define "+m:"",i.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",i.numLightProbes>0?"#define USE_LIGHT_PROBES":"",i.useLegacyLights?"#define LEGACY_LIGHTS":"",i.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",i.logarithmicDepthBuffer?"#define USE_LOGDEPTHBUF":"",i.logarithmicDepthBuffer&&i.rendererExtensionFragDepth?"#define USE_LOGDEPTHBUF_EXT":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",i.toneMapping!==Pa?"#define TONE_MAPPING":"",i.toneMapping!==Pa?oe.tonemapping_pars_fragment:"",i.toneMapping!==Pa?xb("toneMapping",i.toneMapping):"",i.dithering?"#define DITHERING":"",i.opaque?"#define OPAQUE":"",oe.colorspace_pars_fragment,Mb("linearToOutputTexel",i.outputColorSpace),i.useDepthPacking?"#define DEPTH_PACKING "+i.depthPacking:"",`
`].filter(hs).join(`
`)),d=bh(d),d=G_(d,i),d=V_(d,i),h=bh(h),h=G_(h,i),h=V_(h,i),d=X_(d),h=X_(h),i.isWebGL2&&i.isRawShaderMaterial!==!0&&(R=`#version 300 es
`,v=[b,"precision mediump sampler2DArray;","#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+v,N=["precision mediump sampler2DArray;","#define varying in",i.glslVersion===l_?"":"layout(location = 0) out highp vec4 pc_fragColor;",i.glslVersion===l_?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+N);const I=R+v+d,q=R+N+h,B=F_(l,l.VERTEX_SHADER,I),z=F_(l,l.FRAGMENT_SHADER,q);l.attachShader(x,B),l.attachShader(x,z),i.index0AttributeName!==void 0?l.bindAttribLocation(x,0,i.index0AttributeName):i.morphTargets===!0&&l.bindAttribLocation(x,0,"position"),l.linkProgram(x);function dt(mt){if(o.debug.checkShaderErrors){const Et=l.getProgramInfoLog(x).trim(),V=l.getShaderInfoLog(B).trim(),$=l.getShaderInfoLog(z).trim();let O=!0,k=!0;if(l.getProgramParameter(x,l.LINK_STATUS)===!1)if(O=!1,typeof o.debug.onShaderError=="function")o.debug.onShaderError(l,x,B,z);else{const Q=H_(l,B,"vertex"),ot=H_(l,z,"fragment");console.error("THREE.WebGLProgram: Shader Error "+l.getError()+" - VALIDATE_STATUS "+l.getProgramParameter(x,l.VALIDATE_STATUS)+`

Program Info Log: `+Et+`
`+Q+`
`+ot)}else Et!==""?console.warn("THREE.WebGLProgram: Program Info Log:",Et):(V===""||$==="")&&(k=!1);k&&(mt.diagnostics={runnable:O,programLog:Et,vertexShader:{log:V,prefix:v},fragmentShader:{log:$,prefix:N}})}l.deleteShader(B),l.deleteShader(z),w=new hu(l,x),U=bb(l,x)}let w;this.getUniforms=function(){return w===void 0&&dt(this),w};let U;this.getAttributes=function(){return U===void 0&&dt(this),U};let lt=i.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return lt===!1&&(lt=l.getProgramParameter(x,gb)),lt},this.destroy=function(){s.releaseStatesOfProgram(this),l.deleteProgram(x),this.program=void 0},this.type=i.shaderType,this.name=i.shaderName,this.id=_b++,this.cacheKey=e,this.usedTimes=1,this.program=x,this.vertexShader=B,this.fragmentShader=z,this}let Bb=0;class Ib{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e){const i=e.vertexShader,s=e.fragmentShader,l=this._getShaderStage(i),c=this._getShaderStage(s),d=this._getShaderCacheForMaterial(e);return d.has(l)===!1&&(d.add(l),l.usedTimes++),d.has(c)===!1&&(d.add(c),c.usedTimes++),this}remove(e){const i=this.materialCache.get(e);for(const s of i)s.usedTimes--,s.usedTimes===0&&this.shaderCache.delete(s.code);return this.materialCache.delete(e),this}getVertexShaderID(e){return this._getShaderStage(e.vertexShader).id}getFragmentShaderID(e){return this._getShaderStage(e.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){const i=this.materialCache;let s=i.get(e);return s===void 0&&(s=new Set,i.set(e,s)),s}_getShaderStage(e){const i=this.shaderCache;let s=i.get(e);return s===void 0&&(s=new Fb(e),i.set(e,s)),s}}class Fb{constructor(e){this.id=Bb++,this.code=e,this.usedTimes=0}}function Hb(o,e,i,s,l,c,d){const h=new vv,m=new Ib,p=[],g=l.isWebGL2,_=l.logarithmicDepthBuffer,M=l.vertexTextures;let y=l.precision;const b={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distanceRGBA",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function T(w){return w===0?"uv":`uv${w}`}function x(w,U,lt,mt,Et){const V=mt.fog,$=Et.geometry,O=w.isMeshStandardMaterial?mt.environment:null,k=(w.isMeshStandardMaterial?i:e).get(w.envMap||O),Q=k&&k.mapping===Su?k.image.height:null,ot=b[w.type];w.precision!==null&&(y=l.getMaxPrecision(w.precision),y!==w.precision&&console.warn("THREE.WebGLProgram.getParameters:",w.precision,"not supported, using",y,"instead."));const ct=$.morphAttributes.position||$.morphAttributes.normal||$.morphAttributes.color,D=ct!==void 0?ct.length:0;let X=0;$.morphAttributes.position!==void 0&&(X=1),$.morphAttributes.normal!==void 0&&(X=2),$.morphAttributes.color!==void 0&&(X=3);let G,Z,pt,Mt;if(ot){const ke=Ti[ot];G=ke.vertexShader,Z=ke.fragmentShader}else G=w.vertexShader,Z=w.fragmentShader,m.update(w),pt=m.getVertexShaderID(w),Mt=m.getFragmentShaderID(w);const xt=o.getRenderTarget(),It=Et.isInstancedMesh===!0,Nt=Et.isBatchedMesh===!0,kt=!!w.map,ue=!!w.matcap,tt=!!k,ln=!!w.aoMap,Ft=!!w.lightMap,Qt=!!w.bumpMap,Pt=!!w.normalMap,Pe=!!w.displacementMap,ee=!!w.emissiveMap,L=!!w.metalnessMap,A=!!w.roughnessMap,nt=w.anisotropy>0,St=w.clearcoat>0,vt=w.iridescence>0,gt=w.sheen>0,Ht=w.transmission>0,Rt=nt&&!!w.anisotropyMap,Ut=St&&!!w.clearcoatMap,qt=St&&!!w.clearcoatNormalMap,ie=St&&!!w.clearcoatRoughnessMap,_t=vt&&!!w.iridescenceMap,ye=vt&&!!w.iridescenceThicknessMap,le=gt&&!!w.sheenColorMap,Kt=gt&&!!w.sheenRoughnessMap,Dt=!!w.specularMap,wt=!!w.specularColorMap,Xt=!!w.specularIntensityMap,ve=Ht&&!!w.transmissionMap,He=Ht&&!!w.thicknessMap,re=!!w.gradientMap,yt=!!w.alphaMap,F=w.alphaTest>0,At=!!w.alphaHash,Tt=!!w.extensions,jt=!!$.attributes.uv1,Gt=!!$.attributes.uv2,Re=!!$.attributes.uv3;let Ee=Pa;return w.toneMapped&&(xt===null||xt.isXRRenderTarget===!0)&&(Ee=o.toneMapping),{isWebGL2:g,shaderID:ot,shaderType:w.type,shaderName:w.name,vertexShader:G,fragmentShader:Z,defines:w.defines,customVertexShaderID:pt,customFragmentShaderID:Mt,isRawShaderMaterial:w.isRawShaderMaterial===!0,glslVersion:w.glslVersion,precision:y,batching:Nt,instancing:It,instancingColor:It&&Et.instanceColor!==null,supportsVertexTextures:M,outputColorSpace:xt===null?o.outputColorSpace:xt.isXRRenderTarget===!0?xt.texture.colorSpace:Ji,map:kt,matcap:ue,envMap:tt,envMapMode:tt&&k.mapping,envMapCubeUVHeight:Q,aoMap:ln,lightMap:Ft,bumpMap:Qt,normalMap:Pt,displacementMap:M&&Pe,emissiveMap:ee,normalMapObjectSpace:Pt&&w.normalMapType===jM,normalMapTangentSpace:Pt&&w.normalMapType===hv,metalnessMap:L,roughnessMap:A,anisotropy:nt,anisotropyMap:Rt,clearcoat:St,clearcoatMap:Ut,clearcoatNormalMap:qt,clearcoatRoughnessMap:ie,iridescence:vt,iridescenceMap:_t,iridescenceThicknessMap:ye,sheen:gt,sheenColorMap:le,sheenRoughnessMap:Kt,specularMap:Dt,specularColorMap:wt,specularIntensityMap:Xt,transmission:Ht,transmissionMap:ve,thicknessMap:He,gradientMap:re,opaque:w.transparent===!1&&w.blending===ds,alphaMap:yt,alphaTest:F,alphaHash:At,combine:w.combine,mapUv:kt&&T(w.map.channel),aoMapUv:ln&&T(w.aoMap.channel),lightMapUv:Ft&&T(w.lightMap.channel),bumpMapUv:Qt&&T(w.bumpMap.channel),normalMapUv:Pt&&T(w.normalMap.channel),displacementMapUv:Pe&&T(w.displacementMap.channel),emissiveMapUv:ee&&T(w.emissiveMap.channel),metalnessMapUv:L&&T(w.metalnessMap.channel),roughnessMapUv:A&&T(w.roughnessMap.channel),anisotropyMapUv:Rt&&T(w.anisotropyMap.channel),clearcoatMapUv:Ut&&T(w.clearcoatMap.channel),clearcoatNormalMapUv:qt&&T(w.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:ie&&T(w.clearcoatRoughnessMap.channel),iridescenceMapUv:_t&&T(w.iridescenceMap.channel),iridescenceThicknessMapUv:ye&&T(w.iridescenceThicknessMap.channel),sheenColorMapUv:le&&T(w.sheenColorMap.channel),sheenRoughnessMapUv:Kt&&T(w.sheenRoughnessMap.channel),specularMapUv:Dt&&T(w.specularMap.channel),specularColorMapUv:wt&&T(w.specularColorMap.channel),specularIntensityMapUv:Xt&&T(w.specularIntensityMap.channel),transmissionMapUv:ve&&T(w.transmissionMap.channel),thicknessMapUv:He&&T(w.thicknessMap.channel),alphaMapUv:yt&&T(w.alphaMap.channel),vertexTangents:!!$.attributes.tangent&&(Pt||nt),vertexColors:w.vertexColors,vertexAlphas:w.vertexColors===!0&&!!$.attributes.color&&$.attributes.color.itemSize===4,vertexUv1s:jt,vertexUv2s:Gt,vertexUv3s:Re,pointsUvs:Et.isPoints===!0&&!!$.attributes.uv&&(kt||yt),fog:!!V,useFog:w.fog===!0,fogExp2:V&&V.isFogExp2,flatShading:w.flatShading===!0,sizeAttenuation:w.sizeAttenuation===!0,logarithmicDepthBuffer:_,skinning:Et.isSkinnedMesh===!0,morphTargets:$.morphAttributes.position!==void 0,morphNormals:$.morphAttributes.normal!==void 0,morphColors:$.morphAttributes.color!==void 0,morphTargetsCount:D,morphTextureStride:X,numDirLights:U.directional.length,numPointLights:U.point.length,numSpotLights:U.spot.length,numSpotLightMaps:U.spotLightMap.length,numRectAreaLights:U.rectArea.length,numHemiLights:U.hemi.length,numDirLightShadows:U.directionalShadowMap.length,numPointLightShadows:U.pointShadowMap.length,numSpotLightShadows:U.spotShadowMap.length,numSpotLightShadowsWithMaps:U.numSpotLightShadowsWithMaps,numLightProbes:U.numLightProbes,numClippingPlanes:d.numPlanes,numClipIntersection:d.numIntersection,dithering:w.dithering,shadowMapEnabled:o.shadowMap.enabled&&lt.length>0,shadowMapType:o.shadowMap.type,toneMapping:Ee,useLegacyLights:o._useLegacyLights,decodeVideoTexture:kt&&w.map.isVideoTexture===!0&&Ue.getTransfer(w.map.colorSpace)===Fe,premultipliedAlpha:w.premultipliedAlpha,doubleSided:w.side===Ki,flipSided:w.side===In,useDepthPacking:w.depthPacking>=0,depthPacking:w.depthPacking||0,index0AttributeName:w.index0AttributeName,extensionDerivatives:Tt&&w.extensions.derivatives===!0,extensionFragDepth:Tt&&w.extensions.fragDepth===!0,extensionDrawBuffers:Tt&&w.extensions.drawBuffers===!0,extensionShaderTextureLOD:Tt&&w.extensions.shaderTextureLOD===!0,extensionClipCullDistance:Tt&&w.extensions.clipCullDistance&&s.has("WEBGL_clip_cull_distance"),rendererExtensionFragDepth:g||s.has("EXT_frag_depth"),rendererExtensionDrawBuffers:g||s.has("WEBGL_draw_buffers"),rendererExtensionShaderTextureLod:g||s.has("EXT_shader_texture_lod"),rendererExtensionParallelShaderCompile:s.has("KHR_parallel_shader_compile"),customProgramCacheKey:w.customProgramCacheKey()}}function v(w){const U=[];if(w.shaderID?U.push(w.shaderID):(U.push(w.customVertexShaderID),U.push(w.customFragmentShaderID)),w.defines!==void 0)for(const lt in w.defines)U.push(lt),U.push(w.defines[lt]);return w.isRawShaderMaterial===!1&&(N(U,w),R(U,w),U.push(o.outputColorSpace)),U.push(w.customProgramCacheKey),U.join()}function N(w,U){w.push(U.precision),w.push(U.outputColorSpace),w.push(U.envMapMode),w.push(U.envMapCubeUVHeight),w.push(U.mapUv),w.push(U.alphaMapUv),w.push(U.lightMapUv),w.push(U.aoMapUv),w.push(U.bumpMapUv),w.push(U.normalMapUv),w.push(U.displacementMapUv),w.push(U.emissiveMapUv),w.push(U.metalnessMapUv),w.push(U.roughnessMapUv),w.push(U.anisotropyMapUv),w.push(U.clearcoatMapUv),w.push(U.clearcoatNormalMapUv),w.push(U.clearcoatRoughnessMapUv),w.push(U.iridescenceMapUv),w.push(U.iridescenceThicknessMapUv),w.push(U.sheenColorMapUv),w.push(U.sheenRoughnessMapUv),w.push(U.specularMapUv),w.push(U.specularColorMapUv),w.push(U.specularIntensityMapUv),w.push(U.transmissionMapUv),w.push(U.thicknessMapUv),w.push(U.combine),w.push(U.fogExp2),w.push(U.sizeAttenuation),w.push(U.morphTargetsCount),w.push(U.morphAttributeCount),w.push(U.numDirLights),w.push(U.numPointLights),w.push(U.numSpotLights),w.push(U.numSpotLightMaps),w.push(U.numHemiLights),w.push(U.numRectAreaLights),w.push(U.numDirLightShadows),w.push(U.numPointLightShadows),w.push(U.numSpotLightShadows),w.push(U.numSpotLightShadowsWithMaps),w.push(U.numLightProbes),w.push(U.shadowMapType),w.push(U.toneMapping),w.push(U.numClippingPlanes),w.push(U.numClipIntersection),w.push(U.depthPacking)}function R(w,U){h.disableAll(),U.isWebGL2&&h.enable(0),U.supportsVertexTextures&&h.enable(1),U.instancing&&h.enable(2),U.instancingColor&&h.enable(3),U.matcap&&h.enable(4),U.envMap&&h.enable(5),U.normalMapObjectSpace&&h.enable(6),U.normalMapTangentSpace&&h.enable(7),U.clearcoat&&h.enable(8),U.iridescence&&h.enable(9),U.alphaTest&&h.enable(10),U.vertexColors&&h.enable(11),U.vertexAlphas&&h.enable(12),U.vertexUv1s&&h.enable(13),U.vertexUv2s&&h.enable(14),U.vertexUv3s&&h.enable(15),U.vertexTangents&&h.enable(16),U.anisotropy&&h.enable(17),U.alphaHash&&h.enable(18),U.batching&&h.enable(19),w.push(h.mask),h.disableAll(),U.fog&&h.enable(0),U.useFog&&h.enable(1),U.flatShading&&h.enable(2),U.logarithmicDepthBuffer&&h.enable(3),U.skinning&&h.enable(4),U.morphTargets&&h.enable(5),U.morphNormals&&h.enable(6),U.morphColors&&h.enable(7),U.premultipliedAlpha&&h.enable(8),U.shadowMapEnabled&&h.enable(9),U.useLegacyLights&&h.enable(10),U.doubleSided&&h.enable(11),U.flipSided&&h.enable(12),U.useDepthPacking&&h.enable(13),U.dithering&&h.enable(14),U.transmission&&h.enable(15),U.sheen&&h.enable(16),U.opaque&&h.enable(17),U.pointsUvs&&h.enable(18),U.decodeVideoTexture&&h.enable(19),w.push(h.mask)}function I(w){const U=b[w.type];let lt;if(U){const mt=Ti[U];lt=yx.clone(mt.uniforms)}else lt=w.uniforms;return lt}function q(w,U){let lt;for(let mt=0,Et=p.length;mt<Et;mt++){const V=p[mt];if(V.cacheKey===U){lt=V,++lt.usedTimes;break}}return lt===void 0&&(lt=new Pb(o,U,w,c),p.push(lt)),lt}function B(w){if(--w.usedTimes===0){const U=p.indexOf(w);p[U]=p[p.length-1],p.pop(),w.destroy()}}function z(w){m.remove(w)}function dt(){m.dispose()}return{getParameters:x,getProgramCacheKey:v,getUniforms:I,acquireProgram:q,releaseProgram:B,releaseShaderCache:z,programs:p,dispose:dt}}function Gb(){let o=new WeakMap;function e(c){let d=o.get(c);return d===void 0&&(d={},o.set(c,d)),d}function i(c){o.delete(c)}function s(c,d,h){o.get(c)[d]=h}function l(){o=new WeakMap}return{get:e,remove:i,update:s,dispose:l}}function Vb(o,e){return o.groupOrder!==e.groupOrder?o.groupOrder-e.groupOrder:o.renderOrder!==e.renderOrder?o.renderOrder-e.renderOrder:o.material.id!==e.material.id?o.material.id-e.material.id:o.z!==e.z?o.z-e.z:o.id-e.id}function k_(o,e){return o.groupOrder!==e.groupOrder?o.groupOrder-e.groupOrder:o.renderOrder!==e.renderOrder?o.renderOrder-e.renderOrder:o.z!==e.z?e.z-o.z:o.id-e.id}function q_(){const o=[];let e=0;const i=[],s=[],l=[];function c(){e=0,i.length=0,s.length=0,l.length=0}function d(_,M,y,b,T,x){let v=o[e];return v===void 0?(v={id:_.id,object:_,geometry:M,material:y,groupOrder:b,renderOrder:_.renderOrder,z:T,group:x},o[e]=v):(v.id=_.id,v.object=_,v.geometry=M,v.material=y,v.groupOrder=b,v.renderOrder=_.renderOrder,v.z=T,v.group=x),e++,v}function h(_,M,y,b,T,x){const v=d(_,M,y,b,T,x);y.transmission>0?s.push(v):y.transparent===!0?l.push(v):i.push(v)}function m(_,M,y,b,T,x){const v=d(_,M,y,b,T,x);y.transmission>0?s.unshift(v):y.transparent===!0?l.unshift(v):i.unshift(v)}function p(_,M){i.length>1&&i.sort(_||Vb),s.length>1&&s.sort(M||k_),l.length>1&&l.sort(M||k_)}function g(){for(let _=e,M=o.length;_<M;_++){const y=o[_];if(y.id===null)break;y.id=null,y.object=null,y.geometry=null,y.material=null,y.group=null}}return{opaque:i,transmissive:s,transparent:l,init:c,push:h,unshift:m,finish:g,sort:p}}function Xb(){let o=new WeakMap;function e(s,l){const c=o.get(s);let d;return c===void 0?(d=new q_,o.set(s,[d])):l>=c.length?(d=new q_,c.push(d)):d=c[l],d}function i(){o=new WeakMap}return{get:e,dispose:i}}function Wb(){const o={};return{get:function(e){if(o[e.id]!==void 0)return o[e.id];let i;switch(e.type){case"DirectionalLight":i={direction:new at,color:new Me};break;case"SpotLight":i={position:new at,direction:new at,color:new Me,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":i={position:new at,color:new Me,distance:0,decay:0};break;case"HemisphereLight":i={direction:new at,skyColor:new Me,groundColor:new Me};break;case"RectAreaLight":i={color:new Me,position:new at,halfWidth:new at,halfHeight:new at};break}return o[e.id]=i,i}}}function kb(){const o={};return{get:function(e){if(o[e.id]!==void 0)return o[e.id];let i;switch(e.type){case"DirectionalLight":i={shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new xe};break;case"SpotLight":i={shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new xe};break;case"PointLight":i={shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new xe,shadowCameraNear:1,shadowCameraFar:1e3};break}return o[e.id]=i,i}}}let qb=0;function Yb(o,e){return(e.castShadow?2:0)-(o.castShadow?2:0)+(e.map?1:0)-(o.map?1:0)}function jb(o,e){const i=new Wb,s=kb(),l={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let g=0;g<9;g++)l.probe.push(new at);const c=new at,d=new rn,h=new rn;function m(g,_){let M=0,y=0,b=0;for(let mt=0;mt<9;mt++)l.probe[mt].set(0,0,0);let T=0,x=0,v=0,N=0,R=0,I=0,q=0,B=0,z=0,dt=0,w=0;g.sort(Yb);const U=_===!0?Math.PI:1;for(let mt=0,Et=g.length;mt<Et;mt++){const V=g[mt],$=V.color,O=V.intensity,k=V.distance,Q=V.shadow&&V.shadow.map?V.shadow.map.texture:null;if(V.isAmbientLight)M+=$.r*O*U,y+=$.g*O*U,b+=$.b*O*U;else if(V.isLightProbe){for(let ot=0;ot<9;ot++)l.probe[ot].addScaledVector(V.sh.coefficients[ot],O);w++}else if(V.isDirectionalLight){const ot=i.get(V);if(ot.color.copy(V.color).multiplyScalar(V.intensity*U),V.castShadow){const ct=V.shadow,D=s.get(V);D.shadowBias=ct.bias,D.shadowNormalBias=ct.normalBias,D.shadowRadius=ct.radius,D.shadowMapSize=ct.mapSize,l.directionalShadow[T]=D,l.directionalShadowMap[T]=Q,l.directionalShadowMatrix[T]=V.shadow.matrix,I++}l.directional[T]=ot,T++}else if(V.isSpotLight){const ot=i.get(V);ot.position.setFromMatrixPosition(V.matrixWorld),ot.color.copy($).multiplyScalar(O*U),ot.distance=k,ot.coneCos=Math.cos(V.angle),ot.penumbraCos=Math.cos(V.angle*(1-V.penumbra)),ot.decay=V.decay,l.spot[v]=ot;const ct=V.shadow;if(V.map&&(l.spotLightMap[z]=V.map,z++,ct.updateMatrices(V),V.castShadow&&dt++),l.spotLightMatrix[v]=ct.matrix,V.castShadow){const D=s.get(V);D.shadowBias=ct.bias,D.shadowNormalBias=ct.normalBias,D.shadowRadius=ct.radius,D.shadowMapSize=ct.mapSize,l.spotShadow[v]=D,l.spotShadowMap[v]=Q,B++}v++}else if(V.isRectAreaLight){const ot=i.get(V);ot.color.copy($).multiplyScalar(O),ot.halfWidth.set(V.width*.5,0,0),ot.halfHeight.set(0,V.height*.5,0),l.rectArea[N]=ot,N++}else if(V.isPointLight){const ot=i.get(V);if(ot.color.copy(V.color).multiplyScalar(V.intensity*U),ot.distance=V.distance,ot.decay=V.decay,V.castShadow){const ct=V.shadow,D=s.get(V);D.shadowBias=ct.bias,D.shadowNormalBias=ct.normalBias,D.shadowRadius=ct.radius,D.shadowMapSize=ct.mapSize,D.shadowCameraNear=ct.camera.near,D.shadowCameraFar=ct.camera.far,l.pointShadow[x]=D,l.pointShadowMap[x]=Q,l.pointShadowMatrix[x]=V.shadow.matrix,q++}l.point[x]=ot,x++}else if(V.isHemisphereLight){const ot=i.get(V);ot.skyColor.copy(V.color).multiplyScalar(O*U),ot.groundColor.copy(V.groundColor).multiplyScalar(O*U),l.hemi[R]=ot,R++}}N>0&&(e.isWebGL2?o.has("OES_texture_float_linear")===!0?(l.rectAreaLTC1=bt.LTC_FLOAT_1,l.rectAreaLTC2=bt.LTC_FLOAT_2):(l.rectAreaLTC1=bt.LTC_HALF_1,l.rectAreaLTC2=bt.LTC_HALF_2):o.has("OES_texture_float_linear")===!0?(l.rectAreaLTC1=bt.LTC_FLOAT_1,l.rectAreaLTC2=bt.LTC_FLOAT_2):o.has("OES_texture_half_float_linear")===!0?(l.rectAreaLTC1=bt.LTC_HALF_1,l.rectAreaLTC2=bt.LTC_HALF_2):console.error("THREE.WebGLRenderer: Unable to use RectAreaLight. Missing WebGL extensions.")),l.ambient[0]=M,l.ambient[1]=y,l.ambient[2]=b;const lt=l.hash;(lt.directionalLength!==T||lt.pointLength!==x||lt.spotLength!==v||lt.rectAreaLength!==N||lt.hemiLength!==R||lt.numDirectionalShadows!==I||lt.numPointShadows!==q||lt.numSpotShadows!==B||lt.numSpotMaps!==z||lt.numLightProbes!==w)&&(l.directional.length=T,l.spot.length=v,l.rectArea.length=N,l.point.length=x,l.hemi.length=R,l.directionalShadow.length=I,l.directionalShadowMap.length=I,l.pointShadow.length=q,l.pointShadowMap.length=q,l.spotShadow.length=B,l.spotShadowMap.length=B,l.directionalShadowMatrix.length=I,l.pointShadowMatrix.length=q,l.spotLightMatrix.length=B+z-dt,l.spotLightMap.length=z,l.numSpotLightShadowsWithMaps=dt,l.numLightProbes=w,lt.directionalLength=T,lt.pointLength=x,lt.spotLength=v,lt.rectAreaLength=N,lt.hemiLength=R,lt.numDirectionalShadows=I,lt.numPointShadows=q,lt.numSpotShadows=B,lt.numSpotMaps=z,lt.numLightProbes=w,l.version=qb++)}function p(g,_){let M=0,y=0,b=0,T=0,x=0;const v=_.matrixWorldInverse;for(let N=0,R=g.length;N<R;N++){const I=g[N];if(I.isDirectionalLight){const q=l.directional[M];q.direction.setFromMatrixPosition(I.matrixWorld),c.setFromMatrixPosition(I.target.matrixWorld),q.direction.sub(c),q.direction.transformDirection(v),M++}else if(I.isSpotLight){const q=l.spot[b];q.position.setFromMatrixPosition(I.matrixWorld),q.position.applyMatrix4(v),q.direction.setFromMatrixPosition(I.matrixWorld),c.setFromMatrixPosition(I.target.matrixWorld),q.direction.sub(c),q.direction.transformDirection(v),b++}else if(I.isRectAreaLight){const q=l.rectArea[T];q.position.setFromMatrixPosition(I.matrixWorld),q.position.applyMatrix4(v),h.identity(),d.copy(I.matrixWorld),d.premultiply(v),h.extractRotation(d),q.halfWidth.set(I.width*.5,0,0),q.halfHeight.set(0,I.height*.5,0),q.halfWidth.applyMatrix4(h),q.halfHeight.applyMatrix4(h),T++}else if(I.isPointLight){const q=l.point[y];q.position.setFromMatrixPosition(I.matrixWorld),q.position.applyMatrix4(v),y++}else if(I.isHemisphereLight){const q=l.hemi[x];q.direction.setFromMatrixPosition(I.matrixWorld),q.direction.transformDirection(v),x++}}}return{setup:m,setupView:p,state:l}}function Y_(o,e){const i=new jb(o,e),s=[],l=[];function c(){s.length=0,l.length=0}function d(_){s.push(_)}function h(_){l.push(_)}function m(_){i.setup(s,_)}function p(_){i.setupView(s,_)}return{init:c,state:{lightsArray:s,shadowsArray:l,lights:i},setupLights:m,setupLightsView:p,pushLight:d,pushShadow:h}}function Zb(o,e){let i=new WeakMap;function s(c,d=0){const h=i.get(c);let m;return h===void 0?(m=new Y_(o,e),i.set(c,[m])):d>=h.length?(m=new Y_(o,e),h.push(m)):m=h[d],m}function l(){i=new WeakMap}return{get:s,dispose:l}}class Kb extends Lo{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=qM,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}}class Qb extends Lo{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}}const Jb=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,$b=`uniform sampler2D shadow_pass;
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
}`;function tA(o,e,i){let s=new Dh;const l=new xe,c=new xe,d=new hn,h=new Kb({depthPacking:YM}),m=new Qb,p={},g=i.maxTextureSize,_={[Ia]:In,[In]:Ia,[Ki]:Ki},M=new mr({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new xe},radius:{value:4}},vertexShader:Jb,fragmentShader:$b}),y=M.clone();y.defines.HORIZONTAL_PASS=1;const b=new Fa;b.setAttribute("position",new bi(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));const T=new Oa(b,M),x=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=ev;let v=this.type;this.render=function(B,z,dt){if(x.enabled===!1||x.autoUpdate===!1&&x.needsUpdate===!1||B.length===0)return;const w=o.getRenderTarget(),U=o.getActiveCubeFace(),lt=o.getActiveMipmapLevel(),mt=o.state;mt.setBlending(za),mt.buffers.color.setClear(1,1,1,1),mt.buffers.depth.setTest(!0),mt.setScissorTest(!1);const Et=v!==Zi&&this.type===Zi,V=v===Zi&&this.type!==Zi;for(let $=0,O=B.length;$<O;$++){const k=B[$],Q=k.shadow;if(Q===void 0){console.warn("THREE.WebGLShadowMap:",k,"has no shadow.");continue}if(Q.autoUpdate===!1&&Q.needsUpdate===!1)continue;l.copy(Q.mapSize);const ot=Q.getFrameExtents();if(l.multiply(ot),c.copy(Q.mapSize),(l.x>g||l.y>g)&&(l.x>g&&(c.x=Math.floor(g/ot.x),l.x=c.x*ot.x,Q.mapSize.x=c.x),l.y>g&&(c.y=Math.floor(g/ot.y),l.y=c.y*ot.y,Q.mapSize.y=c.y)),Q.map===null||Et===!0||V===!0){const D=this.type!==Zi?{minFilter:Cn,magFilter:Cn}:{};Q.map!==null&&Q.map.dispose(),Q.map=new pr(l.x,l.y,D),Q.map.texture.name=k.name+".shadowMap",Q.camera.updateProjectionMatrix()}o.setRenderTarget(Q.map),o.clear();const ct=Q.getViewportCount();for(let D=0;D<ct;D++){const X=Q.getViewport(D);d.set(c.x*X.x,c.y*X.y,c.x*X.z,c.y*X.w),mt.viewport(d),Q.updateMatrices(k,D),s=Q.getFrustum(),I(z,dt,Q.camera,k,this.type)}Q.isPointLightShadow!==!0&&this.type===Zi&&N(Q,dt),Q.needsUpdate=!1}v=this.type,x.needsUpdate=!1,o.setRenderTarget(w,U,lt)};function N(B,z){const dt=e.update(T);M.defines.VSM_SAMPLES!==B.blurSamples&&(M.defines.VSM_SAMPLES=B.blurSamples,y.defines.VSM_SAMPLES=B.blurSamples,M.needsUpdate=!0,y.needsUpdate=!0),B.mapPass===null&&(B.mapPass=new pr(l.x,l.y)),M.uniforms.shadow_pass.value=B.map.texture,M.uniforms.resolution.value=B.mapSize,M.uniforms.radius.value=B.radius,o.setRenderTarget(B.mapPass),o.clear(),o.renderBufferDirect(z,null,dt,M,T,null),y.uniforms.shadow_pass.value=B.mapPass.texture,y.uniforms.resolution.value=B.mapSize,y.uniforms.radius.value=B.radius,o.setRenderTarget(B.map),o.clear(),o.renderBufferDirect(z,null,dt,y,T,null)}function R(B,z,dt,w){let U=null;const lt=dt.isPointLight===!0?B.customDistanceMaterial:B.customDepthMaterial;if(lt!==void 0)U=lt;else if(U=dt.isPointLight===!0?m:h,o.localClippingEnabled&&z.clipShadows===!0&&Array.isArray(z.clippingPlanes)&&z.clippingPlanes.length!==0||z.displacementMap&&z.displacementScale!==0||z.alphaMap&&z.alphaTest>0||z.map&&z.alphaTest>0){const mt=U.uuid,Et=z.uuid;let V=p[mt];V===void 0&&(V={},p[mt]=V);let $=V[Et];$===void 0&&($=U.clone(),V[Et]=$,z.addEventListener("dispose",q)),U=$}if(U.visible=z.visible,U.wireframe=z.wireframe,w===Zi?U.side=z.shadowSide!==null?z.shadowSide:z.side:U.side=z.shadowSide!==null?z.shadowSide:_[z.side],U.alphaMap=z.alphaMap,U.alphaTest=z.alphaTest,U.map=z.map,U.clipShadows=z.clipShadows,U.clippingPlanes=z.clippingPlanes,U.clipIntersection=z.clipIntersection,U.displacementMap=z.displacementMap,U.displacementScale=z.displacementScale,U.displacementBias=z.displacementBias,U.wireframeLinewidth=z.wireframeLinewidth,U.linewidth=z.linewidth,dt.isPointLight===!0&&U.isMeshDistanceMaterial===!0){const mt=o.properties.get(U);mt.light=dt}return U}function I(B,z,dt,w,U){if(B.visible===!1)return;if(B.layers.test(z.layers)&&(B.isMesh||B.isLine||B.isPoints)&&(B.castShadow||B.receiveShadow&&U===Zi)&&(!B.frustumCulled||s.intersectsObject(B))){B.modelViewMatrix.multiplyMatrices(dt.matrixWorldInverse,B.matrixWorld);const Et=e.update(B),V=B.material;if(Array.isArray(V)){const $=Et.groups;for(let O=0,k=$.length;O<k;O++){const Q=$[O],ot=V[Q.materialIndex];if(ot&&ot.visible){const ct=R(B,ot,w,U);B.onBeforeShadow(o,B,z,dt,Et,ct,Q),o.renderBufferDirect(dt,null,Et,ct,B,Q),B.onAfterShadow(o,B,z,dt,Et,ct,Q)}}}else if(V.visible){const $=R(B,V,w,U);B.onBeforeShadow(o,B,z,dt,Et,$,null),o.renderBufferDirect(dt,null,Et,$,B,null),B.onAfterShadow(o,B,z,dt,Et,$,null)}}const mt=B.children;for(let Et=0,V=mt.length;Et<V;Et++)I(mt[Et],z,dt,w,U)}function q(B){B.target.removeEventListener("dispose",q);for(const dt in p){const w=p[dt],U=B.target.uuid;U in w&&(w[U].dispose(),delete w[U])}}}function eA(o,e,i){const s=i.isWebGL2;function l(){let F=!1;const At=new hn;let Tt=null;const jt=new hn(0,0,0,0);return{setMask:function(Gt){Tt!==Gt&&!F&&(o.colorMask(Gt,Gt,Gt,Gt),Tt=Gt)},setLocked:function(Gt){F=Gt},setClear:function(Gt,Re,Ee,Ve,ke){ke===!0&&(Gt*=Ve,Re*=Ve,Ee*=Ve),At.set(Gt,Re,Ee,Ve),jt.equals(At)===!1&&(o.clearColor(Gt,Re,Ee,Ve),jt.copy(At))},reset:function(){F=!1,Tt=null,jt.set(-1,0,0,0)}}}function c(){let F=!1,At=null,Tt=null,jt=null;return{setTest:function(Gt){Gt?Nt(o.DEPTH_TEST):kt(o.DEPTH_TEST)},setMask:function(Gt){At!==Gt&&!F&&(o.depthMask(Gt),At=Gt)},setFunc:function(Gt){if(Tt!==Gt){switch(Gt){case yM:o.depthFunc(o.NEVER);break;case EM:o.depthFunc(o.ALWAYS);break;case TM:o.depthFunc(o.LESS);break;case du:o.depthFunc(o.LEQUAL);break;case bM:o.depthFunc(o.EQUAL);break;case AM:o.depthFunc(o.GEQUAL);break;case RM:o.depthFunc(o.GREATER);break;case CM:o.depthFunc(o.NOTEQUAL);break;default:o.depthFunc(o.LEQUAL)}Tt=Gt}},setLocked:function(Gt){F=Gt},setClear:function(Gt){jt!==Gt&&(o.clearDepth(Gt),jt=Gt)},reset:function(){F=!1,At=null,Tt=null,jt=null}}}function d(){let F=!1,At=null,Tt=null,jt=null,Gt=null,Re=null,Ee=null,Ve=null,ke=null;return{setTest:function(Ce){F||(Ce?Nt(o.STENCIL_TEST):kt(o.STENCIL_TEST))},setMask:function(Ce){At!==Ce&&!F&&(o.stencilMask(Ce),At=Ce)},setFunc:function(Ce,un,Fn){(Tt!==Ce||jt!==un||Gt!==Fn)&&(o.stencilFunc(Ce,un,Fn),Tt=Ce,jt=un,Gt=Fn)},setOp:function(Ce,un,Fn){(Re!==Ce||Ee!==un||Ve!==Fn)&&(o.stencilOp(Ce,un,Fn),Re=Ce,Ee=un,Ve=Fn)},setLocked:function(Ce){F=Ce},setClear:function(Ce){ke!==Ce&&(o.clearStencil(Ce),ke=Ce)},reset:function(){F=!1,At=null,Tt=null,jt=null,Gt=null,Re=null,Ee=null,Ve=null,ke=null}}}const h=new l,m=new c,p=new d,g=new WeakMap,_=new WeakMap;let M={},y={},b=new WeakMap,T=[],x=null,v=!1,N=null,R=null,I=null,q=null,B=null,z=null,dt=null,w=new Me(0,0,0),U=0,lt=!1,mt=null,Et=null,V=null,$=null,O=null;const k=o.getParameter(o.MAX_COMBINED_TEXTURE_IMAGE_UNITS);let Q=!1,ot=0;const ct=o.getParameter(o.VERSION);ct.indexOf("WebGL")!==-1?(ot=parseFloat(/^WebGL (\d)/.exec(ct)[1]),Q=ot>=1):ct.indexOf("OpenGL ES")!==-1&&(ot=parseFloat(/^OpenGL ES (\d)/.exec(ct)[1]),Q=ot>=2);let D=null,X={};const G=o.getParameter(o.SCISSOR_BOX),Z=o.getParameter(o.VIEWPORT),pt=new hn().fromArray(G),Mt=new hn().fromArray(Z);function xt(F,At,Tt,jt){const Gt=new Uint8Array(4),Re=o.createTexture();o.bindTexture(F,Re),o.texParameteri(F,o.TEXTURE_MIN_FILTER,o.NEAREST),o.texParameteri(F,o.TEXTURE_MAG_FILTER,o.NEAREST);for(let Ee=0;Ee<Tt;Ee++)s&&(F===o.TEXTURE_3D||F===o.TEXTURE_2D_ARRAY)?o.texImage3D(At,0,o.RGBA,1,1,jt,0,o.RGBA,o.UNSIGNED_BYTE,Gt):o.texImage2D(At+Ee,0,o.RGBA,1,1,0,o.RGBA,o.UNSIGNED_BYTE,Gt);return Re}const It={};It[o.TEXTURE_2D]=xt(o.TEXTURE_2D,o.TEXTURE_2D,1),It[o.TEXTURE_CUBE_MAP]=xt(o.TEXTURE_CUBE_MAP,o.TEXTURE_CUBE_MAP_POSITIVE_X,6),s&&(It[o.TEXTURE_2D_ARRAY]=xt(o.TEXTURE_2D_ARRAY,o.TEXTURE_2D_ARRAY,1,1),It[o.TEXTURE_3D]=xt(o.TEXTURE_3D,o.TEXTURE_3D,1,1)),h.setClear(0,0,0,1),m.setClear(1),p.setClear(0),Nt(o.DEPTH_TEST),m.setFunc(du),ee(!1),L(Cg),Nt(o.CULL_FACE),Pt(za);function Nt(F){M[F]!==!0&&(o.enable(F),M[F]=!0)}function kt(F){M[F]!==!1&&(o.disable(F),M[F]=!1)}function ue(F,At){return y[F]!==At?(o.bindFramebuffer(F,At),y[F]=At,s&&(F===o.DRAW_FRAMEBUFFER&&(y[o.FRAMEBUFFER]=At),F===o.FRAMEBUFFER&&(y[o.DRAW_FRAMEBUFFER]=At)),!0):!1}function tt(F,At){let Tt=T,jt=!1;if(F)if(Tt=b.get(At),Tt===void 0&&(Tt=[],b.set(At,Tt)),F.isWebGLMultipleRenderTargets){const Gt=F.texture;if(Tt.length!==Gt.length||Tt[0]!==o.COLOR_ATTACHMENT0){for(let Re=0,Ee=Gt.length;Re<Ee;Re++)Tt[Re]=o.COLOR_ATTACHMENT0+Re;Tt.length=Gt.length,jt=!0}}else Tt[0]!==o.COLOR_ATTACHMENT0&&(Tt[0]=o.COLOR_ATTACHMENT0,jt=!0);else Tt[0]!==o.BACK&&(Tt[0]=o.BACK,jt=!0);jt&&(i.isWebGL2?o.drawBuffers(Tt):e.get("WEBGL_draw_buffers").drawBuffersWEBGL(Tt))}function ln(F){return x!==F?(o.useProgram(F),x=F,!0):!1}const Ft={[ur]:o.FUNC_ADD,[oM]:o.FUNC_SUBTRACT,[lM]:o.FUNC_REVERSE_SUBTRACT};if(s)Ft[Ug]=o.MIN,Ft[Ng]=o.MAX;else{const F=e.get("EXT_blend_minmax");F!==null&&(Ft[Ug]=F.MIN_EXT,Ft[Ng]=F.MAX_EXT)}const Qt={[uM]:o.ZERO,[cM]:o.ONE,[fM]:o.SRC_COLOR,[gh]:o.SRC_ALPHA,[_M]:o.SRC_ALPHA_SATURATE,[mM]:o.DST_COLOR,[dM]:o.DST_ALPHA,[hM]:o.ONE_MINUS_SRC_COLOR,[_h]:o.ONE_MINUS_SRC_ALPHA,[gM]:o.ONE_MINUS_DST_COLOR,[pM]:o.ONE_MINUS_DST_ALPHA,[vM]:o.CONSTANT_COLOR,[SM]:o.ONE_MINUS_CONSTANT_COLOR,[MM]:o.CONSTANT_ALPHA,[xM]:o.ONE_MINUS_CONSTANT_ALPHA};function Pt(F,At,Tt,jt,Gt,Re,Ee,Ve,ke,Ce){if(F===za){v===!0&&(kt(o.BLEND),v=!1);return}if(v===!1&&(Nt(o.BLEND),v=!0),F!==sM){if(F!==N||Ce!==lt){if((R!==ur||B!==ur)&&(o.blendEquation(o.FUNC_ADD),R=ur,B=ur),Ce)switch(F){case ds:o.blendFuncSeparate(o.ONE,o.ONE_MINUS_SRC_ALPHA,o.ONE,o.ONE_MINUS_SRC_ALPHA);break;case wg:o.blendFunc(o.ONE,o.ONE);break;case Dg:o.blendFuncSeparate(o.ZERO,o.ONE_MINUS_SRC_COLOR,o.ZERO,o.ONE);break;case Lg:o.blendFuncSeparate(o.ZERO,o.SRC_COLOR,o.ZERO,o.SRC_ALPHA);break;default:console.error("THREE.WebGLState: Invalid blending: ",F);break}else switch(F){case ds:o.blendFuncSeparate(o.SRC_ALPHA,o.ONE_MINUS_SRC_ALPHA,o.ONE,o.ONE_MINUS_SRC_ALPHA);break;case wg:o.blendFunc(o.SRC_ALPHA,o.ONE);break;case Dg:o.blendFuncSeparate(o.ZERO,o.ONE_MINUS_SRC_COLOR,o.ZERO,o.ONE);break;case Lg:o.blendFunc(o.ZERO,o.SRC_COLOR);break;default:console.error("THREE.WebGLState: Invalid blending: ",F);break}I=null,q=null,z=null,dt=null,w.set(0,0,0),U=0,N=F,lt=Ce}return}Gt=Gt||At,Re=Re||Tt,Ee=Ee||jt,(At!==R||Gt!==B)&&(o.blendEquationSeparate(Ft[At],Ft[Gt]),R=At,B=Gt),(Tt!==I||jt!==q||Re!==z||Ee!==dt)&&(o.blendFuncSeparate(Qt[Tt],Qt[jt],Qt[Re],Qt[Ee]),I=Tt,q=jt,z=Re,dt=Ee),(Ve.equals(w)===!1||ke!==U)&&(o.blendColor(Ve.r,Ve.g,Ve.b,ke),w.copy(Ve),U=ke),N=F,lt=!1}function Pe(F,At){F.side===Ki?kt(o.CULL_FACE):Nt(o.CULL_FACE);let Tt=F.side===In;At&&(Tt=!Tt),ee(Tt),F.blending===ds&&F.transparent===!1?Pt(za):Pt(F.blending,F.blendEquation,F.blendSrc,F.blendDst,F.blendEquationAlpha,F.blendSrcAlpha,F.blendDstAlpha,F.blendColor,F.blendAlpha,F.premultipliedAlpha),m.setFunc(F.depthFunc),m.setTest(F.depthTest),m.setMask(F.depthWrite),h.setMask(F.colorWrite);const jt=F.stencilWrite;p.setTest(jt),jt&&(p.setMask(F.stencilWriteMask),p.setFunc(F.stencilFunc,F.stencilRef,F.stencilFuncMask),p.setOp(F.stencilFail,F.stencilZFail,F.stencilZPass)),nt(F.polygonOffset,F.polygonOffsetFactor,F.polygonOffsetUnits),F.alphaToCoverage===!0?Nt(o.SAMPLE_ALPHA_TO_COVERAGE):kt(o.SAMPLE_ALPHA_TO_COVERAGE)}function ee(F){mt!==F&&(F?o.frontFace(o.CW):o.frontFace(o.CCW),mt=F)}function L(F){F!==iM?(Nt(o.CULL_FACE),F!==Et&&(F===Cg?o.cullFace(o.BACK):F===aM?o.cullFace(o.FRONT):o.cullFace(o.FRONT_AND_BACK))):kt(o.CULL_FACE),Et=F}function A(F){F!==V&&(Q&&o.lineWidth(F),V=F)}function nt(F,At,Tt){F?(Nt(o.POLYGON_OFFSET_FILL),($!==At||O!==Tt)&&(o.polygonOffset(At,Tt),$=At,O=Tt)):kt(o.POLYGON_OFFSET_FILL)}function St(F){F?Nt(o.SCISSOR_TEST):kt(o.SCISSOR_TEST)}function vt(F){F===void 0&&(F=o.TEXTURE0+k-1),D!==F&&(o.activeTexture(F),D=F)}function gt(F,At,Tt){Tt===void 0&&(D===null?Tt=o.TEXTURE0+k-1:Tt=D);let jt=X[Tt];jt===void 0&&(jt={type:void 0,texture:void 0},X[Tt]=jt),(jt.type!==F||jt.texture!==At)&&(D!==Tt&&(o.activeTexture(Tt),D=Tt),o.bindTexture(F,At||It[F]),jt.type=F,jt.texture=At)}function Ht(){const F=X[D];F!==void 0&&F.type!==void 0&&(o.bindTexture(F.type,null),F.type=void 0,F.texture=void 0)}function Rt(){try{o.compressedTexImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Ut(){try{o.compressedTexImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function qt(){try{o.texSubImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function ie(){try{o.texSubImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function _t(){try{o.compressedTexSubImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function ye(){try{o.compressedTexSubImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function le(){try{o.texStorage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Kt(){try{o.texStorage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Dt(){try{o.texImage2D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function wt(){try{o.texImage3D.apply(o,arguments)}catch(F){console.error("THREE.WebGLState:",F)}}function Xt(F){pt.equals(F)===!1&&(o.scissor(F.x,F.y,F.z,F.w),pt.copy(F))}function ve(F){Mt.equals(F)===!1&&(o.viewport(F.x,F.y,F.z,F.w),Mt.copy(F))}function He(F,At){let Tt=_.get(At);Tt===void 0&&(Tt=new WeakMap,_.set(At,Tt));let jt=Tt.get(F);jt===void 0&&(jt=o.getUniformBlockIndex(At,F.name),Tt.set(F,jt))}function re(F,At){const jt=_.get(At).get(F);g.get(At)!==jt&&(o.uniformBlockBinding(At,jt,F.__bindingPointIndex),g.set(At,jt))}function yt(){o.disable(o.BLEND),o.disable(o.CULL_FACE),o.disable(o.DEPTH_TEST),o.disable(o.POLYGON_OFFSET_FILL),o.disable(o.SCISSOR_TEST),o.disable(o.STENCIL_TEST),o.disable(o.SAMPLE_ALPHA_TO_COVERAGE),o.blendEquation(o.FUNC_ADD),o.blendFunc(o.ONE,o.ZERO),o.blendFuncSeparate(o.ONE,o.ZERO,o.ONE,o.ZERO),o.blendColor(0,0,0,0),o.colorMask(!0,!0,!0,!0),o.clearColor(0,0,0,0),o.depthMask(!0),o.depthFunc(o.LESS),o.clearDepth(1),o.stencilMask(4294967295),o.stencilFunc(o.ALWAYS,0,4294967295),o.stencilOp(o.KEEP,o.KEEP,o.KEEP),o.clearStencil(0),o.cullFace(o.BACK),o.frontFace(o.CCW),o.polygonOffset(0,0),o.activeTexture(o.TEXTURE0),o.bindFramebuffer(o.FRAMEBUFFER,null),s===!0&&(o.bindFramebuffer(o.DRAW_FRAMEBUFFER,null),o.bindFramebuffer(o.READ_FRAMEBUFFER,null)),o.useProgram(null),o.lineWidth(1),o.scissor(0,0,o.canvas.width,o.canvas.height),o.viewport(0,0,o.canvas.width,o.canvas.height),M={},D=null,X={},y={},b=new WeakMap,T=[],x=null,v=!1,N=null,R=null,I=null,q=null,B=null,z=null,dt=null,w=new Me(0,0,0),U=0,lt=!1,mt=null,Et=null,V=null,$=null,O=null,pt.set(0,0,o.canvas.width,o.canvas.height),Mt.set(0,0,o.canvas.width,o.canvas.height),h.reset(),m.reset(),p.reset()}return{buffers:{color:h,depth:m,stencil:p},enable:Nt,disable:kt,bindFramebuffer:ue,drawBuffers:tt,useProgram:ln,setBlending:Pt,setMaterial:Pe,setFlipSided:ee,setCullFace:L,setLineWidth:A,setPolygonOffset:nt,setScissorTest:St,activeTexture:vt,bindTexture:gt,unbindTexture:Ht,compressedTexImage2D:Rt,compressedTexImage3D:Ut,texImage2D:Dt,texImage3D:wt,updateUBOMapping:He,uniformBlockBinding:re,texStorage2D:le,texStorage3D:Kt,texSubImage2D:qt,texSubImage3D:ie,compressedTexSubImage2D:_t,compressedTexSubImage3D:ye,scissor:Xt,viewport:ve,reset:yt}}function nA(o,e,i,s,l,c,d){const h=l.isWebGL2,m=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,p=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),g=new WeakMap;let _;const M=new WeakMap;let y=!1;try{y=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function b(L,A){return y?new OffscreenCanvas(L,A):vu("canvas")}function T(L,A,nt,St){let vt=1;if((L.width>St||L.height>St)&&(vt=St/Math.max(L.width,L.height)),vt<1||A===!0)if(typeof HTMLImageElement<"u"&&L instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&L instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&L instanceof ImageBitmap){const gt=A?Th:Math.floor,Ht=gt(vt*L.width),Rt=gt(vt*L.height);_===void 0&&(_=b(Ht,Rt));const Ut=nt?b(Ht,Rt):_;return Ut.width=Ht,Ut.height=Rt,Ut.getContext("2d").drawImage(L,0,0,Ht,Rt),console.warn("THREE.WebGLRenderer: Texture has been resized from ("+L.width+"x"+L.height+") to ("+Ht+"x"+Rt+")."),Ut}else return"data"in L&&console.warn("THREE.WebGLRenderer: Image in DataTexture is too big ("+L.width+"x"+L.height+")."),L;return L}function x(L){return u_(L.width)&&u_(L.height)}function v(L){return h?!1:L.wrapS!==_i||L.wrapT!==_i||L.minFilter!==Cn&&L.minFilter!==si}function N(L,A){return L.generateMipmaps&&A&&L.minFilter!==Cn&&L.minFilter!==si}function R(L){o.generateMipmap(L)}function I(L,A,nt,St,vt=!1){if(h===!1)return A;if(L!==null){if(o[L]!==void 0)return o[L];console.warn("THREE.WebGLRenderer: Attempt to use non-existing WebGL internal format '"+L+"'")}let gt=A;if(A===o.RED&&(nt===o.FLOAT&&(gt=o.R32F),nt===o.HALF_FLOAT&&(gt=o.R16F),nt===o.UNSIGNED_BYTE&&(gt=o.R8)),A===o.RED_INTEGER&&(nt===o.UNSIGNED_BYTE&&(gt=o.R8UI),nt===o.UNSIGNED_SHORT&&(gt=o.R16UI),nt===o.UNSIGNED_INT&&(gt=o.R32UI),nt===o.BYTE&&(gt=o.R8I),nt===o.SHORT&&(gt=o.R16I),nt===o.INT&&(gt=o.R32I)),A===o.RG&&(nt===o.FLOAT&&(gt=o.RG32F),nt===o.HALF_FLOAT&&(gt=o.RG16F),nt===o.UNSIGNED_BYTE&&(gt=o.RG8)),A===o.RGBA){const Ht=vt?pu:Ue.getTransfer(St);nt===o.FLOAT&&(gt=o.RGBA32F),nt===o.HALF_FLOAT&&(gt=o.RGBA16F),nt===o.UNSIGNED_BYTE&&(gt=Ht===Fe?o.SRGB8_ALPHA8:o.RGBA8),nt===o.UNSIGNED_SHORT_4_4_4_4&&(gt=o.RGBA4),nt===o.UNSIGNED_SHORT_5_5_5_1&&(gt=o.RGB5_A1)}return(gt===o.R16F||gt===o.R32F||gt===o.RG16F||gt===o.RG32F||gt===o.RGBA16F||gt===o.RGBA32F)&&e.get("EXT_color_buffer_float"),gt}function q(L,A,nt){return N(L,nt)===!0||L.isFramebufferTexture&&L.minFilter!==Cn&&L.minFilter!==si?Math.log2(Math.max(A.width,A.height))+1:L.mipmaps!==void 0&&L.mipmaps.length>0?L.mipmaps.length:L.isCompressedTexture&&Array.isArray(L.image)?A.mipmaps.length:1}function B(L){return L===Cn||L===Og||L===zf?o.NEAREST:o.LINEAR}function z(L){const A=L.target;A.removeEventListener("dispose",z),w(A),A.isVideoTexture&&g.delete(A)}function dt(L){const A=L.target;A.removeEventListener("dispose",dt),lt(A)}function w(L){const A=s.get(L);if(A.__webglInit===void 0)return;const nt=L.source,St=M.get(nt);if(St){const vt=St[A.__cacheKey];vt.usedTimes--,vt.usedTimes===0&&U(L),Object.keys(St).length===0&&M.delete(nt)}s.remove(L)}function U(L){const A=s.get(L);o.deleteTexture(A.__webglTexture);const nt=L.source,St=M.get(nt);delete St[A.__cacheKey],d.memory.textures--}function lt(L){const A=L.texture,nt=s.get(L),St=s.get(A);if(St.__webglTexture!==void 0&&(o.deleteTexture(St.__webglTexture),d.memory.textures--),L.depthTexture&&L.depthTexture.dispose(),L.isWebGLCubeRenderTarget)for(let vt=0;vt<6;vt++){if(Array.isArray(nt.__webglFramebuffer[vt]))for(let gt=0;gt<nt.__webglFramebuffer[vt].length;gt++)o.deleteFramebuffer(nt.__webglFramebuffer[vt][gt]);else o.deleteFramebuffer(nt.__webglFramebuffer[vt]);nt.__webglDepthbuffer&&o.deleteRenderbuffer(nt.__webglDepthbuffer[vt])}else{if(Array.isArray(nt.__webglFramebuffer))for(let vt=0;vt<nt.__webglFramebuffer.length;vt++)o.deleteFramebuffer(nt.__webglFramebuffer[vt]);else o.deleteFramebuffer(nt.__webglFramebuffer);if(nt.__webglDepthbuffer&&o.deleteRenderbuffer(nt.__webglDepthbuffer),nt.__webglMultisampledFramebuffer&&o.deleteFramebuffer(nt.__webglMultisampledFramebuffer),nt.__webglColorRenderbuffer)for(let vt=0;vt<nt.__webglColorRenderbuffer.length;vt++)nt.__webglColorRenderbuffer[vt]&&o.deleteRenderbuffer(nt.__webglColorRenderbuffer[vt]);nt.__webglDepthRenderbuffer&&o.deleteRenderbuffer(nt.__webglDepthRenderbuffer)}if(L.isWebGLMultipleRenderTargets)for(let vt=0,gt=A.length;vt<gt;vt++){const Ht=s.get(A[vt]);Ht.__webglTexture&&(o.deleteTexture(Ht.__webglTexture),d.memory.textures--),s.remove(A[vt])}s.remove(A),s.remove(L)}let mt=0;function Et(){mt=0}function V(){const L=mt;return L>=l.maxTextures&&console.warn("THREE.WebGLTextures: Trying to use "+L+" texture units while this GPU supports only "+l.maxTextures),mt+=1,L}function $(L){const A=[];return A.push(L.wrapS),A.push(L.wrapT),A.push(L.wrapR||0),A.push(L.magFilter),A.push(L.minFilter),A.push(L.anisotropy),A.push(L.internalFormat),A.push(L.format),A.push(L.type),A.push(L.generateMipmaps),A.push(L.premultiplyAlpha),A.push(L.flipY),A.push(L.unpackAlignment),A.push(L.colorSpace),A.join()}function O(L,A){const nt=s.get(L);if(L.isVideoTexture&&Pe(L),L.isRenderTargetTexture===!1&&L.version>0&&nt.__version!==L.version){const St=L.image;if(St===null)console.warn("THREE.WebGLRenderer: Texture marked for update but no image data found.");else if(St.complete===!1)console.warn("THREE.WebGLRenderer: Texture marked for update but image is incomplete");else{pt(nt,L,A);return}}i.bindTexture(o.TEXTURE_2D,nt.__webglTexture,o.TEXTURE0+A)}function k(L,A){const nt=s.get(L);if(L.version>0&&nt.__version!==L.version){pt(nt,L,A);return}i.bindTexture(o.TEXTURE_2D_ARRAY,nt.__webglTexture,o.TEXTURE0+A)}function Q(L,A){const nt=s.get(L);if(L.version>0&&nt.__version!==L.version){pt(nt,L,A);return}i.bindTexture(o.TEXTURE_3D,nt.__webglTexture,o.TEXTURE0+A)}function ot(L,A){const nt=s.get(L);if(L.version>0&&nt.__version!==L.version){Mt(nt,L,A);return}i.bindTexture(o.TEXTURE_CUBE_MAP,nt.__webglTexture,o.TEXTURE0+A)}const ct={[Mh]:o.REPEAT,[_i]:o.CLAMP_TO_EDGE,[xh]:o.MIRRORED_REPEAT},D={[Cn]:o.NEAREST,[Og]:o.NEAREST_MIPMAP_NEAREST,[zf]:o.NEAREST_MIPMAP_LINEAR,[si]:o.LINEAR,[BM]:o.LINEAR_MIPMAP_NEAREST,[bo]:o.LINEAR_MIPMAP_LINEAR},X={[ZM]:o.NEVER,[ex]:o.ALWAYS,[KM]:o.LESS,[dv]:o.LEQUAL,[QM]:o.EQUAL,[tx]:o.GEQUAL,[JM]:o.GREATER,[$M]:o.NOTEQUAL};function G(L,A,nt){if(nt?(o.texParameteri(L,o.TEXTURE_WRAP_S,ct[A.wrapS]),o.texParameteri(L,o.TEXTURE_WRAP_T,ct[A.wrapT]),(L===o.TEXTURE_3D||L===o.TEXTURE_2D_ARRAY)&&o.texParameteri(L,o.TEXTURE_WRAP_R,ct[A.wrapR]),o.texParameteri(L,o.TEXTURE_MAG_FILTER,D[A.magFilter]),o.texParameteri(L,o.TEXTURE_MIN_FILTER,D[A.minFilter])):(o.texParameteri(L,o.TEXTURE_WRAP_S,o.CLAMP_TO_EDGE),o.texParameteri(L,o.TEXTURE_WRAP_T,o.CLAMP_TO_EDGE),(L===o.TEXTURE_3D||L===o.TEXTURE_2D_ARRAY)&&o.texParameteri(L,o.TEXTURE_WRAP_R,o.CLAMP_TO_EDGE),(A.wrapS!==_i||A.wrapT!==_i)&&console.warn("THREE.WebGLRenderer: Texture is not power of two. Texture.wrapS and Texture.wrapT should be set to THREE.ClampToEdgeWrapping."),o.texParameteri(L,o.TEXTURE_MAG_FILTER,B(A.magFilter)),o.texParameteri(L,o.TEXTURE_MIN_FILTER,B(A.minFilter)),A.minFilter!==Cn&&A.minFilter!==si&&console.warn("THREE.WebGLRenderer: Texture is not power of two. Texture.minFilter should be set to THREE.NearestFilter or THREE.LinearFilter.")),A.compareFunction&&(o.texParameteri(L,o.TEXTURE_COMPARE_MODE,o.COMPARE_REF_TO_TEXTURE),o.texParameteri(L,o.TEXTURE_COMPARE_FUNC,X[A.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){const St=e.get("EXT_texture_filter_anisotropic");if(A.magFilter===Cn||A.minFilter!==zf&&A.minFilter!==bo||A.type===Na&&e.has("OES_texture_float_linear")===!1||h===!1&&A.type===Ao&&e.has("OES_texture_half_float_linear")===!1)return;(A.anisotropy>1||s.get(A).__currentAnisotropy)&&(o.texParameterf(L,St.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(A.anisotropy,l.getMaxAnisotropy())),s.get(A).__currentAnisotropy=A.anisotropy)}}function Z(L,A){let nt=!1;L.__webglInit===void 0&&(L.__webglInit=!0,A.addEventListener("dispose",z));const St=A.source;let vt=M.get(St);vt===void 0&&(vt={},M.set(St,vt));const gt=$(A);if(gt!==L.__cacheKey){vt[gt]===void 0&&(vt[gt]={texture:o.createTexture(),usedTimes:0},d.memory.textures++,nt=!0),vt[gt].usedTimes++;const Ht=vt[L.__cacheKey];Ht!==void 0&&(vt[L.__cacheKey].usedTimes--,Ht.usedTimes===0&&U(A)),L.__cacheKey=gt,L.__webglTexture=vt[gt].texture}return nt}function pt(L,A,nt){let St=o.TEXTURE_2D;(A.isDataArrayTexture||A.isCompressedArrayTexture)&&(St=o.TEXTURE_2D_ARRAY),A.isData3DTexture&&(St=o.TEXTURE_3D);const vt=Z(L,A),gt=A.source;i.bindTexture(St,L.__webglTexture,o.TEXTURE0+nt);const Ht=s.get(gt);if(gt.version!==Ht.__version||vt===!0){i.activeTexture(o.TEXTURE0+nt);const Rt=Ue.getPrimaries(Ue.workingColorSpace),Ut=A.colorSpace===oi?null:Ue.getPrimaries(A.colorSpace),qt=A.colorSpace===oi||Rt===Ut?o.NONE:o.BROWSER_DEFAULT_WEBGL;o.pixelStorei(o.UNPACK_FLIP_Y_WEBGL,A.flipY),o.pixelStorei(o.UNPACK_PREMULTIPLY_ALPHA_WEBGL,A.premultiplyAlpha),o.pixelStorei(o.UNPACK_ALIGNMENT,A.unpackAlignment),o.pixelStorei(o.UNPACK_COLORSPACE_CONVERSION_WEBGL,qt);const ie=v(A)&&x(A.image)===!1;let _t=T(A.image,ie,!1,l.maxTextureSize);_t=ee(A,_t);const ye=x(_t)||h,le=c.convert(A.format,A.colorSpace);let Kt=c.convert(A.type),Dt=I(A.internalFormat,le,Kt,A.colorSpace,A.isVideoTexture);G(St,A,ye);let wt;const Xt=A.mipmaps,ve=h&&A.isVideoTexture!==!0&&Dt!==cv,He=Ht.__version===void 0||vt===!0,re=q(A,_t,ye);if(A.isDepthTexture)Dt=o.DEPTH_COMPONENT,h?A.type===Na?Dt=o.DEPTH_COMPONENT32F:A.type===Ua?Dt=o.DEPTH_COMPONENT24:A.type===fr?Dt=o.DEPTH24_STENCIL8:Dt=o.DEPTH_COMPONENT16:A.type===Na&&console.error("WebGLRenderer: Floating point depth texture requires WebGL2."),A.format===hr&&Dt===o.DEPTH_COMPONENT&&A.type!==Rh&&A.type!==Ua&&(console.warn("THREE.WebGLRenderer: Use UnsignedShortType or UnsignedIntType for DepthFormat DepthTexture."),A.type=Ua,Kt=c.convert(A.type)),A.format===_s&&Dt===o.DEPTH_COMPONENT&&(Dt=o.DEPTH_STENCIL,A.type!==fr&&(console.warn("THREE.WebGLRenderer: Use UnsignedInt248Type for DepthStencilFormat DepthTexture."),A.type=fr,Kt=c.convert(A.type))),He&&(ve?i.texStorage2D(o.TEXTURE_2D,1,Dt,_t.width,_t.height):i.texImage2D(o.TEXTURE_2D,0,Dt,_t.width,_t.height,0,le,Kt,null));else if(A.isDataTexture)if(Xt.length>0&&ye){ve&&He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,Xt[0].width,Xt[0].height);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],ve?i.texSubImage2D(o.TEXTURE_2D,yt,0,0,wt.width,wt.height,le,Kt,wt.data):i.texImage2D(o.TEXTURE_2D,yt,Dt,wt.width,wt.height,0,le,Kt,wt.data);A.generateMipmaps=!1}else ve?(He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,_t.width,_t.height),i.texSubImage2D(o.TEXTURE_2D,0,0,0,_t.width,_t.height,le,Kt,_t.data)):i.texImage2D(o.TEXTURE_2D,0,Dt,_t.width,_t.height,0,le,Kt,_t.data);else if(A.isCompressedTexture)if(A.isCompressedArrayTexture){ve&&He&&i.texStorage3D(o.TEXTURE_2D_ARRAY,re,Dt,Xt[0].width,Xt[0].height,_t.depth);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],A.format!==vi?le!==null?ve?i.compressedTexSubImage3D(o.TEXTURE_2D_ARRAY,yt,0,0,0,wt.width,wt.height,_t.depth,le,wt.data,0,0):i.compressedTexImage3D(o.TEXTURE_2D_ARRAY,yt,Dt,wt.width,wt.height,_t.depth,0,wt.data,0,0):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):ve?i.texSubImage3D(o.TEXTURE_2D_ARRAY,yt,0,0,0,wt.width,wt.height,_t.depth,le,Kt,wt.data):i.texImage3D(o.TEXTURE_2D_ARRAY,yt,Dt,wt.width,wt.height,_t.depth,0,le,Kt,wt.data)}else{ve&&He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,Xt[0].width,Xt[0].height);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],A.format!==vi?le!==null?ve?i.compressedTexSubImage2D(o.TEXTURE_2D,yt,0,0,wt.width,wt.height,le,wt.data):i.compressedTexImage2D(o.TEXTURE_2D,yt,Dt,wt.width,wt.height,0,wt.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):ve?i.texSubImage2D(o.TEXTURE_2D,yt,0,0,wt.width,wt.height,le,Kt,wt.data):i.texImage2D(o.TEXTURE_2D,yt,Dt,wt.width,wt.height,0,le,Kt,wt.data)}else if(A.isDataArrayTexture)ve?(He&&i.texStorage3D(o.TEXTURE_2D_ARRAY,re,Dt,_t.width,_t.height,_t.depth),i.texSubImage3D(o.TEXTURE_2D_ARRAY,0,0,0,0,_t.width,_t.height,_t.depth,le,Kt,_t.data)):i.texImage3D(o.TEXTURE_2D_ARRAY,0,Dt,_t.width,_t.height,_t.depth,0,le,Kt,_t.data);else if(A.isData3DTexture)ve?(He&&i.texStorage3D(o.TEXTURE_3D,re,Dt,_t.width,_t.height,_t.depth),i.texSubImage3D(o.TEXTURE_3D,0,0,0,0,_t.width,_t.height,_t.depth,le,Kt,_t.data)):i.texImage3D(o.TEXTURE_3D,0,Dt,_t.width,_t.height,_t.depth,0,le,Kt,_t.data);else if(A.isFramebufferTexture){if(He)if(ve)i.texStorage2D(o.TEXTURE_2D,re,Dt,_t.width,_t.height);else{let yt=_t.width,F=_t.height;for(let At=0;At<re;At++)i.texImage2D(o.TEXTURE_2D,At,Dt,yt,F,0,le,Kt,null),yt>>=1,F>>=1}}else if(Xt.length>0&&ye){ve&&He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,Xt[0].width,Xt[0].height);for(let yt=0,F=Xt.length;yt<F;yt++)wt=Xt[yt],ve?i.texSubImage2D(o.TEXTURE_2D,yt,0,0,le,Kt,wt):i.texImage2D(o.TEXTURE_2D,yt,Dt,le,Kt,wt);A.generateMipmaps=!1}else ve?(He&&i.texStorage2D(o.TEXTURE_2D,re,Dt,_t.width,_t.height),i.texSubImage2D(o.TEXTURE_2D,0,0,0,le,Kt,_t)):i.texImage2D(o.TEXTURE_2D,0,Dt,le,Kt,_t);N(A,ye)&&R(St),Ht.__version=gt.version,A.onUpdate&&A.onUpdate(A)}L.__version=A.version}function Mt(L,A,nt){if(A.image.length!==6)return;const St=Z(L,A),vt=A.source;i.bindTexture(o.TEXTURE_CUBE_MAP,L.__webglTexture,o.TEXTURE0+nt);const gt=s.get(vt);if(vt.version!==gt.__version||St===!0){i.activeTexture(o.TEXTURE0+nt);const Ht=Ue.getPrimaries(Ue.workingColorSpace),Rt=A.colorSpace===oi?null:Ue.getPrimaries(A.colorSpace),Ut=A.colorSpace===oi||Ht===Rt?o.NONE:o.BROWSER_DEFAULT_WEBGL;o.pixelStorei(o.UNPACK_FLIP_Y_WEBGL,A.flipY),o.pixelStorei(o.UNPACK_PREMULTIPLY_ALPHA_WEBGL,A.premultiplyAlpha),o.pixelStorei(o.UNPACK_ALIGNMENT,A.unpackAlignment),o.pixelStorei(o.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ut);const qt=A.isCompressedTexture||A.image[0].isCompressedTexture,ie=A.image[0]&&A.image[0].isDataTexture,_t=[];for(let yt=0;yt<6;yt++)!qt&&!ie?_t[yt]=T(A.image[yt],!1,!0,l.maxCubemapSize):_t[yt]=ie?A.image[yt].image:A.image[yt],_t[yt]=ee(A,_t[yt]);const ye=_t[0],le=x(ye)||h,Kt=c.convert(A.format,A.colorSpace),Dt=c.convert(A.type),wt=I(A.internalFormat,Kt,Dt,A.colorSpace),Xt=h&&A.isVideoTexture!==!0,ve=gt.__version===void 0||St===!0;let He=q(A,ye,le);G(o.TEXTURE_CUBE_MAP,A,le);let re;if(qt){Xt&&ve&&i.texStorage2D(o.TEXTURE_CUBE_MAP,He,wt,ye.width,ye.height);for(let yt=0;yt<6;yt++){re=_t[yt].mipmaps;for(let F=0;F<re.length;F++){const At=re[F];A.format!==vi?Kt!==null?Xt?i.compressedTexSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,0,0,At.width,At.height,Kt,At.data):i.compressedTexImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,wt,At.width,At.height,0,At.data):console.warn("THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,0,0,At.width,At.height,Kt,Dt,At.data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F,wt,At.width,At.height,0,Kt,Dt,At.data)}}}else{re=A.mipmaps,Xt&&ve&&(re.length>0&&He++,i.texStorage2D(o.TEXTURE_CUBE_MAP,He,wt,_t[0].width,_t[0].height));for(let yt=0;yt<6;yt++)if(ie){Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,0,0,_t[yt].width,_t[yt].height,Kt,Dt,_t[yt].data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,wt,_t[yt].width,_t[yt].height,0,Kt,Dt,_t[yt].data);for(let F=0;F<re.length;F++){const Tt=re[F].image[yt].image;Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,0,0,Tt.width,Tt.height,Kt,Dt,Tt.data):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,wt,Tt.width,Tt.height,0,Kt,Dt,Tt.data)}}else{Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,0,0,Kt,Dt,_t[yt]):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,0,wt,Kt,Dt,_t[yt]);for(let F=0;F<re.length;F++){const At=re[F];Xt?i.texSubImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,0,0,Kt,Dt,At.image[yt]):i.texImage2D(o.TEXTURE_CUBE_MAP_POSITIVE_X+yt,F+1,wt,Kt,Dt,At.image[yt])}}}N(A,le)&&R(o.TEXTURE_CUBE_MAP),gt.__version=vt.version,A.onUpdate&&A.onUpdate(A)}L.__version=A.version}function xt(L,A,nt,St,vt,gt){const Ht=c.convert(nt.format,nt.colorSpace),Rt=c.convert(nt.type),Ut=I(nt.internalFormat,Ht,Rt,nt.colorSpace);if(!s.get(A).__hasExternalTextures){const ie=Math.max(1,A.width>>gt),_t=Math.max(1,A.height>>gt);vt===o.TEXTURE_3D||vt===o.TEXTURE_2D_ARRAY?i.texImage3D(vt,gt,Ut,ie,_t,A.depth,0,Ht,Rt,null):i.texImage2D(vt,gt,Ut,ie,_t,0,Ht,Rt,null)}i.bindFramebuffer(o.FRAMEBUFFER,L),Pt(A)?m.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,St,vt,s.get(nt).__webglTexture,0,Qt(A)):(vt===o.TEXTURE_2D||vt>=o.TEXTURE_CUBE_MAP_POSITIVE_X&&vt<=o.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&o.framebufferTexture2D(o.FRAMEBUFFER,St,vt,s.get(nt).__webglTexture,gt),i.bindFramebuffer(o.FRAMEBUFFER,null)}function It(L,A,nt){if(o.bindRenderbuffer(o.RENDERBUFFER,L),A.depthBuffer&&!A.stencilBuffer){let St=h===!0?o.DEPTH_COMPONENT24:o.DEPTH_COMPONENT16;if(nt||Pt(A)){const vt=A.depthTexture;vt&&vt.isDepthTexture&&(vt.type===Na?St=o.DEPTH_COMPONENT32F:vt.type===Ua&&(St=o.DEPTH_COMPONENT24));const gt=Qt(A);Pt(A)?m.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,gt,St,A.width,A.height):o.renderbufferStorageMultisample(o.RENDERBUFFER,gt,St,A.width,A.height)}else o.renderbufferStorage(o.RENDERBUFFER,St,A.width,A.height);o.framebufferRenderbuffer(o.FRAMEBUFFER,o.DEPTH_ATTACHMENT,o.RENDERBUFFER,L)}else if(A.depthBuffer&&A.stencilBuffer){const St=Qt(A);nt&&Pt(A)===!1?o.renderbufferStorageMultisample(o.RENDERBUFFER,St,o.DEPTH24_STENCIL8,A.width,A.height):Pt(A)?m.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,St,o.DEPTH24_STENCIL8,A.width,A.height):o.renderbufferStorage(o.RENDERBUFFER,o.DEPTH_STENCIL,A.width,A.height),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.DEPTH_STENCIL_ATTACHMENT,o.RENDERBUFFER,L)}else{const St=A.isWebGLMultipleRenderTargets===!0?A.texture:[A.texture];for(let vt=0;vt<St.length;vt++){const gt=St[vt],Ht=c.convert(gt.format,gt.colorSpace),Rt=c.convert(gt.type),Ut=I(gt.internalFormat,Ht,Rt,gt.colorSpace),qt=Qt(A);nt&&Pt(A)===!1?o.renderbufferStorageMultisample(o.RENDERBUFFER,qt,Ut,A.width,A.height):Pt(A)?m.renderbufferStorageMultisampleEXT(o.RENDERBUFFER,qt,Ut,A.width,A.height):o.renderbufferStorage(o.RENDERBUFFER,Ut,A.width,A.height)}}o.bindRenderbuffer(o.RENDERBUFFER,null)}function Nt(L,A){if(A&&A.isWebGLCubeRenderTarget)throw new Error("Depth Texture with cube render targets is not supported");if(i.bindFramebuffer(o.FRAMEBUFFER,L),!(A.depthTexture&&A.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");(!s.get(A.depthTexture).__webglTexture||A.depthTexture.image.width!==A.width||A.depthTexture.image.height!==A.height)&&(A.depthTexture.image.width=A.width,A.depthTexture.image.height=A.height,A.depthTexture.needsUpdate=!0),O(A.depthTexture,0);const St=s.get(A.depthTexture).__webglTexture,vt=Qt(A);if(A.depthTexture.format===hr)Pt(A)?m.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,o.DEPTH_ATTACHMENT,o.TEXTURE_2D,St,0,vt):o.framebufferTexture2D(o.FRAMEBUFFER,o.DEPTH_ATTACHMENT,o.TEXTURE_2D,St,0);else if(A.depthTexture.format===_s)Pt(A)?m.framebufferTexture2DMultisampleEXT(o.FRAMEBUFFER,o.DEPTH_STENCIL_ATTACHMENT,o.TEXTURE_2D,St,0,vt):o.framebufferTexture2D(o.FRAMEBUFFER,o.DEPTH_STENCIL_ATTACHMENT,o.TEXTURE_2D,St,0);else throw new Error("Unknown depthTexture format")}function kt(L){const A=s.get(L),nt=L.isWebGLCubeRenderTarget===!0;if(L.depthTexture&&!A.__autoAllocateDepthBuffer){if(nt)throw new Error("target.depthTexture not supported in Cube render targets");Nt(A.__webglFramebuffer,L)}else if(nt){A.__webglDepthbuffer=[];for(let St=0;St<6;St++)i.bindFramebuffer(o.FRAMEBUFFER,A.__webglFramebuffer[St]),A.__webglDepthbuffer[St]=o.createRenderbuffer(),It(A.__webglDepthbuffer[St],L,!1)}else i.bindFramebuffer(o.FRAMEBUFFER,A.__webglFramebuffer),A.__webglDepthbuffer=o.createRenderbuffer(),It(A.__webglDepthbuffer,L,!1);i.bindFramebuffer(o.FRAMEBUFFER,null)}function ue(L,A,nt){const St=s.get(L);A!==void 0&&xt(St.__webglFramebuffer,L,L.texture,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,0),nt!==void 0&&kt(L)}function tt(L){const A=L.texture,nt=s.get(L),St=s.get(A);L.addEventListener("dispose",dt),L.isWebGLMultipleRenderTargets!==!0&&(St.__webglTexture===void 0&&(St.__webglTexture=o.createTexture()),St.__version=A.version,d.memory.textures++);const vt=L.isWebGLCubeRenderTarget===!0,gt=L.isWebGLMultipleRenderTargets===!0,Ht=x(L)||h;if(vt){nt.__webglFramebuffer=[];for(let Rt=0;Rt<6;Rt++)if(h&&A.mipmaps&&A.mipmaps.length>0){nt.__webglFramebuffer[Rt]=[];for(let Ut=0;Ut<A.mipmaps.length;Ut++)nt.__webglFramebuffer[Rt][Ut]=o.createFramebuffer()}else nt.__webglFramebuffer[Rt]=o.createFramebuffer()}else{if(h&&A.mipmaps&&A.mipmaps.length>0){nt.__webglFramebuffer=[];for(let Rt=0;Rt<A.mipmaps.length;Rt++)nt.__webglFramebuffer[Rt]=o.createFramebuffer()}else nt.__webglFramebuffer=o.createFramebuffer();if(gt)if(l.drawBuffers){const Rt=L.texture;for(let Ut=0,qt=Rt.length;Ut<qt;Ut++){const ie=s.get(Rt[Ut]);ie.__webglTexture===void 0&&(ie.__webglTexture=o.createTexture(),d.memory.textures++)}}else console.warn("THREE.WebGLRenderer: WebGLMultipleRenderTargets can only be used with WebGL2 or WEBGL_draw_buffers extension.");if(h&&L.samples>0&&Pt(L)===!1){const Rt=gt?A:[A];nt.__webglMultisampledFramebuffer=o.createFramebuffer(),nt.__webglColorRenderbuffer=[],i.bindFramebuffer(o.FRAMEBUFFER,nt.__webglMultisampledFramebuffer);for(let Ut=0;Ut<Rt.length;Ut++){const qt=Rt[Ut];nt.__webglColorRenderbuffer[Ut]=o.createRenderbuffer(),o.bindRenderbuffer(o.RENDERBUFFER,nt.__webglColorRenderbuffer[Ut]);const ie=c.convert(qt.format,qt.colorSpace),_t=c.convert(qt.type),ye=I(qt.internalFormat,ie,_t,qt.colorSpace,L.isXRRenderTarget===!0),le=Qt(L);o.renderbufferStorageMultisample(o.RENDERBUFFER,le,ye,L.width,L.height),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+Ut,o.RENDERBUFFER,nt.__webglColorRenderbuffer[Ut])}o.bindRenderbuffer(o.RENDERBUFFER,null),L.depthBuffer&&(nt.__webglDepthRenderbuffer=o.createRenderbuffer(),It(nt.__webglDepthRenderbuffer,L,!0)),i.bindFramebuffer(o.FRAMEBUFFER,null)}}if(vt){i.bindTexture(o.TEXTURE_CUBE_MAP,St.__webglTexture),G(o.TEXTURE_CUBE_MAP,A,Ht);for(let Rt=0;Rt<6;Rt++)if(h&&A.mipmaps&&A.mipmaps.length>0)for(let Ut=0;Ut<A.mipmaps.length;Ut++)xt(nt.__webglFramebuffer[Rt][Ut],L,A,o.COLOR_ATTACHMENT0,o.TEXTURE_CUBE_MAP_POSITIVE_X+Rt,Ut);else xt(nt.__webglFramebuffer[Rt],L,A,o.COLOR_ATTACHMENT0,o.TEXTURE_CUBE_MAP_POSITIVE_X+Rt,0);N(A,Ht)&&R(o.TEXTURE_CUBE_MAP),i.unbindTexture()}else if(gt){const Rt=L.texture;for(let Ut=0,qt=Rt.length;Ut<qt;Ut++){const ie=Rt[Ut],_t=s.get(ie);i.bindTexture(o.TEXTURE_2D,_t.__webglTexture),G(o.TEXTURE_2D,ie,Ht),xt(nt.__webglFramebuffer,L,ie,o.COLOR_ATTACHMENT0+Ut,o.TEXTURE_2D,0),N(ie,Ht)&&R(o.TEXTURE_2D)}i.unbindTexture()}else{let Rt=o.TEXTURE_2D;if((L.isWebGL3DRenderTarget||L.isWebGLArrayRenderTarget)&&(h?Rt=L.isWebGL3DRenderTarget?o.TEXTURE_3D:o.TEXTURE_2D_ARRAY:console.error("THREE.WebGLTextures: THREE.Data3DTexture and THREE.DataArrayTexture only supported with WebGL2.")),i.bindTexture(Rt,St.__webglTexture),G(Rt,A,Ht),h&&A.mipmaps&&A.mipmaps.length>0)for(let Ut=0;Ut<A.mipmaps.length;Ut++)xt(nt.__webglFramebuffer[Ut],L,A,o.COLOR_ATTACHMENT0,Rt,Ut);else xt(nt.__webglFramebuffer,L,A,o.COLOR_ATTACHMENT0,Rt,0);N(A,Ht)&&R(Rt),i.unbindTexture()}L.depthBuffer&&kt(L)}function ln(L){const A=x(L)||h,nt=L.isWebGLMultipleRenderTargets===!0?L.texture:[L.texture];for(let St=0,vt=nt.length;St<vt;St++){const gt=nt[St];if(N(gt,A)){const Ht=L.isWebGLCubeRenderTarget?o.TEXTURE_CUBE_MAP:o.TEXTURE_2D,Rt=s.get(gt).__webglTexture;i.bindTexture(Ht,Rt),R(Ht),i.unbindTexture()}}}function Ft(L){if(h&&L.samples>0&&Pt(L)===!1){const A=L.isWebGLMultipleRenderTargets?L.texture:[L.texture],nt=L.width,St=L.height;let vt=o.COLOR_BUFFER_BIT;const gt=[],Ht=L.stencilBuffer?o.DEPTH_STENCIL_ATTACHMENT:o.DEPTH_ATTACHMENT,Rt=s.get(L),Ut=L.isWebGLMultipleRenderTargets===!0;if(Ut)for(let qt=0;qt<A.length;qt++)i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglMultisampledFramebuffer),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.RENDERBUFFER,null),i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglFramebuffer),o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.TEXTURE_2D,null,0);i.bindFramebuffer(o.READ_FRAMEBUFFER,Rt.__webglMultisampledFramebuffer),i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Rt.__webglFramebuffer);for(let qt=0;qt<A.length;qt++){gt.push(o.COLOR_ATTACHMENT0+qt),L.depthBuffer&&gt.push(Ht);const ie=Rt.__ignoreDepthValues!==void 0?Rt.__ignoreDepthValues:!1;if(ie===!1&&(L.depthBuffer&&(vt|=o.DEPTH_BUFFER_BIT),L.stencilBuffer&&(vt|=o.STENCIL_BUFFER_BIT)),Ut&&o.framebufferRenderbuffer(o.READ_FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.RENDERBUFFER,Rt.__webglColorRenderbuffer[qt]),ie===!0&&(o.invalidateFramebuffer(o.READ_FRAMEBUFFER,[Ht]),o.invalidateFramebuffer(o.DRAW_FRAMEBUFFER,[Ht])),Ut){const _t=s.get(A[qt]).__webglTexture;o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0,o.TEXTURE_2D,_t,0)}o.blitFramebuffer(0,0,nt,St,0,0,nt,St,vt,o.NEAREST),p&&o.invalidateFramebuffer(o.READ_FRAMEBUFFER,gt)}if(i.bindFramebuffer(o.READ_FRAMEBUFFER,null),i.bindFramebuffer(o.DRAW_FRAMEBUFFER,null),Ut)for(let qt=0;qt<A.length;qt++){i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglMultisampledFramebuffer),o.framebufferRenderbuffer(o.FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.RENDERBUFFER,Rt.__webglColorRenderbuffer[qt]);const ie=s.get(A[qt]).__webglTexture;i.bindFramebuffer(o.FRAMEBUFFER,Rt.__webglFramebuffer),o.framebufferTexture2D(o.DRAW_FRAMEBUFFER,o.COLOR_ATTACHMENT0+qt,o.TEXTURE_2D,ie,0)}i.bindFramebuffer(o.DRAW_FRAMEBUFFER,Rt.__webglMultisampledFramebuffer)}}function Qt(L){return Math.min(l.maxSamples,L.samples)}function Pt(L){const A=s.get(L);return h&&L.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&A.__useRenderToTexture!==!1}function Pe(L){const A=d.render.frame;g.get(L)!==A&&(g.set(L,A),L.update())}function ee(L,A){const nt=L.colorSpace,St=L.format,vt=L.type;return L.isCompressedTexture===!0||L.isVideoTexture===!0||L.format===yh||nt!==Ji&&nt!==oi&&(Ue.getTransfer(nt)===Fe?h===!1?e.has("EXT_sRGB")===!0&&St===vi?(L.format=yh,L.minFilter=si,L.generateMipmaps=!1):A=mv.sRGBToLinear(A):(St!==vi||vt!==Ba)&&console.warn("THREE.WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):console.error("THREE.WebGLTextures: Unsupported texture color space:",nt)),A}this.allocateTextureUnit=V,this.resetTextureUnits=Et,this.setTexture2D=O,this.setTexture2DArray=k,this.setTexture3D=Q,this.setTextureCube=ot,this.rebindTextures=ue,this.setupRenderTarget=tt,this.updateRenderTargetMipmap=ln,this.updateMultisampleRenderTarget=Ft,this.setupDepthRenderbuffer=kt,this.setupFrameBufferTexture=xt,this.useMultisampledRTT=Pt}function iA(o,e,i){const s=i.isWebGL2;function l(c,d=oi){let h;const m=Ue.getTransfer(d);if(c===Ba)return o.UNSIGNED_BYTE;if(c===rv)return o.UNSIGNED_SHORT_4_4_4_4;if(c===sv)return o.UNSIGNED_SHORT_5_5_5_1;if(c===IM)return o.BYTE;if(c===FM)return o.SHORT;if(c===Rh)return o.UNSIGNED_SHORT;if(c===av)return o.INT;if(c===Ua)return o.UNSIGNED_INT;if(c===Na)return o.FLOAT;if(c===Ao)return s?o.HALF_FLOAT:(h=e.get("OES_texture_half_float"),h!==null?h.HALF_FLOAT_OES:null);if(c===HM)return o.ALPHA;if(c===vi)return o.RGBA;if(c===GM)return o.LUMINANCE;if(c===VM)return o.LUMINANCE_ALPHA;if(c===hr)return o.DEPTH_COMPONENT;if(c===_s)return o.DEPTH_STENCIL;if(c===yh)return h=e.get("EXT_sRGB"),h!==null?h.SRGB_ALPHA_EXT:null;if(c===XM)return o.RED;if(c===ov)return o.RED_INTEGER;if(c===WM)return o.RG;if(c===lv)return o.RG_INTEGER;if(c===uv)return o.RGBA_INTEGER;if(c===Pf||c===Bf||c===If||c===Ff)if(m===Fe)if(h=e.get("WEBGL_compressed_texture_s3tc_srgb"),h!==null){if(c===Pf)return h.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(c===Bf)return h.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(c===If)return h.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(c===Ff)return h.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(h=e.get("WEBGL_compressed_texture_s3tc"),h!==null){if(c===Pf)return h.COMPRESSED_RGB_S3TC_DXT1_EXT;if(c===Bf)return h.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(c===If)return h.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(c===Ff)return h.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(c===zg||c===Pg||c===Bg||c===Ig)if(h=e.get("WEBGL_compressed_texture_pvrtc"),h!==null){if(c===zg)return h.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(c===Pg)return h.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(c===Bg)return h.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(c===Ig)return h.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(c===cv)return h=e.get("WEBGL_compressed_texture_etc1"),h!==null?h.COMPRESSED_RGB_ETC1_WEBGL:null;if(c===Fg||c===Hg)if(h=e.get("WEBGL_compressed_texture_etc"),h!==null){if(c===Fg)return m===Fe?h.COMPRESSED_SRGB8_ETC2:h.COMPRESSED_RGB8_ETC2;if(c===Hg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:h.COMPRESSED_RGBA8_ETC2_EAC}else return null;if(c===Gg||c===Vg||c===Xg||c===Wg||c===kg||c===qg||c===Yg||c===jg||c===Zg||c===Kg||c===Qg||c===Jg||c===$g||c===t_)if(h=e.get("WEBGL_compressed_texture_astc"),h!==null){if(c===Gg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:h.COMPRESSED_RGBA_ASTC_4x4_KHR;if(c===Vg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:h.COMPRESSED_RGBA_ASTC_5x4_KHR;if(c===Xg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:h.COMPRESSED_RGBA_ASTC_5x5_KHR;if(c===Wg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:h.COMPRESSED_RGBA_ASTC_6x5_KHR;if(c===kg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:h.COMPRESSED_RGBA_ASTC_6x6_KHR;if(c===qg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:h.COMPRESSED_RGBA_ASTC_8x5_KHR;if(c===Yg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:h.COMPRESSED_RGBA_ASTC_8x6_KHR;if(c===jg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:h.COMPRESSED_RGBA_ASTC_8x8_KHR;if(c===Zg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:h.COMPRESSED_RGBA_ASTC_10x5_KHR;if(c===Kg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:h.COMPRESSED_RGBA_ASTC_10x6_KHR;if(c===Qg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:h.COMPRESSED_RGBA_ASTC_10x8_KHR;if(c===Jg)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:h.COMPRESSED_RGBA_ASTC_10x10_KHR;if(c===$g)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:h.COMPRESSED_RGBA_ASTC_12x10_KHR;if(c===t_)return m===Fe?h.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:h.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(c===Hf||c===e_||c===n_)if(h=e.get("EXT_texture_compression_bptc"),h!==null){if(c===Hf)return m===Fe?h.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:h.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(c===e_)return h.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(c===n_)return h.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(c===kM||c===i_||c===a_||c===r_)if(h=e.get("EXT_texture_compression_rgtc"),h!==null){if(c===Hf)return h.COMPRESSED_RED_RGTC1_EXT;if(c===i_)return h.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(c===a_)return h.COMPRESSED_RED_GREEN_RGTC2_EXT;if(c===r_)return h.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return c===fr?s?o.UNSIGNED_INT_24_8:(h=e.get("WEBGL_depth_texture"),h!==null?h.UNSIGNED_INT_24_8_WEBGL:null):o[c]!==void 0?o[c]:null}return{convert:l}}class aA extends gi{constructor(e=[]){super(),this.isArrayCamera=!0,this.cameras=e}}class cu extends Tn{constructor(){super(),this.isGroup=!0,this.type="Group"}}const rA={type:"move"};class ch{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new cu,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new cu,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new at,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new at),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new cu,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new at,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new at),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){const i=this._hand;if(i)for(const s of e.hand.values())this._getHandJoint(i,s)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,i,s){let l=null,c=null,d=null;const h=this._targetRay,m=this._grip,p=this._hand;if(e&&i.session.visibilityState!=="visible-blurred"){if(p&&e.hand){d=!0;for(const T of e.hand.values()){const x=i.getJointPose(T,s),v=this._getHandJoint(p,T);x!==null&&(v.matrix.fromArray(x.transform.matrix),v.matrix.decompose(v.position,v.rotation,v.scale),v.matrixWorldNeedsUpdate=!0,v.jointRadius=x.radius),v.visible=x!==null}const g=p.joints["index-finger-tip"],_=p.joints["thumb-tip"],M=g.position.distanceTo(_.position),y=.02,b=.005;p.inputState.pinching&&M>y+b?(p.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!p.inputState.pinching&&M<=y-b&&(p.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else m!==null&&e.gripSpace&&(c=i.getPose(e.gripSpace,s),c!==null&&(m.matrix.fromArray(c.transform.matrix),m.matrix.decompose(m.position,m.rotation,m.scale),m.matrixWorldNeedsUpdate=!0,c.linearVelocity?(m.hasLinearVelocity=!0,m.linearVelocity.copy(c.linearVelocity)):m.hasLinearVelocity=!1,c.angularVelocity?(m.hasAngularVelocity=!0,m.angularVelocity.copy(c.angularVelocity)):m.hasAngularVelocity=!1));h!==null&&(l=i.getPose(e.targetRaySpace,s),l===null&&c!==null&&(l=c),l!==null&&(h.matrix.fromArray(l.transform.matrix),h.matrix.decompose(h.position,h.rotation,h.scale),h.matrixWorldNeedsUpdate=!0,l.linearVelocity?(h.hasLinearVelocity=!0,h.linearVelocity.copy(l.linearVelocity)):h.hasLinearVelocity=!1,l.angularVelocity?(h.hasAngularVelocity=!0,h.angularVelocity.copy(l.angularVelocity)):h.hasAngularVelocity=!1,this.dispatchEvent(rA)))}return h!==null&&(h.visible=l!==null),m!==null&&(m.visible=c!==null),p!==null&&(p.visible=d!==null),this}_getHandJoint(e,i){if(e.joints[i.jointName]===void 0){const s=new cu;s.matrixAutoUpdate=!1,s.visible=!1,e.joints[i.jointName]=s,e.add(s)}return e.joints[i.jointName]}}class sA extends Ss{constructor(e,i){super();const s=this;let l=null,c=1,d=null,h="local-floor",m=1,p=null,g=null,_=null,M=null,y=null,b=null;const T=i.getContextAttributes();let x=null,v=null;const N=[],R=[],I=new xe;let q=null;const B=new gi;B.layers.enable(1),B.viewport=new hn;const z=new gi;z.layers.enable(2),z.viewport=new hn;const dt=[B,z],w=new aA;w.layers.enable(1),w.layers.enable(2);let U=null,lt=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(G){let Z=N[G];return Z===void 0&&(Z=new ch,N[G]=Z),Z.getTargetRaySpace()},this.getControllerGrip=function(G){let Z=N[G];return Z===void 0&&(Z=new ch,N[G]=Z),Z.getGripSpace()},this.getHand=function(G){let Z=N[G];return Z===void 0&&(Z=new ch,N[G]=Z),Z.getHandSpace()};function mt(G){const Z=R.indexOf(G.inputSource);if(Z===-1)return;const pt=N[Z];pt!==void 0&&(pt.update(G.inputSource,G.frame,p||d),pt.dispatchEvent({type:G.type,data:G.inputSource}))}function Et(){l.removeEventListener("select",mt),l.removeEventListener("selectstart",mt),l.removeEventListener("selectend",mt),l.removeEventListener("squeeze",mt),l.removeEventListener("squeezestart",mt),l.removeEventListener("squeezeend",mt),l.removeEventListener("end",Et),l.removeEventListener("inputsourceschange",V);for(let G=0;G<N.length;G++){const Z=R[G];Z!==null&&(R[G]=null,N[G].disconnect(Z))}U=null,lt=null,e.setRenderTarget(x),y=null,M=null,_=null,l=null,v=null,X.stop(),s.isPresenting=!1,e.setPixelRatio(q),e.setSize(I.width,I.height,!1),s.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(G){c=G,s.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(G){h=G,s.isPresenting===!0&&console.warn("THREE.WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return p||d},this.setReferenceSpace=function(G){p=G},this.getBaseLayer=function(){return M!==null?M:y},this.getBinding=function(){return _},this.getFrame=function(){return b},this.getSession=function(){return l},this.setSession=async function(G){if(l=G,l!==null){if(x=e.getRenderTarget(),l.addEventListener("select",mt),l.addEventListener("selectstart",mt),l.addEventListener("selectend",mt),l.addEventListener("squeeze",mt),l.addEventListener("squeezestart",mt),l.addEventListener("squeezeend",mt),l.addEventListener("end",Et),l.addEventListener("inputsourceschange",V),T.xrCompatible!==!0&&await i.makeXRCompatible(),q=e.getPixelRatio(),e.getSize(I),l.renderState.layers===void 0||e.capabilities.isWebGL2===!1){const Z={antialias:l.renderState.layers===void 0?T.antialias:!0,alpha:!0,depth:T.depth,stencil:T.stencil,framebufferScaleFactor:c};y=new XRWebGLLayer(l,i,Z),l.updateRenderState({baseLayer:y}),e.setPixelRatio(1),e.setSize(y.framebufferWidth,y.framebufferHeight,!1),v=new pr(y.framebufferWidth,y.framebufferHeight,{format:vi,type:Ba,colorSpace:e.outputColorSpace,stencilBuffer:T.stencil})}else{let Z=null,pt=null,Mt=null;T.depth&&(Mt=T.stencil?i.DEPTH24_STENCIL8:i.DEPTH_COMPONENT24,Z=T.stencil?_s:hr,pt=T.stencil?fr:Ua);const xt={colorFormat:i.RGBA8,depthFormat:Mt,scaleFactor:c};_=new XRWebGLBinding(l,i),M=_.createProjectionLayer(xt),l.updateRenderState({layers:[M]}),e.setPixelRatio(1),e.setSize(M.textureWidth,M.textureHeight,!1),v=new pr(M.textureWidth,M.textureHeight,{format:vi,type:Ba,depthTexture:new Cv(M.textureWidth,M.textureHeight,pt,void 0,void 0,void 0,void 0,void 0,void 0,Z),stencilBuffer:T.stencil,colorSpace:e.outputColorSpace,samples:T.antialias?4:0});const It=e.properties.get(v);It.__ignoreDepthValues=M.ignoreDepthValues}v.isXRRenderTarget=!0,this.setFoveation(m),p=null,d=await l.requestReferenceSpace(h),X.setContext(l),X.start(),s.isPresenting=!0,s.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(l!==null)return l.environmentBlendMode};function V(G){for(let Z=0;Z<G.removed.length;Z++){const pt=G.removed[Z],Mt=R.indexOf(pt);Mt>=0&&(R[Mt]=null,N[Mt].disconnect(pt))}for(let Z=0;Z<G.added.length;Z++){const pt=G.added[Z];let Mt=R.indexOf(pt);if(Mt===-1){for(let It=0;It<N.length;It++)if(It>=R.length){R.push(pt),Mt=It;break}else if(R[It]===null){R[It]=pt,Mt=It;break}if(Mt===-1)break}const xt=N[Mt];xt&&xt.connect(pt)}}const $=new at,O=new at;function k(G,Z,pt){$.setFromMatrixPosition(Z.matrixWorld),O.setFromMatrixPosition(pt.matrixWorld);const Mt=$.distanceTo(O),xt=Z.projectionMatrix.elements,It=pt.projectionMatrix.elements,Nt=xt[14]/(xt[10]-1),kt=xt[14]/(xt[10]+1),ue=(xt[9]+1)/xt[5],tt=(xt[9]-1)/xt[5],ln=(xt[8]-1)/xt[0],Ft=(It[8]+1)/It[0],Qt=Nt*ln,Pt=Nt*Ft,Pe=Mt/(-ln+Ft),ee=Pe*-ln;Z.matrixWorld.decompose(G.position,G.quaternion,G.scale),G.translateX(ee),G.translateZ(Pe),G.matrixWorld.compose(G.position,G.quaternion,G.scale),G.matrixWorldInverse.copy(G.matrixWorld).invert();const L=Nt+Pe,A=kt+Pe,nt=Qt-ee,St=Pt+(Mt-ee),vt=ue*kt/A*L,gt=tt*kt/A*L;G.projectionMatrix.makePerspective(nt,St,vt,gt,L,A),G.projectionMatrixInverse.copy(G.projectionMatrix).invert()}function Q(G,Z){Z===null?G.matrixWorld.copy(G.matrix):G.matrixWorld.multiplyMatrices(Z.matrixWorld,G.matrix),G.matrixWorldInverse.copy(G.matrixWorld).invert()}this.updateCamera=function(G){if(l===null)return;w.near=z.near=B.near=G.near,w.far=z.far=B.far=G.far,(U!==w.near||lt!==w.far)&&(l.updateRenderState({depthNear:w.near,depthFar:w.far}),U=w.near,lt=w.far);const Z=G.parent,pt=w.cameras;Q(w,Z);for(let Mt=0;Mt<pt.length;Mt++)Q(pt[Mt],Z);pt.length===2?k(w,B,z):w.projectionMatrix.copy(B.projectionMatrix),ot(G,w,Z)};function ot(G,Z,pt){pt===null?G.matrix.copy(Z.matrixWorld):(G.matrix.copy(pt.matrixWorld),G.matrix.invert(),G.matrix.multiply(Z.matrixWorld)),G.matrix.decompose(G.position,G.quaternion,G.scale),G.updateMatrixWorld(!0),G.projectionMatrix.copy(Z.projectionMatrix),G.projectionMatrixInverse.copy(Z.projectionMatrixInverse),G.isPerspectiveCamera&&(G.fov=Eh*2*Math.atan(1/G.projectionMatrix.elements[5]),G.zoom=1)}this.getCamera=function(){return w},this.getFoveation=function(){if(!(M===null&&y===null))return m},this.setFoveation=function(G){m=G,M!==null&&(M.fixedFoveation=G),y!==null&&y.fixedFoveation!==void 0&&(y.fixedFoveation=G)};let ct=null;function D(G,Z){if(g=Z.getViewerPose(p||d),b=Z,g!==null){const pt=g.views;y!==null&&(e.setRenderTargetFramebuffer(v,y.framebuffer),e.setRenderTarget(v));let Mt=!1;pt.length!==w.cameras.length&&(w.cameras.length=0,Mt=!0);for(let xt=0;xt<pt.length;xt++){const It=pt[xt];let Nt=null;if(y!==null)Nt=y.getViewport(It);else{const ue=_.getViewSubImage(M,It);Nt=ue.viewport,xt===0&&(e.setRenderTargetTextures(v,ue.colorTexture,M.ignoreDepthValues?void 0:ue.depthStencilTexture),e.setRenderTarget(v))}let kt=dt[xt];kt===void 0&&(kt=new gi,kt.layers.enable(xt),kt.viewport=new hn,dt[xt]=kt),kt.matrix.fromArray(It.transform.matrix),kt.matrix.decompose(kt.position,kt.quaternion,kt.scale),kt.projectionMatrix.fromArray(It.projectionMatrix),kt.projectionMatrixInverse.copy(kt.projectionMatrix).invert(),kt.viewport.set(Nt.x,Nt.y,Nt.width,Nt.height),xt===0&&(w.matrix.copy(kt.matrix),w.matrix.decompose(w.position,w.quaternion,w.scale)),Mt===!0&&w.cameras.push(kt)}}for(let pt=0;pt<N.length;pt++){const Mt=R[pt],xt=N[pt];Mt!==null&&xt!==void 0&&xt.update(Mt,Z,p||d)}ct&&ct(G,Z),Z.detectedPlanes&&s.dispatchEvent({type:"planesdetected",data:Z}),b=null}const X=new Av;X.setAnimationLoop(D),this.setAnimationLoop=function(G){ct=G},this.dispose=function(){}}}function oA(o,e){function i(x,v){x.matrixAutoUpdate===!0&&x.updateMatrix(),v.value.copy(x.matrix)}function s(x,v){v.color.getRGB(x.fogColor.value,Ev(o)),v.isFog?(x.fogNear.value=v.near,x.fogFar.value=v.far):v.isFogExp2&&(x.fogDensity.value=v.density)}function l(x,v,N,R,I){v.isMeshBasicMaterial||v.isMeshLambertMaterial?c(x,v):v.isMeshToonMaterial?(c(x,v),_(x,v)):v.isMeshPhongMaterial?(c(x,v),g(x,v)):v.isMeshStandardMaterial?(c(x,v),M(x,v),v.isMeshPhysicalMaterial&&y(x,v,I)):v.isMeshMatcapMaterial?(c(x,v),b(x,v)):v.isMeshDepthMaterial?c(x,v):v.isMeshDistanceMaterial?(c(x,v),T(x,v)):v.isMeshNormalMaterial?c(x,v):v.isLineBasicMaterial?(d(x,v),v.isLineDashedMaterial&&h(x,v)):v.isPointsMaterial?m(x,v,N,R):v.isSpriteMaterial?p(x,v):v.isShadowMaterial?(x.color.value.copy(v.color),x.opacity.value=v.opacity):v.isShaderMaterial&&(v.uniformsNeedUpdate=!1)}function c(x,v){x.opacity.value=v.opacity,v.color&&x.diffuse.value.copy(v.color),v.emissive&&x.emissive.value.copy(v.emissive).multiplyScalar(v.emissiveIntensity),v.map&&(x.map.value=v.map,i(v.map,x.mapTransform)),v.alphaMap&&(x.alphaMap.value=v.alphaMap,i(v.alphaMap,x.alphaMapTransform)),v.bumpMap&&(x.bumpMap.value=v.bumpMap,i(v.bumpMap,x.bumpMapTransform),x.bumpScale.value=v.bumpScale,v.side===In&&(x.bumpScale.value*=-1)),v.normalMap&&(x.normalMap.value=v.normalMap,i(v.normalMap,x.normalMapTransform),x.normalScale.value.copy(v.normalScale),v.side===In&&x.normalScale.value.negate()),v.displacementMap&&(x.displacementMap.value=v.displacementMap,i(v.displacementMap,x.displacementMapTransform),x.displacementScale.value=v.displacementScale,x.displacementBias.value=v.displacementBias),v.emissiveMap&&(x.emissiveMap.value=v.emissiveMap,i(v.emissiveMap,x.emissiveMapTransform)),v.specularMap&&(x.specularMap.value=v.specularMap,i(v.specularMap,x.specularMapTransform)),v.alphaTest>0&&(x.alphaTest.value=v.alphaTest);const N=e.get(v).envMap;if(N&&(x.envMap.value=N,x.flipEnvMap.value=N.isCubeTexture&&N.isRenderTargetTexture===!1?-1:1,x.reflectivity.value=v.reflectivity,x.ior.value=v.ior,x.refractionRatio.value=v.refractionRatio),v.lightMap){x.lightMap.value=v.lightMap;const R=o._useLegacyLights===!0?Math.PI:1;x.lightMapIntensity.value=v.lightMapIntensity*R,i(v.lightMap,x.lightMapTransform)}v.aoMap&&(x.aoMap.value=v.aoMap,x.aoMapIntensity.value=v.aoMapIntensity,i(v.aoMap,x.aoMapTransform))}function d(x,v){x.diffuse.value.copy(v.color),x.opacity.value=v.opacity,v.map&&(x.map.value=v.map,i(v.map,x.mapTransform))}function h(x,v){x.dashSize.value=v.dashSize,x.totalSize.value=v.dashSize+v.gapSize,x.scale.value=v.scale}function m(x,v,N,R){x.diffuse.value.copy(v.color),x.opacity.value=v.opacity,x.size.value=v.size*N,x.scale.value=R*.5,v.map&&(x.map.value=v.map,i(v.map,x.uvTransform)),v.alphaMap&&(x.alphaMap.value=v.alphaMap,i(v.alphaMap,x.alphaMapTransform)),v.alphaTest>0&&(x.alphaTest.value=v.alphaTest)}function p(x,v){x.diffuse.value.copy(v.color),x.opacity.value=v.opacity,x.rotation.value=v.rotation,v.map&&(x.map.value=v.map,i(v.map,x.mapTransform)),v.alphaMap&&(x.alphaMap.value=v.alphaMap,i(v.alphaMap,x.alphaMapTransform)),v.alphaTest>0&&(x.alphaTest.value=v.alphaTest)}function g(x,v){x.specular.value.copy(v.specular),x.shininess.value=Math.max(v.shininess,1e-4)}function _(x,v){v.gradientMap&&(x.gradientMap.value=v.gradientMap)}function M(x,v){x.metalness.value=v.metalness,v.metalnessMap&&(x.metalnessMap.value=v.metalnessMap,i(v.metalnessMap,x.metalnessMapTransform)),x.roughness.value=v.roughness,v.roughnessMap&&(x.roughnessMap.value=v.roughnessMap,i(v.roughnessMap,x.roughnessMapTransform)),e.get(v).envMap&&(x.envMapIntensity.value=v.envMapIntensity)}function y(x,v,N){x.ior.value=v.ior,v.sheen>0&&(x.sheenColor.value.copy(v.sheenColor).multiplyScalar(v.sheen),x.sheenRoughness.value=v.sheenRoughness,v.sheenColorMap&&(x.sheenColorMap.value=v.sheenColorMap,i(v.sheenColorMap,x.sheenColorMapTransform)),v.sheenRoughnessMap&&(x.sheenRoughnessMap.value=v.sheenRoughnessMap,i(v.sheenRoughnessMap,x.sheenRoughnessMapTransform))),v.clearcoat>0&&(x.clearcoat.value=v.clearcoat,x.clearcoatRoughness.value=v.clearcoatRoughness,v.clearcoatMap&&(x.clearcoatMap.value=v.clearcoatMap,i(v.clearcoatMap,x.clearcoatMapTransform)),v.clearcoatRoughnessMap&&(x.clearcoatRoughnessMap.value=v.clearcoatRoughnessMap,i(v.clearcoatRoughnessMap,x.clearcoatRoughnessMapTransform)),v.clearcoatNormalMap&&(x.clearcoatNormalMap.value=v.clearcoatNormalMap,i(v.clearcoatNormalMap,x.clearcoatNormalMapTransform),x.clearcoatNormalScale.value.copy(v.clearcoatNormalScale),v.side===In&&x.clearcoatNormalScale.value.negate())),v.iridescence>0&&(x.iridescence.value=v.iridescence,x.iridescenceIOR.value=v.iridescenceIOR,x.iridescenceThicknessMinimum.value=v.iridescenceThicknessRange[0],x.iridescenceThicknessMaximum.value=v.iridescenceThicknessRange[1],v.iridescenceMap&&(x.iridescenceMap.value=v.iridescenceMap,i(v.iridescenceMap,x.iridescenceMapTransform)),v.iridescenceThicknessMap&&(x.iridescenceThicknessMap.value=v.iridescenceThicknessMap,i(v.iridescenceThicknessMap,x.iridescenceThicknessMapTransform))),v.transmission>0&&(x.transmission.value=v.transmission,x.transmissionSamplerMap.value=N.texture,x.transmissionSamplerSize.value.set(N.width,N.height),v.transmissionMap&&(x.transmissionMap.value=v.transmissionMap,i(v.transmissionMap,x.transmissionMapTransform)),x.thickness.value=v.thickness,v.thicknessMap&&(x.thicknessMap.value=v.thicknessMap,i(v.thicknessMap,x.thicknessMapTransform)),x.attenuationDistance.value=v.attenuationDistance,x.attenuationColor.value.copy(v.attenuationColor)),v.anisotropy>0&&(x.anisotropyVector.value.set(v.anisotropy*Math.cos(v.anisotropyRotation),v.anisotropy*Math.sin(v.anisotropyRotation)),v.anisotropyMap&&(x.anisotropyMap.value=v.anisotropyMap,i(v.anisotropyMap,x.anisotropyMapTransform))),x.specularIntensity.value=v.specularIntensity,x.specularColor.value.copy(v.specularColor),v.specularColorMap&&(x.specularColorMap.value=v.specularColorMap,i(v.specularColorMap,x.specularColorMapTransform)),v.specularIntensityMap&&(x.specularIntensityMap.value=v.specularIntensityMap,i(v.specularIntensityMap,x.specularIntensityMapTransform))}function b(x,v){v.matcap&&(x.matcap.value=v.matcap)}function T(x,v){const N=e.get(v).light;x.referencePosition.value.setFromMatrixPosition(N.matrixWorld),x.nearDistance.value=N.shadow.camera.near,x.farDistance.value=N.shadow.camera.far}return{refreshFogUniforms:s,refreshMaterialUniforms:l}}function lA(o,e,i,s){let l={},c={},d=[];const h=i.isWebGL2?o.getParameter(o.MAX_UNIFORM_BUFFER_BINDINGS):0;function m(N,R){const I=R.program;s.uniformBlockBinding(N,I)}function p(N,R){let I=l[N.id];I===void 0&&(b(N),I=g(N),l[N.id]=I,N.addEventListener("dispose",x));const q=R.program;s.updateUBOMapping(N,q);const B=e.render.frame;c[N.id]!==B&&(M(N),c[N.id]=B)}function g(N){const R=_();N.__bindingPointIndex=R;const I=o.createBuffer(),q=N.__size,B=N.usage;return o.bindBuffer(o.UNIFORM_BUFFER,I),o.bufferData(o.UNIFORM_BUFFER,q,B),o.bindBuffer(o.UNIFORM_BUFFER,null),o.bindBufferBase(o.UNIFORM_BUFFER,R,I),I}function _(){for(let N=0;N<h;N++)if(d.indexOf(N)===-1)return d.push(N),N;return console.error("THREE.WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function M(N){const R=l[N.id],I=N.uniforms,q=N.__cache;o.bindBuffer(o.UNIFORM_BUFFER,R);for(let B=0,z=I.length;B<z;B++){const dt=Array.isArray(I[B])?I[B]:[I[B]];for(let w=0,U=dt.length;w<U;w++){const lt=dt[w];if(y(lt,B,w,q)===!0){const mt=lt.__offset,Et=Array.isArray(lt.value)?lt.value:[lt.value];let V=0;for(let $=0;$<Et.length;$++){const O=Et[$],k=T(O);typeof O=="number"||typeof O=="boolean"?(lt.__data[0]=O,o.bufferSubData(o.UNIFORM_BUFFER,mt+V,lt.__data)):O.isMatrix3?(lt.__data[0]=O.elements[0],lt.__data[1]=O.elements[1],lt.__data[2]=O.elements[2],lt.__data[3]=0,lt.__data[4]=O.elements[3],lt.__data[5]=O.elements[4],lt.__data[6]=O.elements[5],lt.__data[7]=0,lt.__data[8]=O.elements[6],lt.__data[9]=O.elements[7],lt.__data[10]=O.elements[8],lt.__data[11]=0):(O.toArray(lt.__data,V),V+=k.storage/Float32Array.BYTES_PER_ELEMENT)}o.bufferSubData(o.UNIFORM_BUFFER,mt,lt.__data)}}}o.bindBuffer(o.UNIFORM_BUFFER,null)}function y(N,R,I,q){const B=N.value,z=R+"_"+I;if(q[z]===void 0)return typeof B=="number"||typeof B=="boolean"?q[z]=B:q[z]=B.clone(),!0;{const dt=q[z];if(typeof B=="number"||typeof B=="boolean"){if(dt!==B)return q[z]=B,!0}else if(dt.equals(B)===!1)return dt.copy(B),!0}return!1}function b(N){const R=N.uniforms;let I=0;const q=16;for(let z=0,dt=R.length;z<dt;z++){const w=Array.isArray(R[z])?R[z]:[R[z]];for(let U=0,lt=w.length;U<lt;U++){const mt=w[U],Et=Array.isArray(mt.value)?mt.value:[mt.value];for(let V=0,$=Et.length;V<$;V++){const O=Et[V],k=T(O),Q=I%q;Q!==0&&q-Q<k.boundary&&(I+=q-Q),mt.__data=new Float32Array(k.storage/Float32Array.BYTES_PER_ELEMENT),mt.__offset=I,I+=k.storage}}}const B=I%q;return B>0&&(I+=q-B),N.__size=I,N.__cache={},this}function T(N){const R={boundary:0,storage:0};return typeof N=="number"||typeof N=="boolean"?(R.boundary=4,R.storage=4):N.isVector2?(R.boundary=8,R.storage=8):N.isVector3||N.isColor?(R.boundary=16,R.storage=12):N.isVector4?(R.boundary=16,R.storage=16):N.isMatrix3?(R.boundary=48,R.storage=48):N.isMatrix4?(R.boundary=64,R.storage=64):N.isTexture?console.warn("THREE.WebGLRenderer: Texture samplers can not be part of an uniforms group."):console.warn("THREE.WebGLRenderer: Unsupported uniform value type.",N),R}function x(N){const R=N.target;R.removeEventListener("dispose",x);const I=d.indexOf(R.__bindingPointIndex);d.splice(I,1),o.deleteBuffer(l[R.id]),delete l[R.id],delete c[R.id]}function v(){for(const N in l)o.deleteBuffer(l[N]);d=[],l={},c={}}return{bind:m,update:p,dispose:v}}class uA{constructor(e={}){const{canvas:i=ix(),context:s=null,depth:l=!0,stencil:c=!0,alpha:d=!1,antialias:h=!1,premultipliedAlpha:m=!0,preserveDrawingBuffer:p=!1,powerPreference:g="default",failIfMajorPerformanceCaveat:_=!1}=e;this.isWebGLRenderer=!0;let M;s!==null?M=s.getContextAttributes().alpha:M=d;const y=new Uint32Array(4),b=new Int32Array(4);let T=null,x=null;const v=[],N=[];this.domElement=i,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this._outputColorSpace=vn,this._useLegacyLights=!1,this.toneMapping=Pa,this.toneMappingExposure=1;const R=this;let I=!1,q=0,B=0,z=null,dt=-1,w=null;const U=new hn,lt=new hn;let mt=null;const Et=new Me(0);let V=0,$=i.width,O=i.height,k=1,Q=null,ot=null;const ct=new hn(0,0,$,O),D=new hn(0,0,$,O);let X=!1;const G=new Dh;let Z=!1,pt=!1,Mt=null;const xt=new rn,It=new xe,Nt=new at,kt={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0};function ue(){return z===null?k:1}let tt=s;function ln(C,Y){for(let it=0;it<C.length;it++){const rt=C[it],et=i.getContext(rt,Y);if(et!==null)return et}return null}try{const C={alpha:!0,depth:l,stencil:c,antialias:h,premultipliedAlpha:m,preserveDrawingBuffer:p,powerPreference:g,failIfMajorPerformanceCaveat:_};if("setAttribute"in i&&i.setAttribute("data-engine",`three.js r${Ah}`),i.addEventListener("webglcontextlost",yt,!1),i.addEventListener("webglcontextrestored",F,!1),i.addEventListener("webglcontextcreationerror",At,!1),tt===null){const Y=["webgl2","webgl","experimental-webgl"];if(R.isWebGL1Renderer===!0&&Y.shift(),tt=ln(Y,C),tt===null)throw ln(Y)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}typeof WebGLRenderingContext<"u"&&tt instanceof WebGLRenderingContext&&console.warn("THREE.WebGLRenderer: WebGL 1 support was deprecated in r153 and will be removed in r163."),tt.getShaderPrecisionFormat===void 0&&(tt.getShaderPrecisionFormat=function(){return{rangeMin:1,rangeMax:1,precision:1}})}catch(C){throw console.error("THREE.WebGLRenderer: "+C.message),C}let Ft,Qt,Pt,Pe,ee,L,A,nt,St,vt,gt,Ht,Rt,Ut,qt,ie,_t,ye,le,Kt,Dt,wt,Xt,ve;function He(){Ft=new vT(tt),Qt=new hT(tt,Ft,e),Ft.init(Qt),wt=new iA(tt,Ft,Qt),Pt=new eA(tt,Ft,Qt),Pe=new xT(tt),ee=new Gb,L=new nA(tt,Ft,Pt,ee,Qt,wt,Pe),A=new pT(R),nt=new _T(R),St=new wx(tt,Qt),Xt=new cT(tt,Ft,St,Qt),vt=new ST(tt,St,Pe,Xt),gt=new bT(tt,vt,St,Pe),le=new TT(tt,Qt,L),ie=new dT(ee),Ht=new Hb(R,A,nt,Ft,Qt,Xt,ie),Rt=new oA(R,ee),Ut=new Xb,qt=new Zb(Ft,Qt),ye=new uT(R,A,nt,Pt,gt,M,m),_t=new tA(R,gt,Qt),ve=new lA(tt,Pe,Qt,Pt),Kt=new fT(tt,Ft,Pe,Qt),Dt=new MT(tt,Ft,Pe,Qt),Pe.programs=Ht.programs,R.capabilities=Qt,R.extensions=Ft,R.properties=ee,R.renderLists=Ut,R.shadowMap=_t,R.state=Pt,R.info=Pe}He();const re=new sA(R,tt);this.xr=re,this.getContext=function(){return tt},this.getContextAttributes=function(){return tt.getContextAttributes()},this.forceContextLoss=function(){const C=Ft.get("WEBGL_lose_context");C&&C.loseContext()},this.forceContextRestore=function(){const C=Ft.get("WEBGL_lose_context");C&&C.restoreContext()},this.getPixelRatio=function(){return k},this.setPixelRatio=function(C){C!==void 0&&(k=C,this.setSize($,O,!1))},this.getSize=function(C){return C.set($,O)},this.setSize=function(C,Y,it=!0){if(re.isPresenting){console.warn("THREE.WebGLRenderer: Can't change size while VR device is presenting.");return}$=C,O=Y,i.width=Math.floor(C*k),i.height=Math.floor(Y*k),it===!0&&(i.style.width=C+"px",i.style.height=Y+"px"),this.setViewport(0,0,C,Y)},this.getDrawingBufferSize=function(C){return C.set($*k,O*k).floor()},this.setDrawingBufferSize=function(C,Y,it){$=C,O=Y,k=it,i.width=Math.floor(C*it),i.height=Math.floor(Y*it),this.setViewport(0,0,C,Y)},this.getCurrentViewport=function(C){return C.copy(U)},this.getViewport=function(C){return C.copy(ct)},this.setViewport=function(C,Y,it,rt){C.isVector4?ct.set(C.x,C.y,C.z,C.w):ct.set(C,Y,it,rt),Pt.viewport(U.copy(ct).multiplyScalar(k).floor())},this.getScissor=function(C){return C.copy(D)},this.setScissor=function(C,Y,it,rt){C.isVector4?D.set(C.x,C.y,C.z,C.w):D.set(C,Y,it,rt),Pt.scissor(lt.copy(D).multiplyScalar(k).floor())},this.getScissorTest=function(){return X},this.setScissorTest=function(C){Pt.setScissorTest(X=C)},this.setOpaqueSort=function(C){Q=C},this.setTransparentSort=function(C){ot=C},this.getClearColor=function(C){return C.copy(ye.getClearColor())},this.setClearColor=function(){ye.setClearColor.apply(ye,arguments)},this.getClearAlpha=function(){return ye.getClearAlpha()},this.setClearAlpha=function(){ye.setClearAlpha.apply(ye,arguments)},this.clear=function(C=!0,Y=!0,it=!0){let rt=0;if(C){let et=!1;if(z!==null){const Ct=z.texture.format;et=Ct===uv||Ct===lv||Ct===ov}if(et){const Ct=z.texture.type,Ot=Ct===Ba||Ct===Ua||Ct===Rh||Ct===fr||Ct===rv||Ct===sv,Wt=ye.getClearColor(),Yt=ye.getClearAlpha(),Bt=Wt.r,Jt=Wt.g,$t=Wt.b;Ot?(y[0]=Bt,y[1]=Jt,y[2]=$t,y[3]=Yt,tt.clearBufferuiv(tt.COLOR,0,y)):(b[0]=Bt,b[1]=Jt,b[2]=$t,b[3]=Yt,tt.clearBufferiv(tt.COLOR,0,b))}else rt|=tt.COLOR_BUFFER_BIT}Y&&(rt|=tt.DEPTH_BUFFER_BIT),it&&(rt|=tt.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),tt.clear(rt)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.dispose=function(){i.removeEventListener("webglcontextlost",yt,!1),i.removeEventListener("webglcontextrestored",F,!1),i.removeEventListener("webglcontextcreationerror",At,!1),Ut.dispose(),qt.dispose(),ee.dispose(),A.dispose(),nt.dispose(),gt.dispose(),Xt.dispose(),ve.dispose(),Ht.dispose(),re.dispose(),re.removeEventListener("sessionstart",ke),re.removeEventListener("sessionend",Ce),Mt&&(Mt.dispose(),Mt=null),un.stop()};function yt(C){C.preventDefault(),console.log("THREE.WebGLRenderer: Context Lost."),I=!0}function F(){console.log("THREE.WebGLRenderer: Context Restored."),I=!1;const C=Pe.autoReset,Y=_t.enabled,it=_t.autoUpdate,rt=_t.needsUpdate,et=_t.type;He(),Pe.autoReset=C,_t.enabled=Y,_t.autoUpdate=it,_t.needsUpdate=rt,_t.type=et}function At(C){console.error("THREE.WebGLRenderer: A WebGL context could not be created. Reason: ",C.statusMessage)}function Tt(C){const Y=C.target;Y.removeEventListener("dispose",Tt),jt(Y)}function jt(C){Gt(C),ee.remove(C)}function Gt(C){const Y=ee.get(C).programs;Y!==void 0&&(Y.forEach(function(it){Ht.releaseProgram(it)}),C.isShaderMaterial&&Ht.releaseShaderCache(C))}this.renderBufferDirect=function(C,Y,it,rt,et,Ct){Y===null&&(Y=kt);const Ot=et.isMesh&&et.matrixWorld.determinant()<0,Wt=Sn(C,Y,it,rt,et);Pt.setMaterial(rt,Ot);let Yt=it.index,Bt=1;if(rt.wireframe===!0){if(Yt=vt.getWireframeAttribute(it),Yt===void 0)return;Bt=2}const Jt=it.drawRange,$t=it.attributes.position;let Te=Jt.start*Bt,Ze=(Jt.start+Jt.count)*Bt;Ct!==null&&(Te=Math.max(Te,Ct.start*Bt),Ze=Math.min(Ze,(Ct.start+Ct.count)*Bt)),Yt!==null?(Te=Math.max(Te,0),Ze=Math.min(Ze,Yt.count)):$t!=null&&(Te=Math.max(Te,0),Ze=Math.min(Ze,$t.count));const Ke=Ze-Te;if(Ke<0||Ke===1/0)return;Xt.setup(et,rt,Wt,it,Yt);let Kn,ze=Kt;if(Yt!==null&&(Kn=St.get(Yt),ze=Dt,ze.setIndex(Kn)),et.isMesh)rt.wireframe===!0?(Pt.setLineWidth(rt.wireframeLinewidth*ue()),ze.setMode(tt.LINES)):ze.setMode(tt.TRIANGLES);else if(et.isLine){let se=rt.linewidth;se===void 0&&(se=1),Pt.setLineWidth(se*ue()),et.isLineSegments?ze.setMode(tt.LINES):et.isLineLoop?ze.setMode(tt.LINE_LOOP):ze.setMode(tt.LINE_STRIP)}else et.isPoints?ze.setMode(tt.POINTS):et.isSprite&&ze.setMode(tt.TRIANGLES);if(et.isBatchedMesh)ze.renderMultiDraw(et._multiDrawStarts,et._multiDrawCounts,et._multiDrawCount);else if(et.isInstancedMesh)ze.renderInstances(Te,Ke,et.count);else if(it.isInstancedBufferGeometry){const se=it._maxInstanceCount!==void 0?it._maxInstanceCount:1/0,ea=Math.min(it.instanceCount,se);ze.renderInstances(Te,Ke,ea)}else ze.render(Te,Ke)};function Re(C,Y,it){C.transparent===!0&&C.side===Ki&&C.forceSinglePass===!1?(C.side=In,C.needsUpdate=!0,Ha(C,Y,it),C.side=Ia,C.needsUpdate=!0,Ha(C,Y,it),C.side=Ki):Ha(C,Y,it)}this.compile=function(C,Y,it=null){it===null&&(it=C),x=qt.get(it),x.init(),N.push(x),it.traverseVisible(function(et){et.isLight&&et.layers.test(Y.layers)&&(x.pushLight(et),et.castShadow&&x.pushShadow(et))}),C!==it&&C.traverseVisible(function(et){et.isLight&&et.layers.test(Y.layers)&&(x.pushLight(et),et.castShadow&&x.pushShadow(et))}),x.setupLights(R._useLegacyLights);const rt=new Set;return C.traverse(function(et){const Ct=et.material;if(Ct)if(Array.isArray(Ct))for(let Ot=0;Ot<Ct.length;Ot++){const Wt=Ct[Ot];Re(Wt,it,et),rt.add(Wt)}else Re(Ct,it,et),rt.add(Ct)}),N.pop(),x=null,rt},this.compileAsync=function(C,Y,it=null){const rt=this.compile(C,Y,it);return new Promise(et=>{function Ct(){if(rt.forEach(function(Ot){ee.get(Ot).currentProgram.isReady()&&rt.delete(Ot)}),rt.size===0){et(C);return}setTimeout(Ct,10)}Ft.get("KHR_parallel_shader_compile")!==null?Ct():setTimeout(Ct,10)})};let Ee=null;function Ve(C){Ee&&Ee(C)}function ke(){un.stop()}function Ce(){un.start()}const un=new Av;un.setAnimationLoop(Ve),typeof self<"u"&&un.setContext(self),this.setAnimationLoop=function(C){Ee=C,re.setAnimationLoop(C),C===null?un.stop():un.start()},re.addEventListener("sessionstart",ke),re.addEventListener("sessionend",Ce),this.render=function(C,Y){if(Y!==void 0&&Y.isCamera!==!0){console.error("THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(I===!0)return;C.matrixWorldAutoUpdate===!0&&C.updateMatrixWorld(),Y.parent===null&&Y.matrixWorldAutoUpdate===!0&&Y.updateMatrixWorld(),re.enabled===!0&&re.isPresenting===!0&&(re.cameraAutoUpdate===!0&&re.updateCamera(Y),Y=re.getCamera()),C.isScene===!0&&C.onBeforeRender(R,C,Y,z),x=qt.get(C,N.length),x.init(),N.push(x),xt.multiplyMatrices(Y.projectionMatrix,Y.matrixWorldInverse),G.setFromProjectionMatrix(xt),pt=this.localClippingEnabled,Z=ie.init(this.clippingPlanes,pt),T=Ut.get(C,v.length),T.init(),v.push(T),Fn(C,Y,0,R.sortObjects),T.finish(),R.sortObjects===!0&&T.sort(Q,ot),this.info.render.frame++,Z===!0&&ie.beginShadows();const it=x.state.shadowsArray;if(_t.render(it,C,Y),Z===!0&&ie.endShadows(),this.info.autoReset===!0&&this.info.reset(),ye.render(T,C),x.setupLights(R._useLegacyLights),Y.isArrayCamera){const rt=Y.cameras;for(let et=0,Ct=rt.length;et<Ct;et++){const Ot=rt[et];xs(T,C,Ot,Ot.viewport)}}else xs(T,C,Y);z!==null&&(L.updateMultisampleRenderTarget(z),L.updateRenderTargetMipmap(z)),C.isScene===!0&&C.onAfterRender(R,C,Y),Xt.resetDefaultState(),dt=-1,w=null,N.pop(),N.length>0?x=N[N.length-1]:x=null,v.pop(),v.length>0?T=v[v.length-1]:T=null};function Fn(C,Y,it,rt){if(C.visible===!1)return;if(C.layers.test(Y.layers)){if(C.isGroup)it=C.renderOrder;else if(C.isLOD)C.autoUpdate===!0&&C.update(Y);else if(C.isLight)x.pushLight(C),C.castShadow&&x.pushShadow(C);else if(C.isSprite){if(!C.frustumCulled||G.intersectsSprite(C)){rt&&Nt.setFromMatrixPosition(C.matrixWorld).applyMatrix4(xt);const Ot=gt.update(C),Wt=C.material;Wt.visible&&T.push(C,Ot,Wt,it,Nt.z,null)}}else if((C.isMesh||C.isLine||C.isPoints)&&(!C.frustumCulled||G.intersectsObject(C))){const Ot=gt.update(C),Wt=C.material;if(rt&&(C.boundingSphere!==void 0?(C.boundingSphere===null&&C.computeBoundingSphere(),Nt.copy(C.boundingSphere.center)):(Ot.boundingSphere===null&&Ot.computeBoundingSphere(),Nt.copy(Ot.boundingSphere.center)),Nt.applyMatrix4(C.matrixWorld).applyMatrix4(xt)),Array.isArray(Wt)){const Yt=Ot.groups;for(let Bt=0,Jt=Yt.length;Bt<Jt;Bt++){const $t=Yt[Bt],Te=Wt[$t.materialIndex];Te&&Te.visible&&T.push(C,Ot,Te,it,Nt.z,$t)}}else Wt.visible&&T.push(C,Ot,Wt,it,Nt.z,null)}}const Ct=C.children;for(let Ot=0,Wt=Ct.length;Ot<Wt;Ot++)Fn(Ct[Ot],Y,it,rt)}function xs(C,Y,it,rt){const et=C.opaque,Ct=C.transmissive,Ot=C.transparent;x.setupLightsView(it),Z===!0&&ie.setGlobalState(R.clippingPlanes,it),Ct.length>0&&ys(et,Ct,Y,it),rt&&Pt.viewport(U.copy(rt)),et.length>0&&$i(et,Y,it),Ct.length>0&&$i(Ct,Y,it),Ot.length>0&&$i(Ot,Y,it),Pt.buffers.depth.setTest(!0),Pt.buffers.depth.setMask(!0),Pt.buffers.color.setMask(!0),Pt.setPolygonOffset(!1)}function ys(C,Y,it,rt){if((it.isScene===!0?it.overrideMaterial:null)!==null)return;const Ct=Qt.isWebGL2;Mt===null&&(Mt=new pr(1,1,{generateMipmaps:!0,type:Ft.has("EXT_color_buffer_half_float")?Ao:Ba,minFilter:bo,samples:Ct?4:0})),R.getDrawingBufferSize(It),Ct?Mt.setSize(It.x,It.y):Mt.setSize(Th(It.x),Th(It.y));const Ot=R.getRenderTarget();R.setRenderTarget(Mt),R.getClearColor(Et),V=R.getClearAlpha(),V<1&&R.setClearColor(16777215,.5),R.clear();const Wt=R.toneMapping;R.toneMapping=Pa,$i(C,it,rt),L.updateMultisampleRenderTarget(Mt),L.updateRenderTargetMipmap(Mt);let Yt=!1;for(let Bt=0,Jt=Y.length;Bt<Jt;Bt++){const $t=Y[Bt],Te=$t.object,Ze=$t.geometry,Ke=$t.material,Kn=$t.group;if(Ke.side===Ki&&Te.layers.test(rt.layers)){const ze=Ke.side;Ke.side=In,Ke.needsUpdate=!0,Es(Te,it,rt,Ze,Ke,Kn),Ke.side=ze,Ke.needsUpdate=!0,Yt=!0}}Yt===!0&&(L.updateMultisampleRenderTarget(Mt),L.updateRenderTargetMipmap(Mt)),R.setRenderTarget(Ot),R.setClearColor(Et,V),R.toneMapping=Wt}function $i(C,Y,it){const rt=Y.isScene===!0?Y.overrideMaterial:null;for(let et=0,Ct=C.length;et<Ct;et++){const Ot=C[et],Wt=Ot.object,Yt=Ot.geometry,Bt=rt===null?Ot.material:rt,Jt=Ot.group;Wt.layers.test(it.layers)&&Es(Wt,Y,it,Yt,Bt,Jt)}}function Es(C,Y,it,rt,et,Ct){C.onBeforeRender(R,Y,it,rt,et,Ct),C.modelViewMatrix.multiplyMatrices(it.matrixWorldInverse,C.matrixWorld),C.normalMatrix.getNormalMatrix(C.modelViewMatrix),et.onBeforeRender(R,Y,it,rt,C,Ct),et.transparent===!0&&et.side===Ki&&et.forceSinglePass===!1?(et.side=In,et.needsUpdate=!0,R.renderBufferDirect(it,Y,rt,et,C,Ct),et.side=Ia,et.needsUpdate=!0,R.renderBufferDirect(it,Y,rt,et,C,Ct),et.side=Ki):R.renderBufferDirect(it,Y,rt,et,C,Ct),C.onAfterRender(R,Y,it,rt,et,Ct)}function Ha(C,Y,it){Y.isScene!==!0&&(Y=kt);const rt=ee.get(C),et=x.state.lights,Ct=x.state.shadowsArray,Ot=et.state.version,Wt=Ht.getParameters(C,et.state,Ct,Y,it),Yt=Ht.getProgramCacheKey(Wt);let Bt=rt.programs;rt.environment=C.isMeshStandardMaterial?Y.environment:null,rt.fog=Y.fog,rt.envMap=(C.isMeshStandardMaterial?nt:A).get(C.envMap||rt.environment),Bt===void 0&&(C.addEventListener("dispose",Tt),Bt=new Map,rt.programs=Bt);let Jt=Bt.get(Yt);if(Jt!==void 0){if(rt.currentProgram===Jt&&rt.lightsStateVersion===Ot)return je(C,Wt),Jt}else Wt.uniforms=Ht.getUniforms(C),C.onBuild(it,Wt,R),C.onBeforeCompile(Wt,R),Jt=Ht.acquireProgram(Wt,Yt),Bt.set(Yt,Jt),rt.uniforms=Wt.uniforms;const $t=rt.uniforms;return(!C.isShaderMaterial&&!C.isRawShaderMaterial||C.clipping===!0)&&($t.clippingPlanes=ie.uniform),je(C,Wt),rt.needsLights=Ts(C),rt.lightsStateVersion=Ot,rt.needsLights&&($t.ambientLightColor.value=et.state.ambient,$t.lightProbe.value=et.state.probe,$t.directionalLights.value=et.state.directional,$t.directionalLightShadows.value=et.state.directionalShadow,$t.spotLights.value=et.state.spot,$t.spotLightShadows.value=et.state.spotShadow,$t.rectAreaLights.value=et.state.rectArea,$t.ltc_1.value=et.state.rectAreaLTC1,$t.ltc_2.value=et.state.rectAreaLTC2,$t.pointLights.value=et.state.point,$t.pointLightShadows.value=et.state.pointShadow,$t.hemisphereLights.value=et.state.hemi,$t.directionalShadowMap.value=et.state.directionalShadowMap,$t.directionalShadowMatrix.value=et.state.directionalShadowMatrix,$t.spotShadowMap.value=et.state.spotShadowMap,$t.spotLightMatrix.value=et.state.spotLightMatrix,$t.spotLightMap.value=et.state.spotLightMap,$t.pointShadowMap.value=et.state.pointShadowMap,$t.pointShadowMatrix.value=et.state.pointShadowMatrix),rt.currentProgram=Jt,rt.uniformsList=null,Jt}function li(C){if(C.uniformsList===null){const Y=C.currentProgram.getUniforms();C.uniformsList=hu.seqWithValue(Y.seq,C.uniforms)}return C.uniformsList}function je(C,Y){const it=ee.get(C);it.outputColorSpace=Y.outputColorSpace,it.batching=Y.batching,it.instancing=Y.instancing,it.instancingColor=Y.instancingColor,it.skinning=Y.skinning,it.morphTargets=Y.morphTargets,it.morphNormals=Y.morphNormals,it.morphColors=Y.morphColors,it.morphTargetsCount=Y.morphTargetsCount,it.numClippingPlanes=Y.numClippingPlanes,it.numIntersection=Y.numClipIntersection,it.vertexAlphas=Y.vertexAlphas,it.vertexTangents=Y.vertexTangents,it.toneMapping=Y.toneMapping}function Sn(C,Y,it,rt,et){Y.isScene!==!0&&(Y=kt),L.resetTextureUnits();const Ct=Y.fog,Ot=rt.isMeshStandardMaterial?Y.environment:null,Wt=z===null?R.outputColorSpace:z.isXRRenderTarget===!0?z.texture.colorSpace:Ji,Yt=(rt.isMeshStandardMaterial?nt:A).get(rt.envMap||Ot),Bt=rt.vertexColors===!0&&!!it.attributes.color&&it.attributes.color.itemSize===4,Jt=!!it.attributes.tangent&&(!!rt.normalMap||rt.anisotropy>0),$t=!!it.morphAttributes.position,Te=!!it.morphAttributes.normal,Ze=!!it.morphAttributes.color;let Ke=Pa;rt.toneMapped&&(z===null||z.isXRRenderTarget===!0)&&(Ke=R.toneMapping);const Kn=it.morphAttributes.position||it.morphAttributes.normal||it.morphAttributes.color,ze=Kn!==void 0?Kn.length:0,se=ee.get(rt),ea=x.state.lights;if(Z===!0&&(pt===!0||C!==w)){const Dn=C===w&&rt.id===dt;ie.setState(rt,C,Dn)}let Ne=!1;rt.version===se.__version?(se.needsLights&&se.lightsStateVersion!==ea.state.version||se.outputColorSpace!==Wt||et.isBatchedMesh&&se.batching===!1||!et.isBatchedMesh&&se.batching===!0||et.isInstancedMesh&&se.instancing===!1||!et.isInstancedMesh&&se.instancing===!0||et.isSkinnedMesh&&se.skinning===!1||!et.isSkinnedMesh&&se.skinning===!0||et.isInstancedMesh&&se.instancingColor===!0&&et.instanceColor===null||et.isInstancedMesh&&se.instancingColor===!1&&et.instanceColor!==null||se.envMap!==Yt||rt.fog===!0&&se.fog!==Ct||se.numClippingPlanes!==void 0&&(se.numClippingPlanes!==ie.numPlanes||se.numIntersection!==ie.numIntersection)||se.vertexAlphas!==Bt||se.vertexTangents!==Jt||se.morphTargets!==$t||se.morphNormals!==Te||se.morphColors!==Ze||se.toneMapping!==Ke||Qt.isWebGL2===!0&&se.morphTargetsCount!==ze)&&(Ne=!0):(Ne=!0,se.__version=rt.version);let dn=se.currentProgram;Ne===!0&&(dn=Ha(rt,Y,et));let bn=!1,na=!1,bs=!1;const Qe=dn.getUniforms(),Si=se.uniforms;if(Pt.useProgram(dn.program)&&(bn=!0,na=!0,bs=!0),rt.id!==dt&&(dt=rt.id,na=!0),bn||w!==C){Qe.setValue(tt,"projectionMatrix",C.projectionMatrix),Qe.setValue(tt,"viewMatrix",C.matrixWorldInverse);const Dn=Qe.map.cameraPosition;Dn!==void 0&&Dn.setValue(tt,Nt.setFromMatrixPosition(C.matrixWorld)),Qt.logarithmicDepthBuffer&&Qe.setValue(tt,"logDepthBufFC",2/(Math.log(C.far+1)/Math.LN2)),(rt.isMeshPhongMaterial||rt.isMeshToonMaterial||rt.isMeshLambertMaterial||rt.isMeshBasicMaterial||rt.isMeshStandardMaterial||rt.isShaderMaterial)&&Qe.setValue(tt,"isOrthographic",C.isOrthographicCamera===!0),w!==C&&(w=C,na=!0,bs=!0)}if(et.isSkinnedMesh){Qe.setOptional(tt,et,"bindMatrix"),Qe.setOptional(tt,et,"bindMatrixInverse");const Dn=et.skeleton;Dn&&(Qt.floatVertexTextures?(Dn.boneTexture===null&&Dn.computeBoneTexture(),Qe.setValue(tt,"boneTexture",Dn.boneTexture,L)):console.warn("THREE.WebGLRenderer: SkinnedMesh can only be used with WebGL 2. With WebGL 1 OES_texture_float and vertex textures support is required."))}et.isBatchedMesh&&(Qe.setOptional(tt,et,"batchingTexture"),Qe.setValue(tt,"batchingTexture",et._matricesTexture,L));const ia=it.morphAttributes;if((ia.position!==void 0||ia.normal!==void 0||ia.color!==void 0&&Qt.isWebGL2===!0)&&le.update(et,it,dn),(na||se.receiveShadow!==et.receiveShadow)&&(se.receiveShadow=et.receiveShadow,Qe.setValue(tt,"receiveShadow",et.receiveShadow)),rt.isMeshGouraudMaterial&&rt.envMap!==null&&(Si.envMap.value=Yt,Si.flipEnvMap.value=Yt.isCubeTexture&&Yt.isRenderTargetTexture===!1?-1:1),na&&(Qe.setValue(tt,"toneMappingExposure",R.toneMappingExposure),se.needsLights&&ta(Si,bs),Ct&&rt.fog===!0&&Rt.refreshFogUniforms(Si,Ct),Rt.refreshMaterialUniforms(Si,rt,k,O,Mt),hu.upload(tt,li(se),Si,L)),rt.isShaderMaterial&&rt.uniformsNeedUpdate===!0&&(hu.upload(tt,li(se),Si,L),rt.uniformsNeedUpdate=!1),rt.isSpriteMaterial&&Qe.setValue(tt,"center",et.center),Qe.setValue(tt,"modelViewMatrix",et.modelViewMatrix),Qe.setValue(tt,"normalMatrix",et.normalMatrix),Qe.setValue(tt,"modelMatrix",et.matrixWorld),rt.isShaderMaterial||rt.isRawShaderMaterial){const Dn=rt.uniformsGroups;for(let Mn=0,As=Dn.length;Mn<As;Mn++)if(Qt.isWebGL2){const Rs=Dn[Mn];ve.update(Rs,dn),ve.bind(Rs,dn)}else console.warn("THREE.WebGLRenderer: Uniform Buffer Objects can only be used with WebGL 2.")}return dn}function ta(C,Y){C.ambientLightColor.needsUpdate=Y,C.lightProbe.needsUpdate=Y,C.directionalLights.needsUpdate=Y,C.directionalLightShadows.needsUpdate=Y,C.pointLights.needsUpdate=Y,C.pointLightShadows.needsUpdate=Y,C.spotLights.needsUpdate=Y,C.spotLightShadows.needsUpdate=Y,C.rectAreaLights.needsUpdate=Y,C.hemisphereLights.needsUpdate=Y}function Ts(C){return C.isMeshLambertMaterial||C.isMeshToonMaterial||C.isMeshPhongMaterial||C.isMeshStandardMaterial||C.isShadowMaterial||C.isShaderMaterial&&C.lights===!0}this.getActiveCubeFace=function(){return q},this.getActiveMipmapLevel=function(){return B},this.getRenderTarget=function(){return z},this.setRenderTargetTextures=function(C,Y,it){ee.get(C.texture).__webglTexture=Y,ee.get(C.depthTexture).__webglTexture=it;const rt=ee.get(C);rt.__hasExternalTextures=!0,rt.__hasExternalTextures&&(rt.__autoAllocateDepthBuffer=it===void 0,rt.__autoAllocateDepthBuffer||Ft.has("WEBGL_multisampled_render_to_texture")===!0&&(console.warn("THREE.WebGLRenderer: Render-to-texture extension was disabled because an external texture was provided"),rt.__useRenderToTexture=!1))},this.setRenderTargetFramebuffer=function(C,Y){const it=ee.get(C);it.__webglFramebuffer=Y,it.__useDefaultFramebuffer=Y===void 0},this.setRenderTarget=function(C,Y=0,it=0){z=C,q=Y,B=it;let rt=!0,et=null,Ct=!1,Ot=!1;if(C){const Yt=ee.get(C);Yt.__useDefaultFramebuffer!==void 0?(Pt.bindFramebuffer(tt.FRAMEBUFFER,null),rt=!1):Yt.__webglFramebuffer===void 0?L.setupRenderTarget(C):Yt.__hasExternalTextures&&L.rebindTextures(C,ee.get(C.texture).__webglTexture,ee.get(C.depthTexture).__webglTexture);const Bt=C.texture;(Bt.isData3DTexture||Bt.isDataArrayTexture||Bt.isCompressedArrayTexture)&&(Ot=!0);const Jt=ee.get(C).__webglFramebuffer;C.isWebGLCubeRenderTarget?(Array.isArray(Jt[Y])?et=Jt[Y][it]:et=Jt[Y],Ct=!0):Qt.isWebGL2&&C.samples>0&&L.useMultisampledRTT(C)===!1?et=ee.get(C).__webglMultisampledFramebuffer:Array.isArray(Jt)?et=Jt[it]:et=Jt,U.copy(C.viewport),lt.copy(C.scissor),mt=C.scissorTest}else U.copy(ct).multiplyScalar(k).floor(),lt.copy(D).multiplyScalar(k).floor(),mt=X;if(Pt.bindFramebuffer(tt.FRAMEBUFFER,et)&&Qt.drawBuffers&&rt&&Pt.drawBuffers(C,et),Pt.viewport(U),Pt.scissor(lt),Pt.setScissorTest(mt),Ct){const Yt=ee.get(C.texture);tt.framebufferTexture2D(tt.FRAMEBUFFER,tt.COLOR_ATTACHMENT0,tt.TEXTURE_CUBE_MAP_POSITIVE_X+Y,Yt.__webglTexture,it)}else if(Ot){const Yt=ee.get(C.texture),Bt=Y||0;tt.framebufferTextureLayer(tt.FRAMEBUFFER,tt.COLOR_ATTACHMENT0,Yt.__webglTexture,it||0,Bt)}dt=-1},this.readRenderTargetPixels=function(C,Y,it,rt,et,Ct,Ot){if(!(C&&C.isWebGLRenderTarget)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Wt=ee.get(C).__webglFramebuffer;if(C.isWebGLCubeRenderTarget&&Ot!==void 0&&(Wt=Wt[Ot]),Wt){Pt.bindFramebuffer(tt.FRAMEBUFFER,Wt);try{const Yt=C.texture,Bt=Yt.format,Jt=Yt.type;if(Bt!==vi&&wt.convert(Bt)!==tt.getParameter(tt.IMPLEMENTATION_COLOR_READ_FORMAT)){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}const $t=Jt===Ao&&(Ft.has("EXT_color_buffer_half_float")||Qt.isWebGL2&&Ft.has("EXT_color_buffer_float"));if(Jt!==Ba&&wt.convert(Jt)!==tt.getParameter(tt.IMPLEMENTATION_COLOR_READ_TYPE)&&!(Jt===Na&&(Qt.isWebGL2||Ft.has("OES_texture_float")||Ft.has("WEBGL_color_buffer_float")))&&!$t){console.error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}Y>=0&&Y<=C.width-rt&&it>=0&&it<=C.height-et&&tt.readPixels(Y,it,rt,et,wt.convert(Bt),wt.convert(Jt),Ct)}finally{const Yt=z!==null?ee.get(z).__webglFramebuffer:null;Pt.bindFramebuffer(tt.FRAMEBUFFER,Yt)}}},this.copyFramebufferToTexture=function(C,Y,it=0){const rt=Math.pow(2,-it),et=Math.floor(Y.image.width*rt),Ct=Math.floor(Y.image.height*rt);L.setTexture2D(Y,0),tt.copyTexSubImage2D(tt.TEXTURE_2D,it,0,0,C.x,C.y,et,Ct),Pt.unbindTexture()},this.copyTextureToTexture=function(C,Y,it,rt=0){const et=Y.image.width,Ct=Y.image.height,Ot=wt.convert(it.format),Wt=wt.convert(it.type);L.setTexture2D(it,0),tt.pixelStorei(tt.UNPACK_FLIP_Y_WEBGL,it.flipY),tt.pixelStorei(tt.UNPACK_PREMULTIPLY_ALPHA_WEBGL,it.premultiplyAlpha),tt.pixelStorei(tt.UNPACK_ALIGNMENT,it.unpackAlignment),Y.isDataTexture?tt.texSubImage2D(tt.TEXTURE_2D,rt,C.x,C.y,et,Ct,Ot,Wt,Y.image.data):Y.isCompressedTexture?tt.compressedTexSubImage2D(tt.TEXTURE_2D,rt,C.x,C.y,Y.mipmaps[0].width,Y.mipmaps[0].height,Ot,Y.mipmaps[0].data):tt.texSubImage2D(tt.TEXTURE_2D,rt,C.x,C.y,Ot,Wt,Y.image),rt===0&&it.generateMipmaps&&tt.generateMipmap(tt.TEXTURE_2D),Pt.unbindTexture()},this.copyTextureToTexture3D=function(C,Y,it,rt,et=0){if(R.isWebGL1Renderer){console.warn("THREE.WebGLRenderer.copyTextureToTexture3D: can only be used with WebGL2.");return}const Ct=C.max.x-C.min.x+1,Ot=C.max.y-C.min.y+1,Wt=C.max.z-C.min.z+1,Yt=wt.convert(rt.format),Bt=wt.convert(rt.type);let Jt;if(rt.isData3DTexture)L.setTexture3D(rt,0),Jt=tt.TEXTURE_3D;else if(rt.isDataArrayTexture||rt.isCompressedArrayTexture)L.setTexture2DArray(rt,0),Jt=tt.TEXTURE_2D_ARRAY;else{console.warn("THREE.WebGLRenderer.copyTextureToTexture3D: only supports THREE.DataTexture3D and THREE.DataTexture2DArray.");return}tt.pixelStorei(tt.UNPACK_FLIP_Y_WEBGL,rt.flipY),tt.pixelStorei(tt.UNPACK_PREMULTIPLY_ALPHA_WEBGL,rt.premultiplyAlpha),tt.pixelStorei(tt.UNPACK_ALIGNMENT,rt.unpackAlignment);const $t=tt.getParameter(tt.UNPACK_ROW_LENGTH),Te=tt.getParameter(tt.UNPACK_IMAGE_HEIGHT),Ze=tt.getParameter(tt.UNPACK_SKIP_PIXELS),Ke=tt.getParameter(tt.UNPACK_SKIP_ROWS),Kn=tt.getParameter(tt.UNPACK_SKIP_IMAGES),ze=it.isCompressedTexture?it.mipmaps[et]:it.image;tt.pixelStorei(tt.UNPACK_ROW_LENGTH,ze.width),tt.pixelStorei(tt.UNPACK_IMAGE_HEIGHT,ze.height),tt.pixelStorei(tt.UNPACK_SKIP_PIXELS,C.min.x),tt.pixelStorei(tt.UNPACK_SKIP_ROWS,C.min.y),tt.pixelStorei(tt.UNPACK_SKIP_IMAGES,C.min.z),it.isDataTexture||it.isData3DTexture?tt.texSubImage3D(Jt,et,Y.x,Y.y,Y.z,Ct,Ot,Wt,Yt,Bt,ze.data):it.isCompressedArrayTexture?(console.warn("THREE.WebGLRenderer.copyTextureToTexture3D: untested support for compressed srcTexture."),tt.compressedTexSubImage3D(Jt,et,Y.x,Y.y,Y.z,Ct,Ot,Wt,Yt,ze.data)):tt.texSubImage3D(Jt,et,Y.x,Y.y,Y.z,Ct,Ot,Wt,Yt,Bt,ze),tt.pixelStorei(tt.UNPACK_ROW_LENGTH,$t),tt.pixelStorei(tt.UNPACK_IMAGE_HEIGHT,Te),tt.pixelStorei(tt.UNPACK_SKIP_PIXELS,Ze),tt.pixelStorei(tt.UNPACK_SKIP_ROWS,Ke),tt.pixelStorei(tt.UNPACK_SKIP_IMAGES,Kn),et===0&&rt.generateMipmaps&&tt.generateMipmap(Jt),Pt.unbindTexture()},this.initTexture=function(C){C.isCubeTexture?L.setTextureCube(C,0):C.isData3DTexture?L.setTexture3D(C,0):C.isDataArrayTexture||C.isCompressedArrayTexture?L.setTexture2DArray(C,0):L.setTexture2D(C,0),Pt.unbindTexture()},this.resetState=function(){q=0,B=0,z=null,Pt.reset(),Xt.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return Qi}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;const i=this.getContext();i.drawingBufferColorSpace=e===Ch?"display-p3":"srgb",i.unpackColorSpace=Ue.workingColorSpace===Mu?"display-p3":"srgb"}get outputEncoding(){return console.warn("THREE.WebGLRenderer: Property .outputEncoding has been removed. Use .outputColorSpace instead."),this.outputColorSpace===vn?dr:fv}set outputEncoding(e){console.warn("THREE.WebGLRenderer: Property .outputEncoding has been removed. Use .outputColorSpace instead."),this.outputColorSpace=e===dr?vn:Ji}get useLegacyLights(){return console.warn("THREE.WebGLRenderer: The property .useLegacyLights has been deprecated. Migrate your lighting according to the following guide: https://discourse.threejs.org/t/updates-to-lighting-in-three-js-r155/53733."),this._useLegacyLights}set useLegacyLights(e){console.warn("THREE.WebGLRenderer: The property .useLegacyLights has been deprecated. Migrate your lighting according to the following guide: https://discourse.threejs.org/t/updates-to-lighting-in-three-js-r155/53733."),this._useLegacyLights=e}}class cA extends uA{}cA.prototype.isWebGL1Renderer=!0;class bA extends Tn{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,i){return super.copy(e,i),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){const i=super.toJSON(e);return this.fog!==null&&(i.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(i.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(i.object.backgroundIntensity=this.backgroundIntensity),i}}class Ov extends Fa{constructor(e=1,i=32,s=16,l=0,c=Math.PI*2,d=0,h=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:i,heightSegments:s,phiStart:l,phiLength:c,thetaStart:d,thetaLength:h},i=Math.max(3,Math.floor(i)),s=Math.max(2,Math.floor(s));const m=Math.min(d+h,Math.PI);let p=0;const g=[],_=new at,M=new at,y=[],b=[],T=[],x=[];for(let v=0;v<=s;v++){const N=[],R=v/s;let I=0;v===0&&d===0?I=.5/i:v===s&&m===Math.PI&&(I=-.5/i);for(let q=0;q<=i;q++){const B=q/i;_.x=-e*Math.cos(l+B*c)*Math.sin(d+R*h),_.y=e*Math.cos(d+R*h),_.z=e*Math.sin(l+B*c)*Math.sin(d+R*h),b.push(_.x,_.y,_.z),M.copy(_).normalize(),T.push(M.x,M.y,M.z),x.push(B+I,1-R),N.push(p++)}g.push(N)}for(let v=0;v<s;v++)for(let N=0;N<i;N++){const R=g[v][N+1],I=g[v][N],q=g[v+1][N],B=g[v+1][N+1];(v!==0||d>0)&&y.push(R,I,B),(v!==s-1||m<Math.PI)&&y.push(I,q,B)}this.setIndex(y),this.setAttribute("position",new Ai(b,3)),this.setAttribute("normal",new Ai(T,3)),this.setAttribute("uv",new Ai(x,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new Ov(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}}class AA extends Lo{constructor(e){super(),this.isMeshStandardMaterial=!0,this.defines={STANDARD:""},this.type="MeshStandardMaterial",this.color=new Me(16777215),this.roughness=1,this.metalness=0,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new Me(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=hv,this.normalScale=new xe(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.roughnessMap=null,this.metalnessMap=null,this.alphaMap=null,this.envMap=null,this.envMapIntensity=1,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.defines={STANDARD:""},this.color.copy(e.color),this.roughness=e.roughness,this.metalness=e.metalness,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.roughnessMap=e.roughnessMap,this.metalnessMap=e.metalnessMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapIntensity=e.envMapIntensity,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}}class zv extends Tn{constructor(e,i=1){super(),this.isLight=!0,this.type="Light",this.color=new Me(e),this.intensity=i}dispose(){}copy(e,i){return super.copy(e,i),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){const i=super.toJSON(e);return i.object.color=this.color.getHex(),i.object.intensity=this.intensity,this.groundColor!==void 0&&(i.object.groundColor=this.groundColor.getHex()),this.distance!==void 0&&(i.object.distance=this.distance),this.angle!==void 0&&(i.object.angle=this.angle),this.decay!==void 0&&(i.object.decay=this.decay),this.penumbra!==void 0&&(i.object.penumbra=this.penumbra),this.shadow!==void 0&&(i.object.shadow=this.shadow.toJSON()),i}}const fh=new rn,j_=new at,Z_=new at;class fA{constructor(e){this.camera=e,this.bias=0,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new xe(512,512),this.map=null,this.mapPass=null,this.matrix=new rn,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Dh,this._frameExtents=new xe(1,1),this._viewportCount=1,this._viewports=[new hn(0,0,1,1)]}getViewportCount(){return this._viewportCount}getFrustum(){return this._frustum}updateMatrices(e){const i=this.camera,s=this.matrix;j_.setFromMatrixPosition(e.matrixWorld),i.position.copy(j_),Z_.setFromMatrixPosition(e.target.matrixWorld),i.lookAt(Z_),i.updateMatrixWorld(),fh.multiplyMatrices(i.projectionMatrix,i.matrixWorldInverse),this._frustum.setFromProjectionMatrix(fh),s.set(.5,0,0,.5,0,.5,0,.5,0,0,.5,.5,0,0,0,1),s.multiply(fh)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.bias=e.bias,this.radius=e.radius,this.mapSize.copy(e.mapSize),this}clone(){return new this.constructor().copy(this)}toJSON(){const e={};return this.bias!==0&&(e.bias=this.bias),this.normalBias!==0&&(e.normalBias=this.normalBias),this.radius!==1&&(e.radius=this.radius),(this.mapSize.x!==512||this.mapSize.y!==512)&&(e.mapSize=this.mapSize.toArray()),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}}class hA extends fA{constructor(){super(new Rv(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}}class RA extends zv{constructor(e,i){super(e,i),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(Tn.DEFAULT_UP),this.updateMatrix(),this.target=new Tn,this.shadow=new hA}dispose(){this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}}class CA extends zv{constructor(e,i){super(e,i),this.isAmbientLight=!0,this.type="AmbientLight"}}class wA{constructor(e=1,i=0,s=0){return this.radius=e,this.phi=i,this.theta=s,this}set(e,i,s){return this.radius=e,this.phi=i,this.theta=s,this}copy(e){return this.radius=e.radius,this.phi=e.phi,this.theta=e.theta,this}makeSafe(){return this.phi=Math.max(1e-6,Math.min(Math.PI-1e-6,this.phi)),this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,i,s){return this.radius=Math.sqrt(e*e+i*i+s*s),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(e,s),this.phi=Math.acos(wn(i/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:Ah}}));typeof window<"u"&&(window.__THREE__?console.warn("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=Ah);var hh={exports:{}},dh={},ph={exports:{}},mh={};var K_;function dA(){if(K_)return mh;K_=1;var o=Ro();function e(_,M){return _===M&&(_!==0||1/_===1/M)||_!==_&&M!==M}var i=typeof Object.is=="function"?Object.is:e,s=o.useState,l=o.useEffect,c=o.useLayoutEffect,d=o.useDebugValue;function h(_,M){var y=M(),b=s({inst:{value:y,getSnapshot:M}}),T=b[0].inst,x=b[1];return c(function(){T.value=y,T.getSnapshot=M,m(T)&&x({inst:T})},[_,y,M]),l(function(){return m(T)&&x({inst:T}),_(function(){m(T)&&x({inst:T})})},[_]),d(y),y}function m(_){var M=_.getSnapshot;_=_.value;try{var y=M();return!i(_,y)}catch{return!0}}function p(_,M){return M()}var g=typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"?p:h;return mh.useSyncExternalStore=o.useSyncExternalStore!==void 0?o.useSyncExternalStore:g,mh}var Q_;function pA(){return Q_||(Q_=1,ph.exports=dA()),ph.exports}var J_;function mA(){if(J_)return dh;J_=1;var o=Ro(),e=pA();function i(p,g){return p===g&&(p!==0||1/p===1/g)||p!==p&&g!==g}var s=typeof Object.is=="function"?Object.is:i,l=e.useSyncExternalStore,c=o.useRef,d=o.useEffect,h=o.useMemo,m=o.useDebugValue;return dh.useSyncExternalStoreWithSelector=function(p,g,_,M,y){var b=c(null);if(b.current===null){var T={hasValue:!1,value:null};b.current=T}else T=b.current;b=h(function(){function v(B){if(!N){if(N=!0,R=B,B=M(B),y!==void 0&&T.hasValue){var z=T.value;if(y(z,B))return I=z}return I=B}if(z=I,s(R,B))return z;var dt=M(B);return y!==void 0&&y(z,dt)?(R=B,z):(R=B,I=dt)}var N=!1,R,I,q=_===void 0?null:_;return[function(){return v(g())},q===null?void 0:function(){return v(q())}]},[g,_,M,y]);var x=l(p,b[0],b[1]);return d(function(){T.hasValue=!0,T.value=x},[x]),m(x),x},dh}var $_;function gA(){return $_||($_=1,hh.exports=mA()),hh.exports}var DA=gA();export{CA as A,Uo as B,Me as C,RA as D,Ss as E,yA as M,or as P,wo as Q,vA as R,wA as S,EA as T,at as V,uA as W,MA as _,tv as a,Ro as b,xA as c,SA as d,xe as e,cx as f,VS as g,TA as h,bA as i,_A as j,gi as k,rM as l,AA as m,Oa as n,Ov as o,ZS as r,DA as w};
