// ============================================================
//  PERSONAL POLICIAL - ZONA 8  |  Code.gs
//  Backend GAS  |  Arquitectura: REST-style doGet + doPost
// ============================================================

var SS_ID   = "1SRGAx5jzQPEafhY37soUQweXGptLpfsh-QXKV-G2GWE";
var SHEET   = "CONSOLIDADO";

// Columnas (1-indexed)
var COL = {
  CEDULA      : 1,
  GRADO       : 2,
  NOMBRES     : 3,
  DEPENDENCIAS: 4,
  CARGO       : 5,
  NOVEDADES   : 6,
  GRUPO       : 7,
  ESTADO      : 8,
  CELULAR     : 9
};

var ESTADOS_VALIDOS = [
  "LICENCIA",
  "FRANCO",
  "PRESENTE",
  "VACACIONES",
  "TRASLADO TEMPORAL",
  "DESCANSO MEDICO",
  "SERVICIO"
];

// ─── Punto de entrada GET ────────────────────────────────────
function doGet(e) {
  return HtmlService
    .createHtmlOutputFromFile("index")
    .setTitle("Personal Policial – Zona 8")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

// ─── Router de acciones ──────────────────────────────────────
function doPost(e) {
  var payload = JSON.parse(e.postData.contents);
  var action  = payload.action;

  try {
    if (action === "getAll")          return resp(getAll());
    if (action === "updateEstado")    return resp(updateEstado(payload));
    if (action === "getDashboard")    return resp(getDashboard());
    return resp({ ok: false, msg: "Accion desconocida" });
  } catch (err) {
    return resp({ ok: false, msg: err.message });
  }
}

function resp(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

// ─── Leer todos los registros ────────────────────────────────
function getAll() {
  var sheet  = SpreadsheetApp.openById(SS_ID).getSheetByName(SHEET);
  var last   = sheet.getLastRow();
  if (last < 2) return { ok: true, data: [] };

  var range  = sheet.getRange(2, 1, last - 1, 9);
  var values = range.getValues();
  var rows   = [];

  values.forEach(function(r, i) {
    // Normalizar a String para evitar mismatch numérico/string en el frontend
    function str(v) { return (v !== null && v !== undefined) ? String(v).trim() : ""; }

    rows.push({
      fila        : i + 2,
      cedula      : str(r[COL.CEDULA      - 1]),
      grado       : str(r[COL.GRADO       - 1]),
      nombres     : str(r[COL.NOMBRES     - 1]),
      dependencia : str(r[COL.DEPENDENCIAS- 1]),
      cargo       : str(r[COL.CARGO       - 1]),
      novedades   : str(r[COL.NOVEDADES   - 1]),
      grupo       : str(r[COL.GRUPO       - 1]),   // puede ser número en Sheet
      estado      : str(r[COL.ESTADO      - 1]).toUpperCase(),
      celular     : str(r[COL.CELULAR     - 1])
    });
  });

  return { ok: true, data: rows };
}

// ─── Actualizar ESTADO de una fila ───────────────────────────
function updateEstado(payload) {
  var fila   = parseInt(payload.fila);
  var estado = String(payload.estado).toUpperCase().trim();

  if (!fila || fila < 2) {
    return { ok: false, msg: "Fila invalida" };
  }
  if (ESTADOS_VALIDOS.indexOf(estado) === -1) {
    return { ok: false, msg: "Estado no permitido: " + estado };
  }

  var sheet = SpreadsheetApp.openById(SS_ID).getSheetByName(SHEET);
  sheet.getRange(fila, COL.ESTADO).setValue(estado);

  return { ok: true, msg: "Estado actualizado a: " + estado };
}

// ─── Dashboard: aggregados ───────────────────────────────────
function getDashboard() {
  var result   = getAll();
  var rows     = result.data;

  var depMap   = {};   // { dep: { total, estados: {} } }
  var estadoTot= {};
  var grupoTot = {};
  var total    = rows.length;

  rows.forEach(function(r) {
    var dep    = r.dependencia || "SIN DEPENDENCIA";
    var est    = r.estado      || "SIN ESTADO";
    var grp    = r.grupo       || "SIN GRUPO";

    // Por dependencia
    if (!depMap[dep]) depMap[dep] = { total: 0, estados: {} };
    depMap[dep].total++;
    depMap[dep].estados[est] = (depMap[dep].estados[est] || 0) + 1;

    // Global estados
    estadoTot[est] = (estadoTot[est] || 0) + 1;

    // Por grupo
    grupoTot[grp] = (grupoTot[grp] || 0) + 1;
  });

  return {
    ok        : true,
    total     : total,
    depMap    : depMap,
    estadoTot : estadoTot,
    grupoTot  : grupoTot
  };
}

// ─── Llamadas directas desde cliente (HtmlService) ──────────
// (GAS permite llamar funciones JS de servidor con google.script.run)

function serverGetAll() {
  return getAll();
}

function serverUpdateEstado(fila, estado) {
  return updateEstado({ fila: fila, estado: estado });
}

function serverGetDashboard() {
  return getDashboard();
}
