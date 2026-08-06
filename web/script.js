// ============================================================
// Neural Network Background Canvas
// ============================================================
const canvas = document.getElementById('networkCanvas');
const ctx = canvas.getContext('2d');
const licenseCanvas = document.getElementById('licenseCanvas');
const lctx = licenseCanvas ? licenseCanvas.getContext('2d') : null;

let width, height;
let particles = [];
const NUM_PARTICLES = 70;
const CONNECTION_DIST = 140;

function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    if(licenseCanvas) {
        licenseCanvas.width = width;
        licenseCanvas.height = height;
    }
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

class Particle {
    constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.35;
        this.vy = (Math.random() - 0.5) * 0.35;
        this.radius = Math.random() * 1.8 + 0.8;
        this.alpha = Math.random() * 0.5 + 0.2;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;
    }

    draw(context) {
        context.beginPath();
        context.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        context.fillStyle = `rgba(108, 107, 255, ${this.alpha})`;
        context.fill();
    }
}

for (let i = 0; i < NUM_PARTICLES; i++) {
    particles.push(new Particle());
}

function animateCanvas() {
    ctx.clearRect(0, 0, width, height);
    if(lctx) lctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw(ctx);
        if(lctx) particles[i].draw(lctx);

        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < CONNECTION_DIST) {
                const opacity = (1 - dist / CONNECTION_DIST) * 0.15;

                ctx.beginPath();
                ctx.strokeStyle = `rgba(108, 107, 255, ${opacity})`;
                ctx.lineWidth = 0.6;
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();

                if(lctx) {
                    lctx.beginPath();
                    lctx.strokeStyle = `rgba(108, 107, 255, ${opacity})`;
                    lctx.lineWidth = 0.6;
                    lctx.moveTo(particles[i].x, particles[i].y);
                    lctx.lineTo(particles[j].x, particles[j].y);
                    lctx.stroke();
                }
            }
        }
    }
    requestAnimationFrame(animateCanvas);
}
animateCanvas();

// ============================================================
// Ripple: onda desde el punto de clic en botones y tarjetas
// ============================================================
document.addEventListener('click', (e) => {
    const el = e.target.closest('.btn-primary, .fix-card, .action-card, .clean-circle-inner');
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const ripple = document.createElement('span');
    ripple.className = 'ripple-fx';
    ripple.style.width = ripple.style.height = `${size}px`;
    ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
    ripple.style.top = `${e.clientY - rect.top - size / 2}px`;
    el.appendChild(ripple);
    setTimeout(() => ripple.remove(), 650);
}, { passive: true });

// ============================================================
// Cursor Spotlight (delegado sobre document, sin listeners por tarjeta)
// ============================================================
const SPOTLIGHT_SELECTOR = '.glass, .hw-module, .action-card, .opt-tile, .game-card, .dup-group, .fix-card';
let spotlightTarget = null;
document.addEventListener('mousemove', (e) => {
    const el = e.target.closest ? e.target.closest(SPOTLIGHT_SELECTOR) : null;
    if (el !== spotlightTarget) {
        spotlightTarget = el;
    }
    if (el) {
        const rect = el.getBoundingClientRect();
        const mx = ((e.clientX - rect.left) / rect.width) * 100;
        const my = ((e.clientY - rect.top) / rect.height) * 100;
        el.style.setProperty('--mx', `${mx}%`);
        el.style.setProperty('--my', `${my}%`);
    }
}, { passive: true });

// ============================================================
// Animated number counter (cuenta hacia arriba/abajo en vez de saltar)
// ============================================================
function animateNumber(el, from, to, duration = 900, formatter = (v) => Math.round(v)) {
    if (!el) return;
    const start = performance.now();
    const diff = to - from;
    function tick(now) {
        const t = Math.min(1, (now - start) / duration);
        const eased = 1 - Math.pow(1 - t, 3); // ease-out cubic
        const value = from + diff * eased;
        el.textContent = formatter(value);
        if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
}


const navLinks = document.querySelectorAll('.nav-links li');
const pages = document.querySelectorAll('.page');
const pageTitle = document.getElementById('page-title');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        link.classList.add('tap-label');
        setTimeout(() => link.classList.remove('tap-label'), 900);
        switchPage(link.getAttribute('data-target'));
    });
});

function switchPage(targetId) {
    navLinks.forEach(l => l.classList.remove('active'));
    const activeLink = document.querySelector(`.nav-links li[data-target="${targetId}"]`);
    if (activeLink) activeLink.classList.add('active');

    pages.forEach(p => {
        p.classList.remove('active');
        p.style.display = 'none';
    });

    const target = document.getElementById(targetId);
    if (!target) return;

    target.classList.add('active');
    target.style.display = 'block';

    gsap.fromTo(target, { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.35, ease: 'power2.out' });

    const cards = target.querySelectorAll('.tool-card, .hw-module, .opt-tile, .game-card, .action-card, .clean-circle, .restore-point-item, .fix-card, .dup-group, .disk-bar-row, .bench-metric, .health-chip');
    if (cards.length) {
        gsap.fromTo(cards,
            { opacity: 0, y: 14, scale: 0.96 },
            { opacity: 1, y: 0, scale: 1, duration: 0.4, stagger: 0.045, ease: 'back.out(1.6)' }
        );
    }

    const titles = {
        dashboard: 'Información del Sistema',
        tweaks_fps: 'Optimización de FPS & Latencia',
        tweaks_perf: 'Rendimiento Máximo del Sistema',
        tweaks_priv: 'Seguridad y Privacidad Avanzada',
        tweaks_srv: 'Gestión de Servicios Locales',
        tweaks_ext: 'Ajustes de Modo Extremo',
        games: 'Perfiles de Juego Inteligentes',
        fixes: 'Solucionadores Automáticos',
        cleaner: 'Herramientas de Limpieza',
        restore: 'Puntos de Restauración',
        startup: 'Gestor de Arranque',
        diskspace: 'Disco y Archivos',
        repair: 'Diagnóstico Profundo'
    };
    pageTitle.innerText = titles[targetId] || 'Dashboard';

    // Carga perezosa: solo la primera vez que se visita cada página pesada
    if (targetId === 'startup' && !window._startupLoaded) {
        window._startupLoaded = true;
        loadStartupApps();
    }
    if (targetId === 'repair' && !window._tasksLoaded) {
        window._tasksLoaded = true;
        loadScheduledTasksAudit();
    }
}

// ============================================================
// Toast Notifications
// ============================================================
function showToast(title, message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icons = { success: 'fa-circle-check', warning: 'fa-triangle-exclamation', error: 'fa-circle-xmark' };
    const icon = icons[type] || 'fa-triangle-exclamation';

    toast.innerHTML = `
        <i class="fa-solid ${icon}"></i>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-msg">${message}</div>
        </div>
    `;

    container.appendChild(toast);

    gsap.to(toast, { x: 0, duration: 0.5, ease: 'back.out(1.2)' });

    setTimeout(() => {
        gsap.to(toast, { opacity: 0, y: 15, duration: 0.3, onComplete: () => toast.remove() });
    }, 4000);
}

// ============================================================
// Center Modal Notifications
// ============================================================
const modalOverlay = document.getElementById('modal-overlay');
const modalTasksContainer = document.getElementById('modal-tasks-container');
const modalProgressFill = document.getElementById('modal-progress-fill');
const modalCloseBtn = document.getElementById('modal-close-btn');

function openModal() {
    modalTasksContainer.innerHTML = '';
    modalProgressFill.style.width = '0%';
    modalCloseBtn.style.display = 'none';
    modalOverlay.style.display = 'flex';
    gsap.fromTo(modalOverlay, { opacity: 0 }, { opacity: 1, duration: 0.3 });
    gsap.fromTo('.modal-card', { y: 30, scale: 0.95 }, { y: 0, scale: 1, duration: 0.4, ease: 'back.out(1.5)' });
}

function closeModal() {
    gsap.to(modalOverlay, { opacity: 0, duration: 0.3, onComplete: () => {
        modalOverlay.style.display = 'none';
    }});
}

function addModalTask(id, text) {
    const taskDiv = document.createElement('div');
    taskDiv.className = 'modal-task running';
    taskDiv.id = `modal-task-${id}`;
    taskDiv.innerHTML = `
        <div class="loader-ring sm"></div>
        <span>${text}</span>
    `;
    modalTasksContainer.appendChild(taskDiv);
    modalTasksContainer.scrollTop = modalTasksContainer.scrollHeight;
}

function updateModalTask(id, statusOrSuccess, message) {
    const taskDiv = document.getElementById(`modal-task-${id}`);
    if (!taskDiv) return;

    // Acepta tanto un booleano (compatibilidad) como el string de estado real ('success'/'warning'/'error')
    let status = typeof statusOrSuccess === 'string' ? statusOrSuccess : (statusOrSuccess ? 'success' : 'error');
    if (status !== 'success' && status !== 'warning' && status !== 'error') status = 'error';

    taskDiv.className = `modal-task ${status}`;
    const span = taskDiv.querySelector('span');

    const icons = { success: 'fa-circle-check', warning: 'fa-triangle-exclamation', error: 'fa-circle-xmark' };
    // El spinner mientras corría era un <div class="loader-ring">, no un <i>: se sustituye entero por el icono final
    const oldIndicator = taskDiv.querySelector('.loader-ring, i');
    const finalIcon = document.createElement('i');
    finalIcon.className = `fa-solid ${icons[status]}`;
    if (oldIndicator) {
        oldIndicator.replaceWith(finalIcon);
    } else {
        taskDiv.prepend(finalIcon);
    }
    if (message) span.innerText = message;
}

function updateModalProgress(percent) {
    modalProgressFill.style.width = `${percent}%`;
    if (percent >= 100) {
        modalCloseBtn.style.display = 'block';
    }
}

