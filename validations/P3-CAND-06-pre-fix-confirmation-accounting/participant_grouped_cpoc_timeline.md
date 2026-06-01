# P3-CAND-06 Grouped cPoC Timeline

This view groups the candidate timeline by participant, then by epoch, then by cPoC event.
It is meant to show where confirmation weight was still preserved and where it was lost.

Time columns are derived from Tendermint block header time. MSK is UTC+03:00.

Column notes:

- `PoC weight` is the participant root weight at the epoch PoC baseline.
- `CW before -> after` is root confirmation weight before the cPoC effect and at the post-cPoC snapshot.
- For non-failing cPoC rows, the post-cPoC snapshot is the block before the next cPoC trigger.
- For the failing cPoC row, the post-cPoC snapshot is the exclusion block.
- `2/3 min` is computed from the root/network total weight for that epoch, matching the chain validation threshold convention.

## Participants

### `gonka1007py6y2qfn2vaqrthqhtchkwx64hgzc6w544w`

Candidate epochs: `269`. Candidate loss sum: `2228.595538500` GONKA.

#### Epoch `269`

| Metric | Value |
|---|---:|
| PoC start | `4,151,534` / `2026-05-19 17:33:15 MSK` |
| Epoch effective start | `4,151,934` |
| Next epoch PoC start | `4,166,925` |
| Total network weight | `679,397` |
| `>2/3` minimum validating weight | `452,932` |
| Participant PoC weight | `5,324` |
| Exclusion | cPoC `#5` at `4,165,142` / `2026-05-20 13:17:44 MSK` |
| Blocks left to next epoch after loss | `1,783` |
| Candidate loss | `2228.595538500` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,153,434` / `2026-05-19 20:19:10 MSK` | `4,155,549` / `2026-05-19 23:23:22 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `#1` | `4,155,550` / `2026-05-19 23:23:27 MSK` | `4,157,968` / `2026-05-20 02:53:44 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `#2` | `4,157,969` / `2026-05-20 02:53:49 MSK` | `4,162,915` / `2026-05-20 10:03:53 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `#3` | `4,162,916` / `2026-05-20 10:03:55 MSK` | `4,163,711` / `2026-05-20 11:13:07 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `#4` | `4,163,712` / `2026-05-20 11:13:13 MSK` | `4,164,860` / `2026-05-20 12:53:09 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 584,213 (85.9899%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `#5` | `4,164,861` / `2026-05-20 12:53:15 MSK` | `4,165,142` / `2026-05-20 13:17:44 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,784; valid 570,600 (83.9862%) | `7,755` -> `3,182` | `-4,573` | `59.7671%` | LOST |

Loss point: at cPoC `#5` confirmation weight moves from `7,755` to `3,182`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka10mmdjau4dnj8krs7sh7t7635ttnmq9u3vqgz09`

Candidate epochs: `276`. Candidate loss sum: `17356.095656742` GONKA.

#### Epoch `276`

| Metric | Value |
|---|---:|
| PoC start | `4,259,271` / `2026-05-26 05:59:12 MSK` |
| Epoch effective start | `4,259,671` |
| Next epoch PoC start | `4,274,662` |
| Total network weight | `798,029` |
| `>2/3` minimum validating weight | `532,020` |
| Participant PoC weight | `48,865` |
| Exclusion | cPoC `#2` at `4,268,059` / `2026-05-26 18:49:39 MSK` |
| Blocks left to next epoch after loss | `6,603` |
| Candidate loss | `17356.095656742` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,265,964` / `2026-05-26 15:43:16 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 51,904; valid 687,806 (86.1881%) | `67,553` -> `67,553` | `0` | `138.2441%` | kept |
| `#1` | `4,265,965` / `2026-05-26 15:43:21 MSK` | `4,267,777` / `2026-05-26 18:24:58 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 38,048; valid 642,096 (80.4602%) | `67,553` -> `65,994` | `-1,559` | `135.0537%` | kept |
| `#2` | `4,267,778` / `2026-05-26 18:25:04 MSK` | `4,268,059` / `2026-05-26 18:49:39 MSK` | pass_weight; sub 11,552; valid 694,173 (86.9859%) | pass_weight; sub 12,160; valid 628,214 (78.7207%) | `65,994` -> `21,654` | `-44,340` | `44.3139%` | LOST |

