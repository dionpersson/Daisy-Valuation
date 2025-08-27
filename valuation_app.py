import re
import json
import base64
import requests
import msal
from io import BytesIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file if it exists
load_dotenv()

# Vegas-themed styling
st.set_page_config(page_title="Daisy's Business Valuation Calculator", page_icon="🎰", layout="wide")

# Add Poppins font using HTML components
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap" rel="stylesheet" />
""", unsafe_allow_html=True)

# Custom CSS for sophisticated Vegas theme with Daisy brand colors
st.markdown("""
<style>

:root {
    --primary: #00172b;
    --primary-foreground: #ffffff;
    --secondary: #e3e6e8;
    --secondary-foreground: #000000;
    --accent: #e3e8e7;
    --destructive: #bf4040;
    --background: #ffffff;
    --foreground: #1a1a1a;
    --primary-contrast: #fffcf2;
    --primary-orange: #ffc89d;
}

* {
    font-family: 'Poppins', sans-serif !important;
}

.main {
    background: linear-gradient(135deg, var(--primary), #001a33, #002244);
    color: var(--primary-foreground);
    min-height: 100vh;
}

/* Force Poppins on all Streamlit elements */
.stApp, .stApp * {
    font-family: 'Poppins', sans-serif !important;
}

html, body, [class*="css"], .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, var(--primary), #001a33, #002244);
}

/* Enhanced text contrast for better readability */
.stMarkdown p, .stMarkdown div, .stMarkdown span {
    color: #ffffff ;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) ;
}

.stMarkdown strong {
    color: var(--primary-orange) ;
    font-weight: 600 ;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5) ;
}

/* Input labels with better contrast for all devices */
.stTextInput label, 
.stNumberInput label, 
.stSlider label,
.stTextInput > label,
.stNumberInput > label,
.stSlider > label {
    color: #ffffff !important;
    font-weight: 500 !important;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4) !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* Ensure all form-related text is visible */
div[data-testid="stText"],
div[data-testid="stMarkdown"] p,
.stMarkdown p {
    color: #ffffff !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
}

/* Mobile label adjustments */
@media (max-width: 768px) {
    .stTextInput label, 
    .stNumberInput label, 
    .stSlider label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
}

.stTitle {
    color: var(--primary-orange) ;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 ;
    font-size: clamp(1.8rem, 4vw, 2.5rem) ;
    text-align: center ;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) ;
}

.stHeader {
    color: var(--primary-orange) ;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 ;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4) ;
}

.premium-text {
    color: var(--primary-orange);
    font-weight: 600;
    font-family: 'Poppins', sans-serif !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

.elegant-neon {
    color: var(--primary-orange);
    text-shadow: 0 0 30px rgba(255, 200, 157, 0.2), 0 0 60px rgba(255, 200, 157, 0.1);
    font-weight: 700;
    font-family: 'Poppins', sans-serif;
    letter-spacing: 0.5px;
}

.value-display {
    background: linear-gradient(135deg, rgba(255, 200, 157, 0.1), rgba(255, 252, 242, 0.05));
    border: 2px solid var(--primary-orange);
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(255, 200, 157, 0.15);
}

/* Slot Machine Animation Styles */
.slot-machine-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin: 20px 0;
}

.slot-reel {
    background: linear-gradient(135deg, #001a33, #002244);
    border: 2px solid var(--primary-orange);
    border-radius: 8px;
    padding: 15px;
    min-width: 200px;
    height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.slot-reel::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, transparent 20%, rgba(255, 200, 157, 0.05) 50%, transparent 80%);
    pointer-events: none;
}

.daisy-slot-reel {
    color: var(--primary-orange);
}

.slot-title {
    color: var(--primary-orange);
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
}

.slot-value {
    color: #ffffff;
    font-size: 24px;
    font-weight: 700;
    font-family: 'Courier New', monospace;
    text-shadow: 0 0 10px rgba(255, 200, 157, 0.4);
    transition: all 0.1s ease;
}