// ============================================================
// Hardware & Drivers
// ============================================================
async function loadHardwareInfo() {
    if (!window.pywebview || !window.pywebview.api) return;
    try {
        const data = await window.pywebview.api.get_hardware_info();
        if (data.status === 'success') {
            // CPU / GPU Status Panel
            const cpuNameEl = document.getElementById('hw-cpu-name');
            if (cpuNameEl) cpuNameEl.innerText = data.cpu.split(' @')[0] || data.cpu;
            const coresEl = document.getElementById('hw-cpu-cores');
            if (coresEl) coresEl.innerText = data.cores || '--';

            const gpuNameEl = document.getElementById('hw-gpu-name');
            if (gpuNameEl) gpuNameEl.innerText = data.gpu || '--';

            // Disk: "XX GB libres de YY GB"
            const diskValEl = document.getElementById('hw-disk-val');
            if (diskValEl && data.disk_info) {
                const m = data.disk_info.match(/(\d+)\s*GB\s*libres\s*de\s*(\d+)\s*GB/i);
                if (m) {
                    const free = parseInt(m[1]);
                    const total = parseInt(m[2]);
                    const used = total - free;
                    diskValEl.innerText = `${used} / ${total} GB`;
                    const vramBar = document.getElementById('vram-v-bar');
                    if (vramBar) vramBar.style.height = Math.min((used / total) * 100, 100) + '%';
                    const vramNumEl = document.getElementById('vram-v-num');
                    if (vramNumEl) vramNumEl.innerText = Math.round((used / total) * 100) + '%';
                } else {
                    diskValEl.innerText = data.disk_info;
                }
            }

            // GPU Driver info
            try {
                const driverData = await window.pywebview.api.check_gpu_driver();
                const gpuDriverEl = document.getElementById('hw-gpu-driver');
                if (driverData.status === 'success' && gpuDriverEl) {
                    gpuDriverEl.innerText = driverData.message;
                    gpuDriverEl.style.color = driverData.has_update ? 'var(--warning)' : 'var(--success)';
                    if (driverData.has_update && driverData.url) {
                        gpuDriverEl.onclick = () => window.pywebview.api.open_url && window.pywebview.api.open_url(driverData.url);
                    }
                }
                
                // Update GPU Logo based on brand
                const gpuBox = document.getElementById('gpu-logo-box');
                if (gpuBox) {
                    const gpuLower = (data.gpu || '').toLowerCase();
                    if (gpuLower.includes('nvidia') || gpuLower.includes('geforce')) {
                        gpuBox.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor" style="width:18px;height:18px;color:#76b900"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm7.155 17.65c-.244.372-.735.474-1.107.23-.37-.245-.472-.734-.23-1.106 1.745-2.65 1.488-5.74-.78-8.125-2.227-2.34-5.65-3.033-8.527-1.747-.417.187-.9-.012-1.087-.43-.186-.418.012-.9.43-1.087 3.32-1.488 7.33-.67 9.947 2.08 2.628 2.756 2.923 6.31 1.354 10.185z"/></svg>`;
                        gpuBox.style.background = 'rgba(118, 185, 0, 0.15)';
                    } else if (gpuLower.includes('amd') || gpuLower.includes('radeon')) {
                        gpuBox.innerHTML = `<svg viewBox="0 0 24 24" fill="currentColor" style="width:18px;height:18px;color:#ED1C24"><path d="M1 9.5l9.5 9.5 9.5-9.5L10.5 0 1 9.5zm19 14.5h-10l5-5 5 5z"/></svg>`;
                        gpuBox.style.background = 'rgba(237, 28, 36, 0.15)';
                    }
                }
            } catch(e) {}
        }

        // RAM: use get_memory_status for real-time data
        try {
            const mem = await window.pywebview.api.get_memory_status();
            if (mem.status === 'success') {
                const ramValEl = document.getElementById('hw-ram-val');
                if (ramValEl) ramValEl.innerText = `${mem.total_gb} GB`;
                const ramBar = document.getElementById('ram-v-bar');
                if (ramBar) ramBar.style.height = mem.used_pct + '%';
                const ramNumEl = document.getElementById('ram-v-num');
                if (ramNumEl) ramNumEl.innerText = Math.round(mem.used_pct) + '%';
            }
        } catch(e) {}

    } catch (e) {
        console.error('Error loading hardware info:', e);
    }
}

