const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// reveal on scroll
if (!reduce) {
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), {threshold: .15});
  document.querySelectorAll('.rv').forEach(el => io.observe(el));
} else {
  document.querySelectorAll('.rv').forEach(el => el.classList.add('in'));
}

// adaptive calculator (present on Home and AI Enablement)
let applyCalcPersona = () => {};
const rRep = document.getElementById('rRep');
if (rRep) {
  const CALC = {
    mm: { rep: {min:20, max:300, step:5,  val:60},  proc: {min:20, max:500, step:10, val:100}, rate: {min:30, max:150, step:5, val:55} },
    sb: { rep: {min:5,  max:80,  step:5,  val:20},  proc: {min:5,  max:150, step:5,  val:30},  rate: {min:25, max:100, step:5, val:40} }
  };
  const rProc = document.getElementById('rProc'), rRate = document.getElementById('rRate');
  const oRep = document.getElementById('oRep'), oProc = document.getElementById('oProc'), oRate = document.getElementById('oRate');
  const hrs = document.getElementById('hrs'), dollars = document.getElementById('dollars');
  const fill = s => s.style.setProperty('--fill', ((s.value - s.min) / (s.max - s.min) * 100) + '%');
  function recalc() {
    oRep.textContent = rRep.value;
    oProc.textContent = rProc.value;
    oRate.textContent = '$' + rRate.value;
    [rRep, rProc, rRate].forEach(fill);
    const savedHours = Math.round((+rRep.value + +rProc.value) * 0.5 * 12);
    hrs.textContent = savedHours.toLocaleString('en-CA');
    dollars.textContent = (savedHours * +rRate.value).toLocaleString('en-CA');
  }
  applyCalcPersona = sb => {
    const p = CALC[sb ? 'sb' : 'mm'];
    [['rep', rRep], ['proc', rProc], ['rate', rRate]].forEach(([k, s]) => {
      s.min = p[k].min; s.max = p[k].max; s.step = p[k].step; s.value = p[k].val;
    });
    recalc();
  };
  [rRep, rProc, rRate].forEach(s => s.addEventListener('input', recalc));
  recalc();
}

// persona: the choice persists across pages (applied to <body> before paint by
// the inline head script); the toggle itself now lives only on the home hero.
const isSB = document.body.classList.contains('sb');
applyCalcPersona(isSB); // sync any calculator on the page to the stored choice

const segMM = document.getElementById('segMM'), segSB = document.getElementById('segSB');
if (segMM && segSB) {
  segMM.classList.toggle('on', !isSB);
  segSB.classList.toggle('on', isSB);
  const setPersona = sb => {
    document.body.classList.toggle('sb', sb);
    segMM.classList.toggle('on', !sb);
    segSB.classList.toggle('on', sb);
    applyCalcPersona(sb);
    try { localStorage.setItem('iePersona', sb ? 'sb' : 'mm'); } catch (e) {}
    document.body.classList.remove('switched');
    void document.body.offsetWidth;
    document.body.classList.add('switched');
  };
  segMM.addEventListener('click', () => setPersona(false));
  segSB.addEventListener('click', () => setPersona(true));
}

// challenges accordion: one open at a time
document.querySelectorAll('.acc-head').forEach(head => head.addEventListener('click', () => {
  const item = head.parentElement, body = item.querySelector('.acc-body'), wasOpen = item.classList.contains('open');
  document.querySelectorAll('.acc-item.open').forEach(o => {
    o.classList.remove('open');
    o.querySelector('.acc-body').style.maxHeight = '0';
  });
  if (!wasOpen) {
    item.classList.add('open');
    body.style.maxHeight = body.scrollHeight + 'px';
  }
}));

// node-line draw (timeline and bridge rows)
document.querySelectorAll('.how-grid').forEach(grid => {
  if (reduce) { grid.classList.add('drawn'); return; }
  const tio = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { grid.classList.add('drawn'); tio.unobserve(grid); }
  }), {threshold: .4});
  tio.observe(grid);
});

// services page: floating table-of-contents scroll-spy (highlights the active practice)
const toc = document.querySelector('.toc');
if (toc) {
  const heads = [...toc.querySelectorAll('.toc-head')];
  const groups = [...toc.querySelectorAll('.toc-group')];
  const tspy = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) {
      const id = '#' + e.target.id;
      heads.forEach(h => h.classList.toggle('on', h.getAttribute('href') === id));
      groups.forEach(g => g.classList.toggle('on', g.querySelector('.toc-head').getAttribute('href') === id));
    }
  }), {rootMargin: '-30% 0px -60% 0px'});
  heads.forEach(h => { const t = document.querySelector(h.getAttribute('href')); if (t) tspy.observe(t); });
}
