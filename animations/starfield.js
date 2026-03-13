/**
 * CosmicAtlas – Fixed Starfield Engine for Streamlit
 */
(function () {
  'use strict';

  /* ── Canvas Setup (Target Parent if in Iframe) ──────────── */
  const doc = window.parent !== window ? window.parent.document : document;
  let canvas = doc.getElementById('starfieldCanvas');

  // If we can't find it, create it (fallback)
  if (!canvas) {
    canvas = doc.createElement('canvas');
    canvas.id = 'starfieldCanvas';
    Object.assign(canvas.style, {
      position: 'fixed', top: '0', left: '0',
      width: '100%', height: '100%',
      pointerEvents: 'none', zIndex: '0'
    });
    doc.body.insertBefore(canvas, doc.body.firstChild);
  }

  const ctx = canvas.getContext('2d');
  let W = window.parent.innerWidth || window.innerWidth;
  let H = window.parent.innerHeight || window.innerHeight;
  canvas.width  = W;
  canvas.height = H;

  window.addEventListener('resize', () => {
    W = window.parent.innerWidth || window.innerWidth;
    H = window.parent.innerHeight || window.innerHeight;
    canvas.width  = W;
    canvas.height = H;
    initStars();
  });

  /* ── Star Layers (Increased density) ────────────────────── */
  const STAR_LAYERS = [
    { count: 1000, speed: 0.10, size: [0.5, 1.2], alpha: [0.4, 0.7] },
    { count: 400,  speed: 0.25, size: [1.0, 2.0], alpha: [0.6, 0.9] },
    { count: 150,  speed: 0.50, size: [1.8, 3.2], alpha: [0.8, 1.0] },
  ];

  let stars = [];

  function initStars() {
    stars = [];
    STAR_LAYERS.forEach(layer => {
      for (let i = 0; i < layer.count; i++) {
        stars.push({
          x:     Math.random() * W,
          y:     Math.random() * H,
          r:     rnd(layer.size[0], layer.size[1]),
          alpha: rnd(layer.alpha[0], layer.alpha[1]),
          speed: layer.speed,
          twinklePhase: Math.random() * Math.PI * 2,
          twinkleSpeed: rnd(0.5, 2.0),
          color: '#ffffff'
        });
      }
    });
  }

  /* ── Asteroid Particles (Belt focus) ────────────────────── */
  const ASTEROIDS = 35;
  let asteroids = [];

  function initAsteroids() {
    asteroids = [];
    for (let i = 0; i < ASTEROIDS; i++) {
      asteroids.push({
        x:     Math.random() * W,
        y:     H * rnd(0.2, 0.8),
        r:     rnd(1, 4),
        vx:    rnd(-0.3, 0.3),
        vy:    rnd(-0.1, 0.1),
        alpha: rnd(0.2, 0.45),
      });
    }
  }

  /* ── Interaction ────────────────────────────────────────── */
  let mouseX = W / 2;
  let mouseY = H / 2;

  doc.addEventListener('mousemove', e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  /* ── Render Loop ────────────────────────────────────────── */
  let scrollY = 0;
  window.addEventListener('scroll', () => { scrollY = window.scrollY; });
  // Also check parent scroll
  if (window.parent) {
    window.parent.addEventListener('scroll', () => { scrollY = window.parent.scrollY; });
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // Darkening overlay (deep space)
    const depthAlpha = Math.min(scrollY / 5000, 0.8);
    ctx.fillStyle = `rgba(0,0,0,${depthAlpha})`;
    ctx.fillRect(0, 0, W, H);

    const pxFactor = (mouseX / W - 0.5) * 2;
    const pyFactor = (mouseY / H - 0.5) * 2;

    stars.forEach(s => {
      s.twinklePhase += s.twinkleSpeed * 0.02;
      const twinkle = 0.6 + Math.sin(s.twinklePhase) * 0.4;
      
      // Infinite loop wrap
      let drawX = (s.x + pxFactor * s.speed * 80 + W) % W;
      let drawY = (s.y + pyFactor * s.speed * 60 - (scrollY * s.speed * 0.5) + H) % H;

      // Outer glow
      const grd = ctx.createRadialGradient(drawX, drawY, 0, drawX, drawY, s.r * 3);
      grd.addColorStop(0, `rgba(255, 255, 255, ${s.alpha * twinkle * 0.5})`);
      grd.addColorStop(1, 'transparent');
      ctx.fillStyle = grd;
      ctx.beginPath();
      ctx.arc(drawX, drawY, s.r * 3, 0, Math.PI * 2);
      ctx.fill();

      // Sharp Core
      ctx.beginPath();
      ctx.arc(drawX, drawY, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 255, 255, ${s.alpha * twinkle})`;
      ctx.fill();
    });

    asteroids.forEach(a => {
      a.x += a.vx;
      a.y += a.vy;
      if (a.x < -10) a.x = W + 10;
      if (a.x > W + 10) a.x = -10;

      ctx.beginPath();
      ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(180, 180, 180, ${a.alpha})`;
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  /* ── Boot ───────────────────────────────────────────────── */
  function rnd(min, max) { return min + Math.random() * (max - min); }

  initStars();
  initAsteroids();
  draw();

  /* ── Sync CSS Props (Optional) ──────────────────────────── */
  let rot = 0;
  setInterval(() => {
    rot = (rot + 0.12) % 360;
    doc.documentElement.style.setProperty('--planet-rot', rot + 'deg');
  }, 50);

})();
