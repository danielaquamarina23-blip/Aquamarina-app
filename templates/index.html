<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aquamarina Travels — Generador de Documentos</title>
<style>
  :root {
    --azul:      #1a3a5c;
    --azul-med:  #1e5f8e;
    --aqua:      #00b4d8;
    --aqua-soft: #90e0ef;
    --blanco:    #f8fafc;
    --gris:      #e2e8f0;
    --gris-t:    #64748b;
    --rojo:      #e53e3e;
    --verde:     #2d6a4f;
    --radio:     10px;
    --sombra:    0 4px 24px rgba(0,0,0,.10);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: linear-gradient(135deg, #e8f4fd 0%, #f0fafa 100%);
    min-height: 100vh;
    color: #1e293b;
  }

  /* ─── Header ─── */
  header {
    background: var(--azul);
    color: #fff;
    padding: 18px 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,.25);
  }
  header .logo {
    width: 52px; height: 52px;
    background: var(--aqua);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; font-weight: 900; color: var(--azul);
    letter-spacing: -1px;
  }
  header h1 { font-size: 1.4rem; font-weight: 700; }
  header p  { font-size: .85rem; opacity: .75; margin-top: 2px; }

  /* ─── Layout ─── */
  main {
    max-width: 960px;
    margin: 32px auto;
    padding: 0 20px 60px;
  }

  /* ─── Secciones ─── */
  .card {
    background: #fff;
    border-radius: var(--radio);
    box-shadow: var(--sombra);
    margin-bottom: 24px;
    overflow: hidden;
  }
  .card-header {
    background: var(--azul);
    color: #fff;
    padding: 14px 22px;
    font-size: .95rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .card-header .icon {
    background: var(--aqua);
    color: var(--azul);
    border-radius: 6px;
    width: 28px; height: 28px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 900;
  }
  .card-body { padding: 22px; }

  /* ─── Grid campos ─── */
  .grid { display: grid; gap: 16px; }
  .grid-2 { grid-template-columns: 1fr 1fr; }
  .grid-3 { grid-template-columns: 1fr 1fr 1fr; }
  @media(max-width:640px){
    .grid-2, .grid-3 { grid-template-columns: 1fr; }
  }

  /* ─── Campos ─── */
  .field { display: flex; flex-direction: column; gap: 5px; }
  label { font-size: .82rem; font-weight: 600; color: var(--gris-t); text-transform: uppercase; letter-spacing: .04em; }
  input, select, textarea {
    border: 1.5px solid var(--gris);
    border-radius: 7px;
    padding: 9px 12px;
    font-size: .95rem;
    color: #1e293b;
    transition: border-color .2s, box-shadow .2s;
    background: var(--blanco);
  }
  input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: var(--aqua);
    box-shadow: 0 0 0 3px rgba(0,180,216,.15);
  }
  textarea { resize: vertical; min-height: 70px; }
  .required::after { content: " *"; color: var(--rojo); }

  /* ─── Pasajeros ─── */
  .pax-list { display: flex; flex-direction: column; gap: 10px; }
  .pax-row {
    display: grid;
    grid-template-columns: 1fr 1fr auto;
    gap: 10px;
    align-items: end;
  }
  .btn-remove {
    background: #fee2e2;
    border: none; border-radius: 7px;
    color: var(--rojo);
    padding: 9px 13px;
    cursor: pointer;
    font-size: 16px;
    transition: background .15s;
  }
  .btn-remove:hover { background: #fca5a5; }
  #btn-add-pax {
    margin-top: 10px;
    background: #eff6ff;
    border: 1.5px dashed var(--azul-med);
    border-radius: 7px;
    color: var(--azul-med);
    padding: 9px 18px;
    cursor: pointer;
    font-size: .9rem;
    font-weight: 600;
    transition: background .15s;
  }
  #btn-add-pax:hover { background: #dbeafe; }

  /* ─── Acciones ─── */
  .actions {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    margin-top: 28px;
  }
  .btn {
    flex: 1;
    min-width: 200px;
    padding: 14px 24px;
    border: none;
    border-radius: var(--radio);
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: transform .15s, box-shadow .15s, opacity .15s;
  }
  .btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,.15); }
  .btn:active { transform: translateY(0); }
  .btn-contrato {
    background: linear-gradient(135deg, var(--azul) 0%, var(--azul-med) 100%);
    color: #fff;
  }
  .btn-liquidacion {
    background: linear-gradient(135deg, #0d7a5f 0%, #2d9d79 100%);
    color: #fff;
  }
  .btn-ambos {
    background: linear-gradient(135deg, var(--aqua) 0%, #0096c7 100%);
    color: var(--azul);
    flex: 100%;
  }
  .btn:disabled { opacity: .55; cursor: not-allowed; transform: none; }

  /* ─── Toast ─── */
  #toast {
    position: fixed;
    bottom: 28px; left: 50%;
    transform: translateX(-50%) translateY(80px);
    background: var(--verde);
    color: #fff;
    padding: 12px 24px;
    border-radius: 50px;
    font-weight: 600;
    font-size: .95rem;
    box-shadow: 0 4px 20px rgba(0,0,0,.2);
    transition: transform .3s cubic-bezier(.34,1.56,.64,1);
    z-index: 999;
    white-space: nowrap;
  }
  #toast.show { transform: translateX(-50%) translateY(0); }

  /* ─── Nota del valor ─── */
  .valor-nota {
    font-size: .8rem;
    color: var(--gris-t);
    margin-top: 4px;
  }
  .letras-preview {
    font-size: .82rem;
    color: var(--azul-med);
    font-style: italic;
    min-height: 18px;
    margin-top: 2px;
  }
  .separador {
    border: none;
    border-top: 1.5px solid var(--gris);
    margin: 18px 0;
  }
</style>
</head>
<body>

<header>
  <div class="logo">AT</div>
  <div>
    <h1>Aquamarina Travels</h1>
    <p>Generador de Contratos y Liquidaciones — NIT 79489739-9</p>
  </div>
</header>

<main>

  <!-- 1. Datos del titular -->
  <div class="card">
    <div class="card-header">
      <div class="icon">1</div>
      Datos del Titular de la Reserva
    </div>
    <div class="card-body">
      <div class="grid grid-2">
        <div class="field">
          <label class="required" for="titular">Nombre completo</label>
          <input type="text" id="titular" placeholder="Nombres y apellidos completos">
        </div>
        <div class="field">
          <label class="required" for="documento">N° de identificación</label>
          <input type="text" id="documento" placeholder="CC / CE / Pasaporte">
        </div>
        <div class="field">
          <label for="celular">Celular</label>
          <input type="text" id="celular" placeholder="3XX XXX XXXX">
        </div>
        <div class="field">
          <label for="correo">Correo electrónico</label>
          <input type="email" id="correo" placeholder="correo@ejemplo.com">
        </div>
        <div class="field">
          <label for="asesor">Asesor</label>
          <input type="text" id="asesor" placeholder="Nombre del asesor" value="Yamile Segura">
        </div>
        <div class="field">
          <label for="fecha_rsv">Fecha de reserva</label>
          <input type="date" id="fecha_rsv">
        </div>
      </div>
    </div>
  </div>

  <!-- 2. Servicios contratados -->
  <div class="card">
    <div class="card-header">
      <div class="icon">2</div>
      Servicios Contratados
    </div>
    <div class="card-body">
      <div class="grid grid-2">
        <div class="field">
          <label class="required" for="origen">Ciudad de origen</label>
          <input type="text" id="origen" placeholder="Ej: Bogotá" value="Bogotá">
        </div>
        <div class="field">
          <label class="required" for="destino">Ciudad de destino</label>
          <input type="text" id="destino" placeholder="Ej: Cartagena">
        </div>
        <div class="field">
          <label class="required" for="fecha_ida">Fecha de ida</label>
          <input type="date" id="fecha_ida">
        </div>
        <div class="field">
          <label class="required" for="fecha_regreso">Fecha de regreso</label>
          <input type="date" id="fecha_regreso">
        </div>
        <div class="field">
          <label for="noches">N° de noches</label>
          <input type="number" id="noches" min="1" placeholder="5">
        </div>
        <div class="field">
          <label class="required" for="hotel">Hotel seleccionado</label>
          <input type="text" id="hotel" placeholder="Nombre del hotel">
        </div>
      </div>

      <hr class="separador">

      <div class="grid grid-3">
        <div class="field">
          <label for="adultos">Adultos</label>
          <input type="number" id="adultos" min="0" value="2">
        </div>
        <div class="field">
          <label for="ninos">Niños (2–11 años)</label>
          <input type="number" id="ninos" min="0" value="0">
        </div>
        <div class="field">
          <label for="infantes">Infantes (0–23 meses)</label>
          <input type="number" id="infantes" min="0" value="0">
        </div>
      </div>

      <hr class="separador">

      <div class="grid grid-2">
        <div class="field">
          <label for="acomodacion">Acomodación</label>
          <select id="acomodacion">
            <option value="Sencilla">Sencilla</option>
            <option value="Doble" selected>Doble</option>
            <option value="Triple">Triple</option>
            <option value="Niño">Niño</option>
          </select>
        </div>
        <div class="field">
          <label for="tipo_vuelo">Tipo de vuelo</label>
          <select id="tipo_vuelo">
            <option value="Comercial" selected>Comercial</option>
            <option value="Charter">Charter</option>
          </select>
        </div>
      </div>
    </div>
  </div>

  <!-- 3. Pasajeros -->
  <div class="card">
    <div class="card-header">
      <div class="icon">3</div>
      Lista de Pasajeros
    </div>
    <div class="card-body">
      <div class="pax-list" id="pax-list">
        <!-- se genera dinámicamente -->
      </div>
      <button id="btn-add-pax" type="button">+ Agregar pasajero</button>
    </div>
  </div>

  <!-- 4. Valores -->
  <div class="card">
    <div class="card-header">
      <div class="icon">4</div>
      Condiciones Económicas
    </div>
    <div class="card-body">
      <div class="grid grid-2">
        <div class="field">
          <label class="required" for="valor_total">Valor total del contrato ($)</label>
          <input type="number" id="valor_total" min="0" step="1000" placeholder="0" oninput="actualizarLetras()">
          <div class="letras-preview" id="valor_letras"></div>
        </div>
        <div class="field">
          <label for="cuota_inicial">Cuota inicial (30%)</label>
          <input type="number" id="cuota_inicial" min="0" step="1000" placeholder="0">
          <div class="valor-nota">Se calcula automáticamente al ingresar el total</div>
        </div>
        <div class="field">
          <label for="num_cuotas">Número de cuotas</label>
          <input type="number" id="num_cuotas" min="1" value="1" oninput="calcularCuota()">
        </div>
        <div class="field">
          <label for="valor_cuota">Valor por cuota</label>
          <input type="number" id="valor_cuota" min="0" step="1000" placeholder="0" readonly>
        </div>
      </div>
    </div>
  </div>

  <!-- Botones -->
  <div class="actions">
    <button class="btn btn-contrato" onclick="descargar('contrato')">
      📄 Descargar Contrato (.pdf)
    </button>
    <button class="btn btn-liquidacion" onclick="descargar('liquidacion')">
      📊 Descargar Liquidación (.pdf)
    </button>
    <button class="btn btn-ambos" onclick="descargarAmbos()">
      ⚡ Generar los Dos PDFs
    </button>
  </div>

</main>

<div id="toast">✅ Documento generado con éxito</div>

<script>
// ── Número a letras (preview) ─────────────────────────────────────────────
const unidades = ['','uno','dos','tres','cuatro','cinco','seis','siete','ocho','nueve',
  'diez','once','doce','trece','catorce','quince','dieciséis','diecisiete','dieciocho','diecinueve'];
const decenas  = ['','diez','veinte','treinta','cuarenta','cincuenta','sesenta','setenta','ochenta','noventa'];

function numLetras(n) {
  n = parseInt(n) || 0;
  if (n === 0) return 'cero';
  if (n < 0) return 'menos ' + numLetras(-n);
  let r = '';
  if (n >= 1000000) {
    const m = Math.floor(n / 1000000);
    r += (m === 1 ? 'un millón' : numLetras(m) + ' millones') + ' ';
    n %= 1000000;
  }
  if (n >= 1000) {
    const m = Math.floor(n / 1000);
    r += (m === 1 ? 'mil' : numLetras(m) + ' mil') + ' ';
    n %= 1000;
  }
  if (n >= 100) {
    const c = Math.floor(n / 100);
    const cMap = ['','cien','doscientos','trescientos','cuatrocientos','quinientos',
      'seiscientos','setecientos','ochocientos','novecientos'];
    if (n === 100) { r += 'cien'; n = 0; }
    else { r += cMap[c] + ' '; n %= 100; }
  }
  if (n > 0) {
    if (n < 20) { r += unidades[n]; }
    else {
      r += decenas[Math.floor(n/10)];
      if (n % 10) r += ' y ' + unidades[n % 10];
    }
  }
  return r.trim().replace(/\s+/g,' ');
}

function actualizarLetras() {
  const v = parseFloat(document.getElementById('valor_total').value) || 0;
  document.getElementById('valor_letras').textContent = v > 0
    ? numLetras(v).toUpperCase() + ' PESOS M/CTE'
    : '';
  // Auto cuota inicial 30%
  const ci = document.getElementById('cuota_inicial');
  if (!ci.dataset.manual) ci.value = Math.round(v * 0.3);
  calcularCuota();
}

function calcularCuota() {
  const total   = parseFloat(document.getElementById('valor_total').value)    || 0;
  const inicial = parseFloat(document.getElementById('cuota_inicial').value) || 0;
  const cuotas  = parseInt(document.getElementById('num_cuotas').value)       || 1;
  const saldo   = total - inicial;
  document.getElementById('valor_cuota').value = cuotas > 0 ? Math.round(saldo / cuotas) : 0;
}

document.getElementById('cuota_inicial').addEventListener('input', function() {
  this.dataset.manual = '1';
  calcularCuota();
});

// ── Pasajeros ─────────────────────────────────────────────────────────────
let paxCount = 0;

function agregarPasajero(nombre='', doc='') {
  paxCount++;
  const div = document.createElement('div');
  div.className = 'pax-row';
  div.dataset.id = paxCount;
  div.innerHTML = `
    <div class="field">
      <label>Pasajero ${paxCount} — Nombre completo</label>
      <input type="text" class="pax-nombre" value="${nombre}" placeholder="Nombres y apellidos">
    </div>
    <div class="field">
      <label>N° Documento</label>
      <input type="text" class="pax-doc" value="${doc}" placeholder="Documento de identidad">
    </div>
    <button class="btn-remove" onclick="this.parentElement.remove(); recontarPax()" title="Eliminar">✕</button>
  `;
  document.getElementById('pax-list').appendChild(div);
}

function recontarPax() {
  document.querySelectorAll('.pax-row').forEach((row, i) => {
    row.querySelector('label').textContent = `Pasajero ${i+1} — Nombre completo`;
  });
}

document.getElementById('btn-add-pax').addEventListener('click', () => agregarPasajero());

// Inicializar con 2 pasajeros
agregarPasajero();
agregarPasajero();

// Fecha de reserva: hoy
document.getElementById('fecha_rsv').valueAsDate = new Date();

// ── Recopilar datos ────────────────────────────────────────────────────────
function recopilarDatos() {
  const pasajeros = [];
  document.querySelectorAll('.pax-row').forEach(row => {
    const nombre = row.querySelector('.pax-nombre').value.trim();
    const doc    = row.querySelector('.pax-doc').value.trim();
    if (nombre) pasajeros.push({ nombre, doc });
  });

  return {
    titular:       document.getElementById('titular').value.trim(),
    documento:     document.getElementById('documento').value.trim(),
    celular:       document.getElementById('celular').value.trim(),
    correo:        document.getElementById('correo').value.trim(),
    asesor:        document.getElementById('asesor').value.trim(),
    fecha_rsv:     document.getElementById('fecha_rsv').value,
    origen:        document.getElementById('origen').value.trim(),
    destino:       document.getElementById('destino').value.trim(),
    fecha_ida:     document.getElementById('fecha_ida').value,
    fecha_regreso: document.getElementById('fecha_regreso').value,
    noches:        document.getElementById('noches').value,
    hotel:         document.getElementById('hotel').value.trim(),
    adultos:       document.getElementById('adultos').value,
    ninos:         document.getElementById('ninos').value,
    infantes:      document.getElementById('infantes').value,
    acomodacion:   document.getElementById('acomodacion').value,
    tipo_vuelo:    document.getElementById('tipo_vuelo').value,
    valor_total:   document.getElementById('valor_total').value,
    cuota_inicial: document.getElementById('cuota_inicial').value,
    num_cuotas:    document.getElementById('num_cuotas').value,
    valor_cuota:   document.getElementById('valor_cuota').value,
    pasajeros
  };
}

function validar(datos) {
  if (!datos.titular) { alert('⚠️ Por favor ingresa el nombre del titular.'); return false; }
  if (!datos.documento) { alert('⚠️ Por favor ingresa el documento del titular.'); return false; }
  if (!datos.destino) { alert('⚠️ Por favor ingresa el destino.'); return false; }
  return true;
}

// ── Descarga ───────────────────────────────────────────────────────────────
async function descargar(tipo) {
  const datos = recopilarDatos();
  if (!validar(datos)) return;

  const url = tipo === 'contrato' ? '/contrato' : '/liquidacion';
  const btn = document.querySelectorAll('.btn')[tipo === 'contrato' ? 0 : 1];
  btn.disabled = true;
  btn.textContent = '⏳ Generando...';

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });
    if (!res.ok) throw new Error('Error en el servidor');
    const blob = await res.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = res.headers.get('Content-Disposition')?.match(/filename="(.+)"/)?.[1]
      || (tipo === 'contrato' ? 'contrato.pdf' : 'liquidacion.pdf');
    a.click();
    mostrarToast(`✅ ${tipo === 'contrato' ? 'Contrato' : 'Liquidación'} descargado`);
  } catch(e) {
    alert('Error generando el documento: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = tipo === 'contrato' ? '📄 Descargar Contrato (.pdf)' : '📊 Descargar Liquidación (.pdf)';
  }
}

async function descargarAmbos() {
  const datos = recopilarDatos();
  if (!validar(datos)) return;
  const btn = document.querySelector('.btn-ambos');
  btn.disabled = true;
  btn.textContent = '⏳ Generando documentos...';
  try {
    await Promise.all([
      fetch('/contrato',    { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(datos) })
        .then(r => r.blob()).then(b => { const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='Contrato_'+datos.titular+'.docx'; a.click(); }),
      new Promise(r => setTimeout(r, 600)).then(() =>
        fetch('/liquidacion', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(datos) })
          .then(r => r.blob()).then(b => { const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='Liquidacion_'+datos.titular+'.xlsx'; a.click(); })
      )
    ]);
    mostrarToast('✅ Ambos documentos generados');
  } catch(e) {
    alert('Error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = '⚡ Generar los Dos PDFs';
  }
}

function mostrarToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
</script>
</body>
</html>
