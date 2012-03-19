#!/usr/bin/env python
import pycurl
import StringIO
import urllib
import json

class JiraRestClient(object):
	def __init__(self, base_uri, username=None, password=None):
		self.base_uri = base_uri
		self.username = username
		self.password = password

	def get_basic_pycurl_connection(self):
		""" Returns: A pycurl object and an associated StringIO object. """
		_string_io = StringIO.StringIO()
		_connection = pycurl.Curl()
		_connection.setopt(pycurl.SSL_VERIFYPEER, 1)
		_connection.setopt(pycurl.SSL_VERIFYHOST, 2)
		_connection.setopt(pycurl.SSLVERSION, 3)
		_connection.setopt(pycurl.FOLLOWLOCATION, False)
		_connection.setopt(pycurl.WRITEFUNCTION, _string_io.write)
		return _connection, _string_io

	def setup_basic_authed_pycurl_connection(self):
		""" creates a basic pycurl object and adds basic auth info
		    if a username and password have been provided.
		    Returns: A pycurl object and an associated StringIO object.
		"""
		_connection, _string_io = self.get_basic_pycurl_connection()
		if self.username is not None and self.password is not None:
			_connection.setopt(pycurl.USERPWD, "%s:%s" % \
				(urllib.quote(self.username), \
				urllib.quote(self.password)) )
		return _connection, _string_io

	def fetch(self, uri, post_data=None, _connection=None):
		""" XXX: write methods that use this method! """
		if _connection is None:
			_connection, _string_io = self.setup_basic_authed_pycurl_connection()
		_string_io = StringIO.StringIO()
		_connection.setopt(pycurl.WRITEFUNCTION, _string_io.write )
		_connection.setopt(pycurl.URL, uri)
		_connection.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'] )

		if post_data is not None:
			post_data = json.dumps(post_data)
			_connection.setopt(pycurl.POSTFIELDS, post_data)

		_connection.perform()

		return _string_io.getvalue()

