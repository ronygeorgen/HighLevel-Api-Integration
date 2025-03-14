# HighLevel CRM API Integration Task

## Overview
This Django-based project demonstrates how to interact with the HighLevel CRM API to retrieve and update contact information. Specifically, it shows how to:
1. Fetch a random contact from the HighLevel contacts API
2. Update a specific custom field ("DFS Booking Zoom Link") with the value "TEST" for that contact

## Prerequisites
- Python 3.8+
- Django 4.0+
- Basic understanding of REST APIs and OAuth2 authentication

## Installation
```bash
# Clone the repository
git clone https://github.com/ronygeorgen/HighLevel-Api-Integration.git
cd HighlevelAPIIntegration

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration
Create a `.env` file in the project root directory with the following variables:
```
CLIENT_ID={value}
CLIENT_SECRET={value}
REDIRECT_URI=http:{value}
```

## Project Structure
```
highlevel_integration/
├── manage.py
├── requirements.txt
├── .env
├── highlevel_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manager/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
```

## Authentication
The project uses OAuth2 for authentication with HighLevel API. The process involves:
1. Obtaining an authorization code
2. Exchanging the code for an access token
3. Using the access token for API requests

## Usage
```bash
# Run the Django development server
python manage.py runserver

# Visit http://127.0.0.1:8000/ in your browser to start the OAuth flow
```

## Implementation Steps
1. Authenticate with HighLevel API using OAuth2
2. Fetch contacts using the `/contacts/` endpoint
3. Retrieve custom fields to find the ID for "DFS Booking Zoom Link"
4. Update the selected contact's custom field with the value "TEST"


## Key Dependencies
```
django==4.0.0
python-decouple==3.8
requests==2.27.1
urllib3==2.3.0
sqlparse==0.5.3
```

## Error Handling
The application includes proper error handling for:
- Authentication failures
- API rate limits
- Missing contacts or custom fields
- Network errors

## Troubleshooting
- Ensure your API credentials are correct
- Check that the redirect URI matches exactly what is configured in the HighLevel developer portal
- Verify network connectivity to the HighLevel API endpoints
- Check Django debug logs for detailed error messages
