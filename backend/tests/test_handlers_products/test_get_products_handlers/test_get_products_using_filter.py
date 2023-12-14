import pytest

from tests.conftest import products_data


@pytest.mark.parametrize(
    "product_name, min_sum, max_sum, expected_status_code, expected_data",
    [
        (
            "Product A",
            100,
            180,
            200,
            list(filter(lambda product: 100 <= product["sum"] < 180 and product["product_name"] == "Product A", products_data)),

        ),
        (
            "Product C",
            200,
            240,
            200,
            list(filter(lambda product: 200 <= product["sum"] < 240 and product["product_name"] == "Product C", products_data)),
        ),
    ],
)
async def test_get_products_using_filter_handler(
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
    "product_name, min_sum, max_sum, expected_status_code, expected_data",
    [
        (
            "Product C",
            300,
            400,
            404,
            {"detail": "There are no products"},
        ),
    ],
)
async def test_get_products_using_filter_handler_404_not_found(
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
    assert data_from_response == expected_data

async def test_get_products_using_filter_handler_without_parameter(
    client,
):
    response = await client.get(
        f"/products/filter",
    )
    data_from_response = response.json()
    assert response.status_code == 422
    assert data_from_response == {'detail': [{'input': None,
             'loc': ['query', 'product_name'],
             'msg': 'Field required',
             'type': 'missing',
             'url': 'https://errors.pydantic.dev/2.5/v/missing'},
            {'input': None,
             'loc': ['query', 'max_sum'],
             'msg': 'Field required',
             'type': 'missing',
             'url': 'https://errors.pydantic.dev/2.5/v/missing'}]}

@pytest.mark.parametrize(
    "product_name, min_sum, max_sum, expected_status_code, expected_data",
    [
        (
            1,
            "a",
            "b",
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
async def test_get_products_using_filter_handler_422_mistakes(
    client,
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
    assert data_from_response == expected_data