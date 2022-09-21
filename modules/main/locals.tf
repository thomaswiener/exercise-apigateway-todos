locals {
  bucket_storage = "storage-${var.env}-${data.aws_caller_identity.current.account_id}"

  endpoints = {
    list_todos = {
      description = "To-Do-API-Handler (Get all To-Do objects)"
      resource_id = aws_api_gateway_resource.todo_resource.id
      resource_path = aws_api_gateway_resource.todo_resource.path
      http_method = aws_api_gateway_method.list_todos.http_method
    }
    create_todo = {
      description = "To-Do-API-Handler (Update an existing To-Do object)"
      resource_id = aws_api_gateway_resource.todo_resource.id
      resource_path = aws_api_gateway_resource.todo_resource.path
      http_method = aws_api_gateway_method.create_todo.http_method
    }
    get_todo = {
      description = "To-Do-API-Handler (Get a single To-Do object)"
      resource_id = aws_api_gateway_resource.id_resource.id
      resource_path = aws_api_gateway_resource.id_resource.path
      http_method = aws_api_gateway_method.get_todo.http_method
    }
    update_todo = {
      description = "To-Do-API-Handler (Update an existing To-Do object)"
      resource_id = aws_api_gateway_resource.id_resource.id
      resource_path = aws_api_gateway_resource.id_resource.path
      http_method = aws_api_gateway_method.update_todo.http_method
    }
    delete_todo = {
      description = "To-Do-API-Handler (Delete an existing To-Do object)"
      resource_id = aws_api_gateway_resource.id_resource.id
      resource_path = aws_api_gateway_resource.id_resource.path
      http_method = aws_api_gateway_method.delete_todo.http_method
    }
  }
}
