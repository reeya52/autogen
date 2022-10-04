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

# Resource implementation for - /redfish/v1/ResourceBlocks/{ResourceBlockId}/Systems/{ComputerSystemId}/SecureBoot/SecureBootDatabases/{DatabaseId}/Certificates/{CertificateId}
# Program name - Certificate14_api.py

import g
import json, os
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Certificate14 import get_Certificate14_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Certificate14 Collection API
class Certificate14CollectionAPI(Resource):
	def __init__(self):
		logging.info('Certificate14 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ResourceBlockId, ComputerSystemId, DatabaseId):
		logging.info('Certificate14 Collection get called')
		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates', 'index.json').format(ResourceBlockId, ComputerSystemId, DatabaseId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ResourceBlockId, ComputerSystemId, DatabaseId):
		logging.info('Certificate14 Collection post called')

		if DatabaseId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates').format(ResourceBlockId, ComputerSystemId, DatabaseId)
		return create_collection (path, 'Certificate')

	# HTTP PUT Collection
	def put(self, ResourceBlockId, ComputerSystemId, DatabaseId):
		logging.info('Certificate14 Collection put called')

		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates', 'index.json').format(ResourceBlockId, ComputerSystemId, DatabaseId)
		put_object (path)
		return self.get(ResourceBlockId)

# Certificate14 API
class Certificate14API(Resource):
	def __init__(self):
		logging.info('Certificate14 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId):
		logging.info('Certificate14 get called')
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates/{3}', 'index.json').format(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId):
		logging.info('Certificate14 post called')
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates/{3}').format(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)
		collection_path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates', 'index.json').format(ResourceBlockId, ComputerSystemId, DatabaseId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Certificate14CollectionAPI.post(self, ResourceBlockId, ComputerSystemId, DatabaseId)

		if CertificateId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ResourceBlockId':ResourceBlockId, 'ComputerSystemId':ComputerSystemId, 'DatabaseId':DatabaseId, 'CertificateId':CertificateId, 'rb':g.rest_base}
			config=get_Certificate14_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Certificate14API POST exit')
		return resp

	# HTTP PUT
	def put(self, ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId):
		logging.info('Certificate14 put called')
		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates/{3}', 'index.json').format(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)
		put_object(path)
		return self.get(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)

	# HTTP PATCH
	def patch(self, ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId):
		logging.info('Certificate14 patch called')
		path = os.path.join(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates/{3}', 'index.json').format(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)
		patch_object(path)
		return self.get(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)

	# HTTP DELETE
	def delete(self, ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId):
		logging.info('Certificate14 delete called')
		path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates/{3}').format(ResourceBlockId, ComputerSystemId, DatabaseId, CertificateId)
		base_path = create_path(self.root, 'ResourceBlocks/{0}/Systems/{1}/SecureBoot/SecureBootDatabases/{2}/Certificates').format(ResourceBlockId, ComputerSystemId, DatabaseId)
		return delete_object(path, base_path)

