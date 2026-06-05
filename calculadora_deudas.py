import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Calculadora de Deudas | Profit Hispano",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&family=Sora:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg:     #12082A;
    --bg2:    #1B2550;
    --bg3:    #1E2D62;
    --cyan:   #48D9E0;
    --blue:   #4A6CF7;
    --purple: #9B3DF5;
    --red:    #FF4A6A;
    --green:  #00E5A0;
    --text:   #EEF2FF;
    --muted:  #7A94C8;
    --border: rgba(74,108,247,0.25);
}

body, p, div, h1, h2, h3, h4, h5, h6,
input, textarea, select, label, a, li, td, th {
    font-family: 'Sora', sans-serif !important;
}
.material-symbols-rounded {
    font-family: 'Material Symbols Rounded' !important;
    font-optical-sizing: auto !important;
    font-weight: 400 !important;
    font-style: normal !important;
    font-size: 20px !important;
    line-height: 1 !important;
}

.stApp { background: var(--bg) !important; color: var(--text) !important; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.3rem !important;
    padding-left: 1.4rem !important;
    padding-right: 1.4rem !important;
    max-width: 100% !important;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 0.8rem !important;
    padding-bottom: 0.5rem !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] hr { border-color: var(--border) !important; }

[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="collapsedControl"] {
    background: #4A6CF7 !important;
    border-right: 2px solid #48D9E0 !important;
    width: 28px !important;
    opacity: 1 !important;
    visibility: visible !important;
}
[data-testid="collapsedControl"] .material-symbols-rounded {
    color: #ffffff !important;
    font-size: 22px !important;
}

input[type="number"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-family: 'Sora', sans-serif !important;
}
input[type="number"]:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 2px rgba(72,217,224,0.15) !important;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, var(--bg2), var(--bg3)) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    transition: all 0.2s ease;
}
[data-testid="metric-container"]:hover {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 14px rgba(72,217,224,0.12) !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 2px !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: var(--cyan) !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; font-weight: 500 !important; }

[data-testid="stCheckbox"] label {
    font-size: 12px !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
}
[data-testid="stCheckbox"] label:hover { color: var(--cyan) !important; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
    border-radius: 8px !important;
    padding: 3px !important;
    gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    border-radius: 6px !important;
    padding: 5px 14px !important;
    font-family: 'Sora', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background: var(--blue) !important;
    color: white !important;
}

.streamlit-expanderHeader {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

hr { border-color: var(--border) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--blue); border-radius: 4px; }

/* ── MOBILE ── */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 6px !important;
    }
    [data-testid="stHorizontalBlock"] > div {
        min-width: calc(50% - 6px) !important;
        flex: 1 1 calc(50% - 6px) !important;
    }
    [data-testid="stMetricValue"] { font-size: 1rem !important; }
    [data-testid="stMetricLabel"] p { font-size: 9px !important; }
    .block-container {
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES
# ══════════════════════════════════════════════════════════════════════
def tasa_mensual_efectiva(tasa_anual):
    return (1 + tasa_anual / 100) ** (1 / 12) - 1

def tasa_mensual_nominal(tasa_anual):
    return tasa_anual / 100 / 12

def calcular_cuota(monto, i_mensual, meses):
    if i_mensual == 0:
        return monto / meses
    return monto * i_mensual / (1 - (1 + i_mensual) ** (-meses))

@st.cache_data
def calcular_amortizacion(monto, i_mensual, meses, pago_extra=0):
    cuota = calcular_cuota(monto, i_mensual, meses)
    cuota_total = cuota + pago_extra
    saldo = monto
    rows  = []
    for mes in range(1, meses + 1):
        interes = saldo * i_mensual
        capital = min(cuota_total - interes, saldo)
        saldo  -= capital
        rows.append({
            "Mes":            mes,
            "Cuota":          round(cuota_total if saldo > 0.01 else capital + interes, 2),
            "Capital":        round(capital, 2),
            "Intereses":      round(interes, 2),
            "Saldo Restante": round(max(saldo, 0), 2),
        })
        if saldo <= 0.01:
            break
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════
#  PLOTLY THEME — leyenda dentro + ejes fijos (no zoom táctil)
# ══════════════════════════════════════════════════════════════════════
PLOT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(27,37,80,0.5)',
    font=dict(family='Sora, sans-serif', color='#7A94C8', size=11),
    xaxis=dict(gridcolor='rgba(74,108,247,0.12)', linecolor='rgba(74,108,247,0.3)',
               tickfont=dict(size=10, color='#7A94C8'),
               fixedrange=True),
    yaxis=dict(gridcolor='rgba(74,108,247,0.12)', linecolor='rgba(74,108,247,0.3)',
               tickprefix='$', tickformat=',.0f',
               tickfont=dict(size=10, color='#7A94C8'),
               fixedrange=True),
    legend=dict(
        x=0.02, y=0.98,
        xanchor='left', yanchor='top',
        bgcolor='rgba(18,8,42,0.9)',
        bordercolor='rgba(74,108,247,0.4)',
        borderwidth=1,
        font=dict(size=10, color='#EEF2FF')
    ),
    margin=dict(l=6, r=6, t=28, b=6),
    hoverlabel=dict(bgcolor='rgba(18,8,42,0.95)', bordercolor='#4A6CF7',
                    font=dict(family='Sora, sans-serif', size=12)),
)