Loss point: at cPoC `#2` confirmation weight moves from `65,994` to `21,654`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka14g78ez2zy08k8sssue483zmfpgd4qut8zcwlqc`

Candidate epochs: `264`. Candidate loss sum: `2019.930762224` GONKA.

#### Epoch `264`

| Metric | Value |
|---|---:|
| PoC start | `4,074,579` / `2026-05-15 03:53:30 MSK` |
| Epoch effective start | `4,074,979` |
| Next epoch PoC start | `4,089,970` |
| Total network weight | `1,010,191` |
| `>2/3` minimum validating weight | `673,461` |
| Participant PoC weight | `7,158` |
| Exclusion | cPoC `#0` at `4,075,483` / `2026-05-15 05:11:12 MSK` |
| Blocks left to next epoch after loss | `14,487` |
| Candidate loss | `2019.930762224` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,075,202` / `2026-05-15 04:47:04 MSK` | `4,075,483` / `2026-05-15 05:11:12 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 352; valid 713,388 (70.6191%) | `7,534` -> `411` | `-7,123` | `5.7418%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `7,534` to `411`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka14tqh62mangwzrma2lgg2dm375rcjzn2ydy8ttm`

Candidate epochs: `276`. Candidate loss sum: `11765.489995489` GONKA.

#### Epoch `276`

| Metric | Value |
|---|---:|
| PoC start | `4,259,271` / `2026-05-26 05:59:12 MSK` |
| Epoch effective start | `4,259,671` |
| Next epoch PoC start | `4,274,662` |
| Total network weight | `798,029` |
| `>2/3` minimum validating weight | `532,020` |
| Participant PoC weight | `33,125` |
| Exclusion | cPoC `#0` at `4,264,411` / `2026-05-26 13:28:07 MSK` |
| Blocks left to next epoch after loss | `10,251` |
| Candidate loss | `11765.489995489` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,264,411` / `2026-05-26 13:28:07 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 14,784; valid 687,806 (86.1881%) | `50,810` -> `17,149` | `-33,661` | `51.7706%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `50,810` to `17,149`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka16xa2sdc8qe2289nzr4e6vmdyzlke8g8fn8e75s`

Candidate epochs: `271`. Candidate loss sum: `139.200061369` GONKA.

#### Epoch `271`

| Metric | Value |
|---|---:|
| PoC start | `4,182,316` / `2026-05-21 14:12:07 MSK` |
| Epoch effective start | `4,182,716` |
| Next epoch PoC start | `4,197,707` |
| Total network weight | `796,030` |
| `>2/3` minimum validating weight | `530,687` |
| Participant PoC weight | `390` |
| Exclusion | cPoC `#0` at `4,184,667` / `2026-05-21 17:37:04 MSK` |
| Blocks left to next epoch after loss | `13,040` |
| Candidate loss | `139.200061369` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,184,386` / `2026-05-21 17:12:37 MSK` | `4,184,667` / `2026-05-21 17:37:04 MSK` | pass_weight; sub 2,125; valid 622,966 (78.2591%) | no_submission; sub 0; valid 0 (0.0000%) | `2,297` -> `691` | `-1,606` | `177.1795%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `2,297` to `691`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1830lqug50lse998x2lakk4pj5ypfumz5pasz0y`

Candidate epochs: `263`. Candidate loss sum: `1953.032509538` GONKA.

#### Epoch `263`

| Metric | Value |
|---|---:|
| PoC start | `4,059,188` / `2026-05-14 05:51:04 MSK` |
| Epoch effective start | `4,059,588` |
| Next epoch PoC start | `4,074,579` |
| Total network weight | `1,045,290` |
| `>2/3` minimum validating weight | `696,861` |
| Participant PoC weight | `7,158` |
| Exclusion | cPoC `#0` at `4,073,931` / `2026-05-15 02:58:01 MSK` |
| Blocks left to next epoch after loss | `648` |
| Candidate loss | `1953.032509538` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,073,650` / `2026-05-15 02:33:51 MSK` | `4,073,931` / `2026-05-15 02:58:01 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,080; valid 798,165 (76.3582%) | `7,534` -> `2,400` | `-5,134` | `33.5289%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `7,534` to `2,400`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka18xeqnspxpg2vncufnjne485rkaagwvz7whyn0d`

