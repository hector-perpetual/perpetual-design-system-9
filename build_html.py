#!/usr/bin/env python3
"""
Genera la version HTML autocontenida del template "Business deck completo"
(estilo Colora) en marca Perpetual. ~12 slides ejecutivas tipo BCG/McKinsey.
Armin Grotesk embebida en base64, logos SVG inline. Coordenadas = pulgadas x 96px.
"""
import os, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "perpetual-business-deck.html")

# --- fuentes OTF -> @font-face base64 ---
FONTS = [("Normal", 300), ("Regular", 400), ("Semi_Bold", 600), ("Black", 800)]
faces = []
for name, weight in FONTS:
    data = open(os.path.join(ASSETS, "fonts", f"ArminGrotesk_{name}.otf"), "rb").read()
    b64 = base64.b64encode(data).decode()
    faces.append("@font-face{font-family:'Armin Grotesk';font-weight:%d;font-display:swap;"
                 "src:url(data:font/otf;base64,%s) format('opentype');}" % (weight, b64))
FONT_FACES = "\n".join(faces)


def _svg(path):
    return open(os.path.join(ASSETS, "logo", path)).read().split("?>", 1)[-1].strip()
LOGO_COLOR, LOGO_DARK = _svg("perpetual-color.svg"), _svg("perpetual-dark.svg")

# --- tokens ---
ACCENT, ACCENT2, YELLOW = "#1a56db", "#f97316", "#fbb900"
BGD, TEXT, DIM, MUTED = "#0b1220", "#111827", "#374151", "#6b7280"
SURFACE, SURFACE2, BORDER, WHITE, DBE4FF = "#f8f9fc", "#eef1f8", "#dde1ef", "#ffffff", "#dbe4ff"
GREEN, PURPLE = "#059669", "#7e22ce"
# paleta de datos
DATA = [ACCENT, ACCENT2, GREEN, YELLOW, PURPLE, MUTED]
PXIN = 96


def _p(v):
    return f"{v * PXIN:.1f}px"


def box(x, y, w, h, fill=None, r=0, oval=False, shadow=False, line=None):
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
    st += "border-radius:50%;" if oval else (f"border-radius:{r}px;" if r else "")
    if fill: st += f"background:{fill};"
    if line: st += f"border:1px solid {line};"
    if shadow: st += "box-shadow:0 8px 26px rgba(20,40,90,.13);"
    return f'<div style="{st}"></div>'


def txt(x, y, w, h, content, size, color=TEXT, weight=400, align="left",
        valign="top", spacing=None, upper=False, lh=1.1):
    just = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}[valign]
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
          f"display:flex;flex-direction:column;justify-content:{just};overflow:hidden;"
          f"font-size:{size*1.333:.1f}px;color:{color};font-weight:{weight};"
          f"text-align:{align};line-height:{lh};")
    if align == "center": st += "align-items:center;"
    if spacing: st += f"letter-spacing:{spacing}px;"
    if upper: st += "text-transform:uppercase;"
    return f'<div style="{st}">{content}</div>'


def logo(x, y, w, dark=False):
    svg = LOGO_DARK if dark else LOGO_COLOR
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};"
    return f'<div class="lg" style="{st}">{svg}</div>'


def hexagon(x, y, size, fill):
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(size)};height:{_p(size)};"
          f"background:{fill};clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%);")
    return f'<div style="{st}"></div>'


def blob(x, y, d, fill):
    return box(x, y, d, d, fill=fill, oval=True)


def pill(x, y, w, label, fill=ACCENT, fg=WHITE, arrow=True):
    out = [box(x, y, w, 0.62, fill=fill, r=31, shadow=True),
           txt(x + 0.34, y, w - 1.0, 0.62, label, 11.5, fg, 600, "left", "middle",
               spacing=0.8, upper=True)]
    if arrow:
        out.append(box(x + w - 0.74, y + 0.1, 0.42, 0.42, fill=WHITE, oval=True))
        out.append(txt(x + w - 0.74, y + 0.02, 0.42, 0.42, "&rsaquo;", 17, fill, 800, "center", "middle"))
    return "".join(out)


