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

# Resource implementation for - /redfish/v1/Managers/{ManagerId}/HostInterfaces/{HostInterfaceId}
# Program name - HostInterface_api.py

import g
import json, os
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.HostInterface import get_HostInterface_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# HostInterface Collection API
class HostInterfaceCollectionAPI(Resource):
	def __init__(self):
		logging.info('HostInterface Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ManagerId):
		logging.info('HostInterface Collection get called')
		path = os.path.join(self.root, 'Managers/{0}/HostInterfaces', 'index.json').format(ManagerId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ManagerId):
		logging.info('HostInterface Collection post called')

		if ManagerId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Managers/{0}/HostInterfaces').format(ManagerId)
		return create_collection (path, 'HostInterface')

	# HTTP PUT Collection
	def put(self, ManagerId):
		logging.info('HostInterface Collection put called')

		path = os.path.join(self.root, 'Managers/{0}/HostInterfaces', 'index.json').format(ManagerId)
		put_object (path)
		return self.get(ManagerId)

# HostInterface API
class HostInterfaceAPI(Resource):
	def __init__(self):
		logging.info('HostInterface init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ManagerId, HostInterfaceId):
		logging.info('HostInterface get called')
		path = create_path(self.root, 'Managers/{0}/HostInterfaces/{1}', 'index.json').format(ManagerId, HostInterfaceId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ManagerId, HostInterfaceId):
		logging.info('HostInterface post called')
		path = create_path(self.root, 'Managers/{0}/HostInterfaces/{1}').format(ManagerId, HostInterfaceId)
		collection_path = os.path.join(self.root, 'Managers/{0}/HostInterfaces', 'index.json').format(ManagerId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			HostInterfaceCollectionAPI.post(self, ManagerId)

		if HostInterfaceId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ManagerId':ManagerId, 'HostInterfaceId':HostInterfaceId, 'rb':g.rest_base}
			config=get_HostInterface_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('HostInterfaceAPI POST exit')
		return resp

	# HTTP PUT
	def put(self, ManagerId, HostInterfaceId):
		logging.info('HostInterface put called')
		path = create_path(self.root, 'Managers/{0}/HostInterfaces/{1}', 'index.json').format(ManagerId, HostInterfaceId)
		put_object(path)
		return self.get(ManagerId, HostInterfaceId)

	# HTTP PATCH
	def patch(self, ManagerId, HostInterfaceId):
		logging.info('HostInterface patch called')
		path = create_path(self.root, 'Managers/{0}/HostInterfaces/{1}', 'index.json').format(ManagerId, HostInterfaceId)
		patch_object(path)
		return self.get(ManagerId, HostInterfaceId)

	# HTTP DELETE
	def delete(self, ManagerId, HostInterfaceId):
		logging.info('HostInterface delete called')
		path = create_path(self.root, 'Managers/{0}/HostInterfaces/{1}').format(ManagerId, HostInterfaceId)
		base_path = create_path(self.root, 'Managers/{0}/HostInterfaces').format(ManagerId)
		return delete_object(path, base_path)
