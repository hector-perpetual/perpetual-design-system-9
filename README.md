# Perpetual Design System 9 — Business Deck (HTML)

Plantilla de presentacion de negocio autocontenida en HTML, con la marca de
**Perpetual Technologies**. Estilo ejecutivo, formal y minimalista (tipo
BCG / McKinsey). Inspirada en un deck de negocio completo, reinterpretada con
la paleta sobria de Perpetual.

## Que incluye

- `build_html.py` — generador en Python (sin dependencias externas) que produce
  un unico archivo HTML autocontenido.
- `assets/` — fuentes Armin Grotesk (embebidas en base64) y logos SVG inline.
- `perpetual-business-deck.html` — salida generada (se crea al ejecutar el script).

## Slides (12)

1. Portada
2. Tabla de contenidos (01–06)
3. Divisor "01 — Resumen de negocio"
4. Declaracion de mision
5. Nuestra empresa
6. Tendencias de mercado (barras de progreso)
7. Mapa de competidores
8. Nosotros vs ellos (donut charts)
9. Tamano de mercado (burbujas)
10. Planes de precios
11. Nuestro equipo (avatares con iniciales)
12. Testimonios de clientes

## Uso

```bash
python3 build_html.py
```

Esto genera `perpetual-business-deck.html`. Abrelo en cualquier navegador.
Cada slide mide 1280x720 px (coordenadas en pulgadas x 96).

## Marca

- Tipografia: solo Armin Grotesk.
- Fondos claros en blanco; oscuros en `#0b1220`.
- Logo Perpetual presente en todos los slides.
- Sin fotos de personas: los avatares son circulos con iniciales o iconos
  hexagonales.
- Paleta de datos: `#1a56db`, `#f97316`, `#059669`, `#fbb900`, `#7e22ce`, `#6b7280`.
