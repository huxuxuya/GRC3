# P3-CAND-04 Overlap Matrix

This matrix is compensation hygiene only. It does not change the independent
case-4 total; it marks rows that must not be paid twice if another package
is approved for the same address/epoch.

Rows requiring review: `7`.

| Address | Case4 compensation, GNK | Overlap references | P4 e276 | P3-CAND-06 e276 | Action | Reason |
|---|---:|---|---:|---:|---|---|
| `gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc` | `88.946722163` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `1030.751496775` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1amlmhjym02shahjv8ldmupg4cx0qc66q6f85rj` | `242.705232731` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n` | `11.118340270` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0` | `126.369428439` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1duuaqdx06sx8v2dzggltwwmqyuw8lvjkjq7xll` | `180.062876574` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `0.813537092` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5` | `93.556765689` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | `3953.519092736` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1rcpc45n6zch9qlkn4m3cwngekad89xu8mcr09v` | `3.254148371` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1u4zxypjgcr8khlzefwjr0vwdaj2uzruw2cehj3` | `274.975537419` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `645.406093745` | `` | `0` | `0` | `no_local_overlap_signal` | no same-address overlap found in local normalized references |
| `gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau` | `4038.669308466` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `17896.188970852` | `P3-CAND-06` | `0` | `1` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | `38.236243368` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr` | `3785.930451587` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` | `12.203056394` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv` | `3731.965824421` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | `54.778164259` | `P4-CAND-01` | `1` | `0` | `review_before_payment` | same address appears in another local candidate covering epoch 276 |
