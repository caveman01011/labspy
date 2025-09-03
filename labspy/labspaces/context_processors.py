from django.urls import resolve

from .models import Lab, LabMembership, Role
from .util import get_lab_code_from_url

def lab_admin_status(request):
    """
    Context processor to make user_is_admin status available globally.
    This checks if the current user is an admin of any lab they're viewing.
    """

    context = {'user_is_admin': False, 'current_lab': None}
    
    if request.user.is_authenticated:
        # Use Django's resolve to get URL parameters instead of parsing the path
        try:
            lab_code = get_lab_code_from_url(request)
            if lab_code != "":
                try:
                    lab = Lab.objects.get(code=lab_code)
                    # Check if user is admin of this lab
                    owner_role = Role.objects.get(name='Owner', is_default=True, lab__isnull=True)
                    is_admin = LabMembership.objects.filter(
                        lab=lab, 
                        user=request.user, 
                        role=owner_role
                    ).exists()
                    if is_admin:
                        context['user_is_admin'] = True
                        context['current_lab'] = lab
                except Lab.DoesNotExist:
                    pass
        except Exception as e:
            pass
    return context 

