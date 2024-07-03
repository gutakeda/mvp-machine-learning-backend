from flask import jsonify, request
from flask_openapi3 import APIBlueprint
from flasgger import  swag_from
from pydantic import ValidationError
from models.category import Category
from models.transaction import Transaction
from schemas.category import CategoryViewSchema, CategoriesListResponse
from schemas.transaction import TransactionSchema, TransactionListResponse, TransactionDelSchema
from app import db

api = APIBlueprint('api', __name__, url_prefix='/api')

@api.get('/transactions', responses={"200": TransactionListResponse})
def list_transactions():
    """
    List transactions.

    This endpoint retrieves all transactions, ordered by creation date.

    ---
    tags:
        - Transaction
    parameters:
      - name: order_by
        in: query
        required: false
        description: Order transactions by 'asc' or 'desc'
        schema:
          type: string
    responses:
      200:
        description: A list of transactions
        content:
          application/json:
            schema: TransactionListResponse
      400:
        description: Invalid order_by parameter
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    try:
       # Order by 'asc' if param is not provided
        order_by = request.args.get('order_by', 'asc')

        if order_by == 'asc':
            order_clause = Transaction.created_at.asc()
        elif order_by == 'desc':
            order_clause = Transaction.created_at.desc()
        else:
            return jsonify({'error': 'Invalid order_by parameter. Use "asc" or "desc".'}), 400

        transactions = Transaction.query.order_by(order_clause).all()

        transactions_list = [
            {
                'id': transaction.id,
                'title': transaction.title,
                'type': transaction.type,
                'amount': float(transaction.amount),
                'category_id': transaction.category_id,
                'created_at': transaction.created_at,
                'category': transaction.category.name,
            } for transaction in transactions
        ]

        return jsonify(transactions_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.post('/transaction', responses={"200": TransactionSchema})
@swag_from({
    'summary': 'Creates transaction.',
    'description': 'This endpoint creates a new transcation.',
    'tags': ['Transaction'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'description': 'Title of the transaction',
                        'example': 'Grocery shopping'
                    },
                    'type': {
                        'type': 'string',
                        'description': 'Type of the transaction (\'withdraw\' or \'deposit\')',
                        'example': 'withdraw'
                    },
                    'amount': {
                        'type': 'number',
                        'format': 'decimal',
                        'description': 'Amount of the transaction',
                        'example': 50.75
                    },
                    'category_id': {
                        'type': 'integer',
                        'description': 'ID of the category',
                        'example': 1
                    }
                },
                'required': ['title', 'type', 'amount', 'category_id']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Transaction created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        },
        '400': {
            'description': 'Validation error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string'
                    }
                }
            }
        },
        '500': {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def create_transaction():
    data = request.get_json()
    try:
        # Validate through TransactionSchema
        transaction_data = TransactionSchema(**data)
        transaction = Transaction(**transaction_data.model_dump())
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"message": "Transaction added successfully"}), 200

    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.delete('/transaction/<int:transaction_id>', responses={200: TransactionDelSchema})
def delete_transaction(path: TransactionDelSchema):
    """
    Delete a transaction.

    This endpoint deletes a transaction specified by its ID.

    ---
    tags:
        - Transaction
    parameters:
      - name: transaction_id
        in: path
        required: true
        description: ID of the transaction to be deleted
        schema:
          type: integer
    responses:
      200:
        description: Transaction successfully deleted
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      404:
        description: Transaction not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    try:
        transaction_id = path.transaction_id
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404

        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction successfully deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.get('/categories', responses={"200": CategoriesListResponse})
def list_categories():
    """
    List categories with total amounts.

    This endpoint retrieves all categories and calculates the total amount for each category.

    ---
    tags:
        - Category
    responses:
      200:
        description: A list of categories with total amounts
        content:
          application/json:
            schema: CategoriesListResponse
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    try:
        categories = Category.query.all()
        categories_list = []

        for category in categories:
            # Calculate total amount for each category
            transactions = Transaction.query.filter_by(category_id=category.id).all()
            total_amount = 0
            for transaction in transactions:
                if transaction.type == 'withdraw':
                    total_amount -= transaction.amount
                elif transaction.type == 'deposit':
                    total_amount += transaction.amount

            category_data = {
                'id': category.id,
                'name': category.name,
                'total_amount': total_amount
            }
            categories_list.append(category_data)
        return jsonify(categories_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.post('/category', responses={"200": CategoryViewSchema})
@swag_from({
    'summary': 'Creates category.',
    'description': 'This endpoint creates a new category.',
    'tags': ['Category'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Name of the category',
                        'example': 'Food'
                    }
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Category created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    }
                }
            }
        },
        '400': {
            'description': 'Missing name parameter',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string'
                    }
                }
            }
        },
        '500': {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string'
                    }
                }
            }
        }
    }
})
def create_category():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'error': 'Missing name parameter'}), 400

    name = data['name']
    new_category = Category(name=name)

    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Category created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500