# IMPORT LIBRARIES
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import plotly.colors as pc
import numpy as np

# KONFIGURASI DASBOR
st.set_page_config(
    page_title="Automobile Sales Dashboard",
    page_icon=":car:",
    layout="wide"
)

# TEMA WARNA DASBOR + SIDEBAR
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 50%, #ddd6fe 100%);
        color: #4c1d95;
    }

    .stButton>button {
        background: white;
        color: black;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
        border: none;
        box-shadow: 0 4px 6px rgba(139, 92, 246, 0.3);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: #b292d6;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(139, 92, 246, 0.4);
    }

    .stDataFrame {
        background-color: rgba(255, 255, 255, 0.9);
        color: #4c1d95;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(139, 92, 246, 0.1);
        backdrop-filter: blur(10px);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #4c1d95;
        text-shadow: 0 2px 4px rgba(139, 92, 246, 0.1);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e9d5ff 0%, #ddd6fe 100%);
        border-right: 2px solid rgba(139, 92, 246, 0.2);
    }

    .css-1cpxqw2, .css-1d391kg, .css-1v0mbdj, .css-10trblm {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #4c1d95 !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px);
    }

    .css-1p05b0s {
        color: #4c1d95 !important;
        font-weight: 600;
    }

    label {
        color: #4c1d95 !important;
        font-weight: 600;
    }

    .metric-box {
        background-color: #f0f2f6;
        padding: 15px 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        margin-top: 10px;
    }

    .metric-box:hover {
        background-color: #b292d6; 
        box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
    }

    .metric-item {
        margin-bottom: 20px;
    }

    .metric-box h2 {
        color: #0d6efd;
        margin: 5px 0 0 0;
    }

    .metric-box h4 {
        color: #333;
        margin: 0 0 5px 0;
    }

    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 10px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        border: 2px solid rgba(139, 92, 246, 0.3);
        color: #4c1d95;
        font-weight: 600;
        width: auto;
        min-width: 0;
        padding: 8px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: #b292d6;
        color: white;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #4c1d95;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# IMPORT DATA
data = pd.read_csv(r"C:/Users/user/Documents/Statistika 101!/Semester 6/Pengantar Python/Kelompok 4_TBP Python/Auto Sales Data.csv")
data["ORDERDATE"] = pd.to_datetime(data["ORDERDATE"], dayfirst=True)
data["YEAR"] = data["ORDERDATE"].dt.year

# Judul
st.title(":car: Automobile Sales Dashboard")

# Inisialisasi session_state jika belum ada
if 'show_credit' not in st.session_state:
    st.session_state.show_credit = False

if st.button("Click here for credit information"):
    st.session_state.show_credit = not st.session_state.show_credit

if st.session_state.show_credit:
    st.markdown("### Made by: Group 4")
    st.markdown("""
    1. **Hana Widya Syahara**      (M0722041)  
    2. **Lhyanisa Aghina Putri**   (M0722046)  
    3. **Salsa Dhea Anella**       (M0722070)  
    """)
    st.markdown("*Data Source:* Automobile Sales Dataset (https://www.kaggle.com/datasets/ddosad/auto-sales-data)")

# SIDEBAR FILTER
st.sidebar.header("Select filter here:")

# Quick Action Buttons
st.sidebar.markdown("*Quick Actions:*")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🔄 Select All", key="select_all"):
        st.session_state.select_all_filters = True
with col2:
    if st.button("❌ Clear All Filters", key="clear_all"):
        st.session_state.clear_all_filters = True

st.sidebar.markdown("---")

# Initialize session state untuk filter defaults
if 'select_all_filters' not in st.session_state:
    st.session_state.select_all_filters = False
if 'clear_all_filters' not in st.session_state:
    st.session_state.clear_all_filters = False

# Set default values berdasarkan button actions
if st.session_state.select_all_filters:
    default_productline = list(data["PRODUCTLINE"].unique())
    default_dealsize = list(data["DEALSIZE"].unique())
    default_year = list(data["YEAR"].unique())
    default_country = list(data["COUNTRY"].unique())
    st.session_state.select_all_filters = False  # Reset flag
