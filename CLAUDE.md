# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CRM (Customer Relationship Management) System for the Chinese construction/consulting industry, built with FastAPI + Vue.js + PostgreSQL. The system manages company client information and professional talent information, with specialized certificate management for construction industry certifications.

## Development Commands

### Docker (Recommended)
```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# Stop services
docker-compose down

# Clean up all data including volumes
docker-compose down -v
```

### Development Mode
```bash
# Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Vue.js)
cd frontend
npm install
npm run dev        # Development server with hot reload
npm run build      # Production build
npm run preview    # Preview production build
```

### Testing & Tools
```bash
# API connectivity tests
cd tests && python test_frontend_api.py

# Certificate functionality tests
cd tests && python test_new_certificates.py

# End-to-end feature tests
cd tests && python test_final_features.py

# Certificate data analysis
cd tools && python analyze_certificates.py

# Smart Excel import with AI classification
cd tools && python smart_import.py [excel_file_path]
```

## Architecture Overview

### Backend Structure (FastAPI)
- **Entry point**: `backend/app/main.py`
- **API routes**: `backend/app/api/` - modular endpoints for companies, talents, communications, certificates
- **Database models**: `backend/app/models/` - SQLAlchemy models with relationships
- **Data validation**: `backend/app/schemas/` - Pydantic schemas for request/response validation
- **CRUD operations**: `backend/app/crud/` - database operation functions
- **Configuration**: `backend/app/core/config.py` - environment variables and app settings

### Frontend Structure (Vue.js 3)
- **Entry point**: `frontend/src/main.js`
- **Views**: `frontend/src/views/` - page components (Companies.vue, Talents.vue, Communications.vue, Certificates.vue)
- **API client**: `frontend/src/api/` - functions for backend communication
- **Router**: `frontend/src/router/` - Vue Router configuration
- **Components**: `frontend/src/components/` - reusable Vue components

### Database Schema
Core tables with automatic timestamps:
- **companies**: Client company information with A/B/C intention levels and certificate requirements
- **talents**: Professional talent information with certificates, contract prices, and intention levels
- **communications**: Interaction history linked to companies/talents
- **certificates**: Certificate management with intelligent classification

## Key Features & Patterns

### Certificate Intelligence System
The system includes AI-powered certificate classification for Chinese construction industry certifications:
- Automatic recognition of certificate levels (一级/二级建造师, 高级/中级/初级工程师)
- Professional field extraction (建筑工程, 市政工程, 机电工程, etc.)
- Social security status detection (唯一社保, 无社保, 转社保)
- Smart data import tools in `tools/smart_import.py`

### Intention Level Tracking
Both companies and talents use A/B/C classification system:
- **Level A**: High priority/hot leads
- **Level B**: Medium priority/warm leads
- **Level C**: Low priority/cold leads

### API Design Patterns
- RESTful endpoints with consistent patterns
- Pydantic validation for all inputs/outputs
- CORS configured for frontend-backend communication
- Auto-generated Swagger documentation at `/docs`
- Health check endpoint at `/health`

### Frontend Architecture
- Vue 3 Composition API with Element Plus UI components
- Vite dev server with proxy configuration to backend
- Component-based architecture with reusable elements
- Responsive design patterns

## Data Processing Tools

Located in `tools/` directory:
- **analyze_certificates.py**: Analyzes certificate data quality and classification accuracy
- **smart_import.py**: Intelligent Excel import with automatic certificate classification
- **data_import.py**: Basic Excel data import functionality

## Testing Strategy

Tests located in `tests/` directory:
- **test_frontend_api.py**: Validates frontend-backend connectivity via proxy
- **test_new_certificates.py**: Tests certificate recognition and classification
- **test_final_features.py**: End-to-end workflow testing

## Environment Configuration

Required services:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)
- Vue.js frontend dev server (port 3000/3001)

Key environment variables handled in `backend/app/core/config.py`:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT token secret

## Industry-Specific Logic

This CRM is tailored for Chinese construction industry with:
- Certificate expiry management for construction professionals
- Social insurance status tracking
- Contract price management for talent placement
- Communication history tracking for compliance
- Specialized certificate types common in Chinese construction market