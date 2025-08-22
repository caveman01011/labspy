from .models import Lab, LabMembership
from django.urls import resolve

def lab_admin_status(request):
    """
    Context processor to make user_is_admin status available globally.
    This checks if the current user is an admin of any lab they're viewing.
    """

    context = {'user_is_admin': False, 'current_lab': None}
    print("[lab_admin_status] Called for path:", request.path)
    
    if request.user.is_authenticated:
        print("[lab_admin_status] User is authenticated:", request.user)
        # Use Django's resolve to get URL parameters instead of parsing the path
        try:
            resolved = resolve(request.path)
            print("[lab_admin_status] Resolved URL name:", resolved.url_name)
            print("[lab_admin_status] Resolved kwargs:", resolved.kwargs)
            
            # Check if we're in a labspace context by looking for 'code' parameter
            if 'code' in resolved.kwargs:
                lab_code = resolved.kwargs['code']
                print("[lab_admin_status] Found lab code in URL:", lab_code)
                try:
                    lab = Lab.objects.get(code=lab_code)
                    print("[lab_admin_status] Lab found:", lab)
                    # Check if user is admin of this lab
                    is_admin = LabMembership.objects.filter(
                        lab=lab, 
                        user=request.user, 
                        role='owner'
                    ).exists()
                    print("[lab_admin_status] Is user admin of lab?", is_admin)
                    if is_admin:
                        context['user_is_admin'] = True
                        context['current_lab'] = lab
                except Lab.DoesNotExist:
                    print("[lab_admin_status] Lab with code", lab_code, "does not exist.")
        except Exception as e:
            print("[lab_admin_status] Exception during resolve or lab lookup:", e)
    
    print("[lab_admin_status] Returning context:", context)
    return context 