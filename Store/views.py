from django.shortcuts import render
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.db.models import Case, When
from django.core.cache import cache
from .models import *
from .serializers import *
from .search_documents import ProductDocument

def search_test_page(request):
    return render(request, 'search_test.html')
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('brand', 'category').prefetch_related('tags')

    def get_queryset(self):
        q = (self.request.query_params.get('q') or '').strip()
        if not q or len(q) < 2:
            return self.queryset

        s = ProductDocument.search().query(
            'multi_match',
            query=q,
            fields=["name^4", "brand.name^2", "category.name^2", "tags", "name_ngram^2", "brand_ngram", "category_ngram"],
            fuzziness="AUTO",
            prefix_length=2
        )
        response = s.execute()
        ids = [hit.meta.id for hit in response if getattr(hit.meta, 'id', None)]

        if not ids:
            return Product.objects.all()

        preserved_order_case = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(ids)],
            default=len(ids),
            output_field=models.IntegerField()
        )

        combined_qs = Product.objects.annotate(
            search_order=preserved_order_case
        ).order_by('search_order', 'pk')

        return combined_qs

class ProductAutocompleteView(APIView):
    SUGGESTION_FIELDS = [('name_suggest', 'name', 40),('brand_suggest', 'brand.name', 5),('category_suggest', 'category.name', 5)]
    
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
                        'fuzzy': {'fuzziness': 1},
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
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"], url_path="products")
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class TagViewSet(ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

class ConcernViewSet(ModelViewSet):
    queryset = Concerns.objects.all()
    serializer_class = ConcernSerializer

class SkinTypeViewSet(ModelViewSet):
    queryset = SkinType.objects.all()
    serializer_class = SkinTypeSerializer

class IngredientViewSet(ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer