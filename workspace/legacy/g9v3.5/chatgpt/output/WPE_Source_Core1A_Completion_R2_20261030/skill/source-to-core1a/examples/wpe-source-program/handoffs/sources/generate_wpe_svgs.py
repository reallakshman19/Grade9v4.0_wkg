#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates 10 high-fidelity, WCAG-compliant SVG diagrams for the Work, Energy and Power curriculum.
Strict compliance with svg_generator.validate_svg:
- Well-formed XML with xmlns and viewBox
- role="img", non-empty aria-label, <title>, and <desc>
- Font size floor >= 14px on EVERY <text> element (declared explicitly via font-size attribute)
- High contrast color palette (#1e293b, #2563eb, #dc2626, #16a34a, #d97706)
- Physical and geometric fidelity to source textbook / illustrations
"""

import sys
from pathlib import Path

# Add skill scripts directory to sys.path
SKILL_SCRIPTS = Path(r"C:\Users\reall\Documents\antigravity\kind-carson\.agents\skills\olympiad-web-harvester\scripts")
if str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS))

from svg_generator import validate_svg

OUT_DIR = Path(r"D:\CodeD\g9v3.5\work_energy_power_extracted\images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def save_and_validate(filename: str, svg_content: str):
    target = OUT_DIR / filename
    target.write_text(svg_content.strip(), encoding="utf-8")
    
    # Verify strict validation
    valid, errors = validate_svg(svg_content)
    if not valid:
        raise ValueError(f"Validation failed for {filename}:\n" + "\n".join(errors))
    print(f"Validated SVG: {filename}")

# ==========================================
# 1. FIG 01: Positive Work (Acute Angle)
# ==========================================
FIG_01 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 320" width="100%" height="100%" role="img" aria-label="Positive Work: Force applied at acute angle to displacement">
  <title>Positive Work Done by Constant Force</title>
  <desc>A block on a horizontal surface is pulled by force F at an acute angle theta above horizontal, producing positive work W = F s cos(theta) > 0.</desc>
  <defs>
    <marker id="arr-blue-01" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arr-dark-01" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <pattern id="hatch-01" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" stroke-width="1.5" />
    </pattern>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Ground surface -->
  <line x1="60" y1="210" x2="590" y2="210" stroke="#1e293b" stroke-width="2.5" />
  <rect x="60" y="210" width="530" height="20" fill="url(#hatch-01)" />

  <!-- Block -->
  <rect x="190" y="120" width="140" height="90" fill="#eff6ff" stroke="#1e293b" stroke-width="2.5" rx="2" />
  <circle cx="260" cy="165" r="4" fill="#1e293b" />

  <!-- Horizontal reference line -->
  <line x1="260" y1="165" x2="400" y2="165" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5,4" />

  <!-- Force Vector F -->
  <line x1="260" y1="165" x2="385" y2="85" stroke="#2563eb" stroke-width="3" marker-end="url(#arr-blue-01)" />
  <text x="400" y="85" font-size="18px" class="bold" fill="#2563eb">F</text>

  <!-- Angle arc theta -->
  <path d="M 315 165 A 55 55 0 0 0 300 138" fill="none" stroke="#1e293b" stroke-width="2" />
  <text x="325" y="152" font-size="16px" class="math">&#952;</text>

  <!-- Direction of motion vector -->
  <line x1="420" y1="165" x2="530" y2="165" stroke="#1e293b" stroke-width="2.5" marker-end="url(#arr-dark-01)" />
  <text x="425" y="145" font-size="16px" class="bold">Direction of Motion</text>

  <!-- Explanatory Caption -->
  <text x="325" y="270" text-anchor="middle" font-size="16px" font-weight="600">Motion of block in direction of applied force (0&#176; &lt; &#952; &lt; 90&#176; &#8658; W = Fs cos&#952; &gt; 0)</text>
</svg>"""

# ==========================================
# 2. FIG 02: Negative Work (Obtuse Angle)
# ==========================================
FIG_02 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 320" width="100%" height="100%" role="img" aria-label="Negative Work: Force applied at obtuse angle to displacement">
  <title>Negative Work Done by Force</title>
  <desc>A block moving horizontally forward experiences a backward retarding force at an obtuse angle theta, resulting in negative work.</desc>
  <defs>
    <marker id="arr-red-02" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arr-dark-02" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <pattern id="hatch-02" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" stroke-width="1.5" />
    </pattern>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Ground surface -->
  <line x1="60" y1="210" x2="590" y2="210" stroke="#1e293b" stroke-width="2.5" />
  <rect x="60" y="210" width="530" height="20" fill="url(#hatch-02)" />

  <!-- Block -->
  <rect x="250" y="120" width="140" height="90" fill="#fef2f2" stroke="#1e293b" stroke-width="2.5" rx="2" />
  <circle cx="320" cy="165" r="4" fill="#1e293b" />

  <!-- Forward reference line -->
  <line x1="320" y1="165" x2="450" y2="165" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5,4" />

  <!-- Force Vector F backwards at obtuse angle -->
  <line x1="320" y1="165" x2="190" y2="85" stroke="#dc2626" stroke-width="3" marker-end="url(#arr-red-02)" />
  <text x="170" y="85" font-size="18px" class="bold" fill="#dc2626">F</text>

  <!-- Obtuse angle arc from horizontal around to F vector -->
  <path d="M 380 165 A 60 60 0 0 0 255 125" fill="none" stroke="#1e293b" stroke-width="2" />
  <text x="315" y="85" font-size="16px" class="math">&#952;</text>

  <!-- Direction of motion vector -->
  <line x1="450" y1="165" x2="560" y2="165" stroke="#1e293b" stroke-width="2.5" marker-end="url(#arr-dark-02)" />
  <text x="455" y="145" font-size="16px" class="bold">Direction of Motion</text>

  <!-- Caption -->
  <text x="325" y="270" text-anchor="middle" font-size="16px" font-weight="600">Motion of block (Obtuse angle 90&#176; &lt; &#952; &#8804; 180&#176; &#8658; W = Fs cos&#952; &lt; 0)</text>
</svg>"""

# ==========================================
# 3. FIG 03: Free Body Diagram - String Raising (Illustration 2)
# ==========================================
FIG_03 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 380" width="100%" height="100%" role="img" aria-label="Free Body Diagram: Block raised by string tension with upward acceleration">
  <title>Free Body Diagram of Upward Accelerating Block</title>
  <desc>A mass m experiencing upward string tension T and downward gravitational force mg, accelerating upward with acceleration a.</desc>
  <defs>
    <marker id="arr-dark-03" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <marker id="arr-blue-03" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arr-red-03" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arr-green-03" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a"/>
    </marker>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Block of mass m -->
  <rect x="150" y="140" width="100" height="90" fill="#f8fafc" stroke="#1e293b" stroke-width="2.5" rx="3" />
  <text x="200" y="192" font-size="20px" text-anchor="middle" font-weight="bold">m</text>

  <!-- Tension vector T (upwards) -->
  <line x1="200" y1="140" x2="200" y2="40" stroke="#2563eb" stroke-width="3" marker-end="url(#arr-blue-03)" />
  <text x="215" y="55" font-size="18px" class="bold" fill="#2563eb">T</text>

  <!-- Gravity vector mg (downwards) -->
  <line x1="200" y1="230" x2="200" y2="330" stroke="#dc2626" stroke-width="3" marker-end="url(#arr-red-03)" />
  <text x="215" y="325" font-size="18px" class="bold" fill="#dc2626">mg</text>

  <!-- Acceleration vector a (upwards alongside) -->
  <line x1="280" y1="210" x2="280" y2="120" stroke="#16a34a" stroke-width="2.5" marker-end="url(#arr-green-03)" />
  <text x="295" y="165" font-size="18px" class="bold" fill="#16a34a">a</text>

  <!-- Caption -->
  <text x="210" y="365" font-size="15px" text-anchor="middle" font-weight="600">Free Body Diagram: T - mg = ma</text>
</svg>"""

# ==========================================
# 4. FIG 04: Work Done by Variable Force (Calculus & Riemann sum)
# ==========================================
FIG_04 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 360" width="100%" height="100%" role="img" aria-label="Work Done by a Variable Force: Calculus Integral and Riemann Sum">
  <title>Calculus Derivation of Work Done by Variable Force</title>
  <desc>Two plots illustrating the continuous integral under F(x) and its discretization into narrow rectangular strips of width Delta x.</desc>
  <defs>
    <marker id="arr-axis-04" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .axis-label { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Left Graph: Continuous Area -->
  <g transform="translate(40, 20)">
    <!-- Axes -->
    <line x1="50" y1="260" x2="320" y2="260" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-axis-04)" />
    <line x1="50" y1="260" x2="50" y2="30" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-axis-04)" />
    <text x="330" y="265" font-size="16px" class="math">x</text>
    <text x="45" y="25" font-size="16px" class="axis-label" text-anchor="end">F(x)</text>
    <text x="35" y="275" font-size="15px">O</text>

    <!-- Shaded continuous area under curve -->
    <path d="M 100 260 L 100 200 Q 180 180 260 70 L 260 260 Z" fill="#dbeafe" />

    <!-- Curve F(x) -->
    <path d="M 70 215 Q 160 190 280 50" fill="none" stroke="#2563eb" stroke-width="3" />

    <!-- Dashed boundary lines -->
    <line x1="100" y1="260" x2="100" y2="200" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4" />
    <line x1="260" y1="260" x2="260" y2="70" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4" />

    <text x="100" y="280" font-size="16px" text-anchor="middle" class="math">x_i</text>
    <text x="260" y="280" font-size="16px" text-anchor="middle" class="math">x_f</text>
    <text x="180" y="160" font-size="15px" text-anchor="middle" fill="#1e40af" font-weight="600">Area = W</text>
    <text x="180" y="320" font-size="15px" text-anchor="middle" font-weight="600">(a) Continuous Work Integral</text>
  </g>

  <!-- Right Graph: Discretized Riemann Rectangles -->
  <g transform="translate(410, 20)">
    <!-- Axes -->
    <line x1="50" y1="260" x2="320" y2="260" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-axis-04)" />
    <line x1="50" y1="260" x2="50" y2="30" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-axis-04)" />
    <text x="330" y="265" font-size="16px" class="math">x</text>
    <text x="45" y="25" font-size="16px" class="axis-label" text-anchor="end">F(x)</text>
    <text x="35" y="275" font-size="15px">O</text>

    <!-- Discretized Rectangles -->
    <rect x="100" y="195" width="20" height="65" fill="#f1f5f9" stroke="#64748b" stroke-width="1" />
    <rect x="120" y="185" width="20" height="75" fill="#f1f5f9" stroke="#64748b" stroke-width="1" />
    <rect x="140" y="170" width="20" height="90" fill="#f1f5f9" stroke="#64748b" stroke-width="1" />
    <rect x="160" y="150" width="20" height="110" fill="#f1f5f9" stroke="#64748b" stroke-width="1" />
    <!-- Highlighted strip abcd -->
    <rect x="180" y="125" width="24" height="135" fill="#fef08a" stroke="#ca8a04" stroke-width="2" />
    <text x="182" y="120" font-size="14px" font-weight="bold">a</text>
    <text x="202" y="120" font-size="14px" font-weight="bold">b</text>
    <text x="202" y="255" font-size="14px" font-weight="bold">c</text>
    <text x="182" y="255" font-size="14px" font-weight="bold">d</text>

    <rect x="204" y="95" width="20" height="165" fill="#f1f5f9" stroke="#64748b" stroke-width="1" />
    <rect x="224" y="65" width="20" height="195" fill="#f1f5f9" stroke="#64748b" stroke-width="1" />

    <!-- Curve F(x) overlay -->
    <path d="M 70 215 Q 160 190 280 50" fill="none" stroke="#2563eb" stroke-width="2.5" />

    <!-- Labels for strip -->
    <line x1="180" y1="290" x2="204" y2="290" stroke="#1e293b" stroke-width="1.5" />
    <line x1="180" y1="285" x2="180" y2="295" stroke="#1e293b" stroke-width="1.5" />
    <line x1="204" y1="285" x2="204" y2="295" stroke="#1e293b" stroke-width="1.5" />
    <text x="192" y="310" font-size="16px" text-anchor="middle" class="math">&#916;x</text>

    <text x="100" y="280" font-size="16px" text-anchor="middle" class="math">x_i</text>
    <text x="244" y="280" font-size="16px" text-anchor="middle" class="math">x_f</text>
    <text x="180" y="340" font-size="15px" text-anchor="middle" font-weight="600">(b) Riemann Sum Approximation</text>
  </g>
</svg>"""

# ==========================================
# 5. FIG 05: Opposing Friction Direction (Horizontal Track)
# ==========================================
FIG_05 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 300" width="100%" height="100%" role="img" aria-label="Friction Direction: Friction always opposes relative velocity">
  <title>Direction of Friction for Forward and Backward Motion</title>
  <desc>Two blocks on a rough track of length l: left block moving right has friction to left; right block moving left has friction to right.</desc>
  <defs>
    <marker id="arr-dark-05" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <marker id="arr-red-05" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arr-blue-05" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <pattern id="hatch-05" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" stroke-width="1.5" />
    </pattern>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Ground track -->
  <line x1="40" y1="180" x2="700" y2="180" stroke="#1e293b" stroke-width="2.5" />
  <rect x="40" y="180" width="660" height="18" fill="url(#hatch-05)" />

  <!-- Left Block (Moving Right) -->
  <g transform="translate(140, 100)">
    <rect x="0" y="0" width="80" height="80" fill="#eff6ff" stroke="#1e293b" stroke-width="2.5" rx="2" />
    <circle cx="40" cy="40" r="3.5" fill="#1e293b" />

    <!-- Normal N up / Weight mg down -->
    <line x1="40" y1="-10" x2="40" y2="-45" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arr-blue-05)" />
    <text x="48" y="-30" font-size="16px" class="bold" fill="#2563eb">N</text>

    <line x1="40" y1="80" x2="40" y2="125" stroke="#1e293b" stroke-width="2.5" marker-end="url(#arr-dark-05)" />
    <text x="48" y="115" font-size="16px" class="bold">mg</text>

    <!-- Velocity arrow right -->
    <line x1="90" y1="35" x2="145" y2="35" stroke="#16a34a" stroke-width="2.5" marker-end="url(#arr-dark-05)" />
    <text x="110" y="25" font-size="16px" class="bold" fill="#16a34a">v</text>

    <!-- Friction f left -->
    <line x1="0" y1="40" x2="-55" y2="40" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red-05)" />
    <text x="-75" y="45" font-size="18px" class="bold" fill="#dc2626">f</text>
  </g>

  <!-- Right Block (Moving Left) -->
  <g transform="translate(500, 100)">
    <rect x="0" y="0" width="80" height="80" fill="#fef2f2" stroke="#1e293b" stroke-width="2.5" rx="2" />
    <circle cx="40" cy="40" r="3.5" fill="#1e293b" />

    <!-- Normal N up / Weight mg down -->
    <line x1="40" y1="-10" x2="40" y2="-45" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arr-blue-05)" />
    <text x="48" y="-30" font-size="16px" class="bold" fill="#2563eb">N</text>
    <line x1="40" y1="80" x2="40" y2="125" stroke="#1e293b" stroke-width="2.5" marker-end="url(#arr-dark-05)" />
    <text x="48" y="115" font-size="16px" class="bold">mg</text>

    <!-- Velocity arrow left -->
    <line x1="-10" y1="35" x2="-65" y2="35" stroke="#16a34a" stroke-width="2.5" marker-end="url(#arr-dark-05)" />
    <text x="-45" y="25" font-size="16px" class="bold" fill="#16a34a">v</text>

    <!-- Friction f right -->
    <line x1="80" y1="40" x2="135" y2="40" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red-05)" />
    <text x="145" y="45" font-size="18px" class="bold" fill="#dc2626">f</text>
  </g>

  <!-- Dimension line for distance l between blocks -->
  <line x1="220" y1="215" x2="500" y2="215" stroke="#64748b" stroke-width="1.5" />
  <line x1="220" y1="208" x2="220" y2="222" stroke="#64748b" stroke-width="1.5" />
  <line x1="500" y1="208" x2="500" y2="222" stroke="#64748b" stroke-width="1.5" />
  <text x="360" y="235" font-size="16px" text-anchor="middle" class="math">l</text>

  <!-- Caption -->
  <text x="370" y="275" font-size="16px" text-anchor="middle" font-weight="600">Friction Always Opposes Relative Velocity: W_f = -&#956;mgl</text>
</svg>"""

