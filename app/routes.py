import json
import os
from flask import jsonify, request
from flask_openapi3 import APIBlueprint
from flasgger import  swag_from
from models.pipeline import Pipeline
from models.preprocessador import PreProcessador
from pydantic import ValidationError
from models.transaction import Transaction
from schemas.transaction import MappingDictSchema, TransactionSchema, TransactionListResponse, TransactionDelSchema
from app import db

pipeline = Pipeline()
preprocessador = PreProcessador()

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
                'age': transaction.age,
                'sex': transaction.sex,
                'chest_pain_type': transaction.chest_pain_type,
                'resting_bp': transaction.resting_bp,
                'cholesterol': transaction.cholesterol,
                'fasting_bs': transaction.fasting_bs,
                'resting_ecg': transaction.resting_ecg,
                'max_hr': transaction.max_hr,
                'exercise_angina': transaction.exercise_angina,
                'oldpeak': transaction.oldpeak,
                'st_slope': transaction.st_slope,
                'heart_disease': transaction.heart_disease,
                'created_at': transaction.created_at,
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
                        'age': {
                            'type': 'integer',
                            'description': 'Age of the person involved in the transaction',
                            'example': 45
                        },
                        'sex': {
                            'type': 'integer',
                            'description': 'Sex of the person involved in the transaction',
                            'example': 1
                        },
                        'chest_pain_type': {
                            'type': 'integer',
                            'description': 'Type of chest pain experienced',
                            'example': 1,
                        },
                        'resting_bp': {
                            'type': 'integer',
                            'description': 'Resting blood pressure in mm Hg',
                            'example': 130
                        },
                        'cholesterol': {
                            'type': 'integer',
                            'description': 'Serum cholesterol in mg/dl',
                            'example': 233
                        },
                        'fasting_bs': {
                            'type': 'integer',
                            'description': 'Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)',
                            'example': 1
                        },
                        'resting_ecg': {
                            'type': 'integer',
                            'description': 'Resting electrocardiographic results',
                            'example': 1,
                        },
                        'max_hr': {
                            'type': 'integer',
                            'description': 'Maximum heart rate achieved',
                            'example': 150
                        },
                        'exercise_angina': {
                            'type': 'integer',
                            'description': 'Exercise induced angina (Y = Yes; N = No)',
                            'example':  1,
                        },
                        'oldpeak': {
                            'type': 'integer',
                            'description': 'ST depression induced by exercise relative to rest',
                            'example': 1
                        },
                        'st_slope': {
                            'type': 'integer',
                            'description': 'The slope of the peak exercise ST segment',
                            'example': 1,
                        }
                    },
                    'required': [
                        'age', 'sex', 'chest_pain_type', 'resting_bp', 'cholesterol',
                        'fasting_bs', 'resting_ecg', 'max_hr', 'exercise_angina',
                        'oldpeak', 'st_slope'
                    ]
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

    # Preparando os dados para o pipeline
    X_input = PreProcessador.preparar_form(data)
    # Carregando pipeline
    pipeline_path = './machine-learning/pipelines/knn_norm.pkl'
    pipeline = Pipeline.carrega_pipeline(pipeline_path)
    heart_disease = int(Pipeline.preditor(pipeline, X_input)[0])

    try:
        # Validate through TransactionSchema
        transaction_data = TransactionSchema(**data)
        transaction = Transaction(**transaction_data.model_dump(), heart_disease=heart_disease)
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

@api.get('/mapping',responses={200: MappingDictSchema})
def get_mapping():
    """
    Get the mapping dictionary for text-to-numeric transformation.

    This endpoint retrieves the mapping dictionary used for transforming text values into numeric values.

    ---
    tags:
        - Mapping
    responses:
      200:
        description: Mapping dictionary
        content:
          application/json:
            schema:
              type: object
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
        current_dir = os.path.dirname(__file__)
        mapping_dict_path = os.path.join(current_dir, 'mapping_dict.json')
        # Carrega o dicionario do arquivo json
        with open(mapping_dict_path, 'r') as file:
            mapping_dict = json.load(file)

        return jsonify(mapping_dict), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500