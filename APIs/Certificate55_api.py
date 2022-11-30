#
# Copyright (c) 2017-2021, The Storage Networking Industry Association.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name of The Storage Networking Industry Association (SNIA) nor
# the names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
#  THE POSSIBILITY OF SUCH DAMAGE.

# Resource implementation for - /redfish/v1/Systems/{ComputerSystemId}/VirtualMedia/{VirtualMediaId}/ClientCertificates/{CertificateId}
# Program name - Certificate55_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Certificate55 import get_Certificate55_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Certificate55 Collection API
class Certificate55CollectionAPI(Resource):
	def __init__(self):
		logging.info('Certificate55 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ComputerSystemId, VirtualMediaId):
		logging.info('Certificate55 Collection get called')
		path = os.path.join(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates', 'index.json').format(ComputerSystemId, VirtualMediaId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ComputerSystemId, VirtualMediaId):
		logging.info('Certificate55 Collection post called')

		if request.data:
			config = json.loads(request.data)
			if "@odata.type" in config:
				if "Collection" in config["@odata.type"]:
					return "Invalid data in POST body", 400

		if VirtualMediaId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates').format(ComputerSystemId, VirtualMediaId)
		parent_path = os.path.dirname(path)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Certificate', parent_path)

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Certificate55API.post(self, ComputerSystemId, VirtualMediaId, os.path.basename(config['@odata.id']))
			else:
				return Certificate55API.post(self, ComputerSystemId, VirtualMediaId, str(res))
		else:
			return Certificate55API.post(self, ComputerSystemId, VirtualMediaId, str(res))

	# HTTP PUT Collection
	def put(self, ComputerSystemId, VirtualMediaId):
		logging.info('Certificate55 Collection put called')

		path = os.path.join(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates', 'index.json').format(ComputerSystemId, VirtualMediaId)
		put_object (path)
		return self.get(ComputerSystemId)

# Certificate55 API
class Certificate55API(Resource):
	def __init__(self):
		logging.info('Certificate55 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ComputerSystemId, VirtualMediaId, CertificateId):
		logging.info('Certificate55 get called')
		path = create_path(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates/{2}', 'index.json').format(ComputerSystemId, VirtualMediaId, CertificateId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ComputerSystemId, VirtualMediaId, CertificateId):
		logging.info('Certificate55 post called')
		path = create_path(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates/{2}').format(ComputerSystemId, VirtualMediaId, CertificateId)
		collection_path = os.path.join(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates', 'index.json').format(ComputerSystemId, VirtualMediaId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Certificate55CollectionAPI.post(self, ComputerSystemId, VirtualMediaId)

		if CertificateId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ComputerSystemId':ComputerSystemId, 'VirtualMediaId':VirtualMediaId, 'CertificateId':CertificateId, 'rb':g.rest_base}
			config=get_Certificate55_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Certificate55API POST exit')
		return resp

	# HTTP PUT
	def put(self, ComputerSystemId, VirtualMediaId, CertificateId):
		logging.info('Certificate55 put called')
		path = os.path.join(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates/{2}', 'index.json').format(ComputerSystemId, VirtualMediaId, CertificateId)
		put_object(path)
		return self.get(ComputerSystemId, VirtualMediaId, CertificateId)

	# HTTP PATCH
	def patch(self, ComputerSystemId, VirtualMediaId, CertificateId):
		logging.info('Certificate55 patch called')
		path = os.path.join(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates/{2}', 'index.json').format(ComputerSystemId, VirtualMediaId, CertificateId)
		patch_object(path)
		return self.get(ComputerSystemId, VirtualMediaId, CertificateId)

	# HTTP DELETE
	def delete(self, ComputerSystemId, VirtualMediaId, CertificateId):
		logging.info('Certificate55 delete called')
		path = create_path(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates/{2}').format(ComputerSystemId, VirtualMediaId, CertificateId)
		base_path = create_path(self.root, 'Systems/{0}/VirtualMedia/{1}/ClientCertificates').format(ComputerSystemId, VirtualMediaId)
		return delete_object(path, base_path)

