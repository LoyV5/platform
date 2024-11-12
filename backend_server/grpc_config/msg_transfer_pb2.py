# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server/grpc_config/protos/msg_transfer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='server/grpc_config/protos/msg_transfer.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n,server/grpc_config/protos/msg_transfer.proto\"?\n\nMsgRequest\x12\r\n\x05model\x18\x01 \x01(\t\x12\r\n\x05\x66rame\x18\x02 \x01(\t\x12\x13\n\x0b\x66rame_shape\x18\x03 \x01(\t\"/\n\x08MsgReply\x12\x0e\n\x06result\x18\x02 \x01(\t\x12\x13\n\x0b\x66rame_shape\x18\x03 \x01(\t\"\x1c\n\x1aServer_Utilization_Request\"C\n\x18Server_Utilization_Reply\x12\x11\n\tcpu_usage\x18\x01 \x01(\x02\x12\x14\n\x0cmemory_usage\x18\x02 \x01(\x02\"\x1b\n\x19Loaded_Model_Name_Request\"4\n\x17Loaded_Model_Name_Reply\x12\x19\n\x11loaded_model_name\x18\x01 \x01(\t\"7\n\x1cLoad_Specified_Model_Request\x12\x17\n\x0fspecified_model\x18\x01 \x01(\t\"\x1c\n\x1aLoad_Specified_Model_Reply2\xb6\x02\n\x0bMsgTransfer\x12+\n\x0fimage_processor\x12\x0b.MsgRequest\x1a\t.MsgReply\"\x00\x12R\n\x16get_server_utilization\x12\x1b.Server_Utilization_Request\x1a\x19.Server_Utilization_Reply\"\x00\x12P\n\x16get_loaded_models_name\x12\x1a.Loaded_Model_Name_Request\x1a\x18.Loaded_Model_Name_Reply\"\x00\x12T\n\x14load_specified_model\x12\x1d.Load_Specified_Model_Request\x1a\x1b.Load_Specified_Model_Reply\"\x00\x62\x06proto3'
)




_MSGREQUEST = _descriptor.Descriptor(
  name='MsgRequest',
  full_name='MsgRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='MsgRequest.model', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame', full_name='MsgRequest.frame', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_shape', full_name='MsgRequest.frame_shape', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=111,
)


_MSGREPLY = _descriptor.Descriptor(
  name='MsgReply',
  full_name='MsgReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='MsgReply.result', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_shape', full_name='MsgReply.frame_shape', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=160,
)


_SERVER_UTILIZATION_REQUEST = _descriptor.Descriptor(
  name='Server_Utilization_Request',
  full_name='Server_Utilization_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=162,
  serialized_end=190,
)


_SERVER_UTILIZATION_REPLY = _descriptor.Descriptor(
  name='Server_Utilization_Reply',
  full_name='Server_Utilization_Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cpu_usage', full_name='Server_Utilization_Reply.cpu_usage', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory_usage', full_name='Server_Utilization_Reply.memory_usage', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=192,
  serialized_end=259,
)


_LOADED_MODEL_NAME_REQUEST = _descriptor.Descriptor(
  name='Loaded_Model_Name_Request',
  full_name='Loaded_Model_Name_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=261,
  serialized_end=288,
)


_LOADED_MODEL_NAME_REPLY = _descriptor.Descriptor(
  name='Loaded_Model_Name_Reply',
  full_name='Loaded_Model_Name_Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='loaded_model_name', full_name='Loaded_Model_Name_Reply.loaded_model_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=290,
  serialized_end=342,
)


_LOAD_SPECIFIED_MODEL_REQUEST = _descriptor.Descriptor(
  name='Load_Specified_Model_Request',
  full_name='Load_Specified_Model_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='specified_model', full_name='Load_Specified_Model_Request.specified_model', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=344,
  serialized_end=399,
)


_LOAD_SPECIFIED_MODEL_REPLY = _descriptor.Descriptor(
  name='Load_Specified_Model_Reply',
  full_name='Load_Specified_Model_Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=401,
  serialized_end=429,
)

