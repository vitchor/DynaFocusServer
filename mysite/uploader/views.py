from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

# New imports
import sys
import os
import cStringIO
import urllib
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import Image
import _imaging
import random
import string



def index(request):
    return render_to_response('uploader/index.html', {},
                               context_instance=RequestContext(request))
@csrf_exempt
def image(request):
    #Retrieve our source image from a URL
    #fp = urllib.urlopen(request.POST['image_url'])

    #Load the URL data into an image
    #img = cStringIO.StringIO(fp.read())
    img = cStringIO.StringIO(request.FILES['apiupload'].read())
    im2 = Image.open(img)

    #NOTE, we're saving the image into a cStringIO object to avoid writing to disk
    out_im2 = cStringIO.StringIO()
    #You MUST specify the file type because there is no file name to discern it from
    im2.save(out_im2, 'jpeg')

    #Now we connect to our s3 bucket and upload from memory
    #credentials stored in environment AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    conn = S3Connection('AKIAIFPFKLTD5HLWDI2A', 'zrCRXDSD3FKTJwJ3O5m/dsZstL/Ki0NyF6GZKHQi')

    #Connect to bucket and create key
    
    #CSegments = .rpartition('/')
    
    b = conn.get_bucket('dyfocus')
    k = b.new_key(request.POST['data'])

    #Note we're setting contents from the in-memory string provided by cStringIO
    k.set_contents_from_string(out_im2.getvalue())
    return render_to_response('uploader/index.html', {},
                               context_instance=RequestContext(request))