from rest_framework import permissions


class CompanyPermission(permissions.BasePermission):
    """
    Custom permission to ensure users can only access data where companyId matches their own company.
    Admin roles have broader access.
    """
    
    def has_permission(self, request, view):
        # Allow read/write for authenticated users
        if not request.user or not request.user.is_authenticated:
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        # Check if user has admin role
        if hasattr(request.user, 'user_roles'):
            user_roles = request.user.user_roles.all()
            for user_role in user_roles:
                if user_role.role.title.lower() == 'admin':
                    return True
        
        # For non-admin users, check companyId match
        if hasattr(obj, 'company'):
            return obj.company_id == request.user.company_id
        elif hasattr(obj, 'companyId'):
            return obj.companyId == request.user.company_id
        elif hasattr(obj, 'user'):
            # For user-related objects, check if it's the same user or same company
            if obj.user.company_id == request.user.company_id:
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

