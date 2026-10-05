# Terraform for Beginners

## Overview

Terraform is an **Infrastructure as Code (IaC)** tool that lets you create, manage, and update infrastructure using configuration files instead of manually configuring resources.

With Terraform, you can manage resources such as:

- Cloud servers
- Virtual networks
- Databases
- Storage buckets
- DNS records
- Kubernetes resources
- Many other services

This README provides a beginner-friendly introduction to Terraform and the basic workflow you need to get started.

## Prerequisites

Before starting, you should have:

- Basic command-line knowledge
- A text editor or IDE
- An account with a cloud provider if you want to create real infrastructure
- Terraform installed on your computer

## Installing Terraform

Download and install Terraform for your operating system from the official Terraform website.

After installation, verify it:

```bash
terraform version
```

You should see the installed Terraform version.

## How Terraform Works

Terraform configurations are usually written in files ending with `.tf`.

A simple Terraform workflow looks like this:

```text
Write configuration
       ↓
terraform init
       ↓
terraform plan
       ↓
terraform apply
       ↓
Infrastructure is created
```

Terraform keeps track of the infrastructure it manages using a **state file**.

## Your First Terraform Project

Create a directory for your project:

```bash
mkdir terraform-demo
cd terraform-demo
```

Create a file called `main.tf`:

```hcl
terraform {
  required_version = ">= 1.0"
}

resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello from Terraform!"
}
```

This example uses the local provider to create a text file on your computer.

## Terraform Commands

### 1. Initialize the project

Run:

```bash
terraform init
```

`terraform init` prepares your working directory and downloads the providers required by your configuration.

Run this command when you create a new Terraform project or add/change providers.

### 2. Format your code

Run:

```bash
terraform fmt
```

This automatically formats Terraform configuration files.

### 3. Validate your configuration

Run:

```bash
terraform validate
```

This checks whether your Terraform configuration is syntactically valid and internally consistent.

### 4. Preview changes

Run:

```bash
terraform plan
```

Terraform shows what it intends to create, change, or destroy.

**Always review the plan before applying changes**, especially when working with real cloud infrastructure.

### 5. Apply changes

Run:

```bash
terraform apply
```

Terraform will display the planned changes and ask you to confirm.

Type:

```text
yes
```

to apply the changes.

### 6. Destroy resources

When you no longer need the infrastructure, you can remove resources managed by the project:

```bash
terraform destroy
```

Be careful with this command because it can permanently delete infrastructure.

## Important Terraform Concepts

### Providers

A provider allows Terraform to communicate with an external platform or service.

For example:

```hcl
provider "aws" {
  region = "us-east-1"
}
```

Terraform has providers for many platforms and services.

### Resources

A resource represents something Terraform creates or manages.

Example:

```hcl
resource "local_file" "hello" {
  filename = "hello.txt"
  content  = "Hello Terraform!"
}
```

The general structure is:

```hcl
resource "TYPE" "NAME" {
  # configuration
}
```

### Variables

Variables allow you to make your Terraform configuration reusable.

Example:

```hcl
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
```

You can use a variable like this:

```hcl
resource "local_file" "example" {
  filename = "${var.environment}.txt"
  content  = "Terraform environment: ${var.environment}"
}
```

### Outputs

Outputs display useful information after Terraform creates resources.

Example:

```hcl
output "environment" {
  value = var.environment
}
```

Run:

```bash
terraform output
```

to view output values.

### State

Terraform uses a **state file** to keep track of the infrastructure it manages.

By default, Terraform stores state in:

```text
terraform.tfstate
```

**Do not casually commit Terraform state files to Git.** State can contain sensitive information depending on the resources being managed.

For team environments, use a suitable remote backend with state locking and access controls.

## Recommended Project Structure

As your project grows, you can organize it like this:

```text
terraform-project/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
├── terraform.tfvars
├── .gitignore
└── README.md
```

A simple `.gitignore` might include:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
*.tfplan
```

Review your organization's security requirements before deciding which files should be ignored or committed.

## Typical Workflow

For most Terraform projects, your daily workflow will look like:

```bash
terraform fmt
terraform init
terraform validate
terraform plan
terraform apply
```

When you need to remove the infrastructure:

```bash
terraform destroy
```

## Best Practices for Beginners

1. **Run `terraform plan` before `terraform apply`.**
2. **Use version control**, such as Git, for Terraform configuration.
3. **Do not commit secrets** to `.tf` files or variable files.
4. **Use variables** instead of hard-coding values that change between environments.
5. **Keep Terraform files organized** as your project grows.
6. **Use remote state** when working with a team.
7. **Pin provider and Terraform versions** for predictable deployments.
8. **Start with small projects** before managing production infrastructure.
9. **Review `terraform destroy` carefully** before confirming it.
10. **Learn the provider documentation** for the platform you are managing.

## Common Beginner Mistakes

### Running `apply` without checking the plan

Always understand what Terraform intends to change before approving it.

### Accidentally exposing secrets

Avoid putting passwords, API keys, or other credentials directly into Terraform configuration.

### Manually changing Terraform-managed resources

If Terraform manages a resource, make changes through Terraform whenever possible. Manual changes can cause configuration and state to become inconsistent.

### Ignoring state

Terraform state is an important part of how Terraform works. Protect it and use an appropriate backend for collaborative projects.

## Useful Commands Cheat Sheet

| Command | Purpose |
|---|---|
| `terraform init` | Initialize a Terraform project |
| `terraform fmt` | Format Terraform files |
| `terraform validate` | Validate configuration |
| `terraform plan` | Preview changes |
| `terraform apply` | Create/update infrastructure |
| `terraform destroy` | Delete managed infrastructure |
| `terraform show` | Display Terraform state/plan information |
| `terraform output` | Display output values |
| `terraform providers` | Show providers used by the configuration |
| `terraform version` | Show the installed Terraform version |

## Next Steps

Once you understand the basic workflow, learn these topics next:

1. Terraform variables and outputs
2. Providers
3. Resources
4. Data sources
5. Modules
6. State and remote backends
7. Workspaces and environments
8. Secrets management
9. Terraform in CI/CD
10. Infrastructure testing and security

## Conclusion

Terraform makes infrastructure repeatable, version-controlled, and easier to manage.

The most important beginner workflow to remember is:

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Start small, review every plan, protect your state and secrets, and gradually introduce modules and remote state as your projects become more complex.