.slot-value.spinning {
    animation: slotSpin 0.1s infinite;
    color: var(--primary-orange);
    text-shadow: 0 0 15px rgba(255, 200, 157, 0.6);
}

@keyframes slotSpin {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-2px); }
    100% { transform: translateY(0px); }
}

.slot-value.final {
    animation: slotLand 0.5s ease-out;
    color: var(--primary-orange);
    text-shadow: 0 0 20px rgba(255, 200, 157, 0.5);
    font-size: 28px;
}

@keyframes slotLand {
    0% { transform: scale(1.2); }
    50% { transform: scale(0.9); }
    100% { transform: scale(1); }
}

/* Responsive design */
@media (max-width: 768px) {
    .elegant-neon {
        font-size: clamp(1.2rem, 5vw, 1.8rem);
    }
    
    .value-display {
        padding: 12px;
    }
    
    .slot-machine-container {
        flex-direction: column;
        gap: 15px;
    }
    
    .slot-reel {
        min-width: 150px;
        height: 100px;
    }
    
    .slot-value {
        font-size: 20px;
    }
    
    .slot-value.final {
        font-size: 24px;
    }
}

/* Custom button styling */
.stButton, .stDownloadButton {
    display: flex;
    justify-content: center;
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--primary-orange), #ffb366);
    color: var(--primary) ;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(255, 200, 157, 0.3);
    width: fit-content ;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 200, 157, 0.4);
}

/* Comprehensive Input styling for all devices and modes */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextInput input,
.stNumberInput input {
    background: rgba(255, 252, 242, 0.15) !important;
    border: 2px solid var(--accent) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s ease !important;
}

/* Enhanced focus state */
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextInput input:focus,
.stNumberInput input:focus {
    background: rgba(255, 252, 242, 0.25) !important;
    border-color: var(--primary-orange) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(255, 200, 157, 0.3) !important;
    outline: none !important;
}

/* Hover state */
.stTextInput > div > div > input:hover,
.stNumberInput > div > div > input:hover,
.stTextInput input:hover,
.stNumberInput input:hover {
    background: rgba(255, 252, 242, 0.2) !important;
    border-color: rgba(255, 200, 157, 0.8) !important;
}

/* Placeholder text styling */
.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
    font-weight: 400 !important;
}

/* Force text color on all input states including autofill */
.stTextInput input:-webkit-autofill,
.stNumberInput input:-webkit-autofill,
.stTextInput input:-webkit-autofill:hover,
.stNumberInput input:-webkit-autofill:hover,
.stTextInput input:-webkit-autofill:focus,
.stNumberInput input:-webkit-autofill:focus {
    -webkit-text-fill-color: #ffffff !important;
    -webkit-box-shadow: 0 0 0px 1000px rgba(255, 252, 242, 0.15) inset !important;
    transition: background-color 5000s ease-in-out 0s !important;
}

/* Mobile-specific input styling */
@media (max-width: 768px) {
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextInput input,
    .stNumberInput input {
        background: rgba(255, 252, 242, 0.2) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255, 200, 157, 0.6) !important;
        font-size: 16px !important; /* Prevents zoom on iOS */
        padding: 12px 15px !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stTextInput input:focus,
    .stNumberInput input:focus {
        background: rgba(255, 252, 242, 0.3) !important;
        color: #ffffff !important;
        border-color: var(--primary-orange) !important;
    }
}

.stSlider > div > div > div > div {
    background: var(--primary-orange);
}

