---
name: Spike
description: Time-boxed investigation to answer a question or de-risk a design. Output is a decision, not production code.
version: "1"
phases:
  - id: question
    title: Frame the Question
    checklist:
      - "State the decision the spike must inform"
      - "Define the time/effort box and the success criteria"
    gate:
      kind: manual
  - id: investigate
    title: Investigate
    checklist:
      - "Prototype, prototype, or experiment run"
      - "Observations recorded (what worked, what didn't, why)"
    gate:
      kind: checklist-complete
  - id: report
    title: Decide & Report
    checklist:
      - "Written recommendation: go / no-go / needs-more, with evidence"
      - "Cleanup: throwaway prototype removed or explicitly kept"
    gate:
      kind: none
---
## Phase details

### question
A spike answers a specific question within a specific budget. Frame both up front,
or the spike becomes an unbounded project.

### investigate
Build the smallest thing that answers the question — often a throwaway script.
Record observations as you go; the experiment is valuable, not the artifact.

### report
Convert observations into a recommendation with evidence. Decide what to keep (a
helper worth promoting) and what to delete. The report is the deliverable.
