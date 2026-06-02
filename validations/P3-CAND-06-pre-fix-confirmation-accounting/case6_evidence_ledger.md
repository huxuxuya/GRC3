# P3-CAND-06 Evidence Ledger

This ledger is the row-by-row audit surface for P3-CAND-06. It combines
`candidate_rows.csv`, raw cPoC submission/validator evidence, old-formula
replay, bounded v0.2.13-style replay, eligibility status, and overlap
status. It does not approve payouts.

## Summary

| Metric | Value |
|---|---:|
| Candidate rows | `24` |
| Estimated zero-reward loss | `120,822.324371792 GONKA` |
| Old-formula replay matches stored ratio | `22` |
| Bounded v0.2.13-style rows passing alpha | `0` |

## Technical Status

| Status | Rows |
|---|---:|
| `blocked_epoch276_overlap` | `4` |
| `formula_reconciled_policy_required` | `20` |

## Overlap Status

| Status | Rows |
|---|---:|
| `known_p3_cand_04_same_address` | `1` |
| `no_known_overlap_in_local_repo` | `6` |
| `p3_cand_04_epoch_overlap_unresolved` | `3` |
| `p4_cand_01_epoch_range_overlap` | `14` |

## Recommended Action

| Action | Rows |
|---|---:|
| `blocked` | `4` |
| `clear` | `6` |
| `review` | `14` |

## Row Ledger

