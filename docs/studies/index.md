# TRIM Research and Study Index

This is the authoritative navigation page for research lines in the TRIM repository. It distinguishes the active blocked study from public demonstrations, deferred research, and historical retained work.

## Active study

### Design B Human–LLM Friction-Locus Pilot

The active study is a procedural comparison between a pre-exposure human record and independently generated model records. It is not a human intercoder-reliability study and does not treat either record as a truth standard.

Lineage:

- protocol lineage: [PR #17](https://github.com/ZhijiWang/TRIM/pull/17), merged;
- frozen package lineage: [PR #18](https://github.com/ZhijiWang/TRIM/pull/18), open and draft as the frozen dependency;
- authoritative manual lineage: [PR #19](https://github.com/ZhijiWang/TRIM/pull/19), merged;
- blocked preparation layer: [PR #20](https://github.com/ZhijiWang/TRIM/pull/20), merged;
- current execution state: `EXECUTION_BLOCKED`;
- current human-coding state: `HUMAN_CODING_BLOCKED`.

Start with:

- [Pilot overview](human_llm_pilot_readme.md)
- [Gate-resolution plan](human_llm_gate_resolution_plan.md)
- [No-call LLM execution scaffold](human_llm_execution_scaffold.md)
- [No-coding human annotation scaffold](human_coding_scaffold.md)
- [Rights-evidence summary](human_llm_rights_evidence_summary.md)
- [Controlled private-packet handling protocol](private_packet_handling_protocol.md)

Current gate interpretation:

- rights evidence is `PASSED_WITH_DOWNSTREAM_GATES_BLOCKED`, sufficient only for preparation;
- controlled packet handling is `PASSED_WITH_CONTROLLED_ACCESS_ONLY`, sufficient only for controlled-access preparation;
- provider/model/account, runtime settings, pricing, final authorization, human coding, and model execution remain `BLOCKED`;
- merging PR #20 did not authorize packet inspection, provider transmission, human coding, or model execution.

## Public demonstrations

- [Synthetic dry run](../../examples/synthetic_dry_run/valid/README.md): synthetic valid/invalid fixtures for technical validation behavior.
- [In a Grove author-only walkthrough](../../examples/in_a_grove_walkthrough/README.md): repository-bound author demonstration.
- [In a Grove Public Walkthrough v0.2](../../examples/in_a_grove_walkthrough_public_v0_2/RELEASE_NOTES_DRAFT.md): frozen and tagged (`in-a-grove-public-v0.2.0`) Japanese-canonical walkthrough with locked records and descriptive comparison.

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
| [#9](https://github.com/ZhijiWang/TRIM/pull/9) | Superseded by merged PR #10; still open until a separate lifecycle-cleanup task records and closes it. |
| [#13](https://github.com/ZhijiWang/TRIM/pull/13) | Historical v0.2.2 line; not current mainline. |
| [#14](https://github.com/ZhijiWang/TRIM/pull/14) | Historical AI-execution comparison line; not current mainline. |
| [#18](https://github.com/ZhijiWang/TRIM/pull/18) | Open, draft frozen dependency; leave unchanged until its lifecycle is separately decided. |
| [#20](https://github.com/ZhijiWang/TRIM/pull/20) | Merged blocked preparation layer; it did not authorize execution or coding. |

This index records status only. It does not close, merge, retarget, or otherwise modify any pull request.
