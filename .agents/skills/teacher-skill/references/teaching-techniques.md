# Teaching Techniques

Concrete, evidence-based techniques to apply while this skill is active. Most
techniques here come from The Carpentries' Collaborative Lesson Development
Training and Instructor Training curricula (evidence-based curricula used to
develop and certify instructors for Software/Data/Library Carpentry, CC BY
4.0) or The Turing Way's Pathways guide (CC BY 4.0); one is grounded in a
named peer-reviewed education research paper instead. Every technique below
has its source named next to it. Do not add a technique here without a
source; do not apply a technique in a session without reading it here first.

## Find the learner's entry point and persona

The Turing Way's Pathways guide organizes its handbook around a learner's role
so people can "select [the pathway] most relevant to them, without having to
browse different guides" instead of forcing one fixed path on everyone. The
Carpentries' lesson-design training goes further: characterize the learner
along three dimensions before teaching — **expertise level** (novice,
competent practitioner, or expert), **motivation** (what they actually want to
be able to do and why), and **prior knowledge** (what they can already do,
noting that "people are often bad at self-assessment" about this).

- Before teaching, work out in one focused question or from context already
  given: the learner's role/background, their goal, and roughly their
  expertise level. Do not run a long intake questionnaire.
- Adapt style to expertise level: a **novice** benefits from worked examples
  and step-by-step, tutorial-like explanation; a **competent practitioner**
  is better served by room to explore and try their own approach than by
  being walked through every step.

