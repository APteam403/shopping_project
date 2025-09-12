from django.shortcuts import render
from django.db import models
from django.db.models import F, Case, When, Count, Q, F, FloatField, ExpressionWrapper, Value
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.core.cache import cache
from .models import *
from .serializers import *
# from .search_documents import ProductDocument
from django.shortcuts import get_object_or_404
from django.db.models.functions import Abs
from django.db.models import Max

# class ProductViewSet(ModelViewSet):
#     serializer_class = ProductSerializer
#     queryset = Product.objects.select_related('brand', 'category').prefetch_related('tags', 'ingredients', 'concerns_targeted', 'skin_type')

#     def get_queryset(self):
#         q = (self.request.query_params.get('q') or '').strip()
#         if not q or len(q) < 1:
#             queryset = self.queryset
            
#             sort = self.request.query_params.get('sort') or self.request.query_params.get('ordering')
#             if sort == 'views' or sort == '-views_count':
#                 queryset = queryset.order_by('-views_count')
#             elif sort == 'rating_high' or sort == '-rating':
#                 queryset = queryset.order_by('-rating')
#             elif sort == 'rating_low' or sort == 'rating':
#                 queryset = queryset.order_by('rating')
#             elif sort == 'price_high' or sort == '-price':
#                 queryset = queryset.order_by('-price')
#             elif sort == 'price_low' or sort == 'price':
#                 queryset = queryset.order_by('price')
#             return queryset
        
#         s = ProductDocument.search().query(
#             'bool',
#             should=[
#                 {'match': {'name_exact': {'query': q.lower(), 'boost': 10}}},
#                 {'match': {'brand_exact': {'query': q.lower(), 'boost': 8}}},
#                 {'match': {'category_exact': {'query': q.lower(), 'boost': 6}}},
#                 {'match': {'name_ngram': {'query': q, 'boost': 6, 'fuzziness': 'AUTO'}}},
#                 {'match': {'brand_ngram': {'query': q, 'boost': 4, 'fuzziness': 'AUTO'}}},
#                 {'match': {'category_ngram': {'query': q, 'boost': 4, 'fuzziness': 'AUTO'}}},
#                 {'match': {'tags': {'query': q, 'boost': 3}}},
#             ],
#             minimum_should_match=1
#         )
        
#         total_count = s.count()
#         response = s[:total_count].execute()
#         ids = [hit.meta.id for hit in response if getattr(hit.meta, 'id', None)]

#         if not ids:
#             return Product.objects.none()

#         preserved_order_case = Case(
#             *[When(product_id=pk, then=pos) for pos, pk in enumerate(ids)],
#             default=len(ids),
#             output_field=models.IntegerField())

#         combined_qs = Product.objects.filter(product_id__in=ids).annotate(
#             search_order=preserved_order_case)

#         sort = self.request.query_params.get('sort')
#         if sort == 'views':
#             combined_qs = combined_qs.order_by('-views_count', 'search_order', 'product_id')
#         elif sort == 'rating_high':
#             combined_qs = combined_qs.order_by('-rating', 'search_order', 'product_id')
#         elif sort == 'rating_low':
#             combined_qs = combined_qs.order_by('rating', 'search_order', 'product_id')
#         elif sort == 'price_high':
#             combined_qs = combined_qs.order_by('-price', 'search_order', 'product_id')
#         elif sort == 'price_low':
#             combined_qs = combined_qs.order_by('price', 'search_order', 'product_id')
#         else:
#             combined_qs = combined_qs.order_by('search_order', 'product_id')

#         return combined_qs

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         Product.objects.filter(product_id=instance.product_id).update(views_count=F('views_count') + 1)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)

# class ProductAutocompleteView(APIView):
#     SUGGESTION_FIELDS = [('name_suggest', 'name', 40), ('brand_suggest', 'brand.name', 5), ('category_suggest', 'category.name', 5)]

#     def get(self, request):
#         q = request.GET.get('q', '').strip()
#         if len(q) < 2:
#             return Response([])
        
#         cache_key = f'autocomplete_{q}'
#         if cached := cache.get(cache_key):
#             return Response(cached)
        
#         try:
#             s = ProductDocument.search()
#             for field, _, _ in self.SUGGESTION_FIELDS:
#                 s = s.suggest(
#                     field,
#                     q,
#                     completion={
#                         'field': field,
#                         'fuzzy': {'fuzziness': 2},
#                         'size': 8,
#                         'skip_duplicates': True
#                     }
#                 )

