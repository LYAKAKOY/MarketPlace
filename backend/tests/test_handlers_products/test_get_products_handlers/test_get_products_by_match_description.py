import pytest
from tests.conftest import products_data


@pytest.mark.parametrize(
    "description, expected_status_code, expected_data",
    [
        (
                "A",
                200,
                list(filter(lambda p: "A" in p["description"].split(), products_data)),
        ),
        (
                "B",
                200,
                list(filter(lambda p: "B" in p["description"].split(), products_data)),
        ),
    ],
)
async def test_get_products_by_match_description_handler(
        client,
        create_products,
        description,
        expected_status_code,
        expected_data,
):
    response = await client.get(
        f"/products/by_match_description/{description}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert len(data_from_response["products"]) == len(expected_data)
    sort_by = lambda p: p["product_name"] and p["category"] and p["description"] and p["sum"]
    for got_product, expected_product in zip(
            sorted(data_from_response["products"], key=sort_by),
            sorted(expected_data, key=sort_by)):
        assert got_product["id_company"] == expected_product["id_company"]
        assert got_product["product_name"] == expected_product["product_name"]
        assert got_product["description"] == expected_product["description"]
        assert got_product["category"] == expected_product["category"]
        assert got_product["sum"] == expected_product["sum"]


@pytest.mark.parametrize(
    "description, expected_status_code, expected_data",
    [
        (
                "F",
                404,
                {"detail": "There are no products"},
        ),
    ],
)
async def test_get_products_by_match_description_handler_404_not_found(
        client,
        create_products,
        description,
        expected_status_code,
        expected_data,
):
    response = await client.get(
        f"/products/by_match_description/{description}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data
