from rest_framework.decorators  import  api_view
@api_view(["POST"])
def add_transaction(request)