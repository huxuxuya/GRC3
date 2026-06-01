# GRC Chat Update Export - 2026-06-01

Source: `Exported Data_Update.pdf`, generated from the Telegram export `ChatExport_2026-06-01`.

This file indexes the update messages used to refresh the public case tracker.

| Message ID | Date (UTC+03) | Author | Case / Topic | Fact |
|---|---|---|---|---|
| `510` | 2026-05-26 09:23:34 | Evgenii Maksimenkov | P3-CAND-02 | The broad unclaimed-reward scan found 576 participants, then narrowed to 19 participants conclusively affected by the negative-balance settle-drop path; total recovery stated as about 1,075 GNK. |
| `517` | 2026-05-26 19:13:35 | Votkon | Coordination | `@OpenMindedPerson` elected as proposal coordinator. |
| `518` | 2026-05-26 19:25:04 | Votkon | P3-CAND-03 | Proposed deciding the failed cPoC / preserved Kimi shortfall case and noted that identifying all affected parties is difficult because preserved-node history is unclear. |
| `522` | 2026-05-26 21:54:54 | Egor | P3-CAND-04 | `LastUpgradeHeight` was not written after `v0.2.13`, so the cPoC skip did not detect the recent upgrade; epoch group data retained old snapshot scales. |
| `527` | 2026-05-27 09:31:07 | Evgenii Maksimenkov | P3-CAND-04 | `UpgradeProtectionWindow` was supposed to be 10,000 blocks, nearly 15 hours. |
| `528` | 2026-05-27 10:12:47 | Evgenii Maksimenkov | P3-CAND-04 | Published `gonkavip/payout276`; methodology compares block heights `4267299` and `4274661`; total stated as 36,209 GNK. |
| `529` | 2026-05-27 12:09:27 | Nik | P3-CAND-04 | Re-ran `payout_276.py node1.gonka.ai`; script completed and matched expected unreceived coins. |
| `533` | 2026-05-27 17:50:23 | Votkon | P4-CAND-01 | Published the full Kimi e265-e276 analysis; stated root cause as a third-party attack and proposed voting on GRC inclusion. |
| `538`-`541` | 2026-05-27 18:07-18:15 | Arturs Plisko; Nik; Votkon | P4-CAND-01 | Discussed whether losses went to governance or were redistributed under network rules; Votkon noted that on-chain PoC nonces can restore precise loss. |
| `542` | 2026-05-27 23:42:28 | Fedor Tmkhv | Proposal #3 assignments | Listed five Proposal #3 cases and current investigator / validator assignments. |
| `548` | 2026-05-28 18:44:50 | Fedor Tmkhv | Proposal #3 assignments | Assigned validators: case #2 `@dem_ww`; case #3 `@dem_ww` and `@votkon`; case #4 `@votkon` and `@OpenMindedPerson`; case #5 `@maksimenkoff` and `@mikenosov`. |
| `553` | 2026-05-29 08:29:41 | Evgenii Maksimenkov | P4-CAND-01 | Reviewed Kimi case: numbers appear correct; supports direct attack impact more than GroupCap effects across later epochs. |
| `554` | 2026-05-29 08:37:19 | Votkon | P4-CAND-01 | Stated GRC voted against including the Kimi case and that the GRC position would be recorded. |
| `556` | 2026-05-30 18:29:45 | Mike | Process | Proposed a GRC intake form before investigation / validation. |
| `558` | 2026-05-30 18:40:58 | Votkon | P3-CAND-03 | Clarified that he proposed case #3 after encountering it during the Kimi investigation. |
| `559` | 2026-05-30 18:57:45 | Mike | P3-CAND-03 | Published `gonkalabs/GRC-e267-kimi_shortfall/blob/main/grc-form.md`. |
| `560` | 2026-05-30 20:49:22 | Mike | P3-CAND-03 | Published report v1; one fully valid participant set with about 10.2k GNK; validators asked to review. |
| `561`-`573` | 2026-05-30 20:55-21:14 | Evgenii Maksimenkov; Mike; Nik; Gleb Morgachev; Votkon | P3-CAND-03 | Eligibility disputed due to old proxy configuration / missing `poc/proofs` exemption; Gleb warned against a precedent for node misconfiguration; Votkon suggested voting. |
| `576` | 2026-05-31 23:28:32 | Fedor Tmkhv | P3-CAND-01 | Case #1 draft and preliminary calculations were prepared; validator changed to `@mikenosov` because the case requires devshard data. |
| `577` | 2026-05-31 23:29:05 | Fedor Tmkhv | Schedule | Suggested finishing all work by Monday, 2026-06-08. |
| `583` | 2026-06-01 00:54:34 | Mike | P4-CAND-01 | Raised Kimi validation objections: e265-e266 GRC scope, e267-e276 denominator, e276 proration, and e266 script/output mismatch. |
| `585` | 2026-06-01 15:39:29 | Fedor Tmkhv | P3-CAND-01 | Case #1 ready for `@mikenosov` review; 6 affected participants; estimated compensation `30,715.490665898 GNK`; epochs 273-280 did not show the same pattern; `v0.2.13` likely addressed it. |
