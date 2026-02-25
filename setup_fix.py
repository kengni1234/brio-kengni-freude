#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kengni Finance v2.1 - Setup and Fix Script
Organizes files, fixes errors, and prepares the application
"""

import os
import shutil
import sys

def setup_project():
    """Setup and organize the project structure"""
    
    print("=" * 70)
    print("🚀 KENGNI FINANCE v2.1 - SETUP & FIX")
    print("=" * 70)
    print()
    
    base_dir = "/home/claude/kengni_finance_v2_complete"
    
    # Step 1: Organize HTML templates
    print("📁 Step 1: Organizing templates...")
    template_files = [
        'ai_assistant.html', 'analysis.html', 'base.html', 'dashboard.html',
        'finance.html', 'finances.html', 'history.html', 'index.html',
        'login.html', 'notifications.html', 'portfolio.html', 'register.html',
        'reports.html', 'settings.html', 'trading.html', 'trading_journal.html'
    ]
    
    templates_dir = os.path.join(base_dir, 'templates')
    
    for template in template_files:
        src = os.path.join(base_dir, template)
        dst = os.path.join(templates_dir, template)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            os.remove(src)
            print(f"  ✅ Moved {template}")
    
    # Step 2: Create verify_token.html template
    print("\n📝 Step 2: Creating verify_token.html template...")
    verify_token_html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vérification - Kengni Finance</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background: linear-gradient(135deg, #0f1419 0%, #1a1a2e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Inter', sans-serif;
        }
        .verify-container {
            background: #1a1a2e;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            max-width: 500px;
            width: 100%;
        }
        .logo {
            text-align: center;
            margin-bottom: 2rem;
        }
        .logo img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 3px solid #00d4aa;
            box-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
        }
        h2 {
            color: #00d4aa;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 700;
        }
        .form-control {
            background: #0f1419;
            border: 2px solid #2d3748;
            color: #ffffff;
            padding: 0.8rem;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            letter-spacing: 10px;
            font-weight: bold;
        }
        .form-control:focus {
            background: #0f1419;
            border-color: #00d4aa;
            color: #ffffff;
            box-shadow: 0 0 0 0.2rem rgba(0, 212, 170, 0.25);
        }
        .btn-verify {
            background: linear-gradient(135deg, #00d4aa, #00ff88);
            border: none;
            color: #0f1419;
            padding: 0.8rem;
            border-radius: 10px;
            font-weight: 600;
            width: 100%;
            margin-top: 1rem;
        }
        .btn-verify:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0, 212, 170, 0.4);
        }
        .btn-resend {
            background: transparent;
            border: 2px solid #00d4aa;
            color: #00d4aa;
            padding: 0.6rem;
            border-radius: 10px;
            font-weight: 600;
            width: 100%;
            margin-top: 1rem;
        }
        .btn-resend:hover {
            background: rgba(0, 212, 170, 0.1);
        }
    </style>
</head>
<body>
    <div class="verify-container">
        <div class="logo">
            <img src="{{ url_for('static', filename='img/logo.jpeg') }}" alt="Kengni Finance">
        </div>
        <h2><i class="fas fa-shield-alt"></i> Vérification</h2>
        
        {% if error %}
        <div class="alert alert-danger">{{ error }}</div>
        {% endif %}
        
        {% if message %}
        <div class="alert alert-success">{{ message }}</div>
        {% endif %}
        
        <div class="alert alert-info">
            <i class="fas fa-envelope"></i> Un code de vérification a été envoyé à<br>
            <strong>{{ email }}</strong>
        </div>
        
        <form method="POST" action="{{ url_for('verify_token_route') }}" id="verifyForm">
            <div class="mb-3">
                <label class="form-label text-white">Code de vérification (6 chiffres)</label>
                <input type="text" class="form-control" name="token" id="tokenInput" 
                       required maxlength="6" pattern="[0-9]{6}" 
                       placeholder="000000" autocomplete="off">
            </div>
            
            <input type="hidden" name="is_registration" value="{{ 'true' if is_registration else 'false' }}">
            
            <button type="submit" class="btn btn-verify">
                <i class="fas fa-check"></i> Vérifier
            </button>
        </form>
        
        <form method="POST" action="{{ url_for('resend_token') }}" id="resendForm">
            <input type="hidden" name="is_registration" value="{{ 'true' if is_registration else 'false' }}">
            <button type="submit" class="btn btn-resend">
                <i class="fas fa-redo"></i> Renvoyer le code
            </button>
        </form>
        
        <div class="text-center mt-3">
            <a href="{{ url_for('login') }}" style="color: #00d4aa; text-decoration: none;">
                ← Retour à la connexion
            </a>
        </div>
        
        <p class="text-center text-muted mt-3">v2.1 - 2FA Enabled</p>
    </div>

    <script>
        // Auto-format token input
        document.getElementById('tokenInput').addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
        
        // Auto-submit when 6 digits entered
        document.getElementById('tokenInput').addEventListener('input', function(e) {
            if (this.value.length === 6) {
                // Optional: auto-submit
                // document.getElementById('verifyForm').submit();
            }
        });
        
        // Handle resend form
        document.getElementById('resendForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            
            try {
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('✅ Code renvoyé! Vérifiez votre email.');
                } else {
                    alert('❌ Erreur lors de l\'envoi du code.');
                }
            } catch (error) {
                alert('❌ Erreur de connexion.');
            }
        });
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'verify_token.html'), 'w', encoding='utf-8') as f:
        f.write(verify_token_html)
    print("  ✅ Created verify_token.html")
    
    # Step 3: Create CSS for animations
    print("\n🎨 Step 3: Creating animated CSS...")
    animated_css = '''/* Kengni Finance v2.1 - Animated Dashboard CSS */

/* Gold and Money Rain Animation */
@keyframes goldRain {
    0% {
        transform: translateY(-100vh) rotate(0deg);
        opacity: 0;
    }
    10% {
        opacity: 1;
    }
    90% {
        opacity: 1;
    }
    100% {
        transform: translateY(100vh) rotate(360deg);
        opacity: 0;
    }
}

@keyframes silverRain {
    0% {
        transform: translateY(-100vh) rotate(0deg);
        opacity: 0;
    }
    10% {
        opacity: 0.8;
    }
    90% {
        opacity: 0.8;
    }
    100% {
        transform: translateY(100vh) rotate(-360deg);
        opacity: 0;
    }
}

@keyframes tradeSignal {
    0%, 100% {
        transform: scale(1);
        opacity: 0.7;
    }
    50% {
        transform: scale(1.2);
        opacity: 1;
    }
}

@keyframes pulse {
    0%, 100% {
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.4);
    }
    50% {
        box-shadow: 0 0 40px rgba(0, 212, 170, 0.8);
    }
}

@keyframes glow {
    0%, 100% {
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    }
    50% {
        text-shadow: 0 0 20px rgba(255, 215, 0, 1);
    }
}

@keyframes shimmer {
    0% {
        background-position: -1000px 0;
    }
    100% {
        background-position: 1000px 0;
    }
}

/* Money Rain Container */
.money-rain-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
    z-index: 1;
}

/* Gold Coins */
.gold-coin {
    position: absolute;
    font-size: 2rem;
    animation: goldRain linear infinite;
    color: gold;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
}

/* Silver Coins */
.silver-coin {
    position: absolute;
    font-size: 1.5rem;
    animation: silverRain linear infinite;
    color: silver;
    text-shadow: 0 0 8px rgba(192, 192, 192, 0.6);
}

/* Trading Signals */
.trade-signal {
    position: absolute;
    font-size: 1.2rem;
    animation: tradeSignal 2s ease-in-out infinite;
}

.trade-signal.buy {
    color: #00ff88;
}

.trade-signal.sell {
    color: #ff4757;
}

/* Glowing Stats */
.stat-card.glow {
    animation: pulse 2s ease-in-out infinite;
}

.stat-card h2.gold-text {
    color: gold;
    animation: glow 2s ease-in-out infinite;
}

/* Shimmer Effect */
.shimmer {
    background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}

/* Dashboard Stats Enhancement */
.stat-card {
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 215, 0, 0.1) 0%, transparent 70%);
    animation: pulse 3s ease-in-out infinite;
    pointer-events: none;
}

/* Profit Indicator */
.profit-indicator {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    animation: glow 1.5s ease-in-out infinite;
}

.profit-indicator.positive {
    background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 212, 170, 0.3));
    color: #00ff88;
}

.profit-indicator.negative {
    background: linear-gradient(135deg, rgba(255, 71, 87, 0.2), rgba(255, 0, 0, 0.3));
    color: #ff4757;
}

/* Trading Chart Glow */
canvas {
    filter: drop-shadow(0 0 10px rgba(0, 212, 170, 0.3));
}

/* Button Animations */
.btn-primary-custom {
    position: relative;
    overflow: hidden;
}

.btn-primary-custom::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transition: left 0.5s;
}

.btn-primary-custom:hover::before {
    left: 100%;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .gold-coin, .silver-coin {
        font-size: 1.5rem;
    }
    
    .trade-signal {
        font-size: 1rem;
    }
}'''
    
    with open(os.path.join(base_dir, 'static/css/animations.css'), 'w', encoding='utf-8') as f:
        f.write(animated_css)
    print("  ✅ Created animations.css")
    
    # Step 4: Create JavaScript for animations
    print("\n⚡ Step 4: Creating animation JavaScript...")
    animated_js = '''/* Kengni Finance v2.1 - Dashboard Animations */

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
console.log('✨ All enhancements loaded');'''
    
    with open(os.path.join(base_dir, 'static/js/animations.js'), 'w', encoding='utf-8') as f:
        f.write(animated_js)
    print("  ✅ Created animations.js")
    
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("📁 Project location: /home/claude/kengni_finance_v2_complete")
    print()
    print("📋 Next steps:")
    print("  1. Install dependencies: pip3 install -r requirements.txt")
    print("  2. Run the application: python3 app.py")
    print("  3. Open browser: http://localhost:5001")
    print()
    print("🎯 Features:")
    print("  ✅ 2FA Email verification")
    print("  ✅ PDF Report generation")
    print("  ✅ Animated dashboard (gold, silver, trading signals)")
    print("  ✅ Delete functions for all entities")
    print("  ✅ Notifications system")
    print()

if __name__ == '__main__':
    setup_project()
