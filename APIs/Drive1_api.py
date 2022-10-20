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

# Resource implementation for - /redfish/v1/Chassis/{ChassisId}/Drives/{DriveId}
# Program name - Drive1_api.py

import g
import json, os, random, string
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Drive1 import get_Drive1_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Drive1 Collection API
class Drive1CollectionAPI(Resource):
	def __init__(self):
		logging.info('Drive1 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ChassisId):
		logging.info('Drive1 Collection get called')
		path = os.path.join(self.root, 'Chassis/{0}/Drives', 'index.json').format(ChassisId)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, ChassisId):
		logging.info('Drive1 Collection post called')

		if ChassisId in members:
			resp = 404
			return resp
		path = create_path(self.root, 'Chassis/{0}/Drives').format(ChassisId)
		if not os.path.exists(path):
			os.mkdir(path)
			create_collection (path, 'Drive')

		res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		if request.data:
			config = json.loads(request.data)
			if "@odata.id" in config:
				return Drive1API.post(self, os.path.basename(config['@odata.id']))
			else:
				return Drive1API.post(self, str(res))
		else:
			return Drive1API.post(self, str(res))

	# HTTP PUT Collection
	def put(self, ChassisId):
		logging.info('Drive1 Collection put called')

		path = os.path.join(self.root, 'Chassis/{0}/Drives', 'index.json').format(ChassisId)
		put_object (path)
		return self.get(ChassisId)

# Drive1 API
class Drive1API(Resource):
	def __init__(self):
		logging.info('Drive1 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, ChassisId, DriveId):
		logging.info('Drive1 get called')
		path = create_path(self.root, 'Chassis/{0}/Drives/{1}', 'index.json').format(ChassisId, DriveId)
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, ChassisId, DriveId):
		logging.info('Drive1 post called')
		path = create_path(self.root, 'Chassis/{0}/Drives/{1}').format(ChassisId, DriveId)
		collection_path = os.path.join(self.root, 'Chassis/{0}/Drives', 'index.json').format(ChassisId)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Drive1CollectionAPI.post(self, ChassisId)

		if DriveId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'ChassisId':ChassisId, 'DriveId':DriveId, 'rb':g.rest_base}
			config=get_Drive1_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Drive1API POST exit')
		return resp

	# HTTP PUT
	def put(self, ChassisId, DriveId):
		logging.info('Drive1 put called')
		path = create_path(self.root, 'Chassis/{0}/Drives/{1}', 'index.json').format(ChassisId, DriveId)
		put_object(path)
		return self.get(ChassisId, DriveId)

	# HTTP PATCH
	def patch(self, ChassisId, DriveId):
		logging.info('Drive1 patch called')
		path = create_path(self.root, 'Chassis/{0}/Drives/{1}', 'index.json').format(ChassisId, DriveId)
		patch_object(path)
		return self.get(ChassisId, DriveId)

	# HTTP DELETE
	def delete(self, ChassisId, DriveId):
		logging.info('Drive1 delete called')
		path = create_path(self.root, 'Chassis/{0}/Drives/{1}').format(ChassisId, DriveId)
		base_path = create_path(self.root, 'Chassis/{0}/Drives').format(ChassisId)
		return delete_object(path, base_path)

