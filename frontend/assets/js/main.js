
const journalData = {
    '2025-09-01': {
        pnl: 150.00,
        trades: [
            { ticker: 'AAPL', pnl: 250.00, win: true, before_img: 'samples/samples-img/dashboard1.png', after_img: 'samples/samples-img/dashboard2.png', note: 'Good entry on breakout.' },
            { ticker: 'TSLA', pnl: -100.00, win: false, before_img: 'samples/samples-img/dashboard3.png', after_img: 'samples/samples-img/dashboard4.png', note: 'Stopped out, bad timing.' },
        ],
        note: 'Overall a good day. Followed my plan on AAPL, but was a bit early on TSLA.'
    },
    '2025-09-02': {
        pnl: 500.00,
        trades: [
            { ticker: 'GOOG', pnl: 500.00, win: true, before_img: 'samples/samples-img/dashboard5.png', after_img: 'samples/samples-img/dashboard6.png', note: 'Caught the reversal perfectly.' },
        ],
        note: 'Excellent trading day. Very focused.'
    },
    '2025-09-03': {
        pnl: -350.00,
        trades: [
            { ticker: 'AMZN', pnl: -250.00, win: false, before_img: 'samples/samples-img/report1.png', after_img: 'samples/samples-img/report2.png', note: 'Choppy market.' },
            { ticker: 'MSFT', pnl: -100.00, win: false, before_img: 'samples/samples-img/dashboard1.png', after_img: 'samples/samples-img/dashboard2.png', note: 'Revenge trade.' },
        ],
        note: 'Frustrating day. Need to work on my discipline.'
    },
    '2025-09-04': {
        pnl: 750.00,
        trades: [
            { ticker: 'NVDA', pnl: 750.00, win: true, before_img: 'samples/samples-img/dashboard3.png', after_img: 'samples/samples-img/dashboard4.png', note: 'Earnings play worked out perfectly.' },
        ],
        note: 'Great win today. Patience paid off.'
    },
    '2025-09-05': {
        pnl: 0,
        trades: [],
        note: 'No trades today. Market was too uncertain.'
    },
};

const tradeData = {
    netPNL: 14742,
    profitFactor: 1.82,
    winrate: 31.78,
    avgWinLoss: 3.90,
    recentTrades: [
        { date: '2025-09-01', ticker: 'AAPL', net_pnl: 250.00, roi: 1.67 },
        { date: '2025-09-01', ticker: 'TSLA', net_pnl: -1000.00, roi: -1.11 },
        { date: '2025-08-30', ticker: 'GOOG', net_pnl: 2500.00, roi: 0.89 },
    ],
    journal: journalData
};

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Feather Icons
    feather.replace();

    // Initialize animations
    AOS.init({
        duration: 800,
        once: true,
    });

    // Theme switcher
    initializeTheme();

    // Render charts
    renderEquityCurve();
    renderNetBarChart();
    renderPerformanceRadar();

    // Render calendars
    if (document.getElementById('calendar-grid')) {
        if (window.location.pathname.includes('daily-journal.html')) {
            const urlParams = new URLSearchParams(window.location.search);
            const date = urlParams.get('date');
            const today = date ? new Date(date + 'T00:00:00') : new Date(2025, 8, 1);
            renderJournalCalendar(today.getFullYear(), today.getMonth(), today.getDate());
            renderJournal(today.toISOString().split('T')[0]);
        } else {
            renderDashboardCalendar();
        }
    }
});

