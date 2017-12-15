# LSWA-Project

Repo for LSWA Project - Fall 2017

> From Project Design

Logics:

1. User A follows (->) User B, B -> C, so A should probably follow C
2. Multiple people that A follows all follow User C, so A probably wants to follow C.
  A → {B};   {B}→ H; so A → H
3. Indirect recommendation by following a chain of followers
  A -> B -> … -> Z. so A -> Z
4. If A follows B and C follows B, A might want to follow C.
  A → B; C → B; so A ←→ C
5. A and C both follow multiple people in common, so A and C should follow each other
  A → {B}; C → {B}; so A ← → C
6. User A does not follow User B, but User B follows A. Might want to follow back?
  A does not follow B, B → A; A → B

# Responsibilities:

Matthew - Grouping weight + preventing cycles (Logic 2 + 6). + Setting up deployment environment

Rye - weighting by number of followers following (Logic 1 + 6). + Ensuring populate scripts work.

Malini - Going through the chain of subscriptions (Logic 3 + 5).

Kelly - Shared following interest recommendation service via RPC service (Logic 4).

# General Outline for the Project:

We have a giant list of users, all of whom have subscriptions.

We want to generate new subscriptions they do not currently have:

To do that, we generate a mapping based upon some sort of logic (see above).

Check against if we currently follow them

Check against if we are followed

Check against if they follow who we follow

If all is good, we throw them into a giant map!

Then, after we have a giant mapping of users, we reduce it by the summing up the number of times a user shows up in the map.

For scaling, we do that again for all they follow, up to some number of layers.

For the online component, we have a cache of recommend users--update on request.

For the offline component, we actually do the computations and weighting.
