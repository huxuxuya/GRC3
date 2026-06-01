# P3-CAND-06 Grouped cPoC Timeline

This view groups the candidate timeline by participant, then by epoch, then by cPoC event.
It is meant to show where confirmation weight was still preserved and where it was lost.

Time columns are derived from Tendermint block header time. MSK is UTC+03:00.

Column notes:

- Each participant/epoch section starts with the epoch PoC baseline and ends with the next epoch PoC baseline.
- `PoC weight` is the participant root weight for that row's event epoch.
- `CW before -> after` is root confirmation weight before the cPoC effect and at the post-cPoC snapshot.
- `CW before -> after` is intentionally blank for PoC baseline rows; those rows show root/PoC weight only.
- For non-failing cPoC rows, the post-cPoC snapshot is the block before the next cPoC trigger.
- For the failing cPoC row, the post-cPoC snapshot is the exclusion block.
- For cPoC rows after `LOST`, the post-cPoC snapshot continues to the next cPoC or the next epoch PoC.
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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,151,534` / `2026-05-19 17:33:15 MSK` | `5,324` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,153,434` / `2026-05-19 20:19:10 MSK` | `4,155,549` / `2026-05-19 23:23:22 MSK` | `5,324` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `cPoC #1` | `4,155,550` / `2026-05-19 23:23:27 MSK` | `4,157,968` / `2026-05-20 02:53:44 MSK` | `5,324` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `cPoC #2` | `4,157,969` / `2026-05-20 02:53:49 MSK` | `4,162,915` / `2026-05-20 10:03:53 MSK` | `5,324` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `cPoC #3` | `4,162,916` / `2026-05-20 10:03:55 MSK` | `4,163,711` / `2026-05-20 11:13:07 MSK` | `5,324` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 589,387 (86.7515%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `cPoC #4` | `4,163,712` / `2026-05-20 11:13:13 MSK` | `4,164,860` / `2026-05-20 12:53:09 MSK` | `5,324` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 7,232; valid 584,213 (85.9899%) | `7,755` -> `7,755` | `0` | `145.6612%` | kept |
| `cPoC #5` | `4,164,861` / `2026-05-20 12:53:15 MSK` | `4,165,142` / `2026-05-20 13:17:44 MSK` | `5,324` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,784; valid 570,600 (83.9862%) | `7,755` -> `3,182` | `-4,573` | `59.7671%` | LOST |
| `PoC epoch 270` |  | `4,166,925` / `2026-05-20 15:52:11 MSK` | `0` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,259,271` / `2026-05-26 05:59:12 MSK` | `48,865` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,265,964` / `2026-05-26 15:43:16 MSK` | `48,865` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 51,904; valid 687,806 (86.1881%) | `67,553` -> `67,553` | `0` | `138.2441%` | kept |
| `cPoC #1` | `4,265,965` / `2026-05-26 15:43:21 MSK` | `4,267,777` / `2026-05-26 18:24:58 MSK` | `48,865` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 38,048; valid 642,096 (80.4602%) | `67,553` -> `65,994` | `-1,559` | `135.0537%` | reduced |
| `cPoC #2` | `4,267,778` / `2026-05-26 18:25:04 MSK` | `4,268,059` / `2026-05-26 18:49:39 MSK` | `48,865` | pass_weight; sub 11,552; valid 694,173 (86.9859%) | pass_weight; sub 12,160; valid 628,214 (78.7207%) | `65,994` -> `21,654` | `-44,340` | `44.3139%` | LOST |
| `cPoC #3` | `4,270,605` / `2026-05-26 22:36:05 MSK` | `4,274,661` / `2026-05-27 04:36:32 MSK` | `48,865` | pass_weight; sub 12,096; valid 703,765 (88.1879%) | pass_weight; sub 12,768; valid 629,637 (78.8990%) | `21,654` -> `18,447` | `-3,207` | `37.7509%` | after loss |
| `PoC epoch 277` |  | `4,274,662` / `2026-05-27 04:36:37 MSK` | `12,961` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,074,579` / `2026-05-15 03:53:30 MSK` | `7,158` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,075,202` / `2026-05-15 04:47:04 MSK` | `4,075,483` / `2026-05-15 05:11:12 MSK` | `7,158` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 352; valid 713,388 (70.6191%) | `7,534` -> `411` | `-7,123` | `5.7418%` | LOST |
| `cPoC #1` | `4,075,770` / `2026-05-15 05:35:44 MSK` | `4,089,969` / `2026-05-16 01:48:37 MSK` | `7,158` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,272; valid 724,283 (71.6976%) | `411` -> `411` | `0` | `5.7418%` | after loss |
| `PoC epoch 265` |  | `4,089,970` / `2026-05-16 01:48:39 MSK` | `0` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,259,271` / `2026-05-26 05:59:12 MSK` | `33,125` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,264,411` / `2026-05-26 13:28:07 MSK` | `33,125` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 14,784; valid 687,806 (86.1881%) | `50,810` -> `17,149` | `-33,661` | `51.7706%` | LOST |
| `cPoC #1` | `4,265,965` / `2026-05-26 15:43:21 MSK` | `4,267,777` / `2026-05-26 18:24:58 MSK` | `33,125` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `17,149` -> `0` | `-17,149` | `0.0000%` | after loss |
| `cPoC #2` | `4,267,778` / `2026-05-26 18:25:04 MSK` | `4,270,604` / `2026-05-26 22:36:00 MSK` | `33,125` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #3` | `4,270,605` / `2026-05-26 22:36:05 MSK` | `4,274,661` / `2026-05-27 04:36:32 MSK` | `33,125` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 277` |  | `4,274,662` / `2026-05-27 04:36:37 MSK` | `4,448` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,182,316` / `2026-05-21 14:12:07 MSK` | `390` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,184,386` / `2026-05-21 17:12:37 MSK` | `4,184,667` / `2026-05-21 17:37:04 MSK` | `390` | pass_weight; sub 2,125; valid 622,966 (78.2591%) | no_submission; sub 0; valid 0 (0.0000%) | `2,297` -> `691` | `-1,606` | `177.1795%` | LOST |
| `cPoC #1` | `4,185,816` / `2026-05-21 19:17:22 MSK` | `4,186,812` / `2026-05-21 20:44:20 MSK` | `390` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `691` -> `0` | `-691` | `0.0000%` | after loss |
| `cPoC #2` | `4,186,813` / `2026-05-21 20:44:25 MSK` | `4,190,337` / `2026-05-22 01:51:35 MSK` | `390` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #3` | `4,190,338` / `2026-05-22 01:51:40 MSK` | `4,191,445` / `2026-05-22 03:28:02 MSK` | `390` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #4` | `4,191,446` / `2026-05-22 03:28:08 MSK` | `4,193,852` / `2026-05-22 06:57:35 MSK` | `390` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #5` | `4,193,853` / `2026-05-22 06:57:40 MSK` | `4,194,322` / `2026-05-22 07:38:32 MSK` | `390` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #6` | `4,194,323` / `2026-05-22 07:38:37 MSK` | `4,197,706` / `2026-05-22 12:32:37 MSK` | `390` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 272` |  | `4,197,707` / `2026-05-22 12:32:39 MSK` | `397` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,059,188` / `2026-05-14 05:51:04 MSK` | `7,158` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,073,650` / `2026-05-15 02:33:51 MSK` | `4,073,931` / `2026-05-15 02:58:01 MSK` | `7,158` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,080; valid 798,165 (76.3582%) | `7,534` -> `2,400` | `-5,134` | `33.5289%` | LOST |
| `PoC epoch 264` |  | `4,074,579` / `2026-05-15 03:53:30 MSK` | `6,404` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,074,579` / `2026-05-15 03:53:30 MSK` | `7,158` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,075,202` / `2026-05-15 04:47:04 MSK` | `4,075,483` / `2026-05-15 05:11:12 MSK` | `7,158` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,880; valid 713,388 (70.6191%) | `7,534` -> `3,373` | `-4,161` | `47.1221%` | LOST |
| `cPoC #1` | `4,075,770` / `2026-05-15 05:35:44 MSK` | `4,089,969` / `2026-05-16 01:48:37 MSK` | `7,158` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `3,373` -> `3,373` | `0` | `47.1221%` | after loss |
| `PoC epoch 265` |  | `4,089,970` / `2026-05-16 01:48:39 MSK` | `14,284` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,059,188` / `2026-05-14 05:51:04 MSK` | `7,021` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,073,650` / `2026-05-15 02:33:51 MSK` | `4,073,931` / `2026-05-15 02:58:01 MSK` | `7,021` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 160; valid 798,165 (76.3582%) | `7,390` -> `184` | `-7,206` | `2.6207%` | LOST |
| `PoC epoch 264` |  | `4,074,579` / `2026-05-15 03:53:30 MSK` | `6,282` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,089,970` / `2026-05-16 01:48:39 MSK` | `1,066` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,095,682` / `2026-05-16 09:55:01 MSK` | `4,098,878` / `2026-05-16 14:25:55 MSK` | `1,066` | pass_weight; sub 4,960; valid 639,915 (70.7732%) | no_submission; sub 0; valid 0 (0.0000%) | `1,254` -> `1,254` | `0` | `117.6360%` | kept |
| `cPoC #1` | `4,098,879` / `2026-05-16 14:26:01 MSK` | `4,102,889` / `2026-05-16 20:05:14 MSK` | `1,066` | pass_weight; sub 5,696; valid 669,448 (74.0395%) | no_submission; sub 0; valid 0 (0.0000%) | `1,254` -> `1,254` | `0` | `117.6360%` | kept |
| `cPoC #2` | `4,102,890` / `2026-05-16 20:05:17 MSK` | `4,103,171` / `2026-05-16 20:29:07 MSK` | `1,066` | pass_weight; sub 704; valid 629,010 (69.5671%) | no_submission; sub 0; valid 0 (0.0000%) | `1,254` -> `236` | `-1,018` | `22.1388%` | LOST |
| `PoC epoch 266` |  | `4,105,361` / `2026-05-16 23:31:35 MSK` | `1,084` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,259,271` / `2026-05-26 05:59:12 MSK` | `10,016` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,265,964` / `2026-05-26 15:43:16 MSK` | `10,016` | pass_weight; sub 4,224; valid 614,628 (77.0183%) | no_submission; sub 0; valid 0 (0.0000%) | `8,698` -> `8,698` | `0` | `86.8411%` | kept |
| `cPoC #1` | `4,265,965` / `2026-05-26 15:43:21 MSK` | `4,266,246` / `2026-05-26 16:07:52 MSK` | `10,016` | pass_weight; sub 4,128; valid 613,141 (76.8319%) | no_submission; sub 0; valid 0 (0.0000%) | `8,698` -> `1,343` | `-7,355` | `13.4085%` | LOST |
| `cPoC #2` | `4,267,778` / `2026-05-26 18:25:04 MSK` | `4,270,604` / `2026-05-26 22:36:00 MSK` | `10,016` | pass_weight; sub 4,128; valid 694,624 (87.0425%) | no_submission; sub 0; valid 0 (0.0000%) | `1,343` -> `1,343` | `0` | `13.4085%` | after loss |
| `cPoC #3` | `4,270,605` / `2026-05-26 22:36:05 MSK` | `4,274,661` / `2026-05-27 04:36:32 MSK` | `10,016` | pass_weight; sub 4,224; valid 704,216 (88.2444%) | no_submission; sub 0; valid 0 (0.0000%) | `1,343` -> `1,343` | `0` | `13.4085%` | after loss |
| `PoC epoch 277` |  | `4,274,662` / `2026-05-27 04:36:37 MSK` | `7,533` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,197,707` / `2026-05-22 12:32:39 MSK` | `1,059` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,574` / `2026-05-22 19:37:00 MSK` | `1,059` | pass_weight; sub 896; valid 794,373 (96.5002%) | no_submission; sub 0; valid 0 (0.0000%) | `1,114` -> `291` | `-823` | `27.4788%` | LOST |
| `cPoC #1` | `4,202,715` / `2026-05-22 19:49:20 MSK` | `4,208,127` / `2026-05-23 03:41:03 MSK` | `1,059` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `291` -> `0` | `-291` | `0.0000%` | after loss |
| `cPoC #2` | `4,208,128` / `2026-05-23 03:41:08 MSK` | `4,209,685` / `2026-05-23 05:56:56 MSK` | `1,059` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #3` | `4,209,686` / `2026-05-23 05:57:01 MSK` | `4,211,723` / `2026-05-23 08:54:11 MSK` | `1,059` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #4` | `4,211,724` / `2026-05-23 08:54:16 MSK` | `4,213,097` / `2026-05-23 10:53:45 MSK` | `1,059` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 273` |  | `4,213,098` / `2026-05-23 10:53:51 MSK` | `585` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,213,098` / `2026-05-23 10:53:51 MSK` | `585` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,215,427` / `2026-05-23 14:16:57 MSK` | `4,215,708` / `2026-05-23 14:41:29 MSK` | `585` | pass_weight; sub 832; valid 566,480 (74.6631%) | no_submission; sub 0; valid 0 (0.0000%) | `615` -> `274` | `-341` | `46.8376%` | LOST |
| `PoC epoch 274` |  | `4,228,489` / `2026-05-24 09:11:40 MSK` | `371` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,228,489` / `2026-05-24 09:11:40 MSK` | `371` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,229,666` / `2026-05-24 10:54:36 MSK` | `4,231,814` / `2026-05-24 14:02:37 MSK` | `371` | pass_weight; sub 960; valid 528,504 (68.9230%) | no_submission; sub 0; valid 0 (0.0000%) | `390` -> `312` | `-78` | `84.0970%` | reduced |
| `cPoC #1` | `4,231,815` / `2026-05-24 14:02:43 MSK` | `4,232,096` / `2026-05-24 14:27:23 MSK` | `371` | pass_weight; sub 320; valid 639,375 (83.3818%) | no_submission; sub 0; valid 0 (0.0000%) | `312` -> `103` | `-209` | `27.7628%` | LOST |
| `cPoC #2` | `4,232,787` / `2026-05-24 15:27:37 MSK` | `4,234,330` / `2026-05-24 17:42:30 MSK` | `371` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `103` -> `0` | `-103` | `0.0000%` | after loss |
| `cPoC #3` | `4,234,331` / `2026-05-24 17:42:36 MSK` | `4,242,456` / `2026-05-25 05:27:16 MSK` | `371` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #4` | `4,242,457` / `2026-05-25 05:27:22 MSK` | `4,243,879` / `2026-05-25 07:31:22 MSK` | `371` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 275` |  | `4,243,880` / `2026-05-25 07:31:28 MSK` | `328` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,243,880` / `2026-05-25 07:31:28 MSK` | `328` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,248,892` / `2026-05-25 14:50:15 MSK` | `4,249,773` / `2026-05-25 16:07:25 MSK` | `328` | pass_weight; sub 896; valid 663,716 (90.0656%) | no_submission; sub 0; valid 0 (0.0000%) | `345` -> `289` | `-56` | `88.1098%` | reduced |
| `cPoC #1` | `4,249,774` / `2026-05-25 16:07:31 MSK` | `4,258,196` / `2026-05-26 04:25:02 MSK` | `328` | pass_weight; sub 960; valid 548,096 (74.3761%) | no_submission; sub 0; valid 0 (0.0000%) | `289` -> `289` | `0` | `88.1098%` | kept |
| `cPoC #2` | `4,258,197` / `2026-05-26 04:25:08 MSK` | `4,258,478` / `2026-05-26 04:49:49 MSK` | `328` | pass_weight; sub 320; valid 666,218 (90.4051%) | no_submission; sub 0; valid 0 (0.0000%) | `289` -> `105` | `-184` | `32.0122%` | LOST |
| `PoC epoch 276` |  | `4,259,271` / `2026-05-26 05:59:12 MSK` | `328` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,151,534` / `2026-05-19 17:33:15 MSK` | `1,280` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,153,434` / `2026-05-19 20:19:10 MSK` | `4,153,715` / `2026-05-19 20:43:43 MSK` | `1,280` | pass_weight; sub 1,728; valid 594,093 (87.4442%) | no_submission; sub 0; valid 0 (0.0000%) | `1,347` -> `562` | `-785` | `43.9062%` | LOST |
| `cPoC #1` | `4,155,550` / `2026-05-19 23:23:27 MSK` | `4,157,968` / `2026-05-20 02:53:44 MSK` | `1,280` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `562` -> `562` | `0` | `43.9062%` | after loss |
| `cPoC #2` | `4,157,969` / `2026-05-20 02:53:49 MSK` | `4,162,915` / `2026-05-20 10:03:53 MSK` | `1,280` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `562` -> `0` | `-562` | `0.0000%` | after loss |
| `cPoC #3` | `4,162,916` / `2026-05-20 10:03:55 MSK` | `4,163,711` / `2026-05-20 11:13:07 MSK` | `1,280` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #4` | `4,163,712` / `2026-05-20 11:13:13 MSK` | `4,164,860` / `2026-05-20 12:53:09 MSK` | `1,280` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #5` | `4,164,861` / `2026-05-20 12:53:15 MSK` | `4,166,924` / `2026-05-20 15:52:05 MSK` | `1,280` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 270` |  | `4,166,925` / `2026-05-20 15:52:11 MSK` | `0` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,197,707` / `2026-05-22 12:32:39 MSK` | `426` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,574` / `2026-05-22 19:37:00 MSK` | `426` | pass_weight; sub 1,375; valid 793,001 (96.3335%) | no_submission; sub 0; valid 0 (0.0000%) | `2,506` -> `447` | `-2,059` | `104.9296%` | LOST |
| `cPoC #1` | `4,202,715` / `2026-05-22 19:49:20 MSK` | `4,208,127` / `2026-05-23 03:41:03 MSK` | `426` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `447` -> `0` | `-447` | `0.0000%` | after loss |
| `cPoC #2` | `4,208,128` / `2026-05-23 03:41:08 MSK` | `4,209,685` / `2026-05-23 05:56:56 MSK` | `426` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #3` | `4,209,686` / `2026-05-23 05:57:01 MSK` | `4,211,723` / `2026-05-23 08:54:11 MSK` | `426` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #4` | `4,211,724` / `2026-05-23 08:54:16 MSK` | `4,213,097` / `2026-05-23 10:53:45 MSK` | `426` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 273` |  | `4,213,098` / `2026-05-23 10:53:51 MSK` | `436` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,136,143` / `2026-05-18 19:14:41 MSK` | `62,145` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,136,924` / `2026-05-18 20:22:09 MSK` | `4,139,231` / `2026-05-18 23:42:55 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 77,984; valid 575,036 (82.3080%) | `91,616` -> `90,027` | `-1,589` | `144.8660%` | reduced |
| `cPoC #1` | `4,139,232` / `2026-05-18 23:43:01 MSK` | `4,141,308` / `2026-05-19 02:43:44 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 77,504; valid 579,803 (82.9904%) | `90,027` -> `89,471` | `-556` | `143.9714%` | reduced |
| `cPoC #2` | `4,141,309` / `2026-05-19 02:43:50 MSK` | `4,144,897` / `2026-05-19 07:56:14 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 77,120; valid 588,609 (84.2508%) | `89,471` -> `89,030` | `-441` | `143.2617%` | reduced |
| `cPoC #3` | `4,144,898` / `2026-05-19 07:56:20 MSK` | `4,145,179` / `2026-05-19 08:20:52 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 12,480; valid 619,380 (88.6552%) | `89,030` -> `14,477` | `-74,553` | `23.2955%` | LOST |
| `cPoC #4` | `4,148,831` / `2026-05-19 13:39:06 MSK` | `4,149,819` / `2026-05-19 15:04:43 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `14,477` -> `0` | `-14,477` | `0.0000%` | after loss |
| `cPoC #5` | `4,149,820` / `2026-05-19 15:04:49 MSK` | `4,150,412` / `2026-05-19 15:56:09 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `cPoC #6` | `4,150,413` / `2026-05-19 15:56:15 MSK` | `4,151,533` / `2026-05-19 17:33:09 MSK` | `62,145` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 269` |  | `4,151,534` / `2026-05-19 17:33:15 MSK` | `23,602` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,197,707` / `2026-05-22 12:32:39 MSK` | `65,281` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,714` / `2026-05-22 19:49:14 MSK` | `65,281` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 38,944; valid 715,470 (86.9151%) | `74,947` -> `44,527` | `-30,420` | `68.2082%` | reduced |
| `cPoC #1` | `4,202,715` / `2026-05-22 19:49:20 MSK` | `4,208,127` / `2026-05-23 03:41:03 MSK` | `65,281` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 25,792; valid 757,571 (92.0295%) | `44,527` -> `44,339` | `-188` | `67.9202%` | reduced |
| `cPoC #2` | `4,208,128` / `2026-05-23 03:41:08 MSK` | `4,209,685` / `2026-05-23 05:56:56 MSK` | `65,281` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 38,368; valid 745,006 (90.5031%) | `44,339` -> `44,078` | `-261` | `67.5204%` | reduced |
| `cPoC #3` | `4,209,686` / `2026-05-23 05:57:01 MSK` | `4,209,967` / `2026-05-23 06:21:32 MSK` | `65,281` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 23,872; valid 748,261 (90.8985%) | `44,078` -> `27,426` | `-16,652` | `42.0122%` | LOST |
| `cPoC #4` | `4,211,724` / `2026-05-23 08:54:16 MSK` | `4,213,097` / `2026-05-23 10:53:45 MSK` | `65,281` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 13,184; valid 774,646 (94.1037%) | `27,426` -> `27,426` | `0` | `42.0122%` | after loss |
| `PoC epoch 273` |  | `4,213,098` / `2026-05-23 10:53:51 MSK` | `21,183` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,228,489` / `2026-05-24 09:11:40 MSK` | `468` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,229,666` / `2026-05-24 10:54:36 MSK` | `4,231,814` / `2026-05-24 14:02:37 MSK` | `468` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `492` -> `492` | `0` | `105.1282%` | kept |
| `cPoC #1` | `4,231,815` / `2026-05-24 14:02:43 MSK` | `4,232,786` / `2026-05-24 15:27:32 MSK` | `468` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `492` -> `492` | `0` | `105.1282%` | kept |
| `cPoC #2` | `4,232,787` / `2026-05-24 15:27:37 MSK` | `4,233,068` / `2026-05-24 15:52:09 MSK` | `468` | pass_weight; sub 416; valid 612,200 (79.8379%) | no_submission; sub 0; valid 0 (0.0000%) | `492` -> `136` | `-356` | `29.0598%` | LOST |
| `cPoC #3` | `4,234,331` / `2026-05-24 17:42:36 MSK` | `4,242,456` / `2026-05-25 05:27:16 MSK` | `468` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `136` -> `136` | `0` | `29.0598%` | after loss |
| `cPoC #4` | `4,242,457` / `2026-05-25 05:27:22 MSK` | `4,243,879` / `2026-05-25 07:31:22 MSK` | `468` | pass_weight; sub 1,600; valid 675,634 (88.1104%) | no_submission; sub 0; valid 0 (0.0000%) | `136` -> `136` | `0` | `29.0598%` | after loss |
| `PoC epoch 275` |  | `4,243,880` / `2026-05-25 07:31:28 MSK` | `419` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,059,188` / `2026-05-14 05:51:04 MSK` | `17,777` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,073,650` / `2026-05-15 02:33:51 MSK` | `4,073,931` / `2026-05-15 02:58:01 MSK` | `17,777` | pass_weight; sub 7,264; valid 726,111 (69.4650%) | no_submission; sub 0; valid 0 (0.0000%) | `17,777` -> `2,387` | `-15,390` | `13.4275%` | LOST |
| `PoC epoch 264` |  | `4,074,579` / `2026-05-15 03:53:30 MSK` | `17,777` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,259,271` / `2026-05-26 05:59:12 MSK` | `28,493` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,264,130` / `2026-05-26 13:03:34 MSK` | `4,264,411` / `2026-05-26 13:28:07 MSK` | `28,493` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 13,920; valid 595,705 (74.6470%) | `48,847` -> `16,147` | `-32,700` | `56.6701%` | LOST |
| `cPoC #1` | `4,265,965` / `2026-05-26 15:43:21 MSK` | `4,267,777` / `2026-05-26 18:24:58 MSK` | `28,493` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 14,112; valid 628,376 (78.7410%) | `16,147` -> `16,135` | `-12` | `56.6279%` | after loss |
| `cPoC #2` | `4,267,778` / `2026-05-26 18:25:04 MSK` | `4,270,604` / `2026-05-26 22:36:00 MSK` | `28,493` | no_submission; sub 0; valid 0 (0.0000%) | no_submission; sub 0; valid 0 (0.0000%) | `16,135` -> `0` | `-16,135` | `0.0000%` | after loss |
| `cPoC #3` | `4,270,605` / `2026-05-26 22:36:05 MSK` | `4,274,661` / `2026-05-27 04:36:32 MSK` | `28,493` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 13,568; valid 629,637 (78.8990%) | `0` -> `0` | `0` | `0.0000%` | after loss |
| `PoC epoch 277` |  | `4,274,662` / `2026-05-27 04:36:37 MSK` | `8,997` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,074,579` / `2026-05-15 03:53:30 MSK` | `6,982` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,075,202` / `2026-05-15 04:47:04 MSK` | `4,075,483` / `2026-05-15 05:11:12 MSK` | `6,982` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 2,272; valid 713,388 (70.6191%) | `7,349` -> `2,660` | `-4,689` | `38.0980%` | LOST |
| `cPoC #1` | `4,075,770` / `2026-05-15 05:35:44 MSK` | `4,089,969` / `2026-05-16 01:48:37 MSK` | `6,982` | no_submission; sub 0; valid 0 (0.0000%) | pass_weight; sub 4,800; valid 724,283 (71.6976%) | `2,660` -> `2,660` | `0` | `38.0980%` | after loss |
| `PoC epoch 265` |  | `4,089,970` / `2026-05-16 01:48:39 MSK` | `0` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,197,707` / `2026-05-22 12:32:39 MSK` | `23,298` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,202,293` / `2026-05-22 19:12:26 MSK` | `4,202,574` / `2026-05-22 19:37:00 MSK` | `23,298` | pass_weight; sub 13,056; valid 792,893 (96.3204%) | no_submission; sub 0; valid 0 (0.0000%) | `24,524` -> `4,249` | `-20,275` | `18.2376%` | LOST |
| `cPoC #1` | `4,202,715` / `2026-05-22 19:49:20 MSK` | `4,208,127` / `2026-05-23 03:41:03 MSK` | `23,298` | pass_weight; sub 8,640; valid 705,182 (85.6653%) | no_submission; sub 0; valid 0 (0.0000%) | `4,249` -> `3,263` | `-986` | `14.0055%` | after loss |
| `cPoC #2` | `4,208,128` / `2026-05-23 03:41:08 MSK` | `4,209,685` / `2026-05-23 05:56:56 MSK` | `23,298` | pass_weight; sub 8,768; valid 712,788 (86.5893%) | no_submission; sub 0; valid 0 (0.0000%) | `3,263` -> `3,263` | `0` | `14.0055%` | after loss |
| `cPoC #3` | `4,209,686` / `2026-05-23 05:57:01 MSK` | `4,211,723` / `2026-05-23 08:54:11 MSK` | `23,298` | pass_weight; sub 8,640; valid 709,757 (86.2210%) | no_submission; sub 0; valid 0 (0.0000%) | `3,263` -> `3,263` | `0` | `14.0055%` | after loss |
| `cPoC #4` | `4,211,724` / `2026-05-23 08:54:16 MSK` | `4,213,097` / `2026-05-23 10:53:45 MSK` | `23,298` | pass_weight; sub 8,896; valid 702,463 (85.3350%) | no_submission; sub 0; valid 0 (0.0000%) | `3,263` -> `3,263` | `0` | `14.0055%` | after loss |
| `PoC epoch 273` |  | `4,213,098` / `2026-05-23 10:53:51 MSK` | `3,128` |  |  |  |  |  | next PoC |

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

| Event | Trigger / MSK | Snapshot / MSK | PoC weight | Qwen | Kimi | CW before -> after | Delta | After/PoC weight | Status |
|---:|---|---|---:|---|---|---:|---:|---:|---|
| `PoC` |  | `4,213,098` / `2026-05-23 10:53:51 MSK` | `8,069` |  |  |  |  |  | PoC |
| `cPoC #0` | `4,215,427` / `2026-05-23 14:16:57 MSK` | `4,215,708` / `2026-05-23 14:41:29 MSK` | `8,069` | pass_weight; sub 8,128; valid 558,411 (73.5996%) | no_submission; sub 0; valid 0 (0.0000%) | `10,669` -> `3,062` | `-7,607` | `37.9477%` | LOST |
| `PoC epoch 274` |  | `4,228,489` / `2026-05-24 09:11:40 MSK` | `7,339` |  |  |  |  |  | next PoC |

Loss point: at cPoC `#0` confirmation weight moves from `10,669` to `3,062`; this is the row where the participant becomes a candidate for lost reward accounting.
