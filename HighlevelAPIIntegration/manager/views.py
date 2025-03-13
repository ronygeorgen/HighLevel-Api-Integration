from django.http import JsonResponse
from django.shortcuts import redirect
import requests
import urllib.parse
from django.conf import settings



# Load environment variables 
CLIENT_ID = settings.GHL_CLIENT_ID
CLIENT_SECRET = settings.GHL_CLIENT_SECRET
REDIRECT_URI = settings.GHL_REDIRECT_URI
CALLBACK_URI = settings.GHL_CALLBACK_URI
LOCATION_ID = settings.GHL_LOCATION_ID
CUSTOM_FIELD_NAME = settings.GHL_CUSTOM_FIELD_NAME

# API endpoints
API_BASE_URL = settings.GHL_API_BASE_URL
AUTH_URL = settings.GHL_AUTH_URL
TOKEN_URL = settings.GHL_TOKEN_URL
DEFAULT_SCOPES = settings.GHL_DEFAULT_SCOPES


def auth_connect(request):

    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": DEFAULT_SCOPES
    }
    
    encoded_params = urllib.parse.urlencode(auth_params)
    auth_request_url = f"{AUTH_URL}?{encoded_params}"
    
    return redirect(auth_request_url)


def oauth_callback(request):

    authorization_code = request.GET.get("code")
    
    if not authorization_code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)

    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": CALLBACK_URI,
    }
    
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(TOKEN_URL, json=payload, headers=headers)
        
        if response.status_code != 200:
            response = requests.post(TOKEN_URL, data=payload)
        
        response.raise_for_status()
        response_data = response.json()
        
        # Store tokens in session
        request.session['access_token'] = response_data.get('access_token')
        request.session['refresh_token'] = response_data.get('refresh_token')
        request.session['location_id'] = response_data.get('locationId')
        
        return JsonResponse({
            "message": "Authentication successful",
            "access_token": response_data.get('access_token'),
            "location_id": response_data.get('locationId')
        })
            
    except requests.exceptions.HTTPError as e:
        error_detail = {}
        try:
            error_detail = response.json()
        except:
            error_detail = {"text": response.text}
            
        return JsonResponse({
            "error": f"Failed to obtain access token: {response.status_code}",
            "details": error_detail
        }, status=response.status_code)
        
    except Exception as e:
        return JsonResponse({"error": "Failed to obtain access token", "details": str(e)}, status=500)


def get_contacts(request):
    access_token = request.session.get('access_token')
    location_id = request.session.get('location_id', LOCATION_ID)

    if not access_token:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    url = f"{API_BASE_URL}/contacts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }

    try:
        response = requests.get(url, params={"locationId": location_id}, headers=headers)
        response.raise_for_status()

        contacts_data = response.json().get("contacts", [])
        if not contacts_data:
            return JsonResponse({"error": "No contacts found"}, status=404)

        formatted_contacts = [{"contact": contact} for contact in contacts_data]
        
        return JsonResponse(formatted_contacts, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": "Failed to fetch contacts", "details": str(e)}, status=500)
    

def update_contact(request, contact_id):

    ACCESS_TOKEN = request.session.get('access_token')
    
    if not ACCESS_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    custom_fields_url = f"{API_BASE_URL}/locations/{LOCATION_ID}/customFields"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Version": "2021-07-28"
    }
    
    try:
        custom_fields_response = requests.get(custom_fields_url, headers=headers)
        custom_fields_response.raise_for_status()
        custom_fields = custom_fields_response.json().get('customFields', [])
        
        field_id = None
        for field in custom_fields:
            if field.get('name') == CUSTOM_FIELD_NAME:
                field_id = field.get('id')
                break
        
        if not field_id:
            return JsonResponse({"error": f"Custom field '{CUSTOM_FIELD_NAME}' not found"}, status=404)
        
        field_value = request.GET.get('value', "TEST")
        
        update_url = f"{API_BASE_URL}/contacts/{contact_id}"
        
        data = {
            "customFields": [
                {
                    "id": field_id,
                    "value": field_value
                }
            ]
        }
        
        response = requests.put(update_url, json=data, headers=headers)
        
        verification_response = requests.get(update_url, headers=headers)
        verification_response.raise_for_status()
        contact_data = verification_response.json().get('contact', {})
        
        result = {
            "succeded": True, 
            "contact": contact_data, 
            "update_status_code": response.status_code,
            "current_contact_data": verification_response.json() 
        }
        
        return JsonResponse(result)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "succeeded": False,
            "error": str(e)
        }, status=500)
    except Exception as e:
        return JsonResponse({
            "succeeded": False,
            "error": str(e)
        }, status=500)