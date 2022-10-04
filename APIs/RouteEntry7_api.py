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

# Resource implementation for - /redfish/v1/Systems/{ComputerSystemId}/FabricAdapters/{FabricAdapterId}/SSDT/{SSDTId}
# Program name - RouteEntry7_api.py

import g
import json, os
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.RouteEntry7 import get_RouteEntry7_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# RouteEntry7 Collection API
class RouteEntry7CollectionAPI(Resource):
	def __init__(self):
		logging.info('RouteEntry7 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ComputerSystemId, FabricAdapterId):
		logging.info('RouteEntry7 Collection get called')
		path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT', 'index.json').format(ComputerSystemId, FabricAdapterId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ComputerSystemId, FabricAdapterId):
		logging.info('RouteEntry7 Collection post called')

		if FabricAdapterId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT').format(ComputerSystemId, FabricAdapterId)
		return create_collection (path, 'RouteEntry')

	# HTTP PUT Collection
	def put(self, ComputerSystemId, FabricAdapterId):
		logging.info('RouteEntry7 Collection put called')

		path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT', 'index.json').format(ComputerSystemId, FabricAdapterId)
		put_object (path)
		return self.get(ComputerSystemId)

# RouteEntry7 API
class RouteEntry7API(Resource):
	def __init__(self):
		logging.info('RouteEntry7 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ComputerSystemId, FabricAdapterId, SSDTId):
		logging.info('RouteEntry7 get called')
		path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT/{2}', 'index.json').format(ComputerSystemId, FabricAdapterId, SSDTId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ComputerSystemId, FabricAdapterId, SSDTId):
		logging.info('RouteEntry7 post called')
		path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT/{2}').format(ComputerSystemId, FabricAdapterId, SSDTId)
		collection_path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT', 'index.json').format(ComputerSystemId, FabricAdapterId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			RouteEntry7CollectionAPI.post(self, ComputerSystemId, FabricAdapterId)

		if SSDTId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ComputerSystemId':ComputerSystemId, 'FabricAdapterId':FabricAdapterId, 'SSDTId':SSDTId, 'rb':g.rest_base}
			config=get_RouteEntry7_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('RouteEntry7API POST exit')
		return resp

	# HTTP PUT
	def put(self, ComputerSystemId, FabricAdapterId, SSDTId):
		logging.info('RouteEntry7 put called')
		path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT/{2}', 'index.json').format(ComputerSystemId, FabricAdapterId, SSDTId)
		put_object(path)
		return self.get(ComputerSystemId, FabricAdapterId, SSDTId)

	# HTTP PATCH
	def patch(self, ComputerSystemId, FabricAdapterId, SSDTId):
		logging.info('RouteEntry7 patch called')
		path = os.path.join(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT/{2}', 'index.json').format(ComputerSystemId, FabricAdapterId, SSDTId)
		patch_object(path)
		return self.get(ComputerSystemId, FabricAdapterId, SSDTId)

	# HTTP DELETE
	def delete(self, ComputerSystemId, FabricAdapterId, SSDTId):
		logging.info('RouteEntry7 delete called')
		path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT/{2}').format(ComputerSystemId, FabricAdapterId, SSDTId)
		base_path = create_path(self.root, 'Systems/{0}/FabricAdapters/{1}/SSDT').format(ComputerSystemId, FabricAdapterId)
		return delete_object(path, base_path)
