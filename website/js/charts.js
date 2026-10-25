/* ============================================= */
/*         CHART.JS — All 6 Charts                */
/*         Retail Sales Analytics                 */
/* ============================================= */

// ------ Chart.js Global Defaults for Dark Theme ------ //
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.06)';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(26, 26, 46, 0.95)';
Chart.defaults.plugins.tooltip.titleColor = '#f1f5f9';
Chart.defaults.plugins.tooltip.bodyColor = '#94a3b8';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.cornerRadius = 8;
Chart.defaults.plugins.tooltip.padding = 12;
Chart.defaults.plugins.tooltip.displayColors = true;
Chart.defaults.plugins.tooltip.boxPadding = 4;
Chart.defaults.scale.grid = { color: 'rgba(255, 255, 255, 0.04)' };

// Common color palette
const COLORS = {
    teal:       '#10b981',
    tealLight:  '#34d399',
    blue:       '#3b82f6',
    blueLight:  '#60a5fa',
    purple:     '#8b5cf6',
    purpleLight:'#a78bfa',
    orange:     '#f97316',
    yellow:     '#facc15',
    red:        '#ef4444',
    pink:       '#ec4899',
    cyan:       '#06b6d4',
    emerald:    '#059669',
    indigo:     '#6366f1',
};

const CHART_COLORS = [
    '#10b981', '#3b82f6', '#8b5cf6', '#f97316', '#06b6d4',
    '#ec4899', '#facc15', '#ef4444', '#34d399', '#60a5fa',
    '#a78bfa', '#fb923c', '#22d3ee'
];

// =============================================
// CHART 1: Monthly Sales Trend (Line Chart)
// =============================================
function initMonthlySalesChart() {
    const ctx = document.getElementById('monthlySalesChart');
    if (!ctx) return;

    const months2011 = [120, 95, 140, 150, 170, 190, 180, 200, 230, 250, 160, 370];
    const months2012 = [130, 110, 160, 180, 200, 210, 195, 220, 260, 280, 180, 450];
    const months2013 = [160, 140, 200, 220, 250, 270, 240, 280, 320, 350, 220, 460];
    const months2014 = [190, 170, 240, 260, 300, 320, 280, 340, 400, 430, 270, 600];

    const allData = [...months2011, ...months2012, ...months2013, ...months2014];

    const labels = [];
    const years = ['2011', '2012', '2013', '2014'];
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    years.forEach(y => {
        monthNames.forEach(m => {
            labels.push(`${m} ${y}`);
        });
    });

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Monthly Sales ($K)',
                data: allData,
                borderColor: COLORS.teal,
                backgroundColor: 'rgba(16, 185, 129, 0.08)',
                fill: true,
                tension: 0.4,
                pointRadius: 1.5,
                pointHoverRadius: 6,
                pointBackgroundColor: COLORS.teal,
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: COLORS.teal,
                pointHoverBorderWidth: 2,
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Sales: $${context.parsed.y}K`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 12,
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => `$${v}K`
                    }
                }
            }
        }
    });
}

// =============================================
// CHART 2: Category Sales vs Profit (Grouped Bar)
// =============================================
function initCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Furniture', 'Office Supplies', 'Technology'],
            datasets: [
                {
                    label: 'Sales',
                    data: [4110874, 3787070, 4744557],
                    backgroundColor: 'rgba(16, 185, 129, 0.7)',
                    borderColor: COLORS.teal,
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.7,
                    categoryPercentage: 0.6,
                },
                {
                    label: 'Profit',
                    data: [285205, 518474, 663779],
                    backgroundColor: 'rgba(59, 130, 246, 0.7)',
                    borderColor: COLORS.blue,
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.7,
                    categoryPercentage: 0.6,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: $${(context.parsed.y / 1e6).toFixed(2)}M`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => `$${(v / 1e6).toFixed(1)}M`
                    }
                }
            }
        }
    });
}

// =============================================
// CHART 3: Sales by Region (Doughnut)
// =============================================
function initRegionChart() {
    const ctx = document.getElementById('regionChart');
    if (!ctx) return;

    const regionLabels = [
        'Central', 'South', 'North', 'Oceania', 'Southeast Asia',
        'North Asia', 'EMEA', 'Africa', 'Central Asia', 'West',
        'East', 'Caribbean', 'Canada'
    ];
    const regionData = [
        2822303, 1600907, 1248166, 1100185, 884423,
        848310, 806161, 783773, 752827, 725458,
        678781, 324281, 66929
    ];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: regionLabels,
            datasets: [{
                data: regionData,
                backgroundColor: CHART_COLORS,
                borderColor: 'rgba(26, 26, 46, 0.8)',
                borderWidth: 2,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '55%',
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: { size: 11 },
                        padding: 10,
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((context.parsed / total) * 100).toFixed(1);
                            return `${context.label}: $${(context.parsed / 1e6).toFixed(2)}M (${pct}%)`;
                        }
                    }
                }
            }
        }
    });
}

