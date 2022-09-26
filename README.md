# Install Guide

Follow these instructions carefully to setup a new environment from scratch.

## Prerequisities

Before heading to terraform, these setups need to be processed first.

- Setup Terraform Bucket
- Setup DynamoDB

#### Setup Bucket (Terraform State Storage)

Setup a sharable, centralized terraform state object store.

```sh
aws s3api create-bucket \
--bucket terraform-state-${ACCOUNT_ID}
```

Block all public access

```sh
aws s3api put-public-access-block \
--bucket ${NAME}-${ACCOUNT_ID}-terraform-state \
--public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

#### Setup DynamoDB Table (Terraform State Storage)

Setup a dynamodb table to handle lock states.

```sh
aws dynamodb create-table \
--attribute-definitions AttributeName=LockID,AttributeType=S \
--table-name terraform-state-lock \
--key-schema AttributeName=LockID,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```
---

### Terraform

##### Set terraform version to v1.1.9

```sh
tfenv install 1.1.9
tfenv use 1.1.9
```

##### Init Terraform

```
# change to env directory
cd environments/dev
```

```sh
terraform init
```

```sh
terraform apply
```