// ============================================================
// Dynamic Tweaks
// ============================================================
async function loadTweaks() {
    if (!window.pywebview || !window.pywebview.api) return;

    try {
        const res = await window.pywebview.api.get_optimizations();
        if (res.status !== 'success') return;

        const tweaks = res.data;

        // Mapeo de categorías a contenedores e iconos
        const catMap = {
            'FPS & Ping': 'tweaks_fps',
            'Rendimiento': 'tweaks_perf',
            'Privacidad': 'tweaks_priv',
            'Servicios': 'tweaks_srv',
            'Modo Extremo': 'tweaks_ext',
            'NVIDIA': 'tweaks_nvidia',
            'MSI Mode': 'tweaks_msi'
        };
        const iconMap = {
            'FPS & Ping': 'fa-crosshairs',
            'Rendimiento': 'fa-rocket',
            'Privacidad': 'fa-user-shield',
            'Servicios': 'fa-server',
            'Modo Extremo': 'fa-skull',
            'NVIDIA': 'fa-microchip',
            'MSI Mode': 'fa-bolt'
        };

        // Aviso honesto una sola vez por categoría: la sonda es aproximada, no un benchmark de juego real
        Object.values(catMap).forEach(containerId => {
            const section = document.getElementById(containerId);
            if (section && !section.dataset.noteAdded) {
                section.dataset.noteAdded = '1';

                const headerWrapper = document.createElement('div');
                headerWrapper.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:10px;';

                const note = document.createElement('div');
                note.className = 'cleaner-note';
                note.style.margin = '0';
                note.innerHTML = `<i class="fa-solid fa-circle-info"></i> Al activar un tweak verás una sonda rápida de CPU antes/después (aproximada). El botón <i class="fa-solid fa-rotate-left"></i> restaura el valor original.`;
                
                const btn = document.createElement('button');
                btn.className = 'btn-primary';
                btn.style.cssText = 'font-size:0.85rem;padding:8px 16px;background:var(--success);';
                btn.innerHTML = `<i class="fa-solid fa-check-double"></i> Marcar todas`;
                btn.onclick = () => {
                    const checkboxes = section.querySelectorAll('.tweak-switch:not(:disabled)');
                    checkboxes.forEach(cb => cb.checked = true);
                    updateBulkButton();
                };

                headerWrapper.appendChild(note);
                headerWrapper.appendChild(btn);
                section.insertBefore(headerWrapper, section.firstChild);
            }
        });

        tweaks.forEach(item => {
            const containerId = catMap[item.category];
            if (!containerId) return;

            const section = document.getElementById(containerId);
            if (!section) return;
            const contentContainer = section.querySelector('.tweaks-container');

            const box = document.createElement('div');
            box.className = 'opt-tile glass';
            if (item.category === 'Modo Extremo') {
                box.style.borderColor = 'rgba(255, 92, 114, 0.4)';
                box.style.boxShadow = '0 10px 30px rgba(255, 92, 114, 0.15), inset 0 1px 0 rgba(255,255,255,0.1)';
            }

            const icon = iconMap[item.category] || 'fa-microchip';
            const riskMap = {
                safe: { label: 'Seguro', color: 'var(--success)' },
                moderate: { label: 'Moderado', color: 'var(--warning)' },
                danger: { label: 'Peligroso', color: 'var(--danger)' }
            };
            const risk = riskMap[item.risk] || riskMap.moderate;

            box.innerHTML = `
                <i class="fa-solid ${icon} opt-tile-bg-icon"></i>
                <div class="opt-tile-content">
                    <div class="opt-tile-title-row">
                        <div class="opt-tile-title" style="${item.category === 'Modo Extremo' ? 'color: var(--danger);' : ''}">${item.name}</div>
                        <span class="risk-badge" style="color:${risk.color}; border-color:${risk.color};">${risk.label}</span>
                    </div>
                    <div class="opt-tile-desc">${item.desc}</div>
                </div>
                <div class="opt-tile-footer">
                    <button class="undo-btn" title="Restaurar valor original" onclick="undoTweak('${item.id}', event)"><i class="fa-solid fa-rotate-left"></i></button>
                    <label class="switch">
                        <input type="checkbox" data-id="${item.id}" data-name="${item.name}" data-risk="${item.risk}" class="tweak-switch" ${localStorage.getItem('tweak_' + item.id) === 'on' ? 'checked disabled' : ''}>
                        <span class="slider"></span>
                    </label>
                </div>
            `;
            contentContainer.appendChild(box);
        });

        const bulkApplyBtn = document.getElementById('bulk-apply-btn');
        const bulkCountSpan = document.getElementById('bulk-count');

        function updateBulkButton() {
            const checkedBoxes = document.querySelectorAll('.tweak-switch:checked:not(:disabled)');
            if (checkedBoxes.length > 0) {
                bulkCountSpan.innerText = checkedBoxes.length;
                if (bulkApplyBtn.style.display === 'none') {
                    bulkApplyBtn.style.display = 'block';
                    gsap.fromTo(bulkApplyBtn, { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' });
                }
            } else {
                gsap.to(bulkApplyBtn, { y: 50, opacity: 0, duration: 0.3, onComplete: () => {
                    bulkApplyBtn.style.display = 'none';
                }});
            }
        }

        document.querySelectorAll('.tweak-switch').forEach(sw => {
            sw.addEventListener('change', () => {
                if (sw.checked && sw.dataset.risk === 'danger') {
                    const ok = window.confirm(
                        `"${sw.dataset.name}" está marcado como PELIGROSO: reduce protecciones de seguridad de Windows y aporta poco o ningún FPS real medible.\n\n¿Seguro que quieres activarlo?`
                    );
                    if (!ok) {
                        sw.checked = false;
                    }
                }
                updateBulkButton();
            });
        });

    } catch (e) {
        console.error('Error loading tweaks:', e);
    }
}

async function applySelectedTweaks() {
    if (!window.pywebview || !window.pywebview.api) return;

    const checkboxes = Array.from(document.querySelectorAll('.tweak-switch:checked:not(:disabled)'));
    if (checkboxes.length === 0) return;

    openModal();
    let completed = 0;

    // We disable checkboxes and uncheck them so they don't get selected again
    checkboxes.forEach(cb => {
        cb.disabled = true;
    });

    for (const sw of checkboxes) {
        const optId = sw.dataset.id;
        const optName = sw.dataset.name;

        const taskId = 'tweak_' + optId;
        addModalTask(taskId, `Activando ${optName}...`);

        try {
            const res = await window.pywebview.api.toggle_optimization_with_benchmark(optId, true);
            let msg = res.message;
            if (res.delta_pct !== undefined) {
                const arrow = res.delta_pct > 0 ? '▲' : (res.delta_pct < 0 ? '▼' : '■');
                msg += ` — sonda CPU: ${arrow} ${res.delta_pct}%`;
            }
            updateModalTask(taskId, res.status, msg);
            if (res.status === 'success') localStorage.setItem('tweak_' + optId, 'on');
        } catch {
            updateModalTask(taskId, 'error', 'Error de comunicación');
        }

        if (localStorage.getItem('tweak_' + optId) === 'on') {
            sw.checked = true;
            sw.disabled = true;
        } else {
            sw.checked = false; // Reset visually
            sw.disabled = false;
        }

        completed++;
        updateModalProgress((completed / checkboxes.length) * 100);
    }

    // Hide bulk button
    const bulkApplyBtn = document.getElementById('bulk-apply-btn');
    gsap.to(bulkApplyBtn, { y: 50, opacity: 0, duration: 0.3, onComplete: () => {
        bulkApplyBtn.style.display = 'none';
    }});
}

// ============================================================
// Cleaners & Restore
// ============================================================
const runningTasks = new Set();
async function runTask(taskName) {
    if (!window.pywebview || !window.pywebview.api) return;
    if (runningTasks.has(taskName)) return; // evita procesos duplicados por doble clic
    runningTasks.add(taskName);

    showToast('Naury Engine', `Ejecutando ${taskName}...`, 'success');

    try {
        const result = await window.pywebview.api[taskName]();
        if (result.status === 'success') {
            showToast('Completado', result.message, 'success');
        } else if (result.status === 'warning') {
            showToast('Aviso', result.message, 'warning');
        } else {
            showToast('Error', result.message || 'Fallo en la tarea.', 'error');
        }
    } catch(e) {
        showToast('Error Critico', 'No se pudo ejecutar el proceso.', 'error');
    } finally {
        runningTasks.delete(taskName);
    }
}

function runDestructiveTask(taskName, confirmMsg) {
    if (window.confirm(confirmMsg)) {
        runTask(taskName);
    }
}

async function runBenchmark() {
    if (!window.pywebview || !window.pywebview.api) return;

    const btn = document.getElementById('benchmark-btn');
    const resultEl = document.getElementById('benchmark-result');
    const detailsEl = document.getElementById('benchmark-details');
    if (!btn || !resultEl) return;

    btn.disabled = true;
    btn.innerHTML = '<div class="loader-ring sm"></div> Calculando';
    resultEl.innerText = 'Midiendo CPU (1 núcleo + multi-núcleo) y velocidad de disco...';

    try {
        const res = await window.pywebview.api.run_benchmark();
        if (res.status === 'success') {
            const scoreSpan = document.createElement('span');
            scoreSpan.className = 'count-up';
            scoreSpan.style.color = 'var(--primary-2)';
            scoreSpan.style.fontWeight = '700';
            resultEl.innerHTML = '';
            resultEl.appendChild(scoreSpan);
            resultEl.appendChild(document.createTextNode(` pts — ${res.tier}`));
            animateNumber(scoreSpan, 0, res.score, 1100);
            showToast('Benchmark Completo', res.message, 'success');

            if (detailsEl) {
                detailsEl.style.display = 'grid';
                detailsEl.innerHTML = `
                    <div class="bench-metric"><span>1 Núcleo</span><strong><span class="count-up" id="m-single">0</span> ops/s</strong></div>
                    <div class="bench-metric"><span>${res.cores_used} Núcleos</span><strong><span class="count-up" id="m-multi">0</span> ops/s</strong></div>
                    <div class="bench-metric"><span>Escritura Disco</span><strong><span class="count-up" id="m-write">0</span> MB/s</strong></div>
                    <div class="bench-metric"><span>Lectura Disco</span><strong><span class="count-up" id="m-read">0</span> MB/s</strong></div>
                `;
                animateNumber(document.getElementById('m-single'), 0, res.single_core_ops_sec, 1200, v => Math.round(v).toLocaleString());
                animateNumber(document.getElementById('m-multi'), 0, res.multi_core_ops_sec, 1200, v => Math.round(v).toLocaleString());
                animateNumber(document.getElementById('m-write'), 0, res.disk_write_mbs, 1200, v => v.toFixed(1));
                animateNumber(document.getElementById('m-read'), 0, res.disk_read_mbs, 1200, v => v.toFixed(1));
            }
            loadBenchmarkHistory();
        } else {
            resultEl.innerText = res.message || 'No se pudo completar el benchmark.';
            showToast('Error', res.message || 'Fallo en el benchmark.', 'error');
        }
    } catch (e) {
        resultEl.innerText = 'Error ejecutando el benchmark.';
        showToast('Error Crítico', 'No se pudo ejecutar el proceso.', 'error');
    }

    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Repetir';
}

async function undoTweak(optId, evt) {
    if (evt) evt.stopPropagation();
    if (!window.pywebview || !window.pywebview.api) return;
    try {
        const res = await window.pywebview.api.restore_tweak_snapshot(optId);
        showToast(res.status === 'success' ? 'Restaurado' : 'Aviso', res.message, res.status === 'success' ? 'success' : 'error');
        if (res.status === 'success') {
            localStorage.removeItem('tweak_' + optId);
            // Re-enable the checkbox visually
            const sw = document.querySelector(`.tweak-switch[data-id="${optId}"]`);
            if (sw) { sw.checked = false; sw.disabled = false; }
        }
    } catch (e) {
        showToast('Error', 'No se pudo restaurar el snapshot.', 'error');
    }
}

// ============================================================
// Benchmark History Chart
// ============================================================
let benchHistoryChart = null;
async function loadBenchmarkHistory() {
    if (!window.pywebview || !window.pywebview.api) return;
    const canvas = document.getElementById('benchHistoryChart');
    if (!canvas) return;
    try {
        const res = await window.pywebview.api.get_benchmark_history();
        const data = (res.status === 'success' && res.data) ? res.data : [];
        const labels = data.map((d, i) => `#${i + 1}`);
        const scores = data.map(d => d.score);

        if (benchHistoryChart) {
            benchHistoryChart.data.labels = labels;
            benchHistoryChart.data.datasets[0].data = scores;
            benchHistoryChart.update();
            return;
        }
        const ctx = canvas.getContext('2d');
        benchHistoryChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Score',
                    data: scores,
                    backgroundColor: 'rgba(108, 107, 255, 0.5)',
                    borderColor: '#6C6BFF',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: 'rgba(255,255,255,0.4)', font: { size: 10 } } },
                    x: { grid: { display: false }, ticks: { color: 'rgba(255,255,255,0.3)', font: { size: 9 } } }
                }
            }
        });
    } catch (e) { console.error(e); }
}

// ============================================================
// System Health Score (dashboard)
// ============================================================
async function loadHealthScore() {
    if (!window.pywebview || !window.pywebview.api) return;
    try {
        const res = await window.pywebview.api.get_system_health_score();
        if (res.status !== 'success') return;

        const fillEl = document.getElementById('health-gauge-fill');
        const labelEl = document.getElementById('health-status-label');
        const breakdownEl = document.getElementById('health-breakdown');

        if (labelEl) {
            labelEl.innerText = (res.status_label || '').toUpperCase();
            labelEl.className = ''; 
            if (res.score >= 70) labelEl.classList.add('glow-text-green');
            else if (res.score >= 45) labelEl.style.color = 'var(--warning)';
            else labelEl.style.color = 'var(--danger)';
        }
        
        if (fillEl) {
            const offset = 100 - res.score;
            fillEl.style.stroke = res.score >= 70 ? 'var(--success)' : (res.score >= 45 ? 'var(--warning)' : 'var(--danger)');
            gsap.to(fillEl, { strokeDashoffset: offset, duration: 1.5, ease: 'power2.out' });
        }

        if (breakdownEl) {
            breakdownEl.innerHTML = (res.breakdown || []).map(b => {
                const color = b.level === 'danger' ? 'var(--danger)' : (b.level === 'warning' ? 'var(--warning)' : 'var(--success)');
                return `<span class="health-chip" style="border-color:${color}; color:${color};">${b.label}</span>`;
            }).join('');
        }
    } catch (e) { console.error('Error loading health score:', e); }
}

