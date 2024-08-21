from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import logging
import razorpay
from django.conf import settings

@csrf_exempt
def order_payment(request):
    amount = 200  # Amount in INR
    client = razorpay.Client(auth=('rzp_test_OJWc1xRotti82Y', 'iFnUSeG5AWKVVxaFjlNfVebi'))

    data = {
        "amount": amount * 100,  # Amount in paise
        "currency": "INR",
        "payment_capture": 1
    }

    try:
        # Print request data for debugging
        logging.debug(f"Creating order with data: {data}")

        # Create order with Razorpay
        razorpay_order = client.order.create(data=data)

        # Print response data for debugging
        logging.debug(f"Order created: {razorpay_order}")

    except razorpay.errors.BadRequestError as e:
        pass
        # logging.error(f"Error creating order: {e}")
        # return render(request, "error.html", {'error': str(e)})

    return render(request, "index.html", {'razorpay_order': data})




def verify_payment(request):
    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('razorpay_order_id')
    signature = request.POST.get('razorpay_signature')

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        # Payment is verified
        return HttpResponse('Payment verified successfully')
    except razorpay.errors.SignatureVerificationError:
        # Signature verification failed
        return HttpResponse('Payment verification failed', status=400)