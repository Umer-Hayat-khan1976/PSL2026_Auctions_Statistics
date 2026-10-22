"""PSL 2026 Auction Analysis - Streamlit dashboard."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
DATA_FILE = "psl2026_auction_clean.csv"
ASSETS = Path("assets")  # optional: assets/players/<slug>.png, assets/teams/<slug>.png

BASE, SOLD = "base_price_pkr_lakh", "sold_price_pkr_lakh"

# Brand palette (edit freely)
NAVY, GREEN, GOLD = "#0B1F3A", "#00A651", "#F5B700"
INK, MUTED, LINE = "#14213D", "#64748B", "#E5E9F0"

TEAM_COLORS = {
    "Islamabad United": "#E31E24",
    "Karachi Kings": "#1E6FD9",
    "Lahore Qalandars": "#2FB44A",
    "Peshawar Zalmi": "#F5B700",
    "Quetta Gladiators": "#6B2FA0",
    "Hyderabad Kingsmen": "#F26B21",
    "Sialkot Stallionz": "#9B1B30",
    "Pindiz": "#0AA6B8",
}
ROLE_COLORS = {
    "Batsman": "#1E6FD9",
    "Bowler": "#E31E24",
    "All-rounder": GREEN,
    "Wicketkeeper-Batsman": GOLD,
}

st.set_page_config(page_title="PSL 2026 Auction Analysis", layout="wide")

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
#MainMenu, footer {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem; max-width: 1280px; }}

.hero {{
    background: linear-gradient(120deg, {NAVY} 0%, #123A5E 55%, #0A6B4A 100%);
    border-radius: 20px; padding: 2.4rem 2.6rem; color: #fff; margin-bottom: 1.2rem;
    border-bottom: 5px solid {GOLD};
}}
.hero .eyebrow {{ color: {GOLD}; font-weight: 700; letter-spacing: .18em; font-size: .78rem; }}
.hero h1 {{ color: #fff; font-size: 2.5rem; font-weight: 800; margin: .3rem 0 .4rem; padding: 0; }}
.hero p {{ color: #CBD5E1; font-size: 1.02rem; margin: 0; max-width: 720px; }}

.team-strip {{ display: flex; height: 6px; border-radius: 6px; overflow: hidden; margin-bottom: 1.6rem; }}
.team-strip div {{ flex: 1; }}

.kpi {{
    background: #fff; border: 1px solid {LINE}; border-radius: 16px; padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, .05); border-top: 4px solid var(--accent);
}}
.kpi .label {{ color: {MUTED}; font-size: .75rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; }}
.kpi .value {{ color: {INK}; font-size: 1.85rem; font-weight: 800; margin-top: .25rem; }}
.kpi .sub {{ color: {MUTED}; font-size: .82rem; margin-top: .1rem; }}

.section {{ margin: 2.2rem 0 .8rem; }}
.section .num {{ color: {GREEN}; font-weight: 800; font-size: .8rem; letter-spacing: .15em; }}
.section h2 {{ color: {INK}; font-size: 1.45rem; font-weight: 700; margin: 0; padding: 0; }}

.insight {{
    background: #F6FAF8; border: 1px solid #D5EBDF; border-left: 5px solid {GREEN};
    border-radius: 12px; padding: .9rem 1.3rem .5rem; margin-top: .4rem;
}}
.insight .title {{ color: {GREEN}; font-weight: 700; font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; }}
.insight ul {{ margin: .4rem 0 .5rem 1.1rem; padding: 0; color: {INK}; }}
.insight li {{ margin-bottom: .35rem; font-size: .95rem; }}

.player {{
    display: flex; align-items: center; gap: .9rem; background: #fff; border: 1px solid {LINE};
    border-radius: 16px; padding: .9rem 1rem; box-shadow: 0 2px 10px rgba(15, 23, 42, .05);
    border-left: 6px solid var(--team);
}}
.avatar {{
    width: 56px; height: 56px; border-radius: 50%; flex: none; display: flex; align-items: center;
    justify-content: center; color: #fff; font-weight: 800; background: var(--team); object-fit: cover;
    box-shadow: 0 0 0 3px #fff, 0 0 0 5px var(--team);
}}
.player .rank {{ color: {MUTED}; font-size: .7rem; font-weight: 700; letter-spacing: .1em; }}
.player .name {{ color: {INK}; font-weight: 700; font-size: 1.02rem; line-height: 1.2; }}
.player .meta {{ color: {MUTED}; font-size: .8rem; }}
.player .price {{ color: {INK}; font-weight: 800; font-size: 1.1rem; margin-top: .15rem; }}

.team-card {{
    background: #fff; border: 1px solid {LINE}; border-radius: 16px; padding: 1rem 1.1rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, .05); overflow: hidden; margin-bottom: 1rem;
    border-top: 6px solid var(--team);
}}
.team-card .tname {{ color: {INK}; font-weight: 700; font-size: 1rem; display: flex; align-items: center; gap: .5rem; }}
.team-card .tname img {{ height: 26px; }}
.team-card .row {{ display: flex; justify-content: space-between; color: {MUTED}; font-size: .83rem; margin-top: .4rem; }}
.team-card .row b {{ color: {INK}; }}

[data-testid="stSidebar"] {{ background: {NAVY}; }}
[data-testid="stSidebar"] * {{ color: #E2E8F0; }}
[data-testid="stSidebar"] h2 {{ color: {GOLD}; font-size: 1.05rem; letter-spacing: .08em; }}
[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {{ background: {GREEN}; }}
[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] * {{ color: #fff; }}
.stDownloadButton button {{
    background: {GREEN}; color: #fff; border: 0; border-radius: 10px; font-weight: 600; padding: .6rem 1.2rem;
}}
.stDownloadButton button:hover {{ background: #008A45; color: #fff; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_FILE)
    for col in (BASE, SOLD):
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data


# --------------------------------------------------------------------------
# UI helpers
# --------------------------------------------------------------------------
def slug(text: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in text).strip("_")


def lakh(value: float) -> str:
    return f"{value:,.0f} lakh"


def image_uri(kind: str, name: str) -> str | None:
    """Return a data URI for assets/<kind>/<slug>.png if it exists."""
    import base64

    for ext in ("png", "jpg", "jpeg", "webp"):
        path = ASSETS / kind / f"{slug(name)}.{ext}"
        if path.exists():
            encoded = base64.b64encode(path.read_bytes()).decode()
            return f"data:image/{ext};base64,{encoded}"
    return None


def initials(name: str) -> str:
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def section(number: str, title: str) -> None:
    st.markdown(
        f'<div class="section"><div class="num">{number}</div><h2>{title}</h2></div>',
        unsafe_allow_html=True,
    )


def kpi(col, label: str, value: str, sub: str, accent: str) -> None:
    col.markdown(
        f'<div class="kpi" style="--accent:{accent}"><div class="label">{label}</div>'
        f'<div class="value">{value}</div><div class="sub">{sub}</div></div>',
        unsafe_allow_html=True,
    )


def insights(points: list[str]) -> None:
    """Render chart insights as a styled markdown bullet list."""
    items = "\n".join(f"- {p}" for p in points)
    st.markdown(
        f'<div class="insight"><div class="title">Key insights</div>\n\n{items}\n\n</div>',
        unsafe_allow_html=True,
    )


def style_fig(fig: go.Figure, height: int = 400) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=INK, size=13),
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(orientation="h", y=-0.2, title=None),
    )
    fig.update_xaxes(showgrid=False, linecolor=LINE, title_font=dict(color=MUTED))
    fig.update_yaxes(gridcolor=LINE, zeroline=False, title_font=dict(color=MUTED))
    return fig


def show(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
strip = "".join(f'<div style="background:{c}"></div>' for c in TEAM_COLORS.values())
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">PAKISTAN SUPER LEAGUE</div>
        <h1>PSL 2026 Auction Analysis</h1>
        <p>Explore player roles, team squads and recorded auction prices
        across all eight franchises.</p>
    </div>
    """
    + f'<div class="team-strip">{strip}</div>',
    unsafe_allow_html=True,
)

