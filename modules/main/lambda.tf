resource "aws_lambda_permission" "apigw_lambda" {
  for_each      = local.endpoints
  statement_id  = "AllowExecutionFromAPIGateway-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = lookup(lookup(aws_lambda_function.function, each.key), "function_name")
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${data.aws_region.current.id}:${data.aws_caller_identity.current.id}:${aws_api_gateway_rest_api.rest_api.id}/*/${each.value.http_method}/v1"
}

data "archive_file" "file" {
  for_each      = local.endpoints
  type        = "zip"
  source_dir  = "${path.module}/functions/${each.key}/src"
  output_path = "${path.module}/functions/${each.key}.zip"
}

resource "aws_lambda_function" "function" {
  for_each         = local.endpoints
  function_name    = replace(each.key, "_", "-")
  description      = each.value.description
  filename         = lookup(lookup(data.archive_file.file, each.key), "output_path")
  source_code_hash = filebase64sha256(lookup(lookup(data.archive_file.file, each.key), "output_path"))
  handler          = "${each.key}.lambda_handler"
  runtime          = "python3.9"
  role             = aws_iam_role.lambda_basic.arn
  memory_size      = 128
  timeout          = 30
  publish          = true
  environment {
    variables = {
      BUCKET_STORAGE = aws_s3_bucket.storage.id
    }
  }
}

resource "aws_cloudwatch_log_group" "function" {
  for_each          = local.endpoints
  name              = "/aws/lambda/${lookup(lookup(aws_lambda_function.function, each.key), "function_name")}"
  retention_in_days = 1
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
      "lambda:*"
      #"lambda:invokeFunction"
    ]
    resources = [
      "*"
    ]
  }
}

resource "aws_iam_role" "lambda_basic" {
  name               = "lambda-basic"
  assume_role_policy = data.aws_iam_policy_document.lambda_basic.json
}

data "aws_iam_policy_document" "lambda_basic" {
  statement {
    effect = "Allow"
    principals {
      identifiers = [
        "lambda.amazonaws.com"
      ]
      type = "Service"
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role_policy_attachment" "attachment" {
  role        = aws_iam_role.lambda_basic.name
  policy_arn  = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_policy_attachment" {
  role   = aws_iam_role.lambda_basic.name
  policy = data.aws_iam_policy_document.lambda_policy_document.json
}

data "aws_iam_policy_document" "lambda_policy_document" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
      "s3:DeleteObject",
      "s3:PutObject",
    ]
    resources = [
      aws_s3_bucket.storage.arn,
      "${aws_s3_bucket.storage.arn}/*"
    ]
  }
}