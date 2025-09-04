from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from django.urls import resolve
from django.db.models import Q

from .models import Lab, LabMembership, Role
from .forms import LabCreationForm, LabJoinForm, UserManagementSearchForm

#Role validation tests
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
        owner_role = Role.objects.get(name='owner', is_default=True, lab__isnull=True)
        manager_role = Role.objects.get(name='manager', is_default=True, lab__isnull=True)
        return LabMembership.objects.filter(
            lab=lab, 
            user=user, 
            role__in=[owner_role, manager_role]
        ).exists()
    except Lab.DoesNotExist:
        return False

def is_lab_member(user, lab_code):
    try:
        lab = Lab.objects.get(code=lab_code)
        return LabMembership.objects.filter(
            lab=lab, 
            user=user, 
            role__name__in=['owner', 'admin', 'member'],
            role__is_default=True
        ).exists()
    except Lab.DoesNotExist:
        return False

# Create your views here.
@login_required
def home(request):
    # Get labs where user is owner or member (exclude pending)
    user_labs_qs = Lab.objects.filter(
        labmembership__user=request.user,
        labmembership__role__name__in=["owner", "member"],
        labmembership__role__is_default=True
    ).distinct()
    user_labs = list(user_labs_qs)

    # Get labs where user is pending
    pending_labs_qs = Lab.objects.filter(
        labmembership__user=request.user,
        labmembership__role__name="pending",
        labmembership__role__is_default=True
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
                role=Role.objects.get(name='owner', is_default=True, lab__isnull=True)
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
        role__name__in=['owner', 'manager', 'researcher', 'guest', 'member'],
        role__is_default=True
    ).exists()

    is_pending = LabMembership.objects.filter(
        lab=labspace,
        user=request.user,
        role__name = 'pending',
        role__is_default=True
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
        role__name__in=['owner', 'admin'],
        role__is_default=True
    ).exists()

    # Check if there are pending requests for this lab (for admin sidebar icon)
    has_pending_requests = LabMembership.objects.filter(
        lab=labspace,
        role__name='pending',
        role__is_default=True
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
                role=Role.objects.get(name='pending', is_default=True, lab__isnull=True)
            )
            print(f"LAB: {lab_code}")
            return redirect('labspaces:home')
        except Lab.DoesNotExist:
            return redirect('labspaces:home')
    else:
        return HttpResponseNotAllowed("Invalid request method")

@login_required
@require_POST
def cancel_join_request(request):
    lab_id = request.POST.get("lab_id")
    if not lab_id:
        return HttpResponseNotAllowed("Lab ID not provided")
    try:
        lab = Lab.objects.get(id=lab_id)
    except Lab.DoesNotExist:
        raise Http404("Lab not found")
    try:
        lab_request = LabMembership.objects.get(
            user=request.user,
            lab=lab,
            role__name="pending",
            role__is_default=True
        )
        print(f"FOUND LAB REQUEST: {lab_request}")
        lab_request.delete()
        return redirect('labspaces:user_pending_labs')
    except LabMembership.DoesNotExist:
        raise Http404("Request not found")

@login_required
def pending_requests(request, code):
    if not is_lab_admin(request.user, code):
        return HttpResponseForbidden("You are not authorized to view this page")
    try:
        labspace = Lab.objects.get(code=code)
        pending_requests = LabMembership.objects.filter(lab=labspace, role__name='pending', role__is_default=True)
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
        member_role = Role.objects.get(name='member', is_default=True, lab__isnull=True)
        if is_lab_admin(request.user, code):
            membership_request.role = member_role
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
        labmembership__role__name='pending',
        labmembership__role__is_default=True
        ).distinct()
    return render(request, 'labspaces/user_pending_labs.html', {'pending_labs': pending_labs})

