// ── Tab Switching ─────────────────────────────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.tab).classList.add('active');
  });
});

// ── Password Toggle ───────────────────────────────────────────────────────
document.querySelectorAll('.toggle-pw').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = document.getElementById(btn.dataset.target);
    const icon  = btn.querySelector('i');
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
      input.type = 'password';
      icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
  });
});

// ── Password Strength ─────────────────────────────────────────────────────
const embedPw       = document.getElementById('embed-password');
const strengthFill  = document.getElementById('embed-strength');
const strengthLabel = document.getElementById('embed-strength-label');

embedPw.addEventListener('input', () => {
  const val = embedPw.value;
  let score = 0;
  if (val.length >= 8)            score++;
  if (val.length >= 12)           score++;
  if (/[A-Z]/.test(val))         score++;
  if (/[0-9]/.test(val))         score++;
  if (/[^A-Za-z0-9]/.test(val)) score++;

  const levels = [
    { pct: '0%',   color: 'transparent', label: '' },
    { pct: '25%',  color: '#ff3b5c',     label: '⚠ Weak' },
    { pct: '50%',  color: '#ff6b35',     label: '▲ Fair' },
    { pct: '75%',  color: '#00d4ff',     label: '◆ Strong' },
    { pct: '90%',  color: '#00ff9d',     label: '✔ Very Strong' },
    { pct: '100%', color: '#00ff9d',     label: '✔ Excellent' },
  ];

  const lvl = levels[score] || levels[0];
  strengthFill.style.width      = lvl.pct;
  strengthFill.style.background = lvl.color;
  strengthFill.style.boxShadow  = score >= 3 ? `0 0 8px ${lvl.color}` : 'none';
  strengthLabel.textContent     = lvl.label;
  strengthLabel.style.color     = lvl.color;
});

// ── Video Preview ─────────────────────────────────────────────────────────
function setupVideoPreview(inputId, previewId, playerId) {
  const input   = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  const player  = document.getElementById(playerId);

  input.addEventListener('change', () => {
    const file = input.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      player.src = url;
      preview.classList.add('active');
    } else {
      preview.classList.remove('active');
      player.src = '';
    }
  });
}

setupVideoPreview('embed-video',   'embed-video-preview',   'embed-video-player');
setupVideoPreview('extract-video', 'extract-video-preview', 'extract-video-player');

// ── Drop Zone Setup ───────────────────────────────────────────────────────
function setupDropZone(dropId, inputId, infoId, accept) {
  const drop  = document.getElementById(dropId);
  const input = document.getElementById(inputId);
  const info  = document.getElementById(infoId);

  // Click anywhere in drop zone OR on browse span to open file picker
  
  
  const browseSpan = drop.querySelector('span');
  if (browseSpan) {
    browseSpan.addEventListener('click', (e) => {
      e.stopPropagation();
      input.click();
    });
  }

  input.addEventListener('change', () => {
    if (input.files[0]) showFileInfo(input.files[0], drop, info);
  });

  drop.addEventListener('dragover', e => {
    e.preventDefault();
    drop.classList.add('dragover');
  });

  drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));

  drop.addEventListener('drop', e => {
    e.preventDefault();
    drop.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
      const ext = file.name.split('.').pop().toLowerCase();
      if (!accept.includes(ext)) {
        showToast(`❌ File type .${ext} not allowed!`);
        return;
      }
      const dt = new DataTransfer();
      dt.items.add(file);
      input.files = dt.files;
      showFileInfo(file, drop, info);

      // Trigger preview if video
      input.dispatchEvent(new Event('change'));
    }
  });
}

function showFileInfo(file, drop, info) {
  drop.classList.add('has-file');
  drop.querySelector('i').className = 'fas fa-circle-check';
  drop.querySelector('i').style.color = 'var(--accent2)';
  const size = file.size < 1024 * 1024
    ? (file.size / 1024).toFixed(1) + ' KB'
    : (file.size / (1024 * 1024)).toFixed(2) + ' MB';
  info.textContent = `✔ ${file.name} (${size})`;
}

