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
| `archive_lcd_height_4104861_poc_delegation_gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt.json` | `GET http://204.12.168.157:1317/productscience/inference/inference/poc_delegation/gonka1tja3g2da45efhe2p83gk3whtussmgmtsdlgprt` with header `x-cosmos-block-height: 4104861` | `a8318456e4ca9b1a405a703a4e6f8b215c5cec895b87a35b16232e21e685e0fd` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka1hwvel7n3zuk6wruefuzc356l9myske9stckwnz.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `3d039d4deb1c58382cf5cb881eb886f23a5ab862021290e221e7582301b61b22` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka12pcu9mcrpa4w4sjd9y3dsksnvu495ss6f9r4ra.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `b67480ef7c1b11790e88f28ada41d2f30c1553b8022792743372a4bde9ecf7d9` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka1tlvg4kjx7ljd5thgd5fkgh39q6lu8cmxupktgg.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `6e69a69ca4c5a914f3cf2d7eb4e67a1b84e2a0e3d8d3f0978dcb53cde6a6cbd9` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `e8712b579a1ebfb4b4b7d370224c7a55201db11b9403f062d4d87554d5db28fe` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `f45360a42f0eae95891de605440af2f6f7961e83cead6c155f910b0ea936cb33` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka1tmk2tzdneht6smu34pkmqdvu7p34qavvmwtwq2.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `5dc5aee04a87ef0dd5adf3b0cfee35990c5620809bcfde8b4124b669b73d21a7` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `52edfe4bb78af957df5cabd7af365aac38bc707eadf8e378653453ff38bf327c` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4104861_poc_delegation_gonka14ef2pxjge75gflqftn7m2wy0xv59gq9uc7qnct.json` | Same `poc_delegation/<address>` request with header `x-cosmos-block-height: 4104861` | `96f0f3474d0ce2adf353ac811844f0ad1d3e89752cf74ec81ff97c8ba2e46d3f` | Raw e266 delegation snapshot: Kimi delegated to `gonka1q5xt54...`. |
| `archive_lcd_height_4105361_params.json` | `GET http://204.12.168.157:1317/productscience/inference/inference/params` with header `x-cosmos-block-height: 4105361` | `ba83ae0f9b35d858e056d368c33d0d9cc3232c9aca5b3d69fe9bfe226628d16b` | Raw params used for e266 delegation pass; confirms `deploy_window=500`, `no_participation_penalty=0.15`, and `delegation_share=0.05`. |
| `archive_lcd_openapi.json` | `GET http://204.12.168.157:1317/openapi.json` | `0997274c660bbfd2b6ab793e213760071578a56774fd10dcaaa3bfecb584ed26` | LCD returned `Not Implemented`; kept as route-discovery evidence. |
| `archive_lcd_swagger.json` | `GET http://204.12.168.157:1317/swagger.json` | `0997274c660bbfd2b6ab793e213760071578a56774fd10dcaaa3bfecb584ed26` | LCD returned `Not Implemented`; kept as route-discovery evidence. |
| `archive_lcd_productscience_inference_query_service_descriptor.json` | `GET http://204.12.168.157:1317/productscience/inference/inference` | `0997274c660bbfd2b6ab793e213760071578a56774fd10dcaaa3bfecb584ed26` | LCD returned `Not Implemented`; kept as route-discovery evidence. |
| `archive_cli_all_poc_v2_store_commits_4105361_stdout.json` | CLI `inferenced query inference all-poc-v2-store-commits 4105361` without sandbox network access | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | First CLI attempt stdout; empty because sandbox blocked network. |
| `archive_cli_all_poc_v2_store_commits_4105361_stderr.txt` | Same first CLI attempt stderr | `d8af7fcd7bb8b9efc100607b5dfe2eee9ba44bc3873cf74441a38bdefef4c1aa` | Contains sandbox `operation not permitted` error. |
| `archive_cli_all_poc_v2_store_commits_4105361_stdout_retry1.json` | CLI current-state query with network allowed, no `--height` | `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356` | Returned `{}`; current state does not expose the historical commit store. |
| `archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stdout.json` | CLI `inferenced query inference all-poc-v2-store-commits 4105361 --height 4120751 --node tcp://204.12.168.157:26657 -o json` | `a8a06da88128b63a87a9ca0b5cc15130b567c7d801cd3b326db97244229c78af` | Historical archive query succeeded: `44` commit rows, `41` unique submitters. |
| `archive_cli_height_4120751_all_poc_v2_store_commits_4105361_stderr.txt` | Same historical CLI query stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stderr; query succeeded. |
| `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stdout.json` | First CLI `poc-v2-validations-for-stage 4105361` attempt | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stdout; first attempt used invalid positional argument. |
| `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stderr.txt` | Same first attempt stderr | `0b707766896e876da1b24fffe5b5d32bf5aff075cc8cbfa7d1da48bbe0a102e4` | CLI usage error: command requires `--block-height`. |
| `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stdout_retry1.json` | CLI validation query retry with correct flag but sandboxed network | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stdout; sandbox blocked RPC connection. |
| `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stderr_retry1.txt` | Same retry stderr | `d8af7fcd7bb8b9efc100607b5dfe2eee9ba44bc3873cf74441a38bdefef4c1aa` | Contains sandbox `operation not permitted` error. |
| `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stdout_retry2.json` | CLI `poc-v2-validations-for-stage --block-height 4105361 --height 4120751 --node tcp://204.12.168.157:26657 -o json` with network allowed | `c3e4e0e5f5ac52d9bae169435aefa8a42f8eb4620c2e5330b4aa201da32817ae` | Historical archive query succeeded; validation records exist but do not include `model_id`. |
| `archive_cli_height_4120751_poc_v2_validations_for_stage_4105361_stderr_retry2.txt` | Same successful retry stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stderr; query succeeded. |
| `archive_cli_height_4120751_poc_validation_snapshot_4105361_stdout.json` | CLI `po-c-validation-snapshot --poc-stage-start-height 4105361 --height 4120751` | `ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356` | Returned `{}`; no usable e266 stage snapshot from this query. |
| `archive_cli_height_4120751_poc_validation_snapshot_4105361_stderr.txt` | Same snapshot query stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stderr; query succeeded but returned empty object. |
| `archive_cli_height_4103170_epoch_group_data_265_stdout.json` | CLI `show-epoch-group-data 265 --height 4103170` | `a37153a76ad523b9cb667952c2e2f0b1202b7fb86934089fa0a315a23c4ea4f1` | Epoch `265` root group state at last healthy height used for e265 row classifier. |
| `archive_cli_height_4105360_epoch_group_data_265_stdout.json` | CLI `show-epoch-group-data 265 --height 4105360` | `d85b4feb34994939db8058cf0db916562d7cd55b4c8715299d3018e7bda0928c` | Epoch `265` root group state at epoch end used for e265 row classifier. |
| `archive_cli_height_4103170_epoch_group_data_265_model_kimi_stdout.json` | CLI `show-epoch-group-data 265 --model-id moonshotai/Kimi-K2.6 --height 4103170` | `f42ae7355b95d77f136bd90f2127effc36ecf5c24fdf1af2ca0e74c7c674185a` | Epoch `265` Kimi model rows at healthy height. |
| `archive_cli_height_4105360_epoch_group_data_265_model_kimi_stdout.json` | CLI `show-epoch-group-data 265 --model-id moonshotai/Kimi-K2.6 --height 4105360` | `f42ae7355b95d77f136bd90f2127effc36ecf5c24fdf1af2ca0e74c7c674185a` | Epoch `265` Kimi model rows at epoch end; same content hash as healthy-height Kimi model rows. |
| `archive_cli_epoch265_performance_gonka1j7x6dv42xehe9e5au4ku3wvzwtqlegfjhlvzj6_stdout.json` | CLI `show-epoch-performance-summary-by-participant 265 gonka1j7...` | `d78cd92c2cabeec66508d422be857033d145f64652228de42fccfe9ec8e58b72` | Performance row lacks `rewarded_coins`; treated as zero reward in classifier. |
| `archive_cli_epoch265_performance_gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu_stdout.json` | CLI `show-epoch-performance-summary-by-participant 265 gonka17...` | `65eb46fcdc0203915ecc016b41b57c0c1519d064cc8c01addfb0da45f722cf77` | Performance row has `rewarded_coins=54393492283376`. |
| `archive_cli_epoch265_performance_gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y_stdout.json` | CLI `show-epoch-performance-summary-by-participant 265 gonka1830...` | `ddaed873db26fe55f1d01edf68643ad9d18eb3ca704bf9c143ecdbfe19a4e663` | Performance row lacks `rewarded_coins`; treated as zero reward in classifier. |
| `archive_cli_excluded_participants_265_stdout.json` | First CLI `excluded-participants 265` attempt stdout | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stdout; first attempt used invalid positional argument. |
| `archive_cli_excluded_participants_265_stderr.txt` | First CLI `excluded-participants 265` attempt stderr | `0b707766896e876da1b24fffe5b5d32bf5aff075cc8cbfa7d1da48bbe0a102e4` | CLI usage error: command requires `--epoch-index`. |
| `archive_cli_excluded_participants_265_stdout_retry1.json` | CLI `excluded-participants --epoch-index 265` | `5fe1bc769fc3f5ef20e41289093347feea0150d05807a1c6abbd8a736ad435df` | Epoch `265` exclusions; includes `gonka1j7...` and `gonka1830...` as `failed_confirmation_poc` at block `4103171`. |
| `archive_cli_excluded_participants_265_stderr_retry1.txt` | Same retry stderr | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty stderr; query succeeded. |
| `case6_raw_stage_4102890_all_poc_v2_store_commits.json` | Copied raw cache from Case 6: `GET /productscience/inference/inference/all_poc_v2_store_commits/4102890` | `c4db53cda087750c230e3433158ea3c2e1ddd192530bfc08714a5d3821fbb6e2` | Stage `4102890` raw commits used for e265 `gonka1830...` row-level cPoC evidence. |
| `case6_raw_stage_4102890_poc_v2_validations_for_stage.json` | Copied raw cache from Case 6: `GET /productscience/inference/inference/poc_v2_validations_for_stage/4102890` | `d38a8ed68e2b065879046d04a11d6d5f1d1642033db3eb8c03c49f9e04b04f1e` | Stage `4102890` raw validation records used to distinguish submission shortfall from no-submission rows. |
| `case6_raw_height_4103171_stage_4102890_poc_validation_snapshot.json` | Copied raw cache from Case 6: `GET /productscience/inference/inference/poc_validation_snapshot/4102890` at height `4103171` | `9060941b61a1fae67de64a50cdb05630372df2b34400bdd17c4298cb4847aaf9` | Snapshot model voting powers used for the `>2/3` validation-power check. |
| `case6_raw_epoch265_model_qwen_epoch_group_data.json` | Copied raw cache from Case 6: `GET /productscience/inference/inference/epoch_group_data/265?model_id=Qwen%2FQwen3-235B-A22B-Instruct-2507-FP8` | `ebcd9fe3db081e747970cb9f6fe048ad248900fa8396f5942c83810eeef0390a` | Epoch `265` Qwen model group state used to prove `gonka1830...` is not in the Qwen model group. |
| `node1_epoch_group_data_267.json` | `GET /productscience/inference/inference/epoch_group_data/267` | `db78c6276b813d3421db997f49ccb86e22d748029f6a3ff20374fb6c2b7fe3da` | Root epoch `267` group data: `51` rows, `total_weight=541415`, summed confirmation weight `948169`. |
| `node1_epoch_group_data_267_model_kimi.json` | `GET /productscience/inference/inference/epoch_group_data/267?model_id=moonshotai%2FKimi-K2.6` | `4edeaabe053b23eac623c473115ac6b8158a9de40b57d82e3e19e06af532b342` | Epoch `267` Kimi model rows: `27` rows, model-row weight sum `658820`, confirmation-weight sum `915743`. |
| `node1_epoch_group_data_275.json` | `GET /productscience/inference/inference/epoch_group_data/275` | `d8425fb96f9e344f2cde420a756d51f287ca5b9c08d90917b0edd1c394b52413` | Root epoch `275` group data: `55` rows, `total_weight=736925`, summed confirmation weight `945908`. |
| `node1_epoch_group_data_275_model_kimi.json` | `GET /productscience/inference/inference/epoch_group_data/275?model_id=moonshotai%2FKimi-K2.6` | `b3c8e4804279288988f47d8fa325ac8206c7402b0824d8a06d96b6813846fb17` | Epoch `275` Kimi model rows: `24` rows, model-row weight sum `589904`, confirmation-weight sum `763391`. |

