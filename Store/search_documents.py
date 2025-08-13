from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'filter': {
                    'autocomplete_filter': {
                        'type': 'edge_ngram',
                        'min_gram': 2,
                        'max_gram': 20
                    }
                },
                'analyzer': {
                    'autocomplete': {
                        'type': 'custom',
                        'tokenizer': 'standard',
                        'filter': [
                            'lowercase',
                            'autocomplete_filter'
                        ]
                    }
                }
            }
        }
    
    name_suggest = fields.CompletionField()
    brand_suggest = fields.CompletionField()
    category_suggest = fields.CompletionField()
    
    name_ngram = fields.TextField(analyzer='autocomplete')
    brand_ngram = fields.TextField(analyzer='autocomplete')
    category_ngram = fields.TextField(analyzer='autocomplete')
    
    brand = fields.ObjectField(properties={'name': fields.TextField(), })
    category = fields.ObjectField(properties={'name': fields.TextField(), })
    tags = fields.TextField(multi=True)
    
    class Django:
        model = Product
        fields = ['name', 'description']
    
    def prepare(self, instance):
        data = super().prepare(instance)
        
        data['name_ngram'] = instance.name
        if instance.brand:
            data['brand_ngram'] = instance.brand.name
        if instance.category:
            data['category_ngram'] = instance.category.name
        
        return data
    
    def prepare_name_suggest(self, instance):
        return {
            "input": [instance.name],
            "weight": 10
            }

    def prepare_brand_suggest(self, instance):
        if instance.brand:
            return {
                "input": [instance.brand.name],
                "weight": 5
            }
        return {}

    def prepare_category_suggest(self, instance):
        if instance.category:
            return {
                "input": [instance.category.name],
                "weight": 5
            }
        return {}
    
    def prepare_brand(self, instance):
        if instance.brand:
            return {
                "name": instance.brand.name
            }
        return {}

    def prepare_category(self, instance):
        if instance.category:
            return {
                "name": instance.category.name
            }
        return {}

    def prepare_tags(self, instance):
        return list(instance.tags.values_list('name', flat=True))