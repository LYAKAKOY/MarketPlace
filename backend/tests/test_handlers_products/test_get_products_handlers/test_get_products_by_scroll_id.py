from typing import List

import pytest
from tests.conftest import create_product
from tests.conftest import products_data

@pytest.mark.parametrize(
    "additional_products_data, expected_status_code",
    [
        (
            [
                {"id_company": 20, "product_name": "Product A", "description": "Description A", "category": "Category X", "sum": 500},
                {"id_company": 20, "product_name": "Product A", "description": "Description B", "category": "Category Y", "sum": 600},
                {"id_company": 30, "product_name": "Product C", "description": "Description C", "category": "Category Z", "sum": 800},
            ],
            200,
        ),
    ],
)
async def test_get_products_by_scroll_id_handler(
    client,
    create_products,
    additional_products_data,
    expected_status_code
):
    for product in additional_products_data:
        await create_product(document=product)
    response = await client.get(
        f"/products/",
    )
    data_from_response = response.json()
    assert data_from_response.get("scroll_id") is not None
    got_products: List[dict] = data_from_response.get('products')
    response = await client.get(
        f"/products/scroll/{data_from_response.get('scroll_id')}/",
    )
    data_from_response = response.json()
    got_products.extend(data_from_response.get("products"))
    products_data.extend(additional_products_data)
    assert len(got_products) == len(products_data)
    sort_by = lambda p: p["product_name"] and p["category"] and p["description"] and p["sum"]
    for got_product, expected_product in zip(
            sorted(got_products, key=sort_by),
            sorted(products_data, key=sort_by)):
        assert got_product["id_company"] == expected_product["id_company"]
        assert got_product["product_name"] == expected_product["product_name"]
        assert got_product["description"] == expected_product["description"]
        assert got_product["category"] == expected_product["category"]
        assert got_product["sum"] == expected_product["sum"]

async def test_get_products_by_scroll_id_handler_404_not_found(
    client,
    create_products,
):
    response = await client.get(
        f"/products/",
    )
    data_from_response = response.json()
    assert data_from_response.get("scroll_id") is not None
    response = await client.get(
        f"/products/scroll/{data_from_response.get('scroll_id')}/",
    )
    data_from_response = response.json()
    assert response.status_code == 404
    assert data_from_response == {"detail": "There are no products"}

async def test_get_products_by_scroll_id_handler_incorrect_scroll_id(
    client,
    create_products,
):
    response = await client.get(
        f"/products/",
    )
    data_from_response = response.json()
    assert data_from_response.get("scroll_id") is not None
    response = await client.get(
        f"/products/scroll/1/",
    )
    data_from_response = response.json()
    assert response.status_code == 404
    assert data_from_response == {"detail": "There are no products"}