## Pass 06 GroupCap Raw Files

The pass 06 scan saved root epoch group data, Kimi model-group data, and epoch
performance summaries for every epoch `267..276` from
`http://node1.gonka.ai:8000/chain-api`.

| Epoch | Root group SHA-256 | Kimi model group SHA-256 | Performance summary SHA-256 |
|---:|---|---|---|
| `267` | `db78c6276b813d3421db997f49ccb86e22d748029f6a3ff20374fb6c2b7fe3da` | `4edeaabe053b23eac623c473115ac6b8158a9de40b57d82e3e19e06af532b342` | `2b2f94b5856385ad67f296b738f088d80e671b03cfaaa03901434d0958775528` |
| `268` | `92d61eb9ba3d049fd7d381804d8b6cef09b2f901495e944da56def2de8c77beb` | `09baae0dfafda61823cc8830c00cc0f5593035ff93f0a9af39b9393e11b287b3` | `46f634b5d320fa213f1f8f6bfed8a54fd77cd61c51cdb88f86b94749b9cd8547` |
| `269` | `46ec8aa8ec7fb6cb704426524167d048ea9d4326a1b2c5db332aa1e521c57e38` | `2c6e70195615eb82ff311074493cbac2b51a80bc9c35519932f64bc4ab2fd6ab` | `558f767f029c9a8c0e54e50c12cb0365a54e5197616a5f9963566682a54ed1c6` |
| `270` | `a8eef9021083d79e7044053e8b847fddf7af67eee46e35550791b1e15d7d1cab` | `c3e0a9429228ba5e526295dfff924be952098fb3f24bcbd881de86dcac08cc60` | `89228652a17b999cdefdabc3b85562031f031f32fa271bad4f13c23d1d61f63e` |
| `271` | `36a42f9cbe3513e83597b1b1f22a31153b0ba7473c08c132fb179f07234944c6` | `5b916c348a4fdaa706a1435a03e0542df196ec3417751d95991adde35514bebe` | `010d97499a5de56afc88d8015024ab25c175e4e9d42fc7d15268cd7bd3036987` |
| `272` | `ae428c77e3822a880ed6f4dbd0e39a71f444729be9e63f83f76dbc3345e87cb9` | `e58742facb4918944f7fd8614b73aa54f07f5ed014e28a8cc101bf6ae3a5fe5a` | `a78e178995e3d75d1a7575d0a07af74d8711a1fb8545343294e5781a8f5bcc08` |
| `273` | `8843022be7caabfaff93f68467a0dc8c868ba24e98d45d85e9e72a918a81d747` | `60b29655d4dbc0d584dd90740703ad61a78b90c22f24d0caec8997345af67958` | `baaf44b8d7587a71e26ffd938add732cecdccd94a6740ea958420536c5e607be` |
| `274` | `6cc394c98a300dc8e9023a6c49a9b4663094691d9385fd1ab842b3b0d8ce6f3e` | `62b3307bfc31952cfd09d017774c58c0f0ad3f052d8ebebf20ebe1db28da3f3f` | `eae6659bcbb9ffcfa1d14152b258e154c8bd895d8e87d5efec497ed75517c6ca` |
| `275` | `d8425fb96f9e344f2cde420a756d51f287ca5b9c08d90917b0edd1c394b52413` | `b3c8e4804279288988f47d8fa325ac8206c7402b0824d8a06d96b6813846fb17` | `5a62dfa9bd0020561c5aa58fcb265ef79b4097eeca2a0aae42329c377f109155` |
| `276` | `e2e0be3f8b22bf53b55e025d34019b3b592133bcec83a31ebc6630128a3ec2c0` | `ee4de8c23dc8aa1212014d4c0eea1b86cfb6c222465922afdd6df09aec4635f8` | `39e5cff979cc4630d16dbe54e9296037b09c506ef9ddb3d03983576a67707105` |

The matching pass 06 `.stderr.txt` files are empty with SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Current Limitations

- Current-state LCD endpoints do not expose historical PoC commit data for
  start height `4105361`; they return empty commit arrays or `{}`.
- The archive RPC plus local `inferenced` CLI with `--height 4120751` does
  expose the historical e266 commit store.
- Empty current commit-store responses must not be interpreted as proof that no
  historical commits existed.
- The historical CLI commit output does not include `model_id`; it proves PoC
  commit submission by address/count/root hash, not model-specific submission.
- The e266 delegation pass also stores matching `.stderr.txt` files for the
  `poc_delegation` and params requests; all are empty with SHA-256
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
