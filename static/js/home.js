// ===== HOME.JS - Homepage logic =====

let todayData = null;
let iftarInterval = null;

function getLocalIsoDate() {
    const now = new Date();
    const offsetMinutes = now.getTimezoneOffset();
    const localDate = new Date(now.getTime() - offsetMinutes * 60000);
    return localDate.toISOString().split('T')[0];
}

async function loadTodayData() {
    try {
        const res = await fetch('/api/today/');
        if (!res.ok) {
            throw new Error(`Request failed with status ${res.status}`);
        }
        const json = await res.json();
        if (json.data) {
            todayData = json.data;
            renderCard(todayData);
            updateHeroDate(todayData);
            updateStats(todayData);
            startCountdown(todayData);
        } else {
            document.getElementById('card-loading').classList.add('hidden');
            document.getElementById('card-no-data').classList.remove('hidden');
        }
    } catch (err) {
        console.error('Error loading today data:', err);
        document.getElementById('card-loading').classList.add('hidden');
        document.getElementById('card-no-data').classList.remove('hidden');
    }
}

function renderCard(data) {
    document.getElementById('card-loading').classList.add('hidden');
    document.getElementById('card-wrapper').classList.remove('hidden');

    document.getElementById('card-day-number').textContent = data.ramadan_day;
    document.getElementById('card-day-en').textContent = data.day_name_en;
    document.getElementById('card-day-ur').textContent = data.day_name_ur || '';
    document.getElementById('card-day-hi').textContent = data.day_name_hi || '';
    document.getElementById('card-islamic-date').textContent = data.islamic_date;
    document.getElementById('card-greg-date').textContent = data.gregorian_date_display;
    document.getElementById('card-sehri-time').textContent = data.sehri_time_formatted;
    document.getElementById('card-iftar-time').textContent = data.iftar_time_formatted;
    document.getElementById('card-org-name').textContent = data.organization_name || 'Ramadan Timetable 1447 AH';
    document.getElementById('card-location').textContent = data.location || 'India';

    const duaSection = document.getElementById('card-dua-section');
    if (data.dua_text) {
        document.getElementById('card-dua-text').textContent = data.dua_text;
        document.getElementById('card-dua-translation').textContent = data.dua_translation || '';
        duaSection.style.display = 'block';
    } else {
        duaSection.style.display = 'none';
    }
}

function updateHeroDate(data) {
    document.getElementById('gregorian-date-hero').textContent = data.gregorian_date_display;
    document.getElementById('islamic-date-hero').textContent = data.islamic_date;
}

function updateStats(data) {
    document.getElementById('stat-sehri').textContent = data.sehri_time_formatted;
    document.getElementById('stat-iftar').textContent = data.iftar_time_formatted;
    document.getElementById('stat-day').textContent = `Day ${data.ramadan_day}`;
}

function startCountdown(data) {
    if (!data.iftar_time) return;

    function tick() {
        const now = new Date();
        const today = getLocalIsoDate();
        const iftarStr = `${today}T${data.iftar_time}`;
        const iftarTime = new Date(iftarStr);
        const diff = iftarTime - now;

        const label = document.getElementById('countdown-iftar-label');
        const val = document.getElementById('countdown-iftar-val');
        if (val) val.textContent = data.iftar_time_formatted;

        if (diff <= 0) {
            document.getElementById('ct-hours').textContent = '00';
            document.getElementById('ct-minutes').textContent = '00';
            document.getElementById('ct-seconds').textContent = '00';
            if (label) label.innerHTML = '🎉 <strong>Iftar Time! Ramadan Mubarak!</strong>';
            return;
        }

        const hours = Math.floor(diff / 3600000);
        const minutes = Math.floor((diff % 3600000) / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);

        document.getElementById('ct-hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('ct-minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('ct-seconds').textContent = String(seconds).padStart(2, '0');
    }

    tick();
    iftarInterval = setInterval(tick, 1000);
}

// Download card as image
async function downloadCard() {
    const card = document.getElementById('timetable-card');
    const btn = document.getElementById('download-btn');
    if (!card) return;

    btn.textContent = '⏳ Generating...';
    btn.disabled = true;

    try {
        const dayNumberEl = document.getElementById('card-day-number');
        if (dayNumberEl && todayData && String(dayNumberEl.textContent || '').trim() === '') {
            dayNumberEl.textContent = todayData.ramadan_day;
        }

        if (document.fonts && document.fonts.ready) {
            await document.fonts.ready;
        }

        card.classList.add('capture-mode');
        const canvas = await html2canvas(card, {
            scale: 3,
            backgroundColor: '#0a1628',
            useCORS: true,
            logging: false,
        });
        card.classList.remove('capture-mode');

        const link = document.createElement('a');
        const dayNum = todayData ? todayData.ramadan_day : 'today';
        link.download = `ramadan-day-${dayNum}-timetable.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
    } catch (err) {
        card.classList.remove('capture-mode');
        console.error('Download error:', err);
        alert('Could not generate image. Please try again.');
    } finally {
        btn.innerHTML = '<span class="download-icon">⬇️</span> Download Today\'s Timetable';
        btn.disabled = false;
    }
}

// Share card
async function shareCard() {
    const card = document.getElementById('timetable-card');
    if (!card) return;

    try {
        const canvas = await html2canvas(card, { scale: 2, backgroundColor: '#0a1628', useCORS: true });
        canvas.toBlob(async (blob) => {
            if (navigator.share && navigator.canShare) {
                const file = new File([blob], 'ramadan-timetable.png', { type: 'image/png' });
                if (navigator.canShare({ files: [file] })) {
                    await navigator.share({ files: [file], title: 'Ramadan Timetable', text: 'رمضان مبارک - Ramadan Mubarak!' });
                    return;
                }
            }
            // Fallback: download
            downloadCard();
        });
    } catch (err) {
        downloadCard();
    }
}

// Init
loadTodayData();
