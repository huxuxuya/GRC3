# P4 Source Cache Manifest

This folder stores copied source artifacts from the pinned Votkon repository
used as claim labels during the conceptual audit. These are not treated as raw
chain proof.

Source repository: `https://github.com/votkon/gonka-kimi-restitution`

Pinned source commit: `5462c55a6b95d50dfb53bdc4211cdcd31369c2ea`

## Files

| File | Source path | SHA-256 | Use |
|---|---|---|---|
| `votkon_e265_compensation_265.json` | `e265/compensation_265.json` | `9cb20ca589e28da48df183ea141d07fdabf6e8c011f617f2c55c6edb041266ab` | Source aggregate e265 claim used for attack summary labels and theoretical reward-pool input. |
| `votkon_e265_compensation_265.csv` | `e265/compensation_265.csv` | `cc381ee8b259bcfb001f508bdf9629259d72b5ea4ef940f2a0ac2be0da20a44a` | Source e265 row set used as claim labels for affected-row counts. |
| `votkon_e266_epoch266_commits.json` | `e266/epoch266_commits.json` | `f1a016c29a10fe4d8f752f12b2bd597cf6303cbcc4e51f1c85c139cbcbbd20b5` | Source model labels for e266 commit rows; exact raw commit row match is checked in pass 04. |
| `votkon_e266_compensation_266_nonces.csv` | `e266/compensation_266_nonces.csv` | `c948b9c67519825b290f7f76a0fbe0a5b55c12a672cab5a3b386d957605ec330` | Source nonce-compensation row set used for scope classification. |
| `votkon_e266_compensation_266_delegation.csv` | `e266/compensation_266_delegation.csv` | `b8099566d0c70c10ce97e5fbdd984727db9f1362e8cf54d35353bdd4c1b36186` | Source delegation-compensation row set used for scope classification. |
| `votkon_e266_compensation_266.json` | `e266/compensation_266.json` | `9501bc38755245ce796abc2c43bac9b2d8d19efc057ceb4b4c60befba89ff26f` | Source aggregate e266 claim, including excluded-operator list. |
| `votkon_e266_epoch266_kimi_delegators.json` | `e266/epoch266_kimi_delegators.json` | `2d01136568a4ef93ea178b01887b2064bf2d6e7a6e94f090aa270c9965cabed5` | Source delegation snapshot labels used only to cross-check raw chain `poc_delegation` responses in pass 05. |

## Pass 06 GroupCap Source Files

| Epoch | JSON file / SHA-256 | CSV file / SHA-256 |
|---:|---|---|
| `267` | `votkon_e267_compensation_267.json` / `ccc0574a479829ab4060839a8d43ebde439179a0885c4ca5622b27015bc17ead` | `votkon_e267_compensation_267.csv` / `568fc2e4dd6c5e7a70cb13aea999e4e239e743604225ab57ee1505a6debc8704` |
| `268` | `votkon_e268_compensation_268.json` / `28252eea9a1e01fd7dc3f1fd88c0ffd72f6c5e13eff37bc27fcf8995f04f33e6` | `votkon_e268_compensation_268.csv` / `daaa8a77a43a9059426967b5bf8d843ac278b21c3c6d2023a102e0dcbe0b621a` |
| `269` | `votkon_e269_compensation_269.json` / `9ba1edc9d13f4931c85cff7363c8025ed2ccc95d26bd6fe52cf40e5c41d5f7b0` | `votkon_e269_compensation_269.csv` / `b7e54976bc8a6f0f6f90834c4e186ba3f7a598a3940e7f7f7abebf3e73bf489e` |
| `270` | `votkon_e270_compensation_270.json` / `58b2cb355f63e5790ab17225797383abe3e6cb996d7dfd9a90e57a354fa78110` | `votkon_e270_compensation_270.csv` / `fc3270493979c14b48a3d86660fe199e111f89aeb85e0252d2dbd0c7f7e41abc` |
| `271` | `votkon_e271_compensation_271.json` / `395f2ba4eac1027de46c4421df6c71e40e0d7f3bed3b4c566c01d747dbf65d00` | `votkon_e271_compensation_271.csv` / `8e974f7398c74417e75df8f4639a93a20fba6462f1b536b0d062f8232a12d45b` |
| `272` | `votkon_e272_compensation_272.json` / `051bb43fd5ade21da0aaf5e2c39cb1af55be06538497863b59d45c7b93ce183e` | `votkon_e272_compensation_272.csv` / `10d269155f92e0cb7382c523c4ca6d2a16adfb6c65a5d2fe37450c4862114e25` |
| `273` | `votkon_e273_compensation_273.json` / `745c786bb611ae65b5cc9c1f1f0d349e38e40244ca08a9a6e3e94036bb98f8d4` | `votkon_e273_compensation_273.csv` / `9a9270ba12b2922df8c9b8ca68783b0d9a3c39031826e235af329e66eb7bafcb` |
| `274` | `votkon_e274_compensation_274.json` / `d43bd732929e97e3f25b9f3dfcaa79d4d47d33afc94dcf0bee0c3efdb35eaa20` | `votkon_e274_compensation_274.csv` / `31f1fa0686439b2334fa3e9fc6463d99a6067ad8a28a182a80eb5401734a3969` |
| `275` | `votkon_e275_compensation_275.json` / `0f5d18c1f6350038065365f200991d1b2dc649c69f7d66199512928aeeb81ae3` | `votkon_e275_compensation_275.csv` / `0ef73e7196debe2b6689f780f33428c4398d53a6943a50d4653010aa53b08882` |
| `276` | `votkon_e276_compensation_276.json` / `00b17edf445df178e97e8ff6eb3abcd046d771122c404bc71023eb3d8e9ea707` | `votkon_e276_compensation_276.csv` / `66e2e38de0a2a23982a4e1bbe7682ce1ca6e3c1d059401ad65b61ee16248873f` |

Additional source note copied for methodology review:

| File | Source path | SHA-256 | Use |
|---|---|---|---|
| `votkon_e267_GROUP_CAP.md` | `e267/GROUP_CAP.md` | `d861cab4c4c722d5ee407bc7a7a6eb45db40fadc98130bbac3cd79dd4110e19a` | Source GroupCap methodology text used to identify denominator claims and internal wording conflict. |
