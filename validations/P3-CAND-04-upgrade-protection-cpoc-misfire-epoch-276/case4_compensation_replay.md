# P3-CAND-04 Compensation Replay

This replay starts from archive-chain state only. It does not execute the
`gonkavip/payout276` code.

## Summary

| Metric | Value |
|---|---:|
| Members at h_before | `54` |
| ACTIVE before upgrade | `46` |
| Dropped | `7` |
| Reduced confirmation weight | `12` |
| Affected rows | `19` |
| Total rewarded in epoch | `193,820.331174280 GNK` |
| Total cw before | `845946` |
| Total cw after | `714732` |
| Total full weight after | `798029` |
| Eligible lost cw | `133526` |
| Total compensation | `32,429.966254822 GNK` |

Formula: `lost_cw * total_rewarded_ngonka // total_full_weight_after`.

## Rows

| Address | Before -> After | cw before -> after | lost cw | Dropped | Rewarded, GNK | Compensation, GNK |
|---|---|---:|---:|---:|---:|---:|
| `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `ACTIVE` -> `INACTIVE` | `65994` -> `18447` | `65994` | `1` | `0.000000000` | `16,028.213179615` |
| `gonka10079cnl3nuh2k82mhkm04dj0slhtw9kmjewwau` | `ACTIVE` -> `ACTIVE` | `45840` -> `30947` | `14893` | `0` | `7,564.721688269` | `3,617.119418189` |
| `gonka1mmlyd5xxu5l68yx8wzclrkxkxvm88mhq5tp5s0` | `ACTIVE` -> `INACTIVE` | `14579` -> `0` | `14579` | `1` | `0.000000000` | `3,540.857046786` |
| `gonka1gvrrhjmy4w4mayvs2s5l23edj8ertcmtd2v4zr` | `ACTIVE` -> `ACTIVE` | `61659` -> `47698` | `13961` | `0` | `11,860.324284660` | `3,390.761041922` |
| `gonka1scskt6wpnjnumsah6kjphmdu87vjgvcxmn4rxv` | `ACTIVE` -> `ACTIVE` | `31283` -> `17521` | `13762` | `0` | `4,412.103146383` | `3,342.429156860` |
| `gonka17pw6099q758qwzewtrqmqpf5c2lrhr97fwqexu` | `ACTIVE` -> `INACTIVE` | `3801` -> `0` | `3801` | `1` | `0.000000000` | `923.163292052` |
| `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `ACTIVE` -> `ACTIVE` | `8301` -> `5921` | `2380` | `0` | `1,997.913395460` | `578.039630382` |
| `gonka1u4zxypjgcr8khlzefwjr0vwdaj2uzruw2cehj3` | `ACTIVE` -> `INACTIVE` | `1014` -> `0` | `1014` | `1` | `0.000000000` | `246.274027398` |
| `gonka1amlmhjym02shahjv8ldmupg4cx0qc66q6f85rj` | `ACTIVE` -> `INACTIVE` | `895` -> `0` | `895` | `1` | `0.000000000` | `217.372045879` |
| `gonka1duuaqdx06sx8v2dzggltwwmqyuw8lvjkjq7xll` | `ACTIVE` -> `ACTIVE` | `129237` -> `128573` | `664` | `0` | `43,384.023411292` | `161.268199400` |
| `gonka1d694r00czmq75txghwjcuk07lxvc8d4ekgsha0` | `ACTIVE` -> `INACTIVE` | `466` -> `0` | `466` | `1` | `0.000000000` | `113.179188133` |
| `gonka1gyk0aahvr3qeju4zx0nplfreej6cy4jjk8svc5` | `ACTIVE` -> `INACTIVE` | `345` -> `0` | `345` | `1` | `0.000000000` | `83.791459026` |
| `gonka14ljarev2nlzu4ej50vx7ylj2rvg4n20fnq2ysc` | `ACTIVE` -> `ACTIVE` | `16651` -> `16323` | `328` | `0` | `3,779.519367305` | `79.662604523` |
| `gonka1yal0ysgzc860zt3y8cds8656tnueusgymftvkw` | `ACTIVE` -> `ACTIVE` | `14650` -> `14448` | `202` | `0` | `3,345.483781660` | `49.060506444` |
| `gonka168rtjfkszuhcggg4dfyse4yh7xn9zwfglnkns2` | `ACTIVE` -> `ACTIVE` | `15129` -> `14988` | `141` | `0` | `3,732.634999625` | `34.245204993` |
| `gonka1kx9mca3xm8u8ypzfuhmxey66u0ufxhs7nm6wc5` | `ACTIVE` -> `ACTIVE` | `5315` -> `5270` | `45` | `0` | `1,520.190103568` | `10.929320742` |
| `gonka1ce02jjduga8jvwj8jx39mxn0jr345vgkx7lk2n` | `ACTIVE` -> `ACTIVE` | `7503` -> `7462` | `41` | `0` | `1,727.617912092` | `9.957825565` |
| `gonka1rcpc45n6zch9qlkn4m3cwngekad89xu8mcr09v` | `ACTIVE` -> `ACTIVE` | `4844` -> `4832` | `12` | `0` | `1,458.743167138` | `2.914485531` |
| `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `ACTIVE` -> `ACTIVE` | `168` -> `165` | `3` | `0` | `55.408798167` | `0.728621382` |