PLOT_CONFIG = {
    'displayModeBar': False,
    'scrollZoom': False,
    'doubleClick': 'reset',
    'displaylogo': False,
}


# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="font-size:10px; letter-spacing:3px; color:#48D9E0; text-transform:uppercase;
                padding:2px 0 10px 0; border-bottom:1px solid rgba(74,108,247,0.2);
                margin-bottom:12px;">💳 Tu Préstamo</div>
    """, unsafe_allow_html=True)

    monto = st.number_input(
        "💰 Monto del Préstamo (USD)", min_value=100, value=10_000, step=500,
        help="Cuánto dinero necesitas pedir. Ej: $10,000 para un carro o $50,000 para una casa."
    )
    tasa_anual = st.number_input(
        "📊 Tasa de Interés Anual (%)", min_value=0.1, value=12.0, step=0.5,
        help="Tasa anual del banco. Por defecto calculamos con Tasa Nominal. Si tu banco te da una Tasa Efectiva, activa el modo avanzado."
    )
    meses = st.slider(
        "📅 Plazo (Meses)", min_value=3, max_value=360, value=36, step=3,
        help="En cuántos meses pagarás. 12 = 1 año · 36 = 3 años · 60 = 5 años · 360 = 30 años"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:10px; letter-spacing:2px; color:#4A6CF7; text-transform:uppercase;
                margin-bottom:4px;">⚡ Pago Extra Mensual</div>
    <div style="font-size:11px; color:#7A94C8; margin-bottom:8px; line-height:1.5;">
        ¿Puedes pagar un poco más cada mes? Ve cuánto tiempo y dinero ahorras.
    </div>
    """, unsafe_allow_html=True)

    pago_extra = st.number_input(
        "➕ Pago extra al mes (USD)", min_value=0, value=0, step=50,
        help="Monto adicional sobre la cuota normal. Aunque sean $50 extra, el ahorro a largo plazo es enorme."
    )

    # ── MODO AVANZADO ──────────────────────────────────────────────────
    st.markdown("---")
    modo_avanzado = st.checkbox(
        "⚙️ Modo avanzado (tipo de tasa)",
        help="Activa esto si tu banco te especificó que la tasa es Efectiva Anual. En la mayoría de créditos de consumo no es necesario."
    )

    tipo_tasa = "nominal"
    if modo_avanzado:
        st.markdown("""
        <div style="font-size:11px; color:#7A94C8; margin-bottom:8px; line-height:1.5;">
            ¿Cómo te dieron la tasa?
        </div>
        """, unsafe_allow_html=True)

        tipo_tasa = st.radio(
            "Tipo de tasa:",
            options=["nominal", "efectiva"],
            format_func=lambda x: (
                "Nominal Anual (TNA)"
                if x == "nominal" else
                "Efectiva Anual (TEA)"
            ),
            help="Tasa Nominal: se divide entre 12. Tasa Efectiva: se convierte con fórmula exacta.",
            index=0
        )

        if tipo_tasa == "efectiva":
            st.markdown("""
            <div style="background:rgba(155,61,245,0.08); border:1px solid rgba(155,61,245,0.25);
                        border-radius:6px; padding:8px; font-size:11px; color:#7A94C8;
                        line-height:1.6;">
                🌍 <b style="color:#9B3DF5;">Común en:</b> Colombia (EA),
                Venezuela, España (TAE), Europa en general.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(72,217,224,0.08); border:1px solid rgba(72,217,224,0.25);
                        border-radius:6px; padding:8px; font-size:11px; color:#7A94C8;
                        line-height:1.6;">
                🌍 <b style="color:#48D9E0;">Común en:</b> USA (APR),
                créditos de consumo, tarjetas de crédito.
            </div>
            """, unsafe_allow_html=True)

    # Calcular tasa mensual
    if tipo_tasa == "efectiva":
        i_mensual = tasa_mensual_efectiva(tasa_anual)
    else:
        i_mensual = tasa_mensual_nominal(tasa_anual)

    st.markdown(f"""
    <div style="background:rgba(74,108,247,0.1); border:1px solid rgba(74,108,247,0.25);
                border-radius:8px; padding:10px; margin-top:10px; line-height:1.8;">
        <div style="font-size:10px; letter-spacing:2px; color:#4A6CF7;
                    text-transform:uppercase; margin-bottom:6px;">🔢 Conversión automática</div>
        <div style="font-size:12px; color:#7A94C8;">
            Tasa anual: <b style="color:#EEF2FF;">{tasa_anual:.2f}%</b>
            <span style="color:#9B3DF5; font-size:10px;">
                {"(Efectiva)" if tipo_tasa == "efectiva" else "(Nominal)"}
            </span><br>
            Tasa mensual: <b style="color:#48D9E0;">{i_mensual*100:.4f}%</b><br>
            Plazo: <b style="color:#EEF2FF;">{meses} meses</b>
            <span style="color:#7A94C8;"> ({meses/12:.1f} años)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not modo_avanzado:
        st.markdown("""
        <div style="font-size:10px; color:#7A94C8; margin-top:6px; padding:0 2px;
                    line-height:1.5; opacity:0.8;">
            Calculado con Tasa Nominal. Si tu banco te dio una Tasa Efectiva,
            activa el modo avanzado ⬆
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:11px; color:#7A94C8; border-left:2px solid #FF4A6A;
                padding-left:8px; margin-top:10px; line-height:1.5;">
        <em>"Un préstamo mal entendido es la forma más cara de pagar algo."</em>
        <br><span style="color:#FF4A6A; font-size:10px;">— Profit Hispano</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  CÁLCULOS
# ══════════════════════════════════════════════════════════════════════
cuota_mensual   = calcular_cuota(monto, i_mensual, meses)
df              = calcular_amortizacion(monto, i_mensual, meses, pago_extra)
df_normal       = calcular_amortizacion(monto, i_mensual, meses, 0)
meses_reales    = len(df)
total_pagado    = df["Cuota"].sum()
total_intereses = df["Intereses"].sum()
costo_real_pct  = (total_intereses / monto) * 100
por_cada_100    = (total_pagado / monto) * 100

if pago_extra > 0:
    meses_ahorrados = len(df_normal) - meses_reales
    dinero_ahorrado = df_normal["Intereses"].sum() - total_intereses
else:
    meses_ahorrados, dinero_ahorrado = 0, 0


# ══════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding:4px 0 2px 0;">
    <div style="font-size:9px; letter-spacing:5px; color:#4A6CF7;
                text-transform:uppercase; margin-bottom:3px;">PROFIT HISPANO</div>
    <div style="font-size:clamp(16px,2.2vw,26px); font-weight:800; letter-spacing:1px;
                background:linear-gradient(90deg,#FF4A6A,#4A6CF7,#48D9E0);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">
        CALCULADORA DE DEUDAS
    </div>
    <p style="color:#7A94C8; font-size:12px; margin:3px 0 0 0;">
        Entiende exactamente cuánto te cuesta un préstamo antes de firmarlo
    </p>
</div>
<div style="height:1px; background:linear-gradient(90deg,transparent,#FF4A6A,transparent);
            margin:5px 0 6px 0;"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  KPIs
# ══════════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💳 Cuota Mensual",      f"${cuota_mensual:,.2f}")
with c2:
    st.metric("💰 Total a Pagar",      f"${total_pagado:,.2f}",
              delta=f"+${total_intereses:,.2f} en intereses",
              delta_color="inverse")
with c3:
    st.metric("🔥 Total en Intereses", f"${total_intereses:,.2f}",
              delta=f"{costo_real_pct:.1f}% del préstamo",
              delta_color="inverse")
with c4:
    st.metric("📊 Por cada $100",      f"${por_cada_100/100:.2f}",
              delta=f"pagas ${(por_cada_100-100)/100:.2f} de interés",
              delta_color="inverse")

# Alerta dinámica
ratio = total_intereses / monto
if ratio > 0.5:
    ac, ai, am = "#FF4A6A", "⚠️", f"Pagarás {costo_real_pct:.1f}% del préstamo solo en intereses — considera negociar la tasa o acortar el plazo."
elif ratio > 0.25:
    ac, ai, am = "#FF9A3C", "💡", f"Pagarás {costo_real_pct:.1f}% extra en intereses. Un pago adicional mensual puede ahorrarte meses y dinero."
else:
    ac, ai, am = "#00E5A0", "✅", f"Buen préstamo. Los intereses representan solo el {costo_real_pct:.1f}% del monto — dentro de un rango razonable."

st.markdown(f"""
<div style="display:flex; gap:5px; margin:5px 0 4px 0;">
    <div style="flex:3; background:rgba(27,37,80,0.7); border:1px solid {ac}40;
                border-left:3px solid {ac}; border-radius:7px; padding:7px 12px;">
        <span style="font-size:12px; color:{ac};">{ai} <b>{am}</b></span>
    </div>
    <div style="flex:1; background:rgba(27,37,80,0.7); border:1px solid rgba(74,108,247,0.2);
                border-radius:7px; padding:7px 10px; text-align:center;">
        <div style="font-size:9px; color:#7A94C8; text-transform:uppercase; letter-spacing:1px;">
            Tasa mensual</div>
        <div style="font-size:15px; font-weight:700; color:#48D9E0;">{i_mensual*100:.4f}%</div>
    </div>
    <div style="flex:1; background:rgba(27,37,80,0.7); border:1px solid rgba(74,108,247,0.2);
                border-radius:7px; padding:7px 10px; text-align:center;">
        <div style="font-size:9px; color:#7A94C8; text-transform:uppercase; letter-spacing:1px;">
            Plazo real</div>
        <div style="font-size:15px; font-weight:700; color:#4A6CF7;">{meses_reales} meses</div>
    </div>
</div>
""", unsafe_allow_html=True)

if pago_extra > 0 and meses_ahorrados > 0:
    st.markdown(f"""
    <div style="background:rgba(0,229,160,0.08); border:1px solid rgba(0,229,160,0.3);
                border-left:3px solid #00E5A0; border-radius:7px; padding:7px 14px;
                font-size:12px; color:#EEF2FF; margin-bottom:4px;">
        🚀 <b style="color:#00E5A0;">Pagando ${pago_extra:,.0f} extra al mes</b>
        terminas <b>{meses_ahorrados} meses antes</b> y ahorras
        <b style="color:#00E5A0;">${dinero_ahorrado:,.2f}</b> en intereses.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "📉  Evolución del Saldo",
    "🥧  Composición del Pago",
    "📋  Tabla de Amortización",
])

with tab1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_normal["Mes"], y=df_normal["Saldo Restante"],
        name="Saldo normal",
        line=dict(color="#4A6CF7", width=2.5),
        fill="tozeroy", fillcolor="rgba(74,108,247,0.06)",
        hovertemplate="<b>Mes %{x}</b><br>Saldo: <b>$%{y:,.2f}</b><extra></extra>",
    ))
    if pago_extra > 0:
        fig1.add_trace(go.Scatter(
            x=df["Mes"], y=df["Saldo Restante"],
            name=f"Saldo con ${pago_extra:,.0f} extra",
            line=dict(color="#00E5A0", width=2.5, dash="dash"),
            hovertemplate="<b>Mes %{x}</b><br>Saldo: <b>$%{y:,.2f}</b><extra></extra>",
        ))
    fig1.update_layout(
        title=dict(text="¿Cómo va bajando tu deuda mes a mes?",
                   font=dict(family="Sora", size=12, color="#7A94C8")),
        hovermode="x unified", legend_title_text="", height=265, **PLOT)
    st.plotly_chart(fig1, use_container_width=True, config=PLOT_CONFIG)

    st.markdown(f"""
    <div style="background:rgba(74,108,247,0.1); border:1px solid rgba(74,108,247,0.3);
                border-left:3px solid #48D9E0; border-radius:8px; padding:8px 14px;
                font-size:12px; line-height:1.7; color:#EEF2FF;">
        💡 <b style="color:#48D9E0;">Conclusión:</b>
        Por un préstamo de <b>${monto:,.0f}</b> al <b>{tasa_anual}% anual
        {"efectiva" if tipo_tasa == "efectiva" else "nominal"}</b>
        en <b>{meses} meses</b>, tu cuota es <b>${cuota_mensual:,.2f}</b>/mes.
        Al finalizar habrás pagado <b style="color:#FF4A6A;">${total_pagado:,.2f}</b>
        — <b>${total_intereses:,.2f} más</b> de lo que pediste.
        El banco cobra <b style="color:#FF4A6A;">{costo_real_pct:.1f}%</b> extra sobre tu dinero.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        step    = max(1, meses_reales // 20)
        df_plot = df_normal.iloc[::step].copy()
        fig2    = go.Figure()
        fig2.add_trace(go.Bar(
            name="Capital", x=df_plot["Mes"], y=df_plot["Capital"],
            marker_color="rgba(72,217,224,0.85)",
            marker_line=dict(color="#48D9E0", width=0.5),
            hovertemplate="Mes %{x}<br>Capital: <b>$%{y:,.2f}</b><extra></extra>",
        ))
        fig2.add_trace(go.Bar(
            name="Intereses", x=df_plot["Mes"], y=df_plot["Intereses"],
            marker_color="rgba(255,74,106,0.75)",
            marker_line=dict(color="#FF4A6A", width=0.5),
            hovertemplate="Mes %{x}<br>Intereses: <b>$%{y:,.2f}</b><extra></extra>",
        ))
        fig2.update_layout(
            barmode="stack",
            title=dict(text="¿Cuánto va a capital vs intereses cada mes?",
                       font=dict(family="Sora", size=12, color="#7A94C8")),
            height=300, **PLOT)
        st.plotly_chart(fig2, use_container_width=True, config=PLOT_CONFIG)

    with col_b:
        fig3 = go.Figure(go.Pie(
            labels=["Lo que queda para ti (capital)",
                    "Lo que se lleva el banco (intereses)"],
            values=[monto, total_intereses], hole=0.58,
            marker=dict(colors=["#48D9E0","#FF4A6A"],
                        line=dict(color="#12082A", width=3)),
            textfont=dict(family="Sora", size=12),
            hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>",
        ))
        fig3.add_annotation(
            text=f"{costo_real_pct:.0f}%<br>interés",
            x=0.5, y=0.5,
            font=dict(family="Sora", size=20, color="#FF4A6A"),
            showarrow=False
        )
        fig3.update_layout(
            title=dict(text="De todo lo que pagas, ¿cuánto es tuyo?",
                       font=dict(family="Sora", size=12, color="#7A94C8")),
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Sora, sans-serif', color='#7A94C8', size=11),
            margin=dict(l=6, r=6, t=28, b=6),
            legend=dict(font=dict(size=10, color='#EEF2FF')),
        )
        st.plotly_chart(fig3, use_container_width=True, config=PLOT_CONFIG)

with tab3:
    fmt = {c: "${:,.2f}" for c in ["Cuota","Capital","Intereses","Saldo Restante"]}
    st.dataframe(
        df.style.format(fmt)
          .background_gradient(subset=["Saldo Restante"], cmap="Blues_r")
          .background_gradient(subset=["Intereses"], cmap="Reds"),
        use_container_width=True, height=370,
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Exportar tabla completa CSV", data=csv,
        file_name=f"amortizacion_{monto}_{meses}meses.csv",
        mime="text/csv"
    )

# Footer
st.markdown("""
<div style="text-align:center; padding:6px 0 2px 0;
            border-top:1px solid rgba(74,108,247,0.15); margin-top:4px;">
    <span style="font-size:11px; font-weight:700; color:#48D9E0; letter-spacing:3px;">
        PROFIT HISPANO
    </span>
    <span style="font-size:11px; color:#7A94C8; margin-left:10px;">
        | IA &amp; FINANZAS — Decisiones basadas en datos, no en emociones.
    </span>
</div>
""", unsafe_allow_html=True)
