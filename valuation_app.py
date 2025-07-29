import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO

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
    font-family: 'Poppins', sans-serif;
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

.stTitle {
    color: var(--primary-orange) !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: clamp(1.8rem, 4vw, 2.5rem) !important;
    text-align: center !important;
}

.stHeader {
    color: var(--primary-orange) !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
}



.premium-text {
    color: var(--primary-orange);
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
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

/* Responsive design */
@media (max-width: 768px) {
    .elegant-neon {
        font-size: clamp(1.2rem, 5vw, 1.8rem);
    }
    
    .value-display {
        padding: 12px;
    }
}

/* Custom button styling */
.stButton, .stDownloadButton {
    display: flex;
    justify-content: center;
}
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, var(--primary-orange), #ffb366);
    color: var(--primary) !important;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-family: 'Poppins', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(255, 200, 157, 0.3);
    width: fit-content !important;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 200, 157, 0.4);
}

/* Input styling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(255, 252, 242, 0.1);
    border: 1px solid var(--accent);
    color: var(--primary-foreground);
    border-radius: 6px;
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
revenue = st.number_input("1. Total Annual Revenue ($)", min_value=0, value=1000000, step=1, format="%d")
num_employees = st.number_input("2. Number of Employees", min_value=0, step=1)
profit_margin = st.slider("3. Net Margin (after addbacks) (%)", 0, 100, 15)
recurring_pct = st.slider("4. Recurring Revenue (% of revenue)", 0, 100, 10)
rmr_pct = st.slider("5. RMR - Recurring Monthly Revenue (% of revenue)", 0, 100, 5)
growth_pct_input = st.slider("6. Average Growth Rate (%)", 0, 100, 10)
growth_pct = min(growth_pct_input, 25)  # Cap at 25%
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


def daisy_valuation(revenue):
    return revenue * 1.45 * 0.2 * 12.5  # Daisy = revenue × 3.625


# Handle Calculate button with elegant animation
if "calc_done" not in st.session_state:
    st.session_state.calc_done = False

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎯 Calculate Business Valuation", type="primary", use_container_width=True):
        with st.spinner("✨ Analyzing your business metrics..."):
            # Elegant progress animation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.015)
                progress_bar.progress(i + 1)
            progress_bar.empty()

        st.session_state.base_val = base_valuation(revenue, profit_margin, recurring_pct, growth_pct)
        st.session_state.daisy_val = daisy_valuation(revenue)
        st.session_state.pm = profit_margin
        st.session_state.gr = growth_pct
        st.session_state.rr = recurring_pct
        st.session_state.rmr = rmr_pct
        st.session_state.dealer_name = dealer_name
        st.session_state.company_name = company_name
        st.session_state.location = location
        st.session_state.email = email
        st.session_state.revenue = revenue
        st.session_state.calc_done = True
        st.balloons()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# PDF Generation Function
def generate_pdf(dealer_name, company_name, location, email, revenue, val_base, val_daisy, pm, rr, rmr, gr):
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
        pdf.cell(0, 6, f"Recurring Revenue: {rr}%", ln=True)
        pdf.cell(0, 6, f"RMR (Recurring Monthly Revenue): {rmr}%", ln=True)
        pdf.cell(0, 6, f"Growth Rate: {gr}%", ln=True)

        # Valuation Results Section - Table Style
        pdf.ln(8)
        pdf.set_fill_color(*primary_orange)
        pdf.set_text_color(*primary_blue)
        pdf.set_font("Arial", size=14, style='B')
        pdf.cell(0, 10, "VALUATION RESULTS", ln=True, fill=True, align='C')

        pdf.ln(3)

        # Table headers
        pdf.set_fill_color(245, 245, 245)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(63, 8, "Current Valuation", border=1, fill=True, align='C')

        pdf.set_fill_color(*primary_orange)
        pdf.set_text_color(*primary_blue)
        pdf.cell(64, 8, "With Daisy Partnership", border=1, fill=True, align='C')

        pdf.set_fill_color(200, 255, 200)
        pdf.set_text_color(0, 100, 0)
        pdf.cell(63, 8, "Potential Increase", ln=True, border=1, fill=True, align='C')

        # Table values
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=12, style='B')
        pdf.set_fill_color(255, 255, 255)
        pdf.cell(63, 10, f"${val_base:,.0f}", border=1, fill=True, align='C')

        pdf.set_fill_color(255, 245, 230)
        pdf.set_text_color(*primary_blue)
        pdf.cell(64, 10, f"${val_daisy:,.0f}", border=1, fill=True, align='C')

        pdf.set_fill_color(240, 255, 240)
        pdf.set_text_color(0, 120, 0)
        pdf.cell(63, 10, f"${val_daisy - val_base:,.0f}", ln=True, border=1, fill=True, align='C')

        # Key Value Enhancement Opportunities
        pdf.ln(8)
        pdf.set_fill_color(*primary_blue)
        pdf.set_text_color(*primary_orange)
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 8, "KEY VALUE ENHANCEMENT OPPORTUNITIES", ln=True, fill=True, align='C')

        # Generate tips
        if pm < 10 and gr < 10 and rr < 30:
            tips = [
                "Improve net margin (after addbacks) to 20%",
                "Increase recurring revenue to 30%",
                "Target growth rate above 10%",
                "Implement comprehensive tech stack"
            ]
        elif pm < 10 and gr >= 10 and rr < 30:
            tips = [
                "Improve net margin (after addbacks) to 20%",
                "Increase recurring revenue to 30%",
                "Implement comprehensive tech stack",
                f"Accelerate growth rate to {gr + 5:.0f}%"
            ]
        else:
            tips = [
                "Increase recurring revenue to 30%",
                "Implement comprehensive tech stack",
                "Maintain net margins at 20% or higher",
                "Target growth rate of 15% or higher"
            ]

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11)
        pdf.ln(3)

        for i, tip in enumerate(tips, 1):
            pdf.cell(0, 6, f"{i}. {tip}", ln=True)

        # Footer with disclaimer
        pdf.ln(8)
        pdf.set_fill_color(*primary_blue)
        pdf.set_text_color(*primary_orange)
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(0, 7, "IMPORTANT DISCLAIMER", ln=True, fill=True, align='C')

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=9, style='I')
        pdf.ln(2)
        pdf.cell(0, 5, "This calculator is for entertainment purposes only and just like the slots, results may vary!", ln=True, align='C')
        pdf.cell(0, 5, "Actual company valuations depend on many factors and cannot be guaranteed.", ln=True, align='C')
        pdf.cell(0, 5, "What happens in Daisy's Vegas booth... stays in Daisy's Vegas booth,", ln=True, align='C')
        pdf.cell(0, 5, "unless it's your valuation which we hope shoots to the moon!", ln=True, align='C')

        # Create an in-memory binary stream and save PDF to it
        output_buffer = BytesIO()
        pdf.output(output_buffer)
        pdf_bytes = output_buffer.getvalue()
        output_buffer.close()

        return pdf_bytes
    except Exception as inner_e:
        raise Exception(f"PDF generation failed: {str(inner_e)}")


# If calculation has been run, show results
if st.session_state.calc_done:
    val_base = st.session_state.base_val
    val_daisy = st.session_state.daisy_val

    df = pd.DataFrame({
        "Scenario": ["Without Daisy", "With Daisy's Help"],
        "Valuation": [val_base, val_daisy]
    })

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#00172b')
    ax.set_facecolor('#001a33')
    bars = ax.bar(df["Scenario"], df["Valuation"], color=["#e3e6e8", "#ffc89d"],
                  edgecolor='#ffc89d', linewidth=2, alpha=0.9)
    ax.set_ylabel("Valuation ($)", color='#ffc89d', fontsize=12, fontweight='600')
    ax.set_title("Business Valuation Comparison", color='#ffc89d', fontsize=16, fontweight='bold', pad=20)
    ax.ticklabel_format(axis='y', style='plain')
    ax.tick_params(colors='#ffc89d', labelsize=10)
    ax.spines['bottom'].set_color('#ffc89d')
    ax.spines['left'].set_color('#ffc89d')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.1, color='#ffc89d')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height * 1.01, f"${height:,.0f}",
                ha='center', va='bottom', color='#ffc89d', fontweight='bold', fontsize=11)

    plt.tight_layout()
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
        <div class="value-display" style="min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4 style="color: #ffffff; margin: 0; font-weight: 400;">Current Valuation</h4>
            <h2 style="color: #ffffff; margin: 10px 0; font-family: Poppins; font-weight: 400;">${val_base:,.0f}</h2>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="value-display" style="background: linear-gradient(135deg, rgba(255, 200, 157, 0.2), rgba(255, 252, 242, 0.1)); border: 3px solid #ffc89d; box-shadow: 0 8px 32px rgba(255, 200, 157, 0.3); min-height: 140px; display: flex; flex-direction: column; justify-content: center;">
            <h4 style="color: #ffc89d; margin: 0; font-weight: 600;">Projected Valuation</h4>
            <p style="color: #ffc89d; margin: 0; font-weight: 500; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">In three years, based on Daisy's expectations</p>
            <h2 style="color: #ffc89d; margin: 10px 0; font-family: Poppins; font-weight: 700; font-size: 2.2rem; text-shadow: 0 0 20px rgba(255, 200, 157, 0.4);">${val_daisy:,.0f}</h2>
        </div>
        ''', unsafe_allow_html=True)

    increase = val_daisy - val_base
    if increase > 0:
        st.markdown(f'''
        <div style="text-align: center; margin: 20px 0;">
            <h3 class="premium-text">✨ Potential Value Increase: ${increase:,.0f}</h3>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # PDF and Meeting Section
    st.markdown('<h3 class="premium-text" style="text-align: center;">📋 Next Steps</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Single button to generate and download PDF
        try:
            pdf_data = generate_pdf(
                st.session_state.dealer_name,
                st.session_state.company_name,
                st.session_state.location,
                st.session_state.email,
                st.session_state.revenue,
                val_base,
                val_daisy,
                st.session_state.pm,
                st.session_state.rr,
                st.session_state.rmr,
                st.session_state.gr
            )

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_data,
                file_name=f"{st.session_state.company_name or 'Business'} Valuation Report.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"⚠️ Unable to generate PDF: {str(e)}")
            st.button("📄 PDF Unavailable", disabled=True, type="secondary", use_container_width=True)

    with col2:
        if st.button("📅 Schedule Consultation", type="primary"):
            st.markdown("""
            <div style="background: rgba(255, 200, 157, 0.1); padding: 16px; border-radius: 8px; text-align: center; border: 2px solid #ffc89d; box-shadow: 0 4px 16px rgba(255, 200, 157, 0.15);">
                <h4 style="color: #ffc89d; margin: 0; font-weight: 600;">💼 Ready to Maximize Your Value?</h4>
                <p style="color: #ffffff; margin: 10px 0; font-size: 14px;">Schedule a consultation with our experts.</p>
                <a href="https://calendly.com/daisy-valuation" target="_blank" style="color: #ffc89d; font-weight: 600; text-decoration: none; font-size: 16px;">
                    🗓️ Book Your Consultation
                </a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Show tips if checkbox selected
    pm = st.session_state.pm
    gr = st.session_state.gr
    rr = st.session_state.rr

    if pm < 10 and gr < 10 and rr < 30:
        tips = [
            "📊 Improve net margin (after addbacks) to ~20%",
            "🔄 Increase recurring revenue to 30%",
            "📈 Target growth rate above 10%",
            "💻 Implement comprehensive tech stack"
        ]
    elif pm < 10 and gr >= 10 and rr < 30:
        tips = [
            "📊 Improve net margin (after addbacks) to ~20%",
            "🔄 Increase recurring revenue to 30%",
            "💻 Implement comprehensive tech stack",
            f"📈 Accelerate growth rate to {gr + 5:.0f}%"
        ]
    else:
        tips = [
            "🔄 Increase recurring revenue to 30%",
            "💻 Implement comprehensive tech stack",
            "📊 Maintain net margins at 20% or higher",
            "📈 Target growth rate of 15% or higher"
        ]

    st.markdown('<h3 class="premium-text" style="text-align: center; margin-top: 30px;">🎯 Key Value Enhancement Opportunities</h3>',
                unsafe_allow_html=True)
    for tip in tips:
        st.markdown(
            f"<p style='color: #ffffff; font-size: 15px; margin: 8px 0; text-align: center;'>• {tip}</p>", unsafe_allow_html=True)

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
