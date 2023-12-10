import pytest
from tests.conftest import products_data
from db.elasticsearch.indexes import NAME_INDEX_PRODUCTS

@pytest.mark.parametrize(
    "products_data, company_id, expected_status_code, expected_data",
    [
        (
            products_data,
            1,
            200,
            list(filter(lambda p: p["id_company"] == 1, products_data)),
        ),
        (
            products_data,
            3,
            200,
            list(filter(lambda p: p["id_company"] == 3, products_data)),
        ),
        (
            products_data,
            20,
            404,
            list(filter(lambda p: p["id_company"] == 20, products_data)),
        ),
    ],
)
async def test_get_products_using_filter_handler(
    client,
    test_client_es,
    products_data,
    company_id,
    expected_status_code,
    expected_data,
):
    for test_product in products_data:
        await test_client_es.index(index=NAME_INDEX_PRODUCTS, document=test_product, params={"refresh": "true"})
    response = await client.get(
        f"/products/by_company/{company_id}/",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    try:
        products = data_from_response["products"]
    except KeyError:
        products = []
    assert len(products) == len(expected_data)
    sort_by = lambda p: p["product_name"] and p["category"] and p["description"] and p["sum"]
    for got_product, expected_product in zip(
            sorted(products, key=sort_by),
            sorted(expected_data, key=sort_by)):
        assert got_product["id_company"] == expected_product["id_company"]
        assert got_product["product_name"] == expected_product["product_name"]
        assert got_product["description"] == expected_product["description"]
        assert got_product["category"] == expected_product["category"]
        assert got_product["sum"] == expected_product["sum"]