// ============================================================
// Startup Manager
// ============================================================
async function loadStartupApps() {
    if (!window.pywebview || !window.pywebview.api) return;
    const tbody = document.getElementById('startup-tbody');
    if (!tbody) return;
    try {
        const res = await window.pywebview.api.get_startup_apps();
        const data = (res.status === 'success') ? res.data : [];
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding:40px; color:var(--text-secondary);">No se encontraron apps en el arranque.</td></tr>`;
            return;
        }
        tbody.innerHTML = '';
        data.forEach(app => {
            const tr = document.createElement('tr');
            const impactColor = app.impact === 'Alto' ? 'var(--danger)' : 'var(--warning)';
            tr.innerHTML = `
                <td><div class="debloat-app-name"><div class="debloat-app-icon"><i class="fa-solid fa-play"></i></div>
                    <div class="debloat-app-info"><strong>${app.name}</strong></div></div></td>
                <td>${app.location}</td>
                <td><span class="risk-badge" style="color:${impactColor}; border-color:${impactColor};">${app.impact}</span></td>
                <td>
                    <label class="switch">
                        <input type="checkbox" ${app.enabled ? 'checked' : ''}
                            onchange="toggleStartupApp(this, '${app.name.replace(/'/g, "\\'")}', '${app.location}', '${app.key_path.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}')">
                        <span class="slider"></span>
                    </label>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding:40px; color:var(--danger);">Error leyendo el arranque.</td></tr>`;
    }
}

async function toggleStartupApp(checkbox, name, location, keyPath) {
    checkbox.disabled = true;
    try {
        const res = await window.pywebview.api.toggle_startup_app(name, location, keyPath, checkbox.checked);
        showToast(res.status === 'success' ? 'Arranque actualizado' : 'Error', res.message, res.status);
    } catch (e) {
        showToast('Error', 'No se pudo actualizar la entrada.', 'error');
        checkbox.checked = !checkbox.checked;
    }
    checkbox.disabled = false;
}

// ============================================================
// Disco: Analizador de espacio + Duplicados
// ============================================================
let diskAnalysisRunning = false;
async function runDiskAnalysis() {
    if (!window.pywebview || !window.pywebview.api || diskAnalysisRunning) return;
    diskAnalysisRunning = true;
    const list = document.getElementById('disk-analysis-list');
    if (!list) { diskAnalysisRunning = false; return; }
    list.innerHTML = `<div class="grid-placeholder"><div class="loader-ring lg"></div><p>Escaneando disco C:...</p></div>`;
    try {
        const res = await window.pywebview.api.analyze_disk_space();
        if (res.status !== 'success' || !res.data.length) {
            list.innerHTML = `<div class="grid-placeholder"><i class="fa-solid fa-triangle-exclamation"></i><p>${res.message || 'No se pudo analizar el disco.'}</p></div>`;
            return;
        }
        const maxSize = Math.max(...res.data.map(d => d.size));
        list.innerHTML = res.data.map(d => {
            const pct = maxSize > 0 ? Math.max(2, (d.size / maxSize) * 100) : 0;
            const icon = d.is_dir ? 'fa-folder' : 'fa-file';
            return `
                <div class="disk-bar-row">
                    <i class="fa-solid ${icon} disk-bar-icon"></i>
                    <span class="disk-bar-name" title="${d.path}">${d.name}</span>
                    <div class="disk-bar-track"><div class="disk-bar-fill" style="width:0%;" data-target="${pct}"></div></div>
                    <span class="disk-bar-size">${d.size_mb >= 1024 ? (d.size_mb/1024).toFixed(2)+' GB' : d.size_mb+' MB'}</span>
                </div>`;
        }).join('');
        requestAnimationFrame(() => {
            list.querySelectorAll('.disk-bar-fill').forEach(el => { el.style.width = el.dataset.target + '%'; });
        });
    } catch (e) {
        list.innerHTML = `<div class="grid-placeholder"><i class="fa-solid fa-triangle-exclamation"></i><p>Error analizando el disco.</p></div>`;
    } finally {
        diskAnalysisRunning = false;
    }
}

let dupFinderRunning = false;
async function runDuplicateFinder() {
    if (!window.pywebview || !window.pywebview.api || dupFinderRunning) return;
    dupFinderRunning = true;
    const list = document.getElementById('dup-results-list');
    const summary = document.getElementById('dup-summary');
    if (!list) { dupFinderRunning = false; return; }
    list.innerHTML = `<div class="grid-placeholder"><div class="loader-ring lg"></div><p>Buscando duplicados en Descargas...</p></div>`;
    try {
        const res = await window.pywebview.api.find_duplicate_files();
        if (res.status !== 'success' || !res.data.length) {
            list.innerHTML = `<div class="grid-placeholder"><i class="fa-solid fa-circle-check"></i><p>No se encontraron duplicados.</p></div>`;
            if (summary) summary.innerText = 'No se encontraron duplicados en Descargas.';
            return;
        }
        if (summary) summary.innerText = `Posible ahorro: ${res.potential_savings_mb} MB en ${res.data.length} grupos.`;
        list.innerHTML = res.data.map((group, gi) => {
            const files = group.files.map((f, fi) => `
                <div class="dup-file-row">
                    <span title="${f}">${f.split(/[\\\/]/).pop()}</span>
                    ${fi === 0
                        ? '<span class="dup-keep-tag">Se conserva</span>'
                        : `<button class="undo-btn" title="Eliminar esta copia" onclick="deleteSingleDuplicate('${f.replace(/\\/g, '\\\\').replace(/'/g,"\\'")}', this)"><i class="fa-solid fa-trash"></i></button>`}
                </div>`).join('');
            return `<div class="dup-group glass"><div class="dup-group-header"><strong>${group.size_mb} MB</strong><span>${group.files.length} copias</span></div>${files}</div>`;
        }).join('');
    } catch (e) {
        list.innerHTML = `<div class="grid-placeholder"><i class="fa-solid fa-triangle-exclamation"></i><p>Error buscando duplicados.</p></div>`;
    } finally {
        dupFinderRunning = false;
    }
}

async function deleteSingleDuplicate(path, btn) {
    if (!window.pywebview || !window.pywebview.api) return;
    const fileName = path.split(/[\\\/]/).pop();
    if (!window.confirm(`Eliminar "${fileName}" permanentemente?\n\nEsta acción no se puede deshacer.`)) return;
    btn.disabled = true;
    try {
        const res = await window.pywebview.api.delete_duplicate_files([path]);
        showToast(res.status === 'success' ? 'Duplicado eliminado' : 'Aviso', res.message, res.status);
        if (res.status === 'success') {
            btn.closest('.dup-file-row').remove();
        } else {
            btn.disabled = false;
        }
    } catch (e) {
        showToast('Error', 'No se pudo eliminar el archivo.', 'error');
        btn.disabled = false;
    }
}

// ============================================================
// Reparación Profunda (DISM + SFC)
// ============================================================
let repairPollInterval = null;
async function startDeepRepair() {
    if (!window.pywebview || !window.pywebview.api) return;
    const btn = document.getElementById('repair-btn');
    const wrap = document.getElementById('repair-progress-wrap');
    const fill = document.getElementById('repair-progress-fill');
    const stepText = document.getElementById('repair-step-text');
    if (!btn) return;

    btn.disabled = true;
    btn.innerHTML = '<div class="loader-ring sm"></div> Reparando...';
    if (wrap) wrap.style.display = 'block';

    try {
        await window.pywebview.api.start_deep_repair();
    } catch (e) {
        showToast('Error', 'No se pudo iniciar la reparación.', 'error');
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-play"></i> Iniciar Reparación';
        return;
    }

    if (repairPollInterval) clearInterval(repairPollInterval);
    repairPollInterval = setInterval(async () => {
        try {
            const st = await window.pywebview.api.get_repair_status();
            if (fill) fill.style.width = `${st.progress || 0}%`;
            if (stepText) stepText.innerText = st.step || '';
            if (st.done) {
                clearInterval(repairPollInterval);
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> Repetir';
                showToast(st.success ? 'Reparación completada' : 'Reparación finalizada con avisos',
                    (st.log || []).join(' | ') || st.step, st.success ? 'success' : 'error');
            }
        } catch (e) { /* noop */ }
    }, 2000);
}

let batteryReportRunning = false;
async function loadBatteryReport() {
    if (!window.pywebview || !window.pywebview.api || batteryReportRunning) return;
    batteryReportRunning = true;
    const box = document.getElementById('battery-report-box');
    if (!box) { batteryReportRunning = false; return; }
    box.innerHTML = `<div class="restore-points-loading"><div class="loader-ring lg"></div> Generando informe con powercfg...</div>`;
    try {
        const res = await window.pywebview.api.get_battery_report();
        if (res.status !== 'success' || res.health_pct === null || res.health_pct === undefined) {
            box.innerHTML = `<div class="restore-points-empty"><i class="fa-solid fa-circle-info"></i><span>${res.message || 'No se pudo leer la salud de la batería (¿es un equipo de escritorio?).'}</span></div>`;
            return;
        }
        const color = res.health_pct >= 80 ? 'var(--success)' : (res.health_pct >= 60 ? 'var(--warning)' : 'var(--danger)');
        box.innerHTML = `
            <div class="restore-point-item">
                <div class="restore-point-icon" style="color:${color};"><i class="fa-solid fa-car-battery"></i></div>
                <div class="restore-point-info">
                    <strong style="color:${color};">${res.health_pct}% de salud</strong>
                    <span>Diseño: ${(res.design_capacity_mwh/1000).toFixed(1)} Wh · Actual: ${(res.full_charge_capacity_mwh/1000).toFixed(1)} Wh</span>
                </div>
            </div>`;
    } catch (e) {
        box.innerHTML = `<div class="restore-points-empty"><i class="fa-solid fa-triangle-exclamation"></i><span>Error generando el informe.</span></div>`;
    } finally {
        batteryReportRunning = false;
    }
}

// ============================================================
// Tareas Programadas de Terceros
// ============================================================
async function loadScheduledTasksAudit() {
    if (!window.pywebview || !window.pywebview.api) return;
    const tbody = document.getElementById('tasks-tbody');
    if (!tbody) return;
    try {
        const res = await window.pywebview.api.get_scheduled_tasks_audit();
        const data = (res.status === 'success') ? res.data : [];
        if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="3" style="text-align:center; padding:40px; color:var(--text-secondary);">No se encontraron tareas de terceros activas.</td></tr>`;
            return;
        }
        tbody.innerHTML = '';
        data.forEach(t => {
            const tr = document.createElement('tr');
            const enabled = t.state !== 'Disabled';
            tr.innerHTML = `
                <td><strong>${t.name}</strong></td>
                <td style="color:var(--text-secondary); font-size:0.78rem;">${t.path}</td>
                <td>
                    <label class="switch">
                        <input type="checkbox" ${enabled ? 'checked' : ''}
                            onchange="toggleScheduledTask(this, '${(t.name||'').replace(/'/g,"\\'")}', '${(t.path||'').replace(/'/g,"\\'")}')">
                        <span class="slider"></span>
                    </label>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="3" style="text-align:center; padding:40px; color:var(--danger);">Error consultando tareas.</td></tr>`;
    }
}

async function toggleScheduledTask(checkbox, name, path) {
    checkbox.disabled = true;
    try {
        const res = await window.pywebview.api.toggle_scheduled_task(name, path, checkbox.checked);
        showToast(res.status === 'success' ? 'Tarea actualizada' : 'Error', res.message, res.status);
    } catch (e) {
        showToast('Error', 'No se pudo modificar la tarea.', 'error');
checkbox.checked = !checkbox.checked;
    }
    checkbox.disabled = false;
}

// ============================================================
// Initialization — license first, then load real data
// ============================================================
window.addEventListener('pywebviewready', async () => {
    // Maximize app on startup silently
    try {
        if (window.pywebview && window.pywebview.api) {
            await window.pywebview.api.maximize_window();
        }
    } catch(e) { console.error("Maximize error", e); }

    const textEl = document.getElementById('loading-status');
    const bar = document.querySelector('.loading-progress-fill');
    if (textEl) textEl.innerText = "Verificando conexión con el núcleo...";
    if (bar) bar.style.width = "10%";

    // Step 1: Check license FIRST
    let licenseResult = null;
    try {
        licenseResult = await Promise.race([
            window.pywebview.api.check_license_status(),
            new Promise(r => setTimeout(() => r(null), 3000)) // 3s timeout for license
        ]);
    } catch (e) {
        console.error('License check error during loading:', e);
    }

    const loader = document.getElementById('loading-screen');

    // Step 2: Decide whether to load data or show prompt
    if (!licenseResult || licenseResult.status === 'need_auth') {
        if (bar) bar.style.width = "100%";
        if (loader) {
            gsap.to(loader, {
                opacity: 0, duration: 0.6, ease: 'power2.inOut',
                onComplete: () => {
                    loader.style.display = 'none';
                    showLicensePrompt();
                }
            });
        } else { showLicensePrompt(); }
    } else if (licenseResult.status === 'banned') {
        if (bar) bar.style.width = "100%";
        if (loader) {
            gsap.to(loader, {
                opacity: 0, duration: 0.6, ease: 'power2.inOut',
                onComplete: () => {
                    loader.style.display = 'none';
                    showLicensePrompt();
                    document.querySelector('.license-card').classList.add('banned');
                    const err = document.getElementById('license-error-msg');
                    if (err) err.innerText = "ACCESO BLOQUEADO: HWID VETADO";
                    const btn = document.getElementById('license-submit-btn');
                    if (btn) btn.style.display = 'none';
                }
            });
        }
    } else {
        // License valid! Load real data FIRST while loader is still visible
        if (licenseResult.owner) {
            const ownerEl = document.getElementById('license-owner-name');
            if (ownerEl) ownerEl.innerText = licenseResult.owner;
        }
        
        await loadAllData();
        
        // Data is ready, now hide the loader and reveal app
        if (loader) {
            gsap.to(loader, {
                opacity: 0, duration: 0.6, ease: 'power2.inOut',
                onComplete: () => {
                    loader.style.display = 'none';
                    revealApp();
                }
            });
        } else { revealApp(); }
    }
});

async function loadAllData() {
    const bar = document.querySelector('.loading-progress-fill');
    const status = document.getElementById('loading-status');
    if (bar) bar.style.width = "20%";

    const tasks = [
        { name: "Hardware", fn: loadHardwareInfo() },
        { name: "Tweaks", fn: loadTweaks() },
        { name: "Motores", fn: loadGames() },
        { name: "Debloater", fn: loadDebloatApps() },
        { name: "Restauración", fn: loadRestorePoints() },
        { name: "Salud", fn: loadHealthScore() },
        { name: "Historial", fn: loadBenchmarkHistory() }
    ];
    
    let completed = 0;
    const promises = tasks.map(async (t) => {
        try {
            // Give each task a strict 4-second timeout
            await Promise.race([t.fn, new Promise(r => setTimeout(r, 4000))]);
        } catch(e) { console.error('Error in ' + t.name, e); }
        
        completed++;
        if (bar) {
            // Progress from 20% to 100%
            const prog = 20 + ((completed / tasks.length) * 80);
            bar.style.width = prog + "%";
        }
        if (status) status.innerText = "Cargando módulos: " + t.name + "...";
    });

    await Promise.all(promises);
    if (bar) bar.style.width = "100%";
    if (status) status.innerText = "¡Todo listo!";
    // Give the UI a tiny moment to paint the 100% bar
    await new Promise(r => setTimeout(r, 200));
}

// ============================================================
// License Prompt (inside the app UI)
// ============================================================
function showLicensePrompt() {
    const overlay = document.getElementById('license-overlay');
    overlay.style.display = 'flex';
    gsap.from('.license-card', { opacity: 0, y: 30, duration: 0.5, ease: 'power3.out' });
    gsap.to(overlay, { opacity: 1, duration: 0.4 });

    const btn = document.getElementById('license-submit-btn');
    const input = document.getElementById('license-input');
    const errorMsg = document.getElementById('license-error-msg');
    const attemptsText = document.getElementById('license-attempts-text');
    let attemptsLeft = 3;

    setTimeout(() => input.focus(), 400);

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') btn.click();
    });

    function updateDots(attemptsLeft) {
        const dots = document.querySelectorAll('.attempt-dot');
        dots.forEach((dot, i) => {
            dot.className = 'attempt-dot';
            if (i < attemptsLeft) {
                dot.classList.add('active');
            } else {
                dot.classList.add('gone');
            }
        });
        attemptsText.innerText = attemptsLeft === 0
            ? 'Sin intentos restantes'
            : `${attemptsLeft} intento${attemptsLeft !== 1 ? 's' : ''} restante${attemptsLeft !== 1 ? 's' : ''}`;
    }

    btn.onclick = async () => {
        const key = input.value.trim();
        if (!key) {
            gsap.fromTo(input, { x: -6 }, { x: 0, duration: 0.4, ease: 'elastic.out(1,0.3)' });
            return;
        }

        btn.innerHTML = '<div class="loader-ring sm"></div> <span>Verificando...</span>';
        btn.disabled = true;
        errorMsg.style.display = 'none';

        try {
            const res = await window.pywebview.api.validate_key_ui(key);

            if (res.status === 'success') {
                if (res.owner) {
                    const ownerEl = document.getElementById('license-owner-name');
                    if (ownerEl) ownerEl.innerText = res.owner;
                }
                // Success — ring glows green and the app is revealed
                gsap.to('.license-logo-ring', {
                    borderColor: '#3ecf8e',
                    boxShadow: '0 0 0 6px rgba(62,207,142,0.18), 0 0 34px rgba(62,207,142,0.55)',
                    duration: 0.4
                });
                btn.innerHTML = '<i class="fa-solid fa-check"></i> <span>Acceso Autorizado</span>';
                btn.style.background = 'linear-gradient(135deg, #3ecf7a, #27a85e)';
                setTimeout(async () => {
                    // Load all data NOW that license is valid
                    await loadAllData();
                    gsap.to(overlay, {
                        opacity: 0, duration: 0.4, onComplete: () => {
                            overlay.style.display = 'none';
                            revealApp();
                        }
                    });
                }, 600);

            } else if (res.status === 'banned') {
                document.querySelector('.license-card').classList.add('banned');
                errorMsg.innerText = '⛔ ' + res.message;
                errorMsg.style.display = 'block';
                btn.innerHTML = '<i class="fa-solid fa-ban"></i> <span>HARDWARE BLOQUEADO</span>';
                btn.disabled = true;
                updateDots(0);

            } else {
                // Wrong key — shake and update dots
                attemptsLeft = Math.max(0, attemptsLeft - 1);
                updateDots(attemptsLeft);

                errorMsg.innerText = res.message;
                errorMsg.style.display = 'block';
                gsap.fromTo('.license-card',
                    { x: -10 }, { x: 0, duration: 0.5, ease: 'elastic.out(1,0.3)' }
                );
                input.value = '';
                input.focus();
                btn.innerHTML = '<i class="fa-solid fa-unlock"></i> <span>Verificar Acceso</span>';
                btn.disabled = false;
            }
        } catch (e) {
            console.error('Validate key error:', e);
            btn.innerHTML = '<i class="fa-solid fa-unlock"></i> <span>Verificar Acceso</span>';
            btn.disabled = false;
        }
    };
}

// ============================================================
// Reveal App
// ============================================================
function revealApp() {
    const mainApp = document.getElementById('main-app');
    gsap.to(mainApp, { opacity: 1, duration: 0.8, ease: 'power2.out' });
    switchPage('dashboard');

    setTimeout(() => {
        showToast('Naury Anti-Tamper', 'Sistema protegido contra Cracking', 'success');
    }, 1200);

    // Iniciar loop de temperaturas fluido
    updateTemperatures();
    setInterval(updateTemperatures, 1000); // 1 segundo
}

// -------------------------------------------
// Games & Temperatures
// -------------------------------------------
async function loadGames() {
    if (!window.pywebview || !window.pywebview.api) return;
    try {
        const res = await window.pywebview.api.get_installed_games();
        // Update both games grids (Dashboard and any others)
        const grids = [
            document.getElementById("games-grid"),
            document.getElementById("dashboard-games-container")
        ];
        
        grids.forEach(grid => {
            if (!grid) return;
            grid.innerHTML = "";
            if (res.status === "success" && res.data.length > 0) {
                // Limit to 6 items if this is the dashboard container
                const isDashboard = grid.id === "dashboard-games-container";
                const displayData = isDashboard ? res.data.slice(0, 6) : res.data;
                
                displayData.forEach(g => {
                    const card = document.createElement("div");
                    card.className = "game-card-glass";

                    let iconHtml = '';
                    if (g.icon) {
                        iconHtml = `<img src="data:image/png;base64,${g.icon}" class="game-icon-glass" alt="${g.name}">`;
                    } else {
                        iconHtml = `
                        <div class="game-icon-glass" style="background: rgba(108,107,255,0.16); display:flex; align-items:center; justify-content:center; color: var(--primary-2); font-size: 1.6rem; border-radius: 8px;">
                            <i class="fa-solid fa-gamepad"></i>
                        </div>`;
                    }

                    card.innerHTML = `
                        ${iconHtml}
                        <div class="game-name-glass">${g.name}</div>
                    `;
                    card.addEventListener("click", () => {
                        showToast("Perfil Aplicado", `Afinidad y prioridades inyectadas para ${g.name}.`, "success");
                    });
                    grid.appendChild(card);
                });
            } else {
                grid.innerHTML = `<div style="text-align:center; padding:20px; color:var(--text-secondary); grid-column: 1/-1;">No se detectaron juegos.</div>`;
            }
        });
    } catch(e) { console.error(e); }
}

async function loadRestorePoints() {
    if (!window.pywebview || !window.pywebview.api) return;
    const list = document.getElementById('restore-points-list');
    if (!list) return;

    list.innerHTML = `<div class="restore-points-loading"><div class="loader-ring lg"></div> Consultando el sistema...</div>`;

    try {
        const res = await window.pywebview.api.list_restore_points();
        if (res.status === 'success' && res.data && res.data.length > 0) {
            list.innerHTML = '';
            res.data.forEach(p => {
                const item = document.createElement('div');
                item.className = 'restore-point-item';

                const d = new Date(p.date);
                const dateStr = isNaN(d.getTime())
                    ? p.date
                    : d.toLocaleString('es-ES', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });

                item.innerHTML = `
                    <div class="restore-point-icon"><i class="fa-solid fa-clock-rotate-left"></i></div>
                    <div class="restore-point-info">
                        <strong>${p.description}</strong>
                        <span>${dateStr}</span>
                    </div>
                `;
                list.appendChild(item);
            });
            gsap.fromTo(list.querySelectorAll('.restore-point-item'),
                { opacity: 0, x: -10 }, { opacity: 1, x: 0, duration: 0.3, stagger: 0.05 });
        } else {
            list.innerHTML = `<div class="restore-points-empty"><i class="fa-solid fa-circle-info"></i><span>Aún no tienes puntos de restauración creados en este equipo.</span></div>`;
        }
    } catch (e) {
        list.innerHTML = `<div class="restore-points-empty"><i class="fa-solid fa-triangle-exclamation"></i><span>No se pudo consultar el historial de restauración.</span></div>`;
    }
}

let mainTempChart = null;
let netChart = null;
let currentTempTab = 'cpu'; // 'cpu' or 'gpu'
let tempHistory = { cpu: [], gpu: [], labels: [] };

function switchTempTab(tab) {
    currentTempTab = tab;
    document.querySelectorAll('.monitor-tab').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tab-' + tab).classList.add('active');
    
    document.getElementById('current-temp-label').innerText = tab.toUpperCase();
    if (tempHistory[tab].length > 0) {
        document.getElementById('current-temp-value').innerText = tempHistory[tab][tempHistory[tab].length - 1] + (tab === 'cpu' ? '%' : '°C');
    }
    
    if (mainTempChart) {
        mainTempChart.data.datasets[0].data = tempHistory[tab];
        mainTempChart.update();
    }
}

function createMonitorChart(canvasId, color = '#ff3c78') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;
    const ctx = canvas.getContext("2d");

    // Create intense glowing gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.parentElement.clientHeight || 220);
    const rgbaColor = color === '#ff3c78' ? 'rgba(255, 60, 120, ' : 'rgba(0, 240, 255, ';
    gradient.addColorStop(0, rgbaColor + '0.4)');
    gradient.addColorStop(1, rgbaColor + '0.01)');

    return new Chart(ctx, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                data: [],
                borderColor: color,
                backgroundColor: gradient,
                borderWidth: 2,
                fill: true,
                tension: 0, // 0 makes jagged mountains!
                pointRadius: 0,
                pointHitRadius: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 1000, easing: 'linear' }, // Smooth continuous sliding
            plugins: { 
                legend: { display: false },
                tooltip: { 
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: '#fff',
                    bodyColor: '#ff3c78',
                    displayColors: false
                } 
            },
            scales: {
                x: { 
                    display: true, 
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { display: false } // We use custom HTML ticks below
                },
                y: { 
                    min: 0, max: 100, display: true,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: 'rgba(255, 255, 255, 0.3)', maxTicksLimit: 5, callback: (v) => v }
                }
            },
            elements: { line: { borderJoinStyle: 'round' } }
        }
    });
}

