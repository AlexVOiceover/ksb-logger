# KSB Interpretation Guide for Level 4 Software Developer Apprenticeship

This guide explains what assessors look for when evaluating evidence for each type of KSB (Knowledge, Skill, Behaviour) under the Accelerate People assessment framework.

## General Assessment Principles

### STAR Framework
All portfolio entries should follow the STAR structure:
- **Situation/Task**: What was the context? What needed to be done?
- **Action**: What did you specifically do? (Technical details, decisions made)
- **Result**: What was the outcome? What changed?
- **Reflection**: What did you learn? How did this develop your competency?

### Evidence Requirements by Type

#### Knowledge KSBs (K-prefix)
**What assessors need**: Evidence that you **understand** the concept, not just that you used it.

**Strong evidence shows:**
- Explanation of the concept in your own words
- Decision-making between alternatives with rationale
- Application of understanding to solve a specific problem
- Recognition of trade-offs or limitations
- Context of when/why the concept applies

**Weak evidence:**
- Simply naming or mentioning the concept
- Following a tutorial without explanation
- Copying patterns without understanding why

**Example for K5-3 (Agile vs Waterfall):**
- ✅ Strong: "I chose an iterative approach for this feature because user requirements were unclear. This allowed us to release an MVP and gather feedback, unlike a Waterfall approach which would have required complete upfront specifications."
- ❌ Weak: "We used Agile methodology for this project."

#### Skill KSBs (S-prefix)
**What assessors need**: Evidence that you can **practically apply** the skill to produce results.

**Strong evidence shows:**
- Tangible outputs (code, designs, tests, documentation)
- Technical execution demonstrating competence
- Following established practices or frameworks correctly
- Quality indicators (test coverage, code review feedback, performance)
- Iterative improvement showing skill development

**Weak evidence:**
- Vague descriptions without outputs
- Claims without supporting artifacts
- Superficial application
- No quality indicators

**Example for S13 (Follow testing frameworks):**
- ✅ Strong: "I wrote 12 unit tests using Jest, achieving 95% coverage of the authentication module. I followed the AAA pattern (Arrange, Act, Assert) and used mock objects to isolate dependencies."
- ❌ Weak: "I wrote some tests for the code."

#### Behaviour KSBs (B-prefix)
**What assessors need**: Evidence of **patterns** of professional conduct over time, not one-off actions.

**Strong evidence shows:**
- Repeated demonstrations across multiple situations
- Professional attitudes and approaches
- Interactions with others (collaboration, communication)
- Reflection on personal development
- Initiative and independence
- Examples from different contexts

**Weak evidence:**
- One-time actions
- Generic statements ("I am a team player")
- No specific examples
- No reflection on development

**Example for B4 (Collaborative working):**
- ✅ Strong: "I actively participated in code reviews, providing constructive feedback on 8 PRs this month. When reviewing Sarah's authentication PR, I suggested using environment variables for API keys instead of hardcoding, explaining the security rationale. I also incorporated feedback from team reviews into my own work, such as extracting repeated validation logic into a shared utility function as Tom suggested."
- ❌ Weak: "I work well with my team."

## Specific KSB Guidance

### K1-1: Software Development Life-Cycle
**What this means in practice:**
- Understanding planning → design → implementation → testing → deployment → maintenance
- Contributing meaningfully to multiple stages
- Recognizing what stage you're in and what's appropriate

**Good evidence:**
- PRs spanning different lifecycle stages (requirements discussion → implementation → testing → deployment)
- Explaining decisions appropriate to the stage (e.g., "During design, we chose...")
- Post-deployment maintenance or monitoring

### K3-2: Project roles and responsibilities
**What this means in practice:**
- Knowing who does what in your team/organization
- Understanding your own role and responsibilities
- Working effectively within that structure

**Good evidence:**
- Describing collaboration with specific roles (PM, QA, DevOps, etc.)
- Explaining how you contributed within your role boundaries
- Escalating or coordinating appropriately

### K4-3: Communication methods and adaptation
**What this means in practice:**
- Choosing appropriate channels (email, Slack, meeting, documentation)
- Tailoring message to audience (technical vs non-technical)
- Effective information conveyance

