# P3-CAND-04 Scope Control Scan

Scan range: epochs `270..283`.

The scan classifies cPoC stages around the `v0.2.13` upgrade. A row is
`case4_like_misfire = 1` only when the cPoC trigger is post-upgrade and
still inside the upgrade epoch.

Case4-like rows found: `2`.

| Epoch | Epoch relation | PoC start | Last | Trigger | Trigger MSK | Blocks after upgrade | Upgrade-epoch skip window | Case4-like | Excluded | Interpretation |
|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| `270` | `before_upgrade` | `4166925` | `4182715` | `4168597` | 2026-05-20 18:18:17 MSK | `` | `0` | `0` | `1` | control epoch before upgrade |
| `270` | `before_upgrade` | `4166925` | `4182715` | `4172961` | 2026-05-21 00:38:44 MSK | `` | `0` | `0` | `3` | control epoch before upgrade |
| `271` | `before_upgrade` | `4182316` | `4198106` | `4184386` | 2026-05-21 17:12:37 MSK | `` | `0` | `0` | `2` | control epoch before upgrade |
| `271` | `before_upgrade` | `4182316` | `4198106` | `4185816` | 2026-05-21 19:17:22 MSK | `` | `0` | `0` | `2` | control epoch before upgrade |
| `271` | `before_upgrade` | `4182316` | `4198106` | `4190338` | 2026-05-22 01:51:40 MSK | `` | `0` | `0` | `3` | control epoch before upgrade |
| `272` | `before_upgrade` | `4197707` | `4213497` | `4202293` | 2026-05-22 19:12:26 MSK | `` | `0` | `0` | `4` | control epoch before upgrade |
| `272` | `before_upgrade` | `4197707` | `4213497` | `4208128` | 2026-05-23 03:41:08 MSK | `` | `0` | `0` | `1` | control epoch before upgrade |
| `272` | `before_upgrade` | `4197707` | `4213497` | `4209686` | 2026-05-23 05:57:01 MSK | `` | `0` | `0` | `1` | control epoch before upgrade |
| `272` | `before_upgrade` | `4197707` | `4213497` | `4212947` | 2026-05-23 10:40:41 MSK | `` | `0` | `0` | `1` | control epoch before upgrade |
| `273` | `before_upgrade` | `4213098` | `4228888` | `4215427` | 2026-05-23 14:16:57 MSK | `` | `0` | `0` | `11` | control epoch before upgrade |
| `274` | `before_upgrade` | `4228489` | `4244279` | `4229666` | 2026-05-24 10:54:36 MSK | `` | `0` | `0` | `8` | control epoch before upgrade |
| `274` | `before_upgrade` | `4228489` | `4244279` | `4231815` | 2026-05-24 14:02:43 MSK | `` | `0` | `0` | `3` | control epoch before upgrade |
| `274` | `before_upgrade` | `4228489` | `4244279` | `4232787` | 2026-05-24 15:27:37 MSK | `` | `0` | `0` | `3` | control epoch before upgrade |
| `274` | `before_upgrade` | `4228489` | `4244279` | `4242457` | 2026-05-25 05:27:22 MSK | `` | `0` | `0` | `1` | control epoch before upgrade |
| `275` | `before_upgrade` | `4243880` | `4259670` | `4248892` | 2026-05-25 14:50:15 MSK | `` | `0` | `0` | `6` | control epoch before upgrade |
| `275` | `before_upgrade` | `4243880` | `4259670` | `4258197` | 2026-05-26 04:25:08 MSK | `` | `0` | `0` | `1` | control epoch before upgrade |
| `276` | `upgrade_epoch` | `4259271` | `4275061` | `4264130` | 2026-05-26 13:03:34 MSK | `` | `0` | `0` | `6` | non-target control row |
| `276` | `upgrade_epoch` | `4259271` | `4275061` | `4265965` | 2026-05-26 15:43:21 MSK | `` | `0` | `0` | `2` | non-target control row |
| `276` | `upgrade_epoch` | `4259271` | `4275061` | `4267778` | 2026-05-26 18:25:04 MSK | `478` | `1` | `1` | `5` | post-upgrade cPoC inside upgrade epoch; expected skip under release-note behavior |
| `276` | `upgrade_epoch` | `4259271` | `4275061` | `4270605` | 2026-05-26 22:36:05 MSK | `3305` | `1` | `1` | `2` | post-upgrade cPoC inside upgrade epoch; expected skip under release-note behavior |
| `277` | `after_upgrade_epoch` | `4274662` | `4290452` | `4284638` | 2026-05-27 19:23:22 MSK | `17338` | `0` | `0` | `6` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `278` | `after_upgrade_epoch` | `4290053` | `4305843` | `4290816` | 2026-05-28 04:32:31 MSK | `23516` | `0` | `0` | `1` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `278` | `after_upgrade_epoch` | `4290053` | `4305843` | `4295294` | 2026-05-28 11:09:45 MSK | `27994` | `0` | `0` | `4` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `278` | `after_upgrade_epoch` | `4290053` | `4305843` | `4296271` | 2026-05-28 12:36:24 MSK | `28971` | `0` | `0` | `1` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `278` | `after_upgrade_epoch` | `4290053` | `4305843` | `4301852` | 2026-05-28 20:50:47 MSK | `34552` | `0` | `0` | `6` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `279` | `after_upgrade_epoch` | `4305444` | `4321234` | `4316397` | 2026-05-29 18:32:12 MSK | `49097` | `0` | `0` | `8` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `280` | `after_upgrade_epoch` | `4320835` | `4336625` | `4323125` | 2026-05-30 04:35:46 MSK | `55825` | `0` | `0` | `2` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `281` | `after_upgrade_epoch` | `4336226` | `4352016` | `4338543` | 2026-05-31 03:37:58 MSK | `71243` | `0` | `0` | `2` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `282` | `after_upgrade_epoch` | `4351617` | `4367407` | `4352701` | 2026-06-01 00:44:34 MSK | `85401` | `0` | `0` | `6` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `282` | `after_upgrade_epoch` | `4351617` | `4367407` | `4356074` | 2026-06-01 05:47:39 MSK | `88774` | `0` | `0` | `4` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `282` | `after_upgrade_epoch` | `4351617` | `4367407` | `4360448` | 2026-06-01 12:20:33 MSK | `93148` | `0` | `0` | `2` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `282` | `after_upgrade_epoch` | `4351617` | `4367407` | `4365458` | 2026-06-01 19:50:34 MSK | `98158` | `0` | `0` | `2` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `283` | `after_upgrade_epoch` | `4367008` | `0` | `4370923` | 2026-06-02 04:00:36 MSK | `103623` | `0` | `0` | `5` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
| `283` | `after_upgrade_epoch` | `4367008` | `0` | `4373098` | 2026-06-02 07:15:38 MSK | `105798` | `0` | `0` | `1` | clean later epoch; cPoC is not the same upgrade-epoch misfire |
