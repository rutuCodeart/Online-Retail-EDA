import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
# -----------------------------------------
# ✅ PROFESSIONAL PDF REPORT (ReportLab)
# -----------------------------------------

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

import matplotlib.pyplot as plt
import pandas as pd
import io
# -----------------------------
# ✅ Excel Report
# -----------------------------
import openpyxl

# -----------------------------
# ✅ CSV Report
# -----------------------------
def generate_csv(df):
    file = "report.csv"
    df.to_csv(file, index=False)

    st.success("✅ CSV Report Ready")

    st.download_button(
        "📥 Download CSV",
        open(file, "rb"),
        file,
        "text/csv"
    )


def generate_excel(df):
    file = "report.xlsx"
    df.to_excel(file, index=False)

    st.success("✅ Excel Report Ready")

    st.download_button(
        "📥 Download Excel",
        open(file, "rb"),
        file,
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def generate_pdf(df):

    file = "Professional_Report.pdf"

    doc = SimpleDocTemplate(file, pagesize=A4)

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["Normal"]

    elements = []

    # -----------------------------------
    # ✅ TITLE
    # -----------------------------------
    title = Paragraph("<b>Retail Analytics Report</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 15))

    # -----------------------------------
    # ✅ SUMMARY KPIs
    # -----------------------------------
    total_sales = df["TotalSales"].sum()
    total_orders = df["InvoiceNo"].nunique()
    avg_order = total_sales / total_orders

    summary_data = [
        ["Metric", "Value"],
        ["Total Sales", f"{total_sales:,.2f}"],
        ["Total Orders", total_orders],
        ["Avg Order Value", f"{avg_order:,.2f}"],
    ]

    table = Table(summary_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # -----------------------------------
    # ✅ TOP PRODUCTS TABLE
    # -----------------------------------
    top = (
        df.groupby("Description")["TotalSales"]
        .sum()
        .reset_index()
        .sort_values("TotalSales", ascending=False)
        .head(10)
    )

    top_data = [["Product", "Sales"]] + top.values.tolist()

    top_table = Table(top_data, repeatRows=1)
    top_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightblue),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(Paragraph("<b>Top 10 Products</b>", normal_style))
    elements.append(top_table)
    elements.append(Spacer(1, 20))

    # -----------------------------------
    # ✅ SALES BAR CHART (Image Insert)
    # -----------------------------------
    plt.figure()
    top.plot(kind="bar", x="Description", y="TotalSales")
    plt.xticks(rotation=45)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="PNG")
    plt.close()

    img_buffer.seek(0)

    img = Image(img_buffer, width=400, height=250)
    elements.append(Paragraph("<b>Top Products Chart</b>", normal_style))
    elements.append(img)

    # -----------------------------------
    # ✅ Build PDF
    # -----------------------------------
    doc.build(elements)

    st.success("✅ Professional PDF Generated")

    st.download_button(
        "📥 Download PDF",
        open(file, "rb"),
        file,
        "application/pdf"
    )
    
  
# --- Session State ---
if 'data_uploaded' not in st.session_state:
    st.session_state.data_uploaded = False
if 'df' not in st.session_state:
    st.session_state.df = None
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"

# --- Page config ---
st.set_page_config(page_title="💼 Retail Analytics Pro", layout="wide", page_icon="📊")

# --- Theme ---
theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=["Light","Dark"].index(st.session_state.theme))
st.session_state.theme = theme
if theme == "Dark":
    bg_color = "#121212"
    text_color = "#e0e0e0"
    card_bg = "#1e293b"
    chart_colors = ['#6366f1', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b']
else:
    bg_color = "#f9fafb"
    text_color = "#111827"
    card_bg = "#e0e7ff"
    chart_colors = ['#1e40af', '#7c3aed', '#dc2626', '#059669', '#d97706']

# --- CSS Styling ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
html, body, #root, .appview-container, .main {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'Poppins', sans-serif;
}}
.kpi {{
    background: linear-gradient(135deg, {card_bg}, rgba(99,102,241,0.2));
    padding: 2rem 2.5rem;
    border-radius: 24px;
    text-align: center;
    color: {text_color};
    box-shadow: 0px 12px 32px 0px rgba(149, 157, 165, 0.25);
}}
.kpi:hover {{
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0px 20px 40px 0px rgba(99,102,241,0.4);
}}
.chart-container {{
    animation: chartSlideIn 1s ease-out forwards;
    opacity: 0;
    transform: translateY(30px);
}}
@keyframes chartSlideIn {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}
.stButton > button {{
    background: linear-gradient(135deg, #10b981, #059669);
    color:white;
    border:none;
    border-radius: 40px;
    padding: 12px 32px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 4px 15px rgba(16,185,129,0.3);
    width:100%;
}}
.stButton > button:hover {{
    box-shadow: 0 12px 25px rgba(16,185,129,0.5);
    transform: translateY(-2px) scale(1.05);
}}
.filter-section {{
    background: {card_bg};
    padding: 1.5rem;
    border-radius: 20px;
    margin: 1rem 0;
    border: 1px solid rgba(255,255,255,0.1);
}}
.pulse-animation {{
    animation: pulse-glow 2s ease-in-out infinite;
}}
@keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 0 0 rgba(99,102,241,0.4); }}
    50% {{ box-shadow: 0 0 0 20px rgba(99,102,241,0); }}
}}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("💼 Retail Analytics Pro")
page = st.sidebar.selectbox("Select Page", ["Welcome", "Data Analysis", "Features", "About", "Contact"])