Candidate epochs: `264`. Candidate loss sum: `2019.930762224` GONKA.

#### Epoch `264`

| Metric | Value |
|---|---:|
| PoC start | `4,074,579` / `2026-05-15 03:53:30 MSK` |
| Epoch effective start | `4,074,979` |
| Next epoch PoC start | `4,089,970` |
| Total network weight | `1,010,191` |
| `>2/3` minimum validating weight | `673,461` |
| Participant PoC weight | `7,158` |
| Exclusion | cPoC `#0` at `4,075,483` / `2026-05-15 05:11:12 MSK` |
| Blocks left to next epoch after loss | `14,487` |
| Candidate loss | `2019.930762224` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,075,202` / `2026-05-15 04:47:04 MSK` | `4,075,483` / `2026-05-15 05:11:12 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,880; valid 713,388 (70.6191%) | `7,534` -> `3,373` | `-4,161` | `47.1221%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `7,534` to `3,373`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka19cjm4c5mt3j3qdr8vhytmm4hef3pnkvkm0x7m2`

Candidate epochs: `263`. Candidate loss sum: `1915.652591432` GONKA.

#### Epoch `263`

| Metric | Value |
|---|---:|
| PoC start | `4,059,188` / `2026-05-14 05:51:04 MSK` |
| Epoch effective start | `4,059,588` |
| Next epoch PoC start | `4,074,579` |
| Total network weight | `1,045,290` |
| `>2/3` minimum validating weight | `696,861` |
| Participant PoC weight | `7,021` |
| Exclusion | cPoC `#0` at `4,073,931` / `2026-05-15 02:58:01 MSK` |
| Blocks left to next epoch after loss | `648` |
| Candidate loss | `1915.652591432` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,073,650` / `2026-05-15 02:33:51 MSK` | `4,073,931` / `2026-05-15 02:58:01 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 160; valid 798,165 (76.3582%) | `7,390` -> `184` | `-7,206` | `2.6207%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `7,390` to `184`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1cuwejs77gectp3n32wg8q27hlsa4m3hqspf4ww`

Candidate epochs: `265`. Candidate loss sum: `335.927643572` GONKA.

#### Epoch `265`

| Metric | Value |
|---|---:|
| PoC start | `4,089,970` / `2026-05-16 01:48:39 MSK` |
| Epoch effective start | `4,090,370` |
| Next epoch PoC start | `4,105,361` |
| Total network weight | `904,177` |
| `>2/3` minimum validating weight | `602,785` |
| Participant PoC weight | `1,066` |
| Exclusion | cPoC `#2` at `4,103,171` / `2026-05-16 20:29:07 MSK` |
| Blocks left to next epoch after loss | `2,190` |
| Candidate loss | `335.927643572` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,095,682` / `2026-05-16 09:55:01 MSK` | `4,098,878` / `2026-05-16 14:25:55 MSK` | pass_weight; sub 4,960; valid 639,915 (70.7732%) | no_submission; sub 0; valid 0 (0.0000%) | `1,254` -> `1,254` | `0` | `117.6360%` | kept |
| `#1` | `4,098,879` / `2026-05-16 14:26:01 MSK` | `4,102,889` / `2026-05-16 20:05:14 MSK` | pass_weight; sub 5,696; valid 669,448 (74.0395%) | no_submission; sub 0; valid 0 (0.0000%) | `1,254` -> `1,254` | `0` | `117.6360%` | kept |
| `#2` | `4,102,890` / `2026-05-16 20:05:17 MSK` | `4,103,171` / `2026-05-16 20:29:07 MSK` | pass_weight; sub 704; valid 629,010 (69.5671%) | no_submission; sub 0; valid 0 (0.0000%) | `1,254` -> `236` | `-1,018` | `22.1388%` | LOST |