let simulatedStats = {
    cpu: 45, gpu: 40, ram: 45, vram: 15, net: 40
};

function wanderValue(val, min, max, maxChange) {
    let delta = (Math.random() * maxChange * 2) - maxChange;
    let newVal = val + delta;
    if (newVal < min) newVal = min + Math.abs(delta);
    if (newVal > max) newVal = max - Math.abs(delta);
    return newVal;
}

async function updateTemperatures() {
    if (!window.pywebview || !window.pywebview.api) return;
    try {
        const res = await window.pywebview.api.get_temperatures();
        if (res.status === "success") {
            const now = new Date().toLocaleTimeString();
            
            // Wander values smoothly to simulate realistic live usage
            simulatedStats.cpu = wanderValue(simulatedStats.cpu, 20, 95, 6);
            simulatedStats.gpu = wanderValue(simulatedStats.gpu, 30, 85, 4);
            simulatedStats.ram = wanderValue(simulatedStats.ram, 30, 80, 2);
            simulatedStats.vram = wanderValue(simulatedStats.vram, 10, 40, 1.5);
            simulatedStats.net = wanderValue(simulatedStats.net, 5, 200, 30);
            
            const cpuVal = simulatedStats.cpu.toFixed(1);
            const gpuVal = simulatedStats.gpu.toFixed(1);
            const ramVal = simulatedStats.ram.toFixed(0);
            const vramVal = simulatedStats.vram.toFixed(0);
            const netVal = simulatedStats.net.toFixed(1);

            // Update top Dials with fluid simulated data
            const cpuCirc = document.getElementById('cpu-circ-prog');
            const ramCirc = document.getElementById('ram-circ-prog');
            const vramCirc = document.getElementById('vram-circ-prog');
            if (cpuCirc) { cpuCirc.style.setProperty('--prog', cpuVal + '%'); document.getElementById('cpu-circ-val').innerText = Math.round(cpuVal) + '%'; }
            if (ramCirc) { ramCirc.style.setProperty('--prog', ramVal + '%'); document.getElementById('ram-circ-val').innerText = ramVal + '%'; }
            if (vramCirc) { vramCirc.style.setProperty('--prog', vramVal + '%'); document.getElementById('vram-circ-val').innerText = vramVal + '%'; }

            // Init charts
            if (!mainTempChart) mainTempChart = createMonitorChart("mainTempChart", "#ff3c78");
            if (!netChart) netChart = createMonitorChart("netLineChart", "#00f0ff");

            // Store history
            if (tempHistory.labels.length > 40) {
                tempHistory.labels.shift();
                tempHistory.cpu.shift();
                tempHistory.gpu.shift();
            }
            tempHistory.labels.push(now);
            tempHistory.cpu.push(cpuVal);
            tempHistory.gpu.push(gpuVal);

            // Update visible badge
            const v = currentTempTab === 'cpu' ? cpuVal + '%' : gpuVal + '°C';
            const tempValEl = document.getElementById('current-temp-value');
            if (tempValEl) tempValEl.innerText = v;

            // Update main chart
            if (mainTempChart) {
                mainTempChart.data.labels = tempHistory.labels;
                mainTempChart.data.datasets[0].data = tempHistory[currentTempTab];
                mainTempChart.update();
            }

            // Update Network Chart
            if (netChart) {
                if (netChart.data.labels.length > 40) {
                    netChart.data.labels.shift();
                    netChart.data.datasets[0].data.shift();
                }
                netChart.data.labels.push(now);
                netChart.data.datasets[0].data.push(netVal);
                netChart.update();
                
                const dlEl = document.getElementById('net-dl-val');
                if (dlEl) dlEl.innerText = netVal;
            }
        }
    } catch(e) {}
}

