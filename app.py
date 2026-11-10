import streamlit as st

# Настройка страницы (для патента: указываем название системы)
st.set_page_config(
    page_title="СППВР: ИТ ЖКТ",
    page_icon="🏥",
    layout="centered"
)

# Инициализация состояния (State Management)
if 'step' not in st.session_state:
    st.session_state.step = 'start'
if 'protocol' not in st.session_state:
    st.session_state.protocol = []

def add_to_protocol(text):
    """Добавляет шаг в историю (для медицинского протокола)"""
    st.session_state.protocol.append(text)

def reset_app():
    """Сброс приложения в начальное состояние"""
    st.session_state.step = 'start'
    st.session_state.protocol = []

def render_protocol():
    """Отрисовка боковой панели с историей решений"""
    with st.sidebar:
        st.header("📋 Протокол врача")
        if not st.session_state.protocol:
            st.info("Опрос только начался...")
        else:
            for i, step in enumerate(st.session_state.protocol, 1):
                st.write(f"**{i}.** {step}")
        
        st.divider()
        st.button("🔄 Начать заново", on_click=reset_app, use_container_width=True)

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🏥 Система поддержки принятия врачебных решений")
st.subheader("Ведение пациентов с инородными телами (ИТ) дистальных отделов ЖКТ")
st.write("---")

render_protocol()

# Логика алгоритма (State Machine)
if st.session_state.step == 'start':
    st.markdown("### Шаг 1. Первичная оценка")
    st.write("Есть ли у пациента клинические признаки перитонита?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Да, есть признаки перитонита", use_container_width=True):
            add_to_protocol("Выявлены клинические признаки перитонита")
            st.session_state.step = 'peritonitis_yes'
            st.rerun()
    with col2:
        if st.button("🟢 Нет, признаков перитонита нет", use_container_width=True):
            add_to_protocol("Признаков перитонита нет")
            st.session_state.step = 'peritonitis_no'
            st.rerun()

elif st.session_state.step == 'peritonitis_yes':
    st.error("⚠️ Сценарий: Клинические признаки перитонита")
    
    st.markdown("""
    **Предоперационная тактика:**
    1. Дообследование.
    2. Предоперационная подготовка.
    3. Оперативное лечение в экстренном порядке.
    
    **Интраоперационная тактика:**
    * Лапаротомия;
    * Ревизия, санация брюшной полости;
    * Колотомия (если ИТ не находится в брюшной полости);
    * Удаление ИТ;
    * Устранение повреждений внутренних органов при необходимости;
    * Колостомия.
    
    **Завершение:** Контрольное эндоскопическое исследование.
    """)
    
    if st.button("Завершить протокол", type="primary"):
        add_to_protocol("Назначена экстренная лапаротомия, удаление ИТ, контрольное эндоскопическое исследование")
        st.success("Протокол сформирован. Извлечение ИТ завершено.")
        st.stop() # Останавливаем дальнейшее выполнение

elif st.session_state.step == 'peritonitis_no':
    st.markdown("### Шаг 2. Дообследование")
    st.write("Оцените инородное тело:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🟢 Потенциально не опасное (нет признаков включения в просвет кишки)", use_container_width=True):
            add_to_protocol("ИТ потенциально не опасное, без включения")
            st.session_state.step = 'safe_fb'
            st.rerun()
    with col2:
        if st.button("🔴 Потенциально опасное (есть признаки включения в просвет кишки)", use_container_width=True):
            add_to_protocol("ИТ потенциально опасное, с признаками включения")
            st.session_state.step = 'dangerous_fb'
            st.rerun()

elif st.session_state.step == 'dangerous_fb':
    st.error("⚠️ Сценарий: Потенциально опасное ИТ")
    
    st.markdown("""
    **Тактика:**
    1. Предоперационная подготовка.
    2. Лапаротомия.
    3. Решение вопроса о необходимости колостомии.
    
    **Завершение:** Колостомия (при необходимости), контрольное эндоскопическое исследование.
    """)
    
    if st.button("Завершить протокол", type="primary"):
        add_to_protocol("Выполнена лапаротомия, решен вопрос о колостомии")
        st.success("Протокол сформирован. Извлечение ИТ завершено.")
        st.stop()

elif st.session_state.step == 'safe_fb':
    st.markdown("### Шаг 3. Малоинвазивное извлечение")
    st.write("Попытка транснального извлечения ИТ с помощью доступных инструментов. Удалось?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Да, удалось извлечь", use_container_width=True):
            add_to_protocol("Успешное транснальное извлечение ИТ")
            st.session_state.step = 'success'
            st.rerun()
    with col2:
        if st.button("❌ Нет, не удалось", use_container_width=True):
            add_to_protocol("Неудачная попытка транснального извлечения")
            st.session_state.step = 'reduction_attempt'
            st.rerun()

elif st.session_state.step == 'reduction_attempt':
    st.markdown("### Шаг 4. Низведение ИТ")
    st.write("Попытка низведения и транснального извлечения ИТ (ректо-, колоноскоп, операционный ректоскоп). Удалось?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Да, удалось извлечь", use_container_width=True):
            add_to_protocol("Успешное низведение и извлечение ИТ")
            st.session_state.step = 'success'
            st.rerun()
    with col2:
        if st.button("❌ Нет, не удалось", use_container_width=True):
            add_to_protocol("Неудачная попытка низведения")
            st.session_state.step = 'surgery_final'
            st.rerun()

elif st.session_state.step == 'surgery_final':
    st.error("⚠️ Сценарий: Хирургическое вмешательство")
    
    st.markdown("""
    **Тактика:**
    * Лапаротомия с попыткой низведения и транснального извлечения ИТ.
    * Колотомия.
    
    **Завершение:** Контрольное эндоскопическое исследование.
    """)
    
    if st.button("Завершить протокол", type="primary"):
        add_to_protocol("Выполнена лапаротомия, колотомия. ИТ извлечено.")
        st.success("Протокол сформирован. Извлечение ИТ завершено.")
        st.stop()

elif st.session_state.step == 'success':
    st.success("✅ УСПЕХ: Инородное тело извлечено.")
    st.info("Назначено: Контрольное эндоскопическое исследование.")
    
    if st.button("Завершить протокол", type="primary"):
        add_to_protocol("Извлечение ИТ завершено. Назначено контрольное эндоскопическое исследование.")
        st.stop()