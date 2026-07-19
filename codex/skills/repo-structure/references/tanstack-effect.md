# TanStack and Effect architecture

The app owns separate client/server ManagedRuntimes. Browser HTTP uses Fetch.
Server loaders receive the same application client through an in-process handler
Layer, avoiding deployment loopback and preserving one composition graph.

Loader Effects are executed at the route boundary. An owning Schema encodes an
`Exit` before it crosses SSR and restores it during rendering. Typed transport
failures remain in the error channel; impossible codec failures are defects.

Routes own cross-feature orchestration and shared page policy. A leaf component
owns its specific query/read/command, skeleton, and fallback; do not hoist those
only to pass values back down. Pure presentation leaves accept narrow readonly
props and stay service-unaware.

RPC and HTTP API are parallel transports over one domain service. They must not
import each other or copy domain policy. Runtime execution and Layer assembly
remain app-owned.
