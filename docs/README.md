# PRIME Public Health Data Infrastructure

- [PRIME Public Health Data Infrastructure](#prime-public-health-data-infrastructure)
  - [Overview](#overview)
    - [Problem Scope](#problem-scope)
    - [Target Users](#target-users)
  - [Technical](#technical)
    - [Getting Started](#getting-started)
    - [Decision Records](#decision-records)
  - [Standard Notices](#standard-notices)
    - [Public Domain Standard Notice](#public-domain-standard-notice)
    - [License Standard Notice](#license-standard-notice)
    - [Privacy Standard Notice](#privacy-standard-notice)
    - [Contributing Standard Notice](#contributing-standard-notice)
    - [Records Management Standard Notice](#records-management-standard-notice)
    - [Related documents](#related-documents)
    - [Additional Standard Notices](#additional-standard-notices)

**General disclaimer** This repository was created for use by CDC programs to collaborate on public health related projects in support of the [CDC mission](https://www.cdc.gov/about/organization/mission.htm). GitHub is not hosted by the CDC, but is a third party website used by CDC and its partners to share information and collaborate on software. CDC use of GitHub does not imply an endorsement of any one particular service, product, or enterprise.

## Overview

The PRIME Public Health Data Infrastructure projects are part of the Pandemic-Ready Interoperability Modernization Effort, a multi-year collaboration between CDC and the U.S. Digital Service (USDS) to strengthen data quality and information technology systems in state and local health departments.

This repository represents the source code for three related workstreams in this area:

- **Data Storage, Tooling, and Preparation (DSTP)** - Assist STLTs in implementing modern infrastructure that is flexible enough to allow jurisdictions to prepare for as-of-yet unknown use cases, while providing a long-term storage mechanism and query solution for effective daily use and timely response.
- **Common Data Model** - Define USCDI+ for Public Health and implementation guidance that specifies common data elements, value sets, and APIs to enable interoperability, data cleaning, and data linkage across the ecosystem of public health data senders and receivers
- **Workbench** - Develop a platform for high quality tools, services, analytical products, and reporting that addresses identified pain points for data receivers/public health departments, and incentivizes adoption of the Common Data Model

All three projects will begin with a time-limited prototype, focused on working with raw ELR, eCR, and VXU data from the commonwealth of Virginia Department of Health, for the purpose of experimenting with a unified data lake paradigm. Over time they will evolve to tackle new STLTs and new challenges around data quality and standardization.

The PRIME Public Health Data Infrastructure prototype a sibling project to [PRIME ReportStream](https://reportstream.cdc.gov), focusing on delivering COVID-19 test data to public health departments, and [PRIME SimpleReport](https://simplereport.gov), working on a better way to report COVID-19 rapid tests.

### Problem Scope

Long-term Vision for all three workstreams: Public health systems to digest, analyze, and respond to data are siloed. Lacking access to actionable data, our national, as well as state, local, and territorial infrastructure, isn’t pandemic-ready. Our objective was to learn how the CDC can best support STLTs in moving towards a modern public health data infrastructure.

Vision for short-term prototype: The Commonwealth of Virginia Department of Public Health would like to move towards a more ‘holistic’ solution for electronic data processing and integration, so that currently siloed datasets can be processed and ultimately used in a more efficient and effective manner. Specifically, in order to support the vision of ‘holistic processing’, this prototype is focusing the on seeing what can be done with raw data, focused on COVID-19 breakthrough cases.

### Target Users

Eventual target users of this system include:

- Public Health Departments
  - Epidemiologists who rely on health data to take regular actions
  - Senior stakeholders who make executive decisions using aggregate health data
  - IT teams who have to support epidemiologists and external stakeholders integrating with the PHD
  - PHDs may include state, county, city, and tribal organizations

## Technical

### Getting Started

To start development against this project, please consult the [Getting Started](getting_started.md) doc for more details on setting up local development environments, deployments, and more.

### Decision Records

See A record of all decisions that have been made on the project and propose your own by going to the [decisions](decisions) directory and following instructions there.

## Standard Notices

### Public Domain Standard Notice

This repository constitutes a work of the United States Government and is not
subject to domestic copyright protection under 17 USC § 105. This repository is in
the public domain within the United States, and copyright and related rights in
the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this repository will be released under the CC0 dedication. By
submitting a pull request you are agreeing to comply with this waiver of
copyright interest.

### License Standard Notice

This project is in the public domain within the United States, and copyright and
related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
All contributions to this project will be released under the CC0 dedication. By
submitting a pull request or issue, you are agreeing to comply with this waiver
of copyright interest and acknowledge that you have no expectation of payment,
unless pursuant to an existing contract or agreement.

### Privacy Standard Notice

This repository contains only non-sensitive, publicly available data and
information. All material and community participation is covered by the
[Disclaimer](https://github.com/CDCgov/template/blob/master/DISCLAIMER.md)
and [Code of Conduct](https://github.com/CDCgov/template/blob/master/code-of-conduct.md).
For more information about CDC's privacy policy, please visit [http://www.cdc.gov/other/privacy.html](https://www.cdc.gov/other/privacy.html).

### Contributing Standard Notice

Anyone is encouraged to contribute to the repository by [forking](https://help.github.com/articles/fork-a-repo)
and submitting a pull request. (If you are new to GitHub, you might start with a
[basic tutorial](https://help.github.com/articles/set-up-git).) By contributing
to this project, you grant a world-wide, royalty-free, perpetual, irrevocable,
non-exclusive, transferable license to all users under the terms of the
[Apache Software License v2](http://www.apache.org/licenses/LICENSE-2.0.html) or
later.

All comments, messages, pull requests, and other submissions received through
CDC including this GitHub page may be subject to applicable federal law, including but not limited to the Federal Records Act, and may be archived. Learn more at [http://www.cdc.gov/other/privacy.html](http://www.cdc.gov/other/privacy.html).

### Records Management Standard Notice

This repository is not a source of government records, but is a copy to increase
collaboration and collaborative potential. All government records will be
published through the [CDC web site](http://www.cdc.gov).

### Related documents

- [Open Practices](open_practices.md)
- [Rules of Behavior](rules_of_behavior.md)
- [Thanks and Acknowledgements](thanks.md)
- [Disclaimer](DISCLAIMER.md)
- [Contribution Notice](CONTRIBUTING.md)
- [Code of Conduct](code-of-conduct.md)

### Additional Standard Notices

Please refer to [CDC's Template Repository](https://github.com/CDCgov/template)
for more information about [contributing to this repository](https://github.com/CDCgov/template/blob/master/CONTRIBUTING.md),
[public domain notices and disclaimers](https://github.com/CDCgov/template/blob/master/DISCLAIMER.md),
and [code of conduct](https://github.com/CDCgov/template/blob/master/code-of-conduct.md).