Loss point: at cPoC `#2` confirmation weight moves from `1,254` to `236`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1f0u3y2wneer8zhz3ypw4x54h38cpa0qsy8ts3e`

Candidate epochs: `276`. Candidate loss sum: `3557.528990032` GONKA.

#### Epoch `276`

| Metric | Value |
|---|---:|
| PoC start | `4,259,271` / `2026-05-26 05:59:12 MSK` |
| Epoch effective start | `4,259,671` |
| Next epoch PoC start | `4,274,662` |
| Total network weight | `798,029` |
| `>2/3` minimum validating weight | `532,020` |
| Participant PoC weight | `10,016` |
| Exclusion | cPoC `#1` at `4,266,246` / `2026-05-26 16:07:52 MSK` |
| Blocks left to next epoch after loss | `8,416` |
| Candidate loss | `3557.528990032` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,265,964` / `2026-05-26 15:43:16 MSK` | pass_weight; sub 4,224; valid 614,628 (77.0183%) | no_submission; sub 0; valid 0 (0.0000%) | `8,698` -> `8,698` | `0` | `86.8411%` | kept |
| `#1` | `4,265,965` / `2026-05-26 15:43:21 MSK` | `4,266,246` / `2026-05-26 16:07:52 MSK` | pass_weight; sub 4,128; valid 613,141 (76.8319%) | no_submission; sub 0; valid 0 (0.0000%) | `8,698` -> `1,343` | `-7,355` | `13.4085%` | LOST |

Loss point: at cPoC `#1` confirmation weight moves from `8,698` to `1,343`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1fvly5jrewyjmjfgwah3khy9rttq4cqajcesv9p`

Candidate epochs: `272, 273, 274, 275`. Candidate loss sum: `847.691711099` GONKA.

#### Epoch `272`

| Metric | Value |
|---|---:|
| PoC start | `4,197,707` / `2026-05-22 12:32:39 MSK` |
| Epoch effective start | `4,198,107` |
| Next epoch PoC start | `4,213,098` |
| Total network weight | `823,183` |
| `>2/3` minimum validating weight | `548,789` |
| Participant PoC weight | `1,059` |
| Exclusion | cPoC `#0` at `4,202,574` / `2026-05-22 19:37:00 MSK` |
| Blocks left to next epoch after loss | `10,524` |
| Candidate loss | `365.340258948` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,574` / `2026-05-22 19:37:00 MSK` | pass_weight; sub 896; valid 794,373 (96.5002%) | no_submission; sub 0; valid 0 (0.0000%) | `1,114` -> `291` | `-823` | `27.4788%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `1,114` to `291`; this is the row where the participant becomes a candidate for lost reward accounting.

#### Epoch `273`

| Metric | Value |
|---|---:|
| PoC start | `4,213,098` / `2026-05-23 10:53:51 MSK` |
| Epoch effective start | `4,213,498` |
| Next epoch PoC start | `4,228,489` |
| Total network weight | `758,715` |
| `>2/3` minimum validating weight | `505,811` |
| Participant PoC weight | `585` |
| Exclusion | cPoC `#0` at `4,215,708` / `2026-05-23 14:41:29 MSK` |
| Blocks left to next epoch after loss | `12,781` |
| Candidate loss | `218.861247867` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,215,427` / `2026-05-23 14:16:57 MSK` | `4,215,708` / `2026-05-23 14:41:29 MSK` | pass_weight; sub 832; valid 566,480 (74.6631%) | no_submission; sub 0; valid 0 (0.0000%) | `615` -> `274` | `-341` | `46.8376%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `615` to `274`; this is the row where the participant becomes a candidate for lost reward accounting.

