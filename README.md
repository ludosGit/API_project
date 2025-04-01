# API_project
(WIP) Flask implementation of an API for storing and retrieving my favourite movies with comments and images.

Run using

```flask --app flaskr run --debug```

when using an external debugger (i.e. vscode), the built-in debugger and reloader should be disabled so they don’t interfere with the external debugger:

```flask --app hello run --debug --no-debugger --no-reload```

### Run the app as a **Docker Container**
Build Image:
```docker build -t my-flask-app .```

Run Container
```docker run -p 5000:5000 my-flask-app```

Go to ```http://localhost:5000```

**NOTE**
- A container is a running instance of an image (like an object in OOP), and consumes CPU/RAM when running;
- Docker creates internal networks where containers get their own IPs and communicate securely.

## Technical Notes

Base URL is \mymoviesapi (see flaskr\mymovies_blueprint.py) and the access points to the resources are:
- \genres\<genre> to get list of all movie ids for a specific genre
- 


## RESTful APIs

Bibliography: https://restfulapi.net/


`REST` is an acronym for REpresentational State Transfer and an architectural style for distributed hypermedia systems. \
REST is not a protocol or a standard, it is an architectural style for designing loosely coupled applications over the network\ 
A REST API consists of an assembly of interlinked resources. This set of resources is known as the REST API’s resource model.

REST defines 6 architectural constraints which make any web service a truly RESTful API i.e. ```Uniform interface, Client–server, Stateless, Cacheable, Layered system, Code on demand (optional)```.

- **Uniform interface** As the constraint name itself applies, you MUST decide APIs interface for resources inside the system which are exposed to API consumers and follow religiously. A resource in the system should have only one logical URI, and that should provide a way to fetch related or additional data. It’s always better to synonymize a resource with a web page. 
  
  Any single resource should not be too large and contain each and everything in its representation. Whenever relevant, a resource should contain links (HATEOAS) pointing to relative URIs to fetch related information.

  4 ``sub-principles`` 
  - **Resource Identification** (e.g., using URIs) - The interface must uniquely identify each resource involved in the interaction between the client and the server.
  - **Resource Manipulation Through Representations** - The resources should have uniform representations in the server response. API consumers should use these representations to modify the resource state in the server.
  - **Self-descriptive Messages** - Each resource representation should carry enough information to describe how to process the message. It should also provide information of the additional actions that the client can perform on the resource.
  - **Hypermedia As The Engine Of Application State** (**HATEOAS**) - The client should have only the initial URI of the application. The client application should dynamically drive all other resources and interactions with the use of hyperlinks.
  ```In simpler words, REST defines a consistent and uniform interface for interactions between clients and servers. For example, the HTTP-based REST APIs make use of the standard HTTP methods (GET, POST, PUT, DELETE, etc.) and the URIs (Uniform Resource Identifiers) to identify resources.```

- **Client-server** This constraint essentially means that client applications and server applications MUST be able to evolve separately without any dependency on each other. A client should know only resource URIs, and that’s all. 
  
- **Stateless** Make all client-server interactions stateless. The server will not store anything about the latest HTTP request the client made. It will treat every request as new. No session, no history.  \
  No client context shall be stored on the server between requests. The client is responsible for managing the state of the application. Each request from the client should contain all the information necessary to service the request – including authentication and authorization details.

- **Cacheable** Well-managed caching partially or completely eliminates some client-server interactions, further improving scalability and performance. \ Caching can be implemented on the server or client side.

- REST allows you to use a **layered system** architecture where you deploy the APIs on server A, and store data on server B and authenticate requests in Server C, for example. A client cannot ordinarily tell whether it is connected directly to the end server or an intermediary along the way.

### Resource
The key abstraction of information in REST is a resource. Any information that can be named can be a resource: a document or image, a temporal service (e.g. “today’s weather in Los Angeles”), a collection of other resources, a non-virtual object (e.g., a person), and so on.

In other words, any concept that might be the target of an author’s hypertext reference must fit within the definition of a resource.

A resource is a conceptual mapping to a set of entities, not the entity that corresponds to the mapping at any particular point in time \
REST APIs use Uniform Resource Identifiers (URIs) to address resources. REST API designers should create URIs that convey a REST API’s resource model to the potential clients of the API. When resources are named well, an API is intuitive and easy to use. If done poorly, that same API can be challenging to use and understand. \
See https://restfulapi.net/resource-naming/ for best practises.


## Flask

## Glossary

- **Web application** = application software that is created with web technologies and runs via a web browser. Web applications emerged during the late 1990s and allowed for the server to dynamically build a response to the request, in contrast to static web pages.
  
- **URI** 
A *Uniform Resource Identifier* (URI), formerly Universal Resource Identifier, is a unique sequence of characters that identifies an abstract or physical resource, such as resources on a webpage, mail address, phone number, books, real-world objects such as people and places, concepts.

- **URL**
  A uniform resource locator (URL), colloquially known as an address on the Web, is a reference to a resource that specifies its location on a computer network and a mechanism for retrieving it.  A URL is a specific type of URI. \ 
  A typical URL could have the form http://www.example.com/index.html, which indicates a protocol (http), a hostname (www.example.com), and a file name (index.html)



