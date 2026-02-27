def theme_context(request):
    return {
        'current_theme': request.session.get('theme', 'light')
    }