DESCRIPTOR.message_types_by_name['MsgRequest'] = _MSGREQUEST
DESCRIPTOR.message_types_by_name['MsgReply'] = _MSGREPLY
DESCRIPTOR.message_types_by_name['Server_Utilization_Request'] = _SERVER_UTILIZATION_REQUEST
DESCRIPTOR.message_types_by_name['Server_Utilization_Reply'] = _SERVER_UTILIZATION_REPLY
DESCRIPTOR.message_types_by_name['Loaded_Model_Name_Request'] = _LOADED_MODEL_NAME_REQUEST
DESCRIPTOR.message_types_by_name['Loaded_Model_Name_Reply'] = _LOADED_MODEL_NAME_REPLY
DESCRIPTOR.message_types_by_name['Load_Specified_Model_Request'] = _LOAD_SPECIFIED_MODEL_REQUEST
DESCRIPTOR.message_types_by_name['Load_Specified_Model_Reply'] = _LOAD_SPECIFIED_MODEL_REPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MsgRequest = _reflection.GeneratedProtocolMessageType('MsgRequest', (_message.Message,), {
  'DESCRIPTOR' : _MSGREQUEST,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:MsgRequest)
  })
_sym_db.RegisterMessage(MsgRequest)

MsgReply = _reflection.GeneratedProtocolMessageType('MsgReply', (_message.Message,), {
  'DESCRIPTOR' : _MSGREPLY,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:MsgReply)
  })
_sym_db.RegisterMessage(MsgReply)

Server_Utilization_Request = _reflection.GeneratedProtocolMessageType('Server_Utilization_Request', (_message.Message,), {
  'DESCRIPTOR' : _SERVER_UTILIZATION_REQUEST,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:Server_Utilization_Request)
  })
_sym_db.RegisterMessage(Server_Utilization_Request)

Server_Utilization_Reply = _reflection.GeneratedProtocolMessageType('Server_Utilization_Reply', (_message.Message,), {
  'DESCRIPTOR' : _SERVER_UTILIZATION_REPLY,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:Server_Utilization_Reply)
  })
_sym_db.RegisterMessage(Server_Utilization_Reply)

Loaded_Model_Name_Request = _reflection.GeneratedProtocolMessageType('Loaded_Model_Name_Request', (_message.Message,), {
  'DESCRIPTOR' : _LOADED_MODEL_NAME_REQUEST,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:Loaded_Model_Name_Request)
  })
_sym_db.RegisterMessage(Loaded_Model_Name_Request)

Loaded_Model_Name_Reply = _reflection.GeneratedProtocolMessageType('Loaded_Model_Name_Reply', (_message.Message,), {
  'DESCRIPTOR' : _LOADED_MODEL_NAME_REPLY,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:Loaded_Model_Name_Reply)
  })
_sym_db.RegisterMessage(Loaded_Model_Name_Reply)

Load_Specified_Model_Request = _reflection.GeneratedProtocolMessageType('Load_Specified_Model_Request', (_message.Message,), {
  'DESCRIPTOR' : _LOAD_SPECIFIED_MODEL_REQUEST,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:Load_Specified_Model_Request)
  })
_sym_db.RegisterMessage(Load_Specified_Model_Request)

Load_Specified_Model_Reply = _reflection.GeneratedProtocolMessageType('Load_Specified_Model_Reply', (_message.Message,), {
  'DESCRIPTOR' : _LOAD_SPECIFIED_MODEL_REPLY,
  '__module__' : 'server.grpc_config.protos.msg_transfer_pb2'
  # @@protoc_insertion_point(class_scope:Load_Specified_Model_Reply)
  })
_sym_db.RegisterMessage(Load_Specified_Model_Reply)



_MSGTRANSFER = _descriptor.ServiceDescriptor(
  name='MsgTransfer',
  full_name='MsgTransfer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=432,
  serialized_end=742,
  methods=[
  _descriptor.MethodDescriptor(
    name='image_processor',
    full_name='MsgTransfer.image_processor',
    index=0,
    containing_service=None,
    input_type=_MSGREQUEST,
    output_type=_MSGREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_server_utilization',
    full_name='MsgTransfer.get_server_utilization',
    index=1,
    containing_service=None,
    input_type=_SERVER_UTILIZATION_REQUEST,
    output_type=_SERVER_UTILIZATION_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_loaded_models_name',
    full_name='MsgTransfer.get_loaded_models_name',
    index=2,
    containing_service=None,
    input_type=_LOADED_MODEL_NAME_REQUEST,
    output_type=_LOADED_MODEL_NAME_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='load_specified_model',
    full_name='MsgTransfer.load_specified_model',
    index=3,
    containing_service=None,
    input_type=_LOAD_SPECIFIED_MODEL_REQUEST,
    output_type=_LOAD_SPECIFIED_MODEL_REPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MSGTRANSFER)

DESCRIPTOR.services_by_name['MsgTransfer'] = _MSGTRANSFER

# @@protoc_insertion_point(module_scope)
