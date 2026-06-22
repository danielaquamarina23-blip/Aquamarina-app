import os
import io
import shutil
import tempfile
import subprocess
from pathlib import Path

from flask import Flask, request, send_file, render_template
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn
import openpyxl
from num2words import num2words

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
CONT_TEMPLATE = BASE_DIR / "CONT_plantilla.docx"
LIQUI_TEMPLATE = BASE_DIR / "LIQUI_plantilla.xlsx"


def pesos_en_letras(valor: float) -> str:
    try:
        letras = num2words(int(valor), lang="es").upper()
        return f"{letras} PESOS M/CTE"
    except Exception:
        return ""


def set_cell(cell, text: str):
    """Escribe texto en una celda preservando formato existente."""
    para = cell.paragraphs[0]
    # Preservar el run existente si hay, o crear uno nuevo
    if para.runs:
        run = para.runs[0]
        # Limpiar otros runs
        for r in para.runs[1:]:
            r.text = ""
        run.text = text
    else:
        run = para.add_run(text)
    # Aplicar negrita y color azul igual al resto de la tabla
    run.bold = True
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x8B)


def get_unique_cells(row):
    """Retorna celdas únicas de una fila (sin repetir por merge)."""
    seen = set()
    unique = []
    for c in row.cells:
        if id(c) not in seen:
            seen.add(id(c))
            unique.append(c)
    return unique


def fill_contrato(doc: Document, d: dict):
    """Llena la tabla de datos de la plantilla del contrato."""
    table = doc.tables[0]

    def row_cells(idx):
        return get_unique_cells(table.rows[idx])

    # Fila 1: NOMBRE TITULAR | No DOCUMENTO
    cells = row_cells(1)
    set_cell(cells[0], f"NOMBRE TITULAR: {d['nombre_titular']}")
    set_cell(cells[1], f"No DOCUMENTO TITULAR RSV: {d['doc_titular']}")

    # Fila 2: CELULAR | CORREO
    cells = row_cells(2)
    set_cell(cells[0], f"NUMERO CELULAR: {d['celular']}")
    set_cell(cells[1], f"CORREO ELECTRONICO: {d['correo']}")

    # Fila 3: HOTEL | ORIGEN | DESTINO
    cells = row_cells(3)
    set_cell(cells[0], f"HOTEL: {d['hotel']}")
    set_cell(cells[1], f"ORIGEN: {d['origen']}")
    set_cell(cells[2], f"DESTINO: {d['destino']}")

    # Fila 4: ADULTOS | FECHA SALIDA
    cells = row_cells(4)
    set_cell(cells[0], f"ADULTOS: {d['adultos']}")
    set_cell(cells[1], f"FECHA DE SALIDA: {d['fmt_salida']}")

    # Fila 5: NIÑOS | FECHA REGRESO
    cells = row_cells(5)
    set_cell(cells[0], f"NIÑOS 2-11 AÑOS: {d['ninos']}")
    set_cell(cells[1], f"FECHA DE REGRESO: {d['fmt_regreso']}")

    # Fila 6: INFANTES | TOTAL NOCHES
    cells = row_cells(6)
    set_cell(cells[0], f"INFANTES 0-23 MESES: {d['infantes']}")
    set_cell(cells[1], f"TOTAL NOCHES: {d['total_noches']}")

    # Fila 7: ACOMODACION
    cells = row_cells(7)
    set_cell(cells[0], f"ACOMODACION HABITACIONAL: {d['acomodacion']}")

    # Filas 10-16: Pasajeros (filas vacías)
    pasajeros = d.get("pasajeros", [])
    for i, p in enumerate(pasajeros[:7]):
        fila_idx = 10 + i
        cells = get_unique_cells(table.rows[fila_idx])
        set_cell(cells[0], p.get("nombre", ""))
        set_cell(cells[1], p.get("documento", ""))

    # Fila 17: TARIFA EN LETRAS | TARIFA EN NUMEROS
    cells = row_cells(17)
    set_cell(cells[0], f"TARIFA TOTAL EN LETRAS: {d['tarifa_letras']}")
    set_cell(cells[1], f"TARIFA EN NUMEROS: ${d['tarifa_total']:,.0f}")

    # Filas 18-21: TARIFA (col 0) | ACUERDO DE PAGOS (col 2)
    tarifas_labels = ["", "CUOTA INICIAL:", "NUMERO CUOTAS:", "VALOR CUOTA:"]
    tarifas_vals   = ["", f"${d['cuota_inicial']:,.0f}", str(d['num_cuotas']), f"${d['valor_cuota']:,.0f}"]
    for i in range(4):
        cells = get_unique_cells(table.rows[18 + i])
        if i == 0:
            set_cell(cells[0], f"TARIFA: ${d['tarifa_total']:,.0f}")
        if len(cells) >= 3 and tarifas_labels[i]:
            set_cell(cells[2], f"{tarifas_labels[i]} {tarifas_vals[i]}")