elif st.session_state.clear_all_filters:
    default_productline = []
    default_dealsize = []
    default_year = []
    default_country = []
    st.session_state.clear_all_filters = False  # Reset flag
else:
    default_productline = list(data["PRODUCTLINE"].unique())
    default_dealsize = list(data["DEALSIZE"].unique())
    default_year = list(data["YEAR"].unique())
    default_country = list(data["COUNTRY"].unique())

# Filter dengan searchable multiselect
category_sb = st.sidebar.multiselect(
    "🔍 Search & Select Product Line:",
    options=["📋 Select All"] + sorted(data["PRODUCTLINE"].unique()),
    default=default_productline,
    help="Type to search for specific product lines or click 'Select All'"
)

segment_sb = st.sidebar.multiselect(
    "🔍 Search & Select Deal Size:",
    options=["📋 Select All"] + sorted(data["DEALSIZE"].unique()),
    default=default_dealsize,
    help="Type to search for specific deal sizes or click 'Select All'"
)

year_sb = st.sidebar.multiselect(
    "🔍 Search & Select Year:",
    options=["📋 Select All"] + sorted(data["YEAR"].unique()),
    default=default_year,
    help="Type to search for specific years or click 'Select All'"
)

country_sb = st.sidebar.multiselect(
    "🔍 Search & Select Country:",
    options=["📋 Select All"] + sorted(data["COUNTRY"].unique()),
    default=default_country,
    help="Type to search for specific countries or click 'Select All'"
)

# FILTER DATA - Handle "Select All" option
def process_filter_selection(selected_items, all_unique_values):
    """Process filter selection, handling 'Select All' option"""
    if "📋 Select All" in selected_items:
        return list(all_unique_values)
    else:
        return [item for item in selected_items if item != "📋 Select All"]

# Process each filter
category_filter = process_filter_selection(category_sb, data["PRODUCTLINE"].unique())
segment_filter = process_filter_selection(segment_sb, data["DEALSIZE"].unique())
year_filter = process_filter_selection(year_sb, data["YEAR"].unique())
country_filter = process_filter_selection(country_sb, data["COUNTRY"].unique())

# Apply filters - if empty, show no data
if not category_filter:
    category_filter = []
if not segment_filter:
    segment_filter = []
if not year_filter:
    year_filter = []
if not country_filter:
    country_filter = []

data_selection = data[
    (data['PRODUCTLINE'].isin(category_filter) if category_filter else False) &
    (data['DEALSIZE'].isin(segment_filter) if segment_filter else False) &
    (data['YEAR'].isin(year_filter) if year_filter else False) &
    (data['COUNTRY'].isin(country_filter) if country_filter else False)
]

# Jika semua filter kosong, tampilkan pesan
if data_selection.empty and (not category_filter or not segment_filter or not year_filter or not country_filter):
    st.warning("⚠️ No data to display. Please select at least one option from each filter or use 'Select All' button.")

# KPI UTAMA
total_sales = int(data_selection["SALES"].sum())
average_quantity = round(data_selection["QUANTITYORDERED"].mean())
average_sales = round(data_selection["SALES"].mean(), 2)

# KPI KARTU UTAMA
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown(f'<div class="metric-box"><h3>Total Sales:</h3><h2>US$ {total_sales:,}</h2></div>', unsafe_allow_html=True)
with middle_column:
    st.markdown(f'<div class="metric-box"><h3>Average Quantity Sold:</h3><h2>{average_quantity} Units</h2></div>', unsafe_allow_html=True)
with right_column:
    st.markdown(f'<div class="metric-box"><h3>Average Sales:</h3><h2>US$ {average_sales:,}</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# MAIN TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Statistics", 
    "📋 Data Table", 
    "📦 Sales Distribution", 
    "📈 Time Series", 
    "🌍 Geographic Analysis", 
    "🍩 Deal Size Analysis", 
    "🚘 Product Analysis"
])

