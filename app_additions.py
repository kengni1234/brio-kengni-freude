"""
════════════════════════════════════════════════════════════════════════
  MODIFICATIONS À APPORTER DANS app.py — Boutique
  1. Migration DB (colonne extra_images + rôle shop_manager)
  2. Route /shop/admin — passer all_users + current_role
  3. Route /shop/api/product POST/PUT — inclure extra_images
  4. Routes /shop/api/access/* — gestion des accès boutique
  5. Guard élargi (shop_manager) sur create/update/toggle produit
════════════════════════════════════════════════════════════════════════
"""


# ─────────────────────────────────────────────────────────────────────
# 1.  MIGRATION DB — À ajouter dans init_db() (ou exécuter une fois)
# ─────────────────────────────────────────────────────────────────────

def migrate_shop_db():
    """
    Ajoute les colonnes manquantes si elles n'existent pas déjà.
    Appeler une fois au démarrage, après init_db().
    """
    conn = get_db_connection()
    if not conn: return
    try:
        cur = conn.cursor()

        # Colonne extra_images dans shop_products
        try:
            cur.execute("ALTER TABLE shop_products ADD COLUMN extra_images TEXT DEFAULT '[]'")
            print("[Shop] Colonne extra_images ajoutée")
        except Exception:
            pass  # déjà existante

        # Rôle shop_manager dans users — la colonne 'role' existe déjà,
        # on s'assure juste que la valeur est acceptée (SQLite n'a pas de CHECK alterable)
        # Rien à migrer, le rôle est juste une chaîne de caractères.

        conn.commit()
    except Exception as e:
        print(f"[ShopMigration] {e}")
    finally:
        conn.close()

# Ajoutez dans le bloc __name__ == '__main__' ET dans le bloc else (gunicorn) :
# migrate_shop_db()


# ─────────────────────────────────────────────────────────────────────
# 2.  HELPER — vérifie si l'utilisateur peut gérer la boutique
# ─────────────────────────────────────────────────────────────────────

SHOP_WRITE_ROLES  = ('admin', 'superadmin', 'shop_manager')  # écriture
SHOP_DELETE_ROLES = ('admin', 'superadmin')                   # suppression
SHOP_ADMIN_ROLES  = ('admin', 'superadmin')                   # accès à l'admin


def can_write_shop():
    return session.get('role') in SHOP_WRITE_ROLES

def can_delete_shop():
    return session.get('role') in SHOP_DELETE_ROLES


# ─────────────────────────────────────────────────────────────────────
# 3.  ROUTE /shop/admin — REMPLACE l'existante
# ─────────────────────────────────────────────────────────────────────

@app.route('/shop/admin')
@login_required
def shop_admin():
    role = session.get('role')
    # shop_manager peut accéder mais avec un scope limité
    if role not in ('admin', 'superadmin', 'shop_manager'):
        return redirect(url_for('shop'))

    conn = get_db_connection()
    products, orders, all_users = [], [], []
    total_revenue = pending_count = active_count = 0
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM shop_products ORDER BY created_at DESC")
        products = [dict(r) for r in cur.fetchall()]

        if role in SHOP_ADMIN_ROLES:
            cur.execute("SELECT * FROM shop_orders ORDER BY created_at DESC LIMIT 200")
            orders = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT COALESCE(SUM(total),0) FROM shop_orders WHERE status='paid'")
            total_revenue = cur.fetchone()[0] or 0
            pending_count = sum(1 for o in orders if o['status'] == 'pending')

        # Utilisateurs — uniquement pour superadmin (pour la section Accès)
        if role == 'superadmin':
            cur.execute(
                "SELECT id, username, email, role, status FROM users ORDER BY username"
            )
            all_users = [dict(r) for r in cur.fetchall()]

        active_count = sum(1 for p in products if p['is_active'])

    except Exception as e:
        print(f"[ShopAdmin] {e}")
    finally:
        if conn: conn.close()

    return render_template(
        'shop_admin.html',
        products=products,
        orders=orders,
        total_revenue=total_revenue,
        pending_count=pending_count,
        active_count=active_count,
        all_users=all_users,
        current_role=role,
    )


# ─────────────────────────────────────────────────────────────────────
# 4.  ROUTE /shop/api/product POST — REMPLACE l'existante
#     Accepte maintenant extra_images
# ─────────────────────────────────────────────────────────────────────

@app.route('/shop/api/product', methods=['POST'])
@login_required
def shop_create_product():
    if not can_write_shop():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403

    d = request.get_json(force=True, silent=True) or {}
    name = (d.get('name') or '').strip()
    if not name:
        return jsonify({'success': False, 'error': 'Nom requis'})

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop_products
            (name, description, features, category, price, original_price,
             stock, image_url, extra_images, badge, delivery_info, is_active)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            name,
            d.get('description', ''),
            d.get('features', ''),
            d.get('category', 'electronique'),
            float(d.get('price', 0) or 0),
            float(d.get('original_price', 0) or 0),
            int(d.get('stock', 10)),
            d.get('image_url', ''),
            d.get('extra_images', '[]'),
            d.get('badge', ''),
            d.get('delivery_info', 'Livraison 3-7 jours'),
            1 if d.get('is_active', True) else 0,
        ))
        conn.commit()
        return jsonify({'success': True, 'id': cur.lastrowid})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn: conn.close()


