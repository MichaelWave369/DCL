# DCL Observatory, React GitHub Pages

Public, static companion to the **Demiurgic Cosmology Lattice Runtime v0.1** in `src/dcl_runtime/`.

## Local setup

    cd site
    npm install
    npm test
    npm run dev
    npm run build

## What the hosted application does

- Explore 12 bounded input variables (6 constraint, 6 coherence) with a live scoring playground.
- Calculate the reference D, Phi, DCR and CMI equations, plus classifications and dominant variables.
- Explore the 12 × 12 × 12 × 12 *conceptual lattice indexing system*.
- Inspect the repository's existing illustrative observation receipt, including sources and counter-evidence.
- Export a **scenario JSON** file clearly marked as non-canonical. The browser **does not** issue or verify canonical receipt IDs.

The Python runtime remains the authoritative local verifier for receipt structure and IDs. There is no remote scoring API, network telemetry, backend, device access, or storage of user-generated scenario data. The default fixture is packaged into the public Pages build and is already public in `examples/receipt_example.json`.

This model does **not** provide proof of metaphysical claims, a literal prison universe, or a twelve-dimensional physics theory. Its numbers are *internal measures defined by the DCL model*, not direct scientific measurements of the world.

## Deploy

After merging the PR, go to **Settings → Pages → Build and deployment** and choose **GitHub Actions** as the source. The `DCL Observatory Pages` workflow builds the app after changes to `main` (or with manual workflow dispatch).

Configured destination: https://michaelwave369.github.io/DCL/

The Vite base path uses the case-sensitive `/DCL/` project route.

## CI

Actions runs the original Python test suite, browser numerical-parity/unit tests, an SSR smoke render test to catch runtime React blank screens, and a production build.
