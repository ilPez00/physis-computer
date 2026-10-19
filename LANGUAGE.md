# Controlled language perception

The qualified CLI and HUD can inspect a small, explicit semantic fragment without
a generative model, network call, or account. The parser is
`controlled:physis-language/1`, not GF or general natural-language understanding.

```sh
physis language infer 'Socrates is human. All humans are mortal.' --language en
physis language infer 'Socrate è un uomo. Tutti gli uomini sono mortali.' --language it
physis language infer 'Human(socrates); forall x: Human(x) -> Mortal(x)' --language formal
physis language compare 'Socrates is human. All humans are mortal.' \
  'Socrate è un uomo. Tutti gli uomini sono mortali.'
physis language linearize 'Human(socrates); forall x: Human(x) -> Mortal(x)' \
  --language formal --target-language it
```

`inspect`, `parse`, `normalize`, `compare`, `infer`, and `linearize` are read-only.
Only explicit `ingest` records a source and its conditional derivations. `explain`
accepts its source ID or a projected proposition/proof ID. `withdraw <source-id>`
removes that source's active projections but preserves the append-only history.
Identical withdrawn input cannot silently revive itself.

The concept map is `socrates-human-mortal/1`: Human/Mortal, H/M, English/Italian
lexical realizations, and explicit Socrates/Socrate/s aliases. Other formal
predicates are not automatically translatable concepts. Source spans are UTF-8
byte offsets. Formula identities normalize bound-variable names; original source
identities and evidence remain separate.

The admitted fragment is unary, range-restricted Horn logic with explicit signed
facts. Negation is not inferred from absence. Contradictory support is retained,
not turned into arbitrary conclusions. Use `No humans are mortal` / `Nessun uomo
è mortale` for an unambiguous universal negative. Ambiguous quantifier-negation
scope, pronouns, unsupported syntax and partial semantics remain explicit gaps.

Every proof names its premise, rule and substitution and is independently
replayed. `grounded=false` is intentional: valid inference from asserted premises
does not measure the physical world or certify their truth.

Limits are separate: 16 KiB source, 64 statements, at most 256 matching steps,
and 256 KiB serialized response. Exhaustion is not a completed fixed point.

In the HUD, type `:language it Socrate è un uomo. Tutti gli uomini sono mortali.`.
The Ontologies inspector shows source, normalized assertions, gaps and proofs.
`--snapshot --view='language:formal Human(socrates); forall x: Human(x) -> Mortal(x)'`
uses the same runtime without writing evidence. A cached interactive report is
marked historical when the observed world changes.

The native MCP `language` area exposes the same operations:
`PHYSIS_MCP_SURFACE=area:language physis serve --stdio --path .`.

## Repeatable qualification loop

The support script uses Python 3's standard library; the engine has no Python
runtime dependency. It exercises independent positive/negative controls, the real
MCP stdio transport, persistence/restart/withdrawal, and the exact HUD bytes.
Mutation is confined to a fresh temporary world; the receipt hashes both binaries.

```sh
python3 language-loop.py --physis ./bin/physis --hud ./bin/physis-hud
```

Missing executables report `UNVERIFIABLE` and exit nonzero. Failed checks report
the reason and exit nonzero. This loop does not qualify GF, Z3, Stanza, legacy
Logos/Nous transports, open-domain language, or arbitrary program equivalence.

Existing `v1.2.0` release bytes are immutable. This capability belongs in a newly
qualified release, not a replacement archive with the same tag.
