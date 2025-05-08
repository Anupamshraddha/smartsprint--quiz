import random
import string
from django.utils import timezone
from .models import PasswordResetOTP

def generate_otp(length=6):
    """Generate a random numeric OTP of specified length."""
    return ''.join(random.choices(string.digits, k=length))

def create_otp_for_user(user):
    """Create a new OTP for the user."""
    # Invalidate any existing OTPs
    PasswordResetOTP.objects.filter(user=user, is_used=False).update(is_used=True)
    
    # Create new OTP
    otp = generate_otp()
    otp_obj = PasswordResetOTP.objects.create(
        user=user,
        otp=otp
    )
    
    return otp_obj

def validate_otp(user, otp_value):
    """Validate the OTP for the user."""
    try:
        otp_obj = PasswordResetOTP.objects.get(
            user=user,
            otp=otp_value,
            is_used=False
        )
        
        if otp_obj.is_expired:
            return False, "OTP has expired. Please request a new one."
        
        return True, otp_obj
    
    except PasswordResetOTP.DoesNotExist:
        return False, "Invalid OTP. Please try again."