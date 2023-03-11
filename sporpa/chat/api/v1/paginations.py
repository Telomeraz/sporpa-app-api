from rest_framework import pagination


class MessageCursorPagination(pagination.CursorPagination):
    ordering = "-pk"
    page_size = 30
