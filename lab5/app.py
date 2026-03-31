import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Налаштування сторінки
st.set_page_config(layout="wide", page_title="Лабораторна 5: Наука про дані: обмін результатами та початковий аналіз")

# Імітація даних з 2-ї лабораторної роботи для швидкого старту програми
@st.cache_data
def load_data():
    np.random.seed(42)
    provinces = ['Київська', 'Вінницька', 'Одеська', 'Львівська', 'Харківська', 'Дніпропетровська']
    years = list(range(2000, 2024))
    weeks = list(range(1, 53))
    
    data = []
    for p in provinces:
        for y in years:
            for w in weeks:
                data.append([p, y, w])
    df = pd.DataFrame(data, columns=['Province', 'Year', 'Week'])
    df['VCI'] = np.random.uniform(10, 100, len(df))
    df['TCI'] = np.random.uniform(10, 100, len(df))
    df['VHI'] = df['VCI'] * 0.5 + df['TCI'] * 0.5
    return df

df = load_data()

# ---------------------------------------------------------
# Вимога: створіть button для скидання всіх фільтрів і повернення до початкового стану
# ---------------------------------------------------------
def reset_filters():
    st.session_state.indicator = 'VHI'
    st.session_state.province = 'Київська'
    st.session_state.week_range = (1, 52)
    st.session_state.year_range = (2000, 2023)
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

# Ініціалізація початкових значень (щоб програма знала, з чого починати)
if 'indicator' not in st.session_state:
    reset_filters()

st.title("Лабораторна робота №5" + "\n" + "Наука про дані: обмін результатами та початковий аналіз")

# ---------------------------------------------------------
# Вимога: інтерактивні елементи мають бути розміщені в одній колонці, а графіки з таблицею — в іншій.
# ---------------------------------------------------------
col_controls, col_graphs = st.columns([1, 3])

with col_controls:
    st.header("Налаштування")
    
    # Вимога: створіть dropdown список, який дозволяє вибрати часовий ряд VCI, TCI, VHI
    indicator = st.selectbox("Показник", ["VCI", "TCI", "VHI"], key='indicator')
    
    # Вимога: створіть dropdown список, який дозволяє вибрати область
    province = st.selectbox("Область", df['Province'].unique(), key='province')
    
    # Вимога: створіть slider, який дозволяє вибирати інтервал тижнів
    week_range = st.slider("Інтервал тижнів", 1, 52, key='week_range')
    
    # Вимога: створіть slider, який дозволяє вибрати інтервал років
    year_range = st.slider("Інтервал років", 2000, 2023, key='year_range')
    
    # Вимога: створіть два checkbox для сортування даних за зростанням та спаданням
    st.subheader("Сортування")
    sort_asc = st.checkbox("За зростанням", key='sort_asc')
    sort_desc = st.checkbox("За спаданням", key='sort_desc')
    
    st.markdown("---")
    # Та сама кнопка Reset, про яку йшла мова вище
    st.button("Reset (Скинути фільтри)", on_click=reset_filters, type="primary")

with col_graphs:
    # Фільтруємо дані на основі повзунків і випадаючих списків
    mask = (
        (df['Province'] == province) &
        (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) &
        (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
    )
    filtered_df = df[mask].copy()
    
    # ---------------------------------------------------------
    # Вимога: продумайте реакцію програми, якщо увімкнені обидва чекбокси.
    # ---------------------------------------------------------
    if sort_asc and sort_desc:
        st.warning("Увімкнено одночасно сортування за зростанням та спаданням! Сортування скинуто до стандартного хронологічного (Рік -> Тиждень).")
        filtered_df = filtered_df.sort_values(by=['Year', 'Week'])
    elif sort_asc:
        filtered_df = filtered_df.sort_values(by=indicator, ascending=True)
    elif sort_desc:
        filtered_df = filtered_df.sort_values(by=indicator, ascending=False)
    else:
        filtered_df = filtered_df.sort_values(by=['Year', 'Week'])

    # ---------------------------------------------------------
    # Вимога: створіть три вкладки для відображення таблиці, графіка та графіка порівняння.
    # ---------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["Таблиця даних", "Графік показника", "Порівняння областей"])
    
    with tab1:
        st.subheader(f"Відфільтровані дані для області: {province}")
        # Виводимо таблицю
        st.dataframe(filtered_df[['Year', 'Week', 'Province', indicator]], use_container_width=True)
        
    with tab2:
        # Вимога: перший графік повинен відображати відфільтровані дані (часові ряди)
        st.subheader(f"Динаміка {indicator} ({year_range[0]}-{year_range[1]})")
        
        # Для красивого лінійного графіка рахуємо середнє значення показника за обрані тижні у кожному році
        yearly_data = filtered_df.groupby('Year')[indicator].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(yearly_data['Year'], yearly_data[indicator], marker='o', color='#2ca02c', linewidth=2)
        ax.set_xlabel('Рік')
        ax.set_ylabel(f'Середній {indicator}')
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)
        
    with tab3:
        # Вимога: другий графік має відображати порівняння значень для обраної області з усіма іншими
        st.subheader(f"Порівняння {indicator}: {province} та інші області")
        
        # Відбираємо дані для ВСІХ областей, але застосовуємо фільтри років і тижнів
        mask_all = (
            (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1]) &
            (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])
        )
        df_all_filtered = df[mask_all]
        
        # Рахуємо середнє по кожній області
        comparison_data = df_all_filtered.groupby(['Year', 'Province'])[indicator].mean().unstack()
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        for col in comparison_data.columns:
            if col == province:
                # Обрану область виділяємо товстою лінією
                ax2.plot(comparison_data.index, comparison_data[col], lw=3, label=f'{col} (Вибрана)', zorder=5)
            else:
                # Інші області малюємо тонкими напівпрозорими лініями
                ax2.plot(comparison_data.index, comparison_data[col], lw=1, alpha=0.4, label=col)
        
        ax2.set_xlabel('Рік')
        ax2.set_ylabel(f'Середній {indicator}')
        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax2.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig2)