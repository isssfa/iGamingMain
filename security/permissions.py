from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import APICSRFToken
from .utils import get_client_ip, validate_origin, rate_limit_check


class PublicReadOnly(permissions.BasePermission):
    """
    Allow public read access (GET, HEAD, OPTIONS) but require authentication for writes.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class ProtectedPostPermission(permissions.BasePermission):
    """
    Permission class for POST endpoints that require CSRF token validation
    and rate limiting instead of API token authentication.
    """
    
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS without restrictions
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For POST/PUT/PATCH/DELETE, require CSRF token
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Get CSRF token from header or data
            csrf_token = request.META.get('HTTP_X_CSRF_TOKEN') or request.data.get('csrf_token')
            
            if not csrf_token:
                raise PermissionDenied(
                    detail="CSRF token is required. Please obtain a token from /api/security/csrf-token/"
                )
            
            # Validate CSRF token
            ip_address = get_client_ip(request)
            is_valid, token_obj = APICSRFToken.validate_token(csrf_token, ip_address)
            
            if not is_valid:
                raise PermissionDenied(
                    detail="Invalid or expired CSRF token. Please obtain a new token."
                )
            
            # Validate origin (optional but recommended)
            if not validate_origin(request):
                raise PermissionDenied(
                    detail="Request origin is not allowed."
                )
            
            # Rate limiting check
            is_allowed, remaining, reset_time = rate_limit_check(
                request,
                rate=getattr(view, 'rate_limit', '10/m'),
                method=request.method
            )
            
            if not is_allowed:
                raise PermissionDenied(
                    detail=f"Rate limit exceeded. Please try again later."
                )
            
            # Store rate limit info in request for potential response headers
            request.rate_limit_remaining = remaining
            request.rate_limit_reset = reset_time
            
            return True
        
        return False

