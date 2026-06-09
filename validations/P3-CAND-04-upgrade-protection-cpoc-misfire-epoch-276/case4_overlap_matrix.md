# P3-CAND-04 Overlap Matrix

This matrix is compensation hygiene only. It does not change the independent
case-4 total; it marks rows that must not be paid twice if another package
is approved for the same address/epoch.

Rows requiring review: `7`.

| Address | Case4 compensation, GNK | Overlap references | P4 e276 | P3-CAND-06 e276 | Action | Reason |
|---|---:|---|---:|---:|---|---|
| `gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc` | `79.662604523` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `923.163292052` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1amlmhjym02shahjv8ldmupg4cx0qc66q6f85rj` | `217.372045879` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n` | `9.957825565` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0` | `113.179188133` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1duuaqdx06sx8v2dzggltwwmqyuw8lvjkjq7xll` | `161.268199400` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `0.728621382` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5` | `83.791459026` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | `3540.857046786` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1rcpc45n6zch9qlkn4m3cwngekad89xu8mcr09v` | `2.914485531` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1u4zxypjgcr8khlzefwjr0vwdaj2uzruw2cehj3` | `246.274027398` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `578.039630382` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau` | `3617.119418189` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `16028.213179615` | `P3-CAND-06` | `0` | `1` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | `34.245204993` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr` | `3390.761041922` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` | `10.929320742` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv` | `3342.429156860` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | `49.060506444` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
