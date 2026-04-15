import streamlit as st
import pandas as pd
import os
import urllib.request
import datetime
import matplotlib.pyplot as plt
import ssl
import io

ssl._create_default_https_context = ssl._create_unverified_context
st.set_page_config(layout="wide", page_title="Лабораторна 5: VHI/VCI/TCI")

dict_obl = {
    1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
    6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
    11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
    16: 'Рівненська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
    21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим'
}

@st.cache_data(show_spinner="Читання даних...")
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "vhi_data")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_year = datetime.datetime.now().year
    df_list = []
    
    for province_id in range(1, 28):
        existing_files = [f for f in os.listdir(output_dir) if f.startswith(f"vhi_id_{province_id}_")]
        if not existing_files:
            url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1=1981&year2={current_year}&type=Mean"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                wp = urllib.request.urlopen(req, timeout=10)
                text = wp.read()
                if b"Request Rejected" not in text:
                    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"vhi_id_{province_id}_{now}.csv"
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(text)
            except Exception:
                pass

    for filename in os.listdir(output_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(output_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                text = text.replace('<tt><pre>', '').replace('</pre></tt>', '').replace('<br>', '')
                
                df = pd.read_csv(io.StringIO(text), skiprows=2, header=None, 
                                 names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
                df.drop(columns=['empty'], inplace=True, errors='ignore')
                df = df.dropna()
                
                df = df[df['Year'].apply(lambda x: str(x).strip().isdigit())]
                df['Year'] = df['Year'].astype(int)
                
                obl_id = int(filename.split('_')[2])
                new_obl_id = obl_id
                if obl_id == 1: new_obl_id = 22
                elif obl_id == 2: new_obl_id = 24
                elif obl_id == 3: new_obl_id = 23
                elif obl_id == 4: new_obl_id = 25
                elif obl_id == 5: new_obl_id = 3
                elif obl_id == 6: new_obl_id = 4
                elif obl_id == 7: new_obl_id = 8
                elif obl_id == 8: new_obl_id = 19
                elif obl_id == 9: new_obl_id = 20
                elif obl_id == 10: new_obl_id = 21
                elif obl_id == 11: new_obl_id = 9
                elif obl_id == 12: new_obl_id = 26 
                elif obl_id == 13: new_obl_id = 10
                elif obl_id == 14: new_obl_id = 11
                elif obl_id == 15: new_obl_id = 12
                elif obl_id == 16: new_obl_id = 13
                elif obl_id == 17: new_obl_id = 14
                elif obl_id == 18: new_obl_id = 15
                elif obl_id == 19: new_obl_id = 16
                elif obl_id == 20: new_obl_id = 27 
                elif obl_id == 21: new_obl_id = 17
                elif obl_id == 22: new_obl_id = 18
                elif obl_id == 23: new_obl_id = 6
                elif obl_id == 24: new_obl_id = 1
                elif obl_id == 25: new_obl_id = 2
                elif obl_id == 26: new_obl_id = 7
                elif obl_id == 27: new_obl_id = 5
                
                df['Province'] = dict_obl.get(new_obl_id, "Невідома область")
                df_list.append(df)
            except Exception:
                pass

    if not df_list:
        return pd.DataFrame()
        
    final_df = pd.concat(df_list, ignore_index=True)
    final_df = final_df[final_df['Province'] != "Невідома область"]
    final_df = final_df[final_df['VHI'] >= 0]
    return final_df

df = load_data()

if df.empty:
    st.error("Помилка: дані не знайдено.")
    st.stop()

def reset_filters():
    st.session_state.indicator = 'VHI'
    st.session_state.province = sorted(df['Province'].unique())[0] 
    st.session_state.week_range = (1, 52)
    st.session_state.year_range = (int(df['Year'].min()), int(df['Year'].max()))
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

if 'indicator' not in st.session_state:
    reset_filters()

st.title("Аналіз вегетаційних індексів (Лабораторна 5)")

col_controls, col_graphs = st.columns([1, 3])

with col_controls:
    st.header("Налаштування")
    indicator = st.selectbox("Показник", ["VCI", "TCI", "VHI"], key='indicator')
    province_list = sorted(df['Province'].unique())
    province = st.selectbox("Область", province_list, key='province')
    week_range = st.slider("Інтервал тижнів", 1, 52, key='week_range')
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.slider("Інтервал років", min_year, max_year, key='year_range')
    st.subheader("Сортування")
    sort_asc = st.checkbox("За зростанням", key='sort_asc')
    sort_desc = st.checkbox("За спаданням", key='sort_desc')
    st.markdown("---")
    st.button("Reset (Скинути фільтри)", on_click=reset_filters, type="primary")

with col_graphs:
    mask = ((df['Province'] == province) & (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]))
    filtered_df = df[mask].copy()
    
    if sort_asc and sort_desc:
        st.warning("Увімкнено одночасно сортування за зростанням та спаданням! Сортування скинуто до стандартного (Рік -> Тиждень).")
        filtered_df = filtered_df.sort_values(by=['Year', 'Week'])
    elif sort_asc:
        filtered_df = filtered_df.sort_values(by=indicator, ascending=True)
    elif sort_desc:
        filtered_df = filtered_df.sort_values(by=indicator, ascending=False)
    else:
        filtered_df = filtered_df.sort_values(by=['Year', 'Week'])

    tab1, tab2, tab3 = st.tabs(["📊 Таблиця даних", "📈 Графік показника", "🌍 Порівняння областей"])
    
    with tab1:
        st.subheader(f"Відфільтровані дані для області: {province}")
        st.dataframe(filtered_df[['Year', 'Week', 'Province', indicator]], use_container_width=True)
        
    with tab2:
        st.subheader(f"Динаміка {indicator} ({year_range[0]}-{year_range[1]})")
        yearly_data = filtered_df.groupby('Year')[indicator].mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(yearly_data['Year'], yearly_data[indicator], marker='o', color='#2ca02c', linewidth=2)
        ax.set_xlabel('Рік')
        ax.set_ylabel(f'Середній {indicator}')
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
        
    with tab3:
        st.subheader(f"Порівняння {indicator}: {province} та інші області")
        mask_all = ((df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]))
        df_all_filtered = df[mask_all]
        comparison_data = df_all_filtered.groupby(['Year', 'Province'])[indicator].mean().unstack()
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        for col in comparison_data.columns:
            if col == province:
                ax2.plot(comparison_data.index, comparison_data[col], lw=3, label=f'{col} (Вибрана)', zorder=5)
            else:
                ax2.plot(comparison_data.index, comparison_data[col], lw=1, alpha=0.4, label=col)
        ax2.set_xlabel('Рік')
        ax2.set_ylabel(f'Середній {indicator}')
        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small', ncol=2)
        ax2.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig2)