def graphic(x, y, w, h, tint="#DBE7FB", variant="abstract", r=12, shadow=False):
    """Grafico de marca (en vez de foto): composicion abstracta on-brand."""
    out = [box(x, y, w, h, fill=tint, r=r, shadow=shadow)]
    cx, cy = x + w / 2, y + h / 2
    if variant == "growth":
        n, bw, gap = 4, w * 0.13, w * 0.06
        total = n * bw + (n - 1) * gap
        bx, base = cx - total / 2, y + h * 0.8
        cols = [ACCENT, ACCENT2, YELLOW, ACCENT]
        for i in range(n):
            bh = h * (0.16 + 0.13 * i)
            out.append(box(bx + i * (bw + gap), base - bh, bw, bh, fill=cols[i], r=4))
        out.append(box(cx - w * 0.3, y + h * 0.16, h * 0.2, h * 0.2, fill=ACCENT, oval=True))
        out.append(hexagon(cx + w * 0.16, y + h * 0.14, h * 0.16, YELLOW))
    elif variant == "quote":
        out.append(txt(x, y + h * 0.06, w, h * 0.45, "&ldquo;", 92, ACCENT, 800, "center"))
        out.append(txt(x, y + h * 0.62, w, h * 0.2,
                       "&#9733; &#9733; &#9733; &#9733; &#9733;", 17, YELLOW, 700, "center"))
    else:  # abstract: circulos + hexagono de marca
        out.append(box(cx - w * 0.28, cy - h * 0.16, h * 0.34, h * 0.34, fill=ACCENT, oval=True))
        out.append(box(cx + w * 0.03, cy - h * 0.02, h * 0.22, h * 0.22, fill=ACCENT2, oval=True))
        out.append(box(cx - w * 0.02, cy + h * 0.16, h * 0.13, h * 0.13, fill=YELLOW, oval=True))
        out.append(hexagon(cx + w * 0.12, cy - h * 0.26, h * 0.17, WHITE))
    return "".join(out)


def title(runs, x=0.7, y=0.7, w=8.5, size=33):
    return logo(0.6, 0.5, 1.15) + txt(x, y + 0.55, w, 1.2, runs, size, TEXT, 800, lh=1.0)


def footer(page, dark=False):
    fg = DBE4FF if dark else MUTED
    return (logo(0.55, 7.02, 0.92, dark=dark)
            + txt(1.75, 7.0, 7, 0.3, "Confidencial &middot; Perpetual Technologies &copy; 2026",
                  8.5, fg, 400, "left", "middle")
            + txt(11.7, 7.0, 1.1, 0.3, str(page).zfill(2), 8.5, fg, 400, "right", "middle"))


def AC(t):  # helper: envuelve en span de acento
    return f'<span style="color:{ACCENT}">{t}</span>'


# ===========================================================================
# Helpers de graficas
# ===========================================================================
def progress_bar(x, y, w, pct, fill=ACCENT, track=SURFACE2):
    """Barra de progreso horizontal con porcentaje al final."""
    bh = 0.34
    return (box(x, y, w, bh, fill=track, r=int(bh * PXIN / 2))
            + box(x, y, w * pct / 100, bh, fill=fill, r=int(bh * PXIN / 2))
            + txt(x + w + 0.18, y, 0.95, bh, f"{pct}%", 13, TEXT, 800, "left", "middle"))


def donut(cx, cy, r, pct, fill=ACCENT, track=SURFACE2, label=None, thick=0.18):
    """Donut chart (un solo valor) usando conic-gradient. cx,cy = centro."""
    d = r * 2
    deg = pct / 100 * 360
    hole = d - thick * 2
    st = (f"position:absolute;left:{_p(cx-r)};top:{_p(cy-r)};width:{_p(d)};height:{_p(d)};"
          f"border-radius:50%;background:conic-gradient({fill} 0 {deg:.1f}deg,{track} {deg:.1f}deg 360deg);")
    out = [f'<div style="{st}"></div>',
           box(cx - hole / 2, cy - hole / 2, hole, hole, fill=WHITE, oval=True),
           txt(cx - r, cy - 0.22, d, 0.44, f"{pct}%", 14, TEXT, 800, "center", "middle")]
    if label:
        out.append(txt(cx - r - 0.3, cy + r + 0.08, d + 0.6, 0.3, label, 10, MUTED, 600, "center", upper=True, spacing=0.4))
    return "".join(out)


def bubble(cx, cy, d, fill, pct=None, fg=WHITE):
    """Burbuja (circulo proporcional) con porcentaje centrado."""
    out = [box(cx - d / 2, cy - d / 2, d, d, fill=fill, oval=True)]
    if pct is not None:
        out.append(txt(cx - d / 2, cy - 0.22, d, 0.44, pct, min(22, d * 14), fg, 800, "center", "middle"))
    return "".join(out)