#### Epoch `274`

| Metric | Value |
|---|---:|
| PoC start | `4,228,489` / `2026-05-24 09:11:40 MSK` |
| Epoch effective start | `4,228,889` |
| Next epoch PoC start | `4,243,880` |
| Total network weight | `766,804` |
| `>2/3` minimum validating weight | `511,203` |
| Participant PoC weight | `371` |
| Exclusion | cPoC `#1` at `4,232,096` / `2026-05-24 14:27:23 MSK` |
| Blocks left to next epoch after loss | `11,784` |
| Candidate loss | `137.269776102` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,229,666` / `2026-05-24 10:54:36 MSK` | `4,231,814` / `2026-05-24 14:02:37 MSK` | pass_weight; sub 960; valid 528,504 (68.9230%) | no_submission; sub 0; valid 0 (0.0000%) | `390` -> `312` | `-78` | `84.0970%` | kept |
| `#1` | `4,231,815` / `2026-05-24 14:02:43 MSK` | `4,232,096` / `2026-05-24 14:27:23 MSK` | pass_weight; sub 320; valid 639,375 (83.3818%) | no_submission; sub 0; valid 0 (0.0000%) | `312` -> `103` | `-209` | `27.7628%` | LOST |

Loss point: at cPoC `#1` confirmation weight moves from `312` to `103`; this is the row where the participant becomes a candidate for lost reward accounting.

#### Epoch `275`

| Metric | Value |
|---|---:|
| PoC start | `4,243,880` / `2026-05-25 07:31:28 MSK` |
| Epoch effective start | `4,244,280` |
| Next epoch PoC start | `4,259,271` |
| Total network weight | `736,925` |
| `>2/3` minimum validating weight | `491,284` |
| Participant PoC weight | `328` |
| Exclusion | cPoC `#2` at `4,258,478` / `2026-05-26 04:49:49 MSK` |
| Blocks left to next epoch after loss | `793` |
| Candidate loss | `126.220428182` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,248,892` / `2026-05-25 14:50:15 MSK` | `4,249,773` / `2026-05-25 16:07:25 MSK` | pass_weight; sub 896; valid 663,716 (90.0656%) | no_submission; sub 0; valid 0 (0.0000%) | `345` -> `289` | `-56` | `88.1098%` | kept |
| `#1` | `4,249,774` / `2026-05-25 16:07:31 MSK` | `4,258,196` / `2026-05-26 04:25:02 MSK` | pass_weight; sub 960; valid 548,096 (74.3761%) | no_submission; sub 0; valid 0 (0.0000%) | `289` -> `289` | `0` | `88.1098%` | kept |
| `#2` | `4,258,197` / `2026-05-26 04:25:08 MSK` | `4,258,478` / `2026-05-26 04:49:49 MSK` | pass_weight; sub 320; valid 666,218 (90.4051%) | no_submission; sub 0; valid 0 (0.0000%) | `289` -> `105` | `-184` | `32.0122%` | LOST |

