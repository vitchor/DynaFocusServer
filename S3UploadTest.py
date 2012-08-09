#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Victor Oliveira on 2012-08-09.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.

Access Key ID = AKIAIFPFKLTD5HLWDI2A
Secret Access Key = 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
"""

import sys
import os
import cStringIO
import urllib
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import Image
import _imaging

def main():
	pass


if __name__ == '__main__':
	main()
	
	print('- Code Started -')
	
	#Creates a connection
	conn = S3Connection('AKIAIFPFKLTD5HLWDI2A', 'zrCRXDSD3FKTJwJ3O5m/dsZstL/Ki0NyF6GZKHQi')
	
	#Gets the bucket 
	bucket = conn.create_bucket('dyfocus')
	
	# Creates a key (hardcoded: TODO)
	k = Key(bucket)
	k.key = 'foobar'
	k.set_contents_from_string('Test was OK')
	
	print("- Added Value -")



	print("Testing Results...")
	
	c = S3Connection('AKIAIFPFKLTD5HLWDI2A', 'zrCRXDSD3FKTJwJ3O5m/dsZstL/Ki0NyF6GZKHQi')
	b = c.create_bucket('dyfocus')
	k = Key(b)
	k.key = 'foobar'
	
	print(k.get_contents_as_string())



	print("Uploading Image...")
		
	#Retrieve our source image from a URL
	fp = urllib.urlopen('http://h11.hostseguro.com/~wwwbiom/images/icone_email.png')
	
	#Load the URL data into an image
	img = cStringIO.StringIO(fp.read())
	im2 = Image.open(img)
	
	#NOTE, we're saving the image into a cStringIO object to avoid writing to disk
	out_im2 = cStringIO.StringIO()
	#You MUST specify the file type because there is no file name to discern it from
	im2.save(out_im2, 'PNG')
	
	#Now we connect to our s3 bucket and upload from memory
	#credentials stored in environment AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
	conn = S3Connection('AKIAIFPFKLTD5HLWDI2A', 'zrCRXDSD3FKTJwJ3O5m/dsZstL/Ki0NyF6GZKHQi')

	#Connect to bucket and create key
	b = conn.get_bucket('dyfocus')
	k = b.new_key('marceloChamine.png')
	
	#Note we're setting contents from the in-memory string provided by cStringIO
	k.set_contents_from_string(out_im2.getvalue())
	
	print('- Code Ended -')

