resource "aws_api_gateway_rest_api" "rest_api" {
  name = "rest-api"
  description = "An API that meets the requirements"
  binary_media_types = ["*/*"]
}

# tfsec:ignore:aws-api-gateway-enable-tracing
resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.rest_api.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  stage_name    = "dev"
  access_log_settings {
    destination_arn = "arn:aws:logs:eu-central-1:643355622722:log-group:apigateway"
    format          = "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] \"$context.httpMethod $context.resourcePath $context.protocol\" $context.status $context.responseLength $context.requestId $context.integrationErrorMessage"
  }
}

resource "aws_api_gateway_deployment" "rest_api" {
  depends_on = [
    aws_api_gateway_method.list_todos,
    aws_api_gateway_method.list_todos,
    aws_api_gateway_method.create_todo,
    aws_api_gateway_method.get_todo,
    aws_api_gateway_method.update_todo,
    aws_api_gateway_method.delete_todo,
    aws_api_gateway_integration.integration,
    aws_lambda_function.function,
    aws_iam_role_policy.attachment
  ]
  rest_api_id = aws_api_gateway_rest_api.rest_api.id

  triggers = {
    # NOTE: The configuration below will satisfy ordering considerations,
    #       but not pick up all future REST API changes. More advanced patterns
    #       are possible, such as using the filesha1() function against the
    #       Terraform configuration file(s) or removing the .id references to
    #       calculate a hash against whole resources. Be aware that using whole
    #       resources will show a difference after the initial implementation.
    #       It will stabilize to only change when resources change afterwards.
    redeployment = sha1(jsonencode(concat([
      aws_api_gateway_resource.version_resource.id,
      aws_api_gateway_resource.todo_resource.id,
      aws_api_gateway_resource.id_resource.id,
      aws_api_gateway_method.list_todos.id,
      aws_api_gateway_method.create_todo.id,
      aws_api_gateway_method.get_todo.id,
      aws_api_gateway_method.update_todo.id,
      aws_api_gateway_method.delete_todo.id,
      aws_iam_role_policy.attachment.id
    ],
      [for v in aws_api_gateway_integration.integration: v["id"]],
      [for v in aws_lambda_function.function: v["id"]],
    )))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_resource" "version_resource" {
  path_part   = "v1"
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
}

resource "aws_api_gateway_resource" "todo_resource" {
  path_part   = "todo"
  parent_id   = aws_api_gateway_resource.version_resource.id
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
}

resource "aws_api_gateway_resource" "id_resource" {
  path_part   = "{id}"
  parent_id   = aws_api_gateway_resource.todo_resource.id
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
}

# tfsec:ignore:aws-api-gateway-no-public-access
resource "aws_api_gateway_method" "list_todos" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.todo_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# tfsec:ignore:aws-api-gateway-no-public-access
resource "aws_api_gateway_method" "update_todo" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.todo_resource.id
  http_method   = "PUT"
  authorization = "NONE"
}

# tfsec:ignore:aws-api-gateway-no-public-access
resource "aws_api_gateway_method" "get_todo" {
  rest_api_id        = aws_api_gateway_rest_api.rest_api.id
  resource_id        = aws_api_gateway_resource.id_resource.id
  http_method        = "GET"
  authorization      = "NONE"
  request_parameters = {
    "method.request.path.id" = true
  }
}

# tfsec:ignore:aws-api-gateway-no-public-access
resource "aws_api_gateway_method" "create_todo" {
  rest_api_id        = aws_api_gateway_rest_api.rest_api.id
  resource_id        = aws_api_gateway_resource.id_resource.id
  http_method        = "PUT"
  authorization      = "NONE"
  request_parameters = {
    "method.request.path.id" = true
  }
}

# tfsec:ignore:aws-api-gateway-no-public-access
resource "aws_api_gateway_method" "delete_todo" {
  rest_api_id        = aws_api_gateway_rest_api.rest_api.id
  resource_id        = aws_api_gateway_resource.id_resource.id
  http_method        = "DELETE"
  authorization      = "NONE"
  request_parameters = {
    "method.request.path.id" = true
  }
}

resource "aws_api_gateway_integration" "integration" {
  for_each                = local.endpoints
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = each.value.resource_id
  http_method             = each.value.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  credentials             = aws_iam_role.apigateway_execution.arn
  uri                     = lookup(lookup(aws_lambda_function.function, each.key), "qualified_invoke_arn")
}

resource "aws_iam_role" "apigateway_execution" {
  name               = "apigateway-execution"
  assume_role_policy = data.aws_iam_policy_document.apigateway_execution.json
}

data "aws_iam_policy_document" "apigateway_execution" {
  statement {
    effect = "Allow"
    principals {
      identifiers = [
        "apigateway.amazonaws.com",
        "lambda.amazonaws.com"
      ]
      type = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy" "attachment" {
  role   = aws_iam_role.apigateway_execution.name
  policy = data.aws_iam_policy_document.document.json
}

data "aws_iam_policy_document" "document" {
  statement {
    effect = "Allow"
    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [for v in aws_lambda_function.function: v["qualified_arn"]]
  }
}