function initializeTheme() {
    const lightModeIcon = document.getElementById('light-mode-icon');
    const darkModeIcon = document.getElementById('dark-mode-icon');
    const body = document.body;

    const theme = localStorage.getItem('theme');
    if (theme === 'dark') {
        body.classList.add('dark-mode');
        if(lightModeIcon) lightModeIcon.classList.remove('active');
        if(darkModeIcon) darkModeIcon.classList.add('active');
    } else {
        body.classList.remove('dark-mode');
        if(lightModeIcon) lightModeIcon.classList.add('active');
        if(darkModeIcon) darkModeIcon.classList.remove('active');
    }

    if(lightModeIcon) {
        lightModeIcon.addEventListener('click', () => {
            body.classList.remove('dark-mode');
            lightModeIcon.classList.add('active');
            darkModeIcon.classList.remove('active');
            localStorage.setItem('theme', 'light');
        });
    }

    if(darkModeIcon) {
        darkModeIcon.addEventListener('click', () => {
            body.classList.add('dark-mode');
            lightModeIcon.classList.remove('active');
            darkModeIcon.classList.add('active');
            localStorage.setItem('theme', 'dark');
        });
    }
}

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: '#94a3b8'
            }
        }
    },
    scales: {
        y: {
            beginAtZero: false,
            grid: {
                color: '#334155'
            },
            ticks: {
                color: '#94a3b8'
            }
        },
        x: {
            grid: {
                color: '#334155'
            },
            ticks: {
                color: '#94a3b8'
            }
        }
    }
};

function renderEquityCurve() {
    const ctx = document.getElementById('equityCurve')?.getContext('2d');
    if (!ctx) return;

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.4)');
    gradient.addColorStop(1, 'rgba(56, 189, 248, 0)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Equity',
                data: [10000, 12000, 11500, 13000, 14000, 15000, 14742],
                backgroundColor: gradient,
                borderColor: '#38bdf8',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#38bdf8',
                pointBorderColor: '#fff',
                pointHoverRadius: 7,
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#38bdf8'
            }]
        },
        options: chartOptions
    });
}

function renderNetBarChart() {
    const ctx = document.getElementById('netBarChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
            datasets: [{
                label: 'Net P&L',
                data: [1500, 2500, -500, 3000, -1000, 4000, 2242],
                backgroundColor: (context) => {
                    const value = context.dataset.data[context.dataIndex];
                    return value >= 0 ? '#34d399' : '#f87171';
                },
                borderRadius: 4,
            }]
        },
        options: {
            ...chartOptions,
            scales: {
                ...chartOptions.scales,
                y: {
                    ...chartOptions.scales.y,
                    beginAtZero: true
                }
            }
        }
    });
}

function renderPerformanceRadar() {
    const ctx = document.getElementById('performanceRadar')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Consistency', 'Winrate', 'Profit Factor', 'Risk Mgmt'],
            datasets: [{
                label: 'Performance',
                data: [80, 60, 75, 90],
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderColor: '#38bdf8',
                pointBackgroundColor: '#38bdf8',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#38bdf8'
            }]
        },
        options: {
            ...chartOptions,
            scales: {
                r: {
                    angleLines: {
                        color: '#334155'
                    },
                    grid: {
                        color: '#334155'
                    },
                    pointLabels: {
                        color: '#94a3b8',
                        font: {
                            size: 12
                        }
                    },
                    ticks: {
                        color: '#94a3b8',
                        backdropColor: 'transparent'
                    }
                }
            }
        }
    });
}

function renderDashboardCalendar() {
    const calendarGrid = document.getElementById('calendar-grid');
    if (!calendarGrid) return;

    const today = new Date(2025, 8, 1);
    const year = today.getFullYear();
    const month = today.getMonth();

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    calendarGrid.innerHTML = '';

    for (let i = 0; i < firstDay; i++) {
        calendarGrid.appendChild(document.createElement('div'));
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayEl = document.createElement('a');
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        dayEl.href = `daily-journal.html?date=${dateStr}`;
        dayEl.className = 'calendar-day p-2 rounded-lg text-center';
        dayEl.textContent = day;

        if (journalData[dateStr]) {
            const pnl = journalData[dateStr].pnl;
            dayEl.classList.add(pnl >= 0 ? 'profit' : 'loss');
        }

        if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
            dayEl.classList.add('selected');
        }

        calendarGrid.appendChild(dayEl);
    }
}

