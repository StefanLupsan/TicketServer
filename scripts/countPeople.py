from ticketdb.models import PromTicket
from ticketdb.models import AfterTicket

def run():
    promcount = 0
    for ticket in PromTicket.objects.all():
        if ticket.is_valid < 1:
            promcount += 1
    aftercount = 0
    for ticket in AfterTicket.objects.all():
        if ticket.is_valid < 1:
            aftercount += 1
    print("Number of people at prom: {0}".format(promcount), end='')
    print("Number of people at after: {0}".format(aftercount))
