# P4 Raw Chain Cache Manifest

All node responses fetched during the P4 conceptual audit are stored under
`raw_chain_cache/` before any derived analysis is written. This keeps the audit
re-checkable without another node request.

Default node used for this pass:
`http://node1.gonka.ai:8000/chain-api`.

## Files

| File | Endpoint / request | SHA-256 | Notes |
|---|---|---|---|
| `node1_all_poc_v2_store_commits_4105361.json` | `GET /productscience/inference/inference/all_poc_v2_store_commits/4105361` | `6f2307fbedb93d100c83fe817ea04626a98d7a8696fb6e59a3d7a1452cd7809a` | Current endpoint response; `commits` array is empty. Not sufficient to disprove historical e266 nonce submission. |
| `node1_epoch_group_data_266.json` | `GET /productscience/inference/inference/epoch_group_data/266` | `cc5cb6c7dcae4219c486d86760acfeca7197e134f9fcaadf3d947097fa630c1c` | Current endpoint returns epoch `266` final group with `46` validation-weight rows and `total_weight=335159`. |
| `node1_excluded_participants_266.json` | `GET /productscience/inference/inference/excluded_participants/266` | `c2f0c61423819476ef7488d32a4c056ff17547bb43f944c7520f26292a6c590e` | Current endpoint returns `7` excluded participant rows for epoch `266`. |
| `node1_epoch_performance_summary_266.json` | `GET /productscience/inference/inference/epoch_performance_summary/266` | `d0846c3e0375f104d2225539ecf71b58f258f329b82fe70e52ccab641428ea0e` | Current endpoint returns `48` performance summary rows for epoch `266`. |
| `node1_height_4120751_all_poc_v2_store_commits_4105361.json` | Same commits endpoint with header `x-cosmos-block-height: 4120751` | `e94d861f5d570c546f29faa2cab00c7ee8149b06848978fee7e6043a4baca0e2` | Node returned error `failed to load state at height 4120751`; kept as endpoint-limitation evidence. |
| `node1_height_4120751_epoch_group_data_266.json` | Same group endpoint with header `x-cosmos-block-height: 4120751` | `e94d861f5d570c546f29faa2cab00c7ee8149b06848978fee7e6043a4baca0e2` | Same historical-state error as above. |
| `node1_height_4120751_excluded_participants_266.json` | Same exclusions endpoint with header `x-cosmos-block-height: 4120751` | `e94d861f5d570c546f29faa2cab00c7ee8149b06848978fee7e6043a4baca0e2` | Same historical-state error as above. |
| `node1_height_4120751_epoch_performance_summary_266.json` | Same performance endpoint with header `x-cosmos-block-height: 4120751` | `e94d861f5d570c546f29faa2cab00c7ee8149b06848978fee7e6043a4baca0e2` | Same historical-state error as above. |
| `node1_epoch_group_data_267.json` | `GET /productscience/inference/inference/epoch_group_data/267` | `db78c6276b813d3421db997f49ccb86e22d748029f6a3ff20374fb6c2b7fe3da` | Root epoch `267` group data: `51` rows, `total_weight=541415`, summed confirmation weight `948169`. |
| `node1_epoch_group_data_267_model_kimi.json` | `GET /productscience/inference/inference/epoch_group_data/267?model_id=moonshotai%2FKimi-K2.6` | `4edeaabe053b23eac623c473115ac6b8158a9de40b57d82e3e19e06af532b342` | Epoch `267` Kimi model rows: `27` rows, model-row weight sum `658820`, confirmation-weight sum `915743`. |
| `node1_epoch_group_data_275.json` | `GET /productscience/inference/inference/epoch_group_data/275` | `d8425fb96f9e344f2cde420a756d51f287ca5b9c08d90917b0edd1c394b52413` | Root epoch `275` group data: `55` rows, `total_weight=736925`, summed confirmation weight `945908`. |
| `node1_epoch_group_data_275_model_kimi.json` | `GET /productscience/inference/inference/epoch_group_data/275?model_id=moonshotai%2FKimi-K2.6` | `b3c8e4804279288988f47d8fa325ac8206c7402b0824d8a06d96b6813846fb17` | Epoch `275` Kimi model rows: `24` rows, model-row weight sum `589904`, confirmation-weight sum `763391`. |

## Current Limitations

- `node1` current LCD returns final epoch group/performance data for epoch
  `266`, but does not expose historical PoC commit data for start height
  `4105361`.
- `x-cosmos-block-height: 4120751` requests to `node1` failed with a
  historical-state error, so e266 nonce-submission proof remains blocked until
  an archive source is added.
- Empty current commit-store responses must not be interpreted as proof that no
  historical commits existed.
