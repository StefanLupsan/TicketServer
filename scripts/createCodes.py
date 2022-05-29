import qrcode
import numpy as np
from PIL import Image
from ticketdb.models import AfterTicket
from ticketdb.models import PromTicket


def run():
    # img = Image.open('TicketTemplates/bal_bilet.png')
    for i in PromTicket.objects.all():
        qr = qrcode.make(i.qr_link)
        qr.save("{0}.png".format('PROMQRCODES/' + i.name))
        # img_qr = qr.make_image()
        # pos = (img.size[0])
    # img = Image.open('TicketTemplates/after_bilet.png')
    for i in AfterTicket.objects.all():
        qr = qrcode.make(i.qr_link)
        qr.save("{0}.png".format('AFTERQRCODES/' + i.name))
