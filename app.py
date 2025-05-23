import streamlit as st
import pandas as pd
from sku_mapper import SKUMapper
from db import get_engine, save_dataframe


enable_db = True

st.set_page_config(layout="wide", page_title="SKU Mapper Dashboard")

st.title("SKU→MSKU Mapping & Sales Dashboard")

st.sidebar.header("Data Upload")
map_file = st.sidebar.file_uploader("Upload Master Mapping (CSV/XLSX)", type=["csv","xlsx"])
sales_file = st.sidebar.file_uploader("Upload Sales Data (CSV/XLSX)", type=["csv","xlsx"])

if map_file:
    if map_file.name.endswith('.xlsx'):
        map_df = pd.read_excel(map_file)
    else:
        map_df = pd.read_csv(map_file)
    st.sidebar.success("Mapping loaded: %d SKUs" % len(map_df))

if sales_file:
    if sales_file.name.endswith('.xlsx'):
        sales_df = pd.read_excel(sales_file)
    else:
        sales_df = pd.read_csv(sales_file)
    st.sidebar.success("Sales data loaded: %d rows" % len(sales_df))

if st.sidebar.button("Process & Visualize"):
    if not map_file or not sales_file:
        st.error("Please upload both mapping and sales files.")
    else:
        mapper = SKUMapper(map_df)
        sales_df['SKU_clean'] = sales_df['SKU'].astype(str).str.strip().str.upper()
        sales_df['MSKU'] = sales_df['SKU_clean'].apply(mapper.map_sku)

        engine = get_engine()
        save_dataframe(map_df, 'sku_mapping', engine)
        save_dataframe(sales_df, 'sales', engine)

        st.subheader("Sample of Mapped Sales")
        st.dataframe(sales_df.head())

        st.subheader("Sales by MSKU")
        summary = sales_df.groupby('MSKU')['Quantity'].sum().reset_index()
        summary = summary.sort_values('Quantity', ascending=False)
        st.bar_chart(summary.set_index('MSKU'))

        st.subheader("Top SKUs Missing Mapping")
        missing = sales_df[sales_df.MSKU.isna()]['SKU_clean'].value_counts().reset_index()
        missing.columns = ['SKU','Count']
        st.table(missing.head(10))
