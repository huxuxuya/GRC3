# P4 Source Cache Manifest

This folder stores copied source artifacts from the pinned Votkon repository
used as claim labels during the conceptual audit. These are not treated as raw
chain proof.

Source repository: `https://github.com/votkon/gonka-kimi-restitution`

Pinned source commit: `5462c55a6b95d50dfb53bdc4211cdcd31369c2ea`

## Files

| File | Source path | SHA-256 | Use |
|---|---|---|---|
| `votkon_e266_epoch266_commits.json` | `e266/epoch266_commits.json` | `f1a016c29a10fe4d8f752f12b2bd597cf6303cbcc4e51f1c85c139cbcbbd20b5` | Source model labels for e266 commit rows; exact raw commit row match is checked in pass 04. |
| `votkon_e266_compensation_266_nonces.csv` | `e266/compensation_266_nonces.csv` | `c948b9c67519825b290f7f76a0fbe0a5b55c12a672cab5a3b386d957605ec330` | Source nonce-compensation row set used for scope classification. |
| `votkon_e266_compensation_266_delegation.csv` | `e266/compensation_266_delegation.csv` | `b8099566d0c70c10ce97e5fbdd984727db9f1362e8cf54d35353bdd4c1b36186` | Source delegation-compensation row set used for scope classification. |
| `votkon_e266_compensation_266.json` | `e266/compensation_266.json` | `9501bc38755245ce796abc2c43bac9b2d8d19efc057ceb4b4c60befba89ff26f` | Source aggregate e266 claim, including excluded-operator list. |
