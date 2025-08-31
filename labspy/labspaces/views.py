from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.urls import resolve

from .models import Lab, LabMembership
from .forms import LabCreationForm, LabJoinForm

def is_lab_admin(user, lab_code):
    """
    Check if a user is an admin (owner) of a specific lab.
    
    Args:
        user: The user to check
        lab_code: The lab code to check against
        
    Returns:
        bool: True if user is admin, False otherwise
    """
    try:
        lab = Lab.objects.get(code=lab_code)
        return LabMembership.objects.filter(
            lab=lab, 
            user=user, 
            role='owner'
        ).exists()
    except Lab.DoesNotExist:
        return False

def is_lab_member(user, lab_code):
    try:
        lab = Lab.objects.get(code=lab_code)
        return LabMembership.objects.filter(
            lab=lab, 
            user=user, 
            role__in=['owner', 'admin', 'member']
        ).exists()
    except Lab.DoesNotExist:
        return False

# Create your views here.
@login_required
def home(request):
    # Get labs where user is owner or member (exclude pending)
    user_labs_qs = Lab.objects.filter(
        labmembership__user=request.user,
        labmembership__role__in=["owner", "member"]
    ).distinct()
    user_labs = list(user_labs_qs)

    # Get labs where user is pending
    pending_labs_qs = Lab.objects.filter(
        labmembership__user=request.user,
        labmembership__role="pending"
    ).distinct()
    pending_labs = list(pending_labs_qs)

    form = LabJoinForm()
    print(f"User labs: {user_labs}")
    print(f"Pending labs: {pending_labs}")
    return render(
        request,
        'labspaces/home.html',
        {
            "user_labs": user_labs,
            "pending_labs": pending_labs,
            "join_form": form
        }
    )

@login_required
def lab_create(request):
    if request.method == 'POST':
        form = LabCreationForm(request.POST)
        if form.is_valid():
            form.save()
            LabMembership.objects.create(
                lab=form.instance,
                user=request.user,
                role='owner'
            )
            return redirect('labspaces:labspace_view', code=form.instance.code)
    else:
        form = LabCreationForm()
    return render(request, 'labspaces/create-labspace.html', {'form': form})

@login_required
def labspace_view(request, code):
    try:
        labspace = Lab.objects.get(code=code)
    except Lab.DoesNotExist:
        raise Http404("Not found")

    # Check if the user is a member of the lab
    is_member = LabMembership.objects.filter(
        lab=labspace,
        user=request.user,
        role__in=['owner', 'manager', 'researcher', 'guest', 'member']
    ).exists()

    is_pending = LabMembership.objects.filter(
        lab=labspace,
        user=request.user,
        role = 'pending'
    ).exists()

    # Optionally, you could restrict access to only members
    if not is_member:
        if is_pending:
            return HttpResponseForbidden("Your request to join this labspace is still pending, please wait for the labspace admin's approval.")
        return HttpResponseForbidden("Access Denied.")

    # Determine if the user is an admin/owner
    user_is_admin = LabMembership.objects.filter(
        lab=labspace,
        user=request.user,
        role__in=['owner', 'admin']
    ).exists()

    # Check if there are pending requests for this lab (for admin sidebar icon)
    has_pending_requests = LabMembership.objects.filter(
        lab=labspace,
        role='pending'
    ).exists()

    context = {
        'labspace': labspace,
        'current_lab': labspace,
        'user_is_admin': user_is_admin,
        'has_pending_requests': has_pending_requests,
    }
    return render(request, 'labspaces/lab_index.html', context)

@login_required
@require_POST
def lab_join(request):
    if request.method == "POST":
        form = LabJoinForm(request.POST)
        try:
            if form.is_valid():
                lab_code = form.cleaned_data["code"]
            else:
                return redirect('labspaces:home')
            lab = Lab.objects.get(code=lab_code)
            LabMembership.objects.create(
                lab=lab,
                user=request.user,
                role='pending'
            )
            print(f"LAB: {lab_code}")
            return redirect('labspaces:home')
        except Lab.DoesNotExist:
            return redirect('labspaces:home')
    else:
        return HttpResponseNotAllowed("Invalid request method")

@login_required
def pending_requests(request, code):
    if not is_lab_admin(request.user, code):
        return HttpResponseForbidden("You are not authorized to view this page")
    try:
        labspace = Lab.objects.get(code=code)
        pending_requests = LabMembership.objects.filter(lab=labspace, role='pending')
        return render(request, 'labspaces/admin-pending-requests.html', {
            'pending_requests': pending_requests,
            'labspace': labspace
        })
    except Lab.DoesNotExist:
        raise Http404("Lab not found")

@login_required
@require_POST
def accept_request(request):
    try:
        request_id = request.POST.get('request_id')
        membership_request = LabMembership.objects.get(id=request_id)
        labspace = membership_request.lab
        code = labspace.code
        if is_lab_admin(request.user, code):
            membership_request.role = 'member'
            membership_request.save()
            return redirect('labspaces:pending_requests', code=code)
        else:
            return HttpResponseForbidden("You do not have permission to perform this action.")
    except LabMembership.DoesNotExist:
        raise Http404("Request not found")

@login_required
@require_POST
def reject_request(request):
    try:
        request_id = request.POST.get('request_id')
        membership_request = LabMembership.objects.get(id=request_id)
        labspace = membership_request.lab
        code = labspace.code
        if is_lab_admin(request.user, code):
            membership_request.delete()
            return redirect('labspaces:pending_requests', code=code)
        else:
            return HttpResponseForbidden("You do not have permission to perform this action.")
    except LabMembership.DoesNotExist:
        raise Http404("Request not found")

@login_required
def user_pending_labs(request):
    pending_labs = Lab.objects.filter(
        labmembership__user=request.user, 
        labmembership__role='pending'
        ).distinct()
    return render(request, 'labspaces/user_pending_labs.html', {'pending_labs': pending_labs})

@login_required
def manage_members(request, code):
    # Check if the user is an owner of the lab
    if not is_lab_admin(request.user, code):
        return HttpResponseForbidden("You are not authorized to view this page")
    
    try:
        labspace = Lab.objects.get(code=code)
        # Get all members of the lab (excluding pending requests)
        lab_members = LabMembership.objects.filter(
            lab=labspace, 
            role__in=['owner', 'admin', 'member', 'manager', 'researcher', 'guest']
        ).select_related('user').order_by('role', 'user__username')


        
        return render(request, 'labspaces/manage_members.html', {
            'labspace': labspace,
            'lab_members': lab_members
        })
    except Lab.DoesNotExist:
        raise Http404("Lab not found")

@login_required
@require_POST
def remove_member(request, code):
    # Check if the user is an owner of the lab
    if not is_lab_admin(request.user, code):
        return HttpResponseForbidden("You are not authorized to perform this action")
    
    try:
        labspace = Lab.objects.get(code=code)
        member_id = request.POST.get('member_id')
        
        if not member_id:
            return HttpResponseForbidden("Member ID is required")
        
        # Get the membership to remove
        membership = LabMembership.objects.get(id=member_id, lab=labspace)
        
        # Prevent removing the last owner
        if membership.role == 'owner':
            owner_count = LabMembership.objects.filter(lab=labspace, role='owner').count()
            if owner_count <= 1:
                return HttpResponseForbidden("Cannot remove the last owner of the lab")
        
        # Remove the membership
        membership.delete()
        
        return redirect('labspaces:manage_members', code=code)
        
    except Lab.DoesNotExist:
        raise Http404("Lab not found")
    except LabMembership.DoesNotExist:
        raise Http404("Member not found")