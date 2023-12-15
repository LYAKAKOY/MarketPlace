import json

import pytest


@pytest.mark.parametrize(
    "product_data, expected_status_code",
    [
        (
            {
                "id_company": 0,
                "product_name": "MSI GTX 3600TI",
                "description": "Video card for desktop computer",
                "category": "pc",
                "sum": 40000,
            },
            200,
        ),
        (
            {
                "id_company": 1,
                "product_name": "Milk 900ml",
                "description": "",
                "category": "dairy product",
                "sum": 100,
            },
            200,
        ),
    ],
)
async def test_create_product_handler(
    client,
    product_data,
    expected_status_code,
):
    response = await client.post(
        "/products/",
        content=json.dumps(product_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response["id_company"] == product_data["id_company"]
    assert data_from_response["product_name"] == product_data["product_name"]
    assert data_from_response["description"] == product_data["description"]
    assert data_from_response["category"] == product_data["category"]
    assert data_from_response["sum"] == product_data["sum"]


@pytest.mark.parametrize(
    "product_data, expected_status_code",
    [
        (
            {
                "id_company": 0,
                "product_name": "MSI GTX 3600TI",
                "description": "Video card for desktop computer",
                "category": "pc",
                "sum": 40000,
                "parameter": {"type": "gaming", "chip": "nvidia"},
            },
            200,
        ),
        (
            {
                "id_company": 1,
                "product_name": "Milk 900ml",
                "description": "",
                "category": "dairy product",
                "sum": 100,
                "parameter": {"volume": "900ml", "manufacturer": "OOO Milk"},
            },
            200,
        ),
    ],
)
async def test_create_product_with_new_parameter_handler(
    client,
    product_data,
    expected_status_code,
):
    response = await client.post(
        "/products/",
        content=json.dumps(product_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response["id_company"] == product_data["id_company"]
    assert data_from_response["product_name"] == product_data["product_name"]
    assert data_from_response["description"] == product_data["description"]
    assert data_from_response["category"] == product_data["category"]
    assert data_from_response["sum"] == product_data["sum"]
    assert data_from_response["parameter"] == product_data["parameter"]


@pytest.mark.parametrize(
    "product_data, expected_status_code",
    [
        (
            {
                "parameter": {"type": "gaming", "chip": "nvidia"},
            },
            422,
        ),
        (
            {
                "parameter": {"volume": "900ml", "manufacturer": "OOO Milk"},
            },
            422,
        ),
        (
            {},
            422,
        ),
    ],
)
async def test_create_product_without_required_parameters_handler(
    client,
    product_data,
    expected_status_code,
):
    response = await client.post(
        "/product/",
        content=json.dumps(product_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == {
        "detail": [
            {
                "input": product_data,
                "loc": ["body", "id_company"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": product_data,
                "loc": ["body", "product_name"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": product_data,
                "loc": ["body", "description"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": product_data,
                "loc": ["body", "category"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
            {
                "input": product_data,
                "loc": ["body", "sum"],
                "msg": "Field required",
                "type": "missing",
                "url": "https://errors.pydantic.dev/2.5/v/missing",
            },
        ]
    }