def docx_to_pdf(docx_path: Path) -> Path:
    out_dir = docx_path.parent
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(out_dir), str(docx_path)],
        env=env, check=True, capture_output=True, timeout=90
    )
    return docx_path.with_suffix(".pdf")


def xlsx_to_pdf(xlsx_path: Path) -> Path:
    out_dir = xlsx_path.parent
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(out_dir), str(xlsx_path)],
        env=env, check=True, capture_output=True, timeout=90
    )
    return xlsx_path.with_suffix(".pdf")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contrato", methods=["POST"])
def generar_contrato():
    data = request.json or {}

    d = {
        "nombre_titular": data.get("nombre_titular", ""),
        "doc_titular":    data.get("doc_titular", ""),
        "celular":        data.get("celular", ""),
        "correo":         data.get("correo", ""),
        "hotel":          data.get("hotel", ""),
        "origen":         data.get("origen", ""),
        "destino":        data.get("destino", ""),
        "fmt_salida":     data.get("fmt_salida", data.get("fecha_salida", "")),
        "fmt_regreso":    data.get("fmt_regreso", data.get("fecha_regreso", "")),
        "total_noches":   data.get("total_noches", ""),
        "adultos":        data.get("adultos", 0),
        "ninos":          data.get("ninos", 0),
        "infantes":       data.get("infantes", 0),
        "acomodacion":    data.get("acomodacion", ""),
        "pasajeros":      data.get("pasajeros", []),
        "tarifa_total":   float(data.get("tarifa_total", 0)),
        "cuota_inicial":  float(data.get("cuota_inicial", 0)),
        "num_cuotas":     data.get("num_cuotas", ""),
        "valor_cuota":    float(data.get("valor_cuota", 0)),
        "asesor":         data.get("asesor", ""),
        "num_rsv":        data.get("num_rsv", ""),
    }
    d["tarifa_letras"] = pesos_en_letras(d["tarifa_total"])
    output_format = data.get("formato", "pdf")

    nombre_safe = d["nombre_titular"].replace(" ", "_")
    num_rsv     = d["num_rsv"]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        docx_out = tmp / f"Contrato_{nombre_safe}_{num_rsv}.docx"
        shutil.copy(CONT_TEMPLATE, docx_out)

        doc = Document(docx_out)
        fill_contrato(doc, d)
        doc.save(docx_out)

        if output_format == "docx":
            buf = io.BytesIO(docx_out.read_bytes())
            buf.seek(0)
            return send_file(buf,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                as_attachment=True,
                download_name=docx_out.name)

        pdf_out = docx_to_pdf(docx_out)
        buf = io.BytesIO(pdf_out.read_bytes())
        buf.seek(0)
        return send_file(buf, mimetype="application/pdf", as_attachment=True,
            download_name=f"Contrato_{nombre_safe}_{num_rsv}.pdf")


