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

# Resource implementation for - /redfish/v1/ResourceBlocks/{ResourceBlockId}/Systems/{ComputerSystemId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Certificates/{CertificateId}
# Program name - Certificate42_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Certificate42 import get_Certificate42_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Certificate42 Collection API
class Certificate42CollectionAPI(Resource):
	def __init__(self):
		logging.info('Certificate42 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId):
		logging.info('Certificate42 Collection get called')
		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates', 'index.json').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId):
		logging.info('Certificate42 Collection post called')

		if request.data:
			config = json.loads(request.data)
			if "@odata.type" in config:
				if "Collection" in config["@odata.type"]:
					return "Invalid data in POST body", 400

		if StorageControllerId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId)
		parent_path = os.path.dirname(path)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Certificate', parent_path)

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Certificate42API.post(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, os.path.basename(config['@odata.id']))
			else:
				return Certificate42API.post(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, str(res))
		else:
			return Certificate42API.post(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, str(res))

	# HTTP PUT Collection
	def put(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId):
		logging.info('Certificate42 Collection put called')

		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates', 'index.json').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId)
		put_object (path)
		return self.get(ResourceBlockId)

# Certificate42 API
class Certificate42API(Resource):
	def __init__(self):
		logging.info('Certificate42 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate42 get called')
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates/{4}', 'index.json').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate42 post called')
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates/{4}').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)
		collection_path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates', 'index.json').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Certificate42CollectionAPI.post(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId)

		if CertificateId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ResourceBlockId':ResourceBlockId, 'ComputerSystemId':ComputerSystemId, 'StorageId':StorageId, 'StorageControllerId':StorageControllerId, 'CertificateId':CertificateId, 'rb':g.rest_base}
			config=get_Certificate42_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Certificate42API POST exit')
		return resp

	# HTTP PUT
	def put(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate42 put called')
		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates/{4}', 'index.json').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)
		put_object(path)
		return self.get(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)

	# HTTP PATCH
	def patch(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate42 patch called')
		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates/{4}', 'index.json').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)
		patch_object(path)
		return self.get(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)

	# HTTP DELETE
	def delete(self, ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate42 delete called')
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates/{4}').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId, CertificateId)
		base_path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/Storage/{2}/Controllers/{3}/Certificates').format(ResourceBlockId, ComputerSystemId, StorageId, StorageControllerId)
		return delete_object(path, base_path)

