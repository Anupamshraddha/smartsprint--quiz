
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import login

from .forms import EmailForm, OTPVerificationForm, SetNewPasswordForm
from .models import PasswordResetOTP
from .utils import create_otp_for_user, validate_otp

def request_reset(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # Generate and save OTP
            otp_obj = create_otp_for_user(user)
            
            # Store user_id in session for the next steps
            request.session['reset_user_id'] = user.id
            
            # Redirect to display OTP
            return redirect('display_otp')
    else:
        form = EmailForm()
    
    return render(request, 'request_reset.html', {'form': form})

def display_otp(request):
    # Check if we have user_id in session
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please start the password reset process again.")
        return redirect('request_reset')
    
    try:
        user = User.objects.get(id=user_id)
        otp_obj = PasswordResetOTP.objects.filter(user=user, is_used=False).order_by('-created_at').first()
        
        if not otp_obj or otp_obj.is_expired:
            messages.error(request, "OTP has expired. Please request a new one.")
            return redirect('request_reset')
            
        # Show the OTP to the user
        return render(request, 'display_otp.html', {
            'otp': otp_obj.otp,
            'expires_at': otp_obj.expires_at
        })
        
    except User.DoesNotExist:
        messages.error(request, "User not found. Please try again.")
        return redirect('request_reset')

def verify_otp(request):
    # Check if we have user_id in session
    user_id = request.session.get('reset_user_id')
    if not user_id:
        messages.error(request, "Session expired. Please start the password reset process again.")
        return redirect('request_reset')
    
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            form = OTPVerificationForm(request.POST)
            if form.is_valid():
                otp_value = form.cleaned_data['otp']
                is_valid, result = validate_otp(user, otp_value)
                
                if is_valid:
                    # Mark OTP as used
                    otp_obj = result
                    otp_obj.is_used = True
                    otp_obj.save()
                    
                    # Allow user to reset password
                    request.session['otp_verified'] = True
                    return redirect('reset_password')
                else:
                    messages.error(request, result)
        else:
            form = OTPVerificationForm()
        
        return render(request, 'verify_otp.html', {'form': form})
        
    except User.DoesNotExist:
        messages.error(request, "User not found. Please try again.")
        return redirect('request_reset')

def reset_password(request):
    # Check if user is verified with OTP
    user_id = request.session.get('reset_user_id')
    otp_verified = request.session.get('otp_verified', False)
    
    if not user_id or not otp_verified:
        messages.error(request, "OTP verification required. Please start the password reset process again.")
        return redirect('request_reset')
        
    try:
        user = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                
                # Clear session data
                del request.session['reset_user_id']
                del request.session['otp_verified']
                
                messages.success(request, "Your password has been successfully reset.")
                return redirect('reset_success')
        else:
            form = SetNewPasswordForm(user)
            
        return render(request, 'reset_password.html', {'form': form})
        
    except User.DoesNotExist:
        messages.error(request, "User not found. Please try again.")
        return redirect('request_reset')

def reset_success(request):
    return render(request, 'reset_success.html')