def hex_icon(x, y, size, fill, inner=WHITE):
    """Icono hexagonal de marca (avatar abstracto, NUNCA caras)."""
    return hexagon(x, y, size, fill) + hexagon(x + size * 0.28, y + size * 0.28, size * 0.44, inner)


def avatar(x, y, d, initials, fill=ACCENT, fg=WHITE):
    """Avatar circular con iniciales (NUNCA fotos de personas)."""
    return (box(x, y, d, d, fill=fill, oval=True)
            + txt(x, y, d, d, initials, d * 13, fg, 800, "center", "middle"))


# ===========================================================================
# Slides
# ===========================================================================
def s01_portada():
    return (box(0, 4.7, 13.333, 2.8, fill=ACCENT)
            + blob(9.2, -1.0, 3.2, YELLOW) + blob(11.7, 2.0, 1.9, ACCENT2)
            + blob(8.2, 1.3, 3.3, ACCENT) + hexagon(8.75, 2.05, 2.1, WHITE)
            + box(9.45, 2.75, 0.7, 0.7, fill=ACCENT, oval=True) + blob(11.5, 4.45, 0.8, YELLOW)
            + logo(0.7, 0.7, 1.6)
            + txt(0.65, 1.65, 7.6, 1.6, AC("Perpetual."), 84, TEXT, 800, lh=0.95)
            + txt(0.7, 3.35, 7.2, 0.5, "Plantilla de presentacion de negocio", 17, DIM, 600)
            + txt(0.7, 3.95, 6.6, 0.6, "Marco ejecutivo para construir propuestas, planes y reportes con marca Perpetual.",
                  12.5, MUTED, 400, lh=1.3)
            + pill(0.7, 5.55, 3.1, "Comenzar", fill=WHITE, fg=ACCENT)
            + txt(9.0, 5.6, 3.7, 0.4, "Junio 2026", 12, WHITE, 600, "right"))


def s02_contenido():
    out = [title(f"Tabla de {AC('contenidos.')}"),
           txt(0.7, 1.9, 6.5, 0.5, "Recorrido completo del negocio en seis bloques.", 13, MUTED, 400)]
    items = [("01", "Resumen de negocio"), ("02", "Analisis de mercado"), ("03", "Ventas"),
             ("04", "Plan de gestion"), ("05", "Plan operativo"), ("06", "Plan financiero")]
    cols = DATA
    for i, (n, t) in enumerate(items):
        col = i % 2
        row = i // 2
        x = 0.7 + col * 6.2
        y = 2.7 + row * 1.35
        out += [box(x, y, 5.9, 1.1, fill=SURFACE, r=14, line=BORDER),
                box(x + 0.28, y + 0.25, 0.6, 0.6, fill=cols[i], r=12),
                txt(x + 0.28, y + 0.25, 0.6, 0.6, n, 15, WHITE, 800, "center", "middle"),
                txt(x + 1.1, y, 4.6, 1.1, t, 15, TEXT, 600, "left", "middle")]
    out.append(footer(2))
    return "".join(out)


def s03_divisor():
    return (box(0, 0, 4.9, 7.5, fill=BGD)
            + blob(-0.8, 5.2, 2.6, ACCENT) + hexagon(3.2, 0.7, 1.3, ACCENT2)
            + logo(0.7, 0.6, 1.5, dark=True)
            + txt(0.7, 2.0, 4.0, 2.2, "01", 150, ACCENT, 800, lh=0.9)
            + txt(0.7, 4.4, 3.6, 0.4, "Seccion", 12, DBE4FF, 600, upper=True, spacing=1)
            + txt(5.8, 2.6, 6.8, 1.2, f"Resumen de {AC('negocio.')}", 44, TEXT, 800, lh=1.0)
            + txt(5.8, 3.95, 6.4, 1.4,
                  "Quienes somos, que problema resolvemos y como creamos valor. Una vision clara del modelo "
                  "antes de entrar en detalle.", 14, MUTED, 400, lh=1.4)
            + txt(11.7, 7.0, 1.1, 0.3, "03", 8.5, MUTED, 400, "right", "middle"))