df = load_data()

# --------------------------------------------------------------------------
# Sidebar filters
# --------------------------------------------------------------------------
st.sidebar.header("FILTER PLAYERS")
teams = sorted(df["team"].dropna().unique())
roles = sorted(df["role"].dropna().unique())

selected_teams = st.sidebar.multiselect("Team", teams, default=teams)
selected_roles = st.sidebar.multiselect("Player role", roles, default=roles)

filtered = df[df["team"].isin(selected_teams) & df["role"].isin(selected_roles)].copy()

if filtered.empty:
    st.warning("No players match the current filters. Adjust the sidebar selection.")
    st.stop()

sold = filtered[SOLD].dropna()

# --------------------------------------------------------------------------
# Key metrics
# --------------------------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
kpi(c1, "Player records", f"{len(filtered)}", f"{filtered['team'].nunique()} teams", GREEN)
kpi(c2, "Average sold price", lakh(sold.mean()) if not sold.empty else "N/A", "PKR lakh", GOLD)
kpi(c3, "Highest sold price", lakh(sold.max()) if not sold.empty else "N/A", "PKR lakh", "#E31E24")
kpi(c4, "Total recorded spend", lakh(sold.sum()) if not sold.empty else "N/A", "PKR lakh", "#1E6FD9")

st.caption(
    "Prices are in PKR lakh. Metrics describe the recorded data "
    "and do not independently verify auction outcomes."
)

