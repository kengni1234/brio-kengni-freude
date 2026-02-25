/* Kengni Finance v2.1 - Dashboard Animations */

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', function() {
    initMoneyRain();
    initTradingSignals();
    initStatsAnimation();
});

/**
 * Money Rain Animation - Gold and Silver coins falling
 */
function initMoneyRain() {
    const container = document.createElement('div');
    container.className = 'money-rain-container';
    document.body.appendChild(container);
    
    // Create gold coins
    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            createCoin('gold', container);
        }, i * 800);
    }
    
    // Create silver coins
    for (let i = 0; i < 10; i++) {
        setTimeout(() => {
            createCoin('silver', container);
        }, i * 1200);
    }
    
    // Keep creating coins
    setInterval(() => {
        if (Math.random() > 0.7) {
            createCoin('gold', container);
        }
        if (Math.random() > 0.6) {
            createCoin('silver', container);
        }
    }, 2000);
}

function createCoin(type, container) {
    const coin = document.createElement('div');
    coin.className = type === 'gold' ? 'gold-coin' : 'silver-coin';
    coin.innerHTML = type === 'gold' ? '🪙' : '⚪';
    coin.style.left = Math.random() * 100 + '%';
    coin.style.animationDuration = (5 + Math.random() * 5) + 's';
    coin.style.animationDelay = Math.random() * 2 + 's';
    
    container.appendChild(coin);
    
    // Remove after animation
    setTimeout(() => {
        coin.remove();
    }, parseFloat(coin.style.animationDuration) * 1000 + 2000);
}

/**
 * Trading Signals - Buy/Sell indicators
 */
function initTradingSignals() {
    const container = document.querySelector('.money-rain-container');
    if (!container) return;
    
    setInterval(() => {
        if (Math.random() > 0.5) {
            createTradeSignal(container);
        }
    }, 3000);
}

function createTradeSignal(container) {
    const signal = document.createElement('div');
    const isBuy = Math.random() > 0.5;
    
    signal.className = `trade-signal ${isBuy ? 'buy' : 'sell'}`;
    signal.innerHTML = isBuy ? '📈 BUY' : '📉 SELL';
    signal.style.left = Math.random() * 90 + 5 + '%';
    signal.style.top = Math.random() * 80 + 10 + '%';
    
    container.appendChild(signal);
    
    setTimeout(() => {
        signal.remove();
    }, 3000);
}

/**
 * Stats Cards Animation - Add glow effects
 */
function initStatsAnimation() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
        // Add staggered glow effect
        setTimeout(() => {
            card.classList.add('glow');
        }, index * 200);
        
        // Add gold text to positive values
        const h2 = card.querySelector('h2');
        if (h2 && !h2.textContent.includes('-')) {
            h2.classList.add('gold-text');
        }
    });
}

/**
 * Number Counter Animation
 */
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

/**
 * Add shimmer effect to important elements
 */
function addShimmer() {
    const elements = document.querySelectorAll('.stat-card h2');
    elements.forEach(el => {
        if (!el.classList.contains('shimmer')) {
            el.classList.add('shimmer');
        }
    });
}

/**
 * Trading Chart Enhancements
 */
function enhanceCharts() {
    const charts = document.querySelectorAll('canvas');
    charts.forEach(chart => {
        chart.style.filter = 'drop-shadow(0 0 20px rgba(0, 212, 170, 0.4))';
    });
}

// Initialize enhancements
setTimeout(() => {
    addShimmer();
    enhanceCharts();
}, 1000);

/**
 * Profit/Loss Indicator Animation
 */
function animateProfitIndicators() {
    const indicators = document.querySelectorAll('.change');
    indicators.forEach(indicator => {
        const isPositive = indicator.classList.contains('positive');
        if (isPositive) {
            indicator.style.animation = 'glow 2s ease-in-out infinite';
        }
    });
}

// Run profit indicator animation
setTimeout(animateProfitIndicators, 500);

/**
 * Real-time Clock for Dashboard
 */
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('fr-FR');
    const dateString = now.toLocaleDateString('fr-FR');
    
    const clockElement = document.getElementById('dashboard-clock');
    if (clockElement) {
        clockElement.innerHTML = `
            <div style="font-size: 1.5rem; font-weight: bold; color: #00d4aa;">
                ${timeString}
            </div>
            <div style="font-size: 0.9rem; color: #a8b2d1;">
                ${dateString}
            </div>
        `;
    }
}

// Update clock every second if dashboard page
if (window.location.pathname.includes('dashboard')) {
    setInterval(updateClock, 1000);
    updateClock();
}

/**
 * Toast Notification with Animation
 */
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div style="padding: 15px 25px; background: ${type === 'success' ? '#00d4aa' : '#ff4757'}; 
                    color: white; border-radius: 10px; box-shadow: 0 5px 20px rgba(0,0,0,0.3);
                    position: fixed; top: 20px; right: 20px; z-index: 9999;
                    animation: slideInRight 0.5s ease-out;">
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            ${message}
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.5s ease-out';
        setTimeout(() => toast.remove(), 500);
    }, 3000);
}

// Add slide animations to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Make showToast available globally
window.showToast = showToast;

console.log('✅ Kengni Finance Animations Loaded');
console.log('💰 Money rain active');
console.log('📊 Trading signals active');
console.log('✨ All enhancements loaded');