import pytest
from tests.conftest import products_data


@pytest.mark.parametrize(
    "category, expected_status_code, expected_data",
    [
        (
            "Category X",
            200,
            list(filter(lambda p: p["category"] == "Category X", products_data)),
        ),
        (
            "Category Z",
            200,
            list(filter(lambda p: p["category"] == "Category Z", products_data)),
        ),
    ],
)
async def test_get_products_category_handler(
    client,
    create_products,
    category,
    expected_status_code,
    expected_data,
):
    response = await client.get(
        f"/products/by_category/{category}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert len(data_from_response["products"]) == len(expected_data)
    sort_by = (
        lambda p: p["product_name"] and p["category"] and p["description"] and p["sum"]
    )
    for got_product, expected_product in zip(
        sorted(data_from_response["products"], key=sort_by),
        sorted(expected_data, key=sort_by),
    ):
        assert got_product["id_company"] == expected_product["id_company"]
        assert got_product["product_name"] == expected_product["product_name"]
        assert got_product["description"] == expected_product["description"]
        assert got_product["category"] == expected_product["category"]
        assert got_product["sum"] == expected_product["sum"]


@pytest.mark.parametrize(
    "category, expected_status_code, expected_data",
    [
        (
            "Category LK",
            404,
            {"detail": "There are no products"},
        ),
    ],
)
async def test_get_products_company_id_handler_404_not_found(
    client,
    create_products,
    category,
    expected_status_code,
    expected_data,
):
    response = await client.get(
        f"/products/by_category/{category}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data
