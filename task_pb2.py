# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: task.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ntask.proto\"6\n\x04Task\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04wcet\x18\x02 \x01(\x02\x12\x14\n\x0c\x64\x65pendencies\x18\x03 \x03(\x05\"!\n\tTaskGraph\x12\x14\n\x05tasks\x18\x01 \x03(\x0b\x32\x05.Taskb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'task_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TASK._serialized_start=14
  _TASK._serialized_end=68
  _TASKGRAPH._serialized_start=70
  _TASKGRAPH._serialized_end=103
# @@protoc_insertion_point(module_scope)