Sources: [Pathways](https://book.the-turing-way.org/pathways/pathways/) (The
Turing Way); [Identifying Your Target
Audience](https://carpentries.github.io/lesson-development-training/audience.html)
(The Carpentries).

## Decide what "learned" looks like before explaining

Backward design starts from the outcome, not the content: define the desired
learning outcome, design how you will check it, and only then produce the
explanation that gets the learner there — checking progress and revisiting the
outcome as you go, rather than writing an explanation first and hoping it
lands.

- Before explaining, form a concrete, observable target for this teaching
  moment, phrased with a specific action verb ("explain," "identify,"
  "predict," "write") rather than a vague one like "understand" or "know."
- Decide how you will check that target (a question, a small task) before you
  write the explanation, so the explanation is built to get the learner there.
- Treat your first explanation as a draft: check whether it worked and revise
  your approach for the next chunk rather than assuming one pass is enough.

Source: [Lesson
Design](https://carpentries.github.io/lesson-development-training/lesson-design.html)
and [Defining Lesson
Objectives](https://carpentries.github.io/lesson-development-training/objectives.html)
(The Carpentries).

## Teach in small, self-contained chunks

Working memory holds only about 7±2 items at once, and lessons are built from
short, self-contained chunks (the Carpentries call them "episodes") rather
than one long pass, each covering only two to four objectives and ordered by
what depends on what.

- Teach one sub-skill at a time; do not cover more than a small handful of new
  ideas before checking in.
- Order chunks by prerequisite: what must the learner already have before this
  makes sense, and can a complex skill be decomposed into simpler steps first?
- Show only what you are currently teaching; do not display unrelated
  material or run ahead of what you have explained.
- Use worked or faded examples (partially filled in) before asking the
  learner to do a step fully on their own — this scaffolds novices without
  removing all of the challenge.

Sources: [Episodes](https://carpentries.github.io/lesson-development-training/episodes.html)
(The Carpentries); [Memory and Cognitive
Load](https://carpentries.github.io/instructor-training/05-memory.html) (The
Carpentries).

## Give the chunks a throughline

"Writing your lesson as a story helps learners stay motivated and engaged,
which means they will learn faster." Tying a sequence of chunks to one
authentic, relatable situation — rather than presenting them as a
disconnected list of facts — cuts the mental cost of switching between
unrelated scenarios and gives the learner memory anchors that strengthen
recall.

- When a topic has several connected steps or decisions, tie them to a single
  throughline (the concrete problem being solved, or a running example) and
  say explicitly how each piece serves it, rather than presenting a list.
- Prefer an authentic, relatable example over an abstract or contrived one —
  even a short explanation benefits from one running example rather than a
  new example per point.

Source: [Example Data and
Narrative](https://carpentries.github.io/lesson-development-training/narrative.html)
(The Carpentries).

## Make checks diagnostic, not just right/wrong

When a wrong answer is possible, "the incorrect answers you provide as options
are at least as important as the correct answer because they offer the most
useful insight into the mental model your audience is building."

- When you check understanding with options or a guess, make the plausible
  wrong answers reflect real, specific misconceptions rather than obviously
  wrong choices, so a wrong answer tells you exactly what to correct.
- Treat any mistake the learner makes as diagnostic information about their
  current mental model, not just something to mark wrong.
- If a check reveals a misconception, stop and address it directly before
  moving to the next chunk; do not build the next chunk on a broken
  foundation.

Source: [Designing
Exercises](https://carpentries.github.io/lesson-development-training/misconceptions-mcqs.html)
(The Carpentries).

## Audit your own explanation

Before giving an explanation, and while giving it, watch for the same
demotivating patterns lesson developers are told to remove from written
lessons:

- Dismissive language ("just," "simply").
- Unstated assumptions of prior knowledge ("expert gaps").
- Interchangeable terms used without saying they're interchangeable (for
  example "shell" vs. "bash").
- Unexplained jargon, especially for a novice or a non-native speaker.
- Sudden jumps in difficulty instead of a consistent progression.
- Idioms, regional references, or contractions that could confuse a non-native
  speaker; describe any layout or visual you refer to in words, since a
  learner may not see it the way you do.

Also apply "less is more": cover the few things that matter for the learner's
actual goal thoroughly, rather than everything adjacent to the topic
superficially. If you must cut scope, cut whole objectives — content, checks,
and all — rather than thinning every topic slightly.

Source: [How to Write a
Lesson](https://carpentries.github.io/lesson-development-training/explanation.html)
(The Carpentries).

## Narrate reasoning and demonstrate live

Experts jump straight from problem to solution because their mental models are
densely connected; novices need every intermediate step spelled out, and an
expert who has forgotten what confusion feels like will skip steps without
noticing. For procedural or code tasks, building the solution step by step out
loud is more instructive than presenting a finished result, because it
surfaces the troubleshooting process a finished answer hides.

- Explain your reasoning step by step rather than jumping to the answer, even
  when a step feels obvious to you.
- Model error diagnosis out loud: when something goes wrong, narrate how you
  notice and investigate it, not just the fix.
- Build a solution incrementally instead of pasting a complete answer, so the
  learner can follow each decision.
- Invite questions with real wait time using "What questions do you have?"
  rather than "Does anyone have questions?", which implies none are expected.
- State the actual reasoning outright rather than only dropping hints or
  asking leading questions and waiting for the learner to guess it: for
  novices, minimally-guided discovery is measurably less effective than
  clear, explicit instruction.

Sources: [Expertise and
Instruction](https://carpentries.github.io/instructor-training/04-expertise.html);
[Live Coding Is a
Skill](https://carpentries.github.io/instructor-training/17-live.html) (The
Carpentries); Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). "Why
Minimal Guidance During Instruction Does Not Work: An Analysis of the Failure
of Constructivist, Discovery, Problem-Based, Experiential, and Inquiry-Based
Teaching." *Educational Psychologist*, 41(2), 75-86.

## Give feedback with growth-mindset framing

Effective teaching treats itself as a skill improved through regular feedback,
and how mistakes and effort are framed changes whether a learner keeps trying.

- Periodically ask what is unclear or not working, and say explicitly what you
  are changing in response rather than adjusting silently.
- Frame mistakes as normal and informative, not as a sign of low ability.
- Praise effort and strategy ("you tried two different approaches") rather
  than innate talent ("you're naturally good at this").
- Reframe "I can't do this" as "I can't do this yet."
- Avoid behavior that signals a learner does not belong: contempt for the
  tools or approach they are using, surprise at a knowledge gap ("you've never
  heard of X?"), or taking over their work instead of guiding it.

Sources: [Building Skill With
Feedback](https://carpentries.github.io/instructor-training/06-feedback.html);
[Motivation and
Demotivation](https://carpentries.github.io/instructor-training/08-motivation.html)
(The Carpentries).

## Adapt to accessibility and background needs

Universal Design for Learning designs for diverse learners from the start
rather than retrofitting accessibility later, and what helps one learner tends
to help everyone.

- If a learner states an accessibility or background need, adapt to it
  directly rather than assuming a default learner.
- Offer more than one way to engage with the same material where practical
  (for example, a plain-language explanation alongside a worked example or an
  analogy), rather than only one format.
- Do not assume shared background knowledge; check rather than assume.

Source: [Equity, Inclusion, and
Accessibility](https://carpentries.github.io/instructor-training/09-eia.html)
(The Carpentries).
