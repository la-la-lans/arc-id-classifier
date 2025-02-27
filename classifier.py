import streamlit as st
import pandas as pd
import io

valid_region_codes = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
valid_gender_codes_old = ['A', 'B', 'C', 'D']
valid_gender_codes_new = ['8', '9']

def string_search_old(arc):
    if pd.notna(arc) and isinstance(arc, str) and len(arc) >= 2:
        if arc[0] in valid_region_codes and arc[1] in valid_gender_codes_old:
            return True
    return False

def string_search_new(arc):
    if pd.notna(arc) and isinstance(arc, str) and len(arc) >= 2:
        if arc[0] in valid_region_codes and arc[1] in valid_gender_codes_new:
            return True
    return False

def area_search_old(arc):
    if pd.notna(arc) and isinstance(arc, str) and len(arc) >= 2:
        if arc[1] in ['A', 'B']:
            return '臺灣地區無戶籍國民、大陸地區人民、港澳居民'
        elif arc[1] in ['C', 'D']:
            return '外籍人士'
    return '中華民國國民身分證'

def area_search_new(arc):
    if pd.notna(arc) and isinstance(arc, str) and len(arc) >= 3:
        if arc[2] == '8':
            return '港澳居民'
        elif arc[2] == '9':
            return '大陸地區人民'
        elif arc[2] == '7':
            return '無戶籍'
        return '外籍人士'  
    return '中華民國國民身分證'

st.title('Taiwan ARC & National ID Classifier')
st.write("""
    **The Alien Resident Certificate (ARC)** serves as a temporary ID card for foreign residents in Taiwan. 
    The ARC number consists of two formats depending on the issuance date:

    - **Old Format**: Issued before January 1st, 2022 (two letters + eight digits, e.g., `AB12345678`).
    - **New Format**: Issued after January 2nd, 2022 (one letter + nine digits, e.g., `A123456789`).
    
    Since ARC numbers have a format similar to Taiwanese IDs, distinguishing between them can be challenging. 
    This tool helps quickly identify whether the holder is a foreign resident or a Taiwanese citizen.

    **Current Version:**
    - Differentiate between Taiwanese national IDs and Alien Resident Certificates (ARC) by analyzing 
    the structure of the ID numbers (old and new format).
    - Classifies the holder’s status (foreign national, Mainland Chinese, Hong Kong/Macau resident).
    - Provides a downloadable version of the results.

""")

uploaded_file = st.file_uploader('Upload an Excel file', type=['xlsx', 'xls'])

st.write('Or enter an ARC/ID number for a quick search:')
arc_input = st.text_input('Enter ARC/ID number (e.g., AB12345678, A123456789)')

if arc_input:

    if string_search_old(arc_input):
        result = area_search_old(arc_input)
        st.write(f'The ARC/ID number {arc_input} is classified as: {result}')
    elif string_search_new(arc_input):
        result = area_search_new(arc_input)
        st.write(f'The ARC/ID number {arc_input} is classified as: {result}')
    else:
        st.write('Invalid ARC/ID number format.')

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, engine='openpyxl')  
        elif uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file, engine='xlrd')  
        else:
            st.error('Unsupported file format. Please upload an .xls or .xlsx file.')

        if '身分證字號' not in df.columns:
            st.error("Error: The uploaded file must contain a column named '身分證字號'.")
        else:
            df['身分證字號'] = df['身分證字號'].astype(str)

            new_df_old = df[df['身分證字號'].apply(string_search_old)]
            new_df_new = df[df['身分證字號'].apply(string_search_new)]

            new_df_old['國際'] = new_df_old['身分證字號'].apply(area_search_old)
            new_df_new['國際'] = new_df_new['身分證字號'].apply(area_search_new)

            new_df = pd.concat([new_df_old, new_df_new])

            st.write('### Filtered Results')
            st.dataframe(new_df)

            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                new_df.to_excel(writer, index=False, sheet_name='Filtered Data')
            excel_file.seek(0)

            st.download_button(
                label='Download Filtered Data',
                data=excel_file,
                file_name='filtered_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
    
    except Exception as e:
        st.error(f"Error reading file: {e}")