def s04_mision():
    return (title(f"Nuestra {AC('mision.')}")
            + blob(10.2, 1.0, 2.6, YELLOW) + hexagon(10.8, 1.7, 1.4, ACCENT)
            + box(0.7, 2.4, 8.6, 3.7, fill=SURFACE2, r=18)
            + txt(1.15, 2.85, 1.5, 1.0, "&ldquo;", 80, ACCENT, 800)
            + txt(1.2, 3.55, 7.6, 2.2,
                  "Impulsar el crecimiento sostenible de las empresas de Latinoamerica con tecnologia, "
                  "datos y diseno, convirtiendo la complejidad operativa en ventaja competitiva.",
                  20, TEXT, 600, lh=1.35)
            + txt(1.2, 5.45, 7.0, 0.4, "Comite de Direccion &middot; Perpetual Technologies", 11.5, MUTED, 600, upper=True, spacing=0.6)
            + txt(10.0, 3.0, 2.6, 0.4, "Valores", 11, ACCENT, 700, upper=True, spacing=0.8)
            + txt(10.0, 3.5, 2.8, 0.4, "Rigor analitico", 13, TEXT, 600)
            + txt(10.0, 4.0, 2.8, 0.4, "Cercania con el cliente", 13, TEXT, 600)
            + txt(10.0, 4.5, 2.8, 0.4, "Resultados medibles", 13, TEXT, 600)
            + footer(4))


def s05_empresa():
    out = [title(f"Nuestra {AC('empresa.')}"),
           txt(0.7, 1.95, 6.5, 1.6,
               "Perpetual Technologies acompana a empresas en su transformacion digital: estrategia, "
               "automatizacion y analitica en un mismo socio. Operamos desde 2019 con equipos en Lima, "
               "Bogota y Ciudad de Mexico.", 14, DIM, 400, lh=1.4),
           graphic(7.7, 2.1, 4.9, 3.6, tint="#DBE7FB", variant="abstract", r=18, shadow=True)]
    tags = [("Area de negocio", "Consultoria y software B2B", ACCENT),
            ("Ingresos 2025", "USD 4.8M", GREEN)]
    for i, (t, v, col) in enumerate(tags):
        x = 0.7 + i * 3.4
        out += [box(x, 4.3, 3.2, 1.5, fill=SURFACE, r=14, line=BORDER),
                box(x, 4.3, 0.12, 1.5, fill=col, r=6),
                txt(x + 0.35, 4.55, 2.7, 0.4, t, 10.5, MUTED, 700, upper=True, spacing=0.6),
                txt(x + 0.35, 4.95, 2.7, 0.7, v, 17, TEXT, 800, lh=1.05)]
    out.append(footer(5))
    return "".join(out)


def s06_tendencias():
    out = [title(f"Tendencias de {AC('mercado.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Tres fuerzas que redefinen la demanda en nuestro sector.", 13, MUTED, 400)]
    rows = [("Adopcion de IA en empresas", 50, ACCENT,
             "La mitad de las companias ya pilotea casos de uso de IA."),
            ("Migracion a la nube", 85, GREEN,
             "Mayoria de cargas criticas operan en plataformas cloud."),
            ("Demanda de automatizacion", 70, ACCENT2,
             "Procesos manuales en reduccion acelerada ano tras ano.")]
    for i, (t, pct, col, d) in enumerate(rows):
        y = 2.8 + i * 1.35
        out += [hex_icon(0.7, y - 0.05, 0.78, col),
                txt(1.85, y - 0.1, 7.0, 0.4, t, 14, TEXT, 700),
                progress_bar(1.85, y + 0.4, 8.6, pct, fill=col),
                txt(1.85, y + 0.82, 9.0, 0.4, d, 10.5, MUTED, 400)]
    out.append(footer(6))
    return "".join(out)


def s07_competidores():
    out = [title(f"Mapa de {AC('competidores.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Cuatro actores principales en el segmento objetivo.", 13, MUTED, 400)]
    comps = [("Empresa 1", "Lider en consultoria tradicional, fuerte en grandes cuentas.", ACCENT),
             ("Empresa 2", "Plataforma de automatizacion con enfoque self-service.", ACCENT2),
             ("Empresa 3", "Boutique de datos especializada en retail y banca.", GREEN),
             ("Empresa 4", "Integrador regional con amplia red de partners.", PURPLE)]
    for i, (n, d, col) in enumerate(comps):
        x = 0.7 + i * 3.05
        out += [box(x, 2.7, 2.85, 3.4, fill=SURFACE, r=16, line=BORDER, shadow=True),
                box(x, 2.7, 2.85, 0.14, fill=col, r=6),
                hex_icon(x + 0.35, 3.15, 0.85, col),
                txt(x + 0.35, 4.25, 2.2, 0.4, n, 15, TEXT, 800),
                txt(x + 0.35, 4.7, 2.2, 1.2, d, 11, MUTED, 400, lh=1.35)]
    out.append(footer(7))
    return "".join(out)


