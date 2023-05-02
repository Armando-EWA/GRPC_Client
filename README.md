In order to generate protobuf changes, make sure you are in the Client directory and run:
```
python -m grpc_tools.protoc -I .\proto --python_out=.\compiled_proto_files --grpc_python_out=.\compiled_proto_files greeting.proto 
```