Loss point: at cPoC `#2` confirmation weight moves from `289` to `105`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1naxyjmun6kl23htjdujwd6c5z5avgwapsrmfk3`

Candidate epochs: `269`. Candidate loss sum: `535.800580255` GONKA.

#### Epoch `269`

| Metric | Value |
|---|---:|
| PoC start | `4,151,534` / `2026-05-19 17:33:15 MSK` |
| Epoch effective start | `4,151,934` |
| Next epoch PoC start | `4,166,925` |
| Total network weight | `679,397` |
| `>2/3` minimum validating weight | `452,932` |
| Participant PoC weight | `1,280` |
| Exclusion | cPoC `#0` at `4,153,715` / `2026-05-19 20:43:43 MSK` |
| Blocks left to next epoch after loss | `13,210` |
| Candidate loss | `535.800580255` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,153,434` / `2026-05-19 20:19:10 MSK` | `4,153,715` / `2026-05-19 20:43:43 MSK` | pass_weight; sub 1,728; valid 594,093 (87.4442%) | no_submission; sub 0; valid 0 (0.0000%) | `1,347` -> `562` | `-785` | `43.9062%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `1,347` to `562`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1nku7u6d5mz80h35ty8ydeh0k5xydesvt9w0vjr`

Candidate epochs: `272`. Candidate loss sum: `146.964070171` GONKA.

#### Epoch `272`

| Metric | Value |
|---|---:|
| PoC start | `4,197,707` / `2026-05-22 12:32:39 MSK` |
| Epoch effective start | `4,198,107` |
| Next epoch PoC start | `4,213,098` |
| Total network weight | `823,183` |
| `>2/3` minimum validating weight | `548,789` |
| Participant PoC weight | `426` |
| Exclusion | cPoC `#0` at `4,202,574` / `2026-05-22 19:37:00 MSK` |
| Blocks left to next epoch after loss | `10,524` |
| Candidate loss | `146.964070171` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,574` / `2026-05-22 19:37:00 MSK` | pass_weight; sub 1,375; valid 793,001 (96.3335%) | no_submission; sub 0; valid 0 (0.0000%) | `2,506` -> `447` | `-2,059` | `104.9296%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `2,506` to `447`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1q5xt54wncgzk7dxv9x64uln68455g83wu9tugg`

Candidate epochs: `268, 272`. Candidate loss sum: `47830.124048154` GONKA.

#### Epoch `268`

| Metric | Value |
|---|---:|
| PoC start | `4,136,143` / `2026-05-18 19:14:41 MSK` |
| Epoch effective start | `4,136,543` |
| Next epoch PoC start | `4,151,534` |
| Total network weight | `698,639` |
| `>2/3` minimum validating weight | `465,760` |
| Participant PoC weight | `62,145` |
| Exclusion | cPoC `#3` at `4,145,179` / `2026-05-19 08:20:52 MSK` |
| Blocks left to next epoch after loss | `6,355` |
| Candidate loss | `25309.087745610` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,136,924` / `2026-05-18 20:22:09 MSK` | `4,139,231` / `2026-05-18 23:42:55 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 77,984; valid 575,036 (82.3080%) | `91,616` -> `90,027` | `-1,589` | `144.8660%` | kept |
| `#1` | `4,139,232` / `2026-05-18 23:43:01 MSK` | `4,141,308` / `2026-05-19 02:43:44 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 77,504; valid 579,803 (82.9904%) | `90,027` -> `89,471` | `-556` | `143.9714%` | kept |
| `#2` | `4,141,309` / `2026-05-19 02:43:50 MSK` | `4,144,897` / `2026-05-19 07:56:14 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 77,120; valid 588,609 (84.2508%) | `89,471` -> `89,030` | `-441` | `143.2617%` | kept |
| `#3` | `4,144,898` / `2026-05-19 07:56:20 MSK` | `4,145,179` / `2026-05-19 08:20:52 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 12,480; valid 619,380 (88.6552%) | `89,030` -> `14,477` | `-74,553` | `23.2955%` | LOST |

Loss point: at cPoC `#3` confirmation weight moves from `89,030` to `14,477`; this is the row where the participant becomes a candidate for lost reward accounting.

#### Epoch `272`

