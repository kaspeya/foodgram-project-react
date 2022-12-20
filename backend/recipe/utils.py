from django.http import HttpResponse


def generate_report(ingredients_list):
    shopping_list = []
    for ingredient in ingredients_list:
        shopping_list.append(
            f'{ingredient["ingredient__name"]} - {ingredient["total"]} '
            f'{ingredient["ingredient__measurement_unit"]} \n'
        )

    response = HttpResponse(shopping_list)
    response['Content-Disposition'] = 'attachment; filename="shoppingcart.txt"'
    response['Content-Type'] = 'text/plain'

    return response
