from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'current': self.page.number,
            'pageSize': self.page_size,
            'total': self.page.paginator.count,
            'results': data
        })
