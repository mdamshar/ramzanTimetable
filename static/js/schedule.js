// ===== SCHEDULE.JS - Full schedule page =====

let allDays = [];
let filteredDays = [];
let selectedDay = null;
const todayDate = getLocalIsoDate();

function getLocalIsoDate() {
    const now = new Date();
    const offsetMinutes = now.getTimezoneOffset();
    const localDate = new Date(now.getTime() - offsetMinutes * 60000);
    return localDate.toISOString().split('T')[0];
}

async function loadSchedule() {
    try {
        const res = await fetch('/api/schedule/');
        if (!res.ok) {
            throw new Error(`Request failed with status ${res.status}`);
        }
        allDays = await res.json();
        filteredDays = [...allDays];
        renderSchedule(filteredDays);
        document.getElementById('schedule-loading').classList.add('hidden');
        document.getElementById('schedule-content').classList.remove('hidden');
    } catch (err) {
        console.error('Error loading schedule:', err);
        document.getElementById('schedule-loading').innerHTML = '<p style="color:#f5c842">Error loading schedule. Please refresh.</p>';
    }
}

function renderSchedule(days) {
    renderTable(days);
    renderMobileCards(days);
    document.getElementById('showing-count').textContent = days.length;

    const noResults = document.getElementById('no-results');
    if (days.length === 0) noResults.classList.remove('hidden');
    else noResults.classList.add('hidden');
}

function renderTable(days) {
    const tbody = document.getElementById('schedule-tbody');
    tbody.innerHTML = '';

    days.forEach(day => {
        const isToday = day.gregorian_date === todayDate;
        const tr = document.createElement('tr');
        if (isToday) tr.classList.add('today-row');
        tr.onclick = () => openModal(day);

                tr.innerHTML = `
      <td class="day-num-cell">
        ${day.ramadan_day}
        ${isToday ? '<br><span class="today-badge">Today</span>' : ''}
      </td>
      <td>${day.islamic_date}</td>
      <td>${day.gregorian_date_display}</td>
      <td>
        <div class="day-names-cell">
          <span class="cell-en">${day.day_name_en}</span>
          <span class="cell-ur">${day.day_name_ur || ''}</span>
          <span class="cell-hi">${day.day_name_hi || ''}</span>
        </div>
      </td>
      <td class="time-cell">${day.sehri_time_formatted}</td>
      <td class="time-cell">${day.iftar_time_formatted}</td>
      <td><button class="view-btn" type="button">View Card</button></td>
    `;

        const viewBtn = tr.querySelector('.view-btn');
        if (viewBtn) {
            viewBtn.addEventListener('click', (event) => {
                event.stopPropagation();
                openModal(day);
            });
        }

        tbody.appendChild(tr);
    });
}

function renderMobileCards(days) {
    const container = document.getElementById('mobile-schedule');
    container.innerHTML = '';

    days.forEach(day => {
        const isToday = day.gregorian_date === todayDate;
        const card = document.createElement('div');
        card.className = `mobile-day-card${isToday ? ' today-card' : ''}`;
        card.onclick = () => openModal(day);

        card.innerHTML = `
      <div class="mobile-card-header">
        <div>
          <div class="mobile-day-num">Day ${day.ramadan_day} ${isToday ? '<span class="today-badge">Today</span>' : ''}</div>
          <div class="mobile-dates">${day.islamic_date} • ${day.gregorian_date_display}</div>
        </div>
        <div class="mobile-day-name">${day.day_name_ur || day.day_name_en}</div>
      </div>
      <div class="mobile-times">
        <div class="mobile-time-item">
          <div class="mobile-time-label">🌅 Sehri</div>
          <div class="mobile-time-val">${day.sehri_time_formatted}</div>
        </div>
        <div class="mobile-time-item">
          <div class="mobile-time-label">🌇 Iftar</div>
          <div class="mobile-time-val">${day.iftar_time_formatted}</div>
        </div>
      </div>
    `;
        container.appendChild(card);
    });
}

// Search
const searchInput = document.getElementById('search-input');
if (searchInput) {
    searchInput.addEventListener('input', function () {
        const q = this.value.toLowerCase().trim();
        if (!q) {
            filteredDays = [...allDays];
        } else {
            filteredDays = allDays.filter(day =>
                String(day.ramadan_day).includes(q) ||
                day.day_name_en.toLowerCase().includes(q) ||
                (day.day_name_ur && day.day_name_ur.includes(q)) ||
                (day.day_name_hi && day.day_name_hi.includes(q)) ||
                day.gregorian_date_display.toLowerCase().includes(q) ||
                day.islamic_date.toLowerCase().includes(q)
            );
        }
        renderSchedule(filteredDays);
    });
}

// Modal
function openModal(day) {
    selectedDay = day;
    const modal = document.getElementById('day-modal');

    document.getElementById('modal-day-num').textContent = day.ramadan_day;
    document.getElementById('modal-day-en').textContent = day.day_name_en;
    document.getElementById('modal-day-ur').textContent = day.day_name_ur || '';
    document.getElementById('modal-day-hi').textContent = day.day_name_hi || '';
    document.getElementById('modal-islamic').textContent = day.islamic_date;
    document.getElementById('modal-greg').textContent = day.gregorian_date_display;
    document.getElementById('modal-sehri').textContent = day.sehri_time_formatted;
    document.getElementById('modal-iftar').textContent = day.iftar_time_formatted;
    document.getElementById('modal-org').textContent = day.organization_name || 'Ramadan Timetable 1447 AH';

    const duaSection = document.getElementById('modal-dua-section');
    if (day.dua_text) {
        document.getElementById('modal-dua-text').textContent = day.dua_text;
        document.getElementById('modal-dua-trans').textContent = day.dua_translation || '';
        duaSection.style.display = 'block';
    } else {
        duaSection.style.display = 'none';
    }

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('day-modal').classList.add('hidden');
    document.body.style.overflow = '';
    selectedDay = null;
}

// Close modal on overlay click
const dayModal = document.getElementById('day-modal');
if (dayModal) {
    dayModal.addEventListener('click', function (e) {
        if (e.target === this) closeModal();
    });
}

// Close on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
});

// Download modal card
async function downloadModalCard() {
    const card = document.getElementById('modal-card');
    if (!card || !selectedDay) return;

    try {
        const canvas = await html2canvas(card, {
            scale: 3,
            backgroundColor: '#0a1628',
            useCORS: true,
            logging: false,
        });
        const link = document.createElement('a');
        link.download = `ramadan-day-${selectedDay.ramadan_day}-timetable.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    } catch (err) {
        console.error('Download error:', err);
        alert('Could not generate image. Please try again.');
    }
}

// Init
loadSchedule();