def s08_vs():
    out = [title(f"Nosotros {AC('vs ellos.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Como nos comparamos en las metricas que importan.", 13, MUTED, 400)]
    panels = [("Nosotros", ACCENT, 0.7, [("Satisfaccion", 94, ACCENT), ("Retencion", 88, GREEN), ("Tiempo a valor", 82, ACCENT2)]),
              ("Ellos", MUTED, 6.85, [("Satisfaccion", 71, MUTED), ("Retencion", 65, MUTED), ("Tiempo a valor", 58, MUTED)])]
    for label, hdr, x, metrics in panels:
        out += [box(x, 2.65, 5.75, 3.6, fill=SURFACE if label == "Ellos" else "#eef3fe", r=18,
                    line=BORDER if label == "Ellos" else None),
                box(x + 0.4, 2.95, 2.6, 0.5, fill=hdr, r=12),
                txt(x + 0.4, 2.95, 2.6, 0.5, label, 12, WHITE, 700, "center", "middle", upper=True, spacing=0.8)]
        for j, (mt, pct, col) in enumerate(metrics):
            dx = x + 1.4 + j * 1.55
            out += [donut(dx, 4.55, 0.55, pct, fill=col, label=mt)]
    out.append(footer(8))
    return "".join(out)


def s09_tamano():
    out = [title(f"Tamano de {AC('mercado.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Participacion estimada por actor en el mercado direccionable.", 13, MUTED, 400)]
    # burbujas: (cx, cy, d, fill, pct)
    bubbles = [(5.0, 4.1, 2.4, ACCENT, "40%"), (8.0, 3.4, 1.7, ACCENT2, "25%"),
               (9.9, 5.0, 1.55, GREEN, "20%"), (6.9, 5.6, 1.2, PURPLE, "15%")]
    for cx, cy, d, fill, pct in bubbles:
        out.append(bubble(cx, cy, d, fill, pct))
    # leyenda
    legend = [("Empresa 1", ACCENT), ("Empresa 2", ACCENT2), ("Empresa 3", GREEN), ("Empresa 4", PURPLE)]
    for i, (n, col) in enumerate(legend):
        y = 2.9 + i * 0.62
        out += [box(0.75, y, 0.28, 0.28, fill=col, r=6),
                txt(1.2, y - 0.06, 2.6, 0.4, n, 12.5, TEXT, 600, "left", "middle")]
    out.append(txt(0.75, 5.6, 3.0, 0.8, "Mercado direccionable estimado en USD 320M para 2027.",
                   11, MUTED, 400, lh=1.35))
    out.append(footer(9))
    return "".join(out)


def s10_precios():
    out = [title(f"Planes de {AC('precios.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Estructura modular pensada para cada etapa del cliente.", 13, MUTED, 400)]
    plans = [
        ("Gratis", "$0", "/mes", False, ["Diagnostico inicial", "1 usuario", "Reportes basicos", "Soporte por correo"]),
        ("Estandar", "$20", "/mes", True, ["Todo lo de Gratis", "5 usuarios", "Dashboards en vivo", "Automatizaciones", "Soporte prioritario"]),
        ("Avanzado", "$35", "/mes", False, ["Todo lo de Estandar", "Usuarios ilimitados", "Integraciones API", "Gerente de cuenta"]),
    ]
    for i, (name, price, per, hl, feats) in enumerate(plans):
        x = 0.7 + i * 4.1
        fill = ACCENT if hl else WHITE
        fg = WHITE if hl else TEXT
        sub = DBE4FF if hl else MUTED
        out += [box(x, 2.55, 3.7, 4.05, fill=fill, r=18, shadow=True, line=None if hl else BORDER)]
        if hl:
            out += [box(x + 1.25, 2.3, 1.2, 0.42, fill=YELLOW, r=10),
                    txt(x + 1.25, 2.3, 1.2, 0.42, "Popular", 9.5, BGD, 800, "center", "middle", upper=True, spacing=0.6)]
        out += [txt(x + 0.45, 2.85, 3.0, 0.4, name, 14, sub, 700, upper=True, spacing=0.8),
                txt(x + 0.45, 3.25, 3.0, 0.8, price, 42, fg, 800),
                txt(x + 0.45 + (1.6 if len(price) == 2 else 1.95), 3.62, 1.0, 0.4, per, 12, sub, 600)]
        for j, f in enumerate(feats):
            fy = 4.3 + j * 0.36
            dot = WHITE if hl else ACCENT
            out += [box(x + 0.45, fy + 0.07, 0.13, 0.13, fill=dot, oval=True),
                    txt(x + 0.72, fy - 0.02, 2.8, 0.34, f, 10.8, fg if hl else DIM, 400)]
        bfill = WHITE if hl else ACCENT
        bfg = ACCENT if hl else WHITE
        out.append(pill(x + 0.45, 6.0, 2.8, "Elegir plan", fill=bfill, fg=bfg, arrow=False))
    out.append(footer(10))
    return "".join(out)


