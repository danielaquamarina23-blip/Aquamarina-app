import os
import io
import copy
import shutil
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path

from flask import Flask, request, send_file, jsonify, render_template
from docx import Document
from docx.shared import Pt
import openpyxl
from num2words import num2words

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
CONT_TEMPLATE = BASE_DIR / "CONT_plantilla.docx"
LIQUI_TEMPLATE = BASE_DIR / "LIQUI_plantilla.xlsx"


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def pesos_en_letras(valor: float) -> str:
    """Convierte número a letras en español (pesos colombianos)."""
    try:
        entero = int(valor)
        letras = num2words(entero, lang="es").upper()
        return f"{letras} PESOS M/CTE"
    except Exception:
        return ""


def replace_in_paragraph(paragraph, replacements: dict):
    """Reemplaza marcadores en un párrafo preservando formato."""
    for key, val in replacements.items():
        for run in paragraph.runs:
            if key in run.text:
                run.text = run.text.replace(key, str(val))
        # Si el marcador quedó partido entre runs, reconstruir texto del párrafo
        full = "".join(r.text for r in paragraph.runs)
        if key in full:
            full_replaced = full.replace(key, str(val))
            for i, run in enumerate(paragraph.runs):
                run.text = full_replaced if i == 0 else ""


def replace_in_doc(doc: Document, replacements: dict):
    """Reemplaza en todos los párrafos y tablas del documento."""
    for para in doc.paragraphs:
        replace_in_paragraph(para, replacements)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    replace_in_paragraph(para, replacements)


def docx_to_pdf(docx_path: Path) -> Path:
    """Convierte docx a PDF usando LibreOffice."""
    out_dir = docx_path.parent
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx_path)],
        env=env, check=True, capture_output=True, timeout=60
    )
    return docx_path.with_suffix(".pdf")


def xlsx_to_pdf(xlsx_path: Path) -> Path:
    """Convierte xlsx a PDF usando LibreOffice."""
    out_dir = xlsx_path.parent
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(xlsx_path)],
        env=env, check=True, capture_output=True, timeout=60
    )
    return xlsx_path.with_suffix(".pdf")


