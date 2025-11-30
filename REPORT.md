# 1. Introduction

The Grocery List Application was extended by introducing a complete DevOps pipeline that automates testing, building, deployment, and monitoring. The main focus was to evolve the application into a cloud-ready, containerized, continuously deployed system supported by automated workflows and observability tools.

To achieve this, the codebase was cleaned and reorganized, automated tests were added, and the entire application was packaged into a Docker container. A continuous deployment pipeline was then set up using GitHub Actions, which builds the container on every update, pushes it to Docker Hub, and automatically deploys it to Azure Web App for Containers. Monitoring tools such as Prometheus and Grafana were also introduced to track performance and system health.


Live deployment:
```
https://sofia-grocerylist-hyccc2e2a5c0e7fb.spaincentral-01.azurewebsites.net
```
---

# 2. Code Quality Improvements & Refactoring

As the local application evolved into a cloud-ready service, improving code quality became essential to support maintainability, testability, and consistent behavior across environments. The codebase was reorganized into clearer, more modular components so that the system would be easier to maintain, test, and deploy through an automated pipeline.

Several code smells were removed during this process. Repeated logic was merged into reusable functions, helping reduce duplication around tasks such as item retrieval, validation, and error handling. API responses were also standardized so that all routes return predictable structures and status codes, which simplified both testing and frontend interaction.

The frontend integration was improved by removing hard-coded local URLs. Instead, the frontend now automatically detects the backend’s base path using `window.location.origin`, allowing the same code to work locally, inside Docker, and on Azure without manual adjustments.

Additional cleanup included removing unused files, fixing imports, and reorganizing folders to better support GitHub Actions, Docker builds, and future extensions. Overall, these refactoring steps made the application more consistent, maintainable, and better suited for automated DevOps workflows.

---

# 3. Testing & Coverage

Preparing the application for automated deployment required establishing a reliable testing strategy. Automated tests ensure that core features behave correctly, prevent regressions, and provide confidence when deploying new versions of the application to the cloud.

To achieve this, a set of unit and integration tests was developed using pytest, validating the functionality of the CRUD operations, data models, and API endpoints. Each test was designed to run independently and without relying on external services, allowing for consistent results in both local and CI environments. Edge cases such as invalid input, missing items, or inconsistent states were also covered to guarantee the robustness of the application under unexpected conditions.

Test coverage was measured using pytest-cov, which provides visibility into which parts of the code are executed during testing. This helped identify areas that required additional test cases and guided improvements to the overall test suite. Coverage reports were generated in both terminal and HTML formats for detailed inspection when needed. The final test coverage achieved was **91.3%**, demonstrating strong reliability across the application's core logic and API endpoints.

Testing was integrated directly into the Continuous Integration (CI) workflow. Whenever a new change is pushed to the main branch or submitted as a pull request, GitHub Actions automatically installs all dependencies, runs the full test suite, and verifies that coverage meets the minimum threshold. If any test fails or coverage falls below the required level, the pipeline stops and deployment does not proceed. This ensures that only verified and stable code reaches the containerization and deployment stages.

By enforcing automated testing at every stage of the development workflow, the project gains long-term reliability and resilience. The combination of unit tests, integration tests, and strict coverage enforcement builds confidence in the application’s stability and ensures that new improvements do not introduce regressions.

---

# 4. Continuous Integration Pipeline (CI)

To support automated deployment and maintain consistent code quality, the project integrates a Continuous Integration workflow using GitHub Actions. The purpose of CI in this system is to ensure that every change introduced to the codebase is tested, validated, and verified before it can progress to the containerization and deployment stages.

The CI pipeline is defined in the `ci.yml` workflow, which runs automatically on every push to the main branch and on every pull request targeting it. The workflow begins by setting up the Python environment and installing all project dependencies. Once the environment is ready, the full test suite is executed, including both unit and integration tests.

A key feature of the CI pipeline is test coverage enforcement, configured using pytest-cov. The workflow checks that coverage stays above the required threshold; if it falls below this level, the pipeline fails immediately. Additionally, the workflow performs a lightweight build validation by running:
```
python -m compileall app
```

This identifies syntax errors early in the process and ensures the codebase remains build-ready.

By integrating these checks into GitHub Actions, the CI workflow creates a fast and reliable feedback loop. Errors, missing tests, or regressions are detected early—before they reach production or trigger a new deployment.

---

# 5. Containerization & Deployment Automation (CD)

To prepare the application for cloud deployment, the entire backend and frontend were packaged into a single Docker container. This ensures that the app behaves consistently across environments and allows Azure to run everything from one image. A custom Dockerfile builds the FastAPI backend, includes the frontend files, installs dependencies, and exposes the application on port 80.

A Continuous Deployment workflow was then created using GitHub Actions. On every push to the main branch, the `azure-cd.yml` workflow builds a new Docker image and publishes it to Docker Hub (`sofiabc004/grocery-app:latest`) using stored GitHub secrets. Azure Web App for Containers automatically pulls the latest image and restarts the service, making deployment fully automated with no manual steps needed.

The main challenge during deployment was Azure pointing to an outdated container registry, which prevented the application from starting. Resetting the container configuration and re-selecting Docker Hub with the correct repository, tag, and port resolved the issue. Once fixed, the pipeline became stable and repeatable.

Overall, combining Docker, GitHub Actions, and Azure created a streamlined path from code changes to production deployment.

---

# 6. Monitoring & Health Checks

To ensure the application remains reliable and transparent during operation, a monitoring and observability layer was added using Prometheus and Grafana. Monitoring provides real-time insights into performance, error rates, and system health.

The application exposes two key endpoints:

- **`/health`** — lightweight availability check  
- **`/metrics`** — Prometheus-formatted metrics generated using `prometheus_fastapi_instrumentator`

Prometheus was configured through `prometheus.yml` and run using Docker Compose. It scrapes the application's `/metrics` endpoint at regular intervals. Once collected, the metrics are stored and can be queried in real time.

Grafana dashboards were then created to visualize key indicators such as total requests, latency percentiles, and status-code distribution. The setup was validated by confirming that Prometheus successfully scraped the API and that Grafana updated metrics in real time.

These tools provide a basic but effective monitoring layer, making it easier to diagnose issues and observe performance trends during development and testing.

---

# 7. Challenges Encountered

The most difficult part of the project was deploying the containerized application to Azure Web App for Containers. Even though the Docker image and CI pipeline were functioning correctly, Azure repeatedly failed to start the container due to leftover configuration from an older deployment. Azure continued pointing to an incorrect registry source, resulting in silent startup failures and the message:

> **"No route registered for '/api/registry/webhook’"**

The issue was resolved only after fully resetting the container settings and reconfiguring Azure to pull from Docker Hub with the correct repository, tag, and port.

Another challenge was ensuring the frontend communicated properly with the deployed backend. The original implementation relied on local URLs, which broke once the app was hosted on Azure. Switching the frontend to use `window.location.origin` made it environment-agnostic and ensured consistent behavior across local and cloud deployments.

These issues highlighted the importance of proper cloud configuration and flexible frontend design when working with automated DevOps pipelines.

---

# 8. Conclusion

This project transformed a simple local application into a fully automated, cloud-deployed service with strong testing, containerization, continuous integration, continuous deployment, and real-time monitoring. Through Docker, GitHub Actions, Azure Web App for Containers, and a Prometheus–Grafana stack, the system now operates reliably and consistently across environments.

The process highlighted the importance of automation, observability, and cloud-ready design, resulting in a more maintainable, scalable, and production-ready application.
