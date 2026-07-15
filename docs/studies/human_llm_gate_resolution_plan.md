# Human-LLM gate resolution plan

Status: planning document only. Rights evidence and controlled private-packet handling are documented for protocol review. Provider/model/account planning and the metadata-only v0.2 audit are documented, but account availability remains unverified because the audit environment had no credential. The merged preparation and audit layers do not authorize human coding, model execution, provider transmission, final execution, or empirical analysis. See the [current evidence index](human_llm_current_evidence_index.md).

This PR does not authorize coding or execution. In the current merged-tree
context, the same prohibition applies to every preparation and metadata-audit
layer described above.

Overall execution status remains: `EXECUTION_BLOCKED`.

## Remaining sequence

1. Rights evidence has been documented for every selected case.
2. Controlled private-packet handling has been approved for controlled storage, metadata-only public documentation, hash verification, and future separately authorized access logs only.
3. The historical provider/model/account planning record remains at `data/studies/human_llm_pilot/provider_model_account_verification.json`. The current v0.2 audit at `data/studies/human_llm_pilot/provider_model_account_verification_v0_2.json` found no credential and made no provider request, so exact-model account access remains unverified.
4. Verify runtime and structured-output settings, including response mode, sampling controls, token limits, retry policy, and request/response preservation.
5. Verify pricing immediately before execution and confirm the hard spending ceiling.
6. Authorize a non-study dry run only after rights, private-packet, provider, runtime, pricing, and logging gates are ready for that limited purpose.
7. Authorize human coding only after packet hashes are verified under the access protocol, the human coding environment is documented, record locking is ready, and final authorization is granted.
8. Authorize model execution only after all provider-transmission, model/account/runtime/pricing, prompt, and preservation gates pass.
9. Begin empirical analysis only after all human records and model records are created, locked, hashed, and validated under the frozen protocol.

Closed, unmerged PR #18 remains the sample/prompt freeze provenance reference at its frozen head. Merged PR #20 contains the rights/private-packet gate evidence plus the no-call LLM and no-coding human scaffolds; merged PR #22 adds metadata-only provider/runtime auditing. Neither starts coding or execution.
