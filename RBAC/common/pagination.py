from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_current_page(self):
        if self.page.has_next():
            # if self.page.next_page_number():
            return self.page.next_page_number() - 1
        elif self.page.has_previous():
            return self.page.previous_page_number() + 1
        return 1

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'current': self.request.build_absolute_uri(),
            'cpage': self.get_current_page(),
            'page_size': self.page_size,
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })