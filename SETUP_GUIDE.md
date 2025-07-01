# 🌱 RemedyOS - Quick Setup Guide

Welcome to RemedyOS! This guide will help you get your natural healing system up and running in minutes.

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8+ (Python 3.13 recommended)
- pip package manager

### 1. Clone & Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd remedyos

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run RemedyOS
```bash
# Method 1: Using the simple runner
python run.py

# Method 2: Direct streamlit command
streamlit run app.py

# Method 3: Using the runner script with activated venv
source venv/bin/activate && streamlit run app.py
```

### 3. Access Your App
Open your browser and go to: `http://localhost:8501`

## 🎯 First Time Usage

1. **Start Your Journey**: Click "Start Your Healing Journey" on the welcome screen
2. **Input Symptoms**: Go to "Symptom Input" and describe how you're feeling
3. **Get Your Protocol**: Receive personalized healing recommendations
4. **Track Progress**: Log daily metrics and monitor your improvement

## 📱 Example User Flow

**Try this example:**
1. Go to "📝 Symptom Input"
2. Enter: "I feel bloated. I sleep badly. My skin looks dull. I get anxious for no reason and I can't focus after lunch."
3. Click "🔍 Analyze My Symptoms"
4. Review your personalized protocol
5. Go to "📋 My Protocol" to start tracking

## 🛠 Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Run on different port
streamlit run app.py --server.port 8502
```

**Python Version Issues:**
- RemedyOS works best with Python 3.9-3.13
- Avoid Python 3.8 if possible for better pandas compatibility

### Dependencies Not Installing

If you encounter build errors with pandas:
```bash
# Update pip first
pip install --upgrade pip

# Install with compatible versions
pip install "pandas>=2.2.0" "numpy>=1.26.0"
```

## 🎨 Customization

### Adding New Protocols
1. Edit `data/protocols.json`
2. Add new protocols following the existing structure
3. Restart the application

### Modifying UI
1. Edit CSS in `app.py` under the markdown section
2. Modify layout and styling as needed
3. Streamlit will hot-reload changes

## 📊 Data Storage

RemedyOS stores your data locally in browser session state:
- **Health metrics**: Stored during your session
- **Protocols**: Loaded from `data/protocols.json`
- **Progress tracking**: Maintained in session

For persistent storage across sessions, consider implementing database integration.

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py --server.port 8501
```

### Heroku Deployment
1. Use the included `Procfile`
2. Push to Heroku
3. Set environment variables if needed

### Docker (Coming Soon)
Docker configuration will be added in future releases.

## 💡 Tips for Best Experience

1. **Use Chrome/Firefox** for best compatibility
2. **Enable full-screen mode** for mobile-like experience
3. **Regular tracking** improves protocol effectiveness
4. **Try different symptoms** to explore various protocols

## 🆘 Getting Help

- **Issues**: Check the troubleshooting section above
- **Feature requests**: Consider contributing to the project
- **Questions**: Review the README.md for more details

## 🔄 Updates

To update RemedyOS:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**You're all set! Start your natural healing journey with RemedyOS.** 🌱

Remember: RemedyOS provides educational information only. Always consult healthcare providers for medical concerns.