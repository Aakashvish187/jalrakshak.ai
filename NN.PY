<html lang="en"><head><script>
(function(){
  let proxyEcharts = null;

  let originInit = null;

  const DefaultFontOptions = [
      { key: 'xAxis', stylePath: 'xAxis.axisLabel' },
      { key: 'yAxis', stylePath: 'yAxis.axisLabel' },
      { key: 'legend', stylePath: 'legend.textStyle' },
      { key: 'tooltip', stylePath: 'tooltip.textStyle' },
      { key: 'title', stylePath: 'title.textStyle' },
      { key: 'series', stylePath: 'series.n.label', isArray: true },
  ];

  function setVal(source, keys, val, setFn) {
      if (!Array.isArray(keys)) {
          keys = keys.split('.');
      }
      keys = [...keys];
      const valKey = keys.pop();
      while (keys.length) {
          const parentKey = keys.shift();
          if (typeof source[parentKey] !== 'object' && typeof source[parentKey] !== 'function') {
              const childKey = keys[0] === undefined ? valKey : keys[0];
              let newVal = {};
              if (!isNaN(childKey * 1)) {
                  newVal = [];
              }
              if (setFn) {
                  setFn(source, parentKey, newVal);
              } else {
                  source[parentKey] = newVal;
              }
          }
          source = source[parentKey];
      }
      if (setFn) {
          setFn(source, valKey, val);
      } else {
          source[valKey] = val;
      }
  }

  function setFontFamily(options) {
      return options;
  }

  function setSeriesFamily(options) {
      if (options.series) {
          options.series = options.series.map(item => {
              item.label = { ...item.label };
              return item;
          });
      }
      return options;
  }


  function addResizeListener(echartsInstance) {
      const mountDom = echartsInstance.getDom();
      const resizeObserver = new ResizeObserver(() => {
          echartsInstance.resize();
      });
      resizeObserver.observe(mountDom);
      return resizeObserver;
  }

  function proxyInit(...arg) {
      if (!originInit) return null;
      let instance = null;
      try {
        instance = originInit.apply(this, arg);
      } catch (e) {
        console.error(e);
        const div = document.createElement('div');
        div.style.display = 'none';
        document.body.appendChild(div);
        instance = originInit.call(this, div);
        document.body.removeChild(div);
      }
      const originSetOption = instance.setOption;
      addResizeListener(instance);
      instance.setOption = async function setOptionProxy(options) {
          options = options || {};
          options.animation = false;
          try {
            return originSetOption.call(this, options);
          } catch (e) {
            console.error(e);
            return originSetOption.call(this, {});
          }
      };
      return instance;
  }

  Object.defineProperty(globalThis, 'echarts', {
      get() {
          return proxyEcharts;
      },
      set(value) {
          originInit = value.init;
          defineInit(value);
          proxyEcharts = value;
      },
      configurable: true,
  });

  function defineInit(value) {
      Object.defineProperty(value, 'init', {
          get() {
              return proxyInit;
          },
          set(v) {
              originInit = v;
          },
          enumerable: true,
      });
  }
})()
</script><script>console.warn = () => {};console.log = () => {};</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JalRakshā AI - Flood Early Warning System</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Pacifico&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/echarts/5.5.0/echarts.min.js"></script>
<style>
:where([class^="ri-"])::before { content: "\f3c2"; }
</style>
<script>
tailwind.config = {
theme: {
extend: {
colors: {
primary: '#06b6d4',
secondary: '#0891b2'
},
borderRadius: {
'none': '0px',
'sm': '4px',
DEFAULT: '8px',
'md': '12px',
'lg': '16px',
'xl': '20px',
'2xl': '24px',
'3xl': '32px',
'full': '9999px',
'button': '8px'
}
}
}
}
</script>
<script>
    // window.setInterval = () => {};
    // window.clearInterval = () => {};
    // window.setTimeout = () => {};
    // window.clearTimeout = () => {};
  </script><style>
    /* 自定义滚动条样式 */
    /* WebKit 浏览器 (Chrome, Safari, Edge) */
    ::-webkit-scrollbar {
        width: 0; /* 滚动条宽度 */
        height: 0; /* 水平滚动条高度 */
    }

    ::-webkit-scrollbar-track {
        background: transparent; /* 轨道透明，使内容可见 */
    }

    ::-webkit-scrollbar-thumb {
        background-color: rgba(0, 0, 0, 0.5); /* 滚动条滑块颜色 */
        border-radius: 4px; /* 滑块圆角 */
    }

    ::-webkit-scrollbar-thumb:hover {
        background-color: rgba(0, 0, 0, 0.7); /* 悬停时颜色 */
    }
  </style><script>
  window.addEventListener('load', () => {
    if (typeof AOS !== 'undefined' && AOS) {
      AOS.refresh?.();
    }
  });