// -------------------------------------------
// DEBLOATER LOGIC
// -------------------------------------------
let allApps = { Desktop: [], Store: [] };
let currentAppView = "Desktop";

async function loadDebloatApps() {
    if (!window.pywebview || !window.pywebview.api) return;
    try {
        const res = await window.pywebview.api.get_installed_programs();
        if (res.status === "success") {
            allApps = res.data;
            renderDebloatTable();
        }
    } catch(e) { console.error(e); }
}

function renderDebloatTable() {
    const tbody = document.getElementById("debloat-tbody");
    if(!tbody) return;
    tbody.innerHTML = "";

    const apps = allApps[currentAppView] || [];
    const search = (document.getElementById("debloat-search-input")?.value || "").toLowerCase();

    const filtered = apps.filter(a => a.Name.toLowerCase().includes(search));

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; padding:40px; color:var(--text-secondary);">No se encontraron aplicaciones</td></tr>`;
        return;
    }

    filtered.forEach(app => {
        const tr = document.createElement("tr");

        const n = app.Name.toLowerCase();
        let iconClass = "fa-solid fa-window-maximize";
        let iconColor = "#8888aa";

        // --- Redes sociales & Comunicación ---
        if (n.includes("spotify")) { iconClass = "fa-brands fa-spotify"; iconColor = "#1DB954"; }
        else if (n.includes("discord")) { iconClass = "fa-brands fa-discord"; iconColor = "#5865F2"; }
        else if (n.includes("slack")) { iconClass = "fa-brands fa-slack"; iconColor = "#4A154B"; }
        else if (n.includes("telegram")) { iconClass = "fa-brands fa-telegram"; iconColor = "#26A5E4"; }
        else if (n.includes("whatsapp")) { iconClass = "fa-brands fa-whatsapp"; iconColor = "#25D366"; }
        else if (n.includes("skype")) { iconClass = "fa-brands fa-skype"; iconColor = "#00aff0"; }
        else if (n.includes("teams")) { iconClass = "fa-brands fa-microsoft"; iconColor = "#6264A7"; }
        else if (n.includes("zoom")) { iconClass = "fa-solid fa-video"; iconColor = "#2D8CFF"; }
        else if (n.includes("facebook") || n.includes("meta")) { iconClass = "fa-brands fa-facebook"; iconColor = "#1877F2"; }
        else if (n.includes("instagram")) { iconClass = "fa-brands fa-instagram"; iconColor = "#E1306C"; }
        else if (n.includes("tiktok")) { iconClass = "fa-brands fa-tiktok"; iconColor = "#ff0050"; }
        else if (n.includes("twitter") || n.includes("x app")) { iconClass = "fa-brands fa-x-twitter"; iconColor = "#ffffff"; }
        else if (n.includes("linkedin")) { iconClass = "fa-brands fa-linkedin"; iconColor = "#0A66C2"; }
        else if (n.includes("snapchat")) { iconClass = "fa-brands fa-snapchat"; iconColor = "#FFFC00"; }
        else if (n.includes("pinterest")) { iconClass = "fa-brands fa-pinterest"; iconColor = "#E60023"; }
        else if (n.includes("reddit")) { iconClass = "fa-brands fa-reddit"; iconColor = "#FF4500"; }
        else if (n.includes("youtube")) { iconClass = "fa-brands fa-youtube"; iconColor = "#FF0000"; }
        else if (n.includes("twitch")) { iconClass = "fa-brands fa-twitch"; iconColor = "#9146FF"; }
        // --- Navegadores ---
        else if (n.includes("chrome")) { iconClass = "fa-brands fa-chrome"; iconColor = "#4285F4"; }
        else if (n.includes("firefox")) { iconClass = "fa-brands fa-firefox-browser"; iconColor = "#FF7139"; }
        else if (n.includes("edge")) { iconClass = "fa-brands fa-edge"; iconColor = "#0078D7"; }
        else if (n.includes("opera")) { iconClass = "fa-brands fa-opera"; iconColor = "#FF1B2D"; }
        else if (n.includes("brave")) { iconClass = "fa-brands fa-brave"; iconColor = "#FB542B"; }
        // --- Gaming ---
        else if (n.includes("xbox")) { iconClass = "fa-brands fa-xbox"; iconColor = "#107C10"; }
        else if (n.includes("steam")) { iconClass = "fa-brands fa-steam"; iconColor = "#1b2838"; }
        else if (n.includes("playstation") || n.includes("ps remote")) { iconClass = "fa-brands fa-playstation"; iconColor = "#003087"; }
        else if (n.includes("epic") || n.includes("fortnite")) { iconClass = "fa-solid fa-gamepad"; iconColor = "#2f2d2e"; }
        else if (n.includes("riot") || n.includes("valorant") || n.includes("league")) { iconClass = "fa-solid fa-crosshairs"; iconColor = "#D32936"; }
        else if (n.includes("game") || n.includes("solitaire") || n.includes("candy") || n.includes("wildtangent")) { iconClass = "fa-solid fa-dice"; iconColor = "#FF6B6B"; }
        // --- Antivirus / Seguridad ---
        else if (n.includes("mcafee") || n.includes("norton") || n.includes("avast") || n.includes("avg") || n.includes("kaspersky") || n.includes("bitdefender")) { iconClass = "fa-solid fa-shield-virus"; iconColor = "#ff0000"; }
        else if (n.includes("malware") || n.includes("security") || n.includes("defender")) { iconClass = "fa-solid fa-shield-halved"; iconColor = "#00a8ff"; }
        // --- Microsoft / Office ---
        else if (n.includes("word")) { iconClass = "fa-solid fa-file-word"; iconColor = "#2B579A"; }
        else if (n.includes("excel")) { iconClass = "fa-solid fa-file-excel"; iconColor = "#217346"; }
        else if (n.includes("powerpoint")) { iconClass = "fa-solid fa-file-powerpoint"; iconColor = "#D24726"; }
        else if (n.includes("onenote") || n.includes("one note")) { iconClass = "fa-solid fa-note-sticky"; iconColor = "#7719AA"; }
        else if (n.includes("outlook") || n.includes("mail")) { iconClass = "fa-solid fa-envelope"; iconColor = "#0078D4"; }
        else if (n.includes("onedrive")) { iconClass = "fa-brands fa-microsoft"; iconColor = "#0078D4"; }
        else if (n.includes("cortana")) { iconClass = "fa-solid fa-circle-nodes"; iconColor = "#00BCF2"; }
        else if (n.includes("microsoft") || n.includes("windows") || currentAppView === "Store") { iconClass = "fa-brands fa-microsoft"; iconColor = "#00a4ef"; }
        // --- Streaming / Media ---
        else if (n.includes("disney")) { iconClass = "fa-solid fa-film"; iconColor = "#113CCF"; }
        else if (n.includes("netflix")) { iconClass = "fa-solid fa-tv"; iconColor = "#E50914"; }
        else if (n.includes("amazon") || n.includes("prime")) { iconClass = "fa-brands fa-amazon"; iconColor = "#FF9900"; }
        else if (n.includes("hbo")) { iconClass = "fa-solid fa-film"; iconColor = "#5822b4"; }
        else if (n.includes("vlc")) { iconClass = "fa-solid fa-play"; iconColor = "#FF8800"; }
        else if (n.includes("itunes") || n.includes("apple")) { iconClass = "fa-brands fa-apple"; iconColor = "#A2AAAD"; }
        // --- Fabricantes OEM ---
        else if (n.includes("hp ") || n.includes("hewlett")) { iconClass = "fa-solid fa-laptop-code"; iconColor = "#0096D6"; }
        else if (n.includes("lenovo")) { iconClass = "fa-solid fa-laptop-code"; iconColor = "#E2231A"; }
        else if (n.includes("dell")) { iconClass = "fa-solid fa-laptop-code"; iconColor = "#007DB8"; }
        else if (n.includes("asus")) { iconClass = "fa-solid fa-laptop-code"; iconColor = "#00BFFF"; }
        else if (n.includes("acer")) { iconClass = "fa-solid fa-laptop-code"; iconColor = "#83B81A"; }
        else if (n.includes("samsung")) { iconClass = "fa-solid fa-mobile-screen"; iconColor = "#1428A0"; }
        // --- Desarrollo ---
        else if (n.includes("python")) { iconClass = "fa-brands fa-python"; iconColor = "#3776AB"; }
        else if (n.includes("node") || n.includes("npm")) { iconClass = "fa-brands fa-node-js"; iconColor = "#339933"; }
        else if (n.includes("java")) { iconClass = "fa-brands fa-java"; iconColor = "#007396"; }
        else if (n.includes("git")) { iconClass = "fa-brands fa-git-alt"; iconColor = "#F05032"; }
        else if (n.includes("visual studio") || n.includes("vs code") || n.includes("vscode")) { iconClass = "fa-solid fa-code"; iconColor = "#007ACC"; }
        // --- Utilidades / Otros ---
        else if (n.includes("adobe") || n.includes("photoshop") || n.includes("illustrator") || n.includes("acrobat")) { iconClass = "fa-solid fa-palette"; iconColor = "#FF0000"; }
        else if (n.includes("winrar") || n.includes("7-zip") || n.includes("zip") || n.includes("rar")) { iconClass = "fa-solid fa-file-zipper"; iconColor = "#6C63FF"; }
        else if (n.includes("driver") || n.includes("booster")) { iconClass = "fa-solid fa-gears"; iconColor = "#FFC107"; }
        else if (n.includes("clean") || n.includes("ccleaner")) { iconClass = "fa-solid fa-broom"; iconColor = "#E44D26"; }
        else if (n.includes("nvidia") || n.includes("geforce")) { iconClass = "fa-solid fa-display"; iconColor = "#76B900"; }
        else if (n.includes("amd") || n.includes("radeon")) { iconClass = "fa-solid fa-display"; iconColor = "#ED1C24"; }
        else if (n.includes("intel")) { iconClass = "fa-solid fa-microchip"; iconColor = "#0071C5"; }
        else if (n.includes("realtek")) { iconClass = "fa-solid fa-volume-high"; iconColor = "#0066CC"; }
        else if (n.includes("update") || n.includes("updater")) { iconClass = "fa-solid fa-arrows-rotate"; iconColor = "#4CAF50"; }
        else if (n.includes("print") || n.includes("scan")) { iconClass = "fa-solid fa-print"; iconColor = "#607D8B"; }
        else if (n.includes("calculator") || n.includes("calc")) { iconClass = "fa-solid fa-calculator"; iconColor = "#795548"; }
        else if (n.includes("photo") || n.includes("camera") || n.includes("image")) { iconClass = "fa-solid fa-camera"; iconColor = "#9C27B0"; }
        else if (n.includes("map")) { iconClass = "fa-solid fa-map-location-dot"; iconColor = "#4CAF50"; }
        else if (n.includes("weather")) { iconClass = "fa-solid fa-cloud-sun"; iconColor = "#03A9F4"; }
        else if (n.includes("clock") || n.includes("alarm")) { iconClass = "fa-solid fa-clock"; iconColor = "#FF9800"; }
        else if (n.includes("note") || n.includes("sticky")) { iconClass = "fa-solid fa-note-sticky"; iconColor = "#FFEB3B"; }
        else if (n.includes("paint") || n.includes("draw") || n.includes("3d")) { iconClass = "fa-solid fa-paintbrush"; iconColor = "#E91E63"; }
        else if (n.includes("record") || n.includes("voice") || n.includes("sound")) { iconClass = "fa-solid fa-microphone"; iconColor = "#9C27B0"; }
        else if (n.includes("book") || n.includes("reader") || n.includes("kindle")) { iconClass = "fa-solid fa-book"; iconColor = "#795548"; }
        else if (n.includes("cloud") || n.includes("dropbox") || n.includes("backup")) { iconClass = "fa-solid fa-cloud"; iconColor = "#42A5F5"; }
        else if (n.includes("vpn") || n.includes("tunnel")) { iconClass = "fa-solid fa-lock"; iconColor = "#00BCD4"; }
        else if (n.includes("torrent") || n.includes("utorrent") || n.includes("bittorrent")) { iconClass = "fa-solid fa-download"; iconColor = "#43A047"; }
        else if (n.includes("notepad") || n.includes("text") || n.includes("editor")) { iconClass = "fa-solid fa-file-lines"; iconColor = "#78909C"; }
        else if (n.includes("phone") || n.includes("link") || n.includes("your")) { iconClass = "fa-solid fa-mobile"; iconColor = "#0078D4"; }
        else if (n.includes("help") || n.includes("feedback") || n.includes("tips")) { iconClass = "fa-solid fa-circle-question"; iconColor = "#78909C"; }
        else if (n.includes("store") || n.includes("shop") || n.includes("booking")) { iconClass = "fa-solid fa-bag-shopping"; iconColor = "#003580"; }

        let iconHtml = `<div class="debloat-app-icon" style="color: ${iconColor}; text-shadow: 0 0 10px ${iconColor}40;"><i class="${iconClass}"></i></div>`;

        const sizeStr = app.SizeMB > 0 ? `${app.SizeMB} MB` : "N/A";
        // Almacenar el comando en dataset para la desinstalación
        tr.dataset.cmd = app.UninstallCmd;
        tr.dataset.name = app.Name;

        tr.innerHTML = `
            <td><input type="checkbox" class="debloat-cb"></td>
            <td>
                <div class="debloat-app-name">
                    ${iconHtml}
                    <div class="debloat-app-info">
                        <strong>${app.Name}</strong>
                        <span>${app.Version}</span>
                    </div>
                </div>
            </td>
            <td>${sizeStr}</td>
            <td>${app.Date}</td>
        `;
        tbody.appendChild(tr);
    });

    updateDebloatSelection();

    // Bind checkboxes
    document.querySelectorAll(".debloat-cb").forEach(cb => {
        cb.addEventListener("change", updateDebloatSelection);
    });
}

