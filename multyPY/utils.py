from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def is_teacher(user):
    """Check if user is a teacher"""
    return user.is_authenticated and user.groups.filter(name='teacher').exists()

def is_student(user):
    """Check if user is a student"""
    return user.is_authenticated and user.groups.filter(name='student').exists()

def teacher_required(view_func):
    """Decorator to require teacher role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_teacher(request.user):
            logger.warning(f"Non-teacher user {request.user.username} attempted to access teacher view")
            raise PermissionDenied("Teacher access required")
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)

def student_required(view_func):
    """Decorator to require student role"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_student(request.user):
            logger.warning(f"Non-student user {request.user.username} attempted to access student view")
            raise PermissionDenied("Student access required")
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)

def exam_permission_required(base_number):
    """Decorator to check specific exam permissions"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            permission_name = f'multyPY.canExamBase_number{base_number}'
            if not request.user.has_perm(permission_name):
                logger.info(f"User {request.user.username} lacks permission for exam {base_number}")
                raise PermissionDenied(f"Permission required for table {base_number}")
            return view_func(request, *args, **kwargs)
        return login_required(wrapper)
    return decorator

def safe_int(value, default=0):
    """Safely convert value to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def validate_multiplication_range(base_number, multiplier):
    """Validate that base_number and multiplier are in valid range"""
    if not (1 <= base_number <= 12):
        raise ValueError(f"Base number {base_number} must be between 1 and 12")
    if not (1 <= multiplier <= 12):
        raise ValueError(f"Multiplier {multiplier} must be between 1 and 12")
    return True

def log_user_action(action, user, details=None):
    """Log user actions for auditing"""
    log_message = f"User {user.username} performed action: {action}"
    if details:
        log_message += f" - Details: {details}"
    logger.info(log_message)
