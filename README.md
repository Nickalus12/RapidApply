# 🚀 RapidApply - AI-Powered LinkedIn Job Application Automation

<div align="center">

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Nickalus12/RapidApply/pulls)
[![Discord](https://img.shields.io/badge/Discord-Join%20Community-7289DA)](https://discord.com/users/nickalus)

**Automate your LinkedIn job search with AI-powered precision. Apply to 100+ jobs in under an hour.**

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Configuration](#-configuration) • [Contributing](#-contributing) • [Support](#-support)

</div>

---

## 🎯 What is RapidApply?

RapidApply is an advanced automation tool that revolutionizes the job application process on LinkedIn. Using intelligent web scraping and AI capabilities, it automatically searches for relevant positions, customizes your applications, and submits them - all while you focus on interview preparation.

### 🏆 Key Benefits

- **⚡ Lightning Fast**: Apply to 100+ jobs in less than 60 minutes
- **🎯 Smart Targeting**: AI-powered job matching based on your preferences
- **📝 Dynamic Resumes**: Automatically tailors your resume for each position
- **🤖 Intelligent Responses**: Answers application questions using AI
- **📊 Application Tracking**: Comprehensive logs and analytics
- **🔒 Stealth Mode**: Advanced anti-detection mechanisms

## 📽️ See RapidApply in Action

<div align="center">
  <a href="https://youtu.be/gMbB1fWZDHw">
    <img src="https://img.youtube.com/vi/gMbB1fWZDHw/maxresdefault.jpg" alt="RapidApply Demo Video" width="600">
  </a>
  <br>
  <em>Click to watch the full demo on YouTube</em>
</div>

## ✨ Features

### 🚀 Core Automation
- **Smart Job Search**: Configurable filters for location, salary, experience level, and more
- **Auto-Apply**: One-click applications with intelligent form filling
- **Question Answering**: AI-powered responses to application questions
- **Resume Customization**: Dynamic resume generation based on job requirements
- **Multi-Profile Support**: Manage multiple LinkedIn accounts seamlessly

### 🛡️ Advanced Capabilities
- **Stealth Mode**: Undetected ChromeDriver with human-like behavior simulation
- **Error Recovery**: Intelligent retry mechanisms and fallback strategies
- **Batch Processing**: Queue multiple searches and run overnight
- **External Applications**: Collects links for applications outside LinkedIn
- **Blacklist Management**: Skip companies or positions with specific keywords

### 📊 Analytics & Tracking
- **Application History**: Detailed logs of all applications
- **Success Metrics**: Track application success rates
- **Skills Analysis**: Identify in-demand skills from job postings
- **Export Reports**: Generate CSV/Excel reports for analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Google Chrome (latest version)
- LinkedIn account
- (Optional) OpenAI API key for AI features

### 30-Second Setup

```bash
# Clone the repository
git clone https://github.com/Nickalus12/RapidApply.git
cd RapidApply

# Run the setup script
# For Windows:
./setup/windows-setup.bat

# For Linux/Mac:
./setup/setup.sh

# Start applying!
python runAiBot.py
```

## 📋 Installation

### Detailed Installation Steps

1. **Install Python 3.10+**
   ```bash
   # Windows: Download from python.org or Microsoft Store
   # Linux: sudo apt install python3.10
   # Mac: brew install python@3.10
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Chrome & ChromeDriver**
   - Download [Google Chrome](https://www.google.com/chrome)
   - ChromeDriver installs automatically with setup scripts

4. **Clone RapidApply**
   ```bash
   git clone https://github.com/Nickalus12/RapidApply.git
   cd RapidApply
   ```

## ⚙️ Configuration

### 1. Personal Information (`config/personals.py`)
Configure your personal details for applications:
```python
name = "Your Name"
phone = "+1234567890"
email = "your.email@example.com"
linkedin = "https://linkedin.com/in/yourprofile"
```

### 2. Search Preferences (`config/search.py`)
Define your job search criteria:
```python
keywords = ["Software Engineer", "Python Developer"]
location = "United States"
experience_level = ["Entry level", "Associate"]
job_type = ["Full-time", "Contract"]
```

### 3. Application Settings (`config/questions.py`)
Configure application behavior:
```python
pause_before_submit = True  # Review before submitting
save_screenshots = True     # Debug failed applications
use_ai_answers = True      # Enable AI for questions
```

### 4. AI Configuration (`config/secrets.py`)
Add your API keys (optional):
```python
openai_api_key = "your-api-key-here"
linkedin_email = "your-email@example.com"
linkedin_password = "your-password"
```

## 🏗️ Enterprise Architecture

### Branch Structure
```
main           → Production-ready code
├── develop    → Integration branch
├── feature/*  → New features
├── hotfix/*   → Emergency fixes
└── release/*  → Release preparation
```

### Version Control
- Semantic Versioning (MAJOR.MINOR.PATCH)
- Automated changelog generation
- Tagged releases with binaries

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Guide
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request to `develop` branch

## 📊 Roadmap

### 🎯 Current Focus
- [ ] Multi-language support
- [ ] Chrome extension version
- [ ] Indeed.com integration
- [ ] Advanced AI resume builder

### 🔮 Future Plans
- [ ] Mobile app for monitoring
- [ ] Cloud-based execution
- [ ] Integration with more job platforms
- [ ] Machine learning for success prediction

## 🆘 Support

### Community Support
- **Discord**: Connect with me at **Nickalus** on Discord
- **GitHub Issues**: [Report bugs or request features](https://github.com/Nickalus12/RapidApply/issues)
- **Discussions**: [Join the conversation](https://github.com/Nickalus12/RapidApply/discussions)

### Documentation
- [User Guide](https://github.com/Nickalus12/RapidApply/wiki)
- [API Reference](https://github.com/Nickalus12/RapidApply/wiki/API-Reference)
- [Troubleshooting](https://github.com/Nickalus12/RapidApply/wiki/Troubleshooting)

## 🏆 Success Stories

> "RapidApply helped me land my dream job! Applied to 500+ positions in a week and got 50+ interviews." - *Software Developer*

> "The AI resume customization feature is a game-changer. My response rate increased by 300%!" - *Data Scientist*

## 📜 Credits & Acknowledgments

This project is based on the original work from [Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn) by GodsScion. We've enhanced and rebranded it as RapidApply with significant improvements in AI integration, user experience, and automation capabilities.

## ⚖️ License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🛡️ Disclaimer

**Educational Purpose Only**: This tool is designed for educational and personal use. Users are responsible for complying with LinkedIn's Terms of Service and all applicable laws. Use at your own risk.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Nickalus12/RapidApply&type=Date)](https://star-history.com/#Nickalus12/RapidApply&Date)

---

<div align="center">
  <h3>Built with ❤️ by the RapidApply Community</h3>
  <p>If RapidApply helps you land your dream job, give us a ⭐!</p>
</div>