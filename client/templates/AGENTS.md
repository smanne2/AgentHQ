# Agent HQ — bootstrap required

Before ANY work in this project:

1. Call `agent_hq.bootstrap` with `{"projectPath": "__PROJECT_PATH__"}`.
2. Follow the returned workflow: phases in order, one at a time.
3. At each phase start, call `agent_hq.get_checklist` for that phase;
   consult the returned roles / instructions / skills before acting.
4. At each phase end, call `agent_hq.report_progress` with completed
   checklist indices and evidence. If the response flags a failed gate,
   stop and surface it to the user.
5. Never skip or reorder phases. If you must deviate, ask the user first
   and record the deviation in your report.

Project profile (pinned content): `.agent-hq/profile.yaml`
Detected stack: __STACK__ · profile: __PROFILE__
