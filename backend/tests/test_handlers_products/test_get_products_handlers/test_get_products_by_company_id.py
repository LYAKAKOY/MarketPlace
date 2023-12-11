import pytest
from tests.conftest import products_data

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
    ],
)
async def test_get_products_company_id_handler(
    client,
    create_products,
    products_data,
    company_id,
    expected_status_code,
    expected_data,
):
    response = await client.get(
        f"/products/by_company/{company_id}/",
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
    "products_data, company_id, expected_status_code, expected_data",
    [
        (
            products_data,
            20,
            404,
            {"detail": "There are no products"},
        ),
    ],
)
async def test_get_products_company_id_handler_404_not_found(
    client,
    create_products,
    products_data,
    company_id,
    expected_status_code,
    expected_data,
):
    response = await client.get(
        f"/products/by_company/{company_id}/",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data
@pytest.mark.parametrize(
    "company_id, expected_status_code, expected_data",
    [
        (
            "a",
            422,
            {'detail': [{'input': 'b',
                         'loc': ['query', 'max_sum'],
                         'msg': 'Input should be a valid integer, unable to parse string '
                                'as an integer',
                         'type': 'int_parsing',
                         'url': 'https://errors.pydantic.dev/2.5/v/int_parsing'},
                        {'input': 'a',
                         'loc': ['query', 'min_sum'],
                         'msg': 'Input should be a valid integer, unable to parse string '
                                'as an integer',
                         'type': 'int_parsing',
                         'url': 'https://errors.pydantic.dev/2.5/v/int_parsing'}]},
        ),
    ],
)
async def test_get_products_company_id_handler_without_int_parameter(
    client,
    company_id,
    expected_status_code,
    expected_data,
):
    response = await client.get(
        "/products/by_company/a/",
    )
    data_from_response = response.json()
    assert response.status_code == 422
    assert data_from_response == {'detail': [{'input': 'a',
             'loc': ['path', 'company_id'],
             'msg': 'Input should be a valid integer, unable to parse string '
                    'as an integer',
             'type': 'int_parsing',
             'url': 'https://errors.pydantic.dev/2.5/v/int_parsing'}]}