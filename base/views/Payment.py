from django.shortcuts import render
import razorpay
from django.conf import settings
from base.models import FolderManager, UserSubscription, PaymentDb
from django.http import HttpResponseBadRequest

def cost_course(request, folder_id):
    folder = FolderManager.objects.get(id=folder_id)
    amount = folder.cost * 100
    print(folder,folder.id,folder.description, folder.FolderName, str(folder.path)+"."+str(folder.FolderName))
    print("amount",amount)
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        # auth=("rzp_test_9ZBBHFD0ZPBpL6", "GkUxYA80oP3EG4FcC24R94l0"))
    payment = client.order.create({'amount': amount, 'currency': 'INR',
                                   'payment_capture': '1'})
    print(payment)
    return render(request, 'Payment/view_product.html', {'folder':folder,'amount': amount, 'key':settings.RAZORPAY_KEY_ID, 'payment':payment,'path':str(folder.path)+"."+str(folder.FolderName)})

def success(request, path):
    if request.method == 'POST':
        # Use request.POST to directly access form data
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        try:
            payment, created = PaymentDb.objects.get_or_create(
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                razorpay_signature=razorpay_signature
            )
        except:
            print("Error at payment Db..")
        
        print(razorpay_order_id, razorpay_payment_id, razorpay_signature)
        
        try:
            print("start loading...!")
            print(razorpay_order_id, razorpay_payment_id, razorpay_signature)

            # Rest of your code for payment verification and subscription creation
            verify = verify_and_process_payment(request, path, razorpay_order_id, razorpay_payment_id, razorpay_signature)

            if verify:
                return render(request, 'Payment/payment_sucess.html',  {'path': path})
            else:
                return HttpResponseBadRequest("Payment verification failed in inner..!")
                

        except Exception as e:
            print("Unexpected error:", e)
            return HttpResponseBadRequest("Payment verification failed")

    else:
        return HttpResponseBadRequest("403 Error")
        


def verify_and_process_payment(request,path, razorpay_order_id, razorpay_payment_id, razorpay_signature):
    # Replace 'YOUR_RAZORPAY_KEY_ID' and 'YOUR_RAZORPAY_KEY_SECRET' with your actual Razorpay API key credentials
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    try:
        # Verify the payment signature
        print("Payment verification start in the function...", path)
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        print("verify_payment_signature verifyed...!")
        # Payment verification succeeded, process the payment and create the subscription
        print("request is updated...!")

        # Assuming you have a User model and 'path' corresponds to 'course_premium'
        user_subscription, created = UserSubscription.objects.get_or_create(
            user_id=request.user,  # Assuming 'request' contains the current user
            course_premium=path  # Adjust based on your model fields
        )
        
        # to update the validity
        
        # obj = FolderManager.objects.get(category=path.split('.')[1])
        # # Assuming you have a User model and 'path' corresponds to 'course_premium'
        # user_subscription, created = UserSubscription.objects.get_or_create(
        #     user_id=request.user,  # Assuming 'request' contains the current user
        #     course_premium=path,  # Adjust based on your model fields
        #     validity_days = obj.validity_days
        # )
        
        # for i in obj:
        #     print(i.user_id, i.course_premium)

        print("user_subscription created")

        if created:
            print("User Created...!")
            try:
                obj = UserSubscription.objects.all()
                print(path,request.user)
                print(user_subscription.user.id, user_subscription.course_premium)
            except Exception as e:
                print(e)

        # Add any additional logic for updating fields or creating related records
        return True


    except razorpay.errors.SignatureVerificationError as e:
        # Signature verification failed
        return False
    
    