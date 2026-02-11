# Overview

Code to set-up and populate the GraphQL sever using strawberry.

# Use

Make sure uv is installed on your machine.

1. Run `uv sync` within the top directory of this repo.
2. Run `uv run strawberry dev main --port 5432` to get a development server

The first command should build the environment needed, and the second should
start a GraphQL dev server that listens at port 5432.

# Design

## What's been implemented

So far, this is minimal.  I have begun to flush out the Nomad data model.
I started with the most basic objects, Element, which is not stored in 
the Nomad repo but within a json file called elementData.json.  I built an
object to lazy load this data and a GraphQL API to pull all data
(elements) and to just a pull a single element (element(symbol) where symbol is "H" or "Pb").
If you go to the dev server, you can play around with GraphQL API queries.

## Tools planned

Element (as well as future classes) will inherit from strawberry.relay.Node.
This will allow us to use Relay in conjuction with React on the front end to
build a modern, fast, GraphQL compliant web-application supporting extension
and maintenance.

Once I have to connected to Nomad database, I plan to utilize
strawberry.dataloader.DataLoader to consolidate requests to Nomad API.

While Nomad supports pagination inherently, I am planning to implement
GraphQL pagination through strawberry's ListConnection.  This does not
deliver totalCounts (of results) as Nomad does, but I am thinking it we might
not need that information.

In addition, I might need to choose an ORM.  I have not decided upon this yet
as I do not know if the Nomad API really supports that.  If I need to, I am considering 
django as strawberry there seems to be a lot of support for django in
strawberry.

I will note that I personally believe that searching and filtering are
different tasks that should be thought about carefully.  I rather deliver more
data to the user and have the client-side library implement post-hoc filtering routines
than to assume that all filtering should be done at the data access layer.
I'll showcase this more within the presentation layer once that gets going.
