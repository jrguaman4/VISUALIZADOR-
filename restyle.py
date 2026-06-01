import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_css = """
    /* ── RESET & ROOT ─────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    :root {
      --violet-800: #5b21b6;
      --violet-700: #6d28d9;
      --violet-600: #7c3aed;
      --violet-500: #8b5cf6;
      --violet-400: #a78bfa;
      --violet-100: #ede9fe;
      --white: #ffffff;
      --text-main: #1e293b;
      --muted: #64748b;
      --border: rgba(255, 255, 255, 0.6);
      --glass-bg: rgba(255, 255, 255, 0.55);
      --glass-hover: rgba(255, 255, 255, 0.8);
      --card-bg: rgba(255, 255, 255, 0.45);
      --sidebar-w: 280px;
      --hdr-h: 70px;
      --radius: 24px;
      --trans: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      --shadow: 0 10px 40px -10px rgba(139, 92, 246, 0.15);
      --shadow-hover: 0 16px 50px -12px rgba(139, 92, 246, 0.25);
      --shadow-inner: inset 0 2px 4px 0 rgba(255, 255, 255, 0.5);
    }

    body {
      font-family: 'Outfit', 'Segoe UI', sans-serif;
      background: #f1f5f9;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(139, 92, 246, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 50% 100%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
        url('data:image/svg+xml;utf8,<svg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><circle cx="2" cy="2" r="1" fill="rgba(139,92,246,0.05)"/></svg>');
      color: var(--text-main);
      min-height: 100vh;
      overflow-x: hidden;
    }

    #app { display: flex; height: 100vh; position: relative; z-index: 1; }

    /* ── SIDEBAR ─────────────────────────────── */
    #sidebar {
      width: var(--sidebar-w);
      min-width: var(--sidebar-w);
      background: rgba(255, 255, 255, 0.4);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: transform var(--trans);
      z-index: 100;
      box-shadow: 10px 0 30px -10px rgba(0,0,0,0.02);
    }

    .sidebar-header { padding: 26px 24px 20px; border-bottom: 1px solid var(--border); }

    .sidebar-logo { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }

    .logo-icon {
      width: 44px; height: 44px;
      background: linear-gradient(135deg, var(--violet-400), var(--violet-600));
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      font-size: 24px; flex-shrink: 0;
      color: white;
      box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3), var(--shadow-inner);
    }

    .logo-text { line-height: 1.2; }
    .logo-text strong { font-size: 15px; font-weight: 800; color: var(--violet-800); letter-spacing: 0.2px; display: block; }
    .logo-text span { font-size: 11px; color: var(--muted); font-weight: 500; }

    .sidebar-subtitle {
      font-size: 11px; color: var(--violet-600); font-weight: 600; margin-top: 8px;
      padding-top: 8px; border-top: 1px dashed var(--border);
    }

    .nav-section-label {
      font-size: 10px; font-weight: 800; letter-spacing: 1.5px;
      color: var(--muted); padding: 18px 24px 8px; text-transform: uppercase;
    }

    .nav-item {
      display: flex; align-items: center; gap: 12px;
      padding: 12px 24px; cursor: pointer; color: var(--text-main);
      font-size: 13.5px; font-weight: 500; transition: all var(--trans);
      border-left: 4px solid transparent; user-select: none;
      margin: 4px 12px; border-radius: 12px; border-left: none;
    }
    .nav-item:hover { background: var(--glass-bg); box-shadow: var(--shadow); transform: translateX(4px); }
    .nav-item.active { background: var(--white); color: var(--violet-700); box-shadow: var(--shadow); font-weight: 700; }
    .nav-item .nav-icon { font-size: 16px; width: 22px; text-align: center; }
    .nav-item .nav-badge {
      margin-left: auto;
      background: var(--violet-100); color: var(--violet-700);
      font-size: 11px; font-weight: 800; padding: 2px 8px;
      border-radius: 20px; box-shadow: var(--shadow-inner);
    }
    .nav-item.active .nav-badge { background: var(--violet-600); color: white; }

    /* ── SIDEBAR TOGGLE ────── */
    #sidebar-toggle {
      display: flex; align-items: center; justify-content: center;
      width: 40px; height: 40px; border-radius: 12px;
      border: 1px solid var(--border); background: var(--glass-bg);
      cursor: pointer; flex-shrink: 0; transition: all var(--trans);
      color: var(--violet-600); font-size: 18px;
      backdrop-filter: blur(10px);
    }
    #sidebar-toggle:hover { background: var(--white); box-shadow: var(--shadow); transform: translateY(-2px); }

    #sidebar.collapsed { width: 0; min-width: 0; overflow: hidden; border: none; }

    /* ── ACORDEÓN DEPENDENCIAS ───────────── */
    .nav-group { overflow: visible; margin: 0 12px; }

    .nav-group-header {
      display: flex; align-items: center; gap: 10px;
      padding: 12px 16px; cursor: pointer; color: var(--text-main);
      font-size: 13.5px; font-weight: 600; transition: all var(--trans);
      border-radius: 12px; user-select: none; background: transparent;
    }
    .nav-group-header:hover { background: var(--glass-bg); }
    .nav-group-header.open { color: var(--violet-700); background: var(--white); box-shadow: var(--shadow); }

    .nav-group-header .nav-icon { font-size: 16px; width: 22px; text-align: center; }
    .nav-group-header .nav-label { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .nav-group-header .nav-count { font-size: 11px; color: var(--violet-600); font-weight: 800; margin-right: 6px; background: var(--violet-100); padding: 2px 8px; border-radius: 20px;}

    .nav-chevron { font-size: 10px; color: var(--muted); transition: transform 0.3s cubic-bezier(0.4,0,0.2,1); flex-shrink: 0; }
    .nav-group-header.open .nav-chevron { transform: rotate(180deg); color: var(--violet-600); }

    .nav-group-body {
      max-height: 0; overflow: hidden; transition: max-height 0.4s cubic-bezier(0.4,0,0.2,1);
    }
    .nav-group-body.open {
      max-height: calc(100vh - 250px); overflow-y: auto; overflow-x: hidden;
      margin-top: 4px; padding-bottom: 8px;
    }
    .nav-group-body::-webkit-scrollbar { width: 4px; }
    .nav-group-body::-webkit-scrollbar-track { background: transparent; }
    .nav-group-body::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.2); border-radius: 99px; }
    .nav-group-body::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 246, 0.4); }

    .nav-sub-item {
      display: flex; align-items: center; gap: 10px;
      padding: 10px 16px 10px 24px; cursor: pointer; color: var(--muted);
      font-size: 12.5px; font-weight: 500; transition: all var(--trans);
      border-radius: 10px; margin: 2px 8px; user-select: none;
    }
    .nav-sub-item:hover { background: rgba(255,255,255,0.4); color: var(--violet-600); transform: translateX(4px); }
    .nav-sub-item.active { background: var(--white); color: var(--violet-700); box-shadow: 0 4px 10px rgba(0,0,0,0.03); font-weight: 700; }
    .nav-sub-item .sub-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--muted); flex-shrink: 0; transition: all var(--trans); }
    .nav-sub-item:hover .sub-dot { background: var(--violet-400); transform: scale(1.5); }
    .nav-sub-item.active .sub-dot { background: var(--violet-600); transform: scale(1.5); box-shadow: 0 0 8px var(--violet-400); }
    
    .nav-sub-item .sub-badge {
      margin-left: auto; background: var(--white); color: var(--violet-600);
      font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 20px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid var(--border);
    }
    .nav-sub-item.active .sub-badge { background: var(--violet-100); color: var(--violet-800); border: none; }

    .sidebar-footer {
      margin-top: auto; padding: 20px 24px;
      border-top: 1px solid var(--border); background: rgba(255,255,255,0.2);
      font-size: 11px; color: var(--muted); line-height: 1.6; font-weight: 500;
    }

    /* ── MAIN ────────────────────────────────── */
    #main { flex: 1; display: flex; flex-direction: column; overflow: hidden; }

    #topbar {
      height: var(--hdr-h); min-height: var(--hdr-h);
      background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; padding: 0 32px; gap: 20px;
      box-shadow: 0 4px 20px -10px rgba(0,0,0,0.05); z-index: 90;
    }
    #topbar h1 { font-size: 18px; font-weight: 800; color: var(--text-main); letter-spacing: 0.2px; flex: 1; display: flex; align-items: center; gap: 8px;}
    #topbar h1 span { color: var(--violet-600); background: var(--violet-100); padding: 4px 12px; border-radius: 20px; font-size: 15px;}
    .topbar-actions { display: flex; align-items: center; gap: 14px; }

    .btn {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 10px 20px; border-radius: 14px;
      font-size: 13px; font-weight: 700; cursor: pointer;
      border: 1px solid transparent; transition: all var(--trans);
      font-family: 'Outfit', sans-serif;
    }
    .btn-gold { background: linear-gradient(135deg, var(--violet-500), var(--violet-700)); color: white; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3), var(--shadow-inner); }
    .btn-gold:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4), var(--shadow-inner); }
    .btn-outline { background: var(--white); border: 1px solid var(--border); color: var(--violet-700); box-shadow: var(--shadow); }
    .btn-outline:hover { border-color: var(--violet-400); transform: translateY(-2px); box-shadow: var(--shadow-hover); }

    /* Chip filtro activo */
    #filter-chip {
      display: none; align-items: center; gap: 8px;
      background: var(--white); border: 1px solid var(--violet-200);
      border-radius: 20px; padding: 6px 14px;
      font-size: 12px; font-weight: 700; color: var(--violet-700);
      box-shadow: var(--shadow);
    }
    #filter-chip.show { display: flex; animation: slideIn 0.3s ease; }
    #filter-chip button {
      background: var(--violet-100); border: none; color: var(--violet-700);
      cursor: pointer; font-size: 14px; line-height: 1; padding: 2px 6px; border-radius: 50%; transition: all 0.2s;
    }
    #filter-chip button:hover { background: var(--violet-600); color: white; }

    @keyframes slideIn { from { opacity: 0; transform: translateX(10px); } to { opacity: 1; transform: translateX(0); } }

    .search-wrap { position: relative; }
    .search-wrap input {
      background: var(--white); border: 1px solid var(--border);
      border-radius: 16px; color: var(--text-main); font-weight: 500;
      font-size: 13px; padding: 10px 16px 10px 40px; outline: none;
      width: 220px; transition: all var(--trans);
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
      font-family: 'Outfit', sans-serif;
    }
    .search-wrap input:focus { border-color: var(--violet-400); width: 280px; box-shadow: 0 0 0 4px var(--violet-100); }
    .search-wrap input::placeholder { color: var(--muted); font-weight: 400;}
    .search-icon {
      position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
      color: var(--violet-500); font-size: 16px; pointer-events: none;
    }

    #content { flex: 1; overflow-y: auto; padding: 32px; }

    .view { display: none; animation: fadeIn 0.4s ease; }
    .view.active { display: block; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    /* ── DASHBOARD ────────────────────────────── */
    .dash-title {
      font-size: 14px; font-weight: 800; letter-spacing: 1px;
      text-transform: uppercase; color: var(--violet-700);
      margin-bottom: 24px; display: flex; align-items: center; gap: 10px;
    }
    .dash-title::before {
      content: '✨'; font-size: 18px;
    }

    /* KPI cards clicables */
    .kpi-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 20px; margin-bottom: 32px; }

    .kpi-card {
      background: var(--glass-bg); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 24px 20px;
      backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      position: relative; overflow: hidden;
      transition: all var(--trans); cursor: pointer;
      box-shadow: var(--shadow);
    }
    .kpi-card:hover { transform: translateY(-5px) scale(1.02); border-color: var(--violet-300); box-shadow: var(--shadow-hover); background: var(--glass-hover); }
    .kpi-card.active-filter { border-color: var(--violet-500); box-shadow: 0 0 0 3px var(--violet-100), var(--shadow-hover); background: var(--white); }
    
    .kpi-card .kpi-hint {
      position: absolute; bottom: 12px; right: 16px;
      font-size: 10px; color: var(--muted); font-weight: 600;
      background: rgba(0,0,0,0.04); padding: 4px 8px; border-radius: 12px;
    }
    .kpi-num   { font-size: 42px; font-weight: 800; color: var(--violet-800); line-height: 1; text-shadow: 2px 2px 4px rgba(0,0,0,0.05); }
    .kpi-label { font-size: 12px; color: var(--muted); margin-top: 8px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
    .kpi-icon  { position: absolute; right: -10px; top: -10px; font-size: 70px; opacity: 0.1; filter: grayscale(0.5); transform: rotate(15deg); transition: all 0.3s;}
    .kpi-card:hover .kpi-icon { transform: rotate(0deg) scale(1.1); opacity: 0.2; filter: grayscale(0); }

    /* Grid 2 cols */
    .dash-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px; }

    .dash-card {
      background: var(--glass-bg); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 24px; backdrop-filter: blur(16px);
      box-shadow: var(--shadow);
    }
    .dash-card-title {
      font-size: 13px; font-weight: 800; letter-spacing: 1px;
      text-transform: uppercase; color: var(--violet-700);
      margin-bottom: 20px; border-bottom: 2px solid var(--border); padding-bottom: 12px;
      display: flex; align-items: center; justify-content: space-between;
    }

    /* Filas de estadística con barra */
    .stat-row {
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 12px; border-bottom: 1px dashed var(--border); font-size: 13px;
      cursor: pointer; border-radius: 12px; transition: all var(--trans);
      background: transparent; margin-bottom: 4px;
    }
    .stat-row:hover { background: var(--white); transform: translateX(5px); box-shadow: 0 4px 10px rgba(0,0,0,0.03); border-bottom-color: transparent;}
    .stat-row.active-filter { background: var(--violet-100); border-bottom-color: transparent; }
    .stat-row:last-child { border: none; }
    .stat-row .label { color: var(--text-main); font-weight: 600; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-right: 12px; }
    .stat-row .val   { color: var(--violet-800); font-weight: 800; font-size: 14px; background: var(--white); padding: 2px 10px; border-radius: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    .bar-wrap { display: flex; align-items: center; gap: 12px; flex: 1; }
    .bar-bg   { flex: 1; height: 8px; background: rgba(0,0,0,0.04); border-radius: 99px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); }
    .bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--violet-400), var(--violet-600)); transition: width 1s cubic-bezier(.22,.68,0,1.2); box-shadow: inset 0 2px 4px rgba(255,255,255,0.4); }

    /* ── TABLA GRUPOS (numérica) ────────────── */
    .grupos-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 16px;
    }

    .grupo-kpi {
      background: var(--white); border: 1px solid var(--border);
      border-radius: 16px; padding: 16px;
      display: flex; flex-direction: column; gap: 6px;
      cursor: pointer; transition: all var(--trans);
      box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    .grupo-kpi:hover { border-color: var(--violet-300); transform: translateY(-3px); box-shadow: var(--shadow); }
    .grupo-kpi.active-filter { border-color: var(--violet-500); box-shadow: 0 0 0 3px var(--violet-100); }
    .grupo-kpi .gk-num   { font-size: 32px; font-weight: 800; color: var(--violet-700); line-height: 1; }
    .grupo-kpi .gk-label { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 700;}
    .grupo-kpi .gk-hint  { font-size: 10px; color: var(--violet-400); font-weight: 600; margin-top: auto; }

    /* Tabla grupos por dependencia */
    .grp-tbl { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 12px; margin-top: 10px; }
    .grp-tbl th {
      padding: 12px 10px; text-align: center;
      font-size: 10px; font-weight: 800; letter-spacing: 1px;
      text-transform: uppercase; color: var(--violet-600);
      border-bottom: 2px solid var(--border); white-space: nowrap;
    }
    .grp-tbl th:first-child { text-align: left; }
    .grp-tbl td {
      padding: 10px; border-bottom: 1px dashed rgba(0,0,0,0.05);
      text-align: center; color: var(--text-main); font-weight: 500;
    }
    .grp-tbl td:first-child { text-align: left; color: var(--muted); font-weight: 600; font-size: 12px; }
    .grp-tbl tr:hover td { background: rgba(255,255,255,0.5); }
    .grp-tbl tr:last-child td { border: none; }
    .grp-tbl tr.total-row td { border-top: 2px solid var(--border); color: var(--violet-800); font-weight: 800; padding-top: 14px; }
    .grp-tbl td .cell-val { display: inline-flex; align-items: center; justify-content: center; min-width: 28px; }
    .grp-tbl td .cell-val.nonzero {
      background: var(--violet-100); border-radius: 8px;
      padding: 2px 8px; color: var(--violet-700); font-weight: 800;
    }
    .grp-tbl td .cell-val.zero { color: var(--muted); opacity: 0.4; }

    /* ── TABLA TODAS LAS DEPENDENCIAS ──────── */
    .all-deps-section { margin-top: 16px; }
    .all-deps-header {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 20px;
    }

    /* ── TABLA PERSONAL ──────────────────── */
    .table-wrap {
      background: var(--glass-bg); border: 1px solid var(--border);
      border-radius: var(--radius); overflow: hidden; backdrop-filter: blur(16px);
      box-shadow: var(--shadow);
    }
    .table-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 20px 24px; border-bottom: 1px solid var(--border);
      background: rgba(255,255,255,0.4);
    }
    .table-header-title { font-size: 15px; font-weight: 800; color: var(--violet-800); text-transform: uppercase; letter-spacing: 0.5px;}
    .table-header-sub   { font-size: 12px; color: var(--muted); margin-top: 4px; font-weight: 600;}
    .tbl-scroll { overflow-x: auto; padding: 0 10px 10px 10px; }

    table { width: 100%; border-collapse: separate; border-spacing: 0 6px; font-size: 13px; }
    thead tr { background: transparent; }
    thead th {
      padding: 14px 16px; text-align: left;
      font-size: 11px; font-weight: 800; letter-spacing: 1px;
      text-transform: uppercase; color: var(--muted); white-space: nowrap;
      border-bottom: 2px solid var(--border);
    }
    tbody tr { background: var(--white); transition: all var(--trans); box-shadow: 0 2px 8px rgba(0,0,0,0.02); border-radius: 12px;}
    tbody tr td:first-child { border-top-left-radius: 12px; border-bottom-left-radius: 12px; }
    tbody tr td:last-child { border-top-right-radius: 12px; border-bottom-right-radius: 12px; }
    tbody tr:hover { transform: translateY(-2px); box-shadow: 0 8px 15px rgba(139, 92, 246, 0.08); z-index: 10; position: relative;}
    tbody td { padding: 14px 16px; color: var(--text-main); vertical-align: middle; }

    /* Celda de nombres: GRADO primero */
    .cell-grado  { font-size: 10px; font-weight: 800; color: var(--violet-500); letter-spacing: 0.8px; text-transform: uppercase; background: var(--violet-100); display: inline-block; padding: 2px 8px; border-radius: 20px;}
    .cell-nombre { font-weight: 700; font-size: 14px; margin-top: 6px; color: var(--text-main); display: flex; align-items: center; gap: 8px;}
    .cell-nombre::before { content: '🧑‍✈️'; font-size: 18px; }
    .cell-cargo  { font-size: 12px; color: var(--muted); font-weight: 500;}
    .cell-dep    { font-size: 12px; color: var(--violet-700); font-weight: 600;}

    .novedad-badge {
      display: inline-block; padding: 4px 10px; border-radius: 8px;
      font-size: 11px; font-weight: 700;
      background: #fef3c7; color: #d97706;
      border: 1px solid #fde68a;
      max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }
    .novedad-badge.empty { opacity: 0.4; background: #f1f5f9; color: var(--muted); border-color: #e2e8f0;}

    .estado-select {
      background: var(--white); border: 2px solid var(--border);
      border-radius: 10px; color: var(--text-main); font-size: 12px; font-weight: 700;
      padding: 6px 12px; cursor: pointer; outline: none;
      transition: all var(--trans); min-width: 160px;
      font-family: 'Outfit', sans-serif;
      box-shadow: 0 2px 5px rgba(0,0,0,0.02);
      appearance: none;
      background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%2364748b%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
      background-repeat: no-repeat, repeat;
      background-position: right .7em top 50%, 0 0;
      background-size: .65em auto, 100%;
    }
    .estado-select:hover, .estado-select:focus { border-color: var(--violet-400); box-shadow: 0 0 0 3px var(--violet-100); }
    .estado-select.PRESENTE          { color: #059669; background-color: #d1fae5; border-color: #a7f3d0; }
    .estado-select.FRANCO            { color: #2563eb; background-color: #dbeafe; border-color: #bfdbfe; }
    .estado-select.LICENCIA          { color: #d97706; background-color: #fef3c7; border-color: #fde68a; }
    .estado-select.VACACIONES        { color: #7c3aed; background-color: #ede9fe; border-color: #ddd6fe; }
    .estado-select.TRASLADO-TEMPORAL { color: #ea580c; background-color: #ffedd5; border-color: #fed7aa; }
    .estado-select.DESCANSO-MEDICO   { color: #e11d48; background-color: #ffe4e6; border-color: #fecdd3; }
    .estado-select.SERVICIO          { color: #0284c7; background-color: #e0f2fe; border-color: #bae6fd; }

    .save-btn {
      background: linear-gradient(135deg, var(--violet-500), var(--violet-700)); border: none; border-radius: 10px;
      color: white; font-size: 11px; font-weight: 800;
      padding: 8px 14px; cursor: pointer; transition: all var(--trans);
      letter-spacing: 0.5px; box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
      font-family: 'Outfit', sans-serif;
    }
    .save-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(139, 92, 246, 0.4); }
    .save-btn:disabled { opacity: 0.5; cursor: default; transform: none; box-shadow: none; background: var(--muted); }
    .save-btn.saved { background: #10b981; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); }

    .grupo-pill {
      display: inline-block; padding: 4px 12px; border-radius: 20px;
      font-size: 11px; font-weight: 800;
      background: var(--violet-100); color: var(--violet-700);
      border: 1px solid var(--violet-200); white-space: nowrap;
    }

    /* ── VISTA DEPENDENCIA ─────────────────────── */
    .dep-header {
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 24px; gap: 16px; flex-wrap: wrap;
    }
    .dep-header-left { display: flex; align-items: center; gap: 16px; }
    .dep-header-icon {
      font-size: 32px; width: 64px; height: 64px;
      background: var(--white); border: 2px solid var(--violet-100);
      border-radius: 20px; display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; box-shadow: var(--shadow);
    }
    .dep-header-title { font-size: 22px; font-weight: 800; color: var(--violet-800); }
    .dep-header-sub   { font-size: 13px; color: var(--muted); margin-top: 4px; font-weight: 600; }

    /* KPI row de dependencia */
    .dep-kpi-row {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(140px,1fr));
      gap: 16px; margin-bottom: 24px;
    }
    .dep-kpi {
      background: var(--white); border: 1px solid var(--border);
      border-radius: 16px; padding: 16px; position: relative; overflow: hidden;
      cursor: pointer; transition: all var(--trans); box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    .dep-kpi:hover { border-color: var(--violet-300); transform: translateY(-3px); box-shadow: var(--shadow); }
    .dep-kpi.active-filter { border-color: var(--violet-500); box-shadow: 0 0 0 3px var(--violet-100); }
    .dep-kpi .dk-num   { font-size: 28px; font-weight: 800; color: var(--violet-700); line-height: 1; margin-bottom: 6px;}
    .dep-kpi .dk-label { font-size: 10px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 700;}
    .dep-kpi .dk-icon  { position: absolute; right: 12px; top: 12px; font-size: 24px; opacity: 0.15; filter: grayscale(1); }

    /* Secciones de dependencia */
    .dep-section {
      background: var(--glass-bg); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 20px 24px;
      margin-bottom: 20px; backdrop-filter: blur(16px); box-shadow: var(--shadow);
    }
    .dep-section-title {
      font-size: 12px; font-weight: 800; letter-spacing: 1px;
      text-transform: uppercase; color: var(--violet-700); margin-bottom: 16px;
    }

    /* Novedades */
    .dep-novedades-list { display: flex; flex-wrap: wrap; gap: 12px; }
    .novedad-item {
      display: flex; align-items: center; gap: 10px;
      background: #fffbeb; border: 1px solid #fde68a;
      border-radius: 12px; padding: 10px 16px; font-size: 12px; max-width: 380px;
      box-shadow: 0 2px 8px rgba(217, 119, 6, 0.1);
    }
    .novedad-item .ni-nombre { font-weight: 800; color: #b45309; white-space: nowrap; }
    .novedad-item .ni-text   { color: #92400e; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 220px; font-weight: 500;}
    .novedad-item .ni-dot    { width: 8px; height: 8px; border-radius: 50%; background: #f59e0b; flex-shrink: 0; box-shadow: 0 0 6px #fbbf24;}

    /* Filtro grupos */
    .dep-grupos-filter { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
    .dep-grupo-btn {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 8px 16px; border-radius: 20px; border: 1px solid var(--border);
      background: var(--white); color: var(--text-main);
      font-size: 12px; font-weight: 700; cursor: pointer; transition: all var(--trans);
      box-shadow: 0 2px 6px rgba(0,0,0,0.03); font-family: 'Outfit', sans-serif;
    }
    .dep-grupo-btn:hover { border-color: var(--violet-300); color: var(--violet-700); transform: translateY(-2px); box-shadow: 0 4px 10px rgba(139, 92, 246, 0.1); }
    .dep-grupo-btn.active { background: var(--violet-600); color: white; border-color: var(--violet-600); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3); }
    .dep-grupo-btn .dg-count {
      background: var(--violet-100); color: var(--violet-700); border-radius: 20px;
      padding: 2px 8px; font-size: 10px; font-weight: 800;
    }
    .dep-grupo-btn.active .dg-count { background: rgba(255,255,255,0.2); color: white; }

    /* ── LOADING ─────────────────────────────── */
    #loading-overlay {
      position: fixed; inset: 0; background: rgba(248, 250, 252, 0.8);
      backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      z-index: 999; gap: 16px; transition: opacity 0.5s ease;
    }
    #loading-overlay.hidden { opacity: 0; pointer-events: none; }
    .loader-logo { font-size: 50px; margin-bottom: 8px; animation: bounce 2s infinite cubic-bezier(0.28, 0.84, 0.42, 1); }
    .loader-text { font-size: 14px; color: var(--violet-700); font-weight: 700; letter-spacing: 1px; text-transform: uppercase;}
    .loader-bar  { width: 200px; height: 6px; background: rgba(139, 92, 246, 0.1); border-radius: 99px; overflow: hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);}
    .loader-fill { height: 100%; background: linear-gradient(90deg, var(--violet-400), var(--violet-600)); border-radius: 99px; animation: load 1.5s ease-in-out infinite; }

    @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-15px) scale(1.05); } }
    @keyframes load  { 0%{width:0;margin-left:0} 50%{width:100%;margin-left:0} 100%{width:0;margin-left:100%} }

    /* Toast */
    #toast {
      position: fixed; bottom: 32px; right: 32px;
      background: var(--white); border: 1px solid var(--border);
      border-radius: 16px; padding: 16px 24px; font-size: 14px; font-weight: 600; color: var(--text-main);
      z-index: 500; transform: translateY(50px); opacity: 0; transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
      display: flex; align-items: center; gap: 12px;
      min-width: 250px; max-width: 350px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    #toast.show { opacity: 1; transform: translateY(0); }
    #toast.ok  { border-left: 6px solid #10b981; }
    #toast.ok .ti { color: #10b981; font-size: 20px;}
    #toast.err { border-left: 6px solid #ef4444; }
    #toast.err .ti { color: #ef4444; font-size: 20px;}

    .empty-state { text-align: center; padding: 80px 20px; color: var(--muted); }
    .empty-state .ei { font-size: 60px; margin-bottom: 16px; opacity: 0.5; filter: grayscale(1); }
    .empty-state div { font-weight: 600; font-size: 16px;}

    ::-webkit-scrollbar       { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 99px; border: 2px solid #f8fafc;}
    ::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 246, 0.6); }

    @media (max-width: 900px) {
      #sidebar { position: fixed; left: 0; top: 0; bottom: 0; transform: translateX(-100%); }
      #sidebar.open { transform: translateX(0); box-shadow: 0 0 50px rgba(0,0,0,0.2); }
      .dash-grid { grid-template-columns: 1fr; }
      #topbar { padding: 0 20px; }
      .search-wrap input { width: 160px; }
      .search-wrap input:focus { width: 200px; }
    }
"""

style_block_pattern = r'<style>.*?</style>'
new_content = re.sub(style_block_pattern, f'<style>\n{new_css}\n  </style>', content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("CSS updated successfully.")
