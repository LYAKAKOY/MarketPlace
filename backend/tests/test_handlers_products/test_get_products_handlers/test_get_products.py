# import pytest
#
# from tests.test_data import products
#
#
# @pytest.mark.parametrize(
#     "product_name, min_sum, max_sum, expected_status_code, expected_data",
#     [
#         (
#             "Product A",
#             100,
#             180,
#             200,
#             list(filter(lambda product: 100 <= product["sum"] < 180 and product["product_name"] == "Product A", products)),
#
#         ),
#         (
#             "Product C",
#             200,
#             240,
#             200,
#             list(filter(lambda product: 200 <= product["sum"] < 240 and product["product_name"] == "Product C", products)),
#         ),
#         (
#             "Product C",
#             300,
#             400,
#             404,
#             list(filter(lambda product: 300 <= product["sum"] < 400 and product["product_name"] == "Product C", products)),
#         ),
#     ],
# )
# async def test_get_products_using_filter_handler(
#     client,
#     create_products,
#     product_name,
#     min_sum,
#     max_sum,
#     expected_status_code,
#     expected_data,
# ):
#     response = await client.get(
#         f"/products/filter?product_name={product_name}&min_sum={min_sum}&max_sum={max_sum}",
#     )
#     data_from_response = response.json()
#     assert response.status_code == expected_status_code
#     assert len(data_from_response["products"]) == len(expected_data)
