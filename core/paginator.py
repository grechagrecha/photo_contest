import urllib.parse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SmartPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args)

        self.params = {key: value for key, value in request.GET.items()}

        self.first_page_params = urllib.parse.urlencode({**self.params, 'page': 1})
        self.last_page_params = urllib.parse.urlencode({**self.params, 'page': self.num_pages})

    def page(self, number):
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages

        page = super().page(number)

        try:
            page.previous_page_number = page.previous_page_number()
        except EmptyPage:
            page.previous_page_number = None
        try:
            page.next_page_number = page.next_page_number()
        except EmptyPage:
            page.next_page_number = None

        page.previous_page_params = urllib.parse.urlencode({**self.params, 'page': page.previous_page_number})
        page.next_page_params = urllib.parse.urlencode({**self.params, 'page': page.next_page_number})

        return page
