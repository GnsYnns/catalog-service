from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['price_cents', 'created_at', 'stock']

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        try:
            threshold = int(request.query_params.get('threshold', 5))
        except ValueError:
            return Response({'threshold': 'Le seuil doit être un entier.'}, status=status.HTTP_400_BAD_REQUEST)
        products = self.filter_queryset(self.get_queryset().filter(stock__lte=threshold))
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