/* Sidebar styling if present */
.css-1d391kg {
    background: var(--primary);
}
</style>
""", unsafe_allow_html=True)

# Daisy Branding with sophisticated Vegas flair
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("images/daisy_full_sunrise + warm connection.png", use_container_width=False)

st.markdown('<h1 class="elegant-neon" style="text-align: center;">Business Valuation Calculator</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="premium-text" style="text-align: center; font-weight: 400; margin-bottom: 30px;">Discover Your Company\'s True Potential</h3>', unsafe_allow_html=True)

# Contact Information Section
st.header("👤 Contact Information")
st.markdown("**Please provide your details to receive your personalized valuation report:**")

col1, col2 = st.columns(2)
with col1:
    dealer_name = st.text_input("Full Name", placeholder="Enter your name")
    company_name = st.text_input("Company Name", placeholder="Your company name")
with col2:
    location = st.text_input("Location", placeholder="City, State")
    email = st.text_input("Email Address", placeholder="your.email@company.com")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Business Information Section
st.header("📊 Business Metrics")
st.markdown(
    "**Enter your business details below.** "
    "If you don't have exact numbers, provide your best estimates."
)

# Inputs
revenue = st.number_input("1. Total Annual Revenue ($)", min_value=0,
                          value=1000000, step=1, format="%d")
num_employees = st.number_input("2. Number of Employees", min_value=0, step=1)
profit_margin = st.slider("3. Net Margin (after addbacks) (%)", 0, 100, 15)
recurring_pct = st.slider("4. RMR/Recurring Revenue (% of revenue)", 0, 100, 10)
growth_pct = st.slider("5. Average Growth Rate (%)", 0, 100, 10)
st.markdown('</div>', unsafe_allow_html=True)


# Valuation Functions
def base_valuation(revenue, margin, recurring, growth):
    m = margin / 100
    r = recurring / 100
    g = growth / 100
    Z = 10 * m
    A = 4 * r
    B = 8 * g
    X = 2.5 + Z + A + B
    return revenue * m * X


# Handle Calculate button with elegant animation
if "calc_done" not in st.session_state:
    st.session_state.calc_done = False

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎯 Calculate Business Valuation", type="primary", use_container_width=True):
        # Calculate values first
        base_val = base_valuation(revenue, profit_margin, recurring_pct, growth_pct)

        # Slot machine animation
        slot_title = st.empty()
        slot_title.markdown(
            "<div style='text-align: center; font-size: 24px; font-weight: 600; margin-top: 20px;'>🎰 Calculating Your Business Value...</div>", unsafe_allow_html=True)

        # Create slot machine container
        slot_container = st.empty()

        # Animation parameters
        animation_duration = 3  # 3 seconds
        update_interval = 0.1  # Update every 100ms
        total_updates = int(animation_duration / update_interval)

        import random

        # Animate the slot machine
        for i in range(total_updates):
            # Generate random values during spinning
            if i < total_updates - 10:  # Keep spinning until near the end
                random_base = random.randint(int(base_val * 0.5), int(base_val * 1.5))
                spinning_class = "spinning"
            else:
                # Gradually approach final values in last 10 updates
                progress = (i - (total_updates - 10)) / 10
                random_base = int(base_val * (0.8 + 0.2 * progress))
                spinning_class = "spinning"

            # Display single slot machine reel
            slot_container.markdown(f"""
            <div class="slot-machine-container" style="justify-content: center; margin: 30px 0;">
                <div class="slot-reel" style="min-width: 400px; min-height: 150px;">
                    <div class="slot-title" style="font-size: 18px;">Your Business Valuation</div>
                    <div class="slot-value {spinning_class}" style="font-size: 32px;">${random_base:,.0f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            time.sleep(update_interval)

        # Final dramatic reveal
        slot_title.markdown(
            "<div style='text-align: center; font-size: 24px; font-weight: 600; margin-top: 20px;'>🎉 Calculation Complete!</div>", unsafe_allow_html=True)
        slot_container.markdown(f"""
        <div class="slot-machine-container" style="justify-content: center; margin: 30px 0;">
            <div class="slot-reel" style="min-width: 400px; min-height: 150px;">
                <div class="slot-title" style="font-size: 18px;">Your Business Valuation</div>
                <div class="slot-value final" style="font-size: 36px;">${base_val:,.0f}</div>
            </div>
        </div>
        <style>
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); }}
        }}
        </style>
        """, unsafe_allow_html=True)

        # Store values in session state
        st.session_state.base_val = base_val
        st.session_state.pm = profit_margin
        st.session_state.gr = growth_pct
        st.session_state.rr = recurring_pct
        st.session_state.revenue = revenue
        st.session_state.calc_done = True
        st.balloons()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# PDF Generation Function
def generate_pdf(dealer_name, company_name, location, email, revenue, val_base, pm, rr, gr, recommendations):
    try:
        pdf = FPDF()
        pdf.add_page()

        # Define colors (RGB values)
        primary_blue = (0, 23, 43)  # #00172b
        primary_orange = (255, 200, 157)  # #ffc89d
        white = (255, 255, 255)
        light_gray = (240, 240, 240)

        # Full-width Header
        pdf.set_fill_color(*primary_blue)
        pdf.rect(0, 0, 210, 30, 'F')

        # Title in orange on blue background
        pdf.set_text_color(*primary_orange)
        pdf.set_font("Arial", size=18, style='B')
        pdf.set_xy(10, 10)
        pdf.cell(0, 10, "DAISY BUSINESS VALUATION REPORT", ln=True, align='C')

        # Contact Information Section
        pdf.set_xy(10, 40)
        pdf.set_fill_color(*light_gray)
        pdf.set_text_color(*primary_blue)
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 8, "CONTACT INFORMATION", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)
        pdf.cell(0, 6, f"Name: {dealer_name or 'N/A'}", ln=True)
        pdf.cell(0, 6, f"Company: {company_name or 'N/A'}", ln=True)
        pdf.cell(0, 6, f"Location: {location or 'N/A'}", ln=True)
        pdf.cell(0, 6, f"Email: {email or 'N/A'}", ln=True)

        # Business Metrics Section
        pdf.ln(6)
        pdf.set_fill_color(*light_gray)
        pdf.set_text_color(*primary_blue)
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 8, "BUSINESS METRICS", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)
        pdf.cell(0, 6, f"Annual Revenue: ${revenue:,.0f}", ln=True)
        pdf.cell(0, 6, f"Net Margin (after addbacks): {pm}%", ln=True)
        pdf.cell(0, 6, f"RMR/Recurring Revenue: {rr}%", ln=True)
        pdf.cell(0, 6, f"Growth Rate: {gr}%", ln=True)

        # Valuation Results Section
        pdf.ln(8)
        pdf.set_fill_color(*primary_orange)
        pdf.set_text_color(*primary_blue)
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 10, "BUSINESS VALUATION", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=16, style='B')
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(0, 12, f"${val_base:,.0f}", ln=True, fill=True, align='C', border=1)

        # Personalized Recommendations
        pdf.ln(8)
        pdf.set_fill_color(*primary_blue)
        pdf.set_text_color(*primary_orange)
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 8, "PERSONALIZED RECOMMENDATIONS", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=10)
        pdf.ln(3)

        for i, rec in enumerate(recommendations, 1):
            pdf.set_font("Arial", size=10, style='B')
            pdf.cell(0, 6, f"Recommendation #{i}:", ln=True)
            pdf.set_font("Arial", size=9)

            # Word wrap for long recommendations
            words = rec.split(' ')
            line = ''
            for word in words:
                if pdf.get_string_width(line + word + ' ') < 180:
                    line += word + ' '
                else:
                    pdf.cell(0, 5, line.strip(), ln=True)
                    line = word + ' '
            if line:
                pdf.cell(0, 5, line.strip(), ln=True)
            pdf.ln(2)

        # Contact Information Section
        pdf.ln(8)
        pdf.set_fill_color(*primary_orange)
        pdf.set_text_color(*primary_blue)
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 8, "CONTACT DAISY", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11)
        pdf.ln(2)
        pdf.cell(0, 6, "Contact Daisy for a free consultation and additional recommendations", ln=True, align='C')
        pdf.cell(0, 6, "Email: businessvaluations@daisyco.com", ln=True, align='C')

        # Footer with disclaimer
        pdf.ln(8)
        pdf.set_fill_color(*primary_blue)
        pdf.set_text_color(*primary_orange)
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(0, 7, "IMPORTANT DISCLAIMER", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=9, style='I')
        pdf.ln(2)
        pdf.cell(0, 5, "This calculator provides estimates based on the information provided.", ln=True, align='C')
        pdf.cell(0, 5, "Actual company valuations depend on many factors and should be verified by professionals.", ln=True, align='C')
        pdf.cell(0, 5, "Results are for informational purposes and cannot be guaranteed.", ln=True, align='C')

        # Create an in-memory binary stream and save PDF to it
        output_buffer = BytesIO()
        pdf.output(output_buffer)
        pdf_bytes = output_buffer.getvalue()
        output_buffer.close()

        return pdf_bytes
    except Exception as inner_e:
        raise Exception(f"PDF generation failed: {str(inner_e)}")