def s11_equipo():
    out = [title(f"Nuestro {AC('equipo.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Liderazgo multidisciplinario con foco en ejecucion.", 13, MUTED, 400)]
    members = [("Ana Rojas", "Directora General", "AR", ACCENT),
               ("Luis Vega", "Director de Tecnologia", "LV", GREEN),
               ("Mara Diaz", "Directora de Operaciones", "MD", ACCENT2)]
    for i, (n, role, ini, col) in enumerate(members):
        x = 0.85 + i * 4.05
        out += [box(x, 2.7, 3.55, 3.5, fill=SURFACE, r=18, line=BORDER, shadow=True),
                avatar(x + 1.15, 3.15, 1.25, ini, fill=col),
                txt(x, 4.6, 3.55, 0.4, n, 16, TEXT, 800, "center"),
                txt(x, 5.05, 3.55, 0.4, role, 11.5, ACCENT, 600, "center", upper=True, spacing=0.4),
                txt(x + 0.45, 5.5, 2.65, 0.6, "Mas de 10 anos liderando equipos en la region.",
                    10.5, MUTED, 400, "center", lh=1.3)]
    out.append(footer(11))
    return "".join(out)


def s12_testimonios():
    out = [title(f"Lo que dicen {AC('los clientes.')}"),
           txt(0.7, 1.9, 8.0, 0.5, "Resultados reales de companias que confiaron en Perpetual.", 13, MUTED, 400)]
    quotes = [
        ("Reducimos el tiempo de cierre mensual de diez dias a dos. El equipo de Perpetual entendio "
         "nuestro negocio desde la primera semana.", "Carla Mendoza", "CFO, Grupo Andina", ACCENT),
        ("La automatizacion de reportes nos devolvio horas cada semana y mejoro la calidad de las "
         "decisiones de direccion.", "Diego Salas", "COO, Logistica del Pacifico", GREEN),
    ]
    for i, (q, name, role, col) in enumerate(quotes):
        x = 0.7 + i * 6.2
        out += [box(x, 2.6, 5.9, 3.7, fill=SURFACE, r=18, line=BORDER, shadow=True),
                txt(x + 0.45, 2.7, 2.0, 1.0, "&ldquo;", 78, col, 800),
                txt(x + 0.5, 3.65, 5.0, 1.6, q, 14, TEXT, 600, lh=1.4),
                box(x + 0.5, 5.55, 0.55, 0.55, fill=col, oval=True),
                txt(x + 0.5, 5.55, 0.55, 0.55, "".join(w[0] for w in name.split()[:2]), 13, WHITE, 800, "center", "middle"),
                txt(x + 1.25, 5.5, 4.4, 0.35, name, 13, TEXT, 800),
                txt(x + 1.25, 5.85, 4.4, 0.35, role, 10.5, MUTED, 600, upper=True, spacing=0.4)]
    out.append(footer(12))
    return "".join(out)


SLIDES = [s01_portada, s02_contenido, s03_divisor, s04_mision, s05_empresa, s06_tendencias,
          s07_competidores, s08_vs, s09_tamano, s10_precios, s11_equipo, s12_testimonios]
stages = "\n".join(f'<div class="slide">{fn()}</div>' for fn in SLIDES)

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perpetual &middot; Business Deck</title>
<style>
{FONT_FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#c9ccd6;font-family:'Armin Grotesk',system-ui,sans-serif;padding:30px 0}}
.deck{{width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:24px}}
.slide{{position:relative;width:1280px;height:720px;background:#fff;overflow:hidden;
  border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.18)}}
.lg svg{{display:block;width:100%;height:auto}}
</style></head><body>
<div class="deck">
{stages}
</div>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK:", OUT, "|", round(len(HTML) / 1024), "KB |", len(SLIDES), "slides")