# --------------------------------------------------------------------------
# Top buys
# --------------------------------------------------------------------------
section("TOP BUYS", "Highest Recorded Sold Prices")
top = filtered.nlargest(4, SOLD).reset_index(drop=True)
for i, (col, row) in enumerate(zip(st.columns(len(top)), top.itertuples()), start=1):
    color = TEAM_COLORS.get(row.team, GREEN)
    photo = image_uri("players", row.player_name)
    avatar = (
        f'<img class="avatar" src="{photo}">'
        if photo
        else f'<div class="avatar">{initials(row.player_name)}</div>'
    )
    col.markdown(
        f"""<div class="player" style="--team:{color}">{avatar}<div>
        <div class="rank">#{i} &middot; {row.role.upper()}</div>
        <div class="name">{row.player_name}</div>
        <div class="meta">{row.team}</div>
        <div class="price">{lakh(getattr(row, SOLD))}</div></div></div>""",
        unsafe_allow_html=True,
    )

# --------------------------------------------------------------------------
# Chart 1: player counts by role
# --------------------------------------------------------------------------
section("01", "Player Records by Role")
role_counts = filtered["role"].value_counts()

fig1 = px.bar(
    x=role_counts.index,
    y=role_counts.values,
    color=role_counts.index,
    color_discrete_map=ROLE_COLORS,
    text=role_counts.values,
    labels={"x": "Player role", "y": "Number of records"},
)
fig1.update_traces(textposition="outside", marker_cornerradius=6)
fig1.update_layout(showlegend=False)
show(style_fig(fig1))

share = role_counts / role_counts.sum() * 100
points = [
    f"**{role_counts.idxmax()}** is the largest group with **{role_counts.max()} records** "
    f"({share.max():.0f}% of the filtered squad)."
]
if len(role_counts) > 1:
    points.append(
        f"**{role_counts.idxmin()}** is the smallest group with only **{role_counts.min()} records** "
        f"({share.min():.0f}%)."
    )
    points.append(
        f"The gap between the largest and smallest role is **{role_counts.max() - role_counts.min()} players**."
    )
if {"Batsman", "Bowler"} <= set(role_counts.index):
    points.append(
        f"Bowlers outnumber batsmen **{role_counts['Bowler']} to {role_counts['Batsman']}**."
        if role_counts["Bowler"] > role_counts["Batsman"]
        else f"Batsmen outnumber bowlers **{role_counts['Batsman']} to {role_counts['Bowler']}**."
    )
insights(points)

# --------------------------------------------------------------------------
# Chart 2: average sold price by role
# --------------------------------------------------------------------------
section("02", "Average Recorded Sold Price by Role")
role_stats = (
    filtered.groupby("role")[SOLD].agg(["mean", "median", "max"]).dropna().sort_values("mean", ascending=False)
)

if role_stats.empty:
    st.info("No valid sold prices are available for these filters.")
else:
    fig2 = px.bar(
        x=role_stats.index,
        y=role_stats["mean"],
        color=role_stats.index,
        color_discrete_map=ROLE_COLORS,
        text=role_stats["mean"].round(1),
        labels={"x": "Player role", "y": "Average sold price (PKR lakh)"},
    )
    fig2.update_traces(textposition="outside", marker_cornerradius=6)
    fig2.update_layout(showlegend=False)
    show(style_fig(fig2))

    top_role, low_role = role_stats["mean"].idxmax(), role_stats["mean"].idxmin()
    points = [
        f"**{top_role}** commands the highest average price at **{lakh(role_stats['mean'].max())}**."
    ]
    if len(role_stats) > 1:
        ratio = role_stats["mean"].max() / role_stats["mean"].min()
        points.append(
            f"**{low_role}** has the lowest average at **{lakh(role_stats['mean'].min())}**, "
            f"so the top role averages **{ratio:.1f}x** more."
        )
    skewed = role_stats[role_stats["mean"] > role_stats["median"] * 1.5]
    if not skewed.empty:
        names = ", ".join(f"**{r}**" for r in skewed.index)
        points.append(
            f"The average is well above the median for {names}, meaning a few "
            "expensive stars pull the average up while most players sell for far less."
        )
    top_player = filtered.loc[filtered[SOLD].idxmax()]
    points.append(
        f"The single most expensive record is **{top_player.player_name}** "
        f"({top_player.role}, {top_player.team}) at **{lakh(top_player[SOLD])}**."
    )
    insights(points)

