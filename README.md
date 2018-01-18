# SingularityNET

[![Build Status](https://travis-ci.org/singnet/singnet.svg?branch=master)](https://travis-ci.org/singnet/singnet)

[![Coverage Status](https://coveralls.io/repos/github/singnet/singnet/badge.svg)](https://coveralls.io/github/singnet/singnet)

[![Documentation Status](https://readthedocs.org/projects/singnet/badge/?version=latest)](http://singnet.readthedocs.io/en/latest/?badge=latest)

SingularityNET allows multiple AI computing agents to work as a whole to
provide various services in a distributed and decentralized way.
 
For the first time, we have a financial substrate in the blockchain that
lets us align diverse AI technologies and functions into a coherent financial
and cognitive whole. The SingularityNET architecture incorporating block-chain 
smart-contracts and automatic payment will let diverse AIs integrate together
into a single dynamic intelligence. AI agents incorporating the OpenCog AGI
framework, Google Tensorflow and other powerful tools, interacting within the
SingularityNET; will bootstrap the research and development of an AGI economy.



## Contents


* [**Architectural Overview**](#architectural-overview) - the system architecture
 and high-level design
* [**Getting Started**](#getting-started) - instructions for getting
 SingularityNET running on your system
* [**Example Scenario**](#example-scenario) - a non-trivial example of
 SingularityNET agent interaction
* [**SingularityNET API**](#singularitynet-api) - the interfaces required to
 implement or call agents to perform services

## Architectural Overview

There are seven major interacting components in the SingularityNET architecture:

* **Network** - the block-chain and smart-contract network used for agent 
  negotiation and discovery
  
* **Agent** - the agent which provides services and responds to service
 requests by other agents in the SingularityNET

* **Ontology** - contains definitions of services available in SingularityNET. 
 Ontologies are versioned and define the semantics of network operations.

* **ServiceDescriptor** - a signed immutable post-negotiation description of a
 service which can be performed by an Agent
 
* **JobDescriptor** - a list of jobs which tie a particular ServiceDescriptor with 
 job-specific data like input and output data types, URLs, specific communication
 protocols etc.

* **ServiceAdapter** - a wrapper for AI and other services which an Agent can
 invoke to perform the actual services required to perform a job according to
 the negotiated ServiceDescriptor.

* **ExternalServiceAdapter** - a wrapper for interacting with external service
 agents in the SingularityNET universe.



## Getting Started


These instructions will get you a copy of the project up and running on your local
machine for development and testing purposes. See deployment for notes on how to
deploy the project on a live system.

The agent servver is responsible for communicating with AI Adapters which connect
to individual AI systems and the rest of the network. You can run an Agent connected
 to the SingularityNET network as a server that runs stand-alone or as one that
 forwareds requests for work to other servers running specialized AI services.


### Prerequisites

SingularityNET runs on Mac OS X, or any Linux which has Python 3 installed and
Docker or Docker for Mac installed.

The core devs regularly develop on Mac OS X Sierra, Linux Mint Mate 18.2, and
Linux Ubuntu 16.04 LTS among others.

Docker and Docker Compose are used heavily, so you must have a recent version of
Docker installed to take advantage of most of the automation and to isolate
yourself from the dependency hell which often results from installing software
with complex dependencies directly onto your host development OS.

The current development demo runs from a `dev` docker container which can be
launched from your host computer command line using our helper tool shell
script: `tools.sh`.

```
./tools.sh dev
```
This will bring up a set of docker containers and expose port 8000 to the 
local host machine. Visit the demo via:

http://localhost:8000

in a modern browser.


### Adapter Examples

There are two kinds of Service Adapter examples in the project: real AI integration
and template examples designed to teach concepts.

The directory `singnet/agent/adapters` contains working AI adapters that connect
with AI services from OpenCog, TensorFlow, and Aigents, among others... Some
knowledge of the underlying AI architectures and systems will be necessary to
understand the code in these Service Adapters.

The directory `singnet/agent/examples` contains examples that are designed to
show how to do something without necessarily implementing real AI so you can
understand the mechanics without needing to understnd any particular AI sytems.

### Running tests

Tests are handled by PyTest via Tox, but we've made it very easy for you.

Just run:

```
./tools.sh agent-test
```

### Generating docs

Docs are not currently included in the source as they are changing rapidly. We
do suggest you create the docs and look them over. Once this settles, we will
likely have an online reference to these. We could use some help if you like
writing documentation and don't mind trying to keep up with a fast-moving
project.

```
./tools.sh agent-docs
```

### Contributing


Please read [CONTRIBUTING](CONTRIBUTING.md) for details on the process for submitting pull requests to the SingularityNET project.

Here are some of list of the [contributors](https://github.com/opencog/singnet/graphs/contributors) who participate in this project.

### Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/opencog/singnet/tags). 



## Example Scenario


A SingularityNET Agent provides document summarization services for corporate work
groups. As inputs for this service, it might require:

* **Glossary** - a glossary of terms and entities relevant to the corporate service client

* **People Images** - a set of images representing people to be recognized

* **Object Images** - a set of images representing things to be identified
  
* **Documents** - a set of documents to summarize in accepted formats

The task of performing document summarization requires summarizing text; identifying
relevant objects and people in images; ranking relevance; processing video to
extract objects, people and a textual description; and generating
a ranked summary of the document.


### Internal Services

The SingularityNET Agent might perform the following services internally:

* **Final Document Summary** - assembling the parts and generating the final product

* **Text Summary** - processing the text to build a summary of text-only portions


### External Services

The Agent might use ExternalServiceProvider agents to perform the following services:

* **Word Sense Disambiguation** - a sub-service used by the Agent's Text Summary
 service to disambiguate words and meanings from text and context when more than
 one sense is possible and grammatically correct. 

* **Entity Extraction** - a sub-service which extracts object identities from
 images and text which match the Glossary and Images entries.

* **Video Summary** - a sub-service which extracts object identities from
 images and text which match the Glossary and both Images inputs.

* **Face Recognizer** - a sub-service which identifies people from the People
Images inputs

The architecture supports scenarios like the above where individual agents may 
provide subsets or all of the services required to deliver any Service in the
ontology.



## SingularityNET API


### NetworkABC
The base class for block-chain networks. NetworkABC defines the protocol for
managing the interactions of Agents, Ontology, ServiceDescriptors, as well as 
Agent discovery, and negotiation. Each block-chain implementation will require a
separate NetworkABC subclass which implements the smart-contracts and communication
protocols required to implement the Network ABC API.

NetworkABC subclasses must implement:
* **`join_network`** - creates a new agent on the block chain
* **`leave_network`** - removes agent from the block chain
* **`logon_network`** - opens a connection for an agent
* **`logoff_network`** - closes the connection for an agent
* **`get_network_status`** - get the agents status on the network
* **`update_ontology`** - queries the block-chain and updates the ontology to current version
* **`advertise_service`** - registers an agent's service offerings on the blockchain
* **`remove_service_advertisement`** - removes an agents service offerings from the blockchain
* **`find_service_providers`** - returns a list of external service provider agents


### ServiceAdapterABC
This is the base class for all Service Adapters. Services can be AI services or
other services of use by the network like file storage, backup, etc.

ServiceAdapterABC subclasses must implement:
* **`perform`** - perform the service defined by the JobDescriptor

Additionally, ServiceAdapterABC subclasses may also implement:
* **`init`** - perform service one-time initialization
* **`start`** - connect with external network providers required to perform service
* **`stop`** - disconnect in preparation for taking the service offline
* **`can_perform`** - override to implement service specific logic
* **`all_required_agents_can_perform`** - check if dependent agents can perform
 sub-services

---
## Built With

* [AIOHttp](https://aiohttp.readthedocs.io/en/stable/) - The async web
framework used to handle JSONRPC and HTML requests
* [SQLAlchemy](https://www.sqlalchemy.org/) - Internal data storage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