function renderJournalCalendar(year, month, selectedDay) {
    const calendarGrid = document.getElementById('calendar-grid');
    if (!calendarGrid) return;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    calendarGrid.innerHTML = '';

    for (let i = 0; i < firstDay; i++) {
        calendarGrid.appendChild(document.createElement('div'));
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayEl = document.createElement('a');
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        
        dayEl.href = `daily-journal.html?date=${dateStr}`;
        dayEl.className = 'calendar-day rounded-lg';
        
        let dayContent = `<div class="day-number">${day}</div>`;

        if (journalData[dateStr]) {
            const data = journalData[dateStr];
            const pnl = data.pnl;
            const trades = data.trades?.length || 0;
            dayEl.classList.add(pnl >= 0 ? 'profit' : 'loss');
            dayContent += `
                <div class="day-details">
                    <div class="day-pnl ${pnl >= 0 ? 'text-success' : 'text-danger'}">${pnl.toFixed(2)}</div>
                    <div class="day-trades">${trades} trades</div>
                </div>
            `;
        }

        dayEl.innerHTML = dayContent;

        if (day === selectedDay) {
            dayEl.classList.add('selected');
        }

        calendarGrid.appendChild(dayEl);
    }
}

function renderJournal(dateStr) {
  const data = journalData[dateStr];
  const journalDateEl = document.getElementById('journal-date');
  const dailyLogContent = document.getElementById('daily-log-content');
  
  journalDateEl.textContent = new Date(dateStr + 'T00:00:00').toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  
  if (!data) {
    dailyLogContent.innerHTML = `<div class="text-center py-12"><i data-feather="calendar" class="w-16 h-16 mx-auto text-text-secondary/50"></i><p class="text-text-secondary mt-4">No trades or notes for this day.</p></div>`;
    feather.replace();
    return;
  }

  const totalPnl = data.pnl;
  const wins = data.trades.filter(t => t.win).length;
  const losses = data.trades.length - wins;

  let tradesHtml = data.trades.map(trade => `
    <div class="border-t border-border-color pt-4 mt-4">
      <div class="flex justify-between items-center">
        <div class="font-semibold text-lg">${trade.ticker}</div>
        <div class="font-bold text-lg ${trade.win ? 'text-success' : 'text-danger'}">${trade.pnl.toFixed(2)}</div>
      </div>
      <p class="text-sm text-text-secondary mt-2">${trade.note}</p>
      <div class="grid grid-cols-2 gap-4 mt-4">
        <div>
          <p class="text-xs text-center text-text-secondary mb-1">Before</p>
          <img src="/${trade.before_img}" alt="Before trade" class="rounded-lg shadow-md border border-border-color">
        </div>
        <div>
          <p class="text-xs text-center text-text-secondary mb-1">After</p>
          <img src="/${trade.after_img}" alt="After trade" class="rounded-lg shadow-md border border-border-color">
        </div>
      </div>
    </div>
  `).join('');

  dailyLogContent.innerHTML = `
    <div class="flex justify-between items-start mb-6">
      <h3 class="text-xl font-bold font-display">Daily Log</h3>
      <div class="text-right">
        <div class="text-sm text-text-secondary">Total PNL</div>
        <div class="text-2xl font-bold ${totalPnl >= 0 ? 'text-success' : 'text-danger'}">${totalPnl.toFixed(2)}</div>
      </div>
    </div>
    <div class="flex gap-6 text-sm mb-6 pb-6 border-b border-border-color">
      <div><strong>Total Trades:</strong> ${data.trades.length}</div>
      <div><strong>Wins:</strong> <span class="text-success font-semibold">${wins}</span></div>
      <div><strong>Losses:</strong> <span class="text-danger font-semibold">${losses}</span></div>
    </div>
    <div>
      <h4 class="font-semibold mb-2">Notes</h4>
      <div class="text-text-secondary bg-background p-4 rounded-lg">${data.note}</div>
    </div>
    <div class="mt-6">
       <h4 class="font-semibold mb-4">Trade Reviews</h4>
       ${tradesHtml}
    </div>
  `;
  feather.replace();
}
