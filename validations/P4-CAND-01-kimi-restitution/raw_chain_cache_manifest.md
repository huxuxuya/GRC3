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
| `archive_rpc_status_26657.json` | `GET http://204.12.168.157:26657/status` | `df6011685b425ae31b31d9bc2ddc721dec4d4acc73be45f2a60815de658cc55e` | Archive RPC status: `gonka-mainnet`, latest height `4444251`, not catching up. |
| `archive_rpc_status_26657_recheck.json` | Same RPC status endpoint, later recheck | `434da4c15331c298055162c9db5ece5786b079a0ea173cb2b3ba575c90556d65` | Later status recheck; latest height advanced from the first status response. |
| `archive_lcd_node_info_1317.json` | `GET http://204.12.168.157:1317/cosmos/base/tendermint/v1beta1/node_info` | `71de6f7578c06cd701b88b7abf1871c306eacea98a2033acc028711a449d9e1d` | Archive LCD node info: `gonka-mainnet`, app version `v0.2.13`. |
| `archive_lcd_node_info_1317_recheck.json` | Same LCD node info endpoint, later recheck | `71de6f7578c06cd701b88b7abf1871c306eacea98a2033acc028711a449d9e1d` | Same content as initial node-info response. |
| `archive_lcd_all_poc_v2_store_commits_4105361.json` | `GET http://204.12.168.157:1317/productscience/inference/inference/all_poc_v2_store_commits/4105361` | `6f2307fbedb93d100c83fe817ea04626a98d7a8696fb6e59a3d7a1452cd7809a` | Archive LCD current-state response; `commits` array is empty. |
| `archive_lcd_epoch_group_data_266.json` | `GET http://204.12.168.157:1317/productscience/inference/inference/epoch_group_data/266` | `cc5cb6c7dcae4219c486d86760acfeca7197e134f9fcaadf3d947097fa630c1c` | Archive LCD final epoch `266` group; same content as `node1_epoch_group_data_266.json`. |
| `archive_lcd_excluded_participants_266.json` | `GET http://204.12.168.157:1317/productscience/inference/inference/excluded_participants/266` | `c2f0c61423819476ef7488d32a4c056ff17547bb43f944c7520f26292a6c590e` | Archive LCD epoch `266` exclusions; same content as `node1_excluded_participants_266.json`. |
| `archive_lcd_epoch_performance_summary_266.json` | `GET http://204.12.168.157:1317/productscience/inference/inference/epoch_performance_summary/266` | `d0846c3e0375f104d2225539ecf71b58f258f329b82fe70e52ccab641428ea0e` | Archive LCD epoch `266` performance; same content as `node1_epoch_performance_summary_266.json`. |
| `archive_lcd_openapi.json` | `GET http://204.12.168.157:1317/openapi.json` | `0997274c660bbfd2b6ab793e213760071578a56774fd10dcaaa3bfecb584ed26` | LCD returned `Not Implemented`; kept as route-discovery evidence. |
| `archive_lcd_swagger.json` | `GET http://204.12.168.157:1317/swagger.json` | `0997274c660bbfd2b6ab793e213760071578a56774fd10dcaaa3bfecb584ed26` | LCD returned `Not Implemented`; kept as route-discovery evidence. |
| `archive_lcd_productscience_inference_query_service_descriptor.json` | `GET http://204.12.168.157:1317/productscience/inference/inference` | `0997274c660bbfd2b6ab793e213760071578a56774fd10dcaaa3bfecb584ed26` | LCD returned `Not Implemented`; kept as route-discovery evidence. |
| `archive_cli_all_poc_v2_store_commits_4105361_stdout.json` | CLI `inferenced query inference all-poc-v2-store-commits 4105361` without sandbox network access | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | First CLI attempt stdout; empty because sandbox blocked network. |
| `archive_cli_all_poc_v2_store_commits_4105361_stderr.txt` | Same first CLI attempt stderr | `d8af7fcd7bb8b9efc100607b5dfe2eee9ba44bc3873cf74441a38bdefef4c1aa` | Contains sandbox `operation not permitted` error. |
| `archive_cli_all_poc_v2_store_commits_4105361_stdout_retry1.json` | CLI current-state query with network allowed, no `--height` | `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356` | Returned `{}`; current state does not expose the historical commit store. |
| `archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stdout.json` | CLI `inferenced query inference all-poc-v2-store-commits 4105361 --height 4120751 --node tcp://204.12.168.157:26657 -o json` | `a8a06da88128b63a87a9ca0b5cc15130b567c7d801cd3b326db97244229c78af` | Historical archive query succeeded: `44` commit rows, `41` unique submitters. |
| `archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stderr.txt` | Same historical CLI query stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stderr; query succeeded. |
| `node1_epoch_group_data_267.json` | `GET /productscience/inference/inference/epoch_group_data/267` | `db78c6276b813d3421db997f49ccb86e22d748029f6a3ff20374fb6c2b7fe3da` | Root epoch `267` group data: `51` rows, `total_weight=541415`, summed confirmation weight `948169`. |
| `node1_epoch_group_data_267_model_kimi.json` | `GET /productscience/inference/inference/epoch_group_data/267?model_id=moonshotai%2FKimi-K2.6` | `4edeaabe053b23eac623c473115ac6b8158a9de40b57d82e3e19e06af532b342` | Epoch `267` Kimi model rows: `27` rows, model-row weight sum `658820`, confirmation-weight sum `915743`. |
| `node1_epoch_group_data_275.json` | `GET /productscience/inference/inference/epoch_group_data/275` | `d8425fb96f9e344f2cde420a756d51f287ca5b9c08d90917b0edd1c394b52413` | Root epoch `275` group data: `55` rows, `total_weight=736925`, summed confirmation weight `945908`. |
| `node1_epoch_group_data_275_model_kimi.json` | `GET /productscience/inference/inference/epoch_group_data/275?model_id=moonshotai%2FKimi-K2.6` | `b3c8e4804279288988f47d8fa325ac8206c7402b0824d8a06d96b6813846fb17` | Epoch `275` Kimi model rows: `24` rows, model-row weight sum `589904`, confirmation-weight sum `763391`. |

## Current Limitations

- Current-state LCD endpoints do not expose historical PoC commit data for
  start height `4105361`; they return empty commit arrays or `{}`.
- The archive RPC plus local `inferenced` CLI with `--height 4120751` does
  expose the historical e266 commit store.
- Empty current commit-store responses must not be interpreted as proof that no
  historical commits existed.
- The historical CLI commit output does not include `model_id`; it proves PoC
  commit submission by address/count/root hash, not model-specific submission.