setupDropZone('embed-video-drop',  'embed-video',  'embed-video-info',  ['mp4','avi','mkv']);
setupDropZone('embed-secret-drop', 'embed-secret', 'embed-secret-info', ['pdf','txt','docx','png','jpg','jpeg','zip','gif','webp','bmp','mp3','wav','xlsx','csv']);
setupDropZone('extract-video-drop','extract-video','extract-video-info',['mp4','avi','mkv']);

// ── Progress Bar ──────────────────────────────────────────────────────────
function runProgress(barId, stepPrefix, stepCount, duration, callback) {
  const bar      = document.getElementById(barId);
  const wrap     = bar.closest('.progress-wrap');
  const lines    = wrap.querySelectorAll('.progress-line');

  wrap.classList.add('active');
  bar.style.width = '0%';

  // Reset all steps
  for (let i = 1; i <= stepCount; i++) {
    const step = document.getElementById(`${stepPrefix}${i}`);
    step.classList.remove('active', 'done');
  }
  lines.forEach(l => l.classList.remove('done'));

  let current = 0;
  const stepDuration = duration / stepCount;

  const interval = setInterval(() => {
    current++;

    // Mark previous as done
    if (current > 1) {
      const prev = document.getElementById(`${stepPrefix}${current - 1}`);
      prev.classList.remove('active');
      prev.classList.add('done');
      if (lines[current - 2]) lines[current - 2].classList.add('done');
    }

    if (current <= stepCount) {
      const step = document.getElementById(`${stepPrefix}${current}`);
      step.classList.add('active');
      bar.style.width = `${(current / stepCount) * 85}%`;
    }

    if (current >= stepCount) {
      clearInterval(interval);
      if (callback) callback();
    }
  }, stepDuration);

  return interval;
}

function completeProgress(barId, stepPrefix, stepCount) {
  const bar   = document.getElementById(barId);
  const wrap  = bar.closest('.progress-wrap');
  const lines = wrap.querySelectorAll('.progress-line');

  bar.style.width = '100%';

  for (let i = 1; i <= stepCount; i++) {
    const step = document.getElementById(`${stepPrefix}${i}`);
    step.classList.remove('active');
    step.classList.add('done');
  }
  lines.forEach(l => l.classList.add('done'));

  setTimeout(() => wrap.classList.remove('active'), 2000);
}

function resetProgress(barId, stepPrefix, stepCount) {
  const bar  = document.getElementById(barId);
  const wrap = bar.closest('.progress-wrap');
  wrap.classList.remove('active');
  bar.style.width = '0%';
  for (let i = 1; i <= stepCount; i++) {
    const step = document.getElementById(`${stepPrefix}${i}`);
    step.classList.remove('active', 'done');
  }
  wrap.querySelectorAll('.progress-line').forEach(l => l.classList.remove('done'));
}

