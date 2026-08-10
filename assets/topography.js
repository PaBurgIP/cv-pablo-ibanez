(() => {
  const canvas = document.getElementById('topography');
  if (!canvas) return;
  const gl = canvas.getContext('webgl2', {alpha:true, antialias:false, premultipliedAlpha:true});
  if (!gl) { canvas.hidden = true; return; }

  const vertex = `#version 300 es
  in vec2 position;
  void main(){gl_Position=vec4(position,0.0,1.0);}`;
  const fragment = `#version 300 es
  precision highp float;
  uniform vec2 iResolution;
  uniform float iTime;
  uniform vec2 uMouse;
  uniform float uMouseActive;
  out vec4 fragColor;
  float bez(float t,vec4 c){float w=6.2831853*t;return .5*(c.x*sin(w)+c.y*cos(w)+c.z*sin(2.*w)+c.w*cos(2.*w));}
  vec4 ctrl(float seed){return 2.7*vec4(sin(iTime*.12+seed),sin(iTime*.09+seed*2.1),sin(iTime*.07+seed*3.2),sin(iTime*.11+seed*4.3));}
  float field(vec2 uv){vec2 a=vec2(bez(uv.x,ctrl(1.)),bez(uv.x,ctrl(2.)));vec2 b=vec2(bez(uv.y,ctrl(3.)),bez(uv.y,ctrl(4.)));return distance(a,b);}
  void main(){
    vec2 uv=gl_FragCoord.xy/iResolution;
    vec2 d=uv-uMouse;d.x*=iResolution.x/max(iResolution.y,1.);
    float fv=field((uv-.5)/.92+.5)+exp(-dot(d,d)/.075)*.28*uMouseActive;
    float f=fv*2.35,part=fract(f),dist=min(part,1.-part),aa=fwidth(f)+.0001;
    float line=1.-smoothstep(.012-aa,.012+aa,dist);
    float glow=(1.-smoothstep(.012,.23+aa,dist))*.48;
    float elev=clamp(fv/7.5,0.,1.);
    vec3 low=vec3(.184,.561,.322),mid=vec3(.416,.855,.549),high=vec3(.949,.792,.424);
    vec3 col=mix(low,mid,smoothstep(0.,.5,elev));col=mix(col,high,smoothstep(.5,1.,elev));
    float alpha=clamp(line+glow*.5,0.,1.)*.74;
    float grain=fract(sin(dot(gl_FragCoord.xy,vec2(12.9898,78.233))+iTime)*43758.5453);
    alpha=clamp(alpha+(grain-.5)*.035,0.,1.);
    fragColor=vec4(col*alpha,alpha);
  }`;
  const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;};
  let program;
  try{program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(program));}
  catch(error){console.warn('Topography WebGL disabled:',error);canvas.hidden=true;return;}
  gl.useProgram(program);
  const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);
  const position=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(position);gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
  const resolution=gl.getUniformLocation(program,'iResolution'),time=gl.getUniformLocation(program,'iTime'),mouse=gl.getUniformLocation(program,'uMouse'),mouseActive=gl.getUniformLocation(program,'uMouseActive');
  let target=[.5,.5],current=[.5,.5],active=0,targetActive=0,raf=0,visible=true,pageVisible=!document.hidden;
  const resize=()=>{const dpr=Math.min(devicePixelRatio||1,2),r=canvas.getBoundingClientRect(),w=Math.max(1,Math.round(r.width*dpr)),h=Math.max(1,Math.round(r.height*dpr));if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h);}gl.uniform2f(resolution,w,h);};
  const render=ms=>{resize();current[0]+=(target[0]-current[0])*.05;current[1]+=(target[1]-current[1])*.05;active+=(targetActive-active)*.05;gl.uniform1f(time,ms*.001);gl.uniform2f(mouse,current[0],current[1]);gl.uniform1f(mouseActive,active);gl.drawArrays(gl.TRIANGLES,0,3);raf=requestAnimationFrame(render);};
  const start=()=>{if(visible&&pageVisible&&!raf)raf=requestAnimationFrame(render);};
  const stop=()=>{if(raf){cancelAnimationFrame(raf);raf=0;}};
  canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect();target=[(e.clientX-r.left)/r.width,1-(e.clientY-r.top)/r.height];targetActive=1;});
  canvas.addEventListener('pointerleave',()=>{targetActive=0;});
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(([e])=>{visible=e.isIntersecting;visible?start():stop();}).observe(canvas);
  document.addEventListener('visibilitychange',()=>{pageVisible=!document.hidden;pageVisible?start():stop();});
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){resize();gl.uniform1f(time,0);gl.uniform2f(mouse,.5,.5);gl.uniform1f(mouseActive,0);gl.drawArrays(gl.TRIANGLES,0,3);}else start();
})();