| Epoch | Participant | Trigger -> Exclusion | Pass model(s) | Qwen evidence | Kimi evidence | Stored ratio | Old replay | New-style pass | Loss, GNK | Decision boundary |
|---:|---|---|---|---|---|---:|---|---|---:|---|
| 263 | `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y` | `4073650` -> `4073931` | Kimi | no_submission; no commit; commits 0; valid 0/696861 (0.0000%); validators 0/0 | pass_weight; commit; commits 2080; valid 798165/696861 (76.3582%); validators 16/16 | 35.0447% | 35.0447%; match `True` | `False` | 1,953.032509538 | `policy: decide whether single-model pass is compensable` |
| 263 | `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2` | `4073650` -> `4073931` | Kimi | no_submission; no commit; commits 0; valid 0/696861 (0.0000%); validators 0/0 | pass_weight; commit; commits 160; valid 798165/696861 (76.3582%); validators 16/16 | 2.7391% | 2.7391%; match `True` | `False` | 1,915.652591432 | `policy: decide whether single-model pass is compensable` |
| 263 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `4073650` -> `4073931` | Qwen | pass_weight; commit; commits 7264; valid 726111/696861 (69.4650%); validators 26/26 | no_submission; no commit; commits 0; valid 0/696861 (0.0000%); validators 0/0 | 14.7717% | 14.7717%; match `True` | `False` | 4,850.385431974 | `policy: decide whether single-model pass is compensable` |
| 264 | `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc` | `4075202` -> `4075483` | Kimi | no_submission; no commit; commits 0; valid 0/673461 (0.0000%); validators 0/0 | pass_weight; commit; commits 352; valid 713388/673461 (70.6191%); validators 15/15 | 6.0014% | 6.0014%; match `True` | `False` | 2,019.930762224 | `policy: decide whether single-model pass is compensable` |
| 264 | `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d` | `4075202` -> `4075483` | Kimi | no_submission; no commit; commits 0; valid 0/673461 (0.0000%); validators 0/0 | pass_weight; commit; commits 2880; valid 713388/673461 (70.6191%); validators 15/15 | 49.2523% | 49.2523%; match `True` | `False` | 2,019.930762224 | `policy: decide whether single-model pass is compensable` |
| 264 | `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds` | `4075202` -> `4075483` | Kimi | no_submission; no commit; commits 0; valid 0/673461 (0.0000%); validators 0/0 | pass_weight; commit; commits 2272; valid 713388/673461 (70.6191%); validators 15/15 | 39.8189% | 39.8189%; match `True` | `False` | 1,970.264959744 | `policy: decide whether single-model pass is compensable` |
| 265 | `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww` | `4102890` -> `4103171` | Qwen | pass_weight; commit; commits 704; valid 629010/602785 (69.5671%); validators 22/22 | no_submission; no commit; commits 0; valid 0/602785 (0.0000%); validators 0/0 | 20.7038% | 20.7038%; match `True` | `False` | 335.927643572 | `review: compare against P4-CAND-01 before payout` |
| 268 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `4144898` -> `4145179` | Kimi | no_submission; no commit; commits 0; valid 0/465760 (0.0000%); validators 0/0 | pass_weight; commit; commits 12480; valid 619380/465760 (88.6552%); validators 16/16 | 17.3837% | 17.3837%; match `True` | `False` | 25,309.087745610 | `review: compare against P4-CAND-01 before payout` |
| 269 | `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w` | `4164861` -> `4165142` | Kimi | no_submission; no commit; commits 0; valid 0/452932 (0.0000%); validators 0/0 | pass_weight; commit; commits 2784; valid 570600/452932 (83.9862%); validators 19/19 | 45.1393% | 45.1393%; match `True` | `False` | 2,228.595538500 | `review: compare against P4-CAND-01 before payout` |
| 269 | `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3` | `4153434` -> `4153715` | Qwen | pass_weight; commit; commits 1728; valid 594093/452932 (87.4442%); validators 23/23 | no_submission; no commit; commits 0; valid 0/452932 (0.0000%); validators 0/0 | 45.8992% | 45.8992%; match `True` | `False` | 535.800580255 | `review: compare against P4-CAND-01 before payout` |
| 271 | `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s` | `4184386` -> `4184667` | Qwen | pass_weight; commit; commits 2125; valid 622966/530687 (78.2591%); validators 20/21 | no_submission; no commit; commits 0; valid 0/530687 (0.0000%); validators 0/0 | 33.0943% | 33.0943%; match `True` | `False` | 139.200061369 | `review: compare against P4-CAND-01 before payout` |
| 272 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4202293` -> `4202574` | Qwen | pass_weight; commit; commits 896; valid 794373/548789 (96.5002%); validators 25/25 | no_submission; no commit; commits 0; valid 0/548789 (0.0000%); validators 0/0 | 28.7372% | 28.7372%; match `True` | `False` | 365.340258948 | `review: compare against P4-CAND-01 before payout` |
| 272 | `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr` | `4202293` -> `4202574` | Qwen | pass_weight; commit; commits 1375; valid 793001/548789 (96.3335%); validators 23/24 | no_submission; no commit; commits 0; valid 0/548789 (0.0000%); validators 0/0 | 19.6229% | 19.6229%; match `True` | `False` | 146.964070171 | `review: compare against P4-CAND-01 before payout` |
| 272 | `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg` | `4209686` -> `4209967` | Kimi | no_submission; no commit; commits 0; valid 0/548789 (0.0000%); validators 0/0 | pass_weight; commit; commits 23872; valid 748261/548789 (90.8985%); validators 20/20 | 40.2573% | 40.2573%; match `True` | `False` | 22,521.036302544 | `review: compare against P4-CAND-01 before payout` |
| 272 | `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p` | `4202293` -> `4202574` | Qwen | pass_weight; commit; commits 13056; valid 792893/548789 (96.3204%); validators 23/23 | no_submission; no commit; commits 0; valid 0/548789 (0.0000%); validators 0/0 | 19.0604% | 19.0604%; match `True` | `False` | 8,037.485696859 | `review: compare against P4-CAND-01 before payout` |
| 273 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4215427` -> `4215708` | Qwen | pass_weight; commit; commits 832; valid 566480/505811 (74.6631%); validators 27/27 | no_submission; no commit; commits 0; valid 0/505811 (0.0000%); validators 0/0 | 49.0130% | 49.0130%; match `True` | `False` | 218.861247867 | `review: compare against P4-CAND-01 before payout` |
| 273 | `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx` | `4215427` -> `4215708` | Qwen | pass_weight; commit; commits 8128; valid 558411/505811 (73.5996%); validators 26/26 | no_submission; no commit; commits 0; valid 0/505811 (0.0000%); validators 0/0 | 31.5761% | 31.5761%; match `True` | `False` | 3,018.788733411 | `review: compare against P4-CAND-01 before payout` |
| 274 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4231815` -> `4232096` | Qwen | pass_weight; commit; commits 320; valid 639375/511203 (83.3818%); validators 26/26 | no_submission; no commit; commits 0; valid 0/511203 (0.0000%); validators 0/0 | 29.0542% | 29.0542%; match `True` | `False` | 137.269776102 | `review: compare against P4-CAND-01 before payout` |
| 274 | `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl` | `4232787` -> `4233068` | Qwen | pass_weight; commit; commits 416; valid 612200/511203 (79.8379%); validators 16/16 | no_submission; no commit; commits 0; valid 0/511203 (0.0000%); validators 0/0 | 30.4095% | 30.4095%; match `True` | `False` | 173.159717563 | `review: compare against P4-CAND-01 before payout` |
| 275 | `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p` | `4258197` -> `4258478` | Qwen | pass_weight; commit; commits 320; valid 666218/491284 (90.4051%); validators 22/22 | no_submission; no commit; commits 0; valid 0/491284 (0.0000%); validators 0/0 | 33.4816% | 33.4816%; match `True` | `False` | 126.220428182 | `review: compare against P4-CAND-01 before payout` |
| 276 | `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09` | `4267778` -> `4268059` | Qwen+Kimi | pass_weight; commit; commits 11552; valid 694173/532020 (86.9859%); validators 22/23 | pass_weight; commit; commits 12160; valid 628214/532020 (78.7207%); validators 15/15 | 35.2638% | 40.0967%; match `False` | `False` | 17,356.095656742 | `blocked: resolve P3-CAND-04 duplicate risk` |
| 276 | `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm` | `4264130` -> `4264411` | Kimi | no_submission; no commit; commits 0; valid 0/532020 (0.0000%); validators 0/0 | pass_weight; commit; commits 14784; valid 687806/532020 (86.1881%); validators 17/17 | 37.1301% | 37.1322%; match `False` | `False` | 11,765.489995489 | `blocked: resolve P3-CAND-04 duplicate risk` |
| 276 | `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e` | `4265965` -> `4266246` | Qwen | pass_weight; commit; commits 4128; valid 613141/532020 (76.8319%); validators 25/25 | no_submission; no commit; commits 0; valid 0/532020 (0.0000%); validators 0/0 | 16.9861% | 16.9861%; match `True` | `False` | 3,557.528990032 | `blocked: resolve P3-CAND-04 duplicate risk` |
| 276 | `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239` | `4264130` -> `4264411` | Kimi | no_submission; no commit; commits 0; valid 0/532020 (0.0000%); validators 0/0 | pass_weight; commit; commits 13920; valid 595705/532020 (74.6470%); validators 16/16 | 36.3655% | 36.3655%; match `True` | `False` | 10,120.274911440 | `blocked: resolve P3-CAND-04 duplicate risk` |

## How To Read This

- `pass_weight` means the model had strict validator weight above
  `TotalNetworkWeight * 2 / 3` for the cPoC stage.
- `old replay match True` means the pre-fix chain accounting formula
  reproduces the stored confirmation ratio for that row.
- `New-style pass False` means the bounded replay using the available
  Qwen/Kimi evidence does not by itself make the row pass alpha.
- `blocked` rows must be resolved against P3-CAND-04 before payout.
- `review` rows need duplicate-payment comparison against P4-CAND-01.
- `policy` rows are technically reproducible, but payout depends on
  whether single-model pass rows are compensable.

Machine-readable versions are in `case6_evidence_ledger.csv` and
`case6_evidence_ledger.json`.
