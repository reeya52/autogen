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

# Resource implementation for - /redfish/v1/Storage/{StorageId}/Volumes/{VolumeId}/StorageGroups/{StorageGroupId}
# Program name - StorageGroup3_api.py

import g
import json, os
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.StorageGroup3 import get_StorageGroup3_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# StorageGroup3 Collection API
class StorageGroup3CollectionAPI(Resource):
	def __init__(self):
		logging.info('StorageGroup3 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, StorageId, VolumeId):
		logging.info('StorageGroup3 Collection get called')
		path = os.path.join(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups', 'index.json').format(StorageId, VolumeId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, StorageId, VolumeId):
		logging.info('StorageGroup3 Collection post called')

		if VolumeId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups').format(StorageId, VolumeId)
		return create_collection (path, 'StorageGroup')

	# HTTP PUT Collection
	def put(self, StorageId, VolumeId):
		logging.info('StorageGroup3 Collection put called')

		path = os.path.join(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups', 'index.json').format(StorageId, VolumeId)
		put_object (path)
		return self.get(StorageId)

# StorageGroup3 API
class StorageGroup3API(Resource):
	def __init__(self):
		logging.info('StorageGroup3 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, StorageId, VolumeId, StorageGroupId):
		logging.info('StorageGroup3 get called')
		path = create_path(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups/{2}', 'index.json').format(StorageId, VolumeId, StorageGroupId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, StorageId, VolumeId, StorageGroupId):
		logging.info('StorageGroup3 post called')
		path = create_path(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups/{2}').format(StorageId, VolumeId, StorageGroupId)
		collection_path = os.path.join(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups', 'index.json').format(StorageId, VolumeId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			StorageGroup3CollectionAPI.post(self, StorageId, VolumeId)

		if StorageGroupId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'StorageId':StorageId, 'VolumeId':VolumeId, 'StorageGroupId':StorageGroupId, 'rb':g.rest_base}
			config=get_StorageGroup3_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('StorageGroup3API POST exit')
		return resp

	# HTTP PUT
	def put(self, StorageId, VolumeId, StorageGroupId):
		logging.info('StorageGroup3 put called')
		path = os.path.join(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups/{2}', 'index.json').format(StorageId, VolumeId, StorageGroupId)
		put_object(path)
		return self.get(StorageId, VolumeId, StorageGroupId)

	# HTTP PATCH
	def patch(self, StorageId, VolumeId, StorageGroupId):
		logging.info('StorageGroup3 patch called')
		path = os.path.join(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups/{2}', 'index.json').format(StorageId, VolumeId, StorageGroupId)
		patch_object(path)
		return self.get(StorageId, VolumeId, StorageGroupId)

	# HTTP DELETE
	def delete(self, StorageId, VolumeId, StorageGroupId):
		logging.info('StorageGroup3 delete called')
		path = create_path(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups/{2}').format(StorageId, VolumeId, StorageGroupId)
		base_path = create_path(self.root, 'Storage/{0}/Volumes/{1}/StorageGroups').format(StorageId, VolumeId)
		return delete_object(path, base_path)
