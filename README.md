# Codecrafters Redis Server

A simplified `redis-server` implementation written in Python according to the challenges posed in ["Build Your Own Redis"](https://codecrafters.io/challenges/redis).

It should be compatible with `redis-cli` for all commands and features listed below.

## Supported Commands and Features

### Commands

- `CONFIG GET`
  - Retrieves the value of a configuration parameter.

- `DISCARD`
  - Discards all commands issued after `MULTI`.

- `ECHO`
  - Responds with the same message that was sent.

- `EXEC`
  - Executes all commands issued after `MULTI`.
  - Requires `MULTI` to be issued first.

- `GET`
  - Gets the value of a key.

- `INCR`
  - Increments the integer value of a key by one.

- `INFO`
  - Provides information and statistics about the server.
  - Supports the `REPLICATION` section.

- `KEYS`
  - Returns all keys that match the pattern given as an arg.

- `MULTI`
  - Marks the start of a transaction block.

- `PING`
  - Responds with `PONG`.

- `PSYNC`
  - Part of the replication protocol.
  - Responds with `+FULLRESYNC` and sends an RDB file.

- `REPLCONF`
  - Configures replication settings.
  - Supports simplified `LISTENING-PORT`, `CAPA`, and `GETACK` subcommands.

- `SET`
  - Sets the value of a key.
  - Supports expiration with the `PX` option.
  - Other options aren't supported.

- `TYPE`
  - Returns the type of the value stored at the key.

- `WAIT`
  - Waits for the specified number of replicas to acknowledge writes.

- `XADD`
  - Appends a new entry to a stream.

- `XRANGE`
  - Returns a range of entries from a stream.

- `XREAD`
  - Reads entries from multiple streams given a set of keys and ids.
  - Supports blocking read until new info is written.

### Features

- **RESP2**
  - All communication with redis-cli is done according to Redis serialization protocol (RESP), specifically version 2

- **Replication**
  - Supports master-slave replication.
  - Handles full resynchronization with `PSYNC`.
  - Only propagates `SET` commands.

- **Persistence**
  - Loads data from RDB files.
  - It only loads simple String data written with `SET` alongside their expiration.

### Limitations

- This implementation is a simplified version of Redis and does not support all features and edge cases of the official Redis server.
- Performance optimizations present in the official Redis server may not be implemented.

## Getting Started

To run the server, use the following command:

```sh
./your_program.sh
```

Then you may connect with it using a redis-cli on port `6379`.

### Options
  - `--dir`: The directory where the RDB file is located.
  - `--dbfilename`: The name of the RDB file.
  - `--port`: The port on which the server will listen (default: 6379).
  - `--replicaof`: The host and port of the master server for replication (e.g., "127.0.0.1 6379").
