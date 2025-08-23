from django.url import resolve

def get_lab_code_from_url(request)
    lab_code = ""
    if user.is_authenticated:
        resolved = resolve(request.path)
                    # Check if we're in a labspace context by looking for 'code' parameter
                    if 'code' in resolved.kwargs:
                        lab_code = resolved.kwargs['code']
    return lab_code