# TAB 1: STATISTIK DESKRIPTIF
with tab1:
    st.subheader("📊 Statistic Descriptive Analysis")
    
    # Hitung statistik deskriptif
    sales_stats = data_selection["SALES"].describe()
    sales_max = data_selection["SALES"].max()
    sales_min = data_selection["SALES"].min()
    sales_std = data_selection["SALES"].std()
    sales_var = data_selection["SALES"].var()
    sales_cv = (sales_std / data_selection["SALES"].mean()) * 100 if data_selection["SALES"].mean() != 0 else 0
    sales_range = sales_max - sales_min
    sales_iqr = sales_stats['75%'] - sales_stats['25%']

    # Z-score untuk identifikasi outlier
    z_scores = np.abs((data_selection["SALES"] - data_selection["SALES"].mean()) / sales_std)
    outliers_count = len(z_scores[z_scores > 2])

    # Tampilkan KPI statistik dalam 4 kolom
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("### Top and Bottom Sales")
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-item">
                <h4>📈 Highest Sales</h4>
                <h2>US$ {sales_max:,.0f}</h2>
            </div>
            <div class="metric-item">
                <h4>📉 Lowest Sales</h4>
                <h2>US$ {sales_min:,.0f}</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown("### Sales Variability")
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-item">
                <h4>🎯 Std. Deviation</h4>
                <h2>US$ {sales_std:,.0f}</h2>
            </div>
            <div class="metric-item">
                <h4>📐 Variance</h4>
                <h2>{sales_var:,.0f}</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown("### Range & Spread")
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-item">
                <h4>➖ Range</h4>
                <h2>US$ {sales_range:,.0f}</h2>
            </div>
            <div class="metric-item">
                <h4>📏 IQR</h4>
                <h2>US$ {sales_iqr:,.0f}</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown("### Variation & Outliers")
        st.markdown(f'''
        <div class="metric-box">
            <div class="metric-item">
                <h4>📎 Coeff. of Variation</h4>
                <h2>{sales_cv:.1f}%</h2>
            </div>
            <div class="metric-item">
                <h4>🚨 Outliers (Z > 2)</h4>
                <h2>{outliers_count} Transactions</h2>
            </div>
        </div>
        ''', unsafe_allow_html=True)

    # TRANSACTION COUNTS BY STATUS
    st.markdown("---")
    st.subheader("⏳ Transaction Counts by Status")

    # Hitung dan urutkan status
    count_by_status = (
        data_selection["STATUS"]
        .value_counts()
        .sort_values(ascending=True)
        .reset_index()
    )
    count_by_status.columns = ["STATUS", "COUNT"]

    # Buat 3 kolom
    left_column, middle_column, right_column = st.columns(3)
    cols = [left_column, middle_column, right_column]

    # Loop tiap status, isi kolom bergantian
    for i, row in count_by_status.iterrows():
        with cols[i % 3]:
            st.markdown(
                f'<div class="metric-box"><h3>{row["STATUS"]}</h3><h2>{row["COUNT"]:,}</h2></div>',
                unsafe_allow_html=True,
            )

# TAB 2: DATA TABEL
with tab2:
    st.subheader("📋 Filtered Data")
    st.dataframe(data_selection)

# TAB 3: BOXPLOT DISTRIBUTION
with tab3:
    st.subheader("📦 Sales Distribution Analysis by BoxPlot")

    # Create subtabs for different boxplot views
    subtab1, subtab2, subtab3 = st.tabs(["By Deal Size", "By Product Line", "By Year"])

    with subtab1:
        # Boxplot berdasarkan Deal Size
        fig_box1 = px.box(
            data_selection,
            x="DEALSIZE",
            y="SALES",
            title="<b>Sales Distribution by Deal Size</b>",
            color="DEALSIZE",
            color_discrete_sequence=px.colors.qualitative.Set3,
            template="plotly_white"
        )
        fig_box1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="<b>Deal Size</b>",
            yaxis_title="<b>Sales (US$)</b>",
            showlegend=False
        )
        st.plotly_chart(fig_box1, use_container_width=True)

    with subtab2:
        # Boxplot berdasarkan Product Line
        fig_box2 = px.box(
            data_selection,
            x="PRODUCTLINE",
            y="SALES",
            title="<b>Sales Distribution by Product Line</b>",
            color="PRODUCTLINE",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_white"
        )
        fig_box2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="<b>Product Line</b>",
            yaxis_title="<b>Sales (US$)</b>",
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_box2, use_container_width=True)

    with subtab3:
        # Boxplot berdasarkan Year
        fig_box3 = px.box(
            data_selection,
            x="YEAR",
            y="SALES",
            title="<b>Sales Distribution by Year</b>",
            color="YEAR",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template="plotly_white"
        )
        fig_box3.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="<b>Year</b>",
            yaxis_title="<b>Sales (US$)</b>",
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_box3, use_container_width=True)