# Function to generate personalized recommendations
def get_recommendations(margin, growth, recurring):
    x = margin  # margin rate
    y = growth  # growth rate
    z = recurring  # recurring revenue rate

    recommendations = []

    # First recommendation based on margin and growth
    if x < 10:
        rec1 = f"Given your margin is {x}% and your growth rate is {y}%, you should focus on driving margins more than growth. In our experience, for a higher valuation, at margins of 10% or higher, it is best to focus on increasing growth. At margins below 10%, margin improvement becomes more important than growth."
    elif x >= 10 and y < 15:
        rec1 = f"Given your margin is {x}% and your growth rate is {y}%, you should focus on improving your growth rate to 15% or above as long as you can continue to keep your margins above 10%. In our experience, for a higher valuation, at margins of 10% or higher, it is best to focus on increasing growth. At margins below 10%, margin improvement becomes more important than growth."
    elif x >= 10 and x <= 20 and y >= 15:
        rec1 = f"Given your margin is {x}% and your growth rate is {y}%, you should focus on maintaining your excellent business performance with a priority on improving your margin above 20%. In our experience, for a higher valuation, at margins of 10% or higher, it is best to focus on increasing growth. At margins below 10%, margin improvement becomes more important than growth."
    elif x > 20:
        rec1 = f"Given your margin is {x}% and your growth rate is {y}%, you should focus on maintaining your excellent business performance with a priority on increasing your growth rate while keeping your margins steady. In our experience, for a higher valuation, at margins of 10% or higher, it is best to focus on increasing growth. At margins below 10%, margin improvement becomes more important than growth."
    else:
        rec1 = f"Given your margin is {x}% and your growth rate is {y}%, you should focus on maintaining your excellent business performance with a priority on improving your margin above 20%. In our experience, for a higher valuation, at margins of 10% or higher, it is best to focus on increasing growth. At margins below 10%, margin improvement becomes more important than growth."

    recommendations.append(rec1)

    # Second recommendation based on recurring revenue
    if z < 40:
        rec2 = f"We recommend that you increase your recurring revenue from {z}% to 40% of your revenue to obtain the type of valuations in security and pest businesses (up to 4x revenue). Investors value recurring revenue significantly more than project revenue. Daisy has a proven system for increasing your recurring revenue in a dramatic way through DaisyCare."
    elif z >= 40 and z < 100:
        target = min(z + 20, 100)
        rec2 = f"We recommend that you increase your recurring revenue from {z}% to {target}% to obtain the type of valuations in security and pest businesses (up to 4x revenue). Investors value recurring revenue significantly more than project revenue. Daisy has a proven system for increasing your recurring revenue in a dramatic way through DaisyCare."
    else:  # z == 100
        rec2 = "You are doing great on recurring revenue!! Investors value recurring revenue significantly more than project revenue. Keep it up!"

    recommendations.append(rec2)

    # Third recommendation - tech stack
    rec3 = "We recommend building out or obtaining a comprehensive tech stack for your business that contains detailed records of all of your customer interactions (a customer relationship management tool), a financial system with business intelligence that really lets you understand your business performance in real time, and act on it, and an always-updated quoting tool that helps you expedite quotes based on current product and pricing information. Daisy has built out these tools and can help you apply them to your business."
    recommendations.append(rec3)

    return recommendations


