# Claude Code bridge compatibility experiment

Research-stage compatibility work for connecting an isolated Hermes Agent instance to the third-party [claude-sub-as-api](https://github.com/huybik/claude-sub-as-api) bridge. This is not a production bridge, a Claude Code distribution, or an authentication service. No account credentials or conversations are included.

## What is here

`cache_adapter.py` defines a pure Python request transformation. It removes top-level `cache_control` fields from `system` content blocks and `tools`, leaving the original request and message-level markers unchanged. `cache-marker.patch` implements the corresponding transformation in the upstream bridge's validator path. The bridge revision inspected was `e38abb6197cd0c731536869b4515f56f1c2b6911`. The patch was checked against that exact revision; apply it only in a disposable copy using `git apply --check cache-marker.patch` followed by `git apply cache-marker.patch`. It is experimental and is not a production-ready installation.

Run the local tests:

```sh
python3 -m unittest -v test_cache_adapter
```

## Observations and limitations

- In an isolated offline test, a Hermes copy, a temporary adapted bridge, and a simulated Claude process completed a tool-call round trip. This does not test real Claude Code, real authentication, subscriptions, or billing.
- The upstream bridge rejects cache markers on system and tool blocks; removing them is a compatibility workaround, not evidence that prompt caching works or that its economics are acceptable.
- A synthetic process crash after a partial stream caused the bridge to emit an error; Anthropic SDK 0.87.0 raised `APIStatusError`. End-to-end error handling in Hermes remains unverified.
- The upstream bridge writes history to temporary files. An isolated SIGKILL test left synthetic history on disk (mode 0600). Claude Code may also create its own files; do not use private conversations until persistence is understood and mitigated.
- The third-party bridge has not received a full security audit. Test in an isolated environment, with synthetic data and no access to unrelated credentials. Respect service terms and supported-region requirements. Actual suitability of this integration under provider terms is unverified.

No upstream bridge code is redistributed in this repository. The adapter and tests alone do not provide a running service.
