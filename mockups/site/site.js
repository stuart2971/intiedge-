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

// contact form: live character counter, validation, and mailto compose
// (static site, no backend — matches the site's existing mailto pattern)
const cForm = document.getElementById('contactForm');
if (cForm) {
  const LIMIT = 1000;
  // Web3Forms access key: paste the key from web3forms.com here to deliver
  // submissions to shelly@intiedge.com. While empty, the form falls back to a
  // mailto compose so it always does something.
  const WEB3FORMS_KEY = '';
  const name = document.getElementById('cfName');
  const email = document.getElementById('cfEmail');
  const body = document.getElementById('cfBody');
  const count = document.getElementById('cfCount');
  const status = document.getElementById('cfStatus');
  const emailOK = v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

  const updateCount = () => {
    const n = body.value.length;
    count.textContent = n + ' / ' + LIMIT;
    count.classList.toggle('over', n >= LIMIT);
  };
  body.addEventListener('input', updateCount);
  updateCount();

  // clear a field's error state as soon as the user fixes it
  [name, email, body].forEach(el => el.addEventListener('input', () => el.closest('.field').classList.remove('invalid')));

  cForm.addEventListener('submit', async e => {
    e.preventDefault();
    status.classList.remove('show', 'err');
    const checks = [
      [name, name.value.trim().length > 0],
      [email, emailOK(email.value.trim())],
      [body, body.value.trim().length > 0 && body.value.length <= LIMIT]
    ];
    let firstBad = null;
    checks.forEach(([el, ok]) => {
      el.closest('.field').classList.toggle('invalid', !ok);
      if (!ok && !firstBad) firstBad = el;
    });
    if (firstBad) { firstBad.focus(); return; }

    // Web3Forms: post straight to Shelly's inbox without leaving the page.
    if (WEB3FORMS_KEY) {
      const btn = cForm.querySelector('button[type="submit"]');
      const label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending...';
      try {
        const res = await fetch('https://api.web3forms.com/submit', {
          method: 'POST',
          headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
          body: JSON.stringify({
            access_key: WEB3FORMS_KEY,
            subject: 'Website enquiry from ' + name.value.trim(),
            from_name: name.value.trim(),
            name: name.value.trim(),
            email: email.value.trim(),
            message: body.value.trim()
          })
        });
        const data = await res.json().catch(() => ({}));
        if (res.ok && data.success) {
          cForm.reset(); updateCount();
          status.textContent = 'Thanks, your message is on its way. Shelly will be in touch soon.';
          status.classList.add('show');
        } else {
          status.textContent = 'Something went wrong. Please email shelly@intiedge.com directly.';
          status.classList.add('show', 'err');
        }
      } catch (err) {
        status.textContent = 'Network error. Please email shelly@intiedge.com directly.';
        status.classList.add('show', 'err');
      } finally {
        btn.disabled = false; btn.textContent = label;
      }
      return;
    }

    // fallback (until the access key is set): open the visitor's email app
    const subject = 'Website enquiry from ' + name.value.trim();
    const message = body.value.trim() + '\n\nFrom: ' + name.value.trim() + '\nEmail: ' + email.value.trim();
    window.location.href = 'mailto:shelly@intiedge.com?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(message);
    status.textContent = 'Opening your email app...';
    status.classList.add('show');
  });
}

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