# Microsoft Graph API Email Configuration
# IMPORTANT: Configure these settings before deploying
TENANT_ID = os.environ.get('TENANT_ID')  # Your Azure tenant ID
CLIENT_ID = os.environ.get('CLIENT_ID')  # Your app registration client ID
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')  # Your app registration client secret
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')  # Email address that will send emails
BCC_EMAILS = os.environ.get('BCC_EMAILS')  # Comma-separated list of BCC email addresses (optional)

# Microsoft Graph API Configuration Instructions:
# 1. Register an app in Azure Portal (App registrations)
# 2. Grant Mail.Send permission (Application type)
# 3. Admin consent for the tenant
# 4. Create a client secret
# 5. Use environment variables in production
# 6. The sender email must belong to your Azure tenant
# 7. BCC_EMAILS is optional - format: "email1@domain.com,email2@domain.com"


def validate_email(email):
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_graph_access_token():
    """Get access token for Microsoft Graph API"""
    try:
        # Create a confidential client application
        app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{TENANT_ID}",
            client_credential=CLIENT_SECRET,
        )

        # Get token for Microsoft Graph
        scopes = ["https://graph.microsoft.com/.default"]
        result = app.acquire_token_for_client(scopes=scopes)

        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Failed to acquire token: {result.get('error_description', 'Unknown error')}")

    except Exception as e:
        raise Exception(f"Authentication failed: {str(e)}")