# TAB 4: TIME SERIES
with tab4:
    st.subheader("📆 Sales Over Time")

    data_selection["MONTH"] = data_selection["ORDERDATE"].dt.to_period("M").dt.to_timestamp()
    sales_per_month = data_selection.groupby("MONTH").sum(numeric_only=True)[["SALES"]].reset_index()
    fig = px.line(
        sales_per_month,
        x="MONTH",
        y="SALES",
        color_discrete_sequence=["#b0b0b0"],
        template="plotly_white"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="<b>Order Date</b>",
        yaxis_title="<b>Sales</b>",
        legend_title="<b>Legend</b>"
    )
    st.plotly_chart(fig, use_container_width=True)

# TAB 5: GEOGRAPHIC ANALYSIS
with tab5:
    st.subheader("🌍 Geographic Analysis")
    
    # TOP 10 COUNTRY DISTRIBUTION
    st.markdown("### Top 10 Country Distribution")

    # Hitung jumlah transaksi per negara dan ambil top 10
    country_counts = data_selection['COUNTRY'].value_counts().head(10).reset_index()
    country_counts.columns = ['Country', 'Count']

    # Buat horizontal bar chart dengan gradasi warna biru
    fig_country = go.Figure()

    # Buat gradasi warna dari ungu tua ke ungu muda
    colors = ['#4c1d95', '#5b21b6', '#6d28d9', '#7c3aed', '#8b5cf6',
              '#a855f7', '#c084fc', '#d8b4fe', '#e9d5ff', '#ede9fe']

    fig_country.add_trace(go.Bar(
        y=country_counts['Country'],
        x=country_counts['Count'],
        orientation='h',
        marker_color=colors[:len(country_counts)],
        text=country_counts['Count'],
        textposition='outside',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{y}</b><br>Transactions: %{x}<extra></extra>'
    ))

    fig_country.update_layout(
        xaxis_title="<b>Number of Transactions</b>",
        yaxis_title="<b>Country</b>",
        template="plotly_white",
        height=500,
        margin=dict(l=100, r=50, t=50, b=50),
        yaxis=dict(
            categoryorder='total ascending',
            gridcolor='rgba(139, 92, 246, 0.1)'
        ),
        xaxis=dict(
            gridcolor='rgba(139, 92, 246, 0.1)'
        )
    )

    st.plotly_chart(fig_country, use_container_width=True)

    # Summary statistics untuk Top 10 Countries
    st.markdown("*📋 Top 10 Countries Summary:*")
    top_countries_summary = data_selection[data_selection['COUNTRY'].isin(country_counts['Country'])].groupby('COUNTRY').agg({
        'SALES': ['sum', 'mean'],
        'QUANTITYORDERED': 'sum',
        'COUNTRY': 'count'
    }).round(2)

    # Flatten column names
    top_countries_summary.columns = ['Total Sales', 'Avg Sales per Transaction', 'Total Quantity', 'Transaction Count']
    top_countries_summary = top_countries_summary.reset_index()
    top_countries_summary = top_countries_summary.sort_values('Transaction Count', ascending=False)

    # Format currency columns
    top_countries_summary['Total Sales'] = top_countries_summary['Total Sales'].apply(lambda x: f"${x:,.0f}")
    top_countries_summary['Avg Sales per Transaction'] = top_countries_summary['Avg Sales per Transaction'].apply(lambda x: f"${x:,.0f}")

    st.dataframe(top_countries_summary, use_container_width=True)

    # GRAFIK BAR: SALES PER NEGARA
    st.markdown("---")
    st.markdown("### Sales by Country")
                 
    sales_per_country = data_selection.groupby("COUNTRY").sum(numeric_only=True)[["SALES"]].sort_values(by="SALES", ascending=False).reset_index()
    num_bars = len(sales_per_country)
    purple_colors = pc.sample_colorscale("Purples", [1 - i / (num_bars - 1) for i in range(num_bars)])
    sales_per_country['color'] = purple_colors
    color_map = dict(zip(sales_per_country['COUNTRY'], sales_per_country['color']))

    fig = px.bar(
        sales_per_country,
        x="COUNTRY",
        y="SALES",
        color="COUNTRY",  
        color_discrete_map=color_map,  
        template="plotly_white"
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="<b>Country</b>",
        yaxis_title="<b>Sales</b>",
        legend_title="<b>Legend</b>"
    )

    st.plotly_chart(fig, use_container_width=True)

