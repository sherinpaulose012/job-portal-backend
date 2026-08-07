import uuid


class PaymentService:

    @staticmethod
    def create_order(amount):
        return {
            "order_id": str(uuid.uuid4()),
            "amount": amount,
            "currency": "INR",
            "status": "created"
        }

    @staticmethod
    
    def verify_payment(payment_id, signature):

        if not payment_id or not signature:
            return False

        if signature.startswith("pay_"):
            return True

        return False

    @staticmethod
    def capture_payment(payment_id):
        return {
            "payment_id": payment_id,
            "status": "captured"
        }