def send_valuation_email(recipient_email, dealer_name, company_name, pdf_data):
    """Send valuation report as email attachment using Microsoft Graph API"""
    try:
        # Validate required environment variables
        missing_vars = []
        if not TENANT_ID:
            missing_vars.append('TENANT_ID')
        if not CLIENT_ID:
            missing_vars.append('CLIENT_ID')
        if not CLIENT_SECRET:
            missing_vars.append('CLIENT_SECRET')
        if not SENDER_EMAIL:
            missing_vars.append('SENDER_EMAIL')

        if missing_vars:
            return False, f"Missing required environment variables: {', '.join(missing_vars)}"

        # Get access token
        access_token = get_graph_access_token()

        # Email body
        body_text = f"""
Dear {dealer_name or 'Valued Client'},

Thank you for using Daisy's Business Valuation Calculator!

Attached to this email is your personalized business valuation report for {company_name or 'your company'}.

This report includes:
- Your calculated business valuation
- Personalized recommendations based on your metrics
- Next steps to maximize your company's value

If you'd like to discuss your valuation further or need help implementing these recommendations, please don't hesitate to contact us for a free consultation.

Best regards,
The Daisy Team
Daisy Business Valuations
Email: businessvaluations@daisyco.com

---
This email was sent automatically from Daisy's Business Valuation Calculator.
For any questions, please reply to this email or contact us at businessvaluations@daisyco.com
        """

        # Encode PDF as base64
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
        filename = f"{company_name or 'Business'} Valuation Report.pdf"

        # Prepare BCC recipients if configured
        bcc_recipients = []
        if BCC_EMAILS:
            bcc_emails_list = [email.strip() for email in BCC_EMAILS.split(',') if email.strip()]
            for bcc_email in bcc_emails_list:
                if validate_email(bcc_email):
                    bcc_recipients.append({
                        "emailAddress": {
                            "address": bcc_email
                        }
                    })

        # Create email message for Graph API
        email_message = {
            "message": {
                "subject": f"Your Business Valuation Report - {company_name or 'Your Company'}",
                "body": {
                    "contentType": "Text",
                    "content": body_text
                },
                "toRecipients": [
                    {
                        "emailAddress": {
                            "address": recipient_email
                        }
                    }
                ],
                "attachments": [
                    {
                        "@odata.type": "#microsoft.graph.fileAttachment",
                        "name": filename,
                        "contentType": "application/pdf",
                        "contentBytes": pdf_base64
                    }
                ]
            },
            "saveToSentItems": "true"
        }

        # Add BCC recipients if any are configured
        if bcc_recipients:
            email_message["message"]["bccRecipients"] = bcc_recipients

        # Send email using Microsoft Graph API
        graph_url = f"https://graph.microsoft.com/v1.0/users/{SENDER_EMAIL}/sendMail"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            graph_url,
            headers=headers,
            data=json.dumps(email_message)
        )

        if response.status_code == 202:
            return True, "Email sent successfully!"
        else:
            error_details = response.text
            try:
                error_json = response.json()
                error_message = error_json.get('error', {}).get('message', error_details)
            except:
                error_message = error_details
            return False, f"Failed to send email: {error_message}"

    except Exception as e:
        return False, f"Failed to send email: {str(e)}"