# TAB 6: DEAL SIZE ANALYSIS
with tab6:
    st.subheader("🍩 Deal Size Analysis")

    # Buat mapping warna untuk konsistensi
    deal_size_colors = {
        'Small': '#EF553B',   
        'Medium': '#10B981',  
        'Large': '#3B82F6'    
    }

    # Create two columns for donut charts
    col_donut1, col_donut2 = st.columns(2)
    with col_donut1:
        # Donut chart berdasarkan Deal Size (Count)
        deal_size_count = data_selection['DEALSIZE'].value_counts().reset_index()
        deal_size_count.columns = ['Deal Size', 'Count']

        fig_donut1 = px.pie(
            deal_size_count,
            values='Count',
            names='Deal Size',
            title="<b>Transaction Count by Deal Size</b>",
            color='Deal Size',
            color_discrete_map=deal_size_colors,
            template="plotly_white",
            hole=0.4
        )
        fig_donut1.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='white', width=2))
        )
        fig_donut1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            annotations=[dict(text='Transactions', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        st.plotly_chart(fig_donut1, use_container_width=True)

    with col_donut2:
        # Donut chart berdasarkan Deal Size (Sales Value)
        deal_size_sales = data_selection.groupby('DEALSIZE')['SALES'].sum().reset_index()
        deal_size_sales.columns = ['Deal Size', 'Total Sales']

        fig_donut2 = px.pie(
            deal_size_sales,
            values='Total Sales',
            names='Deal Size',
            title="<b>Sales Value by Deal Size</b>",
            color='Deal Size',
            color_discrete_map=deal_size_colors,
            template="plotly_white",
            hole=0.4
        )
        fig_donut2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='white', width=2))
        )
        fig_donut2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            annotations=[dict(text='Sales Value', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        st.plotly_chart(fig_donut2, use_container_width=True)

    # Summary statistics untuk Deal Size
    st.markdown("*📋 Deal Size Summary:*")
    deal_summary = data_selection.groupby('DEALSIZE').agg({
        'SALES': ['sum', 'mean', 'count'],
        'QUANTITYORDERED': 'mean'
    }).round(2)

    # Flatten column names
    deal_summary.columns = ['Total Sales', 'Avg Sales', 'Transaction Count', 'Avg Quantity']
    deal_summary = deal_summary.reset_index()

    # Format currency columns
    deal_summary['Total Sales'] = deal_summary['Total Sales'].apply(lambda x: f"${x:,.0f}")
    deal_summary['Avg Sales'] = deal_summary['Avg Sales'].apply(lambda x: f"${x:,.0f}")

    st.dataframe(deal_summary, use_container_width=True)

# TAB 7: PRODUCT ANALYSIS
with tab7:
    st.subheader("🚘 Sales by Product Line")

    sales_per_productline = data_selection.groupby("PRODUCTLINE").sum(numeric_only=True)[["SALES"]].sort_values(by="SALES", ascending=False).reset_index()

    # Daftar warna berbeda untuk tiap Product Line
    custom_colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880']

    fig = px.bar(
        sales_per_productline,
        x="PRODUCTLINE",
        y="SALES",
        color="PRODUCTLINE",  # <- Beda warna tiap jenis
        color_discrete_sequence=custom_colors,
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title="<b>Product Line</b>",
        yaxis_title="<b>Sales</b>",
        legend_title="<b>Product Line</b>",  # <- Disesuaikan dengan kategori warna
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)