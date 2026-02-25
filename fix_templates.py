#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction - Création automatique de tous les templates HTML manquants
À exécuter AVANT de lancer app.py
"""

import os

def create_all_templates():
    """Create all missing HTML templates"""
    
    # Ensure templates directory exists
    os.makedirs('templates', exist_ok=True)
    
    templates = {
        'base.html': '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Kengni Finance{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        .navbar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .navbar-brand {
            font-size: 24px;
            font-weight: 700;
            text-decoration: none;
            color: white;
        }
        .navbar-menu {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .navbar-menu a {
            color: white;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .navbar-menu a:hover {
            background: rgba(255,255,255,0.2);
        }
        .container {
            max-width: 1400px;
            margin: 30px auto;
            padding: 0 20px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: transform 0.2s;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-success {
            background: #4caf50;
            color: white;
        }
        .btn-danger {
            background: #f44336;
            color: white;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e1e8ed;
        }
        th {
            background: #f5f7fa;
            font-weight: 600;
            color: #333;
        }
        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% if session.user_id %}
    <nav class="navbar">
        <a href="/dashboard" class="navbar-brand">💰 Kengni Finance</a>
        <div class="navbar-menu">
            <a href="/dashboard">📊 Dashboard</a>
            <a href="/finances">💵 Finances</a>
            <a href="/trading">📈 Trading</a>
            <a href="/portfolio">💼 Portfolio</a>
            <a href="/trading-journal">📝 Journal</a>
            <a href="/analysis">🧠 Analyse</a>
            <a href="/settings">⚙️ Paramètres</a>
            <a href="/logout" style="background: rgba(255,255,255,0.2);">Déconnexion</a>
        </div>
    </nav>
    {% endif %}
    
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    
    {% block extra_js %}{% endblock %}
</body>
</html>''',

        'login.html': '''{% extends "base.html" %}
{% block title %}Connexion - Kengni Finance{% endblock %}
{% block content %}
<style>
    .login-box {
        max-width: 450px;
        margin: 100px auto;
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .login-logo {
        text-align: center;
        font-size: 64px;
        margin-bottom: 20px;
    }
    .login-title {
        text-align: center;
        color: #333;
        margin-bottom: 30px;
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #666;
        font-weight: 500;
    }
    .form-group input {
        width: 100%;
        padding: 12px;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        font-size: 16px;
    }
    .form-group input:focus {
        outline: none;
        border-color: #667eea;
    }
</style>

<div class="login-box">
    <div class="login-logo">💰</div>
    <h2 class="login-title">Connexion à Kengni Finance</h2>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST">
        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email" required placeholder="votre@email.com">
        </div>
        <div class="form-group">
            <label>Mot de passe</label>
            <input type="password" name="password" required placeholder="••••••••">
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;">Se connecter</button>
    </form>
    
    <div class="alert alert-info" style="margin-top: 20px;">
        <strong>Compte par défaut:</strong><br>
        Email: fabrice.kengni@icloud.com<br>
        Password: kengni
    </div>
</div>
{% endblock %}''',

        'dashboard.html': '''{% extends "base.html" %}
{% block title %}Dashboard - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">📊 Dashboard</h1>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px;">
    <div class="card">
        <h3 style="color: #666; font-size: 14px; margin-bottom: 10px;">SOLDE TOTAL</h3>
        <div style="font-size: 32px; font-weight: 700; color: #333;">
            {{ "%.2f"|format(stats.total_balance if stats else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px; margin-bottom: 10px;">REVENUS DU MOIS</h3>
        <div style="font-size: 32px; font-weight: 700; color: #4caf50;">
            +{{ "%.2f"|format(stats.monthly_revenue if stats else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px; margin-bottom: 10px;">DÉPENSES DU MOIS</h3>
        <div style="font-size: 32px; font-weight: 700; color: #f44336;">
            -{{ "%.2f"|format(stats.monthly_expenses if stats else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px; margin-bottom: 10px;">POSITIONS OUVERTES</h3>
        <div style="font-size: 32px; font-weight: 700; color: #333;">
            {{ stats.open_positions if stats else 0 }}
        </div>
    </div>
</div>

<div class="card">
    <h2 style="margin-bottom: 20px;">Dernières transactions</h2>
    {% if transactions %}
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Description</th>
                <th>Montant</th>
            </tr>
        </thead>
        <tbody>
            {% for t in transactions[:10] %}
            <tr>
                <td>{{ t.date }}</td>
                <td>{{ t.type }}</td>
                <td>{{ t.reason or t.symbol or '-' }}</td>
                <td style="color: {{ '#4caf50' if t.type == 'revenue' else '#f44336' }};">
                    {{ "%.2f"|format(t.amount) }} €
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune transaction récente</p>
    {% endif %}
</div>
{% endblock %}''',

        'finances.html': '''{% extends "base.html" %}
{% block title %}Finances - Kengni Finance{% endblock %}
{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
    <h1>💵 Gestion Financière</h1>
    <button class="btn btn-primary" onclick="showAddTransactionModal()">➕ Nouvelle transaction</button>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">REVENUS TOTAL</h3>
        <div style="font-size: 28px; font-weight: 700; color: #4caf50;">
            {{ "%.2f"|format(summary.total_revenue if summary else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">DÉPENSES TOTAL</h3>
        <div style="font-size: 28px; font-weight: 700; color: #f44336;">
            {{ "%.2f"|format(summary.total_expenses if summary else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">SOLDE NET</h3>
        <div style="font-size: 28px; font-weight: 700; color: {{ '#4caf50' if (summary.total_revenue - summary.total_expenses) > 0 else '#f44336' }};">
            {{ "%.2f"|format((summary.total_revenue - summary.total_expenses) if summary else 0) }} €
        </div>
    </div>
</div>

<div class="card">
    <h2 style="margin-bottom: 20px;">Historique des transactions</h2>
    {% if transactions %}
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Heure</th>
                <th>Type</th>
                <th>Catégorie</th>
                <th>Raison</th>
                <th>Montant</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            {% for t in transactions %}
            <tr>
                <td>{{ t.date }}</td>
                <td>{{ t.time }}</td>
                <td><span style="padding: 4px 8px; border-radius: 4px; background: {{ '#d4edda' if t.type == 'revenue' else '#f8d7da' }};">{{ t.type }}</span></td>
                <td>{{ t.category }}</td>
                <td>{{ t.reason }}</td>
                <td style="font-weight: 600; color: {{ '#4caf50' if t.type == 'revenue' else '#f44336' }};">
                    {{ '+' if t.type == 'revenue' else '-' }}{{ "%.2f"|format(t.amount) }} €
                </td>
                <td>{{ t.status }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune transaction enregistrée</p>
    {% endif %}
</div>

<script>
function showAddTransactionModal() {
    alert('Modal d\'ajout de transaction à implémenter');
}
</script>
{% endblock %}''',

        'portfolio.html': '''{% extends "base.html" %}
{% block title %}Portfolio - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">💼 Mon Portfolio</h1>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">VALEUR TOTALE</h3>
        <div style="font-size: 28px; font-weight: 700; color: #333;">
            {{ "%.2f"|format(summary.total_value if summary else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">COÛT TOTAL</h3>
        <div style="font-size: 28px; font-weight: 700; color: #666;">
            {{ "%.2f"|format(summary.total_cost if summary else 0) }} €
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">P&L TOTAL</h3>
        <div style="font-size: 28px; font-weight: 700; color: {{ '#4caf50' if (summary.total_pl if summary else 0) >= 0 else '#f44336' }};">
            {{ "%.2f"|format(summary.total_pl if summary else 0) }} €
        </div>
    </div>
</div>

<div class="card">
    <h2 style="margin-bottom: 20px;">Positions ouvertes</h2>
    {% if positions %}
    <table>
        <thead>
            <tr>
                <th>Symbole</th>
                <th>Quantité</th>
                <th>Prix moyen</th>
                <th>Prix actuel</th>
                <th>Valeur</th>
                <th>P&L</th>
                <th>P&L %</th>
            </tr>
        </thead>
        <tbody>
            {% for p in positions %}
            <tr>
                <td><strong>{{ p.symbol }}</strong></td>
                <td>{{ p.quantity }}</td>
                <td>{{ "%.2f"|format(p.avg_price) }} €</td>
                <td>{{ "%.2f"|format(p.current_price) }} €</td>
                <td>{{ "%.2f"|format(p.quantity * p.current_price) }} €</td>
                {% set pl = (p.current_price - p.avg_price) * p.quantity %}
                <td style="color: {{ '#4caf50' if pl >= 0 else '#f44336' }};">
                    {{ "%.2f"|format(pl) }} €
                </td>
                <td style="color: {{ '#4caf50' if pl >= 0 else '#f44336' }};">
                    {{ "%.2f"|format((pl / (p.avg_price * p.quantity) * 100) if p.avg_price > 0 else 0) }}%
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune position ouverte</p>
    {% endif %}
</div>
{% endblock %}''',

        'trading.html': '''{% extends "base.html" %}
{% block title %}Trading - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">📈 Trading</h1>

<div class="card">
    <h2 style="margin-bottom: 20px;">Positions actives</h2>
    {% if positions %}
    <table>
        <thead>
            <tr>
                <th>Symbole</th>
                <th>Type</th>
                <th>Quantité</th>
                <th>Prix d'entrée</th>
                <th>Prix actuel</th>
                <th>Stop Loss</th>
                <th>Take Profit</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for p in positions %}
            <tr>
                <td><strong>{{ p.symbol }}</strong></td>
                <td>{{ p.type or 'LONG' }}</td>
                <td>{{ p.quantity }}</td>
                <td>{{ "%.2f"|format(p.avg_price) }} €</td>
                <td>{{ "%.2f"|format(p.current_price) }} €</td>
                <td>{{ "%.2f"|format(p.stop_loss) if p.stop_loss else '-' }}</td>
                <td>{{ "%.2f"|format(p.take_profit) if p.take_profit else '-' }}</td>
                <td>
                    <button class="btn btn-danger" style="font-size: 12px; padding: 6px 12px;">Fermer</button>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune position active</p>
    {% endif %}
</div>
{% endblock %}''',

        'trading_journal.html': '''{% extends "base.html" %}
{% block title %}Journal de Trading - Kengni Finance{% endblock %}
{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
    <h1>📝 Journal de Trading</h1>
    <button class="btn btn-primary">➕ Nouvelle entrée</button>
</div>

<div class="card">
    <h2 style="margin-bottom: 20px;">Mes entrées</h2>
    {% if entries %}
    <div style="display: grid; gap: 20px;">
        {% for entry in entries %}
        <div style="border: 1px solid #e1e8ed; border-radius: 10px; padding: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <div>
                    <strong style="font-size: 18px;">{{ entry.symbol }}</strong>
                    <span style="margin-left: 10px; color: #666;">{{ entry.date }} {{ entry.time }}</span>
                </div>
                <div style="padding: 4px 12px; border-radius: 4px; background: {{ '#d4edda' if entry.type == 'buy' else '#f8d7da' }};">
                    {{ entry.type.upper() }}
                </div>
            </div>
            <p><strong>Stratégie:</strong> {{ entry.strategy or '-' }}</p>
            <p><strong>Setup:</strong> {{ entry.setup_description or '-' }}</p>
            <p><strong>Émotions:</strong> {{ entry.emotions or '-' }}</p>
            <p><strong>Leçons:</strong> {{ entry.lessons_learned or '-' }}</p>
            {% if entry.profit_loss %}
            <p><strong>P&L:</strong> <span style="color: {{ '#4caf50' if entry.profit_loss >= 0 else '#f44336' }};">{{ "%.2f"|format(entry.profit_loss) }} €</span></p>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune entrée dans le journal</p>
    {% endif %}
</div>
{% endblock %}''',

        'analysis.html': '''{% extends "base.html" %}
{% block title %}Analyse Psychologique - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">🧠 Analyse Psychologique</h1>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px;">
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">SCORE GLOBAL</h3>
        <div style="font-size: 36px; font-weight: 700; color: {{ '#4caf50' if (score.overall_score if score else 0) >= 70 else '#f44336' }};">
            {{ "%.0f"|format(score.overall_score if score else 0) }}/100
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">DISCIPLINE</h3>
        <div style="font-size: 28px; font-weight: 700; color: #667eea;">
            {{ "%.0f"|format(score.discipline_score if score else 0) }}/100
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">GESTION DU RISQUE</h3>
        <div style="font-size: 28px; font-weight: 700; color: #764ba2;">
            {{ "%.0f"|format(score.risk_management_score if score else 0) }}/100
        </div>
    </div>
    <div class="card">
        <h3 style="color: #666; font-size: 14px;">CONTRÔLE ÉMOTIONNEL</h3>
        <div style="font-size: 28px; font-weight: 700; color: #f39c12;">
            {{ "%.0f"|format(score.emotional_control_score if score else 0) }}/100
        </div>
    </div>
</div>

<div class="card">
    <h2 style="margin-bottom: 20px;">Patterns psychologiques détectés</h2>
    {% if patterns %}
    <div style="display: grid; gap: 15px;">
        {% for p in patterns %}
        <div style="border-left: 4px solid {{ '#f44336' if p.severity == 'high' else '#ff9800' if p.severity == 'medium' else '#4caf50' }}; padding: 15px; background: #f5f7fa; border-radius: 5px;">
            <strong>{{ p.pattern_type }}</strong>
            <p style="margin: 8px 0;">{{ p.description }}</p>
            <small style="color: #666;">Fréquence: {{ p.frequency }} fois | Dernière observation: {{ p.last_observed }}</small>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucun pattern détecté pour le moment</p>
    {% endif %}
</div>
{% endblock %}''',

        'settings.html': '''{% extends "base.html" %}
{% block title %}Paramètres - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">⚙️ Paramètres</h1>

<div class="card">
    <h2 style="margin-bottom: 20px;">Informations du compte</h2>
    <form method="POST" action="/api/update-settings">
        <div style="display: grid; gap: 20px;">
            <div>
                <label style="display: block; margin-bottom: 8px; font-weight: 500;">Nom d'utilisateur</label>
                <input type="text" name="username" value="{{ settings.username if settings else '' }}" style="width: 100%; padding: 10px; border: 2px solid #e1e8ed; border-radius: 8px;">
            </div>
            <div>
                <label style="display: block; margin-bottom: 8px; font-weight: 500;">Email</label>
                <input type="email" value="{{ settings.email if settings else '' }}" disabled style="width: 100%; padding: 10px; border: 2px solid #e1e8ed; border-radius: 8px; background: #f5f7fa;">
            </div>
            <div>
                <label style="display: block; margin-bottom: 8px; font-weight: 500;">Devise préférée</label>
                <select name="preferred_currency" style="width: 100%; padding: 10px; border: 2px solid #e1e8ed; border-radius: 8px;">
                    <option value="EUR" {{ 'selected' if (settings.preferred_currency if settings else 'EUR') == 'EUR' else '' }}>EUR (€)</option>
                    <option value="USD" {{ 'selected' if (settings.preferred_currency if settings else '') == 'USD' else '' }}>USD ($)</option>
                    <option value="GBP" {{ 'selected' if (settings.preferred_currency if settings else '') == 'GBP' else '' }}>GBP (£)</option>
                </select>
            </div>
            <div>
                <label style="display: block; margin-bottom: 8px; font-weight: 500;">Thème</label>
                <select name="theme" style="width: 100%; padding: 10px; border: 2px solid #e1e8ed; border-radius: 8px;">
                    <option value="dark" {{ 'selected' if (settings.theme if settings else 'dark') == 'dark' else '' }}>Sombre</option>
                    <option value="light" {{ 'selected' if (settings.theme if settings else '') == 'light' else '' }}>Clair</option>
                </select>
            </div>
            <div style="border-top: 1px solid #e1e8ed; padding-top: 20px;">
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="checkbox" name="notifications_email" {{ 'checked' if (settings.notifications_email if settings else True) else '' }}>
                    Recevoir les notifications par email
                </label>
            </div>
            <div>
                <label style="display: flex; align-items: center; gap: 10px;">
                    <input type="checkbox" name="notifications_app" {{ 'checked' if (settings.notifications_app if settings else True) else '' }}>
                    Recevoir les notifications dans l'application
                </label>
            </div>
        </div>
        <button type="submit" class="btn btn-primary" style="margin-top: 20px;">Sauvegarder les modifications</button>
    </form>
</div>
{% endblock %}''',

        'notifications.html': '''{% extends "base.html" %}
{% block title %}Notifications - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">🔔 Notifications</h1>

<div class="card">
    {% if notifications %}
    <div style="display: grid; gap: 15px;">
        {% for n in notifications %}
        <div style="border-left: 4px solid {{ '#667eea' if n.type == 'info' else '#4caf50' if n.type == 'success' else '#f44336' }}; padding: 15px; background: {{ '#f5f7fa' if n.is_read else 'white' }}; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <strong style="font-size: 16px;">{{ n.title }}</strong>
                    <p style="margin: 8px 0; color: #666;">{{ n.message }}</p>
                    <small style="color: #999;">{{ n.created_at }}</small>
                </div>
                {% if not n.is_read %}
                <button onclick="markAsRead({{ n.id }})" class="btn btn-primary" style="font-size: 12px; padding: 6px 12px;">Marquer comme lu</button>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune notification</p>
    {% endif %}
</div>

<script>
function markAsRead(id) {
    fetch('/api/mark-notification-read/' + id, { method: 'POST' })
        .then(() => location.reload());
}
</script>
{% endblock %}''',

        'reports.html': '''{% extends "base.html" %}
{% block title %}Rapports - Kengni Finance{% endblock %}
{% block content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
    <h1>📋 Rapports Financiers</h1>
    <button class="btn btn-primary">➕ Générer un rapport</button>
</div>

<div class="card">
    <h2 style="margin-bottom: 20px;">Mes rapports</h2>
    {% if reports %}
    <table>
        <thead>
            <tr>
                <th>Titre</th>
                <th>Type</th>
                <th>Période</th>
                <th>Revenus</th>
                <th>Dépenses</th>
                <th>Profit</th>
                <th>Marge</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            {% for r in reports %}
            <tr>
                <td><strong>{{ r.title }}</strong></td>
                <td>{{ r.report_type }}</td>
                <td>{{ r.period_start }} - {{ r.period_end }}</td>
                <td style="color: #4caf50;">{{ "%.2f"|format(r.revenue) }} €</td>
                <td style="color: #f44336;">{{ "%.2f"|format(r.expenses) }} €</td>
                <td style="font-weight: 600; color: {{ '#4caf50' if r.profit >= 0 else '#f44336' }};">
                    {{ "%.2f"|format(r.profit) }} €
                </td>
                <td>{{ "%.1f"|format(r.profit_margin) }}%</td>
                <td>{{ r.created_at[:10] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucun rapport généré</p>
    {% endif %}
</div>
{% endblock %}''',

        'history.html': '''{% extends "base.html" %}
{% block title %}Historique - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">📜 Historique des Transactions</h1>

<div class="card">
    {% if transactions %}
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Symbole</th>
                <th>Type</th>
                <th>Quantité</th>
                <th>Prix</th>
                <th>Montant</th>
                <th>Frais</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            {% for t in transactions %}
            <tr>
                <td>{{ t.created_at[:19] }}</td>
                <td><strong>{{ t.symbol }}</strong></td>
                <td><span style="padding: 4px 8px; border-radius: 4px; background: {{ '#d4edda' if t.type == 'buy' else '#f8d7da' }};">{{ t.type.upper() }}</span></td>
                <td>{{ t.quantity }}</td>
                <td>{{ "%.2f"|format(t.price) }} €</td>
                <td style="font-weight: 600;">{{ "%.2f"|format(t.amount) }} €</td>
                <td>{{ "%.2f"|format(t.fees) }} €</td>
                <td>{{ t.status }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="text-align: center; color: #999; padding: 40px 0;">Aucune transaction dans l'historique</p>
    {% endif %}
</div>
{% endblock %}''',

        'ai_assistant.html': '''{% extends "base.html" %}
{% block title %}Assistant IA - Kengni Finance{% endblock %}
{% block content %}
<h1 style="margin-bottom: 30px;">🤖 Assistant IA</h1>

<div class="card">
    <div id="chat-messages" style="height: 500px; overflow-y: auto; border: 1px solid #e1e8ed; border-radius: 8px; padding: 20px; margin-bottom: 20px; background: #f5f7fa;">
        <p style="text-align: center; color: #999;">Posez-moi vos questions sur vos finances ou votre trading...</p>
    </div>
    
    <div style="display: flex; gap: 10px;">
        <input type="text" id="chat-input" placeholder="Tapez votre message..." style="flex: 1; padding: 12px; border: 2px solid #e1e8ed; border-radius: 8px;" onkeypress="if(event.key==='Enter') sendMessage()">
        <button onclick="sendMessage()" class="btn btn-primary">Envoyer</button>
    </div>
</div>

<script>
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;
    
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML += '<div style="margin: 10px 0; text-align: right;"><span style="background: #667eea; color: white; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%;">' + message + '</span></div>';
    
    input.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Simuler une réponse
    setTimeout(() => {
        chatMessages.innerHTML += '<div style="margin: 10px 0;"><span style="background: white; color: #333; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%; border: 1px solid #e1e8ed;">Je suis en cours de développement. Cette fonctionnalité sera bientôt disponible!</span></div>';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}
</script>
{% endblock %}''',

        'index.html': '''{% extends "base.html" %}
{% block title %}Accueil - Kengni Finance{% endblock %}
{% block content %}
<div style="text-align: center; padding: 100px 20px;">
    <div style="font-size: 80px; margin-bottom: 20px;">💰</div>
    <h1 style="font-size: 48px; margin-bottom: 20px;">Kengni Finance</h1>
    <p style="font-size: 20px; color: #666; margin-bottom: 40px;">Plateforme complète de gestion financière et trading</p>
    <div style="display: flex; gap: 20px; justify-content: center;">
        <a href="/login" class="btn btn-primary" style="font-size: 18px; padding: 15px 30px;">Se connecter</a>
        <a href="/register" class="btn" style="font-size: 18px; padding: 15px 30px; background: white; color: #333; border: 2px solid #e1e8ed;">S'inscrire</a>
    </div>
</div>
{% endblock %}''',

        'register.html': '''{% extends "base.html" %}
{% block title %}Inscription - Kengni Finance{% endblock %}
{% block content %}
<style>
    .register-box {
        max-width: 500px;
        margin: 50px auto;
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-group label {
        display: block;
        margin-bottom: 8px;
        color: #666;
        font-weight: 500;
    }
    .form-group input {
        width: 100%;
        padding: 12px;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        font-size: 16px;
    }
</style>

<div class="register-box">
    <h2 style="text-align: center; margin-bottom: 30px;">Créer un compte</h2>
    
    {% if error %}
    <div class="alert alert-error">{{ error }}</div>
    {% endif %}
    
    <form method="POST">
        <div class="form-group">
            <label>Nom d'utilisateur</label>
            <input type="text" name="username" required>
        </div>
        <div class="form-group">
            <label>Email</label>
            <input type="email" name="email" required>
        </div>
        <div class="form-group">
            <label>Mot de passe</label>
            <input type="password" name="password" required>
        </div>
        <div class="form-group">
            <label>Confirmer le mot de passe</label>
            <input type="password" name="confirm_password" required>
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;">S'inscrire</button>
    </form>
    
    <p style="text-align: center; margin-top: 20px; color: #666;">
        Déjà un compte? <a href="/login" style="color: #667eea;">Se connecter</a>
    </p>
</div>
{% endblock %}'''
    }
    
    # Write all templates
    created_count = 0
    for filename, content in templates.items():
        filepath = os.path.join('templates', filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Créé: {filename}")
            created_count += 1
        else:
            print(f"⏭️  Existe déjà: {filename}")
    
    print(f"\n✅ {created_count} templates créés avec succès!")
    print(f"📁 Total de templates disponibles: {len(templates)}")
    return True

if __name__ == '__main__':
    print("=" * 70)
    print("🔧 Création automatique des templates HTML")
    print("=" * 70)
    print()
    
    create_all_templates()
    
    print()
    print("=" * 70)
    print("✅ TERMINÉ!")
    print("=" * 70)
    print()
    print("Vous pouvez maintenant lancer l'application:")
    print("  python app.py")
    print()
