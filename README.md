# Agricultural  Supply Chain Backend API

A FastAPI-based backend service for managing agricultural supply chain operations with a focus on medicinal plants and Ayurvedic products.

## Overview

This backend service provides REST APIs to handle:
- User registration and profile management across multiple roles (Farmers, Processors, Labs, etc.)
- Supply chain transaction tracking
- Validation of medicinal plant harvesting and processing
- Integration with MongoDB for data persistence
- FHIR-compliant data structures
- QR code-based batch tracking

## System Requirements

- Python 3.8+
- MongoDB
- Environment variables configured

## Installation

1. Clone the repository:
```sh
git clone https://github.com/herbtrace/backend.git
cd backend
```

2. Create and activate virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```sh
MONGO_URI=your_mongodb_connection_string
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Project dependencies
├── validation.json      # Medicinal plant validation rules
├── models/             
│   ├── signup.py       # User profile models
│   └── stages.py       # Supply chain stage models
└── routes/
    ├── profile.py      # User profile management endpoints
    └── transaction.py  # Supply chain transaction endpoints
```

## API Endpoints

### Profile Management (`/profiles`)

- `POST /profiles/create` - Create new user profile
- `POST /profiles/login` - SCM admin login
- `GET /profiles/get` - Get all profiles
- `GET /profiles/user_login` - User login via profile ID
- `GET /profiles/check_if_user_exists` - Check profile existence

### Transaction Management

- `POST /start` - Initialize crop transaction
- `GET /get` - Retrieve profile data
- `POST /transactions` - Process supply chain transaction

## Data Models

### User Roles
- Farmer
- Wild Collector
- Processor
- Laboratory
- Manufacturer
- Packer
- Storage

### Transaction Events
- Collection Event
- Transport Event
- Processing Event
- Quality Test
- Manufacturing Event
- Packing Event

## Validation System

The system includes validation rules for medicinal plants (`validation.json`) covering:
- Approved collection regions
- Harvesting seasons
- Quality parameters
- Processing requirements
- Sustainability guidelines

## Running the Application

1. Start the FastAPI server:
```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

- **Role-based Access Control**: Different user roles with specific permissions
- **Supply Chain Tracking**: Complete tracking of medicinal plants from collection to packaging
- **Data Validation**: Comprehensive validation rules for medicinal plant processing
- **FHIR Compliance**: Healthcare data standard compatibility
- **QR Code Integration**: Batch tracking through QR codes
- **MongoDB Integration**: Scalable data storage solution

## Security Features

- CORS enabled
- Authentication tokens
- Role-based access control
- Secure password handling
- Input validation

## Error Handling

The API implements proper error handling with appropriate HTTP status codes and error messages for:
- Invalid requests
- Authentication failures
- Database errors
- Validation failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request
