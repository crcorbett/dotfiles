# TanStack and Effect architecture

The app owns separate client/server ManagedRuntimes. Browser HTTP uses Fetch.
Server loaders receive the same application client through an in-process handler
Layer, avoiding deployment loopback and preserving one composition graph.

Loader Effects are executed at the route boundary. An owning Schema encodes an
`Exit` before it crosses SSR and restores it during rendering. Typed transport
failures remain in the error channel; impossible codec failures are defects.

Routes or feature boundaries own data loading, Effect/service execution,
mutations, commands, shared state, and page workflow/error policy. Presentation
leaves accept narrow readonly values and action callbacks, then own rendering,
accessibility, pure derivation, and genuinely local UI state. They remain
service-unaware.

RPC and HTTP API are parallel transports over one domain service. They must not
import each other or copy domain policy. Runtime execution and Layer assembly
remain app-owned.
