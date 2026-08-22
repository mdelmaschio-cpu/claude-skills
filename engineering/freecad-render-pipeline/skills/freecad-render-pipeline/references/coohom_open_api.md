# Coohom Open API — what's confirmed vs. what needs your partner docs

The user-facing product the initial request called "Cohoom" is **Coohom**
(coohom.com) — a cloud-based interior/space design and rendering platform.
This note documents exactly what's publicly confirmable about its API
versus what only shows up behind partner onboarding, so
`scripts/coohom_client.py` doesn't guess at anything it can't verify.

## Confirmed from Coohom's own public pages

- **Developer hub**: https://developer.coohom.com/ — the entry point for
  API guides and reference docs.
- **Open Platform**: https://open.coohom.com/ — integration hub; per its
  own "For API solutions" page
  (https://open.coohom.com/pub/saas/open-platform/management-integration),
  the integration lets a partner "create a floor plan on your website and
  provide design and rendering service to your users."
- **B2B API service / partner application**: https://www.coohom.com/b2b/api
  — where a business applies for API access; this is a partner program,
  not open/self-serve signup.
- **Response envelope**, per Coohom's own "API Design Standard" help
  article (https://www.coohom.com/helpcenter/api-design-standard /
  mirrored at https://developer.coohom.com/docs/api-design-standard):
  all Open APIs are hosted over HTTPS and respond in JSON with a **unified
  outer structure** — list resources include `count`, `totalCount`,
  `hasMore`, and `result`; a `c` field carries the business status code,
  where **`0` means success** and any other value is an exception. This is
  the one structural fact `coohom_client.py`'s `call()` function relies on
  (`ok = raw.get("c") == 0`).
- **Named API families** referenced in Coohom's own documentation/blog
  material: an **SSO (Single Sign-On) API** to associate an end user with
  Coohom, and **BOM APIs** to retrieve a finished design's bill of
  materials (with SKUs) after the customer completes a design — intended
  for e-commerce integrations where the customer designs with your
  catalog, renders, then purchases.

## Deliberately NOT hardcoded here

Everything below lives behind partner authentication at
https://developer.coohom.com/reference and was not reachable during this
skill's research (that reference host is access-gated, and the specific
paths were not present in any public page found):

- Exact endpoint **paths** (e.g. the real path behind "create a design"
  or "start a render job").
- The **request-signing scheme** (this client only sends an
  `X-Coohom-App-Key` header as a placeholder — replace it with whatever
  your partner docs specify; Coohom's SSO API most likely requires a
  signed request, standard practice for this class of partner API, but
  the exact algorithm is not guessable and this skill will not invent one).
- Whether **arbitrary external 3D models** (FreeCAD/glTF meshes) can be
  uploaded directly, versus Coohom's core workflow being furniture-catalog
  + floorplan based (interior design assembled from a product catalog
  rather than free-form mesh import). Confirm this with your partner
  contact before assuming glTF upload is even in scope — if it isn't, the
  local Blender/Cycles path in this skill is the way to get a
  photorealistic render of arbitrary FreeCAD/BIM geometry regardless.

## How `coohom_client.py` stays honest about this gap

- `coohom_status` never reports `configured: true` unless every endpoint
  path in the config has been overwritten with something that isn't the
  placeholder string, and both `COOHOM_APP_KEY`/`COOHOM_APP_SECRET` are
  set.
- `coohom_call` reads the endpoint path and auth header value entirely
  from your filled-in config — it has no built-in fallback endpoint to
  silently call instead.
- The response parser trusts only the one documented structural fact (the
  `c`/`result` envelope) and passes the rest of the raw response through
  unchanged, so nothing about the payload shape is invented.

## Getting real access

1. Apply for partner API access: https://www.coohom.com/b2b/api
2. Once approved, pull the real base URL, endpoint paths, and signing
   scheme from https://developer.coohom.com/reference
3. Copy `scripts/coohom_endpoints.example.json` to
   `coohom_endpoints.json` and fill in every `REPLACE...` value
4. `export COOHOM_APP_KEY=... COOHOM_APP_SECRET=...`
5. `python scripts/coohom_client.py status --config coohom_endpoints.json`
   should report `configured: true` before you attempt `call`
