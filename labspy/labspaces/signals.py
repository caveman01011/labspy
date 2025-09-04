from django.db.models import Signal
from django.dispatch import reciever

my_signal = Signal()

@reciever(my_signal)
def my_signal_handlere(sender, **kwargs):
    print(f"Signal recieved from {sender}")