# ==========================================
# 6. FIG 06: Block Sliding Down Incline (Illustration 4 Setup)
# ==========================================
FIG_06 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 550 340" width="100%" height="100%" role="img" aria-label="Block sliding down rough incline of 37 degrees">
  <title>Block on Inclined Plane</title>
  <desc>A 4 kg block sliding down an incline tilted at 37 degrees with sliding distance s = 3 meters and friction coefficient 0.2.</desc>
  <defs>
    <marker id="arr-dark-06" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <pattern id="hatch-06" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" stroke-width="1.5" />
    </pattern>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Ground -->
  <line x1="40" y1="250" x2="480" y2="250" stroke="#1e293b" stroke-width="2.5" />
  <rect x="40" y="250" width="440" height="18" fill="url(#hatch-06)" />

  <!-- Inclined Wedge: 37 degrees -->
  <polygon points="100,250 420,250 100,70" fill="#f8fafc" stroke="#1e293b" stroke-width="2.5" />

  <!-- Angle arc 37 degrees at vertex (420, 250) -->
  <path d="M 360 250 A 60 60 0 0 0 372 225" fill="none" stroke="#1e293b" stroke-width="2" />
  <text x="330" y="240" font-size="15px" font-weight="600">37&#176;</text>

  <!-- Block resting on incline: midpoint around (230, 143) -->
  <g transform="translate(230, 143) rotate(-37)">
    <rect x="-35" y="-50" width="70" height="50" fill="#dbeafe" stroke="#1e293b" stroke-width="2.5" rx="2" />
    <text x="0" y="-20" font-size="16px" text-anchor="middle" font-weight="bold">4 kg</text>
    <!-- Motion arrow down incline -->
    <line x1="45" y1="-25" x2="85" y2="-25" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-dark-06)" />
  </g>

  <!-- Length dimension line s = 3m -->
  <g transform="translate(260, 120) rotate(-37)">
    <text x="0" y="-45" font-size="16px" text-anchor="middle" font-weight="600">s = 3 m</text>
  </g>

  <!-- Caption -->
  <text x="260" y="300" font-size="16px" text-anchor="middle" font-weight="600">Block Sliding Down Rough Incline (&#956; = 0.2, s = 3 m, &#952; = 37&#176;)</text>
</svg>"""

# ==========================================
# 7. FIG 07: Incline Free Body Diagram (Illustration 4 Solution)
# ==========================================
FIG_07 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 420" width="100%" height="100%" role="img" aria-label="Free body diagram on inclined plane">
  <title>Free Body Diagram of Block on Incline</title>
  <desc>Shows normal reaction R, friction mu R up the plane, displacement s down the plane, and gravity mg vertically downward.</desc>
  <defs>
    <marker id="arr-blue-07" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arr-red-07" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#dc2626"/>
    </marker>
    <marker id="arr-dark-07" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <marker id="arr-green-07" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#16a34a"/>
    </marker>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Incline surface line tilted at -37 degrees -->
  <line x1="80" y1="80" x2="400" y2="320" stroke="#94a3b8" stroke-width="2" stroke-dasharray="6,4" />

  <!-- Block body tilted at -37 deg -->
  <g transform="translate(240, 200) rotate(-37)">
    <rect x="-40" y="-30" width="80" height="60" fill="#f8fafc" stroke="#1e293b" stroke-width="2.5" rx="3" />
    <circle cx="0" cy="0" r="3.5" fill="#1e293b" />

    <!-- Normal force R perpendicular to incline (pointing up-left) -->
    <line x1="0" y1="-30" x2="0" y2="-120" stroke="#2563eb" stroke-width="3" marker-end="url(#arr-blue-07)" />
    <text x="12" y="-115" font-size="18px" class="bold" fill="#2563eb">R</text>

    <!-- Friction force mu R up the plane -->
    <line x1="-40" y1="0" x2="-125" y2="0" stroke="#dc2626" stroke-width="3" marker-end="url(#arr-red-07)" />
    <text x="-135" y="-10" font-size="18px" class="bold" fill="#dc2626">&#956;R</text>

    <!-- Displacement vector s down the plane -->
    <line x1="40" y1="0" x2="125" y2="0" stroke="#16a34a" stroke-width="3" marker-end="url(#arr-green-07)" />
    <text x="135" y="-5" font-size="18px" class="bold" fill="#16a34a">s</text>
  </g>

  <!-- Weight mg vertically downwards (unrotated, from 240, 200) -->
  <line x1="240" y1="200" x2="240" y2="340" stroke="#1e293b" stroke-width="3" marker-end="url(#arr-dark-07)" />
  <text x="250" y="335" font-size="18px" class="bold">mg</text>

  <!-- Normal axis label -->
  <line x1="240" y1="200" x2="180" y2="120" stroke="#64748b" stroke-width="1.5" stroke-dasharray="4,4" />
  <text x="175" y="105" font-size="14px" fill="#64748b">Normal Axis</text>

  <!-- Caption -->
  <text x="260" y="390" font-size="16px" text-anchor="middle" font-weight="600">FBD on Incline: W_N = 0, W_g = mgs sin(37&#176;), W_f = -&#956;Rs</text>
</svg>"""

# ==========================================
# 8. FIG 08: Work Along 3D Curved Path (Section 10)
# ==========================================
FIG_08 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 360" width="100%" height="100%" role="img" aria-label="Work along curved path from point P1 to P2">
  <title>Work Done Along General 3D Curved Trajectory</title>
  <desc>A smooth space curve from P1 to P2 with infinitesimal displacement vector dr and net applied force vector F at angle theta.</desc>
  <defs>
    <marker id="arr-dark-08" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <marker id="arr-blue-08" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#2563eb"/>
    </marker>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Curved Trajectory from P1 to P2 -->
  <path d="M 120 280 C 180 200 240 160 330 140 C 420 120 480 80 540 50" fill="none" stroke="#1e293b" stroke-width="2.5" />

  <!-- Direction arrows along path -->
  <circle cx="120" cy="280" r="5" fill="#1e293b" />
  <text x="100" y="295" font-size="16px" class="bold">P&#8321;</text>

  <circle cx="540" cy="50" r="5" fill="#1e293b" />
  <text x="555" y="55" font-size="16px" class="bold">P&#8322;</text>

  <!-- Midpoint differential displacement dr at (330, 140) -->
  <line x1="310" y1="144" x2="360" y2="133" stroke="#16a34a" stroke-width="4" marker-end="url(#arr-dark-08)" />
  <text x="330" y="170" font-size="16px" class="bold" fill="#16a34a">dr</text>

  <!-- Force vector F acting at angle to dr -->
  <line x1="330" y1="140" x2="385" y2="60" stroke="#2563eb" stroke-width="3" marker-end="url(#arr-blue-08)" />
  <text x="395" y="65" font-size="18px" class="bold" fill="#2563eb">F</text>

  <!-- Angle arc between dr and F -->
  <path d="M 350 135 A 35 35 0 0 0 348 114" fill="none" stroke="#1e293b" stroke-width="1.8" />
  <text x="360" y="115" font-size="16px" class="math">&#952;</text>

  <!-- Formula Callout -->
  <rect x="80" y="30" width="220" height="70" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" rx="4" />
  <text x="190" y="58" font-size="15px" text-anchor="middle" class="math">W = &#8747; F &#183; dr</text>
  <text x="190" y="85" font-size="14px" text-anchor="middle" fill="#475569">W = &#916;K = &#189;mv&#8322;&#178; - &#189;mv&#8321;&#178;</text>

  <!-- Caption -->
  <text x="310" y="330" font-size="16px" text-anchor="middle" font-weight="600">Work Along a General Curved Path from P&#8321; to P&#8322;</text>
</svg>"""

# ==========================================
# 9. FIG 09: Overhanging Chain Slipping Off Table (Illustration 11)
# ==========================================
FIG_09 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 380" width="100%" height="100%" role="img" aria-label="Flexible chain overhanging smooth table corner">
  <title>Uniform Overhanging Chain Slipping Off Table</title>
  <desc>A uniform chain with 2/3 on the table and 1/3 hanging vertically, showing an infinitesimal mass element dx at depth x below the surface.</desc>
  <defs>
    <pattern id="hatch-09" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" stroke-width="1.5" />
    </pattern>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Smooth Table Surface (horizontal top, vertical right edge) -->
  <polygon points="60,110 380,110 380,340 360,340 360,130 60,130" fill="#f1f5f9" stroke="#1e293b" stroke-width="2.5" />
  <rect x="60" y="130" width="300" height="20" fill="url(#hatch-09)" />

  <!-- Chain Links on Table (2/3 of length l) -->
  <g stroke="#1e293b" stroke-width="2.5" fill="#eff6ff">
    <ellipse cx="140" cy="100" rx="14" ry="7" />
    <ellipse cx="165" cy="100" rx="14" ry="7" />
    <ellipse cx="190" cy="100" rx="14" ry="7" />
    <ellipse cx="215" cy="100" rx="14" ry="7" />
    <ellipse cx="240" cy="100" rx="14" ry="7" />
    <ellipse cx="265" cy="100" rx="14" ry="7" />
    <ellipse cx="290" cy="100" rx="14" ry="7" />
    <ellipse cx="315" cy="100" rx="14" ry="7" />
    <ellipse cx="340" cy="100" rx="14" ry="7" />
    <ellipse cx="365" cy="100" rx="14" ry="7" />

    <!-- Corner bend link -->
    <ellipse cx="385" cy="115" rx="10" ry="14" transform="rotate(30 385 115)" />

    <!-- Overhanging Vertical Chain Links (1/3 of length l) -->
    <ellipse cx="395" cy="140" rx="7" ry="13" />
    <ellipse cx="395" cy="165" rx="7" ry="13" />
    <ellipse cx="395" cy="190" rx="7" ry="13" />
    <ellipse cx="395" cy="215" rx="7" ry="13" />
    <ellipse cx="395" cy="240" rx="7" ry="13" fill="#fef08a" stroke="#ca8a04" />
    <ellipse cx="395" cy="265" rx="7" ry="13" />
  </g>

  <!-- Labels for horizontal part (2l/3) -->
  <line x1="120" y1="70" x2="380" y2="70" stroke="#64748b" stroke-width="1.5" />
  <line x1="120" y1="65" x2="120" y2="75" stroke="#64748b" stroke-width="1.5" />
  <line x1="380" y1="65" x2="380" y2="75" stroke="#64748b" stroke-width="1.5" />
  <text x="250" y="60" font-size="15px" text-anchor="middle" font-weight="600">2l/3 (on table)</text>

  <!-- Dimension line for depth x and element dx -->
  <line x1="430" y1="110" x2="430" y2="240" stroke="#64748b" stroke-width="1.5" />
  <line x1="425" y1="110" x2="435" y2="110" stroke="#64748b" stroke-width="1.5" />
  <line x1="425" y1="240" x2="435" y2="240" stroke="#64748b" stroke-width="1.5" />
  <text x="445" y="175" font-size="16px" class="math">x</text>

  <!-- Element dx marker -->
  <line x1="430" y1="240" x2="430" y2="253" stroke="#ca8a04" stroke-width="2.5" />
  <text x="445" y="250" font-size="15px" class="bold" fill="#ca8a04">dx</text>

  <!-- Total overhang label (l/3) -->
  <line x1="480" y1="110" x2="480" y2="278" stroke="#1e293b" stroke-width="1.5" />
  <line x1="475" y1="110" x2="485" y2="110" stroke="#1e293b" stroke-width="1.5" />
  <line x1="475" y1="278" x2="485" y2="278" stroke="#1e293b" stroke-width="1.5" />
  <text x="500" y="200" font-size="15px" font-weight="600">l/3</text>

  <!-- Caption -->
  <text x="300" y="355" font-size="16px" text-anchor="middle" font-weight="600">Uniform Chain Slipping Off Table: &#916;U_loss = 4/9 mgl &#8658; K = 4/9 mgl</text>
</svg>"""

# ==========================================
# 10. FIG 10: Spring-Block Oscillator System (Illustration 12)
# ==========================================
FIG_10 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 340" width="100%" height="100%" role="img" aria-label="Spring block system released from compressed state">
  <title>Block Released from Compressed Spring</title>
  <desc>A block of mass m compressed to half the natural length of spring L0/2 against a wall, sliding to the right with velocity v.</desc>
  <defs>
    <marker id="arr-dark-10" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e293b"/>
    </marker>
    <pattern id="hatch-10" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" stroke-width="1.5" />
    </pattern>
  </defs>
  <style>
    text { font-family: system-ui, -apple-system, sans-serif; fill: #1e293b; }
    .bold { font-weight: bold; }
    .math { font-style: italic; font-family: 'Times New Roman', serif; }
  </style>

  <!-- Left Wall -->
  <line x1="80" y1="60" x2="80" y2="220" stroke="#1e293b" stroke-width="3" />
  <rect x="60" y="60" width="20" height="160" fill="url(#hatch-10)" />

  <!-- Frictionless Floor -->
  <line x1="80" y1="220" x2="620" y2="220" stroke="#1e293b" stroke-width="2.5" />

  <!-- Spring (coiled path from wall at x=80 to block at x=230) -->
  <path d="M 80 170 L 100 170 
           C 105 145, 115 145, 120 170 
           C 125 195, 135 195, 140 170 
           C 145 145, 155 145, 160 170 
           C 165 195, 175 195, 180 170 
           C 185 145, 195 145, 200 170 
           C 205 195, 215 195, 220 170 
           L 230 170" fill="none" stroke="#2563eb" stroke-width="3" />
  <text x="155" y="135" font-size="18px" class="bold" fill="#2563eb">k</text>

  <!-- Compressed Block (mass m) at x = L0/2 -->
  <rect x="230" y="130" width="60" height="90" fill="#eff6ff" stroke="#1e293b" stroke-width="2.5" rx="2" />
  <text x="260" y="175" font-size="18px" text-anchor="middle" font-weight="bold">m</text>

  <!-- Future position of block detached moving right -->
  <rect x="390" y="130" width="60" height="90" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="5,4" rx="2" />
  <!-- Velocity arrow v -->
  <line x1="465" y1="175" x2="540" y2="175" stroke="#16a34a" stroke-width="3" marker-end="url(#arr-dark-10)" />
  <text x="495" y="160" font-size="18px" class="bold" fill="#16a34a">v</text>

  <!-- Dimension line for compressed position L0/2 -->
  <line x1="80" y1="245" x2="230" y2="245" stroke="#1e293b" stroke-width="1.5" />
  <line x1="80" y1="238" x2="80" y2="252" stroke="#1e293b" stroke-width="1.5" />
  <line x1="230" y1="238" x2="230" y2="252" stroke="#1e293b" stroke-width="1.5" />
  <text x="155" y="265" font-size="15px" text-anchor="middle" font-weight="600">L&#8320;/2</text>

  <!-- Dimension line for general position x -->
  <line x1="80" y1="285" x2="390" y2="285" stroke="#64748b" stroke-width="1.5" />
  <line x1="80" y1="278" x2="80" y2="292" stroke="#64748b" stroke-width="1.5" />
  <line x1="390" y1="278" x2="390" y2="292" stroke="#64748b" stroke-width="1.5" />
  <text x="235" y="305" font-size="16px" text-anchor="middle" class="math">x</text>

  <!-- Caption -->
  <text x="350" y="330" font-size="16px" text-anchor="middle" font-weight="600">Block Released from Compressed Spring (L&#8320;/2 &#8804; x &#8804; L&#8320;)</text>
</svg>"""

if __name__ == "__main__":
    svgs = [
        ("fig_01_work_sign_positive.svg", FIG_01),
        ("fig_02_work_sign_negative.svg", FIG_02),
        ("fig_03_fbd_string_raising.svg", FIG_03),
        ("fig_04_variable_force_calculus.svg", FIG_04),
        ("fig_05_friction_direction.svg", FIG_05),
        ("fig_06_incline_block.svg", FIG_06),
        ("fig_07_incline_fbd.svg", FIG_07),
        ("fig_08_curved_path_work.svg", FIG_08),
        ("fig_09_overhanging_chain.svg", FIG_09),
        ("fig_10_spring_block_wall.svg", FIG_10)
    ]
    for fn, content in svgs:
        save_and_validate(fn, content)
    print("All 10 SVGs successfully generated and strictly validated!")