@login_required
def manage_members(request, code):
    # Check if the user is an owner of the lab
    if not is_lab_admin(request.user, code):
        return HttpResponseForbidden("You are not authorized to view this page")
    
    try:
        labspace = Lab.objects.get(code=code)
        
        # Initialize search form
        search_form = UserManagementSearchForm(request.GET)
        
        # Get all members of the lab (excluding pending requests)
        lab_members = LabMembership.objects.filter(
            lab=labspace, 
            role__name__in=['owner', 'member', 'manager', 'guest'],
            role__is_default=True
        ).select_related('user').order_by('role', 'user__username')
        
        # Apply search filters if form is valid
        if search_form.is_valid():
            username = search_form.cleaned_data.get('username')
            first_name = search_form.cleaned_data.get('first_name')
            last_name = search_form.cleaned_data.get('last_name')
            role = search_form.cleaned_data.get('role')
            
            # Build filter conditions
            if username:
                lab_members = lab_members.filter(user__username__icontains=username)
            if first_name:
                lab_members = lab_members.filter(user__first_name__icontains=first_name)
            if last_name:
                lab_members = lab_members.filter(user__last_name__icontains=last_name)
            if role:
                lab_members = lab_members.filter(role__name__iexact=role)
        
        return render(request, 'labspaces/manage_members.html', {
            'labspace': labspace,
            'lab_members': lab_members,
            'search_form': search_form
        })
    except Lab.DoesNotExist:
        raise Http404("Lab not found")

@login_required
@require_POST
def remove_member(request):
    # Get membership and resolve labspace
    member_id = request.POST.get('member_id')
    if not member_id:
        return HttpResponseForbidden("Member ID is required")
    try:
        membership = LabMembership.objects.select_related('lab').get(id=member_id)
        labspace = membership.lab
    except LabMembership.DoesNotExist:
        raise Http404("Member not found")

    # Check if the user is an owner/admin of the lab
    if not is_lab_admin(request.user, labspace.code):
        return HttpResponseForbidden("You are not authorized to perform this action")

    # Prevent removing the last owner
    owner_role = Role.objects.get(name='owner', is_default=True, lab__isnull=True)
    if membership.role == owner_role:
        owner_count = LabMembership.objects.filter(lab=labspace, role__name='owner').count()
        if owner_count <= 1:
            return HttpResponseForbidden("Cannot remove the last owner of the lab")

    # Remove the membership
    membership.delete()

    return redirect('labspaces:manage_members', code=labspace.code)

@login_required
def manage_permissions(request, code):
    if not is_lab_admin(request.user, code):
        return HttpResponseForbidden("Access denied")
    roles = Role.objects.filter(Q(lab__code=code) | (Q(is_default=True) & Q(lab__isnull=True)))
    roles_with_members = []
    for role in roles:
        members = LabMembership.objects.filter(lab__code=code, role=role).select_related('user')
        roles_with_members.append({
            'role': role,
            'members': members
        })
    context = {
        'roles_with_members': roles_with_members,
        'labspace': Lab.objects.get(code=code),
        'all_roles': roles,
    }
    print(f"ROLES FOUND: {roles}")
    print(f"MEMBERS FOUND: {roles_with_members}")
    return render(request, "labspaces/manage_permissions.html", context)

@login_required
@require_POST
def change_role(request):
    membership_id = request.POST.get('membership_id')
    new_role_name = request.POST.get('new_role')
    if not membership_id or not new_role_name:
        return HttpResponseNotAllowed("Missing parameters")

    # Resolve membership and lab
    try:
        membership = LabMembership.objects.select_related('lab').get(id=membership_id)
        lab = membership.lab
    except LabMembership.DoesNotExist:
        raise Http404("Membership not found")

    # Permission check
    if not is_lab_admin(request.user, lab.code):
        return HttpResponseForbidden("You are not authorized to perform this action")

    # Resolve the new role (either default-global or lab-specific)
    try:
        new_role = Role.objects.get(
            Q(name=new_role_name) & (Q(is_default=True, lab__isnull=True) | Q(lab=lab))
        )
    except Role.DoesNotExist:
        raise Http404("Role not found")

    # Prevent removing the last owner by demoting the only owner
    owner_role = Role.objects.get(name='owner', is_default=True, lab__isnull=True)
    if membership.role == owner_role and new_role != owner_role:
        owner_count = LabMembership.objects.filter(lab=lab, role=owner_role).count()
        if owner_count <= 1:
            from django.contrib import messages
            messages.error(request, "Cannot change role of the last owner of the lab")
            return redirect('labspaces:manage_permissions', code=lab.code)

    membership.role = new_role
    membership.save()
    return redirect('labspaces:manage_permissions', code=lab.code)