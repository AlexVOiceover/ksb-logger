# Portfolio

## KSB Evidence Summary

| KSB ID | Description | Evidence |
|--------|-------------|----------|
| K1 | All stages of the software development life-cycle | [View Evidence](#ksb-k1) |
| K3 | The roles and responsibilities of the project life-cycle wit... | [View Evidence](#ksb-k3) |
| K4 | How best to communicate using the different communication me... | [View Evidence](#ksb-k4) |
| K5 | The similarities and differences between different software ... | ❌ No evidence yet |
| K7 | Software design approaches and patterns | [View Evidence](#ksb-k7) |
| K8 | Organisational policies and procedures relating to the tasks... | [View Evidence](#ksb-k8) |
| K10 | Principles and uses of relational and non-relational databas... | [View Evidence](#ksb-k10) |
| K12 | Software testing frameworks and methodologies | [View Evidence](#ksb-k12) |
| S2 | Develop effective user interfaces | [View Evidence](#ksb-s2) |
| S3 | Link code to data sets | [View Evidence](#ksb-s3) |
| S5 | Conduct a range of test types | [View Evidence](#ksb-s5) |
| S8 | Create simple software designs to effectively communicate un... | [View Evidence](#ksb-s8) |
| S9 | Create analysis artefacts | [View Evidence](#ksb-s9) |
| S13 | Follow testing frameworks and methodologies | [View Evidence](#ksb-s13) |
| S14 | Follow company | [View Evidence](#ksb-s14) |
| S15 | Communicate software solutions and ideas to technical and no... | [View Evidence](#ksb-s15) |
| S17 | Interpret and implement a given design whist remaining compl... | [View Evidence](#ksb-s17) |
| B1 | Works independently and takes responsibility. For example | [View Evidence](#ksb-b1) |
| B4 | Works collaboratively with a wide range of people in differe... | [View Evidence](#ksb-b4) |
| B5 | Acts with integrity with respect to ethical | [View Evidence](#ksb-b5) |
| B6 | Shows initiative and takes responsibility for solving proble... | [View Evidence](#ksb-b6) |
| B7 | Communicates effectively in a variety of situations to both ... | [View Evidence](#ksb-b7) |
| B8 | Shows curiosity to the business context in which the solutio... | [View Evidence](#ksb-b8) |
| B9 | Committed to continued professional development | [View Evidence](#ksb-b9) |

---

## <a id="ksb-k1"></a>"Harmonising Multi-Platform User Experience with Tooltip Enhancements and Mobile Optimisation" [==KSB K1==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/42 ==]
### Achieving Harmonised User Experience Across Platforms

A critical need for a more robust solution emerged when we discovered conflicting requirements for desktop and mobile user experiences. To address these issues, several enhancements were implemented to ensure a cohesive and user-friendly interface. A comprehensive tooltip system was introduced with smart positioning across eight possible placements and augmented with accessibility features to serve diverse user needs. Contextual tooltips were added to indicate question status, promoting better understanding among users. This system also included tooltips for the visibility toggle to clarify response-sharing settings. Adjusting the tooltip show delay to 300 ms was critical to enhance user interaction by reducing distraction from prematurely appearing tooltips.

[==insert code snippet of: Tooltip component with smart positioning==]

### Balancing Design Aesthetics with Functionality

In addressing the balancing act between design aesthetics and functionality, mobile user experience improvements were prioritised. Enhanced viewport handling, achieved by transitioning from `h-screen` to `h-[100dvh]`, facilitated better mobile compatibility, while safe area insets ensured content remained accessible across devices, such as iPhones. UI and layout improvements included refined spacing, alignment consistency, and the strategic removal of visual clutter, such as the header's borderline and the dark theme. These comprehensive changes culminated in a more intuitive and visually appealing interface, demonstrating that a small, well-placed change can have a massive, positive ripple effect.

[==insert image of: improved mobile footer layout with safe area padding==]
## <a id="ksb-k3"></a>"Enhancing UI Consistency and Database Efficiency with Tailwind CSS and Improved Scripting" [==KSB K3==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/19 ==]
### Introducing Tailwind for Enhanced UI Styling

I inherited a piece of code that was difficult to test, which prompted me to reassess our project's styling framework. To advance the project's frontend development, I implemented Tailwind CSS, replacing placeholder classes with a more consistent and scalable styling approach. This change significantly improved the maintainability and appearance of the project's UI components. Key files such as `ListItem.svelte` and `Dash.svelte` were updated with the new styling framework. The transition to Tailwind facilitated a more streamlined development process by reducing the complexity of managing CSS classes, ultimately enhancing the visual coherence of the user interface.

[==insert code snippet of: an example of Tailwind CSS implementation in a Svelte component==]

### Streamlining Database Management with Enhanced Scripts

The project also involved integrating improved scripts to manage database operations more efficiently. These scripts were designed to handle both local and production environments, incorporating fake data generation and management actions. This involved creating scripts like `generate-test-data.js` and `prod-seed-questions.sh`, which were pivotal in automating data management. By structuring the scripts to differentiate between local and production use, the deployment process was optimised, ensuring seamless data migration and testing. This experience highlighted the value of feature flagging and gradually rolling out changes to users, as it allowed for safer and more controlled updates to the system.

[==insert code snippet of: a database script to seed data for testing==]
## <a id="ksb-k4"></a>"Enhancing Email System Performance Through JSON-Based Generation and Type Conversion Optimisation" [==KSB K4==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/21 ==]
### Optimising Email System for Enhanced Performance

This change simplified the onboarding process for new developers by optimising the email system. I identified inefficiencies in how emails were generated, which was a bottleneck due to basic text output methods. To address this, I implemented a JSON-based email generation system within `emailBuilder.ts` and `email.ts`. This included creating `EmailData` interfaces to structure email content and introducing functions like `generateEmailData()` for creating JSON objects from user responses and `renderEmailToHTML()` to transform this into styled HTML. These modifications facilitated more efficient data handling and improved the scalability of the email system. Additionally, I applied brand colours for visual consistency. This experience solidified my understanding of core asynchronous programming concepts.

[==insert code snippet of: generateEmailData() function==]

### Streamlining Action Service Type Handling

Another focal point was standardizing the type conversion process in the action services (`actions.ts`). Inconsistencies in type conversions were causing performance lags and potential data errors during database operations. I standardised the conversion from database types to `tableMain` types across all action service functions, including `getUserActions`, `createAction`, and others. The implementation of the new `getActionsByResponseId` function, complete with versioning logic, further optimised data retrieval processes, ensuring consistent and seamless function outputs.

[==insert code snippet of: type conversion implementation in actions.ts==]

### Visual Improvements in Email Preview

Although the visual styling is not finalised, I made preliminary updates to the `EmailPreview.svelte` component to support the new JSON-based system, replacing plain text with HTML rendering. This preliminary visual enhancement ensures emails now display category headers with a brand-styled teal background, clear Q&A hierarchies, and action items with status indicators for better functionality and readability.

[==insert image of: updated EmailPreview component showing structured content==]
## <a id="ksb-k7"></a>"Developing a Comprehensive Tooltip and Mobile Interface System for Enhanced User Experience" [==KSB K7==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/42 ==]
### Enhancing Usability: A Comprehensive Tooltip System

The discussion in the original issue ticket highlighted a clear need for a more intuitive and informative user experience, leading to the implementation of a comprehensive tooltip system. This enhancement bridges the gap between low-level technical details and the user-friendly interface, offering users contextual assistance as they navigate the application. The new tooltip component includes smart positioning with eight potential placements and ample accessibility features. Contextual tooltips are now available for question status indicators and the visibility toggle, aiding users in discerning between statuses and sharing responses effectively. Additionally, a default 300ms show delay was introduced to enhance user interaction without overwhelming them with immediate responses.

[==insert code snippet of: Tooltip component implementation with smart positioning==]

### Streamlining Mobile Experience & Interface Layout

Significant improvements were made to the mobile user experience by addressing viewport handling issues and optimizing layout responsiveness. Enhancements include using `h-[100dvh]` for dynamic viewport height and adding safe area insets specific to iPhones, ensuring elements do not clutter or extend beyond the viewable screen. The layout experienced polish with consistent max-width constraints across views, card-based grouping of dashboard categories, and improved spacing, notably reducing dashboard tile margins and footer padding. Though the dark theme was temporarily disabled for future contemplation, these refinements collectively create a more cohesive and accessible interface. Through these changes, I gained a practical understanding of how cryptographic signing works within user interface adjustments, ensuring a secure and seamless user experience.

[==insert image of: Updated mobile layout with safe area insets and improved footer==]
## <a id="ksb-k8"></a>"Developing an Automated Dashboard Solution for Enhanced Resource Access for Neurodivergent Employees" [==KSB K8==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/30 ==]
### Automating Resource Access for Neurodivergent Employees

In response to direct user feedback about the difficulty in accessing workplace support resources, I implemented an automated solution by introducing a new resources tile to the dashboard. This tile enables neurodivergent employees to conveniently access a curated list of 12 workplace resources, which are automatically populated each time the database is reset. The solution included adding a resources table to the database schema and creating a production seeding script to streamline deployment. This approach optimises the user experience by removing unnecessary UI elements and ensuring that resources can be efficiently maintained and updated. 

[==insert code snippet of: the creation and population of resources table==]

### Dashboard Enhancements and User Navigation Improvements

Enhancements were made to the dashboard interface to accommodate the new resources tile, which now appears alongside existing components. The tile displays the number of available resources and provides a streamlined list view with clickable URLs, which open in new tabs for seamless navigation without disrupting the user's workflow. This work demonstrates that a small, well-placed change can have a massive, positive ripple effect by improving access to essential information through better UI/UX design.

[==insert image of: resources tile on the dashboard showing resource count==]
## <a id="ksb-k10"></a>Standardising Database Seeding by Reconciling Environment Discrepancies and Optimising Schema Compatibility [==KSB K10==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/26 ==]
### Harmonising Seeding Processes Across Environments

The journey to deprecating a legacy system began with addressing significant issues in the database seeding scripts. This pull request focused on reconciling the discrepancies between local and production environments by adjusting scripts and schemas to align with current database requirements. By fixing the malformed URL encoding in the `prod-seed-test-data.sh` script, the data seeding process now accurately performs question lookups, thereby resolving critical malfunctions that previously hindered the creation of responses and actions. Additionally, by removing the deprecated `is_latest` field from response creation API calls, both environments have been standardised to ensure reliability in data generation.

[==insert code snippet of: fixed URL encoding in question lookup query==]

### Balancing Legacy and Modern Requirements

Navigating through conflicting requirements of outdated schemas and the need for a more streamlined approach, this pull request demonstrates a successful compromise between legacy constraints and modern database needs. Key changes involved regenerating test data SQL files to ensure their compatibility with the updated schema and integrating enhanced error handling mechanisms for question lookups. Removal of obsolete fields not only decluttered the code but also optimised the overall performance of database interactions. This meticulous effort culminated in a robust seeding process, ultimately leading to a newfound respect for the maintainers of the open-source libraries undeniably pivotal in our development process.

[==insert code snippet of: regenerated test data SQL files]==]
## <a id="ksb-k12"></a>"Integrating Contextual User Testing and UI Consistency Enhancements with Improved Developer Workflow" [==KSB K12==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/33 ==]
### Balancing Testing Requirements with Development Needs

This change is a foundational prerequisite for an upcoming feature, showcasing the delicate balance between improving testing capabilities and advancing UI consistency. A significant addition is the user selector dropdown, facilitating contextual user testing during development. The dropdown integrates with real user data fetched from the database, enabling seamless transitions and interactions with test user profiles. Emphasizing transient use, all related testing code and components are marked with "TESTING ONLY" comments to ensure easy removal prior to production deployment.
[==insert code snippet of: user selector dropdown implementation and "TESTING ONLY" comments==]

### Elevating UI Consistency and Developer Workflow

UI enhancements aim to harmonise the dashboard's visual layout, introducing consistency across tiles and list items. Changes include cursor behaviour adjustments to enhance user interaction feedback and meticulous refactoring of CSS classes to optimise component styling. Moreover, the PR restructures components, specifically relocating EmailPreview for cleaner architecture. Further improvements were made in responsive design, aided by upgraded TailwindCSS and DaisyUI theming. Coupled with these UI advancements, the introduction of GitHub Actions workflows and enhanced documentation fortifies development practices, making the environment more agile and comprehensive.

[==insert image of: improved UI layout and cursor behaviour on the dashboard==]

Overall, this task underscored the necessity of a comprehensive and fast test suite, ensuring that both testing requirements and ongoing development are synchronised effectively.
## <a id="ksb-s2"></a>"Optimising User Interface with Enhanced Tooltip System and Responsive Mobile Design Improvements" [==KSB S2==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/42 ==]
### Enhancing User Guidance and Mobile Experience

This update provided an opportunity to experiment with a new approach to solve a long-standing problem of improving user experience through better interface tools. By developing a comprehensive tooltip system, I directly addressed user feedback regarding the lack of contextual guidance within the application. Smart positioning with eight possible positions for tooltips was implemented, ensuring visibility without obstructing other UI elements. The system was augmented by including accessibility features to aid users relying on keyboard navigation, and default show delay settings prevent tooltips from appearing too rapidly. Contextual tooltips now provide guidance on question status indicators, such as pink requiring attention and grey marking answered or skipped questions, and on visibility toggles explaining public and private settings. This strategic enhancement empowers users to navigate more efficiently and makes the application more intuitive.

[==insert code snippet of: Tooltip component with smart positioning and accessibility features==]

### Responsive Design and Mobile UX Refinements

Significant improvements were made to the mobile user experience, responding to issues where content would appear misaligned or overly cluttered on smaller screens. The updates included switching from the `h-screen` utility to `h-[100dvh]` for dynamic viewport height handling, optimizing the layout for various devices. Safe area insets were added for iPhone compatibility, and footer spacing was adjusted to prevent content from touching screen edges. These changes ensured seamless functionality and a visually appealing interface on mobile devices. Legal compliance was enhanced through the addition of responsive Terms of Use and Privacy Policy buttons, incorporating comprehensive modals. As a result, users benefit from improved navigation and accessibility across diverse devices, with a cleaner and more organised interface.

[==insert image of: improved mobile footer layout with responsive legal buttons==]
## <a id="ksb-s3"></a>"Implementing Local Development Environment for Neo4j Using Docker and Environment-Specific Configurations" [==KSB S3==]
[==PR Link https://github.com/foundersandcoders/LIFT-backend/pull/7 ==]
### Enhancing Offline Development Experience

In response to direct user feedback about recurring issues with development relying on a remote database, I implemented a comprehensive local development setup using Docker for Neo4j. This change allows our team to work offline and avoid unintended modifications to the production database. By introducing `.env.local` and `.env.production` files, we enable environment-specific configurations. The `neo4j.ts` has been updated to dynamically load the appropriate `.env` file, facilitating seamless switching between local and production environments. This ensures that the command `deno task dev` initiates the backend connection with the local Neo4j Docker instance, while `deno task prod` connects it to AuraDB. This approach aims to enrich the developer experience by reducing dependency on remote services during development.  
[==insert code snippet of: introducing `.env.local` and `.env.production` for environment-specific configurations==]

### Streamlining Development with Docker

The incorporation of Docker for a local Neo4j setup is a pivotal addition. By providing detailed instructions to set up Docker Desktop and run a Neo4j container, developers can now locally manage their database instances. This Dockerisation ensures a consistent setup across various development environments, eradicating discrepancies that often arise from differing local configurations. The setup includes specific commands to start the local environment and seed the database, which can be accessed and verified through a local instance. This experience taught me to value progress over perfection, reinforcing that establishing a solid foundation can substantially improve the overall workflow for developers.  
[==insert image of: Docker running a local Neo4j instance==]
## <a id="ksb-s5"></a>"Optimising Database Structure and Email Preview System for Enhanced Performance and User Experience" [==KSB S5==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/24 ==]
### Refining the Database Structure

The performance of the search feature had degraded over time, prompting an investigation into the database structure and related functionality. In this pull request, I removed the obsolete `is_latest` column from the `responses` and `actions` tables. This decision was based on the move towards a more version-based logic which offers a cleaner and more efficient way to determine the latest entries. All related database scripts and functionalities were updated to support this change, including modifications to the version filtering functions and test data generation scripts. These updates ensure a more streamlined process and accurate version filtering, reducing unnecessary data handling operations.

[==insert code snippet of: database schema migration without is_latest column==]

### Enhancing the Email Preview System

In parallel with the database optimisation, I identified and resolved significant issues within the email preview functionality. This involved implementing filters to exclude deleted responses, which were appearing due to being created as new versions with empty content. Through updates in `emailBuilder.ts`, responses and actions with empty fields are now effectively filtered out, aligning with the "1 response = 1 action" business rule. Additionally, I introduced navigation and action buttons, such as "Back" and "Send", to the email preview interface to improve user interaction, adhering to DaisyUI design principles in `app.css`.

[==insert code snippet of: filtering logic for empty responses in emailBuilder.ts==]

[==insert image of: enhanced email preview UI with navigation buttons==]

These modifications collectively enhance both the backend structure and frontend user experience. In the process, I became much more adept at using the browser's performance profiling tools to hunt down bottlenecks, reflecting a significant growth in my technical expertise.
## <a id="ksb-s8"></a>"Redesigning File Upload User Experience with Smart Tooltips and Enhanced Mobile Optimisation" [==KSB S8==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/42 ==]
### Enhancing User Experience Through Tooltips and Mobile Optimisation

The user experience for file uploads was a known pain point, and I was tasked with redesigning it. This pull request addresses several crucial elements in the UI to improve both desktop and mobile user interactions. A major feature is the implementation of a comprehensive tooltip system, which includes smart positioning capabilities in eight different orientations and enhanced accessibility features. These tooltips provide contextual help, such as indicating question statuses (pink for needing attention, grey for answered/skipped) and explaining visibility controls, thereby facilitating a more intuitive navigation experience. To prevent unnecessary interruptions, a default 300ms delay has been added to tooltip display, ensuring a smoother interaction flow. 

[==insert code snippet of: Tooltip component with smart positioning==]

Significant improvements were also made to the mobile user experience, including optimised viewport handling and better content spacing. By switching from `h-screen` to `h-[100dvh]`, the application now handles dynamic viewport height more effectively, catering to a range of mobile devices. Additionally, the footer was enhanced with responsive legal compliance modals and improved button layouts, ensuring users have seamless access to important information. The layout adjustments, such as the consistent max-width constraint on all view content and the introduction of card-based grouping for better category organisation, collectively bring about a visually cohesive and user-centred design.

[==insert image of: improved mobile layout with better spacing==]

### Linting, Deployment, and Version Management Enhancements

Realising the power of a well-defined data contract in a microservices architecture, the deployment process was refined with the inclusion of an automated script to streamline version management. The new `deploy.sh` script automates the version increment and deployment processes, thereby enhancing the CI/CD pipeline's efficiency and reliability. By dynamically fetching version numbers from `package.json`, the deployment workflow is not only optimised but also greatly reduced the risk of human error caused by hardcoded values.

[==insert code snippet of: automated deployment script==]

Overall, the improvements made in this iteration not only enhance user interactions across devices but also effectively strengthen the development and deployment processes through automation and optimisation.
## <a id="ksb-s9"></a>"Refactoring Action Filtering and Creation Logic for Enhanced Application Stability and Reliability" [==KSB S9==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/35 ==]
### Enhancing Application Stability with Question-Based Action Filtering

I began by writing a failing test to reproduce the reported bug, highlighting risks in the existing actions system. The core issue stemmed from the response-based filtering mechanism, which threatened data consistency and obfuscated the system's state. To mitigate these risks, I refactored the actions filtering system from a response-based approach to a more reliable question-based strategy. By updating `filterLatestActions` to associate actions with `user_id + question_id` instead of `user_id + response_id`, the system can now more effectively return the latest action per question. This change ensures improved stability as actions align more intuitively with user interactions, reducing potential for data mismanagement. Additionally, an optional `question_id` field was integrated into the Action type to bolster filtering logic. These adjustments collectively fortify the system against inconsistencies by centralising the logic around questions rather than disparate responses.

[==insert code snippet of: filterLatestActions using user_id + question_id==]

### Automatic Action Creation for Improved Reliability

In conjunction with the improved filtering logic, I implemented automatic action creation to enhance the application's reliability. Previously, actions were often not created, even when users provided the necessary data, leading to incomplete records and user frustration. By integrating logic within the FormButton to detect when users include action type and description, actions are now created instantly upon response submission. This development not only streamlines processes but also guarantees data integrity through immediate action-response linkage. During this process, I reinforced the system by adding error handling mechanisms to maintain the backward compatibility of existing records and enhance the overall robustness of data operations. Ultimately, this initiative highlighted the importance of writing clear and concise documentation, allowing future developers to navigate enhancements easily.

[==insert code snippet of: logic in FormButton for automatic action creation==]
## <a id="ksb-s13"></a>"Enhancing Database Seeding through Schema and Encoding Fixes for Environment Consistency" [==KSB S13==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/26 ==]
### Database Seeding Challenges and Solutions

The primary objective was to enhance the database seeding process, aiming for a seamless and responsive user interface. Initially, the hypothesis was that deprecated schema fields and malformed API queries were causing disruptions, preventing necessary responses and actions from being created accurately in the production environment. Investigations led to identifying issues with URL encoding and deprecated fields in the API calls, necessitating a solution that could restore proper functionality to the seeding scripts. The changes implemented involved correcting malformed URL encoding in the `prod-seed-test-data.sh` script, removing deprecated `is_latest` fields from API calls, and integrating more robust error handling for question lookups. These adjustments were meticulously tested to ensure both local and production environments are capable of accurate data seeding. 
[==insert code snippet of: URL encoding fix and removal of deprecated fields==]

### Testing and Validation for Consistent Environments

To address the inconsistencies in the local and production environments, test data generation scripts were updated and regenerated to align with the current schema. Enhancements were made to the `scripts/generate-test-data.sh` to ensure it generated data that adhered to the updated schema requirements. By removing references to outdated fields, the team guaranteed that both responses and actions could be generated seamlessly without issues in both test environments. The updates not only optimised the production environment but also ensured that local tests aligned with production standards. As a result of these targeted efforts, it became an invaluable experience in effectively communicating complex technical constraints and resolutions to non-technical stakeholders.
[==insert code snippet of: updated test data generation script==]

Overall, this work has helped facilitate a smooth transition for both environments, ensuring reliable and efficient data seeding processes aligned with real-world requirements.
## <a id="ksb-s14"></a>"Refactoring Frontend Aesthetics with Tailwind and Streamlining Database Management Scripts" [==KSB S14==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/19 ==]
### Modernising Frontend Aesthetics

The core objective of this pull request was to refactor a critical piece of legacy code by merging aesthetic improvements from the `make-pretty` branch into the `auto_deploy` branch. This significant update involves a comprehensive revamp of the UI components using Tailwind styling, replacing previous dev placeholder classes to enhance visual consistency and sophistication across the application. Frontend file changes extend from styling in `ListItem.svelte` and `Footer.svelte` to views such as `Dash.svelte`, `Detail.svelte`, and `List.svelte`, integrating a more cohesive and appealing design throughout. These enhancements serve to not only improve user engagement but also to standardise visual elements, making the codebase more manageable and less prone to future styling inconsistencies. 

[==insert image of: updated UI with Tailwind styling==]

### Streamlining Database Management

In addition to UI improvements, this update is instrumental in pruning technical debt relating to database management scripts. The branch introduces several scripts for maintaining local and production database instances effectively. These scripts are designed to handle a range of tasks, from seeding fake data for testing to executing production migrations, ensuring a robust and flexible database configuration. This meticulous organisation of database scripts, like `generate-test-data.js` and `prod-seed-questions.sh`, helps clarify the distinction between local and production environments, reducing potential errors and enhancing overall codebase reliability. The work not only maintains existing functionality but optimises processes, contributing positively to the stability and maintainability of the application.

[==insert code snippet of: database script update for production seeding==]

This experience underscored the value of thoughtful code management and the importance of good mentorship, as effective refactoring and documentation provide significant support to junior developers navigating complex codebases.
## <a id="ksb-s15"></a>"Implementing a JSON-Based Email Preview System and Standardised Data Handling for Enhanced User Experience" [==KSB S15==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/21 ==]
### Enhancing User Experience through Structured Email Preview

This pull request introduces a JSON-based email preview system designed to improve the clarity and usability of email content by integrating user feedback. The new functionality allows users to see actions clearly displayed below question and answer pairs within preview emails, addressing a common user request for better visibility and structure. This enhancement leverages JSON objects to organise email data, converting them into styled HTML for better user interaction. Notably, brand colours and category headers are used to improve visual hierarchy and theme coherence, thus improving the overall aesthetic and user experience of emails. This update empowers users by providing a structured, visually appealing interface that makes relevant information more accessible and comprehensible.  

[==insert image of: the new email preview with structured content and action items displayed==]

### Consistent Data Handling for Improved Service Experience

Realising the power of a well-defined data contract in a microservices architecture, this update standardises type conversion across all action service functions, ensuring no breaking changes in existing code. This standardisation is crucial for maintaining data integrity and eliminating discrepancies that may confuse users. Several functions within the actions service, such as database operations related to user actions, have now been corrected to align with consistent 'tableMain' types. By ensuring uniform data handling, users can expect consistent, reliable interactions, which is especially critical for those relying on accurate and timely information for decision-making processes. This consistency across the board underscores the importance of robust data contracts in enhancing user trust and experience.

[==insert code snippet of: standardised type conversion for action service functions==]
## <a id="ksb-s17"></a>"Enhancing Tooltip System and Mobile User Experience with Smart Positioning and Responsive Design" [==KSB S17==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/42 ==]
### Comprehensive Tooltip and Mobile UX Enhancements

To improve the developer experience and streamline our workflow, I focused on enhancing the application's tooltip system and mobile user experience. A new component for tooltips was introduced, offering smart positioning across eight orientations, along with accessibility features. Tooltips now provide contextual assistance, such as explaining question status indicators and the implications of response visibility settings. This enhancement aims to guide users more effectively through the interface by delivering timely information. Additionally, a show delay of 300 milliseconds was added to tooltips to prevent them from appearing too quickly, ensuring they do not obstruct user interactions inadvertently. 

[==insert code snippet of: Tooltip component addition with smart positioning and accessibility features==]

### Design Consistency and Mobile Optimisation

Significant efforts were made to optimise the layout for mobile and ensure consistency across devices. The application's responsive design was improved by implementing safe area insets for compatibility with iPhones and other mobile browsers. Adjustments in the layout and spacing, such as reducing dashboard tile margins and ensuring footer components have sufficient safe area padding, contribute to a cleaner and more organised interface. Footer enhancements included responsive adjustments to Terms of Use and Privacy Policy buttons, ensuring legal compliance modals display appropriately across devices. These improvements enhance the overall user experience on mobile, making interactions smoother and more intuitive.

[==insert image of: improved footer layout with responsive text display on mobile devices==]

This project gave me a better appreciation for the challenges of API design, as enhancing the user experience necessitated a careful balance of aesthetics and functionality within the constraints of interface design principles.
## <a id="ksb-b1"></a>"Introducing a User-friendly Confirmation Modal with Enhanced Response Management and Button Functionality in Svelte Components" [==KSB B1==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/39 ==]
### Introduction of a User-friendly Confirmation Workflow

I was tasked with simplifying a notoriously complex part of the codebase by introducing a user-friendly confirmation modal to address a subtle, intermittent bug that had long plagued the team. This enhancement involved the creation of a new component, `ConfirmModal.svelte`, designed with DaisyUI styling. The modal not only provides users with the ability to cancel out accidental deletions by supporting click-outside-to-close functionality but also enhances the overall user experience with improved focus management and accessibility. Furthermore, to align with the existing UI framework, the modal follows DaisyUI conventions. This ensures seamless integration and consistency across the application.

[==insert code snippet of: ConfirmModal.svelte structure==]

### Streamlining Response Management and Button Functionality

In conjunction with the confirmation modal, I enhanced the `QuestionCard.svelte` by implementing a delete confirmation workflow, which triggers asynchronous handling of deletions, complete with error management. This improvement allows for automatic navigation back to the list view once a response is deleted, significantly improving the user interaction flow. To maintain audit trails, a "skipped" response is created instead of performing a hard delete, adhering to the project's versioning system. Additionally, modifications to `FormButton.svelte` now permit custom click handlers, supporting both default form submissions and specialised actions, while retaining backward compatibility. Through this PR, I learned to write code that was not just correct but also easy to delete, ensuring future adaptations can be made effortlessly.

[==insert code snippet of: updated QuestionCard.svelte logic==]
[==insert image of: updated UI with confirm modal for deletion==]
## <a id="ksb-b4"></a>"Optimising Tooltip and Mobile Layout Systems for Enhanced User Experience and Accessibility" [==KSB B4==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/42 ==]
### Streamlining the Tooltip System for Better UX

I was tasked with simplifying a notoriously complex part of the codebase by re-engineering the tooltip system to improve user interaction and accessibility across the application. To achieve this, I implemented a component with smart positioning capabilities that supports eight different positioning options, enhancing the clarity and usability of tooltips. Contextual tooltips were introduced for visual indicators, such as question status, which now provide explanations for both pink (requiring attention) and grey (answered/skipped) states. Additional tooltips clarify the functionalities of features like the visibility toggle for shared responses. To further enhance user experience, a default 300ms show delay was added to prevent tooltips from appearing too abruptly when users hover over interactive elements, reducing unnecessary distractions.

[==insert code snippet of: Tooltip component with smart positioning and contextual explanations==]

### Enhancing Mobile Accessibility and Layout Consistency

In parallel with the tooltip improvements, mobile user experience was meticulously enhanced to ensure a smoother and more intuitive interaction on smaller screens. The mobile handling was refined by using dynamic viewport units, replacing static configurations like `h-screen` with `h-[100dvh]` to accommodate a variety of devices efficiently. Layout adjustments, such as the addition of safe-area insets for devices like iPhones, were made to maintain content within viewable regions. Moreover, footer spacing was optimised to prevent content from bleeding off screen, ensuring that elements like the Terms of Use and Privacy Policy buttons remain accessible and readable. These refinements illustrate the value of building a minimal, reproducible example when addressing layout challenges, providing a clearer path to optimise mobile and responsive design effectively.

[==insert image of: improved mobile layout with responsive footer and dynamic viewport handling==]
## <a id="ksb-b5"></a>"Enhancing Security and Consistency through Custom CORS Middleware and Route Handler Optimisation in a Neo4j Application" [==KSB B5==]
[==PR Link https://github.com/foundersandcoders/LIFT-backend/pull/9 ==]
### Implementing a Custom CORS Middleware for Enhanced Security

An accessibility audit identified several areas for improvement in our UI, prompting us to address security concerns at the system level. In this update, I focused on mapping out and clarifying the existing CORS handling, which was previously underdeveloped. To enhance cross-origin resource sharing security, I developed a custom CORS middleware that dynamically reads allowed origins from environment variables. This implementation ensures that the server only permits requests from explicitly defined frontend origins, thereby fortifying the security framework while maintaining extensibility. 

[==insert code snippet of: custom CORS middleware setting headers based on environment variables==]

### Updating Route Handlers for Consistent Context Usage

I came to appreciate the foresight required to build extensible software as I refined the route handling within our Neo4j-driven application. By updating the route handlers to utilise Oak's context consistently, I ensured standardised response formatting and seamless request processing. Changes in `hub.ts` included reading and writing to the context, specifically modifying the `/newEntry` endpoint to process incoming JSON data and respond appropriately. Additionally, I configured Neo4j to source connection details from environment variables, enhancing the maintainability and configurability of the system.

[==insert code snippet of: updated `/newEntry` endpoint using Oak's context==]
## <a id="ksb-b6"></a>"Implementing Reactive State Management and User Interface Enhancements for Action Status Handling" [==KSB B6==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/29 ==]
### Diagnostic and Solution Deployment

Our monitoring alerts pointed to a recurring, unhandled exception in the status management of workplace accommodation actions, leading to inconsistent displays and user interface issues. The implementation of a comprehensive action management system addressed this critical production issue. This enhancement enables users to toggle action statuses between active and archived, providing clarity and avoiding previous confusion caused by placeholder texts. The key development included the creation of a custom `ActionStatusToggle` component, which manages state reactively and provides text labels for status clarity. An optimistic UI update approach ensures that user experience remains seamless, even if a network failure requires an immediate rollback. Moreover, database functions, such as `updateActionStatus()`, support persistent status updates, while enhanced type safety and error handling improve code reliability.  
[==insert code snippet of: ActionStatusToggle component with text labels and reactive state management==]

### User Interface and Experience Enhancements

Significant user interface improvements were made to bolster usability and accessibility. The list view now prominently features action descriptions, eliminating the generic "ACTION" placeholder, and implements left-aligned text for improved readability of lengthy entries. Each action now represents the most recent version, preventing duplicate entries. Changes to the `ListItem.svelte` component support action-specific styling and status management, while styling updates introduce custom accent colours for toggles to ensure visibility and contrast. These collective updates mitigate prior user experience frustrations and align with accessibility standards. This project honed my skills in debugging complex, multi-threaded race conditions, ensuring the system’s robustness and user satisfaction.  
[==insert image of: enhanced list view with left-aligned action descriptions and toggle functionality==]
## <a id="ksb-b7"></a>"Developing Svelte-Based Component Infrastructure with Tailwind CSS and Code Duplication Mitigation Strategies" [==KSB B7==]
[==PR Link https://github.com/JasonWarrenUK/kannotban/pull/3 ==]
### Establishing Component Infrastructure

The challenge of balancing technical needs with project priorities has resulted in the creation of key components to enhance the efficiency of future developments. This pull request includes the creation of shell components like BoardLayout, Column, TaskCard, TaskForm, and ConfirmDialog. These components serve as the building blocks for further development, adhering to the predefined architectural framework, and are complemented by basic styling using Tailwind CSS. The purpose of this initial setup is to simplify the import and export processes for these components, thereby maintaining a seamless workflow and codebase consistency. These components have been developed in isolated files, conforming to Svelte conventions, ensuring their ease of integration into the broader system.  
[==insert code snippet of: component structure and imports/exports using Svelte conventions==]

### Guarding Against Code Duplication

The development process underscored the importance of idempotent operations by highlighting the risk of code duplication when tasks are completed in parallel. While no architectural changes were deemed necessary at this stage, attention was given to avoid replicating code across separate tickets. This concern is particularly relevant when defining types, as maintaining a uniform type structure across components is crucial to preventing discrepancies. As the author navigated through the creation process, the collaboration with Claude, an AI assistance tool, provided clarity in maintaining stylistic and standardisation consistency across components, aiding in efficient decision-making and reinforcing the integrity of the initial architecture.  
[==insert image of: folder structure with new component files==]
## <a id="ksb-b8"></a>"Implementing JSON-Based Dynamic Email Rendering and Standardising Action Services for Enhanced System Consistency" [==KSB B8==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/21 ==]
### Introducing a Dynamic Email Preview System

This pull request marks the transformation of the email system by implementing a JSON-based rendering approach to generate structured and styled emails. The new system facilitates the inclusion of actions displayed beneath corresponding Q&A pairs, bringing a more interactive and dynamic user experience. The introduction of `EmailData` interfaces enables structured email content generation, while the `generateEmailData()` and `renderEmailToHTML()` functions ensure the conversion of user responses into HTML formatted emails. In terms of design, brand colours are applied throughout, enhancing visual appeal and ensuring consistency with the organisational standards. The email preview component has been updated to incorporate these advancements, transitioning from plain text to styled HTML content, thus significantly improving the user's workflow efficiency.

[==insert code snippet of: JSON-based email generation with conversion functions==]

### Standardising Actions and Enhancing Utility Functions

This update to the codebase removes technical debt by standardising the handling of action services. All actions now consistently convert database responses to `tableMain` types, ensuring smooth operation across functions such as `getUserActions`, `createAction`, and `updateAction`. Additionally, a new `getActionsByResponseId` function adds further robustness with proper versioning logic. Text processing utilities are also enhanced, with improvements like the complete removal of underscores using `replaceAll`, and better display of category names in the email preview. These refinements collectively lead to a cleaner, more predictable codebase, which aids developers in maintaining the system and users in experiencing a seamless service.

[==insert code snippet of: standard type conversion in action services==]
## <a id="ksb-b9"></a>"Streamlining Supabase Configuration and Database Seeding for Enhanced Development Efficiency" [==KSB B9==]
[==PR Link https://github.com/foundersandcoders/LIFT02/pull/2 ==]
### Automating Supabase Configuration and Database Seeding

To efficiently process a large volume of data without impacting user performance, I focused on improving our Supabase local development setup. This entailed migrating the configuration system from `config.toml` files to environment-based files, allowing for improved project management and cleaner environment configurations. This change was necessary to reduce manual errors and enhance the scalability of our configurations, making the setup more adaptable to different environments. By implementing this automated system, the overhead involved in managing configuration complexities was significantly reduced. 
[==insert code snippet of: environment file setup replacing config.toml==]

### Enhanced Data Seeding for Reliable Testing

I aimed to enhance the database seeding process, which is crucial for testing and development, by improving the quality and structure of seed data found in `supabase/data/questions.json`. This effort focused on updating the seeding scripts to ensure reliability across various development environments. By creating a more robust seeding setup, testing accuracy and development efficiency have been optimised, reducing errors and improving data integrity. In this process, I developed a deeper intuition for choosing between relational and non-relational data stores, enhancing data handling strategies in different contexts.
[==insert code snippet of: improved seeding script with enhanced data organisation==]