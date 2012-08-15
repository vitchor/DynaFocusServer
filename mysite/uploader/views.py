from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import sys
import os
import cStringIO
import urllib
import boto
import Image
import _imaging
import random
import string

from uploader.models import User, FOF, Frame

def index(request):
    return render_to_response('uploader/index.html', {},
                               context_instance=RequestContext(request))
@csrf_exempt
def image(request):
    
    image = Image.open(cStringIO.StringIO(request.FILES['apiupload'].read()))
    
    out_image = cStringIO.StringIO()
    image.save(out_image, 'jpeg')
    
    #Connect to S3, with AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    conn = S3Connection('AKIAIFPFKLTD5HLWDI2A', 'zrCRXDSD3FKTJwJ3O5m/dsZstL/Ki0NyF6GZKHQi')
    
    #Gets information from post
    user_device_id = request.POST['device_id']
    frame_index = request.POST['frame_index']
    fof_name = request.POST['fof_name']
    fof_size = request.POST['fof_size']    
    
    try:
        frame_user = User.objects.get(device_id=user_device_id)
    except (KeyError, Choice.DoesNotExist):
        frame_user = User(name='', device_id=user_device_id)
        frame_user.save()
        
    try:
        frame_FOF = FOF.objects.get(name=fof_name)
    except (KeyError, Choice.DoesNotExist):
        frame_FOF = frame_user.fof_set.create(name = fof_name, size = fof_size)
        
    ###TODO###
    #Creates the image key with the following format:
    #frame_name = <device_id>_<fof_name>_<frame_index>.jpeg
    frame_name = device_id
    frame_name += '_'
    frame_name += fof_name
    frame_name += '_'
    frame_name += frame_index
    frame_name += '.jpeg'
        
    ###TODO###
    #Creates url:
    #frame_url = <s3_url>/<frame_name>
    frame_url = 'http://s3.amazonaws.com/dyfocus/'
    frame_url += frame_name
    
    frame = frame_FOF.frame_set.create(url=frame_url,index = frame_index)
    
    b = conn.get_bucket('dyfocus')
    k = b.new_key(frame_name)
    
    #Note we're setting contents from the in-memory string provided by cStringIO
    k.set_contents_from_string(out_image.getvalue())
    
    return render_to_response('uploader/index.html', {},
                               context_instance=RequestContext(request))