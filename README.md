# 🎰 Daisy's Vegas Valuation Calculator

Welcome to Daisy's Vegas-themed business valuation calculator! This interactive web application helps dealers calculate their business value with a fun casino twist, perfect for trade shows and client engagement.

## 🚀 Features

- **Vegas Casino Theme**: Complete with slot machine animations, neon styling, and casino terminology
- **Contact Collection**: Capture dealer information (name, company, location, email)
- **Business Valuation**: Calculate current and projected business values
- **PDF Reports**: Generate downloadable valuation reports
- **Meeting Scheduling**: Direct integration with Calendly for consultations
- **Interactive Tips**: Business improvement recommendations
- **Responsive Design**: Works on desktop and tablet displays

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.7+** (Download from [python.org](https://python.org))
- **pip** (Python package installer - comes with Python)

## 🛠️ Installation

1. **Clone or download the repository**

   ```bash
   git clone <repository-url>
   cd Daisy-Valuation
   ```

2. **Install required packages**

   ```bash
   pip install streamlit numpy pandas matplotlib fpdf2
   ```

   **Important:** Make sure to install `fpdf2` (not `fpdf`) for PDF generation:

   ```bash
   pip install fpdf2
   ```

## ▶️ Running the Application

1. **Start the Streamlit server**

   ```bash
   streamlit run valuation_app.py
   ```

2. **Open your browser**

   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

3. **For public access (trade shows)**
   ```bash
   streamlit run valuation_app.py --server.address 0.0.0.0 --server.port 8501
   ```

## 🎯 Usage

### For Dealers:

1. **High Roller Registration**: Enter your contact information
2. **Business Information**: Input your company's financial metrics
3. **Spin the Wheel**: Click the valuation button to see results
4. **Get Your Report**: Download PDF or schedule a meeting with Daisy

### For Trade Show Setup:

1. Connect a large display or tablet
2. Ensure stable internet connection for PDF downloads and meeting scheduling
3. Position near your booth for maximum visibility
4. Consider running in fullscreen mode for best presentation

## 🔧 Configuration

### Scheduling Integration

Update the Scheduling URL in the code (line ~252):

```python
<a href="https://calendly.com/your-calendly-link" target="_blank">
```

## 📊 Technical Details

### Dependencies

- **streamlit**: Web application framework
- **numpy**: Numerical computations
- **pandas**: Data manipulation
- **matplotlib**: Chart generation
- **fpdf2**: PDF report generation

### File Structure

```
Daisy-Valuation/
├── valuation_app.py    # Main application file
├── README.md          # This file
└── requirements.txt   # Python dependencies (optional)
```

## 🎰 Vegas Theme Elements

- **Slot Machine Containers**: Styled input sections
- **Neon Text Effects**: Eye-catching headers
- **Casino Colors**: Gold, red, and dark blue palette
- **Animated Spinner**: Progress bar during calculations
- **Casino Language**: "High Roller", "Jackpot", "House Rules"

## 🐛 Troubleshooting

### Common Issues:

**App won't start:**

- Ensure Python 3.7+ is installed
- Check all dependencies are installed
- Verify you're in the correct directory

**PDF generation fails:**

- Ensure fpdf2 is installed: `pip install fpdf2`
- Check that all form fields are filled out

**Charts not displaying:**

- Ensure matplotlib is installed: `pip install matplotlib`
- Try restarting the application

**Port already in use:**

```bash
streamlit run valuation_app.py --server.port 8502
```

## 📞 Support

For technical support or questions:

- Check the troubleshooting section above
- Ensure all dependencies are properly installed
- Restart the application if encountering issues

## 🎲 Disclaimer

This calculator is for entertainment purposes only and just like the slots, results may vary! Actual company valuations depend on many factors and cannot be guaranteed. What happens in Daisy's Vegas booth… stays in Daisy's Vegas booth, unless it's your valuation which we hope shoots to the moon! 🚀🌙

---

**Ready to hit the jackpot?** Run the app and let the Vegas magic begin! 🎰✨