#             response = s.execute()
#             options = set()

#             for field, _, _ in self.SUGGESTION_FIELDS:
#                 for suggest in response.suggest.get(field, []):
#                     for option in suggest.options:
#                         options.add(option.text)
                        
#             results = sorted(options)
#             cache.set(cache_key, results, timeout=60*15)
#             return Response(results)
        
#         except Exception:
#             results = set()
#             for field, model_field, _ in self.SUGGESTION_FIELDS:
#                 if model_field == 'name':
#                     results.update(Product.objects.filter(
#                         name__icontains=q
#                     ).values_list('name', flat=True)[:8])
#                 elif 'brand' in model_field:
#                     results.update(Brand.objects.filter(
#                         name__icontains=q
#                     ).values_list('name', flat=True)[:5])
#                 elif 'category' in model_field:
#                     results.update(Category.objects.filter(
#                         name__icontains=q
#                     ).values_list('name', flat=True)[:5])

#             return Response(sorted(results))
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

def index_page(response):
    products = Product.objects.all()
    return render(response, 'Store/index.html', {'products' : products})

def detail_page(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.user.is_authenticated:
        profile = request.user.profile
        preferences = profile.preferences
        wishlist = profile.wishlist
        viewed_products = profile.views_product
    else:
        preferences = []
        wishlist = []
        viewed_products = []

    max_views = cache.get('max_views')
    if max_views is None:
        max_views = Product.objects.aggregate(max_views=Max('views_count'))['max_views'] or 1
        cache.set('max_views', max_views, 300)
    
    views_score = ExpressionWrapper(
        (F('views_count') / max_views) * 5,
        output_field=FloatField()
    )
    price_diff = Abs(F('price') - product.price)
    max_score_price = 8
    max_price_diff = 1000
    price_score = ExpressionWrapper(
        Value(max_score_price) * (1 - (price_diff / max_price_diff)),
        output_field=FloatField()
    )
    products = Product.objects.exclude(pk=product.pk).annotate(
    score=(
        Case(
            When(brand=product.brand, then=Value(8)),
            default=Value(0),
            output_field=FloatField()
        ) +
        Case(
            When(category=product.category, then=Value(10)),
            default=Value(0),
            output_field=FloatField()
        ) +
        Count('skin_type', filter=Q(skin_type__in=product.skin_type.all())) * 6 +
        Count('tags', filter=Q(tags__in=product.tags.all())) * 6 +
        price_score +
        views_score
        )
    ).select_related('brand', 'category').prefetch_related('tags', 'skin_type')

    views_categories = set(p.category for p in Product.objects.filter(slug__in=set(viewed_products)))
    views_brand = set(p.category for p in Product.objects.filter(slug__in=set(viewed_products)))

    wishlist_categories = set(p.category for p in Product.objects.filter(slug__in=set(wishlist)))
    wishlist_brands = set(p.brand for p in Product.objects.filter(slug__in=set(wishlist)))

    preferences_categories = set(p.category for p in Product.objects.filter(slug__in=set(preferences)))
    preferences_brands = set(p.brand for p in Product.objects.filter(slug__in=set(preferences)))

    for p in products:
        if p.category in wishlist_categories:
            p.score += 5
        if p.brand in wishlist_brands:
            p.score += 4
        if p.category in preferences_categories:
            p.score += 3   
        if p.brand in preferences_brands:
            p.score += 3
        if p.category in views_categories:
            p.score += 1
        if p.brand in views_brand:
            p.score += 1

    TOP_N = 20
    top_by_score = products.order_by('-score')[:TOP_N]
    recommended = sorted(
        top_by_score,
        key=lambda product: (product.views_count, getattr(product, 'score', 0)),
        reverse=True
    )[:8]

    context = {
        'product': product,
        'products': products,
        'product_recommended': recommended
    }
    return render(request, 'Store/detail.html', context)

def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'products': products
    }
    
    return render(request, 'Store/category.html', context)

def views_hot_page(request):
    products = Product.objects.all()
    products2 = products.order_by('-views_count')
    context = {
        'all_views_hot' : products2
    }
    return render(request, 'Store/views_hot.html', context)

def search_test_page(request):
    return render(request, 'Store/search_test.html')

def weblog(request):
    return render(request, 'Store/weblog.html')

def about_us(request):
    return render(request, 'Store/about-us.html')