# ─────────────────────────────────────────────────────────────────────
# 5.  ROUTE /shop/api/product/<pid> PUT — REMPLACE l'existante
# ─────────────────────────────────────────────────────────────────────

@app.route('/shop/api/product/<int:pid>', methods=['PUT'])
@login_required
def shop_update_product(pid):
    if not can_write_shop():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403

    d = request.get_json(force=True, silent=True) or {}
    conn = get_db_connection()
    try:
        conn.execute("""
            UPDATE shop_products SET
                name=?, description=?, features=?, category=?,
                price=?, original_price=?, stock=?,
                image_url=?, extra_images=?, badge=?,
                delivery_info=?, is_active=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """, (
            (d.get('name') or '').strip(),
            d.get('description', ''),
            d.get('features', ''),
            d.get('category', 'electronique'),
            float(d.get('price', 0) or 0),
            float(d.get('original_price', 0) or 0),
            int(d.get('stock', 10)),
            d.get('image_url', ''),
            d.get('extra_images', '[]'),
            d.get('badge', ''),
            d.get('delivery_info', 'Livraison 3-7 jours'),
            1 if d.get('is_active', True) else 0,
            pid,
        ))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn: conn.close()


# ─────────────────────────────────────────────────────────────────────
# 6.  ROUTE toggle — REMPLACE l'existante (élargie à shop_manager)
# ─────────────────────────────────────────────────────────────────────

@app.route('/shop/api/product/<int:pid>/toggle', methods=['POST'])
@login_required
def shop_toggle_product(pid):
    if not can_write_shop():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE shop_products SET is_active=1-is_active, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (pid,)
        )
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn: conn.close()


# ─────────────────────────────────────────────────────────────────────
# 7.  ROUTE DELETE — inchangée (réservée admin/superadmin)
# ─────────────────────────────────────────────────────────────────────

@app.route('/shop/api/product/<int:pid>', methods=['DELETE'])
@login_required
def shop_delete_product(pid):
    if not can_delete_shop():
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM shop_products WHERE id=?", (pid,))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn: conn.close()


# ─────────────────────────────────────────────────────────────────────
# 8.  NOUVELLES ROUTES — Gestion des accès boutique
# ─────────────────────────────────────────────────────────────────────

@app.route('/shop/api/access/set', methods=['POST'])
@login_required
def shop_access_set():
    """
    Accorde ou retire le rôle shop_manager à un utilisateur.
    Réservé au superadmin uniquement.
    """
    if session.get('role') != 'superadmin':
        return jsonify({'success': False, 'error': 'Réservé au superadmin'}), 403

    data    = request.get_json(force=True, silent=True) or {}
    user_id = data.get('user_id')
    new_role = data.get('role', 'user')

    # Sécurité : on n'autorise que des transitions sûres
    ALLOWED_ROLES = ('user', 'shop_manager')
    if new_role not in ALLOWED_ROLES:
        return jsonify({'success': False, 'error': 'Rôle non autorisé'}), 400

    if not user_id:
        return jsonify({'success': False, 'error': 'user_id manquant'}), 400

    conn = get_db_connection()
    try:
        # Vérifier que l'utilisateur cible n'est pas admin/superadmin
        row = conn.execute(
            "SELECT role FROM users WHERE id=?", (user_id,)
        ).fetchone()
        if not row:
            return jsonify({'success': False, 'error': 'Utilisateur introuvable'})
        if row['role'] in ('admin', 'superadmin'):
            return jsonify({'success': False, 'error': 'Impossible de modifier un admin'})

        conn.execute(
            "UPDATE users SET role=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (new_role, user_id)
        )
        conn.commit()
        return jsonify({'success': True, 'new_role': new_role})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn: conn.close()


@app.route('/shop/api/access/list')
@login_required
def shop_access_list():
    """Retourne la liste des shop_managers actifs."""
    if session.get('role') != 'superadmin':
        return jsonify({'success': False, 'error': 'Non autorisé'}), 403
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT id, username, email, role FROM users WHERE role='shop_manager' ORDER BY username"
        ).fetchall()
        return jsonify({'success': True, 'managers': [dict(r) for r in rows]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if conn: conn.close()


# ─────────────────────────────────────────────────────────────────────
# 9.  RÉSUMÉ DES CHANGEMENTS À FAIRE DANS app.py
# ─────────────────────────────────────────────────────────────────────
"""
ÉTAPES :

1. Cherchez et REMPLACEZ les fonctions suivantes dans app.py par celles
   de ce fichier (même nom de route) :
   - shop_admin()
   - shop_create_product()
   - shop_update_product()
   - shop_toggle_product()
   - shop_delete_product()

2. AJOUTEZ à la fin du module boutique (avant "if __name__ == '__main__'") :
   - shop_access_set()
   - shop_access_list()
   - migrate_shop_db()

3. AJOUTEZ les helpers can_write_shop() et can_delete_shop() n'importe
   où dans app.py, par exemple juste avant les routes boutique.

4. Dans votre bloc __name__ == '__main__' ET dans le bloc else (gunicorn),
   ajoutez APRÈS init_db() :
       migrate_shop_db()

5. La colonne extra_images sera créée automatiquement au premier démarrage.
   Aucune donnée existante n'est perdue.
"""