</script><script>(function () {
  // 内存存储
  const memoryStorage = {
    local: new Map(),
    session: new Map()
  };

  // 保存原始方法
  // const originalLocalStorage = {
  //   setItem: localStorage.setItem.bind(localStorage),
  //   getItem: localStorage.getItem.bind(localStorage),
  //   removeItem: localStorage.removeItem.bind(localStorage),
  //   clear: localStorage.clear.bind(localStorage),
  //   key: localStorage.key.bind(localStorage)
  // };

  // const originalSessionStorage = {
  //   setItem: sessionStorage.setItem.bind(sessionStorage),
  //   getItem: sessionStorage.getItem.bind(sessionStorage),
  //   removeItem: sessionStorage.removeItem.bind(sessionStorage),
  //   clear: sessionStorage.clear.bind(sessionStorage),
  //   key: sessionStorage.key.bind(sessionStorage)
  // };

  // 只重写方法，不动属性
  localStorage.setItem = function (key, value) {
    memoryStorage.local.set(key, value);
  };

  localStorage.getItem = function (key) {
    return memoryStorage.local.get(key) ?? null;
  };

  localStorage.removeItem = function (key) {
    memoryStorage.local.delete(key);
  };

  localStorage.clear = function () {
    memoryStorage.local.clear();
  };

  localStorage.key = function (n) {
    return Array.from(memoryStorage.local.keys())[n] ?? null;
  };

  // sessionStorage 同样的处理
  sessionStorage.setItem = function (key, value) {
    memoryStorage.session.set(key, value);
  };

  sessionStorage.getItem = function (key) {
    return memoryStorage.session.get(key) ?? null;
  };

  sessionStorage.removeItem = function (key) {
    memoryStorage.session.delete(key);
  };

  sessionStorage.clear = function () {
    memoryStorage.session.clear();
  };

  sessionStorage.key = function (n) {
    return Array.from(memoryStorage.session.keys())[n] ?? null;
  };
})();
</script><style>*, ::before, ::after{--tw-border-spacing-x:0;--tw-border-spacing-y:0;--tw-translate-x:0;--tw-translate-y:0;--tw-rotate:0;--tw-skew-x:0;--tw-skew-y:0;--tw-scale-x:1;--tw-scale-y:1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness:proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgb(59 130 246 / 0.5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }::backdrop{--tw-border-spacing-x:0;--tw-border-spacing-y:0;--tw-translate-x:0;--tw-translate-y:0;--tw-rotate:0;--tw-skew-x:0;--tw-skew-y:0;--tw-scale-x:1;--tw-scale-y:1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness:proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgb(59 130 246 / 0.5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }/* ! tailwindcss v3.4.16 | MIT License | https://tailwindcss.com */*,::after,::before{box-sizing:border-box;border-width:0;border-style:solid;border-color:#e5e7eb}::after,::before{--tw-content:''}:host,html{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;tab-size:4;font-family:ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent}body{margin:0;line-height:inherit}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,pre,samp{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;font-feature-settings:normal;font-variation-settings:normal;font-size:1em}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}button,input,optgroup,select,textarea{font-family:inherit;font-feature-settings:inherit;font-variation-settings:inherit;font-size:100%;font-weight:inherit;line-height:inherit;letter-spacing:inherit;color:inherit;margin:0;padding:0}button,select{text-transform:none}button,input:where([type=button]),input:where([type=reset]),input:where([type=submit]){-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dd,dl,figure,h1,h2,h3,h4,h5,h6,hr,p,pre{margin:0}fieldset{margin:0;padding:0}legend{padding:0}menu,ol,ul{list-style:none;margin:0;padding:0}dialog{padding:0}textarea{resize:vertical}input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}[role=button],button{cursor:pointer}:disabled{cursor:default}audio,canvas,embed,iframe,img,object,svg,video{display:block;vertical-align:middle}img,video{max-width:100%;height:auto}[hidden]:where(:not([hidden=until-found])){display:none}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0, 0, 0, 0);white-space:nowrap;border-width:0}.fixed{position:fixed}.absolute{position:absolute}.relative{position:relative}.sticky{position:sticky}.inset-0{inset:0px}.bottom-4{bottom:1rem}.left-4{left:1rem}.left-\[20\%\]{left:20%}.left-\[35\%\]{left:35%}.left-\[40\%\]{left:40%}.left-\[60\%\]{left:60%}.right-4{right:1rem}.top-0{top:0px}.top-4{top:1rem}.top-\[25\%\]{top:25%}.top-\[30\%\]{top:30%}.top-\[40\%\]{top:40%}.top-\[60\%\]{top:60%}.z-50{z-index:50}.mb-1{margin-bottom:0.25rem}.mb-2{margin-bottom:0.5rem}.mb-3{margin-bottom:0.75rem}.mb-4{margin-bottom:1rem}.mb-6{margin-bottom:1.5rem}.mr-1{margin-right:0.25rem}.mr-2{margin-right:0.5rem}.mt-2{margin-top:0.5rem}.mt-4{margin-top:1rem}.block{display:block}.flex{display:flex}.inline-flex{display:inline-flex}.grid{display:grid}.hidden{display:none}.h-10{height:2.5rem}.h-12{height:3rem}.h-2{height:0.5rem}.h-20{height:5rem}.h-3{height:0.75rem}.h-48{height:12rem}.h-6{height:1.5rem}.h-64{height:16rem}.h-8{height:2rem}.h-80{height:20rem}.h-96{height:24rem}.max-h-80{max-height:20rem}.min-h-screen{min-height:100vh}.w-10{width:2.5rem}.w-11{width:2.75rem}.w-12{width:3rem}.w-2{width:0.5rem}.w-3{width:0.75rem}.w-8{width:2rem}.w-full{width:100%}.max-w-2xl{max-width:42rem}.max-w-md{max-width:28rem}.flex-1{flex:1 1 0%}@keyframes pulse{50%{opacity:.5}}.animate-pulse{animation:pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite}.cursor-pointer{cursor:pointer}.grid-cols-1{grid-template-columns:repeat(1, minmax(0, 1fr))}.grid-cols-3{grid-template-columns:repeat(3, minmax(0, 1fr))}.items-center{align-items:center}.justify-center{justify-content:center}.justify-between{justify-content:space-between}.gap-3{gap:0.75rem}.gap-4{gap:1rem}.gap-6{gap:1.5rem}.space-x-2 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(0.5rem * var(--tw-space-x-reverse));margin-left:calc(0.5rem * calc(1 - var(--tw-space-x-reverse)))}.space-x-3 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(0.75rem * var(--tw-space-x-reverse));margin-left:calc(0.75rem * calc(1 - var(--tw-space-x-reverse)))}.space-x-4 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(1rem * var(--tw-space-x-reverse));margin-left:calc(1rem * calc(1 - var(--tw-space-x-reverse)))}.space-x-6 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(1.5rem * var(--tw-space-x-reverse));margin-left:calc(1.5rem * calc(1 - var(--tw-space-x-reverse)))}.space-y-2 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(0.5rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(0.5rem * var(--tw-space-y-reverse))}.space-y-3 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(0.75rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(0.75rem * var(--tw-space-y-reverse))}.space-y-4 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(1rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(1rem * var(--tw-space-y-reverse))}.space-y-6 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(1.5rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(1.5rem * var(--tw-space-y-reverse))}.overflow-hidden{overflow:hidden}.overflow-y-auto{overflow-y:auto}.whitespace-nowrap{white-space:nowrap}.rounded-button{border-radius:8px}.rounded-full{border-radius:9999px}.rounded-lg{border-radius:16px}.rounded-xl{border-radius:20px}.border{border-width:1px}.border-2{border-width:2px}.border-b{border-bottom-width:1px}.border-l-2{border-left-width:2px}.border-blue-500\/30{border-color:rgb(59 130 246 / 0.3)}.border-green-500{--tw-border-opacity:1;border-color:rgb(34 197 94 / var(--tw-border-opacity, 1))}.border-green-500\/30{border-color:rgb(34 197 94 / 0.3)}.border-orange-500{--tw-border-opacity:1;border-color:rgb(249 115 22 / var(--tw-border-opacity, 1))}.border-orange-500\/30{border-color:rgb(249 115 22 / 0.3)}.border-primary\/30{border-color:rgb(6 182 212 / 0.3)}.border-red-500{--tw-border-opacity:1;border-color:rgb(239 68 68 / var(--tw-border-opacity, 1))}.border-red-500\/30{border-color:rgb(239 68 68 / 0.3)}.border-slate-600{--tw-border-opacity:1;border-color:rgb(71 85 105 / var(--tw-border-opacity, 1))}.border-slate-600\/30{border-color:rgb(71 85 105 / 0.3)}.border-slate-700{--tw-border-opacity:1;border-color:rgb(51 65 85 / var(--tw-border-opacity, 1))}.border-slate-700\/50{border-color:rgb(51 65 85 / 0.5)}.border-yellow-500{--tw-border-opacity:1;border-color:rgb(234 179 8 / var(--tw-border-opacity, 1))}.border-yellow-500\/30{border-color:rgb(234 179 8 / 0.3)}.bg-black\/50{background-color:rgb(0 0 0 / 0.5)}.bg-blue-500\/10{background-color:rgb(59 130 246 / 0.1)}.bg-blue-500\/20{background-color:rgb(59 130 246 / 0.2)}.bg-green-500{--tw-bg-opacity:1;background-color:rgb(34 197 94 / var(--tw-bg-opacity, 1))}.bg-green-500\/20{background-color:rgb(34 197 94 / 0.2)}.bg-orange-400{--tw-bg-opacity:1;background-color:rgb(251 146 60 / var(--tw-bg-opacity, 1))}.bg-orange-500\/10{background-color:rgb(249 115 22 / 0.1)}.bg-orange-500\/20{background-color:rgb(249 115 22 / 0.2)}.bg-primary{--tw-bg-opacity:1;background-color:rgb(6 182 212 / var(--tw-bg-opacity, 1))}.bg-primary\/20{background-color:rgb(6 182 212 / 0.2)}.bg-red-400{--tw-bg-opacity:1;background-color:rgb(248 113 113 / var(--tw-bg-opacity, 1))}.bg-red-500{--tw-bg-opacity:1;background-color:rgb(239 68 68 / var(--tw-bg-opacity, 1))}.bg-red-500\/10{background-color:rgb(239 68 68 / 0.1)}.bg-red-500\/20{background-color:rgb(239 68 68 / 0.2)}.bg-slate-600\/50{background-color:rgb(71 85 105 / 0.5)}.bg-slate-700{--tw-bg-opacity:1;background-color:rgb(51 65 85 / var(--tw-bg-opacity, 1))}.bg-slate-700\/50{background-color:rgb(51 65 85 / 0.5)}.bg-slate-800{--tw-bg-opacity:1;background-color:rgb(30 41 59 / var(--tw-bg-opacity, 1))}.bg-slate-800\/50{background-color:rgb(30 41 59 / 0.5)}.bg-slate-900{--tw-bg-opacity:1;background-color:rgb(15 23 42 / var(--tw-bg-opacity, 1))}.bg-slate-900\/50{background-color:rgb(15 23 42 / 0.5)}.bg-slate-900\/80{background-color:rgb(15 23 42 / 0.8)}.bg-slate-900\/90{background-color:rgb(15 23 42 / 0.9)}.bg-slate-950{--tw-bg-opacity:1;background-color:rgb(2 6 23 / var(--tw-bg-opacity, 1))}.bg-yellow-400{--tw-bg-opacity:1;background-color:rgb(250 204 21 / var(--tw-bg-opacity, 1))}.bg-yellow-500{--tw-bg-opacity:1;background-color:rgb(234 179 8 / var(--tw-bg-opacity, 1))}.bg-yellow-500\/10{background-color:rgb(234 179 8 / 0.1)}.bg-yellow-500\/20{background-color:rgb(234 179 8 / 0.2)}.bg-gradient-to-r{background-image:linear-gradient(to right, var(--tw-gradient-stops))}.from-yellow-500{--tw-gradient-from:#eab308 var(--tw-gradient-from-position);--tw-gradient-to:rgb(234 179 8 / 0) var(--tw-gradient-to-position);--tw-gradient-stops:var(--tw-gradient-from), var(--tw-gradient-to)}.to-red-500{--tw-gradient-to:#ef4444 var(--tw-gradient-to-position)}.bg-cover{background-size:cover}.bg-center{background-position:center}.p-3{padding:0.75rem}.p-4{padding:1rem}.p-6{padding:1.5rem}.px-3{padding-left:0.75rem;padding-right:0.75rem}.px-4{padding-left:1rem;padding-right:1rem}.px-6{padding-left:1.5rem;padding-right:1.5rem}.py-1\.5{padding-top:0.375rem;padding-bottom:0.375rem}.py-2{padding-top:0.5rem;padding-bottom:0.5rem}.py-3{padding-top:0.75rem;padding-bottom:0.75rem}.py-4{padding-top:1rem;padding-bottom:1rem}.px-2{padding-left:0.5rem;padding-right:0.5rem}.py-1{padding-top:0.25rem;padding-bottom:0.25rem}.pr-8{padding-right:2rem}.pl-4{padding-left:1rem}.text-2xl{font-size:1.5rem;line-height:2rem}.text-lg{font-size:1.125rem;line-height:1.75rem}.text-sm{font-size:0.875rem;line-height:1.25rem}.text-xl{font-size:1.25rem;line-height:1.75rem}.text-xs{font-size:0.75rem;line-height:1rem}.font-bold{font-weight:700}.font-medium{font-weight:500}.font-semibold{font-weight:600}.text-blue-400{--tw-text-opacity:1;color:rgb(96 165 250 / var(--tw-text-opacity, 1))}.text-green-400{--tw-text-opacity:1;color:rgb(74 222 128 / var(--tw-text-opacity, 1))}.text-green-500{--tw-text-opacity:1;color:rgb(34 197 94 / var(--tw-text-opacity, 1))}.text-orange-400{--tw-text-opacity:1;color:rgb(251 146 60 / var(--tw-text-opacity, 1))}.text-orange-500{--tw-text-opacity:1;color:rgb(249 115 22 / var(--tw-text-opacity, 1))}.text-primary{--tw-text-opacity:1;color:rgb(6 182 212 / var(--tw-text-opacity, 1))}.text-red-400{--tw-text-opacity:1;color:rgb(248 113 113 / var(--tw-text-opacity, 1))}.text-red-500{--tw-text-opacity:1;color:rgb(239 68 68 / var(--tw-text-opacity, 1))}.text-slate-300{--tw-text-opacity:1;color:rgb(203 213 225 / var(--tw-text-opacity, 1))}.text-slate-400{--tw-text-opacity:1;color:rgb(148 163 184 / var(--tw-text-opacity, 1))}.text-slate-500{--tw-text-opacity:1;color:rgb(100 116 139 / var(--tw-text-opacity, 1))}.text-white{--tw-text-opacity:1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.text-yellow-400{--tw-text-opacity:1;color:rgb(250 204 21 / var(--tw-text-opacity, 1))}.text-yellow-500{--tw-text-opacity:1;color:rgb(234 179 8 / var(--tw-text-opacity, 1))}.backdrop-blur-sm{--tw-backdrop-blur:blur(4px);-webkit-backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia);backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia)}.transition-all{transition-property:all;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms}.transition-colors{transition-property:color, background-color, border-color, fill, stroke, -webkit-text-decoration-color;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke, -webkit-text-decoration-color;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms}.after\:absolute::after{content:var(--tw-content);position:absolute}.after\:bottom-0::after{content:var(--tw-content);bottom:0px}.after\:left-0::after{content:var(--tw-content);left:0px}.after\:left-\[2px\]::after{content:var(--tw-content);left:2px}.after\:top-\[2px\]::after{content:var(--tw-content);top:2px}.after\:h-0\.5::after{content:var(--tw-content);height:0.125rem}.after\:h-5::after{content:var(--tw-content);height:1.25rem}.after\:w-5::after{content:var(--tw-content);width:1.25rem}.after\:w-full::after{content:var(--tw-content);width:100%}.after\:rounded-full::after{content:var(--tw-content);border-radius:9999px}.after\:border::after{content:var(--tw-content);border-width:1px}.after\:border-slate-300::after{content:var(--tw-content);--tw-border-opacity:1;border-color:rgb(203 213 225 / var(--tw-border-opacity, 1))}.after\:bg-primary::after{content:var(--tw-content);--tw-bg-opacity:1;background-color:rgb(6 182 212 / var(--tw-bg-opacity, 1))}.after\:bg-white::after{content:var(--tw-content);--tw-bg-opacity:1;background-color:rgb(255 255 255 / var(--tw-bg-opacity, 1))}.after\:transition-all::after{content:var(--tw-content);transition-property:all;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms}.after\:content-\[\'\'\]::after{--tw-content:'';content:var(--tw-content)}.hover\:bg-blue-500\/30:hover{background-color:rgb(59 130 246 / 0.3)}.hover\:bg-green-500\/30:hover{background-color:rgb(34 197 94 / 0.3)}.hover\:bg-orange-500\/30:hover{background-color:rgb(249 115 22 / 0.3)}.hover\:bg-primary\/30:hover{background-color:rgb(6 182 212 / 0.3)}.hover\:bg-red-500\/30:hover{background-color:rgb(239 68 68 / 0.3)}.hover\:bg-red-600:hover{--tw-bg-opacity:1;background-color:rgb(220 38 38 / var(--tw-bg-opacity, 1))}.hover\:bg-slate-700:hover{--tw-bg-opacity:1;background-color:rgb(51 65 85 / var(--tw-bg-opacity, 1))}.hover\:bg-yellow-500\/30:hover{background-color:rgb(234 179 8 / 0.3)}.hover\:text-primary:hover{--tw-text-opacity:1;color:rgb(6 182 212 / var(--tw-text-opacity, 1))}.hover\:text-white:hover{--tw-text-opacity:1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.hover\:underline:hover{-webkit-text-decoration-line:underline;text-decoration-line:underline}.peer:checked ~ .peer-checked\:bg-primary{--tw-bg-opacity:1;background-color:rgb(6 182 212 / var(--tw-bg-opacity, 1))}.peer:checked ~ .peer-checked\:after\:translate-x-full::after{content:var(--tw-content);--tw-translate-x:100%;transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.peer:checked ~ .peer-checked\:after\:border-white::after{content:var(--tw-content);--tw-border-opacity:1;border-color:rgb(255 255 255 / var(--tw-border-opacity, 1))}.peer:focus ~ .peer-focus\:outline-none{outline:2px solid transparent;outline-offset:2px}@media (min-width: 768px){.md\:flex{display:flex}.md\:hidden{display:none}.md\:grid-cols-2{grid-template-columns:repeat(2, minmax(0, 1fr))}.md\:grid-cols-3{grid-template-columns:repeat(3, minmax(0, 1fr))}.md\:grid-cols-4{grid-template-columns:repeat(4, minmax(0, 1fr))}}@media (min-width: 1024px){.lg\:col-span-2{grid-column:span 2 / span 2}.lg\:grid-cols-3{grid-template-columns:repeat(3, minmax(0, 1fr))}}</style><style>*, ::before, ::after{--tw-border-spacing-x:0;--tw-border-spacing-y:0;--tw-translate-x:0;--tw-translate-y:0;--tw-rotate:0;--tw-skew-x:0;--tw-skew-y:0;--tw-scale-x:1;--tw-scale-y:1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness:proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgb(59 130 246 / 0.5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }::backdrop{--tw-border-spacing-x:0;--tw-border-spacing-y:0;--tw-translate-x:0;--tw-translate-y:0;--tw-rotate:0;--tw-skew-x:0;--tw-skew-y:0;--tw-scale-x:1;--tw-scale-y:1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness:proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width:0px;--tw-ring-offset-color:#fff;--tw-ring-color:rgb(59 130 246 / 0.5);--tw-ring-offset-shadow:0 0 #0000;--tw-ring-shadow:0 0 #0000;--tw-shadow:0 0 #0000;--tw-shadow-colored:0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }/* ! tailwindcss v3.4.16 | MIT License | https://tailwindcss.com */*,::after,::before{box-sizing:border-box;border-width:0;border-style:solid;border-color:#e5e7eb}::after,::before{--tw-content:''}:host,html{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;tab-size:4;font-family:ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent}body{margin:0;line-height:inherit}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,pre,samp{font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;font-feature-settings:normal;font-variation-settings:normal;font-size:1em}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}button,input,optgroup,select,textarea{font-family:inherit;font-feature-settings:inherit;font-variation-settings:inherit;font-size:100%;font-weight:inherit;line-height:inherit;letter-spacing:inherit;color:inherit;margin:0;padding:0}button,select{text-transform:none}button,input:where([type=button]),input:where([type=reset]),input:where([type=submit]){-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dd,dl,figure,h1,h2,h3,h4,h5,h6,hr,p,pre{margin:0}fieldset{margin:0;padding:0}legend{padding:0}menu,ol,ul{list-style:none;margin:0;padding:0}dialog{padding:0}textarea{resize:vertical}input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}[role=button],button{cursor:pointer}:disabled{cursor:default}audio,canvas,embed,iframe,img,object,svg,video{display:block;vertical-align:middle}img,video{max-width:100%;height:auto}[hidden]:where(:not([hidden=until-found])){display:none}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0, 0, 0, 0);white-space:nowrap;border-width:0}.fixed{position:fixed}.absolute{position:absolute}.relative{position:relative}.sticky{position:sticky}.inset-0{inset:0px}.bottom-4{bottom:1rem}.left-4{left:1rem}.left-\[20\%\]{left:20%}.left-\[35\%\]{left:35%}.left-\[40\%\]{left:40%}.left-\[60\%\]{left:60%}.right-4{right:1rem}.top-0{top:0px}.top-4{top:1rem}.top-\[25\%\]{top:25%}.top-\[30\%\]{top:30%}.top-\[40\%\]{top:40%}.top-\[60\%\]{top:60%}.z-50{z-index:50}.mb-1{margin-bottom:0.25rem}.mb-2{margin-bottom:0.5rem}.mb-3{margin-bottom:0.75rem}.mb-4{margin-bottom:1rem}.mb-6{margin-bottom:1.5rem}.mr-1{margin-right:0.25rem}.mr-2{margin-right:0.5rem}.mt-2{margin-top:0.5rem}.mt-4{margin-top:1rem}.block{display:block}.flex{display:flex}.inline-flex{display:inline-flex}.grid{display:grid}.hidden{display:none}.h-10{height:2.5rem}.h-12{height:3rem}.h-2{height:0.5rem}.h-20{height:5rem}.h-3{height:0.75rem}.h-48{height:12rem}.h-6{height:1.5rem}.h-64{height:16rem}.h-8{height:2rem}.h-80{height:20rem}.h-96{height:24rem}.max-h-80{max-height:20rem}.min-h-screen{min-height:100vh}.w-10{width:2.5rem}.w-11{width:2.75rem}.w-12{width:3rem}.w-2{width:0.5rem}.w-3{width:0.75rem}.w-8{width:2rem}.w-full{width:100%}.max-w-2xl{max-width:42rem}.max-w-md{max-width:28rem}.flex-1{flex:1 1 0%}@keyframes pulse{50%{opacity:.5}}.animate-pulse{animation:pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite}.cursor-pointer{cursor:pointer}.grid-cols-1{grid-template-columns:repeat(1, minmax(0, 1fr))}.grid-cols-3{grid-template-columns:repeat(3, minmax(0, 1fr))}.items-center{align-items:center}.justify-center{justify-content:center}.justify-between{justify-content:space-between}.gap-3{gap:0.75rem}.gap-4{gap:1rem}.gap-6{gap:1.5rem}.space-x-2 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(0.5rem * var(--tw-space-x-reverse));margin-left:calc(0.5rem * calc(1 - var(--tw-space-x-reverse)))}.space-x-3 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(0.75rem * var(--tw-space-x-reverse));margin-left:calc(0.75rem * calc(1 - var(--tw-space-x-reverse)))}.space-x-4 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(1rem * var(--tw-space-x-reverse));margin-left:calc(1rem * calc(1 - var(--tw-space-x-reverse)))}.space-x-6 > :not([hidden]) ~ :not([hidden]){--tw-space-x-reverse:0;margin-right:calc(1.5rem * var(--tw-space-x-reverse));margin-left:calc(1.5rem * calc(1 - var(--tw-space-x-reverse)))}.space-y-2 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(0.5rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(0.5rem * var(--tw-space-y-reverse))}.space-y-3 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(0.75rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(0.75rem * var(--tw-space-y-reverse))}.space-y-4 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(1rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(1rem * var(--tw-space-y-reverse))}.space-y-6 > :not([hidden]) ~ :not([hidden]){--tw-space-y-reverse:0;margin-top:calc(1.5rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(1.5rem * var(--tw-space-y-reverse))}.overflow-hidden{overflow:hidden}.overflow-y-auto{overflow-y:auto}.whitespace-nowrap{white-space:nowrap}.rounded-button{border-radius:8px}.rounded-full{border-radius:9999px}.rounded-lg{border-radius:16px}.rounded-xl{border-radius:20px}.border{border-width:1px}.border-2{border-width:2px}.border-b{border-bottom-width:1px}.border-blue-500\/30{border-color:rgb(59 130 246 / 0.3)}.border-green-500{--tw-border-opacity:1;border-color:rgb(34 197 94 / var(--tw-border-opacity, 1))}.border-green-500\/30{border-color:rgb(34 197 94 / 0.3)}.border-orange-500{--tw-border-opacity:1;border-color:rgb(249 115 22 / var(--tw-border-opacity, 1))}.border-orange-500\/30{border-color:rgb(249 115 22 / 0.3)}.border-primary\/30{border-color:rgb(6 182 212 / 0.3)}.border-red-500{--tw-border-opacity:1;border-color:rgb(239 68 68 / var(--tw-border-opacity, 1))}.border-red-500\/30{border-color:rgb(239 68 68 / 0.3)}.border-slate-600{--tw-border-opacity:1;border-color:rgb(71 85 105 / var(--tw-border-opacity, 1))}.border-slate-600\/30{border-color:rgb(71 85 105 / 0.3)}.border-slate-700{--tw-border-opacity:1;border-color:rgb(51 65 85 / var(--tw-border-opacity, 1))}.border-slate-700\/50{border-color:rgb(51 65 85 / 0.5)}.border-yellow-500{--tw-border-opacity:1;border-color:rgb(234 179 8 / var(--tw-border-opacity, 1))}.border-yellow-500\/30{border-color:rgb(234 179 8 / 0.3)}.bg-black\/50{background-color:rgb(0 0 0 / 0.5)}.bg-blue-500\/10{background-color:rgb(59 130 246 / 0.1)}.bg-blue-500\/20{background-color:rgb(59 130 246 / 0.2)}.bg-green-500{--tw-bg-opacity:1;background-color:rgb(34 197 94 / var(--tw-bg-opacity, 1))}.bg-green-500\/20{background-color:rgb(34 197 94 / 0.2)}.bg-orange-400{--tw-bg-opacity:1;background-color:rgb(251 146 60 / var(--tw-bg-opacity, 1))}.bg-orange-500\/10{background-color:rgb(249 115 22 / 0.1)}.bg-orange-500\/20{background-color:rgb(249 115 22 / 0.2)}.bg-primary{--tw-bg-opacity:1;background-color:rgb(6 182 212 / var(--tw-bg-opacity, 1))}.bg-primary\/20{background-color:rgb(6 182 212 / 0.2)}.bg-red-400{--tw-bg-opacity:1;background-color:rgb(248 113 113 / var(--tw-bg-opacity, 1))}.bg-red-500{--tw-bg-opacity:1;background-color:rgb(239 68 68 / var(--tw-bg-opacity, 1))}.bg-red-500\/10{background-color:rgb(239 68 68 / 0.1)}.bg-red-500\/20{background-color:rgb(239 68 68 / 0.2)}.bg-slate-600\/50{background-color:rgb(71 85 105 / 0.5)}.bg-slate-700{--tw-bg-opacity:1;background-color:rgb(51 65 85 / var(--tw-bg-opacity, 1))}.bg-slate-700\/50{background-color:rgb(51 65 85 / 0.5)}.bg-slate-800{--tw-bg-opacity:1;background-color:rgb(30 41 59 / var(--tw-bg-opacity, 1))}.bg-slate-800\/50{background-color:rgb(30 41 59 / 0.5)}.bg-slate-900{--tw-bg-opacity:1;background-color:rgb(15 23 42 / var(--tw-bg-opacity, 1))}.bg-slate-900\/50{background-color:rgb(15 23 42 / 0.5)}.bg-slate-900\/80{background-color:rgb(15 23 42 / 0.8)}.bg-slate-900\/90{background-color:rgb(15 23 42 / 0.9)}.bg-slate-950{--tw-bg-opacity:1;background-color:rgb(2 6 23 / var(--tw-bg-opacity, 1))}.bg-yellow-400{--tw-bg-opacity:1;background-color:rgb(250 204 21 / var(--tw-bg-opacity, 1))}.bg-yellow-500{--tw-bg-opacity:1;background-color:rgb(234 179 8 / var(--tw-bg-opacity, 1))}.bg-yellow-500\/10{background-color:rgb(234 179 8 / 0.1)}.bg-yellow-500\/20{background-color:rgb(234 179 8 / 0.2)}.bg-gradient-to-r{background-image:linear-gradient(to right, var(--tw-gradient-stops))}.from-yellow-500{--tw-gradient-from:#eab308 var(--tw-gradient-from-position);--tw-gradient-to:rgb(234 179 8 / 0) var(--tw-gradient-to-position);--tw-gradient-stops:var(--tw-gradient-from), var(--tw-gradient-to)}.to-red-500{--tw-gradient-to:#ef4444 var(--tw-gradient-to-position)}.bg-cover{background-size:cover}.bg-center{background-position:center}.p-3{padding:0.75rem}.p-4{padding:1rem}.p-6{padding:1.5rem}.px-3{padding-left:0.75rem;padding-right:0.75rem}.px-4{padding-left:1rem;padding-right:1rem}.px-6{padding-left:1.5rem;padding-right:1.5rem}.py-1\.5{padding-top:0.375rem;padding-bottom:0.375rem}.py-2{padding-top:0.5rem;padding-bottom:0.5rem}.py-3{padding-top:0.75rem;padding-bottom:0.75rem}.py-4{padding-top:1rem;padding-bottom:1rem}.pr-8{padding-right:2rem}.text-2xl{font-size:1.5rem;line-height:2rem}.text-lg{font-size:1.125rem;line-height:1.75rem}.text-sm{font-size:0.875rem;line-height:1.25rem}.text-xl{font-size:1.25rem;line-height:1.75rem}.text-xs{font-size:0.75rem;line-height:1rem}.font-bold{font-weight:700}.font-medium{font-weight:500}.font-semibold{font-weight:600}.text-blue-400{--tw-text-opacity:1;color:rgb(96 165 250 / var(--tw-text-opacity, 1))}.text-green-400{--tw-text-opacity:1;color:rgb(74 222 128 / var(--tw-text-opacity, 1))}.text-green-500{--tw-text-opacity:1;color:rgb(34 197 94 / var(--tw-text-opacity, 1))}.text-orange-400{--tw-text-opacity:1;color:rgb(251 146 60 / var(--tw-text-opacity, 1))}.text-orange-500{--tw-text-opacity:1;color:rgb(249 115 22 / var(--tw-text-opacity, 1))}.text-primary{--tw-text-opacity:1;color:rgb(6 182 212 / var(--tw-text-opacity, 1))}.text-red-400{--tw-text-opacity:1;color:rgb(248 113 113 / var(--tw-text-opacity, 1))}.text-red-500{--tw-text-opacity:1;color:rgb(239 68 68 / var(--tw-text-opacity, 1))}.text-slate-300{--tw-text-opacity:1;color:rgb(203 213 225 / var(--tw-text-opacity, 1))}.text-slate-400{--tw-text-opacity:1;color:rgb(148 163 184 / var(--tw-text-opacity, 1))}.text-slate-500{--tw-text-opacity:1;color:rgb(100 116 139 / var(--tw-text-opacity, 1))}.text-white{--tw-text-opacity:1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.text-yellow-400{--tw-text-opacity:1;color:rgb(250 204 21 / var(--tw-text-opacity, 1))}.text-yellow-500{--tw-text-opacity:1;color:rgb(234 179 8 / var(--tw-text-opacity, 1))}.backdrop-blur-sm{--tw-backdrop-blur:blur(4px);-webkit-backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia);backdrop-filter:var(--tw-backdrop-blur) var(--tw-backdrop-brightness) var(--tw-backdrop-contrast) var(--tw-backdrop-grayscale) var(--tw-backdrop-hue-rotate) var(--tw-backdrop-invert) var(--tw-backdrop-opacity) var(--tw-backdrop-saturate) var(--tw-backdrop-sepia)}.transition-all{transition-property:all;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms}.transition-colors{transition-property:color, background-color, border-color, fill, stroke, -webkit-text-decoration-color;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke;transition-property:color, background-color, border-color, text-decoration-color, fill, stroke, -webkit-text-decoration-color;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms}.after\:absolute::after{content:var(--tw-content);position:absolute}.after\:bottom-0::after{content:var(--tw-content);bottom:0px}.after\:left-0::after{content:var(--tw-content);left:0px}.after\:left-\[2px\]::after{content:var(--tw-content);left:2px}.after\:top-\[2px\]::after{content:var(--tw-content);top:2px}.after\:h-0\.5::after{content:var(--tw-content);height:0.125rem}.after\:h-5::after{content:var(--tw-content);height:1.25rem}.after\:w-5::after{content:var(--tw-content);width:1.25rem}.after\:w-full::after{content:var(--tw-content);width:100%}.after\:rounded-full::after{content:var(--tw-content);border-radius:9999px}.after\:border::after{content:var(--tw-content);border-width:1px}.after\:border-slate-300::after{content:var(--tw-content);--tw-border-opacity:1;border-color:rgb(203 213 225 / var(--tw-border-opacity, 1))}.after\:bg-primary::after{content:var(--tw-content);--tw-bg-opacity:1;background-color:rgb(6 182 212 / var(--tw-bg-opacity, 1))}.after\:bg-white::after{content:var(--tw-content);--tw-bg-opacity:1;background-color:rgb(255 255 255 / var(--tw-bg-opacity, 1))}.after\:transition-all::after{content:var(--tw-content);transition-property:all;transition-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transition-duration:150ms}.after\:content-\[\'\'\]::after{--tw-content:'';content:var(--tw-content)}.hover\:bg-blue-500\/30:hover{background-color:rgb(59 130 246 / 0.3)}.hover\:bg-green-500\/30:hover{background-color:rgb(34 197 94 / 0.3)}.hover\:bg-orange-500\/30:hover{background-color:rgb(249 115 22 / 0.3)}.hover\:bg-primary\/30:hover{background-color:rgb(6 182 212 / 0.3)}.hover\:bg-red-500\/30:hover{background-color:rgb(239 68 68 / 0.3)}.hover\:bg-red-600:hover{--tw-bg-opacity:1;background-color:rgb(220 38 38 / var(--tw-bg-opacity, 1))}.hover\:bg-slate-700:hover{--tw-bg-opacity:1;background-color:rgb(51 65 85 / var(--tw-bg-opacity, 1))}.hover\:bg-yellow-500\/30:hover{background-color:rgb(234 179 8 / 0.3)}.hover\:text-primary:hover{--tw-text-opacity:1;color:rgb(6 182 212 / var(--tw-text-opacity, 1))}.hover\:text-white:hover{--tw-text-opacity:1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.hover\:underline:hover{-webkit-text-decoration-line:underline;text-decoration-line:underline}.peer:checked ~ .peer-checked\:bg-primary{--tw-bg-opacity:1;background-color:rgb(6 182 212 / var(--tw-bg-opacity, 1))}.peer:checked ~ .peer-checked\:after\:translate-x-full::after{content:var(--tw-content);--tw-translate-x:100%;transform:translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y))}.peer:checked ~ .peer-checked\:after\:border-white::after{content:var(--tw-content);--tw-border-opacity:1;border-color:rgb(255 255 255 / var(--tw-border-opacity, 1))}.peer:focus ~ .peer-focus\:outline-none{outline:2px solid transparent;outline-offset:2px}@media (min-width: 768px){.md\:flex{display:flex}.md\:hidden{display:none}.md\:grid-cols-2{grid-template-columns:repeat(2, minmax(0, 1fr))}.md\:grid-cols-3{grid-template-columns:repeat(3, minmax(0, 1fr))}.md\:grid-cols-4{grid-template-columns:repeat(4, minmax(0, 1fr))}}@media (min-width: 1024px){.lg\:col-span-2{grid-column:span 2 / span 2}.lg\:grid-cols-3{grid-template-columns:repeat(3, minmax(0, 1fr))}}</style></head>
<body class="bg-slate-950 text-white min-h-screen">
<header class="bg-slate-900/90 backdrop-blur-sm border-b border-primary/30 sticky top-0 z-50">
<div class="px-6 py-4">
<div class="flex items-center justify-between">
<div class="flex items-center space-x-4">
<div class="text-2xl">🌊</div>
<div>
<h1 class="text-2xl font-bold text-primary">JalRakshā AI</h1>
<p class="text-sm text-slate-400">Flood Early Warning &amp; Rescue System</p>
</div>
</div>
<div class="hidden md:flex items-center space-x-6">
<button id="dashboardBtn" class="text-primary hover:text-primary transition-colors relative after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-primary after:rounded-full">Dashboard</button>
<button id="analyticsBtn" class="text-slate-300 hover:text-primary transition-colors">Analytics</button>
<button id="teamsBtn" class="text-slate-300 hover:text-primary transition-colors">Teams</button>
<button id="settingsBtn" class="text-slate-300 hover:text-primary transition-colors">Settings</button>
</div>
<button class="md:hidden w-8 h-8 flex items-center justify-center">
<i class="ri-menu-line text-xl"></i>
</button>
</div>
</div>
</header>
<main class="p-6 space-y-6">
<div id="dashboardPage" class="">
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between mb-4">
<h2 class="text-xl font-semibold flex items-center">
<i class="ri-map-2-line text-primary mr-2"></i>
AI Risk Map
</h2>
<div class="flex items-center space-x-4">
<div class="flex items-center space-x-2 text-sm">
<div class="w-3 h-3 bg-green-500 rounded-full"></div>
<span>Safe</span>
</div>
<div class="flex items-center space-x-2 text-sm">
<div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
<span>Warning</span>
</div>
<div class="flex items-center space-x-2 text-sm">
<div class="w-3 h-3 bg-red-500 rounded-full animate-pulse" style="opacity: 1;"></div>
<span>Critical</span>
</div>
</div>
</div>
<div class="relative h-96 bg-slate-800 rounded-lg overflow-hidden">
<div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://public.readdy.ai/gen_page/map_placeholder_1280x720.png')"></div>
<div class="absolute top-4 left-4 space-y-2">
<div class="flex items-center space-x-2 bg-slate-900/80 px-3 py-2 rounded-lg">
<i class="ri-home-3-line text-blue-400"></i>
<span class="text-sm">12 Shelters</span>
</div>
<div class="flex items-center space-x-2 bg-slate-900/80 px-3 py-2 rounded-lg">
<i class="ri-hospital-line text-green-400"></i>
<span class="text-sm">8 Hospitals</span>
</div>
<div class="flex items-center space-x-2 bg-slate-900/80 px-3 py-2 rounded-lg">
<i class="ri-plane-line text-primary"></i>
<span class="text-sm">15 Rescue Teams</span>
</div>
</div>
<!-- Map Markers -->
<div class="absolute inset-0">
<!-- Mumbai Marker -->
<div class="absolute left-[20%] top-[40%]">
<button class="map-marker" data-city="mumbai">
<div class="w-8 h-8 bg-red-500/20 rounded-full flex items-center justify-center border-2 border-red-500 cursor-pointer hover:bg-red-500/30 transition-all">
<i class="ri-checkbox-circle-fill text-red-500"></i>
</div>
</button>
</div>
<!-- Chennai Marker -->
<div class="absolute left-[40%] top-[60%]">
<button class="map-marker" data-city="chennai">
<div class="w-8 h-8 bg-yellow-500/20 rounded-full flex items-center justify-center border-2 border-yellow-500 cursor-pointer hover:bg-yellow-500/30 transition-all">
<i class="ri-checkbox-circle-fill text-yellow-500"></i>
</div>
</button>
</div>
<!-- Kolkata Marker -->
<div class="absolute left-[60%] top-[30%]">
<button class="map-marker" data-city="kolkata">
<div class="w-8 h-8 bg-orange-500/20 rounded-full flex items-center justify-center border-2 border-orange-500 cursor-pointer hover:bg-orange-500/30 transition-all">
<i class="ri-checkbox-circle-fill text-orange-500"></i>
</div>
</button>
</div>
<!-- Delhi Marker -->
<div class="absolute left-[35%] top-[25%]">
<button class="map-marker" data-city="delhi">
<div class="w-8 h-8 bg-green-500/20 rounded-full flex items-center justify-center border-2 border-green-500 cursor-pointer hover:bg-green-500/30 transition-all">
<i class="ri-checkbox-circle-fill text-green-500"></i>
</div>
</button>
</div>
</div>
<div class="absolute bottom-4 right-4">
<div class="bg-red-500/20 border border-red-500 px-3 py-2 rounded-lg animate-pulse">
<span class="text-red-400 text-sm font-medium">High Risk Zone Detected</span>
</div>
</div>
</div>
<!-- City Data Modal -->
<div id="cityModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 hidden">
<div class="flex items-center justify-center min-h-screen p-4">
<div class="bg-slate-900 rounded-xl border border-slate-700 p-6 w-full max-w-2xl">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-semibold text-orange-500">Kolkata</h3>
<button class="close-city-modal w-8 h-8 flex items-center justify-center text-slate-400 hover:text-white">
<i class="ri-close-line"></i>
</button>
</div>
<div class="space-y-6">
<div class="grid grid-cols-1 md:grid-cols-3 gap-4">
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="text-sm text-slate-400">Risk Level</div>
<div class="text-2xl font-bold text-orange-500">Medium-High</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="text-sm text-slate-400">Population at Risk</div>
<div class="text-2xl font-bold population-at-risk">180,000</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="text-sm text-slate-400">Active Alerts</div>
<div class="text-2xl font-bold active-alerts">10</div>
</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<h4 class="text-lg font-semibold mb-4">Historical Events</h4>
<div class="space-y-4 historical-events">
<div class="border-l-2 border-slate-700 pl-4 py-2">
<div class="flex items-center justify-between mb-1">
<span class="text-sm font-medium">2024-07-20</span>
<span class="text-xs px-2 py-1 rounded-full bg-orange-500/20 text-orange-400">High</span>
</div>
<p class="text-sm mb-1">River overflow</p>
<p class="text-xs text-slate-400">Low-lying areas affected</p>
</div>

<div class="border-l-2 border-slate-700 pl-4 py-2">
<div class="flex items-center justify-between mb-1">
<span class="text-sm font-medium">2023-08-15</span>
<span class="text-xs px-2 py-1 rounded-full bg-yellow-500/20 text-yellow-400">Moderate</span>
</div>
<p class="text-sm mb-1">Heavy rainfall flooding</p>
<p class="text-xs text-slate-400">400 people evacuated</p>
</div>
</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<h4 class="text-lg font-semibold mb-4">Current Status</h4>
<div class="space-y-2">
<div class="flex items-center justify-between">
<span class="text-slate-400">Water Level</span>
<span class="water-level">3.2m above normal</span>
</div>
<div class="flex items-center justify-between">
<span class="text-slate-400">Rainfall</span>
<span class="rainfall">Very Heavy (150mm/day)</span>
</div>
<div class="flex items-center justify-between">
<span class="text-slate-400">Evacuation Status</span>
<span class="evacuation-status">In Progress</span>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-water-flash-line text-primary mr-2"></i>
Water Level Trends
</h3>
<div id="waterChart" class="h-64" style="user-select: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); position: relative;" _echarts_instance_="ec_1757249364961"><div style="position: relative; width: 324px; height: 272px; padding: 0px; margin: 0px; border-width: 0px; cursor: pointer;"><canvas data-zr-dom-id="zr_0" width="405" height="340" style="position: absolute; left: 0px; top: 0px; width: 324px; height: 272px; user-select: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0px; margin: 0px; border-width: 0px;"></canvas></div><div class=""></div></div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-cloudy-2-line text-primary mr-2"></i>
Rainfall Forecast
</h3>
<div id="rainfallChart" class="h-64" style="user-select: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); position: relative;" _echarts_instance_="ec_1757249364962"><div style="position: relative; width: 324px; height: 272px; padding: 0px; margin: 0px; border-width: 0px; cursor: default;"><canvas data-zr-dom-id="zr_0" width="405" height="340" style="position: absolute; left: 0px; top: 0px; width: 324px; height: 272px; user-select: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); padding: 0px; margin: 0px; border-width: 0px;"></canvas></div><div class="" style="position: absolute; display: block; border-style: solid; white-space: nowrap; z-index: 9999999; box-shadow: rgba(0, 0, 0, 0.2) 1px 2px 10px; background-color: rgba(15, 23, 42, 0.9); border-width: 1px; border-radius: 4px; color: rgb(241, 245, 249); font: 14px / 21px &quot;Microsoft YaHei&quot;; padding: 10px; top: 0px; left: 0px; transform: translate3d(123px, 174px, 0px); border-color: rgb(71, 85, 105); pointer-events: none; visibility: hidden; opacity: 0;"><div style="margin: 0px 0 0;line-height:1;"><div style="margin: 0px 0 0;line-height:1;"><span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:rgba(251, 191, 114, 1);"></span><span style="font-size:14px;color:#f1f5f9;font-weight:400;margin-left:2px">Tue</span><span style="float:right;margin-left:20px;font-size:14px;color:#f1f5f9;font-weight:900">32</span><div style="clear:both"></div></div><div style="clear:both"></div></div></div></div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-team-line text-primary mr-2"></i>
Active Rescue Teams
</h3>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
<div class="bg-slate-800/50 rounded-lg p-4 border border-slate-600/30">
<div class="flex items-center justify-between mb-2">
<span class="font-medium">Team Alpha-1</span>
<div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
</div>
<p class="text-sm text-slate-400 mb-2">Location: Sector 15, Zone A</p>
<p class="text-sm text-slate-400 mb-3">Status: Available</p>
<button class="w-full bg-primary/20 text-primary border border-primary/30 px-3 py-2 rounded-button text-sm hover:bg-primary/30 transition-colors whitespace-nowrap">
Assign Mission
</button>
</div>
<div class="bg-slate-800/50 rounded-lg p-4 border border-slate-600/30">
<div class="flex items-center justify-between mb-2">
<span class="font-medium">Team Beta-2</span>
<div class="w-3 h-3 bg-yellow-500 rounded-full animate-pulse"></div>
</div>
<p class="text-sm text-slate-400 mb-2">Location: Sector 22, Zone B</p>
<p class="text-sm text-slate-400 mb-3">Status: In Transit</p>
<button class="w-full bg-slate-600/50 text-slate-400 border border-slate-600/30 px-3 py-2 rounded-button text-sm whitespace-nowrap" disabled="">
Busy
</button>
</div>
<div class="bg-slate-800/50 rounded-lg p-4 border border-slate-600/30">
<div class="flex items-center justify-between mb-2">
<span class="font-medium">Team Gamma-3</span>
<div class="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
</div>
<p class="text-sm text-slate-400 mb-2">Location: Sector 8, Zone C</p>
<p class="text-sm text-slate-400 mb-3">Status: On Mission</p>
<button class="w-full bg-red-500/20 text-red-400 border border-red-500/30 px-3 py-2 rounded-button text-sm whitespace-nowrap" disabled="">
Active Rescue
</button>
</div>
</div>
</div>
</div>
<div class="space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between mb-4">
<h3 class="text-lg font-semibold flex items-center">
<i class="ri-alarm-warning-line text-yellow-500 mr-2"></i>
AI Alerts
</h3>
<div class="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
</div>
<div class="space-y-3 max-h-80 overflow-y-auto">
<div class="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
<div class="flex items-center justify-between mb-2">
<span class="text-red-400 text-sm font-medium">CRITICAL</span>
<span class="text-xs text-slate-400">2 min ago</span>
</div>
<p class="text-sm mb-2">Rapid water rise detected in Riverside District</p>
<div class="flex items-center justify-between">
<span class="text-xs text-slate-400">AI Confidence: 94%</span>
<i class="ri-error-warning-line text-red-400"></i>
</div>
</div>
<div class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3">
<div class="flex items-center justify-between mb-2">
<span class="text-yellow-400 text-sm font-medium">HIGH</span>
<span class="text-xs text-slate-400">5 min ago</span>
</div>
<p class="text-sm mb-2">Heavy rainfall predicted in Northern Sector</p>
<div class="flex items-center justify-between">
<span class="text-xs text-slate-400">AI Confidence: 87%</span>
<i class="ri-cloudy-2-line text-yellow-400"></i>
</div>
</div>
<div class="bg-orange-500/10 border border-orange-500/30 rounded-lg p-3">
<div class="flex items-center justify-between mb-2">
<span class="text-orange-400 text-sm font-medium">MEDIUM</span>
<span class="text-xs text-slate-400">12 min ago</span>
</div>
<p class="text-sm mb-2">Drainage system capacity at 75% in Zone B</p>
<div class="flex items-center justify-between">
<span class="text-xs text-slate-400">AI Confidence: 78%</span>
<i class="ri-water-flash-line text-orange-400"></i>
</div>
</div>
<div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3">
<div class="flex items-center justify-between mb-2">
<span class="text-blue-400 text-sm font-medium">INFO</span>
<span class="text-xs text-slate-400">18 min ago</span>
</div>
<p class="text-sm mb-2">Weather monitoring station online in Sector 12</p>
<div class="flex items-center justify-between">
<span class="text-xs text-slate-400">AI Confidence: 99%</span>
<i class="ri-checkbox-circle-line text-blue-400"></i>
</div>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-alarm-line text-red-500 mr-2"></i>
Emergency SOS
</h3>
<button id="sosButton" class="w-full bg-red-500 hover:bg-red-600 text-white px-6 py-4 rounded-button font-semibold text-lg mb-4 animate-pulse whitespace-nowrap">
<i class="ri-alarm-warning-line mr-2"></i>
RAISE SOS
</button>
<div class="space-y-3">
<div class="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Medical Emergency</span>
<span class="text-xs text-red-400">URGENT</span>
</div>
<p class="text-xs text-slate-400 mb-2">Location: Sector 15, Building A-203</p>
<p class="text-xs text-slate-400">Assigned: Team Alpha-1 (ETA: 8 min)</p>
</div>
<div class="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Evacuation Request</span>
<span class="text-xs text-yellow-400">HIGH</span>
</div>
<p class="text-xs text-slate-400 mb-2">Location: Riverside Apartments, Block C</p>
<p class="text-xs text-slate-400">Assigned: Team Beta-2 (ETA: 15 min)</p>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-brain-line text-primary mr-2"></i>
AI Insights
</h3>
<div class="space-y-4">
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Flood Risk Prediction</span>
<span class="text-primary text-sm">Next 24h</span>
</div>
<div class="w-full bg-slate-700 rounded-full h-2 mb-2">
<div class="bg-gradient-to-r from-yellow-500 to-red-500 h-2 rounded-full" style="width: 78%"></div>
</div>
<p class="text-xs text-slate-400">78% chance of flooding in low-lying areas</p>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Evacuation Routes</span>
<span class="text-green-400 text-sm">Optimized</span>
</div>
<p class="text-xs text-slate-400 mb-2">AI has calculated 5 safe evacuation routes</p>
<button class="text-primary text-xs hover:underline">View Routes →</button>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Resource Allocation</span>
<span class="text-blue-400 text-sm">Balanced</span>
</div>
<p class="text-xs text-slate-400">Teams distributed optimally across risk zones</p>
</div>
</div>
</div>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">Active Alerts</p>
<p class="text-2xl font-bold text-red-400">23</p>
</div>
<div class="w-12 h-12 bg-red-500/20 rounded-lg flex items-center justify-center">
<i class="ri-alarm-warning-line text-red-400 text-xl"></i>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">People Evacuated</p>
<p class="text-2xl font-bold text-green-400">1,247</p>
</div>
<div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
<i class="ri-user-3-line text-green-400 text-xl"></i>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">Rescue Operations</p>
<p class="text-2xl font-bold text-blue-400">15</p>
</div>
<div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
<i class="ri-plane-line text-blue-400 text-xl"></i>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">AI Accuracy</p>
<p class="text-2xl font-bold text-primary">94.2%</p>
</div>
<div class="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
<i class="ri-brain-line text-primary text-xl"></i>
</div>
</div>
</div>
</div>
</div>
<div id="analyticsPage" class="hidden">
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h2 class="text-xl font-semibold flex items-center mb-6">
<i class="ri-line-chart-line text-primary mr-2"></i>
Historical Data Analysis
</h2>
<div id="historicalChart" class="h-80"></div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-bubble-chart-line text-primary mr-2"></i>
Risk Distribution
</h3>
<div id="riskChart" class="h-64"></div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-bar-chart-grouped-line text-primary mr-2"></i>
Response Metrics
</h3>
<div id="responseChart" class="h-64"></div>
</div>
</div>
</div>
<div class="space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-ai-generate text-primary mr-2"></i>
AI Predictions
</h3>
<div class="space-y-4">
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Flood Risk Level</span>
<span class="text-yellow-400">High</span>
</div>
<div class="w-full bg-slate-700 rounded-full h-2 mb-2">
<div class="bg-yellow-400 h-2 rounded-full" style="width: 75%"></div>
</div>
<p class="text-xs text-slate-400">75% probability in next 48 hours</p>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Infrastructure Impact</span>
<span class="text-orange-400">Medium</span>
</div>
<div class="w-full bg-slate-700 rounded-full h-2 mb-2">
<div class="bg-orange-400 h-2 rounded-full" style="width: 45%"></div>
</div>
<p class="text-xs text-slate-400">45% potential damage risk</p>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Population at Risk</span>
<span class="text-red-400">Critical</span>
</div>
<div class="w-full bg-slate-700 rounded-full h-2 mb-2">
<div class="bg-red-400 h-2 rounded-full" style="width: 85%"></div>
</div>
<p class="text-xs text-slate-400">85% in flood-prone areas</p>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-calendar-event-line text-primary mr-2"></i>
Seasonal Analysis
</h3>
<div id="seasonalChart" class="h-48"></div>
</div>
</div>
</div>
<div class="grid grid-cols-1 md:grid-cols-4 gap-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">Accuracy Rate</p>
<p class="text-2xl font-bold text-primary">96.5%</p>
</div>
<div class="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center">
<i class="ri-percent-line text-primary text-xl"></i>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">Data Points</p>
<p class="text-2xl font-bold text-blue-400">124K</p>
</div>
<div class="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
<i class="ri-database-2-line text-blue-400 text-xl"></i>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">Predictions Made</p>
<p class="text-2xl font-bold text-green-400">5,847</p>
</div>
<div class="w-12 h-12 bg-green-500/20 rounded-lg flex items-center justify-center">
<i class="ri-radar-line text-green-400 text-xl"></i>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between">
<div>
<p class="text-slate-400 text-sm">Alert Success</p>
<p class="text-2xl font-bold text-yellow-400">98.2%</p>
</div>
<div class="w-12 h-12 bg-yellow-500/20 rounded-lg flex items-center justify-center">
<i class="ri-notification-badge-line text-yellow-400 text-xl"></i>
</div>
</div>
</div>
</div>
</div>
<div id="teamsPage" class="hidden">
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<div class="flex items-center justify-between mb-6">
<h2 class="text-xl font-semibold flex items-center">
<i class="ri-team-line text-primary mr-2"></i>
Active Teams
</h2>
<button class="bg-primary/20 text-primary border border-primary/30 px-4 py-2 rounded-button text-sm hover:bg-primary/30 transition-colors whitespace-nowrap">
<i class="ri-add-line mr-1"></i>
Add Team
</button>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
<div class="bg-slate-800/50 rounded-lg p-4 border border-slate-600/30">
<div class="flex items-center space-x-3 mb-3">
<div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center">
<i class="ri-team-line text-blue-400"></i>
</div>
<div>
<h4 class="font-medium">Rapid Response Unit</h4>
<p class="text-sm text-slate-400">Team ID: RR-001</p>
</div>
</div>
<div class="space-y-2 mb-3">
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Status:</span>
<span class="text-green-400">Active</span>
</div>
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Members:</span>
<span>8</span>
</div>
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Location:</span>
<span>Zone A</span>
</div>
</div>
<div class="flex space-x-2">
<button class="flex-1 bg-slate-700/50 text-white px-3 py-1.5 rounded-button text-sm hover:bg-slate-700 transition-colors whitespace-nowrap">
Details
</button>
<button class="flex-1 bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded-button text-sm hover:bg-primary/30 transition-colors whitespace-nowrap contact-team-btn" data-team-id="RR-001">
Contact
</button>
</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4 border border-slate-600/30">
<div class="flex items-center space-x-3 mb-3">
<div class="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
<i class="ri-team-line text-green-400"></i>
</div>
<div>
<h4 class="font-medium">Medical Response Team</h4>
<p class="text-sm text-slate-400">Team ID: MR-002</p>
</div>
</div>
<div class="space-y-2 mb-3">
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Status:</span>
<span class="text-yellow-400">On Mission</span>
</div>
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Members:</span>
<span>6</span>
</div>
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Location:</span>
<span>Zone C</span>
</div>
</div>
<div class="flex space-x-2">
<button class="flex-1 bg-slate-700/50 text-white px-3 py-1.5 rounded-button text-sm hover:bg-slate-700 transition-colors whitespace-nowrap">
Details
</button>
<button class="flex-1 bg-primary/20 text-primary border border-primary/30 px-3 py-1.5 rounded-button text-sm hover:bg-primary/30 transition-colors whitespace-nowrap contact-team-btn" data-team-id="MR-002">
Contact
</button>
</div>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-map-pin-line text-primary mr-2"></i>
Team Locations
</h3>
<div class="relative h-96 bg-slate-800 rounded-lg overflow-hidden">
<div class="absolute inset-0 bg-cover bg-center" style="background-image: url('https://public.readdy.ai/gen_page/map_placeholder_1280x720.png')"></div>
</div>
</div>
</div>
<div class="space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-notification-4-line text-primary mr-2"></i>
Team Updates
</h3>
<div class="space-y-4">
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Rapid Response Unit</span>
<span class="text-xs text-green-400">5 min ago</span>
</div>
<p class="text-sm text-slate-400 mb-2">Successfully evacuated 23 residents from flood-prone area</p>
<div class="flex items-center text-xs text-slate-500">
<i class="ri-map-pin-line mr-1"></i>
Sector 7, Block B
</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<div class="flex items-center justify-between mb-2">
<span class="text-sm font-medium">Medical Response Team</span>
<span class="text-xs text-green-400">15 min ago</span>
</div>
<p class="text-sm text-slate-400 mb-2">Provided medical assistance to 8 people at temporary shelter</p>
<div class="flex items-center text-xs text-slate-500">
<i class="ri-map-pin-line mr-1"></i>
Community Center, Zone A
</div>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-calendar-todo-line text-primary mr-2"></i>
Upcoming Shifts
</h3>
<div class="space-y-3">
<div class="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
<div class="flex items-center justify-between mb-1">
<span class="font-medium">Morning Shift</span>
<span class="text-xs text-primary">06:00 - 14:00</span>
</div>
<p class="text-sm text-slate-400">Team: Alpha Squad</p>
<p class="text-xs text-slate-500">4 members on duty</p>
</div>
<div class="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
<div class="flex items-center justify-between mb-1">
<span class="font-medium">Evening Shift</span>
<span class="text-xs text-primary">14:00 - 22:00</span>
</div>
<p class="text-sm text-slate-400">Team: Beta Squad</p>
<p class="text-xs text-slate-500">5 members on duty</p>
</div>
<div class="bg-slate-800/50 rounded-lg p-3 border border-slate-600/30">
<div class="flex items-center justify-between mb-1">
<span class="font-medium">Night Shift</span>
<span class="text-xs text-primary">22:00 - 06:00</span>
</div>
<p class="text-sm text-slate-400">Team: Gamma Squad</p>
<p class="text-xs text-slate-500">6 members on duty</p>
</div>
</div>
</div>
</div>
</div>
</div>
<div id="settingsPage" class="hidden">
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
<div class="lg:col-span-2 space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h2 class="text-xl font-semibold flex items-center mb-6">
<i class="ri-settings-3-line text-primary mr-2"></i>
System Settings
</h2>
<div class="space-y-6">
<div>
<h3 class="text-lg font-medium mb-4">Notifications</h3>
<div class="space-y-4">
<div class="flex items-center justify-between">
<div>
<p class="font-medium">Emergency Alerts</p>
<p class="text-sm text-slate-400">Receive critical emergency notifications</p>
</div>
<label class="relative inline-flex items-center cursor-pointer">
<input type="checkbox" class="sr-only peer" checked="">
<div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
<div class="flex items-center justify-between">
<div>
<p class="font-medium">Team Updates</p>
<p class="text-sm text-slate-400">Get updates about team activities</p>
</div>
<label class="relative inline-flex items-center cursor-pointer">
<input type="checkbox" class="sr-only peer" checked="">
<div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
<div class="flex items-center justify-between">
<div>
<p class="font-medium">System Alerts</p>
<p class="text-sm text-slate-400">Receive system maintenance notifications</p>
</div>
<label class="relative inline-flex items-center cursor-pointer">
<input type="checkbox" class="sr-only peer">
<div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
</div>
</div>
<div>
<h3 class="text-lg font-medium mb-4">Map Settings</h3>
<div class="space-y-4">
<div>
<label class="block text-sm font-medium mb-2">Default View</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>Satellite View</option>
<option>Terrain View</option>
<option>Street View</option>
</select>
</div>
<div>
<label class="block text-sm font-medium mb-2">Update Frequency</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>Real-time</option>
<option>Every 5 minutes</option>
<option>Every 15 minutes</option>
<option>Every 30 minutes</option>
</select>
</div>
</div>
</div>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-database-2-line text-primary mr-2"></i>
Data Management
</h3>
<div class="space-y-4">
<div>
<label class="block text-sm font-medium mb-2">Data Retention Period</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>30 days</option>
<option>60 days</option>
<option>90 days</option>
<option>180 days</option>
</select>
</div>
<div>
<label class="block text-sm font-medium mb-2">Backup Frequency</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>Daily</option>
<option>Weekly</option>
<option>Monthly</option>
</select>
</div>
<button class="w-full bg-primary/20 text-primary border border-primary/30 px-4 py-2 rounded-button text-sm hover:bg-primary/30 transition-colors whitespace-nowrap mt-4">
<i class="ri-download-cloud-line mr-1"></i>
Export Data
</button>
</div>
</div>
</div>
<div class="space-y-6">
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-shield-keyhole-line text-primary mr-2"></i>
Security Settings
</h3>
<div class="space-y-4">
<div>
<label class="block text-sm font-medium mb-2">Two-Factor Authentication</label>
<label class="relative inline-flex items-center cursor-pointer">
<input type="checkbox" class="sr-only peer" checked="">
<div class="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
</label>
</div>
<div>
<label class="block text-sm font-medium mb-2">Session Timeout</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>15 minutes</option>
<option>30 minutes</option>
<option>1 hour</option>
<option>4 hours</option>
</select>
</div>
<button class="w-full bg-red-500/20 text-red-400 border border-red-500/30 px-4 py-2 rounded-button text-sm hover:bg-red-500/30 transition-colors whitespace-nowrap mt-2">
<i class="ri-logout-box-line mr-1"></i>
Logout All Devices
</button>
</div>
</div>
<div class="bg-slate-900/50 backdrop-blur-sm rounded-xl border border-slate-700/50 p-6">
<h3 class="text-lg font-semibold mb-4 flex items-center">
<i class="ri-user-settings-line text-primary mr-2"></i>
Account Settings
</h3>
<div class="space-y-4">
<div>
<label class="block text-sm font-medium mb-2">Email</label>
<input type="email" value="admin@jalraksha.ai" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white" readonly="">
</div>
<div>
<label class="block text-sm font-medium mb-2">Language</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>English</option>
<option>Hindi</option>
<option>Marathi</option>
</select>
</div>
<div>
<label class="block text-sm font-medium mb-2">Time Zone</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>Asia/Kolkata (GMT+5:30)</option>
<option>UTC</option>
<option>Pacific Time</option>
</select>
</div>
</div>
</div>
</div>
</div>
</div>
</main>
<div id="sosModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm hidden z-50">
<div class="flex items-center justify-center min-h-screen p-4">
<div class="bg-slate-900 rounded-xl border border-slate-700 p-6 w-full max-w-md">
<div class="flex items-center justify-between mb-4">
<h3 class="text-xl font-semibold text-red-400">Emergency SOS</h3>
<button id="closeSos" class="w-8 h-8 flex items-center justify-center text-slate-400 hover:text-white">
<i class="ri-close-line"></i>
</button>
</div>
<form class="space-y-4">
<div>
<label class="block text-sm font-medium mb-2">Emergency Type</label>
<select class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white pr-8">
<option>Medical Emergency</option>
<option>Evacuation Needed</option>
<option>Food &amp; Water</option>
<option>Shelter Required</option>
</select>
</div>
<div>
<label class="block text-sm font-medium mb-2">Location</label>
<input type="text" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white" placeholder="Enter your location">
</div>
<div>
<label class="block text-sm font-medium mb-2">Description</label>
<textarea class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white h-20" placeholder="Describe the emergency..."></textarea>
</div>
<div>
<label class="block text-sm font-medium mb-2">Contact Number</label>
<input type="tel" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-white" placeholder="Your phone number">
</div>
<button type="submit" class="w-full bg-red-500 hover:bg-red-600 text-white px-4 py-3 rounded-button font-semibold whitespace-nowrap">
Submit Emergency Request
</button>
</form>
</div>
</div>
</div>
<script id="waterChart">
document.addEventListener('DOMContentLoaded', function() {
const waterChart = echarts.init(document.getElementById('waterChart'));
const waterOption = {
animation: false,
backgroundColor: 'transparent',
textStyle: { color: '#94a3b8' },
grid: { top: 0, right: 0, bottom: 0, left: 0 },
xAxis: {
type: 'category',
data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
axisLine: { lineStyle: { color: '#475569' } },
axisTick: { show: false },
axisLabel: { color: '#94a3b8', fontSize: 10 }
},
yAxis: {
type: 'value',
axisLine: { show: false },
axisTick: { show: false },
axisLabel: { color: '#94a3b8', fontSize: 10 },
splitLine: { lineStyle: { color: '#334155' } }
},
series: [{
data: [2.1, 2.8, 3.2, 4.1, 3.9, 3.5],
type: 'line',
smooth: true,
symbol: 'none',
lineStyle: { color: 'rgba(87, 181, 231, 1)', width: 2 },
areaStyle: {
color: {
type: 'linear',
x: 0, y: 0, x2: 0, y2: 1,
colorStops: [
{ offset: 0, color: 'rgba(87, 181, 231, 0.3)' },
{ offset: 1, color: 'rgba(87, 181, 231, 0.1)' }
]
}
}
}],
tooltip: {
backgroundColor: 'rgba(15, 23, 42, 0.9)',
borderColor: '#475569',
textStyle: { color: '#f1f5f9' }
}
};
waterChart.setOption(waterOption);
});
</script>
<script id="rainfallChart">
document.addEventListener('DOMContentLoaded', function() {
const rainfallChart = echarts.init(document.getElementById('rainfallChart'));
const rainfallOption = {
animation: false,
backgroundColor: 'transparent',
textStyle: { color: '#94a3b8' },
grid: { top: 0, right: 0, bottom: 0, left: 0 },
xAxis: {
type: 'category',
data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
axisLine: { lineStyle: { color: '#475569' } },
axisTick: { show: false },
axisLabel: { color: '#94a3b8', fontSize: 10 }
},
yAxis: {
type: 'value',
axisLine: { show: false },
axisTick: { show: false },
axisLabel: { color: '#94a3b8', fontSize: 10 },
splitLine: { lineStyle: { color: '#334155' } }
},
series: [{
data: [15, 32, 28, 45, 67, 23, 12],
type: 'bar',
itemStyle: {
color: 'rgba(251, 191, 114, 1)',
borderRadius: [4, 4, 0, 0]
}
}],
tooltip: {
backgroundColor: 'rgba(15, 23, 42, 0.9)',
borderColor: '#475569',
textStyle: { color: '#f1f5f9' }
}
};
rainfallChart.setOption(rainfallOption);
});
</script>
<script id="sosModal">
document.addEventListener('DOMContentLoaded', function() {
const sosButton = document.getElementById('sosButton');
const sosModal = document.getElementById('sosModal');
const closeSos = document.getElementById('closeSos');
sosButton.addEventListener('click', function() {
sosModal.classList.remove('hidden');
});
closeSos.addEventListener('click', function() {
sosModal.classList.add('hidden');
});
sosModal.addEventListener('click', function(e) {
if (e.target === sosModal) {
sosModal.classList.add('hidden');
}
});
});
</script>
<script id="mapInteractions">
document.addEventListener('DOMContentLoaded', function() {
const cityData = {
mumbai: {
name: 'Mumbai',
riskLevel: 'High',
color: 'text-red-500',
populationAtRisk: '245,000',
activeAlerts: 12,
waterLevel: '4.5m above normal',
rainfall: 'Extreme (180mm/day)',
evacuationStatus: 'Urgent Evacuation',
historicalEvents: [
{
date: '2024-08-15',
event: 'Major flooding in lower areas',
impact: 'Over 1000 people evacuated',
severity: 'Severe'
},
{
date: '2023-07-26',
event: 'Coastal flooding due to cyclone',
impact: '500 homes damaged',
severity: 'High'
},
{
date: '2022-09-03',
event: 'Flash floods in suburban areas',
impact: 'Infrastructure damage',
severity: 'Moderate'
}
]
},
chennai: {
name: 'Chennai',
riskLevel: 'Medium',
color: 'text-yellow-500',
populationAtRisk: '125,000',
activeAlerts: 8,
waterLevel: '2.8m above normal',
rainfall: 'Heavy (120mm/day)',
evacuationStatus: 'Partial Evacuation',
historicalEvents: [
{
date: '2024-06-12',
event: 'Urban flooding',
impact: 'Transportation disrupted',
severity: 'Moderate'
},
{
date: '2023-11-30',
event: 'Monsoon flooding',
impact: '300 families relocated',
severity: 'High'
}
]
},
kolkata: {
name: 'Kolkata',
riskLevel: 'Medium-High',
color: 'text-orange-500',
populationAtRisk: '180,000',
activeAlerts: 10,
waterLevel: '3.2m above normal',
rainfall: 'Very Heavy (150mm/day)',
evacuationStatus: 'In Progress',
historicalEvents: [
{
date: '2024-07-20',
event: 'River overflow',
impact: 'Low-lying areas affected',
severity: 'High'
},
{
date: '2023-08-15',
event: 'Heavy rainfall flooding',
impact: '400 people evacuated',
severity: 'Moderate'
}
]
},
delhi: {
name: 'Delhi',
riskLevel: 'Low',
color: 'text-green-500',
populationAtRisk: '50,000',
activeAlerts: 3,
waterLevel: '1.5m above normal',
rainfall: 'Moderate (60mm/day)',
evacuationStatus: 'Monitoring',
historicalEvents: [
{
date: '2024-05-10',
event: 'Local flooding',
impact: 'Minor disruptions',
severity: 'Low'
},
{
date: '2023-07-28',
event: 'Brief flash floods',
impact: 'Temporary road closures',
severity: 'Low'
}
]
}
};
const modal = document.getElementById('cityModal');
const cityName = modal.querySelector('.city-name');
const riskLevel = modal.querySelector('.risk-level');
const populationAtRisk = modal.querySelector('.population-at-risk');
const activeAlerts = modal.querySelector('.active-alerts');
const waterLevel = modal.querySelector('.water-level');
const rainfall = modal.querySelector('.rainfall');
const evacuationStatus = modal.querySelector('.evacuation-status');
const historicalEvents = modal.querySelector('.historical-events');
document.querySelectorAll('.map-marker').forEach(marker => {
marker.addEventListener('click', () => {
const city = marker.dataset.city;
const data = cityData[city];
cityName.textContent = data.name;
cityName.className = `text-xl font-semibold ${data.color}`;
riskLevel.textContent = data.riskLevel;
riskLevel.className = `text-2xl font-bold ${data.color}`;
populationAtRisk.textContent = data.populationAtRisk;
activeAlerts.textContent = data.activeAlerts;
waterLevel.textContent = data.waterLevel;
rainfall.textContent = data.rainfall;
evacuationStatus.textContent = data.evacuationStatus;
historicalEvents.innerHTML = data.historicalEvents.map(event => `
<div class="border-l-2 border-slate-700 pl-4 py-2">
<div class="flex items-center justify-between mb-1">
<span class="text-sm font-medium">${event.date}</span>
<span class="text-xs px-2 py-1 rounded-full ${getSeverityClass(event.severity)}">${event.severity}</span>
</div>
<p class="text-sm mb-1">${event.event}</p>
<p class="text-xs text-slate-400">${event.impact}</p>
</div>
`).join('');
modal.classList.remove('hidden');
});
});
function getSeverityClass(severity) {
switch(severity.toLowerCase()) {
case 'severe':
return 'bg-red-500/20 text-red-400';
case 'high':
return 'bg-orange-500/20 text-orange-400';
case 'moderate':
return 'bg-yellow-500/20 text-yellow-400';
default:
return 'bg-blue-500/20 text-blue-400';
}
}
modal.querySelector('.close-city-modal').addEventListener('click', () => {
modal.classList.add('hidden');
});
modal.addEventListener('click', (e) => {
if (e.target === modal) {
modal.classList.add('hidden');
}
});
setInterval(function() {
const alertIndicator = document.querySelector('.animate-pulse');
if (alertIndicator) {
alertIndicator.style.opacity = '0.3';
setTimeout(() => {
alertIndicator.style.opacity = '1';
}, 200);
}
}, 30000);
});
</script>
<div id="contactModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm hidden z-50">
<div class="flex items-center justify-center min-h-screen p-4">
<div class="bg-slate-900 rounded-xl border border-slate-700 p-6 w-full max-w-md">
<div class="flex items-center justify-between mb-6">
<h3 class="text-xl font-semibold text-white team-name">Team Contact Information</h3>
<button class="close-contact-modal w-8 h-8 flex items-center justify-center text-slate-400 hover:text-white">
<i class="ri-close-line"></i>
</button>
</div>
<div class="space-y-6">
<div class="bg-slate-800/50 rounded-lg p-4">
<h4 class="text-lg font-medium mb-3">Team Leader</h4>
<div class="flex items-center space-x-3 mb-4">
<div class="w-12 h-12 bg-primary/20 rounded-full flex items-center justify-center">
<i class="ri-user-star-line text-primary text-xl"></i>
</div>
<div>
<p class="font-medium team-leader">Rajesh Kumar</p>
<p class="text-sm text-slate-400">On Duty</p>
</div>
</div>
<div class="space-y-2">
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Status:</span>
<span class="text-green-400">Available</span>
</div>
<div class="flex items-center justify-between text-sm">
<span class="text-slate-400">Experience:</span>
<span>8 years</span>
</div>
</div>
</div>
<div class="bg-slate-800/50 rounded-lg p-4">
<h4 class="text-lg font-medium mb-3">Contact Details</h4>
<div class="space-y-4">
<div>
<p class="text-sm text-slate-400 mb-1">Emergency Contact</p>
<div class="flex items-center space-x-2">
<i class="ri-phone-line text-primary"></i>
<span class="emergency-phone">+91 98765 43210</span>
</div>
</div>
<div>
<p class="text-sm text-slate-400 mb-1">Radio Frequency</p>
<div class="flex items-center space-x-2">
<i class="ri-radio-line text-primary"></i>
<span class="radio-freq">Channel 7 (162.425 MHz)</span>
</div>
</div>
<div>
<p class="text-sm text-slate-400 mb-1">Email</p>
<div class="flex items-center space-x-2">
<i class="ri-mail-line text-primary"></i>
<span class="team-email">rr001@jalraksha.ai</span>
</div>
</div>
</div>
</div>
<div class="grid grid-cols-3 gap-3">
<button class="bg-green-500/20 text-green-400 border border-green-500/30 px-4 py-2 rounded-button text-sm hover:bg-green-500/30 transition-colors whitespace-nowrap flex items-center justify-center">
<i class="ri-phone-line mr-2"></i>
Call
</button>
<button class="bg-blue-500/20 text-blue-400 border border-blue-500/30 px-4 py-2 rounded-button text-sm hover:bg-blue-500/30 transition-colors whitespace-nowrap flex items-center justify-center">
<i class="ri-message-2-line mr-2"></i>
Message
</button>
<button class="bg-red-500/20 text-red-400 border border-red-500/30 px-4 py-2 rounded-button text-sm hover:bg-red-500/30 transition-colors whitespace-nowrap flex items-center justify-center">
<i class="ri-alarm-warning-line mr-2"></i>
Dispatch
</button>
</div>
</div>
</div>
</div>
</div>

<script id="contactModal">
document.addEventListener('DOMContentLoaded', function() {
    const teamData = {
        'RR-001': {
            name: 'Rapid Response Unit',
            leader: 'Rajesh Kumar',
            status: 'Available',
            experience: '8 years',
            emergency: '+91 98765 43210',
            radio: 'Channel 7 (162.425 MHz)',
            email: 'rr001@jalraksha.ai'
        },
        'MR-002': {
            name: 'Medical Response Team',
            leader: 'Dr. Priya Sharma',
            status: 'On Mission',
            experience: '12 years',
            emergency: '+91 98765 43211',
            radio: 'Channel 8 (162.450 MHz)',
            email: 'mr002@jalraksha.ai'
        }
    };

    const contactModal = document.getElementById('contactModal');
    const closeContactBtn = contactModal.querySelector('.close-contact-modal');

    document.querySelectorAll('.contact-team-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const teamId = btn.dataset.teamId;
            const team = teamData[teamId];
            
            if (team) {
                contactModal.querySelector('.team-name').textContent = team.name;
                contactModal.querySelector('.team-leader').textContent = team.leader;
                contactModal.querySelector('.emergency-phone').textContent = team.emergency;
                contactModal.querySelector('.radio-freq').textContent = team.radio;
                contactModal.querySelector('.team-email').textContent = team.email;
                
                contactModal.classList.remove('hidden');
            }
        });
    });

    closeContactBtn.addEventListener('click', () => {
        contactModal.classList.add('hidden');
    });

    contactModal.addEventListener('click', (e) => {
        if (e.target === contactModal) {
            contactModal.classList.add('hidden');
        }
    });
});
</script>

