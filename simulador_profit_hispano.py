import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Simulador | Profit Hispano",
    page_icon="📈",
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

[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

[data-testid="collapsedControl"] {
    background: var(--bg2) !important;
    border-right: 2px solid var(--cyan) !important;
}
[data-testid="collapsedControl"] .material-symbols-rounded {
    color: var(--cyan) !important;
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
[data-testid="stMetricDelta"] {
    font-size: 11px !important;
    font-weight: 500 !important;
}

[data-testid="stVerticalBlock"] > div { gap: 0.3rem !important; }

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
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  FUNCIONES
# ══════════════════════════════════════════════════════════════════════
@st.cache_data
def calcular_proyeccion(principal, tasa, años, aportacion=0):
    tm = tasa / 12
    rows = []
    for t in range(años + 1):
        simple    = principal * (1 + tasa * t)
        compuesto = principal * (1 + tasa) ** t
        m         = t * 12
        if t == 0:
            comp_ap = principal
        elif aportacion > 0:
            comp_ap = (principal * (1+tm)**m
                       + aportacion * (((1+tm)**m - 1) / tm))
        else:
            comp_ap = compuesto
        rows.append({
            "Año":                    t,
            "Interés Simple":         simple,
            "Interés Compuesto":      compuesto,
            "Compuesto + Aportación": comp_ap,
            "Ganancia Simple":        simple - principal,
            "Ganancia Compuesta":     compuesto - principal,
            "Total Aportado":         principal + aportacion * 12 * t,
            "Ganancia Neta":          comp_ap - (principal + aportacion * 12 * t),
        })
    return pd.DataFrame(rows)

def regla_72(tasa): return 72 / (tasa * 100)


# ══════════════════════════════════════════════════════════════════════
#  PLOTLY THEME
# ══════════════════════════════════════════════════════════════════════
PLOT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(27,37,80,0.5)',
    font=dict(family='Sora, sans-serif', color='#7A94C8', size=11),
    xaxis=dict(gridcolor='rgba(74,108,247,0.12)', linecolor='rgba(74,108,247,0.3)',
               tickfont=dict(size=10, color='#7A94C8')),
    yaxis=dict(gridcolor='rgba(74,108,247,0.12)', linecolor='rgba(74,108,247,0.3)',
               tickprefix='$', tickformat=',.0f',
               tickfont=dict(size=10, color='#7A94C8')),
    legend=dict(bgcolor='rgba(18,8,42,0.85)', bordercolor='rgba(74,108,247,0.3)',
                borderwidth=1, font=dict(size=11)),
    margin=dict(l=6, r=6, t=28, b=6),
    hoverlabel=dict(bgcolor='rgba(18,8,42,0.95)', bordercolor='#4A6CF7',
                    font=dict(family='Sora, sans-serif', size=12)),
)


# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="font-size:10px; letter-spacing:3px; color:#48D9E0; text-transform:uppercase;
                padding:2px 0 10px 0; border-bottom:1px solid rgba(74,108,247,0.2);
                margin-bottom:12px;">⚙ Parámetros</div>
    """, unsafe_allow_html=True)

    principal = st.number_input(
        "💰 Capital Inicial (USD)", min_value=0, value=10_000, step=500,
        help="El dinero que inviertes hoy. Ej: $10,000"
    )
    tasa = st.slider(
        "📊 Retorno Anual (%)", 1.0, 30.0, 10.0, 0.5, format="%.1f%%",
        help="Rendimiento anual esperado. El S&P 500 históricamente rinde ~10% anual."
    ) / 100
    años = st.slider(
        "⏳ Horizonte (Años)", 1, 40, 20,
        help="Por cuántos años mantendrás la inversión."
    )

    st.markdown("""<hr style="margin:10px 0;">""", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:10px; letter-spacing:2px; color:#4A6CF7; text-transform:uppercase;
                margin-bottom:4px;">➕ Aportación Mensual</div>
    <div style="font-size:11px; color:#7A94C8; margin-bottom:8px; line-height:1.5;">
        Cuánto agregas cada mes. Incluso $50 hace una gran diferencia.
    </div>
    """, unsafe_allow_html=True)

    aportacion = st.number_input(
        "📥 Aportación mensual (USD)", min_value=0, value=0, step=50,
        help="Dinero adicional que aportas cada mes."
    )

    r72 = regla_72(tasa)

    st.markdown(f"""
    <div style="background:rgba(74,108,247,0.1); border:1px solid rgba(74,108,247,0.25);
                border-radius:8px; padding:10px; margin-top:10px; line-height:1.7;">
        <div style="font-size:10px; letter-spacing:2px; color:#4A6CF7;
                    text-transform:uppercase; margin-bottom:6px;">📐 ¿Sabías que...?</div>
        <div style="font-size:12px; color:#7A94C8;">
            Con <b style="color:#EEF2FF;">{tasa*100:.1f}%</b> anual, tu dinero
            se <b style="color:#48D9E0;">duplica</b> cada
            <b style="color:#EEF2FF;">{r72:.1f} años</b>.
        </div>
        <div style="font-size:10px; color:#7A94C8; margin-top:4px;">— Regla del 72</div>
    </div>
    <div style="font-size:11px; color:#7A94C8; border-left:2px solid #48D9E0;
                padding-left:8px; margin-top:10px; line-height:1.5;">
        <em>"El interés compuesto es la octava maravilla del mundo."</em>
        <br><span style="color:#48D9E0; font-size:10px;">— Albert Einstein</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  CÁLCULOS
# ══════════════════════════════════════════════════════════════════════
df = calcular_proyeccion(principal, tasa, años, aportacion)

final_simple  = df["Interés Simple"].iloc[-1]
final_comp    = df["Interés Compuesto"].iloc[-1]
final_con_ap  = df["Compuesto + Aportación"].iloc[-1]
total_ap      = df["Total Aportado"].iloc[-1]
ganancia_neta = final_con_ap - total_ap
multiplicador = final_con_ap / principal if principal > 0 else 0
ventaja_comp  = final_comp - final_simple
diff_pct      = ((ventaja_comp / (final_simple - principal)) * 100
                 if (final_simple - principal) > 0 else 0)
pct_v         = diff_pct


# ══════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; padding:4px 0 2px 0;">
    <div style="font-size:9px; letter-spacing:5px; color:#4A6CF7;
                text-transform:uppercase; margin-bottom:3px;">PROFIT HISPANO</div>
    <div style="font-size:clamp(16px,2.2vw,26px); font-weight:800; letter-spacing:1px;
                background:linear-gradient(90deg,#48D9E0,#4A6CF7,#9B3DF5);
                -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">
        SIMULADOR DE INVERSIONES
    </div>
    <p style="color:#7A94C8; font-size:12px; margin:3px 0 0 0;">
        Descubre el poder del interés compuesto sobre tu dinero
    </p>
</div>
<div style="height:1px; background:linear-gradient(90deg,transparent,#4A6CF7,transparent);
            margin:5px 0 6px 0;"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  KPIs
# ══════════════════════════════════════════════════════════════════════
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💼 Capital Inicial",   f"${principal:,.0f}")
with c2:
    st.metric("📏 Interés Simple",    f"${final_simple:,.0f}",
              delta=f"+${df['Ganancia Simple'].iloc[-1]:,.0f} ganancia")
with c3:
    st.metric("📈 Interés Compuesto", f"${final_comp:,.0f}",
              delta=f"+${df['Ganancia Compuesta'].iloc[-1]:,.0f} ganancia")
with c4:
    if aportacion > 0:
        st.metric("🚀 Con Aportaciones", f"${final_con_ap:,.0f}",
                  delta=f"+${ganancia_neta:,.0f} ganancia")
    else:
        st.metric("⚡ Multiplicador", f"×{multiplicador:.1f}x",
                  delta=f"Doblas en {r72:.1f} años")

# Insight bar
st.markdown(f"""
<div style="display:flex; gap:5px; margin:5px 0 4px 0;">
    <div style="flex:1; background:rgba(27,37,80,0.7); border:1px solid rgba(74,108,247,0.2);
                border-radius:7px; padding:6px 10px; text-align:center;">
        <div style="font-size:9px; color:#7A94C8; letter-spacing:1px; text-transform:uppercase;">
            El compuesto genera</div>
        <div style="font-size:15px; font-weight:700; color:#48D9E0;">+{diff_pct:.0f}% más</div>
        <div style="font-size:9px; color:#7A94C8;">que el interés simple</div>
    </div>
    <div style="flex:1; background:rgba(27,37,80,0.7); border:1px solid rgba(74,108,247,0.2);
                border-radius:7px; padding:6px 10px; text-align:center;">
        <div style="font-size:9px; color:#7A94C8; letter-spacing:1px; text-transform:uppercase;">
            Tu dinero se multiplica</div>
        <div style="font-size:15px; font-weight:700; color:#4A6CF7;">×{multiplicador:.1f}x</div>
        <div style="font-size:9px; color:#7A94C8;">en {años} años</div>
    </div>
    <div style="flex:1; background:rgba(27,37,80,0.7); border:1px solid rgba(74,108,247,0.2);
                border-radius:7px; padding:6px 10px; text-align:center;">
        <div style="font-size:9px; color:#7A94C8; letter-spacing:1px; text-transform:uppercase;">
            Capital se duplica cada</div>
        <div style="font-size:15px; font-weight:700; color:#9B3DF5;">{r72:.1f} años</div>
        <div style="font-size:9px; color:#7A94C8;">con tasa {tasa*100:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════
COLORS = {
    "Interés Simple":          "#4A6CF7",
    "Interés Compuesto":       "#48D9E0",
    "Compuesto + Aportación":  "#9B3DF5",
}

tab1, tab2, tab3 = st.tabs([
    "📈  Curva de Crecimiento",
    "🏛  Composición del Capital",
    "📊  Datos Año a Año",
])

with tab1:
    series = ["Interés Simple", "Interés Compuesto"]
    if aportacion > 0:
        series.append("Compuesto + Aportación")

    fig1 = go.Figure()
    for i, s in enumerate(series):
        fig1.add_trace(go.Scatter(
            x=df["Año"], y=df[s], name=s,
            line=dict(color=COLORS[s], width=2.5),
            fill="tozeroy" if i == 0 else "none",
            fillcolor="rgba(74,108,247,0.05)",
            hovertemplate=f"<b>{s}</b><br>Año %{{x}}<br><b>${{y:,.0f}}</b><extra></extra>",
        ))

    val_final = final_con_ap if aportacion > 0 else final_comp
    fig1.add_trace(go.Scatter(
        x=[años], y=[val_final],
        mode="markers+text",
        marker=dict(color="#48D9E0", size=9, line=dict(color="#12082A", width=2)),
        text=[f"  ${val_final:,.0f}"],
        textposition="middle right",
        textfont=dict(color="#48D9E0", size=11),
        showlegend=False, hoverinfo="skip",
    ))

    fig1.update_layout(
        title=dict(text="Crecimiento de tu dinero en el tiempo",
                   font=dict(family="Sora", size=12, color="#7A94C8")),
        hovermode="x unified", legend_title_text="", height=268, **PLOT)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown(f"""
    <div style="background:rgba(74,108,247,0.1); border:1px solid rgba(74,108,247,0.3);
                border-left:3px solid #48D9E0; border-radius:8px; padding:9px 14px;
                font-size:12px; line-height:1.7; color:#EEF2FF;">
        💡 <b style="color:#48D9E0;">Conclusión:</b>
        Invirtiendo <b>${principal:,.0f}</b> durante <b>{años} años</b>
        al <b>{tasa*100:.1f}%</b> anual, el interés compuesto genera
        <b style="color:#48D9E0;">${final_comp:,.0f}</b> —
        <b>${ventaja_comp:,.0f} más</b> que el interés simple ({pct_v:.0f}% de ventaja).
        Tu dinero se multiplica <b style="color:#9B3DF5;">×{multiplicador:.1f}x</b>.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        cats  = ["Simple", "Compuesto"]
        caps  = [principal, principal]
        gains = [df["Ganancia Simple"].iloc[-1], df["Ganancia Compuesta"].iloc[-1]]
        gcols = ["rgba(74,108,247,0.85)", "rgba(72,217,224,0.9)"]
        if aportacion > 0:
            cats.append("+ Aportación"); caps.append(total_ap)
            gains.append(ganancia_neta);  gcols.append("rgba(155,61,245,0.9)")

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Lo que pusiste", x=cats, y=caps,
                              marker_color="rgba(74,108,247,0.3)",
                              marker_line=dict(color="#4A6CF7", width=1.2)))
        fig2.add_trace(go.Bar(name="Lo que ganaste", x=cats, y=gains,
                              marker_color=gcols,
                              marker_line=dict(color=["#4A6CF7","#48D9E0","#9B3DF5"][:len(cats)], width=1)))
        fig2.update_layout(barmode="stack",
                           title=dict(text=f"¿Cuánto pusiste vs cuánto ganaste? (Año {años})",
                                      font=dict(family="Sora", size=12, color="#7A94C8")),
                           height=310, **PLOT)
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        val_cap = total_ap if aportacion > 0 else principal
        val_gan = ganancia_neta if aportacion > 0 else df["Ganancia Compuesta"].iloc[-1]

        fig3 = go.Figure(go.Pie(
            labels=["Lo que invertiste", "Lo que generó solo"],
            values=[val_cap, val_gan], hole=0.58,
            marker=dict(colors=["#1B2550","#48D9E0"], line=dict(color="#12082A", width=3)),
            textfont=dict(family="Sora", size=12),
            hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig3.add_annotation(text=f"×{multiplicador:.1f}x", x=0.5, y=0.5,
                            font=dict(family="Sora", size=26, color="#48D9E0"),
                            showarrow=False)
        fig3.update_layout(
            title=dict(text="El dinero trabajando por ti",
                       font=dict(family="Sora", size=12, color="#7A94C8")),
            height=310, **PLOT)
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    cols_show = ["Año", "Interés Simple", "Interés Compuesto",
                 "Ganancia Simple", "Ganancia Compuesta"]
    if aportacion > 0:
        cols_show += ["Compuesto + Aportación", "Total Aportado", "Ganancia Neta"]

    fmt = {c: "${:,.2f}" for c in cols_show if c != "Año"}
    st.dataframe(
        df[cols_show].style.format(fmt)
          .background_gradient(subset=["Interés Compuesto"], cmap="Blues")
          .background_gradient(subset=["Ganancia Compuesta"], cmap="Purples"),
        use_container_width=True, height=370,
    )
    csv = df[cols_show].to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Exportar CSV", data=csv,
                       file_name=f"simulador_{años}a_{tasa*100:.0f}pct.csv",
                       mime="text/csv")

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
