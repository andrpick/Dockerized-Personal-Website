# Personal Website Showcase (Flask Version)

A responsive, multi-page personal website built with Flask, HTML, CSS, and JavaScript, demonstrating modern web development practices, Docker containerization, and comprehensive testing with AI-assisted development.

## Project Overview

This website serves as a comprehensive portfolio showcasing skills, experience, and projects in the field of Information Systems. Built as part of Assignment 6 for the MSIS program at Indiana University. The site now runs on Flask for local development and easy templating.

## Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Multi-page Navigation**: Home, About, Resume, Projects, and Contact pages
- **Interactive Contact Form**: Complete with validation and thank you page
- **Database-Driven Projects**: SQLite database with CRUD operations for project management
- **Docker Containerization**: Full Docker support for development and production
- **Comprehensive Testing**: 55+ pytest tests with 93% success rate
- **Modern Styling**: Gradient backgrounds, card layouts, and smooth animations
- **Accessibility**: Semantic HTML5 elements and proper form labels
- **AI Documentation**: Detailed logging of AI-assisted development process

## File Structure

```
├── app.py                    # Flask application entrypoint
├── DAL.py                    # Database access layer
├── requirements.txt          # Python dependencies
├── projects.db              # SQLite database
├── test_app.py              # Flask application tests
├── test_database.py         # Database layer tests
├── conftest.py              # Test configuration
├── pytest.ini              # Pytest settings
├── Dockerfile               # Container definition
├── docker-compose.yml       # Development setup
├── docker-compose.prod.yml  # Production setup
├── nginx.conf               # Reverse proxy config
├── .dockerignore            # Build optimization
├── .gitignore               # Git exclusions
├── DOCKER.md                # Docker documentation
├── templates/               # Jinja templates
│   ├── index.html
│   ├── about.html
│   ├── resume.html
│   ├── projects.html
│   ├── contact.html
│   ├── add_project.html
│   ├── edit_project.html
│   └── thankyou.html
├── static/                  # Static assets
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       ├── al28281_A1101360-a.jpg
│       ├── movers.jpg
│       ├── Revenue.jpg
│       ├── totals.jpg
│       └── waste.jpg
├── .prompt/                 # AI development documentation
│   └── dev_notes.md
└── README.md               # Project documentation
```

## Technical Implementation

### HTML5 Semantic Elements
- `<header>` for site navigation
- `<nav>` for menu structure
- `<main>` for primary content
- `<footer>` for site information
- Proper form labels and accessibility attributes

### CSS Features
- CSS Grid and Flexbox for responsive layouts
- CSS custom properties for consistent theming
- Mobile-first responsive design
- Smooth transitions and hover effects
- Gradient backgrounds and modern styling

### JavaScript Functionality
- Image modal system for project screenshots
- Scroll-to-top button functionality
- Sticky header with shadow effects
- Smooth animations and transitions

## AI-Assisted Development

This project demonstrates the effective use of AI tools (GitHub Copilot/Cursor) in modern web development:

- **Scaffolding**: AI generated initial HTML structure and CSS layouts
- **Complex Logic**: AI assisted with JavaScript form validation
- **Responsive Design**: AI provided mobile-first CSS frameworks
- **Human Oversight**: Manual customization and content personalization

## Browser Compatibility

Tested and validated in:
- Chrome (latest)
- Firefox (latest)
- Edge (latest)
- Safari (latest)

## Getting Started

### Option 1: Using Docker (Recommended)

1. **Prerequisites**: Install Docker and Docker Compose
2. **Build and run**:
   ```bash
   docker-compose up --build
   ```
3. **Access the website**: Open `http://localhost:5000` in your browser
4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Local Flask Development

1. Clone or download the project files
2. (Optional) Create and activate a virtual environment
   - Windows (PowerShell): `python -m venv .venv && .\.venv\Scripts\Activate.ps1`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python app.py`
5. Open `http://127.0.0.1:5000` in your browser

### Testing

Run the comprehensive test suite:
```bash
# Run all tests
python -m pytest -v

# Run with coverage
python -m pytest --cov=app --cov=DAL --cov-report=term-missing

# Run specific test files
python -m pytest test_database.py -v
python -m pytest test_app.py -v
```

### Docker Production Deployment

For production deployment with nginx reverse proxy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```
Access at `http://localhost` (port 80)

## Assignment Requirements Met

✅ **Content Quality (20%)**: Comprehensive biography, resume, projects, and contact information  
✅ **Design & Layout (20%)**: Consistent styling, responsiveness, and accessibility  
✅ **Technical Correctness (20%)**: Valid HTML/CSS, working navigation, functional form  
✅ **AI Documentation (20%)**: Complete .prompt/dev_notes.md with prompts and reflection  
✅ **Professionalism (20%)**: Clean organization and attention to detail  

## Current Features

- Professional headshot and dashboard screenshots integrated
- Interactive image gallery with modal functionality
- Database-driven project management with CRUD operations
- Comprehensive test suite (55+ tests, 93% success rate)
- Docker containerization for development and production
- Responsive design optimized for all devices
- Modern UI with glassmorphism effects and animations
- Complete AI development documentation

## Future Enhancements

- Implement backend form processing
- Add more interactive features
- Optimize for performance
- Add dark mode toggle

## Contact

For questions about this project or collaboration opportunities, please use the contact form on the website.

---

*Built with HTML, CSS, JavaScript, and AI assistance*  
*Assignment 5 - MSIS Program, Indiana University*
