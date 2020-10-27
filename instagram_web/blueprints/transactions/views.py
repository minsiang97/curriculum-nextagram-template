from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from models.image import Image
from models.transaction import Transaction
import braintree
from app import TRANSACTION_SUCCESS_STATUSES, app
from decimal import Decimal
from flask_login import current_user
from helpers import gateway
import requests
from braintree.successful_result import SuccessfulResult

transactions_blueprint = Blueprint('transactions',
                            __name__,
                            template_folder='templates')



@transactions_blueprint.route('/new', methods = ["GET"])
def new_checkout(image_id):
    image = Image.get_or_none(Image.id == image_id)
    client_token = gateway.client_token.generate()
    return render_template('transactions/new.html',client_token = client_token, image = image)


@transactions_blueprint.route('/<transaction_id>', methods = ["GET"])
def show_checkout(image_id, transaction_id):
    image = Image.get_or_none(Image.id == image_id)
    transaction = gateway.transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES :
        result = {
            'header' : "Transaction Successful",
            'icon' : "success",
            'message' : "Your transaction has been successfully processed."
        }
    else :
        result = {
            'header' : "Transaction Failed",
            'icon' : "failed",
            'message' : "Your transaction cannot be processed"
        }
    return render_template("transactions/show.html", transaction = transaction, result = result, image = image)

@transactions_blueprint.route("/", methods=["POST"])
def create_checkout(image_id):
    image = Image.get_or_none(Image.id == image_id)
    nonce_from_the_client = request.form["payment_method_nonce"]
    result = gateway.transaction.sale({
    "amount": request.form['amount'],
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
    })
    if type(result) == SuccessfulResult:
        new_transaction = Transaction(donation_amount = request.form.get('amount'), image_id = image.id , user = current_user.id)
    
        if new_transaction.save():
            mailgun_api = app.config.get("MAILGUN_KEY") 
            requests.post(
                "https://api.mailgun.net/v3/sandbox81a71eab5677440880b5fcdad887e818.mailgun.org/messages",
		        auth=("api", mailgun_api),
		        data={"from": "Mailgun Sandbox <postmaster@sandbox81a71eab5677440880b5fcdad887e818.mailgun.org>",
			        "to": [current_user.name, "<ongminsiang@gmail.com>"],
			        "subject": "Hello!",
			        "text": "Successfully donated!"})

            return redirect(url_for('transactions.show_checkout', image_id = image.id, transaction_id=result.transaction.id ))

    else :
        return redirect(url_for('transactions.show_checkout', image_id = image.id, transaction_id=result.transaction.id ))    
    