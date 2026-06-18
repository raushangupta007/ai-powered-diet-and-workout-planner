import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Diet & Workout Planner",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium UI Look
st.markdown("""
<style>
    .main-title { font-size: 40px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    .subtitle { font-size: 18px; color: #6B7280; text-align: center; margin-bottom: 30px; }
    .metric-box { background-color: #F3F4F6; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .metric-val { font-size: 24px; font-weight: bold; color: #10B981; }
    .section-header { font-size: 22px; font-weight: 700; color: #1F2937; border-left: 5px solid #3B82F6; padding-left: 10px; margin-top: 25px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# Load datasets safely without any inline heavy transformation inside cache
@st.cache_data
def load_data():
    try:
        gym = pd.read_csv('megaGymDataset.csv')
        nut = pd.read_csv('nutrients_csvfile.csv')
        return gym, nut
    except Exception as e:
        st.error(f"Error loading CSV files: {e}")
        return None, None

gym_df_raw, nut_df_raw = load_data()

# Process Data outside the cache function safely
if nut_df_raw is not None:
    nut_df = nut_df_raw.copy()
    for col in ['Calories', 'Protein', 'Fat', 'Sat.Fat', 'Fiber', 'Carbs']:
        if col in nut_df.columns:
            nut_df[col] = nut_df[col].astype(str).str.replace(',', '').str.replace('t', '0').str.strip()
            nut_df[col] = pd.to_numeric(nut_df[col], errors='coerce').fillna(0)
else:
    nut_df = None

if gym_df_raw is not None:
    gym_df = gym_df_raw.copy()
    if 'Rating' in gym_df.columns:
        gym_df['Rating'] = pd.to_numeric(gym_df['Rating'], errors='coerce').fillna(0)
    if 'Level' in gym_df.columns:
        gym_df['Level'] = gym_df['Level'].str.capitalize()
else:
    gym_df = None

# ================= SIDEBAR INPUT SECTION =================
st.sidebar.header("👤 User Profile & Goals")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 15, 80, 25)
weight = st.sidebar.number_input("Weight (kg)", min_value=30, max_value=200, value=75)
height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=175)

activity_mapping = {
    "Sedentary (Little or no exercise)": 1.2,
    "Lightly Active (Exercise 1-3 days/week)": 1.375,
    "Moderately Active (Exercise 3-5 days/week)": 1.55,
    "Very Active (Exercise 6-7 days/week)": 1.725
}
activity_choice = st.sidebar.selectbox("Activity Level", list(activity_mapping.keys()))
activity_level = activity_mapping[activity_choice]

goal = st.sidebar.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance"])
goal_map = {"Weight Loss": "loss", "Muscle Gain": "gain", "Maintenance": "maintain"}

st.sidebar.header("🏋️‍♂️ Workout Preferences")
user_level = st.sidebar.selectbox("Your Fitness Level", ["Beginner", "Intermediate", "Expert"])

if gym_df is not None:
    available_body_parts = sorted(gym_df['BodyPart'].dropna().unique().tolist())
else:
    available_body_parts = ["Chest", "Abdominals", "Biceps", "Triceps", "Lats"]
    
target_muscles = st.sidebar.multiselect("Target Body Parts", available_body_parts, default=["Chest", "Abdominals"])

# ================= CORE LOGIC FUNCTIONS =================
def calculate_macros(weight_kg, height_cm, age, gender, activity_level, goal_str):
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    tdee = bmr * activity_level
    
    if goal_str == 'loss':
        target_calories = tdee - 500
        p_ratio, f_ratio, c_ratio = 0.30, 0.25, 0.45
    elif goal_str == 'gain':
        target_calories = tdee + 400
        p_ratio, f_ratio, c_ratio = 0.25, 0.25, 0.50
    else:
        target_calories = tdee
        p_ratio, f_ratio, c_ratio = 0.25, 0.30, 0.45
        
    return (round(target_calories), 
            round((target_calories * p_ratio) / 4), 
            round((target_calories * f_ratio) / 9), 
            round((target_calories * c_ratio) / 4))

# ================= MAIN UI CONTENT AREA =================
st.markdown("<div class='main-title'>🏋️‍♂️ AI-Powered Diet & Workout Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your personalized AI Coach for automated diet planning and custom gym routines</div>", unsafe_allow_html=True)

if st.button("🚀 Generate My Custom Plan", type="primary", use_container_width=True):
    calories, protein, fat, carbs = calculate_macros(weight, height, age, gender, activity_level, goal_map[goal])
    
    # 1. Target Metrics Dashboard Cards
    st.markdown("<div class='section-header'>📊 Your Daily Target Requirements</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'>🔥 <b>Calories</b><br><span class='metric-val'>{calories} kcal</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'>🍗 <b>Protein</b><br><span class='metric-val'>{protein}g</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'>🥑 <b>Fats</b><br><span class='metric-val'>{fat}g</span></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'>🍞 <b>Carbs</b><br><span class='metric-val'>{carbs}g</span></div>", unsafe_allow_html=True)
        
    # 2. Food / Diet Section
    st.markdown("<div class='section-header'>🥗 AI Recommended Food Items</div>", unsafe_allow_html=True)
    if nut_df is not None and not nut_df.empty:
        df_nut = nut_df.copy()
        
        # Calculate Density safely on global dataframe scope
        df_nut['Protein_Density'] = df_nut['Protein'] / (df_nut['Calories'] + 1)
        recommended_diet = df_nut.sort_values(by='Protein_Density', ascending=False).head(8)
        
        st.dataframe(
            recommended_diet[['Food', 'Measure', 'Calories', 'Protein', 'Carbs', 'Fat', 'Category']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nutrients dataset not found or failed to load.")
        
    # 3. Workout Routine Section
    st.markdown("<div class='section-header'>💪 Custom Workout Schedule</div>", unsafe_allow_html=True)
    if gym_df is not None and len(target_muscles) > 0:
        filtered_gym = gym_df[gym_df['Level'].str.lower() == user_level.lower()]
        
        for muscle in target_muscles:
            st.subheader(f"🎯 Target Muscle: {muscle}")
            part_exercises = filtered_gym[filtered_gym['BodyPart'].str.lower() == muscle.lower()]
            top_exercises = part_exercises.sort_values(by='Rating', ascending=False).head(3)
            
            if not top_exercises.empty:
                st.table(top_exercises[['Title', 'Type', 'Equipment', 'Rating']].rename(columns={'Title': 'Exercise Name'}))
            else:
                st.caption("No highly-rated exercises found for this specific combination. Try modifying filters.")
    else:
        st.info("Please select at least one Target Body Part from the sidebar to view workout plan.")
else:
    st.info("👈 Sahi info sidebar me select karo aur 'Generate My Custom Plan' par click karo apna personalized routine dekhne ke liye!")