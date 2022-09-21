resource "aws_iam_user" "readonly" {
  name = "ReadOnly"
}

resource "aws_iam_user_policy_attachment" "attachment" {
  user        = aws_iam_user.readonly.name
  policy_arn  = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}