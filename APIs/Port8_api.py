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

# Resource implementation for - /redfish/v1/CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}
# Program name - Port8_api.py

import g
import json, os
import traceback
import logging

from flask import Flask, request
from flask_restful import Resource
from .constants import *
from api_emulator.utils import update_collections_json, create_path, get_json_data, create_and_patch_object, delete_object, patch_object, put_object, delete_collection, create_collection
from .templates.Port8 import get_Port8_instance

members = []
member_ids = []
INTERNAL_ERROR = 500

# Port8 Collection API
class Port8CollectionAPI(Resource):
	def __init__(self):
		logging.info('Port8 Collection init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports):
		logging.info('Port8 Collection get called')
		path = os.path.join(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}', 'index.json').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)
		return get_json_data (path)

	# HTTP POST Collection
	def post(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports):
		logging.info('Port8 Collection post called')

		if CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports in members:
			resp = 404
			return resp
		path = create_path(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)
		return create_collection (path, 'Port')

	# HTTP PUT Collection
	def put(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports):
		path = os.path.join(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}', 'index.json').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)
		put_object (path)
		return self.get(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)

# Port8 API
class Port8API(Resource):
	def __init__(self):
		logging.info('Port8 init called')
		self.root = PATHS['Root']

	# HTTP GET
	def get(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}):
		logging.info('Port8 get called')
		path = create_path(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}/{PortId}', 'index.json').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})
		return get_json_data (path)

	# HTTP POST
	# - Create the resource (since URI variables are available)
	# - Update the members and members.id lists
	# - Attach the APIs of subordinate resources (do this only once)
	# - Finally, create an instance of the subordiante resources
	def post(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}):
		logging.info('Port8 post called')
		path = create_path(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}/{PortId}').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})
		collection_path = os.path.join(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}', 'index.json').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)

		# Check if collection exists:
		if not os.path.exists(collection_path):
			Port8CollectionAPI.post(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)

		if PortId in members:
			resp = 404
			return resp
		try:
			global config
			wildcards = {'CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}':CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}, 'rb':g.rest_base}
			config=get_Port8_instance(wildcards)
			config = create_and_patch_object (config, members, member_ids, path, collection_path)
			resp = config, 200

		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('Port8API POST exit')
		return resp

	# HTTP PUT
	def put(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}):
		logging.info('Port8 put called')
		path = os.path.join(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}/{PortId}', 'index.json').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})
		put_object(path)
		return self.get(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})

	# HTTP PATCH
	def patch(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}):
		logging.info('Port8 patch called')
		path = os.path.join(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}/{PortId}', 'index.json').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})
		patch_object(path)
		return self.get(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})

	# HTTP DELETE
	def delete(self, CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId}):
		logging.info('Port8 delete called')
		path = create_path(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}/{PortId}').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports/{PortId})
		base_path = create_path(self.root, 'CompositionService/{0}/{ResourceBlockId}/{1}/{{1}Id}/{2}/{{1}ControllerId}/{3}').format(CompositionService/ResourceBlocks/{ResourceBlockId}/Storage/{StorageId}/Controllers/{StorageControllerId}/Ports)
		return delete_object(path, base_path)