function updateDebloatSelection() {
    const checked = document.querySelectorAll(".debloat-cb:checked").length;
    const btn = document.getElementById("debloat-uninstall-btn");
    btn.innerText = `Uninstall (${checked})`;
    if(checked > 0) {
        btn.classList.add("ready");
        btn.disabled = false;
    } else {
        btn.classList.remove("ready");
        btn.disabled = true;
    }
}

// Bind events on load
window.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("debloat-search-input");
    if(searchInput) searchInput.addEventListener("input", renderDebloatTable);

    const tDesk = document.getElementById("toggle-desktop");
    const tStore = document.getElementById("toggle-store");

    if(tDesk) {
        tDesk.addEventListener("click", () => {
            tDesk.classList.add("active"); tStore.classList.remove("active");
            currentAppView = "Desktop"; renderDebloatTable();
        });
    }
    if(tStore) {
        tStore.addEventListener("click", () => {
            tStore.classList.add("active"); tDesk.classList.remove("active");
            currentAppView = "Store"; renderDebloatTable();
        });
    }

    const selectAll = document.getElementById("debloat-select-all");
    if(selectAll) {
        selectAll.addEventListener("change", (e) => {
            document.querySelectorAll(".debloat-cb").forEach(cb => cb.checked = e.target.checked);
            updateDebloatSelection();
        });
    }

    const uninstBtn = document.getElementById("debloat-uninstall-btn");
    if(uninstBtn) {
        uninstBtn.addEventListener("click", async () => {
            const rows = document.querySelectorAll("#debloat-tbody tr");
            const selected = [];
            rows.forEach(r => {
                const cb = r.querySelector(".debloat-cb");
                if(cb && cb.checked) {
                    selected.push({ name: r.dataset.name, cmd: r.dataset.cmd, isStore: currentAppView === "Store" });
                }
            });
            if(selected.length === 0) return;
            await uninstallAppsList(selected);
        });
    }
});

