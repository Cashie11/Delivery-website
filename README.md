# 🚚 SwiftTrack Delivery - Modern Package Tracking Platform

SwiftTrack is a premium, full-featured delivery tracking application built with **Django**. It provides an interactive experience for both senders and receivers, featuring real-time tracking, secure package verification, and a professional, mobile-first design.

![SwiftTrack Homepage](file:///home/cyber/.gemini/antigravity/brain/bc653ab1-195c-4864-b899-3e53fd79a064/homepage_hero_1766218838356.png)

## 🌟 Key Features

- **Interactive Dashboard** - Real-time monitoring of all sent and received packages with clickable statistics cards and filtered views.
- **Secure Verification System** - 6-digit verification codes generated per package, ensuring only the intended receiver can confirm delivery.
- **Sender-Led Tracking** - Senders can manually update package status and locations in real-time via a dedicated portal.
- **Visual Tracking History** - A professional timeline showing every step of the package journey, including locations and sender notes.
- **Modern UI/UX** - Dark theme with glassmorphism effects, smooth CSS transitions, and high-quality iconography.
- **Mobile Optimized** - Fully responsive design verified on mobile devices (iPhone/Android) for tracking on the go.

## 🛠 Tech Stack

- **Backend:** Django 5.1+, Python 3.10+
- **Frontend:** Vanilla HTML5, CSS3 (Glassmorphism), JavaScript
- **Database:** SQLite (Default), easily switchable to PostgreSQL
- **Design:** Custom-built design system with Google Fonts (Inter)

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/swifttrack.git
   cd swifttrack
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python3 manage.py migrate
   ```

4. **Load Sample Data (Optional but Recommended):**
   ```bash
   python3 manage.py create_sample_data
   ```

5. **Start Developer Server:**
   ```bash
   python3 manage.py runserver
   ```

6. **Access the App:**
   - Website: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin Detail: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 📱 Demos & Verification

### Interactive Dashboard
![Dashboard Demo](file:///home/cyber/.gemini/antigravity/brain/bc653ab1-195c-4864-b899-3e53fd79a064/dashboard_fix_final_verification_1766478560528.webp)
*Interactive filtering and tracking history timeline.*

### Mobile Experience
![Mobile Demo](file:///home/cyber/.gemini/antigravity/brain/bc653ab1-195c-4864-b899-3e53fd79a064/mobile_view_verification_final_1766346348920.webp)
*Fluid layout and optimized UI for mobile users.*

## 📄 Project Structure

```text
del/
├── accounts/           # User authentication and profiles
├── delivery/           # Core business logic (Packages, Events, Claims)
├── templates/          # Modern glassmorphism HTML templates
├── static/             # Global CSS/JS and media assets
├── swifttrack/         # Site configuration
└── manage.py           # Django CLI
```

## 🚀 Future Roadmap

- [ ] Automated Email/SMS Notifications
- [ ] Stripe/PayPal Integration for Shipping Fees
- [ ] Interactive Google Maps tracking
- [ ] REST API for mobile app integration

---
**SwiftTrack** is a portfolio-ready project demonstrating robust backend logic combined with premium frontend design! 🎉