# --- Welcome / Main Page ---
if page == "Welcome":

    st.markdown("""
    <div class="welcome-box">
        <h1>🚀 Welcome to Retail Analytics Pro</h1>
        <p>Upload your retail CSV and get instant insights!</p>
    </div>

    <style>

    /* -----------------------------
       SKY BLUE ANIMATED BOX
    ------------------------------*/
    .welcome-box {
        background: linear-gradient(135deg, rgba(135,206,250,0.95), rgba(0,191,255,0.9));
        padding: 4rem;
        border-radius: 2.2rem;
        text-align: center;
        color: #003352;

        /* sky blue glow */
        box-shadow: 0 0 25px rgba(135,206,250,0.7),
                    0 0 45px rgba(0,191,255,0.5);

        animation: fadeUp 1.2s ease forwards,
                   float 4s ease-in-out infinite;

        opacity: 0;
        transform: translateY(40px);
    }

    .welcome-box h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .welcome-box p {
        font-size: 1.3rem;
        opacity: 0.9;
    }

    /* -----------------------------
       FADE-IN ANIMATION
    ------------------------------*/
    @keyframes fadeUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* -----------------------------
       FLOATING EFFECT
    ------------------------------*/
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
        100% { transform: translateY(0px); }
    }

    </style>
    """, unsafe_allow_html=True)

    # ✅ Space below hero
    st.markdown("<br>", unsafe_allow_html=True)

    # ✅ Video (optional)
    # st.video("videoplayback.mp4")


    uploaded_file = st.file_uploader("📁 Choose CSV file", type=['csv'])

    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file
        st.success("File uploaded! Ab 'Data Analysis' page pe jao.")

    if 'uploaded_file' in st.session_state:
        with st.spinner("Processing data..."):
            time.sleep(1.5)
            df = pd.read_csv(st.session_state['uploaded_file'])
            st.session_state.df = df  # Ye line sabse important hai
        
        st.info("File loaded! Ab left side se 'Data Analysis' page pe jao.")

        # --- Data processing ---
        if 'InvoiceDate' in df.columns:
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
            df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
                df['Month'] = df['InvoiceDate'].dt.month
                df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek
            if all(col in df.columns for col in ['Quantity','UnitPrice']):
                df['TotalSales'] = df['Quantity'] * df['UnitPrice']
            if 'InvoiceNo' in df.columns:
                df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C')
                df = df[~df['IsCancelled']]
            
            st.session_state.df = df
            st.session_state.data_uploaded = True
            st.success("✅ Data processed successfully! 🎉")
            #st_lottie(lottie_confetti, height=200, key="confetti")
            #st.balloons()
            
            # --- Summary Table ---
            st.subheader("📊 Data Summary")
            summary_metrics = {
                "Total Revenue": df['TotalSales'].sum() if 'TotalSales' in df.columns else 0,
                "Total Orders": df['InvoiceNo'].nunique() if 'InvoiceNo' in df.columns else 0,
                "Average Order Value": df['TotalSales'].sum()/df['InvoiceNo'].nunique() if ('TotalSales' in df.columns and 'InvoiceNo' in df.columns and df['InvoiceNo'].nunique()>0) else 0,
                "Unique Customers": df['CustomerID'].nunique() if 'CustomerID' in df.columns else 0,
                "Unique Products": df['StockCode'].nunique() if 'StockCode' in df.columns else 0,
                "Cancelled Orders": df['IsCancelled'].sum() if 'IsCancelled' in df.columns else 0,
                "Min Order Value": df['TotalSales'].min() if 'TotalSales' in df.columns else 0,
                "Max Order Value": df['TotalSales'].max() if 'TotalSales' in df.columns else 0,
                "Median Order Value": df['TotalSales'].median() if 'TotalSales' in df.columns else 0,
                "Average Quantity": df['Quantity'].mean() if 'Quantity' in df.columns else 0,
                "Max Quantity": df['Quantity'].max() if 'Quantity' in df.columns else 0,
                "Min Quantity": df['Quantity'].min() if 'Quantity' in df.columns else 0,
                "Total Quantity Sold": df['Quantity'].sum() if 'Quantity' in df.columns else 0,
                "Most Sold Product": df.groupby('StockCode')['Quantity'].sum().idxmax() if 'StockCode' in df.columns else "N/A",
                "Top Country by Revenue": df.groupby('Country')['TotalSales'].sum().idxmax() if 'Country' in df.columns else "N/A"
            }
            st.table(pd.DataFrame.from_dict(summary_metrics, orient='index', columns=["Value"]))