# --------------------------------------------------------------------------
# Chart 3: base price vs sold price
# --------------------------------------------------------------------------
section("03", "Base Price vs Recorded Sold Price")
scatter = filtered.dropna(subset=[BASE, SOLD]).copy()
missing_base = len(filtered) - len(scatter)

if scatter.empty:
    st.info("No complete base-price and sold-price pairs are available.")
else:
    fig3 = px.scatter(
        scatter,
        x=BASE,
        y=SOLD,
        color="team",
        color_discrete_map=TEAM_COLORS,
        hover_name="player_name",
        hover_data={"role": True, "team": False, BASE: ":,.0f", SOLD: ":,.0f"},
        labels={BASE: "Base price (PKR lakh)", SOLD: "Sold price (PKR lakh)", "team": "Team"},
    )
    top_base = scatter[BASE].max()
    fig3.add_trace(
        go.Scatter(
            x=[0, top_base],
            y=[0, top_base],
            mode="lines",
            name="Sold = base",
            line=dict(color=MUTED, dash="dash", width=1.5),
            hoverinfo="skip",
        )
    )
    fig3.update_traces(
        marker=dict(size=11, opacity=0.8, line=dict(width=1, color="#fff")),
        selector=dict(mode="markers"),
    )
    show(style_fig(fig3, 460))

    points = []
    if len(scatter) > 2 and scatter[BASE].nunique() > 1:
        corr = scatter[BASE].corr(scatter[SOLD])
        strength = "strong" if abs(corr) >= 0.7 else "moderate" if abs(corr) >= 0.4 else "weak"
        points.append(
            f"Base and sold prices show a **{strength} positive relationship** (correlation **{corr:.2f}**): "
            "higher base prices generally lead to higher sold prices."
        )
    above = (scatter[SOLD] > scatter[BASE]).mean() * 100
    at_base = (scatter[SOLD] == scatter[BASE]).mean() * 100
    points.append(
        f"**{above:.0f}%** of players sold above their base price, while **{at_base:.0f}%** sold exactly at base."
    )
    scatter["multiple"] = scatter[SOLD] / scatter[BASE]
    best = scatter.loc[scatter["multiple"].idxmax()]
    points.append(
        f"The biggest jump is **{best.player_name}** ({best.team}), who sold for "
        f"**{best.multiple:.1f}x** the base price ({lakh(best[BASE])} to {lakh(best[SOLD])})."
    )
    points.append(f"The median player sold for **{scatter['multiple'].median():.2f}x** the base price.")
    if missing_base:
        points.append(
            f"**{missing_base} records** have no base price (for example direct signings) "
            "and are excluded from this chart."
        )
    insights(points)

# --------------------------------------------------------------------------
# Team snapshot
# --------------------------------------------------------------------------
section("TEAMS", "Squad Snapshot")
team_stats = (
    filtered.groupby("team")
    .agg(players=("player_name", "count"), total=(SOLD, "sum"), avg=(SOLD, "mean"))
    .sort_values("total", ascending=False)
)
for start in range(0, len(team_stats), 4):
    chunk = team_stats.iloc[start : start + 4]
    for col, (team, row) in zip(st.columns(4), chunk.iterrows()):
        logo = image_uri("teams", team)
        logo_html = f'<img src="{logo}">' if logo else ""
        col.markdown(
            f"""<div class="team-card" style="--team:{TEAM_COLORS.get(team, GREEN)}">
            <div class="tname">{logo_html}{team}</div>
            <div class="row"><span>Players</span><b>{int(row.players)}</b></div>
            <div class="row"><span>Total spend</span><b>{lakh(row.total)}</b></div>
            <div class="row"><span>Average price</span><b>{lakh(row.avg)}</b></div></div>""",
            unsafe_allow_html=True,
        )

# --------------------------------------------------------------------------
# Data table and download
# --------------------------------------------------------------------------
section("DATA", "Player Records")
with st.expander("View filtered player records"):
    st.dataframe(filtered, width="stretch", hide_index=True)

st.download_button(
    label="Download filtered clean data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="psl2026_auction_filtered.csv",
    mime="text/csv",
)
