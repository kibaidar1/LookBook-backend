import math
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class APIListPagination(PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 600
    last_page_strings = ('last',)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('countAll', self.page.paginator.count),
            ('countPageItems', self.page_size),
            ('currentPage', self.page.number),
            ('previous', self.get_previous_link()),
            ('next', self.get_next_link()),
            ('lastPage', math.ceil(self.page.paginator.count / self.page_size)),
            ('results', data)
        ]))

