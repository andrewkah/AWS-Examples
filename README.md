# AWS-Examples

This repository provides practical examples and starter scripts for working with **Amazon Web Services (AWS)**.  
It demonstrates multiple approaches to managing AWS resources — from simple shell scripts, to SDK-based automation in Java and Python, to Infrastructure-as-Code (IaC) with CloudFormation.

The goal is to help developers and DevOps engineers quickly learn and apply AWS resource management patterns across different tools and languages.

---

## 📂 Repository Structure

### `s3-scripts/`

    - Bash scripts for **CRUD operations on S3 buckets**.
    - Useful for quick testing, automation, or learning AWS CLI basics.
    - Examples include creating, listing, updating, and deleting buckets.

### `SDK/`

    - **Java SDK project**: Demonstrates how to interact with AWS services programmatically using the AWS SDK for Java.
    - **Python SDK project**: Includes an `S3Manager` class for performing CRUD operations on S3 buckets with proper error handling (`ClientError` from `botocore`).

### `IAC/CFN/`

    - CloudFormation templates for provisioning AWS resources.
    - Example: `template.yaml` defines an S3 bucket stack.
    - Includes a `deploy` helper script to simplify stack deployment.

---

## 🚀 Significance

This repo is designed to:
    - Show **multiple approaches** to AWS resource management (CLI, SDKs, IaC).
    - Provide **ready-to-use examples** for learning and experimentation.
    - Serve as a **reference toolkit** for building production-ready AWS workflows.

By exploring each folder, you’ll see how the same AWS resource (like an S3 bucket) can be managed:
    - Directly via CLI commands.
    - Programmatically via SDKs in different languages.
    - Declaratively via CloudFormation templates.

---

## 🛠️ Getting Started

1. **Prerequisites**
   - AWS account and credentials configured (`aws configure`).
   - AWS CLI installed (`aws --version`).
   - For SDK projects: Java or Python runtime installed.

2. **Run Bash Scripts**

   ```bash
   cd s3-scripts
   ./create_bucket my-test-bucket
   ```