# ──────────────────────────────────────────────
# Rutas
# ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contrato", methods=["POST"])
def generar_contrato():
    """Genera el contrato Word/PDF con los datos del formulario."""
    data = request.json or {}

    nombre_titular    = data.get("nombre_titular", "")
    doc_titular       = data.get("doc_titular", "")
    celular           = data.get("celular", "")
    correo            = data.get("correo", "")
    hotel             = data.get("hotel", "")
    origen            = data.get("origen", "")
    destino           = data.get("destino", "")
    fecha_salida      = data.get("fecha_salida", "")
    fecha_regreso     = data.get("fecha_regreso", "")
    total_noches      = data.get("total_noches", "")
    adultos           = data.get("adultos", 0)
    ninos             = data.get("ninos", 0)
    infantes          = data.get("infantes", 0)
    acomodacion       = data.get("acomodacion", "")
    pasajeros         = data.get("pasajeros", [])   # lista de {nombre, documento}
    tarifa_total      = float(data.get("tarifa_total", 0))
    cuota_inicial     = float(data.get("cuota_inicial", 0))
    num_cuotas        = data.get("num_cuotas", "")
    valor_cuota       = float(data.get("valor_cuota", 0))
    asesor            = data.get("asesor", "")
    num_rsv           = data.get("num_rsv", "")
    fmt_salida        = data.get("fmt_salida", fecha_salida)
    fmt_regreso       = data.get("fmt_regreso", fecha_regreso)
    output_format     = data.get("formato", "pdf")   # "pdf" o "docx"

    tarifa_letras = pesos_en_letras(tarifa_total)

    # Tabla de pasajeros: construir texto
    pasajeros_texto = ""
    for p in pasajeros:
        pasajeros_texto += f"{p.get('nombre','')} — {p.get('documento','')}\n"

    replacements = {
        "{{NOMBRE_TITULAR}}":  nombre_titular,
        "{{DOC_TITULAR}}":     doc_titular,
        "{{CELULAR}}":         celular,
        "{{CORREO}}":          correo,
        "{{HOTEL}}":           hotel,
        "{{ORIGEN}}":          origen,
        "{{DESTINO}}":         destino,
        "{{FECHA_SALIDA}}":    fmt_salida,
        "{{FECHA_REGRESO}}":   fmt_regreso,
        "{{TOTAL_NOCHES}}":    total_noches,
        "{{ADULTOS}}":         adultos,
        "{{NINOS}}":           ninos,
        "{{INFANTES}}":        infantes,
        "{{ACOMODACION}}":     acomodacion,
        "{{TARIFA_LETRAS}}":   tarifa_letras,
        "{{TARIFA_TOTAL}}":    f"${tarifa_total:,.0f}",
        "{{CUOTA_INICIAL}}":   f"${cuota_inicial:,.0f}",
        "{{NUM_CUOTAS}}":      num_cuotas,
        "{{VALOR_CUOTA}}":     f"${valor_cuota:,.0f}",
        "{{ASESOR}}":          asesor,
        "{{NUM_RSV}}":         num_rsv,
        "MIL PESOS ($)":       tarifa_letras,   # reemplaza placeholder en cláusula 3
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        docx_out = tmp / f"Contrato_{nombre_titular.replace(' ','_')}_{num_rsv}.docx"
        shutil.copy(CONT_TEMPLATE, docx_out)

        doc = Document(docx_out)
        replace_in_doc(doc, replacements)

        # Llenar tabla de pasajeros
        for table in doc.tables:
            headers = [c.text.strip() for c in table.rows[0].cells]
            if "NOMBRE Y APELLIDOS COMPLETOS" in headers or any("PASAJEROS" in h for h in headers):
                # Encontrar fila de encabezado de datos
                for row in table.rows:
                    texts = [c.text.strip() for c in row.cells]
                    if "NOMBRE Y APELLIDOS COMPLETOS" in texts:
                        # Insertar pasajeros después de esta fila
                        idx = list(table.rows).index(row)
                        for i, p in enumerate(pasajeros):
                            try:
                                target_row = table.rows[idx + 1 + i]
                                target_row.cells[0].text = p.get("nombre", "")
                                target_row.cells[-1].text = p.get("documento", "")
                            except IndexError:
                                pass
                        break

        doc.save(docx_out)

        if output_format == "docx":
            buf = io.BytesIO(docx_out.read_bytes())
            buf.seek(0)
            return send_file(
                buf,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                as_attachment=True,
                download_name=docx_out.name
            )

        # Convertir a PDF
        pdf_out = docx_to_pdf(docx_out)
        buf = io.BytesIO(pdf_out.read_bytes())
        buf.seek(0)
        return send_file(
            buf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Contrato_{nombre_titular.replace(' ','_')}_{num_rsv}.pdf"
        )


@app.route("/liquidacion", methods=["POST"])
def generar_liquidacion():
    """Rellena la plantilla XLSX de liquidación y la devuelve como PDF o XLSX."""
    data = request.json or {}

    num_rsv_h        = data.get("num_rsv_h", "")
    num_rsv_v        = data.get("num_rsv_v", "")
    nombre_titular   = data.get("nombre_titular", "")
    doc_titular      = data.get("doc_titular", "")
    celular          = data.get("celular", "")
    correo           = data.get("correo", "")
    ciudad           = data.get("ciudad", "")
    fecha_rsv        = data.get("fecha_rsv", "")
    asesor           = data.get("asesor", "")
    origen           = data.get("origen", "")
    destino          = data.get("destino", "")
    fecha_ida        = data.get("fecha_ida", "")
    fecha_regreso    = data.get("fecha_regreso", "")
    hotel            = data.get("hotel", "")
    noches           = data.get("noches", 0)
    tipo_vuelo       = data.get("tipo_vuelo", "Comercial")
    adultos          = int(data.get("adultos", 0))
    ninos            = int(data.get("ninos", 0))
    infantes         = int(data.get("infantes", 0))
    acomodacion      = data.get("acomodacion", "DOBLE")  # SENCILLA/DOBLE/TRIPLE
    tarifa_sencilla  = float(data.get("tarifa_sencilla", 0))
    tarifa_doble     = float(data.get("tarifa_doble", 0))
    tarifa_triple    = float(data.get("tarifa_triple", 0))
    tarifa_nino      = float(data.get("tarifa_nino", 0))
    tarifa_infante   = float(data.get("tarifa_infante", 0))
    cant_sencilla    = int(data.get("cant_sencilla", 0))
    cant_doble       = int(data.get("cant_doble", 0))
    cant_triple      = int(data.get("cant_triple", 0))
    cant_nino        = int(data.get("cant_nino", 0))
    cant_infante     = int(data.get("cant_infante", 0))
    tours            = [float(x) for x in data.get("tours", [0, 0, 0, 0, 0])]
    asistencia       = [float(x) for x in data.get("asistencia", [0, 0, 0, 0, 0])]
    equipaje         = [float(x) for x in data.get("equipaje", [0, 0, 0, 0, 0])]
    cuota_inicial    = float(data.get("cuota_inicial", 0))
    num_cuotas       = int(data.get("num_cuotas", 1))
    output_format    = data.get("formato", "pdf")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        xlsx_out = tmp / f"Liquidacion_{nombre_titular.replace(' ','_')}_{num_rsv_h}.xlsx"
        shutil.copy(LIQUI_TEMPLATE, xlsx_out)

        wb = openpyxl.load_workbook(xlsx_out)
        ws = wb.active  # Hoja CONFIRMACION

        # Mapeo de celdas según estructura de la plantilla
        cell_map = {
            "H1":  num_rsv_h,
            "H2":  num_rsv_v,
            "D5":  "Yamile Segura",       # Director (fijo)
            "D6":  asesor,
            "D7":  fecha_rsv,
            "H7":  ciudad,
            "D9":  nombre_titular,
            "D10": doc_titular,
            "D11": "",                     # dirección (opcional)
            "H9":  celular,
            "H10": "",                     # tel alternativo
            "H11": correo,
            "D13": origen,
            "H13": destino,
            "D14": fecha_ida,
            "H14": fecha_regreso,
            "D15": adultos,
            "F15": ninos,
            "H15": infantes,
            "D16": hotel,
            "F17": noches,
            "H17": tipo_vuelo,
            # Cantidades acomodación
            "D19": cant_sencilla,
            "E19": cant_doble,
            "F19": cant_triple,
            "G19": cant_nino,
            "H19": cant_infante,
            # Tarifas
            "D21": tarifa_sencilla,
            "E21": tarifa_doble,
            "F21": tarifa_triple,
            "G21": tarifa_nino,
            "H21": tarifa_infante,
            # Tours
            "D22": tours[0] if len(tours) > 0 else 0,
            "E22": tours[1] if len(tours) > 1 else 0,
            "F22": tours[2] if len(tours) > 2 else 0,
            "G22": tours[3] if len(tours) > 3 else 0,
            "H22": tours[4] if len(tours) > 4 else 0,
            # Asistencia médica
            "D23": asistencia[0] if len(asistencia) > 0 else 0,
            "E23": asistencia[1] if len(asistencia) > 1 else 0,
            "F23": asistencia[2] if len(asistencia) > 2 else 0,
            "G23": asistencia[3] if len(asistencia) > 3 else 0,
            "H23": asistencia[4] if len(asistencia) > 4 else 0,
            # Equipaje
            "D24": equipaje[0] if len(equipaje) > 0 else 0,
            "E24": equipaje[1] if len(equipaje) > 1 else 0,
            "F24": equipaje[2] if len(equipaje) > 2 else 0,
            "H24": equipaje[4] if len(equipaje) > 4 else 0,
            # Cantidades de personas
            "D25": cant_sencilla,
            "E25": cant_doble,
            "F25": cant_triple,
            "G25": cant_nino,
            "H25": cant_infante,
        }

        for cell_ref, val in cell_map.items():
            ws[cell_ref] = val

        # Calcular totales para campo en letras (fila 28)
        total = (
            tarifa_sencilla * cant_sencilla +
            tarifa_doble    * cant_doble +
            tarifa_triple   * cant_triple +
            tarifa_nino     * cant_nino +
            tarifa_infante  * cant_infante
        )
        ws["D28"] = pesos_en_letras(total)

        # Acuerdo de pagos (fila 30)
        saldo = total - cuota_inicial
        valor_cuota_calc = saldo / num_cuotas if num_cuotas > 0 else saldo
        ws["D30"] = cuota_inicial
        ws["F30"] = num_cuotas
        ws["H30"] = saldo

        wb.save(xlsx_out)

        if output_format == "xlsx":
            buf = io.BytesIO(xlsx_out.read_bytes())
            buf.seek(0)
            return send_file(
                buf,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name=xlsx_out.name
            )

        pdf_out = xlsx_to_pdf(xlsx_out)
        buf = io.BytesIO(pdf_out.read_bytes())
        buf.seek(0)
        return send_file(
            buf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Liquidacion_{nombre_titular.replace(' ','_')}_{num_rsv_h}.pdf"
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
