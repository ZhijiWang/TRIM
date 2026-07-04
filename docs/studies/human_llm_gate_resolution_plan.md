# Human-LLM gate resolution plan

Status: planning document only. This PR does not authorize private-packet inspection, rights approval, human coding, model execution, or empirical analysis.

Overall execution status remains: `BLOCKED_PENDING_RIGHTS_PRIVATE_PACKETS_MODEL_ACCOUNT_RUNTIME_SETTINGS_PRICING_AND_FINAL_EXECUTION_AUTHORIZATION`.

## Remaining sequence

1. Collect documentary rights evidence for every selected case, including source, edition, translation, jurisdiction, and redistribution/provider-transmission status where applicable.
2. Review and approve the controlled private-packet handling protocol. Do not inspect private packet text before this gate is approved.
3. Verify provider, model, account availability, data-handling terms, and endpoint compatibility.
4. Verify runtime and structured-output settings, including response mode, sampling controls, token limits, retry policy, and request/response preservation.
5. Verify pricing immediately before execution and confirm the hard spending ceiling.
6. Authorize a non-study dry run only after rights, private-packet, provider, runtime, pricing, and logging gates are ready for that limited purpose.
7. Authorize human coding only after rights status is resolved for every selected packet, private-packet handling is approved, packet hashes are verified, and record locking is ready.
8. Authorize model execution only after all rights, provider-transmission, model/account/runtime/pricing, prompt, and preservation gates pass.
9. Begin empirical analysis only after all human records and model records are created, locked, hashed, and validated under the frozen protocol.

PR #18 remains the sample/prompt freeze reference. This PR prepares the rights/private-packet gate evidence framework only.
