# Portfolio

## KSB Evidence Summary

| KSB ID | Description | Evidence |
|--------|-------------|----------|
| B1 | Works independently and takes responsibility. For example | [View Evidence](#ksb-b1) |
| B4 | Works collaboratively with a wide range of people in differe... | [View Evidence](#ksb-b4) |
| B5 | Acts with integrity with respect to ethical | ❌ No evidence yet |
| B6 | Shows initiative and takes responsibility for solving proble... | [View Evidence](#ksb-b6) |
| B7 | Communicates effectively in a variety of situations to both ... | [View Evidence](#ksb-b7) |
| B8 | Shows curiosity to the business context in which the solutio... | [View Evidence](#ksb-b8) |
| B9 | Committed to continued professional development | [View Evidence](#ksb-b9) |
| K1 | All stages of the software development life-cycle | [View Evidence](#ksb-k1) |
| K10 | Principles and uses of relational and non-relational databas... | [View Evidence](#ksb-k10) |
| K12 | Software testing frameworks and methodologies | [View Evidence](#ksb-k12) |
| K3 | The roles and responsibilities of the project life-cycle wit... | [View Evidence](#ksb-k3) |
| K4 | How best to communicate using the different communication me... | [View Evidence](#ksb-k4) |
| K5 | The similarities and differences between different software ... | [View Evidence](#ksb-k5) |
| K7 | Software design approaches and patterns | [View Evidence](#ksb-k7) |
| K8 | Organisational policies and procedures relating to the tasks... | [View Evidence](#ksb-k8) |
| S13 | Follow testing frameworks and methodologies | [View Evidence](#ksb-s13) |
| S14 | Follow company | [View Evidence](#ksb-s14) |
| S15 | Communicate software solutions and ideas to technical and no... | [View Evidence](#ksb-s15) |
| S17 | Interpret and implement a given design whist remaining compl... | [View Evidence](#ksb-s17) |
| S2 | Develop effective user interfaces | [View Evidence](#ksb-s2) |
| S3 | Link code to data sets | [View Evidence](#ksb-s3) |
| S5 | Conduct a range of test types | [View Evidence](#ksb-s5) |
| S8 | Create simple software designs to effectively communicate un... | [View Evidence](#ksb-s8) |
| S9 | Create analysis artefacts | ❌ No evidence yet |

---

## <a id="ksb-b1"></a>"Optimising Project File Structure and Naming Conventions for Enhanced Developer Experience and Codebase Scalability" [==KSB B1==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/43 ==]
### Optimising File Structure for Performance Improvements

To improve the developer experience and streamline our workflow, I focused on optimising the folder structure and standardising file naming conventions in the project. Initially, I identified that inconsistencies in naming and file organisation were causing build failures and ESLint issues. By renaming UI component files to PascalCase and utility files to camelCase, the code now adheres to React conventions, which ensures consistency across the project. The changes also included updating import paths and modifying the `tsconfig.app.json` to resolve case sensitivity issues. These actions have significantly reduced the cognitive load for developers, allowing for easier navigation and understanding of the codebase.

[==insert code snippet of: PascalCase and camelCase renaming for UI and utility files==]

### Enhancing Codebase Organisation for Scalability 

Another critical aspect was reorganising the folder structure to align with feature-specific architectures. This involved creating dedicated folders for features like help, auth, questions, statements, and progress. UI components were moved to their corresponding feature directories, along with the introduction of `index.ts` barrel files to support cleaner import paths. By removing unutilised barrel files with single exports, I eliminated unnecessary abstraction, simplifying the codebase and improving its scalability. The refactoring efforts directly addressed previous issues and facilitated adherence to a more organised, scalable structure, ultimately contributing to a more efficient development workflow.

[==insert image of: reorganised folder structure with feature-specific directories and barrel files==]

This experience gave me a deeper empathy for junior developers and the importance of good mentorship, emphasising the value of maintaining clear and consistent coding practices in collaborative projects.
## <a id="ksb-b4"></a>Resolving Production Error by Implementing Radix-Utils Polyfill and Replacing Radix UI with Custom React Components [==KSB B4==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/29 ==]
### Immediate Response to Production Error

The primary goal of this pull request was to resolve a critical production incident caused by a missing data validation layer in the deployed environment, resulting in a "Cannot read properties of undefined (reading useLayoutEffect)" error. To address this, I implemented the radix-utils polyfill to ensure that `React.useLayoutEffect` was correctly handled across all Radix UI components, preventing recurring errors. A new comprehensive React polyfill was also added to manage global methods like `createContext` and `useLayoutEffect`, ensuring that the React environment was stable before any code execution. This immediate reaction was crucial to maintaining application stability and preventing further disruptions in deployment environments.

[==insert code snippet of: added radix-utils polyfill and updated index.html with comprehensive React polyfill==]

### Long-Term Solutions and Future Prevention

To hedge against similar incidents in the future, I undertook a thorough refactor to replace Radix UI components with custom React counterparts, thereby removing all Radix UI dependencies. This included developing SimpleDialog, SimpleTooltip, and SimpleLabel components and a compatibility layer to ensure a seamless transition and reduced code changes. The changes improved error handling capabilities while ensuring API compatibility with Radix UI. Furthermore, I initiated a functional tooltip implementation using React context and portals, which adheres to best practices, ensuring both current and future stability of our user interface components. This experience reinforced my understanding of the intricate workings of our dependent open-source libraries.

[==insert code snippet of: removed Radix UI dependencies and created custom components==]

[==insert image of: updated UI with new custom React components replacing Radix UI components==]
## <a id="ksb-b6"></a>"Replacing Radix UI Components with Custom React Alternatives for Simplified Dependency Management" [==KSB B6==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/29 ==]
### Simplifying Component Dependencies

This pull request represents the culmination of a week-long research spike into simplifying the UI components used in the project by addressing the complexities arising from Radix UI dependencies. To reduce complexity and improve the maintainability of the codebase, I have replaced all Radix UI components with simple React-based alternatives. This change primarily involved creating new components like `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel`, which serve as pure React alternatives to their Radix counterparts. A compatibility layer was also developed in `radix-compatibility.tsx` to ensure minimal disruptions in existing code functionality. The package configuration was updated to reflect these changes, removing all Radix UI dependencies from `package.json` and replacing component imports throughout the project to leverage the newly implemented React components.

[==insert code snippet of: creation of SimpleDialog, SimpleTooltip, and compatibility layer==]

### Addressing Deployment Errors

The integration of Radix UI had introduced issues related to React's `useLayoutEffect`, which were particularly problematic in the deployed environment. To resolve these, I added a `radix-utils` polyfill to ensure `React.useLayoutEffect` availability and eliminated the recurring 'Cannot read properties of undefined' error. Further optimisations included introducing a comprehensive React polyfill in `index.html` to handle `createContext` and `useLayoutEffect`. This polyfill provides non-configurable properties and improved error handling to address conflicts and ensure robust functionality. The outcome of these changes has led to a more stable deployment process free from errors related to the utilisation of React global methods.

[==insert code snippet of: implementation of `radix-utils` and polyfill in `index.html`==]
## <a id="ksb-b7"></a>"Implementing a Polyfill to Enhance React Component Compatibility and Stability in Diverse Environments" [==KSB B7==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/21 ==]
### Enhancing Component Compatibility Across Environments

Our monitoring alerts pointed to a recurring, unhandled exception in the deployed environment, notably the 'Cannot read properties of undefined (reading useLayoutEffect)' error. To resolve this, I implemented a crucial code change by adding a `radix-utils` polyfill. This ensures that `React.useLayoutEffect` is consistently available across all environments, preventing further deployment issues tied to this error. By incorporating this polyfill, I removed a significant hurdle for developers working with Radix UI components, enhancing the stability and compatibility of the codebase across diverse deployment scenarios. 

[==insert code snippet of: radix-utils polyfill implementation for useLayoutEffect==]

### Promoting Code Reusability and Clarity

In addition to resolving the specific error, this pull request focused on streamlining the code by importing the polyfill into all Radix UI components. This approach not only fixed the immediate problem but also laid the groundwork for future-proofing the components, making them more reliable for other developers to use in multiple projects. Throughout this process, I learned that a well-placed comment explaining the "why" of a piece of code is invaluable. By documenting the reason behind the implementation, we ensure that future maintainers of the code understand the rationale, thus facilitating effective communication, especially in varied technical discussions.

[==insert code snippet of: polyfill import into Radix UI components==]
## <a id="ksb-b8"></a>"Automating Microservices Compatibility with React Polyfills and Native Component Integration" [==KSB B8==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/28 ==]
### Automating Error Handling and Component Compatibility

This task involved orchestrating a delicate dance between multiple microservices primarily by addressing compatibility and error handling issues in the deployment environment. The pull request introduced a series of polyfills tailored to automate the resolution of 'useLayoutEffect' and 'createContext' errors, which were pervasive in the deployment environment. By incorporating the radix-utils polyfill and a comprehensive React shim, I ensured that critical React methods such as `useLayoutEffect` and `createContext` function seamlessly, hiding underlying complexities from the development team. This approach appreciably streamlined the error handling process, saving valuable time during deployment.

[==insert code snippet of: react-shim.ts implementing polyfills for global React methods==]

### Shifting from Radix UI Components to Native React Alternatives

In pursuit of a more efficient and less error-prone interface, I identified the repetitive challenges associated with Radix UI components and devised native React-based alternatives. Through the development of simple components like `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel`, I established a compatibility layer that minimizes code alterations but significantly enhances flexibility. These modifications are a strategic move towards phasing out Radix UI dependencies, resulting in improved component performance and reduced deployment issues.

[==insert code snippet of: compatibility layer in radix-compatibility.tsx==]
## <a id="ksb-b9"></a>"Adapting Codebase for External API Changes by Implementing a Polyfill and React Alternates to Enhance Stability" [==KSB B9==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/26 ==]
### Rethinking the Integration Strategy due to External API Changes

Faced with a critical alteration in an external API's contract, our team undertook a comprehensive refactoring of the codebase to adapt to these changes effectively. One significant move was the incorporation of a `radix-utils` polyfill to prevent a 'Cannot read properties of undefined (reading useLayoutEffect)' error that arose in the deployed environment. This modification ensured the availability of `React.useLayoutEffect` across Radix UI components, forestalling application breakdowns in production. Additionally, I replaced all `@radix-ui` components with simple React mockups temporarily, aiming to isolate and identify the error's origin. After pinpointing the issue, I reverted the mock components to their original Radix UI components, ensuring minimal disruption to the existing codebase.

[==insert code snippet of: radix-utils polyfill implementation==]

### Navigating Ambiguity with a Newly Mapped Code Landscape

Successfully mapping out a clearer interpretation of the system's unexplored complexities, I introduced simple React-based alternatives to Radix UI components, including `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel`. These additions, coupled with a compatibility layer in `radix-compatibility.tsx`, offered a forward-looking approach to lessen reliance on Radix UI. This effort represents a proactive first step towards complete independence from external UI dependencies, enhancing system stability and clarity for future developers. Notably, this endeavour addressed the significant challenge of navigating through the initial ambiguity in specifications, ultimately culminating in a more robust and comprehensible code structure.

[==insert code snippet of: compatibility layer in radix-compatibility.tsx==]
## <a id="ksb-k1"></a>"Development of a Mobile-First Interface with Enhanced Usability and Asynchronous Integration" [==KSB K1==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/40 ==]
### Designing a New User Experience for Mobile Interfaces

The challenge lay in retrofitting a modern design and security standard into a legacy mobile interface. In this endeavour, I undertook the design and implementation of a mobile-friendly interface, which involved multiple style adjustments and feature enhancements. Key design decisions included adding a 'driver tour' feature to aid in user navigation and employing conditional rendering for the FilterBar on smaller displays to enhance usability across varying screen sizes. Additionally, dynamic size and transition adjustments were integrated for editing user and manager information, ensuring an intuitive and responsive design. Tailwind’s utilities were expanded to include an extra-small (xs) screen size, optimising the interface for smaller devices. This experience allowed me to deep-dive into user-centric design principles and adaptive UI components, solidifying my understanding of mobile-first development methodologies.  
[==insert code snippet of: dynamic size adjustment for user and manager information on mobile interfaces==]  
[==insert image of: updated mobile interface with enhanced navigation features==]

### Implementing Core Asynchronous Features and API Adjustments

Simultaneously, I redesigned and refactored underlying components to incorporate asynchronous programming, a core necessity for a seamless user experience. Updates to the Action interface and gratitude API were necessary for cohesive integration, ensuring data consistency and real-time updates. These changes presented trade-offs in complexity and performance, ultimately contributing to a more robust and responsive application architecture. Furthermore, I incorporated a welcome panel that dynamically retrieves text from a JSON file, enhancing flexibility and simplifying content management. This project reinforced my competencies in core asynchronous programming concepts, proving invaluable in creating fluid, interactive applications.  
[==insert code snippet of: Action interface update and gratitude API adjustment==]  
[==insert image of: implementation of asynchronous welcome panel==]
## <a id="ksb-k10"></a>"Resolving Deployment Issues by Replacing Radix UI with React Alternatives and Introducing Compatibility Shims" [==KSB K10==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/26 ==]
### Diagnosing the Persistent Bug

This pull request encompasses a crucial update aimed at addressing a subtle, persistent bug encountered during the deployment process. The issue was traced back to the use of `useLayoutEffect` in Radix UI components, which caused an error when deployed in certain environments. A comprehensive diagnostic approach was undertaken, temporarily replacing all `@radix-ui` components with simple React mock-ups to isolate the error source. This debugging strategy proved effective in narrowing down the problematic components, allowing for a targeted fix. The reliance on Radix UI was a major hurdle, indicating the importance of well-defined data contracts in microservices architecture to ensure seamless integration and deployment processes.

[==insert code snippet of: diagnostic commit replacing Radix UI components with React mock-ups==]

### Implementing a Long-Term Solution

To resolve the identified issue, a robust React shim was introduced to polyfill the `useLayoutEffect` and `createContext` methods, providing necessary compatibility in environments where these features were undefined. The solution involved modifying the `vite.config.ts` to incorporate `radix-utils` instead of `react-polyfill`, optimising the application's dependency management. Additionally, pure React alternatives to Radix UI components were developed, including `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel`, establishing a long-term strategy to potentially eliminate dependency on Radix UI altogether. This optimisation not only fixed the deployment issue but also simplified the onboarding process for new developers by standardising component usage and promoting a unified coding practice across the team.

[==insert code snippet of: React shim for useLayoutEffect and createContext==]
## <a id="ksb-k12"></a>"Optimising Asynchronous Testing and User Interface Enhancements for Improved Scalability and User Experience" [==KSB K12==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/6 ==]
### Enhancing the User Interface and Testing Capabilities

A key architectural decision we faced was how to handle asynchronous operations effectively within our testing framework, particularly with Cypress. This pull request reflects significant enhancements to both the user interface and the testing environment, aiming at unlocking future capabilities. Notably, the renaming of 'statements' to 'entries' indicates a shift towards clearer, more intuitive naming conventions, setting the stage for future scalability. Additionally, the enhancement of the Cypress configuration to support WSL2 through retry logic and browser options reflects a proactive approach to ensuring smooth async testing operations. This not only optimises existing processes but also enriches our testing toolkit for future needs.

[==insert code snippet of: renaming statements to entries in the code==]

### Implementing UI Innovations for a Cohesive User Experience

The user interface underwent several improvements beyond immediate project requirements, anticipating future user interaction needs. The reinstatement of the 'add statement' button and the introduction of the SentimentVerbPicker component are critical enhancements intended to add depth to the user experience. These additions, along with the implementation of a StepContainer intermediate component, support a more modular and flexible design ethos. The updated styling, where 'Next' and 'Continue' buttons now appear consistently, reflects attention to detail aimed at a more cohesive UI.

[==insert image of: consistent styling of Next and Continue buttons==]

Ultimately, this work was about more than just code; it was about improving the way our team collaborates by building a foundation for future developments and cohesive communication across components.
## <a id="ksb-k14"></a>"Creating a Reusable Component for Compliant Employer Data Fetching with Deno Configurations and Enhanced Testing" [==KSB K14==]
[==PR Link https://github.com/foundersandcoders/LIFT-frontend/pull/4 ==]
### Implementing a Reusable Component for Employer Data Fetching

The driving motivation behind this pull request was to comply with a new data privacy regulation by creating a reusable component that fetches employer names for the Dashboard. This change was pivotal in ensuring that the Employers Dashboard could seamlessly comply with the updated regulations, while also serving as a model for similar future needs across multiple projects. The code changes involved adding specific Deno configurations for both development and production environments, which facilitated the proper testing of the Cross-Origin Resource Sharing (CORS) settings on the deployed version. This was crucial for validating the secure and efficient cross-domain data requests. 

[==insert code snippet of: the configuration setup for Deno in development and production==]

### Enhancing Test Coverage for Data Submission

In addition to implementing the fetching mechanism, this pull request introduced a testing function aimed at evaluating data submission processes on the Employers component. By implementing this test, I was able to demystify the dependency injection framework used in our setup, providing valuable insights that optimised the workflow. The test feature was specifically designed to simulate data posting to the server, ensuring robustness and reliability when handling real-world usage scenarios. This step not only enhanced the component's effectiveness but also laid groundwork for integrating similar features into other parts of the application, thus broadening its utility as a reusable module.

[==insert code snippet of: test function for data posting on the Employers component==]
## <a id="ksb-k3"></a>"Enhancing Application Security and Flexibility through Custom CORS Middleware and Refined Route Handling" [==KSB K3==]
[==PR Link https://github.com/foundersandcoders/LIFT-backend/pull/9 ==]
### Pruning and Optimising for Future Growth

This change laid the groundwork for a more significant feature to come by addressing technical debt and updating the existing codebase for better adaptability. The introduction of a custom CORS middleware was a pivotal step in enhancing security and flexibility. By allowing the application to dynamically set the "Access-Control-Allow-Origin" header from environment variables, the middleware prevents unauthorised cross-origin requests and paves the way for smooth integration with future frontend services. This ensures that as new features are implemented, they will be built on a secure and adaptable foundation. 

[==insert code snippet of: custom CORS middleware setup in the application==]

### Refined Route Handling and Secure Configuration

The update further involved refining route handlers to utilise Oak's context management for more effective response setting. This systematic prune of existing code means cleaner, streamlined handling of HTTP requests—demonstrated by the revised `/newEntry` endpoint, which now processes requests more robustly by adopting structured validation and response logic. Additionally, the neo4j configuration was updated to secure connection details through environment variables, reducing security risks and enhancing the maintainability of database interactions. This task highlighted the importance of considering internationalisation and localisation from the start by ensuring the codebase remains flexible and secure for diverse deployment environments.

[==insert code snippet of: updated /newEntry route handler in the application==]
## <a id="ksb-k4"></a>"Optimising Mobile UI and Code Structuring with Enhanced Documentation" [==KSB K4==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/11 ==]
### Enhancing Mobile User Experience and Documentation

The performance of the search feature had degraded over time, and I was asked to investigate its impacts on the mobile interface. Initially, the code supporting the mobile design was complex and not fully optimised for narrow screens. To improve the user experience, I introduced several styling enhancements, such as smart content hiding for narrower screens, which involved adjusting the colours and making the header responsive to mobile devices. Media queries were also utilised to ensure that the `editStatement` feature adjusts seamlessly for mobile users. These changes resulted in a refined and more accessible interface for mobile users. 

[==insert image of: updated mobile interface with smart content hiding and responsive header==]

### Improving Code Structure and Documentation

The project also necessitated code refactoring for better maintainability, which involved reorganising the file structure. Files were systematically arranged to facilitate easier navigation and understanding for current and future developers. Alongside these structural improvements, I documented the use of `Magic_Link` authentication. This inclusion serves as an important guide, enhancing onboarding for new team members and maintaining consistency in authentication practices. The documentation clearly outlines the setup and usage of `Magic_Link`, reflecting a more structured approach to error handling and code documentation.

[==insert code snippet of: reorganised file structure with new paths==]  
[==insert code snippet of: Magic_Link documentation demonstrating setup and usage==]

This project taught me to be more deliberate in my approach to error handling, ensuring robust and scalable solutions.
## <a id="ksb-k5"></a>"Enhancing Application Stability and Error Management through Comprehensive Data Validation and React Component Refactoring" [==KSB K5==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/33 ==]
### Strengthening Application Stability with Enhanced Data Validation

The goal was to eliminate a whole class of bugs by introducing a stricter data validation layer. Recognising potential risks associated with the incomplete implementation of React functions, I implemented a comprehensive Radix polyfill to enhance application stability. This corrective measure was driven by the frequent occurrence of errors like 'Cannot read properties of undefined' when deploying React useLayoutEffect in a live environment. To mitigate this, I added a detailed polyfill script in `index.html` ensuring essential React global methods, such as createContext and useLayoutEffect, were fully operational. This foundational change is vital for preventing deployment failures that were previously common, thereby safeguarding the system's reliability.

[==insert code snippet of: comprehensive React polyfill added to index.html==]

### Reinforcing Error Handling through Component Refactoring

This project taught me to be more deliberate in my approach to error handling. To address the operational issues posed by the existing Radix UI components, I developed a set of simple React-based alternatives. These included creating SimpleDialog, SimpleTooltip, and SimpleLabel components to replace Radix's counterparts, thereby nullifying the original dependencies. A compatibility layer was also introduced, enabling seamless integration with the existing codebase. This strategic move not only resolved the useLayoutEffect and createContext errors but also represented a pivotal step towards completely removing the Radix UI dependency. Enhancing TypeScript type handling for the global React object further strengthened the application’s resilience against type-related errors, demonstrating a proactive approach to system protection.

[==insert code snippet of: simple React-based alternatives for Radix UI components==]

[==insert code snippet of: TypeScript type handling improvement for global React object==]
## <a id="ksb-k7"></a>"Developing a React Polyfill and Transitioning from Radix UI to Enhance Application Stability" [==KSB K7==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/33 ==]
### Implementing a Comprehensive React Polyfill for Stability

The path to a more scalable architecture began with a single observation: persistent errors related to `useLayoutEffect` and `createContext` in a deployed environment. To address this, I implemented a comprehensive React polyfill, ensuring these functions were consistently available. Initially, errors were traced by temporarily replacing `@radix-ui` components with simple React mockups to diagnose which component triggered issues. Post-identification, a more robust `react-shim.ts` was introduced, enhancing TypeScript type handling for the global React object. These modifications significantly reduced deployment error rates, promoting application stability.

[==insert code snippet of: implementing React polyfill in react-shim.ts==]

### Transition from Radix UI to Pure React Components

Addressing the root cause of `useLayoutEffect` errors necessitated a transition away from Radix UI components towards pure React alternatives. I created straightforward replacements for several UI components such as Dialog, Tooltip, Dropdown, and Label, complete with a compatibility layer to minimise code alterations. This strategic shift not only eradicated proprietary Radix dependencies but also safeguarded the application against recurring React-related errors. As a key takeaway, there was a delicate balance between perfection and shipping; the implementation underscored the importance of adaptability in design approaches to uphold system reliability.

[==insert code snippet of: creating simple React-based components and compatibility layer==]
## <a id="ksb-k8"></a>"Transitioning Radix UI Elements to Native React Components for Enhanced Deployment Stability and User Experience" [==KSB K8==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/35 ==]
### Transitioning from Radix UI to Native React Components

The final piece of the puzzle was to address critical deployment issues due to `useLayoutEffect` errors in the deployed environment. Initially, I added a `radix-utils` polyfill to ensure that `React.useLayoutEffect` was available in all necessary environments, as part of an effort to stabilise the deployment. This involved updating the `vite.config.ts` to utilise this new polyfill. Additionally, I created a `react-shim.ts` file to handle other potential React global method issues, aiming to ensure comprehensive support in the deployment context. The polyfill was included in the `index.html` through a script tag to guarantee its execution prior to any React code. As a diagnostic step, I temporarily replaced all Radix UI components with simple React mockups to locate the error, which eventually allowed me to safely revert to the original Radix components after enhancements.

[==insert code snippet of: addition of radix-utils polyfill==]

### Developing Pure React Components and Enhancing UX

I realised the power of a well-defined data contract in a microservices architecture as I proceeded to completely mitigate the Radix UI dependency by developing pure React alternatives. This included creating components like `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel`, along with a compatibility layer to facilitate easy swapping without extensive code modifications. These new components were integrated into the application's primary UI parts, such as the `UserDataModal` and main `App` components. To improve overall usability, I introduced functional tooltips with proper positioning, using React context and portals for optimal results. Enhancements to the user experience, such as implementing auto-scroll and making modals dismissible by clicking outside, significantly refined the application interaction patterns.

[==insert image of: the refined user's data modal for mobile after UI changes==]
## <a id="ksb-s13"></a>"Optimising UI Frameworks by Replacing Radix UI Components with React Solutions" [==KSB S13==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/32 ==]
### Automating Error Resolution in UI Framework Conversion

To accommodate a predicted 10x increase in traffic, I initiated a project focused on replacing Radix UI components with native React solutions to improve system stability and error handling. The primary focus was on resolving the recurring `useLayoutEffect` and `createContext` errors that arose during deployment of Radix UI components. This involved the creation and implementation of a `radix-utils` polyfill, integrated into the `vite.config.ts` and all relevant component files, to ensure compatibility and address these errors. Through comprehensive diagnostic testing and temporary mockups of components, I identified the root cause of these errors, leading to the development of a robust React polyfill solution. This polyfill, incorporated as a script in `index.html`, was designed to address dependency injections smoothly, safeguarding against deployment issues. 
[==insert code snippet of: integrating radix-utils polyfill in vite.config.ts==]

### Streamlining UI Component Functionality with Simplified React Alternatives

The second phase of this endeavour involved the full transition from Radix UI to React-based alternatives. By developing custom components such as `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel`, I crafted a compatibility layer in `radix-compatibility.tsx` to streamline the transition while minimising disruptions to existing code. This effort not only involved refactoring imports and removing redundant Radix components but also enhancing the system's functionality with features such as auto-scroll upon category changes. The project not only optimised our UI framework but also demystified the inner workings of React's dependency system, significantly aiding future development initiatives. 
[==insert image of: updated UI with React-based alternatives for Radix components==]
## <a id="ksb-s14"></a>"Refactoring User Interface Elements and Reducing Technical Debt in Codebase" [==KSB S14==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/2 ==]
### Pruning and Optimising Interface Elements

This work was born out of a team-wide discussion about improving code quality and centres around refactoring and optimising the user interface elements related to tracking question progress. Significant attention was given to styling the components that reflect the number of questions answered versus the total questions available, adding an element of gamification to enhance user engagement. The new design aims to provide immediate visual feedback, thereby enriching the user experience. This improvement follows best practices for user interface design while ensuring clarity and interaction efficiency for users. 
[==insert image of: styled progress components showing questions answered vs total questions==]

### Eliminating Redundancies and Addressing Technical Debt

A crucial part of this pull request involved addressing technical debt to improve the codebase's health. This included fixing TypeScript errors in the old wizard and statement builder, which were essential to maintain code integrity and prevent future compilation issues. Additionally, redundant code and icons that were no longer in use were successfully removed to minimise clutter and confusion for developers. These changes reflect a concerted effort to clean up the codebase and enhance its maintainability. This project helped me understand the true cost of technical debt, highlighting the importance of routine maintenance and strategic refactoring for the long-term success of software projects.
[==insert code snippet of: removal of unused code icons and TypeScript error fixes==]
## <a id="ksb-s15"></a>"Optimising React Application Performance through Polyfills and Component Simplification" [==KSB S15==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/29 ==]
### Addressing Performance Bottlenecks through Polyfills and Component Refactoring

A persistent performance bottleneck related to the `useLayoutEffect` error was affecting the deployment environment of the application. The issue stemmed from React components' reliance on certain Radix UI elements, leading to compatibility and maintainability challenges. Initially, a diagnostic polyfill was implemented in `index.html` to ensure `useLayoutEffect` and `createContext` methods were correctly defined before any React code executed. This intervention included introducing a comprehensive React shim, refining the configuration in `vite.config.ts` to switch from `react-polyfill` to `radix-utils`, and perfecting TypeScript type handling for global React objects. The refined approach led to successful deployment without errors. 

[==insert code snippet of: updated vite.config.ts to use radix-utils instead of react-polyfill==]

### Transition towards Simplified Components

Faced with persistent issues linked to Radix UI dependencies, an alternative solution was critically examined: transitioning to simpler React-based components. New components such as `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel` were developed to serve as drop-in replacements while maintaining minimal reconfiguration requirements. This transition aimed to address the inherent polyfill challenges and reinforce the codebase's maintainability and readability. With Radix components entirely phased out, a compatibility layer was utilised to streamline this transition. Ultimately, this effort not only resolved the immediate performance bottleneck but also underscored the importance of clear, maintainable code in software solutions.

[==insert code snippet of: created SimpleDialog, SimpleTooltip, and SimpleLabel components==]
## <a id="ksb-s17"></a>"Addressing Legacy System Dependencies by Replacing Radix UI with React-Based Solutions" [==KSB S17==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/34 ==]
### Transitioning from Legacy Dependencies

The journey to deprecating a legacy system began with this first, crucial step of addressing the intermittent useLayoutEffect error. I tackled this issue by introducing a comprehensive polyfill that provided necessary React functionalities such as `createContext` and `useLayoutEffect`. This inclusion ensured compatibility and resolved errors occurring in the deployed environment by incorporating the polyfill within `index.html` as a script tag, maintaining its execution prior to any React code. Additionally, mock versions of Radix UI components were employed temporarily to pinpoint the exact components causing the error, eventually leading to the integration of simple React components as an alternative to Radix UI components. This step marked significant progress toward removing the Radix UI dependency altogether and alleviated existing deployment errors. 

[==insert code snippet of: comprehensive React polyfill implementation==]

### Innovating with Alternative Solutions

To circumvent the limitations imposed by the Radix UI components, new, simple React-based components such as `SimpleDialog`, `SimpleTooltip`, and `SimpleLabel` were developed. These components served as efficient replacements while maintaining API compatibility. Furthermore, improvements included enhanced tooltip functionality using React context and portals, providing proper hover actions and positioning capabilities. This strategic transition not only resolved the ongoing bugs but also laid the groundwork for a future without the Radix UI dependency. Throughout this process, I came to appreciate the foresight required to build extensible software, understanding how incremental steps facilitate meaningful transformations in systems architecture.

[==insert image of: simplified React-based UI components integrated into the application==]
## <a id="ksb-s2"></a>"Transition to Custom React UI Components with Error-Resistant Deployment Solutions" [==KSB S2==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/32 ==]
### Transition from Radix UI to Simpler React Components

The project began with a deceptively simple goal: to transition the UI components from Radix UI to custom React-based solutions while maintaining ongoing feature enhancements and ensuring a smooth deployment process. This involved developing alternatives such as SimpleDialog, SimpleTooltip, and SimpleLabel, which are pure React components. A compatibility layer, `radix-compatibility.tsx`, was introduced to streamline code changes, ensuring existing functionalities remained intact without heavy refactoring. This strategic shift from Radix UI was motivated by recurring errors associated with `useLayoutEffect` and `createContext`, prompting the need for bespoke solutions that would not only resolve these issues but also facilitate future component enhancements. 

[==insert code snippet of: creation of SimpleDialog, SimpleTooltip, and SimpleLabel components as React alternatives==]

### Ensuring a Seamless Technical Migration with Error Resolution

The transition involved addressing technical challenges that arose in the deployed environment, primarily errors related to React's `useLayoutEffect` and `createContext`. To prevent these, a comprehensive React polyfill was implemented, which included a robust `react-shim.ts` to ensure the availability of necessary global methods across all environments. This polyfill was optimised to handle property settings safely and reduce conflicts, thereby preventing deployment errors historically encountered. Through this process, there was an enhancement in error handling mechanisms, allowing for smoother deployments and thereby achieving the perfect balance between migrating technologies and delivering functional updates without compromising the integrity of the application.

[==insert code snippet of: react-shim.ts implementation to fix useLayoutEffect and createContext errors==]

Ultimately, the work facilitated a practical understanding of how cryptographic signing works through the strategic solutions deployed to stabilise UI functionality amidst migratory efforts.
## <a id="ksb-s3"></a>"Streamlining Deployment with Radix-Utils and Comprehensive Compatibility Testing in Legacy System Transition" [==KSB S3==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/24 ==]
### Balancing Modernisation and Functionality in Deployment

The journey to deprecating a legacy system began with this first crucial step: addressing deployment issues linked to outdated polyfills and component requirements. In navigating conflicting technical requirements, I integrated a `radix-utils` polyfill and ensured its importation across all Radix UI components to rectify the `useLayoutEffect` error encountered within the deployed environment. Moreover, the update of `vite.config.ts` to utilise the `radix-utils` instead of an earlier `react-polyfill` demonstrates a decisive move towards a streamlined configuration. These changes are indicative of a meticulous approach to handling differing technical opinions regarding which approach best suited the deployment needs.

[==insert code snippet of: radix-utils polyfill import to rectify useLayoutEffect error==]

### Identifying and Resolving Underlying Compatibility Concerns

In a fascinating deep dive into a part of the web platform I hadn't explored before, I conducted a series of diagnostic test commits. This involved temporarily replacing all @radix-ui components with simple React mock-ups to trace the root cause of the error. Additionally, I included a comprehensive React polyfill to address broader issues of `createContext` and `useLayoutEffect`, scripting it into `index.html` to run prior to any React code execution. This diagnostic process was pivotal in reconciling diverse stakeholder opinions and ensuring consistent component behaviour in the final deployment setup.

[==insert code snippet of: diagnostic test process with React mockups==]
## <a id="ksb-s5"></a>"Optimising Memory and Deployment Efficiency Through Polyfill Integration and Component Refactoring" [==KSB S5==]
[==PR Link https://github.com/foundersandcoders/lift-frontend-v2/pull/33 ==]
### Reducing Memory Footprint with Enhanced Polyfills and Component Refactoring

In the pursuit of optimising the memory usage of our main data processing service, a comprehensive update was made to our front-end dependencies and their configurations. A significant change included the introduction of a radix-utils polyfill, aimed at preventing errors related to React's `useLayoutEffect` in a deployed environment. This was executed by integrating a comprehensive React polyfill, which solves issues involving `createContext` and other global methods, ensuring React's components function correctly when deployed. The import of this polyfill across all Radix UI component files ensures consistency and mitigates the occurrence of undefined properties errors during execution. In parallel, simple React alternatives like `SimpleDialog` and `SimpleTooltip` were developed, effectively phasing out the Radix UI dependency that previously caused several execution errors. This strategic removal of Radix UI dependencies from the `package.json` file is a move towards a more streamlined and error-resilient deployment process. 

[==insert code snippet of: comprehensive React polyfill integration==]

### Strengthening Code Quality and Deploy Stability

In a broader scope of maintaining code quality and enhancing deploy stability, the pull request introduces improvements to the continuous integration and continuous deployment (CI/CD) pipeline. Diagnostic tests identified and temporary mockups of Radix UI components were implemented to track down the specific sources of the `useLayoutEffect` error. Beyond error resolution, the introduction of functional tooltips with accurate hovering features and enhanced positioning capabilities serves as an addition to elevate user interaction quality. GitHub Actions scripts were fine-tuned to reinstate the creation of the `.env.development` from Deno secrets, optimising environment management in the deployment pipeline. Overall, these efforts underscore the crucial role of structured logging for improved observability, ensuring that any issues encountered during deployment are quickly identified and addressed.

[==insert image of: updated tooltip with enhanced positioning==]
## <a id="ksb-s8"></a>"Automating and Documenting Dropdown Features for Improved User Interface Interactions" [==KSB S8==]
[==PR Link https://github.com/foundersandcoders/LIFT-frontend/pull/3 ==]
### Automating User Interaction with Dropdowns

This work laid the foundation for a more interactive and dynamic user experience by introducing automated dropdown components into the software. The primary task focused on creating a dropdown feature that was both simple and effective, leveraging native dropdown functionality to enhance user selection processes. The implementation began with transforming existing data into descriptors and constructing a component for autocomplete functionality. Subsequently, a singular, cohesive dropdown component was developed to streamline this interaction. Simplifying the dropdown element was a priority to ensure efficiency and user-friendly design, alongside incorporating placeholders to improve accessibility for users.

[==insert code snippet of: simplified dropdown component implementation==]

### Enhancing Component Structure and Documentation

In parallel, significant efforts were directed towards building a structured and comprehensible design framework for these new components. Documentation, such as the `reactModStructure.md` file, was updated to provide clear guidance and understanding of the program's new dropdown elements. This task taught me the value of building a minimal, reproducible example when reporting a bug, as it highlighted potential issues early in the design process. Documenting the structure and behaviour of the dropdown elements within the codebase was essential for future development and debugging tasks, thereby reducing manual effort and mitigating potential errors.

[==insert image of: improved dropdown user interface with placeholders for accessibility==]