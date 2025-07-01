import streamlit as st
import pandas as pd
import numpy as np
import json
import datetime
from typing import Dict, List, Tuple
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
import re
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.protocol_loader import ProtocolLoader, Protocol

# Configure Streamlit page
st.set_page_config(
    page_title="RemedyOS - Your Natural Healing System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .symptom-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .protocol-item {
        background: #f0f8f0;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #4CAF50;
    }
    .insight-box {
        background: #fff9e6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #ff9800;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Data models
@dataclass
class HealthMetrics:
    energy: int
    sleep_quality: int
    mood: int
    digestion: int
    stress: int
    focus: int

# Protocol class is now imported from utils.protocol_loader

class SymptomAnalyzer:
    def __init__(self):
        self.symptom_patterns = {
            "fatigue": ["tired", "exhausted", "energy", "drained", "sluggish"],
            "digestive": ["bloated", "stomach", "digestion", "gut", "nausea", "constipated"],
            "mental": ["anxious", "focus", "brain fog", "concentration", "memory", "overwhelmed"],
            "sleep": ["sleep", "insomnia", "wake up", "rest", "dreams"],
            "inflammation": ["pain", "aches", "inflamed", "swollen", "sore"],
            "skin": ["skin", "acne", "rash", "dry", "dull", "breakouts"],
            "hormonal": ["cycle", "period", "hormones", "mood swings", "PMS"],
            "stress": ["stressed", "tension", "worry", "pressure", "overwhelmed"]
        }
        
        self.root_causes = {
            "cortisol_imbalance": {
                "triggers": ["fatigue", "mental", "sleep", "stress"],
                "description": "Cortisol cycling issues and adrenal stress"
            },
            "mineral_depletion": {
                "triggers": ["fatigue", "mental", "sleep"],
                "description": "Essential mineral deficiencies affecting cellular function"
            },
            "circadian_disruption": {
                "triggers": ["sleep", "fatigue", "mental"],
                "description": "Disrupted natural rhythms and light exposure"
            },
            "digestive_inflammation": {
                "triggers": ["digestive", "inflammation", "skin"],
                "description": "Gut inflammation affecting overall health"
            },
            "nervous_system_dysregulation": {
                "triggers": ["mental", "stress", "sleep"],
                "description": "Overstimulated nervous system and poor vagal tone"
            }
        }

    def analyze_symptoms(self, symptom_text: str) -> Tuple[List[str], List[str], str]:
        """Analyze symptoms and return categories, root causes, and insight"""
        symptom_text = symptom_text.lower()
        
        # Identify symptom categories
        detected_categories = []
        for category, keywords in self.symptom_patterns.items():
            if any(keyword in symptom_text for keyword in keywords):
                detected_categories.append(category)
        
        # Identify root causes
        root_causes = []
        for cause, data in self.root_causes.items():
            if any(trigger in detected_categories for trigger in data["triggers"]):
                root_causes.append(cause)
        
        # Generate insight
        insight = self._generate_insight(detected_categories, root_causes)
        
        return detected_categories, root_causes, insight

    def _generate_insight(self, categories: List[str], root_causes: List[str]) -> str:
        if "cortisol_imbalance" in root_causes and "circadian_disruption" in root_causes:
            return "You're showing signs of cortisol cycling issues and circadian mismatch, likely worsened by overstimulation and poor light exposure."
        elif "digestive_inflammation" in root_causes:
            return "Your symptoms suggest digestive inflammation is affecting your overall wellbeing and energy levels."
        elif "nervous_system_dysregulation" in root_causes:
            return "Your nervous system appears overstimulated, affecting sleep, mood, and cognitive function."
        else:
            return "Your symptoms indicate a need for foundational support of your body's natural healing processes."

# Protocol generation is now handled by ProtocolLoader

# Initialize session state
if 'health_data' not in st.session_state:
    st.session_state.health_data = []
if 'current_protocol' not in st.session_state:
    st.session_state.current_protocol = []
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False

# Initialize analyzers
symptom_analyzer = SymptomAnalyzer()
protocol_loader = ProtocolLoader()

# Header
st.markdown("""
<div class="main-header">
    <h1>🌱 RemedyOS</h1>
    <p>Your intelligent natural healing system. Describe how you feel, get personalized protocols based on ancient wisdom and modern science.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.selectbox("Choose your path", [
    "🏠 Home", 
    "📝 Symptom Input", 
    "📋 My Protocol", 
    "📊 Progress Tracking",
    "📚 Education Hub",
    "⚙️ Settings"
])

if page == "🏠 Home":
    if not st.session_state.onboarding_complete:
        st.markdown("## Welcome to Your Healing Journey 🌟")
        st.write("RemedyOS helps you understand what's happening in your body and gives you clear, natural protocols to feel better.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🔍 Analyze</h3>
                <p>Describe symptoms in your own words</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Protocol</h3>
                <p>Get personalized healing protocols</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📈 Track</h3>
                <p>Monitor your progress over time</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Your Healing Journey", type="primary"):
            st.session_state.onboarding_complete = True
            st.rerun()
    
    else:
        st.markdown("## Your Healing Dashboard")
        
        if st.session_state.current_protocol:
            st.markdown("### 📋 Today's Protocol")
            for protocol in st.session_state.current_protocol[:3]:
                st.markdown(f"""
                <div class="protocol-item">
                    <strong>{protocol.title}</strong> ({protocol.timing})<br>
                    {protocol.description}
                </div>
                """, unsafe_allow_html=True)
        
        if st.session_state.health_data:
            st.markdown("### 📊 Recent Progress")
            df = pd.DataFrame([{
                'Date': entry['date'],
                'Energy': entry['metrics'].energy,
                'Sleep': entry['metrics'].sleep_quality,
                'Mood': entry['metrics'].mood
            } for entry in st.session_state.health_data[-7:]])  # Last 7 days
            
            fig = px.line(df, x='Date', y=['Energy', 'Sleep', 'Mood'], 
                         title="Your Wellness Trends")
            st.plotly_chart(fig, use_container_width=True)

elif page == "📝 Symptom Input":
    st.markdown("## Tell Me How You're Feeling")
    st.write("Describe your symptoms in your own words. Be as specific as possible about what you're experiencing.")
    
    # Symptom input
    symptoms = st.text_area(
        "How are you feeling today?",
        placeholder="I feel bloated. I sleep badly. My skin looks dull. I get anxious for no reason and I can't focus after lunch.",
        height=150
    )
    
    if st.button("🔍 Analyze My Symptoms", type="primary") and symptoms:
        with st.spinner("Analyzing your symptoms..."):
            categories, root_causes, insight = symptom_analyzer.analyze_symptoms(symptoms)
            
            st.markdown(f"""
            <div class="insight-box">
                <h3>🧠 Your Health Insight</h3>
                <p>{insight}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🎯 Detected Issues")
            for i, category in enumerate(categories):
                st.markdown(f"• {category.replace('_', ' ').title()}")
            
            # Generate protocol
            protocol = protocol_loader.get_protocols_for_causes(root_causes)
            st.session_state.current_protocol = protocol
            
            st.markdown("### 📋 Your 7-Day Protocol")
            st.write("Here's your personalized healing plan:")
            
            for protocol_item in protocol:
                with st.expander(f"🎯 {protocol_item.title} ({protocol_item.difficulty})"):
                    st.write(f"**When:** {protocol_item.timing}")
                    st.write(f"**What:** {protocol_item.description}")
                    st.write(f"**Why:** {protocol_item.evidence}")
                    
                    if protocol_item.instructions:
                        st.write("**Instructions:**")
                        for instruction in protocol_item.instructions:
                            st.write(f"• {instruction}")
                    
                    if protocol_item.benefits:
                        st.write("**Benefits:**")
                        for benefit in protocol_item.benefits:
                            st.write(f"✓ {benefit}")
            
            st.success("✅ Protocol generated! Check 'My Protocol' to start tracking.")

elif page == "📋 My Protocol":
    if st.session_state.current_protocol:
        st.markdown("## Your Current Protocol")
        
        # Protocol overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            for i, protocol in enumerate(st.session_state.current_protocol):
                with st.expander(f"{protocol.title} - {protocol.timing}"):
                    st.write(f"**Action:** {protocol.description}")
                    st.write(f"**Evidence:** {protocol.evidence}")
                    st.write(f"**Category:** {protocol.category}")
                    
                    if protocol.instructions:
                        st.write("**Detailed Instructions:**")
                        for instruction in protocol.instructions:
                            st.write(f"• {instruction}")
                    
                    # Simple completion tracking
                    completed = st.checkbox(f"Completed today", key=f"protocol_{i}")
        
        with col2:
            st.markdown("### 📈 Quick Health Check")
            
            if st.button("🔄 Log Today's Metrics"):
                with st.form("daily_metrics"):
                    st.write("Rate how you feel today (1-10):")
                    
                    energy = st.slider("Energy Level", 1, 10, 5)
                    sleep_quality = st.slider("Sleep Quality", 1, 10, 5)
                    mood = st.slider("Mood", 1, 10, 5)
                    digestion = st.slider("Digestion", 1, 10, 5)
                    stress = st.slider("Stress Level (lower is better)", 1, 10, 5)
                    focus = st.slider("Mental Focus", 1, 10, 5)
                    
                    submitted = st.form_submit_button("💾 Save Metrics")
                    
                    if submitted:
                        metrics = HealthMetrics(energy, sleep_quality, mood, digestion, stress, focus)
                        
                        st.session_state.health_data.append({
                            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                            'metrics': metrics,
                            'symptoms': '',
                            'notes': ''
                        })
                        
                        st.success("✅ Metrics saved!")
                        st.rerun()
    else:
        st.warning("⚠️ No active protocol. Please input your symptoms first!")
        if st.button("📝 Input Symptoms"):
            st.session_state.page = "📝 Symptom Input"
            st.rerun()

elif page == "📊 Progress Tracking":
    st.markdown("## Your Healing Progress")
    
    if st.session_state.health_data:
        # Create dataframe from health data
        df = pd.DataFrame([{
            'Date': entry['date'],
            'Energy': entry['metrics'].energy,
            'Sleep Quality': entry['metrics'].sleep_quality,
            'Mood': entry['metrics'].mood,
            'Digestion': entry['metrics'].digestion,
            'Stress Level': 11 - entry['metrics'].stress,  # Invert stress so higher is better
            'Focus': entry['metrics'].focus
        } for entry in st.session_state.health_data])
        
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        
        # Overall wellness score
        df['Wellness Score'] = df[['Energy', 'Sleep Quality', 'Mood', 'Digestion', 'Stress Level', 'Focus']].mean(axis=1)
        
        # Display current metrics
        if len(df) > 0:
            latest = df.iloc[-1]
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔋 Energy", f"{latest['Energy']}/10")
            with col2:
                st.metric("😴 Sleep", f"{latest['Sleep Quality']}/10")
            with col3:
                st.metric("😊 Mood", f"{latest['Mood']}/10")
            with col4:
                st.metric("🎯 Overall", f"{latest['Wellness Score']:.1f}/10")
        
        # Progress charts
        fig = px.line(df, x='Date', y='Wellness Score', 
                     title="📈 Overall Wellness Trend",
                     line_shape='spline')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed metrics
        fig2 = px.line(df, x='Date', 
                      y=['Energy', 'Sleep Quality', 'Mood', 'Digestion', 'Focus'],
                      title="📊 Detailed Health Metrics")
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Export option
        if st.button("📄 Export Progress Report"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"remedyos_progress_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    else:
        st.info("📊 Start tracking your daily metrics to see progress over time!")

elif page == "📚 Education Hub":
    st.markdown("## Learn About Natural Healing")
    
    education_topics = {
        "🌅 Circadian Rhythms": {
            "description": "How light exposure affects your sleep, energy, and hormones",
            "key_points": [
                "Morning sunlight sets your biological clock",
                "Blue light at night disrupts melatonin production",
                "Consistent sleep-wake times improve hormone balance"
            ]
        },
        "🧂 Mineral Balance": {
            "description": "Essential minerals for cellular function and energy",
            "key_points": [
                "Magnesium is needed for 300+ enzymatic processes",
                "Trace minerals support adrenal and thyroid function",
                "Unrefined salt provides natural electrolyte balance"
            ]
        },
        "🫁 Breathwork": {
            "description": "How breathing patterns affect your nervous system",
            "key_points": [
                "Slow exhales activate the parasympathetic nervous system",
                "Box breathing reduces stress hormones",
                "Nasal breathing improves oxygen utilization"
            ]
        },
        "🔥 Digestive Fire": {
            "description": "Traditional wisdom on optimal digestion",
            "key_points": [
                "Warm foods are easier to digest than cold",
                "Eating in a calm state improves nutrient absorption",
                "Digestive bitters stimulate natural enzyme production"
            ]
        }
    }
    
    for topic, content in education_topics.items():
        with st.expander(topic):
            st.write(content["description"])
            st.write("**Key Points:**")
            for point in content["key_points"]:
                st.write(f"• {point}")

elif page == "⚙️ Settings":
    st.markdown("## Settings & Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔔 Notifications")
        morning_reminder = st.checkbox("Morning protocol reminder", value=True)
        evening_reminder = st.checkbox("Evening wind-down reminder", value=True)
        progress_check = st.checkbox("Weekly progress check-in", value=True)
    
    with col2:
        st.markdown("### 🎯 Goals")
        primary_goal = st.selectbox("Primary health goal", [
            "Increase Energy",
            "Improve Sleep",
            "Reduce Stress",
            "Better Digestion",
            "Mental Clarity"
        ])
    
    st.markdown("### 📱 Data Management")
    if st.button("🗑️ Clear All Data"):
        if st.checkbox("I understand this will delete all my progress"):
            st.session_state.health_data = []
            st.session_state.current_protocol = []
            st.session_state.onboarding_complete = False
            st.success("✅ Data cleared successfully!")
            st.rerun()
    
    if st.button("📤 Export All Data"):
        data_export = {
            'health_data': st.session_state.health_data,
            'current_protocol': [p.__dict__ for p in st.session_state.current_protocol],
            'export_date': datetime.datetime.now().isoformat()
        }
        
        json_data = json.dumps(data_export, indent=2, default=str)
        st.download_button(
            label="⬇️ Download Data",
            data=json_data,
            file_name=f"remedyos_data_{datetime.datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🌱 RemedyOS - Your natural healing companion<br>
    <small>This app provides educational information only. Consult healthcare providers for medical concerns.</small>
</div>
""", unsafe_allow_html=True)