// ── Toast ─────────────────────────────────────────────────────────────────
function showToast(message) {
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed; bottom: 2rem; right: 2rem; z-index: 9999;
    background: var(--card); border: 1px solid var(--danger);
    color: var(--text); padding: 1rem 1.5rem; border-radius: 12px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.85rem;
    box-shadow: 0 0 20px rgba(255,59,92,0.3);
    animation: fadeSlideIn 0.3s ease;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// ── Format Bytes ──────────────────────────────────────────────────────────
function formatBytes(bytes) {
  if (bytes < 1024)         return bytes + ' B';
  if (bytes < 1024 * 1024)  return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// ── EMBED ─────────────────────────────────────────────────────────────────
document.getElementById('embed-btn').addEventListener('click', async () => {
  const video    = document.getElementById('embed-video').files[0];
  const secret   = document.getElementById('embed-secret').files[0];
  const password = document.getElementById('embed-password').value.trim();
  const result   = document.getElementById('embed-result');

  if (!video)    return showToast('❌ Please select a cover video!');
  if (!secret)   return showToast('❌ Please select a secret file!');
  if (!password) return showToast('❌ Please enter a password!');
  if (password.length < 6) return showToast('❌ Password must be at least 6 characters!');

  const formData = new FormData();
  formData.append('video', video);
  formData.append('secret', secret);
  formData.append('password', password);

  result.innerHTML = '';
  resetProgress('embed-bar', 'ps-', 4);

  // Animate progress during processing
  runProgress('embed-bar', 'ps-', 4, 4000);

  try {
    const res  = await fetch('/embed', { method: 'POST', body: formData });
    const data = await res.json();

    completeProgress('embed-bar', 'ps-', 4);

    if (data.success) {
      result.innerHTML = `
        <div class="result-success">
          <h3><i class="fas fa-circle-check"></i> File Successfully Hidden!</h3>
          <div class="result-info">
            <div>SECRET FILE &nbsp;→ <span>${data.secret_filename}</span></div>
            <div>OUTPUT SIZE &nbsp;→ <span>${formatBytes(data.output_size)}</span></div>
            <div>INTEGRITY HASH → <span style="word-break:break-all">${data.original_hash}</span></div>
          </div>
          <a class="download-btn" href="${data.download_url}" download>
            <i class="fas fa-download"></i> Download Stego Video
          </a>
        </div>`;
    } else {
      result.innerHTML = `
        <div class="result-error">
          <h3><i class="fas fa-triangle-exclamation"></i> Error</h3>
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.85rem">${data.error}</p>
        </div>`;
    }
  } catch (err) {
    result.innerHTML = `
      <div class="result-error">
        <h3><i class="fas fa-triangle-exclamation"></i> Connection Error</h3>
        <p style="font-family:'Share Tech Mono',monospace;font-size:0.85rem">Could not reach the server. Is Flask running?</p>
      </div>`;
  }
});

// ── EXTRACT ───────────────────────────────────────────────────────────────
document.getElementById('extract-btn').addEventListener('click', async () => {
  const video    = document.getElementById('extract-video').files[0];
  const password = document.getElementById('extract-password').value.trim();
  const result   = document.getElementById('extract-result');

  if (!video)    return showToast('❌ Please select a stego video!');
  if (!password) return showToast('❌ Please enter the password!');

  const formData = new FormData();
  formData.append('video', video);
  formData.append('password', password);

  result.innerHTML = '';
  resetProgress('extract-bar', 'ep-', 4);

  // Animate progress during processing
  runProgress('extract-bar', 'ep-', 4, 4000);

  try {
    const res  = await fetch('/extract', { method: 'POST', body: formData });
    const data = await res.json();

    completeProgress('extract-bar', 'ep-', 4);

    if (data.success) {
      result.innerHTML = `
        <div class="result-success">
          <h3><i class="fas fa-circle-check"></i> File Successfully Extracted!</h3>
          <div class="result-info">
            <div>FILENAME  → <span>${data.original_filename}</span></div>
            <div>FILE SIZE → <span>${formatBytes(data.file_size)}</span></div>
            <div>INTEGRITY → <span style="color:var(--accent2)">✔ Verified — Not Tampered</span></div>
          </div>
          <a class="download-btn" href="${data.download_url}" download>
            <i class="fas fa-download"></i> Download Extracted File
          </a>
        </div>`;
    } else {
      result.innerHTML = `
        <div class="result-error">
          <h3><i class="fas fa-triangle-exclamation"></i> Error</h3>
          <p style="font-family:'Share Tech Mono',monospace;font-size:0.85rem">${data.error}</p>
        </div>`;
    }
  } catch (err) {
    result.innerHTML = `
      <div class="result-error">
        <h3><i class="fas fa-triangle-exclamation"></i> Connection Error</h3>
        <p style="font-family:'Share Tech Mono',monospace;font-size:0.85rem">Could not reach the server. Is Flask running?</p>
      </div>`;
  }
});