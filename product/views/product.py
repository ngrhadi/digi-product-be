from django.http import JsonResponse
from django.db import connection
from uuid import uuid4
from django.views import View
import json

class MasterProductView(View):
    def get(self, request, product_id=None):
        with connection.cursor() as cursor:
            if product_id:
                cursor.execute("SELECT * FROM master_product WHERE id = %s", [product_id])
                product = cursor.fetchone()
                if product is None:
                    return JsonResponse({'error': 'Product not found'}, status=404)
                columns = [col[0] for col in cursor.description]
                product = dict(zip(columns, product))
                return JsonResponse(product)
            else:
                cursor.execute("SELECT * FROM master_product")
                columns = [col[0] for col in cursor.description]
                products = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return JsonResponse(products, safe=False)

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