@app.route("/liquidacion", methods=["POST"])
def generar_liquidacion():
    data = request.json or {}

    num_rsv_h       = data.get("num_rsv_h", "")
    nombre_titular  = data.get("nombre_titular", "")
    doc_titular     = data.get("doc_titular", "")
    celular         = data.get("celular", "")
    correo          = data.get("correo", "")
    ciudad          = data.get("ciudad", "")
    fecha_rsv       = data.get("fecha_rsv", "")
    asesor          = data.get("asesor", "")
    origen          = data.get("origen", "")
    destino         = data.get("destino", "")
    fecha_ida       = data.get("fecha_ida", "")
    fecha_regreso   = data.get("fecha_regreso", "")
    hotel           = data.get("hotel", "")
    noches          = data.get("noches", 0)
    tipo_vuelo      = data.get("tipo_vuelo", "Comercial")
    adultos         = int(data.get("adultos", 0))
    ninos           = int(data.get("ninos", 0))
    infantes        = int(data.get("infantes", 0))
    tarifa_sencilla = float(data.get("tarifa_sencilla", 0))
    tarifa_doble    = float(data.get("tarifa_doble", 0))
    tarifa_triple   = float(data.get("tarifa_triple", 0))
    tarifa_nino     = float(data.get("tarifa_nino", 0))
    tarifa_infante  = float(data.get("tarifa_infante", 0))
    cant_sencilla   = int(data.get("cant_sencilla", 0))
    cant_doble      = int(data.get("cant_doble", 0))
    cant_triple     = int(data.get("cant_triple", 0))
    cant_nino       = int(data.get("cant_nino", 0))
    cant_infante    = int(data.get("cant_infante", 0))
    tours           = [float(x) for x in data.get("tours", [0]*5)]
    asistencia      = [float(x) for x in data.get("asistencia", [0]*5)]
    equipaje        = [float(x) for x in data.get("equipaje", [0]*5)]
    cuota_inicial   = float(data.get("cuota_inicial", 0))
    num_cuotas      = int(data.get("num_cuotas", 1))
    num_rsv_v       = data.get("num_rsv_v", "")
    output_format   = data.get("formato", "pdf")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        nombre_safe = nombre_titular.replace(" ", "_")
        xlsx_out = tmp / f"Liquidacion_{nombre_safe}_{num_rsv_h}.xlsx"
        shutil.copy(LIQUI_TEMPLATE, xlsx_out)

        wb = openpyxl.load_workbook(xlsx_out)
        ws = wb.active

        cell_map = {
            "H1": num_rsv_h, "H2": num_rsv_v,
            "D5": "Yamile Segura", "D6": asesor,
            "D7": fecha_rsv, "H7": ciudad,
            "D9": nombre_titular, "D10": doc_titular,
            "H9": celular, "H11": correo,
            "D13": origen, "H13": destino,
            "D14": fecha_ida, "H14": fecha_regreso,
            "D15": adultos, "F15": ninos, "H15": infantes,
            "D16": hotel, "F17": noches, "H17": tipo_vuelo,
            "D19": cant_sencilla, "E19": cant_doble,
            "F19": cant_triple, "G19": cant_nino, "H19": cant_infante,
            "D21": tarifa_sencilla, "E21": tarifa_doble,
            "F21": tarifa_triple, "G21": tarifa_nino, "H21": tarifa_infante,
            "D22": tours[0], "E22": tours[1], "F22": tours[2],
            "G22": tours[3], "H22": tours[4],
            "D23": asistencia[0], "E23": asistencia[1], "F23": asistencia[2],
            "G23": asistencia[3], "H23": asistencia[4],
            "D24": equipaje[0], "E24": equipaje[1], "F24": equipaje[2],
            "H24": equipaje[4],
            "D25": cant_sencilla, "E25": cant_doble,
            "F25": cant_triple, "G25": cant_nino, "H25": cant_infante,
        }
        for ref, val in cell_map.items():
            ws[ref] = val

        total = (tarifa_sencilla*cant_sencilla + tarifa_doble*cant_doble +
                 tarifa_triple*cant_triple + tarifa_nino*cant_nino +
                 tarifa_infante*cant_infante)
        ws["D28"] = pesos_en_letras(total)
        saldo = total - cuota_inicial
        ws["D30"] = cuota_inicial
        ws["F30"] = num_cuotas
        ws["H30"] = saldo

        wb.save(xlsx_out)

        if output_format == "xlsx":
            buf = io.BytesIO(xlsx_out.read_bytes())
            buf.seek(0)
            return send_file(buf,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True, download_name=xlsx_out.name)

        pdf_out = xlsx_to_pdf(xlsx_out)
        buf = io.BytesIO(pdf_out.read_bytes())
        buf.seek(0)
        return send_file(buf, mimetype="application/pdf", as_attachment=True,
            download_name=f"Liquidacion_{nombre_safe}_{num_rsv_h}.pdf")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