| Metric | Value |
|---|---:|
| PoC start | `4,197,707` / `2026-05-22 12:32:39 MSK` |
| Epoch effective start | `4,198,107` |
| Next epoch PoC start | `4,213,098` |
| Total network weight | `823,183` |
| `>2/3` minimum validating weight | `548,789` |
| Participant PoC weight | `65,281` |
| Exclusion | cPoC `#3` at `4,209,967` / `2026-05-23 06:21:32 MSK` |
| Blocks left to next epoch after loss | `3,131` |
| Candidate loss | `22521.036302544` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,714` / `2026-05-22 19:49:14 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 38,944; valid 715,470 (86.9151%) | `74,947` -> `44,527` | `-30,420` | `68.2082%` | kept |
| `#1` | `4,202,715` / `2026-05-22 19:49:20 MSK` | `4,208,127` / `2026-05-23 03:41:03 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 25,792; valid 757,571 (92.0295%) | `44,527` -> `44,339` | `-188` | `67.9202%` | kept |
| `#2` | `4,208,128` / `2026-05-23 03:41:08 MSK` | `4,209,685` / `2026-05-23 05:56:56 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 38,368; valid 745,006 (90.5031%) | `44,339` -> `44,078` | `-261` | `67.5204%` | kept |
| `#3` | `4,209,686` / `2026-05-23 05:57:01 MSK` | `4,209,967` / `2026-05-23 06:21:32 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 23,872; valid 748,261 (90.8985%) | `44,078` -> `27,426` | `-16,652` | `42.0122%` | LOST |

Loss point: at cPoC `#3` confirmation weight moves from `44,078` to `27,426`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1qwfrtz9c7kcrfkrrlne2pkcye74mj6ce33xdkl`

Candidate epochs: `274`. Candidate loss sum: `173.159717563` GONKA.

#### Epoch `274`

| Metric | Value |
|---|---:|
| PoC start | `4,228,489` / `2026-05-24 09:11:40 MSK` |
| Epoch effective start | `4,228,889` |
| Next epoch PoC start | `4,243,880` |
| Total network weight | `766,804` |
| `>2/3` minimum validating weight | `511,203` |
| Participant PoC weight | `468` |
| Exclusion | cPoC `#2` at `4,233,068` / `2026-05-24 15:52:09 MSK` |
| Blocks left to next epoch after loss | `10,812` |
| Candidate loss | `173.159717563` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,229,666` / `2026-05-24 10:54:36 MSK` | `4,231,814` / `2026-05-24 14:02:37 MSK` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `492` -> `492` | `0` | `105.1282%` | kept |
| `#1` | `4,231,815` / `2026-05-24 14:02:43 MSK` | `4,232,786` / `2026-05-24 15:27:32 MSK` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `492` -> `492` | `0` | `105.1282%` | kept |
| `#2` | `4,232,787` / `2026-05-24 15:27:37 MSK` | `4,233,068` / `2026-05-24 15:52:09 MSK` | pass_weight; sub 416; valid 612,200 (79.8379%) | no_submission; sub 0; valid 0 (0.0000%) | `492` -> `136` | `-356` | `29.0598%` | LOST |

Loss point: at cPoC `#2` confirmation weight moves from `492` to `136`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1ujnc662v6g69jm6fgxnr79a2m7ehzeut059239`

Candidate epochs: `263, 276`. Candidate loss sum: `14970.660343414` GONKA.

#### Epoch `263`

| Metric | Value |
|---|---:|
| PoC start | `4,059,188` / `2026-05-14 05:51:04 MSK` |
| Epoch effective start | `4,059,588` |
| Next epoch PoC start | `4,074,579` |
| Total network weight | `1,045,290` |
| `>2/3` minimum validating weight | `696,861` |
| Participant PoC weight | `17,777` |
| Exclusion | cPoC `#0` at `4,073,931` / `2026-05-15 02:58:01 MSK` |
| Blocks left to next epoch after loss | `648` |
| Candidate loss | `4850.385431974` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,073,650` / `2026-05-15 02:33:51 MSK` | `4,073,931` / `2026-05-15 02:58:01 MSK` | pass_weight; sub 7,264; valid 726,111 (69.4650%) | no_submission; sub 0; valid 0 (0.0000%) | `17,777` -> `2,387` | `-15,390` | `13.4275%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `17,777` to `2,387`; this is the row where the participant becomes a candidate for lost reward accounting.

#### Epoch `276`

