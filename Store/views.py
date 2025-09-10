from django.shortcuts import render
from django.db import models
from django.db.models import F, Case, When
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.core.cache import cache
from .models import *
from .serializers import *
from .search_documents import ProductDocument

def search_test_page(request):
    return render(request, 'search_test.html')
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('brand', 'category').prefetch_related('tags', 'ingredients', 'concerns_targeted', 'skin_type')

    def get_queryset(self):
        q = (self.request.query_params.get('q') or '').strip()
        if not q or len(q) < 1:
            queryset = self.queryset
            
            sort = self.request.query_params.get('sort') or self.request.query_params.get('ordering')
            if sort == 'views' or sort == '-views_count':
                queryset = queryset.order_by('-views_count')
            elif sort == 'rating_high' or sort == '-rating':
                queryset = queryset.order_by('-rating')
            elif sort == 'rating_low' or sort == 'rating':
                queryset = queryset.order_by('rating')
            elif sort == 'price_high' or sort == '-price':
                queryset = queryset.order_by('-price')
            elif sort == 'price_low' or sort == 'price':
                queryset = queryset.order_by('price')
            return queryset
        
        s = ProductDocument.search().query(
            'bool',
            should=[
                {'match': {'name_exact': {'query': q.lower(), 'boost': 10}}},
                {'match': {'brand_exact': {'query': q.lower(), 'boost': 8}}},
                {'match': {'category_exact': {'query': q.lower(), 'boost': 6}}},
                {'match': {'name_ngram': {'query': q, 'boost': 6, 'fuzziness': 'AUTO'}}},
                {'match': {'brand_ngram': {'query': q, 'boost': 4, 'fuzziness': 'AUTO'}}},
                {'match': {'category_ngram': {'query': q, 'boost': 4, 'fuzziness': 'AUTO'}}},
                {'match': {'tags': {'query': q, 'boost': 3}}},
            ],
            minimum_should_match=1
        )
        
        total_count = s.count()
        response = s[:total_count].execute()
        ids = [hit.meta.id for hit in response if getattr(hit.meta, 'id', None)]

        if not ids:
            return Product.objects.none()

        preserved_order_case = Case(
            *[When(product_id=pk, then=pos) for pos, pk in enumerate(ids)],
            default=len(ids),
            output_field=models.IntegerField())

        combined_qs = Product.objects.filter(product_id__in=ids).annotate(
            search_order=preserved_order_case)

        sort = self.request.query_params.get('sort')
        if sort == 'views':
            combined_qs = combined_qs.order_by('-views_count', 'search_order', 'product_id')
        elif sort == 'rating_high':
            combined_qs = combined_qs.order_by('-rating', 'search_order', 'product_id')
        elif sort == 'rating_low':
            combined_qs = combined_qs.order_by('rating', 'search_order', 'product_id')
        elif sort == 'price_high':
            combined_qs = combined_qs.order_by('-price', 'search_order', 'product_id')
        elif sort == 'price_low':
            combined_qs = combined_qs.order_by('price', 'search_order', 'product_id')
        else:
            combined_qs = combined_qs.order_by('search_order', 'product_id')

        return combined_qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Product.objects.filter(product_id=instance.product_id).update(views_count=F('views_count') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class ProductAutocompleteView(APIView):
    SUGGESTION_FIELDS = [('name_suggest', 'name', 40), ('brand_suggest', 'brand.name', 5), ('category_suggest', 'category.name', 5)]

    def get(self, request):
        q = request.GET.get('q', '').strip()
        if len(q) < 2:
            return Response([])
        
        cache_key = f'autocomplete_{q}'
        if cached := cache.get(cache_key):
            return Response(cached)
        
        try:
            s = ProductDocument.search()
            for field, _, _ in self.SUGGESTION_FIELDS:
                s = s.suggest(
                    field,
                    q,
                    completion={
                        'field': field,
                        'fuzzy': {'fuzziness': 2},
                        'size': 8,
                        'skip_duplicates': True
                    }
                )

            response = s.execute()
            options = set()

            for field, _, _ in self.SUGGESTION_FIELDS:
                for suggest in response.suggest.get(field, []):
                    for option in suggest.options:
                        options.add(option.text)
                        
            results = sorted(options)
            cache.set(cache_key, results, timeout=60*15)
            return Response(results)
        
        except Exception:
            results = set()
            for field, model_field, _ in self.SUGGESTION_FIELDS:
                if model_field == 'name':
                    results.update(Product.objects.filter(
                        name__icontains=q
                    ).values_list('name', flat=True)[:8])
                elif 'brand' in model_field:
                    results.update(Brand.objects.filter(
                        name__icontains=q
                    ).values_list('name', flat=True)[:5])
                elif 'category' in model_field:
                    results.update(Category.objects.filter(
                        name__icontains=q
                    ).values_list('name', flat=True)[:5])

            return Response(sorted(results))
class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        brand = self.get_object()
        products = Product.objects.filter(brand=brand)
        
        sort = request.query_params.get('sort')
        if sort == 'views':
            products = products.order_by('-views_count')
        elif sort == 'rating_high':
            products = products.order_by('-rating')
        elif sort == 'rating_low':
            products = products.order_by('rating')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'price_low':
            products = products.order_by('price')
        else:
            products = products.order_by('name')  

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)

        sort = request.query_params.get('sort')
        if sort == 'views':
            products = products.order_by('-views_count')
        elif sort == 'rating_high':
            products = products.order_by('-rating')
        elif sort == 'rating_low':
            products = products.order_by('rating')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'price_low':
            products = products.order_by('price')
        else:
            products = products.order_by('name')  

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class TagViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        tag = self.get_object()
        products = Product.objects.filter(tags=tag)
        
        sort = request.query_params.get('sort')
        if sort == 'views':
            products = products.order_by('-views_count')
        elif sort == 'rating_high':
            products = products.order_by('-rating')
        elif sort == 'rating_low':
            products = products.order_by('rating')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'price_low':
            products = products.order_by('price')
        else:
            products = products.order_by('name')  

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
class ConcernViewSet(ModelViewSet):
    queryset = Concerns.objects.all()
    serializer_class = ConcernSerializer
class SkinTypeViewSet(ModelViewSet):
    queryset = SkinType.objects.all()
    serializer_class = SkinTypeSerializer
class IngredientViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer