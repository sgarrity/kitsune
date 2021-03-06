import urllib

from django.core import paginator
from django.utils.encoding import smart_str

import jinja2

from .parser import WikiParser


def paginate(request, queryset, per_page=20):
    """Get a Paginator, abstracting some common paging actions."""
    p = paginator.Paginator(queryset, per_page)

    # Get the page from the request, make sure it's an int.
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    # Get a page of results, or the first page if there's a problem.
    try:
        paginated = p.page(page)
    except (paginator.EmptyPage, paginator.InvalidPage):
        paginated = p.page(1)

    base = request.build_absolute_uri(request.path)

    items = [(k, v) for k in request.GET if k != 'page'
             for v in request.GET.getlist(k) if v]

    qsa = urlencode(items)

    paginated.url = u'%s?%s' % (base, qsa)
    return paginated


def urlencode(items):
    """A Unicode-safe URLencoder."""

    try:
        return urllib.urlencode(items)
    except UnicodeEncodeError:
        return urllib.urlencode([(k, smart_str(v)) for k, v in items])


def wiki_to_html(wiki_markup, wiki_hooks=False):
    """Wiki Markup -> HTML"""
    parser = WikiParser(wiki_hooks=wiki_hooks)
    return jinja2.Markup(parser.parse(wiki_markup, False))
