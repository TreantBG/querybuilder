from querybuilder import filters
from querybuilder.rules import Rule


class SomeFilters(filters.Filters):
    def __init__(self, item):
        self.item = item

    def add_dynamically_param(self, filter_type, filter_params):
        @filter_type(**filter_params)
        def dynamic_param(id):
            return self.item[id]


rule_1 = Rule({
    "condition": "AND",
    "rules": [
        {
            "id": "price",
            "field": "price",
            "type": "double",
            "input": "number",
            "operator": "less",
            "value": "10.25"
        },
        {
            "id": "id",
            "field": "id",
            "type": "string",
            "input": "select",
            "operator": "equal",
            "value": "abcd-1234-de56"
        },
        {
            "condition": "OR",
            "rules": [
                {
                    "id": "name",
                    "field": "name",
                    "type": "string",
                    "input": "select",
                    "operator": "equal",
                    "value": "1"
                },
                {
                    "id": "category",
                    "field": "category",
                    "type": "integer",
                    "input": "select",
                    "operator": "equal",
                    "value": "2"
                },

            ]
        }
    ],
    "valid": True
})

if __name__ == '__main__':
    item = {'price': 10,
            'name': '1',
            'category': 1,
            'in_stock': 'True',
            'id': 'abcd-1234-de56'
            }

    some_filters = SomeFilters(item)

    mongo_filters = {
        'id': {
            'type': 'string',
            'params': {
                'id': 'id',
                'label': 'Identifier',
                'type': 'string',
                'placeholder': '____-____-____',
                'operators': ['equal', 'not_equal'],
                'validation': {'format': '/^.{4}-.{4}-.{4}$/'}
            }
        },
        'category': {
            'type': 'integer',
            'params': {
                'id': 'category',
                'label': 'Category',
                'type': 'integer',
                'input': 'select',
                'values': {
                    1: 'Books',
                    2: 'Movies',
                    3: 'Music',
                    4: 'Tools',
                    5: 'Goodies',
                    6: 'Clothes'
                },
                'operators': ['equal', 'not_equal', 'in', 'not_in', 'is_null', 'is_not_null']
            }
        },
        'name': {
            'type': 'string',
            'params': {
                'id': 'name',
                'label': 'Name',
                'type': 'string'
            }
        },
        'in_stock': {
            'type': 'boolean',
            'params': {
                'id': 'in_stock',
                'label': 'In stock',
                'type': 'integer',
                'input': 'radio',
                'values': {
                    1: 'Yes',
                    0: 'No'
                },
                'operators': ['equal']
            }
        },
        'price': {
            'type': 'numeric',
            'params': {
                'id': 'price',
                'label': 'Price',
                'type': 'double',
                'validation': {
                    'min': 0,
                    'step': 0.01
                }
            }
        }
    }

    filters = {
        'integer': filters.IntegerFilter,
        'string': filters.StringFilter,
        'boolean': filters.BooleanFilter,
        'numeric': filters.NumericFilter
    }

    for filter_name in mongo_filters:
        filter_type = filters[mongo_filters[filter_name]['type']]
        filter_params = mongo_filters[filter_name]['params']

        some_filters.add_dynamically_param(filter_type, filter_params)

    print(rule_1.is_valid(some_filters))