# If calculation has been run, show results
if st.session_state.calc_done:
    val_base = st.session_state.base_val
    pm = st.session_state.pm
    gr = st.session_state.gr
    rr = st.session_state.rr

    # Get personalized recommendations
    recommendations = get_recommendations(pm, gr, rr)

    # Display recommendations prominently
    st.markdown('<h2 class="elegant-neon" style="text-align: center; margin: 40px 0 20px 0;">🌟 Your Personalized Recommendations for Creating Generational Wealth</h2>', unsafe_allow_html=True)
    st.markdown('<h4 class="premium-text" style="text-align: center; margin-bottom: 30px;">Here are your top three recommendations based on your business metrics:</h4>', unsafe_allow_html=True)

    # Style for recommendation boxes
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f'''
        <div style="background: linear-gradient(135deg, rgba(255, 200, 157, 0.15), rgba(255, 252, 242, 0.08)); 
                    border: 2px solid #ffc89d; border-radius: 12px; padding: 20px; margin: 20px 0; 
                    box-shadow: 0 6px 20px rgba(255, 200, 157, 0.2);">
            <h4 style="color: #ffc89d; margin: 0 0 15px 0; font-weight: 600; font-size: 1.2rem;">
                💡 Recommendation #{i}
            </h4>
            <p style="color: #ffffff; margin: 0; font-size: 16px; line-height: 1.6;">
                {rec}
            </p>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # PDF and Meeting Section
    st.markdown('<h3 class="premium-text" style="text-align: center;">📋 Next Steps</h3>', unsafe_allow_html=True)

    # Single button to generate and download PDF
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            pdf_data = generate_pdf(
                dealer_name,
                company_name,
                location,
                email,
                st.session_state.revenue,
                val_base,
                st.session_state.pm,
                st.session_state.rr,
                st.session_state.gr,
                recommendations
            )

            # Email button with validation
            if st.button("📧 Email me my valuation report", type="primary", use_container_width=True):
                # Use current email input, not session state (in case user changed it after calculation)
                if not email or not email.strip():
                    st.error("⚠️ Please provide an email address in the contact information section above.")
                elif not validate_email(email):
                    st.error("⚠️ Please enter a valid email address.")
                else:
                    with st.spinner("📤 Sending your valuation report..."):
                        success, message = send_valuation_email(
                            email,
                            dealer_name,
                            company_name,
                            pdf_data
                        )

                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
                        # Fallback option to download if email fails
                        st.download_button(
                            label="📄 Download PDF instead",
                            data=pdf_data,
                            file_name=f"{company_name or 'Business'} Valuation Report.pdf",
                            mime="application/pdf",
                            type="secondary",
                            use_container_width=True,
                        )
        except Exception as e:
            st.error(f"⚠️ Unable to generate PDF: {str(e)}")
            st.button("📄 PDF Unavailable", disabled=True, type="secondary", use_container_width=True)

        st.markdown(f"""
        <div style="text-align: center;">
            <a href="https://outlook.office.com/book/DaisyCoCEDIABusinessValuationConsultations@daisyco.com" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #ffc89d, #ffb366); color: #00172b; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 400; box-shadow: 0 4px 16px rgba(255, 200, 157, 0.3); transition: all 0.3s ease;">
                📅 Contact me for my free consultation
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown('<h3 class="premium-text" style="text-align: center; margin-top: 30px;">⚖️ Important Disclaimer</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: #ffffff; font-style: italic; font-size: 14px; text-align: center;">
        This calculator is for entertainment purposes only and just like the slots, results may vary! 
        Actual company valuations depend on many factors and cannot be guaranteed. 
        What happens in Daisy's Vegas booth… stays in Daisy's Vegas booth, 
        unless it's your valuation which we hope shoots to the moon! 🚀🌙
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
