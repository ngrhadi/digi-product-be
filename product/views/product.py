from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from uuid import uuid4
from rest_framework.views import APIView
from django.views import View
import json
from rest_framework import status, permissions
from uuid import UUID
from ..models import MasterProduct



class MasterProductView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            # Extract query parameters
            product_id = request.GET.get('id')
            category = request.GET.get('category')
            location = request.GET.get('location')
            product_name = request.GET.get('product_name')
            quantity = request.GET.get('quantity')
            total_selling = request.GET.get('total_selling')

            # Assuming you want to filter based on these parameters
            filters = {}
            if product_id:
                try:
                    filters['id'] = UUID(product_id)
                except ValueError:
                    return JsonResponse({'error': 'Invalid product_id'}, status=400)
            if category:
                filters['category'] = category
            if location:
                filters['location'] = location
            if product_name:
                filters['product_name__icontains'] = product_name
            if quantity:
                try:
                    filters['quantity'] = int(quantity)
                except ValueError:
                    return JsonResponse({'error': 'Invalid quantity'}, status=400)
            if total_selling:
                try:
                    filters['total_selling'] = int(total_selling)
                except ValueError:
                    return JsonResponse({'error': 'Invalid total selling'}, status=400)

            products = MasterProduct.objects.filter(**filters)

            # Serialize the results to JSON (assuming you have a suitable method)
            product_list = list(products.values())

            return JsonResponse(product_list, safe=False, status=200)
        except Exception as e:
            return JsonResponse(
                {'error': str(e)},
                status=500
            )

    def post(self, request):
        data = json.loads(request.body)  # Assuming the data comes in JSON format
        product_id = uuid4()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO master_product (id, code, product_name, price, store_name, quantity, total_selling, category, description, country, location, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    product_id,
                    data.get('code'),
                    data.get('product_name'),
                    data.get('price'),
                    data.get('store_name'),
                    data.get('quantity'),
                    data.get('total_selling'),
                    data.get('category'),
                    data.get('description'),
                    data.get('country'),
                    data.get('location'),
                    data.get('image_url')
                ]
            )
        return JsonResponse({"id": product_id}, status=201)

    def put(self, request, product_id):
        data = json.loads(request.body)  # Assuming the data comes in JSON format
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE master_product
                SET code = %s, product_name = %s, price = %s, store_name = %s, quantity = %s, total_selling = %s, category = %s, description = %s, country = %s, location = %s, image_url = %s
                WHERE id = %s
                """,
                [
                    data.get('code'),
                    data.get('product_name'),
                    data.get('price'),
                    data.get('store_name'),
                    data.get('quantity'),
                    data.get('total_selling'),
                    data.get('category'),
                    data.get('description'),
                    data.get('country'),
                    data.get('location'),
                    data.get('image_url'),
                    product_id
                ]
            )
        return JsonResponse({"status": "success"}, status=200)

    def delete(self, request, product_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM master_product WHERE id = %s",
                [product_id]
            )
        return JsonResponse({"status": "deleted"}, status=204)
