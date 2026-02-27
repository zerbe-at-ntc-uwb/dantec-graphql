# Overview

Code to set-up and populate the GraphQL sever using strawberry.

# Use

Make sure uv is installed on your machine.  The following two commands 
build the environment necessary to run the code and then
starts a GraphQL dev server that listens at port 5432.

1. Run `uv sync` within the top directory of this repo.
2. Run `uv run strawberry dev main --port 5432` to get a development server
  - Make sure to run the command from your local drive, not a networked drive, or you will get an error in your browser.
    - This is because the browser cannot go to the graphql server as it is looking for the port on your local machine whereas I think the server is listening to the port on the networked machine.
    -  Alternative solution might be to port-forward, but that's more steps that have not been determined yet.  Running the dev server from a local drive resolves this issue without this extra step.
  - When the dev server is started, a http url is printed to the console.  Within this url, replace "0.0.0.0" with "localhost" before you put it into your browser nav bar.  localhost maps to 127.0.0.1, so I don't think 0.0.0.0 works otherwise.

# Design

## What's been implemented

I started with a simple test, Element, which is not stored in 
the Nomad repo but within a json file called `api/nomad/types/json_files/elementData.json` to test whether I
could get GraphQL
connected correctly.  I built an object, ElementResource,
to lazy load this data, i.e. the data access layer, and then implemented a 
GraphQL API to pull all data
(elements) and to just a pull a single element via element(symbol) (where symbol
is a string refering to an element like "H" for hydrogen or "Pb" for lead).
If you go to the dev server, you can play around with these GraphQL API queries.

Also, I built a interface generic interface to paginated "record" data.
I created a Record type (in `api/types/record.py`) that is just has an id and a contents JSON.
To allow for "forward" pagination, I create a ForwardPaginationInput object
(in `api/resolvers/inputs/forwardPaginationInput.py`)
that takes a string for disambiguating the source, an integer telling how many
results are requested from the source, and a string telling whether the source
should start after some internal record.  I then created an object holding this
pagination data and a list of records that I called RecordConnection (also in `api/types/record.py`)
consistent with naming practices of pagination types online.

I also built an input interface called SearchRecordInput (a class in
`api/resolvers/inputs`).  This class has class attributes that hold the values
we will allow to be passed to the API.  I suggest you look at the class to
better understand what I mean by this, but it only has a few class attributes
currently.  This class is translated to the API commands needed by Nomad within
the NomadEntryQueryAPI class defined in 
`api/nomad/resolvers/nomad_data_access/nomad_entry_query_api.py`; it is my
intention that a similar translation will be done for the Invenio API once
this API is understood.  That code should be stored in `api/dantec` and
sub-directories once we develop it.

## Tools planned

We might need to choose an ORM.  I don't think this is appropriate for Nomad,
but we need to evaluate it for DANTEc.  I am considering 
django there seems to be a lot of support for django in
strawberry.  We will see if this is needed, though.

I will note that I personally believe that searching and filtering are
different tasks that should be thought about carefully.  I'd rather deliver more
data to the user and have the client-side library implement post-hoc filtering routines
than to assume that all filtering should be done solely at the data access layer.
I'll showcase this more within the presentation layer once that gets going.
