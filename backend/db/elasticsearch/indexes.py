MAPPING_FOR_INDEX_PRODUCTS = {
            "properties": {
                "id_company": {
                    "type": "integer",
                },
                "product_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "description": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "category": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword"
                        }
                    }
                },
                "sum": {
                    "type": "integer",
                },
            }
        }

all_indexes = {
    "products": MAPPING_FOR_INDEX_PRODUCTS,
}