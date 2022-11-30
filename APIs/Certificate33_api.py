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

# Resource implementation for - /redfish/v1/CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/StorageControllers/{StorageControllerId}/Certificates/{CertificateId}
# Program name - Certificate33_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Certificate33 import get_Certificate33_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Certificate33 Collection API
class Certificate33CollectionAPI(Resource):
	def __init__(self):
		logging.info('Certificate33 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ResourceBlockId, StorageId, StorageControllerId):
		logging.info('Certificate33 Collection get called')
		path = os.path.join(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates', 'index.json').format(ResourceBlockId, StorageId, StorageControllerId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ResourceBlockId, StorageId, StorageControllerId):
		logging.info('Certificate33 Collection post called')

		if request.data:
			config = json.loads(request.data)
			if "@odata.type" in config:
				if "Collection" in config["@odata.type"]:
					return "Invalid data in POST body", 400

		if StorageControllerId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates').format(ResourceBlockId, StorageId, StorageControllerId)
		parent_path = os.path.dirname(path)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Certificate', parent_path)

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Certificate33API.post(self, ResourceBlockId, StorageId, StorageControllerId, os.path.basename(config['@odata.id']))
			else:
				return Certificate33API.post(self, ResourceBlockId, StorageId, StorageControllerId, str(res))
		else:
			return Certificate33API.post(self, ResourceBlockId, StorageId, StorageControllerId, str(res))

	# HTTP PUT Collection
	def put(self, ResourceBlockId, StorageId, StorageControllerId):
		logging.info('Certificate33 Collection put called')

		path = os.path.join(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates', 'index.json').format(ResourceBlockId, StorageId, StorageControllerId)
		put_object (path)
		return self.get(ResourceBlockId)

# Certificate33 API
class Certificate33API(Resource):
	def __init__(self):
		logging.info('Certificate33 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ResourceBlockId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate33 get called')
		path = create_path(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates/{3}', 'index.json').format(ResourceBlockId, StorageId, StorageControllerId, CertificateId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ResourceBlockId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate33 post called')
		path = create_path(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates/{3}').format(ResourceBlockId, StorageId, StorageControllerId, CertificateId)
		collection_path = os.path.join(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates', 'index.json').format(ResourceBlockId, StorageId, StorageControllerId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Certificate33CollectionAPI.post(self, ResourceBlockId, StorageId, StorageControllerId)

		if CertificateId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ResourceBlockId':ResourceBlockId, 'StorageId':StorageId, 'StorageControllerId':StorageControllerId, 'CertificateId':CertificateId, 'rb':g.rest_base}
			config=get_Certificate33_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Certificate33API POST exit')
		return resp

	# HTTP PUT
	def put(self, ResourceBlockId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate33 put called')
		path = os.path.join(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates/{3}', 'index.json').format(ResourceBlockId, StorageId, StorageControllerId, CertificateId)
		put_object(path)
		return self.get(ResourceBlockId, StorageId, StorageControllerId, CertificateId)

	# HTTP PATCH
	def patch(self, ResourceBlockId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate33 patch called')
		path = os.path.join(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates/{3}', 'index.json').format(ResourceBlockId, StorageId, StorageControllerId, CertificateId)
		patch_object(path)
		return self.get(ResourceBlockId, StorageId, StorageControllerId, CertificateId)

	# HTTP DELETE
	def delete(self, ResourceBlockId, StorageId, StorageControllerId, CertificateId):
		logging.info('Certificate33 delete called')
		path = create_path(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates/{3}').format(ResourceBlockId, StorageId, StorageControllerId, CertificateId)
		base_path = create_path(self.root, 'CompositionService/ResourceBlocks/{0}/Storage/{1}/StorageControllers/{2}/Certificates').format(ResourceBlockId, StorageId, StorageControllerId)
		return delete_object(path, base_path)

