# Cava

Abbreviation of *Italian*: Automa cavaliere, lit. "Automaton knight", Leonardo's original robot

## Intention

A system that will automatically react and fix issues identified in my home automation system.

## Components

* A simple queuing mechanism for capturing events.
* One or more emitters
* A message parsing processor function that will analyze and standardize events
* A correlation function that will tie events to actions to be taken
* An execution system that will take the prescribed actions
* A metrics system to display things occuring through the platform

### Queueing System

A simple system, likely RabbitMQ that can accept inputs on various channels/queues based on the originating event sytem. Our platform can rely on the fact that messages coming on a specific queue have certaoin attributes that can be parsed in a specific way.

### Emitters

These can take various forms, one will be an emitter coming directly from Icinga, as an example. Others could be simple webhook programs, etc.

#### Webhook Emitter

Takes any json object and drops it into the Message Exchange queue with `type: webook`

##### High Level Specs

* Should only accept json data, return 400 for bad (non json) data
* Should only emit a copy of the json data to the queue
* Should use /api/v1/:route\_key: where :route\_key: will be the routing key
* No authentication

#### Icinga Emitter

Listens to the Icinga API and emits messages to the Mesage Exchange queue with `type: icinga`

### Message Parsing Processor

A system(s) that read from a specific queue and knows how to standardize messages and drop them on the central processing queue.

### Correlation function

A system that has been instructed to react to messages of a specific type and initiates actions to be taken, can also log metrics on frequency of an event.

### Metrics System

Use the current Influxdb, Grafana, etc.

Todo:

- \[ \] Create a "Reader" to use during testing, add to Dev Kustomize
- \[ \] Add logging to webhook
- \[ \] Move secrets to k8s secrets and environment variables
- \[ \] Sanitize inputs (look at bleach)
- \[ \] Add more tests to Webhook