

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# إعداد الصفحة
st.set_page_config(page_title="Axiom-Zero", layout="wide")

st.title("Axiom-Zero: Sovereign Neural Engine")
st.subheader("Algorithmic Macro-Governance Dashboard")

st.write("Welcome to the foundational neural architecture for future-ready states.")

# تحميل البيانات
try:
    data = pd.read_csv('data.csv')
    
    # تحويل البيانات إلى أرقام للتدريب
    x = np.arange(len(data)).reshape(-1, 1)
    y = data['Economic KPI'].values
    
    # تدريب النموذج
    model = LinearRegression()
    model.fit(x, y)
    
    st.success("Model trained successfully!")
    st.line_chart(data['Economic KPI'])
    
except Exception as e:
    st.error(f"Error: {e}")

st.title("Axiom-Zero: Sovereign Neural Engine")
st.subheader("Algorithmic Macro-Governance Dashboard")

st.write("Welcome to the foundational neural architecture for future-ready states.")
data = pd.read_csv('data.csv')

# --- إضافة خوارزمية التنبؤ ---
from sklearn.linear_model import LinearRegression

# تحويل البيانات إلى أرقام للتدريب
x = np.arange(len(data)).reshape(-1, 1)
y = data['Economic KPI'].values 

# تدريب النموذج
model = LinearRegression()
model.fit(x, y)

# التنبؤ بالنقاط القادمة (لـ 5 خطوات مستقبلية)
future_x = np.arange(len(data), len(data) + 5).reshape(-1, 1)
predictions = model.predict(future_x)

# عرض النتائج
st.subheader("تحليل وتنبؤ Axiom-Zero")
st.line_chart(data) # عرض البيانات الحالية
st.write("توقعات المسار المستقبلي للمؤشر الاقتصادي:")
st.line_chart(predictions) # عرض التنبؤات