# --- Data Analysis Page ---
elif page == "Data Analysis":
    if not st.session_state.data_uploaded:
        st.error("❌ Please upload your CSV file first on the Welcome page!")
        st.stop()
    
    df = st.session_state.df.copy()
    st.header("📊 Retail Dashboard")
    
    # --- Filters ---
    with st.sidebar:
        st.markdown('<div class="filter-section">🔧 Filters</div>', unsafe_allow_html=True)
        selected_countries, selected_customers, date_range = [], [], []
        if 'Country' in df.columns:
            countries = df['Country'].dropna().unique()
            selected_countries = st.multiselect("🌍 Countries", countries, default=countries.tolist())
        if 'CustomerID' in df.columns:
            customers = df['CustomerID'].dropna().unique()
            selected_customers = st.multiselect("👥 Customers", customers, default=customers[:20])
        if 'InvoiceDate' in df.columns:
            date_range = st.date_input("📅 Date Range", [df['InvoiceDate'].min().date(), df['InvoiceDate'].max().date()])
    
    # --- Apply Filters ---
    if selected_countries:
        df = df[df['Country'].isin(selected_countries)]
    if selected_customers:
        df = df[df['CustomerID'].isin(selected_customers)]
    if date_range:
        df = df[(df['InvoiceDate'] >= pd.to_datetime(date_range[0])) & (df['InvoiceDate'] <= pd.to_datetime(date_range[1]))]
    
    # --- KPIs ---
    total_sales = df['TotalSales'].sum() if 'TotalSales' in df.columns else 0
    total_orders = df['InvoiceNo'].nunique() if 'InvoiceNo' in df.columns else 0
    avg_order = total_sales / total_orders if total_orders else 0
    top_product = df.groupby('StockCode')['TotalSales'].sum().idxmax() if 'StockCode' in df.columns else "N/A"
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    st.markdown("### 📥 Generate Reports")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 PDF Report"):
            generate_pdf(df)
    
    with col2:
        if st.button("📊 Excel Report"):
            generate_excel(df)
    
    with col3:
        if st.button("💾 CSV Report"):
            generate_csv(df)
    
        
    kpi_col1.markdown(f"<div class='kpi'>💰<h3>Total Revenue</h3><h2>₹{total_sales:,.0f}</h2></div>", unsafe_allow_html=True)
    kpi_col2.markdown(f"<div class='kpi'>📦<h3>Total Orders</h3><h2>₹{total_orders:,}</h2></div>", unsafe_allow_html=True)
    kpi_col3.markdown(f"<div class='kpi'>💵<h3>Avg Order</h3><h2>₹{avg_order:,.0f}</h2></div>", unsafe_allow_html=True)
    kpi_col4.markdown(f"<div class='kpi'>⭐<h3>Top Product</h3><h2>₹{top_product}</h2></div>", unsafe_allow_html=True)
    
    # --- Tabs for charts ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Data", "🌍 Markets", "👥 Customers", "📈 Trends", "⭐ Products",  "💰 Profit",])
    
    with tab1:
        st.dataframe(df.head(1000), use_container_width=True)
        st.download_button("💾 Download Filtered Data", df.to_csv(index=False).encode(), "retail_data_filtered.csv", "text/csv")
    
    with tab2:
        if 'Country' in df.columns and 'InvoiceDate' in df.columns and 'TotalSales' in df.columns:
            temp = df.copy()
            temp['YearMonth'] = temp['InvoiceDate'].dt.to_period('M').astype(str)
            country_sales = (
                temp.groupby(['YearMonth','Country'])['TotalSales']
                .sum().reset_index()
            )
            # Top N countries overall
            top_countries = (
                country_sales.groupby('Country')['TotalSales']
                .sum().sort_values(ascending=False).head(10).index
            )
            country_sales = country_sales[country_sales['Country'].isin(top_countries)]
            
            fig = px.bar(
                country_sales,
                x='Country',
                y='TotalSales',
                color='TotalSales',
                color_continuous_scale='Viridis',
                animation_frame='YearMonth',
                title="🌍 Top Markets Over Time"
            )
            
            # Animation ko slow / readable banane ke liye
            fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1200 # 1.2 second per frame
            fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 600 # smooth transition
            
            fig.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font_color=text_color,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif 'Country' in df.columns and 'TotalSales' in df.columns:
            # Fallback: static chart if date nahi
            country_sales = (
                df.groupby('Country')['TotalSales']
                .sum().sort_values(ascending=False).head(10).reset_index()
            )
            fig = px.bar(
                country_sales, x='Country', y='TotalSales', text_auto=True,
                color='TotalSales', color_continuous_scale='Viridis',
                title="🌍 Top Markets"
            )
            fig.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font_color=text_color,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if {'CustomerID','InvoiceDate','TotalSales'}.issubset(df.columns):
            temp = df.copy()
            temp['YearMonth'] = temp['InvoiceDate'].dt.to_period('M').astype(str)
            
            # Har month ke Top 15 customers
            monthly_customer = (
                temp.groupby(['YearMonth','CustomerID'])['TotalSales']
                .sum().reset_index()
            )
            
            # Overall top 15 customers choose kar lo
            top_customers = (
                monthly_customer.groupby('CustomerID')['TotalSales']
                .sum().sort_values(ascending=False).head(15).index
            )
            monthly_customer = monthly_customer[monthly_customer['CustomerID'].isin(top_customers)]
            
            fig = px.bar(
                monthly_customer,
                x='CustomerID',
                y='TotalSales',
                color='TotalSales',
                color_continuous_scale='Plasma',
                animation_frame='YearMonth',
                title="👥 Top Customers Over Time"
            )
            
            # yahan speed slow kar rahe hain
            fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1200 # har frame 1.2 sec
            fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 600 # smooth transition
            
            fig.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font_color=text_color,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif {'CustomerID','TotalSales'}.issubset(df.columns):
            # fallback: tumhara original static chart
            customer_sales = (
                df.groupby('CustomerID')['TotalSales']
                .sum().sort_values(ascending=False).head(15).reset_index()
            )
            fig = px.bar(
                customer_sales,
                x='CustomerID',
                y='TotalSales',
                text_auto=True,
                color='TotalSales',
                color_continuous_scale='Plasma',
                title="👥 Top Customers"
            )
            fig.update_layout(
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font_color=text_color,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        if 'InvoiceDate' in df.columns and 'TotalSales' in df.columns:
            temp = df.copy()
            temp['YearMonth'] = temp['InvoiceDate'].dt.to_period('M')
            monthly_sales = (
                temp.groupby('YearMonth')['TotalSales']
                .sum().reset_index()
            )
            monthly_sales['YearMonthStr'] = monthly_sales['YearMonth'].dt.strftime('%b %Y')
            
            fig_trend = px.line(
                monthly_sales,
                x='YearMonthStr',
                y='TotalSales',
                markers=True,
                title="📈 Monthly Revenue Trend",
            )
            fig_trend.update_traces(line=dict(color='#6366f1', width=4))
            
            # animation: cumulative frame-wise
            frames = []
            for i in range(1, len(monthly_sales)+1):
                frames.append(
                    go.Frame(
                        data=[go.Scatter(
                            x=monthly_sales['YearMonthStr'][:i],
                            y=monthly_sales['TotalSales'][:i],
                            mode='lines+markers',
                            line=dict(color='#6366f1', width=4),
                            marker=dict(size=8),
                            name='Revenue'
                        )],
                        name=str(i)
                    )
                )
            fig_trend.frames = frames
            fig_trend.update_layout(
                xaxis_title="Month",
                yaxis_title="Total Revenue ($)",
                xaxis_tickangle=-45,
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font=dict(color=text_color),
                updatemenus=[{
                    "type": "buttons",
                    "buttons": [
                        {"label": "Play", "method": "animate",
                         "args": [None, {"frame": {"duration": 900, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 600}}]},
                        {"label": "Pause", "method": "animate",
                         "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                         "mode": "immediate",
                                         "transition": {"duration": 0}}]}
                    ]
                }]
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.warning("⚠️ Required columns 'InvoiceDate' and 'TotalSales' not found.")
    
    with tab5:
        if 'StockCode' in df.columns:
            product_sales = df.groupby('StockCode')['TotalSales'].sum().sort_values(ascending=False).head(15).reset_index()
            fig = px.treemap(product_sales, path=['StockCode'], values='TotalSales',
                           color='TotalSales', color_continuous_scale='RdYlGn', title="⭐ Top Products")
            fig.update_layout(plot_bgcolor=bg_color, paper_bgcolor=bg_color, font_color=text_color)
            st.plotly_chart(fig, use_container_width=True)
    with tab6:
        st.subheader("✨ Profit Bars ")
    
        required_cols = ["Description", "Quantity", "UnitPrice"]
    
        if all(col in df.columns for col in required_cols):
    
            # ✅ Profit calculation
            df["TotalSales"] = df["Quantity"] * df["UnitPrice"]
            df["Profit"] = df["TotalSales"]
    
            # ✅ Top 10 categories
            top = (
                df.groupby("Description")["Profit"]
                .sum()
                .reset_index()
                .sort_values("Profit", ascending=False)
                .head(10)
            )
    
            categories = top["Description"].tolist()
            profits = top["Profit"].tolist()
    
            import plotly.graph_objects as go
            import plotly.colors as pc
            import numpy as np
    
            # ✅ Multi-color palette
            colors = pc.qualitative.Bold[:len(profits)]
    
            # ✅ Initial figure → all bars 0 height
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=categories,
                        y=[0] * len(profits),
                        marker=dict(color=colors, line=dict(width=1, color="black")),
                        opacity=0.9,
                    )
                ]
            )
    
            # ----------------------------------------------------------
            # ✅ Frames → One-by-One reveal animation with bounce
            # ----------------------------------------------------------
            frames = []
    
            bounce_steps = 6  # bounce animation smoothness
    
            for bar_idx in range(len(profits)):
    
                # For each bar we animate bounce growth
                for step in range(1, bounce_steps + 1):
    
                    bounce = 1 + 0.25 * np.sin(step * np.pi / bounce_steps)
    
                    y_vals = []
    
                    for j in range(len(profits)):
                        if j < bar_idx:
                            # already grown bars → final value
                            y_vals.append(profits[j])
                        elif j == bar_idx:
                            # currently animating bar
                            y_vals.append(profits[j] * bounce)
                        else:
                            # not reached yet → zero
                            y_vals.append(0)
    
                    frames.append(
                        go.Frame(
                            name=f"bar{bar_idx}_step{step}",
                            data=[
                                go.Bar(
                                    x=categories,
                                    y=y_vals,
                                    marker=dict(color=colors, line=dict(width=1, color="black")),
                                    opacity=0.95,
                                )
                            ]
                        )
                    )
    
            # ✅ Final frame → sab bars real value
            frames.append(
                go.Frame(
                    name="final",
                    data=[
                        go.Bar(
                            x=categories,
                            y=profits,
                            marker=dict(color=colors, line=dict(width=1, color="black")),
                            opacity=1,
                        )
                    ]
                )
            )
    
            fig.frames = frames
    
            # ----------------------------------------------------------
            # ✅ Layout + professional play button
            # ----------------------------------------------------------
            fig.update_layout(
                title="✨ Premium Animated Bars",
                template="plotly_white",
                xaxis_title="Product Category",
                yaxis_title="Profit",
    
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="right",
                        x=0.0,
                        y=1.15,
                        showactive=True,
                        buttons=[
                            dict(
                                label="▶ Play",
                                method="animate",
                                args=[
                                    None,
                                    {
                                        "frame": {"duration": 180, "redraw": True},
                                        "transition": {"duration": 0},
                                        "fromcurrent": True,
                                    },
                                ],
                            ),
                            dict(
                                label="⏸ Pause",
                                method="animate",
                                args=[
                                    [None],
                                    {"frame": {"duration": 0}, "mode": "immediate"},
                                ],
                            ),
                        ],
                    )
                ],
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
        else:
            st.warning("⚠️ Required columns missing.")


            # --- Vertical Chart Buttons ---
        st.markdown("---")
        st.subheader("📊 Visualizations")
            
    # Bubble Chart
    if st.button("📊 Show Customer Bubble Chart", key="bubble_chart"):
        if 'InvoiceDate' in df.columns and 'CustomerID' in df.columns and 'TotalSales' in df.columns and 'InvoiceNo' in df.columns:
            bubble_df = df.copy()
            bubble_df['YearMonth'] = bubble_df['InvoiceDate'].dt.to_period('M').astype(str)
            customer_summary = bubble_df.groupby(['YearMonth', 'CustomerID']).agg(
                TotalSales=('TotalSales', 'sum'),
                Orders=('InvoiceNo', 'nunique')
            ).reset_index()
            customer_summary['AvgOrder'] = customer_summary['TotalSales'] / customer_summary['Orders']
            fig_bubble = px.scatter(
                customer_summary,
                x='Orders',
                y='TotalSales',
                size='AvgOrder',
                color='CustomerID',
                animation_frame='YearMonth',
                hover_name='CustomerID',
                size_max=60,
                title="👥 Customer Spending & Orders Over Time"
            )
            fig_bubble.update_layout(
                xaxis_title="Number of Orders",
                yaxis_title="Total Spending ($)",
                plot_bgcolor=bg_color,
                paper_bgcolor=bg_color,
                font_color=text_color
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
    
    # Animated Pie Chart
    if st.button("📊 Show Animated Pie Chart (Top 10 Products)", key="animated_pie"):
        if 'InvoiceDate' in df.columns and 'Description' in df.columns and 'TotalSales' in df.columns:
            df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
            pie_df = df.groupby(['YearMonth', 'Description'])['TotalSales'].sum().reset_index()
            top_products = df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10).index
            pie_df = pie_df[pie_df['Description'].isin(top_products)]
            months = pie_df['YearMonth'].unique()
            fig = go.Figure(
                data=[go.Pie(
                    labels=pie_df[pie_df['YearMonth']==months[0]]['Description'],
                    values=pie_df[pie_df['YearMonth']==months[0]]['TotalSales'],
                    hole=0.3,
                    textinfo='percent+label'
                )],
                layout=go.Layout(
                    title="⭐ Top 10 Best-Selling Products Over Time",
                    plot_bgcolor=bg_color,
                    paper_bgcolor=bg_color,
                    font_color=text_color,
                    updatemenus=[{
                        "type":"buttons",
                        "buttons":[
                            {"label":"Play","method":"animate","args":[None, {"frame":{"duration":1000,"redraw":True},"fromcurrent":True,"transition":{"duration":500}}]},
                            {"label":"Pause","method":"animate","args":[[None], {"frame":{"duration":0,"redraw":False},"mode":"immediate","transition":{"duration":0}}]}
                        ]
                    }]
                ),
                frames=[
                    go.Frame(
                        data=[go.Pie(
                            labels=pie_df[pie_df['YearMonth']==month]['Description'],
                            values=pie_df[pie_df['YearMonth']==month]['TotalSales'],
                            hole=0.3,
                            textinfo='percent+label'
                        )],
                        name=month
                    ) for month in months
                ]
            )
            st.plotly_chart(fig, use_container_width=True)
    
   #3DDD
  # 3D Bars
    if st.button("📊 Show 3D Movable Vertical Bars", key="3d_bars"):
        if 'InvoiceDate' in df.columns and 'TotalSales' in df.columns:
            monthly_sales = df.groupby(df['InvoiceDate'].dt.to_period('M'))['TotalSales'].sum().reset_index()
            monthly_sales['Month'] = monthly_sales['InvoiceDate'].dt.strftime('%b %Y')
            monthly_sales = monthly_sales.sort_values('InvoiceDate')
            x_pos = np.arange(len(monthly_sales))
            y_pos = np.zeros(len(monthly_sales))
            heights = monthly_sales['TotalSales'].values
            import plotly.graph_objects as go

            fig = go.Figure()

            for xi, yi, hi, month in zip(x_pos, y_pos, heights, monthly_sales['Month']):
                x_corners = [xi, xi+0.5, xi+0.5, xi, xi, xi+0.5, xi+0.5, xi]
                y_corners = [yi, yi, yi+0.5, yi+0.5, yi, yi, yi+0.5, yi+0.5]
                z_corners = [0, 0, 0, 0, hi, hi, hi, hi]
                fig.add_trace(go.Mesh3d(
                    x=x_corners,
                    y=y_corners,
                    z=z_corners,
                    color=chart_colors[xi % len(chart_colors)],
                    opacity=0.8,
                    hovertext=f"{month}: ${hi:,.0f}",
                    hoverinfo='text'
                ))
            fig.update_layout(
                title="📈 3D Movable Vertical Monthly Sales",
                scene=dict(
                    xaxis=dict(title='Month', tickvals=x_pos+0.25, ticktext=monthly_sales['Month']),
                    yaxis=dict(title=''),
                    zaxis=dict(title='Total Sales ($)'),
                ),
                width=900,
                height=600,
                paper_bgcolor=bg_color,
                font=dict(color=text_color)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    
   # Exploding Pie Chart
    if st.button("📊 Show Top 10 Products Pie Chart", key="exploding_pie"):
        if 'Description' in df.columns and 'TotalSales' in df.columns:
            top_products = df.groupby('Description')['TotalSales'].sum().sort_values(ascending=False).head(10).reset_index()
            pull_values = [0]*len(top_products)
            fig_pie = go.Figure(go.Pie(
                labels=top_products['Description'],
                values=top_products['TotalSales'],
                textinfo='label+percent',
                hoverinfo='label+value',
                pull=pull_values,
                marker=dict(colors=chart_colors)
            ))
            fig_pie.update_layout(title="⭐ Top 10 Products by Revenue", paper_bgcolor=bg_color, font=dict(color=text_color))
            pie_chart = st.plotly_chart(fig_pie, use_container_width=True)
            for i in range(len(top_products)):
                pull_values[i] = 0.2
                fig_pie.data[0].pull = pull_values
                pie_chart.plotly_chart(fig_pie, use_container_width=True)
                time.sleep(0.5)

 
# --- Features Page ---
elif page == "Features":
    st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 1.8rem; border-radius: 12px; color: white; text-align:center;">
    <h1 style="font-size:1.8rem; font-weight:700; margin:0;">🎯 Features & Benefits</h1>
    <p style="font-size:0.95rem; margin:0.5rem 0 0 0;">Why Retail Analytics Pro is essential for your business</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 🌟 Core Features
    - 📊 Interactive Charts with hover & animations
    - 💰 Real-Time KPIs: Revenue, Orders, Avg Order, Top Products
    - 🕵️‍♂️ Filters: Country, Customer, Date Range
    - 🎨 Light & Dark Themes
    - ⚡ Fast Data Processing
    - 📂 Auto-calculate TotalSales & remove cancelled orders
    
    ### 🎯 Benefits
    - 💹 Revenue Insights & Market Analysis
    - 👥 Customer Behavior Tracking
    - 📈 Trend Monitoring & Product Analysis
    - ⚙️ Faster reporting & data export
    """, unsafe_allow_html=True)

# --- About Page ---
elif page == "About":
    st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); padding: 1.8rem; border-radius: 12px; color: white; text-align:center;">
    <h1 style="font-size:1.8rem; font-weight:700; margin:0;">👨‍💻 About Retail Analytics Pro</h1>
    <p style="font-size:0.95rem; margin:0.5rem 0 0 0;">Simplifying retail data analysis for smarter business decisions</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### 📌 Purpose
    Retail Analytics Pro helps businesses track sales, revenue, product performance, and customer behavior in one unified dashboard, enabling data-driven decisions.
    
    ### ❓ Why Retail Analytics is Needed
    - Understand sales trends and revenue growth over time
    - Identify top-performing products & markets
    - Detect opportunities to reduce losses and increase margins
    - Improve marketing and inventory decisions based on customer behavior
    
    ### 🌟 Outcomes & Benefits
    - Faster insights with interactive visualizations
    - Exportable data and reports for stakeholders
    - Custom filters that let you answer specific business questions
    """, unsafe_allow_html=True)

# --- Contact Page ---
elif page == "Contact":
    st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)
        
    st.markdown(r"""
    <h2>📬 Connect With Us</h2>
    <p>We’re here to help. Reach out anytime!</p>
    """, unsafe_allow_html=True)

    
    st.markdown("""
<style>
.contact-grid {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 20px;
}

.info {
    background: #f0f2f6;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    width: 200px;
}

.info span {
    font-size: 30px;
}
</style>

""", unsafe_allow_html=True)

    # -----------------------------
    # ✅ Contact Form
    # -----------------------------
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=120)

        submitted = st.form_submit_button("🚀 Send Message")

        if submitted:
            st.success("✅ Message sent! We’ll get back to you soon.")


st.markdown("""
<div class="footer-small">
    © 2025 Retail Analytics Pro • All Rights Reserved
</div>

<style>
.footer-small {
    text-align: center;
    font-size: 12px;
    color: #aaa;
    padding: 8px;
}
</style>
""", unsafe_allow_html=True)
