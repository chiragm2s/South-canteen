from rest_framework import pagination
from rest_framework.response import Response

class APIPagination(pagination.PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data):
        if data == []:
            status = False
            message = "No Details Found"
        else:
            status = True
            message = "Details Fetched"
        return Response({
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            # },
            # 'meta': {
                'count': self.page.paginator.count,
                'pages': self.page.paginator.num_pages,
                'current_page_number': self.page.number,
            },
            'status' : status,
            'message' : message,
            'data': data
        })
