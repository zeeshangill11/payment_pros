from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from django.urls import reverse

from .filters import TransactionFilter

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import requests

import json
import base64

def transaction_list(request):


    # BlueSnap API endpoint for tokenization
    api_url = 'https://sandbox.bluesnap.com/services/2/payment-fields-tokens'

    # BlueSnap API credentials
    username = 'API_16872799899141798439898'
    password = 'Findaway11!$'

    # Credit card details
    card_number = '4111111111111111'
    expiration_month = '12'
    expiration_year = '2025'
    cvv = '123'

    # Prepare the request payload
    payload = {
        'number': card_number,
        'expMonth': expiration_month,
        'expYear': expiration_year,
        'cvv': cvv
    }

    # Send the request
    response = requests.post(api_url, data=json.dumps(payload), auth=(username, password))
    print("====================");
    print(response.text);
    print("<<<======================");
    # Check the response status code
    if response.status_code == 200:
        # Extract the token from the response
        token = response.json().get('paymentFieldsTokens', {}).get('paymentFieldsTokenId')
        print('Token2222222222:', token)
    else:
        # Handle the error
        print('Error:', response.text)


    transactions = Transaction.objects.all()

    form = TransactionForm(request.POST)
    
    transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.all())

    return render(request, 'transactions/transaction_list.html', {'transactions': transactions,'filter': transaction_filter ,'form':form})

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('transactions:transaction_list'))
    else:
        form = TransactionForm()
    button_text = "Add Transaction"
    return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text})


def transaction_create_ajax(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():

            # Retrieve the dynamic values from the form
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            amount = form.cleaned_data['amount']
            zip_code = form.cleaned_data['zip_code']
            card_number = form.cleaned_data['card_number']
            exp_month = form.cleaned_data['exp_month']
            exp_year = form.cleaned_data['exp_year']
            cvv = form.cleaned_data['cvv']

            url = "https://sandbox.bluesnap.com/services/2/transactions"


            username = 'API_16872799899141798439898'
            password = 'Findaway11!$'

            # Encode the username and password
            credentials = f'{username}:{password}'
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            print(encoded_credentials)

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Basic {encoded_credentials}',
                'bluesnap-version': '3.0',
                'Cookie': 'JSESSIONID=4DE670BDBB9367ECEC24FE4E3733CED0; TS0157275e=018b1f380ba76b438611e3dcc76ccee03c26cd38799e263e55c7722e70322357109b6f60bec79c1b4683b85c005f59f6607206e6818027fcee0fac59a8948d0e064fd37706; TS01dbdafe=018b1f380bac5d9673236c5c75a8112797c469b1ad93a48c1bfb2ccd7c0448a3a42a2c2c691f8c15f16b0e199ed3224d658c766230'
            }

            payload = {
                "amount": amount,
                "softDescriptor": "DescTest",
                "cardHolderInfo": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "zip": zip_code
                },
                "currency": "USD",
                "creditCard": {
                    "expirationYear": exp_year,
                    "securityCode": cvv,
                    "expirationMonth": exp_month,
                    "cardNumber": card_number
                },
                "cardTransactionType": "AUTH_CAPTURE"
            }


            # Convert the payload to JSON string
            payload_json = json.dumps(payload)

            response = requests.post(url, headers=headers, data=payload_json)

            response_text = response.text
            print(response_text)

            response_json = json.loads(response_text)
            transaction_id = response_json.get('transactionId')

            if transaction_id is not None:
                print(f"Transaction ID: {transaction_id}")
                #token = response_json['creditCard']['token']
                #form.instance.credit_card_number = token  # Store the token in the credit_card_number field
                form.instance.transaction_id = str(transaction_id)
                form.save()
                return JsonResponse({'success': True})

            else:
                print(response_text)
                description = response_json.get('message')
                print("Transaction ID not found.")
                return JsonResponse({'success': False, 'errors': form.errors, 'message': response_text})

        else:
            return JsonResponse({'success': False, 'errors': form.errors, 'message': 'aaaa'})
    else:
        form = TransactionForm()
        button_text = "Add Transaction"



def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST or None, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect(reverse('transactions:transaction_list'))
    else:
        form = TransactionForm(instance=transaction)
    button_text = "Update Transaction"
    return render(request, 'transactions/transaction_form.html', {'form': form, 'button_text': button_text})


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect(reverse('transactions:transaction_list'))
    return render(request, 'transactions/transaction_confirm_delete.html', {'transaction': transaction})


@api_view(['POST'])

def add_api_record(request):
    token = request.data.get('token')
    if token == 'dyno@123':
        # Extract the transaction data from the request
        transaction_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'company': request.data.get('company'),
            'address': request.data.get('address', ''),  # Use default value if not provided in the request
            'city': request.data.get('city'),
            'state': request.data.get('state'),
            'zip_code': request.data.get('zip_code'),
            'country': request.data.get('country'),
            'phone_number': request.data.get('phone_number'),
            'amount': request.data.get('amount'),
            'payment_method': request.data.get('payment_method'),
            'transaction_type': request.data.get('transaction_type'),
            'card_number': request.data.get('card_number'),
            'exp_date': request.data.get('exp_date'),
            'cvv': request.data.get('cvv'),
            'email': request.data.get('email'),
        }

        # Create a new transaction record
        transaction = Transaction.objects.create(**transaction_data)

        # Return a success response
        return Response({'message': 'Transaction added successfully'})
    else:
    # Return an error response if the token is invalid
        return Response({'error': 'Invalid token'}, status=401)


