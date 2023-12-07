import pytest

from tests.test_data import products


@pytest.mark.parametrize(
    "product_name, min_sum, max_sum, expected_status_code, expected_data",
    [
        (
            "Product A",
            100,
            180,
            200,
            list(filter(lambda product: 100 <= product["sum"] < 180 and product["product_name"] == "Product A", products)),

        ),
        (
            "Product C",
            200,
            240,
            200,
            list(filter(lambda product: 200 <= product["sum"] < 240 and product["product_name"] == "Product C", products)),
        ),
    ],
)
async def test_create_product_handler(
    client,
    create_products,
    product_name,
    min_sum,
    max_sum,
    expected_status_code,
    expected_data,
):
    response = await client.get(
        f"/products/filter?product_name={product_name}&min_sum={min_sum}&max_sum={max_sum}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert len(data_from_response["products"]) == len(expected_data)
    sort = lambda p: p["id_company"] and p["category"] and p["product_name"]
    for product_from_response, expected_product in zip(
            sorted(data_from_response["products"], key=sort),
            sorted(expected_data, key=sort)):
        assert product_from_response["id_company"] == expected_product["id_company"]
        assert product_from_response["product_name"] == expected_product["product_name"]
        assert product_from_response["description"] == expected_product["description"]
        assert product_from_response["category"] == expected_product["category"]
        assert product_from_response["sum"] == expected_product["sum"]