| Metric | Value |
|---|---:|
| PoC start | `4,259,271` / `2026-05-26 05:59:12 MSK` |
| Epoch effective start | `4,259,671` |
| Next epoch PoC start | `4,274,662` |
| Total network weight | `798,029` |
| `>2/3` minimum validating weight | `532,020` |
| Participant PoC weight | `28,493` |
| Exclusion | cPoC `#0` at `4,264,411` / `2026-05-26 13:28:07 MSK` |
| Blocks left to next epoch after loss | `10,251` |
| Candidate loss | `10120.274911440` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,264,411` / `2026-05-26 13:28:07 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 13,920; valid 595,705 (74.6470%) | `48,847` -> `16,147` | `-32,700` | `56.6701%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `48,847` to `16,147`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1xwkesaxvdadh9wt9yyladu0r260s7whklcktds`

Candidate epochs: `264`. Candidate loss sum: `1970.264959744` GONKA.

#### Epoch `264`

| Metric | Value |
|---|---:|
| PoC start | `4,074,579` / `2026-05-15 03:53:30 MSK` |
| Epoch effective start | `4,074,979` |
| Next epoch PoC start | `4,089,970` |
| Total network weight | `1,010,191` |
| `>2/3` minimum validating weight | `673,461` |
| Participant PoC weight | `6,982` |
| Exclusion | cPoC `#0` at `4,075,483` / `2026-05-15 05:11:12 MSK` |
| Blocks left to next epoch after loss | `14,487` |
| Candidate loss | `1970.264959744` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,075,202` / `2026-05-15 04:47:04 MSK` | `4,075,483` / `2026-05-15 05:11:12 MSK` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,272; valid 713,388 (70.6191%) | `7,349` -> `2,660` | `-4,689` | `38.0980%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `7,349` to `2,660`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1ym3np7guxart483yfdxnlztuazx22cjt0e4a2p`

Candidate epochs: `272`. Candidate loss sum: `8037.485696859` GONKA.

#### Epoch `272`

| Metric | Value |
|---|---:|
| PoC start | `4,197,707` / `2026-05-22 12:32:39 MSK` |
| Epoch effective start | `4,198,107` |
| Next epoch PoC start | `4,213,098` |
| Total network weight | `823,183` |
| `>2/3` minimum validating weight | `548,789` |
| Participant PoC weight | `23,298` |
| Exclusion | cPoC `#0` at `4,202,574` / `2026-05-22 19:37:00 MSK` |
| Blocks left to next epoch after loss | `10,524` |
| Candidate loss | `8037.485696859` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,574` / `2026-05-22 19:37:00 MSK` | pass_weight; sub 13,056; valid 792,893 (96.3204%) | no_submission; sub 0; valid 0 (0.0000%) | `24,524` -> `4,249` | `-20,275` | `18.2376%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `24,524` to `4,249`; this is the row where the participant becomes a candidate for lost reward accounting.

### `gonka1zktn8j65wlys8a8e38hqhf4y3x6m4x04zskkrx`

Candidate epochs: `273`. Candidate loss sum: `3018.788733411` GONKA.

#### Epoch `273`

| Metric | Value |
|---|---:|
| PoC start | `4,213,098` / `2026-05-23 10:53:51 MSK` |
| Epoch effective start | `4,213,498` |
| Next epoch PoC start | `4,228,489` |
| Total network weight | `758,715` |
| `>2/3` minimum validating weight | `505,811` |
| Participant PoC weight | `8,069` |
| Exclusion | cPoC `#0` at `4,215,708` / `2026-05-23 14:41:29 MSK` |
| Blocks left to next epoch after loss | `12,781` |
| Candidate loss | `3018.788733411` GONKA |

| cPoC | Trigger / MSK | Snapshot / MSK | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---|---|---:|---:|---:|---|
| `#0` | `4,215,427` / `2026-05-23 14:16:57 MSK` | `4,215,708` / `2026-05-23 14:41:29 MSK` | pass_weight; sub 8,128; valid 558,411 (73.5996%) | no_submission; sub 0; valid 0 (0.0000%) | `10,669` -> `3,062` | `-7,607` | `37.9477%` | LOST |

Loss point: at cPoC `#0` confirmation weight moves from `10,669` to `3,062`; this is the row where the participant becomes a candidate for lost reward accounting.
