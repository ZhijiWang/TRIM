# TRIM Research and Study Index

This is the authoritative navigation page for research lines in the TRIM repository. It distinguishes the active blocked study from public demonstrations, deferred research, and historical retained work.

## Active study

### Design B Human–LLM Friction-Locus Pilot

The active study is a procedural comparison between a pre-exposure human record and independently generated model records. It is not a human intercoder-reliability study and does not treat either record as a truth standard.

Lineage:

- protocol lineage: [PR #17](https://github.com/ZhijiWang/TRIM/pull/17), merged;
- frozen package lineage: [PR #18](https://github.com/ZhijiWang/TRIM/pull/18), closed, draft, and unmerged at the frozen dependency head;
- authoritative manual lineage: [PR #19](https://github.com/ZhijiWang/TRIM/pull/19), merged;
- blocked preparation layer: [PR #20](https://github.com/ZhijiWang/TRIM/pull/20), merged;
- navigation layer: [PR #21](https://github.com/ZhijiWang/TRIM/pull/21), merged;
- metadata-only provider/runtime audit: [PR #22](https://github.com/ZhijiWang/TRIM/pull/22), merged;
- current execution state: `EXECUTION_BLOCKED`;
- current human-coding state: `HUMAN_CODING_BLOCKED`.

Start with:

- [Pilot overview](human_llm_pilot_readme.md)
- [Gate-resolution plan](human_llm_gate_resolution_plan.md)
- [No-call LLM execution scaffold](human_llm_execution_scaffold.md)
- [Provider and runtime capability audit](provider_runtime_capability_audit.md)
- [Current evidence and status index](human_llm_current_evidence_index.md)
- [No-coding human annotation scaffold](human_coding_scaffold.md)
- [Rights-evidence summary](human_llm_rights_evidence_summary.md)
- [Controlled private-packet handling protocol](private_packet_handling_protocol.md)

Current gate interpretation:

- rights evidence is `PASSED_WITH_DOWNSTREAM_GATES_BLOCKED`, sufficient only for preparation;
- controlled packet handling is `PASSED_WITH_CONTROLLED_ACCESS_ONLY`, sufficient only for controlled-access preparation;
- provider/model/account, runtime settings, pricing, final authorization, human coding, and model execution remain `BLOCKED`;
- merging PR #20 did not authorize packet inspection, provider transmission, human coding, or model execution.

The versioned provider/runtime capability audit found no local API credential on 2026-07-13, made no provider request, and left account access unverified. The [current evidence index](human_llm_current_evidence_index.md) distinguishes that v0.2 result from the historical v0.1 blocked record. Runtime settings remain unfrozen pending a separately authorized no-source synthetic inference verification; pricing and final authorization also remain blocked.

## Public demonstrations

- [Synthetic dry run](../../examples/synthetic_dry_run/valid/README.md): synthetic valid/invalid fixtures for technical validation behavior.
- [In a Grove author-only walkthrough](../../examples/in_a_grove_walkthrough/README.md): repository-bound author demonstration whose English translation remains `NOT_AUTHORIZED_FOR_UNRESTRICTED_REDISTRIBUTION`; it is not a public release-bundle component.
- [In a Grove Public Walkthrough v0.2](in_a_grove_public_v0_2_release_status.md): current external release-status addendum for the frozen and tagged (`in-a-grove-public-v0.2.0`) Japanese-canonical walkthrough with locked records and descriptive comparison.

These demonstrations show representational and auditability behavior. They are not empirical validation, participant research, reliability evidence, a truth verdict, or a general claim about model behavior.

## Deferred research

- [TRIM-HAA position note](../../research/position_note/TRIM_HAA_position_note_v0_1.md): deferred publication and claim-boundary line.
- [Future human-subject exposure/instrumentation study](../../research/future_human_study/README.md): ethics and protocol drafts for a separate future pilot.

Neither deferred line is the current Design B Human–LLM Friction-Locus Pilot. No recruitment or data collection is authorized by their presence in the repository.

## Historical retained lines

- **Legacy TRIM External-Coder Retest v0.2.x:** historical project line. The legacy runtime is retained through Git history and tag `legacy-trim-v0.2.1`, not the active tree. See [Legacy History](../legacy_history.md).
- **PR #13:** [historical v0.2.2 retest deployment line](https://github.com/ZhijiWang/TRIM/pull/13), not current mainline.
- **PR #14:** [historical AI-execution comparison line](https://github.com/ZhijiWang/TRIM/pull/14), not current mainline.

## Pull-request lifecycle notes

| PR | Current interpretation |
|---|---|
| [#9](https://github.com/ZhijiWang/TRIM/pull/9) | Closed and unmerged; retained historically after being superseded by merged PR #10. |
| [#13](https://github.com/ZhijiWang/TRIM/pull/13) | Closed and unmerged historical v0.2.2 line; not current mainline. |
| [#14](https://github.com/ZhijiWang/TRIM/pull/14) | Closed and unmerged historical AI-execution comparison line; not current mainline. |
| [#18](https://github.com/ZhijiWang/TRIM/pull/18) | Closed, draft, and unmerged frozen historical dependency at head `eac65f27bbe302a17e5f508ac1d516178e917aea`. |
| [#20](https://github.com/ZhijiWang/TRIM/pull/20) | Merged blocked preparation layer; it did not authorize execution or coding. |
| [#21](https://github.com/ZhijiWang/TRIM/pull/21) | Merged repository-navigation layer. |
| [#22](https://github.com/ZhijiWang/TRIM/pull/22) | Merged metadata-only provider/runtime audit; no credential was available and no provider request occurred. |

This index records status only. It does not close, merge, retarget, or otherwise modify any pull request.
