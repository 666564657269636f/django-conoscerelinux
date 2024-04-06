from .models import StaticPage


def add_page_links_for_header(request):
    # TODO: filter to show only available or selected ones
    links = []
    for page in StaticPage.objects.all():
        links.append({"url": page.get_absolute_url(), "title": page.title})
    return {"links": links}