**Good evidence:**
- Examples of different communication modes for different purposes
- Explaining why you chose a method
- Adapting explanation based on audience knowledge

### K5-3: Agile vs Waterfall methodologies
**What this means in practice:**
- Understanding the fundamental differences in approach
- Recognizing benefits and limitations of each
- Making appropriate choices based on context

**Good evidence:**
- Comparing specific characteristics (iterative vs sequential, flexibility vs planning, etc.)
- Explaining how methodology choice affects your work
- Describing experience with at least one methodology in detail

### K7-7: Design patterns
**What this means in practice:**
- Recognizing common problems with established solutions
- Applying patterns appropriately (not over-engineering)
- Understanding when and why to use specific patterns

**Good evidence:**
- Identifying a pattern by name (Singleton, Factory, Observer, MVC, etc.)
- Explaining why the pattern solved your problem
- Describing the structure and how you implemented it
- Discussing alternatives you considered

### K8-3: Organizational policies (e.g., GDPR)
**What this means in practice:**
- Knowing relevant company policies, security standards, legal requirements
- Following them in your work
- Understanding when they apply

**Good evidence:**
- Describing specific policies you followed
- Explaining how they affected your implementation choices
- Examples of compliance in code or process

### K10-2: Relational and non-relational databases
**What this means in practice:**
- Understanding structured (SQL) vs flexible (NoSQL) data storage
- Knowing when to use each type
- Recognizing characteristics and trade-offs

**Good evidence:**
- Comparing specific features (schemas, relationships, query methods, scalability)
- Explaining your database choice for a project
- Demonstrating use of appropriate database operations

### K12-7: Testing frameworks and methodologies
**What this means in practice:**
- Understanding different test types (unit, integration, E2E, etc.)
- Knowing testing strategies and approaches
- Awareness of testing tools and frameworks

**Good evidence:**
- Explaining test types and when to use them
- Describing testing approaches (TDD, BDD, etc.)
- Demonstrating knowledge of testing tools (Jest, Pytest, Selenium, etc.)

### S2-5: Develop effective user interfaces
**What this means in practice:**
- Creating UIs that are usable, intuitive, and accessible
- Considering layout, color, typography, interaction
- Focusing on user experience

**Good evidence:**
- Screenshots or descriptions of UI implementations
- Explaining design decisions (why this layout, why these colors)
- Demonstrating responsiveness, accessibility, or usability improvements
- User feedback or testing results

### S3-5: Link code to data sets
**What this means in practice:**
- Writing code that reads, writes, and updates data
- Working with files, databases, or APIs
- Managing data flow in applications

**Good evidence:**
- Code examples showing data operations (CRUD operations)
- Explaining data sources and formats
- Demonstrating error handling and data validation
- Database queries or API integration

### S5-8: Conduct range of test types
**What this means in practice:**
- Performing multiple test types, not just unit tests
- Ensuring quality through comprehensive testing
- Going beyond basic functionality tests

**Good evidence:**
- Examples of different test types (integration, system, UAT, performance, security)
- Test code or test plans
- Describing what each test type validated
- Test results and bug discoveries

### S8: Create simple software designs
**What this means in practice:**
- Drawing diagrams to communicate program structure
- Using flowcharts, wireframes, or UML
- Making technical concepts visual

**Good evidence:**
- Actual diagrams (flowcharts, component diagrams, wireframes, sequence diagrams)
- Explaining what the design communicates
- Showing how it guided implementation

### S9: Create analysis artefacts (use cases/user stories)
**What this means in practice:**
- Translating requirements into structured formats
- Writing user stories (As a... I want... So that...)
- Detailing use cases with steps and actors

**Good evidence:**
- Actual user stories or use cases you created
- Showing how they guided development
- Demonstrating acceptance criteria
- Examples of story refinement or decomposition