<script id="navHighlight">
document.addEventListener('DOMContentLoaded', function() {
const pages = {
dashboard: document.querySelector('#dashboardPage'),
analytics: document.querySelector('#analyticsPage'),
teams: document.querySelector('#teamsPage'),
settings: document.querySelector('#settingsPage')
};
const navButtons = {
dashboard: document.getElementById('dashboardBtn'),
analytics: document.getElementById('analyticsBtn'),
teams: document.getElementById('teamsBtn'),
settings: document.getElementById('settingsBtn')
};
function showPage(pageId) {
Object.values(pages).forEach(page => {
if (page) {
page.classList.add('hidden');
}
});
if (pages[pageId]) {
pages[pageId].classList.remove('hidden');
}
}
Object.entries(navButtons).forEach(([pageId, button]) => {
if (button) {
button.addEventListener('click', function() {
Object.values(navButtons).forEach(btn => {
if (btn) {
btn.className = 'text-slate-300 hover:text-primary transition-colors';
}
});
this.className = 'text-primary hover:text-primary transition-colors relative after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-primary after:rounded-full';
showPage(pageId);
});
}
});
showPage('dashboard');
});
</script>

<script>
    (function() {
      const imgs = Array.from(document.querySelectorAll('img'));
      Promise.all(imgs.map((img) => new Promise((resolve) => {
        img.onload = () => {
          resolve(null);
        };
      }))).finally(() => {
        window.parent.postMessage({
          type: 'iframeHeight',
          height: document.body.offsetHeight
        }, '*');
      })
    })()
  </script><script>
      (function () {
  'use strict';

  const originalWindowOpen = window.originalWindowOpen ?? window.open;

  function processAnchor(url) {
    // 查找锚点，平滑滚动
    const anchor = document.querySelector(url);
    if (anchor) {
      anchor.scrollIntoView({ behavior: 'smooth' });
    }
    // 发送 hashchange 事件
    const event = new Event('hashchange');
    event.newURL = url;
    event.oldURL = window.location.href;
    // 因为预览 iframe 没有 url，所以需要手动设置
    window.location.hash = url;
    window.dispatchEvent(event);
  }

  // 重写 window.open
  window.open = function (url, target, features) {
    if (url.startsWith('#')) {
      // 查找锚点，平滑滚动
      processAnchor(url);
      return;
    }
    originalWindowOpen(url, '_blank', features);
    return null;
  };
})();

      
  window.addEventListener('click', (event) => {
    const target = event.target;
    const closest = target.closest('a');
    if (!closest) return;
    if (closest.tagName === 'A') {
      event.preventDefault();
      const href = closest.getAttribute('href');
      if (!href) return;
      // check is void link
      if (['#', 'javascript:void(0)', ''].includes(href)) {
        return;
      }
      // 锚点链接也不处理
      if (href.startsWith('#')) {
        return;
      }
      window.open(closest.href, '_blank');
    }
  });

      
  document.addEventListener('submit', (event) => {
    event.preventDefault();
  }, true);

    </script></body></html>