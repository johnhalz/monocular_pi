# Convert `.proto` file to python
Run the following command:

``` bash
protoc --python_out=. ./filename.proto
```

Note that the latest version of the `protobuf` module will require you to compile the `.proto` file with a `protoc` version higher than 3.19.

Foxglove Protobuf schemas: <https://foxglove.dev/docs/studio/messages/introduction>