### S13: Follow testing frameworks and methodologies
**What this means in practice:**
- Actually using testing frameworks (not just knowing about them - that's K12)
- Writing and executing tests
- Following testing best practices

**Good evidence:**
- Test code using specific frameworks
- Test coverage reports
- Describing your testing approach
- Following testing patterns (AAA, Given-When-Then, etc.)

### S14: CI/CD, version control, source control
**What this means in practice:**
- Using Git effectively (branching, commits, PRs, merges)
- Working with CI pipelines
- Collaborating through source control

**Good evidence:**
- Git workflow descriptions
- PR examples with meaningful commits
- CI pipeline configurations or fixes
- Branching strategies
- Merge conflict resolution

### S15: Communicate to technical and non-technical stakeholders
**What this means in practice:**
- Explaining solutions to different audiences
- Adapting technical depth appropriately
- Ensuring understanding across skill levels

**Good evidence:**
- Examples of technical documentation for developers
- Examples of user-facing documentation or explanations
- Presentation or demo descriptions
- Showing how you adapted communication style

### S17: Implement design with security and maintainability
**What this means in practice:**
- Turning designs into working code
- Writing secure code (input validation, authentication, avoiding vulnerabilities)
- Writing maintainable code (readable, modular, documented)

**Good evidence:**
- Implementation following a design
- Security measures (authentication, authorization, input sanitization)
- Code quality indicators (clear naming, documentation, modularity)
- Describing security or maintainability considerations

### B1: Works independently and takes responsibility
**What this means in practice:**
- Self-managing and owning your work
- Staying motivated through challenges
- Being accountable for quality and outcomes

**Good evidence:**
- Examples of working independently on tasks
- Overcoming challenges or setbacks
- Taking ownership of problems
- Self-directed learning
- Multiple examples showing pattern

### B4: Works collaboratively with diverse people
**What this means in practice:**
- Being an effective team player
- Working with people in different roles
- Inclusive and respectful behavior

**Good evidence:**
- Collaboration examples (code reviews, pair programming, meetings)
- Working with different roles (designers, QA, PM, etc.)
- Incorporating feedback
- Helping others
- Multiple collaboration examples

### B5: Acts with integrity (ethical, legal, regulatory)
**What this means in practice:**
- Being trustworthy and responsible
- Following ethical guidelines
- Protecting user data and privacy
- Making secure and legal choices

**Good evidence:**
- Examples of ethical decision-making
- GDPR or data protection implementations
- Security-conscious choices
- Explaining integrity considerations

### B6: Shows initiative and resourcefulness
**What this means in practice:**
- Being proactive, not just reactive
- Solving problems independently before asking
- Finding creative solutions

**Good evidence:**
- Examples of proactive improvements
- Describing problem-solving approach
- Self-guided research
- Going beyond requirements
- Multiple initiative examples

### B7: Communicates effectively in variety of situations
**What this means in practice:**
- Flexible communication across contexts
- Adapting to different settings (formal/informal, written/verbal)
- Clear technical and non-technical communication

**Good evidence:**
- Examples from different situations
- Different communication formats
- Adapting to different audiences
- Multiple communication examples

### B8: Shows curiosity about business context
**What this means in practice:**
- Understanding the "why" behind technical work
- Being curious about users and business needs
- Exploring new technologies and approaches
- Creative problem-solving

**Good evidence:**
- Explaining business rationale for technical choices
- Describing user impact
- Learning new technologies
- Asking questions about requirements
- Multiple curiosity examples

### B9: Committed to continued professional development
**What this means in practice:**
- Actively learning and improving skills
- Keeping up with technology changes
- Developing soft skills as well as technical skills

**Good evidence:**
- Learning new languages, frameworks, or tools
- Taking courses or certifications
- Reading documentation or articles
- Improving based on feedback
- Multiple learning examples over time

## Minimum Evidence Standards

For portfolio assessment:
- **Each KSB needs**: At least 400-600 words of narrative + clear supporting evidence
- **Evidence must be**: Verifiable (links, code snippets, screenshots, documents)
- **Multiple sources**: Ideally use 2-3 pieces of evidence per KSB where possible
- **Reflection required**: Show what you learned, how you've grown
- **Context essential**: Explain the situation, the stakes, the constraints

## Red Flags (What to Avoid)

- Generic statements without specific examples
- Claiming skills without demonstrating them
- Evidence that doesn't match the KSB
- No technical depth or detail
- No reflection or learning shown
- Unclear or missing context
- Evidence that could be anyone's work (not personalized)
