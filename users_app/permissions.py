from rest_framework import permissions


class CompanyPermission(permissions.BasePermission):
    """
    Custom permission to ensure users can only access data where companyId matches their own company.
    Admin roles have broader access.
    Supports both JWT authentication (User objects) and ClientToken authentication (ClientPrincipal).
    """
    
    def has_permission(self, request, view):
        # Allow read/write for authenticated users
        if not request.user:
            return False
        
        # Check if authenticated (works for both User and ClientPrincipal)
        if not getattr(request.user, 'is_authenticated', False):
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        # Handle ClientToken authentication (ClientPrincipal)
        if hasattr(request, 'auth_company') and request.auth_company:
            # For client token auth, check if object belongs to the client's company
            if hasattr(obj, 'company'):
                return obj.company_id == request.auth_company.id
            elif hasattr(obj, 'companyId'):
                return obj.companyId == request.auth_company.id
            elif hasattr(obj, 'user'):
                # For user-related objects, check if user belongs to client's company
                return obj.user.company_id == request.auth_company.id
            return False
        
        # Handle JWT authentication (User objects)
        # Check if user has admin role
        if hasattr(request.user, 'user_roles'):
            user_roles = request.user.user_roles.all()
            for user_role in user_roles:
                if user_role.role.title.lower() == 'admin':
                    return True
        
        # For non-admin users, check companyId match
        user_company_id = getattr(request.user, 'company_id', None)
        if not user_company_id:
            return False
        
        if hasattr(obj, 'company'):
            return obj.company_id == user_company_id
        elif hasattr(obj, 'companyId'):
            return obj.companyId == user_company_id
        elif hasattr(obj, 'user'):
            # For user-related objects, check if it's the same user or same company
            if obj.user.company_id == user_company_id:
                return True
            return obj.user_id == request.user.id
        
        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows read-only access to all users,
    but write access only to admin users.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user has admin role
        if hasattr(request.user, 'user_roles'):
            user_roles = request.user.user_roles.all()
            for user_role in user_roles:
                if user_role.role.title.lower() == 'admin':
                    return True
        
        return False


def HasPermission(required_permission):
    """
    Permission class factory that checks if user has a specific permission.
    Permissions are read from JWT token claims to avoid database queries.
    
    Usage:
        permission_classes = [HasPermission('admin.write')]
    """
    
    class PermissionChecker(permissions.BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False
            
            # Try to get permissions from JWT token first (faster, no DB query)
            if hasattr(request, 'auth') and request.auth:
                token_permissions = request.auth.get('permissions', [])
                if required_permission in token_permissions:
                    return True
            
            # Fallback: Check permissions from user roles (database query)
            if hasattr(request.user, 'user_roles'):
                user_roles = request.user.user_roles.select_related('role').all()
                for user_role in user_roles:
                    role_title = user_role.role.title.lower()
                    if role_title == 'admin':
                        # Admin has all permissions
                        admin_permissions = ['admin.read', 'admin.write', 'admin.delete']
                        if required_permission in admin_permissions:
                            return True
                    # Add more role-based permission checks as needed
            
            return False
    
    return PermissionChecker