// =============================================
// CHART 4: Profit Margin by Discount Band (Bar)
// =============================================
function initDiscountChart() {
    const ctx = document.getElementById('discountChart');
    if (!ctx) return;

    const discountData = [25.3, 17.2, 9.9, -17.3, -74.1];
    const discountColors = [
        '#10b981',  // Green for 0%
        '#34d399',  // Light green for 1-10%
        '#facc15',  // Yellow for 11-20%
        '#f97316',  // Orange for 21-40%
        '#ef4444',  // Red for 40%+
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['0%', '1–10%', '11–20%', '21–40%', '40%+'],
            datasets: [{
                label: 'Profit Margin',
                data: discountData,
                backgroundColor: discountColors.map(c => c + 'CC'),
                borderColor: discountColors,
                borderWidth: 1,
                borderRadius: 6,
                barPercentage: 0.7,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Margin: ${context.parsed.y}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        callback: v => `${v}%`
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Discount Band',
                        color: '#64748b',
                    }
                }
            }
        }
    });
}

// =============================================
// CHART 5: Yearly Sales Growth (Bar)
// =============================================
function initYearlyGrowthChart() {
    const ctx = document.getElementById('yearlyGrowthChart');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['2011', '2012', '2013', '2014'],
            datasets: [{
                label: 'Annual Sales',
                data: [2259451, 2677439, 3405746, 4299866],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.5)',
                    'rgba(16, 185, 129, 0.6)',
                    'rgba(16, 185, 129, 0.75)',
                    'rgba(16, 185, 129, 0.9)',
                ],
                borderColor: COLORS.teal,
                borderWidth: 1,
                borderRadius: 8,
                barPercentage: 0.6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Sales: $${(context.parsed.y / 1e6).toFixed(2)}M`;
                        },
                        afterLabel: function(context) {
                            const growth = [null, '18.5%', '27.2%', '26.3%'];
                            if (growth[context.dataIndex]) {
                                return `Growth: +${growth[context.dataIndex]}`;
                            }
                            return '';
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => `$${(v / 1e6).toFixed(1)}M`
                    }
                }
            }
        }
    });
}

// =============================================
// CHART 6: Sales Forecast 2015 (Line, dashed)
// =============================================
function initForecastChart() {
    const ctx = document.getElementById('forecastChart');
    if (!ctx) return;

    // Historical (last 6 months of 2014) + Forecast (first 6 months of 2015)
    const labels = [
        'Jul 2014', 'Aug 2014', 'Sep 2014', 'Oct 2014', 'Nov 2014', 'Dec 2014',
        'Jan 2015', 'Feb 2015', 'Mar 2015', 'Apr 2015', 'May 2015', 'Jun 2015'
    ];

    const historicalData = [280, 340, 400, 430, 270, 600, null, null, null, null, null, null];
    const forecastData   = [null, null, null, null, null, 600, 362, 321, 378, 363, 420, 518];

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Historical Sales ($K)',
                    data: historicalData,
                    borderColor: COLORS.teal,
                    backgroundColor: 'rgba(16, 185, 129, 0.08)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: COLORS.teal,
                    pointHoverRadius: 7,
                    borderWidth: 2.5,
                },
                {
                    label: 'Forecast 2015 ($K)',
                    data: forecastData,
                    borderColor: COLORS.blue,
                    backgroundColor: 'rgba(59, 130, 246, 0.06)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 5,
                    pointBackgroundColor: COLORS.blue,
                    pointHoverRadius: 7,
                    borderWidth: 2.5,
                    borderDash: [8, 4],
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (context.parsed.y === null) return '';
                            return `${context.dataset.label}: $${context.parsed.y}K`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: v => `$${v}K`
                    }
                }
            }
        }
    });
}

// =============================================
// Initialize All Charts
// =============================================
function initAllCharts() {
    initMonthlySalesChart();
    initCategoryChart();
    initRegionChart();
    initDiscountChart();
    initYearlyGrowthChart();
    initForecastChart();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initAllCharts);
