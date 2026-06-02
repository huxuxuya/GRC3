# P3-CAND-05 Timeline

Participant: `gonka15munkmx6x7k6rqqeexjet4556p7at39ks9qgr5`.

Node notation is `node_id:poc_weight:throughput:timeslot_bits`, where `1` in `timeslot_bits` means that the node was allocated for that slot in the epoch group row exposed by the chain. Slot index `0` is `PRE_POC_SLOT`; slot index `1` is `POC_SLOT`. Only `POC_SLOT=true` is treated by the pre-fix chain code as preserved for PoC/inference service.

| Epoch | Nodes | ml3 present | ml3 PRE_POC_SLOT | ml3 POC_SLOT | Kimi weight | Kimi voting power | Qwen weight | Reward, GONKA | Excluded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 266 | ml3;ml8 | True | True | False | 26304 | 31538 |  | 26799.023361427 | False |
| 267 | ml3;ml5;ml8 | True | True | False | 27400 | 9647 |  | 2829.715828861 | False |
| 268 | ml3;ml5;ml8 | True | True | False | 27639 | 22500 |  | 5757.415294226 | False |
| 269 | ml3;ml5 | True | True | False | 17885 | 15496 |  | 6276.820078853 | False |
| 270 | ml1;ml5 | False | False | False | 23670 | 19891 |  | 7880.707923174 | False |
| 271 | ml1;ml5 | False | False | False | 23867 | 24532 |  | 4081.774107222 | False |
| 272 | ml1 | False | False | False | 11175 | 11782 |  | 0.000000000 | False |
| 273 | ml1 | False | False | False | 11175 | 8777 |  | 0.000000000 | False |
| 280 | mlnode-100;mlnode-200 | False | False | False | 6197 | 8390 | 2545 | 3937.861717621 | False |
| 283 | mlnode-100;mlnode-103;mlnode-104 | False | False | False | 6723 | 10216 | 5586 |  | False |

## Model Rows

| Epoch | Model | Weight | Voting power | Confirmation | Nodes |
| --- | --- | --- | --- | --- | --- |
| 263 | Qwen | 16235 | 36087 | 36087 | ml3:16235:0:10 |
| 264 | Qwen | 16235 | 36531 | 36531 | ml3:16235:0:10 |
| 265 | Qwen | 16235 | 33800 | 33800 | ml3:16235:0:10 |
| 266 | Kimi | 26304 | 31538 | 33197 | ml3:16235:0:10;ml8:10069:0:10 |
| 267 | Kimi | 27400 | 9647 | 34581 | ml3:5219:0:10;ml5:12112:0:10;ml8:10069:0:10 |
| 268 | Kimi | 27639 | 22500 | 34882 | ml3:5219:0:10;ml5:12351:0:10;ml8:10069:0:10 |
| 269 | Kimi | 17885 | 15496 | 22572 | ml3:5219:0:10;ml5:12666:0:10 |
| 270 | Kimi | 23670 | 19891 | 29873 | ml1:11175:0:10;ml5:12495:0:10 |
| 271 | Kimi | 23867 | 24532 | 30122 | ml1:11175:0:10;ml5:12692:0:10 |
| 272 | Kimi | 11175 | 11782 | 14103 | ml1:11175:0:10 |
| 273 | Kimi | 11175 | 8777 | 14103 | ml1:11175:0:10 |
