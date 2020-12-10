from chat.models import Clients

def remove_all_clients():
    print("Removing all cached clients")
    Clients.objects.all().delete()