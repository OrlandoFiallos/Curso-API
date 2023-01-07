from rest_framework import serializers
from .models import MenuItem,Category
from decimal import Decimal
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    # title = serializers.CharField(max_length=255,validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only=True) 
    #price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    
    #Métodos para validar campos
    # def validate_price(self,value):
    #     if value < 2:
    #         raise serializers.ValidationError('Price should not be less than 2')
    # def validate_stock(self, value):
    #     if value < 0:
    #         raise serializers.ValidationError('Stock cannot be negative')
    
    #Método validate para validar campos
    def validate(self, attrs):
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
    class Meta:
        model = MenuItem
        #fields = ['id','title','price','inventory']
        fields = ['id','title','price','stock','price_after_tax','category','category_id']
        # extra_kwargs = {
        #     'price':{'min_value':2},
        #     'stock':{'source':'inventory', 'min_value':0}
        # }
        # extra_kwargs = {
        #     'title':{
        #         'validators':[
        #             UniqueValidator(
        #                 queryset=MenuItem.objects.all()
        #             )
        #         ]
        #     }
        # }
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title','price']
            )
        ]
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)