from tests.conftest import products_data

async def test_get_all_products_handler(
    client,
    create_products,
):
    response = await client.get(
        f"/products/",
    )
    data_from_response = response.json()
    assert response.status_code == 200
    assert len(data_from_response["products"]) == len(products_data)
    sort_by = lambda p: p["product_name"] and p["category"] and p["description"] and p["sum"]
    for got_product, expected_product in zip(
            sorted(data_from_response["products"], key=sort_by),
            sorted(products_data, key=sort_by)):
        assert got_product["id_company"] == expected_product["id_company"]
        assert got_product["product_name"] == expected_product["product_name"]
        assert got_product["description"] == expected_product["description"]
        assert got_product["category"] == expected_product["category"]
        assert got_product["sum"] == expected_product["sum"]