// -------------------------------------------
// AUTO DEBLOAT (detecta bloatware conocido y lo desinstala en lote)
// -------------------------------------------
const KNOWN_BLOATWARE = [
    'candy crush', 'xbox game bar', 'mixed reality', '3d viewer', 'paint 3d',
    'skype', 'disney+', 'disney plus', 'tiktok', 'instagram', 'facebook',
    'spotify music', 'mcafee', 'norton', 'wildtangent', 'booking.com',
    'linkedin', 'solitaire', 'feedback hub', 'get help', 'people app',
    'your phone', 'phone link', 'cortana', 'mail and calendar', 'maps',
    'sticky notes', 'clipchamp', 'game assist',
    'hp jumpstart', 'hp support assistant', 'dell supportassist', 'dell digital delivery',
    'asus giftbox', 'lenovo vantage', 'mcafee livesafe', 'driver booster'
];

async function runAutoDebloat() {
    if (!window.pywebview || !window.pywebview.api) return;
    if (!allApps.Desktop.length && !allApps.Store.length) {
        await loadDebloatApps();
    }
    const matches = [];
    ['Desktop', 'Store'].forEach(view => {
        (allApps[view] || []).forEach(app => {
            const low = (app.Name || '').toLowerCase();
            if (KNOWN_BLOATWARE.some(kw => low.includes(kw))) {
                matches.push({ name: app.Name, cmd: app.UninstallCmd, isStore: view === 'Store' });
            }
        });
    });

    if (matches.length === 0) {
        showToast('Auto Debloat', 'No se detectó bloatware conocido. Tu instalación ya está limpia.', 'success');
        return;
    }

    const preview = matches.slice(0, 12).map(m => `• ${m.name}`).join('\n');
    const more = matches.length > 12 ? `\n... y ${matches.length - 12} más` : '';
    const ok = window.confirm(`Se detectaron ${matches.length} apps de bloatware conocido:\n\n${preview}${more}\n\n¿Desinstalarlas todas?`);
    if (!ok) return;

    await uninstallAppsList(matches);
}

async function uninstallAppsList(selected) {
    const taskId = "task_" + Date.now();
    openModal();
    addModalTask(taskId, `Iniciando desinstalación profunda de ${selected.length} apps...`);

    let completed = 0;
    for (let app of selected) {
        try {
            addModalTask(taskId + "_" + completed, `Desinstalando y buscando restos de: ${app.name}...`);
            const res = await window.pywebview.api.advanced_uninstall(app.name, app.cmd, !!app.isStore);
            updateModalTask(taskId + "_" + completed, res.status, res.message);
        } catch {
            updateModalTask(taskId + "_" + completed, 'error', "Error en desinstalador");
        }
        completed++;
        updateModalProgress((completed / selected.length) * 100);
    }
    updateModalTask(taskId, 'success', `Auto Debloat completado (${selected.length} apps procesadas).`);
    loadDebloatApps();
}

// ============================================================
// Logout functionality (in-app modal, not window.confirm)
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    const profileCard = document.querySelector('.sidebar-profile');
    if (profileCard) {
        profileCard.addEventListener('click', () => {
            // Create in-app modal
            let modal = document.getElementById('logout-modal');
            if (modal) modal.remove();
            modal = document.createElement('div');
            modal.id = 'logout-modal';
            modal.style.cssText = 'position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);backdrop-filter:blur(8px);opacity:0;transition:opacity 0.3s';
            modal.innerHTML = `
                <div style="background:var(--card-bg);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:32px 28px;max-width:380px;width:90%;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,0.6)">
                    <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#ff3c78,#ff6b6b);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;font-size:1.5rem;color:#fff">
                        <i class="fa-solid fa-right-from-bracket"></i>
                    </div>
                    <h3 style="color:var(--text-primary);font-size:1.1rem;margin-bottom:8px">Cerrar Sesión</h3>
                    <p style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:24px;line-height:1.5">¿Estás seguro de que quieres cerrar sesión y desvincular tu licencia de este equipo?</p>
                    <div style="display:flex;gap:12px;justify-content:center">
                        <button id="logout-cancel" style="flex:1;padding:12px;border-radius:12px;border:1px solid rgba(255,255,255,0.1);background:rgba(255,255,255,0.05);color:var(--text-secondary);cursor:pointer;font-size:0.85rem;font-weight:600;transition:all 0.2s">Cancelar</button>
                        <button id="logout-confirm" style="flex:1;padding:12px;border-radius:12px;border:none;background:linear-gradient(135deg,#ff3c78,#ff6b6b);color:#fff;cursor:pointer;font-size:0.85rem;font-weight:700;transition:all 0.2s;box-shadow:0 4px 15px rgba(255,60,120,0.4)">Cerrar Sesión</button>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
            requestAnimationFrame(() => modal.style.opacity = '1');

            document.getElementById('logout-cancel').onclick = () => {
                modal.style.opacity = '0';
                setTimeout(() => modal.remove(), 300);
            };
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.opacity = '0';
                    setTimeout(() => modal.remove(), 300);
                }
            });
            document.getElementById('logout-confirm').onclick = async () => {
                try {
                    await window.pywebview.api.logout_license();
                    window.location.reload();
                } catch (e) {
                    console.error('Error logging out', e);
                }
            };
        });
    }
});
// ============================================================
// Auto-Updater Check on Startup (Forced)
// ============================================================
window.addEventListener('pywebviewready', async () => {
    try {
        const res = await window.pywebview.api.check_for_updates();
        if (res.status === "update_available") {
            // Create Forced Update Modal
            const modal = document.createElement('div');
            modal.id = 'update-modal';
            modal.style.cssText = 'position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.85);backdrop-filter:blur(10px);opacity:0;transition:opacity 0.3s';
            
            modal.innerHTML = `
                <div style="background:var(--card-bg);border:1px solid rgba(255,60,120,0.3);border-radius:20px;padding:40px 30px;max-width:420px;width:90%;text-align:center;box-shadow:0 20px 80px rgba(255,60,120,0.2)">
                    <div style="width:70px;height:70px;border-radius:50%;background:linear-gradient(135deg,#ff3c78,#ff6b6b);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:2rem;color:#fff;box-shadow:0 0 20px rgba(255,60,120,0.4)">
                        <i class="fa-solid fa-arrows-rotate"></i>
                    </div>
                    <h3 style="color:var(--text-primary);font-size:1.4rem;margin-bottom:12px;font-weight:700">Actualización Crítica</h3>
                    <p style="color:var(--text-secondary);font-size:0.95rem;margin-bottom:16px;line-height:1.5">
                        Se ha detectado una nueva versión de Naury Utility (v${res.version}).<br><br>
                        <strong style="color:var(--primary)">Esta actualización es obligatoria</strong> para continuar utilizando el software y acceder a los servidores de licencias.
                    </p>
                    ${res.notes ? `<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px;margin-bottom:20px;text-align:left;max-height:120px;overflow-y:auto">
                        <div style="color:#00f0ff;font-size:0.75rem;font-weight:700;text-transform:uppercase;margin-bottom:8px"><i class="fa-solid fa-scroll" style="margin-right:6px"></i>Notas del Desarrollador</div>
                        <p style="color:var(--text-secondary);font-size:0.85rem;line-height:1.5;margin:0;white-space:pre-wrap">${res.notes}</p>
                    </div>` : ''}
                    <button id="force-update-btn" style="width:100%;padding:14px;border-radius:12px;background:var(--primary);color:#fff;border:none;font-size:1rem;font-weight:600;cursor:pointer;transition:transform 0.2s, background 0.2s;box-shadow:0 0 15px rgba(255,60,120,0.3)">
                        ACTUALIZAR AHORA
                    </button>
                    <div id="update-progress-text" style="display:none;margin-top:16px;color:var(--cyan);font-weight:600;font-size:0.9rem">
                        Descargando actualización, por favor espera...
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            // Trigger fade in
            setTimeout(() => modal.style.opacity = '1', 50);

            const updateBtn = modal.querySelector('#force-update-btn');
            const progressText = modal.querySelector('#update-progress-text');
            const icon = modal.querySelector('.fa-arrows-rotate');

            updateBtn.addEventListener('click', async () => {
                updateBtn.disabled = true;
                updateBtn.style.opacity = '0.5';
                progressText.style.display = 'block';
                icon.classList.add('fa-spin');
                
                const upRes = await window.pywebview.api.perform_update(res.url);
                if (upRes.status === "error") {
                    progressText.style.color = '#ff6b6b';
                    progressText.innerText = "Error: " + upRes.message;
                    updateBtn.disabled = false;
                    updateBtn.style.opacity = '1';
                    icon.classList.remove('fa-spin');
                } else {
                    progressText.style.color = '#4CAF50';
                    progressText.innerText = "¡Actualización descargada! Reiniciando...";
                }
            });
        }
    } catch (e) {
        console.error("Updater error:", e);
    }
});
