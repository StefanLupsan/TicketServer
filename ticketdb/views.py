import cv2
import numpy as np
import io
import base64


from PIL import Image
from scripts.camClass import VideoCamera
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from pyzbar.pyzbar import decode
from ticketdb.models import PromTicket
from ticketdb.models import AfterTicket


cam = VideoCamera()


def recieve_image(request):
    if request.method == 'POST':
        form = request.POST['photo']
        split = form.split(",")[1]
        decoded = base64.b64decode(split)
        qrdata = decoder(decoded)
    if(qrdata == None):
        return HttpResponse("Empty")
    for ticket in PromTicket.objects.all():
        if qrdata == ticket.qr_link:
            ticket.is_valid = ticket.is_valid - 1
            ticket.save()
            return HttpResponse("Name: {0} Age: {1} Valid {2}".format(ticket.name, ticket.age, ticket.is_valid + 1))
    for ticket in AfterTicket.objects.all():
        if qrdata == ticket.qr_link:
            ticket.is_valid = ticket.is_valid - 1
            ticket.save()
            return HttpResponse("Name: {0} Age: {1} Valid {2}".format(ticket.name, ticket.age, ticket.is_valid + 1))


def get_log(request):
    global cam
    frame = cam.get_frame()
    qrdata = decoder(frame)
    for ticket in PromTicket.objects.all():
        if qrdata == ticket.qr_link:
            return HttpResponse("Name: {0} Adult: {1} Valid {2}".format(ticket.name, ticket.age, ticket.is_valid))
    for ticket in AfterTicket.objects.all():
        if qrdata == ticket.qr_link:
            return HttpResponse("Name: {0} Adult: {1} Valid {2}".format(ticket.name, ticket.age, ticket.is_valid))


def index(request):
    return render(request, 'ticketdb/index.html')


def decoder(image):
    image = cv2.cvtColor(np.array(Image.open(io.BytesIO(image))), cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img)

    for obj in barcode:
        points = obj.polygon
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        return obj.data.decode("utf-8")


def gen(camera):
    while True:
        image = camera.get_image()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')


@gzip.gzip_page
def video_feed(request):
    global cam
    try:
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:  # This is bad! replace it with proper handling
        print(e)



