# AWS Lambda Layer Builder

- [AWS Lambda Layer Builder](#aws-lambda-layer-builder)
  - [Purpose](#purpose)
  - [How To Use This Action](#how-to-use-this-action)
    - [Inputs](#inputs)
  - [Getting Started](#getting-started)
    - [Share to Specific Account](#share-to-specific-account)
    - [Share to All Accounts](#share-to-all-accounts)
    - [Share to an Organization](#share-to-an-organization)
  - [Resulting Layer Name](#resulting-layer-name)
  - [Layer Paths for each Lambda runtime](#layer-paths-for-each-lambda-runtime)
  - [Examples](#examples)


## Purpose

Lambda layers provide a convenient way to package libraries and other dependencies that you can use with your Lambda functions. Using layers reduces the size of uploaded deployment archives and makes it faster to deploy your code. Layers also promote code sharing and separation of responsibilities so that you can iterate faster on writing business logic.

A layer is a .zip file archive that can contain additional code or data. A layer can contain libraries, a custom runtime, data, or configuration files. Layers promote code sharing and separation of responsibilities so that you can iterate faster on writing business logic.

Created this action to save on all the extra code that is required in a GitHub Workflow to create and publish a layer.  This will do all the undifferentiated heavy lifting for you.


## How To Use This Action
Using this action requires you to add a block of code to your Github workflow.


### Inputs
| Name                 | Type   | Required | Description                                                                               |
| -------------------- | ------ | -------- | ----------------------------------------------------------------------------------------- |
| `layer-name`         | string | Yes      | SSM Parameter Name                                                                        |
| `layer-directory`    | string | Yes      | Working directory in repository where `requirements.txt` file exists                      |
| `runtime`            | string | Yes      | AWS Lambda Runtime.  Allowed Values: `python`, `node`                                     |
| `bucketname`         | string | Yes      | AWS S3 Bucket Name where layer will be uploaded                                           |
| `prefix-folder-path` | string | No       | (Optional) An optional prefix that will be used for a folder path inside the S3 bucket    |
| `principal`          | string | Yes      | An AWS Account ID to grant layer usage permissions to                                     |
| `organization-id`    | string | No       | An AWS Organization ID to grant layer usage permissions to. Principal must be "*" if this is set.                         |

## Getting Started

As as emample, suppose you want to create an AWS Lambda Layer for your lambda function.  You can see in the example below some sameple values and they can be shown in an example below for directory layout.

### Share to Specific Account
```yaml
    - name: Build and Create Layer
      uses: stephenbawks/aws-lambda-layer@v0.2.0
      with:
        layer-name: my-awesome-layer-name
        layer-directory: layer
        runtime: python
        bucketname: my-s3-bucket-name-goes-here
        prefix-folder-path: beta
        principal: "123456789101"
```

### Share to All Accounts

```yaml
    - name: Build and Create Layer
      uses: stephenbawks/aws-lambda-layer@v0.2.0
      with:
        layer-name: my-awesome-layer-name
        layer-directory: layer
        runtime: python
        bucketname: my-s3-bucket-name-goes-here
        prefix-folder-path: beta
        principal: "*"
```

### Share to an Organization

```yaml
    - name: Build and Create Layer
      uses: stephenbawks/aws-lambda-layer@v0.2.0
      with:
        layer-name: my-awesome-layer-name
        layer-directory: layer
        runtime: python
        bucketname: my-s3-bucket-name-goes-here
        prefix-folder-path: beta
        principal: "*"
        organization-id: "o-1234567890"
```

The `layer-name` can be whatever you want to call your layer.  This is unique to you of course and the layer name can contain only letters, numbers, hyphens, and underscores.

The `layer-directory` is more opinionated in its layout.  In this example, in the root of your repository you would have a directory that is called `layer` and under that directory it would contain your `requirements.txt` file with your dependencies you want to bundle up in the layer.  The action is also using this same directory as a working directory to download your requirements and then created the zip file that is used for the layer.  We want to keep it segmented so that its not pulling extra files/folders that accidently get added to your layer.

The `runtime` only accepts `node` and `python` at this time.  More to be added later.

The `bucketname` argument is the name of your S3 bucket where you want the layer to be uploaded to.

The variable `prefix-folder-path` is there to add an extra folder in the folder path where your layer is stored in your S3 bucket.  This variable is optional and not required but could be useful if you want to have different version of your layer stored in different locations.

The default path schema for the layer looks like the following:
* `s3://<bucketname>/<prefix-folder-path>/<layer-name>-<DATE>-<RANDOM_NUMBER>.zip`

And as an example would result in a path that looks like the following:
* `s3://my-s3-bucket-name-goes-here/beta/my-awesome-layer-name-29-12-2021-34522.zip`

The `principal` variable is the account number you want to share the layer with.  If you put "*" here that will share it to the world.

The `organization-id` grants permission to all accounts in the specified organization.  The `principal` needs to be set to `*`.

## Resulting Layer Name

The resulting layer name will look like the following.


arn:aws:lambda:`<AWS_REGION>`:`<AWS_ACCOUNT_ID>`:layer:`<layer-name>`-`<mm-dd-yyy>`:`<layer_version>`


## Layer Paths for each Lambda runtime
For each Lambda runtime, the PATH variable includes specific folders in the /opt directory. If you define the same folder structure in your layer .zip file archive, your function code can access the layer content without the need to specify the path.

The following table lists the folder paths that each runtime supports and the directory the action will be creating and installing your requirements under.

| Runtime              | Path                  |
| -------------------- | --------------------- |
| `node`               | `nodejs/node_modules` |
| `python`             | `python`              |

## Examples

There is also some example requirements file as well as a Github Workflow file you can check out here to get yourself started quickly.

| Example                 | Link                                                    |
| ----------------------- | ------------------------------------------------------- |
| Github Workflow         | [Link](./example/workflow/example-worfklow.yml)         |
| Node Requirements       | [Link](./example/requirements/node-requirements.txt)    |
| Python Requirements     | [Link](./example/requirements/python-requirements.txt)  |
